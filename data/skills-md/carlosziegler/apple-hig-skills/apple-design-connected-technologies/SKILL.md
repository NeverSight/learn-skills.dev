---
name: apple-design-connected-technologies
description: "Design Apple HIG experiences for connected technologies such as CarPlay, HomeKit, maps, iCloud, NFC, and iMessage apps or stickers. Use when integration behavior changes the user experience."
---

# Apple Connected Technology UX

## Apply the skill

Identify the specific integration and read its reference; these technologies have different tasks, environments, and failure modes. Preserve native setup, naming, and interaction patterns where available.

Design for unavailable connectivity, incompatible devices, limited permission, and interrupted operations when those states apply. Separate local changes from remote state and make the visible result truthful. Keep the person’s surroundings and attention demands in mind, especially for driving and physical-world interactions.

Verify current capability, entitlement, regional, and API requirements before implementation. Specify the integration design without sending messages, changing home accessories, or modifying remote data unless the user separately authorized that action.

## Topic references

Select the topic that matches the design decision; do not load this entire list by default.

- [CarPlay](references/carplay.md)
- [HomeKit](references/homekit.md)
- [Maps](references/maps.md)
- [iCloud](references/icloud.md)
- [NFC](references/nfc.md)
- [iMessage apps and stickers](references/imessage-apps-and-stickers.md)

## Source use

These references are original operational summaries of Apple’s public HIG, checked on 2026-09-08. They are guidance for design decisions, not a reproduced manual or a guarantee of App Store acceptance.

Read only the topic references relevant to the current task. Each links to the full official page. Consult that page for exact specifications, platform exceptions, assets, and version-sensitive behavior; use current official developer documentation for APIs and availability. If live documentation is unavailable, state the snapshot date and identify assumptions instead of inventing current requirements.

The user’s product goals, selected framework, and authorized scope remain controlling. Distinguish a source recommendation from a hard platform requirement and from your own proposed implementation.
