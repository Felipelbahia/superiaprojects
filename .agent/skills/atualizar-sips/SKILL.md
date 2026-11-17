---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: atualizar-sips
description: Use when the owner wants to check whether the SIPs installed in the current project are up to date, or to update them ("atualizar os SIPs", "tem atualização dos SIPs?", "os SIPs estão em dia?", "update my SIPs", "check SIP updates"). Runs a read-only status against the project's .agent/SIPS-CONSUMIDOS.md and, with the owner's ok, re-runs each SIP's install prompt.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---

# atualizar-sips

Diz se cada SIP instalado no projeto está defasado em relação ao hub e, onde estiver, atualiza. O status é só leitura; nada muda antes do "ok" do dono.

## Regras
- Nunca diga "em dia" sem ter rodado o status e conferido a saída; o que não foi verificado é "não verificado".
- Só remova **symlink**, nunca arquivo ou pasta real. Conflito de nome com arquivo do dono segue o prompt de instalação do SIP (perguntar caso a caso).
- A data do hub é mantida à mão pelo dono do hub: é dica. Link ausente, agent ou workflow novo ou removido são verificados em disco.

## Passos
1. **Status** (na raiz do projeto):
   ```
   python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/sips_status.py" .
   ```
   Sem `.agent/SIPS-CONSUMIDOS.md`: nenhum SIP registrado. Diga isso, ofereça instalar (tabela de `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/_sips.md`; o `sip-geral` entra sempre) e pare. Para ver todos os projetos: `--all "<pasta dos projetos>"`.
2. **Mostre** em português simples, uma linha por SIP: em dia ou atualizar, com o motivo (hub mais novo, link ausente ou quebrado, agents ou workflows novos, itens que saíram do hub).
3. **Pergunte**, SIP por SIP, se atualiza (sugeridos / nenhum / lista). Sem resposta = nenhum. Tudo em dia: pare e diga isso.
4. **Atualize** cada SIP aprovado seguindo por inteiro o prompt da linha "Para atualizar" do manifesto. Ele refaz os links, mantém a escolha anterior de agents e workflows e pergunta só os itens novos ("Vistos no hub"). Para cada item novo, mostre nome e "use quando"; sem resposta = não instalar. Itens que saíram do hub: mostre os links quebrados e remova só com o "ok".
5. **Verifique**: rode o status de novo e cole a saída. Todo SIP aprovado deve estar "em dia", com a data de hoje no manifesto. O que continuar "atualizar" vira item na `inbox/` do projeto, com o motivo.
6. Se o projeto é um hub de SIP (tem `.agent/skills/sip-*` próprio): confira a data "Última atualização do hub" do resolver e rode `build_sip_index.py --check`.

Termine apresentando: o que estava defasado, o que foi atualizado (com a verificação), o que ficou de fora por escolha do dono e o que ficou "não verificado".
