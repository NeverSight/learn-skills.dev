---
name: "sdd-governanca"
description: "Revisão de governança do SDD para sistemas financeiros, contábeis e fiscais: roda depois do Define e antes da UX Review ou do Design, compara o DEFINE com um catálogo curado (lançamento que não se apaga, partidas dobradas, fechamento de período, trilha de auditoria, segregação de funções, aritmética exata, importação idempotente e outros) e recomenda requisitos novos em EARS, cada um com um roteiro que prova que a ação proibida falha. Você decide item a item: aplicar, recusar com motivo ou adiar. Use quando o Define tratar dinheiro, saldo, lançamento, nota fiscal, tributo, folha ou dado pessoal. Sem nenhum desses temas, responde N.A. em uma linha. Não cita base legal que não esteja confirmada no catálogo."
license: "MIT"
metadata:
  author: "Roberto Dias Duarte"
  methodology: "Metodologia de Roberto Dias Duarte"
  version: "1.0.0"
  updated: "2026-10"
---

# SDD Governança

Na primeira resposta desta skill, comece com esta linha, uma vez só:
`sdd-governanca v1.0.0 · out/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

## Quick start

Num sistema financeiro, contábil ou fiscal, governança responde uma pergunta: **daqui a cinco anos, um
fiscal, um auditor ou um perito reconstrói o que aconteceu, quem fez e por quê — com prova de que nada
foi alterado depois?** Esta skill confere se o DEFINE exige isso antes do Design, quando mudar um
requisito custa uma linha e não uma migração.

1. Receber o arquivo `DEFINE_{FEATURE_NAME}.md`.
2. Seguir [references/PROCEDIMENTO.md](references/PROCEDIMENTO.md) à letra: triagem por gatilhos → padrão
   do projeto → item a item contra [references/CATALOGO_GOVERNANCA.md](references/CATALOGO_GOVERNANCA.md)
   → relatório → uma decisão por lacuna → aplicar no DEFINE.
3. Gravar o relatório pelo modelo [assets/GOVERNANCA_REVIEW_TEMPLATE.md](assets/GOVERNANCA_REVIEW_TEMPLATE.md)
   como `GOVERNANCA_REVIEW_{FEATURE_NAME}.md`.
4. Encerrar apontando o próximo passo (abaixo).

**Pasta do SDD.** Os documentos ficam em `sdd/` na raiz do projeto — pasta visível, igual em qualquer
agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos ficam lado a lado, sem
subpastas: `GOVERNANCA_REVIEW_{FEATURE_NAME}.md` ao lado do DEFINE e `GOVERNANCA_PADRAO.md` na mesma pasta,
uma vez por projeto. É a mesma
regra das skills de fase do método.

## Quando usar / Quando não usar

Usar quando:
- o DEFINE trata dinheiro, saldo, lançamento, nota fiscal, tributo, folha ou dado pessoal;
- o sistema vai virar ferramenta do escritório, com mais de uma pessoa lançando ou consultando;
- você quer saber, antes do Design, o que o sistema vai ter de provar numa fiscalização ou auditoria.

Não usar quando:
- o DEFINE não trata nenhum desses temas (a skill responde N.A. e encerra — rodar não custa nada);
- o objetivo é auditar o banco de dados que já foi construído — para isso, use a skill `rdd-audita-schema`
  depois do Build;
- o objetivo é testar se o sistema no ar está seguro contra ataque — isso é segurança, não governança.

## Como a prova de cada requisito chega até você

Cada lacuna aplicada entra no DEFINE como um teste de aceitação no padrão **If/then**: a ação proibida e a
recusa esperada. Ao lado, vai o **roteiro de prova** do catálogo (`prova_manual`): de 3 a 5 passos, cada um
com o resultado esperado, para você executar e marcar quando o sistema estiver pronto.

O roteiro vai para o AT **sempre**. Se o seu projeto roda o Verify Gate por comando (Claude Code ou Codex com testes automatizados), peça
também o `prova_script` do item: ele já vem invertido — sai `0` só quando o banco **recusa** a ação proibida,
e reprova quando a aceita ou quando o nome de tabela ou coluna não confere. Adapte só os nomes e **não mexa
na inversão nem na guarda de schema**. Rode contra um banco de desenvolvimento, de teste ou um branch —
**nunca contra produção**: mesmo com `rollback`, a tentativa trava a linha e dispara os triggers.

## Regras que não se negociam

- **Base legal só do catálogo, e só `confirmado`.** Base `nao-confirmado` não se cita — nem artigo, nem
  número de lei, nem "aproximadamente". O relatório usa a frase padrão do procedimento e fica com o
  fundamento técnico.
- **Uma decisão por lacuna**: aplicar · recusar (com motivo) · adiar. Nunca "aplicar todos".
- **Sem tema financeiro, sem relatório**: N.A. em uma mensagem, sem arquivo. A triagem é pelo sentido, não só
  pela palavra — e, em dúvida, não é N.A.
- **Quem escreveu o Define não se revisa**: rode esta skill numa conversa nova.

## Onde entregar

- **No chat (ChatGPT, Claude):** entregar o relatório e o DEFINE atualizado para download; no primeiro uso,
  entregar também o `GOVERNANCA_PADRAO.md`, para você guardar na pasta do projeto.
- **No agente com acesso ao projeto (Claude Code, Codex):** gravar os arquivos na pasta do SDD e atualizar
  o DEFINE no lugar.

## Validações e checklist de qualidade

- [ ] Triagem registrada: gatilhos com linha ou AT, ou N.A. em uma mensagem, sem arquivo.
- [ ] `GOVERNANCA_PADRAO.md` lido (confirmado em uma linha) ou criado (5 campos, uma mensagem).
- [ ] Todo item do catálogo com exatamente um veredito; cobertura em uma linha no topo.
- [ ] Cada lacuna com: o que muda no app · por quê · requisito EARS · como provar · severidade.
- [ ] Base legal só de item `confirmado`; senão, a frase padrão.
- [ ] Uma decisão por lacuna; recusa com motivo vai para Riscos aceitos.
- [ ] Aplicados viram teste de aceitação no DEFINE; Clarity Score antes e depois.
- [ ] O relatório fecha com: "A skill recomenda; o profissional decide e responde."

## Tratamento de exceções

**DEFINE não encontrado:** dizer onde procurou e pedir o caminho. Não reconstruir o DEFINE de memória.

**Pergunta sobre a lei:** responder com a base do catálogo se estiver `confirmado`; senão, dizer que ainda
não está confirmada no catálogo e que deve ser conferida na fonte oficial.

**Recusa sem motivo:** repetir a pergunta pedindo o motivo e não gravar nada.

**O profissional quer mudar o catálogo:** registrar a sugestão no relatório; o catálogo muda numa nova
versão da skill, não durante a revisão.

## Texto canônico de recusa

"Esta skill recomenda requisitos de governança; ela não decide por você nem substitui a sua
responsabilidade técnica pelo sistema."

"Não cito base legal que não esteja confirmada no catálogo. Confira na fonte oficial antes de usar."

## Próximo passo

Se o app tem interface e você usa a sua `ux-review`: rode-a agora sobre o DEFINE atualizado. Senão:
Execute o **SDD Design by RDD**.

## Inventário do bundle

- `references/CATALOGO_GOVERNANCA.md`: os 20 itens, as bases legais com status e as provas por item.
- `references/PROCEDIMENTO.md`: os seis passos da revisão.
- `assets/GOVERNANCA_REVIEW_TEMPLATE.md`: modelo do relatório.
- `assets/GOVERNANCA_PADRAO_TEMPLATE.md`: modelo do padrão do projeto (5 campos).
- `evals/cases.json`: oito cenários comportamentais escritos.
- `manifest.json`: o que foi executado, o que está pendente e o que a skill ainda não prova.
- `agents/openai.yaml`: metadados para o ChatGPT.

## Metodologia e autoria

Esta skill foi construída com a metodologia de Roberto Dias Duarte.
