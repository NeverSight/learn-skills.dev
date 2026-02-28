---
name: postmark
description: Use when working with Postmark email platform - routes to specific sub-skills for sending emails, processing inbound email, managing templates, or configuring webhooks.
license: MIT
metadata:
  author: postmark
  version: "1.0.0"
---

# Postmark Skills

Postmark is a transactional email platform built for developers, with 15+ years of deliverability expertise. These skills teach AI agents how to use the Postmark API effectively.

## Sub-Skills

| Feature | Skill | Use When |
|---------|-------|----------|
| **Sending emails** | `postmark-send-email` | Sending transactional or broadcast emails — single, batch, bulk, or with templates |
| **Inbound processing** | `postmark-inbound` | Processing incoming emails via webhooks, building reply-by-email, email-to-ticket, or document extraction |
| **Template management** | `postmark-templates` | Creating, editing, or sending with Postmark's server-side Handlebars templates and layouts |
| **Webhooks** | `postmark-webhooks` | Setting up webhooks for delivery, bounce, open, click, spam complaint, and subscription change events |
| **Best practices** | `postmark-email-best-practices` | Deliverability setup, compliance (CAN-SPAM/GDPR/CASL), email design, list management, testing, and sending reliability |

## Quick Routing

- **"Send an email"** → `postmark-send-email`
- **"Send a batch of emails"** → `postmark-send-email`
- **"Send using a template"** → `postmark-send-email` (template section) or `postmark-templates` (to create/manage templates)
- **"Handle incoming email"** → `postmark-inbound`
- **"Process inbound webhooks"** → `postmark-inbound`
- **"Create an email template"** → `postmark-templates`
- **"Track deliveries/bounces/opens"** → `postmark-webhooks`
- **"Set up bounce handling"** → `postmark-webhooks`
- **"Set up SPF/DKIM/DMARC"** → `postmark-email-best-practices`
- **"Email compliance / GDPR / CAN-SPAM"** → `postmark-email-best-practices`
- **"Domain warm-up"** → `postmark-email-best-practices`
- **"List hygiene / suppression management"** → `postmark-email-best-practices`
- **"Design a transactional email"** → `postmark-email-best-practices`
- **"Test email safely"** → `postmark-email-best-practices`

## Common Setup

### Authentication

Postmark uses two types of API tokens:

| Token | Header | Scope |
|-------|--------|-------|
| **Server Token** | `X-Postmark-Server-Token` | Sending emails, templates, bounces, webhooks, message streams |
| **Account Token** | `X-Postmark-Account-Token` | Managing servers, domains, sender signatures |

Get your Server API Token from [Postmark Servers](https://account.postmarkapp.com/servers).

### SDK Installation

Detect the project language and install the appropriate SDK:

| File | Language | Install Command |
|------|----------|----------------|
| `package.json` | Node.js / TypeScript | `npm install postmark` |
| `requirements.txt` / `pyproject.toml` | Python | `pip install postmarker` |
| `Gemfile` | Ruby | `gem install postmark` |
| `composer.json` | PHP | `composer require wildbit/postmark-php` |
| `*.csproj` / `*.sln` | .NET | `dotnet add package Postmark` |

### Message Streams

Postmark separates email by intent into **Message Streams**:

| Stream | Value | Purpose |
|--------|-------|---------|
| **Transactional** | `outbound` | 1:1 triggered emails (welcome, password reset, receipts) — **default** |
| **Broadcast** | `broadcast` | Marketing, newsletters, announcements |

Never mix transactional and broadcast email in the same stream — it damages deliverability.

## Resources

- [Postmark Developer Docs](https://postmarkapp.com/developer)
- [API Reference](https://postmarkapp.com/developer/api/overview)
- [Postmark API for LLMs](https://postmarkapp.com/llms.txt)
- [Postmark Dashboard](https://account.postmarkapp.com)
