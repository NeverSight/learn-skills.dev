---
name: skill-finder
description: Find and evaluate Claude skills for specific use cases using semantic search, Anthropic best practices assessment, and fitness scoring. Use when the user asks to find skills for a particular task (e.g., "find me a skill for pitch decks"), not for generic "show all skills" requests.
---

# Skill Finder

Find and evaluate Claude skills for your specific needs with intelligent semantic search, quality assessment, and fitness scoring.

## What This Skill Does

Skill-finder is a query-driven evaluation engine that:
- Searches GitHub for skills matching your specific use case
- Fetches and reads actual SKILL.md content
- Evaluates skills against Anthropic's best practices
- Scores fitness to your exact request
- Provides actionable quality assessments and recommendations

This is NOT a "show me popular skills" tool - it's a semantic matcher that finds the RIGHT skill for YOUR specific need.

## When to Use

- User asks to find skills for a **specific purpose**: "find me a skill for creating pitch decks"
- User needs help choosing between similar skills
- User wants quality-assessed recommendations, not just popularity rankings
- User asks "what's the best skill for [specific task]"

## Quick Start Examples

```bash
# Find skills for specific use case
"Find me a skill for creating pitch decks"
"What's the best skill for automated data analysis"
"Find skills that help with git commit messages"

# NOT: "Show me popular skills" (too generic)
# NOT: "List all skills" (use skill list command instead)
```

## Core Workflow

### Phase 1: Query Understanding

**Extract semantic terms from user query:**

User: "Find me a skill for creating pitch decks"

Extract terms:
- Primary: "pitch deck", "presentation"
- Secondary: "slides", "powerpoint", "keynote"
- Related: "business", "template"

### Phase 2: Multi-Source Search

**Search Strategy:**

```bash
# 1. Repository search with semantic terms
gh search repos "claude skills pitch deck OR presentation OR slides" \
  --sort stars --limit 20 --json name,stargazersCount,description,url,pushedAt,owner

# 2. Code search for SKILL.md with keywords
gh search code "pitch deck OR presentation" "filename:SKILL.md" \
  --limit 20 --json repository,path,url

# 3. Search awesome-lists separately
gh search repos "awesome-claude-skills" --sort stars --limit 5 \
  --json name,url,owner
```

**Deduplication:**
Collect all unique repositories from search results.

### Phase 3: Content Fetching

**For each candidate skill:**

```bash
# 1. Find SKILL.md location
gh api repos/OWNER/REPO/git/trees/main?recursive=1 | \
  jq -r '.tree[] | select(.path | contains("SKILL.md")) | .path'

# 2. Fetch full SKILL.md content
gh api repos/OWNER/REPO/contents/PATH/TO/SKILL.md | \
  jq -r '.content' | base64 -d > temp_skill.md

# 3. Fetch repository metadata
gh api repos/OWNER/REPO --jq '{
  stars: .stargazers_count,
  updated: .pushed_at,
  description: .description
}'
```

**IMPORTANT:** Actually READ the SKILL.md content. Don't just use metadata.

### Phase 4: Quality Evaluation

**Use [best-practices-checklist.md](references/best-practices-checklist.md) to evaluate:**

For each skill, assess:

1. **Description Quality (2.0 points)**
   - Specific vs vague?
   - Includes what + when to use?
   - Third person?

2. **Name Convention (0.5 points)**
   - Follows naming rules?
   - Descriptive?

3. **Conciseness (1.5 points)**
   - Under 500 lines?
   - No fluff?

4. **Progressive Disclosure (1.0 points)**
   - Uses reference files?
   - Good organization?

5. **Examples and Workflows (1.0 points)**
   - Has concrete examples?
   - Clear workflows?

6. **Appropriate Degree of Freedom (0.5 points)**
   - Matches task complexity?

7. **Dependencies (0.5 points)**
   - Documented?
   - Verified available?

8. **Structure (1.0 points)**
   - Well organized?
   - Clear sections?

9. **Error Handling (0.5 points)**
   - Scripts handle errors?
   - Validation loops?

10. **Avoids Anti-Patterns (1.0 points)**
    - No time-sensitive info?
    - Consistent terminology?
    - Unix paths?

11. **Testing (0.5 points)**
    - Evidence of testing?

**Calculate quality_score (0-10):**
See [best-practices-checklist.md](references/best-practices-checklist.md) for detailed scoring.

### Phase 5: Fitness Scoring

**Semantic match calculation:**

```python
# Pseudo-code for semantic matching
user_query_terms = ["pitch", "deck", "presentation"]
skill_content = read_skill_md(skill_path)

# Check occurrences of user terms in skill
matches = []
for term in user_query_terms:
    if term.lower() in skill_content.lower():
        matches.append(term)

semantic_match_score = len(matches) / len(user_query_terms) * 10
```

**Fitness formula:**
```
fitness_score = (
  semantic_match * 0.4 +          # How well does it solve the problem?
  quality_score * 0.3 +            # Follows best practices?
  (stars/100) * 0.2 +              # Community validation
  freshness_multiplier * 0.1       # Recent updates
)

Where:
- semantic_match: 0-10 (keyword matching in SKILL.md content)
- quality_score: 0-10 (from evaluation checklist)
- stars: repository star count
- freshness_multiplier: 0-10 based on days since update
```

**Freshness multiplier:**
```bash
days_old=$(( ($(date +%s) - $(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$pushed_at" +%s)) / 86400 ))

if [ $days_old -lt 30 ]; then
  freshness_score=10
  freshness_badge="🔥"
elif [ $days_old -lt 90 ]; then
  freshness_score=7
  freshness_badge="📅"
elif [ $days_old -lt 180 ]; then
  freshness_score=5
  freshness_badge="📆"
else
  freshness_score=2
  freshness_badge="⏰"
fi
```

### Phase 6: Awesome-List Processing

**Extract skills from awesome-lists:**

```bash
# For each awesome-list found
for repo in awesome_lists; do
  # Fetch README or main content
  gh api repos/$repo/readme | jq -r '.content' | base64 -d > readme.md

  # Extract GitHub links to potential skills
  grep -oE 'https://github.com/[^/]+/[^/)]+' readme.md | sort -u

  # For each linked repo, check if it contains SKILL.md
  # If yes, evaluate same as other skills
done
```

**Display awesome-list skills separately** in results for comparison.

### Phase 7: Result Ranking and Display

**Sort by fitness_score (descending)**

**Output format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Skills for: "[USER QUERY]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 #1 skill-name ⭐ STARS FRESHNESS | FITNESS: X.X/10

   Quality Assessment:
   ✅ Description: Excellent (2.0/2.0)
   ✅ Structure: Well organized (0.9/1.0)
   ⚠️  Length: 520 lines (over recommended 500)
   ✅ Examples: Clear workflows included

   Overall Quality: 8.5/10 (Excellent)

   Why it fits your request:
   • Specifically designed for [relevant aspect]
   • Mentions [user's key terms] 3 times
   • Has [relevant feature]
   • Includes [useful capability]

   Why it's high quality:
   • Follows Anthropic best practices
   • Has comprehensive examples
   • Clear workflows and validation
   • Well-tested and maintained

   📎 https://github.com/OWNER/REPO/blob/main/PATH/SKILL.md

   [Preview Full Analysis] [Install]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 #2 another-skill ⭐ STARS FRESHNESS | FITNESS: Y.Y/10

   Quality Assessment:
   ✅ Good description and examples
   ⚠️  Some best practices not followed
   ❌ No progressive disclosure

   Overall Quality: 6.2/10 (Good)

   Why it fits your request:
   • Partially addresses [need]
   • Has [some relevant feature]

   Why it's not ideal:
   • Not specifically focused on [user's goal]
   • Quality could be better
   • Missing [important feature]

   📎 https://github.com/OWNER/REPO/blob/main/SKILL.md

   [Preview] [Install]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 From Awesome Lists:

Found in awesome-claude-skills (BehiSecc):
  • related-skill-1 (FITNESS: 7.5/10) - Good match
  • related-skill-2 (FITNESS: 5.2/10) - Partial match

Found in awesome-claude-skills (travisvn):
  • another-option (FITNESS: 6.8/10) - Consider this

[Evaluate All] [Show Details]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Recommendation: skill-name (FITNESS: 8.7/10)

   Best match for your needs. High quality, well-maintained,
   and specifically designed for [user's goal].

   Next best: another-skill (FITNESS: 7.2/10) if you need [alternative approach]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Key Differences from Generic Search

**Generic/Bad approach:**
- "Show me top 10 popular skills"
- Ranks only by stars
- No evaluation of actual content
- No fitness to user's specific need

**Query-Driven/Good approach:**
- "Find skills for [specific use case]"
- Reads actual SKILL.md content
- Evaluates against best practices
- Scores fitness to user's query
- Explains WHY it's a good match

## Evaluation Workflow

### Quick Evaluation (per skill ~3-4 min)

1. **Fetch SKILL.md** (30 sec)
2. **Read frontmatter** (30 sec)
   - Check description quality
   - Check name convention
3. **Scan body** (1-2 min)
   - Check length
   - Look for examples
   - Check for references
   - Note anti-patterns
4. **Check structure** (30 sec)
   - Reference files?
   - Scripts/utilities?
5. **Calculate scores** (30 sec)
   - Quality score
   - Semantic match
   - Fitness score

### Full Evaluation (for top candidates)

For the top 3-5 candidates by fitness score, provide detailed analysis:

```
Full Analysis for: [skill-name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Quality Breakdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description Quality:      2.0/2.0 ✅
  • Specific and clear
  • Includes what and when to use
  • Written in third person

Name Convention:          0.5/0.5 ✅
  • Follows naming rules
  • Descriptive gerund form

Conciseness:              1.3/1.5 ⚠️
  • 520 lines (over 500 recommended)
  • Could be more concise

Progressive Disclosure:   1.0/1.0 ✅
  • Excellent use of reference files
  • Well-organized structure

Examples & Workflows:     1.0/1.0 ✅
  • Clear concrete examples
  • Step-by-step workflows

Degree of Freedom:        0.5/0.5 ✅
  • Appropriate for task type

Dependencies:             0.5/0.5 ✅
  • All documented
  • Verified available

Structure:                0.9/1.0 ✅
  • Well organized
  • Minor heading inconsistencies

Error Handling:           0.4/0.5 ⚠️
  • Good scripts
  • Could improve validation

Anti-Patterns:            0.9/1.0 ✅
  • Mostly clean
  • One instance of inconsistent terminology

Testing:                  0.5/0.5 ✅
  • Clear testing approach

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Quality Score: 8.5/10 (Excellent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Semantic Match Analysis

User Query: "pitch deck creation"
Skill Content Analysis:
  ✅ "pitch deck" mentioned 5 times
  ✅ "presentation" mentioned 12 times
  ✅ "slides" mentioned 8 times
  ✅ Has templates section
  ✅ Has business presentation examples

Semantic Match Score: 9.2/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Final FITNESS Score: 8.8/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: Highly Recommended ⭐⭐⭐⭐⭐
```

## Reference Files

- [best-practices-checklist.md](references/best-practices-checklist.md) - Anthropic's best practices evaluation criteria
- [search-strategies.md](references/search-strategies.md) - Advanced search patterns
- [ranking-algorithm.md](references/ranking-algorithm.md) - Detailed scoring algorithms
- [installation-workflow.md](references/installation-workflow.md) - Installation process

## Example Usage

See [examples/sample-output.md](examples/sample-output.md) for complete output examples.

## Error Handling

**No results found:**
```
No skills found for: "[user query]"

Suggestions:
• Try broader search terms
• Check if query is too specific
• Search awesome-lists directly
• Consider creating a custom skill
```

**Low fitness scores (all < 5.0):**
```
⚠️  Found skills but none are a strong match.

Best partial matches:
1. [skill-name] (FITNESS: 4.2/10) - Missing [key feature]
2. [skill-name] (FITNESS: 3.8/10) - Different focus

Consider:
• Combine multiple skills
• Request skill from awesome-list curators
• Create custom skill for your specific need
```

**GitHub API rate limit:**
```
⚠️  GitHub API rate limit reached.

Current: 0/60 requests remaining (unauthenticated)
Resets: in 42 minutes

Solution:
export GH_TOKEN="your_github_token"

This increases limit to 5000/hour.
```

## Performance Optimization

**Parallel execution:**
```bash
# Run searches in parallel
{
  gh search repos "claude skills $QUERY" > repos.json &
  gh search code "$QUERY" "filename:SKILL.md" > code.json &
  gh search repos "awesome-claude-skills" > awesome.json &
  wait
}
```

**Caching:**
```bash
# Cache skill evaluations for 1 hour
cache_file=".skill-eval-cache/$repo_owner-$repo_name.json"
if [ -f "$cache_file" ] && [ $(($(date +%s) - $(stat -f %m "$cache_file"))) -lt 3600 ]; then
  cat "$cache_file"
else
  evaluate_skill | tee "$cache_file"
fi
```

## Quality Tiers

Based on fitness score:

- **9.0-10.0:** Perfect match - Highly Recommended ⭐⭐⭐⭐⭐
- **7.0-8.9:** Excellent match - Recommended ⭐⭐⭐⭐
- **5.0-6.9:** Good match - Consider ⭐⭐⭐
- **3.0-4.9:** Partial match - Review carefully ⭐⭐
- **0.0-2.9:** Poor match - Not recommended ⭐

## Important Notes

### This is NOT:
- A "show popular skills" tool
- A generic ranking by stars
- A list of all skills

### This IS:
- A query-driven semantic matcher
- A quality evaluator against Anthropic best practices
- A fitness scorer for your specific need
- A recommendation engine

### Always:
- Read actual SKILL.md content (don't just use metadata)
- Evaluate against best practices checklist
- Score fitness to user's specific query
- Explain WHY a skill fits or doesn't fit
- Show quality assessment, not just stars

---

**Remember:** The goal is to find the RIGHT skill for the user's SPECIFIC need, not just show what's popular.
