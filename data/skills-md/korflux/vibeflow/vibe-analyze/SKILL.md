---
name: vibe-analyze
description: >
  Cruza interview, spec e plan do mesmo alvo e grava em `.vibeflow/phases/phase-N-slug/analyze.md` ou `.vibeflow/mvp/analyze.md`. Use when the user runs /vibe-analyze, pede análise cruzada, consistência, cobertura, gaps, contradição entre artefatos, clarify depois do plan, ou a rota é max com plan em disco, mesmo que não diga vibe-analyze.
---

# vibe-analyze

Não invente `n`, slug ou path. Sem plan no alvo, não há analyze. Sem `.vibeflow/`, pare e mande `/vibe-init`.
Erros óbvios e lacunas determinísticas identificados no cruzamento devem ser corrigidos diretamente nos artefatos (`spec.md`, `design.md` ou `plan.md`). Ambiguidades reais de negócio ou arquitetura devem ser esclarecidas com o usuário via chat.
Não atualize decisões vigentes nem `REGRAS.md`. No MVP, conflito crítico sem `substitui` explícito bloqueia a implementação.

A investigação começa pela pergunta de consistência que precisa ser respondida. Use `rg --files` para localizar interview, spec, plan, analyze, regras e paths citados; use `rg -n` para localizar A*/C*, T*, IDs, símbolos e comandos. Abra somente as entradas e dependências que sustentam o cruzamento e expanda a leitura quando uma lacuna bloquear a prova. O inventário é mapa de seleção, não autorização para ler a árvore inteira.

## 0. Entender e usar o script

1. Resolva o diretório desta skill e leia o motor que vai executar: `scripts/analyze.ps1` no Windows ou `scripts/analyze.py` no fluxo Unix. Entenda alvo, predecessores, recusas, preparação do destino e preservação do arquivo vivo antes de chamá-lo. Se encontrar defeito, corrija o motor e prove o contrato antes de continuar.
2. No cwd do repo:
   - Windows: `pwsh "<skill>/scripts/analyze.ps1"`.
   - Unix: `bash "<skill>/scripts/analyze.sh"`.
   - Alvo MVP: acrescente `-Mvp` ou `--mvp`.
3. Leia o JSON operacional emitido no stdout pelo comando acima. Use `rg --files` e `rg -n` para localizar `spec.md` e `plan.md` (obrigatórios), `interview.md` se houver, `analyze.md`, `.vibeflow/REGRAS.md` e os paths de código necessários. Abra somente os arquivos que sustentam o cruzamento, não a árvore inteira.

Erros determinísticos previstos: `INIT_AUSENTE` exige `/vibe-init`. `ANALYZE_SEM_PLAN` exige plan. `ANALYZE_SEM_SPEC`, `ANALYZE_SEM_INTERVIEW`, `MVP_INESPERADO`, `MODO_INVALIDO` e `FASE_AUSENTE` exigem diagnosticar a causa e não devem ser contornados.

## 1. Abrir

Declare em cerca de cinco linhas: rota, modo, alvo, plan, interview e estado do artefato vivo.

```text
modo: reuse · alvo: phase-1-lock-bloco · plan: sim · interview: sim · artefato vivo: presente
```

- `modo_sugerido=criar`: não há pasta com plan. Não invente fase; mande `/vibe-plan`.
- No MVP, interview, spec e plan são obrigatórios no alvo especial e o plan precisa estar aprovado.

## 2. Gate

| Sinal | Ação |
|---|---|
| Typo ou uma linha óbvia | Não usar analyze |
| Sem `plan.md` no alvo | Parar. Encaminhar para `/vibe-plan` |
| Destino sem `spec.md` | Parar. Não contornar `ANALYZE_SEM_SPEC` |
| Plan `# Status: rascunho` e o humano pediu analyze | Alterar o plan para `aprovado` diretamente no arquivo (1 linha no chat) e seguir |
| Plan rascunho sem pedido de analyze | Parar. Pedir leitura do plan |
| Intenção, sucesso ou limites frouxos de verdade | Devolver para `vibe-interview` ou `vibe-spec`. Não "completar" no chute |
| Dúvida de arquitetura ou regra aberta | Perguntar diretamente ao usuário via chat (Q + RECOMENDO) |

```text
Q: <decisão ou clarificação necessária>
RECOMENDO: <opção>, <1 linha explicando motivo e impacto>
(ok / outra?)
```

## 3. Varredura, Correção e Auditoria de Qualidade

Leia `references/coverage.md` como mapa interno. Não copie a taxonomia no chat.

Audite, cruze e resolva:

1. **Interview → spec:** Resultado da interview (o quê, sucesso, fora) contra Objetivo, A*/C* e Fora da spec.
2. **Spec → plan:** Cada A*/C* possui T* correspondente no campo `Spec:`; cada T* referencia A*/C* ou é infraestrutura justificada.
3. **Plan → spec:** Nenhuma T* inventa comportamento, caminhos ou módulos fora do escopo aprovado.
4. **Design condicional (com UI visível):** Cruza `design.md` além de interview, spec e plan. Com UI visível, design ausente ou não aprovado bloqueia o veredito limpo. Sem UI visível, registra N/A explícito em vez de bloqueio.
5. **Qualidade dos Testes e Executabilidade:**
   - Cada T* tem comando executável de prova? Se a task criar ou alterar um ponto de entrada executável, a prova dessa mesma T* inclui o smoke test real. Não exija uma T1 de baseline para entregas sem ponto de entrada.
   - As tasks possuem comandos reais de teste no repositório? Se houver verificação puramente manual sem comando, converta para comando executável real no `plan.md`.
   - Confira apenas ferramentas exigidas pelas provas escolhidas, como `gitleaks` ou MCP `chrome-devtools`. Resolva preparo local simples quando disponível e autorizado; só proponha T* para setup persistente que faça parte da entrega do projeto. Registre bloqueio externo sem criar task artificial de instalação.
6. **Decisões Críticas (MVP):** Cruze cada ID entre interview, spec e plan. Se houver divergência sem declaração de `substitui` ou ID órfão, ajuste a consistência nos artefatos ou pergunte ao usuário se for mudança intencional.
7. **Conformidade com REGRAS.md:** Violação de regras mandatórias (segurança, auth, dados, segredos, CSP) = aplicar patch corretivo imediato nos artefatos.
8. **Passes de Consistência:** Duplicação, ambiguidade de adjetivos, furos de aceite e inconsistências de termos = aplicar correção direta.

Para cada ajuste aplicado diretamente em `spec.md`, `design.md` ou `plan.md`, registre a entrada na seção **Achados e Resoluções** do `analyze.md`.
Gravidade: `CRITICAL` · `HIGH` · `MEDIUM` · `LOW`. IDs: `F1`, `F2`... na ordem da tabela.

## 4. Clarificações

Quando houver ambiguidade que não seja um erro óbvio e dependa de decisão humana:
- Pergunte diretamente no chat (Q + RECOMENDO), uma por vez.
- Aplique a resposta do usuário no arquivo correspondente (`spec.md`, `design.md` ou `plan.md`).
- Registre o resumo da pergunta e resposta na seção **Clarificações com o Usuário** do `analyze.md`.
- Não há limite arbitrário de perguntas; pergunte o que for estritamente necessário para eliminar ambiguidades.

## 5. Escrever e Salvar

Artefato vivo: `<created.path>/analyze.md`. Molde: `templates/analyze.md`. Mantenha `# Status: rascunho` enquanto a análise estiver em elaboração.
Não pergunte se pode salvar e não cole o corpo do documento no chat.

1. Execute o apply. Ele prepara o arquivo vivo somente quando ausente e preserva bytes quando ele já existe.
2. Escreva ou atualize diretamente o arquivo vivo, certificando a cobertura, os achados corrigidos e a consistência final.
   Veredito: `limpo` quando todas as correções forem aplicadas e o plano estiver validado para execução; `bloqueado` apenas se restar conflito crítico não resolvido.
3. Execute ou registre a prova final conforme os comandos do repositório:
   - Modo phase:
     `pwsh "<skill>/scripts/analyze.ps1" -Apply`
     `bash "<skill>/scripts/analyze.sh" --apply`
   - Modo MVP:
     `pwsh "<skill>/scripts/analyze.ps1" -Apply -Mvp`
     `bash "<skill>/scripts/analyze.sh" --apply --mvp`
4. Responda no chat apenas:

```text
Analyze gravado: <created.path>/analyze.md

- Veredito: limpo | bloqueado
- Cobertura: <A*/C* com T* / total>
- Qualidade de testes: <provas executáveis proporcionais; smoke do ponto de entrada na T* que o entrega; ferramentas ou limitações registradas>
- Correções aplicadas: <F1... no spec.md / design.md / plan.md ou nenhuma necessária>
- Handoff: vibe-implement

Arquivo disponível em <created.path>/analyze.md. Responda "aprovado" para confirmar, "pode ir pro implement" (ou "pode ir para a próxima fase") para avançar imediatamente, ou indique os ajustes desejados.
```

## 6. Ajuste ou Aprovação

| Resposta | Ação |
|---|---|
| Aprovado (sem pedir implementação) | `# Status: aprovado` no vivo **apenas se** veredito `limpo`; parar e aguardar próximo comando |
| "Pode ir pro implement" / "pode ir para a próxima fase" / pede código | `# Status: aprovado` no vivo **apenas se** veredito `limpo`; iniciar imediatamente `vibe-implement` |
| Pedido de alteração | Patch direto no arquivo vivo; até 5 bullets no chat; solicitar nova conferência |
| "Parece bom" sem pedir implementação | Perguntar: "Aprovado no arquivo ou deseja algum ajuste?" |
| Veredito `bloqueado` e usuário pede implementação | Recusar. Exibir os achados bloqueantes pendentes |
| Spec, design, plan ou intenção quebrou | Devolver para a skill responsável. Não forçar implementação |

Rascunho sem "aprovado" e sem pedido da próxima porta não autoriza iniciar o código.

## 7. Fechar

Não commite no git. Não dispare a próxima skill a menos que o usuário tenha pedido explicitamente para avançar (§6).
Informe que o JSON do inventário foi consumido do stdout e não gerou arquivo persistido; os arquivos vivos atualizados entram no git. Recomende abrir um novo chat para `vibe-implement`; continuar no mesmo chat é permitido somente por escolha consciente do humano. O `analyze.md` e os artefatos vivos são a ponte entre chats.
Handoff registrado no arquivo: `vibe-implement`. Zero implementação nesta execução.
