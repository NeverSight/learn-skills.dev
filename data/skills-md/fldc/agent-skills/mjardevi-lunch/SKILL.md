---
name: mjardevi-lunch
description: Hämta dagens lunchmenyer från restauranger i Mjärdevi via Luncha I Mjärdevi API. Använd när användaren frågar efter dagens lunch, lunchmeny eller vad som serveras idag i Mjärdevi.
---

# Mjärdevi Lunch

Hämtar och visar dagens lunchmeny från alla restauranger i Mjärdevi genom Luncha I Mjärdevi API.

## Quick Start

### 1. Konfigurera API-nyckel

Rekommenderat: sätt API-nyckeln i en miljövariabel:

```bash
export MJARDEVI_LUNCH_API_KEY="your_api_key_here"
```

Lokal fallback: lägg till nyckeln i `~/.config/ehh-skills/config.env`, men redigera filen manuellt i en editor i stället för att skriva hemligheter direkt på kommandoraden.

Scriptet läser också `LUNCHA_I_MJARDEVI_API_KEY` eller `API_KEY` i samma fil om du föredrar andra namn.

**Skaffa API-nyckel:**
Registrera en gratis API-nyckel på: https://lunchaimjardevi.com/api/

### 2. Kör scriptet

```bash
python scripts/get_lunch.py [format]
```

**Parametrar:**
- `format`: `text` (standard) eller `json`

Scriptet läser API-nyckeln i denna ordning:
1. `MJARDEVI_LUNCH_API_KEY`
2. `LUNCHA_I_MJARDEVI_API_KEY`
3. `API_KEY`
4. `~/.config/ehh-skills/config.env`

**Exempel:**
```bash
# Använd API-nyckel från miljövariabel eller ~/.config/ehh-skills/config.env
python scripts/get_lunch.py

# Få JSON-output
python scripts/get_lunch.py json
```

Undvik att ange API-nyckeln direkt på kommandoraden eftersom den kan hamna i shell-historik eller processlistor.

## Workflow

1. **Kör scriptet** - Använd `scripts/get_lunch.py` för att hämta dagens menyer
2. **Presentera resultatet** - Scriptet formaterar automatiskt outputen på ett lättläst sätt
3. **Hantera fel** - Scriptet hanterar vanliga fel som:
   - Restaurang stängd
   - Meny ej upplagd än
   - Nätverksproblem
   - Saknad API-nyckel

## Output Format

Scriptet genererar en formaterad lista med:
- Restaurangnamn
- Dagens lunchrätter med beskrivningar
- Eventuella noteringar (t.ex. semesterstängt)
- Felmeddelanden om meny inte är tillgänglig

**Exempel på output:**
```
# Dagens lunch i Mjärdevi - 2026-02-16

## Brödernas Kök

**Fransk kycklinggryta**
  Kycklinggryta serveras med potatispuré

**Laxpudding**
  Laxpudding serveras med skirat smör, dillkräm & citron
```

## API Details

För detaljerad API-dokumentation, se `references/api.md`. API:et tillhandahålls av Luncha I Mjärdevi och uppdateras automatiskt varje timme mellan 00-13 på vardagar.

**Viktiga punkter:**
- Menyer kan saknas om restaurangen är stängd eller inte uppdaterat sin webbplats än
- Vissa restauranger har statiska menyer (ändras inte automatiskt)
- API:et inkluderar både vanliga restauranger och foodtrucks
