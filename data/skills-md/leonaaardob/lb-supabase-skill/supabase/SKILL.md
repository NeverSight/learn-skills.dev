---
name: supabase
description: Complete Supabase platform documentation. Use when working with Supabase - covers authentication (email, OAuth, magic links, phone, SSO), database (PostgreSQL, RLS, migrations), storage (file uploads, CDN), edge functions, realtime subscriptions, AI/embeddings, cron jobs, queues, and platform management. Includes framework integrations (Next.js, React, SvelteKit, etc.).
---
## ⚠️ Security Notice

This skill contains Supabase documentation with command examples. Commands are **for reference only** and should NEVER be auto-executed by agents without explicit user approval.

# Supabase Documentation

Complete Supabase platform documentation embedded in markdown. Read from `references/` to answer questions about authentication, database, storage, edge functions, and platform features.

## Documentation Structure

All documentation is in `references/guides/` organized by product:

### Getting Started (`references/guides/getting-started/`)
- Quickstart guides
- Architecture overview
- Framework integrations
- Database fundamentals

### Authentication (`references/guides/auth/`)
Complete auth system documentation:
- Email & password auth
- OAuth providers (Google, GitHub, etc.)
- Magic links
- Phone auth (SMS, WhatsApp)
- SSO & SAML
- Multi-factor authentication (MFA)
- Row Level Security (RLS)
- User management
- Server-side auth
- Redirect URLs
- Session management

### Database (`references/guides/database/`)
PostgreSQL database features:
- Tables and columns
- Relationships and foreign keys
- Functions and triggers
- Extensions
- Full-text search
- Postgres roles
- Replication
- Connection pooling
- Webhooks
- Migrations

### Storage (`references/guides/storage/`)
File storage and CDN:
- Upload files
- Download files
- Delete files
- List files
- Transform images
- CDN and caching
- Access control with RLS
- Resumable uploads

### Edge Functions (`references/guides/functions/`)
Serverless functions:
- Getting started
- Deploy functions
- Environment variables
- Secrets management
- Database access
- Auth integration
- Logging and monitoring
- Cold starts optimization

### Realtime (`references/guides/realtime/`)
Realtime subscriptions:
- Postgres changes (inserts, updates, deletes)
- Broadcast messages
- Presence tracking
- Authorization

### AI & Embeddings (`references/guides/ai/`)
AI and vector features:
- Embeddings and vector search
- pgvector extension
- Similarity search
- RAG patterns
- AI integrations (OpenAI, etc.)

### Platform (`references/guides/platform/`)
Platform management:
- Organizations
- Projects
- Billing
- Logs and monitoring
- Performance tuning
- Backups
- Custom domains
- SSL certificates

### Self-Hosting (`references/guides/self-hosting/`)
Self-hosted Supabase:
- Docker setup
- Configuration
- Monitoring
- Backups and restore

### Cron Jobs (`references/guides/cron/`)
Scheduled tasks with pg_cron

### Queues (`references/guides/queues/`)
Background job queues with pgmq

### Integrations (`references/guides/integrations/`)
Third-party integrations and tools

### Local Development (`references/guides/local-development/`)
- CLI setup
- Local studio
- Database migrations
- Testing
- CI/CD

### Troubleshooting (`references/troubleshooting/`)
Common issues and solutions

### Error Codes (`references/errorCodes/`)
API and database error reference

## Quick Reference

### Common Tasks

| Task | Directory to Check |
|------|-------------------|
| Setup Supabase | `guides/getting-started/` |
| Email auth | `guides/auth/` |
| OAuth providers | `guides/auth/` |
| Database schema | `guides/database/` |
| RLS policies | `guides/auth/` + `guides/database/` |
| File uploads | `guides/storage/` |
| Edge functions | `guides/functions/` |
| Realtime subscriptions | `guides/realtime/` |
| Vector search | `guides/ai/` |
| Migrations | `guides/database/` + `guides/local-development/` |
| Framework integration | `guides/getting-started/` |
| Self-hosting | `guides/self-hosting/` |

### Framework Integrations

Supabase works with:
- Next.js (App Router, Pages Router, Server Components)
- React (Create React App, Vite)
- SvelteKit
- Nuxt
- Vue
- Angular
- Flutter
- React Native
- And more...

### When to Use This Skill

- Setting up Supabase authentication
- Database schema design with PostgreSQL
- Row Level Security (RLS) policies
- File storage and CDN
- Edge functions deployment
- Realtime subscriptions
- Vector search and AI features
- Migration from other platforms
- Self-hosting Supabase
- Performance optimization
- Troubleshooting errors

### How to Navigate

1. **Start with `guides/getting-started/`** for setup
2. **For auth:** Browse `guides/auth/`
3. **For database:** Check `guides/database/`
4. **For storage:** See `guides/storage/`
5. **For functions:** Use `guides/functions/`
6. **For realtime:** Check `guides/realtime/`
7. **For AI:** See `guides/ai/`
8. **For errors:** Check `troubleshooting/` and `errorCodes/`

All files are `.mdx` (Markdown + JSX) but readable as plain markdown.
