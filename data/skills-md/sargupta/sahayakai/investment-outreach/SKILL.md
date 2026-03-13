---
name: investment-outreach
description: Specialized skill for creating investment and collaboration materials for SARGVISION AI. Use when asked to (1) refine outreach strategies, (2) draft investor emails, (3) create collaboration proposals, or (4) synchronize communications with the project's technical and social impact vision. This skill facilitates professional outreach by analyzing existing project proposals, investor decks, and strategic reviews for deep context, performing web searches for investor/partner profiles, and drafting tailored content.
---

# Investment Outreach Skill

This skill provides a structured workflow for generating high-impact outreach materials tailored to investors, academic collaborators, and strategic partners.

## Core Directives

1.  **Context-First Drafting**: Before drafting any content, you MUST reference the core project documentation. Use the [DOCUMENT_LOOKUP_META.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/internal_reviews/DOCUMENT_LOOKUP_META.md) as your primary index to find the most relevant data.
2.  **Metadata-Aware Search**: Use the metadata guidelines in `DOCUMENT_LOOKUP_META.md` to identify whether a query requires "Technical Due Diligence" (e.g., `CHALLENGING_QUESTIONS.md`) or "Financial Projections" (e.g., `INVESTOR_MATERIALS.md`).
3.  **External Validation**: Use `search_web` to find the latest updates on the recipient or their firm to create a relevant and personalized "Hook."
4.  **Term Consistency**: Maintain the high-fidelity, Berkeley-standard tone established in the project's summit proposals.

## Workflow: Drafting Outreach

### Step 1: Metadata Lookup
Consult [DOCUMENT_LOOKUP_META.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/internal_reviews/DOCUMENT_LOOKUP_META.md) to identify the "Primary Audience" and "Key Content" for the specific outreach target.

### Step 2: Internal Deep Dive (Selective)
Based on Step 1, read the targeted files. **SahayakAI_Whitepaper_2026.md** is the DEFAULT reference for all high-level narrative and vision.

Common combinations:
- **General/Vision Pitch**: [SahayakAI_Whitepaper_2026.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/SahayakAI_Whitepaper_2026.md).
- **Financial Pitch**: [SahayakAI_Whitepaper_2026.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/SahayakAI_Whitepaper_2026.md) + [INVESTOR_MATERIALS.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/internal_reviews/INVESTOR_MATERIALS.md).
- **Technical/Research**: [SahayakAI_Whitepaper_2026.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/SahayakAI_Whitepaper_2026.md) + [CHALLENGING_QUESTIONS.md](file:///Users/sargupta/SahayakAIV2/sahayakai/sahayakai-main/CHALLENGING_QUESTIONS.md).
- **Regional/Policy**: [SahayakAI_Whitepaper_2026.md](file:///Users/sargupta/SahayakAIV2/sahayakai/outputs/investment_and_proposals/SahayakAI_Whitepaper_2026.md) + [RURAL_INDIA_ROADMAP.md](file:///Users/sargupta/SahayakAIV2/sahayakai/sahayakai-main/RURAL_INDIA_ROADMAP.md).

### Step 2: Recipient Research
Use `search_web` to identify:
- Recent investments or public statements made by the individual/firm.
- Specific interest areas (e.g., EdTech, Emerging Markets, Decentralized AI).
- Any existing connections or overlapping interests with SARGVISION AI.

### Step 3: Content Synthesis
Construct the email or proposal using this structure:
- **Subject**: Compelling, high-context, and professional.
- **Hook**: A personalized observation based on Step 2.
- **Proof**: Specific, data-driven metrics from SARGVISION (e.g., 92% alignment, 68% cache hits).
- **The Ask**: A clear, low-friction next step (e.g., a 15-minute briefing).

## Standardized Terms

Use these terms consistently to maintain the SARGVISION identity:
- **Universal Learning Equity**: The core social mission.
- **Sovereign AI**: The resilient, localized technical framework.
- **Agent Garden**: The multi-agent orchestration topology.
- **Frugal Innovation**: Efficiency and cost-reduction at the network edge.
