Migrar Conteúdo e Marca do 0 Mkt para Projeto Local

Quero migrar todo o conteúdo e manual de marca referentes a este projeto que estavam centralizados no hub 0 Mkt (<MARKETING_HUB_PATH>), tornando este projeto autônomo na sua gestão de conteúdo.

Siga rigorosamente este protocolo de migração segura com verificação de integridade:

REGRA GERAL: NUNCA apague nada de 0 Mkt sem antes confirmar que a cópia local foi realizada com 100% de integridade (diff e contagem de arquivos). Ação destrutiva exige confirmação expressa do usuário.

1. Identificação da Marca em 0 Mkt:
   - Identifique a slug correspondente da marca deste projeto em:
     - `_brands/<marca>/` em `<MARKETING_HUB_PATH>/_brands/`
     - `content/<marca>/` em `<MARKETING_HUB_PATH>/content/`
   - Liste em uma tabela simples os arquivos e pastas encontrados antes de iniciar a cópia.

2. Estrutura de Destino no Projeto Local:
   - Se este for um projeto de produto/software (ex: Plinq, WaiMonitor), pergunte ou use a subpasta dedicada: `marketing/` ou `conteudo/`.
   - Se for um projeto puramente de marketing/conteúdo, use as pastas raiz:
     - `brand/` (para onde irão as diretrizes de `_brands/<marca>/`)
     - `conteudos/` (para onde irão os posts e campanhas de `content/<marca>/`)
     - `assets/` (para mídias locais)
   - Crie os diretórios de destino se ainda não existirem.

3. Cópia Segura e Validação de Integridade:
   - Copie o conteúdo de `_brands/<marca>/` para a pasta `brand/` local.
   - Copie o conteúdo de `content/<marca>/` para a pasta `conteudos/` local.
   - Execute um diff de verificação:
     ```bash
     diff -rq "<MARKETING_HUB_PATH>/_brands/<marca>" "./brand"
     diff -rq "<MARKETING_HUB_PATH>/content/<marca>" "./conteudos"
     ```
   - Confirme que todos os arquivos foram replicados com exatidão.

4. Atualização das Regras Interoperáveis:
   - Garanta que as regras do projeto (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) possuam o Protocolo de Fallback apontando para:
     - `1º` Projeto Local
     - `2º` Base Global: `<SUPER_IA_PROJECTS_PATH>/.agent/skills/`
     - `3º` Marketing Global: `<MARKETING_HUB_PATH>/` (para ferramentas de mídia, Sexy Canvas, copywriting e growth)
   - Rode o sincronizador de regras:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Só prossiga se o retorno for "100% synchronized".

5. Atualização da Ficha Técnica:
   - Abra a ficha do projeto em `<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md`.
   - Registre na seção de decisões e histórico a migração do conteúdo de 0 Mkt para a gestão local.
   - Atualize a linha `> **Última sincronização com o kit:** AAAA-MM-DD (kit @ HASH)`.

6. Apresentação e Confirmação de Limpeza:
   - Apresente ao usuário o relatório da migração: total de arquivos transferidos, caminho local onde foram salvos e status da integridade.
   - Pergunte expressamente: "A cópia local está 100% íntegra. Deseja que eu remova ou arquive a pasta legada correspondente em 0 Mkt agora para evitar duplicidade de versões?" (Aguarde resposta antes de qualquer remoção).
