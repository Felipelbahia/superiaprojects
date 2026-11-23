# Legal Matrix (BR · UE · EUA)

> **Triagem de risco, não parecer jurídico.** Uma linha por **obrigação**, uma coluna por jurisdição, e a **régua única**: o que o projeto implementa uma vez para cobrir todas as jurisdições ativas. O processo que usa esta matriz está em `legal-preflight.md`.
>
> **Legenda:** `[V]` = conferido em fonte oficial em 2026-10-12 (fonte na seção "Fontes"). `[N]` = não verificado nesta rodada: conferir antes de afirmar. Revisar a matriz a cada 6 meses ou ao lançar, o que vier primeiro (última revisão: 2026-10-12). O prompt de atualização ainda não existe.
> **Escopo da leitura:** pequena empresa/solo; setores regulados (saúde, finanças) ficam fora.

## Como ler

`Quando` diz que recurso do produto liga a linha. `Régua única` é a decisão de projeto que serve às jurisdições ativas ao mesmo tempo (a mais alta entre elas).

## A. Dados pessoais

| # | Obrigação | Quando | BR (LGPD e ANPD) | UE (GDPR e ePrivacy) | EUA | Régua única | Revisada |
|---|---|---|---|---|---|---|---|
| L01 | Base legal e consentimento | Coleta qualquer dado pessoal | [N] Bases legais do art. 7º; consentimento livre, informado e específico | [N] Art. 6º (bases) e art. 7º (condições do consentimento) | [N] Sem lei geral federal; leis estaduais variam | Registrar a base legal por finalidade; pedir consentimento só quando não houver outra base; consentimento separado por finalidade | 2026-10-12 |
| L02 | Aviso de privacidade | Coleta qualquer dado pessoal | [V] LGPD prevê o aviso com os direitos do art. 18 (art. 9º, VII e § 3º) | [N] Arts. 13 e 14 | [N] CalOPPA; CCPA exige aviso na coleta | Política pública, sem login, que lista cada tabela com dado pessoal, cada terceiro receptor (ver Network) e os direitos de todas as jurisdições ativas | 2026-10-12 |
| L03 | Direitos do titular e exclusão de conta | Cadastro de usuários | [V] Art. 18: confirmação, acesso, correção, **eliminação**, anonimização, bloqueio, portabilidade. Eliminação definida no art. 5º, XIV | [N] Arts. 15 a 22 (acesso, apagamento, portabilidade; resposta em 1 mês) | [N] CCPA: direitos de acesso e exclusão (a lei só se aplica acima dos limiares verificados, ver abaixo) | Exclusão de conta e de dados dentro do app, apagando de verdade (incluindo uploads e conversas); canal de pedido para o que não se resolve no app; exportação de dados | 2026-10-12 |
| L04 | Dados sensíveis (saúde, biometria etc.) | Saúde, biometria, origem, religião etc. | [V] Seção própria de dados sensíveis (art. 11) | [N] Art. 9º | [N] MHMDA (WA), BIPA (IL) e leis estaduais exigem consentimento específico | Tratar como categoria especial em todo lugar: consentimento específico e separado; fora de analytics e pixels | 2026-10-12 |
| L05 | Cookies e rastreamento | Site ou app com analytics, pixels, replay | [N] Guia de cookies da ANPD; LGPD aplica-se | [V] ePrivacy art. 5(3): consentimento para armazenar/acessar dados no dispositivo, salvo estritamente necessário (EDPB). Recusar no mesmo nível de "Aceitar" e retirar tão fácil quanto dar: guia de grupo de trabalho do EDPB (fonte secundária) | [N] Litígio sob CIPA/VPPA contra pixels e replay; CCPA exige opt-out | Banner com "Recusar" no mesmo destaque; **nenhuma tag não essencial antes do aceite**; sem session replay em campos sensíveis; testar em janela anônima | 2026-10-12 |
| L06 | Menores de idade | Provável acesso por menores | [V] ECA Digital (Lei 15.211/2025), em vigor desde 17/03/2026; verificação de idade confiável (autodeclaração não basta); multa até 10% do faturamento do grupo, ou R$ 10 a R$ 1.000 por usuário cadastrado, limitada a R$ 50 mi por infração | [N] GDPR art. 8º: consentimento de criança entre 13 e 16 anos conforme o Estado-membro | [V] COPPA: regra alterada em vigor desde 23/06/2025, **conformidade obrigatória desde 22/04/2026** (menores de 13; consentimento parental verificável separado para divulgar a terceiros; limites de retenção) | Decidir 18+ ou aberto a menores. Se 18+: verificação confiável, não só checkbox. Se aberto: consentimento parental verificável, sem anúncios direcionados | 2026-10-12 |
| L07 | Incidente de segurança (aviso) | Qualquer dado pessoal | [V] Res. CD/ANPD 15/2024: comunicar ANPD **e** titulares em **3 dias úteis** do conhecimento, se houver risco ou dano relevante; manter registro por 5 anos | [V] GDPR art. 33: autoridade em **72 horas**, com justificativa se atrasar | [N] Leis estaduais de notificação de vazamento | Runbook com relógio de **72 horas corridas** (mais curto que 3 dias úteis) e aviso aos titulares no mesmo prazo; registro de incidentes por 5 anos | 2026-10-12 |
| L08 | Encarregado / representante | Dados pessoais de terceiros | [V] Art. 41 (encarregado). Res. CD/ANPD 2/2022: agente de pequeno porte **não é obrigado** a indicar encarregado, mas deve manter canal com o titular; a dispensa não vale para tratamento de alto risco | [N] Art. 37 (DPO só em casos específicos) e art. 27 (representante na UE para quem não tem estabelecimento) | Sem figura equivalente [N] | Publicar um canal de contato de privacidade; indicar um responsável nomeado mesmo se dispensado; avaliar o representante na UE se há usuários lá | 2026-10-12 |
| L09 | Transferência internacional | Provedor fora do país (nuvem, IA, e-mail) | [V] Art. 33 (regras de transferência internacional); exigências detalhadas: [N] | [N] Capítulo V (decisão de adequação, cláusulas-padrão) | Sem regra geral de saída [N] | Listar cada provedor e país na política; usar contrato de tratamento com cláusulas-padrão; escolher região da UE quando houver usuários lá e o provedor oferecer | 2026-10-12 |
| L10 | Segurança dos dados | Qualquer dado pessoal | [N] Art. 46 (medidas de segurança) | [N] Art. 32 | [V] CCPA: vazamento por falta de segurança razoável abre ação privada, com indenização legal de US$ 100 a 750 por incidente (valores nominais, fonte secundária) | Cumprir o checklist `Vibecoding - Segurança - Checagem` (RLS, segredos, headers, criptografia) como baseline | 2026-10-12 |

## B. Consumo, publicidade e comunicação

| # | Obrigação | Quando | BR | UE | EUA | Régua única | Revisada |
|---|---|---|---|---|---|---|---|
| L11 | Assinatura e cancelamento | Cobrança recorrente ou teste grátis | [V] Decreto 11.034/2022: cancelamento "por todos os meios disponíveis para a contratação", efeitos imediatos (escopo do decreto: serviços regulados, [N]) | [N] Regras nacionais de consumo | [V] ROSCA vigora: termos materiais claros antes de cobrar, consentimento informado expresso, mecanismo simples para parar. A regra "Click to Cancel" foi **anulada** pelo 8º Circuito em 08/07/2025; a FTC reabriu a regulamentação em 2026; estados (CA, NY, MA, CO, MN) têm leis próprias de renovação automática | Cancelar no mesmo canal da contratação e com **no máximo os passos de assinar**; termos de preço, periodicidade, renovação e como cancelar **ao lado do botão de compra**; lembrete antes da cobrança de teste grátis | 2026-10-12 |
| L12 | Direito de desistência | Venda online | [V] CDC art. 49: **7 dias** para desistir nas compras fora do estabelecimento | [V] Diretiva 2011/83 art. 9º: **14 dias**; exceção do art. 16(m) para conteúdo digital com consentimento prévio expresso e reconhecimento da perda do direito; existe regra recente do "botão de desistência" [N] (detalhes e data) | Sem direito geral federal de desistência [N] | Aplicar o **maior prazo** entre as jurisdições ativas; no conteúdo digital, coletar o consentimento expresso antes de começar o fornecimento | 2026-10-12 |
| L13 | Publicidade, reviews e alegações | Texto de marketing, depoimentos, prova social | [V] CDC art. 37: proibida toda publicidade enganosa ou abusiva. CONAR [N] | [N] Diretiva de práticas comerciais desleais | [V] Regra da FTC sobre avaliações (16 CFR 465), em vigor desde 21/10/2024: proíbe avaliações falsas, compra de avaliações, supressão e seguidores falsos; multa civil para violação consciente. Alegações de IA sem prova: FTC Act §5 [N] | Só depoimentos reais e rastreáveis; nada gerado por IA como cliente; toda alegação de capacidade ("diagnostica", "garante") com prova; contagens regressivas ligadas a dados reais | 2026-10-12 |
| L14 | E-mail e SMS de marketing | Marketing por e-mail ou SMS | [N] LGPD base legal; CDC | [N] ePrivacy art. 13 (consentimento prévio) | [V] CAN-SPAM: descadastro honrado em até 10 dias úteis, endereço postal, remetente e assunto verdadeiros; até US$ 53.088 por e-mail. TCPA para SMS: [N] | Opt-in explícito registrado (data, IP, texto); descadastro de 1 clique em todo e-mail; endereço no rodapé; transacional separado do marketing | 2026-10-12 |
| L15 | IA: transparência e chatbot | Chatbot ou conteúdo gerado por IA | [V] PL 2338/2023 **não é lei**: aprovado no Senado em 2024, em comissão especial na Câmara em set/2026. STF (Marco Civil, ver L16) presume relativamente a culpa em dano por chatbots | [V] AI Act art. 50 aplica-se desde 02/08/2026 (aviso de interação com IA, marcação de conteúdo sintético); transição até 02/12/2026 para marcar sistemas já existentes (fonte secundária) | [V] Sem lei federal geral. Colorado: lei original (SB 24-205) **substituída** em 2026 por norma mais leve (SB 26-189), em vigor 01/01/2027 e dependente de regulamentação (fonte secundária). Califórnia SB 942 (marcação de mídia gerada): em vigor 02/08/2026 (fonte secundária). Utah: avisos limitados a pedido claro ou interação de alto risco | Avisar na interface, de forma permanente, que é uma IA; marcar mídia sintética de forma legível por máquina quando houver; guardrails de `chatbot-guardrails.md` | 2026-10-12 |

## C. Conteúdo, acessibilidade e produto

| # | Obrigação | Quando | BR | UE | EUA | Régua única | Revisada |
|---|---|---|---|---|---|---|---|
| L16 | Conteúdo de usuário (denúncia e remoção) | Usuários publicam conteúdo | [V] STF (Temas 987 e 533): art. 19 do Marco Civil é **parcialmente inconstitucional**; vale desde 05/08/2025 e foi ajustado em embargos em jun/2026. Provedor notificado que não remove conteúdo ilícito responde, salvo dúvida razoável; ofensas à honra seguem exigindo ordem judicial; anúncios e impulsionamentos geram presunção relativa de culpa; rol de crimes graves com dever de cuidado | [V] DSA art. 16: mecanismo de notificação e ação para provedores de hospedagem; o art. 19 prevê exclusão para micro e pequenas empresas (alcance exato: [N]) | [N] DMCA 512(c): agente designado registrado para o porto seguro | Botão de denunciar em todo conteúdo de usuário; canal de e-mail público; processo documentado de análise e resposta; registro das notificações | 2026-10-12 |
| L17 | Imagens íntimas não consentidas | Uploads de fotos/vídeos | [V] ECA Digital (crimes graves contra crianças) e STF (L16) | [N] DSA (L16) | [V] TAKE IT DOWN Act: desde 19/05/2026 as plataformas cobertas mantêm processo de remoção, aviso claro e removem em **48 horas** o conteúdo e cópias idênticas conhecidas (FTC fiscaliza) | Rota pública `/report-image` com SLA de 48 horas e remoção de duplicatas | 2026-10-12 |
| L18 | Acessibilidade | Serviço ao consumidor | [N] Lei Brasileira de Inclusão (art. 63, acessibilidade em sites) | [V] European Accessibility Act (Diretiva 2019/882): aplicação desde 28/06/2025; isenção de microempresas de serviços (menos de 10 pessoas e faturamento ou balanço abaixo de € 2 mi, fonte secundária) | [N] ADA Título III: ações por falta de acessibilidade | WCAG 2.1 AA como baseline: alt text, contraste 4,5:1, teclado completo; sem "overlay mágico" | 2026-10-12 |
| L19 | Segurança do produto e vulnerabilidades | App distribuído na UE | Sem equivalente | [V] Cyber Resilience Act: desde 11/09/2026, alerta em 24 h, notificação em 72 h, relatório final em 14 dias após correção (ENISA) | Sem equivalente federal [N] | `security.txt` + `runbook-cra.md` + alertas de dependências | 2026-10-12 |
| L20 | Direitos autorais e licenças | Imagens, fontes, uploads | [N] Lei 9.610/1998 | [N] Diretiva de direitos autorais | [N] 17 USC 504(c) (indenização legal por obra) | Licença registrada para toda imagem, fonte e ícone; nada de placeholder em produção | 2026-10-12 |

## Tetos de sanção (referência, não conselho)

| Jurisdição | Teto | Status |
|---|---|---|
| LGPD art. 52, II | até 2% do faturamento no Brasil, limitada a R$ 50 mi **por infração** | [V] |
| GDPR art. 83(5) | até € 20 mi ou 4% do faturamento mundial, o que for maior | [V] |
| ECA Digital art. 35 | até 10% do faturamento do grupo, ou R$ 10 a R$ 1.000 por usuário cadastrado, limitada a R$ 50 mi por infração | [V] |
| CCPA (multa administrativa, 2025) | até US$ 2.663 por violação; US$ 7.988 por violação intencional ou envolvendo menores de 16 | [V] |
| CAN-SPAM | até US$ 53.088 por e-mail | [V] |
| AI Act, CRA, TAKE IT DOWN, DSA, BIPA, TCPA | valores do documento de origem | [N] |

## Limiares do CCPA (quando a lei da Califórnia se aplica)

[V] Faturamento anual acima de US$ 26.625.000 (ajuste de 2025), **ou** compra, venda ou compartilhamento de dados de 100.000 ou mais consumidores ou domicílios por ano, **ou** 50% ou mais da receita vinda de venda/compartilhamento de dados. Um app pequeno costuma ficar abaixo; confirmar ao crescer.

## Ainda `[N]` (lista explícita para a próxima revisão)

L01, L04 (EUA/UE), L05 (BR/EUA), L08 (UE), L09 (UE), L10 (BR/UE), L11 (UE), L12 (botão de desistência da UE), L13 (UE/CONAR/FTC §5 para IA), L14 (BR/UE/TCPA), L16 (EUA), L18 (BR/EUA), L20, tetos de AI Act/CRA/TAKE IT DOWN/DSA/BIPA/TCPA, Illinois HB 1806 e leis de IA de Nova York e Califórnia sobre chatbots e autolesão.

## Fontes verificadas em 2026-10-12

| Tema | Fonte |
|---|---|
| LGPD (arts. 5º XIV, 9º, 11, 18, 33, 41, 48, 52) | planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm |
| Incidente de segurança (Res. CD/ANPD 15/2024) | gov.br/anpd (comunicação de incidentes); texto da resolução |
| Agentes de pequeno porte (Res. CD/ANPD 2/2022) | gov.br/anpd, resolução 2/2022 |
| ECA Digital (Lei 15.211/2025) | planalto.gov.br L15211; gov.br/anpd/eca-digital |
| CDC (arts. 37 e 49); Decreto 11.034/2022 | planalto.gov.br (L8078compilado; D11034) |
| STF, Marco Civil art. 19 (Temas 987 e 533) | portal.stf.jus.br (andamento do Tema 987); conjur.com.br (embargos, 2026) |
| PL 2338/2023 (IA) | camara.leg.br ficha de tramitação; senado.leg.br matéria 157233 |
| GDPR arts. 33 e 83 | gdpr-info.eu; eur-lex.europa.eu (Regulamento 2016/679) |
| ePrivacy art. 5(3) | EDPB (Guidelines 2/2023 e comentários); fonte secundária para banner |
| Diretiva 2011/83 (arts. 9º e 16) | eur-lex.europa.eu |
| EAA (Diretiva 2019/882) | commission.europa.eu; fonte secundária para isenção |
| DSA arts. 16 e 19 | eu-digital-services-act.com (texto final) |
| AI Act art. 50; CRA | ai-act-service-desk.ec.europa.eu; digital-strategy.ec.europa.eu |
| FTC: ROSCA, Click to Cancel | wilmerhale.com, gibsondunn.com, goodwinlaw.com (2025-2026) |
| FTC: CAN-SPAM; avaliações (16 CFR 465); TAKE IT DOWN; COPPA | ftc.gov; federalregister.gov |
| CCPA: limiares e multas | cppa.ca.gov (ajuste de 2025) |
| Estados: leis de IA (Colorado, Califórnia, Utah) | leg.colorado.gov; cooley.com; arnoldporter.com (fontes secundárias) |
