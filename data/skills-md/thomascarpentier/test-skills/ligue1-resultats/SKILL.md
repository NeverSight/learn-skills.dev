---
name: ligue1-resultats
description: This skill should be used when the user asks about "résultats Ligue 1", "ligue 1 results", "scores Ligue 1", "derniers matchs Ligue 1", "derniers résultats", "classement Ligue 1", "résultats foot", or any request related to French Ligue 1 football results, scores, or standings.
version: 1.0.0
---

# Ligue 1 — Résultats & Classement

Ce skill permet d'afficher les derniers résultats, le classement et les prochains matchs de la Ligue 1 française.

## Contexte dynamique

- Date actuelle : !`date "+%A %d %B %Y"`
- Journée en cours (estimation) : !`python3 -c "import datetime; d=datetime.date.today(); start=datetime.date(2024,8,16); week=min(34,max(1,(d-start).days//7+1)); print(f'Journée ~{week}/34')"`

## Workflow

Quand ce skill est déclenché :

1. **Recherche les résultats récents** via `WebSearch` avec la query :
   `Ligue 1 résultats dernière journée 2025 2026`

2. **Recherche le classement actuel** via `WebSearch` avec :
   `classement Ligue 1 2025 2026`

3. **Affiche les résultats** dans ce format :

### Format de sortie attendu

```
## Ligue 1 — Journée XX (JJ/MM/AAAA)

### Résultats

| Domicile       | Score | Extérieur      |
|----------------|-------|----------------|
| PSG            | 3 - 1 | Lyon           |
| Marseille      | 0 - 0 | Monaco         |
| ...            | ...   | ...            |

### Classement (Top 10)

| # | Club           | Pts | J  | G  | N  | P  | Bp | Bc |
|---|----------------|-----|----|----|----|----|----|----|
| 1 | PSG            |  XX | XX | XX | XX | XX | XX | XX |
| 2 | Monaco         |  XX | XX | XX | XX | XX | XX | XX |
| ...                                                      |
```

## Instructions pour Claude

1. Lance **deux recherches en parallèle** :
   - `WebSearch` → résultats de la dernière journée Ligue 1
   - `WebSearch` → classement Ligue 1 actuel

2. **Consolide les informations** des résultats de recherche pour construire le tableau des résultats et le classement.

3. Si les données sont incomplètes, effectue une recherche supplémentaire ciblée sur les matchs manquants.

4. **Présente les données** de façon claire avec :
   - Le numéro de journée et la date
   - Un tableau des scores de la journée
   - Le classement actuel (au moins le top 10)

5. Mentionne toujours la **source** des données et la date de dernière mise à jour.

## Outils utilisés

- `WebSearch` — pour récupérer les résultats et le classement en temps réel
