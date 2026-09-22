---
name: agents-dev
description: "Modo desenvolvedor do fazer.ai agents: trabalhar no código-fonte. Clona o repo (Free público ou Pro via git proxy do hub), orienta nas boas práticas e invariantes (separação Free/Full, aditividade e convenções de docs/), pergunta proativamente o que o usuário quer implementar e conduz a implementação, e ajuda a gerar a própria imagem de deploy. Use quando o usuário quer DESENVOLVER, estender ou contribuir com o código do fazer.ai agents, não apenas subir (onboarding) ou operar (operação) uma instância."
---

# Modo desenvolvedor do fazer.ai agents

Leva um desenvolvedor de "quero mexer no código" até "implementou com as boas práticas do projeto e, se quiser, gerou a própria imagem". Audiência: **desenvolvedor**, não operador. Para subir uma instância do zero use a skill `agents-onboarding`; para debugar/ajustar uma instância em produção use `agents-operation`.

## ⚠️ Distribuição: o Pro é privado

- O **repositório Pro/Full** (`fazer-ai/agents-pro`) e a **imagem Pro** são **privados**. **Nunca** publique o código, a imagem, ou trechos exclusivos do Full em local público (gist, fork público, registry público, post, screenshot).
- O acesso ao Pro é concedido individualmente. Vazar repo/imagem quebra esse modelo.
- **Sugestões e contribuições vão para o repositório Free** (open-source): `fazer-ai/agents`. Abra issues/PRs lá.

## Fluxo

1. **Obter o código** (`references/00-get-the-code.md`), bifurca por edição: Free clona o repo público (sem credencial); Pro clona via git proxy do hub (credencial per-user).
2. **Layout + porta de qualidade** (`references/01-layout-and-bun-check.md`): mapa do repo, `bun install`/`bun dev`, o ciclo `bun check`.
3. **Aditividade + invariantes** (`references/02-free-full-and-invariants.md`): aditividade e onde estão as convenções e os docs por subsistema.
4. **Implementação conduzida** (`references/03-implement.md`): perguntar o que implementar, desenhar desafiando premissas, implementar no estilo vizinho, validar.
5. **Imagem própria + deploy** (`references/04-own-image-and-deploy.md`): gerar a própria imagem e plugá-la num deploy (casa com o Tier C da `agents-onboarding`).

## Guardrails

Ver `guardrails.md` (Pro privado, segredos fora do repo, `bun check` verde) e `gotchas.md` (armadilhas de DB/RLS/CSP).

## Skills irmãs

- `agents-onboarding`: subir uma instância nova num VPS (do zero ao agente).
- `agents-operation`: debugar/ajustar uma instância **em produção**.

## Pendências

- **Wording de não-redistribuição (Pro):** é conteúdo público-facing; confirmar a redação com a revisão de licenciamento.
