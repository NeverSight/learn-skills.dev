---
name: create-proposal
description: Generate PandaDoc proposals from client information or sales call transcripts. Use when user asks to create a proposal, generate a quote, draft a contract, or prepare a client document.
---

# Proposal Generation

## Goal
Create PandaDoc proposals for clients, either from structured information or by extracting details from sales call transcripts.

## Inputs (One of the following)

**Option A: Structured Data**
- Client First Name, Last Name, Email, Company
- Project Title
- 4 Key Problems (brief)
- 4 Key Benefits (brief)
- Project Duration
- Investment Breakdown (Month 1, Month 2, Month 3+)

**Option B: Call Transcript**
- Sales call transcript to extract all details from

## Scripts
- `./scripts/create_proposal.py` - Creates PandaDoc proposal via API
- `./scripts/read_sheet.py` - Read client data from sheets if needed

## Process

### 1. Gather Information
- If user provides structured data, use directly
- If user provides transcript, extract:
  - Client info (name, company, email)
  - Project context and title
  - 4 main problems/pain points
  - 4 proposed solutions/benefits
  - Financial terms (duration, value, costs)
- Ask for any missing critical information

### 2. Generate Content
Expand the 4 problems and 4 benefits into strategic paragraphs:

**Problem Expansion Guidelines:**
- Use direct "you" language (not third-person)
- Focus on revenue impact and dollar amounts
- Be specific and actionable
- Example: "Right now, your top-of-funnel is converting very poorly to booked meetings..."

**Benefit Expansion Guidelines:**
- Address the client directly
- Emphasize ROI and payback period
- Focus on concrete deliverables

**Also generate:**
- Slide Footer: "Confidential | [Company] Strategic Initiative | [Date]"
- Contract Footer: "[Company]-[ProjectTitle]-[YYYY-MM]"
- Created Date: Current date (YYYY-MM-DD)

### 3. Execute Proposal Creation
```bash
python3 ./scripts/create_proposal.py <<'EOF'
{
  "client": {
    "firstName": "...",
    "lastName": "...",
    "email": "...",
    "company": "..."
  },
  "project": {
    "title": "...",
    "problems": {
      "problem01": "[Expanded Problem 1]",
      "problem02": "[Expanded Problem 2]",
      "problem03": "[Expanded Problem 3]",
      "problem04": "[Expanded Problem 4]"
    },
    "benefits": {
      "benefit01": "[Expanded Benefit 1]",
      "benefit02": "[Expanded Benefit 2]",
      "benefit03": "[Expanded Benefit 3]",
      "benefit04": "[Expanded Benefit 4]"
    },
    "monthOneInvestment": "...",
    "monthTwoInvestment": "...",
    "monthThreeInvestment": "..."
  },
  "generated": {
    "slideFooter": "...",
    "contractFooterSlug": "...",
    "createdDate": "..."
  }
}
EOF
```

### 4. Send Follow-Up Email
Use Gmail to send HTML follow-up email:
- Subject: "Re: [Brief Project Context] Discussion"
- Opening: Thank them for discussing challenges
- Body: 2-4 numbered sections with bold headers
- Each section: Description + "Steps:" bullet points
- Closing: "I'll send you a full proposal shortly..."
- Signature: "Thanks, Nick"

### 5. Notify User
- Provide the PandaDoc "internalLink" for review
- Confirm follow-up email was sent

## Output
- PandaDoc proposal URL (for editing/review)
- Follow-up email sent to client

## Environment
Requires in `.env`:
```
PANDADOC_API_KEY=your_key
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_first_name` | string | Yes | Client first name |
| `client_last_name` | string | Yes | Client last name |
| `client_email` | string | Yes | Client email address |
| `client_company` | string | Yes | Client company name |
| `project_title` | string | Yes | Project title |
| `problems` | array | Yes | 4 key problems (brief) |
| `benefits` | array | Yes | 4 key benefits (brief) |
| `investment_breakdown` | object | Yes | Month 1, Month 2, Month 3+ pricing |
| `call_transcript` | string | No | Alternative: sales call transcript to extract details from |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `pandadoc_url` | string | PandaDoc internal link for review |
| `email_sent` | boolean | Whether follow-up email was sent |

### Credentials
| Name | Source |
|------|--------|
| `PANDADOC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `onboarding-kickoff`, `welcome-email`

### Cost
PandaDoc API call (free tier available)
