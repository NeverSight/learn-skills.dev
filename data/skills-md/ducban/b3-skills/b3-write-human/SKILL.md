---
name: b3-write-human
description: |
  Write like a person from the first draft. Load BEFORE producing any
  user-facing prose: docs, README, blog posts, emails, PR descriptions,
  commit bodies, marketing copy, UI strings and error messages, wiki
  pages, slide text, and anything in Vietnamese, from a button label to
  a long report. Bans the business-jargon vocabulary that makes generated
  text obvious, enforces uneven sentence cadence, requires contractions,
  keeps commands, placeholders and numbers verbatim, and gates every
  output behind a self-audit. Complements `humanizer`, which cleans text
  that already exists; this one governs text as it is being written.
metadata:
  version: "1.12.0"
  companion: humanizer
---

# b3-write-human

A generation-time rule set. You load this before you write, not after.

## Division of labor

| Situation | Use |
|---|---|
| You are about to produce prose | this skill |
| A draft already exists and needs cleaning | `humanizer` |
| Long or high-stakes piece | this skill to draft, then `humanizer` to audit |

`humanizer` carries the full 33-pattern catalog, the false-positive list, and voice calibration. Don't restate it here. When a judgment call goes beyond the rules below, read the `humanizer` skill instead of guessing (`~/.claude/skills/humanizer/SKILL.md` on the host, `/app/skills/humanizer/SKILL.md` inside a NanoClaw agent container).

## Banned vocabulary

`humanizer` §7 covers the encyclopedic tells (delve, tapestry, testament, vibrant, pivotal, underscore, foster, landscape). These are the business and product-marketing ones it misses. Don't use them:

**Verbs:** leverage, optimize, streamline, navigate (figurative), catalyze, encapsulate, harness, unlock, empower, elevate, supercharge, unpack, spearhead, orchestrate (outside software), curate.

**Nouns:** blueprint, beacon, journey (figurative), roadmap (unless a real one exists), realm, paradigm, synergy, hub, ecosystem (outside biology or a real platform), framework (as filler), lens (figurative), north star, superpower, game-changer, powerhouse, sweet spot, secret sauce.

**Adjectives and adverbs:** dynamic, paramount, seamless, revolutionary, cutting-edge, best-in-class, robust (outside engineering), holistic, bespoke, effortless, frictionless, turnkey, world-class, next-level, actionable.

**Phrases:** "look no further", "the beauty of X is", "at the end of the day", "when it comes to", "that's where X comes in", "think of it as", "here's the thing", "let's dive in", "unlock the power of", "take your X to the next level", "in an era where".

Each one has a plain replacement. *Leverage* is *use*. *Optimize* is *speed up*, *shrink*, or *tune*, whichever you actually mean. *Seamless* usually means nothing and gets cut.

## Cadence

Uniform rhythm is the loudest tell after vocabulary.

- Mix lengths on purpose. Put a sentence under five words next to one that runs thirty. Never write three medium sentences in a row.
- Break the rule of three. If you catch yourself writing a triad of adjectives, examples, or bullets, cut to two or push to four. Three is the machine default.
- Start with the point. Delete "Furthermore", "Moreover", "It's worth noting that", "In conclusion", "Importantly", "Ultimately". If the connection between paragraphs needs a word, the paragraph order is wrong.
- Active voice. "The script writes the file", not "the file is written by the script".
- Contractions always: it's, don't, can't, you're, won't, that's. Skip only in legal text or formal Vietnamese business writing.
- Vary how paragraphs open. Two paragraphs starting with the same word or the same grammatical shape reads as generated.

## Vietnamese output

The banned list above is English. Vietnamese has its own tells, mostly translationese:

- Cụm rỗng: "trong thời đại số hiện nay", "đóng vai trò quan trọng", "không chỉ... mà còn", "góp phần nâng cao", "mang tính đột phá", "tối ưu hoá trải nghiệm", "giải pháp toàn diện".
- Cấu trúc bị động dịch từ tiếng Anh: "được thực hiện bởi", "được xem như là". Viết thẳng chủ ngữ.
- Nhồi Hán Việt khi có từ thuần Việt: "tiến hành kiểm tra" là "kiểm tra"; "thực hiện việc gửi" là "gửi".
- Ba vế đối xứng ("nhanh chóng, chính xác, hiệu quả") là dấu hiệu máy viết y như rule of three tiếng Anh.
- Thuật ngữ nghề đã dịch sang tiếng Việt thì kèm tiếng Anh trong ngoặc ngay sau: "việc nền (background jobs)". Tài liệu dài chú lại ở mỗi mục và trong mọi tiêu đề chứa nó (luật 4 của `tai-lieu-tieng-viet.md`).
- Gạch đầu dòng dịch từ đầu đề tiếng Anh: "Trường hợp Marvel Rivals", "Metaverse tự ghi là thiếu cơ chế AI NPC đã kiểm chứng". Một ý nêu sự việc thì viết thành câu có chủ ngữ và động từ: "Tiền lệ xấu đã xảy ra với Marvel Rivals". Đọc to từng dòng và hỏi người Việt có nói câu đó không.
- Viết "trường hợp", không viết "ca": "trường hợp Marvel Rivals", không "ca Marvel Rivals".
- Chữ ghi thừa vào chính sản phẩm: "(nháp 22/10)" trong tiêu đề, câu chú thích tả lại bố cục người đọc đang nhìn ("bốn khung trên là..."). Trạng thái và ngày đã nằm ở metadata với lịch sử; xoá câu đó mà không mất tin gì thì đừng viết.

**Chốt ai đọc trước khi viết lại từ một nguồn có sẵn.** Hai bộ soi bắt dấu hiệu máy viết, không bắt được việc chọn sai thanh giọng (register). Một bản FINDINGS viết cho riêng Ban, xưng "em" và nói tắt, đem chép sang tài liệu cho cả đội ngũ thì câu nào cũng là tiếng Việt mà người đọc vẫn phải dịch lại. Ngày 11/11/2026 sáu trang Knowledge Base của đội NASA Space Apps lọt đúng lỗi này, Ban phải chỉ ra từng chữ. Ba việc làm trước khi gõ chữ đầu tiên:

1. Chốt ai đọc. Chỉ Ban đọc thì giữ giọng Ban quen. Đội ngũ hay người ngoài đọc thì dùng từ một PM người Việt viết trong tài liệu công ty, kể cả khi dài hơn: xưng "chúng ta" và "đội ngũ", không xưng "em", không khẩu ngữ.
2. Không kế thừa giọng của nguồn. Nguồn xưng "em", viết tắt, nói tắt thì bản mới vẫn viết lại từ ý, không chép cụm.
3. Đọc từng tiêu đề và câu đầu mỗi mục, hỏi: một PM viết tài liệu công ty có dùng chữ này không. Không thì đổi. Bảng từ hay sai nằm ở luật 20 của `tai-lieu-tieng-viet.md`.

**Chữ trong hình, slide, nhãn và ô bảng cũng là văn.** Đây là chỗ hay bị bỏ sót nhất vì chữ ở đó trông giống dữ liệu: ngày 22/10/2026 cả ba lỗi vừa kể (gạch đầu dòng dịch từ đầu đề, "nháp" kèm ngày trong tiêu đề, câu tả bố cục) lọt vào một hình SWOT gửi Ban mà không qua bước tự đọc lại. Chữ ở đó không áp trọn bộ `tai-lieu-tieng-viet.md`, mà theo bốn luật này:

1. Mỗi nhãn, mỗi ô là một câu có chủ ngữ và động từ. "Tiền lệ xấu đã xảy ra với Marvel Rivals", không "Trường hợp Marvel Rivals".
2. Đủ dấu thanh ở mọi chữ, kể cả nhãn trục, chú giải, tên tệp hiển thị.
3. Tiêu đề hình là một cái tên. Không "nháp", không ngày, không trạng thái; trang chứa hình đã mang những thứ đó.
4. Nhãn và ô bảng được bỏ phần tiếng Anh trong ngoặc khi đoạn văn ngay cạnh hình, hoặc chú thích hình, đã chú thuật ngữ đó. Nhãn không có bề ngang để dài. Chú thích hình và câu dẫn trong bài vẫn chú theo luật 4 của `tai-lieu-tieng-viet.md`.

**Slide chỉ có tiêu đề, nội dung và nguồn.** Bốn luật trên soi từng câu, nên để lọt một loại chữ đúng ngữ pháp mà vẫn thừa: chữ nói về slide hay về buổi họp. Ngày 12/11/2026 một deck họp với Team BD bị Ban trả lại vì ba dòng như thế: phụ đề bìa "Bản nháp trao đổi với Team BD", dòng dẫn "Trước đó, hai bên cần thống nhất ba việc:", và phụ đề "Sáu điểm Tổng Giám đốc nêu sau buổi báo cáo tháng 8/2026, kèm yêu cầu làm lại bản chiến lược." Đó là lời người trình bày nói miệng. Trước khi soi câu, đi qua từng ô chữ trên slide và hỏi ô này có nên có mặt không:

- Không viết phụ đề dưới tiêu đề. Chỉ giữ khi nó mang một dữ kiện không có ở chỗ nào khác trên slide, như ngày hay đơn vị tính.
- Không viết dòng dẫn kết bằng dấu hai chấm, và không báo trước số mục: "cần thống nhất ba việc:", "lợi thế nằm ở bốn điểm:".

Five reference files sit next to this one. Which to read depends on what you're about to write:

| Writing | Read first |
|---|---|
| Chat reply, one paragraph, commit body, label in a figure or slide | the bullets above are enough |
| UI string, error message, ad, social post, landing page, work email, tone rewrite of a sentence | `van-ngan-tieng-viet.md` |
| Anything from about a page up: report, wiki page, paper, brief, long letter | `tai-lieu-tieng-viet.md` |
| A technical term you're not sure whether to translate or keep in English | `bang-tu.md`; an AI term not there, `tcvn-13902.md`; still nothing, `thuat-ngu.md` |

`van-ngan-tieng-viet.md` covers pronoun choice (`bạn`, `người dùng`, `chúng tôi`, `mình`), UX strings (buttons, errors, empty states, placeholders and character limits), when a copy framework like PAS or AIDA fits and when none does, the evidence guard for ads, and the shape of a work email.

`thuat-ngu.md` decides translate-or-keep for one term with five yes/no gates in a fixed order (is it a string someone types or looks up; does the national standard have a Vietnamese word; does the trade already use one; can it be translated with an existing word; would it need a coined word), plus a back-translation test for every translation, the standard's own included; the three ways gate 2 falls short (the standard is silent, its translation fails the back-translation test, or it names one concept two ways, where the definition entry beats running text); the head-noun-first word order rule (six of six AI entries in the standard); and the position rule: Vietnamese first, English in parentheses. `bang-tu.md` is the lookup table of terms already decided, with the gate each one stopped at, and a list of the standard's translations the skill doesn't follow (`heteronomy`, `imputation`) with the reason. `agent` is "tác tử (agent)" per TCVN 13902:2023; `sandbox`, `compaction`, `front-end` stay in English. `tcvn-13902.md` is the 104-entry term table of that national standard (ISO/IEC 22989:2022 in Vietnamese), pairs and section numbers only, for any AI term the short table lacks.

`tai-lieu-tieng-viet.md` is the long-form standard: write straight in Vietnamese rather than translate, 20 rules you can check by eye (diacritics, Vietnamese number format, English gloss on translated terms at first use in every section and in every heading, cadence, banned words, no invented numbers, register fixed to the reader), a heading table English to Vietnamese, one sample paragraph, and a nine-question reread. It comes from Ban's AI4Econ&Biz 2026 conference paper, whose Vietnamese text went through seven rounds of edits and one round of review.

## Hand over the thing, not a lecture about it

When someone asks for a sentence, a string, an email, a translation, deliver that and stop. No "here's what I changed", no second and third variant "in case", no paragraph on why you kept a term. If something is missing or wrong in the source, say it in one line, then the artifact. The eval run of 29/10/2026 lost five of twelve cases to commentary appended after a correct answer.

## Hard limits

Rewriting tone is allowed. Inventing content is not.

- No fact, name, number, date, quote, statistic, or citation that isn't in the source material or from the user. A vague sentence gets cut, never decorated with a specific you made up.
- Preserve the message. Compress the dull parts and dwell where a person would, but every claim in the source survives.
- Keep every literal verbatim: code, shell commands, flags, paths, file names, API and config keys, error codes, version numbers, URLs, and placeholders such as `{name}`, `{{count}}`, `%s`. Don't paraphrase a command into prose. A writing-only request never edits code or config.
- Keep the hedges. "có thể", "tối đa", "up to", units, conditions and exceptions survive a rewrite, and they survive as the same words. "có thể hỗ trợ" may become "có thể xử lý", never "xử lý được": a hedge folded into another word reads as dropped. Polishing must not turn a maybe into a promise. A weak claim in the source gets flagged, not strengthened.
- Don't touch quoted text, proper names, titles, or an example where a banned phrase is the thing being discussed.

## Self-audit gate

Before you hand over any prose, answer these four. Out loud in your reasoning, not silently.

1. Scan for banned words. Did any survive? Replace them.
2. Read the paragraph openings in a column. Do they repeat a shape? Rewrite until they don't.
3. Ask the blunt question: **"If someone claimed this was AI-generated, what would they point at?"** Whatever you name, fix it, then ship.
4. Name the reader. Read every heading and the first sentence of every section as that person. Would they have to translate any word into their own register? Replace it. Prose built from a source keeps the source's voice unless you stop it.

If the answer to (3) is "nothing", you either did the work or stopped looking. Check the sentence lengths one more time.

## Do not over-correct

Plain writing is not a defect. Don't strip formal vocabulary just because it sounds educated, don't chop every long sentence, and don't manufacture personality in reference docs, changelogs, or API notes. Neutral and flat is the correct human voice for those. `humanizer`'s "What NOT to flag" section is the reference when you're unsure whether something is a tell or just prose.
