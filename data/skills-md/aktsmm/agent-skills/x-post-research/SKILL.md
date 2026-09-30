---
name: x-post-research
description: "Collect and analyze public X posts from keywords, hashtags, OR queries, domains, or known post URLs, then trace them to primary sources, official docs, GitHub repos, benchmarks, and reusable images. Use for launch-day reactions to a new model or product, event hashtags, keynote coverage, new-technology use cases, popularity research, or turning noisy X posts into a source-backed research note. Triggers: X で調べて, X の反応, ハッシュタグ調査, キーワードで X 検索, X 投稿からネタ探し. Not for posting or account operations on X."
argument-hint: "検索クエリ（キーワード / ハッシュタグ / OR / ドメイン）または投稿 URL、時間窓、件数、保存先メモ名"
user-invocable: true
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# X Post Research

FxTwitter API を起点に公開投稿を収集し、一次情報 URL、関連 GitHub repo、画像、論点を research 配下へ整理する workspace 用 skill。ハッシュタグに限らず、通常キーワードや既知投稿 URL から始めてよい。

## When to Use

- 新モデル・新機能の名前（例: `"GPT-6 Luna" OR "GPT6 Luna"`）で、発表後の反応、第三者評価、実使用報告を拾いたいとき
- X の通常キーワード、`OR`、ドメイン、既知投稿 URL から新技術やユースケースを探したいとき
- X のハッシュタグからイベント当日の発表を追いたいとき
- 反応数の多い投稿を候補として抽出し、一次成果物まで確認したいとき
- `#MSBuild` や `#MicrosoftBuild` のような event hashtag を直近数時間で総ざらいしたいとき
- keynote 直後に、一次情報 URL と repo の導線を先に集めたいとき
- noisy な実況投稿から、Microsoft Learn / blog / GitHub / session repo に収束させたいとき
- 画像付き投稿も research asset として残したいとき

## Scope

- この skill は X 専用にする
- Bluesky、LinkedIn、YouTube comments などは対象外
- X への投稿やアカウント操作は対象外
- それらを扱いたい場合は別 skill に切り出す

## Default Profile

明示指定がないときの既定候補はこれ。

- time window: `直近 4 時間`
- target posts: `500`
- raw artifact: `tmp/`
- research note: `research/YYYYMMDD-<topic>-from-x.md`
- curated images: `research/assets/YYYYMMDD-<topic>-from-x/`
- bulk images: `research/images/YYYYMMDD-<topic>-from-x/`

## Confirm Collection Scope

検索で投稿群を収集するときは、次の 4 点を確認する。

1. 対象クエリ（ハッシュタグ / キーワード / `OR` / ドメイン）または既知投稿 URL
2. 時間窓
3. 目標件数
4. 保存先メモ名

ユーザーが省略した場合は既定値を提案して確認を取る。勝手に `4時間 / 500件` で走らせない。既知投稿 URL が列挙済みなら、その URL 群が対象と件数を定義するため時間窓は不要。保存先を既存成果物から一意に決められる場合も聞き直さない。発表当日の新モデル名などは `feed=latest` の 500 件が数時間分で尽きるため、件数上限に先に達したら実際の対象期間を記録して未充足と報告し、発表直後の公式投稿を既知 URL として追加取得するか、件数を増やすかを提案する。

## Collection Paths

- 公開投稿の収集は、合意済みの時間窓・件数内に限り `GET https://api.fxtwitter.com/2/search?q=<URL-encoded-query>&feed=latest&count=100` を既定にする。`q` はハッシュタグだけでなく通常キーワード、`OR`、ドメインを URL encode してよい。次ページは `cursor.bottom` を `cursor` に渡す。既知投稿は `GET /2/status/{id}` で再取得する。
- FxTwitter は X の公式 API ではない。Cookie、トークン、アカウント情報を渡さず、公開投稿の一回限りの収集に限定する。
- HTTP ステータスだけでなく JSON の `code` を確認し、`200` の `results` だけを採用する。`400`、`404`、`500` は再試行を重ねず、X の画面または一次情報へ戻る。
- 非公開、削除済み、アクセス制限付き投稿、継続監視には使わない。
- API が失敗するか、投稿の画面文脈を確認する必要がある場合は、ブラウザ系ツールで X の live search を開き、投稿 URL、時刻、本文、画像 URL を取得して下へスクロールする。
- 構造化抽出が弱い場合も、raw 投稿の保存、visible domain / card title による粗い分類、高シグナルな一次情報の深掘りの順番は固定する。
- 全件自動化にこだわらず、公式アカウント、live blog 導線、代表画像を優先する。

この skill の本体はブラウザ操作のコツではなく、SNS ノイズを一次情報へ収束させる順番にある。

## Workflow

1. 収集対象を固定する
   対象クエリ、時間窓、件数目標、主目的、research の保存先を決める。

2. API から効率よく収集する
   API の `results` から status URL を主キーに構造化抽出し、重複排除する。API が失敗した場合だけ画面から補う。

3. raw artifacts を先に保存する
   `tmp/<slug>-posts-raw.json` と batch 単位の中間 JSON を残す。

4. ローカル分類を先にやる
   rawText、tweetText、display text、X card の visible domain から theme、domain、repo、image candidates を作る。人気候補は重複排除後に `likes`、`reposts`、`views` で sort するが、反応数を正確性の根拠にはしない。

5. 高シグナルリンクだけ深掘る
   全 t.co を解決せず、高頻度リンク、公式アカウント、画像付き高シグナル投稿、repo 名が半分読めている投稿だけを追う。外部リンク先の repo / Docs / app /記事で実装と主張を確認し、README の roadmap や planned を実装済みとして数えない。

6. research ノートは source-centric に書く
   投稿の感想ではなく、投稿がどの一次情報へ収束したかを正本にする。A=一次成果物+測定、B=一次成果物、C=投稿内デモ/自己申告、D=アイデアのみ、で証拠レベルを分ける。動画UIしか根拠がない主張は`動画内の説明では`と帰属し、実装、精度、token、費用を確認済みにしない。

7. 画像は 2 層で保存する
   curated set は 5〜10 枚、bulk は 20〜30 枚程度を目安にする。X Article は title / blocks /引用元、画像は原寸、動画は captions または代表 frame を確認し、見ていない media の内容を断定しない。記事掲載では全編の再配布より、主張に必要なbefore / operation / afterなど最小frameを優先し、無関係なbrowser chromeを除く。古い star 数や実装前の説明を含む card 画像は、一次成果物へのリンク以上の価値がなければ採用しない。画像単体で誤認する場合は、筆者追加と分かる注記を入れるか掲載しない。

8. 再現可能な成果物で終える
   research ノート、raw JSON、主要一次情報 URL、画像保存先、必要なら manifest 追記まで揃える。外部mediaを保存・加工した場合は元投稿URL、取得日、source相対path、SHA-256をmanifestへ記録し、builder / auditで照合する。

## Branching Rules

- 公開・一回限り・上限付きの収集: FxTwitter API search を使い、`code: 200` の結果だけを raw artifact に残す
- API が失敗または投稿の画面文脈が必要な場合: 公式アカウント、live blog、official blog、repo 導線付き投稿を優先する
- 短縮 URL 解決が重い場合: 全解決しない。高頻度・高シグナルだけ解決する
- 画像が多すぎる場合: curated を先に確保し、bulk は上限を切る

## Quality Gates

- 収集件数と時間窓の両方を満たしている。満たせない場合は、実際の対象期間と未収集の範囲を research ノートに明記している
- 主要テーマが公開情報の塊として整理されている
- repo 名が切れている場合は本文・card title・公式 blog で補正している
- 画像保存先が research 配下で整理されている
- 元の公開投稿を改変した断定はしていない
- FxTwitter を使った場合、出典は API URL ではなく各 `status.url` の元の X 投稿 URL にしている
- 人気順と証拠レベルを分け、自己申告・アイデアを実証済みとして扱っていない
- repo / app の現在状態を確認し、実装済み・roadmap・作者 benchmark・筆者実測を分けている
- 掲載画像の日時と主張が一致し、筆者追加の注記を原画像の表現と混同させていない

## Efficiency Rules

- `tmp/*.json` に途中結果を保存して取り直しを避ける
- ローカル分類を先にやって、外部 fetch はその後
- 公式 blog の横断記事があるなら、それを hub にして個別記事へ降りる
- browser 固有 tips は抱え込みすぎない。必要なら `browser-max-automation` を使う

## Example Prompts

- `/x-post-research "GPT-6 Luna" OR "GPT6 Luna" を直近7日で500件集めて、記事に足せる第三者評価や注意点を拾って`
- `/x-post-research #MSBuild と #MicrosoftBuild を直近4時間で500件以上集めて、一次情報と repo と画像を research に保存して`
- `/x-post-research #Ignite と #MicrosoftIgnite を2時間で300件、画像は代表8枚だけでいい`

## Related Customizations To Create Next

- X 調査結果を keynote research に差し込む prompt
- 保存画像から記事向きのものだけ選別する skill
- official blog / Learn / GitHub repo のみを二次整理する prompt
