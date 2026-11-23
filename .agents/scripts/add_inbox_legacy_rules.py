#!/usr/bin/env python3
"""
Registra nos inboxes dos projetos pendentes a tarefa de remoção de regras duplicadas (GEMINI.md, .agents/rules/)
e atualização do sync_rules.py.
"""

import os
import re
import sys
from pathlib import Path

BASE = Path("/Users/macbookpro/Documents/IA Projects")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import projects_audit

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import linkutil  # noqa: E402

INBOX_TEMPLATE = """# {num} — Remover regras duplicadas (GEMINI.md, .agents/rules/) e atualizar sync_rules

> **Status:** Aberto  
> **Data:** 2026-11-15  
> **Origem:** Auditoria do Kit (Alinhamento com loop "Regras só CLAUDE e AGENTS")  
> **Classificação:** Governança / Padrões / Regras  

---

## Contexto

Em 14/11/2026, o kit central (`0 Padrões`) aboliu a gravação de regras em arquivos legados (`GEMINI.md` e pasta `.agents/rules/`) e unificou a paridade estrita exclusivamente em:
1. `CLAUDE.md` (lido pelo Claude Code)
2. `AGENTS.md` (lido pelo Antigravity e outros agentes)
*(e `.cursorrules` somente se já existir)*

Este projeto foi auditado antes dessa mudança e ainda possui arquivos legados que duplicam regras lidas pelos agentes.

---

## O que deve ser feito neste projeto

1. **Expurgo de Regras Legadas:**
   - Remover `GEMINI.md` na raiz do projeto.
   - Remover a pasta `.agents/rules/` (caso não contenha regras exclusivas do projeto).
   - Se houver `.claude/CLAUDE.md`, remover a duplicata caso duplique o `./CLAUDE.md`.

2. **Atualização do `sync_rules.py`:**
   - Copiar a versão moderna de `.agents/scripts/sync_rules.py` do kit central (`0 Padrões`).
   - O novo script só grava `CLAUDE.md` e `AGENTS.md` (não recria `GEMINI.md` nem `.agents/rules/`).

3. **Remontagem Modular e Validação:**
   - Executar a remontagem com os módulos do projeto via `assemble_rules.py`.
   - Garantir que 100% das regras locais sob `## Local rules` sejam preservadas intactas:
     ```bash
     python3 .agents/scripts/check_local_rules.py .agents/plans/rules-backup-*/CLAUDE.md CLAUDE.md
     ```
   - Validar a paridade dual:
     ```bash
     python3 .agents/scripts/sync_rules.py --check
     ```

4. **Instalação do Hook Pre-commit:**
   - Instalar `.githooks/pre-commit` com `python3 .agents/scripts/sync_rules.py --check` para blindar contra descompassos.
"""

def get_candidates():
    roots = [projects_audit.BASE / r for r in projects_audit.DEFAULT_ROOTS]
    projects = list(projects_audit.discover(roots))
    candidates = []
    for p in projects:
        # Não mexer no próprio kit
        if p.resolve() == Path("/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões").resolve():
            continue
        has_gemini = (p / "GEMINI.md").exists()
        has_rules = (p / linkutil.adir(p) / "rules").is_dir()
        has_claude_dup = (p / ".claude" / "CLAUDE.md").exists() and (p / "CLAUDE.md").exists()
        if has_gemini or has_rules or has_claude_dup:
            inbox_dir = p / "inbox"
            if not inbox_dir.exists():
                continue
            
            # Checar se já existe item sobre regras duplicadas
            existing_files = list(inbox_dir.glob("*.md"))
            already_has = False
            for ef in existing_files:
                if "regras-duplicadas" in ef.name or "gemini" in ef.name.lower():
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
            candidates.append((p, inbox_dir, next_num, has_gemini, has_rules, has_claude_dup))
    return candidates

def main():
    apply = "--apply" in sys.argv
    candidates = get_candidates()
    print(f"Total de projetos candidatos encontrados: {len(candidates)}")
    for p, inbox_dir, next_num, g, r, c in sorted(candidates, key=lambda x: str(x[0])):
        rel = str(p.relative_to(BASE))
        num_str = f"{next_num:03d}"
        target_file = inbox_dir / f"{num_str}-remover-regras-duplicadas-e-atualizar-sync-rules.md"
        if apply:
            content = INBOX_TEMPLATE.format(num=num_str)
            target_file.write_text(content, encoding="utf-8")
            print(f"[CRIADO] {rel} -> inbox/{target_file.name}")
        else:
            print(f"[DRY-RUN] {rel} -> inbox/{target_file.name} (GEMINI: {g}, rules: {r}, claude_dup: {c})")

    if not apply:
        print("\nPara gravar os arquivos, execute com a flag --apply.")

if __name__ == "__main__":
    main()

