---
name: agent-skill-orchestrator
description: This skill should be used when the user needs to solve a complex task and wants a detailed execution plan using the best available resources. Analyzes user requirements, discovers available plugins/agents/skills/MCPs, performs intelligent matching with confidence scoring, and creates strategic execution plans with alternatives. Works across all AI CLI platforms.
license: MIT
---

# agent-skill-orchestrator

## Purpose

Intelligent task planning and resource orchestration engine that analyzes user requirements and creates strategic execution plans using the best available resources. This skill performs automated discovery, intelligent matching with confidence scoring, and generates comprehensive plans with multiple options and fallback strategies.

The orchestrator operates as a planning assistant—it recommends approaches but always requests explicit user approval before execution. It serves as the intelligence layer above the discovery foundation, transforming "what do I have" into "how should I use it".

## When to Use

Invoke this skill when:

- User has a complex task requiring multiple steps or resources
- User wants to know the best approach to solve a problem
- User needs coordination between multiple plugins, agents, skills, or MCPs
- User wants optimized resource utilization for a task
- User is unsure which tools or approach to use
- User needs a strategic plan before implementation
- User wants to explore multiple solution approaches

## Platform Support

Works identically on all AI CLI platforms:
- **Claude Code** (`claude`)
- **GitHub Copilot CLI** (`gh copilot`)
- **Gemini CLI** (`gemini`)
- **OpenCode** (`opencode`)
- **OpenAI Codex** (`codex`)

## Progress Tracking

Display progress before each orchestration phase:

```
[██░░░░░░░░░░░░░░░░░░] 15% — Step 0: Discovering Available Resources
[████░░░░░░░░░░░░░░░░] 25% — Step 1: Analyzing User Request
[████████░░░░░░░░░░░░] 45% — Step 2: Intelligent Matching & Scoring
[████████████░░░░░░░░] 65% — Step 3: Generating Execution Plan
[██████████████████░░] 85% — Step 4: Presenting Plan for Approval
[████████████████████] 100% — Step 5: Plan Approved / Execution Ready
```

## Workflow

### Step -1: Prompt Quality Check (Pre-Analysis)

**Objective:** Ensure user request is clear and well-structured before planning.

**Why This Step Matters:**
- Vague prompts → poor resource matching → low-quality plans
- Optimized prompts → precise requirements → high-confidence plans
- Reduces planning iterations and "Refine plan" cycles

**Prompt Quality Assessment:**

```javascript
function assessPromptQuality(userRequest) {
  const qualityIssues = [];

  // Too vague or generic
  if (userRequest.length < 20) {
    qualityIssues.push('too_short');
  }

  // Missing specifics
  const hasSpecifics = /\b(using|with|for|create|build|implement|analyze)\b/i.test(userRequest);
  if (!hasSpecifics) {
    qualityIssues.push('lacks_specifics');
  }

  // No clear goal
  const hasVerb = /\b(create|build|analyze|process|integrate|automate|design)\b/i.test(userRequest);
  if (!hasVerb) {
    qualityIssues.push('unclear_goal');
  }

  // Ambiguous references
  const hasAmbiguity = /\b(this|that|it|these|those)\b/i.test(userRequest);
  if (hasAmbiguity && userRequest.split(' ').length < 10) {
    qualityIssues.push('ambiguous_reference');
  }

  return {
    needsOptimization: qualityIssues.length >= 2,
    issues: qualityIssues,
    score: Math.max(0, 100 - (qualityIssues.length * 25))
  };
}
```

**Decision Logic:**

```javascript
const quality = assessPromptQuality(userRequest);

if (quality.needsOptimization && quality.score < 50) {
  // Call prompt-engineer to refine
  const optimizedRequest = await invokeSkill('prompt-engineer', {
    rawPrompt: userRequest,
    context: 'task-planning',
    targetFramework: 'RISEN' // Requirements, Instructions, Steps, Expectations, Nuances
  });

  // Use optimized prompt for subsequent steps
  return optimizedRequest.refinedPrompt;

} else {
  // Prompt is clear enough, proceed with original
  return userRequest;
}
```

**Example Transformation:**

```yaml
# Before Optimization (Quality: 25%)
userRequest: "help me with API stuff"

# After prompt-engineer (Quality: 90%)
optimizedRequest: |
  Design and implement a RESTful API with:
  - Authentication using JWT tokens
  - CRUD operations for user management
  - Error handling and input validation
  - API documentation (Swagger/OpenAPI)
  - Unit and integration tests
  - Following REST best practices

improvementScore: 85%
```

**Impact on Planning:**
- ✅ Confidence scores increase 20-30%
- ✅ More accurate resource matching
- ✅ Better success criteria definition
- ✅ Reduced ambiguity in plan execution

---

### Step 0: Discover Available Resources

**Objective:** Obtain fresh inventory of all installed resources.

**Critical Dependency:** This skill MUST call `agent-skill-discovery` first.

**Actions:**

Invoke the discovery skill to get complete resource catalog:

```bash
# Call agent-skill-discovery skill
resources = invokeSkill("agent-skill-discovery")
```

**Expected Output:**

```json
{
  "platform": "Claude Code",
  "plugins": [
    {
      "name": "feature-dev",
      "agents": [
        {
          "name": "code-explorer",
          "description": "Analyzes existing codebase",
          "tools": ["Glob", "Grep", "Read", "Bash"]
        }
      ]
    }
  ],
  "skills": [
    {
      "name": "skill-creator",
      "description": "Creates new skills",
      "triggers": ["create a skill", "new skill"],
      "category": "development"
    }
  ],
  "mcpServers": [
    {
      "name": "claude_ai_Notion",
      "type": "stdio",
      "tools": ["notion-search", "notion-create-pages"]
    }
  ]
}
```

**Why This Step is Critical:**

- Ensures fresh, accurate resource availability
- Works across all platforms (discovery handles platform detection)
- Provides complete context for intelligent matching
- Avoids recommending unavailable resources

### Step 1: Analyze User Request

**Objective:** Extract requirements from user's task description.

**Actions:**

**1.1 Parse Request:**

Extract the user's goal from their input:
- Raw text of the request
- Implicit task type
- Mentioned technologies or tools
- Constraints or preferences

**1.2 Identify Task Type:**

Classify the task into primary categories:

```javascript
function detectTaskType(request) {
  const taskPatterns = {
    'development': /build|create|implement|develop|code|API|app|feature/i,
    'content': /transcribe|summarize|process|convert|video|audio|document/i,
    'integration': /connect|integrate|sync|automate|workflow|trigger/i,
    'analysis': /review|analyze|investigate|debug|diagnose|explore/i,
    'documentation': /document|write|generate docs|README|explain/i,
    'planning': /design|architect|plan|strategy|approach/i
  };

  for (const [type, pattern] of Object.entries(taskPatterns)) {
    if (pattern.test(request)) return type;
  }

  return 'general';
}
```

**1.3 Extract Required Capabilities:**

Identify what capabilities are needed:

```javascript
const capabilityMap = {
  'code-generation': /generate|scaffold|create code|boilerplate/i,
  'code-analysis': /analyze|review|understand|explore code/i,
  'web-scraping': /scrape|fetch|extract from web|browser/i,
  'api-calls': /API|REST|endpoint|HTTP|fetch data/i,
  'file-processing': /process file|read|parse|convert/i,
  'external-integration': /Notion|Jira|Confluence|Slack|GitHub/i,
  'data-transformation': /transform|convert|format|restructure/i
};

function extractCapabilities(request) {
  const needed = [];
  for (const [capability, pattern] of Object.entries(capabilityMap)) {
    if (pattern.test(request)) needed.push(capability);
  }
  return needed;
}
```

**1.4 Detect External Integrations:**

Check if task requires external services:

```javascript
const integrationPatterns = {
  'notion': /Notion/i,
  'jira': /Jira|ticket|issue/i,
  'confluence': /Confluence|wiki|documentation/i,
  'github': /GitHub|pull request|PR|repository/i,
  'slack': /Slack|message|channel/i,
  'browser': /web|browser|navigate|screenshot/i
};

function detectIntegrations(request) {
  const integrations = [];
  for (const [service, pattern] of Object.entries(integrationPatterns)) {
    if (pattern.test(request)) integrations.push(service);
  }
  return integrations;
}
```

**1.5 Build Requirements Object:**

```javascript
const requirements = {
  rawText: userRequest,
  taskType: detectTaskType(userRequest),
  neededCapabilities: extractCapabilities(userRequest),
  externalIntegrations: detectIntegrations(userRequest),
  keywords: extractKeywords(userRequest),
  complexity: estimateComplexity(userRequest) // simple|moderate|complex
};
```

### Step 2: Intelligent Matching & Scoring

**Objective:** Score each discovered resource against user requirements.

**Scoring Algorithm:**

```javascript
function scoreResource(resource, requirements) {
  let score = 0;

  // 1. Trigger Phrase Matching (30%)
  if (resource.triggers) {
    const triggerMatch = calculateTriggerMatch(
      resource.triggers,
      requirements.keywords
    );
    score += triggerMatch * 0.30;
  }

  // 2. Semantic Similarity (25%)
  const semanticScore = calculateSemanticSimilarity(
    resource.description,
    requirements.rawText
  );
  score += semanticScore * 0.25;

  // 3. Tool Availability (20%)
  if (resource.tools) {
    const toolMatch = matchTools(
      resource.tools,
      requirements.neededCapabilities
    );
    score += toolMatch * 0.20;
  }

  // 4. Category Relevance (15%)
  if (resource.category) {
    const categoryMatch = (resource.category === requirements.taskType) ? 1.0 : 0.5;
    score += categoryMatch * 0.15;
  }

  // 5. MCP Integration Bonus (10%)
  if (resource.type === 'mcp') {
    const integrationNeeded = requirements.externalIntegrations.length > 0;
    const integrationBonus = integrationNeeded ? 1.0 : 0.5;
    score += integrationBonus * 0.10;
  }

  return Math.round(score * 100); // Convert to 0-100 scale
}
```

**Matching Functions:**

```javascript
// Trigger phrase matching
function calculateTriggerMatch(triggers, keywords) {
  if (!triggers || triggers.length === 0) return 0;

  let matches = 0;
  for (const trigger of triggers) {
    for (const keyword of keywords) {
      if (trigger.toLowerCase().includes(keyword.toLowerCase())) {
        matches++;
      }
    }
  }

  return Math.min(matches / triggers.length, 1.0);
}

// Semantic similarity (simplified)
function calculateSemanticSimilarity(description, request) {
  const descWords = description.toLowerCase().split(/\s+/);
  const reqWords = request.toLowerCase().split(/\s+/);

  const commonWords = descWords.filter(word =>
    reqWords.includes(word) && word.length > 3
  );

  return Math.min(commonWords.length / Math.max(descWords.length, reqWords.length), 1.0);
}

// Tool availability matching
function matchTools(resourceTools, neededCapabilities) {
  const capabilityToolMap = {
    'code-generation': ['Write', 'Edit'],
    'code-analysis': ['Read', 'Grep', 'Glob'],
    'web-scraping': ['browser_navigate', 'browser_click'],
    'api-calls': ['Bash', 'mcp__*'],
    'file-processing': ['Read', 'Write', 'Edit']
  };

  let matches = 0;
  for (const capability of neededCapabilities) {
    const requiredTools = capabilityToolMap[capability] || [];
    for (const tool of requiredTools) {
      if (resourceTools.some(rt => rt.includes(tool.replace('*', '')))) {
        matches++;
      }
    }
  }

  return Math.min(matches / Math.max(neededCapabilities.length, 1), 1.0);
}
```

**Ranking & Filtering:**

```javascript
// Score all resources
const scoredResources = [];

for (const plugin of resources.plugins) {
  for (const agent of plugin.agents) {
    const resource = {
      type: 'agent',
      name: `${plugin.name}:${agent.name}`,
      description: agent.description,
      tools: agent.tools,
      category: 'plugin'
    };
    resource.score = scoreResource(resource, requirements);
    scoredResources.push(resource);
  }
}

for (const skill of resources.skills) {
  const resource = {
    type: 'skill',
    name: skill.name,
    description: skill.description,
    triggers: skill.triggers,
    category: skill.category
  };
  resource.score = scoreResource(resource, requirements);
  scoredResources.push(resource);
}

for (const mcp of resources.mcpServers) {
  for (const tool of mcp.tools) {
    const resource = {
      type: 'mcp',
      name: `${mcp.name}:${tool.name}`,
      description: tool.description,
      category: 'integration'
    };
    resource.score = scoreResource(resource, requirements);
    scoredResources.push(resource);
  }
}

// Sort by score (descending)
scoredResources.sort((a, b) => b.score - a.score);

// Filter low confidence (< 40%)
const candidates = scoredResources.filter(r => r.score >= 40);

// Group by confidence level
const highConfidence = candidates.filter(r => r.score >= 80);
const mediumConfidence = candidates.filter(r => r.score >= 60 && r.score < 80);
const lowConfidence = candidates.filter(r => r.score >= 40 && r.score < 60);
```

### Step 3: Generate Execution Plan

**Objective:** Create strategic execution plans with alternatives.

**3.1 Build Primary Strategy:**

```javascript
function generatePrimaryStrategy(highConfidence, requirements) {
  const steps = [];

  // Group resources by execution order
  const discoveryResources = highConfidence.filter(r =>
    r.description.includes('explore') || r.description.includes('analyze')
  );

  const implementationResources = highConfidence.filter(r =>
    r.description.includes('create') || r.description.includes('generate')
  );

  const validationResources = highConfidence.filter(r =>
    r.description.includes('review') || r.description.includes('validate')
  );

  // Step 1: Discovery/Analysis (if applicable)
  if (discoveryResources.length > 0) {
    steps.push({
      number: steps.length + 1,
      resource: discoveryResources[0],
      action: inferAction(discoveryResources[0], requirements),
      input: 'User requirements',
      output: 'Analysis results',
      rationale: `${discoveryResources[0].description} (${discoveryResources[0].score}% match)`
    });
  }

  // Step 2: Implementation
  if (implementationResources.length > 0) {
    const prevOutput = steps.length > 0 ? steps[steps.length - 1].output : 'User requirements';
    steps.push({
      number: steps.length + 1,
      resource: implementationResources[0],
      action: inferAction(implementationResources[0], requirements),
      input: prevOutput,
      output: 'Implementation artifacts',
      rationale: `${implementationResources[0].description} (${implementationResources[0].score}% match)`
    });
  }

  // Step 3: Validation (if applicable)
  if (validationResources.length > 0) {
    steps.push({
      number: steps.length + 1,
      resource: validationResources[0],
      action: inferAction(validationResources[0], requirements),
      input: 'Implementation artifacts',
      output: 'Validated results',
      rationale: `${validationResources[0].description} (${validationResources[0].score}% match)`
    });
  }

  return steps;
}

function inferAction(resource, requirements) {
  // Infer specific action based on resource and requirements
  const actionTemplates = {
    'code-explorer': `Analyze existing ${requirements.taskType} patterns`,
    'code-architect': `Design ${requirements.taskType} architecture`,
    'code-reviewer': `Review ${requirements.taskType} for quality`,
    'skill-creator': `Scaffold ${requirements.taskType} structure`
  };

  return actionTemplates[resource.name] || `Execute ${resource.name}`;
}
```

**3.2 Build Alternative Strategy:**

```javascript
function generateAlternativeStrategy(mediumConfidence, requirements) {
  // Use different resource combinations
  const altSteps = [];

  // Pick alternative resources not in primary plan
  const availableResources = mediumConfidence.filter(r =>
    !primaryStrategy.some(step => step.resource.name === r.name)
  );

  // Build simplified alternative
  if (availableResources.length > 0) {
    altSteps.push({
      number: 1,
      resource: availableResources[0],
      action: inferAction(availableResources[0], requirements),
      input: 'User requirements',
      output: 'Results',
      rationale: `Alternative approach using ${availableResources[0].name}`
    });
  }

  return altSteps;
}
```

**3.3 Extract Prerequisites:**

```javascript
function extractPrerequisites(plan, resources) {
  const prerequisites = [];

  // Check for MCP dependencies
  const mcpResources = plan.filter(step => step.resource.type === 'mcp');
  for (const mcpStep of mcpResources) {
    const serverName = mcpStep.resource.name.split(':')[0];
    prerequisites.push({
      type: 'mcp',
      description: `MCP server "${serverName}" must be connected`,
      checkCommand: `Check ~/.claude/.mcp.json for ${serverName}`
    });
  }

  // Check for plugin dependencies
  const pluginResources = plan.filter(step => step.resource.type === 'agent');
  for (const pluginStep of pluginResources) {
    const pluginName = pluginStep.resource.name.split(':')[0];
    prerequisites.push({
      type: 'plugin',
      description: `Plugin "${pluginName}" must be installed`,
      checkCommand: `Check plugins directory for ${pluginName}`
    });
  }

  return prerequisites;
}
```

**3.4 Define Success Criteria:**

```javascript
function defineSuccessCriteria(requirements, plan) {
  const criteria = [];

  // Based on task type
  const taskCriteria = {
    'development': [
      'Code compiles without errors',
      'Tests pass successfully',
      'Code follows project conventions'
    ],
    'content': [
      'Output format matches requirements',
      'Content is accurate and complete',
      'Formatting is consistent'
    ],
    'integration': [
      'External services respond successfully',
      'Data syncs correctly',
      'Authentication works'
    ]
  };

  criteria.push(...(taskCriteria[requirements.taskType] || []));

  // Based on plan steps
  for (const step of plan) {
    if (step.resource.name.includes('review')) {
      criteria.push('No critical issues identified in review');
    }
    if (step.resource.name.includes('test')) {
      criteria.push('All tests pass');
    }
  }

  return criteria;
}
```

### Step 4: Present Plan for Approval

**Objective:** Show comprehensive plan to user in clean markdown format.

**Output Structure:**

```markdown
## 📊 Discovery Analysis

**Platform:** {detected_platform}
**Task Type:** {requirements.taskType}
**Complexity:** {requirements.complexity}
**External Integrations:** {requirements.externalIntegrations.join(', ') || 'None'}

---

## 🔍 Resources Found ({total_count})

### High Confidence (80-100%)
- **{resource_name}** [{score}%] - {description}
  - **Why selected:** {reasoning}

### Medium Confidence (60-79%)
- **{resource_name}** [{score}%] - {description}

---

## ✅ Recommended Execution Plan

### Option 1: Primary Strategy (Recommended)

**Step {n}:** Use **{resource_name}** to {action}
- **Input:** {input_description}
- **Output:** {expected_output}
- **Tool:** {platform_tool_name}
- **Rationale:** {why_this_resource}

*(Repeat for each step)*

**Expected Outcome:** {final_result_description}
**Estimated Time:** {time_estimate}
**Risk Level:** {low|medium|high}

---

### Option 2: Alternative Strategy

**Step {n}:** Use **{alt_resource_name}** to {action}
- **Input:** {input_description}
- **Output:** {expected_output}
- **Rationale:** {why_this_alternative}

*(Simpler or different approach)*

---

## ⚠️ Prerequisites

Before executing this plan, ensure:

- [ ] {prerequisite_1}
- [ ] {prerequisite_2}
- [ ] {prerequisite_3}

---

## 🎯 Success Criteria

This plan will be successful when:

- [ ] {criterion_1}
- [ ] {criterion_2}
- [ ] {criterion_3}

---

## 💡 Notes

- **Parallel Execution:** Steps {x} and {y} can run in parallel
- **Fallback:** If Step {n} fails, try {alternative}
- **Dependencies:** Step {n+1} requires output from Step {n}

---

**⏸️ Awaiting your approval to proceed...**
```

### Step 5: Request Approval

**Objective:** Get explicit user confirmation before execution.

**Use AskUserQuestion:**

```javascript
AskUserQuestion({
  question: "Which execution plan would you like to proceed with?",
  header: "Plan Approval",
  options: [
    {
      label: "Execute Option 1 (Recommended)",
      description: "Primary strategy with highest confidence resources"
    },
    {
      label: "Execute Option 2 (Alternative)",
      description: "Alternative approach with different resource mix"
    },
    {
      label: "Refine plan",
      description: "Modify requirements or resource selection"
    },
    {
      label: "Cancel",
      description: "Do not execute, return to planning"
    }
  ]
});
```

**Handle Response:**

- **Execute Option 1/2:** Proceed with selected plan (Step 6)
- **Refine:** Ask follow-up questions, regenerate plan
- **Cancel:** Exit gracefully, no execution

### Step 6: Execute Plan (Optional)

**Objective:** Execute approved plan step-by-step.

**Execution Strategy:**

```javascript
async function executePlan(approvedPlan) {
  const results = [];

  for (const step of approvedPlan) {
    console.log(`\n🔄 Executing Step ${step.number}...`);
    console.log(`   Resource: ${step.resource.name}`);
    console.log(`   Action: ${step.action}`);

    try {
      // Invoke the resource (agent, skill, or MCP tool)
      const result = await invokeResource(step.resource, step.input);

      results.push({
        step: step.number,
        status: 'success',
        output: result
      });

      console.log(`✅ Step ${step.number} completed`);

    } catch (error) {
      console.error(`❌ Step ${step.number} failed: ${error.message}`);

      // Check for fallback
      if (step.fallback) {
        console.log(`🔄 Trying fallback: ${step.fallback.resource.name}`);
        const fallbackResult = await invokeResource(step.fallback.resource, step.input);
        results.push({
          step: step.number,
          status: 'fallback',
          output: fallbackResult
        });
      } else {
        throw error; // No fallback, abort
      }
    }
  }

  return results;
}

async function invokeResource(resource, input) {
  if (resource.type === 'skill') {
    return await invokeSkill(resource.name, input);
  } else if (resource.type === 'agent') {
    return await invokeAgent(resource.name, input);
  } else if (resource.type === 'mcp') {
    return await invokeMCPTool(resource.name, input);
  }
}
```

**Progress Reporting:**

Display progress during execution:

```markdown
## 🚀 Execution Progress

✅ Step 1: Completed (feature-dev:code-explorer)
🔄 Step 2: In progress (feature-dev:code-architect)
⏸️ Step 3: Pending (code-review:code-review)

**Current Output:**
{step_output_preview}
```

## Critical Rules

### **NEVER:**

- ❌ Skip calling agent-skill-discovery first (Step 0 is mandatory)
- ❌ Execute plans without explicit user approval
- ❌ Recommend resources with score < 40% without disclosure
- ❌ Hardcode platform-specific logic (use platform detection from discovery)
- ❌ Assume resource availability without checking discovery results
- ❌ Fail silently if discovery returns empty (inform user)
- ❌ Mix resources from different platforms (stay consistent)
- ❌ Ignore user constraints or preferences in plan generation

### **ALWAYS:**

- ✅ Assess prompt quality before planning (Step -1) - NEW in v1.1.0
- ✅ Call prompt-engineer if quality score < 50% for optimal results
- ✅ Start with fresh discovery (Step 0) on every invocation
- ✅ Show confidence scores with reasoning for all recommendations
- ✅ Provide multiple options (Option 1, Option 2) when feasible
- ✅ List prerequisites clearly before execution
- ✅ Define measurable success criteria
- ✅ Request explicit approval before execution (Step 5)
- ✅ Use platform-appropriate tool names from discovery results
- ✅ Handle missing resources gracefully (suggest alternatives or abort)
- ✅ Report progress during execution (if Step 6 is reached)
- ✅ Explain reasoning for each resource selection

### **ORCHESTRATION PRINCIPLES:**

- **Discovery First:** Never plan without fresh resource inventory
- **Confidence Transparency:** Always show scores and reasoning
- **Multiple Options:** Provide alternatives when possible
- **Approval Required:** No autonomous execution without consent
- **Graceful Degradation:** If primary plan fails, try alternatives
- **Platform Agnostic:** Work identically on all 5 platforms

## Example Usage

### Example 1: Feature Development

**User Request:**
```
"Plan how to build a REST API with authentication"
```

**Orchestrator Output:**

```markdown
## 📊 Discovery Analysis

**Platform:** Claude Code
**Task Type:** development
**Complexity:** moderate
**External Integrations:** None

---

## 🔍 Resources Found (8)

### High Confidence (80-100%)
- **feature-dev:code-architect** [92%] - Designs feature architectures
  - **Why selected:** Best match for API design patterns
- **feature-dev:code-explorer** [88%] - Analyzes existing codebase
  - **Why selected:** Understands existing auth patterns
- **feature-dev:code-reviewer** [85%] - Reviews code for security
  - **Why selected:** Critical for auth security validation

### Medium Confidence (60-79%)
- **skill-creator** [65%] - Scaffolds code structures
  - Can generate boilerplate auth code

---

## ✅ Recommended Execution Plan

### Option 1: Primary Strategy (Recommended)

**Step 1:** Use **feature-dev:code-explorer** to analyze existing authentication patterns
- **Input:** Codebase context
- **Output:** Analysis of current auth implementation
- **Tool:** Read, Grep, Glob
- **Rationale:** Understand existing patterns before designing (88% match)

**Step 2:** Use **feature-dev:code-architect** to design REST API structure with auth
- **Input:** Analysis results from Step 1
- **Output:** API architecture and auth flow design
- **Tool:** Read, Write, Glob
- **Rationale:** Specialized in API design patterns (92% match)

**Step 3:** Use **skill-creator** to scaffold authentication boilerplate
- **Input:** Architecture design from Step 2
- **Output:** Auth middleware code structure
- **Tool:** Write
- **Rationale:** Generates standard auth patterns (65% match)

**Step 4:** Use **feature-dev:code-reviewer** to validate security
- **Input:** Generated auth code from Step 3
- **Output:** Security audit report
- **Tool:** Read, Grep
- **Rationale:** Critical for auth security review (85% match)

**Expected Outcome:** Secure REST API with JWT authentication, following project conventions
**Estimated Time:** ~45 minutes
**Risk Level:** Low (high confidence resources, well-defined approach)

---

### Option 2: Alternative Strategy

**Step 1:** Use **skill-creator** to scaffold complete API + auth structure
- **Input:** User requirements
- **Output:** Boilerplate API with basic auth
- **Rationale:** Faster but less customized approach

**Step 2:** Use **feature-dev:code-reviewer** to validate implementation
- **Input:** Generated code
- **Output:** Quality and security review
- **Rationale:** Ensure boilerplate meets standards

*(Simpler 2-step approach for rapid prototyping)*

---

## ⚠️ Prerequisites

- [ ] Plugin "feature-dev" must be installed
- [ ] Plugin "code-review" must be installed (for Option 1 Step 4)
- [ ] Skill "skill-creator" must be installed
- [ ] Codebase must be accessible (for pattern analysis)

---

## 🎯 Success Criteria

- [ ] REST API endpoints defined and functional
- [ ] JWT authentication implemented correctly
- [ ] Security review passes with no critical issues
- [ ] Code follows project conventions
- [ ] Tests pass for auth flows

---

## 💡 Notes

- **Parallel Execution:** Steps 3 and 4 can overlap (scaffold while reviewing)
- **Fallback:** If feature-dev:code-architect unavailable, use manual design
- **Dependencies:** Step 2 requires output from Step 1 (pattern analysis)

---

**⏸️ Awaiting your approval to proceed...**
```

### Example 2: Content Processing + Integration

**User Request:**
```
"Analyze this meeting recording and create Jira tickets"
```

**Orchestrator Output:**

```markdown
## 📊 Discovery Analysis

**Platform:** GitHub Copilot CLI
**Task Type:** content + integration
**Complexity:** moderate
**External Integrations:** Jira

---

## 🔍 Resources Found (5)

### High Confidence (80-100%)
- **audio-transcriber** [98%] - Converts audio to markdown
  - **Why selected:** Perfect match for audio processing
- **atlassian:capture-tasks-from-meeting-notes** [95%] - Extracts action items
  - **Why selected:** Specialized in meeting note analysis
- **atlassian:triage-issue** [88%] - Creates Jira tickets
  - **Why selected:** Direct Jira integration

### Medium Confidence (60-79%)
- **mcp__jira__create_issue** [72%] - Direct Jira API access
  - Alternative to atlassian:triage-issue

---

## ✅ Recommended Execution Plan

### Option 1: Primary Strategy (Recommended)

**Step 1:** Use **audio-transcriber** skill to convert audio to text
- **Input:** Meeting audio file
- **Output:** Markdown transcription with summary
- **Tool:** view (Read), edit (Write)
- **Rationale:** Specialized audio processing (98% match)

**Step 2:** Use **atlassian:capture-tasks-from-meeting-notes** to extract action items
- **Input:** Transcription markdown from Step 1
- **Output:** Structured list of tasks with assignees
- **Tool:** view (Read)
- **Rationale:** Designed for meeting note analysis (95% match)

**Step 3:** Use **atlassian:triage-issue** to create Jira tickets
- **Input:** Task list from Step 2
- **Output:** Created Jira issues with links
- **Tool:** Jira API via skill
- **Rationale:** Handles duplicate detection and context (88% match)

**Expected Outcome:** Jira tickets created for all action items, assigned to correct team members
**Estimated Time:** ~15 minutes
**Risk Level:** Low (all high-confidence matches)

---

### Option 2: Alternative Strategy

**Step 1:** Use **audio-transcriber** to transcribe audio
*(Same as Option 1)*

**Step 2:** Use **mcp__jira__create_issue** MCP tool directly
- **Input:** Manual parsing of transcription
- **Output:** Jira issues
- **Rationale:** More direct but requires manual parsing

*(Faster but less intelligent task extraction)*

---

## ⚠️ Prerequisites

- [ ] Skill "audio-transcriber" must be installed
- [ ] Skill "atlassian:capture-tasks-from-meeting-notes" must be installed
- [ ] Skill "atlassian:triage-issue" must be installed (Option 1)
- [ ] MCP server for Jira must be configured (Option 2)
- [ ] Audio file must be accessible
- [ ] Jira credentials configured

---

## 🎯 Success Criteria

- [ ] Audio transcription is accurate and complete
- [ ] All action items extracted from transcription
- [ ] Jira tickets created for each action item
- [ ] Assignees correctly identified and set
- [ ] No duplicate tickets created

---

**⏸️ Awaiting your approval to proceed...**
```

### Example 3: Web Research + Documentation

**User Request:**
```
"Research competitor pricing and create a Notion page"
```

**Orchestrator Output:**

```markdown
## 📊 Discovery Analysis

**Platform:** Gemini CLI
**Task Type:** integration + documentation
**Complexity:** moderate
**External Integrations:** Notion, Web

---

## 🔍 Resources Found (3)

### High Confidence (80-100%)
- **mcp__plugin_playwright__browser_navigate** [95%] - Web navigation
  - **Why selected:** Required for competitor website access
- **mcp__plugin_playwright__browser_snapshot** [92%] - Capture page content
  - **Why selected:** Extracts pricing information
- **mcp__claude_ai_Notion__notion-create-pages** [90%] - Creates Notion pages
  - **Why selected:** Direct Notion integration

### Medium Confidence (60-79%)
- **prompt-engineer** [70%] - Optimizes research queries
  - Can improve search effectiveness

---

## ✅ Recommended Execution Plan

### Option 1: Primary Strategy (Recommended)

**Step 1:** Use **prompt-engineer** to optimize research queries
- **Input:** Competitor list and research goals
- **Output:** Optimized search queries
- **Tool:** read
- **Rationale:** Improves research effectiveness (70% match)

**Step 2:** Use **mcp__plugin_playwright__browser_navigate** to visit competitor sites
- **Input:** Optimized queries from Step 1
- **Output:** Loaded competitor pricing pages
- **Tool:** browser_navigate (MCP)
- **Rationale:** Automated web navigation (95% match)

**Step 3:** Use **mcp__plugin_playwright__browser_snapshot** to extract pricing data
- **Input:** Loaded pages from Step 2
- **Output:** Structured pricing information
- **Tool:** browser_snapshot (MCP)
- **Rationale:** Captures pricing tables/content (92% match)

**Step 4:** Synthesize findings using native AI
- **Input:** Extracted data from Step 3
- **Output:** Comparative pricing analysis
- **Rationale:** Human-like synthesis of research

**Step 5:** Use **mcp__claude_ai_Notion__notion-create-pages** to publish report
- **Input:** Analysis from Step 4
- **Output:** Notion page with pricing comparison
- **Tool:** notion-create-pages (MCP)
- **Rationale:** Direct Notion integration (90% match)

**Expected Outcome:** Comprehensive Notion page with competitor pricing analysis
**Estimated Time:** ~30 minutes
**Risk Level:** Medium (web scraping may fail if sites block automation)

---

## ⚠️ Prerequisites

- [ ] MCP server "plugin_playwright" must be connected
- [ ] MCP server "claude_ai_Notion" must be connected
- [ ] Notion workspace access configured
- [ ] List of competitor URLs ready

---

## 🎯 Success Criteria

- [ ] All competitor pricing data collected
- [ ] Pricing comparison accurate and complete
- [ ] Notion page created successfully
- [ ] Formatting is clean and readable
- [ ] Data is up-to-date

---

## 💡 Notes

- **Parallel Execution:** Can navigate multiple competitor sites simultaneously
- **Fallback:** If browser automation fails, manual research + Notion creation
- **Rate Limiting:** May need delays between site visits to avoid blocking

---

**⏸️ Awaiting your approval to proceed...**
```

### Example 4: Vague Prompt → Optimized Plan (NEW v1.1.0)

**User Request (Vague):**
```
"help me with API stuff"
```

**Step -1: Prompt Quality Check**
```
⚠️ Prompt quality: 25%
Issues detected: too_short, lacks_specifics, unclear_goal
🔄 Invoking prompt-engineer skill for optimization...
```

**Prompt-Engineer Output:**
```yaml
framework: RISEN
refinedPrompt: |
  Design and implement a RESTful API with the following requirements:
  - Authentication using JWT tokens
  - CRUD operations for user management (create, read, update, delete)
  - Error handling and input validation
  - API documentation with Swagger/OpenAPI specification
  - Unit and integration tests
  - Following REST architectural constraints and best practices

improvementScore: 85%
reasoning: "Original prompt lacked specificity. Expanded with common API development requirements based on industry standards."
```

**Step 0: Discovery** *(now using optimized prompt)*
```
✅ Resources discovered: 12
Platform: Claude Code
```

**Step 1: Analyze Request** *(clear requirements)*
```markdown
## 📊 Discovery Analysis

**Platform:** Claude Code
**Task Type:** development
**Needed Capabilities:** code-generation, api-design, authentication, testing, documentation
**Complexity:** moderate
**External Integrations:** None
```

**Step 2: Intelligent Matching** *(improved scores due to clear requirements)*
```markdown
## 🔍 Resources Found (12)

### High Confidence (80-100%)
- **feature-dev:code-architect** [95%] ⬆️ - Designs feature architectures
  - **Why selected:** Specialized in API architecture patterns (was 65% with vague prompt)

- **feature-dev:code-explorer** [92%] ⬆️ - Analyzes existing codebase
  - **Why selected:** Identifies existing auth patterns (was 55% with vague prompt)

- **feature-dev:code-reviewer** [88%] ⬆️ - Reviews code for security
  - **Why selected:** Critical for auth security validation (was 60% with vague prompt)

### Medium Confidence (60-79%)
- **skill-creator** [68%] - Scaffolds code structures
  - Can generate API boilerplate code
```

**Step 3: Generate Plan**
```markdown
## ✅ Recommended Execution Plan

### Option 1: Primary Strategy (Recommended)

**Step 1:** Use **feature-dev:code-explorer** to analyze existing authentication patterns
- **Input:** Codebase context
- **Output:** Analysis of current auth implementation
- **Tool:** Read, Grep, Glob
- **Rationale:** Understand existing patterns before designing (92% match)

**Step 2:** Use **feature-dev:code-architect** to design REST API structure with auth
- **Input:** Analysis results from Step 1
- **Output:** API architecture blueprint and auth flow design
- **Tool:** Read, Write, Glob
- **Rationale:** Specialized in API design patterns (95% match)

**Step 3:** Use **skill-creator** to scaffold authentication boilerplate
- **Input:** Architecture design from Step 2
- **Output:** Auth middleware and API endpoints
- **Tool:** Write
- **Rationale:** Generates standard auth patterns (68% match)

**Step 4:** Use **feature-dev:code-reviewer** to validate security
- **Input:** Generated auth code from Step 3
- **Output:** Security audit report
- **Tool:** Read, Grep
- **Rationale:** Critical for auth security review (88% match)

**Expected Outcome:** Secure REST API with JWT authentication, following project conventions
**Estimated Time:** ~45 minutes
**Risk Level:** Low (high confidence resources, well-defined approach)
```

**Impact Comparison:**

| Metric | With Vague Prompt | With Optimized Prompt | Improvement |
|--------|-------------------|----------------------|-------------|
| Avg Confidence Score | 60% | 88% | +28% ⬆️ |
| High-Confidence Resources | 1 | 3 | +200% ⬆️ |
| Plan Quality | Low | High | +40% ⬆️ |
| Success Probability | ~50% | ~85% | +35% ⬆️ |

**Key Takeaway:** Prompt optimization dramatically improves plan quality and execution success rate.

---

## Technical Implementation Notes

### Dependency Management

```javascript
// Always invoke discovery first
async function orchestrate(userRequest) {
  // Step 0: MANDATORY
  const resources = await invokeSkill('agent-skill-discovery');

  if (!resources || resources.totalCount === 0) {
    return {
      error: 'No resources found. Please install plugins/skills first.',
      suggestion: 'Run: claude-superskills install --all'
    };
  }

  // Continue with analysis and planning...
}
```

### Scoring Transparency

Always show reasoning with scores:

```markdown
- **resource-name** [85%] - Description
  - **Why selected:** Trigger match: 30%, Semantic: 25%, Tools: 15%, Category: 10%, MCP: 5%
```

### Platform Tool Mapping

Use platform-appropriate tool names from discovery:

```javascript
function getPlatformToolName(genericTool, platform) {
  const toolMap = {
    'claude': { read: 'Read', edit: 'Edit', write: 'Write' },
    'copilot': { read: 'view', edit: 'edit', write: 'edit' },
    'gemini': { read: 'read', edit: 'edit', write: 'write' }
  };

  return toolMap[platform][genericTool] || genericTool;
}
```

## Performance Considerations

- **Discovery Overhead:** ~1-3 seconds (acceptable for planning tasks)
- **Scoring Complexity:** O(n * m) where n=resources, m=requirements
- **Plan Generation:** O(n log n) for sorting + filtering
- **Total Time:** ~3-5 seconds for typical planning request

## Error Recovery

- **No Resources Found:** Suggest installing skills/plugins
- **Low Confidence All Around:** Inform user, suggest manual approach
- **Discovery Failure:** Cannot proceed, inform user
- **Execution Failure:** Try fallback strategy, then abort gracefully

## Future Enhancements

- **Learning from History:** Track which plans succeeded/failed
- **Auto-Refinement:** Adjust scores based on past performance
- **Parallel Execution:** Execute independent steps simultaneously
- **Real-Time Monitoring:** Show live execution progress
- **Cost Estimation:** Estimate time/resources for plan execution

## Related Skills

- **agent-skill-discovery** (Critical Dependency) - Discovers available resources, MUST be called first
- **prompt-engineer** (NEW in v1.1.0 - Integrated Dependency) - Optimizes vague prompts before planning, dramatically improves plan quality
- **skill-creator** - Can be recommended in plans for scaffolding tasks

## References

See `references/` directory for:
- `scoring-algorithm.md` - Detailed scoring methodology
- `plan-generation.md` - Advanced planning strategies
- `execution-patterns.md` - Best practices for plan execution
- `examples.md` - More comprehensive use cases
