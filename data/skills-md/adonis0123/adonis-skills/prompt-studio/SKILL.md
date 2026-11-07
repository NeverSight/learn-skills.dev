---
name: prompt-studio
description: "Turn a one-line image or video request into a finished asset: route it to an image, a code-rendered Code Video or a Model Video, search many GitHub prompt libraries for proven image prompts, video-model prompts (Seedance, Kling, Veo, Hailuo/MiniMax, Wan, Grok Imagine) and code-video templates, show the best 5 with their samples, model, author and license, write a generation brief, hand it to an available channel (host tool, Codex/Grok CLI, API, Hyperframes), then check and log the result. Use whenever the user wants a cover, illustration, poster, thumbnail, infographic, animation, motion clip, AI video, or a better prompt for one, even if they only say 'make me an image'. Also for Chinese-language requests for WeChat covers, illustrations, still-to-motion clips, and image/video prompt optimization. Not for general chatbot or coding prompts, photo editing without generation, UI implementation, or slide decks."
metadata:
  author: adonis
---

# Prompt Studio

Take a short request, find the best proven starting point, make it fit the user, and hand a precise brief to a channel that can generate. Then verify the output and remember what worked. This skill never generates by itself.

Run the helper with `node <skill-dir>/scripts/studio.mjs <command>`; successful commands print JSON; no command prints plain-text usage. Failures may print stderr or a JSON `error` (for example `translate-to-english`) with a non-zero exit. Check the exit status and those fields, not only a `status` key. Terms such as Request Brief, Generation Brief, Channel and Style Pack are defined in `references/glossary.md`; read it if one is unclear.

## Workflow

Respect the requested stopping point: a plan, recommendation list or prompt-only request ends there, without generation. A prompt-only request (帮我找提示词 / 我自己去跑) ends with the adapted prompt in a copyable block, written in the language the target tool works best with (Chinese is fine for 即梦, Kling and Hailuo; English for Veo, Midjourney and most image models), the settings to pick in that tool (ratio, duration, model version), and its attribution line. Settings you could not check against the tool's docs are marked as such in that message ("时长上限未核实"); never tell the user to pick "the latest version" when the prompt was written for a specific one, and do not promise it works as is. “Just make it” skips candidate selection, not explicit no-generation instructions or spending/install approval.

Reply in the user's language. The Chinese lines in this file are examples, not fixed text: for an English request, write the chat in English, pass `"locale":"en"` to the gallery, and use "Pick this" / "pick N" where the examples say 选这个 / 选 N.

### 1. Session probe (once per session)

Run `studio.mjs session --project <dir>`. It replaces separate access, style-pack and channel probes, so you never ask the user what exists.

- On `anonymous`, show its `hint` once and do not repeat it.
- If a Style Pack is found, read its file and apply it to every brief. `stylePackText` on the session object is capped, so the file is the pack. If none is found, add no house style.
- Channels come from the same output (see `references/channels.md`).

### 2. Pick the output type

| The result must…                                                                                                     | Output type                       | Read                        |
| -------------------------------------------------------------------------------------------------------------------- | --------------------------------- | --------------------------- |
| Look right (illustration, scene, character, photo, decorative art)                                                   | Image                             | `references/image.md`       |
| Get text, numbers, data or structure exactly right (charts, labeled diagrams, storyboards, title motion, explainers) | Code Video, or a code-built still | `references/code-video.md`  |
| Move realistically (people, scenes, a product shot or teaser, a character from an image coming alive)                | Model Video                       | `references/model-video.md` |

- A poster or cover with a short slogan (up to about 12 Chinese characters or 6 English words) is an Image: GPT Image and Nano Banana render short quoted text well. Read every character in the result; switch to a code-built still (`code-video.md`) only when the text comes out wrong, or from the start for numbers, data, prices in a table or long copy.
- Ambiguous 动效 / 动起来 / "motionize this still" → Code Video by default: it is free and exact.
- Use Model Video only when the user asks for realistic motion or names a video model; its cost gate is in step 6.
- Several outputs ("cover plus a 5-second motion version"): plan them to share one look, and make the still first.

### 3. Fast path: assume, then search in the same message

Speed matters more than a perfect Request Brief: a wrong default costs one reply, a wasted turn costs more. Do not spend a whole turn on questions only.

- Fill missing gaps (at most 3: use and ratio, subject, style or mood) with defaults and search within the output type chosen above in the same turn. Mention the defaults in one short line, not a list. Image-library `recommend` is only for image candidates, not exact-data stills or video plans.
- No subject at all (推荐几个小红书封面提示词): pick candidates that differ in subject type (person, food, outfit, illustration), fill each prompt's placeholders with that subject, and end with one line asking what the post is about so the next search can be specific.
- Skip any gap the request already answers. When improving a supplied prompt, revise it directly; search only if a missing technique needs a reference.
- For an asset request, pause for the candidate choice. If the user said 直接出 / just make it, take the default candidate and continue.
- Interview first instead when the user asks to discuss or be grilled (先聊聊 / 问我几个问题 / grill), or the asset carries brand or taste weight (a series, a brand cover, a campaign key visual) and the request names no style. Ask in rounds like the `grilling` skill: number each question, give your recommended answer, ask only questions whose prerequisites are settled, at most 2 rounds. Look facts up yourself (Style Pack, existing covers in the project) instead of asking. Then search.

### 4. Recommend (5 candidates)

One command searches many GitHub prompt libraries for all three output types: `studio.mjs recommend "<English keywords>" --kind image|video|code-video --limit 8 --project <dir>`. Same `--project` as session, brief, log and rate, so saved scores affect this ranking. Sources, licenses and model names are in `references/sources.md`.

- Every kind:
  - Translate CJK ideas into English keywords first; a CJK-only query returns `error: translate-to-english` and does not search. When the subject is culturally Chinese (汉服, 春节, 水墨), add one Chinese direction as well: some libraries are written in Chinese.
  - Put the subject in every direction (`cute kitten birthday cake | kitten party hat | pastel kawaii cat`, not `cute | party | pastel`): words shared by all directions count as the subject, and results that miss it rank lower. Use `--subject "<words>"` when the directions cannot all contain it.
  - Add `--model <key>` only when the user named a model (即梦 → `seedance`, 可灵 → `kling`, 海螺 → `hailuo`; full table in `sources.md`) or the channel is already fixed. Candidates flagged `modelMismatch` have samples from another model: say so in their fit line.
  - `refreshing` sources are fine: their cached data was used. Only when `downloading` is not empty and fewer than 5 results came back, say once that more libraries are still downloading and rerun the same command with `--wait-sec 30`. Do not rerun just to wait.
  - Read `directions`: a direction with 0 hits found nothing, so replace it with a more visual phrase instead of repeating it. When results come back but miss the request (only vlogs for a product shot), search once more with different visual words, then go with the best of both; do not search a third time.
  - Write a Chinese direction as 2–4 short words separated by spaces (`春节 红色 海报`, 2 hits in tests), not one long run (`春节红色促销海报`, 0 hits): a long run must match almost as a whole.
  - `referenceInputs > 0` means the prompt needs that many user images (`referenceNote` says which). Without them, skip the candidate or say on its fit line that it will be rewritten as text-only.
- Model Video: `--kind video`. Describe the shot, not the topic (`latte art pour slow motion | barista hands close-up`). When the user supplies the image to animate, add `--mode image-to-video`: it prefers short single-shot motion prompts over multi-shot scripts. Results carry `videos` (playable clips) and `durationSec`; an entry whose own library keeps no clip borrows the one another library keeps for the same X post (`videoFrom` names that library), and a card left without a clip links to the post on X or YouTube; library clips are often 15–30 s multi-shot pieces, so the brief keeps their structure and cuts it to the requested length.
- Code Video: `--kind code-video` returns Hyperframes templates (empty `content`; the name goes to `npx hyperframes add`) and code videos other people made with an agent, with clips. Describe the motion (`animated bar chart growth | kinetic typography title`).
- Images: also pass `--use cover|poster|illustration|infographic|avatar|thumbnail|comic|product|game|app`; it scopes the largest library's categories.
  - Describe the picture, not the topic. The library holds visual prompts, so `isometric tech illustration` finds tech art while `MCP protocol` finds nothing. Send 2–3 visual directions (never more than 3) in one call separated by `|` (for example `isometric tech illustration | glowing network nodes | 3d cute robot mascot`); each result keeps its best direction and lists the words it `matched`. Ranking weights rare words above generic ones (`ai`, `tech`) and rewards matching more of a direction.
  - Covers use `--use cover`, never `social-media-post`. For `cover` / `thumbnail`, put the subject in the keywords (for example `MCP connector AI tools`) and omit the word `cover`: the flag already scopes the category, and the word mostly matches fashion magazines.
  - Read `cacheNote`: a skipped large category was not searched. Add `--allow-large` only when that category is where the request belongs (product shots, social posts).
- Look at the samples of the returned 8 only (images, or video posters; open a clip only when two posters look alike), not 30, and keep the 5 that differ most in look. When the user asks for more, rerun with `--limit 12` and show up to 9 (the page maps number keys 1–9); when fewer than 5 differ in look, show only those. Resolve flagged placeholders from the request or safe defaults; drop a candidate only when essential inputs remain missing. Drop `needReferenceImages` candidates when suitable user references are unavailable.
- Do not `show` or rewrite candidates before the pick: the gallery already carries the full prompt. After the pick, `show` the chosen id only.
- Model-specific prompt rules stay in `references/model-video.md` and `references/code-video.md`; read the one for the chosen kind before writing the brief.
- If nothing in those results fits and `access.onlineSearch` is true, `studio.mjs github "<topic> prompts"` finds libraries; `studio.mjs sources add <owner/repo> --kind <kind>` plugs one into search after you checked its samples and license (`sources.md`). When `onlineSearch` is false, skip `github`: the anonymous hint already explained it, and the command returns no repositories.

Show the candidates as a gallery page, because a terminal cannot render the sample images. The user picks there with one click. Keep commands, JSON and tool status out of the chat unless the user asks to see them; then list every command in order, including the `recommend` and `gallery` already run.

1. Build it: `studio.mjs gallery --project <dir> --serve --json '{"runId":"...","title":"<short title in the user's language>","request":"<user request>","locale":"zh|en (the user's language)","targetModel":"<model you will use, if known>","targetRatio":"16:9","targetDurationSec":<video length>,"candidates":[{"id":"<id>","name":"<2–6 word name, user language>","fit":"<one line, user language>","ratio":"...","default":true}]}'`. The script fills in sample images or clips, the sample's model, author and original post, the full prompt, source and license, and writes `<records>/gallery/<runId>.html`. A non-empty `missing` (exit code 1, no page written) means an id was not in the library: fix it and rerun.
2. `--serve` hosts the page on 127.0.0.1, prints `url` first, then waits for the user's click and prints `{"pick":{"id","number","edited","prompt"}}`. It prints two JSON objects in a row (parse them one at a time). Where the host wakes you when a background command ends (Claude Code: `run_in_background`; Grok: a background task), run it in the background, read the `url` from its output, open it (`open <url>` where available) and end the turn with the step 3 list. Where it does not (Codex: a background shell never reports back, so a click would sit unseen and the user would have to type the number), keep the turn open instead: send the step 3 list with the `url` as a progress message first, then run `--serve` in the foreground (on Codex, keep polling the running command until it prints the pick) and continue from the pick in the same turn. Never end a turn while `--serve` waits on a host that cannot wake you; if you must, say in that message to reply with the number after picking. The user clicks 选这个 (3-second undo) or presses a number key; an edited prompt comes back in `prompt` and replaces the library text. `{"pick":{"status":"timeout"}}` with exit code 3 after 30 minutes is not a failure, even where the host marks the task failed; it means fall back to a chat reply: say so in one line and repeat the numbered list from step 3, so the message stands on its own. Without a background shell, drop `--serve` and open the file: 选这个 then copies 「选 N」 (plus any edited prompt) for the user to paste, so still point them to it.
3. Always also list the candidates in the chat, even though the page has them, in this shape:

   ```text
   1. 等距科技插画（推荐）：把 AI 和工具的连接画成一张架构图
   2. 霓虹网络节点：暗色、科技感强
   3. 3D 可爱机器人：轻松口吻
   候选页：<url> ，点「选这个」或直接回复编号；想改提示词就在页面框里改。
   ```

   If the page cannot be opened, add each prompt (first ~300 characters), sample image URL, source and license under its line.

4. A chat reply (编号, or 编号 plus an edited prompt) counts the same as a click.

Mark one default: the best fit among candidates whose `evidence` is `clip` or `still`. A candidate with `evidence: "none"` may be shown but is the default only when every candidate has none; then say in one line that this is a text-only choice, judged by the prompt and its fit line. Fewer candidates with real samples beat more where some are blank. If a sample cannot be opened, mark visual fit `UNVERIFIED`. Library ids from any kind work in the gallery. Only a candidate that is not in any library (your own plan) needs `content`, `title`, `images` or `videos`, `source` and `license` filled in yourself.

### 5. Write the Generation Brief

- Start from the user's edited `prompt` when the pick has `edited: true`; otherwise from the library prompt. Rewrite it for the user's content: keep its structure and technique, replace its subject. Resolve every template placeholder, including `{argument ...}` and `{style=...}`; literal JSON object braces are valid and need not be removed.
- Apply the Style Pack, then adapt to the target model with the table in `references/image.md` (or the video reference).
- Scaffold with `studio.mjs brief --project <dir> --json '{"runId":"...","promptId":<id>,"title":"...","source":"...","license":"...","channel":"...","model":"...","outputPath":"...","size":"WxH","content":"...","styleNotes":"..."}'`. It writes a provenance file at `<records>/briefs/<runId>.md` (default records directory `<project>/.prompt-studio`, override `PROMPT_STUDIO_RECORDS`). The channel runs `content`, not this file; the handoff shape is in `references/channels.md`. If the user asked for a brief path, copy the finished provenance file there too. `outputPath` is the generated asset, not the brief.
- Credit source and license in the brief; CC BY 4.0 requires attribution when shared.
- Commercial use (ads, promotions, a product or brand asset): prefer candidates with a declared license as the default. When the best look has no license, keep it but say on its fit line that its technique is reused and the wording rewritten, and rewrite it that way. When `brief` returns `attributionRequired: "unknown"`, tell the user in one line: "this prompt's license is not stated; credit the source if you publish the prompt itself".
- Code Video: you are the channel. Write the brief first (it records template, source and license), then build and render from it; there is no handoff step.

### 6. Hand off to a Channel

Follow `references/channels.md` for priority (user-named → Style Pack → host → list the others) and invocation.

- Model Video costs money: before the first paid step of the whole path, list every step (first-frame images, preview clip, final clip) with channel, duration, resolution and estimated cost, then wait for one yes that covers the preview path. List costs in separate lines: media generation (a subscription channel such as Grok or Codex spends plan quota; an API bills per second), the channel's own agent call (Grok and Codex CLIs report it, about $0.05 per call in tests), and anything unknown, marked unknown. Never promise that nothing is charged. After the run, report what the channel itself reported (for example `total_cost_usd`), as reported, not as a verified bill.
- Images: ask for 2–4 variants when supported. Before the first image call, say in one line how many images, on which channel, and what that spends (a subscription CLI such as Codex or Grok uses plan quota per image, plus its agent call; an API bills per image); no separate yes is needed for images unless the user set a budget. Never write that something costs nothing extra.
- On a moderation block, stop and tell the user; do not reword around the filter.
- Named real people need the user's own reference photo.

### 7. Check, refine, record

- Images: look at every variant and pick the best. Covers also run `studio.mjs cover-check <files> --title "..." --size WxH` and look at the previews. Exact size: `studio.mjs check-image <file> --size WxH`.
- Code Video and Model Video: run the gates in their references.
- Feedback ("warmer background") changes only the sentences that cover it; prefer an edit tool over regenerating.
- Log every generation: `studio.mjs log --project <dir> --json '{"runId":"...","promptId":<id>,"channel":"...","model":"...","output":"<path>","brief":"<path>","status":"selected|rejected","note":"why"}'`. Scores: `studio.mjs rate <runId> <1-5> --project <dir>`; 4–5 raises that prompt in later searches.

## Resources from elsewhere

Handled by risk; details in `references/delivery.md`. Shipped text is used directly; fetched library data, templates and other skills' text are kept current and confirmed when changed (`studio.mjs source <url>`); never run scripts from fetched content; installing another skill always needs the user's yes.

## Boundaries

- Never print, store or ask for tokens or API keys; use variable names only.
- No installs, writes into the user's project, or Model Video spend without the confirmations above. Briefs and Run Records in the records directory need none.
- Do not claim a result is done before it passed its quality gate; if it cannot be made right, say what is wrong.
