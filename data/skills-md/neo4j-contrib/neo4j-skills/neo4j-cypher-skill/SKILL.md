---
name: neo4j-cypher-skill
description: Use when upgrading Neo4j 4.x and 5.x Cypher queries to 2025.x/2026.x versions
allowed-tools: WebFetch
---

# Neo4j Cypher skill

This skill uses online guides to upgrade old Neo4j queries to newer versions. It handles all official Cypher queries.

## When to use

Use this skill when:
- a user wants to upgrade a database from version 4.x or 5.x to 2025.x or 2026.x
- a user asks to upgrade Cypher queries to a newer major Neo4j version

## Instructions

1. At the beginning, ALWAYS ask a user what Neo4j version is going to be used after the upgrade. Note, the Neo4j database's version is not upgraded as part of this skill, we just need that information
    a) If the user says that most recent, fetch the version from the [supported version list](https://neo4j.com/developer/kb/neo4j-supported-versions/) along with the most recent driver version
    b) Otherwise, analyze the [supported versions list](https://neo4j.com/developer/kb/neo4j-supported-versions/) and choose the most recent driver version for given Neo4j version

2. Analyze the codebase to see if there are any Neo4j Cypher queries used. If so, include [cypher migration guide](references/cypher-queries.md)

Important: when you plan the upgrade, always include replacement of deprecated functions in the plan