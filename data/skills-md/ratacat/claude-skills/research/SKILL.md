---
name: research
description: Deep web research with relevance scoring and knowledge graph storage. Use when researching topics, companies, people, or concepts. Performs Graph-of-Thoughts style exploration with parallel branching, relevance scoring, and synthesis into themed reports.
---

# Deep Research Skill

A Graph-of-Thoughts research system that builds a knowledge graph through structured exploration, stores all findings in SQLite, and uses graph operations (merging, traversal, contradiction detection, relationship inference) to synthesize insights.

## CRITICAL REQUIREMENTS

**You MUST use the database for all operations.** Every finding, every URL, every search query, every relationship MUST be recorded. The database is not optional—it is the core of this methodology. If you skip database operations, the research is invalid.

**You MUST perform graph operations.** After each exploration phase, you MUST run merging, relationship inference, and contradiction detection. These are not suggestions—they are required steps.

**You MUST work iteratively.** Do not try to gather all information then synthesize. Work in cycles: explore → store → analyze graph → identify gaps → explore gaps → repeat.

## Arguments

Parse the user's input to extract:
- `topic`: The research subject (required unless --list or --continue)
- `--depth N`: How many levels deep to explore (default: 2)
- `--branches N`: How many aspects to explore in parallel (default: 5)
- `--continue "topic"`: Resume a previous research session
- `--list`: Show all saved research sessions

## Database Setup

Before ANY research, initialize the database. This is mandatory:

```bash
sqlite3 research.db < ~/.claude/skills/research/schema.sql 2>/dev/null || true
```

Verify the database exists and has tables:
```bash
sqlite3 research.db "SELECT name FROM sqlite_master WHERE type='table';"
```

If tables are missing, the research CANNOT proceed.

---

# PHASE 1: SESSION INITIALIZATION

## 1.1 Create Session

```sql
INSERT INTO sessions (topic, depth_remaining, branches)
VALUES ('{topic}', {depth}, {branches});
```

Immediately retrieve and store the session ID:
```sql
SELECT last_insert_rowid();
```

**Store this session_id. You will use it in EVERY subsequent database operation.**

## 1.2 Decompose Topic into Branches

Break the topic into {branches} distinct aspects. For each aspect, create an initial "lead" finding:

```sql
INSERT INTO findings (session_id, content, relevance_score, finding_type, branch_name, depth_level)
VALUES
  ({session_id}, 'BRANCH: {aspect_1_description}', 8, 'lead', '{aspect_1_name}', 0),
  ({session_id}, 'BRANCH: {aspect_2_description}', 8, 'lead', '{aspect_2_name}', 0),
  -- ... for all branches
;
```

This seeds the graph with initial nodes to explore.

---

# PHASE 2: EXPLORATION

For each unexplored lead (finding_type='lead' that hasn't been explored):

## 2.1 Generate Search Query

Create a focused search query for the lead. Record it BEFORE executing:

```sql
INSERT INTO search_queries (session_id, query, branch_name, depth_level)
VALUES ({session_id}, '{query}', '{branch}', {current_depth});
```

## 2.2 Execute Search

```bash
python3 ~/.claude/skills/brave-search/brave.py web "{query}" --count 10 --extra-snippets
```

## 2.3 Record URLs

For EVERY URL in results, record it BEFORE fetching:

```sql
INSERT OR IGNORE INTO explored_urls (session_id, url, status)
VALUES ({session_id}, '{url}', 'pending');
```

## 2.4 Fetch and Extract

For promising URLs (top 3-5), fetch content with WebFetch. After fetching, update status:

```sql
UPDATE explored_urls SET status = 'fetched' WHERE session_id = {session_id} AND url = '{url}';
```

If fetch fails:
```sql
UPDATE explored_urls SET status = 'failed' WHERE session_id = {session_id} AND url = '{url}';
```

## 2.5 Create Findings

For EACH discrete piece of information extracted, create a finding:

```sql
INSERT INTO findings (session_id, content, source_url, relevance_score, finding_type, branch_name, depth_level)
VALUES ({session_id}, '{content}', '{url}', {score}, '{type}', '{branch}', {depth});
```

**Scoring Criteria (APPLY STRICTLY):**
- **9-10**: Directly answers a key question; novel insight; actionable
- **7-8**: Useful context; supports or challenges other findings
- **4-6**: Tangentially related; may be useful for completeness
- **1-3**: Barely relevant; keep only if nothing better exists
- **0**: Off-topic; do not insert

**Finding Types:**
- `fact`: Verifiable piece of information with source
- `lead`: Promising direction requiring further exploration
- `question`: Unresolved question raised by the research
- `theme`: Recurring pattern observed across multiple sources
- `contradiction`: Conflicting information (see Phase 3.3)

## 2.6 Update Search Query Result Count

```sql
UPDATE search_queries SET result_count = {count}
WHERE session_id = {session_id} AND query = '{query}';
```

---

# PHASE 3: GRAPH OPERATIONS

**These operations are MANDATORY after each exploration cycle.** Do not skip them.

## 3.1 MERGING: Detect and Combine Similar Findings

Similar findings fragment the graph and reduce insight quality. You MUST merge them.

**Step 1: Identify Candidates**

Query findings in the same branch that may be duplicates:

```sql
SELECT f1.id as id1, f2.id as id2, f1.content as content1, f2.content as content2
FROM findings f1
JOIN findings f2 ON f1.session_id = f2.session_id
  AND f1.branch_name = f2.branch_name
  AND f1.id < f2.id
WHERE f1.session_id = {session_id}
  AND f1.finding_type = f2.finding_type;
```

**Step 2: Evaluate Similarity**

For each pair, assess semantic similarity. Findings should be merged if:
- They state the same fact with different wording
- They cite the same source for the same claim
- One is a subset of the other

**Step 3: Execute Merge**

When merging finding B into finding A (keeping A):

```sql
-- Update A with combined content and best score
UPDATE findings
SET content = '{merged_content}',
    relevance_score = MAX(relevance_score, {b_score}),
    source_url = COALESCE(source_url, '{b_url}')
WHERE id = {a_id};

-- Transfer all relationships from B to A
UPDATE relationships SET from_finding_id = {a_id} WHERE from_finding_id = {b_id};
UPDATE relationships SET to_finding_id = {a_id} WHERE to_finding_id = {b_id};

-- Transfer entity links
UPDATE finding_entities SET finding_id = {a_id} WHERE finding_id = {b_id};

-- Delete B
DELETE FROM findings WHERE id = {b_id};
```

**Step 4: Record Merge**

Log the merge for audit trail (add to content or create a merge log table if needed).

## 3.2 RELATIONSHIP INFERENCE: Build the Graph Edges

Findings without relationships are isolated nodes. You MUST connect them.

**Relationship Types:**
- `supports`: Finding A provides evidence for Finding B
- `contradicts`: Finding A conflicts with Finding B
- `elaborates`: Finding A provides additional detail about Finding B
- `related_to`: Finding A and B discuss the same subtopic

**Step 1: Query Unconnected Findings**

```sql
SELECT f.id, f.content, f.branch_name, f.finding_type
FROM findings f
WHERE f.session_id = {session_id}
  AND f.id NOT IN (SELECT from_finding_id FROM relationships)
  AND f.id NOT IN (SELECT to_finding_id FROM relationships)
  AND f.finding_type IN ('fact', 'theme');
```

**Step 2: For Each Unconnected Finding, Find Related Findings**

```sql
SELECT id, content, branch_name FROM findings
WHERE session_id = {session_id}
  AND id != {current_id}
  AND finding_type IN ('fact', 'theme', 'lead');
```

**Step 3: Evaluate and Create Relationships**

For each potential pair, determine if a relationship exists and its type. If yes:

```sql
INSERT INTO relationships (from_finding_id, to_finding_id, relationship_type)
VALUES ({from_id}, {to_id}, '{type}');
```

**Inference Rules:**
- If Finding A cites a study and Finding B cites the same study → `related_to`
- If Finding A states X and Finding B provides mechanism for X → `supports`
- If Finding A says "X works" and Finding B says "X doesn't work" → `contradicts`
- If Finding A is general and Finding B is specific case → `elaborates`

## 3.3 CONTRADICTION DETECTION

Contradictions are HIGH-VALUE findings. They indicate uncertainty, bias, or nuance.

**Step 1: Query Potential Contradictions**

```sql
SELECT f1.id, f1.content, f1.source_url, f2.id, f2.content, f2.source_url
FROM findings f1
JOIN findings f2 ON f1.session_id = f2.session_id AND f1.id < f2.id
WHERE f1.session_id = {session_id}
  AND f1.finding_type = 'fact'
  AND f2.finding_type = 'fact'
  AND f1.branch_name = f2.branch_name;
```

**Step 2: Evaluate Each Pair**

Look for:
- Opposite claims about effectiveness
- Conflicting statistics or numbers
- Different conclusions from same evidence
- Mutually exclusive recommendations

**Step 3: Record Contradiction**

```sql
-- Create relationship
INSERT INTO relationships (from_finding_id, to_finding_id, relationship_type)
VALUES ({id1}, {id2}, 'contradicts');

-- Create a contradiction finding
INSERT INTO findings (session_id, content, relevance_score, finding_type, branch_name, depth_level)
VALUES (
  {session_id},
  'CONTRADICTION: {description of conflict between findings}. Source 1: {url1}. Source 2: {url2}. Possible explanations: {analysis}',
  9,
  'contradiction',
  '{branch}',
  {depth}
);
```

**Contradictions scoring 9+ because they reveal important nuances.**

## 3.4 ENTITY EXTRACTION AND LINKING

Entities enable cross-session knowledge and pattern detection.

**Step 1: Extract Entities from New Findings**

For each new finding, identify named entities:
- People (researchers, doctors, patients in case studies)
- Organizations (hospitals, research institutions, companies)
- Concepts (specific treatments, mechanisms, conditions)
- Technologies (devices, drugs, protocols)

**Step 2: Create or Find Entity**

```sql
-- Try to insert (will fail silently if exists due to UNIQUE constraint)
INSERT OR IGNORE INTO entities (name, entity_type) VALUES ('{name}', '{type}');

-- Get the entity ID
SELECT id FROM entities WHERE name = '{name}';
```

**Step 3: Link Finding to Entity**

```sql
INSERT OR IGNORE INTO finding_entities (finding_id, entity_id)
VALUES ({finding_id}, {entity_id});
```

---

# PHASE 4: GRAPH TRAVERSAL AND GAP ANALYSIS

After graph operations, analyze the graph structure to identify gaps.

## 4.1 Find Isolated Clusters

```sql
-- Findings with no relationships (isolated nodes)
SELECT id, content, branch_name FROM findings
WHERE session_id = {session_id}
  AND id NOT IN (SELECT from_finding_id FROM relationships)
  AND id NOT IN (SELECT to_finding_id FROM relationships);
```

Isolated nodes indicate unexplored connections. Create leads to investigate them.

## 4.2 Find Weakly Supported Claims

```sql
-- High-relevance findings with few supporting relationships
SELECT f.id, f.content, f.relevance_score, COUNT(r.id) as support_count
FROM findings f
LEFT JOIN relationships r ON r.to_finding_id = f.id AND r.relationship_type = 'supports'
WHERE f.session_id = {session_id} AND f.relevance_score >= 8
GROUP BY f.id
HAVING support_count < 2;
```

Important claims need corroboration. Create leads to find supporting evidence.

## 4.3 Find Unresolved Questions

```sql
SELECT id, content FROM findings
WHERE session_id = {session_id} AND finding_type = 'question';
```

Each question is a gap. Prioritize by relevance score.

## 4.4 Identify Unexplored Leads

```sql
SELECT f.id, f.content, f.branch_name
FROM findings f
LEFT JOIN search_queries sq ON sq.session_id = f.session_id
  AND sq.branch_name = f.branch_name
  AND sq.depth_level > f.depth_level
WHERE f.session_id = {session_id}
  AND f.finding_type = 'lead'
  AND f.relevance_score >= 7
  AND sq.id IS NULL;
```

These are leads that haven't been followed. If depth_remaining > 0, explore them.

## 4.5 Create New Leads from Gaps

For each gap identified, create a lead finding:

```sql
INSERT INTO findings (session_id, content, relevance_score, finding_type, branch_name, depth_level)
VALUES ({session_id}, 'GAP: {description}', 8, 'lead', '{branch}', {depth});
```

---

# PHASE 5: RECURSIVE EXPLORATION

If depth_remaining > 0 and unexplored leads exist:

## 5.1 Decrement Depth

```sql
UPDATE sessions SET depth_remaining = depth_remaining - 1, updated_at = CURRENT_TIMESTAMP
WHERE id = {session_id};
```

## 5.2 Select Leads to Explore

```sql
SELECT id, content, branch_name FROM findings
WHERE session_id = {session_id}
  AND finding_type = 'lead'
  AND relevance_score >= 7
ORDER BY relevance_score DESC
LIMIT {branches};
```

## 5.3 Return to Phase 2

For each selected lead, execute Phase 2 (Exploration) with the lead as the search focus.

After exploration, execute Phase 3 (Graph Operations) again.

Repeat until depth_remaining = 0 or no high-value leads remain.

---

# PHASE 6: SYNTHESIS

## 6.1 Query the Complete Graph

**Get all high-relevance findings:**
```sql
SELECT f.id, f.content, f.source_url, f.relevance_score, f.finding_type, f.branch_name
FROM findings f
WHERE f.session_id = {session_id} AND f.relevance_score >= 7
ORDER BY f.relevance_score DESC, f.branch_name;
```

**Get all relationships:**
```sql
SELECT r.*, f1.content as from_content, f2.content as to_content
FROM relationships r
JOIN findings f1 ON r.from_finding_id = f1.id
JOIN findings f2 ON r.to_finding_id = f2.id
WHERE f1.session_id = {session_id};
```

**Get all entities and their findings:**
```sql
SELECT e.name, e.entity_type, GROUP_CONCAT(f.content, ' | ') as related_findings
FROM entities e
JOIN finding_entities fe ON e.id = fe.entity_id
JOIN findings f ON fe.finding_id = f.id
WHERE f.session_id = {session_id}
GROUP BY e.id;
```

**Get contradictions:**
```sql
SELECT f.content, f.source_url FROM findings f
WHERE f.session_id = {session_id} AND f.finding_type = 'contradiction';
```

**Get unresolved questions:**
```sql
SELECT content FROM findings
WHERE session_id = {session_id} AND finding_type = 'question' AND relevance_score >= 6;
```

## 6.2 Identify Themes via Graph Structure

Themes emerge from clusters of related findings. Query for clusters:

```sql
-- Find findings with most connections (theme candidates)
SELECT f.id, f.content, f.branch_name,
       COUNT(DISTINCT r1.id) + COUNT(DISTINCT r2.id) as connection_count
FROM findings f
LEFT JOIN relationships r1 ON f.id = r1.from_finding_id
LEFT JOIN relationships r2 ON f.id = r2.to_finding_id
WHERE f.session_id = {session_id} AND f.finding_type IN ('fact', 'theme')
GROUP BY f.id
ORDER BY connection_count DESC;
```

Highly connected findings are theme centers. Group their connected findings together.

## 6.3 Generate Report

Structure the report around discovered themes, not just branches:

```markdown
# Research Report: {topic}

**Generated:** {timestamp}
**Session ID:** {session_id}
**Depth:** {depth} | **Branches:** {branch_count} | **Findings:** {finding_count} | **Relationships:** {relationship_count}

## Executive Summary
{2-3 sentences synthesizing the most important insights from the graph}

## Key Themes

### {Theme 1: derived from graph clustering}
{Narrative synthesizing findings in this cluster}

- {Finding} ([Source]({url})) [relevance: {score}]
  - Supported by: {list of supporting findings}
  - Related to: {list of related findings}

### {Theme 2}
...

## Contradictions and Nuances
{Each contradiction finding with analysis of why sources disagree}

## Evidence Quality
| Claim | Support Count | Sources | Confidence |
|-------|---------------|---------|------------|
| {claim} | {count of 'supports' relationships} | {urls} | {high/medium/low} |

## Knowledge Graph Statistics
- Total findings: {count}
- Facts: {count} | Leads: {count} | Themes: {count} | Questions: {count} | Contradictions: {count}
- Relationships: {count}
  - Supports: {count}
  - Contradicts: {count}
  - Elaborates: {count}
  - Related: {count}
- Entities identified: {count}
- URLs explored: {count}

## Open Questions
{List of 'question' type findings, prioritized by relevance}

## Unexplored Leads
{High-scoring leads that weren't followed due to depth limit}

## Sources
| Source | Findings | Relevance Range |
|--------|----------|-----------------|
| {url}  | {count}  | {min}-{max}     |
```

## 6.4 Save Report

```bash
mkdir -p research-reports
```

Write to `research-reports/{topic-slug}-report.md`

## 6.5 Update Session

```sql
UPDATE sessions SET status = 'completed', updated_at = CURRENT_TIMESTAMP
WHERE id = {session_id};
```

---

# LISTING AND CONTINUING SESSIONS

## --list

```sql
SELECT id, topic, status, created_at, updated_at,
       finding_count, high_relevance_count, urls_explored, queries_executed
FROM v_session_summary
ORDER BY updated_at DESC;
```

## --continue "{topic}"

```sql
-- Find session
SELECT id, depth_remaining FROM sessions WHERE topic LIKE '%{topic}%' AND status != 'completed';

-- Load state
SELECT COUNT(*) FROM findings WHERE session_id = {id};
SELECT COUNT(*) FROM explored_urls WHERE session_id = {id};

-- Find unexplored leads
SELECT id, content, branch_name FROM findings
WHERE session_id = {id} AND finding_type = 'lead' AND relevance_score >= 7;
```

Resume at Phase 2 with unexplored leads.

---

# ERROR HANDLING

- **Database missing:** STOP. Run schema initialization. Verify. Then proceed.
- **URL fetch fails:** Record as 'failed' in explored_urls. Continue with other URLs.
- **No findings for branch:** Insert a 'question' finding noting the gap.
- **Merge conflict:** Keep both findings, create 'related_to' relationship instead.
- **Contradiction uncertain:** Create as 'question' type, not 'contradiction'.

---

# VALIDATION CHECKLIST

Before completing synthesis, verify:

- [ ] All search queries recorded in search_queries table
- [ ] All fetched URLs recorded in explored_urls table
- [ ] All findings have relevance_score, finding_type, branch_name
- [ ] Merge operation executed (even if no merges needed)
- [ ] Relationship inference executed (graph should have edges)
- [ ] Contradiction detection executed
- [ ] Session status updated to 'completed'

Query to validate:
```sql
SELECT
  (SELECT COUNT(*) FROM findings WHERE session_id = {id}) as findings,
  (SELECT COUNT(*) FROM relationships r JOIN findings f ON r.from_finding_id = f.id WHERE f.session_id = {id}) as relationships,
  (SELECT COUNT(*) FROM explored_urls WHERE session_id = {id}) as urls,
  (SELECT COUNT(*) FROM search_queries WHERE session_id = {id}) as queries;
```

If relationships = 0, you have NOT completed the graph operations. Go back to Phase 3.
