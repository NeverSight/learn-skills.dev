---
name: copy-swipe-engine
description: Generate high-converting copy for landing pages, VSLs, ads, emails, WhatsApp, and checkout pages using a curated swipe database of ~316 proven copy pieces. The database is a reference of PERSUASION TECHNIQUES and structural patterns — not a content bank by niche. A user selling software may need a supplement swipe that demonstrates excellent "objection handling with authority". The value is in the TECHNIQUE, not the niche. Use when user asks to create, rewrite, improve, or ideate copy from proven patterns; always adapt structure/persuasion devices without copying text verbatim.
---

# Copy Swipe Engine

## Inputs obrigatórios
Solicitar e confirmar antes de escrever:
- Produto/oferta
- ICP/avatar
- Objetivo (lead, venda, clique, agendamento)
- Canal/formato (LP, VSL, anúncio, email, WhatsApp, checkout)
- Nível de consciência (frio/morno/quente ou 1-5 Schwartz)
- Tom de voz da marca
- Principais objeções
- CTA principal

Se faltar dado crítico, assumir explicitamente e seguir.

## Estratégia de busca

O banco de swipes é uma referência de **técnicas de persuasão**, não um banco por nicho. Mapear os inputs do briefing para filtros de técnica:

| Situação no briefing | Técnica(s) a buscar |
|---|---|
| Público tem objeções fortes | `--technique objection-handling` |
| Precisa de credibilidade/confiança | `--technique authority,social-proof` |
| Público frio / não conhece o produto | `--technique storytelling,curiosity` |
| Fase de fechamento / decisão | `--technique urgency,guarantee,value-stacking` |
| Público cético / já tentou tudo | `--technique pain-agitation,mechanism` |
| Produto novo / precisa explicar | `--technique mechanism,before-after` |
| Precisa reduzir risco percebido | `--technique risk-reversal,guarantee` |

**Técnicas disponíveis:** authority, social-proof, storytelling, curiosity, urgency, mechanism, guarantee, pain-agitation, before-after, objection-handling, value-stacking, risk-reversal

## Fluxo de execução
1. Identificar o tipo de entrega (LP curta, LP longa, VSL, email, ad, WhatsApp, checkout).
2. Mapear o briefing para técnicas de persuasão relevantes (ver tabela acima).
3. Buscar candidatos com `scripts/search_swipes.py` usando `--technique` como filtro principal. Executar o script **a partir do diretório desta skill**.
4. Se o índice não existir, gerar com `python scripts/build_swipe_index.py` a partir do diretório desta skill.
5. Ler apenas os candidatos mais próximos (3 a 6 arquivos) para economizar contexto.
6. Extrair padrões reutilizáveis (ângulo, promessa, mecanismo, provas, CTA, ritmo).
7. Gerar variações de alto impacto (ver output por canal abaixo).
8. Montar versão final em blocos modulares.
9. Validar com `references/checklist.md`.
10. Entregar + plano de A/B test.

## Regras de ouro
- Nunca copiar frases longas literalmente do swipe.
- Usar swipe como referência estratégica de TÉCNICA, não como plágio.
- Buscar por técnica de persuasão adequada ao briefing, não por nicho do produto.
- Priorizar clareza, benefício específico e credibilidade.
- Declarar hipóteses quando dados não vierem no briefing.
- Evitar promessas ilegais, médicas absolutas, ou garantias enganosas.

## Output por canal

### LP / VSL (completo)
1. Resumo estratégico (ângulo + mecanismo + promessa)
2. 8-12 headlines
3. 3 leads/hooks
4. Copy principal por blocos: Hero, Problema/agitação, Solução/mecanismo, Provas, Oferta, Objeções + FAQ, CTA
5. 2 estruturas completas (conservadora/agressiva)
6. 3-5 testes A/B recomendados
7. Autoavaliação com checklist

### Email
1. 5 subjects
2. 3 preview texts
3. 2 corpos completos (abertura, story, oferta, CTA)
4. Sequência sugerida (se aplicável)
5. 2-3 testes A/B

### Ad (Facebook/Google/YouTube)
1. 5 hooks (primeiras 2 linhas)
2. 2 corpos curtos
3. CTA options
4. Variação por formato (imagem, carrossel, vídeo)
5. 2-3 testes A/B

### WhatsApp
1. Mensagem de abertura (gancho)
2. Corpo persuasivo curto (3-5 parágrafos)
3. CTA direto
4. Follow-up (1-2 mensagens)

### Checkout
1. Headline de reforço
2. Resumo de valor (bullet points)
3. Garantia/risk reversal
4. Urgência/escassez (se aplicável)
5. Depoimento curto

## Navegação de arquivos
- Swipe files: `swipe-files/` (organizados por autor)
- Índice buscável: `references/swipe-index.jsonl`
- Frameworks: `references/frameworks.md`
- Qualidade: `references/checklist.md`
- Templates: `assets/templates/*.md`

## Comandos úteis
Executar a partir do diretório desta skill:
```bash
# Rebuild do índice (~316 entradas deduplicadas com técnicas)
python3 scripts/build_swipe_index.py

# Buscar por técnica de persuasão (caso principal)
python3 scripts/search_swipes.py --query "prova social" --technique social-proof,authority --limit 8

# Buscar por padrão estrutural para qualquer nicho
python3 scripts/search_swipes.py --query "quebra de objeção" --technique objection-handling --limit 10

# Buscar por tipo + awareness (caso clássico)
python3 scripts/search_swipes.py --query "oferta" --type email --awareness product-aware --limit 8

# Busca aberta por tema
python3 scripts/search_swipes.py --query "urgência escassez" --limit 10

# Busca para público frio
python3 scripts/search_swipes.py --query "história transformação" --technique storytelling,curiosity --limit 8
```
