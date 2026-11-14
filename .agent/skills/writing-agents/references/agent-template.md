# Agent template

Copy to `.agent/agents/<name>.md`. The file name, the `name` field and the brain folder name are the same word (kebab-case).

```markdown
---
name: <name>
description: Use when <the situation that calls for this agent. Name the situation, never the actions the agent takes.>
tools: <the minimum the role needs: only tools a step of Processo uses; list each tool with its step in decisoes.md>
model: inherit
skills: <only skills a step of Processo names, comma-separated, each must exist; a step names only skills listed here>
autonomy: propose
---

# <Name> - <one-line role>

## Papel
Who this agent is and what it owns. Two or three sentences.

## Limites
What it never does (domains it hands to other agents, actions that need the owner).
Always includes: never edits its own file; never writes outside its brain without saying so.
Every limit here has a step in Processo or Formato da entrega that keeps it; a limit with no step is deleted.
Only what the owner said or this skill requires goes in the file. What the builder adds (limits, role wording, a hand-off to another agent) is a builder choice and is listed in `decisoes.md` as `pendente de confirmação`.

## Processo
The steps it follows on every run, in order. Include a step that maps the task to a context of `contextos.md` (none fits: use `geral` and propose the new context to the owner). End with "Aprender" (see below).

## Formato da entrega
What the owner receives: shape, language, where files go (`docs/mapa-de-destinos.md`).
Always ends with the list of files written outside the brain (this is how "without saying so" in Limites is kept).
Say where each deliverable is saved. If `docs/mapa-de-destinos.md` or the row for it is missing: tell the owner and propose the row before saving (pointer to skill `mapa-de-destinos`, not a dependency); never leave a dead path.

## Memória
On activation, read in this order:
1. `.agent/agents/agents_brains/<name>/contextos.md` (accepted contexts)
2. `licoes.md`: lessons with context `geral` + lessons of this task's context
3. Context with no lessons yet: propose the lessons marked `candidata a transferir`
   from other contexts, one by one, for the owner to accept or refuse.

## Aprender
Only with a signal (QA below 10, failed check, owner correction) or an owner instruction:
write a lesson in `licoes.md` (fields: contexto, alcance, problema, lição, gatilho, ocorrências; format in the skill's `references/brain-templates.md`; alcance is `só este contexto` by default, `candidata a transferir` only with a one-line reason)
(a repeated lesson raises `Ocorrências` on the same entry, never a duplicate);
at 3 occurrences propose promoting it to this file.
Never edit this file: write the proposal in `inbox/` of the brain. A change the owner approves is applied by the owner or at the owner's request, and gets an entry in `decisoes.md`.
```

## Frontmatter rules

| Field | Rule |
|---|---|
| `name` | equals the file name without `.md` |
| `description` | starts with "Use when", triggers only (a summary of the process makes the model skip the body). Bad: "Use when a migration needs a reviewer to check locks, rollbacks and indexes" (lists what the agent does). Good: "Use when a database migration is about to run" (names the situation) |
| `tools` | the minimum the role needs: each tool has a step that uses it, listed in `decisoes.md`; do not copy a full list |
| `skills` | only the ones a step names, and a step names only skills listed here; each must exist (`sync_entrypoints.py --check` fails otherwise) |
| `autonomy` | `propose` or `contexts`, always chosen on purpose (see `SKILL.md`) |

Existing agents without `autonomy` are not checked and do not have to migrate.
