---
name: lightspec-loop
description: Use when systematically implementing LightSpec change proposals through clean, sequential delegation
---

# LightSpec Loop: LightSpec Subagent-Driven Development

Implement LightSpec specs by dispatching fresh subagent per spec, with clean context isolation and sequential execution.

**Core principle:** Fresh subagent per spec + sequential execution + clean context = high quality isolated implementation

## When to Use

```dot
digraph when_to_use {
    "Have LightSpec specs to implement?" [shape=diamond];
    "Specs are independent changes?" [shape=diamond];
    "Want clean context per spec?" [shape=diamond];
    "lightspec-subagent-driven-development" [shape=box];
    "Manual execution or other workflow" [shape=box];

    "Have LightSpec specs to implement?" -> "Specs are independent changes?" [label="yes"];
    "Have LightSpec specs to implement?" -> "Manual execution or other workflow" [label="no"];
    "Specs are independent changes?" -> "Want clean context per spec?" [label="yes"];
    "Specs are independent changes?" -> "Manual execution or other workflow" [label="no - tightly coupled"];
    "Want clean context per spec?" -> "lightspec-subagent-driven-development" [label="yes"];
    "Want clean context per spec?" -> "Manual execution or other workflow" [label="no"];
}
```

**Key characteristics:**
- Sequential execution (one spec at a time)
- Fresh subagent per spec (no context pollution)
- Each subagent starts with `/clear`
- Spec archiving verifies completion

## The Process

```dot
digraph process {
    rankdir=TB;

    "Run 'lightspec view' to discover active specs" [shape=box];
    "Present active specs to user" [shape=box];
    "User confirms implementation order" [shape=box];
    "More specs remain?" [shape=diamond];

    subgraph cluster_per_spec {
        label="Per Spec";
        "Dispatch fresh general-purpose subagent" [shape=box];
        "Subagent executes /clear" [shape=box];
        "Subagent exports context usage" [shape=box];
        "Subagent executes /lightspec:apply [spec-id]" [shape=box];
        "Subagent implements all spec changes using /lightspec:apply [spec-id]" [shape=box];
        "Subagent archives the spec using /lightspec:archive [spec-id]" [shape=box];
        "Verify spec archived successfully" [shape=box];
        "Report status to user" [shape=box];
    }

    "Provide implementation summary to user" [shape=box style=filled fillcolor=lightgreen];

    "Run 'lightspec view' to discover active specs" -> "Present active specs to user";
    "Present active specs to user" -> "User confirms implementation order";
    "User confirms implementation order" -> "More specs remain?";
    "More specs remain?" -> "Dispatch fresh general-purpose subagent" [label="yes"];
    "Dispatch fresh general-purpose subagent" -> "Subagent executes /clear";
    "Subagent executes /clear" -> "Subagent exports context usage";
    "Subagent exports context usage" -> "Subagent executes /lightspec:apply [spec-id]";
    "Subagent executes /lightspec:apply [spec-id]" -> "Subagent implements all spec changes";
    "Subagent implements all spec changes" -> "Subagent archives the spec";
    "Subagent archives the spec" -> "Verify spec archived successfully";
    "Verify spec archived successfully" -> "Report status to user";
    "Report status to user" -> "More specs remain?";
    "More specs remain?" -> "Provide implementation summary to user" [label="no"];
}
```

## Subagent Instructions Template

When launching a subagent, provide it with these exact instructions:

```
You are implementing a specific LightSpec change proposal. Your workflow:

1. FIRST ACTION: Execute `/clear` to ensure clean context
2. THIRD ACTION: Execute `/lightspec:apply [spec-id]` to apply the spec you're implementing
3. Implement all changes described in the spec
4. After successful implementation, archive the spec
5. Report completion and terminate

Spec to implement: [spec-details]
```

## Example Workflow

```
You: I'm using LightSpec Subagent-Driven Development to implement pending specs.

[Run 'lightspec view' and parse active changes]
[Present list to user]

You: Found 3 active specs:
  1. add-base-image-uploads
  2. add-strapi-tag-creation
  3. some-other-feature

User: Implement in this order: add-base-image-uploads, then add-strapi-tag-creation

You: Confirmed. Starting implementation...

=== Spec 1: add-base-image-uploads ===

[Dispatch general-purpose subagent with spec details]
[Subagent executes /clear]
[Subagent exports context usage]
[Subagent executes /lightspec:apply add-base-image-uploads]
[Subagent implements changes]
[Subagent archives spec]
[Verify archiving]

You: ✅ add-base-image-uploads completed and archived

=== Spec 2: add-strapi-tag-creation ===

[Dispatch fresh general-purpose subagent with spec details]
[Subagent executes /clear - completely fresh context]
[Subagent exports context usage]
[Subagent executes /lightspec:apply add-strapi-tag-creation]
[Subagent implements changes]
[Subagent archives spec]
[Verify archiving]

You: ✅ add-strapi-tag-creation completed and archived

=== Summary ===

All requested specs implemented successfully:
  ✅ add-base-image-uploads
  ✅ add-strapi-tag-creation

Remaining: some-other-feature
```

## Advantages

**vs. Manual spec implementation:**
- Each spec gets dedicated, focused attention
- Fresh context per spec (no confusion from previous work)
- Automatic context usage tracking per spec
- Spec archiving confirms completion

**vs. Parallel implementation:**
- No context bleed between specs
- Sequential execution prevents conflicts
- Easier to debug if something goes wrong
- Clear progress tracking

**Quality benefits:**
- `/clear` ensures no mental contamination
- Each subagent starts fresh
- Failed specs don't affect subsequent specs
- Clean audit trail per spec

## Operational Constraints

**NEVER:**
- Read the specs directly yourself - always delegate to subagents
- Implement specs yourself - always delegate to subagents
- Allow context to bleed between spec implementations
- Skip the `/clear` action - it's critical for isolation
- Proceed without verifying spec archiving
- Implement specs in parallel - must be sequential
- Use "superpowers:subagent-driven-development" skill

**ALWAYS:**
- Verify spec exists and is valid before dispatching
- Verify spec is archived after completion
- Report failures and ask user how to proceed
- Maintain clear status display

## Error Handling

**If subagent fails to implement its spec:**
- Report the failure to the user
- Ask whether to: retry with new subagent, skip next spec, or abort
- Document the failure reason

**If spec cannot be applied:**
- Do not proceed to next spec without user confirmation
- Get explicit direction before continuing

## Progress Tracking

Maintain a clear status display showing:
- Total specs to implement
- Current spec being implemented
- Completed specs
- Remaining specs

Update after each spec completion.

## Integration

**Required workflow skills:**
- **lightspec:apply** - Applies the spec to be implemented
- **lightspec:archive** - Archives completed specs

**Related workflows:**
- **superpowers:subagent-driven-development** - Original task-based workflow (NOT for LightSpec specs)

## Termination

Terminate after:
- All specs successfully implemented and archived
- User explicitly requests termination
- Unrecoverable error occurs and user chooses to abort
