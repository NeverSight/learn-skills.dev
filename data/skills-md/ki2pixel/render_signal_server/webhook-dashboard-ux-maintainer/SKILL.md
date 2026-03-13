---
name: webhook-dashboard-ux-maintainer
description: Preserve and extend the modern dashboard (dashboard.html + static modules) with WCAG-compliant UX, autosave flows, and modular ES6 patterns.
---

# Webhook Dashboard UX Maintainer

Utilise ce skill pour toute évolution de l'interface dashboard (bandeau statut, panneaux webhooks, routing rules builder, magic link, autosave).

## Pré-requis
- Connaissance des règles dans `.clinerules/codingstandards.md` (pas d'`innerHTML`, accessibilité, autosave debounce).
- Accès au dashboard pour les tests manuels.
- Virtualenv `/mnt/venv_ext4/venv_render_signal_server` pour les tests backend.

## Workflow
1. **Définir la zone impactée**
   - Panneaux Webhooks, Routing Rules, Magic Link, indicateurs de statut, etc.
2. **Mettre à jour le HTML**
   - Respecter les `section-panel`, attributs ARIA (`role="tablist"`, `aria-expanded`).
   - Ajouter les hooks `data-*` nécessaires aux modules.
3. **Adapter les modules ES6**
   - Nouvelles fonctionnalités → créer un service ou composant dédié, exports nommés.
   - Utiliser `ApiService` pour les appels, `MessageHelper` pour les toasts.
4. **États UX**
   - Maintenir `updatePanelStatus`, badges `saving/saved/error`, debounces 2-3s.
   - Ajouter focus states visibles et respect `prefers-reduced-motion`.
5. **Tests manuels**
   - Lancer le helper `bash ./.agents/skills/webhook-dashboard-ux-maintainer/test_dashboard_ux.sh`.
   - Suivre la checklist fournie par le script.
6. **Tests backend**
   - Le script exécute automatiquement les tests API pertinents.
7. **Documentation**
   - Mettre à jour `docs/access/dashboard-ui.md` si l'UX évolue.
   - Documenter les patterns récents (verrouillage routing rules, bandeau statut, flux Magic Link avec `showCopiedFeedback`) dans la Memory Bank.

## Ressources
- `test_dashboard_ux.sh` : checklist manuelle + exécution des tests backend associés.

## Conseils
- Centraliser les chaînes/badges dans les helpers existants.
- Pour les animations, rester cohérent avec les durées (0.2s hover, 0.3s transitions).
- Ajouter des hooks de test (`data-testid`) uniquement si requis par les tests automatisés.
