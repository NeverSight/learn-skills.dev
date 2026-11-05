---
name: periplus-data-extraction
description: Extract structured records from known web pages or captured documents with Periplus. Use for product lists, directories, tables and detail pages needing reliable field alignment, normalization and completeness checks.
---

# Data extraction

Produce usable rows from source content. For a known small source, inspect it and proceed; do not require a separate plan or an unnecessary crawl. Use existing files or a more suitable tool when they already satisfy the request.

## Define rows and fields

Identify the record unit: product, variant, offer, person, location or another explicit entity. Specify requested fields, types, units and repeated-value handling. Preserve original strings alongside normalized values where conversion could lose meaning. For prices, retain currency, billing period, tax basis and market when available; “from”, “contact us”, missing and zero are different values.

## Inspect, extract, expand

Inspect source structure on contrasting examples before generalizing: repeated cards versus detail pages, an alternate layout, a missing price and a record with multiple values. Check whether the captured document actually contains the requested content. An empty client-rendered panel is an acquisition gap. Prefer an available structured source when suitable; treat JSON fields as JSON rather than HTML selectors.

Extract each field within its own record container. Keep capture identity with node identity, and test field alignment when optional elements are absent. Avoid pairing independent title and price arrays by position. Follow a detail-page link when the listing omits a required field. Expand paging URLs, linked records or bounded discovery as needed for the requested coverage.

Check source-stated totals against rendered records and extracted rows. Resolve duplicates at the chosen unit; do not collapse legitimate variants. Inspect failed acquisitions and SQL truncation separately from missing source fields. A page limit limits acquisition, and a result limit limits returned rows; neither guarantees full extraction. Report a partial result with its exact coverage when a remaining gap cannot be resolved within scope.

## Validate the output

Compare extracted records with the source for different layouts and edge cases. Check null rates, repeated values, field shifts, malformed numbers, inconsistent units and key uniqueness. Route exceptions to explicit states such as unavailable in source, acquisition failed, parse failed or ambiguous; do not invent missing values. Preserve repeated values when flattening would change meaning.

Keep source URL, capture ID and observation time for each row. When a field comes from another page, retain that field's evidence. Preserve source dates separately from observation dates. Provide the requested table or file with a short account of completeness, unresolved exceptions and transformations.

If reuse is requested, distinguish the source captures, reusable saved SQL and an exported frozen result. Saving SQL does not save its current rows, and retaining captures does not save the extraction output. Include the extraction logic, parameters and capture manifest with a frozen deliverable, arranging source retention for the required period.

## Live product reference

Read [MCP operational contracts](https://docs.periplus.dev/mcp#agent-workflow) and discover the live schema before querying. Consult [extraction](https://docs.periplus.dev/extraction), [JSON](https://docs.periplus.dev/json), [SQL](https://docs.periplus.dev/sql) and [request diagnostics](https://docs.periplus.dev/requests) for current acquisition, selector, pagination and query mechanics. Keep those mechanics in the live docs rather than assuming stored tool signatures.
