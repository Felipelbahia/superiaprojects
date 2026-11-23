# claude-code-review — Reference

Source: https://code.claude.com/docs/en/code-review (verified 2026-10-11). Heavy detail kept out of `SKILL.md`.

## Set up the managed service `[Claude Code only]`

Owner / Primary Owner of the Claude organization, plus permission to install GitHub Apps.

1. `claude.ai/admin-settings/claude-code` → Code Review section.
2. Click **Setup** → GitHub App installation flow.
3. Install the Claude GitHub App: pick the org, the repositories, approve permissions (read contents; write to pull requests and checks).
4. Select the repositories to enable.
5. Set **Review Behavior** per repo: *Once after PR creation* · *After every push* · *Manual*.
6. Verify with a test PR: the **Claude Code Review** check run appears within minutes (Manual mode: comment `@claude review`).

Costs shown per repo in the table; row actions turn a repo off or remove it. A monthly spend cap lives at `claude.ai/admin-settings/usage`; analytics at `claude.ai/analytics/code-review`.

## Comment commands

| Command | Effect |
|---|---|
| `@claude review` | One review; does not subscribe the PR to pushes |
| `@claude review always` | One review and subscribe to push-triggered reviews |
| `@claude review once` | Same as bare |

Requirements: top-level comment (not inline); command at the start, `once`/`always` on the same line; write, maintain or admin permission on the repo (for forks: on the **base** repo); PR open. Manual triggers also run on draft PRs. A review already running queues the request. Private org membership (GitHub default) means Claude does not recognize you; add yourself as a repo collaborator or publicize membership. Fork PRs: only a comment starts a review — re-running the check or pushing does not.

## REVIEW.md template

```markdown
# Review instructions

## What Important means here
Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, and migrations that aren't backward
compatible. Style, naming, and refactoring suggestions are Nit at most.

## Cap the nits
Report at most five Nits per review. If you found more, say "plus N
similar items" in the summary instead of posting them inline. If
everything you found is a Nit, lead the summary with "No blocking issues."

## Do not report
- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file
- Test-only code that intentionally violates production rules

## Always check
- New API routes have an integration test
- Log lines don't include email addresses, user IDs, or request bodies
- Database queries are scoped to the caller's tenant
```

Keep it short: a long `REVIEW.md` dilutes the rules that matter. General project context belongs in `CLAUDE.md`.

## Gate merges on severity

```bash
# 1) find the check run id for the commit
gh api repos/OWNER/REPO/commits/<commit-sha>/check-runs --jq '.check_runs[] | {id, name}'
# 2) read the machine-readable severity counts (last line of Details)
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
# -> {"normal": 2, "nit": 1, "pre_existing": 0}   (normal = Important)
```

Findings also appear as annotations in **Files changed** and in the check run Details table, independent of inline comments.

## Troubleshooting

- **Failed / timed-out review** (neutral conclusion, never blocks): comment `@claude review`, or click **Re-run** on the check (not for fork PRs).
- **Budget message instead of a review:** spend cap reached (resumes next period or when an admin raises it) or usage credits used up (an admin adds credits).
- **"Issues found" but no inline comments:** look at check run Details, Files changed annotations, and an **Additional findings** section in the review body (lines moved after a push).
- **Rating:** 👍/👎 on each comment feeds Anthropic's tuning; reactions do not re-run anything.

## Local `/code-review` details `[Claude Code only]`

- Runs as a background subagent; findings return to the conversation. Foreground when re-run while one is in progress, in `-p` / Agent SDK, or with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`.
- Follows `CLAUDE.md` like any session; **does not read `REVIEW.md`**. Background `--fix` edits bypass checkpoints.
- Remembers the last typed level (`low`..`max`) across sessions; `ultra` neither updates nor uses it. Without `ultra`, everything after flags is the review target (even if it starts with `/`). With `ultra`, one word = base branch or PR number; longer text becomes a note attached to the review.
- `--comment`: GitHub PR inline comments, or a single GitLab MR note via `glab` (prints in terminal if `glab` is missing). Use a URL or `!123` on self-managed GitLab.
- In hosts that request a findings list (e.g. desktop app) results go through `ReportFindings`; each entry shows file, one-sentence summary and a category tag; fixed findings are re-reported as fixed / skipped / no change needed.
- Claude can start the review by itself. To stop that while keeping the command: `{"skillOverrides": {"code-review": "user-invocable-only"}}` in a settings file.
- `ultra` (cloud): branch vs default branch plus working-tree changes; requires claude.ai auth; **not** on Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, ZDR or HIPAA orgs (falls back to a local review). From CI: `claude ultrareview`.

## Version gates (Claude Code)

| Feature | Minimum |
|---|---|
| `/review` alias; reuse of last typed level | v2.1.223 |
| Background-subagent review (before: inside the conversation) | v2.1.218 |
| Claude may start `/code-review` on its own everywhere | v2.1.246 |
| `--comment` for GitLab MRs | v2.1.257 |
| `--post` (ultra, github.com PR) | v2.1.227 |
| `--max-findings` | v2.1.288 |
| `/code-review` was named `/simplify` (applied fixes by default); `/simplify` is now a separate cleanup-only command | before v2.1.147 |
