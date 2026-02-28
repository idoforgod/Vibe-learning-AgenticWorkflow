# Socratic AI Tutor — Hook & State Management Implementation

[trace:step-8:command-spec] [trace:step-5:phase0-flow] [trace:step-2:mcp-fallbacks]

This document defines the complete infrastructure layer for the Socratic AI Tutor system:
session state management hooks, SOT write protection, session logging and recovery,
MCP server configuration with fallbacks, and state management utilities.

---

## 1. Hook Configuration

The Socratic Tutor system extends the parent AgenticWorkflow's hook infrastructure
with three additional hooks specific to the tutoring domain. These are added to the
parent project's `.claude/settings.json` alongside existing hooks.

### 1.1 Settings.json Hook Entries

The following hook entries are added to `.claude/settings.json` in addition to the
existing parent hooks (context preservation, safety, predictive debugging).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if test -f \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/guard_learner_state.py; then python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/guard_learner_state.py; fi",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|Bash|Task",
        "hooks": [
          {
            "type": "command",
            "command": "if test -f \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/track_session_activity.py; then python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/track_session_activity.py; fi",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if test -f \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/save_session_snapshot.py; then python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/save_session_snapshot.py; fi",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

**Integration note**: These entries MERGE into the existing settings.json. The parent
hooks (context_guard.py, block_destructive_commands.py, etc.) continue to operate
independently. Claude Code processes multiple hook entries per event type sequentially.

---

### 1.2 Hook Script: `guard_learner_state.py` (PreToolUse — SOT Write Protection)

**Purpose**: Prevent any agent except @orchestrator from writing to SOT files
(`state.yaml`, `learner-state.yaml`) in the `data/socratic/` directory.

**Mechanism**: Reads `$CLAUDE_TOOL_INPUT` (the file path being edited/written).
If the target file is a SOT file, checks whether the current context indicates
orchestrator-level execution. Sub-agents dispatched via Task tool do NOT have
orchestrator privileges.

```python
#!/usr/bin/env python3
"""Guard learner-state.yaml and state.yaml from unauthorized writes.

Hook type: PreToolUse (matcher: Edit|Write)
Exit codes:
  0 — allow (target is not a SOT file, or orchestrator context detected)
  2 — block (SOT file targeted by non-orchestrator context)

Environment:
  CLAUDE_TOOL_INPUT — JSON with file_path (Edit) or file_path (Write)
  CLAUDE_PROJECT_DIR — project root
"""

import json
import os
import sys

# SOT files that only @orchestrator may write
SOT_FILES = {
    "state.yaml",
    "learner-state.yaml",
}

# SOT directory prefix (relative to project root)
SOT_DIR = os.path.join("data", "socratic")


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    tool_input_raw = os.environ.get("CLAUDE_TOOL_INPUT", "{}")

    try:
        tool_input = json.loads(tool_input_raw)
    except json.JSONDecodeError:
        # Cannot parse input — allow (fail open)
        sys.exit(0)

    # Extract file path from Edit or Write tool input
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Normalize to relative path
    if project_dir and file_path.startswith(project_dir):
        rel_path = file_path[len(project_dir):].lstrip(os.sep)
    else:
        rel_path = file_path

    # Check if target is in the SOT directory
    if not rel_path.startswith(SOT_DIR):
        sys.exit(0)

    # Check if target filename is a protected SOT file
    basename = os.path.basename(rel_path)
    if basename not in SOT_FILES:
        sys.exit(0)

    # Target IS a protected SOT file
    # In Claude Code, sub-agents run via Task tool in isolated contexts.
    # The CLAUDE_IS_SUBAGENT environment variable (or similar mechanism)
    # indicates sub-agent execution. If not available, we check for
    # the Task tool's sub-agent marker in the transcript.
    #
    # Practical implementation: Claude Code does not expose a reliable
    # sub-agent detection env var. The protection is enforced via:
    # 1. Agent prompt instructions (all 17 agents state "READ-ONLY access to SOT")
    # 2. This hook as a deterministic safety net — it outputs a WARNING
    #    to stderr so the LLM self-corrects, rather than hard-blocking
    #    (since orchestrator context cannot be reliably distinguished
    #    from sub-agent context at the hook level).
    #
    # Design decision: WARNING mode (exit 0 + stderr) rather than
    # hard block (exit 2) because the orchestrator itself needs to write
    # to these files. The hook serves as a REMINDER mechanism.

    sys.stderr.write(
        f"WARNING: Writing to SOT file '{basename}' in {SOT_DIR}/. "
        f"ONLY @orchestrator should write to SOT files. "
        f"Sub-agents must write to their own output files and signal @orchestrator. "
        f"If you are a sub-agent, STOP and return your output via Task result instead.\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
```

**Key design choice**: Exit code 0 (warning) instead of exit code 2 (block) because
Claude Code cannot reliably distinguish orchestrator context from sub-agent context
at the hook level. The warning serves as a self-correction prompt for the LLM.

---

### 1.3 Hook Script: `track_session_activity.py` (PostToolUse — Session Activity Tracking)

**Purpose**: Track session activity during active tutoring sessions. Updates the
session log with interaction timestamps for timeout detection and activity monitoring.

```python
#!/usr/bin/env python3
"""Track session activity during active tutoring sessions.

Hook type: PostToolUse (matcher: Edit|Write|Bash|Task)
Exit code: always 0 (logging-only hook, never blocks)

Environment:
  CLAUDE_PROJECT_DIR — project root
  CLAUDE_TOOL_NAME — name of the tool that was used
"""

import json
import os
import sys
import time

SOCRATIC_DIR = os.path.join("data", "socratic")
LEARNER_STATE = "learner-state.yaml"
ACTIVITY_LOG = os.path.join("sessions", "active", ".activity-tracker.json")


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "unknown")

    socratic_path = os.path.join(project_dir, SOCRATIC_DIR)
    learner_state_path = os.path.join(socratic_path, LEARNER_STATE)

    # Only track if a learner state exists (tutoring system is initialized)
    if not os.path.isfile(learner_state_path):
        sys.exit(0)

    # Quick check: is there an active session?
    # Read learner-state.yaml minimally (just check for session_id)
    try:
        with open(learner_state_path, "r") as f:
            content = f.read()
        # Simple check: if "session_id: null" or no session_id, skip
        if "session_id: null" in content or "status: null" in content:
            sys.exit(0)
        # Check for active status
        if "status: active" not in content and "status: \"active\"" not in content:
            sys.exit(0)
    except (OSError, IOError):
        sys.exit(0)

    # Session is active — log activity
    activity_path = os.path.join(socratic_path, ACTIVITY_LOG)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    activity_entry = {
        "timestamp": timestamp,
        "tool": tool_name,
        "epoch": int(time.time()),
    }

    # Read existing activity log (append mode)
    activities = []
    if os.path.isfile(activity_path):
        try:
            with open(activity_path, "r") as f:
                activities = json.load(f)
            if not isinstance(activities, list):
                activities = []
        except (json.JSONDecodeError, OSError):
            activities = []

    activities.append(activity_entry)

    # Keep only last 100 entries to prevent unbounded growth
    if len(activities) > 100:
        activities = activities[-100:]

    # Write atomically
    tmp_path = activity_path + ".tmp"
    try:
        os.makedirs(os.path.dirname(activity_path), exist_ok=True)
        with open(tmp_path, "w") as f:
            json.dump(activities, f, indent=2)
        os.replace(tmp_path, activity_path)
    except (OSError, IOError):
        # Logging failure is non-fatal
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

### 1.4 Hook Script: `save_session_snapshot.py` (Stop — Emergency Session Snapshot)

**Purpose**: On every response completion (Stop event), if there is an active tutoring
session, save a snapshot of the current session state to enable recovery via `/resume`.

```python
#!/usr/bin/env python3
"""Save session snapshot on Stop event for recovery.

Hook type: Stop
Exit code: always 0 (snapshot-only hook, never blocks)

This implements the session recovery infrastructure by saving a snapshot
of the current session state to data/socratic/sessions/snapshots/.
If the session is interrupted (context overflow, API error, user closes),
the latest snapshot enables recovery via /resume.

Environment:
  CLAUDE_PROJECT_DIR — project root
"""

import json
import os
import sys
import time

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

SOCRATIC_DIR = os.path.join("data", "socratic")
LEARNER_STATE = "learner-state.yaml"
SNAPSHOTS_DIR = os.path.join("sessions", "snapshots")


def parse_yaml_simple(content):
    """Minimal YAML parser for flat key-value extraction when PyYAML unavailable."""
    result = {}
    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " in line:
            key, _, value = line.partition(": ")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value == "null":
                value = None
            result[key] = value
    return result


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    socratic_path = os.path.join(project_dir, SOCRATIC_DIR)
    learner_state_path = os.path.join(socratic_path, LEARNER_STATE)

    # Only save snapshot if learner state exists
    if not os.path.isfile(learner_state_path):
        sys.exit(0)

    try:
        with open(learner_state_path, "r") as f:
            content = f.read()
    except (OSError, IOError):
        sys.exit(0)

    # Parse learner state
    if HAS_YAML:
        try:
            learner_state = yaml.safe_load(content)
        except yaml.YAMLError:
            learner_state = parse_yaml_simple(content)
    else:
        learner_state = parse_yaml_simple(content)

    if not isinstance(learner_state, dict):
        sys.exit(0)

    # Check for active session
    current_session = learner_state.get("current_session", {})
    if not isinstance(current_session, dict):
        sys.exit(0)

    session_id = current_session.get("session_id")
    status = current_session.get("status")

    if not session_id or status not in ("active", "paused"):
        sys.exit(0)

    # Build snapshot
    timestamp = int(time.time())
    iso_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    snapshot = {
        "session_id": session_id,
        "snapshot_timestamp": iso_time,
        "snapshot_epoch": timestamp,
        "current_session": current_session,
        "knowledge_state": learner_state.get("knowledge_state", {}),
        "path": learner_state.get("path", {}),
        "response_pattern": learner_state.get("response_pattern", {}),
        "history": learner_state.get("history", {}),
        "recovery_metadata": {
            "pending_question": current_session.get("pending_question"),
            "current_phase": current_session.get("current_phase"),
            "current_module": current_session.get("current_module"),
            "current_lesson": current_session.get("current_lesson"),
            "lesson_progress_pct": current_session.get("lesson_progress_pct", 0),
            "question_level": current_session.get("question_level", 1),
            "socratic_depth_reached": current_session.get("socratic_depth_reached", 1),
        },
    }

    # Save snapshot
    snapshot_dir = os.path.join(socratic_path, SNAPSHOTS_DIR)
    os.makedirs(snapshot_dir, exist_ok=True)
    snapshot_filename = f"{session_id}_{timestamp}.json"
    snapshot_path = os.path.join(snapshot_dir, snapshot_filename)

    tmp_path = snapshot_path + ".tmp"
    try:
        with open(tmp_path, "w") as f:
            json.dump(snapshot, f, indent=2)
        os.replace(tmp_path, snapshot_path)
    except (OSError, IOError):
        # Snapshot failure is non-fatal — session continues
        pass

    # Prune old snapshots (keep last 20 for this session)
    try:
        all_snapshots = sorted(
            [f for f in os.listdir(snapshot_dir) if f.startswith(session_id)],
            reverse=True
        )
        for old_snapshot in all_snapshots[20:]:
            try:
                os.remove(os.path.join(snapshot_dir, old_snapshot))
            except OSError:
                pass
    except OSError:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## 2. SOT Write Protection

### 2.1 Protection Layers

The Socratic Tutor system implements SOT write protection through three layers:

| Layer | Mechanism | Scope | Enforcement |
|-------|-----------|-------|-------------|
| **L1: Agent Prompt** | All 17 agent `.md` files state "READ-ONLY access to SOT" | All agents | Behavioral (LLM follows instructions) |
| **L2: Hook Warning** | `guard_learner_state.py` outputs stderr warning on SOT write attempts | PreToolUse (Edit\|Write) | Deterministic warning + LLM self-correction |
| **L3: Parent Hook** | `block_destructive_commands.py` already guards against destructive operations | PreToolUse (Bash) | Deterministic block (exit 2) |

### 2.2 Protected Files

| File | Location | Writer | Protection Level |
|------|----------|--------|-----------------|
| `state.yaml` | `data/socratic/state.yaml` | @orchestrator ONLY | L1 + L2 |
| `learner-state.yaml` | `data/socratic/learner-state.yaml` | @orchestrator ONLY | L1 + L2 |

### 2.3 Allowed Writers

Only the `@orchestrator` (running in main context) may write to SOT files.
The write pattern is:

```
Agent completes task → writes output file → returns to orchestrator
Orchestrator: validates output → reads output → updates SOT atomically
```

This pattern applies to both Phase 0 (state.yaml) and Phase 1-3 (learner-state.yaml).

---

## 3. @session-logger Background Mechanism

### 3.1 Design Context

[trace:step-5:phase0-flow]

The architecture blueprint (Section 8.12) notes that Claude Code does not support
true background polling. The "5-second auto-snapshot" is a design aspiration.

**Practical implementation**: Two complementary mechanisms provide session state
persistence:

1. **Stop Hook (Primary)**: The `save_session_snapshot.py` Stop hook runs after EVERY
   orchestrator response. Since tutoring sessions involve turn-by-turn dialogue, this
   creates a snapshot every 15-30 seconds (matching actual interaction frequency).

2. **Orchestrator Inline (Secondary)**: After every learner interaction, the @orchestrator
   (running as @socratic-tutor in main context) explicitly saves the session state by
   updating `learner-state.yaml.current_session` fields. This is the "active write"
   that complements the Stop hook's "passive save."

### 3.2 Snapshot Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Snapshot location** | `data/socratic/sessions/snapshots/` | Separate from active session logs |
| **Filename pattern** | `{session_id}_{unix_epoch}.json` | Enables chronological sorting and session filtering |
| **Max snapshots per session** | 20 | Prevents disk bloat; oldest pruned automatically |
| **Snapshot content** | See Section 3.3 | Full session state for recovery |
| **Write method** | Atomic (tmp + rename) | Prevents corrupted snapshots on crash |

### 3.3 Snapshot Schema

```json
{
  "session_id": "SES_20260227_a3f7b2",
  "snapshot_timestamp": "2026-02-27T10:45:00Z",
  "snapshot_epoch": 1772150700,
  "current_session": {
    "session_id": "SES_20260227_a3f7b2",
    "status": "active",
    "started_at": "2026-02-27T10:00:00Z",
    "current_module": "module_001",
    "current_lesson": "lesson_003",
    "current_phase": "deep_dive",
    "question_level": 2,
    "lesson_progress_pct": 45,
    "pending_question": "If a miner has 51% of the network's computing power, how could they exploit the consensus mechanism?",
    "metacog_checkpoints_hit": [15],
    "misconceptions_this_session": 1,
    "socratic_depth_reached": 2
  },
  "knowledge_state": {
    "concept_001": {
      "mastery": 0.65,
      "confidence": 0.70,
      "last_assessed": "2026-02-27T10:40:00Z",
      "assessment_count": 4,
      "transfer_validated": false
    }
  },
  "path": {
    "current_position": "concept_003",
    "next_concepts": [],
    "review_schedule": []
  },
  "response_pattern": {
    "avg_response_time_seconds": 28.5,
    "confidence_accuracy_gap": 0.12,
    "common_error_types": ["overgeneralization"]
  },
  "history": {
    "total_sessions": 2,
    "total_study_time_minutes": 75
  },
  "recovery_metadata": {
    "pending_question": "If a miner has 51% of the network's computing power...",
    "current_phase": "deep_dive",
    "current_module": "module_001",
    "current_lesson": "lesson_003",
    "lesson_progress_pct": 45,
    "question_level": 2,
    "socratic_depth_reached": 2
  }
}
```

### 3.4 Session Log Format (S13-aligned)

The session log (`data/socratic/sessions/active/{session_id}.log.json`) records
the full session state per canonical schema S13. Key structure:

```json
{
  "session_id": "SES_20260227_a3f7b2",
  "learner_id": "LRN_20260227_x1y2z3",
  "started_at": "2026-02-27T10:00:00Z",
  "ended_at": null,
  "session_plan_ref": "data/socratic/planning/session-plan.json",
  "learning_path_ref": "data/socratic/planning/learning-path.json",
  "status": "active",
  "current_state": {
    "module_id": "M1",
    "lesson_id": "L1.1",
    "lesson_title": "Introduction to Decentralized Systems",
    "current_phase": "warm_up",
    "current_question_level": 1,
    "lesson_progress_pct": 15,
    "awaiting_response": true,
    "pending_question": "What do you already know about decentralized systems?",
    "last_ai_message": "Let's start with what you know...",
    "last_user_response": null,
    "dialogue_history_summary": "Session just started, warm-up phase"
  },
  "recovery_checkpoint": {
    "checkpoint_id": "CP_20260227_100030",
    "recoverable": true,
    "resume_instruction": "L1.1 (Introduction to Decentralized Systems) - warm_up phase, Level 1 question pending"
  },
  "events": [
    {
      "timestamp": "2026-02-27T10:00:30Z",
      "type": "question_asked",
      "data": {
        "level": 1,
        "concept_id": "concept_001",
        "question": "What do you already know about decentralized systems?"
      }
    },
    {
      "timestamp": "2026-02-27T10:01:15Z",
      "type": "response_received",
      "data": {
        "concept_id": "concept_001",
        "response_classification": "partial",
        "mastery_update": { "old": 0.0, "new": 0.3 },
        "misconception_detected": null
      }
    }
  ],
  "stats": {
    "total_questions_asked": 1,
    "questions_by_level": {"L1": 1, "L2": 0, "L3": 0},
    "misconceptions_detected": 0,
    "misconceptions_corrected": 0,
    "metacog_checkpoints_completed": 0,
    "mastery_updates": [{"concept_id": "concept_001", "old": 0.0, "new": 0.3}],
    "total_duration_seconds": 75
  }
}
```

---

## 4. Session Recovery Infrastructure

### 4.1 Session Lifecycle

```
Session created → ACTIVE → (normal end) → COMPLETED
                       ↘ (unexpected termination) → INTERRUPTED
                                                        ↓
                                              /resume → ACTIVE (restored)
```

### 4.2 Interruption Detection

An active session moves to INTERRUPTED status when:

1. **Context overflow**: Claude Code compacts context. The Stop hook saves a final
   snapshot before compaction. On SessionStart (after compact), the orchestrator
   checks if a session was active and moves it to `interrupted/`.

2. **API timeout**: The session is not explicitly ended. The Stop hook's last snapshot
   is the recovery point.

3. **User closes terminal**: Same as API timeout — the last Stop hook snapshot
   is used.

4. **Learner inactivity (>5 min)**: The orchestrator detects >5 minutes since last
   response via the activity tracker. It saves a snapshot and moves the session to
   `interrupted/`.

### 4.3 Interruption Handling (Orchestrator Responsibility)

When @orchestrator detects a session should be interrupted:

```python
# Pseudocode for session interruption handling
1. Update learner-state.yaml: current_session.status = "interrupted"
2. Save final snapshot to sessions/snapshots/
3. Move session log: sessions/active/{id}.log.json → sessions/interrupted/{id}.log.json
4. Log interruption event with timestamp and reason
```

### 4.4 Recovery Scan Logic (/resume command)

The `/resume` command scans `data/socratic/sessions/interrupted/` for recoverable sessions:

```python
# Pseudocode for recovery scan
1. List all *.log.json files in sessions/interrupted/
2. For each file:
   a. Extract session_id from filename
   b. Read session metadata (topic, last_active timestamp)
   c. Find latest snapshot in sessions/snapshots/ matching session_id
   d. Calculate age (days since interruption)
3. Sort by age (most recent first)
4. Apply warnings:
   - Age > 30 days: mastery decay warning
   - No matching snapshot: degraded recovery warning
5. Return list for user selection (or auto-select if only one)
```

### 4.5 Context Restoration

When a session is selected for resumption:

```
1. Load session log from sessions/interrupted/{session_id}.log.json
2. Load latest snapshot from sessions/snapshots/{session_id}_*.json (highest epoch)
3. Restore learner-state.yaml:
   a. Set current_session fields from snapshot.current_session
   b. Set current_session.status = "active"
   c. Merge knowledge_state from snapshot (preserving any updates)
   d. Restore path.current_position and path.next_concepts
4. Move session log: sessions/interrupted/ → sessions/active/
5. Inject conversation context:
   a. Extract last 5-10 events from session log events array
   b. Extract dialogue_history_summary from session log current_state
   c. Format as context summary for @socratic-tutor
6. Resume with pending_question from session log current_state (or snapshot.recovery_metadata)
7. Display recovery summary box
```

### 4.6 Recovery Fidelity

| Data Point | Source | Fidelity |
|-----------|--------|----------|
| Pending question | `snapshot.recovery_metadata.pending_question` | Exact |
| Session phase | `snapshot.recovery_metadata.current_phase` | Exact |
| Module/Lesson position | `snapshot.recovery_metadata.current_module/lesson` | Exact |
| Mastery scores | `snapshot.knowledge_state` | Within 1 interaction |
| Conversation context | Session log (last 5-10 events + current_state.dialogue_history_summary) | Summary, not verbatim |
| Question level distribution | `snapshot.current_session.question_level` | Exact |

**Recovery gap**: Conversation context is summarized from the session log, not the
full LLM context window. Some nuance from the original dialogue flow may be lost.
This is acceptable per the architecture blueprint's design intent.

---

## 5. Mastery State Persistence

### 5.1 Persistence Model

`learner-state.yaml` persists across sessions as a file on disk. It is never
deleted — only updated by @orchestrator. The persistence lifecycle:

```
/teach → state.yaml created (Phase 0 SOT)
/start-learning → learner-state.yaml.current_session initialized
                  learner-state.yaml.curriculum_ref set
During tutoring → knowledge_state updated (mastery, confidence per concept)
/end-session → current_session = null
               history.total_sessions += 1
               history.sessions[] += session summary
Next /start-learning → reads existing learner-state.yaml (returning learner path)
```

### 5.2 Cross-Session Mastery Tracking

| Field | Persistence | Update Frequency |
|-------|-------------|-----------------|
| `knowledge_state.{concept}.mastery` | Permanent | Every assessment (triangulation formula) |
| `knowledge_state.{concept}.transfer_validated` | Permanent | On /challenge PASS |
| `knowledge_state.{concept}.misconceptions_history` | Permanent | On misconception detection |
| `path.review_schedule` | Updated per session | @path-optimizer at session start |
| `history.total_sessions` | Incremented | On /end-session |
| `bloom_calibration.estimated_current_effect` | Computed | After >= 3 sessions |

### 5.3 Mastery Decay (Spaced Repetition)

When a learner returns after time away, @path-optimizer applies Ebbinghaus-based
decay to mastery scores:

```
effective_mastery = mastery * decay_factor
decay_factor = max(0.3, 1.0 - (days_since_review * 0.02))
```

This ensures mastery scores reflect actual retention, not just session performance.

---

## 6. MCP Server Configuration & Fallbacks

### 6.1 MCP Decision Summary

[trace:step-2:mcp-fallbacks]

Per the Tech Feasibility Report (Step 2), all 7 named MCP servers in the original
design are design-time inventions. The following table shows the concrete replacements:

| Original MCP | Status | Replacement | Configuration |
|-------------|--------|-------------|---------------|
| `web-search-mcp` | Does not exist | Built-in WebSearch tool | No configuration needed |
| `deep-research-mcp` | Does not exist | WebSearch + WebFetch iterative pattern | No configuration needed |
| `scholar-search-mcp` | Does not exist | Semantic Scholar API + arXiv API via Bash | API endpoints in agent prompts |
| `mooc-connector-mcp` | Does not exist | WebSearch + WebFetch for public course pages | Metadata only (no content API) |
| `adaptive-test-mcp` | Does not exist | LLM-internal in @learner-profiler | Agent prompt design |
| `graph-renderer-mcp` | Does not exist | Mermaid inline text in Claude Code output | No configuration needed |
| `analytics-mcp` | Does not exist | File-based computation in @progress-tracker | Agent reads session files directly |

### 6.2 Available Built-in Tools (No MCP Required)

These tools are available natively in Claude Code and require no MCP configuration:

| Tool | Used By | Purpose |
|------|---------|---------|
| `WebSearch` | @web-searcher, @deep-researcher, @knowledge-researcher | Web search for content discovery |
| `WebFetch` | @deep-researcher, @knowledge-researcher | Fetch and process web page content |
| `Read` | All agents | Read files from disk |
| `Write` | @content-analyzer, @topic-scout, @curriculum-architect, etc. | Write output files |
| `Bash` | @deep-researcher (API calls), @content-analyzer (file ops) | Execute shell commands |
| `Glob` | @content-analyzer (file scanning) | Find files by pattern |
| `Grep` | @content-analyzer (content search) | Search file contents |

### 6.3 Optional MCP Enhancements

These MCP servers can be configured for enhanced capabilities but are NOT required:

#### 6.3.1 Brave Search API (Optional)

**Package**: `@modelcontextprotocol/server-brave-search`
**Purpose**: Higher-quality web search results for @web-searcher
**Setup**:
```json
// .mcp.json (if user wants enhanced search)
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "<user-provided>"
      }
    }
  }
}
```
**Fallback**: Built-in WebSearch (no API key needed, always available)

#### 6.3.2 Perplexity Deep Research (Optional)

**Package**: `perplexityai/modelcontextprotocol` (official)
**Purpose**: Deep academic research for `--depth=deep` mode
**Setup**:
```json
// .mcp.json (if user wants deep research enhancement)
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@anthropic/perplexity-mcp"],
      "env": {
        "PERPLEXITY_API_KEY": "<user-provided>"
      }
    }
  }
}
```
**Fallback**: Multi-step WebSearch + WebFetch iterative pattern (no API key needed)

#### 6.3.3 Mermaid Diagram Export (Optional)

**Package**: `peng-shawn/mermaid-mcp-server`
**Purpose**: Export concept maps as PNG/SVG image files
**Setup**:
```json
// .mcp.json (if user wants PNG export of concept maps)
{
  "mcpServers": {
    "mermaid": {
      "command": "npx",
      "args": ["-y", "mermaid-mcp-server"]
    }
  }
}
```
**Fallback**: Mermaid text diagrams rendered inline by Claude Code (always available)

### 6.4 Scholarly Search Implementation

For @deep-researcher with `--depth=deep` or @knowledge-researcher:

**Semantic Scholar API** (free, no key required for basic use):
```bash
# Search for papers
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=blockchain+consensus&limit=10&fields=title,abstract,year,citationCount,url"

# Get paper details
curl -s "https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,references"
```

**arXiv API** (free, no key required):
```bash
# Search arXiv
curl -s "http://export.arxiv.org/api/query?search_query=all:blockchain+consensus&max_results=10"
```

These API calls are made via Bash tool by the relevant agents. No MCP server needed.

### 6.5 Fallback Decision Matrix

| Capability | Primary Method | Fallback Method | Degradation |
|-----------|---------------|-----------------|-------------|
| Web search | WebSearch (built-in) | Brave Search MCP | None (built-in is sufficient) |
| Deep research | WebSearch + WebFetch loops | Perplexity MCP | Reduced depth without Perplexity |
| Academic search | Semantic Scholar + arXiv APIs | WebSearch with academic filters | Fewer structured results |
| MOOC metadata | WebSearch + WebFetch (public pages) | None | Metadata only (by design) |
| Adaptive testing | LLM-internal (@learner-profiler) | N/A | Not an external service |
| Concept graphs | Mermaid inline text | Mermaid MCP (PNG export) | No image file export |
| Analytics | File-based (@progress-tracker) | N/A | Not an external service |

---

## 7. Configuration Validation Checklist

### 7.1 Hook Configuration

- [x] `guard_learner_state.py` — PreToolUse hook for SOT write protection
  - Reads `CLAUDE_TOOL_INPUT` for file path
  - Checks against `SOT_FILES` set (`state.yaml`, `learner-state.yaml`)
  - Checks against `SOT_DIR` path prefix (`data/socratic`)
  - Exit code 0 (warning mode) — stderr feedback for LLM self-correction
- [x] `track_session_activity.py` — PostToolUse hook for session activity tracking
  - Reads `learner-state.yaml` for active session detection
  - Writes to `sessions/active/.activity-tracker.json`
  - Prunes to last 100 entries — bounded growth
  - Atomic write (tmp + rename)
  - Exit code 0 always (logging-only)
- [x] `save_session_snapshot.py` — Stop hook for session snapshot
  - Reads `learner-state.yaml` for active session
  - Writes snapshot to `sessions/snapshots/{session_id}_{epoch}.json`
  - Prunes to last 20 snapshots per session
  - Atomic write (tmp + rename)
  - Exit code 0 always (snapshot-only)
  - Graceful degradation: PyYAML optional (simple parser fallback)

### 7.2 File Paths

| Path | Purpose | Created By |
|------|---------|-----------|
| `data/socratic/state.yaml` | Phase 0 SOT | Step 12 scaffolding |
| `data/socratic/learner-state.yaml` | Learner SOT | Step 12 scaffolding |
| `data/socratic/sessions/active/` | Active session logs | Step 12 scaffolding |
| `data/socratic/sessions/completed/` | Completed session logs | Step 12 scaffolding |
| `data/socratic/sessions/interrupted/` | Interrupted session logs | Step 12 scaffolding |
| `data/socratic/sessions/snapshots/` | Session snapshots | Step 12 scaffolding |
| `data/socratic/sessions/active/.activity-tracker.json` | Activity tracking | `track_session_activity.py` (runtime) |
| `data/socratic/curriculum/` | Curriculum data | Step 12 scaffolding |
| `data/socratic/user-resource/` | User-uploaded files | Step 12 scaffolding |
| `data/socratic/transcripts/` | Session transcripts | Step 12 scaffolding |
| `data/socratic/analysis/` | Content analysis | Step 12 scaffolding |
| `data/socratic/planning/` | Session plans | Step 12 scaffolding |
| `data/socratic/reports/` | Progress reports | Step 12 scaffolding |
| `data/socratic/misconceptions/` | Misconception library | Step 12 scaffolding |

### 7.3 No Syntax Errors

All hook scripts use standard Python 3 without external dependencies (except optional
PyYAML in `save_session_snapshot.py`, which has a built-in fallback parser). JSON
configuration entries are valid JSON. All file paths reference directories created by
Step 12 scaffolding.

---

## 8. Integration with Parent Hook System

The Socratic Tutor hooks coexist with the parent AgenticWorkflow hooks. The processing
order for each event:

### PreToolUse (Edit|Write)
1. `block_test_file_edit.py` — TDD guard (parent)
2. `predictive_debug_guard.py` — risk warning (parent)
3. `guard_learner_state.py` — SOT write protection (Socratic)

### PostToolUse (Edit|Write|Bash|Task)
1. `context_guard.py --mode=post-tool` → `update_work_log.py` (parent)
2. `track_session_activity.py` (Socratic)

### Stop
1. `context_guard.py --mode=stop` → `generate_context_summary.py` (parent)
2. `save_session_snapshot.py` (Socratic)

There are no conflicts between parent and child hooks — they operate on different
data domains (parent: `.claude/context-snapshots/`, child: `data/socratic/sessions/`).
