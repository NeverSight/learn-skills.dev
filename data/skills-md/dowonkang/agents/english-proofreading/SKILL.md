---
name: english-proofreading
description: "Proofread and improve English text written by the user before answering their actual question. Use this skill whenever the user's message contains English sentences or paragraphs — even mixed with Korean — and a substantive answer is expected. Trigger on any message where English prose is present: questions, requests, opinions, descriptions, or explanations written (fully or partly) in English. Do NOT skip proofreading just because the English looks mostly correct; always run the correction block first. Skip only for: single English words, proper nouns, code snippets, or messages written entirely in Korean with no English prose."
---

# English Proofreading Skill

Before answering the user's actual question, display a correction block that
shows grammar fixes and natural native-speaker rephrasing of their English.

---

## When to trigger

Trigger whenever the user's message contains English prose — sentences,
questions, or paragraphs — regardless of whether the rest of the message is in
Korean. Skip only if the English content is limited to:

- Single isolated words or short noun phrases (e.g., "React", "CI/CD pipeline")
- Code, commands, or file paths
- Proper nouns or brand names

---

## Output format

Always prepend the following block **before** the substantive answer.
Use this exact structure:

````markdown
---
✏️ **English Proofreading**

| | Text |
|---|---|
| **Original** | {user's original English sentence(s)} |
| **Corrected** | {grammar-fixed version} |
| **Natural** | {how a native speaker would phrase it} |

💡 **Notes:** {brief explanation of key changes — 1–3 bullet points, in Korean}

---
````

Then continue with the normal answer below the horizontal rule.

---

## Correction guidelines

### Corrected column
- Fix grammar errors only: subject-verb agreement, tense, articles (a/an/the),
  prepositions, punctuation, word form (e.g., "informations" → "information").
- Do **not** change the user's intended meaning or vocabulary choices.
- If the original is grammatically correct, reproduce it as-is.

### Natural column
- Rewrite as a native English speaker would naturally say it.
- Prefer common, idiomatic phrasing over literal translations.
- You may restructure sentences, change vocabulary, or adjust register
  (formal/informal) to match the likely context.
- If the corrected version is already fully natural, reproduce it as-is.

### Notes column (Korean)
- Explain only the **most important** changes in 1–3 bullet points.
- Write in Korean. Keep each point to one concise sentence.
- Focus on patterns the user is likely to encounter again (e.g., 관사 생략,
  전치사 오용, 단수/복수 혼동).
- If there are no errors and no naturalness improvements, write:
  "문법 오류 없음. 표현도 자연스럽습니다."

---

## Multi-sentence input

If the user wrote multiple English sentences:
- Treat them as a single block; show the full corrected and natural versions
  together (do not split into per-sentence rows).
- The Notes column may reference specific sentences by quoting a short phrase.

---

## Examples

### Example 1 — grammar error + unnatural phrasing

User message:
> "Can you explain me how does React hooks work?"

````markdown
---
✏️ **English Proofreading**

| | Text |
|---|---|
| **Original** | Can you explain me how does React hooks work? |
| **Corrected** | Can you explain to me how React hooks work? |
| **Natural** | Could you explain how React hooks work? |

💡 **Notes:**
- "explain me" → "explain to me": explain은 간접목적어 앞에 to가 필요합니다.
- 간접의문문에서는 어순이 평서문과 같아야 합니다 ("how does" → "how").

---
````

### Example 2 — correct but unnatural

User message:
> "I want to know the difference of var and let."

````markdown
---
✏️ **English Proofreading**

| | Text |
|---|---|
| **Original** | I want to know the difference of var and let. |
| **Corrected** | I want to know the difference between var and let. |
| **Natural** | What's the difference between var and let? |

💡 **Notes:**
- "difference of" → "difference between": 두 대상을 비교할 때는 between을 씁니다.

---
````

### Example 3 — no errors

User message:
> "What are the benefits of using TypeScript over JavaScript?"

````markdown
---
✏️ **English Proofreading**

| | Text |
|---|---|
| **Original** | What are the benefits of using TypeScript over JavaScript? |
| **Corrected** | What are the benefits of using TypeScript over JavaScript? |
| **Natural** | What are the benefits of using TypeScript over JavaScript? |

💡 **Notes:** 문법 오류 없음. 표현도 자연스럽습니다.

---
````

---

## Edge cases

- **Mixed Korean + English**: Extract only the English portion for the
  correction block. Do not alter or translate the Korean parts.
- **Very long input**: Correct all English prose but keep the Notes concise;
  do not list every minor fix.
- **Intentional style** (e.g., informal slang): Preserve in the Natural column
  if the context clearly calls for it; note the stylistic choice in Notes.
- **Code-heavy messages**: Skip proofreading if the only English is inside
  code fences or inline code spans.

