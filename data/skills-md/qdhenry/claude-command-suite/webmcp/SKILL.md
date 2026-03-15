---
name: webmcp
description: Implement WebMCP in web projects — add browser-native structured tools for AI agents using imperative JS or declarative HTML APIs. Full lifecycle from setup through testing and optimization.
---

<essential_principles>

WebMCP is a browser-native standard that exposes structured tools for AI agents on websites. Instead of screen-scraping, agents interact through typed JavaScript APIs and HTML annotations.

**Two APIs:**
- **Imperative API** — `window.navigator.modelContext` — register tools via JavaScript
- **Declarative API** — HTML `toolname`/`tooldescription` attributes on `<form>` elements

**Prerequisites:** Chrome 146.0.7672.0+, `chrome://flags/#enable-webmcp-testing` enabled.

**Core principles that always apply:**

1. **Tools must be atomic and composable** — one function per tool, no overlapping tools with nuanced differences. Combine similar tools into one with input parameters.

2. **Accept raw user input** — tools should accept natural strings (e.g., "11:00") not computed values (e.g., minutes-from-midnight). Minimize cognitive computing for the model.

3. **Validate in code, not schema** — schema constraints are helpful but not guaranteed. Validate within execute functions and return descriptive errors so agents can self-correct.

4. **Update UI before returning** — agents use UI state to verify execution. Ensure execute/submit logic updates visible state before resolving.

5. **Positive, verb-first descriptions** — describe what the tool does and when to use it. Avoid negations. "Creates a calendar event for a specific date" not "Do not use for weather."

</essential_principles>

<intake>
What would you like to do?

1. **Set up WebMCP** in a project (initial integration)
2. **Add a tool** using the imperative JavaScript API
3. **Add a tool** using the declarative HTML form API
4. **Debug** WebMCP tools that aren't working
5. **Audit** existing WebMCP implementation for best practices
6. **Test** WebMCP tools
7. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "integrate", "install", "start" | `workflows/setup-webmcp.md` |
| 2, "imperative", "javascript", "js", "register", "programmatic" | `workflows/add-imperative-tool.md` |
| 3, "declarative", "html", "form", "annotate" | `workflows/add-declarative-tool.md` |
| 4, "debug", "fix", "broken", "not working", "error" | `workflows/debug-webmcp.md` |
| 5, "audit", "review", "check", "best practices" | `workflows/audit-webmcp.md` |
| 6, "test", "verify", "inspect" | `workflows/test-webmcp.md` |
| 7, other | Clarify, then select workflow or references |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>

All in `references/`:

**APIs:** imperative-api.md, declarative-api.md
**Design:** tool-design.md
**Events:** events-and-css.md
**Quality:** testing.md, anti-patterns.md

</reference_index>

<workflows_index>

All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| setup-webmcp.md | Initial WebMCP integration into a project |
| add-imperative-tool.md | Register tools via JavaScript API |
| add-declarative-tool.md | Annotate HTML forms as WebMCP tools |
| debug-webmcp.md | Diagnose and fix WebMCP issues |
| audit-webmcp.md | Review implementation against best practices |
| test-webmcp.md | Test tools with inspector extension and agents |

</workflows_index>

<templates_index>

All in `templates/`:

| Template | Purpose |
|----------|---------|
| imperative-tool.md | Scaffolding for JS-registered tools |
| declarative-form.md | Scaffolding for HTML form-based tools |

</templates_index>

<verification_loop>

After every WebMCP change:

1. Open Chrome DevTools console — check for JS errors
2. Verify `navigator.modelContext` exists (Chrome flag enabled?)
3. Use Model Context Tool Inspector extension to list registered tools
4. Manually execute a tool from the inspector to confirm it works
5. Check that UI updates are visible after tool execution

Report to user:
- "Tools registered: X imperative, Y declarative"
- "Tool [name]: executes successfully / returns error [detail]"
- "UI state: updates correctly after execution / missing update"

</verification_loop>
