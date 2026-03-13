---
name: eng-system-architecture
description: This skill should be used when the user asks to "design system architecture", "plan the tech stack", "create database schema", "design API structure", "architect the system", "plan the backend", "design infrastructure", or mentions system architecture, technical architecture, database design, API design, or tech stack selection. Transforms product documentation into comprehensive technical blueprints.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# System Architecture Designer

Generate complete system architecture from product specifications before writing code. Outputs comprehensive technical blueprints covering all architectural decisions.

## Two Modes of Operation

### Mode 1: Tech Stack Already Chosen
User provides tech stack upfront. Focus on architecture, file structure, and implementation details.

### Mode 2: Need Tech Stack Recommendations
User needs help choosing stack. Recommend technologies based on requirements, then provide architecture.

## Core Workflow

### Step 1: Gather Context

Ask these questions if not already provided:

**Product Understanding:**
- What is the product and core value proposition?
- Who are the primary users?
- What are the critical user flows?
- What data needs to be stored?

**Technical Context:**
- Do you already have a tech stack in mind?
- Scale expectations? (users, requests, data volume)
- Specific integrations needed? (Stripe, SendGrid, etc.)
- Performance requirements? (real-time, complex queries)
- Security/compliance needs?

### Step 2: Generate Architecture Document

Create a comprehensive markdown document with these sections:

## Output Sections (Quick Reference)

### 1. SYSTEM OVERVIEW
- High-level architecture pattern (monolith, microservices, serverless)
- How pieces connect (client → API → database → services)
- Key architectural decisions and rationale
- Text-based architecture diagram

### 2. TECH STACK
Complete stack with WHY for each choice. See `references/tech-stack-patterns.md` for common recommendations.

### 3. FILE & FOLDER STRUCTURE
Complete project structure with purpose of each directory. See `references/file-structure-patterns.md` for stack-specific examples.

### 4. DATABASE SCHEMA
Complete schema with relationships, indexes, and key queries. See `references/database-patterns.md`.

### 5. API ARCHITECTURE
All endpoints with purpose, auth, request/response formats. See `references/api-patterns.md`.

### 6. STATE MANAGEMENT & DATA FLOW
Where state lives (server, client, component), data flow diagrams.

### 7. SERVICE CONNECTIONS
How services connect (frontend → API → DB → external services), webhook handling.

### 8. AUTHENTICATION & AUTHORIZATION
Auth flow, implementation patterns, permission model.

### 9. KEY FEATURES IMPLEMENTATION
For each major feature: components, API calls, state, edge cases.

### 10. DEPLOYMENT & INFRASTRUCTURE
Environment variables, deployment steps, CI/CD configuration.

### 11. MONITORING & DEBUGGING
Error tracking, logging strategy, performance monitoring.

### 12. SECURITY CHECKLIST
Input validation, auth, secrets, HTTPS, headers, dependencies.

## Critical Principles

**Be Pragmatic:**
- Start simple, scale when needed
- Choose boring, proven tech
- Optimize for developer velocity first
- Clear upgrade path when you grow

**Be Specific:**
- Exact package names and versions
- Real code examples
- Actual file paths
- Named services (not "some auth provider")

**Be Complete:**
- Every file explained
- Every API endpoint documented
- All states accounted for
- Edge cases identified

**Be Production-Ready:**
- Error handling included
- Monitoring planned
- Security considered
- Deployment automated

## Quick Stack Recommendations

| Use Case | Recommended Stack |
|----------|-------------------|
| MVP/Startup | Next.js + Supabase + Vercel |
| Enterprise SaaS | Next.js + PostgreSQL + Clerk + Stripe |
| Real-time App | Next.js + Supabase Realtime + Redis |
| API-first | Express/Fastify + PostgreSQL + Docker |
| Mobile App | React Native + Supabase + Expo |

## Reference Files

For detailed patterns and examples, consult:

- **`references/tech-stack-patterns.md`** - Tech choice comparisons and recommendations
- **`references/file-structure-patterns.md`** - Directory structures by framework
- **`references/database-patterns.md`** - Common schemas and query patterns
- **`references/api-patterns.md`** - REST best practices and endpoint examples
- **`references/auth-patterns.md`** - Authentication implementations
- **`references/deployment-patterns.md`** - CI/CD and infrastructure patterns
