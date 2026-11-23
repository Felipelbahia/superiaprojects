# Legal Pre-flight: processo único (BR · UE · EUA)

> **Triagem de risco, não parecer jurídico.** Um só processo cobre as três jurisdições: o dado está em `legal-matrix.md` (uma linha por obrigação, uma coluna por jurisdição). Um item `[N]` é um aviso para conferir a fonte, nunca um fato para repetir. Última revisão: 2026-10-12; revisar a cada 6 meses.

## Princípio

**Desenhe uma vez, para a régua mais alta entre as jurisdições ativas.** Não existe "versão BR", "versão UE" e "versão EUA" do produto: existe um comportamento por obrigação, escolhido para satisfazer todas as ativas ao mesmo tempo. A coluna *Régua única* da matriz já traz essa escolha.

## Os 6 passos

1. **Perfil.** Pegue as respostas do Launch profile (Q6): jurisdições ativas (BR, UE, EUA) e recursos (cadastro, cobrança recorrente, uploads, menores, chatbot, marketing por e-mail/SMS, analytics, dados sensíveis, app distribuído na UE).
2. **Linhas aplicáveis.** Na matriz, marque as linhas cujo *Quando* bate com os recursos. Linhas fora do perfil são ignoradas, sem recitar.
3. **Régua única.** Para cada linha marcada, adote a *Régua única* e note, por jurisdição ativa, qual célula a justifica. Onde a matriz diz `[N]` para uma jurisdição ativa, confira a fonte antes de decidir.
4. **Evidência.** Para cada linha, aponte o que prova que está implementado: tela, rota, arquivo, comando, teste. Use os prompts de auditoria abaixo como apoio no código.
5. **Registro.** Preencha `templates/legal-register.md` no projeto (obrigação, jurisdições, decisão, evidência, revisar em). No `project-defines`, o registro é o artefato do item `L-05`.
6. **Revisão.** Se a matriz tem mais de 6 meses, ou a linha ativa está `[N]`, ou a lei mudou: verifique a fonte antes de lançar e anote a data no registro.

## Saída padrão

Para cada linha aplicável: `Lxx · jurisdições ativas · decisão · evidência · status da fonte · revisar em`. Reporte só o que falha ou está sem evidência.

## Prompts de auditoria (rodar no repositório; passo 4)

**Prompt 1: checklist item a item (cole as linhas aplicáveis no fim)**
```
I'm going to give you a compliance checklist and access to my codebase. Go through all items one at a time.

For each one, tell me: pass, fail, or can't tell from the code. If it's a fail, show me the specific file and line, then give me the change. If you can't tell, tell me exactly what to look at.

Then rank the failures by how likely each one is to actually hurt me, and give me the fix order. Don't write me a summary. Write me the diffs.

Start with public storage buckets, since that one is silent and the rest of them aren't.
```

**Prompt 2: regulatório (UE/UK/EUA 2026)**
```
Audit this codebase for: images in the repo or public folder with no license record, cookie consent components where reject is harder than accept or where non-essential scripts load before consent, user-generated content with no report or flag route, analytics or pixel calls that include health-related fields or precise location, urgency UI (countdown timers, stock counters, viewer counts) not backed by real database values, system prompts or marketing copy that describe the product as therapy or counseling, pricing logic that varies by user data with no disclosure string, image or video upload features with no notice-and-removal route and no 48-hour SLA, AI chat or generation features with no AI disclosure or content marking, and any mobile or downloadable build with no security contact or vulnerability intake. List each finding with file and line.
```

**Prompt 3: gatilhos de processo**
```
Audit this codebase for: SMS sending without consent tracking, user upload features with no DMCA takedown route, unencrypted personal data at rest, analytics or pixel scripts loading before consent, missing alt text and keyboard handling, signup flows with no age gate, marketing email without an unsubscribe link, chatbot system prompts that let the model state prices, refunds or policies, and any marketing copy claiming AI capabilities. List each finding with file and line.
```

## Ordem de correção

1. Buckets/tabelas públicos (falha silenciosa). 2. Promessas de exclusão não cumpridas. 3. Política de privacidade e uso de IA batendo com o código. 4. Consentimento, age gate, descadastro, alt text, guardrails de chatbot.

## Erros comuns

| Erro | Correção |
|---|---|
| Ler a matriz inteira "por segurança" | Só as linhas cujo *Quando* bate com o perfil |
| Fazer uma versão por país | Uma decisão por obrigação, na régua mais alta |
| Repetir valor de multa `[N]` como fato | Citar o status da célula |
| Tratar a matriz como parecer | Triagem de risco; advogado antes de monetizar |
| Esquecer a data de revisão | Anotar no registro; passo 6 |
