---
name: arg-designer
description: "Comprehensive ARG (Alternate Reality Game) design toolkit for creating immersive puzzle experiences. This skill should be used when: (1) Designing an ARG or puzzle trail from scratch, (2) Creating hidden content with ciphers, steganography, or encoding, (3) Building trailheads (entry points) to hidden content, (4) Connecting puzzle elements in a cohesive narrative, (5) Implementing specific ciphers or encoding methods, (6) Choosing platforms for ARG deployment (Discord, Twilio, YouTube), (7) Reviewing ARG design for TINAG principles. MANDATORY TRIGGERS: ARG, alternate reality game, puzzle trail, cipher, steganography, hidden message, trailhead, TINAG, puzzle hunt, transmedia, unfiction, encode message, hide data"
---

# ARG Designer

Design immersive Alternate Reality Games by combining hiding methods, trailheads, connectors, and narrative principles.

## Core Workflow

### Phase 1: Define the Payload
Identify content to be discovered: TEXT (messages, URLs, passwords), AUDIO (recordings, hidden data), IMAGE (photos, QR codes), VIDEO (frame-hidden content), FILE (documents, archives).

### Phase 2: Choose Hiding Method
Select from `references/hiding-methods.md` based on difficulty (1-5), content type, required tools, and narrative fit.

### Phase 3: Design Trailhead
Create entry point using `references/trailheads.md`. Must feel organic to fictional world and reward observation.

### Phase 4: Build Connectors
Link elements using `references/connectors.md`. Each puzzle output becomes next puzzle input.

### Phase 5: Apply Design Principles
Review against `references/design-principles.md` for TINAG compliance and mimesis preservation.

## Quick Reference

### Cipher Selection
| Difficulty | Ciphers |
|------------|---------|
| 1 (Easy) | Caesar, ROT13, Atbash, Reverse |
| 2 (Medium) | Vigenère, Rail Fence, Base64, Morse |
| 3 (Hard) | Playfair, Nihilist, Book Cipher |
| 4 (Expert) | Custom multi-layer systems |

Full cipher details: `references/ciphers.md`

### Hiding Methods by Content
| Content | Methods |
|---------|---------|
| TEXT | Unicode steganography, EXIF metadata, HTML comments |
| IMAGE | LSB steganography, layer hiding, QR codes |
| AUDIO | Spectrograms, reversed audio, DTMF tones |
| VIDEO | Frame insertion, subtitle tracks, timecodes |
| FILE | Nested archives, polyglot files |

Full hiding methods: `references/hiding-methods.md`

### Platform Selection
| Use Case | Platforms |
|----------|-----------|
| Real-time | Discord, Telegram |
| Phone/voice | Twilio IVR |
| Narrative | Dreamwidth, WordPress |
| Drops | Pastebin, GitHub |

Full platform guide: `references/platforms.md`

## Recipe Pattern

```
[CONTENT] → [HIDING] → [TRAILHEAD] → [CONNECTOR] → [NEXT]
```

Example: `Story fragment → Spectrogram → YouTube audio → Phone number → Twilio IVR → Password`

See complete examples: `references/recipes.md`

## Resources

### scripts/
- `cipher_tools.py` - Encode/decode Caesar, ROT13, Atbash, Vigenère, Rail Fence, Base64, Morse, Binary, Hex
- `steganography.py` - LSB image hiding, metadata hiding, Unicode zero-width encoding
- `spectrogram.py` - Convert images/text to audio spectrograms

### references/
- `ciphers.md` - 30+ cipher types with implementations and tools
- `hiding-methods.md` - 60+ techniques by content type
- `trailheads.md` - 40+ entry point patterns
- `connectors.md` - Puzzle linking methods
- `platforms.md` - Platform setup guides
- `design-principles.md` - TINAG, Crimes Against Mimesis, puppetmaster role, player types, pacing
- `meta-puzzles.md` - Meta-puzzle structures, gating mechanics, puzzle hunt architecture
- `recipes.md` - Complete puzzle chains from famous ARGs (I Love Bees, Cicada 3301, Year Zero)
