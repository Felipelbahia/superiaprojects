# claude-security-scan — Reference

Source: https://code.claude.com/docs/en/claude-security (verified 2026-10-11).

## Install / uninstall

```text
/plugin install claude-security@claude-plugins-official
/plugin marketplace add anthropics/claude-plugins-official      # only if "marketplace not found"
claude plugin uninstall claude-security                          # or via the /plugin menu
```

In the VS Code extension or desktop app use the plugin install flow instead. If the summary says `Run /reload-plugins to apply.`, reload plugins. Platforms: Linux, macOS, Windows.

## Happy path

1. `/claude-security` → **Scan codebase**.
2. Choose the whole repository or a focused area (or answer "I don't know" and take the default for the repo's size).
3. Confirm. A scan may take a while and use many tokens; Claude Code must stay open. Stages are reported as they start; detail under `/workflows`.
4. Read the report.
5. `/claude-security` → **Suggest patches**, pick findings.
6. `git apply` the patches you accept, each in its own PR.

Plain language works too: `/claude-security scan my branch`, "scan commit abc1234", "fix finding F3".

## Output directory

`CLAUDE-SECURITY-<timestamp>/`

| File | Content |
|---|---|
| `CLAUDE-SECURITY-RESULTS.md` | Report; each finding has an ID (`F1`…), impact, exploit scenario, severity, confidence, recommendation |
| `CLAUDE-SECURITY-RESULTS.jsonl` | Same findings, one JSON object per line |
| `CLAUDE-SECURITY-RESULTS.sarif` | SARIF 2.1.0 for GitHub code scanning and any tool that reads the standard; findings classified under CWE categories |
| `CLAUDE-SECURITY-REVISION-<commit>.json` | Revision stamp: commit scanned (`UNVERSIONED` outside version control), effort, whether uncommitted changes were in the tree, how thoroughly the run was verified |
| `patches/F<n>.patch` + note | One per finding that passed review (created by *Suggest patches*) |

A finding only appears after independent verifier agents analyzed it, which keeps reports short. Scans are nondeterministic: two scans of the same code can surface different findings.

## Change scans

When the branch has commits its base lacks, the menu offers to scan only that diff. You can also scan one of your open pull requests, or a single commit by asking. Only **committed** changes are scanned. Finding open PRs is the single step that touches the network, offered only when the session may run the GitHub CLI and `gh` is signed in. Needs a git repository (full scans of unversioned directories still work).

## Patches in detail

- Built against committed code; findings whose code changed since the report are skipped with a note, and a fresh scan is offered.
- Drafted in a scratch copy of the repo; your files stay untouched until you apply.
- An independent agent reviews each patch, running the project's tests when the code has them. If the patched code has no tests, the patch's note says its review ran without a test pass.
- Delivery rule: a patch is written only when the review vouches for **all three** of: it addresses the one finding, introduces no new vulnerability, leaves other behavior unchanged. Otherwise a short note explains why.
- `git apply CLAUDE-SECURITY-<timestamp>/patches/F1.patch` — or ask Claude to apply it and open a PR.

## Models and providers

The agents that hunt, verify, and write and review patches run on **your session's model** (`/model` before starting). A few supporting steps, such as mapping the repo, use the `sonnet` alias. No separate API key. Works on a paid plan, with API access, or on a third-party provider (Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry). On a third-party provider the `sonnet` alias can resolve to a different version: pin it with `ANTHROPIC_DEFAULT_SONNET_MODEL` and the other pinning variables. Automatic model fallback re-runs a request that a model's safeguards flag; on Bedrock, Agent Platform and Foundry it can end in a refusal instead, depending on deployment setup.

## Troubleshooting

- **Python warning in the menu:** no `python3`, or the first one on `PATH` is older than 3.9 — install or reorder, start a new session.
- **"Safeguards flagged this message" on a Fable model:** expected; cybersecurity classifiers flag some requests and Claude Code re-runs them on an Opus model; the scan should still complete.
- **Many permission prompts:** the plugin works best in auto mode, which lets the scan's agents proceed without a prompt at each step.
