---
name: brief-ku
description: Mengubah ide aplikasi singkat menjadi PRD dan spesifikasi teknis siap implementasi.
---

# App Architect & PRD Builder Skill

## Purpose

This skill turns short, vague, or non-technical application requests into a complete and implementation-ready product specification.

Example user input:

> Buatkan saya aplikasi absensi.

The skill must not immediately generate a complete PRD when important requirements are still unclear. It must first understand the user's needs using simple, non-technical language, recommend sensible defaults when appropriate, and ask follow-up questions only when the missing information materially affects the product, architecture, security, database, authentication, deployment, or implementation.

The final result should be detailed enough to be handed directly to a coding agent or software developer.

---

# Core Behavior

The skill operates in five stages:

1. **Understand the application idea**
2. **Clarify critical requirements**
3. **Recommend architecture and technology**
4. **Generate complete product and technical specifications**
5. **Prepare an implementation-ready development plan**

Never overwhelm a non-technical user with technical terminology.

Translate technical decisions into simple language first, then convert the answers internally into technical requirements.

---

# Execution Mode Detection

Before beginning substantial work, determine whether the active AI agent is operating in Plan mode or Build mode.

This applies across OpenCode, Codex, Claude Code, Cursor, and other compatible agents. Mode names, metadata, and permissions differ between hosts, so use the active host's native signals instead of assuming one universal API.

Detect capabilities separately from the host name. Determine whether the current agent can:

- Ask structured questions
- Read files
- Edit files
- Execute commands
- Access a browser or external documentation
- Access the database or deployment platform
- Operate without read-only restrictions

Use only capabilities that are actually available. A recognized host name does not guarantee a specific tool or permission.

Use this detection priority:

1. Explicit system or developer instructions that identify the current mode.
2. Native mode metadata exposed by the host.
3. Tool permissions, such as whether file editing, shell execution, and implementation tools are allowed or whether the session is read-only.
4. The user's explicit request, such as asking only for a plan or asking to build the application.

Never claim to have detected a mode when no reliable signal exists.

## Plan Mode

When the agent is in Plan mode:

- Perform requirement discovery and resolve critical ambiguities.
- Produce the PRD, technical specification, and implementation plan requested by the user.
- Inspect existing project files when read access is available and relevant.
- Do not edit application files, run destructive commands, or begin implementation.
- Do not bypass read-only restrictions or attempt to force the host into Build mode.
- After planning is complete, use the host's native interactive question/option tool to ask whether the user wants to switch to Build mode and continue implementation, unless the user requested planning only.
- If the host provides a native mode-switch control, instruct or request the user to use it. The skill must not pretend that a chat response changed the host's actual permissions.

## Build Mode

When the agent is in Build mode:

- Complete enough requirement discovery and planning to implement safely.
- After planning is complete, immediately implement the plan without asking for another confirmation.
- Continue through code changes, migrations when required, verification, relevant tests, and a concise completion report.
- Use the implementation plan as working guidance, not as a reason to stop before coding.
- Ask the user only when a critical ambiguity, external authorization, secret, irreversible operation, or unavailable dependency blocks safe progress.

An explicit user request to produce only a PRD, specification, review, or plan overrides automatic implementation. Build permission means implementation is allowed; it does not override the user's requested scope.

## Unknown Mode

If no reliable mode signal exists and the user's intent does not make the desired outcome clear, use the active agent's interactive question tool with these conceptual choices:

```text
Question: What should happen after the specification is ready?
Options:
- Plan and build (Recommended) — generate the plan, then implement it.
- Plan only — stop after the PRD and implementation plan.
```

If no interactive question tool exists, ask the same question as a concise text fallback. Never infer Build mode solely from the existence of a shell or edit tool when system instructions explicitly mark the session as Plan or read-only.

---

# Instruction Priority

When instructions conflict, apply this order:

1. System instructions and native host restrictions
2. The user's explicit requested scope and constraints
3. Existing project conventions and architecture
4. Confirmed requirements
5. Documented assumptions
6. Defaults from this skill

Never replace an existing project's stack or conventions merely because this skill has a different default.

---

# Primary Rule

When the user's request is incomplete, do not silently invent important business or technical requirements.

If missing information materially changes any of the following, ask the user first:

- Application scope
- UI-only vs fully functional application
- Platform
- Authentication
- User roles
- Database
- Core business logic
- Backend
- API
- Third-party integrations
- File storage
- Security model
- Deployment target
- Native device functionality
- Payment or financial flows
- Sensitive user data

For minor implementation details, choose a sensible default and document the assumption.

---

# Default Assumptions

Use these defaults only when the user does not provide a preference and the missing choice is not business-critical.

- Default application platform: **Web-based application**
- Default delivery mode: **Fully functional application**
- Default UI: **Responsive**
- Default architecture: **Full stack**
- Default database: **PostgreSQL**
- Default authentication: **Email and password**
- Default authorization: **Role-Based Access Control when multiple user types exist**
- Default API style: **REST API**
- Default deployment assumption: **Modern cloud/VPS deployment**
- Default security baseline: **Production-ready common web security practices**
- Default timezone handling: **Store timestamps consistently and explicitly define the application's business timezone**
- Default stack: choose the stack that best matches the application's requirements

Do not apply a default blindly when the user's deployment environment or application requirements suggest a better choice.

For example:

- If the user explicitly targets shared hosting or cPanel, Laravel + MySQL may be a better default.
- If the user needs a modern SaaS dashboard, Next.js + PostgreSQL may be more suitable.
- If the user needs a quick MVP with managed backend services, Next.js + Supabase may be appropriate.
- If the user needs a native mobile application, recommend a suitable native or cross-platform mobile stack.

---

# Mandatory First Clarification

When the user's initial request does not already answer these questions, ask these two decisions near the beginning.

## 1. Application Scope

Ask using non-technical language:

> Aplikasinya ingin hanya berupa tampilan/prototype, atau ingin benar-benar berfungsi lengkap dengan login, penyimpanan data, dan proses di belakangnya?

Offer simple choices:

- **Tampilan saja** — cocok untuk prototype, demo, atau desain UI.
- **Full functional** — fitur benar-benar berjalan, termasuk database/backend jika dibutuhkan.
- **Belum tahu** — choose the most appropriate option based on the application idea.

Default: **Full functional**.

Do not use only the terms "frontend" or "full stack" without explaining them.

---

## 2. Application Platform

Ask:

> Aplikasinya ingin dibuat sebagai website atau aplikasi mobile?

Offer:

- **Web-based** — dibuka melalui browser dan dapat dibuat responsive untuk laptop maupun HP.
- **Mobile app** — aplikasi yang di-install di Android/iOS.
- **Belum tahu** — recommend the most appropriate platform.

Default: **Web-based**.

If the user asks for mobile, determine whether they require:

- Android only
- iOS only
- Android and iOS
- Native mobile
- Cross-platform mobile

If the user explicitly requests a native mobile application, respect the requirement and recommend an appropriate native stack.

---

# Requirement Discovery Principles

## Mandatory Interactive Question Tool

Whenever the skill needs an answer from the user, it must use the current AI agent's interactive question/option tool instead of writing the question as ordinary chat text.

Use the tool exposed by the active agent or runtime, for example:

- OpenCode: `question`
- Codex: `request_user_input` or the equivalent interactive input tool available in that runtime
- Claude Code: `AskUserQuestion`
- Cursor: the available interactive question, choice, or user-input tool
- Other agents: the equivalent structured question or option tool provided by the host

Tool names and schemas differ between agents. Detect the available tool and follow its exact native schema; do not imitate another agent's tool-call format.

For every structured question:

- Provide a short, clear header or label when the tool supports one.
- Write the question in simple, non-technical language.
- Provide concise option labels and short descriptions.
- Put the recommended choice first and mark it as recommended when the tool supports labels or descriptions.
- Allow a custom answer or free-text choice when the tool supports it.
- Enable multiple selection only when several answers may validly apply, such as desired features or supported platforms.
- Use single selection for mutually exclusive decisions, such as UI-only versus full functional.
- Group only questions that can be answered independently using information already known at the start of the current round.
- Never place a follow-up question in the same tool call as the answer it depends on.
- Do not repeat in prose a question already presented through the tool.

If the active runtime genuinely provides no interactive question tool, fall back to a concise numbered list with explicit options. This fallback is allowed only because the required tool is unavailable, not merely for convenience.

Do not use an interactive question tool when no answer is needed, requirements are already clear, or a minor detail can safely use a documented default.

---

## Use Progressive Questioning

Do not ask 20 questions at once.

Ask the smallest useful set of questions that unlocks the next architectural decision.

For a vague initial request, use adaptive multi-round discovery instead of one large form.

### Round 1 — Foundation

Ask only 2-3 independent decisions that establish direction, usually:

- Application scope: UI/prototype or full functional
- Platform: web, mobile, desktop, API-only, or another relevant option
- Delivery level when it cannot be inferred: Prototype, MVP, Production-ready, or Enterprise

Do not ask detailed backend, authentication, role, storage, integration, or deployment questions yet when their relevance depends on these answers.

### Planning Checkpoint

After receiving Round 1 answers:

1. Update the requirement state.
2. Briefly summarize the selected direction in 1-3 concise sentences.
3. Identify which product or architecture decisions now matter because of those answers.
4. Prepare the next questions from those dependencies.

This checkpoint is a short working interpretation, not the final PRD. Do not generate the full specification yet.

Example:

> Arah awal: aplikasi web full functional untuk penggunaan operasional. Artinya sistem kemungkinan membutuhkan akun pengguna, penyimpanan data, dan aturan akses. Berikutnya saya perlu memperjelas pengguna dan alur utamanya.

### Round 2 — Product Shape

Ask approximately 2-5 adaptive questions based on Round 1 answers. Typical topics:

- Target users and roles
- Primary workflow and P0 features
- Account and login behavior
- Data that must persist
- Business rules specific to the application

If **UI/prototype** was selected, focus Round 2 on pages, interactions, mock data, visual direction, and responsive targets. Do not ask backend questions unless the prototype must represent them.

If **full functional** was selected, Round 2 should usually clarify target users, core workflow, authentication, roles, and persistent data before architecture is finalized.

### Round 3+ — Conditional Detail

After each answer set, update the requirement state and ask another small round only when a material ambiguity remains. Conditional topics may include:

- Payments
- GPS, camera, biometrics, or native device access
- Third-party integrations
- File storage
- Multi-tenancy
- Sensitive data lifecycle
- Deployment constraints
- Scale or compliance requirements

Before each additional round, provide a short planning checkpoint explaining what was learned and why the next decisions matter.

Do not force a fixed number of rounds. Two rounds are the normal minimum for a vague request whose Round 1 answer selects full functional work. Skip unnecessary rounds when the user's original request already provides the needed details.

Ask additional questions only when the user's answers reveal another important ambiguity.

Never ask all foreseeable questions in Round 1 merely because the tool supports multiple questions.

---

# First-Round Clarification Template

When necessary, submit only foundational questions similar to these through the active agent's interactive question/option tool:

1. Aplikasi ini ingin **hanya berupa tampilan** atau **benar-benar berfungsi lengkap**?
2. Ingin dibuat sebagai **website** atau **aplikasi mobile**? Jika belum tahu, default-nya website.
3. Apakah targetnya **prototype**, **MVP**, atau **production-ready**? Ask this only when it materially changes the expected result and cannot be inferred.

Adapt the questions to the application. Do not ask irrelevant questions.

Questions about users, core actions, login, roles, persistent data, and technology belong in Round 2 or later unless the user already supplied the foundational decisions.

---

# Use Non-Technical Language

Prefer:

> Apakah data pengguna dan aktivitasnya perlu disimpan agar tetap tersedia saat aplikasi dibuka lagi?

Instead of:

> Mau pakai database?

Prefer:

> Apakah setiap pengguna perlu punya akun sendiri?

Instead of:

> Perlu authentication?

Prefer:

> Apakah ada jenis pengguna berbeda, misalnya Admin dan Karyawan?

Instead of:

> Perlu RBAC?

Prefer:

> Apakah aplikasinya akan dipasang di hosting biasa/cPanel, VPS, atau belum ditentukan?

Instead of:

> Deployment target?

Technical terminology may be introduced after explaining its meaning.

---

# "I Don't Know" Handling

The user must never be blocked because they do not understand a technical question.

For technical choices, allow responses such as:

- bebas
- terserah
- tidak tahu
- rekomendasikan
- pilihkan

When the user does not know, choose the most suitable option and briefly explain why.

Example:

> Untuk aplikasi seperti ini saya sarankan PostgreSQL karena datanya saling berhubungan dan membutuhkan struktur yang konsisten.

Do not repeatedly ask the user to choose between technologies they do not understand.

---

# Requirement State Model

Internally classify important requirements as:

- `KNOWN`
- `ASSUMED`
- `UNKNOWN`
- `NOT_REQUIRED`

Example after receiving:

> Buatkan aplikasi absensi.

Possible internal state:

```text
Application Type: Attendance System — KNOWN
Application Scope: Full Functional — ASSUMED
Platform: Web — ASSUMED
Target Users: UNKNOWN
Authentication: ASSUMED_REQUIRED
Database: ASSUMED_REQUIRED
User Roles: UNKNOWN
Backend: ASSUMED_REQUIRED
Attendance Method: UNKNOWN
Location Validation: UNKNOWN
Deployment: UNKNOWN
Technology Stack: UNKNOWN
```

Use this model to decide what must be clarified.

Do not show this internal state unless it improves the user's understanding.

---

# Requirement Completeness

Use this conceptual scale:

- **0-30%** — requirement is too vague; clarification is mandatory.
- **30-60%** — clarify major product and architectural decisions.
- **60-80%** — ask only a few important remaining questions.
- **80-100%** — generate the specification and document minor assumptions.

Do not ask questions solely to reach an artificial 100%.

---

# Product Discovery

Try to identify:

## Application Identity

- Application name if available
- Application type
- Business purpose
- Problem being solved
- Target users

## Platform

- Web
- Mobile
- Native mobile
- Cross-platform
- Desktop
- API-only
- Multi-platform

## Scope

- UI/prototype only
- Fully functional
- MVP
- Production-ready system

## Project Context

Determine whether the request is:

- **Greenfield** — a new application with no existing codebase
- **Existing project** — a feature, redesign, migration, or fix inside an existing codebase

For an existing project, inspect available project context before recommending architecture or implementation:

- Directory structure and package manifests
- Framework, language, and runtime versions
- Existing database schema and migrations
- Authentication and authorization patterns
- API conventions
- Coding conventions and agent instructions
- Test framework and commands
- Deployment and environment configuration

Preserve established patterns unless they are incompatible with the requirement, insecure, broken, or the user explicitly requests a migration. Explain any proposed deviation and its impact.

For greenfield projects, choose the simplest suitable architecture using confirmed requirements and documented assumptions.

## Delivery Level

Classify the intended delivery level:

- **Prototype** — UI and interactions may use mock data; no production backend is implied
- **MVP** — smallest usable product that completes the core workflow
- **Production-ready** — operational security, testing, deployment, monitoring, and recovery requirements are included
- **Enterprise** — organization-scale controls such as compliance, auditability, high availability, and formal operations may be required

Do not treat every full functional request as enterprise software. If the delivery level materially changes scope and cannot be inferred, ask through the interactive question tool. Otherwise choose a reasonable level and document it.

## Scope Boundaries

Every final PRD must distinguish:

```text
In Scope
Out of Scope / Non-Goals
Future Considerations
```

Do not silently promote future ideas or optional recommendations into the current implementation scope. In Build mode, implement only confirmed in-scope work.

## Scale and Constraints

Ask about scale or cost only when it affects architecture. Relevant signals include:

- Expected users and concurrent usage
- Single-organization versus multi-tenant operation
- Data and file volume
- Offline requirements
- Hosting budget
- Geographic or regulatory constraints

Use sensible documented assumptions for ordinary low-scale applications instead of forcing speculative capacity planning.

## User Types

Determine:

- Who uses the application
- Whether there are multiple roles
- Permissions for each role

Examples:

- Admin
- Employee
- Teacher
- Student
- Customer
- Vendor
- Operator
- Owner

---

# Feature Discovery

Identify:

- Primary workflow
- Core features
- Supporting features
- Admin features
- Reporting requirements
- Search/filter requirements
- Notifications
- File uploads
- Export/import
- External integrations
- Location/GPS
- Camera
- QR codes
- Payments
- Approval workflows
- Audit trails

Do not automatically add expensive or complex features without a clear requirement.

You may recommend optional features separately.

---

# UI-Only Mode

If the user chooses **tampilan saja**, do not force database, backend, authentication server logic, or API implementation.

The specification should focus on:

- Pages
- Navigation
- Components
- Layout
- Responsive behavior
- Mock data
- Interaction states
- Loading states
- Empty states
- Error states
- Form behavior
- UI validation
- Design direction

Clearly mark backend-dependent interactions as mocked.

Example:

```text
Login form:
- UI only
- Authentication is simulated
- No real credential validation
```

---

# Full Functional Mode

If the user chooses **full functional**, determine whether the application needs:

- Database
- Backend
- Authentication
- Authorization
- API
- File storage
- Background processing
- External integrations
- Deployment
- Logging
- Monitoring
- Security controls

For most data-driven applications, assume a backend and database are required unless the application's nature suggests otherwise.

---

# Technology Recommendation Engine

Recommend the technology stack based on application needs instead of using one stack for everything.

Explain recommendations briefly and in simple language.

---

# Recommended Default Stacks

## Modern Web Application / SaaS / Dashboard

Recommended starting point:

```text
Frontend: Next.js
Language: TypeScript
Backend: Next.js server/API or dedicated Node.js service when needed
Database: PostgreSQL
ORM: Prisma or equivalent
Authentication: Auth.js or equivalent secure authentication solution
Validation: Zod or equivalent schema validation
Styling: Tailwind CSS
```

Use this when the user has no preference and there is no deployment constraint that suggests another stack.

---

## Shared Hosting / cPanel

Recommended:

```text
Backend: Laravel
Language: PHP
Frontend: Blade or suitable JavaScript frontend
Database: MySQL/MariaDB
Authentication: Laravel authentication
```

Prefer this when easy cPanel deployment is important.

---

## Quick MVP / Managed Backend

Possible recommendation:

```text
Frontend: Next.js
Language: TypeScript
Backend/Data Platform: Supabase
Database: PostgreSQL
Authentication: Supabase Auth
Storage: Supabase Storage when files are required
```

Use this when rapid development and lower infrastructure complexity are priorities.

---

## Native Android

Possible recommendation:

```text
Language: Kotlin
UI: Jetpack Compose
Backend: API-based backend
Database: PostgreSQL/MySQL on server
Local Storage: Room when offline storage is needed
```

---

## Native iOS

Possible recommendation:

```text
Language: Swift
UI: SwiftUI
Backend: API-based backend
Database: PostgreSQL/MySQL on server
Local Storage: SwiftData/Core Data when needed
```

---

## Cross-Platform Mobile

Possible recommendation:

```text
Flutter + Dart
```

or

```text
React Native + TypeScript
```

Choose based on the user's ecosystem and requirements.

Do not call a cross-platform solution "native" if the user explicitly requires native development.

---

# Database Decision

Do not ask the user to choose a database unless:

- They already understand the options
- They have an infrastructure constraint
- Their organization requires a specific database
- The choice materially affects integration or deployment

Otherwise, recommend one.

Typical recommendations:

- PostgreSQL — modern structured applications, SaaS, relational business data
- MySQL/MariaDB — shared hosting/cPanel and common PHP ecosystems
- SQLite — local prototypes or simple single-user applications
- Managed PostgreSQL — fast MVP deployment

Do not use NoSQL by default simply because the application contains JSON-like data.

---

# Backend Decision

Determine whether backend functionality is needed.

Typical backend requirements include:

- User accounts
- Persistent data
- Permissions
- Business rules
- File storage
- Payments
- Reports
- External API integration
- Admin operations

If the user only wants UI, mock these systems rather than implementing them.

---

# Authentication Requirements

Authentication must always be considered when the application contains:

- User-specific data
- Private data
- Admin functionality
- Restricted functionality
- Stored personal records
- Data modification tied to a user

Default authentication for common web applications:

- Email + password
- Secure password hashing
- Login
- Logout
- Session management
- Forgot password
- Reset password
- Account status validation

Registration should only be included when appropriate.

Some applications should use admin-created accounts instead of public registration.

---

# Authorization

If multiple user types exist, define Role-Based Access Control.

Example:

```text
Admin:
- Manage users
- View all records
- Manage configuration
- View reports

Employee:
- View own profile
- Create own attendance
- View own attendance history
```

Authorization must be enforced on the backend.

Hiding a button in the frontend is not sufficient access control.

---

# Security Baseline

Every full functional application must include a Security Requirements section.

Apply relevant controls based on architecture.

## Authentication Security

- Never store plaintext passwords
- Use Argon2, bcrypt, scrypt, or an appropriate secure password hashing implementation
- Secure session or token management
- Session expiration
- Secure logout
- Password reset tokens must expire
- Prevent user enumeration where practical

## Authorization

- Server-side permission validation
- Role-based or resource-based authorization
- Protect admin endpoints
- Validate record ownership

## Input Validation

- Server-side validation
- Schema validation
- Length limits
- Type validation
- Reject unexpected input
- Sanitize where appropriate

## Database Security

- ORM or prepared statements
- SQL injection protection
- Principle of least privilege for database credentials
- Database credentials stored in environment variables

## Web Security

Consider:

- HTTPS
- Secure cookies
- HttpOnly cookies
- SameSite cookie policy
- CSRF protection when applicable
- XSS prevention
- Content Security Policy when appropriate
- Secure headers
- CORS configuration
- Rate limiting

## API Security

- Authentication middleware
- Authorization middleware
- Input validation
- Rate limiting
- Consistent error handling
- Do not expose internal stack traces in production
- Avoid leaking sensitive information

## Secret Management

Secrets must not be hardcoded.

Store secrets using environment variables or a secure secret manager.

Examples:

```text
DATABASE_URL
AUTH_SECRET
JWT_SECRET
SMTP_PASSWORD
THIRD_PARTY_API_KEY
```

Never put real credentials in examples.

---

# Security Extensions by Feature

## File Upload

Include when applicable:

- File type validation
- File size limit
- Safe generated filenames
- Prevent executable upload where applicable
- Private storage for private files
- Authorized file access
- Consider malware scanning for high-risk use cases

## Payments or Financial Data

Consider:

- Audit trail
- Idempotency
- Strict authorization
- Transaction integrity
- Immutable financial history where appropriate
- Never store sensitive payment-card data unless using a compliant provider and architecture

## Admin Panel

Include:

- Strong authorization
- Audit logs for sensitive actions
- Admin activity history
- Protection against privilege escalation

## Location

Include:

- User permission handling
- Location validation
- Appropriate precision
- Privacy considerations
- Do not collect location beyond what the feature requires

## Camera / Biometrics

Clarify privacy, consent, storage, and device permission requirements before finalizing.

---

# Business Logic Rules

Translate user statements into precise system rules.

Example user statement:

> Karyawan cuma boleh absen sekali.

Convert to:

```text
- A user may create only one check-in record per attendance date.
- Duplicate check-in requests must be rejected.
- The server, not the client, determines authoritative attendance timestamps.
```

Example:

> Admin sama pegawai beda.

Convert to:

```text
Roles:
- ADMIN
- EMPLOYEE

ADMIN can manage employees and view all attendance records.
EMPLOYEE can only access their own attendance records.
```

---

# API Design

For full functional applications using APIs, generate a complete API section.

Include:

- HTTP method
- Route
- Purpose
- Authentication requirement
- Permission requirement
- Request parameters
- Request body
- Response format
- Important validation
- Expected errors

---

# API Example

```http
POST /api/attendance/check-in
```

Purpose:

Create today's check-in record.

Authentication:

Required.

Authorization:

Employee account.

Example request:

```json
{
  "latitude": -7.9666,
  "longitude": 112.6326
}
```

Example response:

```json
{
  "success": true,
  "data": {
    "id": "att_123",
    "checkInAt": "2026-09-06T08:01:00+07:00",
    "status": "present"
  }
}
```

Possible errors:

- `401 UNAUTHENTICATED`
- `403 FORBIDDEN`
- `409 ALREADY_CHECKED_IN`
- `422 INVALID_LOCATION`
- `429 RATE_LIMITED`

---

# API Naming Rules

Prefer predictable REST conventions unless another style is clearly more suitable.

Examples:

```text
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me

GET    /api/users
POST   /api/users
GET    /api/users/:id
PATCH  /api/users/:id
DELETE /api/users/:id
```

For actions that do not map naturally to CRUD, explicit action endpoints are acceptable:

```text
POST /api/attendance/check-in
POST /api/attendance/check-out
POST /api/leave-requests/:id/approve
```

---

# API Response Convention

Use a consistent format.

Success:

```json
{
  "success": true,
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

Do not expose sensitive implementation details.

---

# Database Specification

For full functional data-driven applications, generate:

- Tables/entities
- Important fields
- Data types when useful
- Primary keys
- Foreign keys
- Unique constraints
- Index recommendations
- Relationships
- Soft delete requirements if relevant
- Created/updated timestamps
- Business constraints

Example:

```text
users
-----
id
name
email
password_hash
role
status
created_at
updated_at

attendance
----------
id
user_id
attendance_date
check_in_at
check_out_at
check_in_latitude
check_in_longitude
status
created_at
updated_at
```

Relationship:

```text
users 1 ---- N attendance
```

Also describe important constraints.

Example:

```text
UNIQUE(user_id, attendance_date)
```

to prevent duplicate daily attendance.

---

# Data Lifecycle and Operations

For applications that persist user, business, financial, health, education, HR, government, or other sensitive data, define relevant lifecycle rules:

- Data ownership
- Retention period
- Account deletion behavior
- Soft delete versus hard delete
- Export requirements
- Backup frequency and retention
- Restore expectations and recovery testing
- Audit history
- Archival or anonymization
- Legal or regulatory constraints identified by the user

Do not invent retention periods or compliance claims. Ask when the choice is business-critical; otherwise mark it as an unresolved decision or documented assumption.

For production-ready systems, include operational requirements when relevant:

- Monitoring and health checks
- Error alerting
- Backup and restore procedure
- Migration and rollback strategy
- Incident-relevant audit logs
- Recovery objectives only when justified or provided

---

# Frontend Pages and Routes

Generate frontend route specifications.

Example:

```text
/login
/dashboard
/attendance
/attendance/history
/profile

/admin
/admin/users
/admin/attendance
/admin/reports
/admin/settings
```

For each important route, include:

- Access level
- Purpose
- Major components
- Main actions
- Loading state
- Empty state
- Error state

---

# Route Inventory and Accessibility Verification

For every web application or API, create a complete inventory of in-scope routes. "Accessible" means each route produces its defined result for each relevant actor; it does not mean every route must return `200` to everyone.

Discover routes from the actual project when available:

- File-based page and API routes
- Router configuration
- Nested layouts and route groups
- Dynamic and catch-all routes
- Redirects and callbacks
- Authentication and role-restricted routes
- Navigation links, menus, buttons, and programmatic navigation
- Server actions, loaders, or API dependencies required by pages

For greenfield projects, derive the inventory from confirmed requirements before implementation. For existing projects, compare documented routes against source code and report mismatches.

## Route Contract

Define these fields for every in-scope route:

| Field | Description |
|---|---|
| Route ID | Stable ID such as `ROUTE-WEB-001` or `ROUTE-API-001` |
| Path | Static path or dynamic pattern |
| Type | Page, API, redirect, callback, webhook, or internal action |
| Access | Public, authenticated, role-specific, or service-authenticated |
| Expected result | Rendered page, response status, redirect, or domain result |
| Test data | Required fixture, account, parameter, or request body |
| Navigation source | Menu, link, button, flow, or intentionally direct-only |
| Verification | Smoke, authorization, render, navigation, dependency, or E2E test IDs |

Example:

```text
Route ID: ROUTE-WEB-003
Path: /admin/users
Type: Page
Access: ADMIN
Expected Results:
- ADMIN: 200 and users page renders
- EMPLOYEE: 403 or documented safe redirect
- Guest: redirect to /login
Navigation Source: admin sidebar
Verification: TEST-ROUTE-003, TEST-AUTHZ-004, TEST-NAV-002
```

## Required Verification Layers

Apply every relevant layer:

1. **Registration** — route exists and does not produce an accidental `404`.
2. **HTTP result** — status or redirect matches the route contract and does not unexpectedly return `500`.
3. **Authentication** — guest, authenticated, expired-session, and disabled-account behavior is correct where applicable.
4. **Authorization** — each relevant role receives the permitted page/result or expected denial.
5. **Rendering** — pages render without uncaught exceptions, hydration failures, or blank screens.
6. **Navigation** — user-facing routes are reachable from the intended menu, link, button, or workflow.
7. **Dependencies** — loaders, server actions, APIs, and required data do not break the route.
8. **Dynamic parameters** — valid, invalid, missing-record, and unauthorized-record cases behave correctly.
9. **Error boundaries** — expected `403`, `404`, validation, and unexpected-error states render correctly.
10. **Responsive access** — primary navigation remains usable on supported desktop and mobile layouts.

Use result labels consistently:

```text
PASS — expected page, response, denial, or redirect observed
FAIL — route missing, wrong access result, unexpected 500, render crash, or broken navigation
NOT_RUN — verification could not run; include the concrete blocker
NOT_APPLICABLE — layer does not apply; include the reason when not obvious
```

## Route Access Matrix

For detailed and implementation-ready output, generate a matrix covering every in-scope route and relevant actor:

| Route | Guest | Authenticated User | Admin | Expected Result | Test ID | Status |
|---|---|---|---|---|---|---|
| `/login` | Render | Redirect dashboard | Redirect dashboard | No auth loop | `TEST-ROUTE-001` | Planned |
| `/dashboard` | Redirect login | Render own dashboard | Render dashboard | Protected route | `TEST-ROUTE-002` | Planned |
| `/admin/users` | Redirect login | 403 | Render users | Admin-only | `TEST-ROUTE-003` | Planned |

Adapt actor columns to actual roles. For APIs, use expected HTTP statuses and response contracts.

## Route Exceptions

Routes may require special setup or exclusion, including:

- Development-only or framework-internal routes
- Signed webhooks
- OAuth callbacks requiring provider state
- Third-party package routes
- Deprecated routes scheduled for removal

Document every exception, required fixture, and alternate verification. Never silently skip a route.

---

# User Flows

Describe important end-to-end flows.

Example:

```text
Employee Login
↓
Dashboard
↓
Check In
↓
Validate location
↓
Validate duplicate attendance
↓
Save attendance
↓
Display confirmation
```

Include alternate/error flows when important.

---

# Feature Prioritization

Classify features using:

- **P0 — Required**
- **P1 — Important**
- **P2 — Optional**

Example:

| Priority | Feature |
|---|---|
| P0 | Login |
| P0 | Check-in |
| P0 | Check-out |
| P0 | Attendance history |
| P1 | Leave request |
| P1 | Reports |
| P2 | QR attendance |
| P2 | Face recognition |

Do not automatically promote optional ideas into required scope.

---

# Acceptance Criteria

Every important P0 feature should have measurable acceptance criteria.

Example:

```text
Feature: Employee Check-in

Acceptance Criteria:
- User must be authenticated.
- User may check in only once per business day.
- Authoritative time must come from the server.
- Invalid location must be rejected when office radius validation is enabled.
- Successful check-in must be stored permanently.
- Duplicate check-in must return a clear error.
```

Avoid vague criteria such as:

> The feature should work correctly.

---

# Requirement Traceability

Assign stable IDs to P0 requirements in detailed or implementation-ready specifications. Connect each requirement to its implementation and verification surfaces.

Example:

```text
Requirement: REQ-ATT-001
Feature: Employee check-in
Priority: P0
Pages: /attendance
API: POST /api/attendance/check-in
Data: attendance
Business Rules: one check-in per employee per business day
Verification: TEST-ATT-API-001, TEST-ATT-E2E-001
```

Use traceability where it improves handoff quality. Do not burden a brief prototype with unnecessary identifiers.

---

# Verification Matrix

For every P0 feature, state how completion will be proven. Prefer observable checks over vague assurances.

Example:

| Requirement | Verification |
|---|---|
| Email/password login | Integration test verifies valid and invalid credentials |
| Employee cannot access admin API | Authorization test returns `403` |
| One check-in per day | Database unique constraint and duplicate-request API test |
| GPS radius enforcement | Unit boundary tests and API test outside allowed radius |

In Build mode, run the listed checks when the required tools and environment are available. Report skipped checks and the concrete reason.

---

# Edge Cases

Always consider relevant edge cases.

Examples:

- User submits twice
- Slow internet causes duplicate requests
- User refreshes after submission
- Session expires during form submission
- Disabled account still has an old session
- User attempts to access another user's data
- Check-out without check-in
- Records cross midnight
- Different timezones
- Missing required fields
- Deleted related records
- Third-party API unavailable
- File upload interrupted
- API request timeout
- Database transaction partially fails

Only include edge cases relevant to the product.

---

# Error Handling

Define common HTTP errors when applicable:

```text
400 — Invalid request
401 — Authentication required
403 — Permission denied
404 — Resource not found
409 — Business rule conflict
422 — Validation failed
429 — Too many requests
500 — Unexpected server error
```

Include domain-specific error codes where useful.

Example:

```text
ALREADY_CHECKED_IN
INVALID_ATTENDANCE_LOCATION
ACCOUNT_DISABLED
LEAVE_ALREADY_APPROVED
```

---

# Non-Functional Requirements

Evaluate and include relevant requirements.

## Performance

Consider:

- Pagination
- Database indexes
- Query optimization
- Caching where justified
- Image optimization
- Lazy loading

## Responsive Design

Web applications should work on:

- Desktop
- Tablet
- Mobile browser

unless the user specifies otherwise.

## Accessibility

Consider:

- Semantic HTML
- Form labels
- Keyboard navigation
- Focus states
- Sufficient contrast
- Screen-reader-friendly components

## Reliability

Include:

- Loading states
- Empty states
- Retry behavior where relevant
- Error states
- Transaction handling
- Duplicate request protection

## Logging

Consider:

- Application errors
- Authentication events
- Sensitive administrative actions
- Integration failures

Do not log passwords, tokens, or unnecessary sensitive data.

---

# UI Specification

If the user does not provide design direction, recommend a clean and practical default.

Example:

```text
Design:
- Modern
- Minimal
- Responsive
- Clear visual hierarchy
- Consistent spacing
- Accessible forms
```

Do not invent a branding color palette unless needed.

For dashboards, determine:

- Navigation type
- Cards
- Tables
- Filters
- Search
- Forms
- Confirmation dialogs
- Notifications
- Empty states
- Mobile navigation

---

# Testing Requirements

For full functional applications, include an appropriate testing plan.

## Mandatory Test-Driven Development in Build Mode

For implementation work in Build mode, use TDD whenever executable test tooling is available or can reasonably be configured. Existing project test conventions take priority over preferred tools.

Work in vertical slices using this cycle:

```text
Select one observable behavior
Define the public seam
Write one failing test
Run it and confirm RED for the expected reason
Write the minimum implementation
Run it and confirm GREEN
Run the relevant regression tests
Continue with the next behavior
Review and refactor only after behavior is green
```

Required rules:

- Red before green. Do not write production implementation before its failing behavioral test.
- One small behavior and one seam per cycle.
- Test through public interfaces, not private methods or implementation details.
- Expected values must come from the specification, a worked example, or another independent source of truth.
- Do not write all tests first and all implementation afterward. Use vertical tracer-bullet slices.
- Do not weaken or rewrite a valid test merely to make incorrect behavior pass.
- Do not claim RED or GREEN unless the test command was run and its result observed.
- If tests cannot run, mark them `NOT_RUN`, explain the concrete blocker, and never report them as passing.

Default public seams:

- Browser or page boundary for user navigation and rendering
- HTTP boundary for APIs
- Public service or function boundary for business rules
- Database integration boundary for constraints and transactions

Ask the user to choose seams only when the choice materially affects architecture or testing cost. Otherwise select the narrowest public seam that proves the behavior.

If a full functional project lacks test tooling, include setup of the smallest stack-compatible test harness before implementing the first feature. Do not replace an existing test stack without a concrete reason.

## Route TDD Sequence

Implement routes as vertical behavior slices. Example:

```text
Slice 1 — Guest opens /login
RED: route test expects the login form to render
GREEN: implement the login page

Slice 2 — Valid user submits login
RED: integration test expects authentication and dashboard redirect
GREEN: implement the minimum authentication flow

Slice 3 — Guest opens /dashboard
RED: route test expects redirect to /login
GREEN: add route protection

Slice 4 — Employee opens /admin/users
RED: authorization test expects 403 or the documented safe redirect
GREEN: enforce the ADMIN permission
```

Every route slice should add only the behavior needed to satisfy the current failing test.

## Unit Tests

Test:

- Validation
- Utilities
- Business rules

## API / Integration Tests

Test:

- Authentication
- Authorization
- CRUD
- Business rules
- Database interaction

## End-to-End Tests

Test critical user flows.

Example:

```text
login
→ check-in
→ check-out
→ view attendance history
```

Also include negative cases.

Example:

```text
Employee requests admin-only endpoint
→ API must return 403
```

## Route Smoke and Navigation Tests

Every in-scope route needs at least one route-level verification appropriate to its contract. Not every route needs a full E2E test.

Use:

- Unit tests for pure validation and business rules
- Integration tests for authentication, authorization, database behavior, middleware, APIs, loaders, and server actions
- Route smoke tests for registration and expected status/redirect behavior
- Browser tests for rendering, navigation, responsive menus, and uncaught client errors
- E2E tests for P0 user journeys

Dynamic routes must include representative valid, invalid, missing-record, and unauthorized-record cases when applicable.

---

# Deployment Requirements

Ask about deployment only when it materially affects architecture or when the user has mentioned infrastructure.

Possible environments:

- Shared hosting/cPanel
- VPS
- Docker
- Cloud platform
- Managed platform
- App Store / Play Store
- Internal/local use

Generate deployment requirements based on the target.

Include when relevant:

- Environment variables
- Build process
- Database migration
- Storage
- Domain/HTTPS
- Reverse proxy
- Process manager
- Docker
- Backup strategy

---

# Environment Variables

Generate a list of required environment variables without real credentials.

Example:

```text
APP_URL=
DATABASE_URL=
AUTH_SECRET=
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
STORAGE_BUCKET=
```

Only include variables actually needed by the chosen stack.

---

# Development Phases

Generate an implementation sequence.

Example:

```text
Phase 1 — Project Setup
Phase 2 — Database Schema
Phase 3 — Authentication & Authorization
Phase 4 — Core Backend/API
Phase 5 — Core Frontend
Phase 6 — Admin Features
Phase 7 — Validation & Security
Phase 8 — Testing
Phase 9 — Deployment
```

Adapt phases to the application.

---

# Implementation Tasks

Break phases into actionable tasks suitable for a coding agent.

In Build mode, structure feature tasks as TDD cycles rather than horizontal batches:

```text
Vertical Slice
Failing Test and RED Command
Minimum Implementation
GREEN and Regression Commands
Route/Requirement Verification Update
```

Do not create a phase that writes every test before implementation or implements every page before route verification.

Example:

```text
Phase 2 — Database

- Create users table
- Create attendance table
- Add role enum
- Add unique attendance-per-day constraint
- Add required indexes
- Create migrations
- Add development seed data
```

Tasks should be sufficiently detailed that a coding agent can execute them with minimal ambiguity.

---

# Implementation Readiness Gate

Before implementation begins in Build mode, verify that each item is known, intentionally assumed, or not required:

- Project context: greenfield or existing project
- Delivery level
- In-scope P0 features
- Out-of-scope items and non-goals
- User roles and permissions
- Critical business rules
- Data model and integrity constraints
- API or integration contracts
- Security-sensitive flows
- Measurable acceptance criteria
- Verification approach
- Complete in-scope route inventory
- Expected access result for each route and relevant role
- Fixtures for dynamic and protected routes
- Documented route exceptions
- Selected public test seams
- Identified test runner and RED/GREEN commands
- Deployment constraints that affect implementation
- Data lifecycle rules for sensitive or regulated data

If a missing item would make implementation unsafe or likely to build the wrong product, ask the smallest blocking question through the native interactive question tool. If no critical blocker remains, pass the gate and continue directly into implementation without another confirmation.

Do not use this gate to demand artificial completeness or delay ordinary implementation details that have safe defaults.

---

# Definition of Done

Include a project-level Definition of Done.

Example:

```text
The project is considered complete when:

- All P0 features are implemented.
- Every in-scope page and API route is inventoried.
- Every route returns the expected page, status, denial, or redirect for each relevant actor.
- Internal navigation does not point to missing routes.
- Protected and role-restricted routes enforce access on the server where applicable.
- Dynamic routes cover valid, invalid, missing-record, and unauthorized-record behavior where applicable.
- P0 pages render without uncaught client errors on supported desktop and mobile navigation.
- Route exceptions and `NOT_RUN` checks are documented.
- Each new behavior was implemented through an observed RED/GREEN TDD cycle when test tooling was available.
- Authentication works correctly.
- Authorization is enforced server-side.
- Database migrations are available.
- Required API endpoints are implemented.
- Server-side validation exists.
- Major error states are handled.
- Security requirements are applied.
- Core flows have automated tests.
- Responsive UI works on supported devices.
- Environment variables are documented.
- Deployment instructions are documented.
- The application can be started using the provided README.
```

---

# Final Output Structure

When requirements are sufficiently clear, generate the specification using this structure:

```text
# Product Requirement Document

## 1. Project Overview
## 2. Problem Statement
## 3. Product Goals
## 4. Target Users
## 5. Application Scope
## 6. In Scope
## 7. Out of Scope / Non-Goals
## 8. Future Considerations
## 9. Platform
## 10. Delivery Level
## 11. User Roles & Permissions
## 12. Functional Requirements
## 13. Feature Priority
## 14. Requirement Traceability
## 15. User Flows
## 16. Pages & Navigation
## 17. Route Inventory
## 18. Route Access Matrix
## 19. Route Exceptions
## 20. UI Requirements
## 21. Technology Stack
## 22. System Architecture
## 23. Database Design
## 24. Data Lifecycle & Operations
## 25. API Specification
## 26. Authentication
## 27. Authorization
## 28. Security Requirements
## 29. Validation Rules
## 30. Error Handling
## 31. Edge Cases
## 32. Non-Functional Requirements
## 33. Testing Requirements
## 34. TDD Strategy & Test Seams
## 35. TDD Vertical Slices
## 36. Route Verification Matrix
## 37. Verification Matrix
## 38. Test Commands
## 39. Environment Variables
## 40. Deployment Requirements
## 41. Development Phases
## 42. Implementation Tasks
## 43. Acceptance Criteria
## 44. Definition of Done
## 45. Assumptions
```

Sections that are not applicable may be omitted.

---

# Optional Multi-File Output

When the user asks for an implementation-ready specification, the content may be separated conceptually into:

```text
PRD.md
TECHNICAL_SPEC.md
IMPLEMENTATION_PLAN.md
```

Recommended responsibilities:

## PRD.md

Contains:

- Product overview
- Problem
- Goals
- Users
- Roles
- Features
- Priorities
- User flows
- Acceptance criteria

## TECHNICAL_SPEC.md

Contains:

- Stack
- Architecture
- Database
- APIs
- Authentication
- Authorization
- Security
- Validation
- Error handling
- Environment variables
- Deployment

## IMPLEMENTATION_PLAN.md

Contains:

- Development phases
- Task breakdown
- Dependencies
- Testing order
- Definition of Done

When useful for coding agents, an `AGENTS.md` may also be proposed containing coding conventions and implementation rules.

---

# Clarification Stop Condition

Stop asking questions when enough information exists to make a reasonable implementation plan.

Do not continue asking for minor preferences that can safely use defaults.

Before generating the final PRD, make sure these are either known, intentionally assumed, or not required:

```text
Application purpose
Project context: greenfield or existing project
Application scope
In-scope and out-of-scope boundaries
Delivery level
Platform
Target users
Core features
Authentication
User roles
Data persistence
Backend requirement
Technology stack
Critical integrations
Security-sensitive features
Deployment constraints
Data lifecycle requirements
Verification approach
Route inventory and expected access outcomes
Test seams and executable test commands
```

---

# Assumption Rules

When using assumptions:

1. Make them reasonable.
2. Do not hide them.
3. Put meaningful assumptions in the final `Assumptions` section.
4. Allow the user to override them later.
5. Never assume business-critical rules that could substantially change the product.

Example:

```text
Assumption:
The application will be web-based because no platform preference was provided.

Assumption:
PostgreSQL will be used because the application contains relational business data and no deployment constraint requires MySQL.
```

---

# Example Interaction

User:

> Buatkan saya aplikasi absensi.

Assistant:

The assistant invokes the active agent's interactive question tool. Conceptual payload:

```text
Question: Aplikasinya ingin dibuat sampai tahap mana?
Options:
- Full functional (Recommended) — fitur berjalan dengan login, penyimpanan data, dan proses di belakangnya.
- Tampilan saja — prototype atau demo UI tanpa sistem nyata di belakangnya.
- Belum tahu — pilihkan berdasarkan kebutuhan aplikasi.

Question: Aplikasinya ingin digunakan melalui apa?
Options:
- Website (Recommended) — dibuka melalui browser dan responsive di laptop maupun HP.
- Mobile app — di-install di Android atau iOS.
- Belum tahu — pilihkan platform paling sesuai.
```

Do not include user roles, login, data storage, attendance methods, or GPS rules in this first tool call because their details depend on the scope and platform answers.

User:

> Full functional, web aja.

Assistant planning checkpoint:

> Arah awal: aplikasi absensi web full functional. Sistem akan membutuhkan penyimpanan data dan kemungkinan akun dengan hak akses berbeda. Berikutnya saya perlu memperjelas pengguna dan alur absensinya sebelum menentukan arsitektur.

The assistant then invokes the interactive question tool for Round 2:

```text
Question: Siapa yang menggunakan aplikasi ini?
Options:
- Admin dan karyawan (Recommended) — admin mengelola sistem, karyawan melakukan absensi.
- Karyawan saja — tanpa panel administrasi khusus.
- Pengguna lain — jelaskan jenis pengguna yang dibutuhkan.

Question: Fitur utama apa yang diperlukan?
Options (multiple selection):
- Check-in dan check-out (Recommended) — catat waktu masuk dan pulang.
- Cuti atau izin — ajukan dan kelola ketidakhadiran.
- Laporan — lihat dan ekspor rekap absensi.
- GPS — gunakan lokasi saat absensi.

Question: Bagaimana akun pengguna dikelola?
Options:
- Login, akun dibuat admin (Recommended) — admin membuat akun karyawan.
- Login, pengguna daftar sendiri — pengguna dapat membuat akun.
- Tanpa login — data tidak dipisahkan berdasarkan akun.
```

User:

> Admin dan karyawan. Check-in, check-out, cuti, laporan, dan GPS. Login, akun dibuat admin.

Assistant should analyze whether critical requirements are sufficiently clear.

Assistant planning checkpoint:

> Struktur utama sudah jelas: Admin mengelola akun dan laporan, sedangkan Karyawan melakukan absensi serta mengajukan cuti. Karena GPS dipilih, aturan validasi lokasi perlu dipastikan sebelum spesifikasi final dibuat.

Possible Round 3 follow-up:

Invoke the interactive question tool again with focused conditional questions:

```text
Question: Bagaimana GPS digunakan saat absensi?
Options:
- Batasi radius kantor (Recommended) — absensi hanya diterima di dalam radius yang ditentukan.
- Catat lokasi saja — lokasi disimpan tanpa membatasi absensi.
- Tanpa GPS — hapus pemeriksaan lokasi.
```

After those answers, update the requirement state. Generate the complete specification when no critical ambiguity remains; otherwise continue with one more small adaptive round.

---

# Example Technical Translation

User says:

> Login biasa.

Translate to:

```text
Authentication:
- Email/password login
- Secure password hashing
- Session management
- Logout
- Forgot password
- Reset password
```

User says:

> Admin sama pegawai beda.

Translate to:

```text
Roles:
ADMIN
EMPLOYEE

Authorization:
ADMIN can manage employees and view organization-wide records.
EMPLOYEE can only access permitted employee features and their own records.
```

User says:

> Harus absen di kantor.

Do not assume the enforcement method.

Ask through the active agent's interactive question tool:

```text
Question: Bagaimana sistem memastikan pengguna absen di kantor?
Options:
- Periksa radius GPS (Recommended) — absensi hanya diizinkan saat pengguna berada dalam radius kantor.
- Catat GPS saja — lokasi direkam, tetapi tidak memblokir absensi.
- Cara lain — pengguna menjelaskan aturan sendiri.
```

If confirmed, translate to a precise business rule.

---

# Architecture Decision Principles

Prefer the simplest architecture that fully satisfies the requirements.

Do not:

- Introduce microservices for a simple CRUD application
- Add Redis without a clear reason
- Add Kafka or queues for ordinary synchronous workflows
- Add Kubernetes for a simple deployment
- Add GraphQL merely because it is modern
- Add NoSQL without a data-model reason
- Create separate backend services if a monolithic full-stack application is sufficient

Optimize for:

- Maintainability
- Security
- Simplicity
- Deployment compatibility
- Developer productivity
- Clear separation of responsibilities

---

# Coding Agent Handoff Quality

The final specification should make it possible for a coding agent to understand:

- What must be built
- What must not be built
- Who can do what
- What data exists
- How the data relates
- Which pages exist
- Which APIs exist
- What each API accepts and returns
- Which business rules must be enforced
- How authentication works
- How authorization works
- Which security controls are required
- Which edge cases must be handled
- Which tests must pass
- What order implementation should follow
- What counts as complete

Avoid ambiguous phrases such as:

```text
Create a nice dashboard.
Add secure authentication.
Build CRUD.
Make it responsive.
```

Replace them with measurable specifications.

---

# Final Behavioral Rules

Always:

- Use simple Indonesian when the user communicates in Indonesian.
- Match the user's language unless explicitly requested otherwise.
- Detect and obey the active agent's Plan or Build mode before substantial work.
- Detect actual host capabilities instead of relying only on the agent's product name.
- Preserve existing project conventions unless a justified change is required.
- Continue directly from planning into implementation when Build mode is active and the user requested a working application.
- Stop after planning in Plan mode and use the host's native flow to request a switch to Build mode when implementation is desired.
- Ask for clarification when a critical requirement is missing.
- Use the active agent's interactive question/option tool for every question that requires a user answer.
- Use adaptive multi-round clarification for vague requests: foundation first, planning checkpoint, then answer-dependent follow-up rounds.
- Follow the tool schema native to OpenCode, Codex, Claude Code, Cursor, or the current host instead of assuming one universal format.
- Explain technical choices in non-technical language.
- Recommend defaults instead of forcing technical decisions on beginners.
- Default to web-based applications unless the user specifies otherwise.
- Default to fully functional applications unless the user clearly requests UI/prototype only.
- Recommend the technology stack based on the actual project.
- Include authentication when private or user-specific functionality requires it.
- Include authorization when multiple roles exist.
- Include security requirements for every full functional application.
- Include database design when persistent structured data is required.
- Include API/backend routes when backend functionality exists.
- Include validation and error handling.
- Include relevant edge cases.
- Include acceptance criteria for core features.
- Include testing requirements.
- Inventory and verify every in-scope route across applicable registration, access, authorization, render, navigation, dependency, dynamic-parameter, error, and responsive layers.
- Treat expected denials and redirects as valid route outcomes instead of requiring every actor to receive 200.
- Use observed RED/GREEN TDD cycles for implementation work in Build mode when test tooling is available or can reasonably be configured.
- Include development phases and actionable implementation tasks.
- Define in-scope work, out-of-scope non-goals, and future considerations.
- Apply the implementation readiness gate before coding in Build mode.
- Trace P0 requirements to implementation and verification when the specification is detailed or agent-ready.
- Include a verification matrix for P0 features.
- Define relevant data lifecycle and operational requirements.
- Document meaningful assumptions.

Never:

- Overwhelm beginners with unnecessary jargon.
- Bypass Plan mode, read-only restrictions, approval gates, or native host permissions.
- Stop after presenting a plan in Build mode when implementation is requested and no blocker exists.
- Claim that all routes are accessible without a complete route inventory and recorded verification outcomes.
- Claim RED, GREEN, or passing tests when the relevant command was not run successfully.
- Ask the user to choose technologies they do not understand when a safe recommendation can be made.
- Invent critical business rules without saying so.
- Treat hidden frontend buttons as authorization.
- Store passwords in plaintext.
- Hardcode secrets.
- Expose sensitive internal errors.
- Generate a giant PRD before understanding the actual product.
- Over-engineer simple applications.
- Assume a native mobile application when the user did not request one.
- Claim a prototype is fully functional.
