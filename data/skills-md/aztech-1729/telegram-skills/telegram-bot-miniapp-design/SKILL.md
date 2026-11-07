---
name: telegram-bot-miniapp-design
description: Design and implement Telegram Mini App visual systems, theme-aware colors, button hierarchy, responsive forms, safe-area layouts and native control lifecycles. Use for browser interface styling and interaction states; use miniapps for signed authentication and backend integration.
---

# Mini App interface design

Read [the design guide](references/guide.md) for theme tokens, action roles,
responsive components and native controls. Read [screen patterns](references/patterns.md)
for forms, lists, checkout and state design. Preserve the existing product's brand
and components when improving a project.

- Derive surfaces and text from Telegram theme variables with usable browser
  fallbacks. Test real pairs for contrast; a token named "hint" isn't guaranteed
  readable body text. Handle runtime theme changes and all four content safe insets.
- Emphasize the main task, keep secondary actions quiet, and reserve danger for
  destructive consequences. Back and Cancel are normally neutral. Use text and
  state together with color.
- Give fields persistent labels, errors and retained input. Show loading, empty,
  denied, offline, uncertain and successful states from actual application results.
- Feature-detect native APIs, register each handler once and clean it up when its
  screen leaves. A client color API cannot change bot keyboard RGB.
- Start with semantic HTML, fluid layout, visible focus and touch-friendly controls.
  Use [accessibility](../telegram-bot-accessibility/SKILL.md) for detailed criteria
  and [Mini Apps](../telegram-bot-miniapps/SKILL.md) for trusted identity/session work.

[assets/theme.css](assets/theme.css) is an extractable theme/layout starting point,
not a complete app. The authenticated [todo frontend](../telegram-bot-miniapps/assets/todo/index.html)
provides a working form/list integration. [Sources](references/sources.md) record
the checked platform baseline. Validate in target WebViews before claiming an
exact native appearance or accessibility result.
