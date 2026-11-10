---
name: wow-api-quests
description: Look up WoW Quest, Quest Log, Quest Info, Quest Offer, Quest
  Session, Quest Task, Campaign, Content Tracking, Quest Hub, and Quest Line
  APIs. Covers C_QuestLog (70+ functions for quest state, objectives, tracking,
  completion), C_QuestInfoSystem (quest type/tag info), C_QuestOffer (quest
  accept/decline), C_QuestSession (party sync quests), C_QuestTaskInfo (bonus
  objectives/world quests), C_ContentTracking, C_CampaignInfo, C_QuestHubUI,
  C_QuestLineUI, C_QuestItemUse, C_WarCampaign (legacy), quest POI functions,
  and quest gossip patterns. Use when working with quest tracking, quest log
  display, quest objectives, quest accept/complete flows, world quests, campaign
  progress, bonus objectives, or content tracking systems. Select Retail,
  Forever, or Classic with wow-client-targets before using historical listings.
---

# api quests

Use for any selected combination of Retail, Forever, and Classic progression. First resolve the target and pinned source with [wow-client-targets](../wow-client-targets/SKILL.md).

## Target-specific decisions

Verify quest log identifiers, objective structures, offer/turn-in APIs and async quest loading. Handle absent campaign/world-quest systems explicitly.

Read the relevant row in [compatibility guidance](../wow-client-targets/references/COMPATIBILITY.md). Verify only the APIs needed for this task, using commit-pinned definitions and loaded client code. Missing evidence means unknown, not supported or removed. When offline, disclose the snapshot version/date and unresolved behavior.

## Detailed lookup material

Use the [pinned source schemas](references/generated/README.md) for complete generated contracts in this domain, including typed arguments, returns, event payloads and restrictions. Query only the needed symbols. Source declarations leave loading, runtime behavior and addon permission unresolved unless separately verified.

The [historical Retail baseline](references/RETAIL-BASELINE.md) retains the original API listings and examples. It is a research aid, not current or cross-client verification. Open only relevant supporting references:

- Start with the pinned source schemas; use the baseline for historical context and verify handwritten helpers separately.

For implementation and release validation, use [wow-addon-development](../wow-addon-development/SKILL.md).
