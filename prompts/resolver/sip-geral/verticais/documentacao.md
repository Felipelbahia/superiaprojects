# documentacao

Documentação: ADRs, templates, runbooks, postmortem, tutoriais, referência de API, diagramas (Mermaid, C4) e explicação de código.

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agents/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agents/agents/<nome>.md"`; workflow: `"<HUB>/.agents/workflows/<nome>.md"`.

## Skills (4)

| Skill | Use quando |
| --- | --- |
| `architecture-decision-records` | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes. |
| `documentation-templates` | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. |
| `incident-runbook-templates` | Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use when building runbooks, responding to incidents, or establishing incident response procedures. |
| `postmortem-writing` | Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writing postmortem documents, or improving incident response processes. |

## Agents (10)

| Agent | Use quando |
| --- | --- |
| `api-documenter` | Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices. Create interactive docs, generate SDKs, and build comprehensive developer portals. Use PROACTIVELY for API documentation or developer portal creation. |
| `c4-code` | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level documentation including function signatures, arguments, dependencies, and code structure. Use when documenting code at the lowest C4 level for individual directories and code modules. |
| `c4-component` | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level architecture, defining component boundaries, interfaces, and relationships. Creates component diagrams and documentation. Use when synthesizing code-level documentation into logical components. |
| `c4-container` | Expert C4 Container-level documentation specialist. Synthesizes Component-level documentation into Container-level architecture, mapping components to deployment units, documenting container interfaces as APIs, and creating container diagrams. Use when synthesizing components into deployment containers and documenting system deployment architecture. |
| `c4-context` | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, user journeys, system features, and external dependencies. Synthesizes container and component documentation with system documentation to create comprehensive context-level architecture. Use when creating the highest-level C4 system context documentation. |
| `docs-architect` | Creates comprehensive technical documentation from existing codebases. Analyzes architecture, design patterns, and implementation details to produce long-form technical manuals and ebooks. Use PROACTIVELY for system documentation, architecture guides, or technical deep-dives. |
| `documentation-writer` | Expert in technical documentation. Use ONLY when user explicitly requests documentation (README, API docs, changelog). DO NOT auto-invoke during normal development. |
| `mermaid-expert` | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. Use PROACTIVELY for visual documentation, system diagrams, or process flows. |
| `reference-builder` | Creates exhaustive technical references and API documentation. Generates comprehensive parameter listings, configuration guides, and searchable reference materials. Use PROACTIVELY for API docs, configuration references, or complete technical specifications. |
| `tutorial-engineer` | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learning experiences with hands-on examples. Use PROACTIVELY for onboarding guides, feature tutorials, or concept explanations. |

## Workflows (3)

| Workflow | Use quando |
| --- | --- |
| `/c4-architecture` | C4 Architecture Documentation Workflow |
| `/code-explain` | Code Explanation and Analysis |
| `/doc-generate` | Automated Documentation Generation |

