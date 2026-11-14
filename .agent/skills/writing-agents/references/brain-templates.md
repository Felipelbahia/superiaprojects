# Brain templates

Folder: `.agent/agents/agents_brains/<name>/`. Create all of it when the agent is created.

The brain is born empty: `licoes.md` has only its title. Never seed an example lesson (a lesson exists only with a real signal, and a seeded one would load as real on the first activation). The example below is a format reference, not content. The initial contexts and the reason the agent exists come from the owner, not from the builder.

```
agents_brains/<name>/
  contextos.md     accepted contexts (short list)
  licoes.md        lessons, newest first
  decisoes.md      history of decisions and improvements of the agent
  referencias/     reference material the agent consults
  inbox/           items the owner will decide later (put a .gitkeep: git drops empty folders)
```

`sync_entrypoints.py --check` requires `contextos.md`, `licoes.md`, `decisoes.md` and `inbox/`.

## contextos.md

```markdown
# Contextos de <name>

| Contexto | Quando usar |
|---|---|
| geral | vale para qualquer tarefa do agente |
| <contexto-1> | <one line> |
```

A task context outside this table is proposed to the owner before use. With `autonomy: contexts` the agent may add the row itself and tells the owner in the reply.

## licoes.md (one entry per lesson)

```markdown
## AAAA-MM-DD · <projeto> · <título curto>
Contexto: <um contexto de contextos.md | geral>
Alcance: só este contexto | candidata a transferir: <justificativa de uma linha>
Problema: <what went wrong or worked, concrete>
Lição: <the rule that follows from it>
Gatilho: <the signal: QA 5/10 in cycle 2 | owner said "...">
Ocorrências: 1
```

Rules:
- A repeated lesson raises `Ocorrências` on the same entry; it never creates a duplicate.
- At `Ocorrências: 3` write a proposal in `inbox/` to promote it to the agent file.
- `candidata a transferir` needs the one-line reason; without it the alcance is `só este contexto`.

## decisoes.md

```markdown
## AAAA-MM-DD · <título>
Decisão: <what changed in the agent or how it works>
Motivo: <the lesson, the inbox item or the owner instruction behind it>
```

One entry per approved change to the agent file or to its brain structure. The first entry records the creation and quotes the owner's instruction in `Motivo` (only what the owner really said); every sentence of the agent file that is neither the owner's quoted words nor the skill's template text is a builder choice: list each one (skills, each tool with its step, each limit, role wording, steps of Processo, premises taken from the brief) with its origin (`briefing`, `dono (parafraseado)` or `construtor`) and where it appears (Papel, title, `description`, step N) as `escolha do construtor, pendente de confirmação`; never write "derived from the owner's words" unless it is quoted; every context added to `contextos.md` gets its own entry with the owner's words (or the owner's approval of the proposal).

## inbox/

One file per item: `NNN-assunto.md`. Two kinds go here and nowhere else:
- a proposal to change the agent file (promoted lesson, new rule);
- a lesson with `candidata a transferir` that the owner may promote to the hub.

Resolved items move to `inbox/arquivo/`, never deleted.

## Hub and project (hybrid)

The agent file lives in the hub. The brain of a project lives at the same path inside that project and holds the lessons of that project only. A lesson reaches the hub brain only as an inbox item of the hub brain, and only when the gain is exponential (it improves many agents or many runs, not one case). The owner approves each one.
