---
name: sgdk-rpg
description: Implement SGDK RPG party stats, equipment, inventory, abilities, status effects, turn order, battle resolution and progression. Use for RPG mechanics and their exploration/menu/save integration, rather than dialogue authoring or general UI alone.
---

# SGDK RPG

Build the game's rules as ordinary C, then connect them to SGDK's display,
input, audio and storage services. SGDK has no built-in party, battle or item
API. Preserve the project's architecture and chosen combat design.

## Start with the rules that matter

Establish party size, battle participants, targeting, action costs, turn/time
policy, progression and what defeat restores. Turn-based, active-time and action
RPGs need different clocks and interruption rules; do not turn one Lab's model
into a requirement for every RPG. Match the project's setting, artwork, music
and pacing. The example's coastal fantasy is illustrative.

Choose one complete loop to prove: prepare a party, enter an encounter, commit
an action, resolve its effects, apply the outcome once, then resume exploration.
Keep those rules independent of rendering where useful. Do not introduce a
universal game framework to demonstrate a small combat system.

## Use the relevant reference

- [Party and combat](references/party-and-combat.md): immutable definitions,
  derived stats, inventory transactions, targeting, turn order, status duration,
  seeded randomness, rewards and defeat recovery.
- [SGDK integration](references/integration.md): region-aware presentation,
  readable targeting, palette/VRAM/DMA budgets, sound ownership and checkpoints.
- [Adventure Lab](assets/adventure-lab/README.md): a standalone three-keeper RPG
  with exploration, equipment, consumables, three encounters and a boss.

Other installed skills are optional: `sgdk-ui` for shared menu/text foundations,
`sgdk-dialogue` for conversations, `sgdk-levels` for streamed exploration,
`sgdk-ai` for roaming enemies, `sgdk-save` for storage formats, and
`sgdk-performance` for measured bottlenecks. The Lab builds on its own.

## Keep the important contracts visible

- Keep definitions in ROM and mutable party/battle state bounded in RAM. Choose
  capacities for this game's content and report exhaustion; a console budget
  does not mandate a particular party size, level cap or battle formation.
- Derive equipment stats from base definitions and equipped IDs. Avoid repeatedly
  adding/removing bonuses from already-modified values.
- Validate the actor, target, item stock and MP before changing state or RNG.
  A rejected action must not consume resources or take a turn.
- Specify when order is sampled, which dead/removed participants are skipped,
  and when status durations decrease. Distinguish turns from display frames.
- Separate committing an action from presenting its result. Message pacing,
  target markers and animation must not apply damage or rewards again.
- Save semantic IDs and explicit bytes, not pointers, C struct images, sprite
  handles or transient battle effects. Validate a complete record before
  replacing the current campaign.

Use `ewrogers/sgdk:latest`, pulled before validation. Verify unfamiliar APIs in
its actual headers and source; the references were checked with SGDK 2.11 and
GCC 16.2.0. Treat the Lab's functions as game code, not SGDK API names.

## Prove the loop

Test missing MP/stock, invalid and fallen targets, healing caps, revival,
equipment changes, status expiry, skipped turns, deterministic ties/RNG,
zero-survivor defeat and exactly-once rewards. Check cancellation and message
acknowledgment without replaying an action. Exercise corrupt/interrupted
checkpoint recovery separately from battle rules.

Compile the actual adapters/resources in release and debug. Execute portable
rules on host and base M68000 when possible. Then playtest complete encounters:
targets should be distinct, attack messages readable, UI unobscured, and audio
and pause consistent. Host tests or ROM compilation cannot establish frame-time
headroom, VDP timing, SRAM retention or artistic quality on physical hardware.
