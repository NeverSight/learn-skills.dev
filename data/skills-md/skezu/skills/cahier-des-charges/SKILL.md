---
name: cahier-des-charges
description: Rédige un Cahier des Charges (CdC) professionnel pour application mobile ou web en français. Ce skill transforme les spécifications techniques (requirements.md, design.md) en un document de cadrage formel. Il met l'accent sur les objectifs stratégiques, l'expérience utilisateur (UX/UI), les fonctionnalités détaillées, les contraintes techniques (iOS/Android, Swift/Kotlin) et la collaboration client-développeur.
---

# Cahier des Charges (CdC) Professionnel

Ce skill guide la rédaction d'un Cahier des Charges exhaustif, servant de contrat moral et technique entre le client et l'équipe de développement.

## Principes Fondamentaux (Bonnes Pratiques)

1. **Objectifs et Besoins** : Commencer par une analyse profonde des besoins métier et des utilisateurs finaux (études de marché, analyses concurrentielles).
2. **Spécifications Fonctionnelles** : Détailler chaque fonctionnalité pour éviter les ambiguïtés. Utiliser des cas d'utilisation (Use Cases) précis.
3. **Expérience Utilisateur (UX)** : Décrire la navigation, l'interactivité et l'ergonomie. Mentionner l'usage de wireframes ou maquettes.
4. **Contraintes Techniques** : Préciser les plateformes (iOS, Android), les langages (Swift, Kotlin, etc.), la gestion des données (MySQL, etc.) et les exigences de performance.
5. **Sécurité et Réglementation** : Inclure la protection des données (RGPD) et la conformité aux normes de sécurité.

## Flux de travail

1. **Collecte d'Intel** : Lire `.agent/specs/{feature-name}/requirements.md` et `design.md`.
2. **Cadrage** : Définir le contexte, le public cible et le positionnement marché.
3. **Rédaction Structurée** : Suivre scrupuleusement le plan défini dans `references/template.md`.
4. **Révision Collaborative** : S'assurer que le document permet une communication fluide et évite les malentendus coûteux.

## Structure Recommandée

- **Introduction** : Présentation de l'entreprise et contexte.
- **Objectifs de l'Application** : Accès aux services, engagement, expérience utilisateur.
- **Fonctionnalités Principales** : Inscription, profil, notifications push, contenu dynamique, intégration sociale.
- **Design & UX** : Identité de marque, couleurs, typographies, réactivité.
- **Contraintes Techniques** : OS, langages, base de données, temps de réponse.
- **Livrables** : Application fonctionnelle, doc technique, manuel utilisateur, rapports de tests.
- **Calendrier & Budget** : Phases de conception, dev, tests et lancement.

## Ressources
- [Template Officiel](references/template.md)
- [Exemple d'Application Mobile](references/example.md)
