## Interface rules

- **Primary agent by interface:**

  | Interface | Agent | Skills |
  |---|---|---|
  | Web | `frontend-specialist` | `frontend-design` |
  | Mobile | `mobile-developer` (never `frontend-specialist`) | `mobile-design` |
  | Astro site | `frontend-specialist` | `astro-development` via `sip-astro` |

- Design rules (palette bans, anti-cliché, design thinking) live in the agent file: read it before any UI work.
- **Stitch MCP (suggest for design):** before coding a new screen, a layout variant or a design system, offer to design it in Stitch (`generate_screen_from_text`, `generate_variants`, `create_design_system`); the owner decides. If used, the code follows the approved screen.
- **shadcn MCP (mandatory for components in React-based web UI: Next.js, Vite, Remix, Astro with React):** build the interface from shadcn registry components through the shadcn MCP before writing a component of your own; write one only when the registry has nothing that fits, and say so. MCP not configured in the project: propose `npx shadcn@latest mcp init --client claude` and run it only after the owner confirms (it writes `.mcp.json`; restart and check `/mcp` shows `Connected`). Not React: does not apply.
- **Context7 MCP (mandatory for UI libraries):** CSS frameworks, component kits, animation and icon libraries go through Context7 before use, like any other library.
- An MCP unavailable: say so; if the owner chose Stitch and it is unavailable, describe the screen in text for approval; without the shadcn MCP, use the shadcn CLI and its docs through Context7.
- After a UI change: run `ux_audit.py` and `accessibility_checker.py` (skill `frontend-design`) and show the output.
