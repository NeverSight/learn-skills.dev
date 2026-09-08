---
name: prove-claim
description: Use when asked to prove, disprove, investigate, or find evidence for a claim about people, concepts, ideas, or their relationships. Also use when asked to explore connections, find who influenced what, trace how ideas developed, or answer questions that require reasoning over multiple linked notes.
---

# Prove or Disprove a Claim

You have access to a knowledge graph built from an Obsidian vault. The graph contains **People**, **Concepts**, **Ideas**, and **conversation summaries** connected by wiki links. Your job is to use the graph tools to find evidence that supports or contradicts a claim.

## Available Tools

All tools are prefixed with `kg_` and accessed via MCP:

| Tool | Purpose |
|------|---------|
| `kg_search` | Semantic or full-text search. Start here to find relevant nodes. |
| `kg_node` | Get a node's full content, frontmatter, and connections. |
| `kg_neighbors` | Get connected nodes at N-hop depth. |
| `kg_paths` | Find all connecting paths between two nodes (up to depth 3). |
| `kg_common` | Find shared connections between two nodes. |
| `kg_subgraph` | Extract a local neighborhood as a self-contained graph. |
| `kg_communities` | List detected communities with summaries. |
| `kg_community` | Get a specific community's members and structure. |
| `kg_bridges` | Find connector nodes (high betweenness centrality). |
| `kg_central` | Find important nodes by PageRank. |
| `kg_index` | Re-index the vault (run if data seems stale). |

## The Prove Workflow

### Step 1: Decompose the claim

Break the claim into entities and relationships. Identify what you need to find.

Example claim: *"Alice's research influenced the Widget Theory concept"*
- Entities: Alice, Widget Theory
- Relationship: research influence on the concept

### Step 2: Find the entities

Use `kg_search` to locate relevant nodes. Use `kg_node` to read their content.

- Search semantically first — it finds conceptually related content
- Fall back to `kg_search` with `fulltext: true` for exact terms
- Names are fuzzy-matched: "Alice" will find "Alice Smith"

### Step 3: Find connections

Use `kg_paths` to find connecting paths between entities. Read the edge context along each path — it explains *why* each link exists.

- Paths go through intermediate nodes (people, concepts, conversation summaries)
- Use `kg_common` to quickly find shared connections between two nodes
- Use `kg_neighbors` to explore a node's local neighborhood

### Step 4: Read the evidence

For each path found, use `kg_node` on the intermediate nodes to read the actual content. The prose around each wiki link provides context for why the connection exists.

**Do not stop at "a path exists."** Read the content to verify the connection is semantically relevant to the claim, not just a coincidence of co-occurrence.

### Step 5: Assess and report

Report your findings with:
- **Verdict**: Supported / Contradicted / Insufficient evidence / Partially supported
- **Evidence chains**: The specific paths with quotes from the content
- **Confidence**: How strong is the evidence?
- **Caveats**: What's missing? What assumptions are you making?

## Tips

- **Granola summaries** (conversation notes) are the temporal spine — they record when and how concepts were discussed with whom. They're often the richest evidence.
- **Stub nodes** (links to pages that don't exist) still carry signal — someone thought the connection was worth noting.
- **Communities** group densely-connected nodes. Use `kg_communities` for holistic questions ("what are the major themes?").
- **Bridges** (`kg_bridges`) are the connector nodes between clusters — often the most interesting nodes in the graph.
- Multiple short paths between two nodes are stronger evidence than a single long path.
- Absence of paths is also evidence — if two well-connected nodes have no connection, that's informative.

## Provenance and Attribution

When a question involves **who** originated, created, or owns something, you MUST check attribution before presenting results.

Idea nodes have frontmatter and content that records provenance:
- `Originated by: Alice` / `Originated by: Bob` — in the Status section
- `source:` field in frontmatter — where the idea came from (e.g., `whatsapp/Some Person`)
- `first_mentioned:` — when it first appeared
- Conversation History sections name who proposed what

**Before attributing an idea to someone, read the node content and check:**
1. The "Originated by" line in the Status section
2. The `source` frontmatter field
3. The conversation history for who proposed it

If the question is "my ideas" or "what did person X come up with," **filter by attribution**. An idea that appears in the vault is not necessarily the vault owner's idea — it may have been proposed by a collaborator and recorded here. Getting attribution wrong undermines trust in everything else you report.

When presenting results that involve attribution, explicitly state the provenance: "This was originated by X" or "This came from Y in a conversation on Z date."

## Anti-patterns

- Do NOT claim a connection exists just because two nodes are in the same community.
- Do NOT treat all paths as equal — a path through a relevant Granola summary is stronger than a path through a generic hub node.
- Do NOT skip reading the actual content along a path. The graph structure shows *that* a connection exists; the content shows *what* the connection means.
- Do NOT give up after one search. Try synonyms, aliases, related terms. The vault may use different terminology than the claim.
- Do NOT attribute an idea to someone without checking the provenance fields. An idea recorded in a person's vault may have originated from someone else.
