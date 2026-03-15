---
name: code-assistant
description: >-
  Orchestrates specialist coding agents (TypeScript, React, frontend, security,
  debugging) to handle coding tasks. Automatically selects the right specialist
  based on the task. Make sure to use this skill whenever the user needs help
  writing, debugging, refactoring, or reviewing code — it coordinates the best
  specialist agent for the job.
---

# Code Assistant

Intelligent orchestrator that analyzes your coding request and automatically selects the most appropriate specialist agent or coordinates multiple agents for complex tasks.

## When to Use

This skill triggers automatically when you need help with:
- Writing new code or features
- Debugging issues or errors
- Refactoring existing code
- Frontend development
- TypeScript-specific work
- React applications
- Tanstack Start applications
- Next.js applications
- Code security reviews
- UI/UX design decisions

## How It Works

### Phase 1: Analysis
Analyzes your request to determine:
- **Language/framework** (TypeScript, React, Next.js, etc.)
- **Task type** (new code, debugging, refactoring, review, design)
- **Complexity** (single agent vs multi-agent coordination)
- **Security sensitivity** (client-side security concerns)
- **Performance concerns** (waterfalls, bundle size, RSC optimization)
- **Code audit requests** (best practices check, review for patterns)

### Phase 2: Agent Selection

Based on analysis, selects the optimal specialist:

| Context | Selected Agent | Why |
|---------|----------------|-----|
| TypeScript code | `typescript-coder` | Type-safe, idiomatic TypeScript |
| React/Vue components | `frontend-developer` | Modern frontend patterns |
| Next.js specific | `nextjs-developer` | App Router, RSC expertise |
| React/Next.js performance | `react-best-practices` skill | Waterfall elimination, bundle optimization |
| React best practices audit | `react-best-practices` skill | Code review against 45 Vercel rules |
| Client-side security | `frontend-security-coder` | XSS prevention, sanitization |
| Debugging issues | `debugger` | Error analysis specialist |
| Code review needed | `code-reviewer` | Quality assurance |
| Refactoring task | `code-refactoring-specialist` | Clean code patterns |
| UI/UX decisions | `ui-ux-designer` | Design systems |
| General implementation | `coder` | Versatile fallback |

### Phase 3: Coordination

For complex requests requiring multiple agents:
1. **Primary agent** handles main task
2. **Secondary agents** handle supporting tasks
3. **Orchestrator** coordinates handoffs

**Example multi-agent workflow:**
```
Request: "Build a secure Next.js form with TypeScript"
     ↓
Orchestrator coordinates:
  1. nextjs-developer → Creates form component structure
  2. typescript-coder → Adds type-safe validation
  3. frontend-security-coder → Implements XSS protection
  4. ui-ux-designer → Reviews accessibility
     ↓
Delivers complete, secure, well-typed component
```

## Agent Profiles

### typescript-coder
**Expertise:** Type-safe TypeScript, "inevitable code" patterns
**Best for:** Complex typing, generics, strict type safety

### frontend-developer
**Expertise:** React 19+, Vue 3, modern web development
**Best for:** Component composition, state management, performance

### nextjs-developer
**Expertise:** Next.js 14+, App Router, Server Components
**Best for:** Full-stack Next.js, SSR, edge functions

### frontend-security-coder
**Expertise:** Client-side security, XSS prevention
**Best for:** User input handling, sanitization, security reviews

### debugger
**Expertise:** Error analysis, test failures, unexpected behavior
**Best for:** Fixing bugs, understanding stack traces

### code-reviewer
**Expertise:** Code quality, best practices, security scanning
**Best for:** PR reviews, quality assurance

### code-refactoring-specialist
**Expertise:** Clean code, reducing complexity, maintainability
**Best for:** Simplifying logic, improving readability

### ui-ux-designer
**Expertise:** Interface design, accessibility, design systems
**Best for:** Component design, user flows, design tokens

### coder
**Expertise:** General implementation from specifications
**Best for:** PRD-based development, general coding tasks

## Selection Algorithm

```
IF request contains ["Next.js", "App Router", "Server Component"]
   → nextjs-developer

ELSE IF request contains ["React" AND ("best practices" OR "audit" OR "optimize" OR "performance")]
   → react-best-practices skill

ELSE IF request contains ["waterfall", "bundle size", "re-render", "RSC optimization"]
   → react-best-practices skill

ELSE IF request contains ["TypeScript" AND (complex types OR generics)]
   → typescript-coder

ELSE IF request contains ["React", "Vue", "frontend", "component"]
   → frontend-developer

ELSE IF request contains ["XSS", "sanitize", "security", "user input"]
   → frontend-security-coder

ELSE IF request contains ["debug", "error", "bug", "failing test"]
   → debugger

ELSE IF request contains ["review", "code quality", "best practices"]
   → code-reviewer

ELSE IF request contains ["refactor", "simplify", "clean up"]
   → code-refactoring-specialist

ELSE IF request contains ["design", "UI", "UX", "interface"]
   → ui-ux-designer

ELSE IF request contains specific implementation requirements
   → coder

ELSE
   → Ask user to clarify or use coder as default
```

## Examples

### Example 1: Automatic Selection
```
User: "I need to debug this React component that's crashing"

Code Assistant analyzes:
  - Task: debugging
  - Framework: React
  - Primary concern: errors

Selects: debugger agent
Announces: "Using debugger to analyze your React component issue"
```

### Example 2: Multi-Agent Coordination
```
User: "Create a user registration form in Next.js with TypeScript validation"

Code Assistant analyzes:
  - Framework: Next.js
  - Language: TypeScript
  - Task: new feature
  - Concerns: validation, security

Coordinates:
  1. nextjs-developer creates form structure
  2. typescript-coder adds type-safe validation
  3. frontend-security-coder reviews input handling

Delivers: Complete, type-safe, secure registration form
```

### Example 3: Ambiguous Request
```
User: "Help me with my code"

Code Assistant:
  "I can help! To select the best specialist, could you tell me more:
   - What language/framework? (React, Next.js, TypeScript, etc.)
   - What do you need? (new feature, debugging, refactoring, review)
   - Any specific concerns? (performance, security, types)"
```

## Override Options

Users can explicitly request specific agents:
- "Use typescript-coder for this"
- "I want the nextjs-developer"
- "Let the debugger handle this"

When explicit request is made, orchestrator defers to user choice.

## Fallback Behavior

If no clear agent match:
1. Ask clarifying questions
2. Use `coder` as versatile default
3. Announce selection rationale

## Performance Notes

- **Analysis overhead:** ~5 seconds for complex requests
- **Single agent:** Same as direct agent invocation
- **Multi-agent:** Sequential execution (no parallelization yet)

## Future Enhancements

- [ ] Parallel multi-agent execution
- [ ] Learning from past selections
- [ ] Context-aware preloading
- [ ] User preference memory

## See Also

- Individual agent documentation in `agents/`
- [Orchestration Patterns](../../../../docs/ORCHESTRATION-PATTERNS.md#skill-based-orchestration)
