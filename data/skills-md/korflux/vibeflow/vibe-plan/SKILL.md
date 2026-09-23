---
name: vibe-plan
description: >
  Fatia a spec em tasks verificáveis e grava em `.vibeflow/phases/phase-N-slug/plan.md` ou `.vibeflow/mvp/plan.md`.
  Use when the user runs /vibe-plan, pede plan, fatiar a spec, criar tasks,
  todo, ordem de execução, ou a rota é high/xhigh/max com spec em disco,
  mesmo que não diga vibe-plan.
---

# vibe-plan

Não invente `n`, slug ou path. Sem spec aprovada no alvo, não há plan. Sem `.vibeflow/`, pare e mande `/vibe-init`.
Um único arquivo. Não escreva código nesta skill. Open Questions no arquivo é defeito.
No MVP, preserve a ação e os IDs das decisões críticas nas tasks que as implementam.

A investigação começa pelo resultado pedido e pelas dependências reais de execução. Use `rg --files` para localizar `spec.md`, `interview.md`, `REGRAS.md`, entradas e testes; use `rg -n` para localizar A*/C*, decisões, símbolos e comandos de verificação. Abra somente esses paths e as dependências do fluxo; expanda a leitura apenas quando uma lacuna bloquear o fatiamento. O inventário é mapa de seleção, não autorização para ler a árvore inteira.


## 0. Entender e usar o script

1. Resolva o diretório desta skill e leia o motor que vai executar: `scripts/plan.ps1` no Windows ou `scripts/plan.py` no fluxo Unix. Entenda seleção de alvo, recusas, preparação do destino e preservação do arquivo vivo antes de chamá-lo. Se encontrar defeito, corrija o motor e prove o contrato antes de continuar.
2. No cwd do repo:
   - Windows: `pwsh "<skill>/scripts/plan.ps1"`.
   - Unix: `bash "<skill>/scripts/plan.sh"`.
   - Alvo MVP: acrescente `-Mvp` ou `--mvp`.
3. Leia o JSON operacional emitido no stdout pelo comando acima. Use `rg --files` e `rg -n` para localizar `spec.md` (obrigatório), `interview.md` se houver, `plan.md` e `.vibeflow/REGRAS.md`, além dos caminhos necessários para definir resultados, dependências e provas. Abra somente as entradas e dependências do fluxo, não a árvore inteira.

Erros determinísticos previstos: `INIT_AUSENTE` exige `/vibe-init`. `PLAN_SEM_SPEC` exige spec prévia. `MVP_INESPERADO`, `MODO_INVALIDO`, `PLAN_JA_ANALISADO` e `FASE_AUSENTE` exigem diagnosticar a causa e não devem ser contornados.

## 1. Abrir

Declare em cerca de cinco linhas: rota, modo, alvo, spec, status da spec e estado do artefato vivo.

```text
modo: reuse · alvo: phase-1-lock-bloco · spec: sim · spec-status: aprovado · artefato vivo: presente
```

- `modo_sugerido=criar`: não há pasta com spec. Não invente fase; mande `/vibe-spec`.
- `rota=mvp`: alvo fixo `.vibeflow/mvp`, sem `--dir`; a spec precisa estar aprovada e declarar as decisões críticas.

## 2. Gate

| Sinal | Ação |
|---|---|
| Typo ou uma linha óbvia | Não usar plan |
| Sem `spec.md` no alvo | Parar. Encaminhar para `/vibe-spec` |
| Spec `# Status: rascunho` e o humano pediu o plan | Alterar a spec para `aprovado` diretamente no arquivo (1 linha no chat) e seguir |
| Spec rascunho sem pedido de plan | Parar. Pedir leitura e aprovação da spec |
| Intenção, sucesso ou limites frouxos | Devolver para `vibe-interview` ou `vibe-spec`. Não completar no chute |
| Dúvida pontual de ordem técnica | Resolver via chat (Q + RECOMENDO) |
| Com UI visível sem `design.md` aprovado na mesma pasta | Parar. Encaminhar para `vibe-design` |
| Sem UI visível | Registrar N/A explícito no plan, sem bloqueio |
| `analyze.md` já existente no alvo | Não sobrescrever. Pedido novo exige outra fase |

```text
Q: <decisão que trava o fatiamento>
RECOMENDO: <opção>, <1 linha explicando o porquê e impacto>
(ok / outra?)
```

## 3. Preparo e ferramentas

Antes de fatiar, confira a spec, a superfície da entrega e somente as ferramentas exigidas pelas provas escolhidas:

1. **Spec sólida:** A*/C* observáveis, limites claros de Fora, direção visual definida se houver UI e caminhos existentes ou acordados. Com UI visível, exige `design.md` aprovado na mesma pasta; sem UI, registra `Design: N/A`.
2. **Preparo local:** Faça uma checklist curta dos comandos, ferramentas e serviços necessários para executar as provas. Confira `gitleaks` quando o repositório ou CI exigir varredura de segredos. Resolva uma instalação ou conexão local simples durante o preparo quando estiver disponível e autorizada. Ausência local, por si só, não cria T*: planeje uma task somente se o setup persistente fizer parte da entrega do projeto. Se uma dependência externa impedir uma prova e não houver solução local, registre o bloqueio ou a limitação.
3. **Validação visual:** Se a entrega envolver interface ou DOM, escolha navegador integrado (`@Browser` ou equivalente), depois MCP Server `chrome-devtools`, ou Playwright somente se já existir no repositório ou for solicitado para fluxos repetíveis e assertions. Ausência de capacidade visual é limitação explícita; não obriga navegador em tasks sem UI nem instalação automática.
4. **Decisões críticas (MVP):** Toda decisão da spec possui ação explícita e as tasks correspondentes citam seus IDs.

## 4. Fatiar por resultado

Agrupe o trabalho em fatias verticais verificáveis, com um resultado coeso por T*. Uma T* pode tocar vários arquivos e durar mais de uma sessão quando continua entregando o mesmo resultado.

Crie outra T* somente quando houver um resultado entregável separado, uma dependência real de execução, um risco que exija isolamento ou uma fatia que não possa ser verificada como unidade. Quantidade de arquivos ou critérios de aceite, duração estimada, pontuação e a conjunção "e" no título não justificam uma quebra por si sós.

### Regras das Tasks

1. **Ponto de entrada:** Quando o resultado criar ou alterar um ponto de entrada executável, inclua o smoke test desse ponto na mesma T*. Não crie T* apenas para repetir baseline ou smoke test genérico.
2. **Estrutura de cada T\*:** Título com verbo e resultado, `Spec: A*/C*`, aceite observável, verificação com comando executável do repo e dependências explícitas (`Deps`). Inclua `Arquivos` ou `Risco` somente quando ajudarem a implementar, isolar ou revisar a fatia.
3. **Decisões críticas:** Quando a task implementar ou substituir decisão crítica, adicionar `Decisões: <ID> (<ação>)`.
4. **Verificação:** Toda task exige comando executável que prove seu aceite. Verificação só manual ou leitura de arquivo não conta como prova suficiente.
5. **Dependências (`Deps`):** Declarar apenas predecessores reais de execução. Fatias independentes usam `Deps: nenhuma`; a linha de dependências define a fila, sem repetir a ordem em outra seção.
6. **Paralelização e checkpoint:** Indique grupos paralelizáveis somente quando independência, ownership dos arquivos e ausência de conflito estiverem claros. Registre checkpoint de review apenas quando um risco ou contrato compartilhado precisar ser julgado antes de outra T*.
7. **UI Greenfield:** Entregue componentes e tokens dentro de fatias de resultado; não crie task de preparo visual sem entrega verificável.
8. **Banco de dados e migrations:** Mantenha migrations e schemas nas respectivas fatias verticais e inclua comandos executáveis de migration e seed mínimo. Migrations devem ser não destrutivas (padrão expand/contract).

IDs estáveis: `T1`, `T2`, `T3`... em ordem sequencial. Sem prefixos arbitrários como `T001`, `[P]` ou `[US1]`.

## 5. Escrever e Salvar

Artefato vivo: `<created.path>/plan.md`. Molde: `templates/plan.md`. Mantenha `# Status: rascunho` enquanto o plano estiver em elaboração.
Não pergunte se pode salvar e não cole o corpo do documento no chat.

1. Execute o apply. Ele prepara o arquivo vivo somente quando ausente e preserva bytes quando ele já existe:
   - Modo phase:
     `pwsh "<skill>/scripts/plan.ps1" -Apply`
     `bash "<skill>/scripts/plan.sh" --apply`
   - Modo MVP:
     `pwsh "<skill>/scripts/plan.ps1" -Apply -Mvp`
     `bash "<skill>/scripts/plan.sh" --apply --mvp`
2. Escreva ou atualize diretamente o arquivo vivo. Omita seções não aplicáveis.
3. Responda no chat apenas:

```text
Plan gravado: <created.path>/plan.md

- Overview: <1 linha>
- Resultados e dependências: <resumo curto da fila, sem repetir cada Deps>
- Preparo: <ferramentas necessárias disponíveis ou bloqueio registrado>
- Execução conjunta/checkpoint: <somente se aplicável>

Arquivo disponível em <created.path>/plan.md. Responda "aprovado" para confirmar, "pode ir pro implement" (ou "pode ir para a próxima fase") para avançar imediatamente, ou indique os ajustes desejados.
```

## 6. Ajuste ou Aprovação

| Resposta | Ação |
|---|---|
| Aprovado (sem pedir próxima porta) | Alterar `# Status: aprovado` diretamente no vivo; parar e aguardar próximo comando |
| "Pode ir pro implement" / "pode ir para a próxima fase" / pede código / `vibe-implement` | Alterar `# Status: aprovado` no vivo; iniciar imediatamente `vibe-implement` (ou `vibe-analyze` se rota MVP) |
| Pedido de alteração | Patch direto no arquivo vivo; até 5 bullets no chat; solicitar nova conferência |
| "Parece bom" sem pedir implementação | Perguntar: "Aprovado no arquivo ou deseja algum ajuste?" |
| Spec ou intenção quebrou | Devolver para `vibe-spec` ou `vibe-interview`. Não forçar implementação |

Rascunho sem "aprovado" e sem pedido da próxima porta não autoriza iniciar o código.

## 7. Fechar

Não commite no git nesta porta. O commit começa na `vibe-implement`, depois da prova verde de cada task. Não dispare a próxima skill a menos que o usuário tenha pedido explicitamente para avançar (§6).
Informe que o JSON do inventário foi consumido do stdout e não gerou arquivo persistido. Recomende abrir um novo chat para `vibe-implement`; continuar no mesmo chat é permitido somente por escolha consciente do humano. O `plan.md` vivo e o handoff são a ponte entre chats.
Handoff normal: `vibe-implement`. Handoff MVP: `vibe-analyze` (pois o modo max exige análise antes do código).
Zero código nesta execução.

