---
name: openrouter-img
description: >-
  Generate or edit images via OpenRouter Image API across top models (Nano
  Banana, GPT Image, FLUX.2, Seedream, Qwen, Grok). Use when the user mentions
  openrouter-img, OpenRouter image gen, or wants to pick among top image models.
disable-model-invocation: true
---

# OpenRouter Img

Gera imagens pela **Image API** do OpenRouter (`POST /api/v1/images`). Chave: `OPENROUTER_API_KEY` (cwd `.env` ou `~/.env`).

## Uso

```bash
# Listar top 10 + preços ao vivo do endpoint
uv run ~/.agents/skills/openrouter-img/scripts/generate_image.py --list --top

# Gerar
uv run ~/.agents/skills/openrouter-img/scripts/generate_image.py \
  --prompt "..." --filename "yyyy-mm-dd-hh-mm-ss-name.png" \
  --model flash --resolution 1K --aspect-ratio 16:9
```

Aliases de `--model`: ver tabela abaixo — ou o slug completo.

Default: `flash` @ `1K` / `16:9`. Só subir resolução se o usuário pedir. Rodar no cwd do usuário. **Não** ler a imagem de volta — informar path (+ `usage.cost` se vier).

Edição: `--input-image path.png` + prompt de edição.

## Modelos empregados (top 10)

| # | Alias | Nome | Slug OpenRouter |
|---|-------|------|-----------------|
| 1 | `pro` / `nb-pro` | Nano Banana Pro (Gemini 3 Pro Image) | `google/gemini-3-pro-image` |
| 2 | `gpt` / `gpt2` | GPT Image 2 | `openai/gpt-image-2` |
| 3 | `flux-max` | FLUX.2 Max | `black-forest-labs/flux.2-max` |
| 4 | `flux` | FLUX.2 Pro | `black-forest-labs/flux.2-pro` |
| 5 | `seedream-pro` | Seedream 5.0 Pro | `bytedance-seed/seedream-5-0-pro` |
| 6 | `seedream` | Seedream 5.0 Lite | `bytedance-seed/seedream-5-0-lite` |
| 7 | `flash` / `nb-flash` | Nano Banana 2 (Gemini 3.1 Flash Image) | `google/gemini-3.1-flash-image` |
| 8 | `qwen` | Qwen Image 3 Pro | `qwen/qwen-image-3-pro` |
| 9 | `grok` | Grok Imagine Image 2.0 | `x-ai/grok-imagine-image-2.0` |
| 10 | `seedream-4.5` | Seedream 4.5 | `bytedance-seed/seedream-4.5` |

## Tabela de custo (consulta)

Valores OpenRouter (snapshot ago/2026). Atualizar com `--list --top`. O response `usage.cost` é a verdade da cobrança.

| Alias | 512 | 1K | 2K | 4K / outro | Unidade |
|-------|----:|---:|---:|------------|---------|
| `flash` | ~$0.045 | ~$0.067 | ~$0.101 | ~$0.151 @4K | token → $/img estimado |
| `pro` | — | ~$0.134 | ~$0.134 | — (sem 4K neste endpoint) | token → $/img estimado |
| `seedream` | — | — | $0.035 | $0.035 @4K | $/imagem fixo |
| `seedream-pro` | — | $0.045 | $0.045 | $0.09 high-res | $/imagem |
| `seedream-4.5` | — | $0.04 | $0.04 | $0.04 | $/imagem |
| `qwen` | — | $0.04 | $0.075 | — | $/imagem |
| `grok` | — | $0.04–0.06 | $0.06–0.08 | — | $/imagem (low/medium) |
| `flux` | — | ~$0.03 | ~$0.12* | — | $0.03 / megapixel |
| `flux-max` | — | ~$0.07 | ~$0.28* | — | $0.07 / megapixel |
| `gpt2` | — | ver `usage.cost` | ver `usage.cost` | — | token (input+output) |

\*Estimativa 2K ≈ 4 MP (2048²); o custo real depende dos pixels gerados.

Resoluções “—” = não listadas / não suportadas nesse endpoint. Se a API rejeitar, mudar `--resolution`.

## Escolha rápida

- UI/mock com texto → `pro` ou `flash`
- Volume barato → `flash`@512, `seedream`, `flux`
- Fotorrealismo / arte → `flux-max`, `seedream-pro`, `gpt2`
