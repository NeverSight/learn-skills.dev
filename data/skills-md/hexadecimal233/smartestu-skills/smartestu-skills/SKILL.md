---
name: smartestu-skills
description: "Work with smartestu.cn (数你最灵) from an agent. Read a student's courses, 作业 list, 作业 detail with every exercise, 批改结果, and submit or resubmit answers through the documented HTTP API. Use when the user mentions smartestu, 数你最灵, 作业, 交卷, 待批改, 习题, 错题本, 签到, 学号登录, or asks to inspect assignment data captured from that site."
metadata:
  version: "2026.10.27"
  source: HAR captures of https://smartestu.cn/assignment taken 2026-10-27
---

# smartestu.cn API notes

Reconstructed from two browser HAR captures of `https://smartestu.cn/assignment` (2026-10-27) plus the JavaScript bundles that page loads. Everything below marked "verified" was observed on the wire; everything else came from reading the client code and is labeled as such.

| File | Content |
| --- | --- |
| `references/math-rendering.md` | Delimiters and KaTeX settings the platform uses, MathJax and typst recipes with verified commands, LaTeX to typst conversion table |
| `references/workflows.md` | Trigger phrase to call sequence, with preconditions, refusals, and a verified/inferred/unknown tag per step |
| `references/student-homework-flow.md` | Request and response bodies for the student assignment flow: captured bodies verbatim, client-derived bodies quoted from the bundle |
| `references/data-models.md` | Homework object, exercise object, question structure, every status enum |
| `references/api-inventory.md` | All 401 endpoint paths grouped by area |
| `references/capture-provenance.md` | Source files, what each capture contains, open questions |
| `scripts/smartestu-api.mjs` | Credential-aware HTTP client, read-only by default |
| `scripts/render-math.sh` | Render one Chinese-plus-math line to PNG or SVG with typst |

## Start here

One check per session, before touching the API:

```bash
node scripts/smartestu-api.mjs doctor
```

It reports node, credentials file and its permissions, cookie presence, a live access-cookie mint with role and masked school id, whether `csrfToken` and `sessionContext` arrived, the course list, the portal pending count, and typst availability. `fail` lines block the work; `warn` lines (no typst, empty course list, unreachable network) get reported while the read flows still run. Exit 0 means ready.

A `fail` on `account` means the refresh cookie is dead, so ask for a fresh copy. A `fail` on `creds file` with `cookie` set means the inline cookie works but nothing is stored yet; run `session` once to persist it.

## Credentials

Two HttpOnly cookies, issued by `https://smartestu.cn`:

| Cookie | Lifetime | Role |
| --- | --- | --- |
| `__Host-auth_refresh_v1` | long | buys access cookies |
| `__Host-auth_access_v1` | 15 minutes, JWT | authenticates every other call |

`GET /api/auth/session` with the refresh cookie answers 200, sets a fresh access cookie, and returns `csrfToken` plus `sessionContext` in the body. Calls then carry the access cookie and three headers:

```
x-auth-protocol: cookie-v1
x-csrf-token: <csrfToken>
x-session-context: <sessionContext>
```

Verified live on 2026-10-28: refresh cookie from Safari, access cookie minted, `role: STUDENT`, `schoolUserId: <school id>-*`.

`scripts/smartestu-api.mjs` performs the exchange itself, keeps `~/.config/smartestu/creds.json` at mode 600, and re-mints when a call answers 401. Only the refresh cookie has to be supplied:

```bash
SMARTESTU_REFRESH_COOKIE="__Host-auth_refresh_v1=..." node scripts/smartestu-api.mjs session
```

Login at this deployment:

```json
{"emailLoginEnabled": false, "schoolUserIdLoginEnabled": true, "registrationEnabled": true, "socialLoginEnabled": false}
```

School ID plus password works. The login body was not captured; reuse a browser session instead of rebuilding the exchange.

## Read recipes

```bash
# who am I
curl -s https://smartestu.cn/api/auth/session -H "x-auth-protocol: cookie-v1" \
  -H "x-csrf-token: $CSRF" -H "x-session-context: $CTX" -H "Cookie: $COOKIE"

# courses the student is enrolled in
curl -s -X POST https://smartestu.cn/api/homework/student/course/query \
  -H 'content-type: application/json' ... -d '{}'

# 作业 list, grouped by course, paginated
curl -s -X POST https://smartestu.cn/api/homework/student/mark/queryHomeworks \
  -H 'content-type: application/json' ... \
  -d '{"courseIds":[7283],"scene":"homework","pageSize":20,"pageNo":1}'

# one 作业 with every exercise, 批改 state, and the reference answer where released
curl -s -X POST https://smartestu.cn/api/homework/student/mark/queryExercisesByHomeworkId \
  -H 'content-type: application/json' ... -d '{"homeworkId":42863}'
```

`scene` accepts `homework`, `online_exam`, and `preview`. The client issues one query per scene and merges the results. `courseIds` must list real course ids: an empty array returns an empty list even when the student has open homework.

Helper that carries the headers and the write guard:

```bash
node scripts/smartestu-api.mjs doctor
node scripts/smartestu-api.mjs session
node scripts/smartestu-api.mjs courses
node scripts/smartestu-api.mjs pending
node scripts/smartestu-api.mjs homeworks --scene homework --page 1
node scripts/smartestu-api.mjs homework 42863
```

`pending` walks both scenes and every page, then prints unfinished homework sorted by deadline with a `late-ok` or `late-no` marker.

## Workflows

`references/workflows.md` maps what the user says to a call sequence. The common ones:

| User says | Reference section | Writes |
| --- | --- | --- |
| 还有哪些作业没交 | 1. Open work list | no |
| 打开这次作业 / 有几题 | 2. Open one 作业 | no |
| 帮我把选择题做了 | 3. Objective answers | answers only |
| 帮我交作业（拍照） | 4. Picture answers | answers only |
| 交卷 | 5. Finalize | files the 作业 |
| 订正第 N 题 | 6. Resubmit one exercise | spends a 订正 quota |
| 看看批改结果 / 错在哪 | 7. Graded review | no |
| 我要申诉 | 8. Appeal | yes |
| 错题本 / 复习错题 | 9. Wrong-question book | partly |
| 今日一题 | 10. Daily question | yes |
| 在线考试还来得及吗 | 11. Online exam window | yes |
| 签到 | 12. Check-in | yes |

Every write workflow starts with the shared precondition block in that file: read `homeworkInfo`, compare `examServerNow` to the deadline, confirm the exercise is answerable, and state the refusal reason when it is not. Saving answers (workflows 3 and 4) and filing the 作业 (workflow 5) are separate permissions; do one without the other only when the user asked for that part.

## Guardrails

Read calls are safe to repeat. These calls change the student's record:

| Call | Effect |
| --- | --- |
| `POST /api/homework/student/homework/submit` with `exercises` | writes answers against the 习题 |
| `POST /api/homework/student/homework/submit` with `finalize: true` | files the 作业 (交卷), no undo |
| `POST /api/homework/student/exercise/resubmit` | spends one 订正 quota (`resubmitTimes`, `subjectiveResubmitTimes`, `objectiveResubmitTimes`) |
| `POST /api/homework/student/shared-images` | attaches one picture set to several exercises |
| `POST /api/appeal/student/submit` | opens a 申诉 against a 批改 result |
| `POST /api/attendance/student/checkin` | marks 签到 |

`scripts/smartestu-api.mjs` refuses non-GET requests unless `--allow-write` is passed, and prints the request it is about to send. Passing the flag asserts that the user confirmed; never pass it on your own initiative.

### Confirmation before every write

Ask, then act. A write happens only after the user answers for that exact action.

1. Show the payload in plain words before sending: 作业 name and id, exercise numbers, the answer for each exercise, and whether `finalize` is set.
2. State what it costs: 交卷 has no undo, late work scores `lateSubmissionScoreRatio` percent, 订正 consumes one quota, 申诉 has its own deadline.
3. Wait for an explicit yes. A general "帮我完成作业" authorizes saving answers for that 作业; filing it is a separate question asked separately.
4. One confirmation covers one call on one 作业. Never carry it to the next 作业, the next 交卷, or a retry.
5. When the user asks for the whole 作业 in one sentence, do the work, show the result, then ask about 交卷 as its own step.
6. Answer a failed or unclear write by re-reading the 作业 first, then sending only what is still missing. A blind retry after a timeout or a 5xx risks a duplicate submission.

Never store the user's `csrfToken`, `sessionContext`, cookie, `schoolUserId`, or name inside a repository. Read them from the environment or a file outside version control.

## Response envelopes

Three shapes appear; check the shape before parsing:

| Shape | Endpoints |
| --- | --- |
| `{"code":200,"msg":"成功","data":...,"success":true}` | `/api/homework/*`, `/api/practice/*` |
| `{"code":200,"message":"成功","data":...}` | `/api/course-contents/student/courses`, `/api/student-tutor/access` |
| Bare object, no envelope | `/api/auth/session`, `/api/roles/{role}`, `/api/user/knowledge-framework/check-access` |

The client branches on the body `code` field, so read `code` and `msg` before trusting an HTTP 200. `code` is a number on success and a string on auth failures: an unauthenticated call answers HTTP 401 with `{"code":"AUTH_UNAUTHENTICATED","message":"无法确认登录状态，请重试"}`. `GET /api/config` and `GET /api/banner/popup` answer 304 when the browser cache revalidates; a 304 body is empty and valid.

Deadlines and exam clocks come from `examServerNow`, a server timestamp repeated inside every homework object. Compare against it when judging whether a 作业 is still open; the local clock drifts.

## Answer submission

Answer images upload first, as multipart with the fields `file`, `exerciseId`, `type` (0 for answer pages, the only value the client uses):

```
POST /api/homework/files/exercise/upload
```

Then the answers land on the 作业:

```
POST /api/homework/student/homework/submit
{"homeworkId":42863,"exercises":[{"exerciseId":123456,"answer":"[\"A\"]"}],"finalize":false}
```

Objective answers travel as a JSON-encoded string: `"[\"A\"]"` for `mcq_single` and `mcq_multi`, `"{\"1\":true,\"2\":false}"` for `tf_multi` keyed by statement id. Subjective answers travel as uploaded image URLs. Finalizing sends the same call with `exercises: []` and `finalize: true`; the reply reports `data.finalized`.

Per-exercise results come back as `data.exercises.results[]` with `exerciseId`, `success`, `message`. Partial failure is normal; only the listed successes were stored.

`POST /api/homework/student/exercise/resubmit` covers 订正 of one exercise, either `{"exerciseId":N,"objectiveAnswer":...}` or `{"exerciseId":N,"subQuestionNumbers":[],"subQuestionIndexes":[],"answerUrls":[...]}`.

## Rendering math

Stems, options, statements and reference answers are Markdown with LaTeX. The platform preprocesses that text with its own rules before KaTeX: `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, `\begin{equation}`, a `$` before a digit left as text, inline math wrapped in `\displaystyle`, mhchem macros re-escaped, and KaTeX run with `strict: false`. Details in `references/math-rendering.md`.

Two tools, two jobs:

- Platform LaTeX unchanged: MathJax `tex2svg`. Same input language, mhchem included, glyphs as paths.
- Your own Chinese-plus-math card: typst, through `scripts/render-math.sh`.

```bash
echo '质量为 $m$ 的物体加速度 $a = F \/ m$' | scripts/render-math.sh --out card.png --ppi 300
echo '若 $lim_(x -> 0) (sin x)\/x = 1$，则' | scripts/render-math.sh --svg --out card.svg
```

typst rejects LaTeX commands: `\frac`, `\sum`, `\int`, `\alpha` all fail with `unknown variable`. Convert first (`a/b`, `sum_(i=1)^n`, `integral_0^1 f dif x`, `alpha`), or use MathJax.

One gotcha worth keeping: typst templates that pass text through `--input` need `#eval(sys.inputs.body, mode: "markup")`. A bare `#sys.inputs.body` prints the `$` delimiters as literal characters.

Rendered cards are not 手写. Uploading one as a 作答 image risks exercise status `4` NOT_HANDWRITING, which is final and blocks 订正. Render for reading and explanation; upload only when the user confirms the teacher accepts typeset work.

## Reading a 批改 result

`queryExercisesByHomeworkId` returns `data.homeworkInfo` (the homework object) and `data.exercises[]`. Each exercise carries `status`, `markScore`, `markPayload`, `answerStructure` (reference answer), `studentAnswerRaw`, `answerImages`, `annotations`, `studentSubExercise[]` (earlier attempts), and `questionStructure` (stem, options, statements).

`status` uses a signed enum shared with the teacher console: `-2` image problem, `-1` grading failed, `0` submitted and 批改中, `1` graded, `3` disputed, `4` non-handwriting, `5` plagiarism, `6` suspected, `7` appeal processed. Full labels in `references/data-models.md`.

Whether the reference answer is released depends on `enableAns`, `hideMarkUntilExamEnd`, `resubmitAnswerRevealMode`, and `objectiveOutcomeReveal`. Treat `answerStructure: null` as "not released yet", not as "no answer exists".

## Scope

The platform also exposes 教师, 学委, 助教, 教务, 签到, 考试 and 自主测试 surfaces; paths are in the inventory. Their request bodies were not captured and are out of scope for this skill. The AI chat endpoints (`/api/ask/*`, `/api/convos`, `/api/agents`) belong to the bundled LibreChat instance.
