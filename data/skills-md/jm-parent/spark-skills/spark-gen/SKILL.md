---
name: spark-gen
description: Génère un livrable (project.md + vidéo /brag + logo + visuels) prêt à être ajouté sur TeamSpark, l'écran d'équipe qui présente les projets en boucle. À utiliser quand l'utilisateur dit "/spark-gen", "/sparck-gen", "génère une fiche TeamSpark", "prépare mon projet pour TeamSpark" ou veut présenter son projet sur l'écran d'équipe.
---

# spark-gen — générer un livrable TeamSpark

Analyse le dépôt courant et crée **uniquement** `_spotlight/<slug>/`. Ne modifie aucun fichier existant du repo. `<slug>` : nom court, minuscules, tirets (ex. `dashboard-ventes`).

## Étape 0 : durée de la vidéo

Demande à l'utilisateur la durée de la vidéo, **entre 20 et 120 secondes, 20 par défaut** (il peut simplement valider le défaut). Si la réponse est hors bornes ou n'est pas un nombre, redemande une fois, puis applique 20. Appelons-la `N`.

## Contenu du dossier

- `project.md`
- Tous les médias référencés, copiés à plat (pas de sous-dossier).

## Format de `project.md`

```
---
title: <nom du projet>
description: "<1 à 2 phrases en français, 160 caractères max, bénéfice utilisateur>"
team: [Prénom Nom, Prénom Nom]
logo: logo.svg
images: [cover.png]
video: brag.mp4
link: https://...
duration: <N>
---
```

`description` DOIT toujours être entre guillemets doubles (un ":" non quoté casse le YAML).

## Étape 1 : vidéo /brag (N secondes)

1. Cherche d'abord une vidéo déjà générée : `brag-output*/brag.mp4`, ou tout .mp4 / .webm de lancement dans `out/`, `renders/`, `docs/`, `assets/`, `media/`. Si elle existe et dure `N` ± 10 % (minimum ± 2 s), réutilise-la (la plus récente si plusieurs). Sinon, régénère-la (point 3).
2. Vérifie que la commande /brag est disponible. Sinon, installe-la :
   `npx skills add https://github.com/latent-spaces/brag --skill brag -g`
   (accepte les choix par défaut ; cible l'agent Copilot / l'agent courant). Vérifie aussi Hyperframes : `npx hyperframes doctor` (corrige ce qu'il signale). Recharge les skills si nécessaire, puis continue.
3. Si aucune vidéo valide n'existe, génère-la : `/brag --duration <N> --format landscape`. La sortie est dans `brag-output/` (ou `brag-output-<date>/`) ; la vidéo est `brag.mp4`.
4. Contrôle la durée : `ffprobe -v error -show_entries format=duration -of csv=p=0 brag.mp4`. Elle doit être à `N` ± 10 % (minimum ± 2 s). Sinon, relance /brag avec `--duration <N>`.
5. Contraintes : 16:9, .mp4 (H.264), 20 Mo maximum (réencode si besoin : `ffmpeg -i in.mp4 -vf scale=1280:-2 -crf 28 -an brag.mp4`). Le son n'est pas utilisé.
6. Copie-la sous le nom `brag.mp4` dans `_spotlight/<slug>/` et renseigne `video: brag.mp4`.
7. `duration` = durée réelle de la vidéo arrondie à l'entier supérieur (bornée entre 5 et 120).
8. Si l'installation ou la génération échoue malgré tout, n'invente rien : omets `video:` et signale-le dans le récapitulatif avec l'erreur rencontrée.

## Étape 2 : le reste de la fiche

- `title` est obligatoire. Tous les autres champs sont optionnels : si l'information manque, OMETS la ligne. N'invente rien.
- `description` : à partir du README et du code, sans jargon technique.
- `team` : déduis-la de `git shortlog -sn --no-merges` (5 max, sans bots), vrais noms et pas les logins.
- `logo` : logo/icône existant (README, public/, assets/, favicon), copié tel quel. Sinon omets.
- `images` : 0 à 4 visuels existants (captures du README, docs/, screenshots/). Ne génère rien. Facultatives si une vidéo est présente.
- `link` : URL publique http(s) du produit déployé, sinon du repo. Sinon omets.
- Chaque fichier cité dans `logo`, `images` et `video` doit exister dans `_spotlight/<slug>/`.

## Fin : récapitulatif et procédure de partage

Affiche :

- le contenu de `project.md` ;
- les fichiers copiés avec leur taille ;
- si la vidéo a été RÉCUPÉRÉE (chemin d'origine) ou GÉNÉRÉE, et si /brag a dû être INSTALLÉ ;
- les champs omis faute d'information.

Crée aussi l'archive `_spotlight/<slug>.zip` (PowerShell : `Compress-Archive -Path _spotlight/<slug>/* -DestinationPath _spotlight/<slug>.zip`, ou `zip -r` sous macOS/Linux), puis termine par cette procédure, avec les chemins réels :

> **Dernière étape : partager le livrable**
> 1. Récupère le dossier `_spotlight/<slug>/` (ou l'archive `_spotlight/<slug>.zip`).
> 2. Envoie-le à **Jean-Marie PARENT** (Teams, mail ou dépôt partagé).
> 3. Il l'ajoutera à TeamSpark et le projet apparaîtra dans la boucle de l'écran d'équipe.
