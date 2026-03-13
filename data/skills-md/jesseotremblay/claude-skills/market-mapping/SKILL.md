---
name: market-mapping
description: Creates visual market maps showing competitive landscape, market segments, ecosystem players, and positioning. Use when the user requests market map, competitive landscape visualization, ecosystem mapping, positioning map, or wants to visualize market structure.
---

# Market Mapping

This skill creates comprehensive market maps to visualize competitive landscapes, market segments, ecosystem players, and strategic positioning.

## When to Use This Skill

Invoke this skill when the user:
- Requests a market map or landscape visualization
- Wants to visualize competitive positioning
- Asks for ecosystem mapping or value chain visualization
- Needs to understand market segmentation visually
- Mentions creating a competitive landscape map
- Wants to identify market gaps or white space

## Types of Market Maps

### Competitive Positioning Map

Visualize competitive positioning across two key dimensions:

**Steps:**
1. Identify the most relevant positioning dimensions (e.g., price vs. features, enterprise vs. SMB, simplicity vs. power)
2. Research and place competitors on the map
3. Identify clusters and gaps in the market
4. Determine positioning strategy
5. Create a 2x2 or scatter plot visualization

**Output Format:**
```
Dimension Y (e.g., Feature Richness)
        ↑
   High │    [Competitor C]
        │         [Competitor D]
        │
        │  [Your Product]
        │              [Competitor A]
  Low   │    [Competitor B]
        │
        └────────────────────────────→ Dimension X (e.g., Price)
           Low                    High

KEY INSIGHTS:
- Cluster 1: Low price, low features (value players)
- Cluster 2: High price, high features (premium players)
- White space: Mid-price, high features opportunity
```

### Market Segmentation Map

Map market segments and their characteristics:

**Steps:**
1. Identify segmentation criteria (industry, size, geography, use case, etc.)
2. Define distinct market segments
3. Size each segment (TAM, number of companies, growth rate)
4. Assess segment attractiveness
5. Map competitive intensity per segment
6. Visualize as a matrix or hierarchy

**Output Format:**
```
MARKET SEGMENTS MAP

By Company Size:
┌─────────────────────────────────────────────────────┐
│ Enterprise (>1000 employees)                        │
│ TAM: $5B | Growth: 12% | Competition: High          │
│ Players: Competitor A, Competitor B, Us             │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Mid-Market (100-1000 employees)                     │
│ TAM: $3B | Growth: 18% | Competition: Medium        │
│ Players: Competitor C, Competitor D                 │
│ OPPORTUNITY: Underserved segment                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ SMB (<100 employees)                                │
│ TAM: $8B | Growth: 25% | Competition: High          │
│ Players: Competitor E, Competitor F, Competitor G   │
└─────────────────────────────────────────────────────┘
```

### Ecosystem Map

Map the broader ecosystem including partners, suppliers, and adjacent players:

**Steps:**
1. Identify your product/company at the center
2. Map direct competitors
3. Add complementary players (partners, integrations)
4. Include suppliers and service providers
5. Map adjacent markets and potential entrants
6. Show relationships and dependencies
7. Identify strategic partnership opportunities

**Output Format:**
```
ECOSYSTEM MAP

                    [Suppliers/Platforms]
                    ┌──────────────────┐
                    │   AWS, Azure     │
                    │   Google Cloud   │
                    └────────┬─────────┘
                             │
        [Complementary]      │      [Complementary]
        ┌──────────┐         │         ┌──────────┐
        │Analytics │         │         │ CRM      │
        │Tools     │         │         │Platforms │
        └────┬─────┘         │         └─────┬────┘
             │               │               │
             │      ┌────────▼────────┐      │
             └─────►│  YOUR PRODUCT   │◄─────┘
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       [Direct Competitors]  │  [Adjacent Markets]
       ┌──────────┐    ┌─────▼─────┐    ┌──────────┐
       │Comp A    │    │Service    │    │Related   │
       │Comp B    │    │Providers  │    │Solutions │
       │Comp C    │    └───────────┘    └──────────┘
       └──────────┘

Key Relationships:
→ Integration partners
⟷ Competitive overlap
⋯ Potential partnerships
```

### Market Landscape Map

Create comprehensive market overview showing all players categorized:

**Steps:**
1. Define market categories/sub-segments
2. Identify and categorize all market players
3. Assess each player's market position
4. Group by business model, technology, or focus area
5. Indicate market leaders, challengers, and niche players
6. Show market evolution and emerging players

**Output Format:**
```
MARKET LANDSCAPE

┌─────────────────────────────────────────────────────┐
│ INFRASTRUCTURE LAYER                                │
├─────────────────────────────────────────────────────┤
│ Leaders: [AWS], [Azure], [GCP]                      │
│ Challengers: [DigitalOcean], [Linode]              │
│ Emerging: [Fly.io], [Railway]                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ PLATFORM LAYER                                      │
├─────────────────────────────────────────────────────┤
│ All-in-one: [Vercel], [Netlify], [Render]         │
│ Container-focused: [Kubernetes], [Docker]          │
│ Serverless: [Cloudflare Workers], [Lambda]        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ DEVELOPER TOOLS LAYER                              │
├─────────────────────────────────────────────────────┤
│ CI/CD: [GitHub Actions], [CircleCI], [Jenkins]    │
│ Monitoring: [Datadog], [New Relic], [Sentry]      │
│ Security: [Snyk], [Dependabot]                     │
└─────────────────────────────────────────────────────┘
```

## Mapping Frameworks

**Framework 1: 2x2 Positioning Matrix**
- **Best for:** Competitive positioning analysis
- **Axes:** Choose 2 most differentiating dimensions
- **Common combinations:**
  - Price vs. Features
  - Ease of use vs. Power/Capabilities
  - Specialization vs. Breadth
  - Enterprise vs. SMB focus
  - On-premise vs. Cloud
  - Innovation vs. Stability

**Framework 2: Gartner Magic Quadrant Style**
- **Best for:** Market maturity assessment
- **Quadrants:**
  - Leaders: High vision, high execution
  - Challengers: Low vision, high execution
  - Visionaries: High vision, low execution
  - Niche Players: Low vision, low execution
- **Axes:** Completeness of Vision vs. Ability to Execute

**Framework 3: Value Chain Map**
- **Best for:** Understanding industry structure
- **Components:**
  - Suppliers → Manufacturers → Distributors → Retailers → End Users
  - Map players at each stage
  - Identify vertical integration opportunities

**Framework 4: Concentric Circle Map**
- **Best for:** Ecosystem and adjacency analysis
- **Layers:**
  - Center: Core market/product
  - Ring 1: Direct competitors
  - Ring 2: Adjacent markets
  - Ring 3: Broader ecosystem
  - Ring 4: Potential future expansion

## Map Creation Process

### Step 1: Define Scope and Purpose

Questions to answer:
- What is the specific market or category to map?
- Who is the primary audience for this map?
- What decisions will this map inform?
- What level of detail is needed?
- What time horizon (current state vs. future state)?

### Step 2: Research and Data Collection

Gather information about:
- All relevant market players (companies, products, solutions)
- Market segments and categories
- Positioning attributes and differentiators
- Market size and share data
- Ecosystem relationships

Use WebSearch to find:
- Industry analyst reports
- Market research publications
- Competitive intelligence
- Company websites and positioning

### Step 3: Choose Mapping Approach

Select based on purpose:
- **Competitive analysis** → Positioning Map
- **Market structure** → Landscape Map
- **Opportunity identification** → Segmentation Map
- **Partnership strategy** → Ecosystem Map
- **Market maturity** → Magic Quadrant style

### Step 4: Create the Map

Layout and visualization:
1. Choose clear, meaningful axes/categories
2. Place all players accurately
3. Use consistent notation
4. Add labels and legends
5. Include market size/share if relevant
6. Highlight white space or opportunities
7. Add annotations for key insights

### Step 5: Derive Insights

Extract strategic insights:
- Where are competitors clustered?
- What gaps exist in the market?
- Which segments are underserved?
- What is our differentiation opportunity?
- Who are potential partners?
- What are the market dynamics?

## Common Mapping Patterns

**Pattern 1: Competitive Crowding Analysis**
- Create positioning map
- Identify clusters of competitors
- Find white space opportunities
- Determine differentiation strategy
- Example: SaaS project management tools clustered on "ease of use" axis

**Pattern 2: Market Evolution Mapping**
- Map current market state
- Overlay emerging players and trends
- Show direction of market movement
- Identify future positioning
- Example: On-premise solutions migrating to cloud

**Pattern 3: Multi-Segment Opportunity**
- Create segment map with attractiveness scores
- Assess competitive intensity per segment
- Calculate addressable market per segment
- Prioritize segments for entry
- Example: Enterprise vs. SMB vs. Consumer segments

**Pattern 4: Ecosystem Partnership Mapping**
- Map complementary players
- Identify integration opportunities
- Assess partnership potential
- Plan go-to-market alliances
- Example: Payment processors, shipping providers, accounting software

## Visualization Best Practices

**Clarity:**
- Use simple, clean layouts
- Limit to 2-3 dimensions
- Clear labels and legends
- Readable text size
- Consistent formatting

**Accuracy:**
- Base positioning on research and data
- Avoid subjective placements
- Cross-validate with multiple sources
- Update regularly
- Note data sources and dates

**Insights:**
- Highlight key findings
- Annotate important patterns
- Show white space clearly
- Use color/size to indicate importance
- Add strategic implications

**Format:**
- Text-based maps for CLI output
- Clear ASCII art or symbols
- Structured tables when appropriate
- Bullet lists for player groupings
- Box diagrams for relationships

## Example Maps

**Example 1: Cloud Storage Market Positioning**

```
                Feature Richness
                       ↑
                 High  │
                       │  [Box]    [Dropbox Business]
                       │
                       │  [Google Drive]  [OneDrive]
                       │
                  Low  │  [iCloud]
                       │
                       └────────────────────────────→ Price
                          Low                    High

Insights:
- Enterprise features cluster at higher price points
- Consumer-focused solutions in low-price, low-feature quadrant
- Opportunity: High features at mid-tier pricing (underserved)
- Box and Dropbox competing head-to-head in enterprise
```

**Example 2: Fintech Ecosystem Map**

```
                [Banking Infrastructure]
                ┌──────────────────────┐
                │ Plaid, Stripe, Dwolla│
                └──────────┬───────────┘
                           │
    [Lending]              │            [Payments]
    ┌──────────┐           │           ┌──────────┐
    │ Affirm   │           │           │ Square   │
    │ SoFi     │───────────┼───────────│ PayPal   │
    └──────────┘           │           └──────────┘
                           │
                  ┌────────▼────────┐
                  │   YOUR NEOBANK  │
                  └────────┬────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    [Investment]      [Competitors]    [Insurance]
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ Robinhood│     │ Chime    │     │ Lemonade │
    │ Acorns   │     │ N26      │     │ Root     │
    └──────────┘     └──────────┘     └──────────┘

Partnership Opportunities:
→ Infrastructure: Integrate Plaid for account linking
→ Payments: Partner with Square for merchant services
→ Investment: Embed Robinhood or similar
→ Insurance: Bundle Lemonade coverage
```

## Validation Checklist

Before finalizing a market map:

- [ ] Purpose and scope clearly defined
- [ ] All major players identified and researched
- [ ] Positioning based on data, not assumptions
- [ ] Axes/dimensions are meaningful and differentiating
- [ ] Visual layout is clear and readable
- [ ] Key insights extracted and highlighted
- [ ] White space opportunities identified
- [ ] Competitive clusters noted
- [ ] Map includes legend/key as needed
- [ ] Sources cited for data points
- [ ] Strategic implications stated

## Map Complexity Options

**Simple Map (15-30 min):**
- Single view (positioning or landscape)
- Top 5-10 players only
- Basic 2x2 format
- High-level insights

**Standard Map (30-60 min):**
- Multiple views (positioning + landscape)
- Comprehensive player list
- Detailed categorization
- Segment analysis
- Strategic insights

**Comprehensive Mapping (1-2 hours):**
- Multiple map types
- Ecosystem view included
- Segment-by-segment analysis
- Quantitative data included (market share, sizing)
- Competitive dynamics explained
- Partnership opportunities identified
- Future state projection

Ask the user for their preferred scope if unclear.

## Additional Notes

- Market maps become outdated quickly - note the date
- Different stakeholders may need different map types
- Combine with market research skill for deeper analysis
- Use TAM analysis skill to size segments on the map
- Maps are most valuable when they drive strategic decisions
- Update maps quarterly or when major market shifts occur
- Consider creating both current state and future state maps
