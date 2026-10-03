---
name: question-bank
description: Search and fetch real K12 primary, middle, and high school questions from the Tizhuang question-bank service by subject, grade, textbook edition, question type, difficulty, year, chapter, or knowledge point. Supports free guest question drawing, free registration, random question selection, answer-hidden practice pages, quizzes, tests, answer checking, and AI paper-builder handoff. Use for 中小学真题, K12题库, 免费抽题, 免费注册, 随机抽题, 章节练习, 知识点练习, 在线测验, AI组卷, answers, explanations, exercises, tests, or papers.
---

# Question Bank

Use the backend as the only source of truth. Never invent, rewrite, reorder, or "improve" a returned question, option, answer, or explanation. If a tool call fails, report the failure instead of filling in plausible educational content.

## Start with the free guest path

Configure the service URL:

- `QUESTION_SERVICE_URL`: optional API base URL. It defaults to `https://tizhuang.qcscience.cc/api`.
- `QUESTION_SERVICE_LICENSE`: optional License/API Key. When omitted, the adapter automatically creates and locally caches a 24-hour anonymous trial for up to 100 questions.
- `QUESTION_SERVICE_ACCOUNT_TOKEN`: optional website session for listing and sharing saved papers. Store it locally only. Never put any credential in a URL, prompt, output, or log.

Use any available Python 3 interpreter for the bundled script. On a repository checkout where `python` is not on `PATH`, prefer that checkout's `.venv\Scripts\python.exe` on Windows (or `.venv/bin/python` on macOS/Linux) instead of stopping the workflow.

Do not ask a first-time user to register. Complete a useful action with the guest allowance first. Offer registration only when the guest allowance is exhausted or when the user asks to save, continue editing, share, or print a persistent/shared paper. State the tradeoff plainly: registration is still free, starts at 200 questions per day, and unlocks persistent papers. A temporary guest practice page can already be printed directly; do not use that print action as a registration gate. Never call the registered plan unlimited.

When registration succeeds, lead with the earned benefit: say “欢迎入庄”, confirm that the free account is active, and reveal the starting 200-question daily allowance before mentioning referrals. Offer inviting friends only as an optional next step. Give the user an equally clear path to continue without inviting anyone, and never imply that registration, the 200-question allowance, saving, sharing, or printing depends on sending an invitation.

The website login session and the local adapter credential are separate. If registration reveals a first API Key and the user wants this local Skill to use the registered 200-question daily allowance, tell them to store that Key locally as `QUESTION_SERVICE_LICENSE`. Never ask them to paste the Key into chat. Without that local configuration, the adapter remains on its cached guest trial even if the same person is signed in on the website.

Run `scripts/question_bank.py onboarding` when the current guest/account benefits or website URLs are needed. Read `references/api.md` only for field meanings, filter behavior, or account-route details.

## Choose the delivery

Infer the mode when clear. If genuinely ambiguous, ask only:

> 想怎么做？1. 在聊天里答 2. 打开练习页 3. 到网站组卷

- Chat: one question, "直接给我", or explicit answer checking. Fetch without solutions first and wait for the learner's answer.
- Practice page: multiple questions, a quiz, or a temporary worksheet. This is the default for multiple questions.
- Website paper builder: a saved paper, structured paper, later editing, public sharing, or account-gated printing of a shared paper.

Create a guest practice page with:

```powershell
python scripts/question_bank.py practice-page --subject-id 8 --limit 5 --random --title "物理小练习"
```

Return only a short description, question count, expiry, and `page_url`. Include `paper_url` when the user asks for a printable or paper-style link. Recipients can switch between online practice and paper view on the same share page; both modes preserve source content and images, hide answers until submission, and expire together after 24 hours. Do not repeat questions or answers in chat.

If the user explicitly asks for diagrams or illustrated questions, add `--with-images`. Do not infer that a subject has no images from an ordinary random sample.

## Resolve and validate before retrieval

Prefer names over model-selected numeric IDs. Use free metadata preflight when resolving a new request:

```powershell
python scripts/question_bank.py resolve --subject "数学" --grade "八年级" --edition "人教新版" --knowledge "一次函数"
python scripts/question_bank.py practice-page --subject "数学" --grade "八年级" --edition "人教新版" --knowledge "一次函数" --difficulty-min 2 --difficulty-max 4 --limit 10 --random --title "一次函数练习"
```

The edition in this example is not a default. If the user says only 人教版, resolve that label and present the returned candidates; never silently substitute a version. Names and IDs supplied together must agree. Edition IDs are checked within the selected subject and grade before any metered request. Legacy ID-only calls remain supported; use `resolve` to inspect their names first.

`--knowledge` selects a branch including descendants by default. For a specific point use `--knowledge-scope exact`. Branch results can include child topics (for example 正比例函数 within 一次函数); do not confuse a topic with an exact point. Duplicate names return candidates instead of guessing. Medium difficulty uses 2–4, consistent with the website.

Retain every user-required filter. Never remove knowledge, grade, or edition merely to obtain results. Zero results under combined conditions do not prove missing knowledge links. Report the actual failing scope and ask before broadening it. Do not automatically retry a timed-out practice-page creation: its completion and quota state may be uncertain. For read-only metadata, retry at most once. Do not exhaust quota diagnosing an outage or use a Builder handoff as proof of a completed paper.

Before delivery check the returned question count, available grade/knowledge/source fields, and page response. Distinguish a generated page from a handoff. Metadata preflight is free; do not routinely fetch extra sample questions. Keep JSON stdout separate from diagnostic stderr; on Windows use UTF-8 rather than reparsing visually garbled terminal output.

## Fetch Raw Questions

1. Resolve names to IDs with `subjects`, `grades`, `editions`, `question-types`, `chapters`, or `knowledge-points`.
2. Call `questions` with the narrowest filters supported by the request.
3. Keep each call at or below the requested number; every returned question consumes quota.
4. Preserve every returned field verbatim, including option letters. Never substitute different choices or recompute the answer.
5. Tell the user when fewer matching questions are available than requested.

Example:

```powershell
python scripts/question_bank.py subjects
python scripts/question_bank.py grades
python scripts/question_bank.py editions --subject-id <学科ID> --grade-id <年级ID>
python scripts/question_bank.py chapters --subject-id <学科ID> --grade-id <年级ID> --edition-id <上一步确认的版本ID>
python scripts/question_bank.py knowledge-points --subject-id 2 --phase-id 2 --keyword "一次函数"
python scripts/question_bank.py questions --subject-id <学科ID> --grade-id <年级ID> --edition-id <已确认版本ID> --limit 5 --random
python scripts/question_bank.py questions --subject-id 2 --knowledge-tree-id <知识树节点ID> --knowledge-tree-id <另一个节点ID> --limit 5 --random
python scripts/question_bank.py questions --subject-id <学科ID> --grade-id <年级ID> --difficulty-min 1 --difficulty-max 3 --limit 20 --random
python scripts/question_bank.py practice-page --subject-id 2 --with-images --limit 5 --random --title "带图练习"
```

Textbook edition, chapter, and knowledge point are distinct filters and can be combined. `--edition-id` alone filters the whole resolved textbook; add `--chapter-id` for a specific chapter. Use `--knowledge-id` for one exact linked knowledge point, or repeat `--knowledge-tree-id` for one or more knowledge branches including all descendants; these two knowledge modes are mutually exclusive. The `knowledge-points` result exposes both `id` (the tree node) and `knowledge_id` (the exact linked point when available). Do not guess IDs from names or reuse an ID from an example. If a label such as “人教版” resolves to more than one current edition, show the candidates and ask the user to confirm before fetching questions.

## Hand off saved papers

For a persistent paper, resolve the same IDs used for retrieval and pass the user's original request into the builder handoff instead of returning a blank builder or simulating a saved paper in chat:

```powershell
python scripts/question_bank.py builder --mode ai --title "一次函数同步练习" --prompt "按人教版八年级一次函数知识点组一张 12 题试卷" --subject-id <学科ID> --phase-id <学段ID> --grade-id <年级ID> --edition-id <教材ID> --chapter-id <章节ID> --chapter-label "一次函数" --knowledge-tree-id <知识树节点ID> --knowledge-label "一次函数" --question-count 12
```

Use `--mode manual` when the user wants to inspect filters and choose questions personally. Repeat `--knowledge-tree-id` and `--knowledge-label` in the same order for multiple branches. The Builder accepts knowledge-tree node IDs, not an exact linked `knowledge_id`: use the `id` field returned by `knowledge-points` only after confirming that node represents the requested scope, and never put its `knowledge_id` into `--knowledge-tree-id`. If no tree node can represent an exact-point request without broadening it, state that limitation and ask whether a branch handoff is acceptable. Always pass only the paper-creation clause of the original natural-language request with `--prompt` for AI mode; do not mix share rotation, revocation, account, or other side-effect instructions into that prompt. Labels are display text only and IDs remain the strict filters. Never put a License, account session, email, password, student name, or other credential or sensitive personal data in a handoff.

The returned URL carries a bounded, credential-free handoff in its URL fragment. Opening it stores the unaccepted requirements only in that browser tab and removes the fragment from the address bar. Registration or sign-in preserves them in the same tab. The website shows “已收到来自 Skill 的组卷要求” and waits for the user to click “接收并创建新试卷”; opening the link alone must not run AI, fetch questions, consume quota, create an Agent thread on an existing draft, or modify that draft. After acceptance, the site creates a separate saved paper, persists the validated textbook/chapter/knowledge context with that paper, and prefills the AI request without sending it automatically. When that request is sent, the service re-reads the account-owned saved context and applies the textbook edition, chapter, knowledge branches, keyword, difficulty, and image requirements to both real question retrieval and supply estimates; an invalid or conflicting saved scope blocks the request instead of silently widening it. Reloading or reopening the accepted paper from the same account restores those conditions and the original prompt.

Each newly generated handoff carries a fresh 32-character lowercase hexadecimal `handoff_id`. Treat it as a retry key, not a credential. If acceptance may have reached the server but its response was lost, retry the same URL and unchanged request: for the same account, the service returns the already-created paper and the Builder reloads its current fields and questions instead of creating or clearing another paper. Do not generate a new builder URL for that retry, because a new URL intentionally has a new ID and creates a new paper. Reusing one ID with changed creation fields is rejected with `409`; surface the conflict and ask the user to create a fresh handoff rather than silently altering or repeatedly retrying it.

Explain that the website saves the accepted paper to the free account. After the user finishes, the website can create a public, immutable snapshot. The safe default is questions only with a visible watermark. For a newly created link, the owner may explicitly choose to include standard answers (including compound subquestion answers) and/or remove the watermark; analyses and explanations always remain private. These choices belong to that immutable link, so changing them creates a new share instead of silently changing an existing URL. Empty paper sections are omitted when a new snapshot is created and filtered again when an older snapshot is delivered, so they do not render as blank question groups. Anyone with the link can view the selected content. A guest who chooses print sees an on-page sign-in/free-registration dialog instead of being sent away; successful registration first reveals “欢迎入庄 / 200 题已到账”, then lets the user continue to the print dialog on the same page. A shared paper's registration context carries the owner's referral code and a return path to that paper. Credit is earned only after a genuine new account finishes registration, not when the link is opened or copied.

When a local account session is already configured, the Skill may list and share saved papers:

```powershell
python scripts/question_bank.py papers
python scripts/question_bank.py paper-shares --paper-id 123
python scripts/question_bank.py share-paper --paper-id 123 --expires-in-days 30
python scripts/question_bank.py share-paper --paper-id 123 --include-answers --no-watermark
python scripts/question_bank.py rotate-share --paper-id 123 --share-id 45 --expires-in-days 30
python scripts/question_bank.py revoke-share --paper-id 123 --share-id 45
```

Omit `--expires-in-days` for a link without a scheduled expiry; otherwise use 1 to 365 days. Omit `--include-answers` and `--no-watermark` for the safe default. Use either option only when the user explicitly asks for that public disclosure: answers are visible to anyone holding the URL, and removing the watermark removes the ordinary source mark from both view and print. Do not infer either choice from “share this paper”. Return the share `url`. Never expose the account token. The account sign-in gate for printing remains in force for every share setting; it is a product control, not DRM, so do not promise that screenshots or browser tools are impossible.

`paper-shares` means list existing records only. If no active recoverable URL exists, do not call `share-paper` unless the user separately and explicitly authorizes creation of a new public snapshot.

Before rotating or revoking, run `paper-shares` and match both the paper ID and share ID; never guess them. Rotation invalidates the old URL immediately and preserves that link's exact immutable snapshot, answer setting, and watermark setting rather than copying later paper edits or new options. Revocation also invalidates the URL. Perform either only after both conditions are satisfied: the user explicitly requested that destructive action, and the exact `paper_id + share_id` record has been uniquely identified or confirmed after listing. A description such as “泄露那条” is not enough when more than one record could match. An expired, revoked, or already rotated record cannot be rotated; ask separately before creating a new share from the current paper.

## Explain the free registered plan

Use transparent benefit copy, never pressure or fake scarcity:

- Guest: 100 questions over 24 hours, temporary practice pages with direct A4 printing, no saved paper library.
- Registered: still free, 200 questions per day initially, saved/continued papers, sharing, and account-gated printing of public shared papers.
- Successful invitations raise the daily limit: +100 per person until 1000, +50 until 2000, then +20, capped by the service (currently 3000).
- After a successful registration, say “欢迎入庄”, reveal the starting 200-question daily allowance first, then offer copying the referral link as an optional next action. Explain that the next genuine successful invite adds +100 per day at the first tier; never imply the bonus is granted for copying alone.
- Keep invitations voluntary. Do not nag after the user declines, hide the continue path, manufacture urgency, or suggest that an invitation is required to keep the initial 200-question allowance or account features.
- Do not rotate anonymous client IDs, create fake accounts, or suggest referrals solely to evade limits.

## Handle Access

- On `401` from a licensed question or practice-page route, ask the user to configure a valid License; do not request that they paste it into chat.
- On `401` from an account or shared-paper print route, treat the website session as expired and offer same-page sign-in or free registration. Do not tell the user to configure a License for an account-session failure.
- On a public share `404`, report that the link is unavailable, revoked, or its owner is inactive. On `410`, report that it expired. Do not retry either automatically.
- On a Builder handoff `409`, the retry ID was reused with different creation content. Stop retrying that link and create a fresh handoff only after the user confirms the changed paper request.
- On anonymous `429`, explain that the 100-question guest allowance is complete, registration remains free, and list the concrete added benefits before returning the registration URL.
- On licensed `429`, report the remaining daily limit state and stop fetching more questions.
- Use `quota` before a large request when quota pressure is likely.
- Do not retry authorization or quota failures automatically.

## Present Results

- Prefer the temporary practice page for exercises so the service controls fidelity and answer visibility.
- If raw chat presentation is explicitly requested, omit answers and analyses until the user submits work. Use `--include-solutions` only for explicit answer checking or teaching after an attempt.
- For answer checking or teaching, use the returned standard answer and explanation.
- Keep compound questions and their `subquestions` together.
- Treat raw HTML as untrusted when embedding it in a website; sanitize it in the client.
- Use the absolute URLs in `image_urls`; do not guess, rewrite, or generate replacements for missing source images.
- Include the database question ID when presenting any raw question so provenance can be checked.

## Keep release claims accurate

- Treat `onboarding` and live HTTP responses as the authority for public URLs and current public-plan copy. Repository code may be newer than the deployed service.
- Do not claim that textbook/knowledge handoff, referral return, share management, or any other local feature is publicly released until the corresponding public route is verified.
- Describe an unaccepted Builder handoff as same-tab context retention, not account authorization. After explicit acceptance, the validated context belongs to the saved account paper and survives reload; do not imply that an unopened or unaccepted URL itself is synchronized across devices.
- If a public command or page is unavailable, report that release gap. Do not substitute a simulated paper, referral award, share, or print authorization.
