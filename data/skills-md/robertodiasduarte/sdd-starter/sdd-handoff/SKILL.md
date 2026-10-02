---
name: sdd-handoff
license: MIT
description: "Fecha um ciclo de trabalho e passa o bastão para a próxima sessão: registra o que foi feito, o que ficou pendente (separando o que está quebrado do que é melhoria), quais são os próximos passos e o que não pode quebrar — e gera um prompt de retomada que funciona sozinho, sem depender da conversa anterior. Mantém um único arquivo de handoff por feature, com cada etapa nova no topo. Use quando o usuário disser que vai parar, que o contexto está acabando, que terminou uma etapa, que quer documentar para continuar depois, ou ao final da fase de Build de um fluxo SDD."
metadata:
  author: Roberto Dias Duarte
---

# SDD Handoff

## Quick start

Registrar o estado do trabalho e preparar a retomada, de forma que a próxima sessão — que não viu nada desta conversa — consiga continuar sem redescobrir o que já foi decidido.

1. Inferir o modo pelo contexto (*continuar* ou *entregar*) e confirmar em uma linha.
2. Resolver a família: já existe handoff desta feature? Atualizar, não criar outro.
3. Reunir o estado a partir da conversa — buscando agora os dados que faltarem.
4. Preencher a ficha e a seção da etapa (seis seções).
5. Classificar as pendências em 🐛 bug fix e ✨ feature improvement.
6. No modo *entregar*, percorrer o checklist de fechamento (que não bloqueia nada).
7. Gravar o arquivo — ou, sem filesystem, entregar no chat dizendo o que fazer com ele.
8. Gerar o prompt de retomada, com todo dado colado.

Consultar [references/handoff-protocol.md](references/handoff-protocol.md) para as regras de decisão. Para os artefatos, usar obrigatoriamente [assets/HANDOFF_TEMPLATE.md](assets/HANDOFF_TEMPLATE.md) e [assets/SESSION_PROMPT_TEMPLATE.md](assets/SESSION_PROMPT_TEMPLATE.md) como moldes. O arquivo [assets/HANDOFF_EXAMPLE.md](assets/HANDOFF_EXAMPLE.md) mostra o nível de detalhe esperado.

## Quando usar / Quando não usar

Usar quando o usuário sinalizar que vai parar, que o contexto está no limite, que terminou uma etapa, ou pedir explicitamente para documentar/passar o bastão. Usar também ao final de um fluxo SDD, depois do Build.

Não usar para escrever documentação de produto, manual de uso ou README — o handoff é registro de trabalho em andamento, não documentação de entrega. Não usar para publicar/implantar nada: esta skill documenta o ciclo, não executa release.

## Dados necessários

Entrada mínima:
- a conversa atual, com o trabalho que foi feito.

Entradas opcionais:
- arquivo de handoff anterior da mesma feature;
- artefatos do fluxo SDD (Brainstorm, Define, Design, Build Report);
- acesso ao projeto para conferir nomes de arquivo, dados e estado.

Não exigir acesso a filesystem, repositório ou sistema externo. Quando algo não estiver acessível, registrar a limitação em vez de inventar.

### Assets obrigatórios de saída

[assets/HANDOFF_TEMPLATE.md](assets/HANDOFF_TEMPLATE.md) é o molde oficial do documento de handoff e [assets/SESSION_PROMPT_TEMPLATE.md](assets/SESSION_PROMPT_TEMPLATE.md) é o molde do prompt de retomada. São **assets de saída**, não material conceitual: sempre reutilizá-los para montar o resultado final, em vez de reconstruir a estrutura de memória.

## Procedimento passo a passo

### 1. Inferir o modo e confirmar

Identificar pelo contexto qual dos dois modos se aplica (tabela de sinais em [references/handoff-protocol.md](references/handoff-protocol.md) § 1):

- **continuar** — o trabalho segue depois. Entrega ficha + prompt de retomada.
- **entregar** — a etapa terminou. Entrega o mesmo, mais o checklist de fechamento.

Confirmar em **uma linha** e seguir. Não abrir menu de escolha, não fazer pergunta de múltipla escolha sobre isso: quem pede um handoff normalmente está sem contexto ou sem tempo. Sem sinal claro, assumir *continuar* e dizer que assumiu.

### 2. Resolver a família da feature

Antes de criar qualquer arquivo, verificar se já existe handoff desta feature — buscando por domínio, não por nome exato. Se existir, **atualizar o arquivo existente**, acrescentando a etapa nova no topo. Em dúvida, perguntar mostrando o que encontrou. Detalhes em [references/handoff-protocol.md](references/handoff-protocol.md) § 2.

Um handoff por feature. Etapas são seções dentro dele, nunca arquivos separados.

### 3. Reunir o estado

Varrer a conversa e reconstruir:

- **O que foi feito** — o que foi construído, decidido, corrigido. Com nomes de arquivo e decisões explícitas.
- **Casos e testes em aberto** — o que estava sendo testado, **com os dados reais**: qual cliente, qual arquivo, qual data, qual identificador.
- **Pendências** — o que está quebrado (🐛) e o que é incremento planejado (✨).
- **Próximos passos** — lista ordenada, cada item com o dado exato e o critério de pronto.
- **Alertas** — o que não pode quebrar; o que está fora de escopo.
- **Onde está o trabalho** — pasta, projeto, branch.

**Se faltar um dado que você consegue buscar agora, busque agora.** A próxima sessão não terá como. Um handoff que diz "o cliente que estava com erro" obriga a próxima sessão a redescobrir qual era.

### 4. Preencher a ficha

Usar [assets/HANDOFF_TEMPLATE.md](assets/HANDOFF_TEMPLATE.md). A ficha do topo é o estado agregado da feature:

- **Objetivo** — estável entre etapas; o que a feature entrega quando estiver pronta.
- **Status** — 🔨 em andamento · ✅ completa · ⏸️ pausada.
- **Feito** / **Falta** — o que já saiu e o que resta.
- **Pronto quando** — critério verificável de conclusão (§ 6 do protocolo). Só marcar ✅ completa quando ele estiver objetivamente satisfeito.

Etapa nova entra como seção **no topo** das etapas anteriores. Etapas antigas já fechadas podem ser resumidas em poucas linhas.

Mudança de escopo, pausa ou replanejamento → **linha nova em `## Eventos`**, com data e motivo. Nunca reescrever "Falta" em silêncio.

### 5. Classificar as pendências

Separar sempre em duas listas: **🐛 bug fix** (quebrado, parcial, comportamento errado) e **✨ feature improvement** (incremento, melhoria, próxima etapa). Categoria sem itens recebe "nenhuma" — a ausência declarada também é informação.

**Registrar mesmo quando não há pendência alguma.** Um handoff de "etapa fechada, nada pendente" continua documentando o que foi feito. Não perguntar se vale a pena registrar: registrar é incondicional.

Risco que foi conscientemente aceito — algo que se decidiu ignorar por ora — entra como pendência com o motivo. Risco conhecido não pode evaporar entre sessões.

### 6. Checklist de fechamento (somente no modo *entregar*)

Percorrer as quatro perguntas com o usuário e registrar o que foi conferido:

1. O código roda?
2. Os critérios de aceite combinados passam?
3. As mudanças estão salvas onde deveriam?
4. O que quebrou está anotado?

**Este checklist não bloqueia a entrega.** Item não confirmado vira pendência e o handoff sai do mesmo jeito. Apresentar como inventário do que foi conferido — sem ✅/❌ pareados, sem contagem que se leia como nota, sem vermelho, sem a palavra "reprovado". Ver [references/handoff-protocol.md](references/handoff-protocol.md) § 7.

### 7. Entregar o documento

**Onde salvar.** Grave em `sdd/` na raiz do projeto — pasta visível, igual em qualquer agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos das cinco fases ficam lado a lado, sem subpastas.

Se houver filesystem de projeto gravável, salvar como `sdd/HANDOFF_{FEATURE}.md` (ou `.claude/sdd/HANDOFF_{FEATURE}.md` quando essa pasta já existir), sem sobrescrever silenciosamente um arquivo existente — quando já existir handoff da mesma feature, atualizar seu conteúdo (passo 2).

Se **não** houver filesystem acessível, entregar o Markdown completo no chat e fechar com estas três informações, nesta ordem:

1. que o documento **não foi gravado**;
2. o **nome de arquivo sugerido** (`HANDOFF_{FEATURE}.md`);
3. **o que fazer com ele** — salvar junto do projeto e reenviar no início da próxima sessão.

Nunca falhar em silêncio nem dar a entender que gravou.

### 8. Gerar o prompt de retomada

Usar [assets/SESSION_PROMPT_TEMPLATE.md](assets/SESSION_PROMPT_TEMPLATE.md), entregue em bloco pronto para copiar.

**Regra de ouro: nada de "como discutimos".** Todo identificador, caminho, comando e dado vai **colado** no prompt. Se uma linha não tem valor concreto, ou você busca o valor agora, ou apaga a linha.

O prompt precisa funcionar **sozinho**: mesmo que o arquivo de handoff se perca, os dados nele devem bastar para continuar.

Quando a feature estiver ✅ completa e não houver continuação, o prompt de retomada pode ser omitido — basta registrar o fechamento.

## Validações e checklist de qualidade

Antes de declarar o handoff concluído, verificar:

- [ ] Modo inferido e confirmado em uma linha, sem menu.
- [ ] Família resolvida: atualizou o handoff existente, ou é feature genuinamente nova.
- [ ] Ficha preenchida: Objetivo · Status · Feito · Falta · Pronto quando.
- [ ] "Pronto quando" é verificável, não uma opinião.
- [ ] As seis seções da etapa preenchidas.
- [ ] Todo caso citado tem o dado concreto junto, não só o apelido.
- [ ] Pendências separadas em 🐛 e ✨, com "nenhuma" declarado quando for o caso.
- [ ] Mudança de escopo registrada em `## Eventos`.
- [ ] Próximos passos ordenados, cada um com critério de pronto.
- [ ] Modo *entregar*: checklist percorrido e apresentado como inventário, sem reprovação.
- [ ] Documento gravado — ou, sem filesystem, entregue no chat com as três informações.
- [ ] Prompt de retomada se sustenta sozinho.
- [ ] Nenhum `{placeholder}` sobrou no resultado final.
- [ ] Nenhuma frase do tipo "como discutimos" ou "continue de onde paramos".

Quando houver filesystem, o script [scripts/validate_handoff.py](scripts/validate_handoff.py) confere mecanicamente parte disso:

```
python3 scripts/validate_handoff.py HANDOFF_{FEATURE}.md
```

Saída `PASS` com código 0; problemas listados com código 2.

## Tratamento de exceções

- **Usuário com pressa ("só me dá o prompt"):** entregar o prompt primeiro, e registrar a ficha logo em seguida — sem transformar isso em negociação. Documentar é incondicional.
- **Não há handoff anterior mas a feature parece antiga:** perguntar antes de criar, mostrando o que procurou.
- **Trabalho de várias features na mesma conversa:** um handoff por feature. Perguntar qual documentar, ou documentar cada uma em seu arquivo.
- **Sem filesystem:** entregar no chat com as três informações do passo 7. Nunca fingir que gravou.
- **Nada foi concluído na sessão:** ainda assim registrar — o que foi tentado, o que não funcionou e por quê é informação valiosa para a próxima sessão.
- **Feature terminou de vez:** marcar ✅ completa somente com o "Pronto quando" satisfeito; o prompt de retomada pode ser omitido.
- **Usuário não sabe dizer o critério de pronto:** ajudar a formular a partir do que ele quer conseguir fazer no fim, em vez de deixar o campo vago.

## Examples

**Contexto acabando**
`Estou no limite do contexto, documenta pra eu continuar em outra sessão.`

Modo *continuar*. Registrar o estado, gerar o prompt com todos os dados colados.

**Etapa concluída**
`Terminei essa parte, quero fechar.`

Modo *entregar*. Registrar o estado, percorrer o checklist de fechamento como inventário e gerar o prompt caso ainda reste trabalho.

**Continuação de feature existente**
`Vamos parar por hoje — isso aqui é continuação do controle de honorários da semana passada.`

Localizar o handoff existente, acrescentar a etapa nova no topo, atualizar a ficha agregada.

**Sem filesystem**
`(no chat da web, sem projeto acessível) Passa o bastão.`

Entregar o documento completo no chat, dizendo que não foi gravado, sugerindo o nome do arquivo e explicando que ele deve ser salvo e reenviado na próxima sessão.

## Next Step

Fluxo SDD concluído. Guarde o arquivo de handoff junto do projeto e comece a próxima sessão com o prompt de retomada.

---

Parte do SDD Open by RDD — https://github.com/robertodiasduarte/sdd-open
