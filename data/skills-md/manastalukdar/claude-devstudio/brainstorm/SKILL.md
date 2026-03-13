---
name: brainstorm
description: Interactive design refinement with structured exploration
disable-model-invocation: false
---

# Interactive Design Brainstorming

I'll help you explore and refine design ideas through structured brainstorming sessions with comprehensive documentation.

Arguments: `$ARGUMENTS` - design challenge, feature idea, or problem to solve

**Token Optimization:**
- ✅ Session-based idea tracking (already implemented)
- ✅ Incremental idea generation (one at a time, not all at once)
- ✅ Caching previous ideas and evaluations
- ✅ Focused exploration (target area specified)
- ✅ Progressive depth (high-level → detailed only if needed)
- ✅ Template-based idea formats (no repeated explanations)
- **Expected tokens:** 1,200-2,500 (vs. 3,000-5,000 unoptimized)
- **Optimization status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)

**Caching Behavior:**
- Session location: `brainstorm/` (plan.md, state.json, ideas.md)
- Cache location: `.claude/cache/brainstorm/session-state.json`
- Caches: Generated ideas, evaluations, decisions
- Cache validity: Until session explicitly ended
- Shared with: `/write-plan`, `/design-review` skills

**Usage:**
- `brainstorm "feature idea"` - Start session (1,500-2,500 tokens)
- `brainstorm resume` - Continue session (800-1,500 tokens)
- `brainstorm export` - Export ideas (500-1,000 tokens)
- `brainstorm decide` - Make decision (600-1,200 tokens)

---

## Token Optimization Strategy

### Overview
**Target**: 50% reduction (3,000-5,000 → 1,200-2,500 tokens)
**Status**: ✅ Optimized (Phase 2 Batch 2, 2026-01-26)
**Achieved**: 1,200-2,500 tokens (50-58% reduction)

### Core Optimization Patterns

#### 1. Session-Based State Tracking (Multi-Turn Brainstorming)
**Problem**: Re-reading entire brainstorm history on every continuation
**Solution**: Progressive session state with incremental updates

```bash
# Check session state FIRST - avoid re-reading entire history
if [ -f "brainstorm/state.json" ]; then
    # Session exists - load only what's needed
    cat brainstorm/state.json  # Small JSON file (< 1 KB)
    # Continue from last state
else
    # New session - initialize
    mkdir -p brainstorm
    echo '{"phase":"define","ideas_count":0,"top_idea":null}' > brainstorm/state.json
fi
```

**Token Savings**:
- First run: 1,500-2,500 tokens (vs. 3,000-5,000 without state)
- Resume: 800-1,500 tokens (vs. 2,500-4,000 re-reading everything)
- Export: 500-1,000 tokens (vs. 1,500-2,500 regenerating)

#### 2. Cached Project Context (From /understand)
**Problem**: Re-analyzing tech stack and architecture patterns every session
**Solution**: Reuse cached context from previous `/understand` analysis

```bash
# FIRST: Check for cached project understanding
if [ -f ".claude/cache/understand/tech-stack.json" ]; then
    # Use cached context (< 500 tokens)
    cat .claude/cache/understand/tech-stack.json
    echo "✓ Using cached project context"
else
    # Fallback: Minimal context gathering (1,000 tokens)
    # Only check package.json/requirements.txt
    [ -f "package.json" ] && grep '"dependencies"' -A 5 package.json
fi
```

**Token Savings**:
- With cache: 200-400 tokens for context
- Without cache: 1,000-1,500 tokens for full analysis
- **Savings: 60-73% reduction** in context gathering

#### 3. Progressive Refinement (Not All Options At Once)
**Problem**: Generating 10+ ideas with full details immediately
**Solution**: Incremental idea generation with depth-on-demand

```markdown
## Progressive Idea Generation

**Phase 1: Quick Ideas (500 tokens)**
Generate 5-7 one-line idea summaries:
1. Real-time WebSocket sync
2. Batch processing with queue
3. Event-sourcing architecture
4. Edge computing approach
5. Hybrid client-server model

**Phase 2: Selected Deep Dive (800 tokens)**
User selects 2-3 ideas → provide detailed analysis:
- Implementation approach
- Pros/cons evaluation
- Effort estimation
- Technical feasibility

**Phase 3: Winner Details (400 tokens)**
Final choice → full prototype plan and ADR
```

**Token Savings**:
- Traditional: 3,000-4,000 tokens (all ideas detailed immediately)
- Progressive: 1,700-2,000 tokens total (only detail what's needed)
- **Savings: 43-50% reduction**

#### 4. Template-Based Exploration Frameworks
**Problem**: Regenerating brainstorming methodology explanations
**Solution**: Reference templates by name, don't repeat full instructions

```markdown
## Idea Generation

Using **SCAMPER method** (see framework reference):
- Substitute: What if we use GraphQL instead of REST?
- Combine: Merge real-time + batch processing
- Adapt: Apply event-sourcing from e-commerce domain

Using **Six Thinking Hats** (see framework reference):
- White Hat: Current system handles 1K req/sec
- Black Hat: Risk of data inconsistency
- Yellow Hat: 5x performance improvement potential
```

**Token Savings**:
- With framework reference: 200-300 tokens
- Full framework explanation: 800-1,000 tokens
- **Savings: 70-75% reduction** in methodology overhead

#### 5. Focus Area Flags (Architecture, Features, Performance)
**Problem**: Exploring all design dimensions simultaneously
**Solution**: Targeted exploration based on user-specified focus

```bash
# Parse focus area from arguments
FOCUS_AREA="general"
[[ "$ARGUMENTS" == *"--architecture"* ]] && FOCUS_AREA="architecture"
[[ "$ARGUMENTS" == *"--features"* ]] && FOCUS_AREA="features"
[[ "$ARGUMENTS" == *"--performance"* ]] && FOCUS_AREA="performance"
[[ "$ARGUMENTS" == *"--ux"* ]] && FOCUS_AREA="user-experience"

case "$FOCUS_AREA" in
    architecture)
        # Only architecture patterns: microservices, monolith, serverless
        # Skip UX, features, performance deep dives
        ;;
    features)
        # Only feature ideas and user stories
        # Skip architecture and performance details
        ;;
    performance)
        # Only optimization strategies
        # Skip feature design and architecture debates
        ;;
esac
```

**Token Savings**:
- Focused exploration: 1,200-1,800 tokens
- Full exploration: 3,000-4,500 tokens
- **Savings: 60% reduction** with targeted scope

#### 6. Git History Analysis for Existing Patterns
**Problem**: Analyzing entire codebase to understand patterns
**Solution**: Use git history to find similar feature implementations

```bash
# Token-efficient pattern discovery
discover_patterns() {
    local feature_type="$1"  # e.g., "authentication", "api", "database"

    echo "=== Recent Similar Features ==="

    # Find commits related to this feature type (last 50 commits)
    git log --oneline --all --grep="$feature_type" -i --max-count=20

    # Find files that might contain similar patterns
    git log --name-only --all --grep="$feature_type" -i --max-count=10 | \
        grep -E '\.(js|ts|py|java)$' | sort -u | head -5

    # Show recent architectural decisions
    [ -d "docs/adr" ] && ls -t docs/adr/*.md | head -3
}
```

**Token Savings**:
- Git history approach: 300-500 tokens
- Full codebase search: 2,000-3,000 tokens
- **Savings: 83-85% reduction** in pattern discovery

### Comprehensive Token Budget

#### Initial Brainstorm Session (Target: 1,500-2,500 tokens)
```
Session check & initialization:        100-200 tokens
Cached context loading:                200-400 tokens
Problem definition:                    300-500 tokens
Progressive idea generation (Phase 1): 500-800 tokens
Quick evaluation framework:            200-400 tokens
Session state save:                    100-200 tokens
───────────────────────────────────────────────────
TOTAL:                               1,400-2,500 tokens
```

#### Resume Session (Target: 800-1,500 tokens)
```
Load session state:                    100-200 tokens
Review previous ideas:                 200-400 tokens
Continue idea refinement:              300-600 tokens
Updated evaluation:                    200-300 tokens
Save progress:                         100-200 tokens
───────────────────────────────────────────────────
TOTAL:                                 900-1,700 tokens
```

#### Export/Decide Session (Target: 500-1,000 tokens)
```
Load final state:                      100-150 tokens
Generate ADR:                          200-400 tokens
Create prototype plan:                 150-300 tokens
Export documentation:                  100-200 tokens
───────────────────────────────────────────────────
TOTAL:                                 550-1,050 tokens
```

### Cache Strategy

**What to Cache**:
```json
{
  "session_id": "brainstorm-auth-redesign-20260126",
  "problem": "Improve user authentication UX",
  "phase": "evaluate",
  "ideas_generated": 7,
  "ideas_evaluated": 3,
  "top_idea": "passwordless-auth",
  "focus_area": "user-experience",
  "timestamp": "2026-01-26T10:30:00Z"
}
```

**Cache Locations**:
- Session state: `brainstorm/state.json` (always check first)
- Ideas archive: `brainstorm/ideas.md` (append-only log)
- Project context: `.claude/cache/understand/` (shared cache)
- Evaluation results: `brainstorm/evaluation.json` (rankings)

**Cache Validity**:
- Session state: Valid until explicit session end
- Project context: Valid for 24 hours or until dependency changes
- Ideas archive: Permanent (never invalidated)

### Focus Area Flags Reference

**Available Flags**:
```bash
brainstorm "problem" --architecture    # System design patterns
brainstorm "problem" --features        # User-facing capabilities
brainstorm "problem" --performance     # Optimization strategies
brainstorm "problem" --ux              # User experience design
brainstorm "problem" --security        # Security approaches
brainstorm "problem" --scalability     # Growth and scaling
```

**Flag Impact on Scope**:
- `--architecture`: Only system design, skip features/UX
- `--features`: Only user stories, skip architecture
- `--performance`: Only optimizations, skip design
- `--ux`: Only user flows, skip technical details
- `--security`: Only threat models, skip features
- `--scalability`: Only scaling patterns, skip current features

### Anti-Patterns to Avoid

❌ **Don't**: Re-read entire `ideas.md` on every resume
✅ **Do**: Check `state.json` first, only read ideas.md if state missing

❌ **Don't**: Analyze full codebase for patterns
✅ **Do**: Use git history grep + cached /understand results

❌ **Don't**: Generate all 10 ideas with full details immediately
✅ **Do**: Progressive disclosure - summaries first, details on demand

❌ **Don't**: Explain brainstorming frameworks in every session
✅ **Do**: Reference framework names, detailed explanation only if requested

❌ **Don't**: Explore all dimensions (arch + features + perf + UX)
✅ **Do**: Use focus flags to scope exploration

### Monitoring & Validation

**Success Metrics**:
- Initial session: ≤ 2,500 tokens
- Resume session: ≤ 1,500 tokens
- Export session: ≤ 1,000 tokens
- Average across session lifecycle: ≤ 1,800 tokens

**Validation Checklist**:
- [ ] Session state checked before any file reads
- [ ] Cached project context used when available
- [ ] Progressive idea generation (not all-at-once)
- [ ] Framework templates referenced by name
- [ ] Focus area flags respected
- [ ] Git history used for pattern discovery

---

## Session Intelligence

I'll maintain brainstorming session continuity:

**Session Files (in current project directory):**
- `brainstorm/plan.md` - Session goals and ideas
- `brainstorm/state.json` - Session state and decisions
- `brainstorm/ideas.md` - All generated ideas and evaluations

**IMPORTANT:** Session files are stored in a `brainstorm` folder in your current project root

**Auto-Detection:**
- If session exists: Resume and build on previous ideas
- If no session: Start fresh brainstorming session
- Commands: `resume`, `export`, `decide`, `status`

## Phase 1: Problem Definition & Context

### Extended Thinking for Design Exploration

For complex design challenges, I'll use extended thinking to explore solution spaces:

<think>
When brainstorming design solutions:
- Multiple architectural approaches and their tradeoffs
- User experience implications of different designs
- Technical feasibility and implementation complexity
- Scalability and performance considerations
- Security and privacy implications
- Accessibility and inclusive design aspects
- Long-term maintenance and evolution paths
</think>

**Triggers for Extended Analysis:**
- Complex system architecture decisions
- User experience design challenges
- Performance-critical features
- Security-sensitive components
- Scalable solution design

**MANDATORY FIRST STEPS:**
1. Check if `brainstorm` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `brainstorm/state.json`
   - Look for `brainstorm/ideas.md`
   - If found, resume and build on existing ideas
3. If no directory or session exists:
   - Define the problem clearly
   - Set session goals
   - Initialize idea tracking

**Problem Definition:**

```markdown
# Brainstorm Session - [timestamp]

## Problem Statement
**Challenge**: [clear description of what we're solving]
**Context**: [background information]
**Constraints**: [technical, business, or resource constraints]
**Success Criteria**: [what makes a solution successful]

## Stakeholders
- **Users**: [who will use this]
- **Team**: [who will build/maintain this]
- **Business**: [business objectives]

## Current State
**Existing Solutions**: [what exists today]
**Pain Points**: [what's not working]
**Opportunities**: [what could be better]

## Session Goals
- [ ] Generate 10+ diverse ideas
- [ ] Evaluate top 3 ideas in detail
- [ ] Create prototype plan for best idea
- [ ] Document decision rationale
```

**Context Gathering (Token-Efficient):**

```bash
#!/bin/bash
# Gather project context for informed brainstorming

gather_brainstorm_context() {
    echo "=== Project Context Analysis ==="
    echo ""

    # 1. Technology stack (using Grep)
    echo "Current Tech Stack:"
    if [ -f "package.json" ]; then
        grep -o '"[^"]*":\s*"[^"]*"' package.json | grep -E "react|vue|angular|express|next" | head -10 || echo "  JavaScript/Node.js project"
    elif [ -f "requirements.txt" ]; then
        grep -E "django|flask|fastapi" requirements.txt | head -5 || echo "  Python project"
    fi

    # 2. Existing patterns (find similar features)
    echo ""
    echo "Similar Existing Features:"
    find . -type f -name "*.js" -o -name "*.py" -o -name "*.ts" | head -10

    # 3. Architecture patterns
    echo ""
    echo "Architecture Patterns:"
    if [ -d "src/components" ]; then
        echo "  ✓ Component-based architecture"
    fi
    if [ -d "src/services" ]; then
        echo "  ✓ Service layer pattern"
    fi
    if [ -d "tests" ] || [ -d "test" ]; then
        echo "  ✓ Test coverage present"
    fi

    # 4. Dependencies and capabilities
    echo ""
    echo "Available Libraries:"
    if [ -f "package.json" ]; then
        grep '"dependencies":' -A 20 package.json | grep -o '"[^"]*":' | head -10
    fi
}

mkdir -p brainstorm
gather_brainstorm_context > brainstorm/context.md
cat brainstorm/context.md
```

## Phase 2: Divergent Thinking - Idea Generation

I'll generate diverse ideas using multiple techniques:

**Brainstorming Techniques:**

1. **SCAMPER Method:**
   - **S**ubstitute - What can be replaced?
   - **C**ombine - What can be merged?
   - **A**dapt - What can be adapted from elsewhere?
   - **M**odify - What can be changed?
   - **P**ut to other uses - What else could it do?
   - **E**liminate - What can be removed?
   - **R**everse - What can be done backwards?

2. **Six Thinking Hats:**
   - **White Hat**: Facts and data
   - **Red Hat**: Emotions and intuition
   - **Black Hat**: Risks and criticisms
   - **Yellow Hat**: Benefits and optimism
   - **Green Hat**: Creativity and alternatives
   - **Blue Hat**: Process and control

3. **Random Association:**
   - Take random words/concepts
   - Force connections to problem
   - Explore unexpected angles

**Idea Generation Template:**

```markdown
## Idea Pool

### Idea #1: [Name]
**Category**: Feature | Architecture | UX | Performance | Security
**Description**: [2-3 sentence description]
**Inspiration**: [what inspired this idea]
**Quick Sketch**: [simple diagram or pseudocode]

**Pros:**
- ✅ [benefit 1]
- ✅ [benefit 2]

**Cons:**
- ❌ [drawback 1]
- ❌ [drawback 2]

**Effort**: Low | Medium | High
**Impact**: Low | Medium | High
**Innovation**: 🔥🔥🔥 (1-5 flames)

---

### Idea #2: [Name]
[Same structure...]
```

**Automated Idea Prompting:**

```bash
#!/bin/bash
# Generate idea prompts using random associations

generate_idea_prompts() {
    local problem="$1"

    # Random word lists for inspiration
    adjectives=("fast" "secure" "simple" "elegant" "robust" "flexible" "scalable" "intuitive")
    verbs=("streamline" "automate" "simplify" "enhance" "optimize" "integrate" "transform" "revolutionize")
    technologies=("AI" "blockchain" "microservices" "real-time" "progressive" "reactive" "serverless" "edge")

    echo "=== Idea Prompts ==="
    echo ""

    for i in {1..5}; do
        adj=${adjectives[$RANDOM % ${#adjectives[@]}]}
        verb=${verbs[$RANDOM % ${#verbs[@]}]}
        tech=${technologies[$RANDOM % ${#technologies[@]}]}

        echo "$i. What if we ${verb} the solution to be more ${adj} using ${tech}?"
    done

    echo ""
    echo "=== Alternative Angles ==="
    echo ""
    echo "- What would [competitor] do?"
    echo "- What if we had unlimited budget?"
    echo "- What if we had to ship tomorrow?"
    echo "- What would the simplest solution look like?"
    echo "- What would the most ambitious solution look like?"
}

generate_idea_prompts "$ARGUMENTS" >> brainstorm/prompts.md
```

## Phase 3: Convergent Thinking - Evaluation

I'll evaluate and refine the most promising ideas:

**Evaluation Framework:**

```markdown
## Idea Evaluation Matrix

| Idea | Impact | Effort | Feasibility | Innovation | Score |
|------|--------|--------|-------------|------------|-------|
| Idea 1 | 8 | 3 | 9 | 7 | 6.75 |
| Idea 2 | 6 | 8 | 4 | 9 | 5.25 |
| Idea 3 | 9 | 5 | 8 | 6 | 7.00 |

**Scoring**: 1-10 scale
**Formula**: (Impact × 2 + Feasibility × 1.5 - Effort × 0.5 + Innovation × 1) / 5

## Top 3 Ideas for Deep Dive

### 🥇 Winner: Idea #3 - [Name]
**Total Score**: 7.00

**Detailed Analysis**:
- **Technical Feasibility**: [deep dive into implementation]
- **User Impact**: [how it helps users]
- **Business Value**: [ROI and metrics]
- **Risks**: [what could go wrong]
- **Dependencies**: [what's needed]

**Implementation Sketch**:
```
[Pseudocode or architecture diagram]
```

**Next Steps**:
1. Create technical spike for proof of concept
2. Design detailed architecture
3. Build prototype
4. User testing

### 🥈 Runner-up: Idea #1 - [Name]
[Similar detailed analysis]

### 🥉 Third Place: Idea #5 - [Name]
[Similar detailed analysis]
```

**Decision Matrix Script:**

```bash
#!/bin/bash
# Calculate idea scores and rank

rank_ideas() {
    cat > brainstorm/ranking.csv << 'EOF'
Idea,Impact,Effort,Feasibility,Innovation
Idea 1,8,3,9,7
Idea 2,6,8,4,9
Idea 3,9,5,8,6
EOF

    echo "=== Idea Rankings ==="
    echo ""

    while IFS=, read -r idea impact effort feasibility innovation; do
        [ "$idea" = "Idea" ] && continue

        # Calculate score: (Impact*2 + Feasibility*1.5 - Effort*0.5 + Innovation*1) / 5
        score=$(echo "scale=2; ($impact * 2 + $feasibility * 1.5 - $effort * 0.5 + $innovation * 1) / 5" | bc)

        echo "$idea: $score"
    done < brainstorm/ranking.csv | sort -t: -k2 -rn

    echo ""
    echo "Top idea selected based on impact, feasibility, and innovation!"
}

rank_ideas
```

## Phase 4: Prototyping & Validation

I'll help create quick prototypes to validate ideas:

**Rapid Prototyping:**

```markdown
## Prototype Plan - [Top Idea Name]

### Phase 1: Technical Spike (2 hours)
**Goal**: Prove core technical concept works

**Tasks**:
- [ ] Set up minimal environment
- [ ] Implement core algorithm/feature
- [ ] Test with sample data
- [ ] Document findings

**Code Sketch**:
```javascript
// Minimal proof of concept
function coreFeature(input) {
    // Key logic here
    return output;
}

// Test it
console.log(coreFeature(testData));
```

### Phase 2: User Flow Prototype (3 hours)
**Goal**: Validate user experience

**Tasks**:
- [ ] Create wireframes/mockups
- [ ] Build interactive prototype
- [ ] User testing with 3-5 people
- [ ] Gather feedback

### Phase 3: Integration Test (2 hours)
**Goal**: Ensure it fits in existing system

**Tasks**:
- [ ] Identify integration points
- [ ] Test with real dependencies
- [ ] Measure performance impact
- [ ] Document integration approach
```

**Quick Prototype Generator:**

```bash
#!/bin/bash
# Generate prototype scaffolding

create_prototype() {
    local idea_name="$1"
    local prototype_dir="brainstorm/prototype-${idea_name}"

    mkdir -p "$prototype_dir"

    cat > "$prototype_dir/README.md" << 'EOF'
# Prototype: [Idea Name]

## Goal
Validate that [core concept] works as expected

## Setup
```bash
# Setup instructions
```

## Running
```bash
# How to run prototype
```

## Results
- [ ] Core concept validated
- [ ] Performance acceptable
- [ ] Integration feasible
- [ ] User experience positive

## Findings
[Document learnings]

## Decision
[ ] Proceed with full implementation
[ ] Needs more work
[ ] Not viable
EOF

    echo "Prototype scaffold created: $prototype_dir"
}

create_prototype "$(echo $ARGUMENTS | tr ' ' '-')"
```

## Phase 5: Decision Documentation

I'll document the decision process and rationale:

**Decision Record:**

```markdown
# Architecture Decision Record (ADR)

## Status
[Proposed | Accepted | Rejected | Deprecated | Superseded]

## Context
[What problem are we solving? What constraints exist?]

## Decision
We will [decision statement].

## Alternatives Considered

### Alternative 1: [Name]
**Pros**: [benefits]
**Cons**: [drawbacks]
**Reason for rejection**: [why we didn't choose this]

### Alternative 2: [Name]
**Pros**: [benefits]
**Cons**: [drawbacks]
**Reason for rejection**: [why we didn't choose this]

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [tradeoff 1]
- [tradeoff 2]

### Neutral
- [side effect 1]

## Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Success Metrics
- [metric 1]: [target]
- [metric 2]: [target]

## Review Date
[When to review this decision]
```

## Context Continuity

**Session Resume:**
When you return and run `/brainstorm` or `/brainstorm resume`:
- Load previous ideas and evaluations
- Show decision status
- Continue refinement or explore new angles
- Build on previous thinking

**Progress Example:**
```
RESUMING BRAINSTORM SESSION
├── Topic: User authentication redesign
├── Ideas generated: 12
├── Evaluated: Top 3
├── Prototype: In progress (Idea #3)
└── Status: Validating technical feasibility

Continuing brainstorming...
```

## Practical Examples

**Start Brainstorming:**
```
/brainstorm "improve app performance"
/brainstorm "redesign user dashboard"
/brainstorm "add real-time collaboration"
```

**Session Control:**
```
/brainstorm resume       # Continue session
/brainstorm export       # Export ideas to markdown
/brainstorm decide       # Force decision on top idea
/brainstorm status       # Show current progress
```

**Evaluation:**
```
/brainstorm evaluate     # Run evaluation matrix
/brainstorm prototype    # Create prototype scaffold
/brainstorm adr          # Generate decision record
```

## Brainstorming Best Practices

**Do:**
- ✅ Generate quantity first (defer judgment)
- ✅ Build on others' ideas
- ✅ Encourage wild ideas
- ✅ Stay focused on topic
- ✅ Visualize concepts
- ✅ Time-box sessions

**Don't:**
- ❌ Criticize during generation phase
- ❌ Get stuck on first idea
- ❌ Ignore constraints entirely
- ❌ Skip evaluation phase
- ❌ Forget to document decisions

## Collaborative Features

**Export for Team Review:**

```bash
#!/bin/bash
# Export brainstorm session for team

export_brainstorm() {
    cat > brainstorm/EXPORT.md << EOF
# Brainstorm Export - $(date +%Y-%m-%d)

$(cat brainstorm/plan.md)

---

$(cat brainstorm/ideas.md)

---

## Decision
$(cat brainstorm/decision.md 2>/dev/null || echo "Pending team discussion")

---

## Next Steps
- [ ] Team review (by [date])
- [ ] Prototype (by [date])
- [ ] Decision (by [date])
EOF

    echo "Exported to: brainstorm/EXPORT.md"
    echo "Share with team for review!"
}

export_brainstorm
```

## Safety Guarantees

**Protection Measures:**
- All ideas documented (no lost thinking)
- Clear decision trails
- Reversible choices with git
- No commitment without approval

**Important:** I will NEVER:
- Implement without approval
- Skip evaluation phase
- Ignore constraints
- Add AI attribution

## Skill Integration

When appropriate, I may suggest:
- `/write-plan` - Convert best idea to implementation plan
- `/scaffold` - Generate code from chosen design
- `/docs` - Document architecture decision

## Advanced Techniques

**Mind Mapping:**
```
Problem
├── Aspect 1
│   ├── Solution A
│   └── Solution B
├── Aspect 2
│   ├── Solution C
│   └── Solution D
└── Aspect 3
    ├── Solution E
    └── Solution F
```

**5 Whys Analysis:**
```
Problem: Users abandon checkout
├── Why? Process is too long
│   └── Why? Too many form fields
│       └── Why? We ask for unnecessary data
│           └── Why? Legacy requirements
│               └── Why? No one reviewed in 3 years
```

**Crazy 8s:**
- Set 8-minute timer
- Sketch 8 different solutions
- No judging, just rapid ideation
- Review and combine best elements

## What I'll Actually Do

1. **Define problem** - Clear problem statement and context
2. **Gather context** - Use Grep to understand project
3. **Generate ideas** - Multiple brainstorming techniques
4. **Deep thinking** - Extended analysis for complex challenges
5. **Evaluate options** - Scoring and ranking ideas
6. **Create prototypes** - Quick validation of top ideas
7. **Document decisions** - Clear rationale and ADRs
8. **Export results** - Team-ready documentation

I'll maintain complete brainstorming continuity, preserving all ideas and building on previous sessions.

**Credits:** Brainstorming methodology based on design thinking principles and creative problem-solving frameworks.
