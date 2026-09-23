---
name: vibe-design
description: >
  Desenha a apresentação de fluxos aprovados e grava em `.vibeflow/phases/phase-N-slug/design.md` ou `.vibeflow/mvp/design.md`.
  Use when the user runs /vibe-design, pede design, desenho de tela, layout, tokens, corrigir UI, analisar UI existente,
  ou a rota tem UI visível com spec aprovada, mesmo que não diga vibe-design.
---

# vibe-design

Não invente `n`, slug ou path. Sem spec aprovada no alvo, não há design. Sem `.vibeflow/`, pare e mande `/vibe-init`.
Não edite source, teste ou lockfile nesta skill. Não gere imagem final. Open Questions no arquivo é defeito.

A investigação começa pela pergunta de apresentação que a spec deixou aberta. Use `rg --files` para localizar `spec.md`, `interview.md`, DS, DESIGN.md e referências de leitura; use `rg -n` para localizar telas, componentes, tokens, decisões e símbolos. Abra somente os paths que sustentam o desenho e expanda a leitura quando uma lacuna bloquear a prova. O inventário é mapa de seleção, não autorização para ler a árvore inteira.

## 0. Entender e usar o script

1. Resolva o diretório desta skill e leia o motor que vai executar: `scripts/design.ps1` no Windows ou `scripts/design.py` no fluxo Unix. Entenda seleção de alvo, recusas, preparação do destino e preservação do arquivo vivo antes de chamá-lo. Se encontrar defeito, corrija o motor e prove o contrato antes de continuar.
2. No cwd do repo:
   - Windows: `pwsh "<skill>/scripts/design.ps1"`.
   - Unix: `bash "<skill>/scripts/design.sh"`.
   - Alvo MVP: acrescente `-Mvp` ou `--mvp`.
3. Leia o JSON operacional emitido no stdout pelo comando acima. Use `rg --files` e `rg -n` para localizar `spec.md` (obrigatória), `interview.md` se houver, `design.md` e `.vibeflow/REGRAS.md`, além das referências de leitura citadas. Abra somente as entradas e dependências do fluxo, não a árvore inteira.

Erros determinísticos previstos: `INIT_AUSENTE` exige `/vibe-init`. `DESIGN_SEM_SPEC` exige spec prévia. `DESIGN_JA_PLANEJADO` exige outra phase. `DESIGN_SEM_ALVO`, `PHASES_INESPERADO`, `MVP_INESPERADO`, `FASE_AUSENTE`, `FASE_EXISTE`, `SLUG_INVALIDO` e `MODO_INVALIDO` exigem diagnosticar a causa e não devem ser contornados.

## 1. Abrir

Declare em cerca de cinco linhas: modo de entrada, uso, alvo, spec e estado do artefato vivo.

```text
modo: com referência · uso: criar · alvo: phase-1-lock-bloco · spec: sim · spec-status: aprovado · artefato vivo: presente
```

- `modo_sugerido=reuse`: existe spec sem design. Use o alvo indicado sem criar pasta.
- `modo_sugerido=criar`: não há spec sem design. Não invente fase; mande `/vibe-spec`.
- `rota=mvp`: alvo fixo `.vibeflow/mvp`, sem `--slug` e sem `--dir`; a spec precisa estar aprovada.

## 2. Gate

| Sinal | Ação |
|---|---|
| Typo, rename ou ajuste de uma linha sem tela | Não usar design |
| Sem `spec.md` no alvo | Parar. Encaminhar para `/vibe-spec` |
| Spec `# Status: rascunho` e o humano pediu a design | Alterar a spec para `aprovado` diretamente no arquivo (1 linha no chat) e seguir |
| Spec rascunho sem pedido de design | Parar. Pedir leitura e aprovação da spec |
| `plan.md` já existente no alvo | Não sobrescrever. Pedido novo exige outra phase |
| Sem UI visível ao usuário | Registrar N/A explícito. Não gravar `design.md` como bloqueio |
| Intenção, fluxo ou aceite frouxos | Devolver para `vibe-spec`. Não completar no chute |
| Dúvida pontual de apresentação | Resolver via chat (Q + RECOMENDO) |

```text
Q: <decisão que trava o desenho>
RECOMENDO: <opção>, <1 linha explicando o porquê e impacto>
(ok / outra?)
```

## 3. Modos de entrada

Leia `references/modos-entrada.md` quando a origem do desenho estiver em jogo. Não copie o catálogo no chat.

| Modo | Quando | Registro no vivo |
|---|---|---|
| Com referência | Existe DS, DESIGN.md ou Figma como leitura | Lista o reusado e o adaptado com motivo, sem copiar a fonte para o repo |
| Greenfield | Sem referência aproveitável | Cria o kit mínimo primeiro, depois mapeia cada tela da spec sobre o kit |

Sem referência, não improvise DS externo. Com referência, primitivo novo na página com DS existente é defeito.

## 4. Usos

Leia `references/kit-e-tokens.md` quando faltar forma de kit, token, ícone, responsivo, estado ou prova. Leia `references/motion.md` quando a tela tiver motion ou alvo mobile. Os três usos gravam no mesmo vivo, sem código.

| Uso | Entrada | Saída no vivo |
|---|---|---|
| Criar | Spec aprovada com F e telas | Inventário de telas e disposição técnica por tela sobre o kit |
| Corrigir | R da review com path e evidência | Ajuste da tela citada com motivo, sem reescrever o arquivo inteiro |
| Analisar | UI existente mais spec | Parecer por tela contra o contrato, com lacunas e próximos passos |

Design não cria comportamento novo. Spec e plan não inventam token. Ações ambíguas mantêm texto, com regra de ícone explícita por tela.

## 5. Escrever e salvar

Artefato vivo: `<created.path>/design.md`. Molde: `templates/design.md`. Mantenha `# Status: rascunho` enquanto o desenho estiver em elaboração.
Não pergunte se pode salvar e não cole o corpo do documento no chat.

1. Execute o apply. Ele prepara o arquivo vivo somente quando ausente e preserva bytes quando ele já existe:
   - Modo phase:
     `pwsh "<skill>/scripts/design.ps1" -Apply`
     `bash "<skill>/scripts/design.sh" --apply`
   - Com `--dir`:
     `pwsh "<skill>/scripts/design.ps1" -Apply -Dir phase-N-slug`
     `bash "<skill>/scripts/design.sh" --apply --dir phase-N-slug`
   - Modo MVP:
     `pwsh "<skill>/scripts/design.ps1" -Apply -Mvp`
     `bash "<skill>/scripts/design.sh" --apply --mvp`
2. Escreva ou atualize diretamente o arquivo vivo. Cada tela traz hierarquia de cima para baixo, layout e grid, ordem de leitura, componente por zona, tokens, iconografia, responsivo com viewport estreita, overflow e truncamento, e estados. Registre a prova visual esperada por tela para a review conferir.
3. Responda no chat apenas:

```text
Design gravado: <created.path>/design.md

- Modo: <com referência | greenfield>
- Uso: <criar | corrigir | analisar>
- Telas: <nomes das telas cobertas>
- Handoff: vibe-plan

Arquivo disponível em <created.path>/design.md. Responda "aprovado" para confirmar, "pode ir pro plan" (ou "pode ir para a próxima fase") para avançar imediatamente, ou indique os ajustes desejados.
```

## 6. Ajuste ou aprovação

| Resposta | Ação |
|---|---|
| Aprovado (sem pedir plan) | Alterar `# Status: aprovado` diretamente no vivo; parar e aguardar próximo comando |
| "Pode ir pro plan" / "pode ir para a próxima fase" / pede `vibe-plan` | Alterar `# Status: aprovado` no vivo; iniciar imediatamente `vibe-plan` |
| Pedido de alteração | Patch direto no arquivo vivo; até 5 bullets no chat; solicitar nova conferência |
| "Parece bom" sem pedir plan | Perguntar: "Aprovado no arquivo ou deseja algum ajuste?" |
| Spec ou intenção quebrou | Devolver para `vibe-spec`. Não forçar plan |

Rascunho sem "aprovado" e sem pedido da próxima porta não autoriza iniciar o plan.

## 7. Fechar

Não commite no git nesta porta. O commit começa na `vibe-implement`, depois da prova verde de cada task. Não dispare a próxima skill a menos que o usuário tenha pedido explicitamente para avançar (§6).
Informe que o JSON do inventário foi consumido do stdout e não gerou arquivo persistido. Recomende abrir um novo chat para `vibe-plan`; continuar no mesmo chat é permitido somente por escolha consciente do humano. O `design.md` vivo e o handoff são a ponte entre chats.
Handoff normal: `vibe-plan`. Sem UI visível, o handoff da spec segue direto para `vibe-plan` com N/A explícito. `plan.md` existente bloqueia nova escrita, pedido novo exige outra phase.
