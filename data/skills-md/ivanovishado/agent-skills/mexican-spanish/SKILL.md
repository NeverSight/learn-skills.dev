---
name: mexican-spanish
description: >
  Expert in Mexican Spanish idioms, slang, and colloquial expressions.
  Trigger: When user asks to write, translate, or interpret text in Mexican Spanish (Español Mexicano).
  Use this skill whenever the user mentions Mexican slang, "hablar mexicano", albures, modismos mexicanos,
  wants text localized for a Mexican audience, or asks about expressions from Mexico — even if they
  don't explicitly say "Mexican Spanish".
license: MIT
metadata:
  author: ivanovishado
  version: "1.0"
---

## When to Use

- When the user asks to rewrite text in "Mexicano" or for a Mexican audience.
- When explaining Mexican idioms, slang, or albures.
- When generating informal or colloquial text that sounds naturally Mexican.
- When interpreting "modismos", "dichos", or slang from text provided by the user.
- When localizing Spanish content specifically for Mexico.

## Critical Patterns

- **Tone**: Mexican Spanish ranges from formal (standard) to highly informal (slang/albur). Context matters — the same word can be affectionate or offensive depending on tone and relationship.
- **Conjugation**: Mexicans use "tú" (not "vos" as in Argentina or "voh" as in Chile). The formal "usted" is used more broadly than in other Latin American countries, including with parents in some regions.
- **Diminutives**: Mexicans use diminutives extensively — not just for size but for politeness, affection, and softening requests ("ahorita", "tantito", "cerquita", "corridito").
- **"Ahorita" ambiguity**: "Ahorita" can mean right now, in a moment, later, or never — context and tone are everything.
- **Common Vocab**:
    - **Güey/Wey**: Context-dependent (friend, dude, or fool).
    - **Chido/Chingón**: Cool/Great/Awesome.
    - **Neta**: Truth / "For real?"
    - **Mande**: Polite "what?" or "pardon?" (uniquely Mexican).
    - **Órale**: Wow / OK / Let's go (multipurpose).
    - **Fresa**: Snobby / preppy person.
    - **Chamba**: Work/Job.
    - **Naco**: Tacky / uncultured (can be offensive).
    - **Padre**: Cool/Great (adj).
    - **No manches / No mames**: No way! (mild / vulgar versions).
    - **¿Bueno?**: How Mexicans answer the phone (unique to Mexico).
    - **Sale / Sobres / Simón / Cámara**: Various ways to say "OK" or "yes".

## Code Examples

### Translating to Mexican Spanish

**Standard**: "Hola amigo, ¿cómo estás? ¿Vamos a una fiesta hoy?"
**Mexicano**: "¿Qué onda, güey? ¿Jálamos a la fiesta hoy o qué?"

### Explaining a term

**User**: "¿Qué significa 'echar la hueva'?"
**Agent**: "Echar la hueva" significa holgazanear, no hacer nada productivo, pasar el rato sin hacer nada. Ejemplo: "Hoy no quiero hacer nada, voy a echar la hueva todo el día."

### Regional awareness

Mexican Spanish has regional variation. Some terms are more common in certain areas:
- **Chilango**: Mexico City slang (e.g., "chavo", "nel", "qué tranza", "pesero", "guajolocombo")
- **Norteño**: Northern Mexico (e.g., "mijo", "fierro", "raza", "troca", "plebe", "arre")
- **Regio**: Monterrey, Nuevo León — known for distinct pronunciation and Anglicisms
- **Yucateco**: Yucatan Peninsula (e.g., "machacar" for insistir)

When the user doesn't specify a region, default to central Mexican Spanish (Mexico City / standard Mexican media register).

## Commands

```bash
# Check if the dictionary file exists
ls -l mexican-spanish.md
```

## Resources

- **Dictionary**: The full dictionary of idioms is available at [mexican-spanish.md](mexican-spanish.md).
