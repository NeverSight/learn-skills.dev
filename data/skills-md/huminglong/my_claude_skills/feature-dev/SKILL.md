---
name: feature-dev
description: 一个全面、结构化的特性开发工作流程，包含代码库探索、架构设计、质量审查和实现等专门阶段。在构建需要以下条件的新特性时使用：（1）在做出更改之前了解现有代码库，（2）通过系统性的提问澄清模糊的需求，（3）在实现之前设计周到的架构，（4）通过多维度的代码审查确保质量。非常适合涉及多个文件、需要架构决策、包含复杂集成或需求有些不明确的功能特性。
---

# Feature Development Workflow

This skill provides a systematic 7-phase approach to building new features, ensuring better-designed features that integrate seamlessly with existing code.

## Philosophy

Building features requires more than just writing code. You need to:

- **Understand the codebase** before making changes
- **Ask questions** to clarify ambiguous requirements
- **Design thoughtfully** before implementing
- **Review for quality** after building

## The 7-Phase Workflow

### Phase 1: Discovery

**Goal**: Understand what needs to be built

**Actions**:

- Clarify the feature request if unclear
- Ask what problem you're solving
- Identify constraints and requirements
- Summarize understanding and confirm with the user

**When to proceed**: Only after confirming understanding with the user

### Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns

**Actions**:

- Use explore-agent to analyze different aspects in parallel:
  - Find features similar to the requested feature
  - Map the architecture and abstractions for relevant areas
  - Analyze current implementation of related features

- Launch multiple explore-agents concurrently to maximize efficiency

**Expected Output**:

- List of similar features with file references
- Architecture patterns and abstractions used
- Key files to understand with line numbers
- Integration points and dependencies

**Before proceeding**: Read all identified key files to build deep understanding

### Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities

**Actions**:

- Review codebase findings and feature request
- Identify underspecified aspects:
  - Edge cases
  - Error handling
  - Integration points
  - Backward compatibility
  - Performance needs

- Present all questions in an organized list
- **Wait for user answers before proceeding**

**Critical**: This phase ensures nothing is ambiguous before design begins.

### Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches

**Actions**:

- Design 2-3 different approaches:
  - **Minimal changes**: Smallest change, maximum reuse
  - **Clean architecture**: Maintainability, elegant abstractions
  - **Pragmatic balance**: Speed + quality

- Present comparison with trade-offs and recommendation
- Ask which approach the user prefers

**Before proceeding**: Wait for explicit user approval of architecture

### Phase 5: Implementation

**Goal**: Build the feature

**Actions**:

- Read all relevant files identified in previous phases
- Implement following chosen architecture
- Follow codebase conventions strictly
- Write clean, well-documented code
- Track progress with todo_write tool

**Important**: Implementation only starts after user approves architecture

### Phase 6: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, and functionally correct

**Actions**:

- Launch debugger agent to review for bugs and correctness
- Review code for:
  - Simplicity and DRY principles
  - Functional correctness and logic errors
  - Project conventions and patterns

- Present findings and ask user what to do:
  - Fix now
  - Fix later
  - Proceed as-is

- Address issues based on user decision

### Phase 7: Summary

**Goal**: Document what was accomplished

**Actions**:

- Mark all todos complete
- Summarize:
  - What was built
  - Key decisions made
  - Files modified
  - Suggested next steps

## When to Use This Workflow

**Use for:**

- New features that touch multiple files
- Features requiring architectural decisions
- Complex integrations with existing code
- Features where requirements are somewhat unclear

**Don't use for:**

- Single-line bug fixes
- Trivial changes
- Well-defined, simple tasks
- Urgent hotfixes

## Best Practices

1. **Use the full workflow for complex features**: The 7 phases ensure thorough planning
2. **Answer clarifying questions thoughtfully**: Phase 3 prevents future confusion
3. **Choose architecture deliberately**: Phase 4 gives you options for a reason
4. **Don't skip code review**: Phase 6 catches issues before they reach production
5. **Read the suggested files**: Phase 2 identifies key files—read them to understand context

## Specialized Agents Used

This workflow leverages these specialized agents:

- **explore-agent**: For deep codebase analysis and pattern discovery
- **debugger**: For quality review and bug detection
- **plan-agent**: For architecture design and implementation planning

Launch agents in parallel when possible to maximize efficiency.