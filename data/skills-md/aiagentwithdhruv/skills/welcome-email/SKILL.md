---
name: welcome-email
description: Send welcome email sequence to new clients. Use when user asks to send welcome emails, onboard new client with emails, or trigger welcome sequence.
---

# Welcome Client Emails

## Goal
Send 3-email welcome sequence (Nick, Peter, Sam) when a new client signs.

## Scripts
- `./scripts/welcome_client_emails.py` - Send welcome sequence

## Process
1. Receive client info (name, email, company)
2. Send email from Nick (welcome, expectations)
3. Send email from Peter (technical setup)
4. Send email from Sam (support intro)

## Usage

```bash
python3 ./scripts/welcome_client_emails.py \
  --client_name "John Doe" \
  --client_email "john@company.com" \
  --company "Acme Corp"
```

## Email Structure
Each email is personalized with client details and sent from different team members to establish relationships.

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_name` | string | Yes | Client full name |
| `client_email` | string | Yes | Client email address |
| `company` | string | Yes | Client company name |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `emails_sent` | integer | Number of welcome emails sent (3) |

### Credentials
| Name | Source |
|------|--------|
| `credentials.json` | file |

### Composable With
Skills that chain well with this one: `onboarding-kickoff`, `create-proposal`

### Cost
Free (Gmail API)
