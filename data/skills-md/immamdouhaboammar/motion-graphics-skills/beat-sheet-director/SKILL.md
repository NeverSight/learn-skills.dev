---
name: beat-sheet-director
description: Build frame-exact beat sheets and lock motion graphics timelines to speech audio or musical bars. Use when timing motion graphics to voiceover audio, creating frame-by-frame beat sheets, or locking cuts to musical drops and tempo grids.
---

# Beat Sheet Director

Structures motion graphics workflows around audio-first timing. Instead of placing keyframes arbitrarily and trying to fit audio later, the beat sheet locks visual events to speech cadence and musical bar grids.

## The Audio-First Protocol

1. **Speech Transcription and Timing**: Run speech through a whisper model (such as whisper-cpp) to extract exact word start and end timestamps.
2. **Tempo and Bar Grid Locking**: Calculate musical bar lengths based on tempo (for example, 100 BPM equals 2.4 seconds per 4/4 bar). Align visual scene changes with downbeats.
3. **Hero Event Isolation**: Guarantee that the primary climax or logo drop receives 60ms of isolated acoustic space with no competing sound effects.

## Standard Motion Graphics Beat Sheet Format

| Beat | Time Range | Duration | Spoken Phrase | Visual Choreography | Audio and SFX Cue |
|---|---|---|---|---|---|
| B1 | 0.00 to 0.50s | 0.50s | Silence | Camera wake and subtle ambient float | Atmospheric sub drone |
| B2 | 0.50 to 2.67s | 2.17s | Hook sentence | Main headline slams into center frame | High-frequency character click |
| B3 | 2.67 to 5.40s | 2.73s | Problem statement | UI card transforms into comparative chart | Soft card wipe sound |
| B4 | 5.40 to 6.60s | 1.20s | Core action | Button tap and numeric roll | Success bell chime |
| B5 | 6.60 to 11.20s | 4.60s | Delivery and proof | Product delivers in realistic perspective | Downbeat hit and bass swell |
| B6 | 11.20 to 15.10s | 3.90s | Value proposition | Narrative typography sequence | Melodic chord progression |
| B7 | 15.10 to 17.50s | 2.40s | Brand climax | Brand logo reveal and slogan | Solitary hero hit |
| B8 | 17.50 to 21.00s | 3.50s | Call to action | Contact details and end card | Reverb tail decay |

## Further Reading

- [references/tempo-math.md](references/tempo-math.md) for tempo to frame rate conversion tables.
