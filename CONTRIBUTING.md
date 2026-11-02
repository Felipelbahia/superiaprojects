# Guia de Contribuição — Super IA Projects

Obrigado por querer contribuir com o **Super IA Projects**! Este ecossistema é mantido pelo **Futuro Mercado** e pela comunidade open-source.

---

## 🛠️ Filosofia de Design de Skills (Inspirado no Superpowers)

Seguimos a metodologia **TDD para Documentação**:

1. **Atômica e Modular:** Cada skill deve resolver um único domínio bem definido. Não crie "mega-skills" genéricas.
2. **Gatilhos Explícitos (YAML Frontmatter):**
   ```yaml
   ---
   name: minha-skill
   description: Use when [gatilho específico com palavras-chave claras].
   ---
   ```
3. **Scripts Dentro da Skill:** Qualquer script executável auxiliar deve residir em `.agent/skills/<nome-da-skill>/scripts/<script>.py`.
4. **Sem Caminhos Absolutos:** Nunca use `/Users/...` ou caminhos específicos da sua máquina local. Use sempre referências relativas.

---

## 🚀 Como Criar uma Nova Skill ou Agente

### 1. Criar a pasta da Skill
```bash
mkdir -p .agent/skills/minha-skill
```

### 2. Criar o arquivo `SKILL.md`
Escreva a documentação procedural contendo instruções diretas para o agente, ferramentas necessárias e critérios de validação.

### 3. Sincronizar Entrypoints e Validar
Após adicionar qualquer skill, persona de agente ou comando de workflow:
```bash
python3 .agent/scripts/sync_entrypoints.py
```
Isso criará automaticamente os symlinks necessários para o **Claude Code** (`.claude/skills/`) e validará o frontmatter.

### 4. Regenerar o Catálogo
```bash
python3 .agent/scripts/generate_catalog.py
```
Isso atualizará o índice Markdown (`.agent/CATALOG.md`) e o painel visual (`catalog.html`).

---

## 📋 Como Submeter Pull Requests

1. Crie uma branch para a sua feature: `git checkout -b feature/minha-nova-skill`
2. Certifique-se de que a validação passou: `python3 .agent/scripts/sync_entrypoints.py --check`
3. Envie o PR descrevendo o problema resolvido e os testes executados.

---

**Futuro Mercado** — [www.futuromercado.com.br](https://www.futuromercado.com.br) | [@felipelbahia](https://instagram.com/felipelbahia)
