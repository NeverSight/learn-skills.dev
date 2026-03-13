---
name: explore-api
description: Use when researching an unfamiliar external API before integration to verify feasibility, integration patterns, and limitations
---

# Explore External API

## Mission
Systematically research external APIs to prevent integration bugs and validate assumptions before implementation.

## When to Use
- Integrating with unfamiliar external APIs or SDKs
- Using new features of existing APIs
- Switching between API versions or providers
- Any time API documentation needs verification

## Research Workflow

### Phase 1: Documentation Discovery
1. **Official Documentation**
   - Primary API reference: [URL]
   - SDK documentation: [URL]
   - Authentication guide: [URL]
   - Rate limits and quotas: [URL]

2. **Compatibility Matrix**
   - Supported versions: [list]
   - Language SDK versions: [list]
   - Known limitations: [list]
   - Deprecation notices: [check]

3. **Community Resources**
   - GitHub issues for known bugs
   - Stack Overflow common problems
   - Blog posts with integration examples

### Phase 2: API Capability Verification
1. **Endpoint/Feature Support**
   - Required feature: [name] - Supported? ✓/✗
   - API method: [name] - Available in version X? ✓/✗
   - Event types (for streaming): [list actual types]

2. **Authentication & Configuration**
   - Auth method: [API key, OAuth, JWT, etc.]
   - Required environment variables: [list]
   - Configuration precedence: [env vars > config file > defaults]

3. **Request/Response Formats**
   - Request parameters: [required, optional, defaults]
   - Response structure: [schema or example]
   - Error response format: [structure]
   - Pagination pattern (if applicable): [method]

### Phase 3: Integration Pattern Research
1. **Official SDK Usage**
   - Initialization pattern: [code example]
   - Basic request example: [code]
   - Error handling pattern: [code]
   - Async/streaming pattern: [code if applicable]

2. **Environment Setup**
   - Import order requirements: [if any]
   - Initialization timing: [when to init client]
   - Configuration loading: [before/during/after init]

3. **Existing Examples**
   - Official examples: [URLs]
   - Working code samples: [URLs]
   - Integration tutorials: [URLs]

### Phase 4: Proof of Concept
Create minimal working example to validate understanding:

```python
# Minimal POC to verify API works as expected
# Test: [what this proves]
```

**Expected Outcome:** [describe success criteria]
**Fallback Plan:** [alternative if POC fails]

### Phase 5: Risk Assessment
1. **Known Issues**
   - Issue: [description]
     - Impact: [high/medium/low]
     - Mitigation: [approach]

2. **Breaking Changes**
   - Version X → Y changes: [list]
   - Migration required: ✓/✗
   - Backward compatibility: ✓/✗

3. **Rate Limits & Quotas**
   - Requests per minute: [limit]
   - Daily quota: [limit]
   - Retry strategy: [approach]

## Output Format

### API Research Document
Create file: `.agents/research/[api-name]-research.md`

Contents:
- API Overview & Version
- Supported Features Matrix
- Integration Patterns & Code Examples
- Configuration Requirements
- Validation Strategy
- Known Issues & Mitigations
- Reference Links

### Quick Reference for Plan
Generate summary block for embedding in plan-feature.md:

```markdown
## API: [Name] v[Version]

**Documentation:** [Primary URL]
**SDK:** [Library] v[Version] - Compatible: ✓/✗

**Key Findings:**
- Feature [X] supported via [method]
- Event type: [actual name] (not [assumed name])
- Requires: [specific config/setup]
- Limitation: [if any]

**Integration Pattern:**
[Brief code example or reference]

**Validation:**
- [ ] POC tested successfully
- [ ] API key validated
- [ ] Response format verified
```

## Validation Checklist

- [ ] Official documentation reviewed
- [ ] SDK compatibility confirmed
- [ ] Code example tested locally
- [ ] Authentication pattern validated
- [ ] Error handling verified
- [ ] Rate limits documented
- [ ] Known issues identified
- [ ] Fallback plan defined

## Example: LangSmith Integration

**What should have been researched:**

### Documentation URLs
- LangSmith Docs: https://docs.smith.langchain.com/
- Python SDK: https://github.com/langchain-ai/langsmith-sdk
- Tracing Guide: https://docs.smith.langchain.com/tracing
- OpenAI Integration: https://docs.smith.langchain.com/tracing/integrations/openai

### Compatibility Check
- Does wrap_openai() support Responses API? **✗ No** (only Chat Completions)
- Alternative: Manual tracing with Client.create_run() / update_run()

### Critical Findings
- Event type: `response.completed` (not `response.done`)
- Trace completion requires: `end_time` parameter in update_run()
- Import order: Must set env vars before OpenAI client init

### POC Test
```python
from langsmith import Client
client = Client()
run_id = uuid.uuid4()
client.create_run(id=run_id, name="test", run_type="llm", inputs={"test": "data"})
client.update_run(run_id=run_id, outputs={"result": "success"}, end_time=datetime.now())
# Verify in dashboard: trace shows SUCCESS status
```

This research would have prevented:
- Wrong event type assumption
- Using unsupported auto-wrapper
- Missing end_time parameter
- Import order issues
