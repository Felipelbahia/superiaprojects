# planejamento-e-processo

Fluxo de trabalho e planejamento: brainstorming, spec, plano, loop de execução, orquestração, subagentes, handoff, pesquisa no código e criação de skills, agents e workflows.

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agents/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agents/agents/<nome>.md"`; workflow: `"<HUB>/.agents/workflows/<nome>.md"`.

## Skills (32)

| Skill | Use quando |
| --- | --- |
| `app-builder` | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. |
| `atualizar-sips` | Use when the owner wants to check whether the SIPs installed in the current project are up to date, or to update them ("atualizar os SIPs", "tem atualização dos SIPs?", "os SIPs estão em dia?", "update my SIPs", "check SIP updates"). Runs a read-only status against the project's .agents/SIPS-CONSUMIDOS.md and, with the owner's ok, re-runs each SIP's install prompt. |
| `behavioral-modes` | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. |
| `brainstorming` | Use when about to create features, build components, add functionality, modify behavior, or plan anything new, in software or out of it, and when a request is complex, vague, or unclear - the Socratic Gate, before any tool use or implementation |
| `context-driven-development` | Use this skill when working with Conductor's context-driven development methodology, managing project context artifacts, or understanding the relationship between product.md, tech-stack.md, and workflow.md files. |
| `deliverable-verification` | Use when a document, report or diagnosis is graded in an execution-loop QA, when a deliverable is assembled from several parts or registries (findings, questions, backlog), when adding a part, finding or id to such a deliverable, or when a file says it is generated and must not be edited by hand. |
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire, "it took too long", "why is it so expensive", "what is it doing" — or wants to build a bug report for the superpowers maintainers, for the current session or a past one identified by id or path, on any harness. |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is available |
| `execution-loop` | Use when starting a non-trivial new feature, build, refactor, or significant change that needs a documented, quality-gated development cycle — also called "Loop de Execução" — before writing implementation code. |
| `intelligent-routing` | Automatic agent selection and intelligent task routing. Analyzes user requests and automatically selects the best specialist agent(s) without requiring explicit user mentions. |
| `launch-readiness` | Use when an app or site built with AI is about to be published or launched, or the user asks for a pre-launch, go-live or "antes de lançar" check beyond code security - email deliverability, app store submission, chatbot risk, kill switch and spend caps, broken links, legal and privacy exposure. |
| `mapa-de-destinos` | Use when about to save a deliverable that is not source code (report, document, content piece, campaign, press material, data export, workflow export, study) and the project has no documented place for it, when creating or aligning a project, when a project gains more than one brand or product, or when someone asks where a kind of file should go. |
| `opus-haiku` | Use when the user invokes /opus-haiku or asks to save plan usage by delegating code writing to a cheaper model while the main model plans and reviews, and in the Execução phase of the execution-loop. |
| `oss-scout` | Use when a project needs a capability that a mature library or service may already solve (login, payments, PDF, dates and time zones, rich text, drag and drop), before installing or recommending any package, or when asked to study, compare or take parts from open source projects. |
| `parallel-agents` | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives. |
| `plan-writing` | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. |
| `project-defines` | Use when a new application or system must be planned, specified and built step by step, when a project contains a _projectdefines/ folder and anything is about to be built, changed or reviewed, or when an owner who does not program needs a safe, lean build path. |
| `project-initializer` | Use when starting a new project from scratch, when user says "Quero criar um projeto novo com base na skill", or when requested to initialize greenfield project setup. |
| `session-handoff` | Use when ending a session with unfinished work that another session will need to continue, or when starting a session that resumes someone else's (or your own past) handoff — captures task status, decisions, learnings, and next steps without losing context. |
| `skill-resolver` | Use whenever a capability seems relevant to the current task but no matching skill appears in the currently loaded skills list, or the Skill tool answers "Unknown skill" for a skill the project rules name — common in Antigravity Kit projects (any repo with a .agents/skills/ directory, or a CLAUDE.md/AGENTS.md that references "0 Padrões"), because Claude Code only auto-discovers SKILL.md files under .claude/skills/ and ~/.claude/skills/, never under .agents/skills/ or inside a hub. Also use when the user names a skill that doesn't show up in the listing, or asks "existe skill pra isso", "do we have a skill for X", "check 0 Padrões for a skill". Runs resolve_skill.py, which searches the project, the SIP hubs it consumes and the kit. This is the fallback for projects with no SIP installed; where `sip-geral` is installed, its resolver covers the same ground. |
| `spec-writing` | Use when a feature or change needs a written specification — Problem, Solution, User Stories, Decisions — before planning or implementation begins, turning what's already been discussed into a concrete document instead of an implicit shared understanding. |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `superiaprojects-criar-sip` | Use quando o usuário quiser transformar um projeto/repositório em um "SIP" (Super IA Projects) — um repositório central de Skills, Agents, Workflows e Conhecimento de um domínio que outros projetos possam consultar, quase como um agente especializado daquele domínio. Dispara em pedidos como "cria um SIP de marketing", "transforma esse repo num hub de X", "quero um repositório central pra Y como fizemos com o n8n", ou quando o usuário referencia o `SIP - N8N` como modelo a replicar para um novo domínio. Faz o scaffolding da skill resolver (`sip-<dominio>`), do prompt de instalação, do inbox de contribuições e do registro na ficha do projeto — não cria o conhecimento de domínio em si (isso é trabalho de skills/agents específicos, feitos depois). |
| `track-management` | Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations. |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `workflow-orchestration-patterns` | Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determinism constraints. Use when building long-running processes, distributed transactions, or microservice orchestration. |
| `workflow-patterns` | Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks, or understanding the verification protocol. |
| `writing-agents` | Use when creating a new agent for the kit, adding memory or learning to an agent, deciding how much autonomy an agent has, or reviewing whether an agent file follows the kit's model. |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

## Agents (11)

| Agent | Use quando |
| --- | --- |
| `codebase-analyzer` | Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components. As always, the more detailed your request prompt, the better! :) |
| `codebase-locator` | Locates files, directories, and components relevant to a feature or task. Call `codebase-locator` with human language prompt describing what you're looking for. Basically a "Super Grep/Glob/LS tool" — Use it if you find yourself desiring to use one of these tools more than once. |
| `codebase-pattern-finder` | codebase-pattern-finder is a useful subagent_type for finding similar implementations, usage examples, or existing patterns that can be modeled after. It will give you concrete code examples based on what you're looking for! It's sorta like codebase-locator, but it will not only tell you the location of files, it will also give you code details! |
| `conductor-validator` | Validates Conductor project artifacts for completeness, consistency, and correctness. Use after setup, when diagnosing issues, or before implementation to verify project context. |
| `context-manager` | Elite AI context engineering specialist mastering dynamic context management, vector databases, knowledge graphs, and intelligent memory systems. Orchestrates context across multi-agent workflows, enterprise AI systems, and long-running projects with 2024/2025 best practices. Use PROACTIVELY for complex AI orchestration. |
| `explorer-agent` | Advanced codebase discovery, deep architectural analysis, and proactive research agent. The eyes and ears of the framework. Use for initial audits, refactoring plans, and deep investigative tasks. |
| `orchestrator` | Multi-agent coordination and task orchestration. Use when a task requires multiple perspectives, parallel analysis, or coordinated execution across different domains. Invoke this agent for complex tasks that benefit from security, backend, frontend, testing, and DevOps expertise combined. |
| `search-specialist` | Expert web researcher using advanced search techniques and synthesis. Masters search operators, result filtering, and multi-source verification. Handles competitive analysis and fact-checking. Use PROACTIVELY for deep research, information gathering, or trend analysis. |
| `thoughts-analyzer` | The research equivalent of codebase-analyzer. Use this subagent_type when wanting to deep dive on a research topic. Not commonly needed otherwise. |
| `thoughts-locator` | Discovers relevant documents in thoughts/ directory (We use this for all sorts of metadata storage!). This is really only relevant/needed when you're in a reseaching mood and need to figure out if we have random thoughts written down that are relevant to your current research task. Based on the name, I imagine you can guess this is the `thoughts` equivilent of `codebase-locator` |
| `web-search-researcher` | Do you find yourself desiring information that you don't quite feel well-trained (confident) on? Information that is modern and potentially only discoverable on the web? Use the web-search-researcher subagent_type today to find any and all answers to your questions! It will research deeply to figure out and attempt to answer your questions! If you aren't immediately satisfied you can get your money back! (Not really - but you can re-run web-search-researcher with an altered prompt in the event you're not satisfied the first time) |

## Workflows (31)

| Workflow | Use quando |
| --- | --- |
| `/brainstorm` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores requirements and design before implementation. |
| `/context-restore` | Context Restoration: Advanced Semantic Memory Rehydration |
| `/context-save` | Context Save Tool: Intelligent Context Management Specialist |
| `/create` | Create new application command. Triggers App Builder skill and starts interactive dialogue with user. |
| `/create_plan` | Create detailed implementation plans through interactive research and iteration |
| `/create_plan_generic` | Create detailed implementation plans with thorough research and iteration |
| `/create_plan_nt` | Create implementation plans with thorough research (no thoughts directory) |
| `/enhance` | Add or update features in existing application. Used for iterative development. |
| `/execute-plan` | Execute plan in batches with review checkpoints |
| `/feature-development` | Orchestrate end-to-end feature development from requirements to production deployment |
| `/implement` | Execute tasks from a track's implementation plan following TDD workflow |
| `/implement_plan` | Implement technical plans from thoughts/shared/plans with verification |
| `/iterate_plan` | Iterate on existing implementation plans with thorough research and updates |
| `/iterate_plan_nt` | Iterate on existing implementation plans with thorough research and updates |
| `/manage` | Manage track lifecycle: archive, restore, delete, rename, and cleanup |
| `/new-track` | Create a new track with specification and phased implementation plan |
| `/oneshot` | Research ticket and launch planning session |
| `/oneshot_plan` | Execute ralph plan and implementation for a ticket |
| `/orchestrate` | Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise. |
| `/plan` | Create project plan using project-planner agent. No code writing - only plan file generation. |
| `/ralph_impl` | Implement highest priority small Linear ticket with worktree setup |
| `/ralph_plan` | Create implementation plan for highest priority Linear ticket ready for spec |
| `/ralph_research` | Research highest priority Linear ticket needing investigation |
| `/research_codebase` | Document codebase as-is with thoughts directory for historical context |
| `/research_codebase_generic` | Research codebase comprehensively using parallel sub-agents |
| `/research_codebase_nt` | Document codebase as-is without evaluation or recommendations |
| `/setup` | Initialize project with Conductor artifacts (product definition, tech stack, workflow, style guides) |
| `/status` | Display project status, active tracks, and next actions |
| `/validate_plan` | Validate implementation against plan, verify success criteria, identify issues |
| `/workflow-automate` | Workflow Automation |
| `/write-plan` | Create detailed implementation plan with bite-sized tasks |

