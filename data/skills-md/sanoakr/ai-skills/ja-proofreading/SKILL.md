---
name: ja-proofreading
license: MIT
description: |
  Proofread Japanese text using textlint with Japanese preset rules. Report issues clearly in Japanese.

  Trigger on:
  - "proofread", "check this Japanese text", "fix Japanese writing"
  - "日本語の文章を校正して" "textlintでチェックして" "文章の誤りを見つけて"
  - Requests to check ら抜き言葉, 二重否定, 読点, 文体統一, etc.
  - Quality checks on blog posts, technical docs, manuals in Japanese
  - Proofreading `.md`, `.txt`, `.mdx` files with Japanese content
  - "文章を直して" "読みやすくして" when the target text is Japanese

  Always report findings in Japanese regardless of the conversation language.
---

# Skill: Japanese Proofreading (textlint)

Detect and report issues in Japanese text using textlint with Japanese preset rules.

## Rule Presets

- **textlint-rule-preset-ja-technical-writing** — 25 rules for technical docs (sentence length, commas, ら抜き, style consistency, etc.)
- **textlint-rule-preset-japanese** — 12 general rules (stable, low false-positive)
- **textlint-rule-preset-ja-spacing** — spacing rules between Japanese and alphanumerics

## Steps

### Step 1: Identify input

- Text pasted in conversation → write to a temp file, then process
- File path given → use that file directly
- Uploaded file → read from `/mnt/user-data/uploads/`

### Step 2: Set up environment

Use `scripts/setup_textlint.sh`. Check for an existing setup at `/tmp/textlint-ja/`; install if missing:

```bash
ls /tmp/textlint-ja/node_modules/.bin/textlint 2>/dev/null || bash <skill-dir>/scripts/setup_textlint.sh
```

### Step 3: Run textlint and format output

```bash
cd /tmp/textlint-ja
./node_modules/.bin/textlint --config .textlintrc.json --format json <target-file> \
  | python3 <skill-dir>/scripts/format_results.py -
```

If `python3` is unavailable, save JSON to a temp file and parse manually.

### Step 4: Report (in Japanese)

Present the formatted output from `format_results.py` as-is. If the script was not available, report in the following format:

```
## 校正結果: <ファイル名>

### 概要
- 指摘件数: X件
- エラー（必須修正）: X件
- 警告（推奨修正）: X件

### 指摘一覧

**1行目: 「〇〇〇」**
- ルール: `preset-ja-technical-writing/no-dropping-the-ra`
- 問題: ら抜き言葉が使われています
- 修正案: 「〇〇られ」→「〇〇れ」

...

### 修正済みテキスト（任意）
<corrected version if requested>
```

### Step 4.5: Colloquial contraction check (supplement)

textlint does not catch colloquial contractions. Run this grep after textlint and include findings in the report:

```bash
grep -n "てた\b\|てる\b\|てく\b\|でた\b\|でる\b\|ちゃ\|じゃ\|なきゃ" <target-file> \
  | grep -v "^\`\`\`" \
  | grep -v "^    "
```

Common contractions and corrections:

| 縮約形 | 正式形 | 例 |
|--------|--------|-----|
| 〜てた | 〜ていた | 「作業をしてたのですが」→「作業をしていたのですが」 |
| 〜てる | 〜ている | 「確認してる」→「確認している」 |
| 〜てく | 〜ていく | 「進めてく」→「進めていく」 |
| 〜ちゃ | 〜ては | 「やっちゃいけない」→「やってはいけない」 |
| 〜なきゃ | 〜なければ | 「直さなきゃ」→「直さなければ」 |

Exclude matches inside code blocks, quotes, file names, or URLs.

### Step 5: Provide corrected text (optional)

If the user asked for corrections, provide the full corrected text. Note which fixes are mechanical and which require judgment.

## textlintrc Configuration

Use the following at `/tmp/textlint-ja/.textlintrc.json`:

```json
{
  "rules": {
    "preset-ja-technical-writing": {
      "sentence-length": {
        "max": 150,
        "skipPatterns": ["\\[.*?\\]\\(.*?\\)"]
      },
      "max-ten": {
        "max": 4
      },
      "no-mix-dearu-desumasu": {
        "preferInBody": "です・ます",
        "preferInHeader": "である",
        "strict": true
      },
      "no-exclamation-question-mark": false,
      "ja-no-weak-phrase": false
    },
    "preset-japanese": true,
    "preset-ja-spacing": {
      "ja-space-between-half-and-full-width": {
        "open": false,
        "close": false
      }
    }
  },
  "filters": {
    "comments": true
  }
}
```

Rationale for customizations:
- `sentence-length.max: 150` — technical docs contain URLs and code; 100 is too strict
- `max-ten.max: 4` — 3-comma limit is too tight; relaxed to 4
- `no-mix-dearu-desumasu.strict: true` — catch style mixing even mid-paragraph and in lists
- `no-exclamation-question-mark: false` — allow `!`/`?` in blog posts
- `ja-no-weak-phrase: false` — "〜と思います" is context-dependent; skip

## Rule Error Reference (Japanese)

| Rule ID | 日本語説明 |
|---------|-----------|
| `sentence-length` | 1文が長すぎます（{max}文字以内にしてください） |
| `max-ten` | 読点「、」が多すぎます（{max}個以内にしてください） |
| `max-comma` | カンマが多すぎます（{max}個以内にしてください） |
| `no-mix-dearu-desumasu` | 「です・ます調」と「だ・である調」が混在しています |
| `no-doubled-conjunction` | 接続詞が連続しています |
| `no-doubled-conjunctive-particle-ga` | 逆接の「が」が連続しています |
| `no-double-negative-ja` | 二重否定が使われています |
| `no-dropping-the-ra` | ら抜き言葉が使われています |
| `no-doubled-joshi` | 同じ助詞が連続しています |
| `ja-no-successive-word` | 同じ単語が連続しています |
| `ja-no-abusage` | よくある誤用が含まれています |
| `ja-no-redundant-expression` | 冗長な表現が含まれています |
| `ja-no-weak-phrase` | 弱い表現（〜かもしれない等）が使われています |
| `no-nfd` | Mac由来の濁点エラーがあります |
| `no-zero-width-spaces` | ゼロ幅スペースが含まれています |
| `ja-no-mixed-period` | 文末句点が統一されていません |
| `no-hankaku-kana` | 半角カナが含まれています |

## Notes

- Code blocks (` ``` `) are not checked — this is expected behavior
- URLs and command examples flagged as "long sentences" are false positives; skip them
- If writing style (です・ます vs だ・である) is unclear, scan the whole document and report the dominant style
- When there are many findings, prioritize errors (severity: error) and report only the count of warnings
- With `strict: true` on `no-mix-dearu-desumasu`, list-item である-style will error. If the user says "lists can use である", either set `strict: false` or suppress that rule only
- Step 4.5 hits inside code, quotes, or URLs are false positives — exclude them
