# Global Coding Standards & Architecture - 0 Padrões

> **Reference for AI Agents**
> This document defines the baseline standards for VibeCoding projects and the 0 Padrões master repository.

## 1. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Directories** | kebab-case | `components/user-profile`, `features/auth` |
| **React Components** | PascalCase | `UserProfile.tsx`, `SubmitButton.tsx` |
| **Hooks** | camelCase (prefix `use`) | `useAuth.ts`, `useWindowSize.ts` |
| **Utilities/Functions** | camelCase | `formatDate.ts`, `calculateTotal.ts` |
| **Types/Interfaces** | PascalCase | `User.ts`, `ApiResponse.ts` |
| **Constants** | SCREAMING_SNAKE_CASE | `MAX_RETRY_LIMIT`, `API_BASE_URL` |
| **Database Migrations** | snake_case (timestamped) | `20240101_add_users_table.sql` |

## 2. Standard Folder Structure

- **`/.agents/`**: Root AI configuration, agents, skills, workflows and rules
- **`/CLAUDE.md` and `/AGENTS.md`**: Master rule files, identical (`GEMINI.md` and `.agents/rules/` are legacy)
- **`/.agents/skills/`**: Modular skills index and domain instructions
- **`/.agents/scripts/`**: Automation and verification scripts
- **`/projetos/`**: Central registry of all VibeCoding projects and sheets

## 3. General Principles from `clean-code` Skill

- **SRP**: Single Responsibility Principle.
- **DRY**: Don't Repeat Yourself.
- **KISS**: Keep It Simple, Stupid.
- **YAGNI**: You Aren't Gonna Need It.

## 4. Agent Instructions

- When entering a new project, check for a root `STANDARDS.md`.
- Ensure dual rules parity (`CLAUDE.md`, `AGENTS.md`) is 100% preserved.
- Always check `.agents/workflows` for project-specific automation.
