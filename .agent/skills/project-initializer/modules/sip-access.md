## Central hub (SIP - Geral)

- This project consumes the kit through the skill `sip-geral` (`.agent/skills/sip-geral`, installed at setup). Other SIPs installed here and their hub paths: `.agent/SIPS-CONSUMIDOS.md`.
- A skill, agent, workflow or script named in these rules that is not in this project: resolve it through `sip-geral` (or the SIP of its domain) and read it by absolute path in the hub. Never improvise from general knowledge when a SIP covers the subject.
- Scripts named `.agent/scripts/<script>.py` that are not local: run the hub's copy from this project's root (`python3 "<hub>/.agent/scripts/<script>.py"`, hub path in `.agent/SIPS-CONSUMIDOS.md`).
- Hub agents and workflows stay in the hub; install one locally only when the owner asks (re-run the SIP's install prompt).
