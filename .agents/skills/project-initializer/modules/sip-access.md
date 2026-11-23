## Central hub (SIP - Geral)

- This project consumes the kit through the skill `sip-geral` (`.agents/skills/sip-geral`, installed at setup). Other SIPs installed here and their hub paths: `.agents/SIPS-CONSUMIDOS.md`.
- A skill, agent, workflow or script named in these rules that is not in this project: resolve it through `sip-geral` (or the SIP of its domain) and read it by absolute path in the hub. Never improvise from general knowledge when a SIP covers the subject.
- When the task needs a domain SIP (`sip-<name>`) named in these rules and it is not installed here: read its pointer at `<kit>/.agents/skills/sip-<name>/SKILL.md` (kit path: the `sip-geral` hub in `.agents/SIPS-CONSUMIDOS.md`; the pointer gives the domain hub path) and offer the owner to install it (the SIP's install prompt).
- Scripts named `.agents/scripts/<script>.py` that are not local: run the hub's copy from this project's root (`python3 "<hub>/.agents/scripts/<script>.py"`, hub path in `.agents/SIPS-CONSUMIDOS.md`).
- Hub agents and workflows stay in the hub; install one locally only when the owner asks (re-run the SIP's install prompt).
