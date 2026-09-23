---
name: amazon-tiktok-signal
description: Analyze current TikTok offsite heat, recent-month momentum, and commercial signals for one or more Amazon ASINs with compatible KOLSprite MCP tools. Use when an Amazon seller provides ASINs or Listings and asks whether they have TikTok signals, how the latest 30 days compare with the prior 30 days, or which ASIN has the stronger TikTok opportunity. Do not use for generic TikTok research, exact Amazon sales attribution, or future-sales prediction.
---

# Amazon TikTok Signal

Turn ASIN-related TikTok video candidates into a decision-ready signal report. Use the active MCP connection that exposes the compatible KOLSprite tool contract automatically; do not ask whether to call it after this Skill applies.

## Compatible MCP routing

- Prefer the SellerSpace Yunya unified MCP when it is available and authenticated.
- Support direct business tools plus current and legacy Yunya facade entrypoints.
- In direct mode, resolve and call `asin_analysis_video` by its semantic business name.
- In Yunya facade mode, if the business tool is not visible at the host's top level, make at most one host-level discovery attempt and prefer the product-specific `yunya_search_kolsprite_tools`. Call it once with the ASIN-video-analysis intent; use the exact internal tool name and complete input schema it returns, then invoke that tool through `call_read_tool`.
- If the product-specific entrypoint is unavailable but the legacy generic `yunya__search_tools` is discoverable, use it with provider `kolsprite`, operation `read`, and the same intent. Do not prefer the generic entrypoint when the product-specific one is available.
- Do not guess a facade namespace, internal tool name, wrapper, or arguments. Reuse the discovered name and schema for the run.
- A host-level miss for `asin_analysis_video` does not prove that the internal business tool is absent. Only report a missing business dependency after direct exposure and the available current or legacy facade lookup fail. If neither facade entrypoint can be discovered, report a connector-discovery failure and do not switch to an unrelated fallback service.
- A standalone KOLSprite MCP remains compatible only when it exposes the same required semantic tool names, input schemas, and response shapes.
- If both connections are enabled, use one connection for the entire run, prefer Yunya, and never duplicate a paid call across both services.
- Treat an absent or schema-incompatible `asin_analysis_video` as a missing dependency and stop as specified below.

## Inputs

- Require one or more Amazon ASINs and an Amazon market such as `US` or `GB`.
- Default TikTok `region` to the Amazon market unless the user specifies another target region.
- Use an Amazon title, leaf category, brand, core function, and key attributes when the host product or user provides them. These fields improve relevance classification; do not invent missing Listing facts.
- Preserve ASINs and all TikTok IDs as strings.

## Select one mode

- **Quick check:** Default for one ASIN when the user asks whether it has TikTok heat or signals. Request page 1 with 20 records. Report head-content heat, evidence quality, diffusion, commerce, and representative evidence.
- **Full signal:** Use when the user asks for a complete/deep analysis, overall heat, recent-month comparison, or why the signal is rising or falling. Request up to pages 1–5 at 20 records per page, stopping earlier when the result is exhausted or a material error occurs. Treat the collected top-play videos as a representative head sample and allow a rough overall latest-30-days versus prior-30-days judgment.
- **ASIN comparison:** Use when the user provides 2–3 ASINs or explicitly asks which product has stronger TikTok opportunity. Use identical market, region, mode, page size, relevance rules, and calculation rules for every ASIN. Default to quick check unless the user explicitly requests a full comparison.

Do not automatically analyze more than three ASINs in one run. One ASIN requires one independent paginated call chain; report partial comparison results when one chain fails.

## Retrieve and normalize MCP evidence

1. Call `asin_analysis_video` with `asin`, `market`, `region`, `page_num`, and `page_size: 20`.
2. Parse the text JSON in the MCP result. Support both an older array response and the paginated form:

   ```text
   list = Array.isArray(data) ? data : data?.list ?? []
   ```

3. Retain `pageNum`, `pageSize`, `total`, requested pages, returned rows, deduplicated rows, and the stop reason.
4. Deduplicate videos by `id`. Detect a suspiciously repeated stable-ID page and stop rather than claiming additional coverage.
5. Classify every video as `same_product_family`, `highly_similar`, `related_scene`, or `noise`. Read [statistics-and-judgment.md](references/statistics-and-judgment.md) before calculating or judging a result.
6. Include `same_product_family` and `highly_similar` with equal weight in all heat, momentum, diffusion, and commerce calculations. Exclude `related_scene` and `noise` from those calculations, while retaining their counts for evidence-quality disclosure.

The unified tool contract supplies videos published within roughly the latest six months, ordered by play count descending and paginated at 20 records. Treat this as intended integration behavior, not a permanent protocol fact: if current MCP metadata or returned records contradict it, disclose the observed boundary and narrow the judgment.

## Judge and explain

- Separate **MCP observations**, **client calculations**, **rough business judgments**, and **recommended actions**.
- A full signal run may say “整体近30天热度较上一个30天上升/持平或混合/下降（粗略）” when the collected representative sample supports it. Base the direction on the visible combination of valid-video activity, creator spread, and age-adjusted play velocity. Always show those underlying values; do not imply a precise prediction score.
- Use publication cohorts and age-adjusted play velocity for recent-month comparison. Do not compare raw total plays alone because older videos have had more time to accumulate views.
- Treat `salesVolumeLst30d` as the current rolling 30-day value. Do not describe it as historical sales generated during the video's publication month.
- Do not describe MCP `total` as the number of valid same/similar videos. It is the server's candidate total.
- Do not claim that TikTok caused Amazon sales, that a TikTok product is the exact Amazon ASIN, or that the Skill predicts future sales.
- Read [output-contract.md](references/output-contract.md) before delivering a full signal or ASIN comparison. A quick check may use its compact template without loading comparison details.

## Evidence and stopping rules

- Fewer than three valid same-product-family/highly-similar videos means **insufficient reliable signal**. Show the best evidence and exclusions, but do not force a heat grade.
- A latest-30-days versus prior-30-days comparison with fewer than three valid cohort videos in total is unavailable. With a small or one-sided cohort, allow only a clearly labelled rough observation rather than a formal trend grade.
- Stop the affected chain on authentication, entitlement, insufficient-point, rate-limit, schema, or repeated server errors. Do not change credentials or hide an interrupted collection.
- If `asin_analysis_video` is absent from the current unified MCP tool list, report that the required tool is unavailable and stop instead of substituting `video_search` or inventing an ASIN mapping.
- Do not fetch discretionary extra pages beyond the selected mode. Ask before expanding a quick comparison into a full comparison when the additional calls materially increase cost or latency.
- Point use follows actual executed MCP calls. Do not hardcode point prices or report a deduction unless the MCP or host exposes it. A failed, empty, or insufficient-evidence result is not proof that an account was charged.

## Finish with one next decision

Lead with the heat and momentum judgment, then the evidence. End with one action tied to the signal type, such as prioritizing an ASIN for validation, testing multiple creators, reproducing a proven content angle, or pausing because current evidence is weak. Keep broader TikTok product, video, caption, or creator research as an optional hand-off after answering the ASIN decision.
