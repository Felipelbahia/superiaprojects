# 🧠 Matriz Canônica de Inteligência de Negócio (Super IA Projects)

> **Módulo Transversal de Inteligência para o Ecossistema Super IA Projects.**  
> Este documento define a arquitetura, taxonomia e integração da Inteligência de Negócio para qualquer projeto de software, SaaS, consultoria ou marketing.

---

## 🎯 Por que Inteligência de Negócio Transversal?

A inteligência de mercado não pertence exclusivamente ao departamento de marketing. Ela orienta:
1. **Desenvolvimento de Produto (SaaS):** Identificar se uma funcionalidade tem demanda real de busca antes de codificar (via Google Trends).
2. **Defesa de Preço & Valor Comercial:** Municiar reuniões de vendas e propostas com dados auditados de mercado (Gartner, MIT, Sebrae).
3. **Autoridade & PR:** Transformar fundadores em porta-vozes requisitados por jornalistas de tecnologia e negócios.
4. **Newsjacking & Timing:** Reagir em menos de 2 horas a mudanças regulatórias, escândalos ou lançamentos de Big Techs.
5. **Engenharia Reversa de Concorrentes & Formatos Virais:** Analisar os conteúdos que performam 3x acima da média no mercado, minerar padrões de ganchos (`hook-mining`) e desmontar formatos de alta retenção (`reel-analyzer`) sem depender de ferramentas pagas.

---

## 🏛️ Os 4 Pilares da Matriz Canônica

```text
inteligencia/
├── 1_radar_tendencias/      # Sinais de busca (Google Trends), fóruns e formatos virais concorrentes (Hooks / Reels)
├── 2_imprensa_pr/           # Posicionamento como fonte, matriz de newsjacking e pautas com quotes
├── 3_estudos_embasamento/   # Dados auditados, banco de cases e pesquisas proprietárias
└── 4_fontes_e_coleta/      # Conexão com os motores de Trends, RSS Feed e Mineração de Ganchos
```

---

## 🔌 Motores Conectados Compartilhados

Projetos do ecossistema podem consumir motores utilitários locais ou na nuvem:
- **Previsão de Demanda:** `<CAMINHO_MOTOR_TRENDS>/trends.sh` (Google Trends via pyline/scripts)
- **RSS Feed (Monitoramento):** `<CAMINHO_MOTOR_RSS>/coletor.py` e `avaliar.py` (Monitoramento de imprensa em tempo real)
- **Mineração de Ganchos (`hook-mining`):** `<SUPER_IA_PROJECTS_PATH>/.agent/skills/hook-mining/scripts/mine_hooks.py` (Classificação de 11 padrões psicológicos por regex em PT-BR, power words, suporte a CSV e coleta via Firecrawl)
- **Engenharia Reversa de Vídeo Curto (`reel-analyzer`):** `<SUPER_IA_PROJECTS_PATH>/.agent/skills/reel-analyzer/SKILL.md` (Desmontagem em 5 camadas: Hook 0-3s, Beat Structure, Ritmo/Pacing, Técnica Visual e Blueprint de Remake)

---

## 📋 Catálogo de Prompts Operacionais

- **Prompt 10:** `10-incluir-inteligencia-no-projeto.md` — Para injetar este módulo em projetos novos ou existentes.
- **Prompt 11:** `11-atualizar-inteligencia-global.md` — Para promover dados e melhorias locais de volta ao repositório central.
