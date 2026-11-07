---
name: telegram-bot-accessibility
description: Audit and improve Telegram bot and Mini App accessibility, including readable labels, contrast, keyboard/focus behavior, forms, status announcements, localization and reduced motion. Use for accessible interaction requirements and acceptance checks; native Telegram rendering remains client-controlled.
---

# Accessible Telegram experiences

Read [the guide](references/guide.md) for native chat versus web responsibilities
and concrete accessibility criteria. Read [the acceptance scenarios](references/acceptance.md)
when reviewing a completed interface. [Sources](references/sources.md) distinguish
WCAG criteria from original recommendations and client limitations.

- A bot controls message content and keyboard labels, not Telegram's native DOM,
  focus ring or pixel target size. Keep text alternatives and test actual clients.
- Mini Apps control their HTML/CSS. Start with semantic elements, visible labels,
  predictable keyboard behavior, preserved form input and announced outcomes.
- Color, custom emoji, haptics and motion are supporting cues. Preserve meaning
  when any cue is absent; reserve red for destructive consequences, not dismissal.
- Check actual color pairs, focus visibility and reflow. An automated contrast
  result alone does not certify an interface's accessibility.

[scripts/contrast.py](scripts/contrast.py) checks opaque sRGB pairs and chooses
black/white text; [tests](scripts/test_contrast.py) exercise its numeric invariants.
Run `python -m unittest discover -s telegram-bot-accessibility/scripts`.
Combine with [bot UX](../telegram-bot-ux/SKILL.md) or
[Mini App design](../telegram-bot-miniapp-design/SKILL.md) to correct an interface.
Report observed defects, completed checks and remaining client/assistive-technology
checks rather than claiming universal compliance.
