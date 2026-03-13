---
name: saas-seeder
description: "Bootstrap a new SaaS from the SaaS Seeder Template: setup database, configure environment, create super admin user, and verify three-tier panel structure. Use when initializing a new multi-tenant SaaS project from this template."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# SaaS Seeder Template Bootstrap

Bootstrap a new multi-tenant SaaS project using the SaaS Seeder Template with proper three-tier panel architecture, Argon2ID authentication, and franchise isolation.

## Security Baseline (Required)

Always load and apply the **Vibe Security Skill** for any seeder work that touches web pages, APIs, authentication, data access, or file handling. Treat its checklist as mandatory.

## Database Standards (Required)

All database schema setup, seeding, and migrations MUST follow **mysql-best-practices** skill patterns including character sets, indexing, foreign keys, and stored procedures.

## Standard Deployment Environments

All SaaS projects deploy across three environments:

| Environment | OS | Database | Web Root |
|---|---|---|---|
| **Development** | Windows 11 (WAMP) | MySQL 8.x | `C:\wamp64\www\{project}\` |
| **Staging** | Ubuntu VPS | MySQL 8.x | `/var/www/html/{project}/` |
| **Production** | Debian VPS | MySQL 8.x | `/var/www/html/{project}/` |

**Cross-platform rules:** Use `utf8mb4_unicode_ci` collation. Match file/directory case exactly (Linux is case-sensitive). Use forward slashes in PHP paths. Production migrations go in `database/migrations-production/` (non-destructive, idempotent).

## When to Use

Use when the user says:

- "Using the seeder-script skill, prepare this repository for [SaaS name]"
- "Bootstrap a new SaaS from this template"
- "Initialize the SaaS Seeder Template"
- "Setup database for new SaaS project"
- "Start a new project from the template"

## Project Preparation Workflow

**BEFORE bootstrapping, developers MUST provide:**

### 1. Requirements & Design Specifications

Place in `docs/project-requirements/`:

```
docs/project-requirements/
├── requirements.md          # Detailed feature requirements
├── business-rules.md         # Business logic and validation rules
├── user-types.md             # User types and their permissions
├── workflows.md              # Key user workflows and processes
└── ui-mockups/               # UI mockups or wireframes (optional)
```

**Use the `project-requirements` skill to create these files with AI assistance.**

### 1.1 Documentation Readiness (Required)

- Confirm end-user manual scope is defined for each core feature
- Plan manual locations in `/manuals/` and a public entry point (e.g., `/public/user-manuals.php`)
- Ensure specs are written in a way that can be translated into manuals and step-by-step guides

### 2. Database Schema Files

Place in `database/schema/`:

```
database/schema/
├── core-schema.sql           # Main database schema
├── seed-data.sql             # Sample/seed data (optional)
└── schema-diagram.png        # Database diagram (optional)
```

**Schema Requirements:**

- All franchise-scoped tables MUST have `franchise_id` column
- Use `utf8mb4_unicode_ci` collation
- Include proper indexes and foreign keys

### AI Agent Preparation Steps

When starting a new project:

1. **Read Project Requirements**
   - Load all files from `docs/project-requirements/`
   - Understand user types, workflows, business rules
   - Identify custom tables needed beyond template defaults

2. **Review Database Schema**
   - Read schema files from `database/schema/`
   - Validate against multi-tenant patterns (franchise_id filtering)
   - Ensure collation is utf8mb4_unicode_ci
   - Check for proper indexes and foreign keys

3. **Update Project Documentation**
   - Replace README.md with project-specific content
   - Update CLAUDE.md with project-specific guidance
   - Remove template docs from docs/ (keep only project-relevant ones)
   - Add project-specific documentation based on requirements
   - Ensure `docs/plans/INDEX.md` exists as the master plan status index and is maintained as plans are created or updated

4. **Customize Template**
   - Update branding (SaaS Seeder → Project Name)
   - Set SESSION_PREFIX to project-specific value
   - Customize user types enum if needed
   - Update environment variable examples
   - Register GIS settings when mapping is required (tile provider keys such as system_settings.osm_api_key)

5. **Validate Completeness**
   - Check all requirements are documented
   - Verify database schema follows multi-tenant patterns
   - Ensure session prefix is customized
   - Confirm user types match requirements

## Critical Architecture Standards

**See `references/architecture.md` for complete details.**

### Three-Tier Panel Structure (CORE Concept)

1. **`/public/` (root)** - Franchise Admin Panel (THE MAIN WORKSPACE)
   - Single franchise management
   - User types: `owner`, `staff`
   - Files: `dashboard.php`, `skeleton.php`

2. **`/public/adminpanel/`** - Super Admin Panel
   - System-wide management
   - Multi-franchise oversight
   - User type: `super_admin`

3. **`/public/memberpanel/`** - End User Portal
   - Self-service for end users
   - User types: `member`, `student`, `customer`, `patient`

**Key Principle:** `/public/` root is NOT a redirect router - it's the franchise admin workspace!

### Session Prefix System

**All session variables use a prefix:**

```php
define('SESSION_PREFIX', 'saas_app_'); // Change per SaaS

// ALWAYS use helpers
setSession('user_id', 123);        // Sets $_SESSION['saas_app_user_id']
$userId = getSession('user_id');   // Gets $_SESSION['saas_app_user_id']
hasSession('user_id');             // Checks if exists
```

**Customize per SaaS:** `school_`, `restaurant_`, `clinic_`, etc.

### Password Hashing

**Uses Argon2ID (NOT bcrypt):**

```
Algorithm: Argon2ID + salt(32 chars) + pepper(64+ chars)
Hash: salt + Argon2ID(HMAC-SHA256(password, pepper) + salt)
```

**CRITICAL:** Use `super-user-dev.php` to create admin users, NOT migration defaults!

## Required Files And Paths

- `docs/seeder-template/migration.sql` - Core auth/RBAC schema
- `docs/seeder-template/fix-collation-and-create-franchises.sql` - Collation fixes + franchises table
- `docs/project-requirements/` - Project requirements (developer provides)
- `database/schema/` - Project database schemas (developer provides)
- `public/super-user-dev.php` - Super admin creator (DEV ONLY)
- `public/dashboard.php` - Franchise admin dashboard
- `public/skeleton.php` - Page template
- `.env` - Environment configuration

## Standard Workflow

**See `references/workflow.md` for complete step-by-step guide.**

### Quick Bootstrap Steps

1. **Environment Setup**
   - Ask for DB credentials, cookie domain, encryption keys
   - Create/update `.env` file

2. **Install Dependencies**

   ```bash
   composer install
   ```

3. **Install PHP Development Tools**

   **See `references/php-tooling.md` for complete setup guide.**

   **Quick install:**

   ```bash
   # Check existing tools
   composer show | grep -E "(phpstan|phpunit|pest|php-cs-fixer)"

   # Install essential tools
   composer require --dev phpstan/phpstan
   composer require --dev friendsofphp/php-cs-fixer
   composer require --dev pestphp/pest --with-all-dependencies
   ```

   **Create configs and add composer scripts (see references/php-tooling.md for details).**

4. **Database Setup**

   ```bash
   .\setup-database.ps1  # Windows PowerShell
   ```

5. **Fix Collations**

   ```bash
   .\fix-database.ps1  # Creates franchises table
   ```

6. **Create Super Admin**
   - Visit `http://localhost:8000/super-user-dev.php`
   - Uses correct Argon2ID hashing

7. **Verify Setup**
   - Login at `http://localhost:8000/sign-in.php`
   - See landing page with navigation buttons

8. **Project Customization**
   - Update SESSION_PREFIX in `src/config/session.php`
   - Customize user types enum
   - Apply project database schema
   - Update branding throughout
   - Create project-specific CLAUDE.md

## Seeding Rules

### User Types & Franchise Requirements

- `super_admin` - Platform operators (franchise_id CAN be NULL)
- `owner` - Franchise owners (franchise_id REQUIRED)
- `staff` - Franchise staff with permissions (franchise_id REQUIRED)
- Custom types - End users (franchise_id REQUIRED)

### Franchise Data

**ALWAYS filter by franchise_id:**

```php
// CORRECT
$stmt = $db->prepare("SELECT * FROM students WHERE franchise_id = ?");
$stmt->execute([getSession('franchise_id')]);

// WRONG - data leakage!
$stmt = $db->prepare("SELECT * FROM students");
```

### Permission Codes

- Uppercase with underscores
- Format: `RESOURCE_ACTION`
- Examples: `INVOICE_CREATE`, `STUDENT_DELETE`, `REPORT_VIEW`

## Troubleshooting

**See `references/troubleshooting.md` for complete guide.**

### Common Issues

**Session Not Persisting**

- HTTPS auto-detection already handled
- Localhost HTTP works without HTTPS requirement

**Password Mismatch**

- Use `super-user-dev.php`, NOT manual password_hash()
- Template uses Argon2ID, not bcrypt

**Collation Errors**

- Run `.\fix-database.ps1`
- Fixes utf8mb4_unicode_ci mismatches

**Missing Franchises Table**

- Run `.\fix-database.ps1`
- Creates tbl_franchises with default data

## Output After Completion

### For New Project from Template

Report to user:

```
✅ [Project Name] Initialized!

Requirements Loaded:
- ✅ Read from docs/project-requirements/
- ✅ Database schema reviewed from database/schema/
- ✅ User types customized: [list custom types]
- ✅ Session prefix set to: [prefix]_

Database Setup:
- ✅ Core schema applied
- ✅ Seed data loaded (if provided)
- ✅ Multi-tenant validation passed

PHP Development Tools Installed:
- ✅ PHPStan (level 8) - Static analysis
- ✅ PHP CS Fixer - PSR-12 formatting
- ✅ PHPUnit/Pest - Testing framework
- ✅ Configuration files created
- ✅ Composer scripts configured

Project Documentation:
- ✅ README.md updated for [Project Name]
- ✅ CLAUDE.md created with project-specific guidance
- ✅ Template docs archived/removed

Branding:
- ✅ Updated throughout application
- ✅ Landing page customized
- ✅ Login page branded

Next Steps:
1. Review updated CLAUDE.md for project-specific guidance
2. Create super admin at http://localhost:8000/super-user-dev.php
3. Login and verify three-tier panel structure
4. Run quality checks: composer quality
5. Begin implementing features from docs/project-requirements/

Development Commands:
- composer test          # Run tests
- composer stan          # Static analysis
- composer cs-fix        # Format code (PSR-12)
- composer quality       # Run all checks

References:
- Requirements: docs/project-requirements/
- Schema: database/schema/
- Development Guide: CLAUDE.md
```

## File Structure After Setup

### Template Structure (Before Project Customization)

```
saas-seeder/
├── public/                # Web root
│   ├── index.php         # Landing page with nav buttons
│   ├── sign-in.php       # Login
│   ├── super-user-dev.php # Super admin creator
│   ├── dashboard.php     # Franchise admin dashboard
│   ├── skeleton.php      # Page template
│   ├── adminpanel/       # Super admin panel
│   ├── memberpanel/      # End user portal
│   └── assets/           # Shared CSS/JS
├── src/
│   ├── config/
│   │   ├── auth.php      # Auth functions + access control
│   │   ├── session.php   # Session prefix helpers
│   │   └── database.php  # Database connection
│   └── Auth/             # Auth services, helpers, DTOs
├── docs/
│   ├── seeder-template/  # Template schemas
│   ├── PANEL-STRUCTURE.md # Architecture guide
│   └── project-requirements/ # ⭐ PUT PROJECT REQUIREMENTS HERE
│       ├── requirements.md
│       ├── business-rules.md
│       ├── user-types.md
│       └── workflows.md
├── database/
│   └── schema/           # ⭐ PUT DATABASE SCHEMAS HERE
│       ├── core-schema.sql
│       └── seed-data.sql
├── .env                  # Environment config
├── composer.json         # Dependencies
├── setup-database.ps1    # Setup script
├── fix-database.ps1      # Fix script
└── CLAUDE.md             # Development guide
```

## References

**Complete documentation in subdirectories:**

- `references/architecture.md` - Complete architectural standards
- `references/workflow.md` - Detailed step-by-step workflow
- `references/troubleshooting.md` - Common issues and solutions
- `references/php-tooling.md` - PHP development tools setup and usage guide

**External references:**

- `../../docs/PANEL-STRUCTURE.md` - Three-tier architecture guide
- `../../CLAUDE.md` - Development guidelines
- `../project-requirements/` - Skill for creating requirements docs

## Quality Assurance

**See `references/php-tooling.md` for complete guide.**

### Quick Commands

```bash
composer cs-fix     # Format code (PSR-12)
composer stan       # Static analysis
composer test       # Run tests
composer quality    # All checks
```

### Pre-Commit Workflow

```bash
composer quality && git commit -m "feat: description"
```

### What to Test

✅ Authentication, franchise isolation, permissions, password hashing, session management, input validation

**See `references/php-tooling.md` for testing examples, CI/CD setup, and IDE integration.**

## Security Checklist Before Production

- [ ] Remove `super-user-dev.php` or restrict access
- [ ] Change `SESSION_PREFIX` from `saas_app_`
- [ ] Set strong `PASSWORD_PEPPER` (64+ chars)
- [ ] Set strong `COOKIE_ENCRYPTION_KEY` (32+ chars)
- [ ] Set `APP_ENV=production`
- [ ] Enable HTTPS (session cookies require it)
- [ ] Review all queries for franchise_id filtering
- [ ] Set proper file permissions on `.env` (600)
