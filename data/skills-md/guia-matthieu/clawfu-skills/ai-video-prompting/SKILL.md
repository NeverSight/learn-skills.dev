---
name: ai-video-prompting
description: "Générez des prompts optimisés pour chaque modèle de génération vidéo IA (Veo 3, Runway Gen-3, Kling 2.6, Pika), en exploitant leurs forces spécifiques. Use when: **Animer des frames de storyboard** - Transformer des images fixes en vidéo; **Choisir le bon modèle** - Sélectionner Veo, Runway, Kling ou Pika selon le besoin; **Optimiser la qualité de génération** - Prompts structurés pour meilleurs résultats; **Créer des transitions fluides** - Scene extension, first/last frame; **Utiliser le mo..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AI Video Prompting

> Générez des prompts optimisés pour chaque modèle de génération vidéo IA (Veo 3, Runway Gen-3, Kling 2.6, Pika), en exploitant leurs forces spécifiques.

## When to Use This Skill

- **Animer des frames de storyboard** - Transformer des images fixes en vidéo
- **Choisir le bon modèle** - Sélectionner Veo, Runway, Kling ou Pika selon le besoin
- **Optimiser la qualité de génération** - Prompts structurés pour meilleurs résultats
- **Créer des transitions fluides** - Scene extension, first/last frame
- **Utiliser le motion control** - Face-driving et performance transfer avec Kling

## Methodology Foundation

**Source**: Documentation officielle Veo 3.1, Runway Gen-3, Kling 2.6, Pika 2.2 + PJ Ace workflow

**Core Principle**: "Chaque modèle a ses forces. Veo excelle en audio natif, Runway en contrôle caméra, Kling en motion control, Pika en accessibilité. Choisissez le bon outil pour chaque shot."

**Why This Matters**: Un prompt générique donne des résultats génériques. En structurant vos prompts selon les spécificités de chaque modèle, vous obtenez des vidéos de qualité professionnelle.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Sélectionne le modèle optimal** - Selon le type de shot et les besoins
2. **Structure les prompts par modèle** - Formats optimisés pour chaque plateforme
3. **Configure les paramètres techniques** - Durée, résolution, aspect ratio
4. **Guide le workflow image-to-video** - Upload et animation des frames
5. **Planifie les extensions de scène** - Clips continus au-delà de 8 secondes

## How to Use

### Animer un storyboard complet
```
J'ai ces frames de storyboard: [description]. Génère les prompts d'animation pour Veo 3.1.
```

### Choisir le bon modèle
```
J'ai besoin de [décrire le shot]. Quel modèle utiliser et comment structurer le prompt?
```

### Créer une séquence continue
```
J'ai un clip de 8 secondes et je veux l'étendre à 30 secondes. Guide-moi avec scene extension.
```

## Instructions

### Step 1: Sélectionner le modèle optimal

```
## Guide de Sélection

| Besoin | Modèle recommandé | Pourquoi |
|--------|-------------------|----------|
| Audio synchronisé natif | **Veo 3.1** | Seul modèle avec génération audio intégrée |
| Contrôle caméra précis | **Runway Gen-3** | Camera control directionnel |
| Face-driving / Performance | **Kling 2.6** | Motion control depuis vidéo référence |
| Transitions image-image | **Pika 2.2** | Pikaframes optimisé pour ça |
| Budget limité | **Pika 2.2** | Freemium généreux |
| Qualité maximale | **Veo 3.1** | 1080p natif, meilleure cohérence |
| Expérimentation rapide | **Pika 2.2** | Itération rapide |
| Personnage récurrent | **Kling 2.6** | Character reference |

### Matrice de décision

**Q1: Avez-vous besoin d'audio synchronisé?**
- Oui → Veo 3.1 (dialogue, sound effects)
- Non → Continuer

**Q2: Avez-vous une vidéo de performance à transférer?**
- Oui → Kling 2.6 (motion control)
- Non → Continuer

**Q3: Avez-vous besoin de contrôle caméra précis?**
- Oui → Runway Gen-3 (camera control)
- Non → Continuer

**Q4: Avez-vous un budget limité?**
- Oui → Pika 2.2
- Non → Veo 3.1 (qualité par défaut)
```

---

### Step 2: Prompts Veo 3.1 (Google)

```
## Veo 3.1 Prompt Structure

### Format de base
[SHOT TYPE] of [SUBJECT] [ACTION] in [SETTING].
[CAMERA MOVEMENT]. [LIGHTING]. [STYLE/MOOD].
[AUDIO DESCRIPTION if needed].

### Paramètres
- Durée: 4-8 secondes/génération
- Résolution: 1080p
- Aspect: 16:9 ou 9:16
- Audio: Activé par défaut (dialogue, SFX, ambiance)

### Exemple complet
```
Medium shot of a confident businesswoman walking through
a modern glass office lobby. Slow dolly following her from
the side. Warm morning sunlight streaming through windows,
creating lens flares. Cinematic corporate style, shallow
depth of field. Sound of heels clicking on marble floor,
ambient office murmur in background.
```

### Tips Veo 3.1
- Décrire explicitement l'audio souhaité
- Utiliser des termes cinématographiques (dolly, tracking, pan)
- Spécifier l'éclairage en détail
- Inclure l'ambiance sonore pour meilleur matching

### Scene Extension (clips longs)
1. Générer clip initial (8s)
2. Télécharger
3. Dans Flow/Gemini: "Extend this scene with [continuation]"
4. Le modèle utilise la dernière seconde comme référence
5. Répéter jusqu'à durée souhaitée
```

---

### Step 3: Prompts Runway Gen-3 Alpha

```
## Runway Gen-3 Prompt Structure

### Format de base
[DESCRIPTIVE SCENE]. [SUBJECT ACTION]. [CAMERA INSTRUCTION].
[LIGHTING AND ATMOSPHERE]. [STYLE REFERENCE].

### Paramètres
- Durée: 5 ou 10 secondes
- Mode: Text-to-Video ou Image-to-Video
- Camera Control: Direction + Intensité
- First/Last Frame: Définir début et/ou fin

### Camera Control Options
| Direction | Effet |
|-----------|-------|
| Pan Left/Right | Rotation horizontale |
| Tilt Up/Down | Rotation verticale |
| Dolly In/Out | Mouvement avant/arrière |
| Truck Left/Right | Mouvement latéral |
| Pedestal Up/Down | Mouvement vertical |
| Zoom In/Out | Changement focal |
| Static | Pas de mouvement |

Intensité: Low / Medium / High

### Exemple avec Camera Control
```
Prompt: A mysterious forest at twilight, fog rolling
between ancient trees, fireflies beginning to glow.
Ethereal fantasy atmosphere, cinematic color grading.

Camera: Dolly In, Medium intensity

First Frame: [Upload image du storyboard]
Duration: 10 seconds
```

### First/Last Frame Technique
- **First Frame**: L'image devient le point de départ
- **Last Frame**: L'image devient la destination
- **Both**: Transition animée entre deux images

### Workflow Image-to-Video
1. Upload frame upscalée du storyboard
2. Sélectionner "First Frame" ou "Last Frame"
3. Écrire prompt décrivant le mouvement souhaité
4. Configurer Camera Control
5. Générer (10 crédits/sec standard)
```

---

### Step 4: Prompts Kling 2.6 Motion Control

```
## Kling 2.6 Prompt Structure

### Concept clé: Motion Transfer
Kling 2.6 permet de "conduire" un personnage généré avec
une vidéo de performance réelle.

### Inputs requis
1. **Reference Image**: Le personnage/look souhaité
2. **Driving Video**: La vidéo de performance (mouvements, expressions)
3. **Text Prompt**: Instructions supplémentaires

### Format de prompt
[SUBJECT DESCRIPTION matching reference image].
[SCENE/ENVIRONMENT]. [STYLE].
Motion: Transfer expressions and movements from driving video.

### Exemple Motion Control
```
Reference Image: [Portrait d'un astronaute stylisé]

Driving Video: [Vous parlant à la caméra, 10 secondes]

Prompt: An astronaut in a futuristic space station,
speaking directly to camera. Sci-fi movie lighting,
volumetric fog, control panels glowing in background.
Transfer facial expressions and lip movements from
driving video.

Duration: 10 seconds
Resolution: 1080p
```

### Best Practices Motion Control
- **Vidéo driving**: Fond simple, contraste élevé
- **Silhouette claire**: Le sujet doit être distinct
- **Mouvements**: Fonctionne pour expressions, lips, corps entier
- **Limite**: Éviter les actions trop rapides ou complexes

### Use Cases
| Scénario | Setup |
|----------|-------|
| 1 acteur → N personnages | 1 driving video, N reference images |
| Lip-sync dialogue | Acteur parle, personnage anime |
| Performance dance | Vidéo danse → personnage stylisé |
| Deep fake éthique | Avec autorisation du sujet |
```

---

### Step 5: Prompts Pika 2.2

```
## Pika 2.2 Prompt Structure

### Format de base
[SCENE DESCRIPTION]. [ACTION]. [STYLE].

### Paramètres
- Durée: Jusqu'à 10 secondes
- Résolution: 1080p
- Outils spéciaux: Pikaframes, Pikaswaps, Pikadditions

### Pikaframes (Transitions)
Anime une transition fluide entre 2-5 images.

```
Input:
- Image 1 (start): Bureau chaotique
- Image 2 (end): Bureau organisé

Prompt: Smooth transformation from messy to organized
office space, papers flying into place, magical
organization sequence. Time-lapse feel, 5 seconds.
```

### Pikaswaps (Remplacement d'objet)
Remplace un élément dans une vidéo existante.

```
Input Video: Personne tenant une tasse de café

Swap: Replace coffee cup with glowing energy drink can

Prompt: Replace the coffee cup with a futuristic
glowing red energy drink, matching lighting and
hand movements perfectly.
```

### Pikadditions (Ajout d'éléments)
Insère des éléments dans un footage existant.

```
Input Video: Scène de rue normale

Addition: Add a friendly dragon flying overhead

Prompt: A colorful cartoon dragon flying through
the scene, casting shadow on the street, looking
down curiously at the people below.
```

### Best Practices Pika
- Prompts plus courts et directs que Veo/Runway
- Idéal pour l'expérimentation rapide
- Utiliser Pikaframes pour les transformations before/after
- Pikaswaps excellent pour les variations de produit
```

---

### Step 6: Workflow d'animation complet

```
## Animation Pipeline

### Phase 1: Préparation des frames
1. Récupérer les frames upscalées du storyboard
2. Nommer clairement: S01_Shot01_Wide.png
3. Organiser par scène

### Phase 2: Génération par modèle

**Pour chaque frame:**

| Frame | Modèle | Pourquoi | Durée |
|-------|--------|----------|-------|
| S01_Shot01 | Veo 3.1 | Establishing + ambiance audio | 4s |
| S01_Shot02 | Runway | Camera dolly in | 3s |
| S01_Shot03 | Veo 3.1 | Dialogue audio | 4s |
| S01_Shot04 | Pika | Transition produit | 3s |

### Phase 3: Scene Extension (si besoin)

Pour clips > 8 secondes:
```
Clip 1 (0:00-0:08): Génération initiale
     ↓
Dernière frame de Clip 1
     ↓
Clip 2 (0:08-0:16): Scene extension avec cette frame
     ↓
Répéter
```

### Phase 4: Export et compilation

Formats recommandés:
- Export: MP4, H.264, 1080p, 24fps
- Couleur: Rec. 709
- Audio: AAC 48kHz (si Veo)

Compilation:
- DaVinci Resolve (gratuit)
- Premiere Pro
- Final Cut Pro
```

## Examples

### Example 1: Publicité produit tech (multi-modèle)

**Context**: 30 secondes pour une app de productivité, besoin de dialogue et transitions

**Input**:
> J'ai 4 frames de storyboard pour une pub TaskFlow. Scène 1: chaos bureau, Scène 2: découverte app, Scène 3: transformation, Scène 4: CTA. Génère les prompts d'animation.

**Output**:

## Plan d'animation multi-modèle

### Scène 1: Chaos Bureau (0:00-0:08)
**Modèle**: Veo 3.1 (audio ambiance + dialogue)

```
Prompt Frame 1.1 (Wide):
Wide shot of a chaotic home office, papers scattered
everywhere, a stressed man in his 30s at a cluttered desk
with multiple monitors showing notifications. Slight
camera shake, documentary style. Sound of notification
pings overlapping, keyboard clacking, frustrated sigh.
Duration: 4 seconds

Prompt Frame 1.2 (Closeup):
Close-up of the same man rubbing his temples, notifications
reflecting in his glasses. Shallow depth of field,
harsh overhead lighting. Sound of phone buzzing,
email notification chime.
Duration: 4 seconds
```

### Scène 2: Découverte App (0:08-0:14)
**Modèle**: Runway Gen-3 (camera control)

```
Prompt Frame 2.1:
Over-the-shoulder shot revealing a clean, modern app
interface on laptop screen. Calming blue interface
with organized task lists. Warm side lighting
beginning to enter frame.

Camera Control: Dolly In, Low intensity
First Frame: [Upload S02_Shot01.png]
Duration: 6 seconds
```

### Scène 3: Transformation (0:14-0:24)
**Modèle**: Pika 2.2 Pikaframes (transition)

```
Pikaframes Input:
- Image 1: Cluttered desk chaos
- Image 2: Same desk, minimalist and organized

Prompt:
Magical time-lapse transformation, papers flying into
organized stacks, cables organizing themselves, coffee
cups disappearing. Satisfying organization sequence.
Light shifting from harsh to warm golden hour.
Duration: 10 seconds
```

### Scène 4: CTA (0:24-0:30)
**Modèle**: Veo 3.1 (audio + voice)

```
Prompt Frame 4.1:
Medium shot of the same man, now relaxed and smiling,
typing confidently on clean desk. TaskFlow logo
appearing as subtle overlay. Warm morning light,
plant in background.

Voiceover (to be generated): "TaskFlow. Work flows.
Life follows."

Ambient: Calm office sounds, gentle keyboard taps
Duration: 6 seconds
```

**Why this works**: Chaque modèle est utilisé pour sa force - Veo pour l'audio, Runway pour le mouvement caméra précis, Pika pour la transition magique.

---

### Example 2: Contenu lifestyle avec face-driving

**Context**: Vidéo pour une marque fitness, un influenceur veut apparaître comme différents athlètes stylisés

**Input**:
> J'ai une vidéo de moi qui parle à la caméra (20 sec). Je veux apparaître comme un athlète futuriste dans un décor sci-fi. Utilise Kling pour le motion control.

**Output**:

## Setup Kling 2.6 Motion Control

### Inputs préparés

**Reference Image (à générer d'abord):**
```
Prompt pour Ideogram/Nano Banana:
Portrait of a futuristic athlete in a high-tech gym,
wearing sleek black and neon blue athletic wear,
cyberpunk aesthetic. Looking directly at camera,
confident expression. Dramatic rim lighting,
holographic displays in background. 8K detail,
cinematic portrait.
```

**Driving Video (votre vidéo):**
- Durée: 20 secondes
- Vous parlant à la caméra
- Fond simple (mur uni idéalement)
- Bonne luminosité sur visage
- Mouvements naturels

### Prompts Kling 2.6

**Clip 1 (0:00-0:10):**
```
Reference: [futuristic_athlete_portrait.png]
Driving: [your_video_clip1.mp4]

Prompt:
A futuristic athlete in a high-tech training facility,
speaking confidently to camera. Holographic workout
stats floating around. Neon blue and purple accent
lighting. Cyberpunk gym aesthetic with chrome equipment.
Transfer full facial expressions, lip movements, and
subtle head gestures from driving video.

Duration: 10 seconds
Resolution: 1080p
```

**Clip 2 (0:10-0:20):**
```
Reference: [same image]
Driving: [your_video_clip2.mp4]

Prompt:
Same athlete continuing to speak, camera slowly
pushing in for more intimate framing. Energy field
glowing around athlete subtly. Maintain performance
transfer for perfect lip sync and expressions.

Duration: 10 seconds
```

### Post-production
1. Assembler les 2 clips
2. Ajouter votre voix originale (ou garder Kling audio)
3. Ajuster couleurs pour cohérence
4. Ajouter texte/CTA en post

**Why this works**: Kling 2.6 excelle dans le transfer de performance. Votre vidéo "driving" donne le timing exact des lèvres et expressions, tandis que le modèle génère le look stylisé souhaité.

---

## Checklists & Templates

### Checklist Prompt Vidéo IA

```
## Validation Prompt

### Structure
- [ ] Shot type spécifié (wide, medium, close-up)
- [ ] Sujet clairement décrit
- [ ] Action/mouvement indiqué
- [ ] Environnement/décor précisé
- [ ] Éclairage détaillé
- [ ] Style/mood défini

### Par modèle
**Veo 3.1:**
- [ ] Description audio incluse (dialogue, SFX, ambiance)
- [ ] Termes cinématographiques utilisés

**Runway Gen-3:**
- [ ] Camera control configuré (direction + intensité)
- [ ] First/Last frame uploadée si image-to-video

**Kling 2.6:**
- [ ] Reference image préparée
- [ ] Driving video qualité suffisante
- [ ] Motion transfer spécifié dans prompt

**Pika 2.2:**
- [ ] Outil approprié sélectionné (Frames/Swaps/Additions)
- [ ] Images input uploadées
```

---

### Template Prompts par Modèle

```
## Veo 3.1 Template
[SHOT] of [SUBJECT] [ACTION] in [SETTING].
[CAMERA MOVEMENT]. [LIGHTING DESCRIPTION].
[VISUAL STYLE]. [AUDIO: dialogue/SFX/ambiance].

## Runway Gen-3 Template
[SCENE DESCRIPTION]. [SUBJECT] [ACTION].
[ATMOSPHERE AND LIGHTING]. [STYLE REFERENCE].
Camera: [DIRECTION], [INTENSITY]
Frame: [First/Last/Both]

## Kling 2.6 Template
Reference: [image file]
Driving: [video file]
[SUBJECT matching reference] in [ENVIRONMENT].
[STYLE]. Transfer [expressions/lips/body] from driving.

## Pika 2.2 Template
[Tool: Pikaframes/Pikaswaps/Pikadditions]
Input: [image(s) or video]
[DESIRED TRANSFORMATION/ADDITION]. [STYLE]. [DURATION].
```

---

### Comparatif Coûts

```
## Coût par seconde de vidéo

| Modèle | Mode | Coût/sec | 30 sec = |
|--------|------|----------|----------|
| Veo 3.1 Fast | API | $0.15 | $4.50 |
| Veo 3.1 Standard | API | $0.40 | $12.00 |
| Runway Gen-3 Alpha | Credits | 10 cr (~$0.45) | ~$13.50 |
| Runway Gen-3 Turbo | Credits | 5 cr (~$0.22) | ~$6.60 |
| Kling 2.6 Standard | Credits | Variable | ~$5-15 |
| Pika 2.2 | Freemium | $0 (limité) | $0-10 |

**Budget recommandé pour pub 30s:**
- Économique: $20-50 (Pika + sélectif Veo)
- Standard: $50-100 (Mix optimal)
- Premium: $100-200 (Tout Veo 3.1 Standard)
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

- [Google Developers - Veo 3.1](https://developers.googleblog.com/introducing-veo-3-1-and-new-creative-capabilities-in-the-gemini-api/)
- [Runway Help - Gen-3 Alpha](https://help.runwayml.com/hc/en-us/articles/30266515017875-Creating-with-Gen-3-Alpha-and-Gen-3-Alpha-Turbo)
- [Higgsfield - Kling 2.6 Guide](https://higgsfield.ai/blog/Kling-2.6-Motion-Control-Full-Guide)
- [Pika Labs Documentation](https://pikalabs.org/)
- [MKTG Skills - Étude Écosystème Vidéo IA](../../docs/etude-ecosysteme-video-ia.md)

## Related Skills

- [ai-storyboard-2x2](../ai-storyboard-2x2/) - Étape précédente: frames à animer
- [ai-voice-design](../ai-voice-design/) - Pour la création audio/voix
- [ai-video-qa](../ai-video-qa/) - Étape suivante: contrôle qualité

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: ai-video-prompting
category: video
subcategory: production
version: 1.0
author: MKTG Skills
source_expert: PJ Ace + Official Documentation
source_work: Veo, Runway, Kling, Pika Documentation
difficulty: intermediate
estimated_value: $1000-5000 (professional animation)
tags: [video, ai, prompting, veo, runway, kling, pika, animation]
created: 2026-01-25
updated: 2026-01-25
```
