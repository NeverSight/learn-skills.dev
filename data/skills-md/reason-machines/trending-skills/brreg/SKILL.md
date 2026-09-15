---
name: brreg
description: Search and retrieve Norwegian company data from Brønnøysundregistrene (the Norwegian Business Registry). Access all ~1.2 million registered companies in Norway.
---

# Norwegian Business Registry (Brreg)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

Access the official open API from Brønnøysundregistrene to search and retrieve data about all registered companies in Norway.

## When to Use

- When the user asks about Norwegian companies
- When searching for company information in Norway
- When looking up organization numbers (organisasjonsnummer)
- When finding companies by name, location, industry, or other criteria
- When checking company status (bankruptcy, dissolution, etc.)

## API Base URL

```
https://data.brreg.no/enhetsregisteret/api
```

## Key Endpoints

### Search Companies (Enheter)

```bash
curl "https://data.brreg.no/enhetsregisteret/api/enheter?navn=SEARCH_TERM&size=20"
```

**Common parameters:**
| Parameter | Description |
|-----------|-------------|
| `navn` | Company name (partial match) |
| `organisasjonsnummer` | 9-digit org number (comma-separated for multiple) |
| `organisasjonsform` | Organization type: AS, ENK, NUF, ANS, DA, etc. |
| `naeringskode` | Industry code (NACE) |
| `kommunenummer` | 4-digit municipality code |
| `postadresse.postnummer` | Postal code |
| `forretningsadresse.postnummer` | Business address postal code |
| `konkurs` | true/false - bankruptcy status |
| `underAvvikling` | true/false - dissolution status |
| `registrertIMvaregisteret` | true/false - VAT registered |
| `fraAntallAnsatte` | Minimum employees |
| `tilAntallAnsatte` | Maximum employees |
| `fraRegistreringsdatoEnhetsregisteret` | Registration date from (YYYY-MM-DD) |
| `tilRegistreringsdatoEnhetsregisteret` | Registration date to (YYYY-MM-DD) |
| `size` | Results per page (default: 20, max depth: 10000) |
| `page` | Page number (0-indexed) |

### Get Company by Org Number

```bash
curl "https://data.brreg.no/enhetsregisteret/api/enheter/123456789"
```

### Search Sub-entities (Underenheter)

Branch offices and departments:

```bash
curl "https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet=123456789"
```

### Get Organization Forms

List all valid organization types:

```bash
curl "https://data.brreg.no/enhetsregisteret/api/organisasjonsformer"
```

**Common organization forms:**
| Code | Description |
|------|-------------|
| AS | Aksjeselskap (Private limited company) |
| ASA | Allmennaksjeselskap (Public limited company) |
| ENK | Enkeltpersonforetak (Sole proprietorship) |
| NUF | Norskregistrert utenlandsk foretak (Foreign enterprise) |
| ANS | Ansvarlig selskap (General partnership) |
| DA | Selskap med delt ansvar (Shared liability partnership) |
| SA | Samvirkeforetak (Cooperative) |
| STI | Stiftelse (Foundation) |

### Get Recent Updates

Track new registrations and changes:

```bash
curl "https://data.brreg.no/enhetsregisteret/api/oppdateringer/enheter?dato=2024-01-01T00:00:00.000Z"
```

## Bulk Downloads

Complete datasets (updated nightly ~05:00 AM):

| Format | URL |
|--------|-----|
| JSON (gzipped) | https://data.brreg.no/enhetsregisteret/api/enheter/lastned |
| CSV | https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv |
| Excel | https://data.brreg.no/enhetsregisteret/api/enheter/lastned/regneark |

## Example Queries

### Find all AS companies in Oslo with 50+ employees

```bash
curl "https://data.brreg.no/enhetsregisteret/api/enheter?organisasjonsform=AS&kommunenummer=0301&fraAntallAnsatte=50&size=100"
```

### Search for tech companies

```bash
curl "https://data.brreg.no/enhetsregisteret/api/enheter?navn=tech&size=50"
```

### Find companies registered this year

```bash
curl "https://data.brreg.no/enhetsregisteret/api/enheter?fraRegistreringsdatoEnhetsregisteret=2024-01-01&size=100"
```

### Get all subsidiaries of a company

```bash
curl "https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet=923609016"
```

## Response Format

Responses are in HAL+JSON format with `_embedded` containing results and `page` containing pagination info:

```json
{
  "_embedded": {
    "enheter": [
      {
        "organisasjonsnummer": "123456789",
        "navn": "Company Name AS",
        "organisasjonsform": {
          "kode": "AS",
          "beskrivelse": "Aksjeselskap"
        },
        "antallAnsatte": 50,
        "forretningsadresse": {
          "adresse": ["Street 1"],
          "postnummer": "0150",
          "poststed": "OSLO",
          "kommune": "OSLO",
          "kommunenummer": "0301"
        },
        "naeringskode1": {
          "kode": "62.010",
          "beskrivelse": "Programmeringstjenester"
        }
      }
    ]
  },
  "page": {
    "size": 20,
    "totalElements": 150,
    "totalPages": 8,
    "number": 0
  }
}
```

## Notes

- API is free and open (NLOD license)
- No authentication required for public data
- Rate limiting may apply for heavy usage
- Results limited to 10,000 per query (use bulk downloads for complete data)
- Data updated continuously during business hours

## Documentation

- Official API docs: https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html
- OpenAPI spec: https://raw.githubusercontent.com/brreg/openAPI/master/specs/enhetsregisteret.json
