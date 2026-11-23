# seguranca

Segurança: auditoria, SAST, modelagem de ameaças e STRIDE, segredos, vulnerabilidades, engenharia reversa e forense, mTLS, conformidade (LGPD/GDPR, PCI), contratos e agentes de pentest e resposta a incidentes de segurança.

> Gerado por build_sip_index.py. Não edite à mão. Skill: `"<HUB>/.agents/skills/<nome>/SKILL.md"`; agent: `"<HUB>/.agents/agents/<nome>.md"`; workflow: `"<HUB>/.agents/workflows/<nome>.md"`.

## Skills (23)

| Skill | Use quando |
| --- | --- |
| `anti-reversing-techniques` | Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use when analyzing protected binaries, bypassing anti-debugging for authorized analysis, or understanding software protection mechanisms. |
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. |
| `auth-implementation-patterns` | Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access control systems. Use when implementing auth systems, securing APIs, or debugging security issues. |
| `binary-analysis-patterns` | Master binary analysis patterns including disassembly, decompilation, control flow analysis, and code pattern recognition. Use when analyzing executables, understanding compiled code, or performing static analysis on binaries. |
| `claude-security-scan` | Use when scanning a repository, branch diff, pull request or commit for vulnerabilities with the Claude Security plugin (/claude-security), reading CLAUDE-SECURITY reports (md, jsonl, SARIF), turning findings into reviewed patches, or choosing between security-review, deep scan, Code Review and CI scanners. Also for varredura de vulnerabilidades. |
| `employment-contract-templates` | Create employment contracts, offer letters, and HR policy documents following legal best practices. Use when drafting employment agreements, creating HR policies, or standardizing employment documentation. |
| `gdpr-data-handling` | Implement GDPR-compliant data handling with consent management, data subject rights, and privacy by design. Use when building systems that process EU personal data, implementing privacy controls, or conducting GDPR compliance reviews. |
| `k8s-security-policies` | Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when securing Kubernetes clusters, implementing network isolation, or enforcing pod security standards. |
| `memory-forensics` | Master memory forensics techniques including memory acquisition, process analysis, and artifact extraction using Volatility and related tools. Use when analyzing memory dumps, investigating incidents, or performing malware analysis from RAM captures. |
| `memory-safety-patterns` | Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing safe systems code, managing resources, or preventing memory bugs. |
| `mtls-configuration` | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate management, or securing internal service communication. |
| `pci-compliance` | Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment processing, achieving PCI compliance, or implementing payment card security measures. |
| `protocol-reverse-engineering` | Master network protocol reverse engineering including packet analysis, protocol dissection, and custom protocol documentation. Use when analyzing network traffic, understanding proprietary protocols, or debugging network communication. |
| `red-team-tactics` | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. |
| `sast-configuration` | Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Use when setting up security scanning, implementing DevSecOps practices, or automating code vulnerability detection. |
| `secrets-management` | Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive credentials, rotating secrets, or securing CI/CD environments. |
| `security-guidance-plugin` | Use when enabling, tuning or debugging the Claude Code security-guidance plugin that reviews Claude's own edits for vulnerabilities during a session, when adding custom security rules or patterns to it, or when writing code that uses eval or exec, unsafe deserialization, raw DOM injection or CI workflow files. Also for avisos de segurança durante a edição. |
| `security-requirement-extraction` | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases. |
| `solidity-security` | Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing smart contracts, auditing existing contracts, or implementing security measures for blockchain applications. |
| `stride-analysis-patterns` | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating security documentation. |
| `threat-mitigation-mapping` | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness. |
| `vibecoding-security-audit` | Use when an app built or edited with AI needs a security pass before shipping - exposed secrets, Supabase row level security, auth and sessions, user uploads, a new dependency an AI suggested, or AI and usage-priced routes that could run up a bill. Also for "auditoria de segurança" or "vibecoding security audit" requests. |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. |

## Agents (11)

| Agent | Use quando |
| --- | --- |
| `backend-security-coder` | Expert in secure backend coding practices specializing in input validation, authentication, and API security. Use PROACTIVELY for backend security implementations or security code reviews. |
| `firmware-analyst` | Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering. Masters firmware extraction, analysis, and vulnerability research for routers, IoT devices, automotive systems, and industrial controllers. Use PROACTIVELY for firmware security audits, IoT penetration testing, or embedded systems research. |
| `frontend-security-coder` | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side security patterns. Use PROACTIVELY for frontend security implementations or client-side security code reviews. |
| `incident-responder` | Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incident management. Masters incident command, blameless post-mortems, error budget management, and system reliability patterns. Handles critical outages, communication strategies, and continuous improvement. Use IMMEDIATELY for production incidents or SRE practices. |
| `legal-advisor` | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements. Use PROACTIVELY for legal documentation, compliance texts, or regulatory requirements. |
| `malware-analyst` | Expert malware analyst specializing in defensive malware research, threat intelligence, and incident response. Masters sandbox analysis, behavioral analysis, and malware family identification. Handles static/dynamic analysis, unpacking, and IOC extraction. Use PROACTIVELY for malware triage, threat hunting, incident response, or security research. |
| `mobile-security-coder` | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific security patterns. Use PROACTIVELY for mobile security implementations or mobile security code reviews. |
| `penetration-tester` | Expert in offensive security, penetration testing, red team operations, and vulnerability exploitation. Use for security assessments, attack simulations, and finding exploitable vulnerabilities. Triggers on pentest, exploit, attack, hack, breach, pwn, redteam, offensive. |
| `reverse-engineer` | Expert reverse engineer specializing in binary analysis, disassembly, decompilation, and software analysis. Masters IDA Pro, Ghidra, radare2, x64dbg, and modern RE toolchains. Handles executable analysis, library inspection, protocol extraction, and vulnerability research. Use PROACTIVELY for binary analysis, CTF challenges, security research, or understanding undocumented software. |
| `security-auditor` | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vulnerability assessment, threat modeling, secure authentication (OAuth2/OIDC), OWASP standards, cloud security, and security automation. Handles DevSecOps integration, compliance (GDPR/HIPAA/SOC2), and incident response. Use PROACTIVELY for security audits, DevSecOps, or compliance implementation. |
| `threat-modeling-expert` | Threat modeling and security architecture review: STRIDE, PASTA, attack trees, risk scoring, mitigation design. Use before building security-sensitive features. |

## Workflows (6)

| Workflow | Use quando |
| --- | --- |
| `/compliance-check` | Regulatory Compliance Check |
| `/deps-audit` | Dependency Audit and Security Analysis |
| `/security-dependencies` | Dependency Vulnerability Scanning |
| `/security-hardening` | Implement comprehensive security hardening with defense-in-depth strategy through coordinated multi-agent orchestration |
| `/security-sast` | Static Application Security Testing (SAST) for code vulnerability analysis across multiple languages and frameworks |
| `/xss-scan` | XSS Vulnerability Scanner for Frontend Code |

