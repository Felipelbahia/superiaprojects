---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: skill-resolver
description: Use whenever a capability seems relevant to the current task but no matching skill appears in the currently loaded skills list, or the Skill tool answers "Unknown skill" for a skill the project rules name — common in Antigravity Kit projects (any repo with a .agents/skills/ directory, or a CLAUDE.md/AGENTS.md that references "0 Padrões"), because Claude Code only auto-discovers SKILL.md files under .claude/skills/ and ~/.claude/skills/, never under .agents/skills/ or inside a hub. Also use when the user names a skill that doesn't show up in the listing, or asks "existe skill pra isso", "do we have a skill for X", "check 0 Padrões for a skill". Runs resolve_skill.py, which searches the project, the SIP hubs it consumes and the kit. This is the fallback for projects with no SIP installed; where `sip-geral` is installed, its resolver covers the same ground.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---
# Skill Resolver

## Why this exists

Claude Code's native Skill tool only lists `SKILL.md` files under the project's `.claude/skills/` and the personal
`~/.claude/skills/`. The Antigravity Kit keeps skills under `.agents/skills/` (and the SIP hubs keep theirs in the hub), a place
Claude Code never scans. A name the rules cite that is not linked there makes the Skill tool answer `Unknown skill`.
**That is not a project error**: the skill exists, it just lives somewhere the tool does not look.

## Which skill answers first

| The project has | Use |
|---|---|
| `sip-geral` (or any `sip-*`) in `.claude/skills/` | its resolver: it explains the same procedure and the hub's index by vertical |
| no SIP installed (no `.agents/SIPS-CONSUMIDOS.md`) | this skill |

Both end in the same command, so the answer is the same.

## Procedure

1. Run, from the project root (the kit's copy, by absolute path):
   ```
   python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/scripts/resolve_skill.py" <name or term>
   ```
   It looks in the project's own `.agents/`, the hubs listed in `.agents/SIPS-CONSUMIDOS.md`, the kit, and the hubs of the SIPs the project
   did not install. It reads each hub from disk now (the manifest is only a snapshot taken at install time) and prints the absolute
   path, the origin and whether that SIP is installed here. Exit 0 found, 1 not found, 2 usage.
2. Read the printed `SKILL.md` first: the index and frontmatter, then only the sections the task needs. Follow it inline, as if the
   Skill tool had loaded it.
3. Tell the owner in one line where it came from (the project's own, a hub, a SIP not installed here). A project-local skill reflects
   decisions of that codebase; a hub one is a generic default that may need adapting.
4. A skill of a SIP the project did not install: the script names that SIP's install prompt. Offer it; never install on your own.

## If nothing matches

The script prints every place it looked. Show that list before saying a skill does not exist. Never invent a procedure from general
knowledge and present it as the skill's guidance: ask the owner, or proceed with your own judgment and say that no dedicated skill
covered this.

## Never copy or link a hub skill into the project by yourself

Read it by its path. Only the *núcleo* (the process skills the rules name in mandatory steps, listed in `nucleo.json` next to the
`sip-geral` resolver) is linked in projects, by the SIP installer and `propagar_sip.py`. A project missing the núcleo links is brought up
to date by the skill `atualizar-sips`, with the owner's ok.
