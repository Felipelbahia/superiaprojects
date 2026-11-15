---
name: writing-agents
description: Use when creating a new agent for the kit, adding memory or learning to an agent, deciding how much autonomy an agent has, or reviewing whether an agent file follows the kit's model.
author: Felipe Bahia (@felipelbahia)
license: MIT
---
# Writing Agents

## Overview

An agent is a role (who does the work); a skill is knowledge (how to do something). This skill builds agents with a fixed file model and a **brain**: a folder that records what the agent learned, so it improves run after run while the owner keeps control.

**Core rule:** the agent proposes, the owner approves. No autonomy level lets an agent edit its own file.

Scope: agents only (workflows and skills have their own rules: `writing-skills`).

## When to Use

- A new agent, or an existing agent that should start learning.
- Choosing `autonomy` for an agent.
- Reviewing an agent that keeps its own memory somewhere else.
- **Not for** one-off subagent prompts that live only inside a task.

## Create an agent

1. Confirm the role does not exist: `ls .agent/agents/` and `.agent/CATALOG.md`. Reuse before build.
2. Copy `references/agent-template.md` to `.agent/agents/<name>.md`. Fill every section; `description` is triggers only ("Use when ..."). Choose `model:` based on role complexity (`inherit` default; `flash_lite` for fast routine execution, converted to `haiku` for Claude Code; `pro` for deep reasoning, converted to `sonnet`). Write only what the owner said or this skill requires; anything you add (limits, role claims, skills, tools) is a builder choice, listed in `decisoes.md` as `pendente de confirmação`. Every limit needs a step that keeps it; each tool in `tools` needs a step that uses it; a step names only skills listed in `skills:`; `description` names the situation, never what the agent does.
3. Choose `autonomy` on purpose and tell the owner which one:

   | Level | The agent may | Default |
   |---|---|---|
   | `propose` | write lessons in its brain; everything else is a proposal | yes |
   | `contexts` | also add a new context to `contextos.md` and tell the owner | no |

   Never grant more: promoting a lesson to the agent file, or writing to the hub, always needs the owner.
4. Create the brain from `references/brain-templates.md` at `.agent/agents/agents_brains/<name>/` (`contextos.md`, `licoes.md`, `decisoes.md`, `referencias/`, `inbox/` with a `.gitkeep`). Born empty: `licoes.md` holds only its title, never an example lesson. Initial contexts come from the owner; the first entry of `decisoes.md` quotes the owner's instruction.
5. Run `python .agent/scripts/sync_entrypoints.py` and `python .agent/scripts/generate_catalog.py`. `--check` must pass: it fails when an agent with `autonomy` lacks its brain.

## Before you finish

Re-read the agent file and `decisoes.md` and check each line. A "step" is any part of the agent file that says what it does (Processo, Formato da entrega, Memória, Aprender).
1. Every tool in `tools` is used by a step, and `decisoes.md` names that step. No step uses it: remove the tool.
2. Every premise taken from the brief (for example "the style changes every time") appears in `decisoes.md` with origin `briefing`, wherever it shows up (Papel, title, `description`, Processo, Formato da entrega). If an idea came from the brief, its origin is ALWAYS `briefing` in every section where it appears—repeating it elsewhere never turns it into `construtor`. Never assign conflicting origin labels to the same premise across different sections.
3. Exact quotes vs paraphrases: Every quote enclosed in quotation marks in `decisoes.md` must be a verbatim word-for-word excerpt of the owner's instruction. If any word is changed, omitted or summarized, do not use quotation marks; label it `dono (parafraseado)`. The origin label must be chosen strictly from the allowed set: `briefing`, `dono (parafraseado)` or `construtor`. Never invent composite or hybrid labels (like `construtor/briefing` or `briefing (parafraseado)`).
4. One sentence per item, one label per item: Every single sentence of the agent file that is not the owner's quoted words nor the template text must be listed in `decisoes.md` as its own separate item (one bullet per sentence—never group multiple sentences into a single block/bullet). Each item states its exact location (Papel, title, `description`, step N) and has exactly one origin label (`briefing`, `dono (parafraseado)` or `construtor`). That includes the `description` and every individual sentence of Papel. A step that only points to another section ("Deliver as in Formato da entrega") is template wording and needs no entry.
5. `python .agent/scripts/sync_entrypoints.py --check` passes.

An empty `skills:` is valid. A skill mentioned only as a pointer in Formato da entrega (for example `mapa-de-destinos`) is not a dependency and need not be in `skills:`.

## The learning cycle

```
signal → lesson (licoes.md) → proposal (inbox/) → owner approves → agent file changes → decisoes.md
```

- **Signal** = QA below 10, a failed check, an owner correction, or an owner instruction. No signal, no lesson.
- **Context + alcance** on every lesson. A lesson is `só este contexto` unless the agent writes one line saying why it transfers (`candidata a transferir`).
- **Activation:** load `geral` + the lessons of the task's context. A context with no lessons yet gets the `candidata a transferir` lessons of other contexts, proposed one by one.
- **3 occurrences** of the same lesson: propose promoting it to the agent file (a file in `inbox/`).
- **Hub vs project:** the brain of a project stays in that project. Only a lesson with exponential gain (many agents or runs) goes up, as an item in the hub brain's `inbox/`, with owner approval.
- Anything about the structure of this skill (fields, folders) goes to the owner's `inbox/`, not decided in the middle of a run.

## Common mistakes

| Mistake | Fix |
|---|---|
| Memory in a separate skill, or in a folder of the consuming project | The brain is `agents_brains/<name>/`, owned by the agent. Skills are knowledge, not per-agent memory |
| No `autonomy` field | Add it; without it the agent is not checked and the owner never chose |
| Inventing limits, hand-offs or role premises the owner never stated | Only owner words and this skill's rules; the rest is listed as pending in `decisoes.md` |
| Seeding an example lesson "to show the format" | The brain is born empty; the format lives in `references/brain-templates.md` |
| `description` that summarizes what the agent does | Triggers only; see the bad/good pair in `references/agent-template.md` |
| Free-form lesson fields | Use the template: contexto, alcance, problema, lição, gatilho, ocorrências |
| The agent edits its own file after a good run | Write the proposal in `inbox/`; the owner approves |
| Lesson recorded without a signal | Skip it; noise costs context on every activation |
| A new context spelled a second way ("doc" vs "documentário") | Use the table in `contextos.md`; new rows only as `autonomy` allows |
| Migrating all old agents at once | Out of scope: an agent without `autonomy` is not checked and stays as it is |
