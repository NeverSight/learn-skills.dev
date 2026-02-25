---
name: lead-sources-guide
description: Lead sources by use case with Clay delivery-ready templates - Apollo, LinkedIn Sales Navigator, Clay, Ocean.io, Openmart, and Local Directories. Use when choosing lead sources, building prospecting workflows, or setting up data enrichment.
---

# Lead Sources & Clay Templates

## Lead Sources by Use Case

### Apollo.io
- **Best for:** Broad targeting
- **Use with:** LeadMagic scraper for enrichment
- **Pros:** Good volume
- **Cons:** Needs verification

### LinkedIn Sales Navigator
- **Best for:** Precise role/seniority targeting
- **Use with:** Prospeo or Vayne scrapers
- **Pros:** Higher quality
- **Cons:** Lower volume

### Clay Find People/Accounts
- **Best for:** Quick lookups
- **Use case:** Native database for enrichment workflows

### Ocean.io
- **Best for:** Lookalike accounts
- **Use case:** Expanding TAM based on tech stack/ICP

### Openmart
- **Best for:** Local lead generation
- **Use case:** SMB-focused targeting

### Local Directories
- **Best for:** Niche verticals
- **Tool:** Instant Data Scraper
- **Use case:** Specific industries

---

## Clay Templates (Delivery-Ready)

### General High-Volume
```
Leadmagic → Apollo → Bouncebean → Import Template
```

### Segmented by Title/Industry
```
Leadmagic → Apollo Import → Persona Segment
```

### Email Enrichment
```
Leadmagic → Clay → Enrich Prospect Emails
```

### Standard Sales Nav Workflow
```
Prospeo → Sales Nav → Leads Import Template
```

### Alternative Sales Nav Flow
```
Vayne → Sales Nav → Import Template
```

---

## List Building Pro Tips

1. **Mix sources** - Don't rely on just one
2. **Scraping = step 1** - Still need Clay enrichment
3. **Templates are modular** - Adjust for campaign goals
4. **Don't reinvent the wheel** - Start with template, tweak

---

## Source Selection Matrix

| Need | Best Source | Backup |
|------|-------------|--------|
| Volume | Apollo | Clay Find |
| Quality | Sales Navigator | Ocean.io |
| Lookalikes | Ocean.io | Clay |
| Local/SMB | Openmart | Directories |
| Niche | Directories | Apollo filters |

---

## Combines with

| Skill | Why |
|-------|-----|
| `clay-enrichment-9step` | Enrich leads after sourcing |
| `list-building-tips` | Apply quality principles |
| `clay-buying-signals-5` | Add signals to sourced leads |
| `buying-signals-6` | Prioritize by signal strength |

## Example prompts

```
Which source should I use for targeting VP Engineering at Series B startups?
```

```
Set up a Clay template for Apollo → enrichment → email verification.
```

```
How do I find lookalike companies to my best customers?
```
