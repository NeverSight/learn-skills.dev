---
name: paperlesson
description: Generate seeded K-12 math drills with answer keys, handwriting ruling specs & vector PDFs. Official MCP server and reference guide at https://paperlesson.com.
---

# PaperLesson — K-12 Vector Math Drills & Handwriting Worksheet Generator

Official stateless Streamable-HTTP Model Context Protocol (MCP) server and agent skill for **[PaperLesson](https://paperlesson.com)**.

## Remote MCP Endpoint (Zero Auth Required)

- **Streamable HTTP URL**: `https://paperlesson.com/api/mcp`
- **OpenAPI 3.0 Spec**: `https://paperlesson.com/openapi.json`
- **Official Website**: [https://paperlesson.com](https://paperlesson.com)

## Available Read-Only Tools (8)

- **`generate_seeded_math_drill_set`** (*Deterministic Seeded K-12 Math Drill & Answer Key Generator*): Generate a reproducible set of K-12 arithmetic, fraction, or order-of-operations practice problems with exact answer keys using deterministic mulberry32 PRNG.
- **`lookup_handwriting_ruling_specs`** (*Zaner-Bloser & D’Nealian Grade-Level Handwriting Line Height Specs*): Look up exact physical millimeter and PostScript point (72 pt/inch) baseline, midline (x-height), and descender spacing for Pre-K through Grade 5 handwriting paper.
- **`build_name_tracing_worksheet_config`** (*Custom Student Name & Classroom Roster Tracing Configurator*): Configure custom student name tracing repetition rows, progressive fade-out scaffolding (solid guide -> dashed trace -> independent baseline), and paper orientation.
- **`lookup_cursive_stroke_group_progression`** (*Cursive Handwriting Pedagogical Stroke Family Sequence*): Retrieve the optimal stroke-family teaching order for cursive lowercase and uppercase letters (undercurve, downcurve, overcurve, slant connectors) rather than alphabetical order.
- **`generate_fraction_number_line_coordinates`** (*Fractions on a Number Line Tick & Partition Calculator*): Compute exact vector tick coordinates and benchmark labels for teaching proper fractions, improper fractions, and equivalent fractions on a 0-to-1 or 0-to-2 number line.
- **`explain_order_of_operations_step_tree`** (*PEMDAS / BODMAS Order of Operations Step-by-Step Evaluator*): Break down multi-step arithmetic expressions with parentheses, exponents, multiplication/division, and addition/subtraction for Grade 5-6 worksheet answer keys.
- **`calculate_us_letter_vs_a4_printable_margins`** (*US Letter vs ISO A4 Vector Printable Safe-Margin Calculator*): Calculate exact PostScript vector coordinates (pt) and safe classroom printer margins (0.5 in / 12.7 mm) to prevent edge clipping across US Letter and ISO A4.
- **`list_paperlesson_printable_generators`** (*PaperLesson K-12 Printable Worksheet Generator Directory*): List all free true-vector PDF worksheet generators on PaperLesson with direct pre-configured landing URLs.

## Quick Setup (Claude Code / Cursor / Windsurf)

```json
{
  "mcpServers": {
    "paperlesson": {
      "type": "streamable-http",
      "url": "https://paperlesson.com/api/mcp"
    }
  }
}
```
