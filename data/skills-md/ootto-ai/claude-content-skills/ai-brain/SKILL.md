---
name: ai-brain
description: >
  Give Claude a permanent, searchable long-term memory using an Obsidian vault as the store. At the
  end of a session, summarize what mattered and save it as a Markdown note in your "AI Brain" vault;
  at the start of a session (or on demand), read back only the relevant past notes. Local markdown you
  own — connected via the Filesystem MCP. Trigger with "wrap up", "save this session", or "remember this".
user-invokable: true
argument-hint: "[wrap up | remember this | recall <topic>]"
license: MIT
metadata:
  author: Ootto
  version: "1.1.0"
  category: memory
---

# AI Brain — persistent memory for Claude via Obsidian

You maintain a long-term memory for the user in an **Obsidian vault** — a folder of Markdown notes the
user owns on disk. The vault is the durable store; this skill is how you write to it and read from it.
You reach the vault through the connected **Filesystem MCP** (read/write files in the vault folder).
Notes live under an `AI Brain/` folder; use Obsidian `[[wikilinks]]` and `#tags` so memories connect.

> One-time setup: in Claude Desktop add the Filesystem connector pointed at your Obsidian vault
> (Settings → Developer → Edit Config). No browser automation, no login — it's just your local notes.

## When the user says "wrap up" / "save this session" / "remember this" — SAVE

1. **Review the whole conversation.** Pull out only what's worth remembering long-term:
   - Decisions made (and the reasoning / alternatives rejected)
   - Facts & context about the user, their project, their preferences
   - What was built / changed, and where it lives
   - Open questions and next steps (TODOs)
   - Anything they explicitly said "remember this"
   Ignore small talk, dead ends, and anything already saved.

2. **Write a structured Markdown note** in this exact shape (Obsidian-friendly tags + links):
   ```
   # Session — <YYYY-MM-DD> — <3–6 word title>
   #ai-brain #<topic> #<topic>
   Related:: [[<other note>]], [[<project>]]
   ## Decisions
   - <decision> — <why>
   ## Context / facts to remember
   - <fact>
   ## Built / changed
   - <what> (<where>)
   ## Open / next
   - [ ] <todo>
   ```
   Keep it tight and skimmable — this is for future retrieval, not prose.

3. **Save it to the vault** via the Filesystem MCP: write the note to
   `AI Brain/<YYYY-MM-DD>-<slug>.md`. If the `AI Brain/` folder doesn't exist yet, create it first.
   Append-only — never overwrite a past session's note.

4. **Link it in.** Add a one-line pointer to a `AI Brain/MOC.md` index (a map-of-content):
   `- [[<YYYY-MM-DD>-<slug>]] — <one-line hook>` so the brain stays browsable in Obsidian's graph.

5. Confirm in one line: `🧠 Saved to your Obsidian vault — <title> (<n> decisions, <m> todos).`

## At session start, or when the user references the past — RECALL

1. Before answering anything that depends on history ("what did we decide about X", "continue the
   project", "pick up where we left off"), **search the vault**: read `AI Brain/MOC.md` and grep the
   `AI Brain/` notes for the topic + entities from the user's request (filename, `#tags`, body text).
2. Open **only the relevant** notes — never load the whole vault. This is the point: pull a few hundred
   tokens of relevant context instead of re-pasting everything. Follow `[[wikilinks]]` to related notes.
3. Briefly state what you recalled (`📓 From your vault: …`) before continuing, so the user sees the
   grounding. If nothing relevant is found, say so and proceed fresh.

## Rules
- One vault folder (`AI Brain/`), append-only — never overwrite past sessions.
- Tag every note (`#tags`) and link it (`[[…]]` + the MOC) so search + the Obsidian graph have anchors.
- Recall is **retrieval, not reload**: fetch the minimum relevant notes. That's what keeps token cost
  low on long-running projects.
- Never invent memories. If the vault has no answer, say "not in memory yet."
- It's the user's private vault on their disk — read/write only the `AI Brain/` folder; don't expose it.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
