---
name: mcp-tester
description: Test and evaluate MCP server tools in the current session. Use when auditing MCP configurations, validating tool quality, testing MCP servers, generating test cases, checking tool descriptions, or analyzing tool efficiency and redundancy.
---

# MCP Tool Tester

A comprehensive skill for testing and evaluating MCP (Model Context Protocol) server tools available in the current Claude Code session.

## When to Use

Use this skill when:
- Auditing MCP server configurations
- Validating tool quality and descriptions
- Generating test cases for MCP tools
- Checking tool naming conventions and parameter efficiency
- Analyzing tool redundancy across servers
- Evaluating response quality and format efficiency
- Debugging MCP integration issues

## Prerequisites

MCP servers must be configured in your Claude Code settings. If the user asks to test tools that don't exist, guide them to add the MCP server to their configuration.

## Workflow

Execute these phases in order for comprehensive testing:

### Phase 1: Discovery

Identify all MCP tools available in the current session.

**Steps:**
1. List all tools with `mcp__` prefix
2. Group by server (namespace before second `__`)
3. Generate inventory table

**Output Format:**
```markdown
## Tool Inventory

| Server | Tool Name | Required Params | Optional Params | Description Preview |
|--------|-----------|-----------------|-----------------|---------------------|
| context7 | resolve-library-id | libraryName, query | - | Resolves package to Context7 ID... |
| context7 | query-docs | libraryId, query | - | Retrieves documentation... |
```

**Metrics to Report:**
- Total servers: [count]
- Total tools: [count]
- Tools per server breakdown

### Phase 2: Quality Analysis

Evaluate each tool's design quality.

#### Naming Convention Analysis

Check for:
- **Kebab-case consistency**: `get-user` not `getUser` or `get_user`
- **Verb-first naming**: `create-item`, `list-users`, `delete-record`
- **Clarity**: Can purpose be understood from name alone?
- **Namespace collisions**: Similar names across servers

#### Description Quality Scoring

| Score | Criteria |
|-------|----------|
| Excellent | Clear purpose, usage context, examples, input/output expectations |
| Good | Clear purpose, some context, basic expectations |
| Fair | Purpose stated but lacking context or examples |
| Poor | Vague, missing, or misleading description |

Evaluate:
- Does it explain WHAT the tool does?
- Does it explain WHEN to use it?
- Are there example scenarios?
- Are edge cases documented?

#### Parameter Efficiency Analysis

Check:
- **Required vs. optional balance**: Are required params truly necessary?
- **Type specificity**: `enum` vs generic `string` where applicable
- **Default values**: Are sensible defaults provided?
- **Naming clarity**: Can param purpose be understood from name?
- **Token cost**: Estimate description length impact on context

**Token Efficiency Formula:**
```
Efficiency = (Useful information conveyed) / (Token count)
```

Flag tools where description is verbose relative to complexity.

#### Severity Indicators

Use these indicators for findings:

- 🔴 **Critical**: Missing description, unclear purpose, broken schema
- 🟡 **Warning**: Overly verbose description, inefficient parameter schema, unclear naming
- 🔵 **Suggestion**: Minor naming improvements, optional enhancements
- ✅ **Positive**: Well-designed, clear, efficient

**Analysis Output Format:**
```markdown
### Tool: `mcp__server__tool-name`

**Naming**: ✅ Clear verb-first naming
**Description**: 🟡 Warning - Verbose (450 tokens), could be reduced to ~200
**Parameters**: 🔵 Suggestion - Consider enum for `format` param

**Detailed Findings:**
- [Specific observations]

**Recommendations:**
- [Actionable improvements]
```

### Phase 3: Test Design

Generate test cases for each tool using the AAA (Arrange-Act-Assert) pattern.

#### Test Categories

**1. Valid Inputs (Happy Path)**
- Minimal required parameters only
- All parameters with valid values
- Edge of valid ranges (max length strings, boundary numbers)

**2. Invalid Inputs (Error Handling)**
- Missing required parameters
- Wrong parameter types (string where number expected)
- Invalid values (negative IDs, malformed URLs)
- Malformed data structures

**3. Edge Cases**
- Empty strings `""`
- Very long strings (1000+ chars)
- Special characters and unicode
- Null-like concepts (`null`, `undefined`, `None`)
- Boundary values (0, -1, MAX_INT)
- Whitespace only strings

#### Test Case Template

```markdown
### Test: [Tool Name] - [Scenario Name]

**Category**: Valid / Invalid / Edge Case

**Arrange**:
- Context: [What setup is needed]
- Preconditions: [What must be true]

**Act**:
```json
{
  "param1": "value1",
  "param2": "value2"
}
```

**Assert**:
- Expected behavior: [What should happen]
- Expected response format: [Structure]
- Expected error (if invalid): [Error type/message]
```

#### Test Generation Guidelines

For each tool, generate at minimum:
1. 1 happy path test with minimal params
2. 1 happy path test with all params
3. 1 missing required param test
4. 1 wrong type test
5. 1 edge case test (empty/boundary)

### Phase 4: Test Execution

Execute generated tests and capture results.

#### Read-Only Tools
Execute immediately without confirmation:
- Tools that fetch/query data
- Tools that list/search resources
- Tools that analyze/inspect

#### Mutating Tools
**ALWAYS ask for confirmation before testing:**

```markdown
⚠️ **Mutating Tool Detected**

Tool: `mcp__server__create-item`
Operation: Creates new item in external system

**Test Parameters:**
```json
{
  "name": "test-item-12345",
  "type": "test"
}
```

**Potential Effects:**
- Will create a new item in the external system
- May trigger webhooks or notifications
- Item may need manual cleanup

**Proceed with this test?** (yes/no/skip)
```

Mutating operations include:
- `create`, `write`, `post`, `add`, `insert`
- `update`, `edit`, `modify`, `patch`, `put`
- `delete`, `remove`, `destroy`, `clear`
- `send`, `publish`, `trigger`, `execute`

#### Response Capture

For each test, capture:
- Full response content (truncate if > 2000 chars)
- Response time (if perceivable delay)
- Error messages and codes
- Unexpected warnings or notices

### Phase 5: Rating & Feedback

Rate each tool's test results and provide actionable feedback.

#### Rating Criteria

| Rating | Symbol | Criteria |
|--------|--------|----------|
| **Worked** | ✅ | Response matches expected format, no errors, useful output |
| **Partially Worked** | 🟡 | Response returned but incomplete, warnings present, or unexpected format |
| **Failed** | ❌ | Error returned, timeout, or completely wrong behavior |

#### Quality Assessment Dimensions

1. **Response Completeness** (High/Medium/Low)
   - Does it return all expected data?
   - Are there missing fields?

2. **Response Efficiency** (High/Medium/Low)
   - Token usage vs. value provided
   - Unnecessary verbosity in response?

3. **Error Handling** (Clear/Vague/Missing)
   - Are error messages helpful?
   - Do they indicate how to fix the issue?

4. **Format Consistency** (Consistent/Inconsistent)
   - Does response format match description?
   - Is format consistent across calls?

#### Feedback Template

```markdown
## Tool: `mcp__server__tool-name`

### Test Results Summary
| Test | Category | Rating | Notes |
|------|----------|--------|-------|
| Minimal params | Valid | ✅ Worked | Response in 200ms |
| All params | Valid | ✅ Worked | - |
| Missing required | Invalid | 🟡 Partial | Error unclear |
| Wrong type | Invalid | ❌ Failed | No error, silent fail |
| Empty string | Edge | ✅ Worked | Handled gracefully |

### Overall Rating: 🟡 Partially Worked (4/5 tests passed)

### Quality Assessment
- **Completeness**: High - Returns all documented fields
- **Efficiency**: Medium - Response includes redundant metadata
- **Error Handling**: Vague - Errors don't indicate fix
- **Consistency**: Consistent

### Critical Issues
🔴 Silent failure on wrong type - should return validation error

### Improvement Suggestions
1. Add input validation with descriptive error messages
2. Remove redundant `metadata.internal_id` from response (saves ~50 tokens)
3. Consider pagination for list responses
```

### Phase 6: Cross-Tool Analysis

Analyze the tool set as a whole.

#### Redundancy Detection

Look for:
- Tools with overlapping functionality
- Similar operations across different servers
- Duplicate capabilities with different names

**Output Format:**
```markdown
## Redundancy Findings

| Tool A | Tool B | Overlap | Recommendation |
|--------|--------|---------|----------------|
| mcp__a__get-user | mcp__b__fetch-user | 90% same function | Consolidate to single tool |
| mcp__a__list-all | mcp__a__search | Search can replace list | Deprecate list-all |
```

#### Consolidation Opportunities

Identify tools that could be:
- **Merged**: Similar tools into one with mode parameter
- **Batched**: Individual operations into batch operations
- **Simplified**: Complex tools broken into focused ones

#### Missing Capabilities

Note gaps in tool coverage:
- CRUD operations incomplete (has create but no delete)
- Read operations without filtering
- No bulk/batch alternatives to individual operations

#### Efficiency Recommendations

```markdown
## Efficiency Recommendations

### High Impact
1. **Reduce description verbosity** - 3 tools have descriptions >500 tokens
   - Potential savings: ~800 tokens total

### Medium Impact
2. **Add enum constraints** - 5 parameters accept free text but have limited valid values
   - Improves: Validation, documentation, autocomplete

### Low Impact
3. **Standardize naming** - Mix of `get-X` and `fetch-X` patterns
   - Improves: Consistency, discoverability
```

## Output Report Template

Generate this report after completing all phases:

```markdown
# MCP Tool Test Report

**Generated**: [timestamp]
**Session ID**: [if available]

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Servers Tested | [N] |
| Tools Tested | [N] |
| Tests Executed | [N] |
| Pass Rate | [X]% |

### Results Overview
- ✅ **Passed**: [X] tools
- 🟡 **Partial**: [Y] tools
- ❌ **Failed**: [Z] tools

### Key Findings
- 🔴 [N] critical issues requiring immediate attention
- 🟡 [N] warnings to address
- 🔵 [N] suggestions for improvement

---

## Tool Inventory

[Phase 1 output]

---

## Quality Analysis

[Phase 2 output for each tool]

---

## Test Results

[Phase 5 output for each tool]

---

## Cross-Tool Analysis

[Phase 6 output]

---

## Recommendations

### 🔴 Critical (Must Address)
1. [Issue] - [Tool] - [Impact] - [Fix]

### 🟡 Warning (Should Address)
1. [Issue] - [Tool] - [Impact] - [Fix]

### 🔵 Suggestions (Consider)
1. [Improvement] - [Tool] - [Benefit]

---

*Report generated by mcp-tester skill*
```

## Examples

### Example 1: Test All Available Tools

**User**: "Test all my MCP tools"

**Response Flow**:
1. Discover 3 servers with 8 total tools
2. Present inventory table for confirmation
3. Analyze quality (2 warnings, 1 suggestion found)
4. Generate 40 test cases (5 per tool)
5. Identify 2 mutating tools, ask confirmation
6. Execute tests, capture results
7. Rate: 6 passed, 1 partial, 1 failed
8. Analyze cross-tool: 1 redundancy found
9. Generate full report

### Example 2: Test Specific Server

**User**: "Test just the context7 MCP tools"

**Response Flow**:
1. Filter to context7 server (2 tools)
2. Deep analysis of both tools
3. Generate 10 test cases
4. No mutating tools - execute all
5. Generate focused report

### Example 3: Quality Audit Only

**User**: "Audit my MCP tool descriptions without running tests"

**Response Flow**:
1. Discovery phase
2. Full quality analysis
3. Skip test execution
4. Provide quality-focused report with improvement recommendations

### Example 4: Missing MCP Server

**User**: "Test the notion MCP tools"

**Response**:
```markdown
I don't see any Notion MCP tools in the current session.

To add a Notion MCP server:

1. Install the server:
   ```bash
   npm install -g @notionhq/notion-mcp-server
   ```

2. Add to your Claude Code MCP config (`~/.claude/mcp_settings.json`):
   ```json
   {
     "mcpServers": {
       "notion": {
         "command": "notion-mcp-server",
         "env": {
           "NOTION_API_KEY": "your-api-key"
         }
       }
     }
   }
   ```

3. Restart Claude Code to load the new server

Would you like me to help you configure this?
```

## Error Recovery

If a test fails or times out:
1. Log the failure with available details
2. Continue testing remaining tools
3. Include failure in final report
4. Suggest debugging steps for failed tools

## Limitations

- Cannot test MCP tools not configured in current session
- Does not make direct HTTP requests to MCP server URLs
- Cannot test tools requiring interactive authentication mid-flow
- Response time measurements are approximate (based on perceived delay)
