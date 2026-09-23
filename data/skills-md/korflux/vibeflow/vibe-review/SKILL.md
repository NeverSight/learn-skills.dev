---
name: vibe-review
description: >
  Julga o patch, os testes e a cobertura pós-código e grava em `.vibeflow/phases/phase-N-slug/review.md` ou `.vibeflow/mvp/review.md`.
  Use when the user runs /vibe-review, pede review, revisa isso, LGTM, pode
  mergear, ou há handoff de vibe-implement / rota medium+, mesmo que não
  diga vibe-review.
---

# vibe-review

Não invente `n` se há plan. Não edite source, teste nem lockfile. Sem `review.md` não há veredito.
Um arquivo por alvo. Sem `.vibeflow/`: `/vibe-init`. Open Questions no arquivo = defeito. Correções ficam na `vibe-implement`; o Git só é finalizado após Approve e confirmação humana.
Decisões vigentes em `REGRAS.md` só são sincronizadas após Approve sem bloqueios e confirmação humana explícita.

A investigação começa pela pergunta de auditoria e pelo T*/diff que precisa ser provado. Use `rg --files` para localizar os artefatos, paths alterados, testes e referências aplicáveis; use `rg -n` para localizar símbolos, contratos e evidências. Abra somente as entradas e dependências do fluxo real e expanda a leitura quando uma lacuna bloquear o veredito. O inventário é mapa de seleção, não autorização para ler a árvore inteira.

## 0. Entender e usar o script

1. Resolva o diretório desta skill e leia o motor que vai executar. Entenda alvo, cadeia exigida, recusas, preparação do destino e preservação do arquivo vivo. Confirme que ele não escreve `REGRAS.md`; corrija e prove qualquer defeito antes de seguir.
2. No cwd do repo:
   - Windows: `pwsh "<skill>/scripts/review.ps1"`
   - Unix: `bash "<skill>/scripts/review.sh"` (Python 3, senão pwsh 7)
   - Alvo MVP: acrescente `-Mvp` ou `--mvp`.
3. Leia o JSON operacional emitido no stdout pelo comando acima. Use `rg --files` e `rg -n` para localizar o alvo, o que `files` listar, `plan.md` com as provas, `spec.md`, `analyze.md` se houver, `REGRAS.md` e o diff apontado pelo humano ou da sessão. Abra somente os paths que sustentam o veredito; não leia a árvore inteira.

`INIT_AUSENTE` exige init. `REVIEW_SEM_ALVO`, `REVIEW_CADEIA_INCOMPLETA`, `MVP_INESPERADO`, `MODO_INVALIDO`, `FASE_AUSENTE` e `SLUG_INVALIDO` não são contornados.

Apply:
- first-pass reuse/atualizar: `pwsh "<skill>/scripts/review.ps1" -Apply` (`--dir` se o alvo errar)
- avulsa sem cadeia: `… -Apply -Slug "<frase curta>"`
- MVP: `… -Apply -Mvp`, sem slug ou dir
- Unix: `review.sh --apply` / `--apply --slug "…"`

## 1. Abrir (6 linhas)

rota · tipo · alvo · plan/fila · spec · analyze · diff

```text
final · etapa 1 first-pass · alvo: phase-2-vibe-review · fila: concluída · spec: sim · analyze: sim · diff: working tree
```

`modo_sugerido=criar` e sem `--slug` = não há pasta. Não grude review nova no N de outro pedido.
Já existe `review.md` = próxima etapa no **mesmo** arquivo.

## 2. Gate

| Sinal | Ação |
|---|---|
| Sem alvo e sem diff | **Para.** Peça path, branch, PR ou `--dir` |
| T* obrigatórias em `[ ]` e o humano pediu “pronto da feature” | Recuse Approve de feature. Pode revisar o diff e listar o que falta no plan |
| Plan declara checkpoint e todas as T* do marco estão concluídas | Faça checkpoint somente do marco, das provas relevantes e do contrato ou risco declarado; registre as T* restantes |
| Plan declara checkpoint, mas alguma T* do marco está aberta | **Para.** Informe a dependência aberta e faça handoff para `vibe-implement` |
| Há T* abertas e não existe checkpoint aplicável no plan | Não faça review final nem invente checkpoint; informe a fila e faça handoff para `vibe-implement` |
| Todas as T* do plan estão concluídas | Faça review final da integração e dos riscos alterados |
| Intenção/sucesso/fora frouxos | Devolve interview/spec. Finding de código não reabre plan |
| Etapa 2+ | Mesmo `review.md`. Edite o vivo diretamente e acrescente a etapa sem substituir o histórico |
| “Já corrige” | Grave o veredito **primeiro**. Handoff implement. Não patche aqui |
| MVP sem cadeia max completa | Recuse review e corrija a porta ausente |

```text
Q: <só se o veredito depende do humano>
RECOMENDO: <opção>, <1 linha>
(ok / outra?)
```

Barra de Approve: saúde do código + convenção do repo. Não bloquear gosto. No Express, julgue só rastreabilidade mais visual, incluindo acessibilidade afetada. Segurança e banco só abrem se o diff tocar essas superfícies.

## 3. Checkpoint, review final e prova proporcional

A review é um processo cético e investigativo. Não confie cegamente em checkboxes nem em logs passados. Escolha o tipo pela fila e pelo checkpoint explícito do `plan.md`; não transforme uma revisão parcial em veredito de fase.

| Tipo | Escopo | Veredito e efeitos |
|---|---|---|
| Checkpoint | Somente as T* concluídas do marco declarado, suas provas, o contrato compartilhado ou risco que justifica a revisão. Registre as T* que continuam abertas. | A etapa pode concluir “Marco aprovado” ou “Request changes”. Nunca declare a feature concluída, marque Approve final, sincronize decisões, crie commit residual ou publique a phase. Com fila aberta e sem bloqueios, mantenha `# Status: rascunho` e faça handoff para `vibe-implement`. |
| Final | Fila do plan concluída; julgue critérios de aceite, código integrado e riscos que o diff alterou. | Approve só depois de comprovar a integração e fechar bloqueios. A finalização Git continua sujeita à confirmação humana explícita. |

### Selecionar e executar provas

1. Confira no `implement.md` as provas registradas por T* e compare os paths cobertos com o estado integrado. Reaproveite prova verde quando não houve edição posterior nos paths cobertos e ela continua relevante para o resultado atual.
2. Execute somente a menor prova que falta para julgar o marco ou a integração. Reexecute uma prova quando estiver ausente, falhou, ficou desatualizada por edição posterior, não cobre a integração entre tasks, ou quando um risco alterado exigir cobertura adicional.
3. Não rode automaticamente a matriz de comandos de cada T*. Na review final, prefira uma verificação agregada existente quando ela comprovar a integração; rode o Smoke Test somente quando a entrada real tiver mudado, sua prova estiver ausente/desatualizada ou for necessária para cobrir o fluxo integrado.
4. Registre em cada etapa as provas reaproveitadas, os comandos executados e o motivo. Se uma prova necessária falhar, abra `R*` `Required` com comando e remédio; não aprove silenciosamente.

Inspecione o código integrado e aplique estes pilares ao escopo da etapa:

1. **Rastreabilidade e Verificação Anti-Alucinação (Audit Trail):**
   - Cruze o pedido (`interview.md` quando houver), os critérios `A*`/`C*` e o `plan.md`. No checkpoint, julgue só o marco declarado; no final, confirme que as tasks concluídas produziram a integração pedida.
   - Inspecione os paths e o fluxo real que comprovam esse escopo. T* marcada sem código correspondente vira `R*` `gap: missing` (`Critical`).
2. **Provas e Integridade dos Testes:**
   - Cace falsos positivos: testes sem asserções reais, testes que dão `assert True`, testes que apenas testam mocks sem exercitar a implementação real.
   - Verifique casos de borda e caminhos de erro relevantes às superfícies alteradas. Use a seleção de provas acima; não repita suites de T* sem lacuna ou risco que o justifique.
   - Se uma prova necessária falhar ou for falso positivo: registre `R*` `Required`.
3. **Auditoria Implacável de Segurança e Hardening:**
   - Nas superfícies tocadas pelo diff, inspecione entradas externas, formulários, parâmetros de URL e bodies de request (`references/security-and-hardening.md`):
     - Há risco de Injeção (SQL, XSS, Command/Shell Injection, SSRF)?
     - Há limite de caracteres e tamanho de payload para prevenir DoS e travamentos?
     - IDOR: o servidor valida se o usuário autenticado tem permissão sobre o recurso manipulado?
     - Há segredos, chaves ou tokens expostos no código, no bundle do frontend ou gravados em logs?
   - Toda brecha explorável vira `R*` `Critical`. Falta de limite/validação de borda vira `R*` `Required`.
4. **Inspeção Visual e Interface:**
   - Se o diff tocar interface de usuário web, selecione nesta ordem, conforme `references/ui-visual-quality.md`: navegador integrado (`@Browser` ou equivalente) primeiro quando disponível, MCP Server `chrome-devtools` para snapshot, screenshot, DOM, estilos, console, rede e assets, ou Playwright somente se já existir no repositório ou for solicitado para fluxos repetíveis e assertions.
   - Registre rota, viewport, estado, ações e evidência observada. Use a checklist da referência para conferir overflow, conteúdo fora da viewport, clipping, sobreposição ou cobertura, z-index, truncamento ou quebra, proporção de largura, controles excessivos, input e ícone inline, viewport estreita, estados loading/empty/error/success, foco, teclado, contraste e console/rede/assets.
   - Para ações compactas, aceite `icon-only` somente quando a ação for universalmente reconhecível, como lixeira para apagar, com nome acessível, área de interação adequada, foco visível e tooltip quando aplicável. Ações ambíguas continuam com texto.
   - Sem capacidade visual ou sem evidência renderizada, abra `R*` `Required`; não aprove silenciosamente e não instale ferramenta automaticamente.
5. **Simplificação e Qualidade de Código:**
   - Inspecione se o código é o mínimo necessário (YAGNI, sem estruturas especulativas, sem duplicação de lógica ou componentes).
   - Verifique se todas as funções criadas ou modificadas possuem comentários semânticos obrigatórios.
   - Decisões críticas: cruze interview, spec, plan e analyze. Decisão desrespeitada ou conflito aberto bloqueia Approve.
6. **Auditoria de Banco de Dados, Migrations e Precisão Numérica:**
   - Se o diff tocar persistência ou valores numéricos/monetários (`references/database-and-migrations.md`):
     - Valores monetários, taxas ou cálculos exatos usam `FLOAT`/`REAL` em vez de `DECIMAL`/`NUMERIC`? Vira `R*` `Critical`.
     - Há queries com risco de SQL Injection ou interpolação não parametrizada? Vira `R*` `Critical`.
     - Há migrations destrutivas (`DROP COLUMN`, `DROP TABLE`) sem plano de rollback e autorização humana? Vira `R*` `Critical`.
     - Há colunas de Foreign Key sem índice explícito ou queries N+1 em loops? Vira `R*` `Required`.
     - Há `SELECT *` desnecessário em código de produção ou paginação por `OFFSET` massivo? Vira `R*` `Required`.

Finding: evidência (`path`) + severidade + remédio nomeado + prova. Sem evidência concreta não entra. Achado novo = próximo `R*` livre. Não renumerar fechados.

| Prefixo | Bloqueia Approve? |
|---|---|
| Critical / Required | Sim |
| Nit / Optional / FYI | Não |

Remédio aponta `vibe-implement` + o que fazer. Esta skill **não** aplica código.

## 4. Escrever e salvar já

Molde: `templates/review.md`. Uma casa por fato. Omita seção que esta etapa não precisa.

| Campo | Abre | Fecha / some |
|---|---|---|
| Tipo de review | Toda etapa | Registre checkpoint ou final e, no checkpoint, a referência exata do marco no plan |
| Cobertura | Há `spec.md` | Sem spec: omitir |
| R* | Achado com path + evidência | `[x]` quando implement provou. Lista vazia some. Sem bloqueio: “nenhum bloqueio” |
| Provas | Toda etapa | Liste provas reaproveitadas, executadas e o motivo; N/A só quando não há prova aplicável |
| Visual | Diff desta etapa toca UI | Sem UI: omitir |
| Segurança | Diff toca superfície listada no §3 | Sem isso: omitir |
| DoD / Notas | Há o que aplicar ou anotar | Vazio / N/A: omitir |
| Etapa N | Toda run desta skill no pedido | Etapa antiga **não** apaga |

Status: `rascunho` durante checkpoints e enquanto o veredito final aguarda confirmação; `request-changes` enquanto houver R* bloqueante em `[ ]`; `aprovado` somente após Approve final, fila concluída e confirmação humana.

Não pergunte se pode salvar. Não cole o corpo no chat.

**Etapa 1 (não há `review.md`):** execute o apply para preparar o `review.md` vivo e escreva nele diretamente (§0). Registre o tipo e o escopo antes de julgar.

**Etapa 2+ (já há `review.md`):** edite o vivo diretamente. Acrescente `### Etapa N` e atualize checklist e provas sem substituir o histórico. Só a review final atualiza o veredito vigente para Approve; checkpoint registra o resultado do marco na própria etapa.

### Resposta no chat

Responda, **só**:

```text
Review gravada: <created.path>/review.md

- Etapa: <N> · Tipo: checkpoint | final · Resultado: Marco aprovado | Request changes | Approve final | Approve com defer
- Fila: <T* restantes | concluída>
- Abriu: <R* ou nenhum>
- Fechou: <R* ou nenhum>
- Handoff: vibe-implement | volta vibe-spec | finalização Git da phase

Arquivo disponível em <created.path>/review.md. Em checkpoint, a fase continua aberta; na review final, responda "aprovado" para sincronizar decisões e encerrar, ou indique os ajustes desejados.
```



## 5. Fechar

Commitável: o `review.md` vivo e, somente no fechamento final aprovado, os artefatos residuais autorizados da phase. Checkpoint não cria commit residual nem publica a phase. O inventário é transitório no stdout. Request changes → handoff `vibe-implement` (arquivo + R* em `[ ]`), com recomendação de novo chat focado na correção. Se o usuário pedir para corrigir imediatamente, inicia `vibe-implement`. Continuar no mesmo chat é permitido somente por escolha consciente do humano; o `review.md` e o diff são a ponte.
Approve final sem R* bloqueantes em `[ ]` ainda é proposta até o humano ler e confirmar.

Após aprovação humana explícita da review final, com a fila concluída:

1. Marque `# Status: aprovado`, o veredito Approve e a aprovação humana no `review.md` vivo.
2. Se **Decisões para vigência** estiver vazia, feche a cadeia sem tocar regras.
3. Se houver linhas, aplique patch mínimo em `.vibeflow/REGRAS.md`. Crie ou atualize uma única seção `## Decisões vigentes` com tabela `ID | Decisão vigente | Fonte`. Atualize por ID, preserve linhas não citadas e use como fonte o review aprovado do alvo.
4. Não copie justificativa, histórico ou impacto para as regras. Eles permanecem nos artefatos.
5. Releia `REGRAS.md` e confirme que apenas os IDs aprovados mudaram. Review rascunho, Request changes ou Approve sem confirmação humana nunca autoriza sync.

### Finalização Git da phase

Esta seção só se aplica à review final, depois da aprovação humana explícita, com todas as T* concluídas e sem Critical ou Required em `[ ]`. Checkpoint nunca abre finalização Git.

1. Execute a prova final necessária para a integração conforme §3, sem repetir automaticamente a matriz de cada T*. Execute `git diff --check` e gitleaks quando previsto pelo repositório.
2. Compare o estado atual com o snapshot da review. Se houver path fora da phase, das decisões aprovadas ou da correção registrada, pare e peça isolamento; não misture trabalho pré-existente.
3. Adicione somente os paths residuais autorizados, com `git add -- path/da/phase .vibeflow/REGRAS.md` quando a sincronização foi aprovada. Nunca use `git add -A` ou `git add .`.
4. Valide `git diff --cached --check` e a lista de paths. Crie `chore(phase-N): finalize review` sem `Co-Authored-By` quando houver mudanças residuais. Não crie commit vazio; se não houver residual, o último commit da task é o HEAD da phase.
5. Execute `git push` para o upstream do branch atual, sem `--force`. Ausência de upstream, falha de commit ou falha de push mantém o handoff bloqueado e precisa ser informada com a causa segura.
6. Registre no `review.md` e no chat o hash do commit final ou o HEAD já existente, o resultado do push e os paths enviados. O inventário é JSON transitório no stdout.
