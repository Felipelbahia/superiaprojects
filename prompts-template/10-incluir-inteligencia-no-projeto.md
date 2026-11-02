# Incluir Módulo de Inteligência de Negócio no Projeto (PULL)

Quero injetar o **Módulo Canônico de Inteligência de Negócio** neste projeto, adaptando-o ao contexto da marca/produto, com base no padrão central em `Super IA Projects` (`<SUPER_IA_PROJECTS_PATH>`).

Este módulo capacita qualquer projeto (seja de Marketing, SaaS, Serviços ou Novos Negócios) a:
1. **Monitorar tendências e demanda real** via Google Trends (motor `Previsão de Demanda`).
2. **Monitorar a imprensa digital e notícias do setor em tempo real** (motor `RSS Feed` cobrindo 293 veículos).
3. **Fundamentar teses com dados auditados** para apoiar vendas, posicionamento e tomadas de decisão.
4. **Gerar pautas e citações para a imprensa especializada (PR)**.
5. **Minerar ganchos e realizar engenharia reversa de concorrentes em vídeo curto** via skills `hook-mining` e `reel-analyzer` (do `0 Mkt`), identificando formatos de alta retenção sem ferramentas pagas.

REGRAS: Nunca apague nem sobrescreva regras locais do projeto: MESCLE. Preserve convenções existentes. Nunca afirme que algo existe sem ter verificado com comando ou leitura. Sem commit sem eu pedir.

---

## 1. Descoberta & Diagnóstico de Nicho (Socratic Gate)
Antes de criar qualquer pasta, analise o projeto (README.md, brand/ ou docs/):
- **Qual é o modelo do projeto?** (SaaS, Consultoria/Serviço, Conteúdo/Mídia, E-commerce, Venture).
- **Quais são os 3 a 5 termos principais de busca** que indicam demanda ou dor do público-alvo deste negócio?
- **Quais editorias de imprensa interessam?** (`tecnologia_inovacao`, `negocios_economia`, `marketing_comunicacao`, etc.).
- **Que dados ou pesquisas** esse negócio precisa ter à mão para provar autoridade para clientes ou investidores?

---

## 2. Estrutura Canônica de Pastas (`inteligencia/`)
Crie a estrutura canônica na raiz do projeto:

```text
inteligencia/
├── README.md                           # Visão geral da inteligência adaptada a este projeto
├── 1_radar_tendencias/                 # O que está em alta e o que está subindo no nicho
│   ├── README.md                       # Semáforo de maturidade (🟢 Subindo, 🟡 Em Alta, 🔴 Saturado)
│   ├── radar_ativo.md                  # Painel dos temas monitorados no ciclo atual
│   ├── sinais_emergentes.md            # Early signals e termos de busca emergentes
│   ├── hooks_minerados.md              # Ganchos de concorrentes classificados em 11 padrões psicológicos (hook-mining)
│   ├── analise_virais_concorrentes.md  # Desmontagem em 5 camadas de vídeos curtos de alta tração (reel-analyzer)
│   └── trends/                         # Coletas brutas e relatórios de sazonalidade
├── 2_imprensa_pr/                      # Relações Públicas, Imprensa & Newsjacking
│   ├── README.md                       # Posicionamento como fonte no setor
│   ├── matriz_newsjacking.md           # Resposta rápida a notícias quentes do nicho
│   ├── ganchos_imprensa.md             # Pautas sugeridas com quotes dos fundadores
│   └── mapa_veiculos_jornalistas.md    # Veículos Tier 1, 2 e 3 do setor
├── 3_estudos_embasamento/              # Dados checados e relatórios de mercado
│   ├── README.md                       # Critérios de rigor e anti-alucinação
│   ├── acervo_dados_metricas.md        # Tabela mestra de dados e estatísticas do setor
│   ├── banco_de_cases.md               # Casos reais de concorrentes/mercado
│   └── dossies/                        # Dossiês temáticos profundos
└── 4_fontes_e_coleta/                 # Conectores, fontes e rotina
    ├── README.md                       # Governança da rotina de escuta
    ├── fontes_curadas.md               # Portais, newsletters e relatórios do segmento
    ├── termos_inteligencia.txt         # Arquivo de termos ponderados (termo|peso) para o RSS Feed
    ├── motores_conectados.md           # Guia de acionamento do Trends, RSS Feed, yt-dlp e mine_hooks.py
    └── playbook_rotina_semanal.md      # SOP de 30 minutos de escuta semanal
```

---

## 3. Conexão com os Motores Locais do Ecossistema
Crie em `scripts/` os três atalhos executáveis:
1. `scripts/coletar_trends.sh` apontando para `<DEMAND_FORECAST_PATH>/scripts/trends.sh`.
2. `scripts/monitorar_imprensa.sh` apontando para `<RSS_FEED_PATH>/coletor.py` e `avaliar.py`, utilizando o arquivo `inteligencia/4_fontes_e_coleta/termos_inteligencia.txt`.
3. `scripts/minerar_hooks.sh` contendo:
   ```bash
   #!/usr/bin/env bash
   python3 "<MARKETING_HUB_PATH>/.agent/skills/hook-mining/scripts/mine_hooks.py" "$@"
   ```
   (Para coletar títulos de Shorts de concorrentes sem ferramentas pagas: `yt-dlp --flat-playlist --print "%(title)s,%(view_count)s" "<url_canal>/shorts" > shorts.csv`).
Dê permissão de execução: `chmod +x scripts/coletar_trends.sh scripts/monitorar_imprensa.sh scripts/minerar_hooks.sh`.

---

## 4. Governança & Paridade Multi-IA
1. Mescle nas regras do projeto (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`, `.agent/rules/*`) a pasta `inteligencia/` na seção `🏛️ ESTRUTURA DO PROJETO`.
2. Adicione ao `STANDARDS.md` as convenções semafóricas e de dados checados.
3. Execute o script de paridade:
   ```bash
   python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
   ```
   Só prossiga com "100% synchronized".

---

## 5. Registro Central na Ficha do Projeto
1. Abra a ficha técnica deste projeto em `<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md`.
2. Registre: `Módulo de Inteligência de Negócio: Ativo (v1.0)`.
3. Adicione este projeto na lista de projetos com inteligência ativa em `Super IA Projects/projetos/README.md`.

---

## 6. Apresentação Final
Finalize mostrando:
- Resumo do nicho e termos calibrados.
- Confirmação de pastas criadas e permissões de scripts.
- Teste de execução dos atalhos com `--help`.
- Link para a ficha técnica atualizada no `Super IA Projects`.
