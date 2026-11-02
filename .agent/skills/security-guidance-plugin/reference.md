# security-guidance-plugin — Reference

Source: https://code.claude.com/docs/en/security-guidance (verified 2026-10-11).

## Prerequisites and bootstrap

- Python 3.7+ on `PATH`. The agentic commit review needs 3.10+, and so do all model-backed reviews on a third-party provider (Amazon Bedrock, Google Cloud's Agent Platform). Interpreter order: `python3.13` … `python3.10`, then `python3`, `python`, `py -3`.
- A git repository for the directory you work in. End-of-turn and commit reviews diff against git state and skip silently outside one; the per-edit check works anywhere.
- First run creates a virtualenv under `~/.claude/security/` and installs the Claude Agent SDK (needs `pip` and network). If that fails, or Python is older than 3.10, the first-party commit review falls back to a single-shot review; on a third-party provider the model-backed reviews skip. A one-time notice appears when old Python is the cause.

## Install and enable

```text
/plugin install security-guidance@claude-plugins-official
/plugin marketplace add anthropics/claude-plugins-official      # only if "marketplace not found"
```

Choose **user scope** to load it in every local session. Where `/plugin` is unavailable: desktop app → **+** → Plugins → Add plugin; VS Code → Manage plugins dialog. Cloud sessions do not load user or repo-settings plugins (see the org plugin docs). Run `/reload-plugins` if the summary asks for it.

Team (checked in):

```json
{ "enabledPlugins": { "security-guidance@claude-plugins-official": true } }
```

Administrators can enable it org-wide through `enabledPlugins` in managed settings. Uninstalling a project-enabled plugin writes an override to `.claude/settings.local.json` for you only.

## Guidance file for the model-backed reviews

`.claude/claude-security-guidance.md`, loaded alongside the built-in checklist:

```markdown
# Security guidance for this repo

- Do not log `customer_id` or `account_number` at INFO level or above.
- All routes under `/admin` must call `require_role("admin")` before any database read.
- Use `crypto.timingSafeEqual` for token comparison instead of `===`.
```

Advisory, additive, not a guardrail. For hard enforcement pair it with a hook that blocks the edit or a CI check.

## Custom per-edit patterns

`.claude/security-patterns.yaml`; the plugin also reads `.claude/security-patterns.yml` and `.claude/security-patterns.json` with the same schema. Deterministic string matches next to the built-ins:

```yaml
patterns:
  - rule_name: internal_api_key
    substrings: ["sk_live_", "AKIA"]
    reminder: "Hardcoded API key prefix. Load credentials from the secret manager."
  - rule_name: tenant_unfiltered_query
    regex: "\\.objects\\.all\\(\\)"
    paths: ["**/src/tenants/**"]
    reminder: "Multi-tenant code must filter by org_id."
```

| Field | Type | Notes |
|---|---|---|
| `rule_name` | string | Shown in the warning |
| `reminder` | string | Appended to Claude's context, capped at 1 KB |
| `regex` | string | Python regex on the edited content |
| `substrings` | list | Literal substrings; give this **or** `regex` |
| `paths` | list | Optional globs; match the **full** path, so prefix with `**/` |
| `exclude_paths` | list | Optional globs to skip |

Up to 50 custom rules; regexes prone to catastrophic backtracking are skipped. YAML needs PyYAML (not installed by the plugin); JSON works everywhere.

## Lookup locations

The plugin finds `claude-security-guidance.md` and `security-patterns.yaml` in the same places, regardless of how it was enabled, and concatenates all that exist (guidance file capped at 8 KB combined):

| Scope | Path |
|---|---|
| User | `~/.claude/claude-security-guidance.md` (every project on the machine; admins can push it via device management) |
| Project | `.claude/claude-security-guidance.md` (checked in) |
| Project local | `.claude/claude-security-guidance.local.md` (personal; add to `.gitignore`) |

## Hooks it registers

| Event | Purpose |
|---|---|
| `SessionStart` | Bootstrap the Python environment |
| `UserPromptSubmit` | Capture the working-tree baseline the end-of-turn review diffs against |
| `PostToolUse` on `Edit`, `Write`, `NotebookEdit` | Per-edit pattern match |
| `Stop` | End-of-turn diff review in the background |
| `PostToolUse` on `Bash` filtered to `git commit` / `git push` | Commit and push review in the background |

Source: `github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance` — a working example of running a separate model call from a hook and feeding the result back.

## Cost

Per-edit: free. End-of-turn: about one review call per turn that changes files. Commit: agentic, possibly several model turns per commit, capped at 20 per rolling hour. Both model layers default to Claude Opus 4.7 (per the page on 2026-10-11); override with `SECURITY_REVIEW_MODEL` (end of turn) and `SG_AGENTIC_MODEL` (commit). Usage counts toward your normal plan usage.

## Silent skips (check `~/.claude/security/log.txt`)

- Not a git repository → end-of-turn and commit reviews skip.
- No Anthropic authentication and no third-party provider → only the per-edit check runs.
- `security-patterns.yaml` present but PyYAML missing → file ignored; use `.json`.
- A clean commit, or findings identical to the end-of-turn ones → no visible output.

## Where it sits in the stack

See the layered-tools table in `claude-security-scan/SKILL.md`. This review reads source in your checkout, not a running site or deployed service.
