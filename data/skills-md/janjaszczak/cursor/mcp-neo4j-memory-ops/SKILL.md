---
name: mcp-neo4j-memory-ops
description: Use Neo4j memory MCP for creating/updating linked memories (entities, relations), de-duplication (DRY), and retrieval queries for project continuity. Use when saving global learnings or querying graph relationships.
compatibility: Requires Neo4j MCP memory server configured; credentials available in MCP config.
allowed-tools: MCP(*)
---

# mcp-neo4j-memory-ops

## When to use (beyond recall)
- User requests “zapisz do pamięci” / “zaktualizuj wspomnienia”.
- Need relationship-aware retrieval: “jak to się łączy z X”, “co już robiliśmy podobnego”.

## Procedure
1. Retrieve candidate existing nodes (fuzzy match).
2. Merge if similar; avoid duplicates.
3. Add explicit relations:
   - PROJECT → DECISION
   - DECISION → CONSTRAINT
   - TOOL → WORKFLOW
4. Store “confidence” and “last_updated”.

## Output
- What nodes/edges changed + short rationale.
