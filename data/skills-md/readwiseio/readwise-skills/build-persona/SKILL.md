---
name: build-persona
description: Build a personalized reading profile from your Readwise Reader data, used by triage, quiz, and other skills
---

You are building a reader persona for the user based on their Readwise Reader library. This persona file is used by other skills (triage, quiz, etc.) to personalize their experience.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout (and pass this context to the subagent). If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`, `readwise search <query>`, `readwise highlights <query>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Welcome

Open with a brief introduction:

> **Build Persona** · Readwise Reader
>
> I'll analyze your reading history — saves, highlights, and tags — and build a `reader_persona.md` profile in the current directory. Other skills (triage, quiz) will use this to personalize their output to you.
>
> I'll start with a quick pass (~1-2 min) and then you can decide if you want a deeper analysis.

## Process

**IMPORTANT:** This skill involves fetching a lot of data. To keep the main conversation context clean, launch a **Task subagent** to do all the heavy lifting.

### Phase 1: Quick Pass

The subagent should do a focused scan to build a solid initial persona fast:

1. **Gather data.** Run ALL of these in parallel (one batch of tool calls):

   - **4 highlight searches:** `mcp__readwise__readwise_search_highlights` with 4 broad queries (e.g. "ideas strategy product", "learning technology culture", "writing craft creativity", "business leadership growth") with `limit=50` each. These are semantic/vector searches so broad multi-word queries work well. Highlights are cheap and high-signal — cast a wide net.
   - **4 document lists:** `mcp__readwise__reader_list_documents` from each non-feed location: `location="new"`, `location="later"`, `location="shortlist"`, and `location="archive"` with `limit=100` each. If the combined results are very sparse (< 20 docs total), also try without a location filter or with `location="feed"` as a fallback. Only fetch metadata: `response_fields=["title", "author", "category", "tags", "site_name", "summary", "saved_at", "published_date"]`. Do NOT fetch full content.
   - **Tags:** `mcp__readwise__reader_list_tags` to understand their organizational system.

2. **Parse results efficiently.** The JSON responses from document lists can be large (25k+ tokens). Do NOT try to read them with the Read tool — it will hit token limits and waste retries. Instead, use a single Bash call with a python3 script to extract and summarize all the data at once. The script should parse all result files together and output:
   - Document counts by category
   - Top 20 sites, authors, and tags
   - Save velocity by month
   - All docs saved in the last 3 weeks (title, category, author, date)
   - A representative sample of highlight texts with their source titles/authors

3. **Write the persona.** Write `reader_persona.md` to the current working directory with these sections:

   - **Identity & Role** — Who they appear to be (profession, role, industry)
   - **Core Interests** — Top themes and topics, ranked by frequency and recency
   - **Reading Personality** — How they read (saves a lot but reads selectively? highlights heavily? prefers short or long-form?)
   - **Current Obsessions** — What they've been saving/reading most in the last 2-3 weeks
   - **Goals & Aspirations** — What they seem to be working toward, inferred from patterns
   - **Taste & Sensibility** — Thinkers and styles they gravitate toward (contrarian? practical? philosophical? technical?)
   - **Anti-interests** — Topics notably absent or avoided
   - **Triage Guidance** — Specific instructions for how to pitch documents to this person (e.g. "lead with practical applicability", "connect to their interest in X", "bar is high for AI content — flag when it's genuinely novel")

4. **Return** a brief summary (3-5 sentences) of the persona AND the absolute path to the file.

**Subagent speed rules:**
- Do NOT call `readwise_list_highlights` — it often errors and is redundant with search.
- Do NOT try to Read large JSON tool-result files — parse them with python3 via Bash.
- Combine all analysis into ONE python script, not multiple sequential scripts.
- Maximize parallel tool calls. Every API fetch in step 1 should be a single parallel batch.

### Phase 2: Deep Pass (optional)

After the quick-pass subagent returns, show the user the results and ask if they want a deeper analysis. If yes, launch a second subagent that:

- Fetches 4-6 more highlight searches with *different, more specific* queries informed by what phase 1 found (e.g. if the persona shows interest in AI tooling, search "AI agents workflows automation"; if they read fiction, search "fiction narrative storytelling") with `limit=50` each
- Paginates beyond the first 100 docs per location using `next_page_cursor` from phase 1 results — fetch the next 100-200 per location to build a much larger sample
- Reads the existing `reader_persona.md` and enriches/rewrites it with the additional data — more nuanced sections, stronger evidence, sharper triage guidance
- Returns a summary of what changed

## After Each Subagent Returns

1. **Show the file link.** Always tell the user: `reader_persona.md` was written to `{absolute_path}`. Display the full path so they can open it.
2. **Show a summary** of the persona (use the subagent's returned summary).
3. After phase 1: **Ask if they want the deep pass** or if the quick version is good enough. Also ask if they want to adjust anything.
4. After phase 2 (if run): **Show what changed** and ask if they want to adjust anything.
5. **If adjustments needed,** edit the file directly based on their feedback.
6. **Confirm saved.** Tell them the file is saved and which skills will now use it (triage, quiz, feed-catchup, etc.).
