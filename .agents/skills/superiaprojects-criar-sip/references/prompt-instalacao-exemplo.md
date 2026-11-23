# Exemplo preenchido: prompt de instalação

Resultado em `<CAMINHO_DO_HUB>/prompts/instalar-skill-sip-exemplo.md`
(caminho fictício — substitua `<CAMINHO_DO_HUB>` pelo caminho real do seu hub):

```markdown
# Prompt: Instalar/Atualizar a skill "sip-exemplo" em outro projeto

Cole isto numa sessão do Claude Code dentro do projeto que precisa consultar o
hub central de exemplo (SIP - Exemplo). Instala o resolver e só os agents/workflows que você escolher:

\`\`\`
Instale/atualize o acesso ao hub central SIP - Exemplo (exemplo) neste projeto.
(Exemplo resumido: o modelo completo está no SKILL.md, Passo 2.)
O resolver sempre; agents e workflows só os que eu escolher; skills especialistas nunca.
Antes de cada `ln -sfn`: se o link já existe como arquivo/pasta REAL, não rode `ln`;
pergunte caso a caso (renomear o meu / substituir movendo o meu para .bak / pular);
sem resposta = pular, registrado em "Conflitos".
Só remova symlinks (`test -L`) cujo destino, lido com `readlink` sem `-f`, aponte
para dentro de "<CAMINHO_DO_HUB>".
1. Resolver, com `ln -sfn` (nunca só `-s`):
   .agents/skills/sip-exemplo -> "<CAMINHO_DO_HUB>/prompts/resolver/sip-exemplo"
   .claude/skills/sip-exemplo -> ../../.agents/skills/sip-exemplo
2. Migração: remova symlinks antigos de skills especialistas deste hub.
3. Escolha: mostre as seções "Agents" (exemplo-arquiteto, exemplo-revisor)
   e "Workflows" (exemplo-publicar) das verticais do resolver e pergunte
   "nenhum / todos / quais". Sem resposta = nenhum. Reinstalação: mantenha a
   escolha do manifesto e pergunte só os itens fora de "Vistos no hub"
   (sem resposta = os novos ficam de fora).
   Instalação antiga sem manifesto: marque os symlinks deste hub já existentes e
   pergunte "manter, mudar ou nenhum" (sem resposta = manter).
4. Instale só o escolhido (par .agents/ absoluto + .claude/ relativo; workflow
   também em .cursor/commands/). Ex.: escolhido exemplo-revisor:
   .agents/agents/exemplo-revisor.md -> "<CAMINHO_DO_HUB>/.agents/agents/exemplo-revisor.md"
   .claude/agents/exemplo-revisor.md -> ../../.agents/agents/exemplo-revisor.md
5. Remova symlinks deste hub que saíram da escolha.
6. Confirme com `ls -la` e rode
   `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/scripts/sync_entrypoints.py" --check`:
   tem de sair com 0.
7. Não copie conteúdo: mantenha como symlink, para herdar atualizações do hub.
8. .gitignore deste projeto: uma linha por symlink instalado (.agents/skills/sip-exemplo,
   .claude/skills/sip-exemplo, .agents/agents/exemplo-revisor.md, .claude/agents/exemplo-revisor.md).
9. Registre a instalação em "<CAMINHO_DO_HUB>/instalacoes/<nome-deste-projeto>.md"
   (skill; agents/workflows escolhidos, ou "nenhum").
10. Atualize .agents/SIPS-CONSUMIDOS.md (substitua a entrada deste hub, se houver):
   ## SIP - Exemplo (`sip-exemplo`)
   - Hub: <CAMINHO_DO_HUB>
   - Instalado/atualizado em: AAAA-MM-DD
   - Skill: sip-exemplo
   - Agents: exemplo-revisor
   - Workflows: nenhum
   - Vistos no hub: agents exemplo-arquiteto, exemplo-revisor; workflows exemplo-publicar
   - Conflitos: nenhum
   - Para atualizar: cole de novo "<CAMINHO_DO_HUB>/prompts/instalar-skill-sip-exemplo.md"
\`\`\`

## Por que symlink e não cópia

A fonte de verdade fica no hub; o resolver fica em `<CAMINHO_DO_HUB>/prompts/resolver/sip-exemplo/SKILL.md`.
Symlink garante que atualizações futuras nesse arquivo já reflitam em todos os
projetos que instalaram, sem rodar este prompt de novo — exceto se o symlink
quebrar (hub movido/renomeado), caso em que basta colar o prompt outra vez.

## Via de volta: contribuir com o hub

A skill instalada também sabe devolver conhecimento ao hub — nunca edita os
arquivos compartilhados direto, só deixa um arquivo em `<CAMINHO_DO_HUB>/inbox/`
para revisão manual. Ver `inbox/README.md` no hub para o formato esperado.
```
