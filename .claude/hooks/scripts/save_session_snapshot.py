#!/usr/bin/env python3
"""Save session snapshot on Stop event for recovery via /resume.

Hook type: Stop
Exit code: always 0 (snapshot-only hook, never blocks)

This implements the session recovery infrastructure by saving a snapshot
of the current session state to data/socratic/sessions/snapshots/.
If the session is interrupted (context overflow, API error, user closes),
the latest snapshot enables recovery via /resume.

Snapshot schema matches the specification in hooks-and-state.md Section 3.3.

Part of: Socratic AI Tutor — Hook & State Management (Step 17)

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
    """Minimal YAML parser for flat/nested key-value extraction.

    Handles:
    - key: value pairs
    - key: null → None
    - Nested keys via indentation tracking
    - Commented lines (#)

    Does NOT handle:
    - Flow mappings ({})
    - Flow sequences ([])
    - Multi-line strings
    - Anchors/aliases

    When PyYAML is available, this function is not used.
    """
    result = {}
    current_section = None
    current_subsection = None

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if ": " in stripped or stripped.endswith(":"):
            if ": " in stripped:
                key, _, value = stripped.partition(": ")
            else:
                key = stripped.rstrip(":")
                value = ""

            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value == "null" or value == "":
                value = None
            elif value.isdigit():
                value = int(value)
            elif value.replace(".", "", 1).isdigit():
                try:
                    value = float(value)
                except ValueError:
                    pass

            if indent == 0:
                if value is None and not stripped.endswith(": null"):
                    current_section = key
                    result[key] = {}
                    current_subsection = None
                else:
                    result[key] = value
                    current_section = None
            elif indent <= 4 and current_section:
                if value is None and not stripped.endswith(": null"):
                    current_subsection = key
                    if not isinstance(result.get(current_section), dict):
                        result[current_section] = {}
                    result[current_section][key] = {}
                else:
                    if not isinstance(result.get(current_section), dict):
                        result[current_section] = {}
                    result[current_section][key] = value
                    current_subsection = None
            elif indent > 4 and current_section and current_subsection:
                section = result.get(current_section, {})
                if isinstance(section, dict):
                    subsection = section.get(current_subsection, {})
                    if isinstance(subsection, dict):
                        subsection[key] = value
                        section[current_subsection] = subsection
                        result[current_section] = section

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
            "socratic_depth_reached": current_session.get(
                "socratic_depth_reached", 1
            ),
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
            [f for f in os.listdir(snapshot_dir)
             if f.startswith(session_id) and f.endswith(".json")],
            reverse=True,
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
