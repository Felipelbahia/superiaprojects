# devops-e-cloud

DevOps e nuvem: CI/CD, Kubernetes, Helm, service mesh, Terraform, observabilidade, SLO, incidentes, deploy, custo, shell e monorepo.

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agent/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agent/agents/<nome>.md"`; workflow: `"<HUB>/.agent/workflows/<nome>.md"`.

## Skills (30)

| Skill | Use quando |
| --- | --- |
| `bash-defensive-patterns` | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety. |
| `bash-linux` | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. |
| `bazel-build-optimization` | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterprise codebases. |
| `cost-optimization` | Optimize cloud costs through resource rightsizing, tagging strategies, reserved instances, and spending analysis. Use when reducing cloud expenses, analyzing infrastructure costs, or implementing cost governance policies. |
| `deployment-pipeline-design` | Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Use when architecting deployment workflows, setting up continuous delivery, or implementing GitOps practices. |
| `deployment-procedures` | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. |
| `distributed-tracing` | Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Use when debugging microservices, analyzing request flows, or implementing observability for distributed systems. |
| `github-actions-templates` | Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD with GitHub Actions, automating development workflows, or creating reusable workflow templates. |
| `gitlab-ci-patterns` | Build GitLab CI/CD pipelines with multi-stage workflows, caching, and distributed runners for scalable automation. Use when implementing GitLab CI/CD, optimizing pipeline performance, or setting up automated testing and deployment. |
| `gitops-workflow` | Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation. Use when implementing GitOps practices, automating Kubernetes deployments, or setting up declarative infrastructure management. |
| `grafana-dashboards` | Create and manage production Grafana dashboards for real-time visualization of system and application metrics. Use when building monitoring dashboards, visualizing metrics, or creating operational observability interfaces. |
| `helm-chart-scaffolding` | Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments. |
| `hybrid-cloud-networking` | Configure secure, high-performance connectivity between on-premises infrastructure and cloud platforms using VPN and dedicated connections. Use when building hybrid cloud architectures, connecting data centers to cloud, or implementing secure cross-premises networking. |
| `istio-traffic-management` | Configure Istio traffic management including routing, load balancing, circuit breakers, and canary deployments. Use when implementing service mesh traffic policies, progressive delivery, or resilience patterns. |
| `k8s-manifest-generator` | Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations. |
| `linkerd-patterns` | Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configuring traffic policies, or implementing zero-trust networking with minimal overhead. |
| `monorepo-management` | Master monorepo management with Turborepo, Nx, and pnpm workspaces to build efficient, scalable multi-package repositories with optimized builds and dependency management. Use when setting up monorepos, optimizing builds, or managing shared dependencies. |
| `multi-cloud-architecture` | Design multi-cloud architectures using a decision framework to select and integrate services across AWS, Azure, and GCP. Use when building multi-cloud systems, avoiding vendor lock-in, or leveraging best-of-breed services from multiple providers. |
| `nx-workspace-patterns` | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands. |
| `on-call-handoff-patterns` | Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use when transitioning on-call responsibilities, documenting shift summaries, or improving on-call processes. |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. |
| `prometheus-configuration` | Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Use when implementing metrics collection, setting up monitoring infrastructure, or configuring alerting systems. |
| `python-packaging` | Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Use when packaging Python libraries, creating CLI tools, or distributing Python code. |
| `server-management` | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. |
| `service-mesh-observability` | Implement comprehensive observability for service meshes including distributed tracing, metrics, and visualization. Use when setting up mesh monitoring, debugging latency issues, or implementing SLOs for service communication. |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability. |
| `slo-implementation` | Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establishing reliability targets, implementing SRE practices, or measuring service performance. |
| `terraform-module-library` | Build reusable Terraform modules for AWS, Azure, and GCP infrastructure following infrastructure-as-code best practices. Use when creating infrastructure modules, standardizing cloud provisioning, or implementing reusable IaC components. |
| `turborepo-caching` | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or implementing distributed caching. |
| `uv-package-manager` | Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Use when setting up Python projects, managing dependencies, or optimizing Python development workflows with uv. |

## Agents (12)

| Agent | Use quando |
| --- | --- |
| `bash-pro` | Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, portable, and testable shell scripts. |
| `cloud-architect` | Expert cloud architect specializing in AWS/Azure/GCP multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns. Masters serverless, microservices, security, compliance, and disaster recovery. Use PROACTIVELY for cloud architecture, cost optimization, migration planning, or multi-cloud strategies. |
| `deployment-engineer` | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation. Masters GitHub Actions, ArgoCD/Flux, progressive delivery, container security, and platform engineering. Handles zero-downtime deployments, security scanning, and developer experience optimization. Use PROACTIVELY for CI/CD design, GitOps implementation, or deployment automation. |
| `devops-engineer` | Expert in deployment, server management, CI/CD, and production operations. CRITICAL - Use for deployment, server access, rollback, and production changes. HIGH RISK operations. Triggers on deploy, production, server, pm2, ssh, release, rollback, ci/cd. |
| `devops-troubleshooter` | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. Masters log analysis, distributed tracing, Kubernetes debugging, performance optimization, and root cause analysis. Handles production outages, system reliability, and preventive monitoring. Use PROACTIVELY for debugging, incident response, or system troubleshooting. |
| `hybrid-cloud-architect` | Expert hybrid cloud architect specializing in complex multi-cloud solutions across AWS/Azure/GCP and private clouds (OpenStack/VMware). Masters hybrid connectivity, workload placement optimization, edge computing, and cross-cloud automation. Handles compliance, cost optimization, disaster recovery, and migration strategies. Use PROACTIVELY for hybrid architecture, multi-cloud strategy, or complex infrastructure integration. |
| `kubernetes-architect` | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration. Masters EKS/AKS/GKE, service mesh (Istio/Linkerd), progressive delivery, multi-tenancy, and platform engineering. Handles security, observability, cost optimization, and developer experience. Use PROACTIVELY for K8s architecture, GitOps implementation, or cloud-native platform design. |
| `network-engineer` | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization. Masters multi-cloud connectivity, service mesh, zero-trust networking, SSL/TLS, global load balancing, and advanced troubleshooting. Handles CDN optimization, network automation, and compliance. Use PROACTIVELY for network design, connectivity issues, or performance optimization. |
| `observability-engineer` | Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, SLI/SLO management, and incident response workflows. Use PROACTIVELY for monitoring infrastructure, performance optimization, or production reliability. |
| `posix-shell-pro` | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts that run on any POSIX-compliant shell (dash, ash, sh, bash --posix). |
| `service-mesh-expert` | Service mesh architecture with Istio and Linkerd: traffic management, mTLS, observability, progressive delivery. Use for cloud-native networking. |
| `terraform-specialist` | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructure patterns. Handles complex module design, multi-cloud deployments, GitOps workflows, policy as code, and CI/CD integration. Covers migration strategies, security best practices, and modern IaC ecosystems. Use PROACTIVELY for advanced IaC, state management, or infrastructure automation. |

## Workflows (8)

| Workflow | Use quando |
| --- | --- |
| `/config-validate` | Configuration Validation |
| `/cost-optimize` | Cloud Cost Optimization |
| `/deploy` | Deployment command for production releases. Pre-flight checks and deployment execution. |
| `/incident-response` | Orchestrate multi-agent incident response with modern SRE practices for rapid resolution and learning |
| `/migration-observability` | Migration monitoring, CDC, and observability infrastructure |
| `/monitor-setup` | Monitoring and Observability Setup |
| `/preview` | Preview server start, stop, and status check. Local development server management. |
| `/slo-implement` | SLO Implementation Guide |

