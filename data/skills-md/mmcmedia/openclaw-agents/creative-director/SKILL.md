---
name: creative-director
description: Analyze songs (lyrics, mood, genre, tempo) and create detailed scene-by-scene storyboards for music videos. Use when planning music video content, mapping visuals to lyrics, or creating video concepts for PsalMix songs or any music video production.
---

# Creative Director - Music Video Storyboarding

Analyze songs and create detailed scene-by-scene visual plans for music video production.

## Workflow

### 1. Analyze the Song

**Required inputs:**
- Song MP3 file or audio URL
- Lyrics (plain text or .srt file)
- Optional: Artist name, genre, target audience

**Analysis steps:**
1. **Listen/analyze** the audio:
   - Tempo (BPM)
   - Mood (uplifting, contemplative, energetic, peaceful, etc.)
   - Genre (worship, gospel, contemporary Christian, etc.)
   - Key musical moments (chorus, bridge, climax, intro/outro)

2. **Read the lyrics**:
   - Identify themes (faith, praise, struggle, redemption, etc.)
   - Find visual keywords (mountains, light, water, hands, etc.)
   - Note emotional shifts throughout the song
   - Map structure (verse, chorus, bridge)

3. **Define visual direction**:
   - Color palette (warm/cool, saturated/muted)
   - Visual themes (nature, urban, abstract, narrative)
   - Energy level (calm/dynamic, simple/complex)
   - Brand consistency (PsalMix styling if applicable)

### 2. Create Scene-by-Scene Storyboard

**Output format:** JSON scene plan

```json
{
  "song": {
    "title": "Song Title",
    "artist": "Artist Name",
    "duration": 210,
    "bpm": 120,
    "genre": "Contemporary Christian",
    "mood": "Uplifting, contemplative",
    "themes": ["faith", "hope", "redemption"]
  },
  "visualDirection": {
    "colorPalette": ["#3A5A78", "#F4E1C1", "#8B4513"],
    "style": "cinematic nature footage with lyric overlays",
    "energy": "calm to dynamic build"
  },
  "scenes": [
    {
      "sceneNumber": 1,
      "timestamp": "0:00-0:15",
      "lyrics": "In the morning light...",
      "lyricSection": "intro",
      "visualTheme": "sunrise over mountains",
      "clipKeywords": ["sunrise", "mountains", "golden hour", "peaceful"],
      "mood": "peaceful, hopeful",
      "transitions": "slow fade in",
      "lyricDisplay": "bottom center, white text with shadow"
    },
    {
      "sceneNumber": 2,
      "timestamp": "0:15-0:45",
      "lyrics": "You lift me up when I am weak...",
      "lyricSection": "verse 1",
      "visualTheme": "person walking through nature",
      "clipKeywords": ["walking", "forest path", "sunlight through trees"],
      "mood": "contemplative, building",
      "transitions": "crossfade",
      "lyricDisplay": "karaoke style, word-by-word highlight"
    }
  ]
}
```

### 3. Scene Mapping Guidelines

**Timing:**
- Match scene transitions to musical beats/phrases
- Allow 3-5 second minimum per scene for readability
- Sync climactic visuals to musical peaks

**Visual variety:**
- Mix wide shots and close-ups
- Alternate between abstract and concrete imagery
- Balance static and dynamic footage
- Consider 60/40 rule: 60% b-roll, 40% lyrics focus

**Lyric display options:**
- Full screen centered (worship style)
- Bottom third karaoke
- Word-by-word highlight (engaging)
- No lyrics (instrumental sections)
- Split screen (lyrics + video)

**Keyword selection for clip sourcing:**
- Be specific enough to find relevant footage
- Include 3-5 keywords per scene
- Consider motion verbs (flowing, soaring, walking)
- Mix concrete + abstract concepts

### 4. Brand Consistency (PsalMix)

When creating videos for PsalMix:
- **Logo placement:** Lower right corner throughout
- **Color scheme:** Clean, family-friendly aesthetics
- **Typography:** Readable sans-serif fonts (Montserrat, Open Sans)
- **Content safety:** G-rated visuals only, positive themes
- **End card:** Include PsalMix logo + "Stream clean music at psalmix.com"

## Reference Files

For detailed examples of effective scene plans, see:
- `references/example-storyboards.md` - Sample scene plans for different genres/moods
- `references/visual-themes.md` - Common visual motifs and their meanings
- `references/pexels-search-tips.md` - How to write effective Pexels search keywords

## Deliverables

1. **JSON scene plan** (primary output) - Machine-readable for video-asset-manager
2. **Human-readable summary** - Overview of creative direction for stakeholder review
3. **Visual mood board** (optional) - Example images representing the direction

## Quality Checklist

Before finalizing the scene plan:
- [ ] Every scene has clear keywords for clip sourcing
- [ ] Timing matches song structure (verse/chorus/bridge)
- [ ] Visual variety (no repetitive scenes)
- [ ] Lyric display style specified for each scene
- [ ] Color palette and mood are consistent
- [ ] Brand guidelines followed (if applicable)
- [ ] Transitions specified between scenes
- [ ] Total scene count = 8-15 scenes for typical 3-4 min song
