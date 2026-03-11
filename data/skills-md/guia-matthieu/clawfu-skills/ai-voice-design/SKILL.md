---
name: ai-voice-design
description: "Concevez et générez des voix IA pour vos vidéos en utilisant ElevenLabs ou Qwen3-TTS, avec clonage vocal, design par description, et synchronisation lip-sync. Use when: **Créer une voix de marque** - Définir le ton vocal pour une campagne; **Cloner une voix existante** - Reproduire une voix avec autorisation; **Designer une voix originale** - Créer une voix à partir d'une description; **Multi-personnages** - Gérer plusieurs voix dans une même vidéo; **Lip-sync vidéo IA** - Synchroniser voix e..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AI Voice Design

> Concevez et générez des voix IA pour vos vidéos en utilisant ElevenLabs ou Qwen3-TTS, avec clonage vocal, design par description, et synchronisation lip-sync.

## When to Use This Skill

- **Créer une voix de marque** - Définir le ton vocal pour une campagne
- **Cloner une voix existante** - Reproduire une voix avec autorisation
- **Designer une voix originale** - Créer une voix à partir d'une description
- **Multi-personnages** - Gérer plusieurs voix dans une même vidéo
- **Lip-sync vidéo IA** - Synchroniser voix et mouvements de lèvres
- **Localisation** - Adapter une voix en plusieurs langues

## Methodology Foundation

**Source**: ElevenLabs Documentation + Qwen3-TTS (Alibaba) + PJ Ace workflow

**Core Principle**: "La voix est 50% de l'impact d'une vidéo. ElevenLabs offre la qualité premium, Qwen3-TTS offre la flexibilité open-source. Le choix dépend du budget et du contrôle souhaité."

**Why This Matters**: Une voix mal choisie ou mal générée casse l'illusion d'une vidéo IA. Le bon matching voix/personnage et une qualité audio professionnelle font la différence entre "AI slop" et contenu crédible.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Compare les solutions TTS** - ElevenLabs vs Qwen3-TTS
2. **Guide le clonage vocal** - Process et requirements
3. **Structure le voice design** - Description textuelle de voix
4. **Gère le multi-voix** - Attribution et cohérence
5. **Prépare le lip-sync** - Intégration avec Kling/Veo

## How to Use

### Designer une voix pour une pub
```
J'ai besoin d'une voix pour ma pub [produit]. Le ton doit être [description]. Aide-moi à la designer.
```

### Cloner une voix
```
Je veux cloner cette voix [description/échantillon]. Guide-moi à travers le process avec [ElevenLabs/Qwen3-TTS].
```

### Gérer plusieurs personnages
```
J'ai 3 personnages dans ma vidéo: [descriptions]. Crée le casting vocal.
```

## Instructions

### Step 1: Choisir la solution TTS

```
## Comparatif ElevenLabs vs Qwen3-TTS

| Critère | ElevenLabs | Qwen3-TTS |
|---------|------------|-----------|
| **Prix** | $5-$330/mois | Gratuit (open-source) |
| **Qualité** | Excellente | Excellente |
| **Voice cloning** | 1-5 min audio | 3 sec audio |
| **Langues** | 29+ | 10 (EN, FR, DE, ES, IT, PT, RU, ZH, JP, KO) |
| **Latence** | ~200ms | 97ms (streaming) |
| **Self-hosted** | Non | Oui |
| **Voice design** | VoiceLab | Description textuelle |
| **API** | Cloud | Local ou cloud |

### Arbre de décision

**Q1: Budget disponible?**
- $0 (gratuit) → Qwen3-TTS
- $5-$100/mois → ElevenLabs Starter/Creator
- $100+/mois → ElevenLabs Pro

**Q2: Besoin de self-hosting?**
- Oui (données sensibles) → Qwen3-TTS
- Non → ElevenLabs ou Qwen3-TTS

**Q3: Langue requise parmi FR, EN, DE, ES, IT, PT, RU, ZH, JP, KO?**
- Oui → Les deux fonctionnent
- Non (autre langue) → ElevenLabs

**Q4: Latence critique (real-time)?**
- Oui → Qwen3-TTS (97ms)
- Non → Les deux
```

---

### Step 2: Voice Design par description

```
## Template de Description de Voix

### Caractéristiques de base
**Genre:** [ ] Masculin [ ] Féminin [ ] Non-binaire
**Âge apparent:** [20s / 30s / 40s / 50s / 60s+]
**Registre:** [ ] Grave [ ] Medium [ ] Aigu

### Qualités vocales
**Texture:**
[ ] Lisse/Veloutée [ ] Rauque/Gravelly
[ ] Nasale [ ] Claire [ ] Résonante

**Énergie:**
[ ] Calme/Posée [ ] Dynamique [ ] Intense
[ ] Chaleureuse [ ] Froide/Distante

**Rythme:**
[ ] Lent/Délibéré [ ] Modéré [ ] Rapide
[ ] Varié (storytelling)

### Accent/Origine
**Accent:** [Ex: Français neutre, British RP, Southern US, etc.]
**Particularités:** [Ex: légèrement rauque le matin, sourire dans la voix]

### Contexte d'utilisation
**Marque/Produit:** ________________________________
**Ton de la campagne:** ________________________________
**Personnage (si fiction):** ________________________________

### Exemples de référence (optionnel)
**Voix similaire à:** [Célébrité, personnage, pub connue]
**Éviter:** [Ce qu'on ne veut pas]
```

**Exemple de description complète:**

```
## Voice Brief: Pub NeuroBoost

**Profil:**
Homme, 40s, registre grave-medium

**Qualités:**
- Texture résonante et autoritaire mais pas intimidante
- Énergie posée, confiante, légèrement inspirante
- Rythme délibéré avec pauses stratégiques

**Accent:**
Français international (pas d'accent régional marqué)
Diction parfaite, articulation claire

**Références:**
- Similaire à: Morgan Freeman mais version française
- Éviter: Ton commercial agressif, urgence artificielle

**Notes:**
Cette voix doit incarner l'expertise et la confiance.
Le spectateur doit sentir qu'il reçoit un conseil d'un
mentor plutôt qu'un pitch de vendeur.
```

---

### Step 3: Clonage vocal

#### ElevenLabs

```
## Process de clonage ElevenLabs

### Instant Clone (1-5 min audio)
**Qualité:** Bonne (80% fidélité)
**Usage:** Tests, itération rapide

1. Préparer audio source:
   - 1-5 minutes de parole claire
   - Pas de musique de fond
   - Qualité minimum: 128kbps
   - Formats: MP3, WAV, M4A

2. Dans ElevenLabs:
   - Voice Lab → Add Voice → Instant Clone
   - Upload audio
   - Nommer la voix
   - Tester avec phrase sample

### Professional Clone (30+ min audio)
**Qualité:** Excellente (95%+ fidélité)
**Usage:** Production commerciale

1. Préparer corpus audio:
   - 30-60 minutes idéalement
   - Variété d'émotions et tons
   - Phrases complètes, pas de mots isolés
   - Studio quality (256kbps+, pas de bruit)

2. Soumettre pour training
   - Délai: 24-48h
   - Coût: Inclus dans plan Pro+

### Paramètres de génération
- **Stability:** 50-70% (naturel) / 80%+ (consistant)
- **Clarity:** 75%+ recommandé
- **Style:** 0-100% selon expressivité souhaitée
```

#### Qwen3-TTS

```
## Process de clonage Qwen3-TTS

### Zero-shot Clone (3 sec audio)
**Qualité:** Très bonne
**Usage:** Toute production

1. Préparer référence:
   - 3-10 secondes de parole claire
   - Pas de bruit de fond
   - Émotion neutre ou représentative

2. API Python:
```python
from qwen3_tts import Qwen3TTS

tts = Qwen3TTS()

# Cloner depuis référence
voice = tts.clone_voice(
    reference_audio="reference.wav",
    voice_name="my_voice"
)

# Générer avec la voix clonée
audio = tts.generate(
    text="Texte à synthétiser",
    voice=voice,
    language="fr"
)
audio.save("output.wav")
```

### Voice Design par texte
```python
# Créer une voix sans référence audio
voice = tts.design_voice(
    description="A warm, confident male voice in his 40s, \
    with a slight French accent, speaking slowly and \
    deliberately with gravitas."
)

audio = tts.generate(
    text="Votre texte ici",
    voice=voice
)
```

### Paramètres avancés
- **emotion:** "neutral", "happy", "sad", "angry", "surprise"
- **speed:** 0.5 (lent) à 2.0 (rapide)
- **pitch:** -10 à +10 (demi-tons)
```

---

### Step 4: Multi-personnages

```
## Casting Vocal Multi-personnages

### Template de casting

| Personnage | Description | Voix | Source |
|------------|-------------|------|--------|
| [Nom] | [Description physique/personnalité] | [Specs vocales] | [Clone/Design/Stock] |

### Exemple: Pub avec 3 personnages

| Personnage | Description | Voix | Source |
|------------|-------------|------|--------|
| CEO Emma | 35 ans, confiante, leader | Femme, medium, autoritaire-warm | Design: "Confident female executive..." |
| Dev Tom | 28 ans, geek enthousiaste | Homme, medium-aigu, rapide | Stock: "Young professional male" |
| Client Marc | 50 ans, sceptique puis convaincu | Homme, grave, hésitant→assuré | Design: "Skeptical older businessman..." |

### Règles de différenciation
- **Registres variés:** Grave, Medium, Aigu
- **Rythmes différents:** Lent vs Rapide
- **Accents distincts:** Si approprié au contexte
- **Énergies contrastées:** Calme vs Dynamique

### Workflow multi-voix
1. Générer chaque réplique séparément
2. Nommer fichiers: `P1_Emma_Line01.wav`
3. Assembler dans timeline audio
4. Vérifier cohérence de volume (normaliser à -6dB)
```

---

### Step 5: Lip-sync et intégration vidéo

```
## Intégration Voix + Vidéo IA

### Option A: Veo 3.1 (Audio natif)
La voix est générée par Veo avec la vidéo.

```
Prompt incluant audio:
"[Scene description]. The character says:
'[Dialogue exact]'. Voice: confident male, 30s,
warm tone. Ambient: office sounds."
```

Limitation: Moins de contrôle sur la voix exacte.

### Option B: Kling 2.6 Motion Control
Lip-sync depuis vidéo "driving".

1. Enregistrer vous-même le dialogue
2. Utiliser Kling avec driving video
3. Le lip-sync suit votre performance
4. Remplacer audio par voix IA en post

```
Workflow:
You → Record driving video with dialogue
Kling → Transfer lips to AI character
Post → Replace audio with ElevenLabs/Qwen voice
```

### Option C: Génération séparée + Post-sync
Pour contrôle maximum.

1. Générer vidéo sans audio (Runway, Pika)
2. Générer voix séparément
3. Synchroniser en post-production
4. Ajuster timing manuellement si besoin

Outils de sync:
- DaVinci Resolve (gratuit)
- Adobe Premiere
- D-ID (sync automatique)

### Checklist Lip-sync
- [ ] Timing voix correspond au mouvement des lèvres
- [ ] Pauses naturelles alignées
- [ ] Volume équilibré avec ambiance
- [ ] Pas de décalage visible (max 2-3 frames)
```

---

### Step 6: Export et spécifications audio

```
## Spécifications Audio Finales

### Format de sortie
- **Codec:** AAC ou WAV
- **Sample rate:** 48kHz (standard vidéo)
- **Bit depth:** 24-bit (WAV) ou 256kbps (AAC)
- **Channels:** Stereo ou Mono selon usage

### Niveaux recommandés
- **Voiceover:** -6dB à -3dB peak
- **Dialogue:** -12dB à -6dB
- **Ambiance:** -18dB à -12dB
- **Musique:** -12dB à -9dB (sous voix)

### Mastering basique
1. Normaliser tous les clips voix à -6dB
2. Appliquer compression légère (ratio 2:1)
3. EQ: couper sous 80Hz, boost léger 2-4kHz (clarté)
4. Limiter à -1dB pour éviter clipping

### Deliverables
```
📁 Audio_[Project]/
├── voiceover/
│   ├── VO_final_master.wav
│   └── VO_stems/
│       ├── P1_lines.wav
│       ├── P2_lines.wav
│       └── ...
├── sfx/
│   └── [sound effects]
├── music/
│   └── [background music]
└── mix/
    └── final_mix.wav
```
```

## Examples

### Example 1: Voice design pour pub premium

**Context**: Marque de montres de luxe, pub cinématique 30s

**Input**:
> J'ai une pub pour une marque de montres haut de gamme. Style très premium, inspiré des pubs Omega ou Rolex. Je veux une voix qui incarne l'excellence et l'héritage.

**Output**:

## Voice Brief: Montres Heritage Collection

### Profil cible
```
Genre: Masculin
Âge: 55-65 ans
Registre: Grave, profond
```

### Caractéristiques détaillées
```
Texture: Résonante, veloutée, avec légère patine
         (comme un bois noble ou un cuir vintage)

Énergie: Posée, contemplative, jamais pressée
         Chaque mot est choisi, chaque pause est intention

Rythme: Très lent, délibéré
        4-5 mots par respiration
        Pauses de 1-2 secondes entre phrases

Diction: Parfaite, aristocratique sans être snob
         Consonnes précises, voyelles riches
```

### Prompt ElevenLabs (Voice Design)
```
Create a distinguished male voice in his 60s.
Deep, resonant baritone with natural gravitas.
Speaking style: slow, deliberate, contemplative.
British Received Pronunciation with slight warmth.
Texture like aged whiskey - smooth with depth.
The voice of someone who has seen much and
speaks only when it matters.
```

### Prompt Qwen3-TTS
```python
voice = tts.design_voice(
    description="""
    Distinguished older gentleman, 60s, deep baritone.
    British accent, RP. Speaking very slowly and
    deliberately, with natural authority and warmth.
    Voice texture is rich and resonant, like aged oak.
    Contemplative, never rushed. Each word carries weight.
    Think: nature documentary narrator meets luxury brand.
    """
)
```

### Script avec indications
```
[PAUSE 2s]

"Time..." [PAUSE 1.5s]

"...is not measured." [PAUSE 1s]

"It is crafted." [PAUSE 2s]

"Heritage Collection." [PAUSE 1s]

"Since 1892."
```

### Paramètres techniques
- Stability: 85% (très consistant pour luxury)
- Speed: 0.7x (plus lent)
- Pas de musique sous la voix (voix seule, puis musique)

**Why this works**: Pour le luxe, less is more. Une voix grave, lente et posée communique la confiance et l'intemporalité. Les pauses créent la tension et la valeur perçue.

---

### Example 2: Multi-personnages comédie

**Context**: Pub SaaS décalée style sitcom avec 3 personnages

**Input**:
> J'ai une pub style The Office avec 3 personnages: le boss incompétent, l'employée exaspérée, et le stagiaire trop enthousiaste. Crée le casting vocal.

**Output**:

## Casting Vocal: "Office Chaos" Pub

### Personnage 1: Michel (Le Boss)
```
Profil:
- Homme, 50 ans
- Confiant mais incompétent
- Parle trop fort et trop vite
- S'interrompt lui-même

Voix:
- Medium-aigu (pas grave malgré l'autorité voulue)
- Nasale légèrement
- Volume variable (starts loud, gets louder)
- Phrases inachevées

Prompt ElevenLabs:
"Middle-aged man who thinks he's charismatic but isn't.
Slightly nasal voice, medium-high pitch. Speaks too
loudly and too fast, often interrupting himself.
French accent, corporate buzzwords enthusiast.
Michael Scott energy."
```

### Personnage 2: Sophie (L'Exaspérée)
```
Profil:
- Femme, 35 ans
- Compétente, fatiguée
- Sarcasme subtil
- Soupirs audibles

Voix:
- Medium, légèrement grave pour femme
- Sèche, précise
- Monotone quand exaspérée
- Soupirs comme ponctuation

Prompt Qwen3-TTS:
"Professional woman in her 30s, tired of everything.
Dry, slightly deadpan delivery. French, neutral accent.
Subtle sarcasm in every line. Occasional audible sighs.
The straight man in every comedy duo."
```

### Personnage 3: Théo (Le Stagiaire)
```
Profil:
- Homme, 22 ans
- Trop enthousiaste
- Voix qui monte en fin de phrase
- Acquiesce à tout

Voix:
- Medium-aigu
- Énergique, rapide
- Upspeak (fin de phrase montante)
- Ponctué de "super!", "génial!"

Prompt:
"Young man, early 20s, overly enthusiastic intern.
High-medium pitch, speaks quickly with upward
inflection at end of sentences. French, sounds
like he just discovered coffee. Every statement
sounds like an excited question."
```

### Exemple de dialogue
```
MICHEL: (loud) "Bon, l'équipe! J'ai une GRANDE nouvelle—
        enfin, moyenne—non, grande!"

SOPHIE: (flat) "[soupir] ...C'est la réunion quotidienne."

THÉO: (excited) "Oh WOW! Une grande nouvelle? C'est GÉNIAL!"

MICHEL: "Théo comprend, LUI. Donc, on va—
        comment ça s'appelle—pivoter!"

SOPHIE: "...On a pivoté hier."

THÉO: "RE-pivoter! J'ADORE re-pivoter!"
```

### Production notes
- Générer chaque personnage séparément
- Michel: boost 3-4kHz (plus "présent")
- Sophie: légère réverb room (distance émotionnelle)
- Théo: compression pour contenir les pics

**Why this works**: Les trois voix sont immédiatement distinctes par registre, rythme et énergie. Le contraste crée la comédie - le chaos de Michel, le calme de Sophie, l'excès de Théo.

---

## Checklists & Templates

### Checklist Voice Design

```
## Validation Voice Design

### Brief complet
- [ ] Genre et âge définis
- [ ] Registre spécifié (grave/medium/aigu)
- [ ] Texture décrite (lisse/rauque/etc)
- [ ] Énergie et rythme indiqués
- [ ] Accent précisé
- [ ] Références incluses

### Génération
- [ ] Prompt testé avec phrase sample
- [ ] Qualité audio vérifiée (pas de glitches)
- [ ] Volume normalisé
- [ ] Cohérence avec brand voice

### Multi-personnages
- [ ] Voix suffisamment distinctes
- [ ] Registres variés
- [ ] Énergies contrastées
- [ ] Test d'écoute ensemble
```

---

### Template Voice Brief

```
## Voice Brief: [Projet]

### Identité
**Projet/Marque:** ________________________________
**Type de contenu:** [ ] Pub [ ] Explainer [ ] Narration [ ] Dialogue
**Durée totale:** __________ secondes

### Profil vocal
**Genre:** [ ] M [ ] F [ ] Non-binaire
**Âge:** _______ ans
**Registre:** [ ] Grave [ ] Medium [ ] Aigu

### Caractéristiques
**Texture:** ________________________________
**Énergie:** ________________________________
**Rythme:** ________________________________
**Accent:** ________________________________

### Contexte émotionnel
**L'auditeur doit ressentir:** ________________________________
**Éviter:** ________________________________

### Référence
**Similaire à:** ________________________________

### Solution technique
[ ] ElevenLabs (budget: $_____/mois)
[ ] Qwen3-TTS (self-hosted)
[ ] Clone d'une voix existante

### Script
```
[Coller le script avec indications de pause]
```
```

---

### Coûts comparatifs

```
## Budget TTS

### ElevenLabs
| Plan | Prix/mois | Caractères | Équivalent |
|------|-----------|------------|------------|
| Free | $0 | 10k | ~2 min |
| Starter | $5 | 30k | ~6 min |
| Creator | $22 | 100k | ~20 min |
| Pro | $99 | 500k | ~100 min |

### Qwen3-TTS (Self-hosted)
| Composant | Coût |
|-----------|------|
| GPU (RTX 3090) | ~$800 one-time |
| Cloud GPU (A10) | ~$1/heure |
| Hébergement | Variable |
| Génération | Illimité |

### Recommandation par volume
- < 5 min/mois → ElevenLabs Free + Qwen3-TTS
- 5-20 min/mois → ElevenLabs Creator ($22)
- 20-100 min/mois → ElevenLabs Pro ($99)
- > 100 min/mois → Qwen3-TTS self-hosted
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- [ElevenLabs Documentation](https://elevenlabs.io/docs)
- [ElevenLabs Voice Cloning](https://elevenlabs.io/voice-cloning)
- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS Blog](https://qwen.ai/blog?id=qwen3tts-0115)
- [MKTG Skills - Étude Écosystème Vidéo IA](../../docs/etude-ecosysteme-video-ia.md)

## Related Skills

- [ai-video-prompting](../ai-video-prompting/) - Intégration audio dans les prompts Veo
- [ai-video-qa](../ai-video-qa/) - Vérification qualité audio
- [copywriting-ogilvy](../../content/copywriting-ogilvy/) - Écriture des scripts voix

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: ai-voice-design
category: video
subcategory: production
version: 1.0
author: MKTG Skills
source_expert: ElevenLabs + Qwen3-TTS + PJ Ace
source_work: TTS Documentation
difficulty: intermediate
estimated_value: $500-2000 (voice design + production)
tags: [video, ai, voice, tts, elevenlabs, qwen, cloning, audio]
created: 2026-01-25
updated: 2026-01-25
```
