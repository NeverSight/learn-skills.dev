---
name: skill-router
description: "Chamada só via /skill-router, quando o usuário pergunta QUAL skill resolve um pedido ('qual skill uso pra isso?', 'tem skill pra X?'). Procura primeiro nas skills e agentes do azvd-toolkit e depois nas skills instaladas no ambiente, e aponta a melhor — não executa a tarefa."
trigger: /skill-router
disable-model-invocation: true
---

# Skill Router — qual skill resolve isso

Papel único: dado um pedido, **apontar** a skill (ou agente) que resolve. Não executa, não encadeia —
encadear é do `orchestrator`. Só roda quando chamado via `/skill-router`.

## Ordem de busca

1. **Skills e agentes do azvd-toolkit** (tabela abaixo). Achou → aponte e pare.
2. **Skills instaladas no ambiente.** Use a lista de skills que o host expõe na sessão; se não houver,
   liste os diretórios de skills do host (ex.: `~/.claude/skills/`, `~/.agents/skills/`, a pasta de
   plugins do agente em uso). Escolha pela `description` de cada uma.
3. **Nada encaixa** → diga isso e pergunte ao usuário. Nunca invente skill.

| Pedido | Aponte para |
|---|---|
| montar/refinar um prompt para uma IA | `prompt-forge` |
| blocos de prompt prontos, ou guardar uma lição como bloco | `prompt-blocks` |
| tarefa que precisa de várias skills ou de sub-agentes (construir + criticar + julgar) | `orchestrator` |
| mapear código/docs em grafo, ou desenhar task graph | `graph-engineering` |
| "aprendi algo", "lembra disso", lição da sessão | `self-learning` |
| conferir um pedido/plano antes de construir (precisa? já existe? critério de aceite) | agente `verificador-previo` |
| implementar um item com escopo fechado | agente `construtor` |
| avaliar uma entrega contra uma régua (nota + defeitos) | agente `critico` |
| decidir entre versões / julgar o conjunto inteiro | agente `juiz` |
| conferir número ou afirmação contra a fonte (banco, API, planilha) | agente `conferidor-dados` |
| conferir algo numa tela de sistema de terceiros (só olhar) | agente `conferidor-tela` |
| testar a sua aplicação: fluxos, erros, acessibilidade, visual, marcas de IA | agente `testador-web` |
| revisar mudança de query SQL (plano, índice, resultado) | agente `revisor-query` |
| qual modelo e nível de esforço usar em cada agente/papel; vale sub-agente?; reduzir custo de tokens | `orchestrator` §2 → bloco `prompt-blocks/blocks/b11-roteamento-modelos.md` (e `b13-orcamento-tokens.md` para medir) |
| classificar, filtrar ou ranquear muitos itens (≥ 20) gastando pouco | agente `triador` (regra: bloco `b11-roteamento-modelos.md`, pergunta 1) |
| acrescentar item novo num loop de construção que já roda | bloco `b12-gauntlet-loop.md`, seção "Item novo no meio do loop" |

## Regras

- **Dedupe:** se a mesma skill existe no toolkit e no ambiente, use a do toolkit (é a fonte).
- **Instalar algo novo** (`npx skills add`, `git clone`): só com permissão do usuário. Listar é seguro.
- **Resposta curta:** a skill ou agente, uma linha de porquê, e como chamar.

## Skills relacionadas

- `orchestrator` — quando a resposta é "precisa de mais de uma peça".
- `self-learning` — rota nova descoberta (pedido → skill) entra na tabela acima.
