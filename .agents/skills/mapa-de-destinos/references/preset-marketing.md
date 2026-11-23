# Preset: projeto de marketing e conteúdo

Migrado da skill `geral-arquitetura-de-projeto` do 0 Mkt (2026-11-12). Vale para projetos que produzem marca, conteúdo, campanhas, imprensa ou vendas. Junte com outros presets em projeto misto. Glossário: **Demanda** = pasta datada `AAAA-MM-DD - Nome da Demanda/` com os arquivos de uma entrega; **Fluxo de aprovação** = como uma peça é aprovada; **Esteira** = pastas `1_a_aprovar`, `2_aprovado`, `3_publicado`, `4_revisar_ajustar`, quando o projeto as escolhe; **Campanha** (não "campaign") em todo caminho novo.

**Escopo por pasta:** cada pasta de topo declara no mapa o seu escopo: `projeto`, `marca` ou `produto`. Só a pasta que diverge entre marcas ou produtos ganha subpasta; o compartilhado fica na raiz. Mono-marca é o caso mais comum.

## As áreas da raiz
| Pasta | O que é | Exemplo |
|---|---|---|
| `brand/` | Regras e identidade da marca | voz, personas, pilares, kit visual, regras de monitoramento |
| `estrategia/` | Planejamento: direção geral e campanhas | estratégia geral, calendários, `campanhas/` |
| `imprensa/` | **Assessoria de imprensa** (produção com ciclo próprio): pauta, pitch, release, seleção de jornalistas, controle de envio, clipping | `imprensa/AAAA-MM-DD - Nome/`, `envios.md`, `clipping/` |
| `vendas/` | **Vendas** (produção com ciclo próprio, na raiz em projeto novo): cadência outbound, playbook de discovery, governança de negócio | `vendas/AAAA-MM-DD - Nome da Demanda/` |
| `conteudos/` | **Produção**: o que a marca cria e publica | roteiro, post, newsletter, e-mail, relatório de cliente |
| `inteligencia/` | **Repositório do mercado**: tendências, pesquisas, estudos, materiais de terceiros, monitoramento. Não guarda o que a marca produz | radar, estudos e cases com fonte, relatório de menções |
| `referencias/` | Referências **do projeto** que influenciam todo o conteúdo | rubrica, perfil e voz, formatos, hooks e iscas já adaptados à marca |
| `assets/` | Arte final e imagens, com inventário | |

Skill que produz peça escreve em `conteudos/`, `imprensa/`, `vendas/` ou `assets/`, nunca em `inteligencia/`. Skill que coleta ou monitora escreve em `inteligencia/`. Registro do que a marca fez (envio de pitch, publicação) é produção: fica em `imprensa/` ou `conteudos/`. A esteira de aprovação vale para `conteudos/`; a imprensa tem o ciclo próprio do `envios.md`.

**Nomes de pasta sem número**, exceto onde o número indica sequência de verdade (a esteira de aprovação: `1_a_aprovar → 4_revisar_ajustar`).

## Campanha é estratégia com foco e prazo
Uma campanha vive em `estrategia/campanhas/AAAA-MM-DD - Nome da Campanha/` e tem um `campanha.md` com objetivo, prazo, etapas, canais e peças, arquivos conectados e **resultado esperado definido antes de começar** (métrica, fonte, janela, critério de sucesso e de fracasso). Ao encerrar, nasce o `resultado.md` (esperado vs. real). As **peças** da campanha ficam em `conteudos/<tipo>/` e o `campanha.md` aponta para elas; cada peça leva `campanha:` nos metadados. Quem cria é `revenue-campanhas` (workflows `revenue-criacao-de-campanha` e `revenue-checklist-de-lancamento-de-campanha`). **Campanha contínua** (sem data de fim) é permitida: `tipo: continua` no `campanha.md`, sem `fim:`, com revisão periódica no lugar da leitura final. Modelo: `revenue-campanhas/references/modelo-campanha.md` (inclui `resultado.md` e a revisão periódica da campanha contínua).

## Assessoria de imprensa
Skill de referência: `pr-assessoria-de-imprensa` (e este mapa).
- **Pauta, pitch, release e seleção de jornalistas** são produção, em `imprensa/AAAA-MM-DD - Nome/`. A **pauta é uma pasta**: `pauta/pauta-principal.md` e um `angulo-<tema>.md` por ângulo; o `pitch/` tem um arquivo por ângulo.
- **Controle de envio** (qual ângulo foi para qual jornalista, quando, e o que voltou): `imprensa/envios.md` (ou `.csv`), com status `enviado → respondeu → publicou → sem retorno` e link para o item do clipping. `lido` é campo opcional (abertura de e-mail é pouco confiável). O envio carrega a demanda e o ângulo (e a marca, em multi-marca; e o produto, nos cenários B e D); o link do clipping usa o nome do arquivo `AAAA-MM-DD_<veiculo>_<tema>.md`. `jornalistas.md` da demanda é a seleção **planejada**; `envios.md` é o **realizado**. Não existe `inteligencia/2_imprensa_pr/`.
- **Clipping** (matérias em que a marca ou o porta-voz é citado): `imprensa/clipping/`.
- **Jornalista, veículo e a metodologia da base** (validação de e-mail, scraping/RSS) só vivem no Hub `Compartilhado/RSS Feed`, nunca duplicados no projeto; consultar via `motores/jornalistas/consultar_hub.py`.
- **Técnica de redação** (ângulos editoriais, matriz de newsjacking, templates de pitch) é playbook reutilizável: mora **na skill** `pr-assessoria-de-imprensa/references/`, não no projeto. O projeto guarda só o que é dele: identidade do porta-voz em `brand/` e a lista de ângulos permanentes da marca (posicionamento) em `brand/ativacao/`. O `angulo-<tema>.md` da pauta é a aplicação de um ângulo a uma pauta específica e cita de qual ângulo permanente nasceu.

## Técnica, referências e inteligência
- **Técnica reutilizável** (playbook de redação, hooks, retenção, formatos genéricos) mora na skill do assunto. **Referência específica do projeto** que influencia todo o conteúdo (rubrica, perfil e voz, formatos adaptados à marca) mora em `referencias/`, na raiz. **Dado e referência do mercado** mora em `inteligencia/`, na raiz, porque alimenta o projeto inteiro. Não existe `conteudos/_base/`; o que seria personalização de uma demanda vai no `briefing.md` da pasta dela.

## Dois modos
| Modo | Quando | Fundações da marca | Peças de conteúdo | Inventário de imagens |
|---|---|---|---|---|
| **0 Mkt** | Marca hospedada no 0 Mkt (`_brands/<marca>/`) | `_brands/<marca>/` | `content/<marca>/<tipo>/AAAA-MM-DD - Nome/` | `_brands/<marca>/ativos/inventario.md` |
| **Projeto** | Marca com projeto próprio (Futuro Mercado, WaiMonitor) | `<projeto>/brand/` (raiz da marca) | `<projeto>/conteudos/` (pastas por tipo e/ou esteira, conforme o mapa) | `<projeto>/assets/inventario.md` |
Projeto novo usa o modo **Projeto**. No modo 0 Mkt, a campanha vive em `content/<marca>/estrategia/campanhas/…` (ver o mapa do 0 Mkt). A árvore completa e as convenções de nome estão na seção "Árvore padrão" abaixo; o modelo do mapa está em `modelo-mapa.md`.

**Modo 0 Mkt (marca hospedada no 0 Mkt):** o `docs/mapa-de-destinos.md` do 0 Mkt manda: identidade em `_brands/<marca>/`, output em `content/<marca>/…` (peças em `<tipo>/`, estratégia e campanhas em `estrategia/`, imprensa em `imprensa/`, vendas em `content/<marca>/vendas/`; em projeto novo, `vendas/` é pasta de raiz). O 0 Mkt é multi-marca por desenho e sempre tem a subpasta `<marca>/`.

**Hub Central** (`Compartilhado/RSS Feed`): nunca gravar nele; é fonte de leitura. Dado novo que deve voltar ao Hub passa pelo procedimento do próprio Hub, com confirmação do usuário.

## Quem escreve onde (modo Projeto, mono-marca)
Em multi-marca, use o caminho completo que o mapa traz, com placeholders (por exemplo `marcas/{marca}/conteudos/{tipo}/`); não monte o prefixo por conta própria.

| Família de skill | Escreve em | Lê de |
|---|---|---|
| Marca (`brand-builder` e sub-skills) | `brand/` e `brand/ativacao/`, `brand/logo/`, `brand/modelos/`, `brand/design-system/` | o próprio `brand/` |
| Estratégia e campanha (`revenue-campanhas`, `conteudo-estrategia`) | `estrategia/`, `estrategia/campanhas/AAAA-MM-DD - Nome/` | `brand/`, `inteligencia/` |
| Conteúdo (peças de qualquer tipo) | `conteudos/<tipo>/AAAA-MM-DD - Nome da Demanda/` e/ou a esteira (`1_a_aprovar` …), conforme o mapa | `brand/`, `estrategia/`, `inteligencia/` |
| Imprensa (`pr-assessoria-de-imprensa`): pauta, pitch, release, seleção de jornalistas, controle de envio, clipping | `imprensa/` | `brand/`, Hub `Compartilhado/RSS Feed` (somente leitura) |
| Vendas (`vendas-direcao-b2b`, `vendas-metodologias-b2b`, `vendas-cold-email`): cadência outbound, playbook de discovery, governança de negócio | `vendas/AAAA-MM-DD - Nome da Demanda/` | `brand/`, `inteligencia/` |
| Monitoramento | **regras** em `brand/ativacao/monitoramento.md` (fonte da verdade); **consultas, termos e relatórios** em `inteligencia/monitoramento/` | Hub (somente leitura), `brand/` |
| Dados e estudos | `inteligencia/estudos/` (registro de fontes, banco de cases) | fontes externas |
| Imagens e arte | `assets/` | `brand/logo/`, `brand/modelos/` |

## Referência rápida
| Preciso de | Pasta |
|---|---|
| Fundações, voz, ativação, kit, modelos | `brand/` |
| Estratégia geral, calendário | `estrategia/` |
| Campanha (plano, meta, resultado) | `estrategia/campanhas/AAAA-MM-DD - Nome/` |
| Post, carrossel, roteiro (com aprovação) | `conteudos/` |
| Técnica de redação (hooks, retenção, formatos, newsjacking) | dentro da skill do assunto, nunca no projeto |
| Benchmark de canal (anexo da ativação) | `brand/ativacao/` |
| Pauta (pasta com ângulos), pitch, release e seleção de jornalistas | `imprensa/AAAA-MM-DD - Nome/` |
| Vendas: cadência outbound, playbook de discovery, governança de negócio | `vendas/AAAA-MM-DD - Nome da Demanda/` (`cadencia-outbound.md`, `playbook-discovery.md`, `deal-governance.md`) |
| Controle de envio de imprensa | `imprensa/envios.md` |
| Clipping | `imprensa/clipping/` |
| Mailing, ficha de jornalista, mapa de veículos, metodologia de e-mail/scraping (**só no Hub**) | `Compartilhado/RSS Feed/bases/jornalistas/`, `bases/veiculos/veiculos.csv` |
| Roteiros de vídeo longo e curto | `conteudos/video/` |
| Blog, LinkedIn, carrossel e post, newsletter, e-mail, apresentação, relatório | `conteudos/blog/`, `linkedin/`, `social/`, `newsletter/`, `email/`, `palestra/`, `apresentacoes/`, `reports/` |
| Consultas de monitoramento, `termos.txt`, relatório de menções | `inteligencia/monitoramento/` |
| Número com fonte, caso do mercado, pesquisa | `inteligencia/estudos/` |
| Tendências | `inteligencia/tendencias/` |
| Imagem e inventário | `assets/` |
| Plano e log de execução | `.agents/plans/` |
| Este mapa | `docs/mapa-de-destinos.md` |

## Fluxo de aprovação: perguntar sempre, padrão é sem esteira
Ao criar o mapa de um projeto novo (ou ao fechar uma inconsistência num projeto sem mapa), perguntar qual das 4 opções usar. Se o usuário não souber ou pular a pergunta, registrar a opção 0 no mapa e seguir:

| # | Opção | Estrutura | Quando preferir |
|---|---|---|---|
| **0 (padrão)** | Sem esteira | Estado vai no campo `status:` dos metadados, dentro de `conteudos/<tipo>/AAAA-MM-DD - Nome/`. Nenhuma pasta nova. | Uma pessoa só aprovando; poucas peças por vez. **É a resposta se o usuário não disser nada.** |
| **A** | Esteira geral, tudo junto | `conteudos/1_a_aprovar/`, `2_aprovado/`, `3_publicado/`, `4_revisar_ajustar/` com peças de todos os tipos misturadas | Volume baixo e um fluxo só |
| **B** | Esteira, espinha primeiro (tipo dentro) | `conteudos/1_a_aprovar/<tipo>/`, `2_aprovado/<tipo>/` … | Mais de uma pessoa aprovando e querendo ver tudo que está num estágio. Precedente: Futuro Mercado (ADR-002, `.agents/plans/fluxo-de-aprovacao-das-pecas.md`) |
| **C** | Esteira, tipo primeiro (estágio dentro) | `conteudos/<tipo>/1_a_aprovar/`, `conteudos/<tipo>/2_aprovado/` … | Equipes por tipo de conteúdo |

Se a resposta for A, B ou C, registrar a escolha no `docs/mapa-de-destinos.md` (linha "Fluxo de aprovação") para não perguntar de novo. Nomes das pastas da esteira ficam sempre `1_a_aprovar`, `2_aprovado`, `3_publicado`, `4_revisar_ajustar`.

## Criar projeto novo (checklist de marketing)
- [ ] Conduzir a **conversa de criação** (marcas e produtos, onde moram, o que é compartilhado)
- [ ] Criar a árvore da seção "Árvore padrão" deste arquivo (só as pastas que o projeto usa; as demais nascem quando precisar)
- [ ] Regras do projeto montadas pelo kit (módulo `content`) com o `sip-marketing` instalado
- [ ] Criar `STANDARDS.md` com nome de arquivo e metadados de peça (inclui o campo `campanha:`)
- [ ] **Perguntar o fluxo de aprovação** (seção acima) antes de escrever o mapa
- [ ] Criar `docs/mapa-de-destinos.md` pelo modelo, com a coluna Escopo, e dizer ao usuário o que cada linha significa
- [ ] Criar o registro de fontes (`registro-de-fontes.md` do `brand-builder`) em `inteligencia/estudos/`
- [ ] **Confirmar com o usuário antes de escrever fora do 0 Mkt**

## Linhas do mapa (modo Projeto)
| Tipo de peça | Caminho | Escopo | Nome e metadados | Observação |
|---|---|---|---|---|
| Fundações da marca e ativação | brand/ | projeto | etapas do brand-builder; versões -vN | |
| Kit visual e modelos | brand/logo/, brand/modelos/, brand/design-system/ | projeto | | |
| Estratégia geral | estrategia/estrategia-geral.md | projeto | | |
| Calendários | estrategia/calendarios/ | projeto | | |
| Campanha (plano, meta, resultado) | estrategia/campanhas/AAAA-MM-DD - Nome da Campanha/ | projeto | `campanha.md`, `checklist-lancamento.md`, `apresentacao.html`, `resultado.md` | resultado esperado definido antes de começar; as peças ficam em conteudos/ |
| Peça de conteúdo por tipo (blog, linkedin, social, newsletter, video…) | conteudos/{tipo}/AAAA-MM-DD - Nome da Demanda/ | projeto | `briefing.md`, `draft.md`; campo `campanha:` | |
| Fluxo de aprovação | <ver "Respostas" abaixo> | projeto | | opção 0 usa o campo `status:`; A/B/C usam as pastas da esteira |
| Assessoria de imprensa: pauta (pasta com ângulos), pitch por ângulo, release, jornalistas | imprensa/AAAA-MM-DD - Nome/ | projeto | `pauta/pauta-principal.md`, `pauta/angulo-<tema>.md`, `pitch/`, `release.md`, `jornalistas.md` | |
| Vendas: cadência outbound, playbook de discovery, governança de negócio | vendas/AAAA-MM-DD - Nome da Demanda/ | projeto | `cadencia-outbound.md`, `playbook-discovery.md`, `deal-governance.md` | pasta de raiz, como imprensa/ |
| Controle de envio de imprensa | imprensa/envios.md | projeto | uma linha por envio | status enviado → respondeu → publicou → sem retorno |
| Clipping | imprensa/clipping/ | projeto | `AAAA-MM-DD_<veiculo>_<tema>.md` | |
| Peças publicadas (registro) | conteudos/publicados.md | projeto | | |
| Monitoramento (consultas, termos, relatório) | inteligencia/monitoramento/ | projeto | | regras em brand/ativacao/monitoramento.md |
| Estudos, dados, cases, registro de fontes | inteligencia/estudos/ | projeto | | |
| Tendências | inteligencia/tendencias/ | projeto | | |
| Fontes e coleta | inteligencia/fontes-e-coleta/ | projeto | | |
| Referências do projeto (rubrica, perfil e voz, formatos adaptados) | referencias/ | projeto | | influenciam todo conteúdo; técnica genérica fica na skill |
| Imagens | assets/ (inventario.md) | projeto | `uso_assunto_AAAA-MM-DD_v1.ext` | |
| Documentos do projeto | docs/ | projeto | | este mapa e demais |
| Planos e log de execução | .agents/plans/ | projeto | | |
| Hub Central | Compartilhado/RSS Feed | — | | **somente leitura** |

## Árvore padrão (modo Projeto, mono-marca)
**Este é o padrão: uma marca ou produto, sem subpasta de marca no caminho.** Marcas e produtos múltiplos só entram se o usuário disser que sim na conversa de criação (ver `cenarios-multi-marca.md`).

Baseada no projeto Futuro Mercado (Marketing - FM), que a testou, com os ajustes de 2026-11-07. Cada pasta nasce quando o projeto precisa dela.

```text
<projeto>/
├── CLAUDE.md  AGENTS.md   # regras do projeto (paridade); acesso ao 0 Mkt pelo sip-marketing
├── STANDARDS.md                      # nome de arquivo e metadados de peça (inclui `campanha:`)
├── brand/                            # raiz da marca
│   ├── 00-intake.md … brandbook.md   # fundações (etapas do brand-builder)
│   ├── _respostas/                   # respostas literais do usuário, por rodada
│   ├── ativacao/                     # conteudo.md, monitoramento.md, audiovisual.md, demanda.md, anexos (referências, ângulos próprios da marca)
│   ├── design-system/  logo/  modelos/
│   ├── identidade-e-ativos.md  registro-de-decisoes.md
├── estrategia/                       # PLANEJAMENTO
│   ├── estrategia-geral.md
│   ├── calendarios/
│   └── campanhas/AAAA-MM-DD - Nome da Campanha/   # campanha.md, checklist-lancamento.md, apresentacao.html, resultado.md
├── imprensa/                         # ASSESSORIA DE IMPRENSA (produção com ciclo próprio)
│   ├── AAAA-MM-DD - Nome/            # pauta/ (pauta-principal.md + angulo-<tema>.md), pitch/ (um por ângulo), release.md, jornalistas.md
│   ├── envios.md                     # controle de envio: enviado → respondeu → publicou → sem retorno
│   └── clipping/
├── vendas/                           # VENDAS (produção com ciclo próprio, na raiz)
│   └── AAAA-MM-DD - Nome da Demanda/ # cadencia-outbound.md, playbook-discovery.md, deal-governance.md
├── conteudos/                        # PRODUÇÃO: o que a marca cria e guarda
│   ├── <tipo>/AAAA-MM-DD - Nome da Demanda/   # video, blog, linkedin, social, newsletter, email, palestra/apresentacoes, reports
│   ├── (fluxo de aprovação — perguntar sempre, padrão é NÃO ter esteira; ver seção "Fluxo de aprovação")
│   │     # 0 padrão: sem pasta nova, campo `status:` dentro de <tipo>/AAAA-MM-DD - Nome/
│   │     # A: 1_a_aprovar/ 2_aprovado/ 3_publicado/ 4_revisar_ajustar/ (tudo junto, sem pasta de tipo)
│   │     # B: 1_a_aprovar/<tipo>/ 2_aprovado/<tipo>/ … (espinha primeiro — precedente: Futuro Mercado)
│   │     # C: <tipo>/1_a_aprovar/ <tipo>/2_aprovado/ … (tipo primeiro)
│   └── publicados.md  publicados.json
├── inteligencia/                     # REPOSITÓRIO DO MERCADO (sem números nos nomes)
│   ├── tendencias/
│   ├── estudos/                      # acervo_dados_metricas.md, banco_de_cases.md, registro-de-fontes.md
│   ├── fontes-e-coleta/
│   └── monitoramento/                # consultas.md, termos.txt, relatorios/
├── referencias/                      # referências DO PROJETO que influenciam todo conteúdo (rubrica, perfil e voz, formatos adaptados); técnica genérica fica na skill
├── assets/                           # imagens; inventario.md
├── docs/                             # mapa-de-destinos.md e demais documentos
├── scripts/
├── .agents/{plans,skills,agents,rules}/   # agentes de revisão da marca em .agents/agents/
└── .claude/{skills,agents}/              # links para .agents/
```

Não existem `conteudos/_base/` nem `inteligencia/2_imprensa_pr/`. Técnica de redação mora na skill do assunto. Projetos antigos (Futuro Mercado) que ainda têm esses nomes continuam como estão até o usuário aprovar a migração; o mapa deles documenta o que existe.

### Convenções de nome
- Peça de conteúdo: `AAAA-MM-DD_<canal>_<tema-curto>.md` (metadados no topo, conforme `STANDARDS.md`; `campanha:` quando a peça serve a uma campanha).
- Arquivos de apoio da peça (briefing visual, blueprint, roteiro): ao lado da peça, com o mesmo prefixo: `AAAA-MM-DD_<canal>_<tema-curto>_briefing-visual.md`. Pasta por demanda usa `AAAA-MM-DD - Nome da Demanda` (com espaços e hífen), igual nos dois modos; arquivo de peça solta da esteira usa `AAAA-MM-DD_<canal>_<tema-curto>.md` ou o código do calendário (`D01_LI.md`).
- Peça por tipo: `conteudos/<tipo>/AAAA-MM-DD - Nome da Demanda/` com `briefing.md`, `draft.md` e os arquivos do tipo. Vídeo: `roteiro-longo.md` ou `roteiro-curto.md`.
- Vendas: `vendas/AAAA-MM-DD - Nome da Demanda/` com `cadencia-outbound.md`, `playbook-discovery.md`, `deal-governance.md` (só os que a demanda pede).
- Assessoria de imprensa: `imprensa/AAAA-MM-DD - Nome/` com `pauta/` (`pauta-principal.md` + `angulo-<tema>.md`), `pitch/` (um por ângulo), `release.md`, `jornalistas.md`.
- Campanha: `estrategia/campanhas/AAAA-MM-DD - Nome da Campanha/campanha.md`; `resultado.md` nasce no encerramento.
- Imagem: `uso_assunto_AAAA-MM-DD_v1.ext`. Versão nova de documento de marca: arquivo `-vN`, o anterior fica.

### Assessoria de imprensa
Produção em `imprensa/`. **Controle de envio** em `imprensa/envios.md` (colunas: data, demanda, ângulo, produto (B/D), jornalista, veículo, status `enviado → respondeu → publicou → sem retorno`, `lido` opcional, link do clipping). **Clipping** em `imprensa/clipping/`. Base de jornalistas e veículos só no Hub `Compartilhado/RSS Feed` (leitura).

### Monitoramento: onde fica cada parte
- **Regras** (grafias, pessoas, termos de risco, classificação, níveis de alerta): `brand/ativacao/monitoramento.md` (**fonte da verdade**).
- **Operação** derivada das regras: `inteligencia/monitoramento/consultas.md` e `termos.txt`. O Hub lê o `termos.txt` pelo argumento `--termos <caminho>` do `avaliar.py` (README do Hub); o arquivo **não** precisa morar dentro do Hub.
- Relatório só quando solicitado: `inteligencia/monitoramento/relatorios/AAAA-MM-DD_<tema>.md`.

### Modo 0 Mkt (marca hospedada no 0 Mkt)
O 0 Mkt tem mapa próprio (`docs/mapa-de-destinos.md`), que a regra 1.4 do `CLAUDE.md` manda seguir. Identidade em `_brands/<marca>/` (e `ativos/inventario.md`); output em `content/<marca>/`: peças em `<tipo>/AAAA-MM-DD - Nome da Demanda/`, estratégia e campanhas em `estrategia/` (`estrategia/campanhas/AAAA-MM-DD - Nome da Campanha/`), imprensa em `imprensa/` (com `envios.md` e `clipping/`), vendas em `content/<marca>/vendas/AAAA-MM-DD - Nome da Demanda/` (**no 0 Mkt, vendas fica dentro de `content/<marca>/`; só em projeto novo ela é pasta de raiz**). Monitoramento, estudos e tendências: ver o mapa (a confirmar).

## Erros comuns de marketing
| Erro | Correção |
|---|---|
| Gravar pitch, release ou roteiro em `inteligencia/` | `inteligencia/` é do mercado; o que a marca produz vai para `conteudos/` |
| Gravar o controle de envio de imprensa em `inteligencia/` | É registro do que a marca fez: `imprensa/envios.md` |
| Guardar playbook genérico de redação em pasta do projeto | Técnica reutilizável mora na skill do assunto; o que é específico do projeto vai para `referencias/` na raiz |
| Criar `conteudos/_base/` | Pesquisa vai para `inteligencia/estudos/`; estratégia para `estrategia/`; personalização de demanda para o `briefing.md` |
| Gravar campanha em `conteudos/campaigns/` num projeto novo | Campanha é estratégia: `estrategia/campanhas/` |
| Copiar as peças para dentro da pasta da campanha | Peças ficam em `conteudos/`; a campanha aponta para elas |
| Campanha sem resultado esperado, ou com meta escrita depois | Definir métrica, fonte, janela e critérios antes de começar |
| Numerar pasta que não tem sequência (`1_radar…`) | Número só na esteira de aprovação |
| Gravar peça em `content/<marca>/` num projeto que já tem esteira | Ler o mapa; a esteira do projeto vence |
| Criar `_brands/<marca>/` para marca que tem projeto próprio | Usar a raiz da marca do projeto |
| Duplicar a lista de veículos e jornalistas no projeto | Consultar o Hub (leitura) |
| Regra de monitoramento em dois lugares | `brand/ativacao/monitoramento.md` manda; `inteligencia/monitoramento/` deriva dele |
| Mover arquivo antigo "para organizar" | Mapear, nunca mover sem aprovação |
| Criar subpasta de marca/produto sem perguntar | Conduzir a conversa de criação; subpasta só com a resposta do usuário |
| Não gravar porque "não achou o mapa", ou gravar sem criar o mapa | Sem mapa, crie o mapa mínimo (regra 2) e grave; a ausência de mapa não bloqueia a entrega, mas também não fica sem mapa |
