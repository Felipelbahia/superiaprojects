# git-e-revisao

Git, commits, pull requests e revisão de código: worktrees, changelog, descrição de PR, revisão local e completa.

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agents/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agents/agents/<nome>.md"`; workflow: `"<HUB>/.agents/workflows/<nome>.md"`.

## Skills (10)

| Skill | Use quando |
| --- | --- |
| `changelog-automation` | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions. |
| `claude-code-review` | Use when setting up, tuning or running Claude Code Review (managed GitHub PR review, REVIEW.md, @claude review) or the local /code-review command, when review findings are noisy, missing or costly, or when gating merges on automated review severity. Also for revisão de PR automatizada and ultrareview requests. |
| `code-review-checklist` | Code review guidelines covering code quality, security, and best practices. |
| `code-review-excellence` | Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining team morale. Use when reviewing pull requests, establishing review standards, or mentoring developers. |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Use when managing complex Git histories, collaborating on feature branches, or troubleshooting repository issues. |
| `github-publisher` | Use when the user asks to publish, upload or push a local folder or project to GitHub for the first time, create a new GitHub repository from existing code, or "subir o projeto pro GitHub" / "criar repositório", and when a repository is about to be shared (made public, a collaborator added, the link sent to someone) - including when they say it is already clean or they are in a hurry. |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |

## Agents (1)

| Agent | Use quando |
| --- | --- |
| `code-reviewer` | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability. Masters static analysis tools, security scanning, and configuration review with 2024/2025 best practices. Use PROACTIVELY for code quality assurance. |

## Workflows (14)

| Workflow | Use quando |
| --- | --- |
| `/ci_commit` | Create git commits for session changes with clear, atomic messages |
| `/ci_describe_pr` | Generate comprehensive PR descriptions following repository templates |
| `/commit` | Create git commits with user approval and no Claude attribution |
| `/create_worktree` | --- |
| `/describe_pr` | Generate comprehensive PR descriptions following repository templates |
| `/describe_pr_nt` | Generate comprehensive PR descriptions following repository templates |
| `/full-review` | Orchestrate comprehensive multi-dimensional code review using specialized review agents |
| `/git-workflow` | Complete Git Workflow with Multi-Agent Orchestration |
| `/issue` | GitHub Issue Resolution Expert |
| `/linear` | Manage Linear tickets - create, update, comment, and follow workflow patterns |
| `/local_review` | Set up worktree for reviewing colleague's branch |
| `/multi-agent-review` | Multi-Agent Code Review Orchestration Tool |
| `/pr-enhance` | Pull Request Enhancement |
| `/revert` | Git-aware undo by logical work unit (track, phase, or task) |

