---
name: linkedin-post
description: Generate high-quality LinkedIn posts for GEO thought leadership. Use when asked to write LinkedIn content, create social media posts, or generate content about SEO/GEO topics.
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# LinkedIn Post Generator Skill

Generate high-quality LinkedIn posts for GEO thought leadership.

## Trigger
Use this skill when asked to write a LinkedIn post, or with `/linkedin-post`

## Process

### Step 1: Understand the Request
Ask if not provided:
- **Topic**: What's the main subject?
- **Pillar**: education | case_study | insight | behind_scenes
- **Context**: Any specific data, audit results, or angle?

### Step 2: Choose Structure by Pillar

#### Education Post
```
[HOOK - 1 ligne choc]

[CONTEXT - Pourquoi c'est important]

[CORE INSIGHT - 3-5 points clés]

[TAKEAWAY - Ce qu'il faut retenir]

[CTA - Question ou appel]
```

#### Case Study Post
```
[HOOK - Le résultat choc]

[DATA - Les chiffres clés]

[ANALYSIS - Ce que ça révèle]

[LESSON - L'apprentissage]

[CTA - Proposer un audit]
```

#### Insight Post
```
[HOOK - L'actualité/tendance]

[CONTEXT - Ce qui s'est passé]

[ANALYSIS - Ce que ça signifie]

[IMPLICATION - L'impact pour l'audience]

[CTA - Question ou réflexion]
```

#### Behind the Scenes Post
```
[HOOK - Story opener]

[STORY - Ce qui s'est passé]

[LESSON - Ce que j'ai appris]

[ASK - Question à l'audience]
```

### Step 3: Apply the 3 Questions Test

Before finalizing, check:

1. **VISUALIZABLE?** Can the reader "see" it?
   - ❌ "Solution innovante" → ✅ "Votre marque citée par ChatGPT"

2. **FALSIFIABLE?** Is it verifiable?
   - ❌ "Excellent service" → ✅ "Score de 67% sur Perplexity"

3. **UNIQUE?** Could a competitor say this?
   - ❌ "Expert SEO" → ✅ "J'ai audité 50 sites avec mon outil GEOTOOL"

### Step 4: Hook Bank (Use for Inspiration)

**Counterintuitive:**
- Votre SEO est parfait. Mais les IA ne vous voient pas.
- Le meilleur contenu ne suffit plus.
- Google vous adore. ChatGPT vous ignore.

**Surprising Data:**
- 23% de visibilité sur GPT-4. 67% sur Perplexity.
- 1 entreprise sur 10 apparaît dans les réponses ChatGPT.

**Question:**
- ChatGPT recommande-t-il votre marque ?
- Savez-vous ce que les IA disent de vous ?

**Bold Claim:**
- Le SEO tel que vous le connaissez est mort.
- Si les IA ne vous citent pas, vous n'existez plus.

**Story Opener:**
- J'ai audité la visibilité IA d'un client. Le résultat m'a choqué.
- La semaine dernière, j'ai fait 5 audits gratuits.

### Step 5: Format Rules

- **Language**: French, professional but accessible
- **Length**: 150-250 words
- **Paragraphs**: 1-2 lines max
- **Line breaks**: Use liberally for readability
- **Emojis**: 1-2 max if really relevant (not required)
- **Hashtags**: 3-5 at the end (optional)
- **CTA**: Always end with question or call to action

### Step 6: Output

Provide the post directly, ready to copy-paste to LinkedIn.
No introduction, no "Here's your post:", just the content.

---

## Example Output

```
Votre site est invisible pour ChatGPT.

Et ce n'est pas un problème de SEO.

C'est un problème de GEO.

Voici 3 raisons :

1. Les LLMs ne crawlent pas comme Google
→ Ils utilisent des bases de connaissances pré-entraînées

2. Le format compte plus que les mots-clés
→ Structure claire, données factuelles, sources citables

3. L'autorité se mesure différemment
→ Pas de PageRank, mais des citations croisées

Ce que ça change pour vous :

Un bon classement Google ≠ visibilité IA.

Il faut optimiser pour les deux.

Vous avez déjà vérifié si ChatGPT recommande votre marque ?

#GEO #IA #SEO #Marketing
```

---

## Integration with GEOTOOL

If user provides audit data, use real numbers:
- Global score
- Scores by model (GPT-4o, Claude, Perplexity, Gemini)
- Mention rates
- Recommendations

Turn audit results into compelling case study posts.

---

## What Claude Does vs What You Decide

| Claude handles | You provide |
|---------------|-------------|
| Applying post structure by pillar | Topic and angle selection |
| Writing hooks from hook bank | Approval of final hook |
| Formatting for LinkedIn readability | Voice authenticity check |
| Generating data-driven case studies | Real audit/data numbers |
| Running 3 Questions Test | Final posting decision |

---

## Skill Boundaries

### This skill excels for:
- GEO/SEO thought leadership content
- Data-driven case study posts
- Educational explainer posts
- Behind-the-scenes insights

### This skill is NOT ideal for:
- Personal/emotional posts → Need authentic human voice
- Controversial opinions → Requires your conviction
- Company announcements → Different format needed

---

## Skill Metadata

```yaml
name: linkedin-post
category: social
version: 2.0
author: GUIA
source_expert: GEO Thought Leadership Framework
difficulty: beginner
mode: cyborg
tags: [linkedin, social-media, content, geo, thought-leadership]
created: 2026-02-03
updated: 2026-02-03
```
