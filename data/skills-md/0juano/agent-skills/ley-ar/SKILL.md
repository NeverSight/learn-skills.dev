---
name: ley-ar
description: >
  Search Argentine legal databases (SAIJ, JUBA, CSJN, JUSCABA) for jurisprudence,
  legislation, case summaries, and doctrine using the `ley` CLI.
  Use when the user asks about Argentine law, court decisions, legal precedents,
  fallos, jurisprudencia, legislación, or mentions SAIJ, JUBA, CSJN, JUSCABA.
  Supports parallel search across databases, JSON/table/text output, and filtering
  by jurisdiction. Built from reverse-engineered MCP servers (hernan-cc) — direct
  HTTP calls, no MCP layer needed.
---

# ley-ar — Argentine Legal Database Search

Search jurisprudence, legislation, and doctrine from 4 public Argentine legal databases.

## Installation

```bash
cd {baseDir}/scripts && pip install -e . --break-system-packages -q
```

Requires Python 3.10+. Dependencies: typer, httpx, rich.

## Databases

| DB | Source | Best For | Reliability |
|---|---|---|---|
| `saij` | saij.gob.ar | National jurisprudence, legislation, doctrine | ✅ Clean JSON API |
| `csjn` | sjconsulta.csjn.gov.ar | Supreme Court summaries | ✅ HTML+JSON |
| `juba` | juba.scba.gov.ar | Buenos Aires Province decisions | ⚠️ HTML scraping |
| `juscaba` | eje.juscaba.gob.ar | CABA court cases/expedientes | ⚠️ Poor free-text |

**Default strategy:** Start with `--db saij,csjn`. Add `juba` only for PBA-specific queries. Use `juscaba` only with case IDs.

## Commands

```bash
# Search all databases (parallel)
ley search "prescripción adquisitiva"

# Filter by database(s)
ley search "daño moral" --db saij,csjn

# Limit results
ley search "phishing bancario" --db saij --limit 5

# JSON output for scripting
ley search "responsabilidad civil" --db csjn --json

# Plain text
ley search "contrato de locación" --text

# Status check
ley status
ley --version
```

## Search Tips

- Use legal terminology: "daños y perjuicios" not "accidente de auto"
- Be specific: "prescripción adquisitiva inmueble" > "prescripción"
- **"Patentes" ambiguity:** returns IP patents, not vehicle tax. Use "impuesto automotor" or "radicación automotor" instead.
- For current tax rates or alícuotas, use web search — these databases index case law, not regulatory info.

## Output

Each result: `db`, `id`, `title`, `date`, `snippet`, `url`. Default: Rich table. `--json` for structured data.

## Limitations

- JUBA depends on ASP.NET WebForms scraping — breaks if site changes
- CSJN full case text may need reCAPTCHA (summaries work)
- JUSCABA works best with case identifiers, not free-text
- No auth required — all public APIs
- Respect rate limits: avoid rapid-fire queries
