---
name: massageinchina
description: Look up Traditional Chinese Medicine (TCM) Tuina massage styles, meridian acupoints & phrases. Official MCP server and reference guide at https://massageinchina.com.
---

# MassageInChina — Authentic TCM Tuina, Acupressure Points & Bilingual Clinic Phrasebook

Official stateless Streamable-HTTP Model Context Protocol (MCP) server and agent skill for **[MassageInChina](https://massageinchina.com)**.

## Remote MCP Endpoint (Zero Auth Required)

- **Streamable HTTP URL**: `https://massageinchina.com/api/mcp`
- **OpenAPI 3.0 Spec**: `https://massageinchina.com/openapi.json`
- **Official Website**: [https://massageinchina.com](https://massageinchina.com)

## Available Read-Only Tools (4)

- **`lookup_tcm_acupoints_and_tuina`** (*TCM Tuina Acupoints & Clinic Modality Lookup*): Look up Traditional Chinese Medicine (TCM) Tuina massage modalities, blind clinical massage (Mangren Anmo), meridian acupoints, and RMB pricing.
- **`generate_mandarin_massage_phrase_card`** (*Bilingual Mandarin & Pinyin Massage Clinic Communication Card*): Generate ready-to-show Chinese character and Pinyin communication cards for adjusting pressure, specifying sore areas, or declining add-ons.
- **`compare_china_massage_venue_types`** (*Hospital TCM Dept vs Blind Tuina vs Foot Spa Chain Comparator*): Compare clinical rigor, typical RMB cost, tipping norms (zero tipping), and booking workflow across Chinese massage venue categories.
- **`check_tuina_cupping_contraindications`** (*Clinical Tuina, Cupping (Baguan) & Gua Sha Safety Checklist*): Check medical contraindications and travel timing tips before receiving deep orthopedic Tuina, fire cupping, or Gua Sha.

## Quick Setup (Claude Code / Cursor / Windsurf)

```json
{
  "mcpServers": {
    "massageinchina": {
      "type": "streamable-http",
      "url": "https://massageinchina.com/api/mcp"
    }
  }
}
```
