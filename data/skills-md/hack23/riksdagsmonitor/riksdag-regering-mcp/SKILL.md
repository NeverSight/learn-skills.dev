---
name: riksdag-regering-mcp
description: Riksdag-Regering MCP server with 32 specialized tools for Swedish political data (Parliament, Government, MPs, votes, documents)
license: Apache-2.0
---

# Riksdag-Regering MCP Server

## Purpose

Provide comprehensive access to Swedish political data through the `riksdag-regering-mcp` Model Context Protocol (MCP) server. Enables intelligence operatives and political analysts to query, analyze, and visualize data from the Swedish Riksdag (Parliament) and Regeringen (Government).

## Core Principles

1. **Authoritative Data Source**: Official Swedish government data (data.riksdagen.se, regeringen.se)
2. **Comprehensive Coverage**: 50+ years of historical data (1971-2024)
3. **Structured API**: 32 specialized tools for different data types
4. **Real-Time Access**: Latest parliamentary and government activities
5. **GDPR Compliance**: Public interest basis (Article 6(1)(e)), no personal data beyond official capacity
6. **Multi-Source Integration**: Riksdag documents + Government publications

## Available Tools (32 Total)

### 🔍 Search & Discovery (6 tools)
- **search_ledamoter**: Search for MPs (349 members) by name, party, constituency
- **search_dokument**: Search parliamentary documents (motions, bills, reports)
- **search_dokument_fulltext**: Full-text search across document content
- **search_anforanden**: Search speeches and parliamentary debates
- **search_voteringar**: Search voting records and roll calls
- **search_regering**: Search government documents (propositions, SOU, Dir)

### 📊 Detailed Information (6 tools)
- **get_dokument**: Get complete document with metadata and content
- **get_ledamot**: Get MP profile with assignments, activities, bio
- **get_dokument_innehall**: Get document content and summary
- **get_g0v_document_content**: Get government document in Markdown
- **get_discussion**: Get specific discussion thread
- **get_discussion_comments**: Get comments from a discussion

### 📝 Parliamentary Documents (6 tools)
- **get_motioner**: Latest motions (proposals from MPs)
- **get_propositioner**: Latest government propositions
- **get_betankanden**: Latest committee reports
- **get_fragor**: Latest written questions
- **get_interpellationer**: Latest interpellations (formal questions)
- **get_utskott**: List parliamentary committees (15 committees)

### 🏛️ Government Documents (4 tools)
- **get_regering_document**: Get government document by ID
- **summarize_regering_document**: AI-powered government document summary
- **get_g0v_document_types**: List available government document types
- **get_g0v_category_codes**: List government policy area codes

### 📈 Analytics & Aggregation (5 tools)
- **get_voting_group**: Get votes grouped by party/constituency
- **list_reports**: List available statistical reports
- **fetch_report**: Get statistical report (MP stats, committee data)
- **analyze_g0v_by_department**: Analyze government documents by department
- **get_g0v_latest_update**: Check latest government data update

### 🔄 Advanced Queries (5 tools)
- **fetch_paginated_documents**: Batch fetch with pagination
- **fetch_paginated_anforanden**: Batch fetch speeches
- **batch_fetch_documents**: Multi-year document batches
- **get_calendar_events**: Parliamentary calendar (debates, committees)
- **enhanced_government_search**: Combined Riksdag + Government search

## Data Coverage

### Swedish Riksdag (Parliament)
- **349 MPs**: Current members across 8 parties
- **15 Committees**: AU, FiU, JuU, KU, SkU, SfU, UU, UtU, etc.
- **Documents**: 50+ years (1971-2024)
  - Motions (mot): MP proposals
  - Propositions (prop): Government bills
  - Reports (bet): Committee reports
  - Questions (fr): Written questions
  - Interpellations (ip): Formal questions
- **Votes**: Complete voting records with party/MP breakdown
- **Speeches**: Parliamentary debates (anföranden)

### Swedish Government (Regeringen)
- **Document Types**: Propositions, SOU (state investigations), Dir (committee directives), DS (department series), Remisser (referrals)
- **Departments**: All 10 ministries
- **Historical Data**: Government documents from 1990s+
- **G0V Integration**: Markdown-formatted documents via g0v.se

### 8 Parliamentary Parties
- **S** - Socialdemokraterna (Social Democrats)
- **M** - Moderaterna (Moderates)
- **SD** - Sverigedemokraterna (Sweden Democrats)
- **MP** - Miljöpartiet (Green Party)
- **C** - Centerpartiet (Centre Party)
- **V** - Vänsterpartiet (Left Party)
- **KD** - Kristdemokraterna (Christian Democrats)
- **L** - Liberalerna (Liberals)

## When to Use

- **Political Intelligence**: Analyze voting patterns, coalition behavior
- **Legislative Monitoring**: Track bills, motions, committee work
- **MP Analysis**: Profile MPs, track activities, voting discipline
- **Coalition Analysis**: Assess government stability, party cooperation
- **Policy Research**: Trace policy development through documents
- **Voting Analysis**: Party cohesion, rebels, cross-party voting
- **Government Oversight**: Track government proposals, investigations
- **Electoral Research**: Historical trends, party evolution
- **Transparency Dashboards**: Real-time political metrics
- **Risk Assessment**: Identify democratic accountability gaps

## Examples

### Good Pattern: MP Voting Discipline Analysis
```javascript
// Get all votes from current riksmöte
const votes = await riksdag_regering_mcp.search_voteringar({
  rm: "2024/25",
  limit: 200
});

// Analyze party cohesion
const partyDiscipline = {};
for (const party of ['S', 'M', 'SD', 'C', 'V', 'KD', 'L', 'MP']) {
  const partyVotes = await riksdag_regering_mcp.get_voting_group({
    rm: "2024/25",
    groupBy: "parti",
    limit: 200
  });
  
  // Calculate cohesion metric
  partyDiscipline[party] = calculateCohesion(partyVotes);
}
```

### Good Pattern: Committee Productivity Analysis
```javascript
// Get reports from all committees
const committees = ['AU', 'FiU', 'JuU', 'KU', 'SkU', 'SfU', 'UU'];
const productivity = {};

for (const committee of committees) {
  const reports = await riksdag_regering_mcp.get_betankanden({
    organ: committee,
    rm: "2024/25",
    limit: 100
  });
  
  productivity[committee] = {
    count: reports.length,
    avgProcessingTime: calculateAvgTime(reports)
  };
}
```

### Good Pattern: Government Document Analysis
```javascript
// Search government propositions on specific topic
const props = await riksdag_regering_mcp.search_regering({
  type: "propositioner",
  title: "migration",
  dateFrom: "2024-01-01",
  limit: 50
});

// Get full content for analysis
for (const prop of props) {
  const content = await riksdag_regering_mcp.get_g0v_document_content({
    regeringenUrl: prop.url
  });
  
  // Analyze policy positions
  analyzePolicy(content);
}
```

### Good Pattern: Multi-Language Political Dashboard
```javascript
// Get latest parliamentary activity
const motions = await riksdag_regering_mcp.get_motioner({ limit: 10 });
const props = await riksdag_regering_mcp.get_propositioner({ limit: 10 });
const questions = await riksdag_regering_mcp.get_fragor({ limit: 10 });

// Create bilingual dashboard (Swedish/English)
const dashboard = {
  sv: formatDashboardSV({ motions, props, questions }),
  en: formatDashboardEN({ motions, props, questions })
};
```

### Anti-Pattern: Over-Fetching Without Filtering
```javascript
// ❌ BAD: Fetching too much data
const allDocs = await riksdag_regering_mcp.search_dokument({
  limit: 200 // Default, could be thousands
});

// ✅ GOOD: Targeted query with filters
const recentDocs = await riksdag_regering_mcp.search_dokument({
  rm: "2024/25",
  doktyp: "mot",
  organ: "FiU",
  limit: 50
});
```

### Anti-Pattern: Ignoring Pagination
```javascript
// ❌ BAD: Only getting first page
const votes = await riksdag_regering_mcp.search_voteringar({ limit: 20 });

// ✅ GOOD: Handling pagination
const allVotes = await riksdag_regering_mcp.fetch_paginated_documents({
  doktyp: "votering",
  rm: "2024/25",
  fetchAll: true,
  maxPages: 10
});
```

## 🔥 MCP Query Best Practices

### ⚡ CRITICAL: Always Check Data Freshness First

**RULE #1: Call `get_sync_status()` before any data queries**

```javascript
// === DATA FRESHNESS CHECK ===
// ALWAYS call this FIRST - validates freshness and warms up server
const syncStatus = get_sync_status({});
console.log("Last data sync:", syncStatus.last_updated);

// Calculate hours since last sync
const lastSync = new Date(syncStatus.last_updated);
const hoursSinceSync = (Date.now() - lastSync.getTime()) / 3600000;

// Warn if data is stale (>48 hours)
if (hoursSinceSync > 48) {
  console.warn(`⚠️ DATA MAY BE STALE: ${hoursSinceSync.toFixed(1)} hours since last sync`);
  // Include disclaimer in analysis/articles
}
```

**Why this matters:**
1. **Data Quality**: Ensures analysis uses recent data, not stale information
2. **Server Warmup**: Warms up MCP server (avoids 30-60s cold start on first query)
3. **User Transparency**: Readers/stakeholders know when data was last updated
4. **Quality Control**: Prevents publishing analysis with outdated information

### 📅 Date Parameter Support Matrix

**Only 3 of 32 tools support explicit date parameters:**

| Tool | Date Parameters | Example |
|------|----------------|---------|
| `get_calendar_events` | `from`, `tom` | `{ from: "2026-02-17", tom: "2026-02-23" }` |
| `search_regering` | `from_date`, `to_date` | `{ from_date: "2026-02-01", to_date: "2026-02-17" }` |
| `analyze_g0v_by_department` | `dateFrom`, `dateTo` | `{ dateFrom: "2026-02-01", dateTo: "2026-02-17" }` |

**All other 29 tools require post-query date filtering by:**
- `datum` - votes, speeches (voting/speech date)
- `publicerad` - committee reports, propositions (publication date)
- `inlämnad` - motions, questions, interpellations (submission date)

### ✅ Good Pattern: Explicit Date Filtering

```javascript
// === STEP 1: Check data freshness ===
const syncStatus = get_sync_status({});

// === STEP 2: Query with explicit dates (where supported) ===
const govDocs = search_regering({
  from_date: "2026-02-01",
  to_date: "2026-02-17",
  limit: 50
});

// === STEP 3: Filter by date for tools without date params ===
const betankanden = get_betankanden({ rm: "2025/26", limit: 100 });

// Filter results by publication date
const fromDate = new Date("2026-02-01");
const recentBetankanden = betankanden.filter(bet => 
  new Date(bet.publicerad) >= fromDate
);

console.log(`Found ${recentBetankanden.length} committee reports from ${fromDate.toISOString().split('T')[0]}`);
```

### ❌ Anti-Pattern: Implicit "Latest" Reliance

```javascript
// ❌ BAD: Relies on implicit sorting without date awareness
const votes = search_voteringar({ rm: "2025/26", limit: 50 });
// Problem: No idea when votes occurred, might be months old

// ✅ GOOD: Explicit date filtering
const votes = search_voteringar({ rm: "2025/26", limit: 50 });
const recentVotes = votes.filter(v => 
  new Date(v.datum) >= new Date("2026-02-01")
);
console.log(`Found ${recentVotes.length} votes since 2026-02-01`);
```

### 🔗 Cross-Referencing Strategy

Combine multiple tools for richer analysis:

#### Pattern 1: Committee Report Deep Dive
```javascript
// 1. Get recent committee reports
const betankanden = get_betankanden({ rm: "2025/26", limit: 20 });
const recentBet = betankanden.filter(b => 
  new Date(b.publicerad) >= new Date("2026-02-01")
);

// 2. Get full details for each report
const reportDetails = recentBet.map(bet => 
  get_dokument({ dok_id: bet.dok_id })
);

// 3. Find related votes
const votes = search_voteringar({ rm: "2025/26", limit: 100 });
const relatedVotes = votes.filter(v => 
  recentBet.some(bet => v.bet === bet.beteckning)
);

// 4. Get committee members' speeches
const speeches = search_anforanden({ rm: "2025/26", limit: 100 });
const committeeSpeeches = speeches.filter(a =>
  recentBet.some(bet => a.dokument_hangar_samman === bet.dok_id)
);

// Now you have: reports + details + votes + speeches
```

#### Pattern 2: Party Behavior Analysis
```javascript
// 1. Get voting patterns by party
const voteGroups = get_voting_group({ rm: "2025/26", groupBy: "parti" });

// 2. Get recent votes
const votes = search_voteringar({ rm: "2025/26", limit: 200 });
const recentVotes = votes.filter(v => 
  new Date(v.datum) >= new Date("2026-02-01")
);

// 3. Get party motions
const motions = get_motioner({ rm: "2025/26", limit: 100 });
const partyMotions = motions.filter(m => 
  new Date(m.inlämnad) >= new Date("2026-02-01")
);

// 4. Calculate party cohesion
const partyDiscipline = calculateCohesion(voteGroups, recentVotes);
```

### 🐛 Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| **Tool not found** | Wrong tool name | Use exact names: `get_calendar_events`, `search_voteringar` |
| **Empty results** | No data in timeframe | Check `get_sync_status()`, widen date range, verify `rm` parameter |
| **Stale data** | Last sync >48h ago | Note in analysis with disclaimer, use available data |
| **Timeout** | Cold start (30-60s) | Wait - MCP framework retries automatically |
| **Too broad results** | No date filtering | Add date params OR filter by datum/publicerad/inlämnad |
| **Swedish-only results** | Riksdag API returns Swedish | Must translate to target languages |
| **Missing documents** | Wrong riksmöte (rm) | Verify rm parameter (e.g., "2025/26") |

### 🚀 Performance Tips

1. **Batch Queries After Warmup**: Call `get_sync_status()` first, then batch data queries
2. **Use Pagination Wisely**: Use `fetch_paginated_documents` for large datasets
3. **Filter Early**: Apply date filters as early as possible
4. **Cache Results**: MCP server data updates daily, cache results when appropriate
5. **Parallel Queries**: Independent queries can run in parallel after server warmup

### 📊 Query Pattern Templates

**Template 1: Daily News Monitoring**
```javascript
const syncStatus = get_sync_status({});
const today = new Date().toISOString().split('T')[0];
const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

// Government activity
const govDocs = search_regering({ 
  from_date: yesterday, 
  to_date: today, 
  limit: 50 
});

// Parliamentary calendar
const events = get_calendar_events({ 
  from: today, 
  tom: today, 
  limit: 50 
});

// Recent votes (filter by date)
const votes = search_voteringar({ rm: "2025/26", limit: 50 });
const todayVotes = votes.filter(v => v.datum === today);
```

**Template 2: Weekly Analysis**
```javascript
const syncStatus = get_sync_status({});
const today = new Date();
const weekAgo = new Date(Date.now() - 7 * 86400000);

// Committee reports (filter by publicerad)
const reports = get_betankanden({ rm: "2025/26", limit: 100 });
const weeklyReports = reports.filter(r => 
  new Date(r.publicerad) >= weekAgo
);

// Propositions (filter by publicerad)
const props = get_propositioner({ rm: "2025/26", limit: 50 });
const weeklyProps = props.filter(p => 
  new Date(p.publicerad) >= weekAgo
);

// Questions (filter by inlämnad)
const questions = get_fragor({ rm: "2025/26", limit: 100 });
const weeklyQuestions = questions.filter(q => 
  new Date(q.inlämnad) >= weekAgo
);
```

**Template 3: MP Activity Analysis**
```javascript
const syncStatus = get_sync_status({});

// Get MP profile
const mp = get_ledamot({ intressent_id: "XXXXXXXX" });

// Get MP's motions
const allMotions = get_motioner({ rm: "2025/26", limit: 200 });
const mpMotions = allMotions.filter(m => 
  m.intressent_id === mp.intressent_id
);

// Get MP's speeches
const speeches = search_anforanden({ 
  rm: "2025/26", 
  talare: mp.tilltalsnamn + " " + mp.efternamn,
  limit: 100
});

// Get MP's voting record
const votes = search_voteringar({ rm: "2025/26", limit: 200 });
// Requires cross-referencing with ledamöter data
```

## MCP Server Configuration


### HTTP Endpoint (Production)
```json
{
  "mcpServers": {
    "riksdag-regering": {
      "type": "http",
      "url": "https://riksdag-regering-ai.onrender.com/mcp",
      "tools": ["*"]
    }
  }
}
```

### Local Installation (Development)
```bash
# Install globally
npm install -g riksdag-regering-mcp

# Run locally
riksdag-regering-mcp
# Listens on http://localhost:3000/mcp
```

## Data Quality Considerations

### Completeness
- **Historical Data**: Complete from 1971 for most document types
- **Real-Time Updates**: Government data updated daily
- **Missing Data**: Some older documents may lack full text

### Accuracy
- **Official Source**: Direct from Swedish government APIs
- **Validation**: Schema validation for all responses
- **Versioning**: API versioned for stability

### Timeliness
- **Parliamentary Data**: Updated within hours of publication
- **Government Data**: Updated daily from regeringen.se
- **Latency**: HTTP endpoint may have cold start delays (~30s)

## GDPR Compliance

### Legal Basis
- **Article 6(1)(e)**: Processing necessary for task carried out in public interest
- **Article 9(2)(g)**: Processing necessary for substantial public interest
- **Offentlighetsprincipen**: Swedish Public Access to Information and Secrecy Act

### Data Minimization
- ✅ Only official capacity data (no private lives)
- ✅ No personal contact information
- ✅ No tracking or cookies
- ✅ No data retention beyond cache

### Transparency
- ✅ Clear data sources documented
- ✅ Open-source MCP server
- ✅ Public API documentation
- ✅ GDPR compliance statement

## Remember

- **Use HTTP endpoint** for production (no local installation needed)
- **Filter queries** with riksmöte (rm), organ, party parameters
- **Handle pagination** for large datasets (use `fetchAll` carefully)
- **Verify data quality** - some older documents may be incomplete
- **Respect rate limits** - HTTP endpoint may throttle heavy usage
- **Cache responses** - avoid redundant API calls
- **GDPR compliance** - only official capacity data, no personal information
- **Multi-language support** - Display data in all 14 supported languages
- **Document IDs** follow pattern: H901FiU1 (Riksmöte + Type + Committee + Number)

## References

- [riksdag-regering-mcp npm package](https://www.npmjs.com/package/riksdag-regering-mcp)
- [Swedish Riksdag Open Data](http://data.riksdagen.se/)
- [Swedish Government Publications](https://www.regeringen.se/)
- [G0V.se - Government Document Archive](https://g0v.se/)
- [Hack23 ISMS - GDPR Compliance](https://github.com/Hack23/ISMS-PUBLIC)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Maintained by**: Hack23 AB
