---
name: concierge
description: Personal AI concierge for contact lookup, availability checks, and autonomous phone calls
version: 1.5.0
triggers:
  - find contact
  - hotel contact
  - accommodation contact
  - property contact
  - airbnb contact
  - booking contact
  - vrbo contact
  - expedia contact
  - direct booking
  - property email
  - property phone
  - call hotel
  - call property
  - call business
  - direct booking call
  - search hotels
  - find hotels
  - hotel search
  - find business contact
  - check availability
  - hotel availability
  - room availability
---

# Concierge

Find contact details (phone, email, WhatsApp, Instagram, etc.) for listings and businesses, search for places via Google Places, check availability on Booking.com, and place autonomous AI phone calls.

## Capabilities

### 1) Find contacts or search for places

The unified `find` command auto-detects whether you pass a listing URL or a text query.

```bash
# URL → contact dossier (same as old find-contact)
concierge find "https://www.airbnb.com/rooms/12345"

# Text query → search Google Places
concierge find "hotels in San Francisco" --limit 5
concierge find "Trisara Resort Phuket"
concierge find "37.7749,-122.4194" --radius-m 5000 --type hotel

# Enrich multi-result with website scraping (slower)
concierge find "hotels in Phuket" --limit 3 --enrich
```

**Aliases:** `find-contact`, `fc`, `search`, `s`

**Options (text search):**
- `-l, --limit <n>` - Max results (default: 10, max: 20)
- `--min-rating <n>` - Minimum rating (0-5)
- `--type <type>` - Place type: lodging, hotel, resort_hotel (default: lodging)
- `--radius-m <meters>` - Search radius for coordinate searches
- `--enrich` - Scrape websites for email/social (auto-enabled for single results)

**Options (URL lookup):**
- `--html <file>` - Path to saved HTML file (for offline/pre-fetched content)

**Search backend:** Prefers `goplaces` CLI. Falls back to direct Google Places API (1 result max) if configured.

### 3) Check hotel availability on Booking.com

```bash
concierge check-availability "Park Hyatt Tokyo" -i 2024-03-15 -o 2024-03-17
concierge ca "https://www.booking.com/hotel/us/hilton.html" -i 2024-03-15 -o 2024-03-17 --json
concierge availability "Hilton NYC" -i 2024-04-01 -o 2024-04-03 -g 3 --screenshot results.png
```

**Options:**
- `-i, --check-in <date>` - Check-in date (YYYY-MM-DD) **required**
- `-o, --check-out <date>` - Check-out date (YYYY-MM-DD) **required**
- `-g, --guests <n>` - Number of guests (default: 2)
- `-r, --rooms <n>` - Number of rooms (default: 1)
- `-s, --screenshot <path>` - Save screenshot of results
- `--headed` - Show browser window (for debugging)

**Requires:** `agent-browser` CLI installed (with Playwright browsers)

### 4) Place an autonomous phone call

```bash
concierge call "+1-555-123-4567" \
  --goal "Book a room for March 12-14" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --context "Prefer direct booking if rate beats Booking.com"
```

The `call` command now auto-manages infra by default: if local server is down, it starts `ngrok` + call server automatically and stops both when the call ends.

### 5) Direct-booking negotiation (minimal inputs)

Uses customer defaults from config and only needs dates plus optional Booking.com price and room type.

```bash
concierge direct-booking "+6676310100" \
  --hotel "Trisara Resort" \
  -i 2026-05-06 -o 2026-05-09 \
  --room "Ocean View Pool Junior Suite" \
  --booking-price 115000 \
  --currency THB
```

If `--room` is omitted, the assistant asks for the cheapest available room.  
If `--booking-price` is omitted, it negotiates for the best direct rate and value-adds.

## Supported listing platforms

- **Airbnb**: `airbnb.com/rooms/...`
- **Booking.com**: `booking.com/hotel/...`
- **VRBO**: `vrbo.com/...`
- **Expedia**: `expedia.com/...Hotel...`

## Examples

### Find contacts for an Airbnb listing
Run:
```bash
concierge find "https://www.airbnb.com/rooms/12345"
```

### Search for hotels in a city
Run:
```bash
concierge find "hotels in Tokyo" --limit 5 --min-rating 4
```

### Search with full enrichment
Run:
```bash
concierge find "hotels in Phuket" --limit 3 --enrich
```

### Check availability for a specific hotel
Run:
```bash
concierge ca "Hilton Garden Inn Times Square" -i 2024-05-01 -o 2024-05-03
```

### Start a call and control turns manually
Run:
```bash
concierge call "+1-555-123-4567" \
  --goal "Negotiate a direct booking rate" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --interactive
```

### Direct-booking negotiation with config defaults
Run:
```bash
concierge direct-booking "+6676310100" \
  --hotel "Trisara Resort" \
  -i 2026-05-06 -o 2026-05-09 \
  --booking-price 115000 \
  --currency THB
```

### JSON output for scripting
```bash
concierge find --json "https://..."
concierge find --json "hotels in Tokyo" --limit 5
```

### Verbose output
```bash
concierge --verbose find "https://..."
```

## Configuration

The CLI stores configuration in:

`~/.config/concierge/config.json5`

### Optional for contact lookup

```bash
concierge config set googlePlacesApiKey "your-key"
```

### Required for AI phone calls

```bash
concierge config set twilioAccountSid "<sid>"
concierge config set twilioAuthToken "<token>"
concierge config set twilioPhoneNumber "+14155551234"
concierge config set deepgramApiKey "<key>"
concierge config set elevenLabsApiKey "<key>"
concierge config set elevenLabsVoiceId "EXAVITQu4vr4xnSDxMaL"
concierge config set anthropicApiKey "<key>"

# Customer defaults for direct-booking
concierge config set customerName "Derek Rein"
concierge config set customerEmail "derek@example.com"
concierge config set customerPhone "+1-555-000-1111"

# Optional for auto ngrok auth
concierge config set ngrokAuthToken "<token>"
```

Check values:

```bash
concierge config show
```

## External Dependencies

| Feature | Required CLI | Install |
|---------|-------------|---------|
| `find` (text search) | `goplaces` | See goplaces documentation |
| `check-availability` | `agent-browser` | `npm install -g agent-browser && npx playwright install chromium` |
| `call` | `ffmpeg`, `ngrok` | `brew install ffmpeg ngrok` |

## Notes

- Contact extraction uses publicly available information.
- `find` (text search) uses Google Places API via the `goplaces` CLI, with fallback to direct API.
- `check-availability` uses browser automation to scrape Booking.com. Results depend on DOM structure which may change.
- `call` validates local dependencies before dialing (`ffmpeg` with MP3 decode support, and `ngrok` when auto-infra is needed).
- `call` runs preflight checks for Twilio, Deepgram, and ElevenLabs quota before dialing.
- When auto infra is used, server/ngrok logs are written under `~/.config/concierge/call-runs/<run-id>/`.
