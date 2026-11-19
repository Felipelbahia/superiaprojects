#!/usr/bin/env python3
"""Super IA Projects - installer for macOS, Linux and Windows (standard library only).

    python install.py          (Windows: py install.py)

Same steps as install.sh: rules files, AI entrypoints, catalog, and the local prompt templates.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / ".agent" / "scripts"


def run(script: str, *args: str) -> int:
    env = {**os.environ, "PYTHONUTF8": "1"}  # same output and file encoding on Windows consoles
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=ROOT, env=env).returncode


def main() -> int:
    print("Super IA Projects - Setup do Ecossistema Multi-IA\n")
    claude, example = ROOT / "CLAUDE.md", ROOT / "CLAUDE.example.md"
    if not claude.exists():
        shutil.copyfile(example, claude)
        print("CLAUDE.md criado a partir de CLAUDE.example.md.")
    else:
        print("CLAUDE.md já existe, preservando seu arquivo local.")
    if not (ROOT / "AGENTS.md").exists():
        print("Criando AGENTS.md (cópia do CLAUDE.md)...")
        run("sync_rules.py")
    if run("sync_rules.py", "--check") != 0:
        print("Arquivos de regra fora de paridade: rode python .agent/scripts/sync_rules.py quando quiser alinhar.")

    print("\nAjustando os caminhos do kit nas skills, prompts e docs para este local...")
    status = run("localize_paths.py")
    print("\nSincronizando entrypoints para Claude Code e Cursor (symlink, junction ou cópia)...")
    status |= run("sync_entrypoints.py")
    print("\nGerando catálogo unificado...")
    status |= run("generate_catalog.py")
    print("\nAtualizando os prompt templates (projetos/prompts/)...")
    status |= run("render_prompts.py")

    if status:
        print("\nA instalação terminou com erros: veja as mensagens acima.")
        return 1
    print("\nPronto. Abra .agent/catalog.html no navegador para explorar skills, agentes e workflows.")
    print("Disciplina de mudança: env_diff_check.py e scope_check.py rodam no checklist.py e no hook (ative uma vez: git config core.hooksPath .githooks).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
