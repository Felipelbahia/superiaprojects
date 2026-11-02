---
name: brainstorming
description: "Use when about to create features, build components, add functionality, modify behavior, or plan anything new, in software or out of it, and when a request is complex, vague, or unclear - the Socratic Gate, before any tool use or implementation"
---

# Brainstorming (Socratic Gate + Discovery)

You build what you believe your human partner wants, and that belief is usually thinner than it feels. This skill finds out what they actually want, and why, before anything gets built. It is the full protocol behind the **Socratic Gate** in CLAUDE.md / GEMINI.md.

People often haven't finished working out what they want. Good questions help them think it through. When you understand the why, you make the hundred decisions they never mention the way they would have made them.

## First: What Do You Actually Know?

Before you reply, ask: what do I know about what they want, and why?

| Situation | Action |
|---|---|
| Everything that matters is in the request ("make the icon cornflower blue") | Quick, clear task. Do it, say what you did. |
| Code edit / bug fix | Confirm your understanding in one line + one impact question (what else touches this?). |
| Build / create / new feature, vague requirements | Start the conversation below. |
| User answered a list (1, 2, 3...) or said "proceed" | Don't skip the gate. Ask **2 edge-case or trade-off questions** the answers left open. |
| Multi-domain / full orchestration | Gate first. No subagents until the user clears it. |

If even 1% is unclear, ask. Never assume.

## Your First Message

Two things, in this order:

1. One line saying that if they'd rather skip the questions and have you just start, they can say so.
2. One open question that gets them describing. Ask about a real moment or concrete picture: "What's the moment you find yourself wishing this existed?"

That's the whole message.

**If they opt out:** the questions stop, but the gate's "never assume" does not. State every assumption you are about to build on (purpose, users, scope, platform/language) in a few plain lines, then proceed through the normal workflow.

## The Conversation

Each message ends with **one** question: a single sentence, no list of example answers hanging off it. Plain language, pitched just above where your human partner is. Match their vocabulary; no process jargon. Be concise; lead with what matters.

**Get them describing.** Open questions come first; their own words carry intent your options can't. Offer a short menu only when they're stuck or the choice is a real trade-off (see `dynamic-questioning.md`; use your harness's structured-question tool if it has one, e.g. `AskUserQuestion` in Claude Code, otherwise a short lettered list in chat). When they say "just guess" or "what do you think?", propose something concrete.

**Minimum coverage (the gate's three questions).** Before a build starts you must have covered all three. Cover them across the conversation, one per message, in your own words, never as a form:

- 🎯 **Purpose**: what problem is this solving, why now, what does success look like?
- 👥 **Users**: who uses it, in what situation?
- 📦 **Scope**: must-have vs nice-to-have; goals, non-goals, anti-goals (what would make this a failure even if it technically works).

Often one good answer covers two of them. Skip a question only when the answer is already on the table; never skip a topic.

**Questions reveal consequences.** Each question must eliminate implementation paths or connect to an architectural decision. Generate them from the request and its context, never from a static template. For domain-specific question banks, read `dynamic-questioning.md`.

**How it gets made.** Find out early which choices about medium, tools, platform and language they want to make, which they hand to you, and what they already have. Build on what existing work already uses. Any choice you make goes in the design as your call, never as something they agreed to.

**More ground to cover** (territory, not a script):

- what kind of thing this is, and what makes it special
- prior art: what they've seen elsewhere, loved or hated
- current state: what exists now, what they've tried
- the details they care about

**Questions that work** anchor in specifics: "Walk me through the last time...", "If it could only do one of these well, which?", "What would make you wince if I got it wrong?" A guess they can correct often beats a question.

**Offer recon.** Once you have some grounding and looking would help (their codebase, files, the web), offer to go look and say what for. They decide.

**Think wide privately.** Before proposing, come up with several ideas and drop the weak ones. Show the comparison (2-3 approaches, your recommendation first, with trade-offs) only when it helps them decide.

**Show, don't tell.** Offer the visual companion (below) whenever seeing would help more than reading: screens, layouts, flows, options that look different, diagrams.

**Spike to feel things out.** A quick throwaway build is often the cheapest way to learn what they want. Offer one when it would help. Spikes are labeled throwaway; keeping one is a new request that comes back through the gate.

## Play It Back

As soon as you understand one part well enough to describe it, describe it back in about 200-300 words, then return to questions about the next part. Playback and questions alternate; the last chunk covers whatever is left.

Mark anything you're guessing as your guess; only what they said goes in as theirs. End each chunk by asking what's wrong or missing. If a chunk describes something they'll look at and they haven't seen the visual companion offer, send the offer first (its own message) and hold the chunk.

## Size the Work

Once you understand what they want, pick a size, say it in plain words. They can override.

| Size | The full description | Then |
|---|---|---|
| A quick, clear task | the request itself | do it |
| A small change | in chat | build it through the normal workflow |
| A project with a written design | a written design document | a full plan (software: `writing-plans`) |

If it grows mid-task, stop, say so, step up a size. If it's really several independent projects, agree on an order and brainstorm them one at a time.

## The Written Design

For a project, write a plain document a talented builder could plan from without going back to your human partner. Cover: intent and the why; goals, non-goals, anti-goals; constraints; the parts of the how they decided, as they decided them; what's left to the builder.

**Where it goes:** `.agent/plans/{task-slug}-design.md` (kit convention, see CLAUDE.md "Plans & Audits"), committed when the user asks for commits. Their preferences override.

**Builder check:** dispatch a fresh subagent with `builder-check-prompt.md` in this directory. Tell your human partner a reviewer will read it first and you may come back once with a few questions. Don't hand over the document until the check is back. Sort what the builder asks into three piles:

- **Answered already** by the conversation or project: put the answer in the document.
- **Minor:** a sensible builder could settle it without changing what gets built. Settle it, mark it as your call.
- **Theirs:** only your human partner can answer it and it changes what gets built.

Bring the "theirs" pile in one message, most important first. Update the document, hand it over with a short list of the calls you made. That's the only round of questions the check produces. Without a subagent tool, read the document as that builder yourself.

<HARD-GATE>
Nothing gets built until your human partner approves the full description: in chat for a small change, the document for a project. Building includes writing product code, scaffolding, installing dependencies, creating projects, invoking subagents, and invoking an implementation skill. Reading and exploring are fine.

Two exceptions. If they opted out of the questions, the skill is done and the gate goes with it (assumptions still stated). A spike they said yes to may be built; it stays labeled throwaway.

After a project's document is approved, for COMPLEX CODE / DESIGN-UI / multi-file work **offer the `execution-loop` skill** (CLAUDE.md Socratic Gate rule 5), then invoke `writing-plans` and no other skill.
</HARD-GATE>

## Red Flags

| Thought | Reality |
|---|---|
| "I'll offer options to save them effort" | Options steer. Ask them to describe it first. |
| "I'll fill in sensible defaults" | Good. Say them out loud. A default they never heard is one they couldn't reject. |
| "I should explain the process first" | Ask your question. The process shows itself. |
| "They said 'sounds good' to the idea" | Approval covers what you showed them. A description you haven't written isn't approved. |
| "The spike works, I'll keep building on it" | Keeping it is a new request. Back through the gate. |
| "They gave me answers 1, 2, 3, so the gate is cleared" | Spec-heavy is not unambiguous. Ask the 2 edge-case questions. |
| "I think..." | Uncertainty means ask instead. |

## Visual Companion

A browser tab for mockups, diagrams and prototypes. A tool, not a mode: accepting it doesn't send every question to the browser.

**Offer it just-in-time**, the first time seeing would help, never upfront. The offer is its own message with nothing else in it:

> "This might be easier if I show you. Want me to open a browser tab with some mockups?"

If they decline, stay in text and don't offer again unless they raise it. Per question, ask: would they understand this better by seeing it? Mockups, layouts, diagrams go in the browser; requirements, scope and trade-offs stay in text.

If they accept, read `visual-companion.md` in this directory before starting the server. (`scripts/start-server.sh` disables upstream telemetry by default in this kit.)

## Related files

- `dynamic-questioning.md`: question generation principles, priority (P0/P1/P2), trade-off format, domain question banks.
- `communication-protocol.md`: status board, error handling, completion message, anti-patterns (use during and after implementation).
- `builder-check-prompt.md`, `visual-companion.md`, `scripts/`: from superpowers v7.0.0.
