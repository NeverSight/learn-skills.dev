---
name: market-mapping
description: Sizes a market by triangulating independent top-down and bottom-up estimates (with a bundled calculator that flags disagreement), then maps demand against supply quality to find attractive, under-served white space. Use whenever the user wants a TAM/SAM/SOM, asks how big a market is, wants to evaluate a new market/segment/geography to enter, or is about to put a single market-size number in a deck without having cross-checked it.
---

# Market Mapping

## When to use
Use whenever someone needs a market size for a business case, an investor deck, or an entry decision — and especially when only one estimation method (usually top-down, "X% of a huge industry report number") has been used. Also use when evaluating where to expand: which segment, geography, or use case is genuinely attractive and under-served, versus crowded and already contested.

## What it does
Builds a triangulated TAM/SAM/SOM using two independent methods that must be reconciled, not just one method dressed up as certainty. Then maps demand intensity against current supply quality across segments to find white space: areas where real demand exists but incumbents serve it poorly.

## Method
1. **Size top-down**: total addressable population × realistic target share × average spend. Sanity-check every input against a named external source, not an assumed percentage.
2. **Size bottom-up independently**: expected customer/unit count × realistic revenue per customer, built from your own funnel or comparable go-to-market economics — do not derive it from the top-down number, or triangulation is fake.
3. **Run the bundled calculator** (`scripts/tam_sam_som.py`) with both sets of inputs. If the two estimates diverge by more than ~30%, that is a finding, not a rounding error — resolve which input is wrong before quoting a single number.
4. **Narrow TAM to SAM** by applying real serviceability filters: geography you can actually reach, segment fit, regulatory eligibility, channel access. Each filter should be a defensible percentage, not a round number picked to make the math work.
5. **Narrow SAM to SOM** using a realistic achievable share over a stated time horizon, benchmarked against how fast comparable entrants have actually captured share in comparable markets — not an aspirational number.
6. **Map demand vs. supply quality by segment**: for each candidate segment, plot demand intensity (growth rate, willingness to pay, unmet need signals) against current supply quality (how well incumbents serve it — price, satisfaction, product fit). High demand + poor supply = white space; high demand + strong supply = a share-fight, not white space.
7. **Name the two or three most attractive segments explicitly**, with the evidence for why they're under-served rather than merely large.

## Inputs
- Industry/population data for top-down sizing
- Your own funnel, pipeline, or comparable go-to-market economics for bottom-up sizing
- Serviceability constraints (geography, regulation, channel)
- Any available data on incumbent satisfaction, pricing, or share by segment

## Output format
Reconciled TAM/SAM/SOM with both estimation methods shown and any variance flagged; a demand-vs-supply-quality map by segment; the top 2-3 white-space segments named with evidence.

## Example
A B2B software company sizes a new vertical top-down at $2.9B and bottom-up (based on realistic sales-cycle economics) at $280M — an 90% variance the calculator flags immediately. Digging in, the top-down number assumed every company in the population is a viable buyer; the bottom-up reflects the actual ICP filter. The reconciled, defensible SAM after serviceability filters comes out near the bottom-up end, and the deck is corrected before the board sees the inflated figure.

## Common pitfalls
- Deriving the "bottom-up" number from the top-down one instead of building it independently — this isn't triangulation, it's the same guess twice.
- Presenting a TAM without ever showing SAM/SOM, letting a huge irrelevant number substitute for a realistic revenue case.
- Calling a segment "white space" because it's large, without checking whether it's actually poorly served or just already won by a strong incumbent.
