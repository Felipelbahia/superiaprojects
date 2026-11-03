# Exemplo preenchido: prompt de instalação

Resultado em `<CAMINHO_DO_HUB>/prompts/instalar-skill-sip-exemplo.md`
(caminho fictício — substitua `<CAMINHO_DO_HUB>` pelo caminho real do seu hub):

```markdown
# Prompt: Instalar/Atualizar a skill "sip-exemplo" em outro projeto

Cole isto numa sessão do Claude Code dentro do projeto que precisa consultar o
hub central de exemplo (SIP - Exemplo):

\`\`\`
Instale/atualize a skill de conhecimento exemplo do hub central SIP - Exemplo neste projeto:
1. Crie a pasta .claude/skills/ se ela não existir.
2. Crie (ou recrie, se já existir e estiver desatualizado/quebrado) um symlink:
   .claude/skills/sip-exemplo -> "<CAMINHO_DO_HUB>/.agent/skills/sip-exemplo"
3. Confirme com `ls -la` que o symlink aponta para esse caminho e que o SKILL.md é legível através dele.
4. Não copie o conteúdo do SKILL.md para este projeto — mantenha como symlink, para
   herdar atualizações futuras do hub automaticamente.
\`\`\`

## Por que symlink e não cópia

A fonte de verdade da skill fica em `<CAMINHO_DO_HUB>/.agent/skills/sip-exemplo/SKILL.md`.
Symlink garante que atualizações futuras nesse arquivo já reflitam em todos os
projetos que instalaram, sem rodar este prompt de novo — exceto se o symlink
quebrar (hub movido/renomeado), caso em que basta colar o prompt outra vez.

## Via de volta: contribuir com o hub

A skill instalada também sabe devolver conhecimento ao hub — nunca edita os
arquivos compartilhados direto, só deixa um arquivo em `<CAMINHO_DO_HUB>/inbox/`
para revisão manual. Ver `inbox/README.md` no hub para o formato esperado.
```
