---
name: legal-tos-privacy
description: Create bulletproof Terms of Service and Privacy Policy documents for SaaS applications. Infers company information from codebase/marketing site, conducts comprehensive audits, drafts documents, then asks user ONLY for missing details at the end. Minimizes user interaction. Use when the user needs to draft, review, or update legal documents (ToS, Terms of Service, Privacy Policy, legal pages). Triggers on requests for legal documents, terms drafting, privacy policy creation, "cover our bases legally", liability protection, or legal compliance for software products.
---

# Legal Document Generator: Terms of Service & Privacy Policy

Generate comprehensive, legally protective Terms of Service and Privacy Policy documents. This skill:
1. **Audits** the codebase and marketing materials
2. **Extracts** company info, service details, and data practices automatically  
3. **Drafts** complete documents (using `[[TEMPLATE_VARIABLES]]` for unknowns)
4. **Asks** the user ONLY for information that couldn't be found (minimal interaction)
5. **Delivers** final, ready-to-publish documents with zero placeholders

## Reference Files

- `references/legal-guide.md` - Comprehensive guide to ToS and Privacy Policy drafting
- `references/compliance-checklist.md` - Jurisdiction-specific requirements (GDPR, CCPA, LGPD, COPPA, etc.)
- `references/protective-clauses.md` - Ready-to-adapt legal clauses for common risk scenarios

Read these references as needed when drafting the actual documents.

## Critical Principle: Infer Everything Possible, Ask Only What's Missing

**Minimize user interaction.** Extract and infer as much information as possible from the codebase, marketing site, config files, and any existing legal documents. Only ask the user for information that genuinely cannot be found or inferred.

**Workflow:**
1. Audit codebase and marketing materials (Phases 1-3)
2. Extract company/service info from code during audit
3. Draft documents with template variables for unknowns (Phases 4-5)
4. Final step: resolve any remaining template variables by asking user (Phase 7)

---

## Phase 1: Codebase & Data Flow Audit

Conduct exhaustive exploration to understand every aspect of data handling. **During this audit, also extract company and service information** from the sources below.

### 1.0 Extract Company & Service Information

Search these locations to infer company details - DO NOT ask the user if you can find it:

```
# Package/project metadata
Read: package.json (name, author, description, homepage, repository)
Read: README.md, README (project name, description, company info)

# Config files with company info
Search for: companyName, company_name, APP_NAME, SITE_NAME, BRAND_NAME
Read: .env.example, .env.local.example (for variable names, not secrets)

# Marketing site footer/header (often contains company info)
Read: footer, Footer, layout, Layout files for copyright notices
Search for: "©", "Copyright", "All rights reserved", "Inc.", "LLC", "Ltd."

# Existing legal pages
Read: terms, privacy, legal folders/files (may have company name, address, contact)
Search for: legal@, privacy@, support@, contact@, hello@

# Site metadata
Search for: <title>, meta description, og:site_name, og:title
Read: metadata, siteConfig, site.config, app.config files

# Contact pages
Read: contact, about, company pages for addresses/emails
```

**Track what you find and what's missing:**

| Field | Found? | Value | Source |
|-------|--------|-------|--------|
| Legal Entity Name | | | |
| DBA/Trade Name | | | |
| Entity Type | | | |
| Physical Address | | | |
| Legal Contact Email | | | |
| Privacy Contact Email | | | |
| Support Contact Email | | | |
| Service/Product Name | | | |
| Website URL | | | |
| Governing Law | | | |

**Inference rules:**
- If copyright says "© 2024 Acme Inc." → Legal entity is likely "Acme Inc."
- If package.json has `"author": "Acme Software"` → Use as company name
- If footer has `hello@acme.com` but no legal email → Use hello@ for legal contact
- If site is `acme.com` → Website URL is `https://acme.com`
- If company address found in footer/contact → Use for physical address
- If no governing law found → Leave as template variable (will ask later)

### 1.1 Data Collection Discovery

Search for ALL data collection points:

```
# User input collection
Search for: form, input, useState, formData, register, signup, login, email, password, name, phone, address, billing, payment

# API data handling  
Search for: req.body, request.body, params, query, headers, authorization, bearer, token, cookie, session

# Database schemas
Search for: schema, model, entity, table, @Column, field, prisma.schema, drizzle, mongoose

# Third-party integrations
Search for: stripe, paddle, polar, analytics, google, facebook, pixel, segment, mixpanel, amplitude, sentry, posthog, plausible
```

**Document every data point found:**
- Field name and type
- Where collected (signup, checkout, in-app)
- Purpose (auth, billing, analytics, marketing)
- Storage location (database, third-party)
- Retention period (if determinable)

### 1.2 Third-Party Service Inventory

Identify ALL external services that receive user data:

```
# Check dependencies
Read: package.json, requirements.txt, go.mod, Cargo.toml

# Check environment variables
Search for: process.env, import.meta.env, Deno.env, .env files

# Check API integrations
Search for: fetch, axios, http, api, client, sdk
```

**For each third-party service, document:**
- Service name and purpose
- What data is shared with them
- Their data processing role (processor vs controller)
- Link to their privacy policy/DPA

### 1.3 Authentication & Security Mechanisms

```
Search for: auth, session, jwt, oauth, password, hash, bcrypt, argon, encrypt, ssl, tls, https, 2fa, mfa, totp
```

**Document:**
- Authentication methods used
- Password storage approach
- Session management
- Security features offered to users

### 1.4 User Content & Generated Data

```
Search for: upload, file, image, document, content, post, comment, message, storage, s3, blob, bucket
```

**Document:**
- Types of user-generated content accepted
- Storage mechanisms
- Processing performed on user content
- Who can access user content

### 1.5 Tracking & Analytics

```
Search for: cookie, localStorage, sessionStorage, tracking, analytics, gtag, ga4, pixel, event, track, identify, page
```

**Document:**
- All cookies set (name, purpose, duration)
- Analytics tools and what they track
- Advertising/remarketing pixels
- Cross-site tracking capabilities

## Phase 2: Marketing Claims Audit

Examine all public-facing materials for claims that must be addressed legally.

### 2.1 Feature Claims

```
# Check marketing site
Read all files in: marketing/, website/, landing/, pages/marketing, app/(marketing)

Search for: guarantee, promise, ensure, always, never, 100%, unlimited, secure, safe, protect, best, fastest, #1, leading
```

**Document every claim that could create liability:**
- Uptime/availability claims
- Security/privacy claims  
- Performance claims
- Results/outcome claims
- Comparison claims

### 2.2 Pricing & Subscription Claims

```
Search for: pricing, price, plan, tier, subscription, trial, free, refund, cancel, money-back
```

**Document:**
- All pricing tiers and what's included
- Trial terms
- Refund policy claims
- Cancellation process claims

### 2.3 Compliance & Certification Claims

```
Search for: GDPR, CCPA, HIPAA, SOC, ISO, compliant, certified, secure
```

**Document any compliance claims that must be legally defensible.**

## Phase 3: Risk Assessment

Before drafting, identify highest-risk areas:

### 3.1 Liability Hotspots

Rate each area (High/Medium/Low risk):

- [ ] **Data breach exposure** - What's the damage if data leaks?
- [ ] **Service failure impact** - What happens if product goes down?
- [ ] **Incorrect output liability** - Could wrong results cause harm?
- [ ] **Third-party dependency risk** - What if integrations fail?
- [ ] **User content liability** - Could user content create legal issues?
- [ ] **Regulatory exposure** - Which regulations apply?

### 3.2 Geographic Scope

Determine applicable regulations based on:
- Company location
- Server/data storage locations
- Target user locations
- Actual user locations (if known)

**Regulations to consider:**
- GDPR (EU/EEA users)
- CCPA/CPRA (California users)
- LGPD (Brazil users)
- PIPEDA (Canada users)
- COPPA (if children might use service)
- Industry-specific (HIPAA, PCI-DSS, etc.)

## Phase 4: Draft Terms of Service

Use findings from audit to draft comprehensive ToS. See `references/legal-guide.md` for detailed section guidance.

### Required Sections Checklist

Every ToS MUST include:

- [ ] **Introduction & Acceptance** - Binding agreement, clickwrap consent, effective date
- [ ] **Definitions** - Define "Service", "User", "Content", "Data", etc.
- [ ] **Account Terms** - Registration, accuracy, security responsibility, no sharing
- [ ] **Acceptable Use Policy** - Prohibited activities tailored to your product
- [ ] **Payment Terms** (if paid) - Pricing, billing, taxes, refunds, cancellation
- [ ] **Intellectual Property** - Company owns service, user owns their content, license grants
- [ ] **User Content License** - Rights you need to operate (host, display, process)
- [ ] **Privacy Reference** - Incorporation of Privacy Policy
- [ ] **Third-Party Services** - Disclaimer for integrated services
- [ ] **Warranty Disclaimer** - "AS IS", no guarantees, use at own risk
- [ ] **Limitation of Liability** - Cap damages, exclude consequential damages
- [ ] **Indemnification** - User covers you for their misuse/violations
- [ ] **Term & Termination** - Duration, termination rights, post-termination
- [ ] **Dispute Resolution** - Arbitration, class action waiver, governing law
- [ ] **Governing Law & Venue** - Jurisdiction selection
- [ ] **Force Majeure** - Excuse for uncontrollable events
- [ ] **Severability** - Invalid clauses don't void agreement
- [ ] **Entire Agreement** - This supersedes prior agreements
- [ ] **Modification Rights** - How terms can change, notification requirement
- [ ] **Contact Information** - How to reach you

### Liability Protection Language

Include these protective clauses:

**Service Availability Disclaimer:**
```
The Service is provided on an "as is" and "as available" basis. We do not 
guarantee that the Service will be uninterrupted, timely, secure, or error-free. 
We make no warranties regarding the accuracy, reliability, or completeness of 
any content or results obtained through the Service.
```

**Consequential Damages Exclusion:**
```
IN NO EVENT SHALL [[LEGAL_ENTITY_NAME]] BE LIABLE FOR ANY INDIRECT, INCIDENTAL, 
SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF 
PROFITS, DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, REGARDLESS OF WHETHER WE 
HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
```
(Note: Replace `[[LEGAL_ENTITY_NAME]]` with actual company name found in audit, or resolve in Phase 7)

**Liability Cap:**
```
OUR TOTAL LIABILITY TO YOU FOR ALL CLAIMS ARISING FROM OR RELATED TO THE SERVICE 
SHALL NOT EXCEED THE GREATER OF (A) THE AMOUNTS YOU PAID TO US IN THE TWELVE (12) 
MONTHS PRECEDING THE CLAIM, OR (B) ONE HUNDRED DOLLARS ($100).
```

**Results Disclaimer (for AI/analytics products):**
```
Any insights, recommendations, or outputs generated by the Service are provided 
for informational purposes only and should not be relied upon as professional 
advice. You are solely responsible for evaluating and verifying any results 
before taking action based on them.
```

### Audit-Specific Additions

Based on your audit findings, add clauses for:

**If AI/ML features exist:**
- Output accuracy disclaimer
- No reliance for critical decisions
- Training data usage rights

**If user content is processed:**
- Content ownership clarification
- License grant for processing
- Prohibited content types
- Takedown procedures

**If financial data is handled:**
- Not financial advice disclaimer
- User responsibility for decisions
- No guarantee of results

**If health-related features:**
- Not medical advice disclaimer  
- Consult professional warning
- Emergency services disclaimer

## Phase 5: Draft Privacy Policy

Create comprehensive privacy policy addressing all audit findings.

### Required Sections Checklist

Every Privacy Policy MUST include:

- [ ] **Introduction** - Who you are, what this policy covers
- [ ] **Information We Collect** - All categories from audit (be exhaustive)
- [ ] **How We Collect Information** - Direct input, automated, third-party sources
- [ ] **Why We Collect Information** - Purpose for each category, legal basis (GDPR)
- [ ] **How We Use Information** - All uses discovered in audit
- [ ] **Information Sharing** - All third parties from inventory
- [ ] **Cookies & Tracking** - All cookies/pixels from audit
- [ ] **Data Retention** - How long each category is kept
- [ ] **Data Security** - Security measures from audit
- [ ] **Your Rights** - Access, correction, deletion, portability, objection
- [ ] **Children's Privacy** - COPPA compliance, age restrictions
- [ ] **International Transfers** - Where data goes, safeguards
- [ ] **California Rights** (if applicable) - CCPA/CPRA specific disclosures
- [ ] **EU/UK Rights** (if applicable) - GDPR specific disclosures
- [ ] **Policy Changes** - How updates are communicated
- [ ] **Contact Information** - Privacy contact, DPO if required

### Data Inventory Table

Create a clear table of all data collected:

| Data Category | Examples | Collection Method | Purpose | Legal Basis | Retention |
|--------------|----------|-------------------|---------|-------------|-----------|
| Account Info | Email, name | Registration form | Service delivery | Contract | Account lifetime |
| Payment Data | Card details | Checkout | Billing | Contract | As required by law |
| Usage Data | Pages viewed, features used | Automatic logging | Product improvement | Legitimate interest | 24 months |
| Device Info | IP, browser, OS | Automatic | Security, support | Legitimate interest | 12 months |

### Third-Party Disclosure Table

List all third parties:

| Service | Purpose | Data Shared | Privacy Policy |
|---------|---------|-------------|----------------|
| Stripe | Payments | Billing info | stripe.com/privacy |
| AWS | Hosting | All data (processor) | aws.amazon.com/privacy |
| Google Analytics | Analytics | Usage data, IP | policies.google.com/privacy |

## Phase 6: Verification Checklist

Before finalizing, verify:

### Legal Protection Verification

- [ ] Every marketing claim has corresponding disclaimer if needed
- [ ] All data collection has stated purpose and legal basis
- [ ] All third parties are disclosed
- [ ] Liability is limited to maximum extent permitted by law
- [ ] Warranty disclaimers cover all product functionality
- [ ] Indemnification protects against user misuse
- [ ] Dispute resolution favors your jurisdiction
- [ ] Force majeure covers service interruptions
- [ ] Termination rights preserved for violations

### Compliance Verification

- [ ] GDPR compliant (if EU users): legal basis, rights, DPO contact if needed
- [ ] CCPA compliant (if CA users): categories listed, sale disclosure, opt-out
- [ ] COPPA compliant: age gate, no children data collection
- [ ] Cookie consent mechanism described
- [ ] Data retention periods specified
- [ ] International transfer safeguards noted

### Consistency Verification

- [ ] ToS and Privacy Policy don't contradict each other
- [ ] No promises in ToS that Privacy Policy contradicts
- [ ] Marketing claims align with legal disclaimers
- [ ] Refund policy matches what checkout shows
- [ ] Data practices match what code actually does

## Phase 7: Resolve Template Variables (FINAL STEP)

After drafting both documents, scan for any remaining template variables. Template variables use the format `[[VARIABLE_NAME]]` (double brackets).

### 7.1 Scan for Remaining Variables

Search the drafted documents for any `[[...]]` patterns. Common ones that may need user input:

| Variable | What to ask |
|----------|-------------|
| `[[LEGAL_ENTITY_NAME]]` | "What is your company's full legal name (e.g., 'Acme Software, Inc.')?" |
| `[[PHYSICAL_ADDRESS]]` | "What address should be used for legal notices?" |
| `[[LEGAL_EMAIL]]` | "What email should receive legal inquiries?" |
| `[[PRIVACY_EMAIL]]` | "What email should receive privacy/GDPR requests?" |
| `[[GOVERNING_LAW_STATE]]` | "Which state/country's laws should govern these terms?" |
| `[[DISPUTE_VENUE]]` | "Where should legal disputes be resolved (city/county, state)?" |
| `[[EFFECTIVE_DATE]]` | "When should these documents take effect? (default: today)" |
| `[[ARBITRATION_PROVIDER]]` | "Do you want binding arbitration? If so, which provider (e.g., JAMS, AAA)?" |

### 7.2 Ask User for Missing Information

If any template variables remain, ask the user for ALL missing values in a single request. Group related questions together.

Example:
```
I've drafted your Terms of Service and Privacy Policy based on your codebase. 
I found most information automatically, but need a few details to finalize:

1. **Legal entity name:** What is your company's full legal name as registered?
   (e.g., "Acme Software, Inc." or "Acme LLC")

2. **Physical address:** What address should appear for legal notices?

3. **Governing law:** Which state's laws should govern? (I'd suggest Delaware 
   or California based on most SaaS companies, but this is your choice)

Once you provide these, I'll finalize the documents with no placeholders.
```

### 7.3 Fill In and Verify

After receiving answers:
1. Replace ALL template variables with actual values
2. Re-scan to confirm zero `[[...]]` patterns remain
3. Present the final, complete documents

**The final output must have NO template variables whatsoever.**

---

## Output Format

### During Drafting (Phases 4-5)

Use `[[VARIABLE_NAME]]` syntax (double brackets) for any information you couldn't find during the audit. This makes variables easy to scan for in Phase 7.

### Final Output (After Phase 7)

**NO PLACEHOLDERS IN FINAL OUTPUT.** After resolving all template variables with the user, the final documents must be complete and ready to publish.

The following are FORBIDDEN in final output:
- `[[VARIABLE]]` double-bracket template variables
- `[COMPANY]`, `[DATE]`, `[ADDRESS]` single-bracket placeholders
- `{{variable}}` or `{variable}` template syntax
- "INSERT X HERE", "YOUR X", "TBD", "TBA", "Coming Soon"

Deliver final documents in this structure:

```markdown
# Terms of Service

**Last Updated: [actual date]**

[Full ToS content - every field filled with real values, zero placeholders]

---

# Privacy Policy  

**Last Updated: [actual date]**

[Full Privacy Policy - every field filled with real values, zero placeholders]
```

## Important Notes

1. **Minimize user interaction** - Infer and extract as much as possible from the codebase. Only ask the user for information that genuinely cannot be found. Batch all questions into a single request at the end (Phase 7).

2. **No placeholders in final output** - Use `[[VARIABLE]]` during drafting for unknowns, but resolve ALL of them before delivering final documents. The user should receive ready-to-publish documents.

3. **Be specific** - Generic templates create liability gaps. Every clause should reflect actual product behavior discovered in audit.

4. **Plain language** - Write clearly. Courts and regulators favor understandable policies.

5. **Conservative claims** - When in doubt, disclaim more. It's better to under-promise legally.

6. **Verify before delivery** - After Phase 7, scan for any remaining `[[...]]` patterns. If found, resolve before presenting final documents.

7. **Not legal advice** - These documents should be reviewed by qualified legal counsel before publication.
