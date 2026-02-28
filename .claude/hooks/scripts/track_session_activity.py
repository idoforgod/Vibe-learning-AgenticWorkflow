#!/usr/bin/env python3
"""Track session activity during active tutoring sessions.

Hook type: PostToolUse (matcher: Edit|Write|Bash|Task)
Exit code: always 0 (logging-only hook, never blocks)

Writes activity entries to sessions/active/.activity-tracker.json for:
- Inactivity timeout detection (>5 min without tool use)
- Session duration computation
- Post-session analytics

Part of: Socratic AI Tutor — Hook & State Management (Step 17)

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
    try:
        with open(learner_state_path, "r") as f:
            content = f.read()
        # Simple check: if session_id is null or status is not active, skip
        if "session_id: null" in content or "status: null" in content:
            sys.exit(0)
        if "status: active" not in content and 'status: "active"' not in content:
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
