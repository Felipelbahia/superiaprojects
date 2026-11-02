---
name: spec-writing
description: Use when a feature or change needs a written specification — Problem, Solution, User Stories, Decisions — before planning or implementation begins, turning what's already been discussed into a concrete document instead of an implicit shared understanding.
---

# Spec Writing

## Overview

Turns what's already been discussed (or already understood from the codebase) into a written spec: Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope. **Synthesis, not interview** — if the ask genuinely hasn't been discussed yet, run `brainstorming` first; don't invent answers here to fill gaps.

## When to Use

- Right after brainstorming/Socratic discovery has clarified an ask, before planning starts.
- Any time "what are we actually building" needs to be written down and confirmed, not just implied.
- As the Espec phase inside `execution-loop` — that skill appends its own 0-10 QA rubric on top of this template; the template itself stays tracker-agnostic.
- Equally valid standalone, for a single-pass feature that doesn't need the full loop.
- **NOT** for one-line fixes — see `execution-loop`'s classifier for when the overhead is worth it.

**Reaching `brainstorming`/`execution-loop`:** if not present in this project's own `.agent/skills/`, both live at `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/` — resolve via Rule 4 (Fallback Resolution Protocol) / `skill-resolver`, the same way this skill itself was found.

## Process

1. **Ground it in the real codebase.** Explore enough to use the project's existing domain vocabulary and respect any ADRs/conventions in the area being touched — don't introduce new terms the codebase doesn't already use.
2. **Sketch the testing seams before writing decisions.** Prefer an existing seam over a new one; use the highest seam possible; fewer seams is better (one is ideal). If a new seam is unavoidable, propose it at the highest point you can, and confirm the choice with the user — the wrong seam here makes every later test awkward.
3. **Write the spec** using the template below.
4. **Publish it** to wherever this project's process actually lives: the loop's `NN Espec.md` file when run inside `execution-loop`, `.agent/plans/{slug}.md` standalone, or — only if the project already uses one — its issue tracker with whatever triage/ready-for-agent label convention it has. Don't invent a tracker workflow that isn't already there.

## Template

```markdown
## Problem Statement
[The problem, from the user's perspective.]

## Solution
[The solution, from the user's perspective.]

## User Stories
1. As a <actor>, I want <feature>, so that <benefit>
2. ...
[Long, numbered, extensive — cover every angle of the feature, not just the obvious path.]

## Implementation Decisions
- Modules to be built/modified, their interfaces, architectural/schema/API decisions, technical clarifications.
- No file paths or code snippets — they go stale fast.
- Exception: a prototype snippet that encodes a decision more precisely than prose (state machine, reducer, schema, type shape) — trimmed to the decision, not a working demo.

## Testing Decisions
- What makes a good test here (behavior, not implementation detail).
- Which modules get tested, at which seam (from Process step 2).
- Prior art: similar tests already in this codebase.

## Out of Scope
[What this spec explicitly does not cover.]

## Further Notes
[Anything else worth flagging.]
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Interviewing the user when the ask was already discussed | Synthesize from context; only ask about what's genuinely still undecided |
| Inlining file paths / code snippets as "decisions" | Describe the decision in prose — paths and snippets rot, prose doesn't |
| Picking a new test seam when an existing one already covers it | Prefer existing seams; a new one needs explicit justification |
| Skipping User Stories because "the ask is obvious" | Write them anyway — Plan and QA rubrics get built from them downstream |
| Assuming every project has an issue tracker with triage labels | Publish to wherever this project's process actually lives; don't invent one |
