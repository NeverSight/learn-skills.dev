---
name: route-researcher
description: Research North American mountain peaks and generate comprehensive route beta reports
---

# Route Researcher

Research mountain peaks across North America and generate comprehensive route beta reports combining data from multiple sources including PeakBagger, SummitPost, WTA, AllTrails, weather forecasts, avalanche conditions, and trip reports.

**Data Sources:** This skill aggregates information from specialized mountaineering websites (PeakBagger, SummitPost, Washington Trails Association, AllTrails, The Mountaineers, and regional avalanche centers). The quality of the generated report depends on the availability of information on these sources. If your target peak lacks coverage on these websites, the report may contain limited details. The skill works best for well-documented peaks in North America.

## When to Use This Skill

Use this skill when the user requests:

- Research on a specific mountain peak
- Route beta or climbing information
- Trip planning information for peaks
- Current conditions for mountaineering objectives

Examples:

- "Research Mt Baker"
- "I'm planning to climb Sahale Peak next month, can you research the route?"
- "Generate route beta for Forbidden Peak"

## Progress Checklist

Research Progress:

- [ ] Phase 1: Peak Identification (peak validated, ID obtained)
- [ ] Phase 2: Peak Information Retrieval (coordinates and details obtained)
- [ ] Phase 3: Data Gathering (parallel execution)
  - [ ] Phase 3a: Python conditions fetch (weather, air quality, daylight, avalanche, peakbagger)
  - [ ] Phase 3b: Researcher agents (3 in parallel - web sources + trip reports)
  - [ ] Phase 3c: Results aggregated
  - [ ] Phase 3d: Access/permits (inline WebSearch)
- [ ] Phase 4: Route Analysis (synthesize route, crux, hazards)
- [ ] Phase 5: Report Generation (Report Writer agent)
- [ ] Phase 6: Report Review & Validation (Report Reviewer agent)
- [ ] Phase 7: Completion (user notified, next steps provided)

## Orchestration Workflow

### Phase 1: Peak Identification

**Goal:** Identify and validate the specific peak to research.

1. **Extract Peak Name** from user message
   - Look for peak names, mountain names, or climbing objectives
   - Common patterns: "Mt Baker", "Mount Rainier", "Sahale Peak", etc.

2. **Search PeakBagger** using peakbagger-cli:

   ```bash
   uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger peak search "{peak_name}" --format json
   ```

   - Parse JSON output to extract peak matches
   - Each result includes: peak_id, name, elevation (feet/meters), location, url

3. **Handle Multiple Matches:**
   - If **multiple peaks** found: Use AskUserQuestion to present options
     - For each option, show: peak name, elevation, location, AND PeakBagger URL
     - Format each option description as: "[Peak Name] ([Elevation], [Location]) - [PeakBagger URL]"
     - This allows user to click through and verify the correct peak
     - Let user select the correct peak
     - Provide "Other" option if none match

   - If **single match** found: Confirm with user
     - Present confirmation message with peak details and PeakBagger link
     - Show: "Found: [Peak Name] ([Elevation], [Location])"
     - Include PeakBagger URL in the message so user can verify: "[PeakBagger URL]"
     - Use AskUserQuestion: "Is this the correct peak? You can verify at [PeakBagger URL]"

   - If **no matches** found:
     - Try peak name variations systematically (see "Peak Name Variations" section):
       - **Word order reversal:** "Mountain Pratt" → "Pratt Mountain"
       - **Title variations:** Mt/Mount, St/Saint
       - **Add location:** Include state or range name
       - **Remove titles:** Try just the core name
     - Run multiple searches in parallel with different variations
     - Combine results and present best matches to user
     - If still no results, use AskUserQuestion to ask for:
       - A different peak name variation
       - Direct PeakBagger peak ID or URL
       - General PeakBagger search

4. **Extract Peak ID:**
   - From search results JSON, extract the `peak_id` field
   - Store for use in subsequent peakbagger-cli commands
   - Also store the PeakBagger URL for reference links

### Phase 2: Peak Information Retrieval

**Goal:** Get detailed peak information and coordinates needed for location-based data gathering.

This phase must complete before Phase 3, as coordinates are required for weather, daylight, and avalanche data.

Retrieve detailed peak information using the peak ID from Phase 1:

```bash
uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger peak show {peak_id} --format json
```

This returns structured JSON with:

- Peak name and alternate names
- Elevation (feet and meters)
- Prominence (feet and meters)
- Isolation (miles and kilometers)
- Coordinates (latitude, longitude in decimal degrees)
- Location (county, state, country)
- Routes (if available): trailhead, distance, vertical gain
- Peak list memberships and rankings
- Standard route description (if available in routes data)

**Error Handling:**

- If peakbagger-cli fails: Fall back to WebSearch/WebFetch and note in "Information Gaps"
- If specific fields missing in JSON: Mark as "Not available" in gaps section
- Rate limiting: Built into peakbagger-cli (default 2 second delay)

**Once coordinates are obtained from this step, immediately proceed to Phase 3.**

### Phase 3: Data Gathering

**Goal:** Gather comprehensive route information from all available sources.

**Execution Strategy:** Run Python script for deterministic API data + dispatch specialized agents in parallel for web research. This hybrid approach minimizes token usage while maximizing parallelism.

#### Step 3A: Fetch Conditions Data (Python Script)

Run the conditions fetcher script to gather all API-based data:

```bash
cd skills/route-researcher/tools
uv run python fetch_conditions.py \
  --coordinates "{latitude},{longitude}" \
  --elevation {elevation_m} \
  --peak-name "{peak_name}" \
  --peak-id {peak_id}
```

This returns JSON with:

- **weather**: 7-day forecast with temperatures, precipitation, freezing levels
- **air_quality**: AQI ratings and any concerns
- **daylight**: Sunrise, sunset, civil twilight
- **avalanche**: NWAC region and URL for manual check
- **peakbagger**: Ascent statistics and recent ascents (if peak_id provided)
- **gaps**: Any API failures noted for report

**Run this in parallel with Step 3B** (no dependency between them).

#### Step 3B: Dispatch Researcher Agents (Parallel)

Dispatch 3 Researcher agents in a single message (all Task calls together). Each agent researches assigned sources and fetches trip report content directly.

**Agent 1: PeakBagger + SummitPost**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from these sources: PeakBagger, SummitPost

## PeakBagger Research
1. Search: "{peak_name} site:peakbagger.com"
2. Extract route descriptions from peak page
3. Identify trip reports with content (word_count > 0)
4. Fetch content for up to 5 recent trip reports using:
   ```bash
   uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger ascent show {ascent_id} --format json
   ```

## SummitPost Research

1. Search: "{peak_name} site:summitpost.org"
2. Use WebFetch to extract: route name, difficulty, approach, description, hazards
3. If WebFetch fails, use:

   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{url}"
   ```

## Trip Report Extraction

For each report fetched, extract: date, author, route conditions, gear mentioned, hazards.

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["PeakBagger", "SummitPost"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "description": "...", "hazards": [...]}
  ],
  "trip_reports": [
    {"source": "...", "date": "...", "author": "...", "url": "...", "summary": "...", "conditions": "...", "has_gpx": false}
  ],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Agent 2: WTA + Mountaineers**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from these sources: WTA, Mountaineers.org

## WTA Research
1. Search: "{peak_name} site:wta.org"
2. Find the hike page and extract: trail name, difficulty, distance, elevation gain, hazards
3. Get trip reports from AJAX endpoint: {wta_url}/@@related_tripreport_listing
4. Fetch content for up to 5 recent trip reports using:
   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{trip_report_url}"
   ```

## Mountaineers Research

1. Search: "{peak_name} site:mountaineers.org route"
2. Extract route beta, technical requirements, hazards

## Fallback

If WebFetch fails for any page, use cloudscrape.py as shown above.

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["WTA", "Mountaineers"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "description": "...", "hazards": [...]}
  ],
  "trip_reports": [
    {"source": "...", "date": "...", "author": "...", "url": "...", "summary": "...", "conditions": "...", "has_gpx": false}
  ],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Agent 3: AllTrails**

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a route researcher gathering mountaineering data for {peak_name}.

## Your Assignment
Research from AllTrails

## AllTrails Research
1. Search: "{peak_name} site:alltrails.com"
2. Use WebFetch to extract: trail name, difficulty, distance, elevation gain, route type, best season, hazards
3. If WebFetch fails, use:
   ```bash
   uv run python {repo_root}/skills/route-researcher/tools/cloudscrape.py "{url}"
   ```

## Output Format (return EXACTLY this JSON)

```json
{
  "sources": ["AllTrails"],
  "route_info": [
    {"source": "...", "name": "...", "difficulty": "...", "distance_miles": N, "elevation_gain_ft": N, "description": "...", "hazards": [...]}
  ],
  "trip_reports": [],
  "gaps": ["what couldn't be fetched and why"]
}
```"""
)
```

**Execute all 3 agents in parallel by including all Task calls in a single response.**

#### Step 3C: Aggregate Results

After Python script and all agents return, aggregate into unified data structure:

```json
{
  "conditions": { /* from fetch_conditions.py */ },
  "route_data": {
    "sources": [ /* merged from all 3 agents */ ],
    "trip_reports": [ /* merged from all agents */ ]
  },
  "gaps": [ /* merged gaps from all sources */ ]
}
```

**Partial Failure Handling:**

- If any agent fails entirely, proceed with data from successful agents
- Note failed sources in the gaps array
- Minimum viable: conditions data + at least one route source

#### Step 3D: Access and Permits (Inline)

Run WebSearch for access information:

```
WebSearch queries:
1. "{peak_name} trailhead access"
2. "{peak_name} permit requirements"
3. "{peak_name} forest service road conditions"
```

Extract trailhead names, required permits, access notes. Add to route_data.

### Phase 4: Route Analysis

**Goal:** Analyze gathered data to determine route characteristics and synthesize information.

#### Step 4A: Determine Route Type

Based on route descriptions, elevation, and gear mentions, classify as:

- **Glacier:** Crevasses mentioned, glacier travel, typically >8000ft
- **Rock:** Technical climbing, YDS ratings (5.x), protection mentioned
- **Scramble:** Class 2-4, exposed but non-technical
- **Hike:** Class 1-2, trail-based, minimal exposure

#### Step 4B: Synthesize Route Information from Multiple Sources

**Goal:** Combine trip reports and route descriptions from Step 3B researcher agents, plus conditions data from Step 3A, into comprehensive route beta.

**Source Priority:**

1. Trip reports (Step 3B agents) - first-hand experiences
2. Route descriptions (Step 3B agents) - published beta baseline
3. PeakBagger/ascent data (Step 3A Python script) - basic info, patterns

**Synthesis Pattern for Route, Crux, and Hazards:**

1. **Start with baseline** from route descriptions (standard route name, published difficulty)
2. **Enrich with trip report details** (landmarks, specific conditions, actual experiences)
3. **Note conflicts** when trip reports disagree with published info
4. **Highlight consensus** ("Multiple reports mention...")
5. **Include specifics** (elevations, locations, quotes)

**Example (Route Description):**
> "The standard route follows the East Ridge (Class 3). Multiple trip reports mention a well-cairned use trail branching right at 4,800 ft—this is the correct turn. The use trail climbs through talus (described as 'tedious' and 'ankle-rolling'). In early season, this section may be snow-covered, requiring microspikes."

**Apply this pattern to:**

- **Route:** Use baseline structure, add landmarks/navigation from trip reports, include actual times
- **Crux:** Describe location/difficulty, add trip report assessments, note conditions-dependent variations
- **Hazards:** Extract ALL hazards from trip reports (rockfall, exposure, route-finding, seasonal), organize by type, include specific locations and mitigation strategies. Be comprehensive—safety-critical.

**Extract Key Information:**

From all synthesized data, identify:

- **Difficulty Rating:** YDS class, scramble grade, or general difficulty (validated by trip reports)
- **Crux:** Hardest/most technical section of route (synthesized above)
- **Hazards:** All identified hazards (synthesized above)
- **Notable Gear:** Any unusual or important gear mentioned in trip reports or beta (to be included in relevant sections, not as standalone section)
- **Trailhead:** Name and approximate location
- **Distance/Gain:** Round-trip distance and elevation gain (compare published vs actual trip report data)
- **Time Estimates:** Calculate three-tier pacing based on distance and gain:
  - **Fast pace:** Calculate based on 2+ mph and 1000+ ft/hr gain rate
  - **Moderate pace:** Calculate based on 1.5-2 mph and 700-900 ft/hr gain rate
  - **Leisurely pace:** Calculate based on 1-1.5 mph and 500-700 ft/hr gain rate
  - Use the **slower** of distance-based or gain-based calculations for each tier
  - Example: For 4 miles, 2700 ft gain:
    - Fast: max(4mi/2mph, 2700ft/1000ft/hr) = max(2hr, 2.7hr) = ~2.5-3 hours
    - Moderate: max(4mi/1.5mph, 2700ft/800ft/hr) = max(2.7hr, 3.4hr) = ~3-4 hours
    - Leisurely: max(4mi/1mph, 2700ft/600ft/hr) = max(4hr, 4.5hr) = ~4-5 hours
- **Freezing Level Analysis:** Compare peak elevation with forecasted freezing levels:
  - **Include Freezing Level Alert if:** Any day in forecast has freezing level within 2000 ft of peak elevation
  - **Omit if:** Freezing level stays >2000 ft above peak throughout forecast (typical summer conditions)
  - Example: 5,469 ft peak with 5,000-8,000 ft freezing levels → Include alert (marginal conditions)
  - Example: 4,000 ft peak with 10,000+ ft freezing levels → Omit alert (well above summit)

#### Step 4C: Identify Information Gaps

Explicitly document what data was **not found or unreliable:**

- Missing trip reports
- No GPS tracks available
- Script failures (weather, avalanche, daylight)
- Conflicting information between sources
- Limited seasonal data

### Phase 5: Report Generation

**Goal:** Create comprehensive Markdown document by dispatching Report Writer agent.

#### Step 5A: Prepare Data Package

Organize all gathered and analyzed data into structured JSON:

```json
{
  "peak": {
    "name": "{peak_name}",
    "id": {peak_id},
    "elevation_ft": {elevation},
    "coordinates": [{latitude}, {longitude}],
    "location": "{location}",
    "peakbagger_url": "{url}"
  },
  "conditions": {
    // From fetch_conditions.py output
    "weather": {...},
    "air_quality": {...},
    "daylight": {...},
    "avalanche": {...}
  },
  "route_data": {
    // Merged from all Researcher agents
    "sources": [...],
    "trip_reports": [...]
  },
  "analysis": {
    // From Phase 4
    "route_type": "{hike|scramble|technical|glacier}",
    "difficulty": "{rating}",
    "crux": "{description}",
    "hazards": [...],
    "time_estimates": {...},
    "access": {...}
  },
  "gaps": [...]
}
```

#### Step 5B: Dispatch Report Writer Agent

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a Report Writer generating a mountaineering route report.

## Instructions

1. **Read the report template:**
   Use the Read tool to read: {repo_root}/skills/route-researcher/assets/report-template.md

2. **Generate report following template structure exactly:**
   - Header with peak name, elevation, location, date
   - AI disclaimer (prominent safety warning)
   - Overview: route type, difficulty, distance/gain, time estimates
   - Route Description: synthesized from sources, include landmarks
   - Crux: describe hardest section with specifics
   - Known Hazards: comprehensive list
   - Current Conditions: weather forecast, freezing levels, air quality, daylight
   - Trip Reports: links organized by source with dates
   - Information Gaps: explicitly list missing data
   - Data Sources: links to all sources used

3. **Markdown Formatting Rules:**
   - ALWAYS add blank line before lists
   - ALWAYS add blank line after section headers
   - Use `-` for bullets (not `*` or `+`)
   - Use `**text**` for bold emphasis
   - Break paragraphs >4 sentences

4. **Save the report:**
   Use the Write tool to save to: {output_dir}/{date}-{peak-name-slug}.md

## Data Package

{data_package_json}

## Output Format (return EXACTLY this JSON)
```json
{
  "status": "SUCCESS",
  "file_path": "/absolute/path/to/report.md",
  "filename": "YYYY-MM-DD-peak-name.md",
  "sections_generated": N
}
```"""
)
```

#### Step 5C: Capture Report File Path

Extract `file_path` from agent's JSON response for use in Phase 6.

### Phase 6: Report Review & Validation

**Goal:** Validate report quality by dispatching Report Reviewer agent.

#### Step 6A: Dispatch Report Reviewer Agent

```
Task(
  subagent_type="general-purpose",
  prompt="""You are a Report Reviewer validating a mountaineering route report.

## Instructions

1. **Read the report:**
   Use the Read tool to read: {report_file_path}

2. **Perform systematic quality checks:**

   **Factual Consistency:**
   - Dates match their stated day-of-week (e.g., "Thu Nov 6, 2025" is actually Thursday)
   - Coordinates, elevations, distances consistent across all mentions
   - Weather forecasts align logically (freezing levels match precipitation types)

   **Mathematical Accuracy:**
   - Elevation gains add up correctly
   - Time estimates reasonable given distance and elevation gain
   - Unit conversions correct (feet to meters, etc.)

   **Internal Logic:**
   - Hazard warnings align with route descriptions
   - Recommendations match current conditions
   - Crux descriptions match overall difficulty rating

   **Completeness:**
   - No placeholder texts like {{peak_name}} or {{YYYY-MM-DD}}
   - All referenced links actually provided
   - Mandatory sections present: Overview, Route, Current Conditions, Trip Reports, Information Gaps, Data Sources

   **Formatting:**
   - Markdown headers properly structured
   - Lists have blank lines before them
   - Tables properly formatted

   **Safety & Responsibility:**
   - AI disclaimer present and prominent
   - Critical hazards properly emphasized
   - Users directed to verify information from primary sources

3. **Fix issues:**
   - **Critical** (safety errors, factual errors, missing disclaimers): MUST fix using Edit tool
   - **Important** (completeness, consistency): SHOULD fix
   - **Minor** (formatting, polish): FIX if quick

## Output Format (return EXACTLY this JSON)
```json
{
  "status": "PASS" | "PASS_WITH_FIXES" | "FAIL",
  "issues_found": N,
  "fixes_applied": ["description of fix 1", "description of fix 2"],
  "remaining_issues": ["issues that couldn't be fixed"],
  "report_path": "/absolute/path/to/report.md"
}
```"""
)
```

#### Step 6B: Process Validation Results

Handle the reviewer agent's response:

- **PASS or PASS_WITH_FIXES:** Proceed to Phase 7 with the `report_path`
- **FAIL:** Present `remaining_issues` to user and ask for guidance

The Report Reviewer automatically fixes issues and returns the corrected file path.

### Phase 7: Completion

**Goal:** Inform user of completion and next steps.

Report to user:

1. **Success message:** "Route research complete for {Peak Name}"
2. **File location:** Full absolute path to generated report
3. **Summary:** Brief 2-3 sentence overview:
   - Route type and difficulty
   - Key hazards or considerations
   - Any significant information gaps
4. **Next steps:** Encourage user to:
   - Review the report
   - Verify critical information from primary sources
   - Check current conditions before attempting route

**Example completion message:**

```
Route research complete for Mount Baker!

Report saved to: 2025-10-20-mount-baker.md

Summary: Mount Baker via Coleman-Deming route is a moderate glacier climb (Class 3) with significant crevasse hazards. The route involves 5,000+ ft elevation gain and typically requires an alpine start. Weather and avalanche forecasts are included.

Next steps: Review the report and verify current conditions before your climb. Remember that mountain conditions change rapidly - check recent trip reports and weather forecasts immediately before your trip.
```

## Error Handling Principles

Throughout execution, follow these error handling guidelines:

### Script Failures

- **Don't block:** If a Python script fails, note in "Information Gaps" and continue
- **Provide alternatives:** Include manual check links (Mountain-Forecast.com, NWAC.us)
- **One retry:** Retry once on network timeouts, then continue

### Missing Data

- **Be explicit:** Always document what wasn't found
- **Be helpful:** Provide links for manual checking
- **Don't guess:** Never fabricate data to fill gaps

### Search Failures

- **Try variations:** If peak not found, try alternate names (Mt vs Mount)
- **Ask user:** If still not found, ask user for clarification or direct URL
- **Provide guidance:** Suggest how to search PeakBagger manually

### WebFetch/WebSearch Issues

- **Universal fallback pattern:** Always try WebFetch first, then cloudscrape.py if it fails
- **Automatic retry:** If WebFetch fails or returns incomplete data, immediately retry with cloudscrape.py
- **Graceful degradation:** Missing one source shouldn't stop entire research
- **Document gaps:** Note which sources were unavailable (both WebFetch AND cloudscrape.py failed)
- **Prioritize safety:** If critical safety info (avalanche, hazards) unavailable, emphasize in gaps section

## Execution Timeouts

- **Individual Python scripts:** 30 seconds each
- **WebFetch operations:** Use default timeout
- **WebSearch operations:** Use default timeout
- **Total skill execution:** Target 3-5 minutes, acceptable up to 10 minutes for comprehensive research

## Quality Principles

Every generated report must:

1. ✅ **Include safety disclaimer** prominently at top
2. ✅ **Document all information gaps** explicitly
3. ✅ **Cite sources** with links
4. ✅ **Use current date** in filename and metadata
5. ✅ **Follow template structure** exactly
6. ✅ **Provide actionable information** (distances, times, gear)
7. ✅ **Emphasize verification** - this is research, not gospel

## Implementation Notes

### Architecture (as of 2026-01-29)

The route-researcher skill uses a hybrid architecture combining Python scripts and LLM agents:

**Components:**

- **Python script** (`tools/fetch_conditions.py`) - Deterministic API calls for weather, air quality, daylight, avalanche, and PeakBagger data
- **Researcher agents** (3 total) - Web research for route info and trip reports from PeakBagger+SummitPost, WTA+Mountaineers, and AllTrails
- **Report Writer agent** - Generates markdown reports from aggregated data
- **Report Reviewer agent** - Validates report quality before presentation

**Benefits:**

- **Reduced token usage** - Python handles deterministic API calls with zero LLM tokens
- **Parallel execution** - Phase 3 runs Python script + 3 researcher agents simultaneously
- **Inline prompts** - Agent instructions embedded in SKILL.md for reliability
- **Clear contracts** - JSON schemas define agent inputs and outputs

See `docs/architecture.md` for detailed execution flow and data contracts.

### Current Status (as of 2026-01-30)

**Implemented:**

- **peakbagger-cli** integration for peak search, info, and ascent data
- Python tools directory structure
- Report generation in user's current working directory
- **cloudscrape.py** - Universal fallback for WebFetch failures, works with ANY website including:
  - Cloudflare-protected sites (SummitPost, PeakBagger, Mountaineers.org)
  - AllTrails (when WebFetch fails)
  - WTA (when WebFetch fails)
  - Any other site that blocks or limits WebFetch access
- **Two-tier fetching strategy:** WebFetch first, cloudscrape.py as automatic fallback
- **Open-Meteo Weather API** for mountain weather forecasts (temperature, precipitation, freezing level, wind)
- **Open-Meteo Air Quality API** for AQI forecasting (US AQI scale with conditional alerts)
- Multi-source weather gathering (Open-Meteo, NOAA/NWS, NWAC)
- Adaptive ascent data retrieval based on peak popularity
- **Sunrise-Sunset.org API** for daylight calculations (sunrise, sunset, civil twilight, day length)
- **High-quality trip report identification** across PeakBagger and WTA sources
- **WTA AJAX endpoint** for trip report extraction (`{wta_url}/@@related_tripreport_listing`)

**Pending Implementation:**

- `fetch_avalanche.py` - NWAC avalanche data (currently using WebSearch/WebFetch as fallback)
- **Browser automation** for Mountaineers.org and AllTrails trip report extraction (requires Playwright/Chrome)
  - Current: Both sites load content via JavaScript, cloudscrape.py cannot extract
  - Future: Add browser automation as 3rd-tier fallback

**When Python scripts are not yet implemented:**

- Note in "Information Gaps" section
- Provide manual check links
- Continue with available data
- Don't block report generation

### peakbagger-cli Command Reference (v1.7.0)

All commands use `--format json` for structured output. Run via:

```bash
uvx --from git+https://github.com/dreamiurg/peakbagger-cli.git@v1.7.0 peakbagger <command> --format json
```

**Available Commands:**

- `peak search <query>` - Search for peaks by name
- `peak show <peak_id>` - Get detailed peak information (coordinates, elevation, routes)
- `peak stats <peak_id>` - Get ascent statistics and temporal patterns
  - `--within <period>` - Filter by period (e.g., '1y', '5y')
  - `--after <YYYY-MM-DD>` / `--before <YYYY-MM-DD>` - Date filters
- `peak ascents <peak_id>` - List individual ascents with trip report links
  - `--within <period>` - Filter by period (e.g., '1y', '5y')
  - `--with-gpx` - Only ascents with GPS tracks
  - `--with-tr` - Only ascents with trip reports
  - `--limit <n>` - Max ascents to return (default: 100)
- `ascent show <ascent_id>` - Get detailed ascent information

**Note:** For comprehensive command options, run `peakbagger --help` or `peakbagger <command> --help`

### Peak Name Variations

Common variations to try if initial search fails:

- **Word order reversal:** "Mountain Pratt" → "Pratt Mountain", "Peak Sahale" → "Sahale Peak"
- **Title expansion:** "Mt" → "Mount", "St" → "Saint"
- **Add location:** "Baker, WA" or "Baker, North Cascades"
- **Remove title:** "Baker" instead of "Mt Baker"
- **Combine variations:** Try reversed order with title expansion (e.g., "Mountain Pratt" → "Pratt Mount" + "Pratt Mountain")

### Google Maps and USGS Links

#### Summit Coordinates Links

**Google Maps (for summit coordinates):**

```
https://www.google.com/maps/search/?api=1&query={latitude},{longitude}
```

Example: `https://www.google.com/maps/search/?api=1&query=48.7768,-121.8144`

**USGS TopoView (for summit coordinates):**

```
https://ngmdb.usgs.gov/topoview/viewer/#{{latitude}}/{longitude}/15
```

Example: `https://ngmdb.usgs.gov/topoview/viewer/#17/48.7768/-121.8144`

**Note:** Use decimal degree format for coordinates. TopoView uses zoom level in URL (15-17 works well for peaks).

#### Trailhead Google Maps Links

**If coordinates available** (e.g., from Mountaineers.org place information):

```
https://www.google.com/maps/search/?api=1&query={latitude},{longitude}
```

Example: `https://www.google.com/maps/search/?api=1&query=48.5123,-121.0456`

**If only trailhead name available:**

```
https://www.google.com/maps/search/?api=1&query={trailhead_name}+{state}
```

Example: `https://www.google.com/maps/search/?api=1&query=Cascade+Pass+Trailhead+WA`

**Note:** Prefer coordinates when available for more precise location.

---

**Skill Version:** --help | **Last Updated:** 2026-01-30
