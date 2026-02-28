#!/usr/bin/env python3
"""Guard learner-state.yaml and state.yaml from unauthorized writes.

Hook type: PreToolUse (matcher: Edit|Write)
Exit codes:
  0 — allow (target is not a SOT file, or orchestrator context detected)
  2 — (reserved for future hard block if sub-agent detection becomes reliable)

Environment:
  CLAUDE_TOOL_INPUT — JSON with file_path (Edit) or file_path (Write)
  CLAUDE_PROJECT_DIR — project root

Part of: Socratic AI Tutor — Hook & State Management (Step 17)
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

    # Target IS a protected SOT file.
    # Output warning to stderr for LLM self-correction.
    # Exit 0 (allow) because orchestrator itself needs to write.
    # The warning serves as a reminder for sub-agents.
    sys.stderr.write(
        f"WARNING: Writing to SOT file '{basename}' in {SOT_DIR}/. "
        f"ONLY @orchestrator should write to SOT files. "
        f"Sub-agents must write to their own output files and signal @orchestrator. "
        f"If you are a sub-agent, STOP and return your output via Task result instead.\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
