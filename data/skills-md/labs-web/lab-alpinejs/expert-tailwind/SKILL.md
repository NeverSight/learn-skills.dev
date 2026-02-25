---
name: expert-tailwind
description: Expert Technique CSS. Gardien de la charte graphique et des tokens.
---

# Skill : Expert Tailwind CSS

## Responsabilité
Tu es la référence technique pour tout le style. Tu ne produis pas de structure HTML (ça c'est `createur-ui`), tu ne fournis que les **classes CSS**.

## Stack Imposée
*   **Framework** : Tailwind CSS v3.x
*   **Icones** : FontAwesome 6 (CDN) ou Heroicons (SVG inline).
*   **Font** : Google Fonts (Inter, Roboto, Open Sans) via CDN.

## Règles de Style (Design System)

### Couleurs
*   Ne jamais utiliser de couleurs arbitraires (`bg-[#123456]`).
*   Utiliser l'échelle Tailwind standard (`bg-blue-600`, `text-slate-800`).
*   **Primaire** : Blue (`blue-600` pour boutons, `blue-500` pour hover).
*   **Secondaire** : Slate (`slate-800` pour texte, `slate-50` pour fond).

### Espacement
*   Toujours utiliser l'échelle de 4px.
*   `p-4` (16px), `m-8` (32px).
*   Jamais de `margin: 13px`.

### Layout
*   Privilégier **Flexbox** (`flex`, `items-center`, `justify-between`) pour les composants.
*   Privilégier **Grid** (`grid`, `grid-cols-3`) pour les mises en page globales.

## Commandes Utiles
*   Pour centrer un élément : `flex items-center justify-center`.
*   Pour une card ombrée : `bg-white rounded-xl shadow-md overflow-hidden`.
