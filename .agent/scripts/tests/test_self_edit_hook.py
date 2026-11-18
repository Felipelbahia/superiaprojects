"""Tests for .agent/hooks/block_agent_self_edit.py (an agent never edits its own file)."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "hooks" / "block_agent_self_edit.py"


def fire(payload: dict | str) -> subprocess.CompletedProcess:
    data = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run([sys.executable, str(HOOK)], input=data, capture_output=True, text=True)


def edit(agent_type, path, tool="Edit") -> dict:
    payload = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"file_path": path}}
    if agent_type:
        payload["agent_type"] = agent_type
        payload["agent_id"] = "x"
    return payload


class SelfEditHook(unittest.TestCase):
    def denied(self, result) -> bool:
        return bool(result.stdout.strip()) and json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_agent_editing_its_own_source_file_is_denied(self):
        r = fire(edit("diretor", "/p/.agent/agents/diretor.md"))
        self.assertEqual(r.returncode, 0)
        self.assertTrue(self.denied(r))
        self.assertIn("inbox", json.loads(r.stdout)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_agent_writing_its_own_claude_copy_is_denied(self):
        self.assertTrue(self.denied(fire(edit("diretor", "/p/.claude/agents/diretor.md", "Write"))))

    def test_agent_writing_in_its_own_brain_is_allowed(self):
        self.assertFalse(self.denied(fire(edit("diretor", "/p/.agent/agents/agents_brains/diretor/licoes.md"))))

    def test_agent_editing_another_agent_is_allowed(self):
        self.assertFalse(self.denied(fire(edit("diretor", "/p/.agent/agents/outro.md"))))

    def test_agent_with_similar_name_is_not_confused(self):
        self.assertFalse(self.denied(fire(edit("diretor", "/p/.agent/agents/diretor-de-arte.md"))))

    def test_main_session_without_agent_type_is_allowed(self):
        self.assertFalse(self.denied(fire(edit(None, "/p/.agent/agents/diretor.md"))))

    def test_call_without_file_path_or_bad_json_is_allowed(self):
        self.assertFalse(self.denied(fire({"agent_type": "diretor", "tool_input": {}})))
        r = fire("not json")
        self.assertEqual((r.returncode, r.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
