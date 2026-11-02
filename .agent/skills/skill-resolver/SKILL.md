---
name: skill-resolver
description: Use whenever a capability seems relevant to the current task but no matching skill appears in the currently loaded skills list — this is common in Antigravity Kit projects (any repo with a .agent/skills/ directory, a .agent/rules/ directory, or a CLAUDE.md/GEMINI.md that references "0 Padrões"), because Claude Code only auto-discovers SKILL.md files under .claude/skills/ and ~/.claude/skills/, never under .agent/skills/. Also use when the user names a skill by name that doesn't show up in the listing, or asks things like "existe skill pra isso", "do we have a skill for X", "check 0 Padrões for a skill". Searches the project's own .agent/skills/ (and .agents/skills/ for older, unmigrated setups), then the global library at 0 Padrões/.agent/skills/, then 0 Mkt/ for marketing, SEO, copywriting or growth topics.
---

# Skill Resolver

## Why this exists

Claude Code's native Skill tool only lists `SKILL.md` files it finds under two
places: the project's `.claude/skills/` and the personal `~/.claude/skills/`.

The Antigravity Kit convention (used across the VibeCoding / Plinq projects)
stores skill content under `.agent/skills/` instead — a Google Antigravity
convention, not a Claude Code one. Claude Code never scans that path on its
own. A project's `CLAUDE.md` usually has a "Fallback Resolution Protocol"
section describing this search order in prose, but prose alone doesn't make
those skills invokable — nothing puts them in the Skill tool's list. This
skill is the actual procedure behind that prose: run it when you suspect a
relevant skill exists but isn't showing up.

## Search order

Run these in order and stop at the first real match. Use `find`/`ls`, not
memory — a name that existed in a past session may have moved or been
renamed.

1. **Project-local, Antigravity convention** — the current project's own
   `.agent/skills/<query>*` (and `.agents/skills/<query>*` for projects not
   yet migrated to the singular `.agent/` form). These are project-specific
   and take priority over anything global.
   ```
   find .agent/skills .agents/skills -maxdepth 1 -iname "*<query>*" 2>/dev/null
   ```
2. **Global base** — the shared skill library at
   `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/`.
   ```
   find "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills" -maxdepth 1 -iname "*<query>*"
   ```
   If nothing matches the literal query, `ls` the directory and scan names by
   eye — skill names are topic-based (`api-patterns`, `database-design`,
   `n8n-workflow-patterns`), not always a substring of what the user said.
3. **Global marketing** — for SEO, copywriting, growth, positioning, or
   marketing-strategy topics only:
   `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/`.

## Once you find a match

1. Read its `SKILL.md` first — treat it exactly like a normal Skill
   invocation: read the index/frontmatter, then only the specific sections
   relevant to the task at hand (don't read every file in the skill folder).
2. Follow its instructions inline, as if the Skill tool had loaded it.
3. Tell the user in one line where it came from (project-local vs. global
   0 Padrões vs. 0 Mkt) — this matters because project-local skills reflect
   decisions specific to that codebase, while global ones are generic
   defaults that may need adapting.

## If nothing matches

Say so plainly — don't fabricate a procedure from general knowledge and
pass it off as the skill's guidance. Ask the user, or proceed with your own
best judgment and flag that no dedicated skill covered this.

## Optional: promote a global skill to native discovery

If a global (`0 Padrões`) skill turns out to be used repeatedly in a given
project, it's worth making it natively discoverable there instead of
resolving it by hand every time — symlink it into that project's
`.claude/skills/`:
```
ln -s "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/<name>" ".claude/skills/<name>"
```
Only do this when asked, or mention it as a suggestion — creating files in a
project is a visible change and shouldn't happen silently.
