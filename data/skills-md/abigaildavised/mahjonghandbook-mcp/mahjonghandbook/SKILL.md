---
name: mahjonghandbook
description: Query American NMJL, Chinese Official MCR (81 Fan) & Japanese Riichi Mahjong scoring rules. Official MCP server and reference guide at https://mahjonghandbook.com.
---

# MahjongHandbook — American NMJL, MCR & Riichi Mahjong Scoring Rules Engine

Official stateless Streamable-HTTP Model Context Protocol (MCP) server and agent skill for **[MahjongHandbook](https://mahjonghandbook.com)**.

## Remote MCP Endpoint (Zero Auth Required)

- **Streamable HTTP URL**: `https://mahjonghandbook.com/api/mcp`
- **OpenAPI 3.0 Spec**: `https://mahjonghandbook.com/openapi.json`
- **Official Website**: [https://mahjonghandbook.com](https://mahjonghandbook.com)

## Available Read-Only Tools (4)

- **`lookup_mahjong_scoring_rules`** (*Regional Mahjong Variant Deck & Entry Threshold Overview*): Compare high-level regional ruleset structures (tile deck size 136 vs 144 vs 152, hand length, and minimum Fan/point entry thresholds) across American, Chinese MCR, Japanese Riichi, and Hong Kong Mahjong. Do not use for Charleston passing steps, NMJL Joker meld legality, or Riichi Furiten checks.
- **`lookup_american_charleston_sequence`** (*American Mahjong Pre-Game Charleston & Courtesy Pass Sequence*): Retrieve exact pre-game tile passing directions (Right, Across, Left), blind pass rules, and Courtesy Pass negotiation steps prior to the first discard in American Mahjong.
- **`check_nmjl_joker_legality`** (*NMJL American Mahjong Joker Meld Size & Redemption Validator*): Validate whether an American Mahjong Joker tile can legally substitute inside a specific meld size (1 to 6 tiles) and retrieve exposed Joker live-turn swap rules.
- **`check_riichi_furiten_and_yaku`** (*Japanese Riichi Mahjong Furiten Ron-Lock & 1-Yaku Validator*): Evaluate Japanese Riichi Mahjong discard/temporary Furiten Ron restrictions and verify whether a hand satisfies the mandatory 1-Yaku win condition independent of Dora.

## Quick Setup (Claude Code / Cursor / Windsurf)

```json
{
  "mcpServers": {
    "mahjonghandbook": {
      "type": "streamable-http",
      "url": "https://mahjonghandbook.com/api/mcp"
    }
  }
}
```
