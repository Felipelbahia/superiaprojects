#!/usr/bin/env python3
"""PreToolUse hook: an agent never edits its own file (skill writing-agents, core rule).

Reads the hook payload from stdin. When the call comes from a subagent (`agent_type`)
and the target is that agent's own file (`.agent/agents/<agent_type>.md` or
`.claude/agents/<agent_type>.md`), it denies the call. Everything else is allowed.
Standard library only.
"""
import json
import re
import sys


def own_file(agent_type: str, file_path: str) -> bool:
    path = file_path.replace("\\", "/")
    return bool(re.search(rf"(^|/)\.(agent|claude)/agents/{re.escape(agent_type)}\.md$", path))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    agent_type = payload.get("agent_type") or ""
    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if agent_type and file_path and own_file(agent_type, file_path):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Agent {agent_type} must not edit its own file. Write a proposal in its brain inbox/ and let the owner approve.",
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
