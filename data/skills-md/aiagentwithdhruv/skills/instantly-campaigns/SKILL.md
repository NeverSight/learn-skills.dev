---
name: instantly-campaigns
description: Create cold email campaigns in Instantly with A/B testing. Use when user asks to create email campaigns, set up cold outreach, build email sequences, or configure Instantly campaigns.
---

# Instantly Campaign Creation

## Goal
Create three email campaigns in Instantly based on a client description and offers. Each campaign has A/B tested first emails and follow-up sequences.

## Inputs
1. **Client Description**: Company name, industry, target audience, value proposition
2. **Offers** (optional): List of 3 offers. If not provided, will be generated.

## Scripts
- `./scripts/instantly_create_campaigns.py` - Creates campaigns via Instantly API
- `./scripts/read_sheet.py` - Read lead data if needed

## Process

### 1. Load Examples
Read `.tmp/instantly_campaign_examples/campaigns.md` for inspiration on personalization + social proof + offer structure.

### 2. Generate Campaigns
```bash
python3 ./scripts/instantly_create_campaigns.py \
  --client_name "ClientName" \
  --client_description "Description of the client..." \
  --offers "Offer 1|Offer 2|Offer 3" \
  --target_audience "Who we're emailing" \
  --social_proof "Credentials/results to mention"
```

### 3. Review Output
The script creates 3 campaigns (one per offer), each with:
- Email 1: Two A/B variants
- Email 2: Follow-up bump
- Email 3: Breakup email

## Campaign Structure

### Email 1 (A/B Split Test)
- Personalization hook (`{{icebreaker}}` or custom opener)
- Social proof (credentials, results)
- Offer (clear value proposition)
- Soft CTA

### Email 2 (Follow-up)
- Brief, friendly bump
- Reference original email
- Restate value
- Clear CTA

### Email 3 (Breakup)
- Short, direct
- Last chance framing
- Simple yes/no ask

## Available Variables
- `{{firstName}}` - Lead's first name
- `{{lastName}}` - Lead's last name
- `{{companyName}}` - Lead's company
- `{{casualCompanyName}}` - Informal company name
- `{{icebreaker}}` - AI-generated icebreaker
- `{{sendingAccountFirstName}}` - Sender's first name

## Edge Cases
- **No offers provided**: Generate 3 distinct offers from client description
- **API errors**: Script retries once, then fails with detailed error
- **Rate limits**: Handled with exponential backoff

## Output
```json
{
  "status": "success",
  "campaigns_created": 3,
  "campaign_ids": ["id1", "id2", "id3"],
  "campaign_names": ["Campaign 1", "Campaign 2", "Campaign 3"]
}
```

## Environment
Requires in `.env`:
```
INSTANTLY_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## API Learnings
- Schedule requires `name` field in each schedule object
- Timezone: Use `America/Chicago` (not all IANA values work)
- HTML: Instantly strips plain text outside HTML tags - wrap in `<p>` tags
- Model: Uses `claude-opus-4-5-20251101` for generation

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_name` | string | Yes | Client company name |
| `client_description` | string | Yes | Company description and value proposition |
| `offers` | string | No | Pipe-separated offers (auto-generated if missing) |
| `target_audience` | string | Yes | Who we're emailing |
| `social_proof` | string | Yes | Credentials/results to mention |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `campaign_ids` | array | 3 Instantly campaign IDs |
| `campaign_names` | array | Campaign names |

### Credentials
| Name | Source |
|------|--------|
| `INSTANTLY_API_KEY` | .env |
| `ANTHROPIC_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `scrape-leads`, `gmaps-leads`, `casualize-names`, `onboarding-kickoff`

### Cost
Claude API + Instantly plan
