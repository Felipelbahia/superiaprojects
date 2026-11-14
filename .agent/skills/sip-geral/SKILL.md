---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: sip-geral
description: Use when the current task involves general software engineering, architecture, backend, frontend, mobile, database, testing, security, DevOps, AI/ML or development workflows (spec, planning, execution-loop, TDD, debugging) in any project other than "SIP - Geral" (0 Padrões) itself, or when the user asks "existe algo no 0 Padrões pra isso", "tem skill/agent/workflow pra isso no hub geral", "consulta o SIP - Geral", or names a 0 Padrões skill, agent or workflow explicitly in a consumer project.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---

# sip-geral

## Por que isso existe

O projeto `SIP - Geral` (`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões`) é a referência central de
conhecimento em geral. Esse conhecimento só é descoberto automaticamente
dentro do próprio hub. Em qualquer outro projeto, nada aponta para ele — sem
esta skill, a IA tende a reinventar padrões do zero. Esta skill é o ponteiro
que faz a ponte: ela mesma não ensina geral, ela leva até quem ensina.

## Passo 0 — acesso ao caminho

Leitura de arquivo fora do diretório de trabalho pode pedir aprovação do
usuario na primeira vez — isso é esperado. Sempre use o caminho absoluto entre
aspas: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões"`.

## Passo 1 — classifique a tarefa

| Tipo de tarefa | O que fazer |
| --- | --- |
| **Consulta pontual** | **Modo consulta** — leia só os arquivos relevantes e aplique inline. |
| **Construção grande / multi-arquivo** | **Modo dispatch** — abra um subagente carregado com a persona do hub. |

## Modo consulta (padrão — prefira este)

1. Ache a linha que bate com o pedido nas tabelas abaixo (Skills, Agents,
   Workflows): elas são o roteador do hub. Se o hub tiver um roteador mestre
   para casos ambíguos, leia-o:
   `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/intelligent-routing/SKILL.md"`
2. Leia só o arquivo do item escolhido, por caminho absoluto no hub
   (`"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/<nome>/SKILL.md"`). Nunca symlinke nem copie
   skills especialistas do hub para o projeto.
3. Aplique o conteúdo inline. Avise o usuário em uma linha que a resposta veio
   do hub `SIP - Geral`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

Não existe invocação nativa de agente cross-projeto no Claude Code. "Disparar"
o agente do hub é montar um subagente genérico (`Agent`,
`subagent_type: "general-purpose"`) com a persona do hub colada no prompt:

1. Leia a persona do agente especialista do hub (se existir, em
   `.agent/agents/`).
2. Leia a(s) skill(s) relevante(s) do hub.
3. Chame `Agent` com o conteúdo colado + a tarefa concreta.
4. Valide o resultado contra a skill de validação do hub (se existir) antes de
   aplicar.

## Skills do hub

Arquivo: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/<nome>/SKILL.md"`.

<!-- skills:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 202.

| Skill | Use quando |
| --- | --- |
| `accessibility-compliance` | Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support. Use when auditing accessibility, implementing ARIA patterns, building for screen readers, or ensuring inclusive user experiences. |
| `airflow-dag-patterns` | Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs. |
| `angular-migration` | Migrate from AngularJS to Angular using hybrid mode, incremental component rewriting, and dependency injection updates. Use when upgrading AngularJS applications, planning framework migrations, or modernizing legacy Angular code. |
| `anti-reversing-techniques` | Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use when analyzing protected binaries, bypassing anti-debugging for authorized analysis, or understanding software protection mechanisms. |
| `api-design-principles` | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewing API specifications, or establishing API design standards. |
| `api-patterns` | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. |
| `app-builder` | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. |
| `architecture` | Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or analyzing system design. |
| `architecture-decision-records` | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes. |
| `architecture-patterns` | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when architecting complex backend systems or refactoring existing applications for better maintainability. |
| `async-python-patterns` | Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations. |
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. |
| `auth-implementation-patterns` | Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access control systems. Use when implementing auth systems, securing APIs, or debugging security issues. |
| `backtesting-frameworks` | Build robust backtesting systems for trading strategies with proper handling of look-ahead bias, survivorship bias, and transaction costs. Use when developing trading algorithms, validating strategies, or building backtesting infrastructure. |
| `bash-defensive-patterns` | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety. |
| `bash-linux` | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. |
| `bats-testing-patterns` | Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities. |
| `bazel-build-optimization` | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterprise codebases. |
| `behavioral-modes` | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. |
| `billing-automation` | Build automated billing systems for recurring payments, invoicing, subscription lifecycle, and dunning management. Use when implementing subscription billing, automating invoicing, or managing recurring payment systems. |
| `binary-analysis-patterns` | Master binary analysis patterns including disassembly, decompilation, control flow analysis, and code pattern recognition. Use when analyzing executables, understanding compiled code, or performing static analysis on binaries. |
| `brainstorming` | Use when about to create features, build components, add functionality, modify behavior, or plan anything new, in software or out of it, and when a request is complex, vague, or unclear - the Socratic Gate, before any tool use or implementation |
| `changelog-automation` | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions. |
| `claude-code-review` | Use when setting up, tuning or running Claude Code Review (managed GitHub PR review, REVIEW.md, @claude review) or the local /code-review command, when review findings are noisy, missing or costly, or when gating merges on automated review severity. Also for revisão de PR automatizada and ultrareview requests. |
| `claude-security-scan` | Use when scanning a repository, branch diff, pull request or commit for vulnerabilities with the Claude Security plugin (/claude-security), reading CLAUDE-SECURITY reports (md, jsonl, SARIF), turning findings into reviewed patches, or choosing between security-review, deep scan, Code Review and CI scanners. Also for varredura de vulnerabilidades. |
| `clean-code` | Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments |
| `code-review-checklist` | Code review guidelines covering code quality, security, and best practices. |
| `code-review-excellence` | Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining team morale. Use when reviewing pull requests, establishing review standards, or mentoring developers. |
| `competitive-landscape` | This skill should be used when the user asks to "analyze competitors", "assess competitive landscape", "identify differentiation", "evaluate market positioning", "apply Porter's Five Forces", or requests competitive strategy analysis. |
| `context-driven-development` | Use this skill when working with Conductor's context-driven development methodology, managing project context artifacts, or understanding the relationship between product.md, tech-stack.md, and workflow.md files. |
| `cost-optimization` | Optimize cloud costs through resource rightsizing, tagging strategies, reserved instances, and spending analysis. Use when reducing cloud expenses, analyzing infrastructure costs, or implementing cost governance policies. |
| `cqrs-implementation` | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems. |
| `data-quality-frameworks` | Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts. |
| `data-storytelling` | Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creating data reports, or building executive presentations. |
| `database-design` | Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. |
| `database-migration` | Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies. |
| `dbt-transformation-patterns` | Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies. Use when building data transformations, creating data models, or implementing analytics engineering best practices. |
| `debugging-strategies` | Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or technology stack. Use when investigating bugs, performance issues, or unexpected behavior. |
| `defi-protocol-templates` | Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentralized finance applications or smart contract protocols. |
| `deliverable-verification` | Use when a document, report or diagnosis is graded in an execution-loop QA, when a deliverable is assembled from several parts or registries (findings, questions, backlog), when adding a part, finding or id to such a deliverable, or when a file says it is generated and must not be edited by hand. |
| `dependency-upgrade` | Manage major dependency version upgrades with compatibility analysis, staged rollout, and comprehensive testing. Use when upgrading framework versions, updating major dependencies, or managing breaking changes in libraries. |
| `deployment-pipeline-design` | Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Use when architecting deployment workflows, setting up continuous delivery, or implementing GitOps practices. |
| `deployment-procedures` | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. |
| `design-system-patterns` | Build scalable design systems with design tokens, theming infrastructure, and component architecture patterns. Use when creating design tokens, implementing theme switching, building component libraries, or establishing design system foundations. |
| `design-system-prompts` | A collection of prompts and workflows to build a complete design system, components, and pages using shadcn/ui. |
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire, "it took too long", "why is it so expensive", "what is it doing" — or wants to build a bug report for the superpowers maintainers, for the current session or a past one identified by id or path, on any harness. |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `distributed-tracing` | Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Use when debugging microservices, analyzing request flows, or implementing observability for distributed systems. |
| `documentation-templates` | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. |
| `dotnet-backend-patterns` | Master C#/.NET backend development patterns for building robust APIs, MCP servers, and enterprise applications. Covers async/await, dependency injection, Entity Framework Core, Dapper, configuration, caching, and testing with xUnit. Use when developing .NET backends, reviewing C# code, or designing API architectures. |
| `e2e-testing-patterns` | Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs, improve confidence, and enable fast deployment. Use when implementing E2E tests, debugging flaky tests, or establishing testing standards. |
| `embedding-strategies` | Select and optimize embedding models for semantic search and RAG applications. Use when choosing embedding models, implementing chunking strategies, or optimizing embedding quality for specific domains. |
| `employment-contract-templates` | Create employment contracts, offer letters, and HR policy documents following legal best practices. Use when drafting employment agreements, creating HR policies, or standardizing employment documentation. |
| `error-handling-patterns` | Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient applications. Use when implementing error handling, designing APIs, or improving application reliability. |
| `event-store-design` | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is available |
| `execution-loop` | Use when starting a non-trivial new feature, build, refactor, or significant change that needs a documented, quality-gated development cycle — also called "Loop de Execução" — before writing implementation code. |
| `fastapi-templates` | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects. |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `frontend-design` | Design thinking and decision-making for web UI. Use when designing components, layouts, color schemes, typography, or creating aesthetic interfaces. Teaches principles, not fixed values. |
| `game-development` | Game development orchestrator. Routes to platform-specific skills based on project needs. |
| `gdpr-data-handling` | Implement GDPR-compliant data handling with consent management, data subject rights, and privacy by design. Use when building systems that process EU personal data, implementing privacy controls, or conducting GDPR compliance reviews. |
| `geo-fundamentals` | Generative Engine Optimization for AI search engines (ChatGPT, Claude, Perplexity). |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Use when managing complex Git histories, collaborating on feature branches, or troubleshooting repository issues. |
| `github-actions-templates` | Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD with GitHub Actions, automating development workflows, or creating reusable workflow templates. |
| `github-publisher` | Use when the user asks to publish, upload or push a local folder or project to GitHub for the first time, create a new GitHub repository from existing code, or "subir o projeto pro GitHub" / "criar repositório", and when a repository is about to be shared (made public, a collaborator added, the link sent to someone) - including when they say it is already clean or they are in a hurry. |
| `gitlab-ci-patterns` | Build GitLab CI/CD pipelines with multi-stage workflows, caching, and distributed runners for scalable automation. Use when implementing GitLab CI/CD, optimizing pipeline performance, or setting up automated testing and deployment. |
| `gitops-workflow` | Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation. Use when implementing GitOps practices, automating Kubernetes deployments, or setting up declarative infrastructure management. |
| `go-concurrency-patterns` | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions. |
| `godot-gdscript-patterns` | Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices. |
| `grafana-dashboards` | Create and manage production Grafana dashboards for real-time visualization of system and application metrics. Use when building monitoring dashboards, visualizing metrics, or creating operational observability interfaces. |
| `helm-chart-scaffolding` | Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments. |
| `hybrid-cloud-networking` | Configure secure, high-performance connectivity between on-premises infrastructure and cloud platforms using VPN and dedicated connections. Use when building hybrid cloud architectures, connecting data centers to cloud, or implementing secure cross-premises networking. |
| `hybrid-search-implementation` | Combine vector and keyword search for improved retrieval. Use when implementing RAG systems, building search engines, or when neither approach alone provides sufficient recall. |
| `i18n-localization` | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. |
| `incident-runbook-templates` | Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use when building runbooks, responding to incidents, or establishing incident response procedures. |
| `intelligent-routing` | Automatic agent selection and intelligent task routing. Analyzes user requests and automatically selects the best specialist agent(s) without requiring explicit user mentions. |
| `interaction-design` | Design and implement microinteractions, motion design, transitions, and user feedback patterns. Use when adding polish to UI interactions, implementing loading states, or creating delightful user experiences. |
| `istio-traffic-management` | Configure Istio traffic management including routing, load balancing, circuit breakers, and canary deployments. Use when implementing service mesh traffic policies, progressive delivery, or resilience patterns. |
| `javascript-testing-patterns` | Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows. |
| `k8s-manifest-generator` | Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations. |
| `k8s-security-policies` | Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when securing Kubernetes clusters, implementing network isolation, or enforcing pod security standards. |
| `kpi-dashboard-design` | Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use when building business dashboards, selecting metrics, or designing data visualization layouts. |
| `landing-page-copy-optimizer` | Analyze and optimize landing page copy using April Dunford's positioning methodology. Use when user wants to evaluate SaaS landing page copy, improve conversion-focused messaging, apply positioning framework (competitive alternatives, unique features, value themes, target customers, market category), or generate prompts for vibe coding tools (Replit, Lovable). Triggers on requests like "analyze my landing page", "improve my website copy", "help with positioning", "optimize my SaaS page", or when user shares a landing page URL for review. |
| `langchain-architecture` | Design LLM applications using LangChain 1.x and LangGraph for agents, memory, and tool integration. Use when building LangChain applications, implementing AI agents, or creating complex LLM workflows. |
| `launch-readiness` | Use when an app or site built with AI is about to be published or launched, or the user asks for a pre-launch, go-live or "antes de lançar" check beyond code security - email deliverability, app store submission, chatbot risk, kill switch and spend caps, broken links, legal and privacy exposure. |
| `linkerd-patterns` | Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configuring traffic policies, or implementing zero-trust networking with minimal overhead. |
| `lint-and-validate` | Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standards. Triggers onKeywords: lint, format, check, validate, types, static analysis. |
| `llm-evaluation` | Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking. Use when testing LLM performance, measuring AI application quality, or establishing evaluation frameworks. |
| `mapa-de-destinos` | Use when about to save a deliverable that is not source code (report, document, content piece, campaign, press material, data export, workflow export, study) and the project has no documented place for it, when creating or aligning a project, when a project gains more than one brand or product, or when someone asks where a kind of file should go. |
| `market-sizing-analysis` | This skill should be used when the user asks to "calculate TAM", "determine SAM", "estimate SOM", "size the market", "calculate market opportunity", "what's the total addressable market", or requests market sizing analysis for a startup or business opportunity. |
| `mcp-builder` | MCP (Model Context Protocol) server building principles. Tool design, resource patterns, best practices. |
| `memory-forensics` | Master memory forensics techniques including memory acquisition, process analysis, and artifact extraction using Volatility and related tools. Use when analyzing memory dumps, investigating incidents, or performing malware analysis from RAM captures. |
| `memory-safety-patterns` | Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing safe systems code, managing resources, or preventing memory bugs. |
| `microservices-patterns` | Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices. |
| `ml-pipeline-workflow` | Build end-to-end MLOps pipelines from data preparation through model training, validation, and production deployment. Use when creating ML pipelines, implementing MLOps practices, or automating model training and deployment workflows. |
| `mobile-android-design` | Master Material Design 3 and Jetpack Compose patterns for building native Android apps. Use when designing Android interfaces, implementing Compose UI, or following Google's Material Design guidelines. |
| `mobile-design` | Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native mobile apps. |
| `mobile-ios-design` | Master iOS Human Interface Guidelines and SwiftUI patterns for building native iOS apps. Use when designing iOS interfaces, implementing SwiftUI views, or ensuring apps follow Apple's design principles. |
| `modern-javascript-patterns` | Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns for writing clean, efficient JavaScript code. Use when refactoring legacy code, implementing modern patterns, or optimizing JavaScript applications. |
| `monorepo-management` | Master monorepo management with Turborepo, Nx, and pnpm workspaces to build efficient, scalable multi-package repositories with optimized builds and dependency management. Use when setting up monorepos, optimizing builds, or managing shared dependencies. |
| `mtls-configuration` | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate management, or securing internal service communication. |
| `multi-cloud-architecture` | Design multi-cloud architectures using a decision framework to select and integrate services across AWS, Azure, and GCP. Use when building multi-cloud systems, avoiding vendor lock-in, or leveraging best-of-breed services from multiple providers. |
| `nextjs-app-router-patterns` | Master Next.js 14+ App Router with Server Components, streaming, parallel routes, and advanced data fetching. Use when building Next.js applications, implementing SSR/SSG, or optimizing React Server Components. |
| `nextjs-best-practices` | Next.js App Router principles. Server Components, data fetching, routing patterns. |
| `nft-standards` | Implement NFT standards (ERC-721, ERC-1155) with proper metadata handling, minting strategies, and marketplace integration. Use when creating NFT contracts, building NFT marketplaces, or implementing digital asset systems. |
| `nodejs-backend-patterns` | Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integration, and API design best practices. Use when creating Node.js servers, REST APIs, GraphQL backends, or microservices architectures. |
| `nodejs-best-practices` | Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying. |
| `nx-workspace-patterns` | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands. |
| `on-call-handoff-patterns` | Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use when transitioning on-call responsibilities, documenting shift summaries, or improving on-call processes. |
| `openapi-spec-generation` | Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance. |
| `opus-haiku` | Use when the user invokes /opus-haiku or asks to save plan usage by delegating code writing to a cheaper model while the main model plans and reviews, and in the Execução phase of the execution-loop. |
| `oss-scout` | Use when a project needs a capability that a mature library or service may already solve (login, payments, PDF, dates and time zones, rich text, drag and drop), before installing or recommending any package, or when asked to study, compare or take parts from open source projects. |
| `parallel-agents` | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives. |
| `paypal-integration` | Integrate PayPal payment processing with support for express checkout, subscriptions, and refund management. Use when implementing PayPal payments, processing online transactions, or building e-commerce checkout flows. |
| `pci-compliance` | Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment processing, achieving PCI compliance, or implementing payment card security measures. |
| `performance-profiling` | Performance profiling principles. Measurement, analysis, and optimization techniques. |
| `plan-writing` | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. |
| `ponytail` | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding task (writing, fixing, refactoring, reviewing, choosing dependencies) and when the user says "ponytail", "be lazy", "simplest solution", "yagni", or complains about over-engineering or bloat. Levels: lite, full (default), ultra. |
| `ponytail-audit` | Quality audit of a whole repo: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delete, merge or split. Ranked, each finding explained in plain English. One-shot report, changes nothing. Use for "audit this codebase", "review the whole repo", "find bloat", "what can I delete", /ponytail-audit. |
| `ponytail-review` | Quality review of a change: is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is every line needed. Reads the connected code, not only the diff. Each finding is explained in plain English. Use for "review this", "code review", "review the last commit", "review my PR", "is this over-engineered", /ponytail-review. |
| `postgresql` | Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features |
| `postmortem-writing` | Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writing postmortem documents, or improving incident response processes. |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. |
| `project-defines` | Use when a new application or system must be planned, specified and built step by step, when a project contains a _projectdefines/ folder and anything is about to be built, changed or reviewed, or when an owner who does not program needs a safe, lean build path. |
| `project-initializer` | Use when starting a new project from scratch, when user says "Quero criar um projeto novo com base na skill", or when requested to initialize greenfield project setup. |
| `projection-patterns` | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| `prometheus-configuration` | Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Use when implementing metrics collection, setting up monitoring infrastructure, or configuring alerting systems. |
| `prompt-engineering-patterns` | Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability in production. Use when optimizing prompts, improving LLM outputs, or designing production prompt templates. |
| `protocol-reverse-engineering` | Master network protocol reverse engineering including packet analysis, protocol dissection, and custom protocol documentation. Use when analyzing network traffic, understanding proprietary protocols, or debugging network communication. |
| `python-packaging` | Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Use when packaging Python libraries, creating CLI tools, or distributing Python code. |
| `python-patterns` | Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying. |
| `python-performance-optimization` | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance. |
| `python-testing-patterns` | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices. |
| `rag-implementation` | Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases. |
| `react-modernization` | Upgrade React applications to latest versions, migrate from class components to hooks, and adopt concurrent features. Use when modernizing React codebases, migrating to React Hooks, or upgrading to latest React versions. |
| `react-native-architecture` | Build production React Native apps with Expo, navigation, native modules, offline sync, and cross-platform patterns. Use when developing mobile apps, implementing native integrations, or architecting React Native projects. |
| `react-native-design` | Master React Native styling, navigation, and Reanimated animations for cross-platform mobile development. Use when building React Native apps, implementing navigation patterns, or creating performant animations. |
| `react-patterns` | Modern React patterns and principles. Hooks, composition, performance, TypeScript best practices. |
| `react-state-management` | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions. |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| `red-team-tactics` | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `responsive-design` | Implement modern responsive layouts using container queries, fluid typography, CSS Grid, and mobile-first breakpoint strategies. Use when building adaptive interfaces, implementing fluid layouts, or creating component-level responsive behavior. |
| `risk-metrics-calculation` | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems. |
| `rust-async-patterns` | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementing concurrent systems, or debugging async code. |
| `saga-orchestration` | Implement saga patterns for distributed transactions and cross-aggregate workflows. Use when coordinating multi-step business processes, handling compensating transactions, or managing long-running workflows. |
| `sast-configuration` | Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Use when setting up security scanning, implementing DevSecOps practices, or automating code vulnerability detection. |
| `screen-reader-testing` | Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibility issues, or ensuring assistive technology support. |
| `secrets-management` | Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive credentials, rotating secrets, or securing CI/CD environments. |
| `security-guidance-plugin` | Use when enabling, tuning or debugging the Claude Code security-guidance plugin that reviews Claude's own edits for vulnerabilities during a session, when adding custom security rules or patterns to it, or when writing code that uses eval or exec, unsafe deserialization, raw DOM injection or CI workflow files. Also for avisos de segurança durante a edição. |
| `security-requirement-extraction` | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases. |
| `seo-fundamentals` | SEO fundamentals, E-E-A-T, Core Web Vitals, and Google algorithm principles. |
| `server-management` | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. |
| `service-mesh-observability` | Implement comprehensive observability for service meshes including distributed tracing, metrics, and visualization. Use when setting up mesh monitoring, debugging latency issues, or implementing SLOs for service communication. |
| `session-handoff` | Use when ending a session with unfinished work that another session will need to continue, or when starting a session that resumes someone else's (or your own past) handoff — captures task status, decisions, learnings, and next steps without losing context. |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability. |
| `similarity-search-patterns` | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance. |
| `skill-resolver` | Use whenever a capability seems relevant to the current task but no matching skill appears in the currently loaded skills list — this is common in Antigravity Kit projects (any repo with a .agent/skills/ directory, or a CLAUDE.md/AGENTS.md that references "0 Padrões"), because Claude Code only auto-discovers SKILL.md files under .claude/skills/ and ~/.claude/skills/, never under .agent/skills/. Also use when the user names a skill by name that doesn't show up in the listing, or asks things like "existe skill pra isso", "do we have a skill for X", "check 0 Padrões for a skill". Searches the project's own .agent/skills/ (and .agents/skills/ for older, unmigrated setups), then the global library at 0 Padrões/.agent/skills/, then 0 Mkt/ for marketing, SEO, copywriting or growth topics. |
| `slo-implementation` | Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establishing reliability targets, implementing SRE practices, or measuring service performance. |
| `solidity-security` | Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing smart contracts, auditing existing contracts, or implementing security measures for blockchain applications. |
| `spark-optimization` | Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, debugging slow jobs, or scaling data processing pipelines. |
| `spec-writing` | Use when a feature or change needs a written specification — Problem, Solution, User Stories, Decisions — before planning or implementation begins, turning what's already been discussed into a concrete document instead of an implicit shared understanding. |
| `sql-optimization-patterns` | Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use when debugging slow queries, designing database schemas, or optimizing application performance. |
| `startup-financial-modeling` | This skill should be used when the user asks to "create financial projections", "build a financial model", "forecast revenue", "calculate burn rate", "estimate runway", "model cash flow", or requests 3-5 year financial planning for a startup. |
| `startup-metrics-framework` | This skill should be used when the user asks about "key startup metrics", "SaaS metrics", "CAC and LTV", "unit economics", "burn multiple", "rule of 40", "marketplace metrics", or requests guidance on tracking and optimizing business performance metrics. |
| `stride-analysis-patterns` | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating security documentation. |
| `stripe-integration` | Implement Stripe payment processing for robust, PCI-compliant payment flows including checkout, subscriptions, and webhooks. Use when integrating Stripe payments, building subscription systems, or implementing secure checkout flows. |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `supabase` | Use when a project creates, reads or writes a Supabase database, sets up its .env, writes migrations, or when the owner works with several Supabase databases (each with its own login) and must not mix them up. |
| `superiaprojects-criar-sip` | Use quando o usuário quiser transformar um projeto/repositório em um "SIP" (Super IA Projects) — um repositório central de Skills, Agents, Workflows e Conhecimento de um domínio que outros projetos possam consultar, quase como um agente especializado daquele domínio. Dispara em pedidos como "cria um SIP de marketing", "transforma esse repo num hub de X", "quero um repositório central pra Y como fizemos com o n8n", ou quando o usuário referencia o `SIP - N8N` como modelo a replicar para um novo domínio. Faz o scaffolding da skill resolver (`sip-<dominio>`), do prompt de instalação, do inbox de contribuições e do registro na ficha do projeto — não cria o conhecimento de domínio em si (isso é trabalho de skills/agents específicos, feitos depois). |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns. |
| `tailwind-patterns` | Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture. |
| `tdd-workflow` | Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. |
| `team-composition-analysis` | This skill should be used when the user asks to "plan team structure", "determine hiring needs", "design org chart", "calculate compensation", "plan equity allocation", or requests organizational design and headcount planning for a startup. |
| `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integration testing, replay testing, and local development setup. Use when implementing Temporal workflow tests or debugging test failures. |
| `terraform-module-library` | Build reusable Terraform modules for AWS, Azure, and GCP infrastructure following infrastructure-as-code best practices. Use when creating infrastructure modules, standardizing cloud provisioning, or implementing reusable IaC components. |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `testing-patterns` | Testing patterns and principles. Unit, integration, mocking strategies. |
| `threat-mitigation-mapping` | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness. |
| `track-management` | Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations. |
| `turborepo-caching` | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or implementing distributed caching. |
| `typescript-advanced-types` | Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for building type-safe applications. Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety in TypeScript projects. |
| `ui-ux-pro-max` | UI/UX design intelligence - styles, color palettes, font pairings, UX guidelines and stack-specific reasoning rules. Use when designing or reviewing interfaces, landing pages, dashboards or design systems. |
| `unity-ecs-patterns` | Master Unity ECS (Entity Component System) with DOTS, Jobs, and Burst for high-performance game development. Use when building data-oriented games, optimizing performance, or working with large entity counts. |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `uv-package-manager` | Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Use when setting up Python projects, managing dependencies, or optimizing Python development workflows with uv. |
| `vector-index-tuning` | Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure. |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `vibecoding-security-audit` | Use when an app built or edited with AI needs a security pass before shipping - exposed secrets, Supabase row level security, auth and sessions, user uploads, a new dependency an AI suggested, or AI and usage-priced routes that could run up a bill. Also for "auditoria de segurança" or "vibecoding security audit" requests. |
| `visual-design-foundations` | Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing design tokens, building style guides, or improving visual hierarchy and consistency. |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. |
| `wcag-audit-patterns` | Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Use when auditing websites for accessibility, fixing WCAG violations, or implementing accessible design patterns. |
| `web-component-design` | Master React, Vue, and Svelte component patterns including CSS-in-JS, composition strategies, and reusable component architecture. Use when building UI component libraries, designing component APIs, or implementing frontend design systems. |
| `web3-testing` | Test smart contracts comprehensively using Hardhat and Foundry with unit tests, integration tests, and mainnet forking. Use when testing Solidity contracts, setting up blockchain test suites, or validating DeFi protocols. |
| `webapp-testing` | Web application testing principles. E2E, Playwright, deep audit strategies. |
| `workflow-orchestration-patterns` | Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determinism constraints. Use when building long-running processes, distributed transactions, or microservice orchestration. |
| `workflow-patterns` | Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks, or understanding the verification protocol. |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

<!-- skills:end -->

## Agents do hub

Arquivo: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/agents/<nome>.md"`. Um agent da tabela é a
persona preferida pro Modo dispatch acima: leia o `.md` inteiro (name +
description + corpo) antes de montar o subagente. Se este projeto escolheu
instalá-lo, ele também está em `.claude/agents/<nome>.md` (mesmo conteúdo).

<!-- agents:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 130.

| Agent | Use quando |
| --- | --- |
| `accessibility-expert` | Expert accessibility specialist ensuring WCAG compliance, inclusive design, and assistive technology compatibility. Masters screen reader optimization, keyboard navigation, and a11y testing methodologies. Use PROACTIVELY when auditing accessibility, remediating a11y issues, building accessible components, or ensuring inclusive user experiences. |
| `ai-engineer` | Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, multimodal AI, agent orchestration, and enterprise AI integrations. Use PROACTIVELY for LLM features, chatbots, AI agents, or AI-powered applications. |
| `api-documenter` | Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices. Create interactive docs, generate SDKs, and build comprehensive developer portals. Use PROACTIVELY for API documentation or developer portal creation. |
| `architect-review` | Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driven systems, and DDD. Reviews system designs and code changes for architectural integrity, scalability, and maintainability. Use PROACTIVELY for architectural decisions. |
| `arm-cortex-expert` | Senior embedded software engineer specializing in firmware and driver development for ARM Cortex-M microcontrollers (Teensy, STM32, nRF52, SAMD). Decades of experience writing reliable, optimized, and maintainable embedded code with deep expertise in memory barriers, DMA/cache coherency, interrupt-driven I/O, and peripheral drivers. |
| `backend-architect` | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Masters REST/GraphQL/gRPC APIs, event-driven architectures, service mesh patterns, and modern backend frameworks. Handles service boundary definition, inter-service communication, resilience patterns, and observability. Use PROACTIVELY when creating new backend services or APIs. |
| `backend-security-coder` | Expert in secure backend coding practices specializing in input validation, authentication, and API security. Use PROACTIVELY for backend security implementations or security code reviews. |
| `backend-specialist` | Expert backend architect for Node.js, Python, and modern serverless/edge systems. Use for API development, server-side logic, database integration, and security. Triggers on backend, server, api, endpoint, database, auth. |
| `bash-pro` | Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, portable, and testable shell scripts. |
| `blockchain-developer` | Build production-ready Web3 applications, smart contracts, and decentralized systems. Implements DeFi protocols, NFT platforms, DAOs, and enterprise blockchain integrations. Use PROACTIVELY for smart contracts, Web3 apps, DeFi protocols, or blockchain infrastructure. |
| `business-analyst` | Master modern business analysis with AI-powered analytics, real-time dashboards, and data-driven insights. Build comprehensive KPI frameworks, predictive models, and strategic recommendations. Use PROACTIVELY for business intelligence or strategic analysis. |
| `c-pro` | Write efficient C code with proper memory management, pointer arithmetic, and system calls. Handles embedded systems, kernel modules, and performance-critical code. Use PROACTIVELY for C optimization, memory issues, or system programming. |
| `c4-code` | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level documentation including function signatures, arguments, dependencies, and code structure. Use when documenting code at the lowest C4 level for individual directories and code modules. |
| `c4-component` | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level architecture, defining component boundaries, interfaces, and relationships. Creates component diagrams and documentation. Use when synthesizing code-level documentation into logical components. |
| `c4-container` | Expert C4 Container-level documentation specialist. Synthesizes Component-level documentation into Container-level architecture, mapping components to deployment units, documenting container interfaces as APIs, and creating container diagrams. Use when synthesizing components into deployment containers and documenting system deployment architecture. |
| `c4-context` | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, user journeys, system features, and external dependencies. Synthesizes container and component documentation with system documentation to create comprehensive context-level architecture. Use when creating the highest-level C4 system context documentation. |
| `cloud-architect` | Expert cloud architect specializing in AWS/Azure/GCP multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns. Masters serverless, microservices, security, compliance, and disaster recovery. Use PROACTIVELY for cloud architecture, cost optimization, migration planning, or multi-cloud strategies. |
| `code-archaeologist` | Expert in legacy code, refactoring, and understanding undocumented systems. Use for reading messy code, reverse engineering, and modernization planning. Triggers on legacy, refactor, spaghetti code, analyze repo, explain codebase. |
| `code-reviewer` | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability. Masters static analysis tools, security scanning, and configuration review with 2024/2025 best practices. Use PROACTIVELY for code quality assurance. |
| `codebase-analyzer` | Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components. As always, the more detailed your request prompt, the better! :) |
| `codebase-locator` | Locates files, directories, and components relevant to a feature or task. Call `codebase-locator` with human language prompt describing what you're looking for. Basically a "Super Grep/Glob/LS tool" — Use it if you find yourself desiring to use one of these tools more than once. |
| `codebase-pattern-finder` | codebase-pattern-finder is a useful subagent_type for finding similar implementations, usage examples, or existing patterns that can be modeled after. It will give you concrete code examples based on what you're looking for! It's sorta like codebase-locator, but it will not only tell you the location of files, it will also give you code details! |
| `conductor-validator` | Validates Conductor project artifacts for completeness, consistency, and correctness. Use after setup, when diagnosing issues, or before implementation to verify project context. |
| `content-marketer` | Elite content marketing strategist specializing in AI-powered content creation, omnichannel distribution, SEO optimization, and data-driven performance marketing. Masters modern content tools, social media automation, and conversion optimization with 2024/2025 best practices. Use PROACTIVELY for comprehensive content marketing. |
| `context-manager` | Elite AI context engineering specialist mastering dynamic context management, vector databases, knowledge graphs, and intelligent memory systems. Orchestrates context across multi-agent workflows, enterprise AI systems, and long-running projects with 2024/2025 best practices. Use PROACTIVELY for complex AI orchestration. |
| `cpp-pro` | Write idiomatic C++ code with modern features, RAII, smart pointers, and STL algorithms. Handles templates, move semantics, and performance optimization. Use PROACTIVELY for C++ refactoring, memory safety, or complex C++ patterns. |
| `csharp-pro` | Write modern C# code with advanced features like records, pattern matching, and async/await. Optimizes .NET applications, implements enterprise patterns, and ensures comprehensive testing. Use PROACTIVELY for C# refactoring, performance optimization, or complex .NET solutions. |
| `customer-support` | Elite AI-powered customer support specialist mastering conversational AI, automated ticketing, sentiment analysis, and omnichannel support experiences. Integrates modern support tools, chatbot platforms, and CX optimization with 2024/2025 best practices. Use PROACTIVELY for comprehensive customer experience management. |
| `data-engineer` | Build scalable data pipelines, modern data warehouses, and real-time streaming architectures. Implements Apache Spark, dbt, Airflow, and cloud-native data platforms. Use PROACTIVELY for data pipeline design, analytics infrastructure, or modern data stack implementation. |
| `data-scientist` | Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analysis, predictive modeling, and business intelligence. Use PROACTIVELY for data analysis tasks, ML modeling, statistical analysis, and data-driven insights. |
| `database-admin` | Expert database administrator specializing in modern cloud databases, automation, and reliability engineering. Masters AWS/Azure/GCP database services, Infrastructure as Code, high availability, disaster recovery, performance optimization, and compliance. Handles multi-cloud strategies, container databases, and cost optimization. Use PROACTIVELY for database architecture, operations, or reliability engineering. |
| `database-architect` | Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and scalable database architectures. Masters SQL/NoSQL/TimeSeries database selection, normalization strategies, migration planning, and performance-first design. Handles both greenfield architectures and re-architecture of existing systems. Use PROACTIVELY for database architecture, technology selection, or data modeling decisions. |
| `database-optimizer` | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. Masters advanced indexing, N+1 resolution, multi-tier caching, partitioning strategies, and cloud database optimization. Handles complex query analysis, migration strategies, and performance monitoring. Use PROACTIVELY for database optimization, performance issues, or scalability challenges. |
| `debugger` | Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues. |
| `deployment-engineer` | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation. Masters GitHub Actions, ArgoCD/Flux, progressive delivery, container security, and platform engineering. Handles zero-downtime deployments, security scanning, and developer experience optimization. Use PROACTIVELY for CI/CD design, GitOps implementation, or deployment automation. |
| `design-system-architect` | Expert design system architect specializing in design tokens, component libraries, theming infrastructure, and scalable design operations. Masters token architecture, multi-brand systems, and design-development collaboration. Use PROACTIVELY when building design systems, creating token architectures, implementing theming, or establishing component libraries. |
| `devops-engineer` | Expert in deployment, server management, CI/CD, and production operations. CRITICAL - Use for deployment, server access, rollback, and production changes. HIGH RISK operations. Triggers on deploy, production, server, pm2, ssh, release, rollback, ci/cd. |
| `devops-troubleshooter` | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. Masters log analysis, distributed tracing, Kubernetes debugging, performance optimization, and root cause analysis. Handles production outages, system reliability, and preventive monitoring. Use PROACTIVELY for debugging, incident response, or system troubleshooting. |
| `django-pro` | Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper architecture, testing, and deployment. Use PROACTIVELY for Django development, ORM optimization, or complex Django patterns. |
| `docs-architect` | Creates comprehensive technical documentation from existing codebases. Analyzes architecture, design patterns, and implementation details to produce long-form technical manuals and ebooks. Use PROACTIVELY for system documentation, architecture guides, or technical deep-dives. |
| `documentation-writer` | Expert in technical documentation. Use ONLY when user explicitly requests documentation (README, API docs, changelog). DO NOT auto-invoke during normal development. |
| `dotnet-architect` | Expert .NET backend architect specializing in C#, ASP.NET Core, Entity Framework, Dapper, and enterprise application patterns. Masters async/await, dependency injection, caching strategies, and performance optimization. Use PROACTIVELY for .NET API development, code review, or architecture decisions. |
| `dx-optimizer` | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects, after team feedback, or when development friction is noticed. |
| `elixir-pro` | Write idiomatic Elixir code with OTP patterns, supervision trees, and Phoenix LiveView. Masters concurrency, fault tolerance, and distributed systems. Use PROACTIVELY for Elixir refactoring, OTP design, or complex BEAM optimizations. |
| `error-detective` | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and identifies root causes. Use PROACTIVELY when debugging issues, analyzing logs, or investigating production errors. |
| `event-sourcing-architect` | Event sourcing, CQRS and event-driven architecture: event store design, projections, sagas, schema evolution. Use for event-sourced systems. |
| `explorer-agent` | Advanced codebase discovery, deep architectural analysis, and proactive research agent. The eyes and ears of the framework. Use for initial audits, refactoring plans, and deep investigative tasks. |
| `fastapi-pro` | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, and modern Python async patterns. Use PROACTIVELY for FastAPI development, async optimization, or API architecture. |
| `firmware-analyst` | Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering. Masters firmware extraction, analysis, and vulnerability research for routers, IoT devices, automotive systems, and industrial controllers. Use PROACTIVELY for firmware security audits, IoT penetration testing, or embedded systems research. |
| `flutter-expert` | Master Flutter development with Dart 3, advanced widgets, and multi-platform deployment. Handles state management, animations, testing, and performance optimization for mobile, web, desktop, and embedded platforms. Use PROACTIVELY for Flutter architecture, UI implementation, or cross-platform features. |
| `frontend-developer` | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next.js 15, and modern frontend architecture. Optimizes performance and ensures accessibility. Use PROACTIVELY when creating UI components or fixing frontend issues. |
| `frontend-security-coder` | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side security patterns. Use PROACTIVELY for frontend security implementations or client-side security code reviews. |
| `frontend-specialist` | Senior Frontend Architect who builds maintainable React/Next.js systems with performance-first mindset. Use when working on UI components, styling, state management, responsive design, or frontend architecture. Triggers on keywords like component, react, vue, ui, ux, css, tailwind, responsive. |
| `game-developer` | Game development across all platforms (PC, Web, Mobile, VR/AR). Use when building games with Unity, Godot, Unreal, Phaser, Three.js, or any game engine. Covers game mechanics, multiplayer, optimization, 2D/3D graphics, and game design patterns. |
| `golang-pro` | Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices. Expert in the latest Go ecosystem including generics, workspaces, and cutting-edge frameworks. Use PROACTIVELY for Go development, architecture design, or performance optimization. |
| `graphql-architect` | Master modern GraphQL with federation, performance optimization, and enterprise security. Build scalable schemas, implement advanced caching, and design real-time systems. Use PROACTIVELY for GraphQL architecture or performance optimization. |
| `haskell-pro` | Expert Haskell engineer specializing in advanced type systems, pure functional design, and high-reliability software. Use PROACTIVELY for type-level programming, concurrency, and architecture guidance. |
| `hr-pro` | Professional, ethical HR partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, and employee relations. Ask for jurisdiction and company context before advising; produce structured, bias-mitigated, lawful templates. |
| `hybrid-cloud-architect` | Expert hybrid cloud architect specializing in complex multi-cloud solutions across AWS/Azure/GCP and private clouds (OpenStack/VMware). Masters hybrid connectivity, workload placement optimization, edge computing, and cross-cloud automation. Handles compliance, cost optimization, disaster recovery, and migration strategies. Use PROACTIVELY for hybrid architecture, multi-cloud strategy, or complex infrastructure integration. |
| `incident-responder` | Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incident management. Masters incident command, blameless post-mortems, error budget management, and system reliability patterns. Handles critical outages, communication strategies, and continuous improvement. Use IMMEDIATELY for production incidents or SRE practices. |
| `ios-developer` | Develop native iOS applications with Swift/SwiftUI. Masters iOS 18, SwiftUI, UIKit integration, Core Data, networking, and App Store optimization. Use PROACTIVELY for iOS-specific features, App Store optimization, or native iOS development. |
| `java-pro` | Master Java 21+ with modern features like virtual threads, pattern matching, and Spring Boot 3.x. Expert in the latest Java ecosystem including GraalVM, Project Loom, and cloud-native patterns. Use PROACTIVELY for Java development, microservices architecture, or performance optimization. |
| `javascript-pro` | Master modern JavaScript with ES6+, async patterns, and Node.js APIs. Handles promises, event loops, and browser/Node compatibility. Use PROACTIVELY for JavaScript optimization, async debugging, or complex JS patterns. |
| `julia-pro` | Master Julia 1.10+ with modern features, performance optimization, multiple dispatch, and production-ready practices. Expert in the Julia ecosystem including package management, scientific computing, and high-performance numerical code. Use PROACTIVELY for Julia development, optimization, or advanced Julia patterns. |
| `kubernetes-architect` | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration. Masters EKS/AKS/GKE, service mesh (Istio/Linkerd), progressive delivery, multi-tenancy, and platform engineering. Handles security, observability, cost optimization, and developer experience. Use PROACTIVELY for K8s architecture, GitOps implementation, or cloud-native platform design. |
| `legacy-modernizer` | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, dependency updates, and backward compatibility. Use PROACTIVELY for legacy system updates, framework migrations, or technical debt reduction. |
| `legal-advisor` | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements. Use PROACTIVELY for legal documentation, compliance texts, or regulatory requirements. |
| `malware-analyst` | Expert malware analyst specializing in defensive malware research, threat intelligence, and incident response. Masters sandbox analysis, behavioral analysis, and malware family identification. Handles static/dynamic analysis, unpacking, and IOC extraction. Use PROACTIVELY for malware triage, threat hunting, incident response, or security research. |
| `mermaid-expert` | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. Use PROACTIVELY for visual documentation, system diagrams, or process flows. |
| `minecraft-bukkit-pro` | Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs. Specializes in event-driven architecture, command systems, world manipulation, player management, and performance optimization. Use PROACTIVELY for plugin architecture, gameplay mechanics, server-side features, or cross-version compatibility. |
| `ml-engineer` | Build production ML systems with PyTorch 2.x, TensorFlow, and modern ML frameworks. Implements model serving, feature engineering, A/B testing, and monitoring. Use PROACTIVELY for ML model deployment, inference optimization, or production ML infrastructure. |
| `mlops-engineer` | Build comprehensive ML pipelines, experiment tracking, and model registries with MLflow, Kubeflow, and modern MLOps tools. Implements automated training, deployment, and monitoring across cloud platforms. Use PROACTIVELY for ML infrastructure, experiment management, or pipeline automation. |
| `mobile-developer` | Develop React Native, Flutter, or native mobile apps with modern architecture patterns. Masters cross-platform development, native integrations, offline sync, and app store optimization. Use PROACTIVELY for mobile features, cross-platform code, or app optimization. |
| `mobile-security-coder` | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific security patterns. Use PROACTIVELY for mobile security implementations or mobile security code reviews. |
| `monorepo-architect` | Monorepo architecture, build systems and dependency management at scale (Nx, Turborepo, Bazel, Lerna). Use for workspace setup and CI optimization. |
| `network-engineer` | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization. Masters multi-cloud connectivity, service mesh, zero-trust networking, SSL/TLS, global load balancing, and advanced troubleshooting. Handles CDN optimization, network automation, and compliance. Use PROACTIVELY for network design, connectivity issues, or performance optimization. |
| `observability-engineer` | Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, SLI/SLO management, and incident response workflows. Use PROACTIVELY for monitoring infrastructure, performance optimization, or production reliability. |
| `orchestrator` | Multi-agent coordination and task orchestration. Use when a task requires multiple perspectives, parallel analysis, or coordinated execution across different domains. Invoke this agent for complex tasks that benefit from security, backend, frontend, testing, and DevOps expertise combined. |
| `payment-integration` | Integrate Stripe, PayPal, and payment processors. Handles checkout flows, subscriptions, webhooks, and PCI compliance. Use PROACTIVELY when implementing payments, billing, or subscription features. |
| `penetration-tester` | Expert in offensive security, penetration testing, red team operations, and vulnerability exploitation. Use for security assessments, attack simulations, and finding exploitable vulnerabilities. Triggers on pentest, exploit, attack, hack, breach, pwn, redteam, offensive. |
| `performance-engineer` | Expert performance engineer specializing in modern observability, application optimization, and scalable system performance. Masters OpenTelemetry, distributed tracing, load testing, multi-tier caching, Core Web Vitals, and performance monitoring. Handles end-to-end optimization, real user monitoring, and scalability patterns. Use PROACTIVELY for performance optimization, observability, or scalability challenges. |
| `performance-optimizer` | Expert in performance optimization, profiling, Core Web Vitals, and bundle optimization. Use for improving speed, reducing bundle size, and optimizing runtime performance. Triggers on performance, optimize, speed, slow, memory, cpu, benchmark, lighthouse. |
| `php-pro` | Write idiomatic PHP code with generators, iterators, SPL data structures, and modern OOP features. Use PROACTIVELY for high-performance PHP applications. |
| `posix-shell-pro` | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts that run on any POSIX-compliant shell (dash, ash, sh, bash --posix). |
| `product-manager` | Expert in product requirements, user stories, and acceptance criteria. Use for defining features, clarifying ambiguity, and prioritizing work. Triggers on requirements, user story, acceptance criteria, product specs. |
| `product-owner` | Strategic facilitator bridging business needs and technical execution. Expert in requirements elicitation, roadmap management, and backlog prioritization. Triggers on requirements, user story, backlog, MVP, PRD, stakeholder. |
| `project-planner` | Smart project planning agent. Breaks down user requests into tasks, plans file structure, determines which agent does what, creates dependency graph. Use when starting new projects or planning major features. |
| `prompt-engineer` | Expert prompt engineer specializing in advanced prompting techniques, LLM optimization, and AI system design. Masters chain-of-thought, constitutional AI, and production prompt strategies. Use when building AI features, improving agent performance, or crafting system prompts. |
| `python-pro` | Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices. Expert in the latest Python ecosystem including uv, ruff, pydantic, and FastAPI. Use PROACTIVELY for Python development, optimization, or advanced Python patterns. |
| `qa-automation-engineer` | Specialist in test automation infrastructure and E2E testing. Focuses on Playwright, Cypress, CI pipelines, and breaking the system. Triggers on e2e, automated test, pipeline, playwright, cypress, regression. |
| `quant-analyst` | Build financial models, backtest trading strategies, and analyze market data. Implements risk metrics, portfolio optimization, and statistical arbitrage. Use PROACTIVELY for quantitative finance, trading algorithms, or risk analysis. |
| `reference-builder` | Creates exhaustive technical references and API documentation. Generates comprehensive parameter listings, configuration guides, and searchable reference materials. Use PROACTIVELY for API docs, configuration references, or complete technical specifications. |
| `reverse-engineer` | Expert reverse engineer specializing in binary analysis, disassembly, decompilation, and software analysis. Masters IDA Pro, Ghidra, radare2, x64dbg, and modern RE toolchains. Handles executable analysis, library inspection, protocol extraction, and vulnerability research. Use PROACTIVELY for binary analysis, CTF challenges, security research, or understanding undocumented software. |
| `risk-manager` | Monitor portfolio risk, R-multiples, and position limits. Creates hedging strategies, calculates expectancy, and implements stop-losses. Use PROACTIVELY for risk assessment, trade tracking, or portfolio protection. |
| `ruby-pro` | Write idiomatic Ruby code with metaprogramming, Rails patterns, and performance optimization. Specializes in Ruby on Rails, gem development, and testing frameworks. Use PROACTIVELY for Ruby refactoring, optimization, or complex Ruby features. |
| `rust-pro` | Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming. Expert in the latest Rust ecosystem including Tokio, axum, and cutting-edge crates. Use PROACTIVELY for Rust development, performance optimization, or systems programming. |
| `sales-automator` | Draft cold emails, follow-ups, and proposal templates. Creates pricing pages, case studies, and sales scripts. Use PROACTIVELY for sales outreach or lead nurturing. |
| `scala-pro` | Master enterprise-grade Scala development with functional programming, distributed systems, and big data processing. Expert in Apache Pekko, Akka, Spark, ZIO/Cats Effect, and reactive architectures. Use PROACTIVELY for Scala system design, performance optimization, or enterprise integration. |
| `search-specialist` | Expert web researcher using advanced search techniques and synthesis. Masters search operators, result filtering, and multi-source verification. Handles competitive analysis and fact-checking. Use PROACTIVELY for deep research, information gathering, or trend analysis. |
| `security-auditor` | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vulnerability assessment, threat modeling, secure authentication (OAuth2/OIDC), OWASP standards, cloud security, and security automation. Handles DevSecOps integration, compliance (GDPR/HIPAA/SOC2), and incident response. Use PROACTIVELY for security audits, DevSecOps, or compliance implementation. |
| `seo-authority-builder` | Analyzes content for E-E-A-T signals and suggests improvements to build authority and trust. Identifies missing credibility elements. Use PROACTIVELY for YMYL topics. |
| `seo-cannibalization-detector` | Analyzes multiple provided pages to identify keyword overlap and potential cannibalization issues. Suggests differentiation strategies. Use PROACTIVELY when reviewing similar content. |
| `seo-content-auditor` | Analyzes provided content for quality, E-E-A-T signals, and SEO best practices. Scores content and provides improvement recommendations based on established guidelines. Use PROACTIVELY for content review. |
| `seo-content-planner` | Creates comprehensive content outlines and topic clusters for SEO. Plans content calendars and identifies topic gaps. Use PROACTIVELY for content strategy and planning. |
| `seo-content-refresher` | Identifies outdated elements in provided content and suggests updates to maintain freshness. Finds statistics, dates, and examples that need updating. Use PROACTIVELY for older content. |
| `seo-content-writer` | Writes SEO-optimized content based on provided keywords and topic briefs. Creates engaging, comprehensive content following best practices. Use PROACTIVELY for content creation tasks. |
| `seo-keyword-strategist` | Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based on the topic. Prevents over-optimization. Use PROACTIVELY for content optimization. |
| `seo-meta-optimizer` | Creates optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. Generates compelling, keyword-rich metadata. Use PROACTIVELY for new content. |
| `seo-snippet-hunter` | Formats content to be eligible for featured snippets and SERP features. Creates snippet-optimized content blocks based on best practices. Use PROACTIVELY for question-based content. |
| `seo-specialist` | SEO and GEO (Generative Engine Optimization) expert. Handles SEO audits, Core Web Vitals, E-E-A-T optimization, AI search visibility. Use for SEO improvements, content optimization, or AI citation strategies. |
| `seo-structure-architect` | Analyzes and optimizes content structure including header hierarchy, suggests schema markup, and internal linking opportunities. Creates search-friendly content organization. Use PROACTIVELY for content structuring. |
| `service-mesh-expert` | Service mesh architecture with Istio and Linkerd: traffic management, mTLS, observability, progressive delivery. Use for cloud-native networking. |
| `sql-pro` | Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. Expert in performance tuning, data modeling, and hybrid analytical systems. Use PROACTIVELY for database optimization or complex analysis. |
| `startup-analyst` | Expert startup business analyst specializing in market sizing, financial modeling, competitive analysis, and strategic planning for early-stage companies. Use PROACTIVELY when the user asks about market opportunity, TAM/SAM/SOM, financial projections, unit economics, competitive landscape, team planning, startup metrics, or business strategy for pre-seed through Series A startups. |
| `tdd-orchestrator` | Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and comprehensive test-driven development practices. Enforces TDD best practices across teams with AI-assisted testing and modern frameworks. Use PROACTIVELY for TDD implementation and governance. |
| `temporal-python-pro` | Master Temporal workflow orchestration with Python SDK. Implements durable workflows, saga patterns, and distributed transactions. Covers async/await, testing strategies, and production deployment. Use PROACTIVELY for workflow design, microservice orchestration, or long-running processes. |
| `terraform-specialist` | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructure patterns. Handles complex module design, multi-cloud deployments, GitOps workflows, policy as code, and CI/CD integration. Covers migration strategies, security best practices, and modern IaC ecosystems. Use PROACTIVELY for advanced IaC, state management, or infrastructure automation. |
| `test-automator` | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. Build scalable testing strategies with advanced CI/CD integration. Use PROACTIVELY for testing automation or quality assurance. |
| `test-engineer` | Expert in testing, TDD, and test automation. Use for writing tests, improving coverage, debugging test failures. Triggers on test, spec, coverage, jest, pytest, playwright, e2e, unit test. |
| `thoughts-analyzer` | The research equivalent of codebase-analyzer. Use this subagent_type when wanting to deep dive on a research topic. Not commonly needed otherwise. |
| `thoughts-locator` | Discovers relevant documents in thoughts/ directory (We use this for all sorts of metadata storage!). This is really only relevant/needed when you're in a reseaching mood and need to figure out if we have random thoughts written down that are relevant to your current research task. Based on the name, I imagine you can guess this is the `thoughts` equivilent of `codebase-locator` |
| `threat-modeling-expert` | Threat modeling and security architecture review: STRIDE, PASTA, attack trees, risk scoring, mitigation design. Use before building security-sensitive features. |
| `tutorial-engineer` | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learning experiences with hands-on examples. Use PROACTIVELY for onboarding guides, feature tutorials, or concept explanations. |
| `typescript-pro` | Master TypeScript with advanced types, generics, and strict type safety. Handles complex type systems, decorators, and enterprise-grade patterns. Use PROACTIVELY for TypeScript architecture, type inference optimization, or advanced typing patterns. |
| `ui-designer` | Expert UI designer specializing in component creation, layout systems, and visual design implementation. Masters modern design patterns, responsive layouts, and design-to-code workflows. Use PROACTIVELY when building UI components, designing layouts, creating mockups, or implementing visual designs. |
| `ui-ux-designer` | Create interface designs, wireframes, and design systems. Masters user research, accessibility standards, and modern design tools. Specializes in design tokens, component libraries, and inclusive design. Use PROACTIVELY for design systems, user flows, or interface optimization. |
| `ui-visual-validator` | Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verification. Masters screenshot analysis, visual regression testing, and component validation. Use PROACTIVELY to verify UI modifications have achieved their intended goals through comprehensive visual analysis. |
| `unity-developer` | Build Unity games with optimized C# scripts, efficient rendering, and proper asset management. Masters Unity 6 LTS, URP/HDRP pipelines, and cross-platform deployment. Handles gameplay systems, UI implementation, and platform optimization. Use PROACTIVELY for Unity performance issues, game mechanics, or cross-platform builds. |
| `vector-database-engineer` | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similarity search. Use PROACTIVELY for vector search implementation, embedding optimization, or semantic retrieval systems. |
| `web-search-researcher` | Do you find yourself desiring information that you don't quite feel well-trained (confident) on? Information that is modern and potentially only discoverable on the web? Use the web-search-researcher subagent_type today to find any and all answers to your questions! It will research deeply to figure out and attempt to answer your questions! If you aren't immediately satisfied you can get your money back! (Not really - but you can re-run web-search-researcher with an altered prompt in the event you're not satisfied the first time) |

<!-- agents:end -->

## Workflows do hub

Arquivo: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/workflows/<nome>.md"`. Um workflow é um
procedimento `/nome`: se o pedido bate com uma linha da tabela, leia o `.md`
e siga o procedimento; não invente um `/comando` que não está na tabela. Se
este projeto escolheu instalá-lo, ele também aparece como `/nome` nativo.

<!-- workflows:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 111.

| Workflow | Use quando |
| --- | --- |
| `/accessibility-audit` | Audit UI code for WCAG compliance |
| `/ai-assistant` | Build AI assistant application with NLU, dialog management, and integrations |
| `/ai-review` | AI-Powered Code Review Specialist |
| `/api-mock` | API Mocking Framework |
| `/brainstorm` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores requirements and design before implementation. |
| `/business-case` | Generate comprehensive investor-ready business case document with market, solution, financials, and strategy |
| `/c4-architecture` | C4 Architecture Documentation Workflow |
| `/ci_commit` | Create git commits for session changes with clear, atomic messages |
| `/ci_describe_pr` | Generate comprehensive PR descriptions following repository templates |
| `/code-explain` | Code Explanation and Analysis |
| `/code-migrate` | Code Migration Assistant |
| `/commit` | Create git commits with user approval and no Claude attribution |
| `/compliance-check` | Regulatory Compliance Check |
| `/component-scaffold` | React/React Native Component Scaffolding |
| `/config-validate` | Configuration Validation |
| `/context-restore` | Context Restoration: Advanced Semantic Memory Rehydration |
| `/context-save` | Context Save Tool: Intelligent Context Management Specialist |
| `/cost-optimize` | Cloud Cost Optimization |
| `/create` | Create new application command. Triggers App Builder skill and starts interactive dialogue with user. |
| `/create-component` | Guided component creation with proper patterns |
| `/create_plan` | Create detailed implementation plans through interactive research and iteration |
| `/create_plan_generic` | Create detailed implementation plans with thorough research and iteration |
| `/create_plan_nt` | Create implementation plans with thorough research (no thoughts directory) |
| `/create_worktree` | --- |
| `/data-driven-feature` | Data-Driven Feature Development |
| `/data-pipeline` | Data Pipeline Architecture |
| `/debug` | Debugging command. Activates DEBUG mode for systematic problem investigation. |
| `/debug-trace` | Debug and Trace Configuration |
| `/deploy` | Deployment command for production releases. Pre-flight checks and deployment execution. |
| `/deps-audit` | Dependency Audit and Security Analysis |
| `/deps-upgrade` | Dependency Upgrade Strategy |
| `/describe_pr` | Generate comprehensive PR descriptions following repository templates |
| `/describe_pr_nt` | Generate comprehensive PR descriptions following repository templates |
| `/design-new-component` | Component Development |
| `/design-new-page` | Page Development |
| `/design-review` | Review existing UI for issues and improvements |
| `/design-system-foundation` | Design System Setup |
| `/design-system-setup` | Initialize a design system with tokens |
| `/doc-generate` | Automated Documentation Generation |
| `/enhance` | Add or update features in existing application. Used for iterative development. |
| `/error-analysis` | Error Analysis and Resolution |
| `/error-trace` | Error Tracking and Monitoring |
| `/execute-plan` | Execute plan in batches with review checkpoints |
| `/feature-development` | Orchestrate end-to-end feature development from requirements to production deployment |
| `/financial-projections` | Create detailed 3-5 year financial model with revenue, costs, cash flow, and scenarios |
| `/founder_mode` | Create Linear ticket and PR for experimental features after implementation |
| `/full-review` | Orchestrate comprehensive multi-dimensional code review using specialized review agents |
| `/full-stack-feature` | Orchestrate full-stack feature development across backend, frontend, and infrastructure layers with modern API-first approach |
| `/git-workflow` | Complete Git Workflow with Multi-Agent Orchestration |
| `/implement` | Execute tasks from a track's implementation plan following TDD workflow |
| `/implement_plan` | Implement technical plans from thoughts/shared/plans with verification |
| `/improve-agent` | Agent Performance Optimization Workflow |
| `/incident-response` | Orchestrate multi-agent incident response with modern SRE practices for rapid resolution and learning |
| `/issue` | GitHub Issue Resolution Expert |
| `/iterate_plan` | Iterate on existing implementation plans with thorough research and updates |
| `/iterate_plan_nt` | Iterate on existing implementation plans with thorough research and updates |
| `/langchain-agent` | Create LangGraph-based agent with modern patterns |
| `/legacy-modernize` | Legacy Code Modernization Workflow |
| `/linear` | Manage Linear tickets - create, update, comment, and follow workflow patterns |
| `/local_review` | Set up worktree for reviewing colleague's branch |
| `/manage` | Manage track lifecycle: archive, restore, delete, rename, and cleanup |
| `/market-opportunity` | Generate comprehensive market opportunity analysis with TAM/SAM/SOM calculations |
| `/migration-observability` | Migration monitoring, CDC, and observability infrastructure |
| `/ml-pipeline` | Machine Learning Pipeline - Multi-Agent MLOps Orchestration |
| `/monitor-setup` | Monitoring and Observability Setup |
| `/multi-agent-optimize` | Multi-Agent Optimization Toolkit |
| `/multi-agent-review` | Multi-Agent Code Review Orchestration Tool |
| `/multi-platform` | Multi-Platform Feature Development Workflow |
| `/new-track` | Create a new track with specification and phased implementation plan |
| `/onboard` | Onboard |
| `/oneshot` | Research ticket and launch planning session |
| `/oneshot_plan` | Execute ralph plan and implementation for a ticket |
| `/orchestrate` | Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise. |
| `/performance-optimization` | Optimize application performance end-to-end using specialized performance and optimization agents |
| `/plan` | Create project plan using project-planner agent. No code writing - only plan file generation. |
| `/pr-enhance` | Pull Request Enhancement |
| `/preview` | Preview server start, stop, and status check. Local development server management. |
| `/prompt-optimize` | Optimize prompts for production with CoT, few-shot, and constitutional AI patterns |
| `/python-scaffold` | Python Project Scaffolding |
| `/ralph_impl` | Implement highest priority small Linear ticket with worktree setup |
| `/ralph_plan` | Create implementation plan for highest priority Linear ticket ready for spec |
| `/ralph_research` | Research highest priority Linear ticket needing investigation |
| `/refactor-clean` | Refactor and Clean Code |
| `/research_codebase` | Document codebase as-is with thoughts directory for historical context |
| `/research_codebase_generic` | Research codebase comprehensively using parallel sub-agents |
| `/research_codebase_nt` | Document codebase as-is without evaluation or recommendations |
| `/revert` | Git-aware undo by logical work unit (track, phase, or task) |
| `/rust-project` | Rust Project Scaffolding |
| `/security-dependencies` | Dependency Vulnerability Scanning |
| `/security-hardening` | Implement comprehensive security hardening with defense-in-depth strategy through coordinated multi-agent orchestration |
| `/security-sast` | Static Application Security Testing (SAST) for code vulnerability analysis across multiple languages and frameworks |
| `/setup` | Initialize project with Conductor artifacts (product definition, tech stack, workflow, style guides) |
| `/slo-implement` | SLO Implementation Guide |
| `/smart-debug` | You are an expert AI-assisted debugging specialist with deep knowledge of modern debugging tools, observability platforms, and automated root cause an |
| `/smart-fix` | Intelligent Issue Resolution with Multi-Agent Orchestration |
| `/sql-migrations` | SQL database migrations with zero-downtime strategies for PostgreSQL, MySQL, SQL Server |
| `/standup-notes` | Standup Notes Generator |
| `/status` | Display project status, active tracks, and next actions |
| `/tdd-cycle` | Execute a comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline |
| `/tdd-green` | Implement minimal code to make failing tests pass in TDD green phase |
| `/tdd-red` | Write comprehensive failing tests following TDD red phase principles. |
| `/tdd-refactor` | Refactor code with confidence using comprehensive test safety net |
| `/tech-debt` | Technical Debt Analysis and Remediation |
| `/test` | Test generation and test running command. Creates and executes tests for code. |
| `/test-generate` | Automated Unit Test Generation |
| `/typescript-scaffold` | TypeScript Project Scaffolding |
| `/ui-ux-pro-max` | AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation |
| `/validate_plan` | Validate implementation against plan, verify success criteria, identify issues |
| `/workflow-automate` | Workflow Automation |
| `/write-plan` | Create detailed implementation plan with bite-sized tasks |
| `/xss-scan` | XSS Vulnerability Scanner for Frontend Code |

<!-- workflows:end -->

## Agent ou workflow não instalado

Use-o assim mesmo, lendo pelo caminho absoluto acima. Só ofereça instalá-lo
(colando de novo o prompt de instalação e escolhendo o item) se o usuário
disser que vai usá-lo com frequência neste projeto. Não instale por conta própria.

## Modo contribuição (devolver conhecimento ao hub)

**Exceção primeiro — edição direta quando o dono já revisou:** se o próprio usuário
dono do hub pediu explicitamente a mudança nesta conversa (ele indicou o hub como
destino, revisou a decisão antes de qualquer arquivo ser escrito), a curadoria já
aconteceu em tempo real — edite `.agent/skills/`/`workflows/`/etc. do hub direto,
sem passar pelo inbox. O fluxo de inbox abaixo é para o caso contrário: uma sessão
rodando num projeto consumidor, só com o symlink do resolver instalado, sem o dono
do hub revisando aquela edição específica.

Nesse segundo caso, nunca edite `.agent/skills/` ou equivalentes do hub direto —
são compartilhados por symlink com todo projeto que instalou esta skill; uma
edição sem curadoria propagaria pra todo mundo instantaneamente. Em vez disso:

1. Leia o formato em `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/inbox/README.md"`.
2. Crie `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/inbox/NNN-<assunto>.md"` (próximo número livre da pasta)
   com todas as seções do formato, escrito para quem nunca viu a conversa.
3. Avise o usuário que a contribuição ficou pendente de revisão, com o caminho do arquivo.

## Atualização

- Última atualização do hub: 2026-11-13 (o dono do hub muda esta data sempre que esta skill, um agent, um workflow ou a estrutura do hub mudar).
- Para atualizar a instalação num projeto (refazer links, escolher entre os
  agents/workflows novos do hub, mudar a escolha): cole de novo o prompt
  `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/instalar-skill-sip-geral.md"` numa sessão daquele projeto.
- A data em que **cada projeto** instalou ou atualizou fica no
  `.agent/SIPS-CONSUMIDOS.md` dele. Se for anterior à data acima, ofereça
  rodar o prompt.

## Se nada bater

Se a tarefa não é de geral, ou se o projeto atual é o próprio
`SIP - Geral`, não force o uso desta skill.
