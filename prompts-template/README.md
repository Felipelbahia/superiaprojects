# Prompts reutilizáveis — Operação Multi-IA (Super IA Projects)

Cada arquivo `NN-*.md` desta pasta contém **somente o prompt**, pronto para copiar inteiro e colar numa sessão nova (Claude Code, Antigravity ou outra IA). O contexto de cada um (quando usar, skill relacionada) está na tabela abaixo, não nos arquivos.

Os prompts trazem **verificações obrigatórias** (`ls`, `grep`, `diff`, `test -L`, `sync_rules.py`…) que existem por causa de achados reais em projetos; o motivo de cada uma está em [HISTORICO.md](./HISTORICO.md).

## Qual prompt usar

| # | Arquivo | Use quando | Skill / referência |
|---|---|---|---|
| 1 | [01-atualizar-projeto-existente.md](./01-atualizar-projeto-existente.md) | O projeto **já existe** e precisa ganhar o padrão multi-IA sem perder as regras locais (Merge & Preserve) | `sync_rules.py`, `sync_entrypoints.py`, `skill-resolver` |
| 2 | [02-criar-projeto-do-zero.md](./02-criar-projeto-do-zero.md) | Projeto **novo de software/código**, sem regras prévias | `project-initializer`, `app-builder` |
| 2b | [02b-criar-projeto-mkt.md](./02b-criar-projeto-mkt.md) | Projeto **novo de marketing e conteúdo**, sem backend/DB | `0 Mkt`, `brand/`, `conteudos/`, `sync_rules.py` |
| 3 | [03-adotar-contrato-brownfield.md](./03-adotar-contrato-brownfield.md) | Projeto existente (aplicação) que vai adotar o contrato `_projectdefines/` descrevendo o que já existe, sem alterar código. Rode o #1 antes se faltam as regras do kit | `project-defines` (`brownfield.md`) |
| 4 | [04-buscar-bibliotecas-prontas.md](./04-buscar-bibliotecas-prontas.md) | Uma capacidade (login, pagamento, PDF, datas, editor…) pode ser resolvida por biblioteca madura, ou você quer revisar o que foi escrito à mão | `oss-scout` (modo Reuso) |
| 5 | [05-estudar-projetos-referencia.md](./05-estudar-projetos-referencia.md) | Aprender com projetos open source e aproveitar partes deles, com portão de licença | `oss-scout` (modo Estudo de referências) |
| 6 | [06-alinhar-padrao-supabase.md](./06-alinhar-padrao-supabase.md) | Na hora de mexer num projeto que usa Supabase (qual banco, nomes de env, prefixo de tabelas) | `supabase`, registro [`_bancos-supabase.md`](../_bancos-supabase.md) |
| 7 | [07-atualizar-fatos-verificados.md](./07-atualizar-fatos-verificados.md) | A cada 6 meses, antes de lançar um produto, ou quando uma lei/regra de loja mudar (próxima revisão até abril de 2027) | `launch-readiness`, `vibecoding-security-audit` |
| 8 | [08-sincronizar-com-o-kit.md](./08-sincronizar-com-o-kit.md) | Rotina: depois de mudar os padrões do kit ou de acrescentar skills num projeto que já roda; alinha o que mudou, gera o catálogo unificado (MD e HTML) e grava a data na ficha | `projects_audit.py`, `generate_catalog.py`, `sync_rules.py` |
| 9 | [09-migrar-conteudo-para-projeto.md](./09-migrar-conteudo-para-projeto.md) | Migrar manual de marca (`_brands/`) e conteúdos (`content/`) do `0 Mkt` para o projeto local autônomo | `0 Mkt`, `brand/`, `conteudos/`, `diff -rq` |
| 10 | [10-incluir-inteligencia-no-projeto.md](./10-incluir-inteligencia-no-projeto.md) | Injetar o módulo canônico de Inteligência de Negócio (Trends, RSS Feed, `hook-mining`, `reel-analyzer`, PR e estudos de embasamento) | `inteligencia/`, `Previsão de Demanda`, `RSS Feed`, `0 Mkt` |
| 11 | [11-atualizar-inteligencia-global.md](./11-atualizar-inteligencia-global.md) | Promover descobertas, dados checados, ganchos e melhorias locais de volta ao repositório central em `Super IA Projects` (PUSH) | `inteligencia/`, `3_estudos_embasamento/`, `1_radar_tendencias/` |

## Como usar

1. Abra o arquivo do prompt e copie **tudo**.
2. Cole numa sessão nova na raiz do projeto-alvo (o #7 roda em `Super IA Projects`).
3. Preencha os trechos entre colchetes `[ ... ]` (escopo, links, etc.) antes de enviar.
4. Cada prompt termina pedindo que a IA **pare e apresente um resumo**; aprove antes de qualquer passo destrutivo.

## Ordem típica

- Projeto novo: **#2** → (opcional) **#4**/**#5** → **#6** se usar Supabase.
- Projeto existente: **#1** → **#3** → **#4**/**#6** conforme a necessidade.
- Manutenção do próprio kit: **#7**.
- Rotina em projetos que já rodam, depois de mexer no kit: rode `projects_audit.py` para ver quem está defasado e aplique o **#8** em cada um.

## Regra de ouro dos prompts

A IA nunca afirma que algo "existe", "está correto" ou "foi configurado" sem ter verificado por comando ou leitura direta; o que não foi verificado vira "não verificado".

## Adicionar ou editar um prompt

- Um prompt = um arquivo `NN-slug.md` com **apenas** o texto do prompt (sem título extra, sem notas, sem cerca de código).
- Contexto de uso vai para a tabela deste README; história e motivação vão para [HISTORICO.md](./HISTORICO.md).
- Ao criar um novo, adicione a linha na tabela acima.
