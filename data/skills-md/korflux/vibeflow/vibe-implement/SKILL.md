---
name: vibe-implement
description: >
  Executa a fatia elegível da fase com prova, registra a execução e marca [x] diretamente no plan.md
  (e spec/review). Use when the user runs /vibe-implement, pede implementar, código, build, faz a T*,
  pode seguir, ou a rota é low/medium/high/xhigh/max com código de comportamento, mesmo que não diga vibe-implement.
---

# vibe-implement

Não invente `n` se há plan. Sem prova e sem teste verde, sem `[x]` no `plan.md` ou commit da task. Sem `todo.md` nem `tasks.md`.
Sem `.vibeflow/`: `/vibe-init`. Open Questions no markdown = defeito. Cada task verde gera um commit isolado; o push fica para o fechamento aprovado da phase.
Proibido pular tasks ou desistir de erros. Diagnostique a causa raiz de qualquer falha no código e repita a prova após corrigir.
Comentários semânticos obrigatórios em todas as funções criadas ou alteradas.
As provas de execução e arquivos modificados são registrados diretamente sob cada task no `plan.md` vivo.
No MVP, não execute código sem analyze `aprovado` e `limpo`; a fila vem somente de `.vibeflow/mvp/plan.md`.

A investigação começa pela pergunta da T* elegível. Use `rg --files` para localizar os paths da task, seus testes e dependências; use `rg -n` para localizar símbolos, chamadas e contratos que formam o fluxo real. Abra somente essas entradas e expanda a leitura quando uma lacuna bloquear a prova. O inventário é mapa de seleção, não autorização para ler a árvore inteira. `implement.md` é o artefato vivo da execução; a IA o escreve diretamente.

## 0. Entender e usar o script

1. Resolva o diretório desta skill e leia o motor que vai executar (`scripts/implement.ps1` no Windows ou `scripts/implement.py` no Unix). Ele realiza inventário determinístico e projeta a fila de dependências, preparando o artefato vivo sem substituir conteúdo existente.
2. No cwd do repo:
   - Windows: `pwsh "<skill>/scripts/implement.ps1"`
   - Unix: `bash "<skill>/scripts/implement.sh"` (Python 3, senão pwsh 7)
   - Alvo MVP: acrescente `-Mvp` ou `--mvp`.
3. Leia o JSON operacional emitido no stdout pelo comando acima. A escolha da T* sai de `fila.elegiveis` no JSON. Use `rg --files` e `rg -n` para localizar `.vibeflow/REGRAS.md`, os paths da T* e os símbolos do fluxo. Abra somente as entradas e dependências relevantes; não leia a árvore inteira.

`INIT_AUSENTE` exige init. `IMPLEMENT_SEM_ALVO`, `IMPLEMENT_SEM_PLAN`, `IMPLEMENT_ANALYZE_AUSENTE`, `IMPLEMENT_ANALYZE_RASCUNHO`, `IMPLEMENT_ANALYZE_BLOQUEADO`, `MVP_INESPERADO`, `MODO_INVALIDO`, `FASE_AUSENTE` e `PHASES_INESPERADO` não são contornados.

## 1. Abrir (5 linhas)

ROUTE · modo A/B · alvo · fila · plan · analyze

```text
ROUTE: high · modo: A · alvo: phase-1-lock-bloco · fila: T2|T4 elegíveis · plan: sim · implement: vivo
```

`modo_sugerido=criar` = não há fase com `plan.md`. Não invente pasta. `high+` para e manda `/vibe-plan`. `fila` nulo = avulsa. `parse=ausente` = plan sem T*.

## 2. Gate

Declare `ROUTE: low|medium|high|xhigh|max` e modo A ou B. Default = **A**.

| Sinal | Ação |
|---|---|
| Typo / rename / uma linha sem runtime | **Não** usar |
| `high+` sem `plan.md` | **Para.** `/vibe-plan` |
| `max` sem `analyze.md` | **Para.** `/vibe-analyze` |
| Analyze ausente, rascunho ou veredito `bloqueado` no MVP | **Para.** Não flipa nem executa. Volta ao analyze |
| Plan/analyze `# Status: rascunho` e o humano pediu **esta** skill | Flip para `aprovado` (1 linha) e siga, se o veredito não for `bloqueado` |
| `low`/`medium` claro sem plan | Avulso: prova mínima no código/teste |
| `review.md` com R* Critical/Required em `[ ]` | Fila = R* primeiro. Q só se houver mais de um |
| `fila` com 2+ elegíveis e o humano não nomeou T* | **Para.** Q. Recomenda a de menor `n`. Sem código |
| `fila` com 1 elegível | Executa essa. Sem Q de escolha |
| `fila` com 0 elegíveis e 0 abertas | Handoff `vibe-review`. Não dispara |
| `fila` com 0 elegíveis e `bloqueadas` | Mostra as deps. Sem Q “qual T*” |
| Humano nomeou T* elegível | Executa essa. Sem Q |
| Humano nomeou T* bloqueada | Mostra deps. Sem código |
| Verificação da T* só manual, sem comando | **Para.** Q (automatizar / humano valida / volta plan) |
| Intenção/sucesso/fora frouxos | Devolve interview/spec |
| Bloqueio externo intransponível | **Para.** Q + RECOMENDO. Não pule em silêncio |

```text
Q: <o que trava>
RECOMENDO: <opção>, <1 linha explicando motivo e impacto>
(ok / outra?)
```

Modo B só se o humano pediu: `auto`, “faz o todo”, “não para”, “run completa” ou execução paralela das T*s independentes elegíveis.
“Pode seguir” no modo A = próxima `T*` elegível. Não existe agrupamento intermediário.

## 3. Ciclo da fatia

Execute cada task seguindo as 6 etapas. O coordenador responde pela integração final, pelos artefatos vivos e pelo índice Git.

1. **Reconhecer (O que já existe?):**
   Formule a pergunta da T*, localize com `rg --files` e `rg -n` os pontos de entrada, símbolos, chamadas e testes da fatia, e trace somente as dependências do fluxo real. Com UI, inclua o `design.md` aprovado do alvo como entrada e siga tokens, motion e prova por tela. No Express (ajuste fino sem comportamento novo, low ou medium), reuse a mesma phase e siga só o recorte existente e alterado do design quando houver, sem exigir design ausente, sem rodar apply de design, sem plan novo e sem reabrir tasks antigas. Reutilize helpers, utilitários, componentes visuais, types e módulos existentes da standard library ou do projeto. Não reescreva o que já existe.
2. **Escolher execução e delegar quando fizer sentido:**
   Use delegação nativa somente se o host a oferecer. Recalcule a fila e delegue apenas T*s elegíveis e independentes; respeite `Deps` e só libere uma dependente depois que o coordenador registrar suas dependências como concluídas. Sem capacidade de delegação ou isolamento seguro, execute a mesma fila em sequência.
   Delimite cada entrega por resultado, aceite, dependências, paths exclusivos e comando de verificação. Use worktree/branch isolada ou ownership sem sobreposição. Se não houver isolamento nem ownership exclusivo, não delegue escrita. Agentes não alteram `plan.md`, `spec.md`, `implement.md` ou `review.md`, nem operam o índice Git, criam commits ou fazem push. Peça que retornem os paths alterados, resumo do diff, prova executada e pendências.
3. **Codar e integrar:**
   Implemente de forma direta, enxuta e restrita ao aceite da T*. O coordenador confere cada retorno, integra somente paths autorizados e resolve conflitos antes de prosseguir. Prova relatada por um agente ajuda no diagnóstico, mas não substitui a prova do estado integrado.
4. **Simplificar antes da prova:**
   Revise o código integrado, remova duplicações e verbosidade desnecessária e preserve validações, segurança e comportamento exigidos. Deixe comentários semânticos em todas as funções criadas ou alteradas.
5. **Executar a prova final:**
   Rode o comando real da T* uma vez no estado integrado e simplificado. Na primeira task funcional (T1), valide obrigatoriamente o *Smoke Test / Walking Skeleton* no ponto de entrada real da aplicação. Se a prova falhar, diagnostique a causa raiz, corrija e execute novamente até ficar verde. Se código ou teste da task for editado depois da prova verde, repita a verificação afetada. Atualizar artefatos vivos e preparar o commit não invalida a prova.
   Se a task tocar interface visual web, selecione nesta ordem, navegador integrado (`@Browser` ou equivalente) primeiro quando disponível, MCP Server `chrome-devtools` para `navigate_page`, `take_snapshot`, interação, `take_screenshot`, DOM, estilos, console, rede e assets, ou Playwright somente se já existir no repositório ou for solicitado para fluxos repetíveis e assertions. Siga `references/chrome-devtools.md`. Registre rota, viewport, estado, ações e evidência observada. Sem capacidade visual, registre a limitação e não marque a task como concluída nem instale ferramenta automaticamente. Para controles compactos, preserve nome acessível, área de interação, foco visível e tooltip quando aplicável; ações ambíguas mantêm texto.
6. **Registrar e fechar:**
   Depois da prova verde, atualize `plan.md` e `spec.md`/`review.md` somente nos critérios provados e acrescente a trilha em `implement.md`. Mantenha `# Status: rascunho` enquanto o registro estiver incompleto; feche a fatia só depois da prova e da integração.

Critérios adicionais:
- DoD: `references/definition-of-done.md` no que couber.
- Banco de dados: Se a fatia tocar banco de dados ou dinheiro, siga `references/database-and-migrations.md` (DECIMAL/NUMERIC para valores monetários, queries parametrizadas obrigatórias, sem N+1, índices em FKs, transações ACID curtas).
- Sem teste verde executável, sem marcação de conclusão no disco.

## 4. Marcar e Registrar no plan.md

Após a aprovação do teste da task, a IA aplica o patch diretamente no `plan.md` vivo sob a seção da task `### T{n}:`:

```markdown
### T1: Ponto de entrada e Smoke Test
- [x] T1 concluída
- **Spec:** A1
- **Deps:** nenhuma
- **Verificação:** `npm test -- --grep "smoke"`
- **Prova:** `npm test` -> 1 passing (115ms)
- **Arquivos:** `src/index.ts`, `tests/smoke.test.ts`
- **Decisões:** AUTH-01 (implementada)
```

Outros arquivos marcados:
| Arquivo | O que marcar |
|---|---|
| `spec.md` | `A*` / `C*` **só** os que a fatia provou |
| `review.md` | `R*` Critical/Required que o fix provou |
| `interview.md` | **Não** |

No MVP, certifique-se de registrar quais IDs críticos foram implementados. Não publique essas decisões em `REGRAS.md`; isso pertence ao pós-review aprovado.

### Commit da task

Depois de atualizar os artefatos e antes de declarar a fatia concluída:

1. Compare o estado do Git com o snapshot capturado antes da task. Se um path da task já estava alterado, pare e peça isolamento ou decisão humana; não misture alterações.
2. Em execução delegada, somente o coordenador altera artefatos vivos e o índice Git. Liste os paths integrados e provados pela task e adicione-os explicitamente, por exemplo `git add -- path/da/task outro/path`. Nunca use `git add -A` ou `git add .`; o inventário é transitório no stdout e não cria arquivo no workspace.
3. Confira `git diff --cached --check` e `git diff --cached --name-only`. Se o diff indexado contiver path fora da task, remova-o do índice e pare se a origem não for clara.
4. Crie um commit sem `Co-Authored-By`, com mensagem no formato `task(Tn): <outcome curto>`. Não faça `git push` nesta etapa.
5. Registre a mensagem e o hash retornado por `git rev-parse HEAD` no resultado da execução e no chat. Não reabra `implement.md` apenas para anexar o hash, pois isso criaria um residual fora do commit da task. O próximo estado começa no commit criado.

## 5. Resposta no Chat

Responda no chat apenas:

```text
Implementação registrada: <alvo>/plan.md

- Fatia: <T* | R* | avulsa>
- Marcado: <T* / A* / C*>
- Prova: <comando> -> <resultado>
- Arquivos: <paths alterados>
- Handoff: vibe-review | próxima T* | Q

Fatia concluída e registrada em <alvo>/plan.md.
```

## 6. Modos

**A (default):** executa exatamente a `T*` escolhida ou única elegível, cria o commit dessa task e para. Se o usuário disser apenas "aprovado" ou "ok", permanece parado aguardando a próxima instrução. Se o usuário disser "pode seguir", "segue" ou "pode ir para a próxima fase", avança imediatamente para a próxima task elegível do plano ou para `vibe-review` se a fila estiver concluída. Quando houver fila, use um chat por T* como recomendação de isolamento e abra um novo chat focado na próxima T*; o `plan.md` e o `implement.md` vivos carregam o contexto verificável. Continue no mesmo chat somente se o humano escolher conscientemente.

**B:** percorre `fila.elegiveis` recalculando após cada item concluído. Pode delegar T*s independentes quando houver capacidade no host e isolamento seguro; tasks dependentes só começam depois da integração, prova, marcação e commit das dependências. O coordenador serializa atualizações dos artefatos vivos e do índice Git, cria um commit por task e para em falha, bloqueio ou fila vazia.

Fila zerada (T* da run, ou R* bloqueantes) → handoff `vibe-review`; recomende um novo chat para a review. Se o usuário autorizar avançar para a review, inicia `vibe-review` diretamente. O `plan.md` e o `implement.md` vivos são a ponte; continuar no mesmo chat exige escolha consciente.

## 7. Fechar

Avise o commit criado e o que entrou nele. O push fica fora desta porta e só ocorre no fechamento aprovado da phase. Fora do commit: qualquer path pré-existente ou não autorizado.
Handoff no chat e no arquivo. Não invente work extra.
