---
name: amazon-to-tiktok-validator
description: Evaluate whether one Amazon ASIN or Listing is worth a small TikTok test by starting with SellerSprite asin_detail and an Amazon evidence brief, then validating it with KOLSprite TikTok evidence. Complete or explicitly degrade the SellerSprite stage before any KOLSprite business-data call. Use when the user asks whether an Amazon product should expand to TikTok, what content and creators to test first, or requests a minimum TikTok test plan. Do not use for signal-only ASIN lookups, generic category research, direct creator searches, Amazon operations analysis, exact cross-platform attribution, or future-sales prediction.
---

# Amazon to TikTok Validator

Decide whether the supplied Amazon product has enough evidence to enter a small TikTok test in the target market, then define the smallest useful content-and-creator experiment. The decision is about entering a test, not committing inventory, ad budget, or a full market launch.

Start with SellerSprite. The exact first business-data tool is `asin_detail` unless a complete, source-labelled Amazon evidence brief already exists in the conversation. Do not call a KOLSprite business-data tool first.

## Compatible MCP routing

- Prefer the SellerSpace Yunya unified MCP when it is available and authenticated. Its verified unified contract fully supports this Skill's SellerSprite-first and KOLSprite-validation workflow through one connection.
- Support direct business tools plus current and legacy Yunya facade entrypoints.
- In direct mode, resolve each required SellerSprite or KOLSprite tool by its semantic business name.
- In Yunya facade mode, when a required business tool is not visible at the host's top level, make at most one host-level discovery attempt and prefer the product-specific entrypoint. Use `yunya_search_sellersprite_tools` for the Amazon stage and invoke its returned exact internal tool names through `call_read_tool`. Complete or explicitly degrade that stage before using `yunya_search_kolsprite_tools` for TikTok-validation tools.
- If a required product-specific entrypoint is unavailable but the legacy generic `yunya__search_tools` is discoverable, use it with provider `sellersprite` or `kolsprite`, operation `read`, and the same smallest necessary query. Do not prefer the generic entrypoint when the corresponding product-specific one is available.
- Use each complete input schema returned by the selected search entrypoint; do not guess a facade namespace, internal tool name, wrapper, or arguments. Batch related discovery where possible and reuse names and schemas for the run.
- A host-level miss for `asin_detail` or a KOLSprite business tool does not prove internal absence. Only report a missing business dependency after direct exposure and the available current or legacy facade lookup fail. If neither facade entrypoint can be discovered, report a connector-discovery failure and do not switch to an unrelated substitute.
- A compatible standalone SellerSprite MCP can complete the Amazon stage when it is available, authenticated, and exposes the required semantic tool names, input schemas, and response shapes. Completing the full workflow through standalone connections requires both the SellerSprite MCP and the KOLSprite MCP.
- On Yunya, keep the logical SellerSprite-first sequencing even though both capability groups come from one MCP connection.
- In a standalone setup, finish or explicitly degrade the SellerSprite stage before using the separate KOLSprite connection.
- When Yunya and standalone services are all visible, prefer Yunya for the whole workflow and never duplicate a paid call across services.
- Resolve tools by semantic business name rather than a client-specific server prefix. Stop or narrow the workflow when a required capability is absent or schema-incompatible.

## Required input

- One Amazon ASIN or Listing.
- Amazon marketplace and target TikTok market. Infer them from the URL and context when reliable; state the assumption. Ask only if ambiguity would materially change the analysis.
- Optional user constraints: price, stock, target audience, creator budget, test duration, or known competitors.

Handle one ASIN per run. If the user gives multiple ASINs, recommend a signal comparison first or ask them to choose one for full validation.

## Select depth from intent

- **Quick validation:** Default when the user asks whether the product is worth exploring or testing. Build the Amazon brief, validate current TikTok evidence, and return a bounded decision without caption analysis or broad creator expansion.
- **Full test plan:** Use when the user explicitly asks how to test, requests content directions and creators, or asks for a deep/complete validation. Add creator qualification and only the minimum representative caption analysis needed for script-level recommendations.

Do not stop after every phase. Continue automatically within the selected depth. Only pause when the product/market identity is materially ambiguous, a requested expansion creates material extra cost not already implied by the request, or external authorization is required.

## Read the relevant references

1. Always read [workflow.md](references/workflow.md) and [decision-rubric.md](references/decision-rubric.md).
2. Read [field-mapping.md](references/field-mapping.md) before converting Amazon evidence into TikTok queries.
3. Read [mcp-capability-map.md](references/mcp-capability-map.md) when discovering or calling SellerSprite or KOLSprite MCP tools.
4. Read [evidence-and-output.md](references/evidence-and-output.md) before calculating the final decision or exporting any artifact.

## Platform-neutral tool use

- Match tools by their MCP-declared business name and input schema. A host may add a namespace or expose tools lazily; do not hardcode a host-specific prefix.
- Verify required capabilities from the current MCP metadata when possible. Live metadata outranks this Skill's snapshot.
- Never guess credentials, category IDs, enum values, request wrappers, or return-field names.
- Keep credentials outside the Skill and outputs.
- Use the smallest set of calls that answers the decision. Reuse returned records.
- Do not report a point or credit deduction unless the MCP or host returns actual usage.

## Hard sequencing invariant

Treat SellerSprite as the product-understanding layer and KOLSprite as the downstream TikTok-validation layer.

1. Discover or confirm SellerSprite capabilities before discovering KOLSprite capabilities. Do not begin with a KOLSprite tool lookup merely because the input contains an ASIN.
2. Unless the conversation already contains a complete, source-labelled Amazon evidence brief, the first business-data call must be SellerSprite `asin_detail`.
3. Complete or explicitly degrade the required SellerSprite evidence stage before calling any KOLSprite business-data tool, including `asin_analysis_video`.
4. Reuse sufficient SellerSprite evidence already established in the same conversation; do not repeat paid calls solely to satisfy ordering.
5. If SellerSprite is unavailable and only an ASIN was supplied, stop before KOLSprite retrieval and request the minimum Listing context. If sufficient user-provided Listing evidence exists, continue with reduced confidence and disclose the substitution.

A host-level connection check is not business analysis. If the host must inspect all configured MCPs up front, keep that check silent where possible and still preserve SellerSprite as the first visible and first business-data stage.

## Core workflow

1. **Normalize the product and markets.** Confirm the ASIN, product form, core function, Amazon marketplace, target TikTok market, and market-code mapping.
2. **Build the Amazon evidence brief.** Use SellerSprite to obtain product identity, current demand/lifecycle evidence, recent customer language, and direct competitor seeds. Mark predicted values as predictions.
3. **Translate evidence into hypotheses.** Produce exact-product, scenario, pain, demonstration, and competitor query groups. Amazon facts generate hypotheses; they do not prove TikTok opportunity.
4. **Validate on TikTok.** Use KOLSprite to collect ASIN-related candidates, products, and videos. Clean relevance before calculating current heat, recent direction, content structure, concentration, and creator diffusion. Expand to creator, shop, or caption tools only when the selected depth requires them.
5. **Judge five dimensions.** Assess Amazon demand validity, TikTok commercial signal, latest-30-day momentum, content fit and competition structure, and creator diffusion/executability. Keep decision and evidence confidence separate.
6. **Return one decision and one minimum test when supported.** Use `worth_testing`, `conditional_test`, or `not_recommended`. If evidence is incomplete, issue no business decision; report the evidence state and the smallest next retrieval instead.

## Non-negotiable evidence rules

- Separate **observed MCP data**, **client calculations**, **business judgment**, and **recommended action**.
- MCP candidate totals are not valid related-result counts.
- Classify records as `same_product_family`, `highly_similar`, `related_scene`, or `noise`. Only the first two enter opportunity calculations.
- Keep latest 30 days, prior 30 days, and cumulative values separate.
- A current rolling-30-day sales field is not historical sales for the video's publication month.
- Do not claim that a TikTok item is the exact Amazon ASIN unless the tool explicitly proves identity.
- Do not claim TikTok caused Amazon sales, predict future sales, or present estimates as official platform data.
- Missing evidence is `unverified`, not zero and not automatically weak.

## Degradation and stopping

- If SellerSprite is unavailable but the user supplied sufficient Listing content, continue with user-provided Amazon evidence and lower confidence. If only an ASIN is available, request the minimum missing Listing context or stop the joint validation.
- If KOLSprite is unavailable, return the Amazon brief and hypotheses, but do not issue a TikTok test recommendation.
- If direct ASIN-to-video analysis is absent, do not substitute generic video search while claiming ASIN mapping. Generic searches may support a clearly labelled product-family study only.
- If category-list tools are unavailable in the host, omit category filters and perform explicit post-retrieval relevance filtering; never invent category values.
- Stop the affected branch on authentication, entitlement, insufficient-point, schema, or repeated server errors. Report what remains verified and what was not executed.
- Fewer than three valid TikTok records normally means the TikTok signal is insufficient for a reliable grade. Show the evidence and next validation step instead of forcing a decision.

## Delivery

Default to a concise in-conversation decision card. Create files only when the user asks to save, export, share, or produce a formal report. Follow the output contract and end with one smallest next action plus a success and stop condition.
