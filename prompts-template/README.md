# Prompts reutilizáveis — Operação Multi-IA (Super IA Projects)

Cada arquivo `NN-*.md` desta pasta contém **somente o prompt**, pronto para copiar inteiro e colar numa sessão nova (Claude Code, Antigravity ou outra IA). O contexto de cada um (quando usar, skill relacionada) está na tabela abaixo, não nos arquivos.

Os prompts trazem **verificações obrigatórias** (`ls`, `grep`, `diff`, `test -L`, `sync_rules.py`…) que existem por causa de achados reais em projetos; o motivo de cada uma está em [HISTORICO.md](./HISTORICO.md).

## Qual prompt usar

| # | Arquivo | Use quando | Skill / referência |
|---|---|---|---|
| 1 | [01-atualizar-projeto-existente.md](./01-atualizar-projeto-existente.md) | O projeto **já existe**: primeira adoção do kit ou atualização depois de mudanças no kit. Preserva as regras locais num bloco próprio, monta as regras pelos módulos, instala os SIPs, cria o mapa de destinos e grava a data na ficha | `assemble_rules.py`, `sync_rules.py`, `sync_entrypoints.py`, `projects_audit.py`, `mapa-de-destinos` |
| 2 | [02-criar-projeto-do-zero.md](./02-criar-projeto-do-zero.md) | Projeto **novo**: software, conteúdo e marketing, automação ou mistura (o prompt pergunta o tipo e monta as regras por módulos; marketing usa o `sip-marketing`), sem regras prévias (inclui `memory.md`, `.gitignore` e publicação GitHub) | `project-initializer`, `app-builder`, `sip-marketing`, `github-publisher` |
| 3 | [03-adotar-contrato-brownfield.md](./03-adotar-contrato-brownfield.md) | Projeto existente (aplicação) que vai adotar o contrato `_projectdefines/` descrevendo o que já existe, sem alterar código. Rode o #1 antes se faltam as regras do kit | `project-defines` (`brownfield.md`) |
| 4 | [04-oss-scout.md](./04-oss-scout.md) | Procurar solução pronta antes de construir: **reuso** (biblioteca madura para login, pagamento, PDF, datas, editor…, ou revisar o que foi escrito à mão) ou **estudo de referências** (aprender com open source, com portão de licença). Começa olhando em todos os seus projetos | `oss-scout` (modos Reuso e Estudo) |
| 6 | [06-alinhar-padrao-supabase.md](./06-alinhar-padrao-supabase.md) | Na hora de mexer num projeto que usa Supabase (qual banco, nomes de env, prefixo de tabelas) | `supabase`, registro [`_bancos-supabase.md`](../_bancos-supabase.md) |
| 7 | [07-seguranca-e-legal.md](./07-seguranca-e-legal.md) | A cada 6 meses, antes de lançar um produto, ou quando uma lei/regra de loja mudar (próxima revisão até abril de 2027) | `launch-readiness`, `vibecoding-security-audit` |
| 8 | [08-atualizar-sips.md](./08-atualizar-sips.md) | Lançador da skill `atualizar-sips` (também chamada direto, de qualquer projeto): descobre se os SIPs instalados estão defasados (hub mudou, link quebrado, agents e workflows novos) e os atualiza, com o seu "ok" | `atualizar-sips` (`sips_status.py`) |

O número 5 está vago de propósito: o antigo #5 (estudar referências) foi fundido no #4 em 2026-11-17, e os números não foram reaproveitados para não quebrar referências externas. Prompts aposentados e removidos desta pasta: 02b (fundido no 02), o 03 antigo (agora lançador), o 04 antigo e o 05 (fundidos no 04), 08 sincronizar (absorvido pelo 01), 09 migrar conteúdo do 0 Mkt e 10 e 11 inteligência (substituídos pelos SIPs `sip-trends-previsao-demanda`, `sip-imprensa` e `sip-marketing` mais as linhas do mapa de destinos).

## Atualização na instalação

`install.sh` e `install.py` rodam `.agent/scripts/render_prompts.py`, que grava `projetos/prompts/` (local, não versionado) a partir deste `prompts-template/`, trocando `<SUPER_IA_PROJECTS_PATH>` pelo caminho real do kit. Rode de novo depois de editar um template.

## Como usar

1. Abra o arquivo do prompt e copie **tudo**.
2. Cole numa sessão nova na raiz do projeto-alvo (o #7 roda em `Super IA Projects`).
3. Preencha os trechos entre colchetes `[ ... ]` (escopo, links, etc.) antes de enviar.
4. Cada prompt termina pedindo que a IA **pare e apresente um resumo**; aprove antes de qualquer passo destrutivo.

## Ordem típica

- Projeto novo: **#2** → (opcional) **#4** → **#6** se usar Supabase.
- Projeto existente: **#1** → **#3** → **#4**/**#6** conforme a necessidade.
- Manutenção do próprio kit: **#7**.
- Rotina em qualquer projeto que consome SIPs: **#8** (diz se algum SIP está defasado e atualiza).
- Rotina em projetos que já rodam, depois de mexer no kit: rode `projects_audit.py` para ver quem está defasado e aplique o **#1** em cada um (ele também serve para atualizar).

## Regra de ouro dos prompts

A IA nunca afirma que algo "existe", "está correto" ou "foi configurado" sem ter verificado por comando ou leitura direta; o que não foi verificado vira "não verificado".

## Adicionar ou editar um prompt

- Um prompt = um arquivo `NN-slug.md` com **apenas** o texto do prompt (sem título extra, sem notas, sem cerca de código).
- Contexto de uso vai para a tabela deste README; história e motivação vão para [HISTORICO.md](./HISTORICO.md).
- Ao criar um novo, adicione a linha na tabela acima.
