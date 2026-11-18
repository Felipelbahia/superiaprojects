# arquitetura-e-qualidade

Arquitetura e qualidade: padrões e decisões de arquitetura, microsserviços, CQRS e event sourcing, código limpo, refatoração, modernização, dependências, performance, débito técnico e a família ponytail (simplicidade e auditoria).

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agent/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agent/agents/<nome>.md"`; workflow: `"<HUB>/.agent/workflows/<nome>.md"`.

## Skills (17)

| Skill | Use quando |
| --- | --- |
| `architecture` | Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or analyzing system design. |
| `architecture-patterns` | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when architecting complex backend systems or refactoring existing applications for better maintainability. |
| `auditing-memory-usage` | Use when the owner says the machine or an app feels heavy, slow or memory-hungry, memory keeps growing, or asks to check a project's code for memory leaks or unnecessary memory use. |
| `clean-code` | Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments |
| `cqrs-implementation` | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems. |
| `dependency-upgrade` | Manage major dependency version upgrades with compatibility analysis, staged rollout, and comprehensive testing. Use when upgrading framework versions, updating major dependencies, or managing breaking changes in libraries. |
| `error-handling-patterns` | Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient applications. Use when implementing error handling, designing APIs, or improving application reliability. |
| `event-store-design` | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| `microservices-patterns` | Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices. |
| `performance-profiling` | Performance profiling principles. Measurement, analysis, and optimization techniques. |
| `ponytail` | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding task (writing, fixing, refactoring, reviewing, choosing dependencies) and when the user says "ponytail", "be lazy", "simplest solution", "yagni", or complains about over-engineering or bloat. Levels: lite, full (default), ultra. |
| `ponytail-audit` | Quality audit of a whole repo: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delete, merge or split. Ranked, each finding explained in plain English. One-shot report, changes nothing. Use for "audit this codebase", "review the whole repo", "find bloat", "what can I delete", /ponytail-audit. |
| `ponytail-review` | Quality review of a change: is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is every line needed. Reads the connected code, not only the diff. Each finding is explained in plain English. Use for "review this", "code review", "review the last commit", "review my PR", "is this over-engineered", /ponytail-review. |
| `projection-patterns` | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| `python-performance-optimization` | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance. |
| `react-modernization` | Upgrade React applications to latest versions, migrate from class components to hooks, and adopt concurrent features. Use when modernizing React codebases, migrating to React Hooks, or upgrading to latest React versions. |
| `saga-orchestration` | Implement saga patterns for distributed transactions and cross-aggregate workflows. Use when coordinating multi-step business processes, handling compensating transactions, or managing long-running workflows. |

## Agents (8)

| Agent | Use quando |
| --- | --- |
| `architect-review` | Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driven systems, and DDD. Reviews system designs and code changes for architectural integrity, scalability, and maintainability. Use PROACTIVELY for architectural decisions. |
| `code-archaeologist` | Expert in legacy code, refactoring, and understanding undocumented systems. Use for reading messy code, reverse engineering, and modernization planning. Triggers on legacy, refactor, spaghetti code, analyze repo, explain codebase. |
| `dx-optimizer` | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects, after team feedback, or when development friction is noticed. |
| `event-sourcing-architect` | Event sourcing, CQRS and event-driven architecture: event store design, projections, sagas, schema evolution. Use for event-sourced systems. |
| `legacy-modernizer` | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, dependency updates, and backward compatibility. Use PROACTIVELY for legacy system updates, framework migrations, or technical debt reduction. |
| `monorepo-architect` | Monorepo architecture, build systems and dependency management at scale (Nx, Turborepo, Bazel, Lerna). Use for workspace setup and CI optimization. |
| `performance-engineer` | Expert performance engineer specializing in modern observability, application optimization, and scalable system performance. Masters OpenTelemetry, distributed tracing, load testing, multi-tier caching, Core Web Vitals, and performance monitoring. Handles end-to-end optimization, real user monitoring, and scalability patterns. Use PROACTIVELY for performance optimization, observability, or scalability challenges. |
| `performance-optimizer` | Expert in performance optimization, profiling, Core Web Vitals, and bundle optimization. Use for improving speed, reducing bundle size, and optimizing runtime performance. Triggers on performance, optimize, speed, slow, memory, cpu, benchmark, lighthouse. |

## Workflows (6)

| Workflow | Use quando |
| --- | --- |
| `/code-migrate` | Code Migration Assistant |
| `/deps-upgrade` | Dependency Upgrade Strategy |
| `/legacy-modernize` | Legacy Code Modernization Workflow |
| `/performance-optimization` | Optimize application performance end-to-end using specialized performance and optimization agents |
| `/refactor-clean` | Refactor and Clean Code |
| `/tech-debt` | Technical Debt Analysis and Remediation |

