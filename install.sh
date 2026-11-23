#!/usr/bin/env bash
# ==============================================================================
# Super IA Projects - One-Line Installer & Setup
# Futuro Mercado - www.futuromercado.com.br
# ==============================================================================

set -e

echo ""
echo "🚀 ==================================================="
echo "    Super IA Projects - Setup do Ecossistema Multi-IA"
echo "    Por Felipe Bahia (Futuro Mercado)"
echo "    www.futuromercado.com.br | @felipelbahia"
echo "======================================================"
echo ""

# 1. Checar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não foi encontrado. Por favor, instale o Python 3 antes de continuar."
    exit 1
fi

echo "✅ Python 3 detectado."

# 2. Inicializar regras se não existirem
if [ ! -f "CLAUDE.md" ]; then
    echo "📋 Criando CLAUDE.md a partir de CLAUDE.example.md..."
    cp CLAUDE.example.md CLAUDE.md
    echo "✅ CLAUDE.md criado com sucesso."
else
    echo "ℹ️  CLAUDE.md já existe, preservando seu arquivo local."
fi

# 2b. AGENTS.md (Antigravity e outras IAs) é a cópia idêntica do CLAUDE.md; só é criado se não existir.
if [ ! -f "AGENTS.md" ]; then
    echo "📋 Criando AGENTS.md (cópia do CLAUDE.md para Antigravity e outras IAs)..."
    python3 .agents/scripts/sync_rules.py
fi
# GEMINI.md e .agents/rules/ são legado: só avisa, nunca apaga sozinho.
python3 .agents/scripts/sync_rules.py --check || echo "ℹ️  Arquivos de regra fora de paridade: rode python3 .agents/scripts/sync_rules.py quando quiser alinhar."

# 2c. Trocar o caminho do kit (escrito na máquina do autor) pelo local onde este kit está
echo "📍 Ajustando os caminhos do kit nas skills, prompts e docs para este local..."
python3 .agents/scripts/localize_paths.py

# 3. Sincronizar Entrypoints (Claude Code, Antigravity, Cursor)
echo "🔗 Sincronizando symlinks para Claude Code e Cursor..."
python3 .agents/scripts/sync_entrypoints.py

# 4. Regenerar Catálogo Unificado
echo "📊 Gerando catálogo unificado (Markdown e HTML interativo)..."
python3 .agents/scripts/generate_catalog.py

# 5. Atualizar os prompt templates (cópia local em projetos/prompts/ com o caminho real do kit)
echo "📝 Atualizando os prompt templates (projetos/prompts/)..."
python3 .agents/scripts/render_prompts.py

echo ""
echo "🎉 ==================================================="
echo "    Tudo pronto! Seu Super IA Projects está ativo."
echo ""
echo "    Para explorar as 220+ skills e 130+ agentes:"
echo "    👉 Abra o arquivo: .agents/catalog.html no seu navegador."
echo "    (Windows: rode  py install.py  no lugar deste script.)"
echo "    Disciplina de mudança: env_diff_check.py e scope_check.py rodam no checklist.py"
echo "    e no hook (ative uma vez: git config core.hooksPath .githooks)."
echo "======================================================"
echo ""
