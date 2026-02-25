---
name: community-campaign-builder
description: Build grassroots political campaign strategies integrating music promotion, community networking, and multi-platform outreach. Use when creating independent MP campaigns, community advocacy campaigns, or grassroots political movements requiring music-driven promotion and social media automation.
license: Proprietary - Sovereign Systems
metadata:
  author: PrecisePointway
  version: "1.0.0"
compatibility: Requires WhatsApp Web access, Suno account, GitHub CLI, browser automation
allowed-tools: Bash Read Write Browser Search
---

# Community Campaign Builder

A sovereign-grade skill for building grassroots political campaigns via the "community help route" - integrating music promotion, multi-platform outreach, and evidence-based intelligence gathering.

## When to Use

- Building an independent MP or political campaign
- Creating grassroots community advocacy movements
- Integrating music (Suno) into promotional campaigns
- Coordinating multi-platform social media outreach
- Gathering intelligence from WhatsApp, email, and news sources
- Developing community-first campaign strategies

## Quick Start

1. **Gather Intelligence** - Search WhatsApp, Gmail, news for candidate/cause context
2. **Build Candidate Profile** - Document background, strengths, community connections
3. **Identify Campaign Pillars** - Define 3-5 core themes from community needs
4. **Curate Music Assets** - Collect/create Suno songs aligned with campaign themes
5. **Create Campaign Blueprint** - Document strategy with action phases
6. **Deploy Promotion** - Distribute across platforms with automation

## Step-by-Step Process

### Phase 1: Intelligence Gathering

Collect information from all available sources:

```
Sources to Search:
├── WhatsApp (browser automation)
├── Gmail (MCP integration)
├── Slack (MCP integration)
├── News articles (web search)
└── Social media profiles
```

**Key Actions:**
- Search WhatsApp for candidate name and related contacts
- Search Gmail for campaign-related communications
- Search news for public profile and recent events
- Document all findings in structured markdown files

### Phase 2: Candidate Profile Development

Create comprehensive profile document:

| Section | Content |
|---------|---------|
| Identity | Name, location, background |
| Credentials | Professional experience, military service, community roles |
| Public Profile | Media coverage, social presence, notable events |
| Support Base | Existing allies, organizations, community groups |
| Campaign Themes | Issues aligned with candidate's story |

### Phase 3: Campaign Pillar Definition

Define 3-5 core campaign pillars based on:
- Candidate's authentic story and experience
- Community needs and concerns
- Differentiation from establishment candidates
- Actionable policy positions

**Example Pillars:**
1. Free Speech & Justice Reform
2. Veterans Rights
3. Community Representation
4. Anti-Corruption / Transparency
5. Local Economic Development

### Phase 4: Music Asset Curation

Collect campaign songs from Suno or create new ones:

```python
# Song tracking structure
CAMPAIGN_SONGS = [
    {
        "title": "Song Title",
        "url": "https://suno.com/s/...",
        "theme": "anthem|awareness|defiance|unity",
        "use_case": "rallies|social_media|videos"
    }
]
```

**Song Selection Criteria:**
- Lyrics align with campaign themes
- Emotional resonance with target audience
- Shareable format for social media
- Rights owned by campaign (Andy's rights)

### Phase 5: Campaign Blueprint Creation

Generate comprehensive strategy document with:

1. **Candidate Profile Summary**
2. **Community Help Route Framework**
3. **Campaign Pillars (detailed)**
4. **Music Promotion Strategy**
5. **Support Network Map**
6. **Electoral Requirements**
7. **Phased Action Plan**
8. **Success Metrics**

See [BLUEPRINT_TEMPLATE.md](references/BLUEPRINT_TEMPLATE.md) for full template.

### Phase 6: Multi-Platform Deployment

Distribute campaign content across:

| Platform | Content Type | Automation |
|----------|--------------|------------|
| WhatsApp | Direct shares, group messages | Browser automation |
| Suno | Song publishing, engagement | Manual + API |
| Spotify | Music distribution | Upload workflow |
| Facebook | Videos, posts, events | Scheduled posts |
| Twitter/X | Clips, announcements | API integration |
| Local media | Press releases | Email outreach |

## Tools Integration

### WhatsApp Search Tool
```bash
# Search messages
python3 whatsapp_search.py --search "candidate name"

# Get chat messages
python3 whatsapp_search.py --messages "Contact Name" --limit 100
```

### NAS Secret Storage
```bash
# Store credentials securely
python3 nas_secrets.py store --name GH_TOKEN --value "token"

# Sync to NAS
python3 nas_secrets.py sync-from-env
```

### Git Integration
```bash
# Push campaign materials
export GH_TOKEN="your_token"
git add -A && git commit -m "Campaign update" && git push
```

## Evidence Management

All gathered intelligence must be:
1. **Timestamped** - ISO format datetime
2. **Hashed** - SHA256 for integrity verification
3. **Stored** - Saved to NAS evidence directory
4. **Version controlled** - Pushed to Git repository

## Output Artifacts

| Artifact | Format | Location |
|----------|--------|----------|
| Candidate Intel | Markdown | `{candidate}_intel.md` |
| WhatsApp Intel | Markdown | `{candidate}_whatsapp_intel.md` |
| Campaign Songs | Markdown | `{candidate}_campaign_songs.md` |
| Campaign Blueprint | Markdown | `{candidate}_campaign_blueprint.md` |
| Automation Scripts | Python | `scripts/` directory |

## Error Handling

| Issue | Resolution |
|-------|------------|
| WhatsApp not logged in | Prompt user for QR scan |
| GitHub auth failed | Request new PAT, store in NAS |
| Suno access blocked | Use browser automation fallback |
| NAS not mounted | Route through cluster node |

## Best Practices

1. **Privacy First** - All data stays sovereign, no cloud dependencies
2. **Evidence Grade** - Hash and timestamp all intelligence
3. **Modular Design** - Each component independently deployable
4. **Community Authentic** - Campaign emerges from community, not imposed
5. **Music Integration** - Songs amplify message, not replace substance

## References

- [BLUEPRINT_TEMPLATE.md](references/BLUEPRINT_TEMPLATE.md) - Full campaign blueprint template
- [ELECTORAL_REQUIREMENTS.md](references/ELECTORAL_REQUIREMENTS.md) - UK MP candidacy requirements
- [MUSIC_DISTRIBUTION.md](references/MUSIC_DISTRIBUTION.md) - Platform distribution guide
