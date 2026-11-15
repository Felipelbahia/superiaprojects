#!/usr/bin/env python3
"""
Registra nos inboxes de todos os projetos do ecossistema a orientação completa
sobre o Mapeamento de Modelos Cross-Platform (Antigravity vs Claude Code)
e a sincronização inteligente de entrypoints.
"""

import os
import re
import sys
from pathlib import Path

BASE = Path("/Users/macbookpro/Documents/IA Projects")
KIT_ROOT = Path("/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões")
sys.path.insert(0, str(KIT_ROOT / ".agent/scripts"))
import projects_audit

# Template para os outros projetos (explicação completa desde o início)
EXTERNAL_PROJECT_INBOX_TEMPLATE = """# {num} — Mapeamento de modelos cross-platform (Antigravity vs Claude Code) e sincronização

> **Status:** Aberto  
> **Data:** 2026-11-15  
> **Origem:** Kit Central / Governança (Loop "Mapeamento de Modelos e Economia de Contexto")  
> **Classificação:** Governança / Agentes / Sincronização  

---

## 1. Contexto & Divergência entre Plataformas

No ecossistema, os projetos podem ser operados simultaneamente pelo **Antigravity** (Google DeepMind) e pelo **Claude Code** (Anthropic). No entanto, as duas plataformas utilizam especificações diferentes para definir os modelos de execução dos subagentes:

| Plataforma | Caminho dos Agentes | Modelos Suportados no Frontmatter (`model:`) |
|---|---|---|
| **Antigravity** (Geral) | `.agent/agents/*.md` | `inherit` (padrão), `flash_lite`, `flash`, `pro` |
| **Claude Code** | `.claude/agents/*.md` | `inherit` (padrão), `haiku`, `sonnet`, `opus` |

### O Problema Anterior
Historicamente, o arquivo `.agent/` funcionava apenas com symlinks puros para `.claude/agents/`. Isso criava uma incompatibilidade:
- Se um agente declarava um modelo do Antigravity (`flash_lite`), o Claude Code falhava por desconhecer o modelo.
- Se fosse gravado um arquivo com modelo do Claude (`haiku`), ferramentas de auditoria e validação acusavam erro de arquivo real quebrando symlink.

---

## 2. A Solução Implementada no Kit Central

A pasta `.agent/agents/` permanece como a **única fonte da verdade** para agentes. O script `sync_entrypoints.py` agora realiza **conversão inteligente e seletiva de modelos** ao sincronizar para `.claude/agents/`:

1. **`model: inherit` (ou sem campo `model:`):**  
   Mantém o comportamento tradicional de **symlink puro** (`.claude/agents/<nome>.md -> ../../.agent/agents/<nome>.md`).
2. **`model: flash_lite` ou `model: flash`:**  
   Gera um arquivo físico em `.claude/agents/<nome>.md` substituindo o modelo por `model: haiku`.
3. **`model: pro`:**  
   Gera um arquivo físico em `.claude/agents/<nome>.md` substituindo o modelo por `model: sonnet`.

Todo arquivo gerado por conversão recebe no topo o cabeçalho identificador:
```html
<!-- antigravity-kit:generated from ../../.agent/agents/<nome>.md (model: <target>) -->
```
O comando `python3 .agent/scripts/sync_entrypoints.py --check` valida tanto os symlinks quanto os arquivos convertidos legítimos, garantindo paridade de conteúdo sem acusar erros.

---

## 3. Protocolo de Retorno Limpo (Clean Return Protocol)

Junto com a padronização de modelos, foi instituída a regra obrigatória de economia de contexto para subagentes:
- Subagentes **nunca** devem despejar saídas brutas de terminal, logs extensos ou cópias integrais de código no chat.
- Cargas pesadas pertencem ao disco (`.agent/plans/`, `scratchpad/` ou mapas de destino).
- O retorno de qualquer subagente deve ser estritamente executivo:
  1. Status de uma linha (`CONCLUÍDO`, `BLOQUEADO`, etc.).
  2. 3 a 5 tópicos resumindo os resultados com links clicáveis para os arquivos gerados.
  3. Apenas dúvidas bloqueantes ou decisões que exijam validação humana.

---

## 4. O que deve ser feito neste projeto

Quando este projeto for aberto para manutenção ou criação de agentes:

1. **Declaração de Agentes:**
   - Se o projeto possuir agentes próprios em `.agent/agents/`, declare os modelos usando a nomenclatura nativa do Antigravity (`inherit`, `flash_lite`, `pro`).
2. **Sincronização:**
   - Executar a sincronização de entrypoints para gerar os links e arquivos compatíveis com o Claude Code:
     ```bash
     python3 .agent/scripts/sync_entrypoints.py
     ```
3. **Validação:**
   - Conferir se todos os links e entrypoints estão íntegros:
     ```bash
     python3 .agent/scripts/sync_entrypoints.py --check
     ```
"""

# Template para o kit central (0 Padrões)
KIT_INBOX_TEMPLATE = """# 035 — Mapeamento de modelos cross-platform (Antigravity vs Claude Code) e migração dos 130 agentes

> **Status:** Aberto  
> **Data:** 2026-11-15  
> **Origem:** Kit Central (Loop "Mapeamento de Modelos e Economia de Contexto")  
> **Classificação:** Governança / Agentes / Padrões  

---

## 1. Contexto

O loop de execução `Mapeamento de Modelos e Economia de Contexto` implementou em `.agent/scripts/sync_entrypoints.py` a matriz `MODEL_MAP_ANTIGRAVITY_TO_CLAUDE`:
- `flash_lite` / `flash` -> `haiku`
- `pro` -> `sonnet`
- `inherit` -> symlink

Os testes unitários em `test_sync_scripts.py` (`SyncEntrypointsModelConversion`) cobrem 100% dos cenários e o script valida perfeitamente.

---

## 2. Pendência Técnica Identificada no Kit

Atualmente, o repositório central possui **130 agentes** sob `.agent/agents/`.
A grande maioria dos agentes com modelo explícito ainda utiliza a nomenclatura da Anthropic diretamente no arquivo fonte:
- `model: sonnet` (ex: `codebase-analyzer`, `database-admin`, `debugger`, `devops-troubleshooter`, etc.)
- `model: haiku` (ex: `customer-support`, `sales-automator`, `seo-content-planner`, etc.)
- `model: opus` (ex: `security-auditor`, `python-pro`, `rust-pro`, `fastapi-pro`, etc.)

Como a pasta `.agent/agents/` é lida diretamente pelo Antigravity, valores como `sonnet` e `opus` não são reconhecidos nativamente pelo Antigravity ao despachar subagentes (`enum: ['inherit', 'flash_lite', 'flash', 'pro']`).

---

## 3. Decisão do Dono & Ações Necessárias

Avaliar e escolher a estratégia de alinhamento:

* **Opção A (Padronização na Fonte - Recomendada):**
  Migrar os frontmatters dos agentes em `.agent/agents/*.md` para os nomes do Antigravity:
  - `haiku` -> `flash_lite`
  - `sonnet` -> `pro`
  - `opus` -> `pro` (ou `inherit`)
  E deixar o `sync_entrypoints.py` gerar automaticamente as versões convertidas para `.claude/agents/*.md`.

* **Opção B (Mapeamento Bidirecional no Sync):**
  Ajustar o `sync_entrypoints.py` para mapear nos dois sentidos ou aceitar ambas as tabelas sem quebrar o Antigravity.
"""

def get_inbox_projects():
    roots = [projects_audit.BASE / r for r in projects_audit.DEFAULT_ROOTS]
    projects = list(projects_audit.discover(roots))
    results = []

    for p in projects:
        # Pular subdiretórios de código internos como pacotes Go (ex: IL - App/internal/application)
        rel_str = str(p.relative_to(BASE))
        if "/internal/" in rel_str or "/node_modules/" in rel_str or "/.venv/" in rel_str:
            continue
        if not ((p / "CLAUDE.md").exists() or (p / "AGENTS.md").exists() or (p / ".agent").exists()):
            continue
        
        inbox_dir = p / "inbox"
        if not inbox_dir.is_dir():
            continue

        rel = str(p.relative_to(BASE))
        is_kit = (p.resolve() == KIT_ROOT.resolve())

        # Calcular próximo número
        existing_files = list(inbox_dir.glob("*.md"))
        
        # Checar se já tem arquivo sobre modelos
        already_has = False
        for ef in existing_files:
            if "mapeamento-de-modelos" in ef.name:
                already_has = True
                break
        if already_has:
            continue

        nums = []
        for ef in existing_files:
            if ef.name == "README.md":
                continue
            m = re.match(r"^(\d+)", ef.name)
            if m:
                nums.append(int(m.group(1)))
        next_num = max(nums) + 1 if nums else 1
        results.append((p, inbox_dir, next_num, is_kit, rel))

    return results

def main():
    apply = "--apply" in sys.argv
    projects = get_inbox_projects()
    print(f"Total de projetos com pasta inbox encontrados: {len(projects)}")

    for p, inbox_dir, next_num, is_kit, rel in sorted(projects, key=lambda x: str(x[0])):
        num_str = f"{next_num:03d}"
        if is_kit:
            target_file = inbox_dir / f"{num_str}-mapeamento-de-modelos-antigravity-claude-e-migracao-de-agentes.md"
            content = KIT_INBOX_TEMPLATE
        else:
            target_file = inbox_dir / f"{num_str}-mapeamento-de-modelos-cross-platform-antigravity-claude.md"
            content = EXTERNAL_PROJECT_INBOX_TEMPLATE.format(num=num_str)

        if apply:
            target_file.write_text(content, encoding="utf-8")
            print(f"[CRIADO] {rel} -> inbox/{target_file.name}")
        else:
            print(f"[DRY-RUN] {rel} -> inbox/{target_file.name}")

    if not apply:
        print("\nPara gravar os arquivos nos inboxes, execute com --apply.")

if __name__ == "__main__":
    main()
