# Registro de instalações e manifesto local de SIPs

> Fonte versionada destes dois trechos. `projetos/_sips.md` (local, fora do git) aponta para cá. O teste `.agents/scripts/tests/test_sip_docs.py` confere os números de passo citados abaixo contra o prompt de instalação (`SKILL.md`).

## Registro de instalações (dentro de cada hub, não aqui)

Cada hub mantém seu próprio `instalacoes/` (fora do git do hub — ver
`.gitignore` de cada um) com um arquivo por projeto consumidor, criado/
atualizado automaticamente pelo próprio prompt de instalação (passo 9).
Serve pro dono do hub saber quem consome o quê sem perguntar projeto por
projeto, quando for mudar algo no hub. Isto é diferente deste `_sips.md`:
aqui é o índice de **quais SIPs existem**; `instalacoes/` em cada hub é
**quem instalou aquele SIP especificamente**.

## Manifesto local (dentro de cada projeto consumidor)

Contrapartida do `instalacoes/` do hub, mas do lado do projeto: cada
consumidor mantém `.agents/SIPS-CONSUMIDOS.md`, criado/atualizado
automaticamente pelo prompt de instalação (último passo). Lá o hub sabe
quem o consome; aqui o projeto sabe o que consome — um lugar só pra ver
"quais SIPs este projeto depende de" sem precisar abrir `.gitignore` nem
seguir symlink manualmente. Existe desde 2026-11-06, depois que um SIP
(`sip-imprensa`) foi descoberto só por acaso, via `.gitignore` mudando num
projeto consumidor.

