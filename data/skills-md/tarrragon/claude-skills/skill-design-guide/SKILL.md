---
name: skill-design-guide
description: "Anthropic skill spec plus this project's conventions: frontmatter, descriptions, loading budgets, and splitting an oversized skill. Use when creating a skill, editing SKILL.md, reviewing skill quality, or moving content into references/."
metadata:
  version: 1.23.2
---

# Skill Design Guide

依據 Anthropic 官方 `skill-creator` 與 Claude Code 平台規範整合的 Skill 設計指引。本檔聚焦「為什麼這樣設計」與「具體該怎麼做」，不重述官方文件全文。

**官方來源**：

- Skill spec: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
- Best practices: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Claude Code skills: <https://code.claude.com/docs/en/skills>
- 官方 `skill-creator`: 已安裝於本環境的 plugin marketplace

**先認你在做哪一件事，三者的第一個動作不同**：

| 你在做的事 | 第一個動作 |
|-----------|-----------|
| 從零建一個 skill | 開 `references/creating-and-adopting-skills.md`，照〈Skill 建立流程〉走 |
| 改既有 skill 的某一部分 | 依下方〈按需讀取〉表選一份開；改完走〈發布前檢查清單〉 |
| 既有 skill 疑似超標 | 先跑〈Progressive Disclosure〉的量測指令確認，超標才進〈超標了怎麼辦〉 |

本檔留下的是三者共用的判斷標準——正文與 references 的分工、三層預算、超標的診斷、發布前檢查清單。

---

## 核心心法

### 正文是操作手冊，references 是它的依據

**Skill 正文是 agent 執行時的操作手冊。** 讀完正文，agent 要答得出三件事：我現在在哪一步、這個狀況該怎麼做、憑什麼這樣判。三者缺一它就得猜，而猜錯不會有人告訴它。

| 放正文 | 放 references |
|--------|--------------|
| 步驟的順序與交棒點（哪一步之後接哪一步） | 每一步的完整程序與分支 |
| **選路所需的判斷條件**——讀者不用它就判不出自己該走哪條路、該讀哪一份 | 判斷條件背後的完整論證與實證 |
| 每個狀況對應的動作（命中 X 就做 Y） | 狀況的細部分類與邊界案例 |
| 正文用到的每個受管詞的定義 | 用詞的來源與判斷標準演進 |
| 門檻值與量測指令 | 門檻的推導、校準過程、誤判分析 |
| — | 範例、正例、反例、可貼用的模板 |

**判斷標準只有一條：agent 照正文走得完嗎。** 走不完有兩種形態，修法相反——正文只給結論而把判斷條件外移，讀者選不了路，把條件搬回正文；正文塞進完整論證，讀者在該動手時還在讀理由，把論證外移只留主張句。


### Concise is Key — context 是公共資源

**預設假設**：Claude 已經夠聰明。每段文字必須通過兩問才能保留。

| 自問 | 通過標準 |
|------|---------|
| 刪掉這段，Claude 的預設輸出會變嗎？ | 會變 → 保留；不會 → 移除 |
| 這段文字值得它的 token 成本嗎？ | 表格 / 範例優於散文，散文優於不存在 |

**第一問問的是行為差異，不是知識空缺。** 「Claude 知不知道」與「Claude 預設會不會這樣做」是兩個獨立維度——**「知道但預設不會做」的內容要留**（量測指令即屬此類：Claude 會算 token，但不會主動去量）。把兩者當成一條線的兩端，這一格會被誤判成移除。

**Action**：判不準時做刪除測試——把該段拿掉，在乾淨 session 對同一任務重跑，比對兩次產出。這一問可外部驗證，「Claude 知不知道」不能。


### Progressive Disclosure — 三層載入

| 層 | 載入時機 | 預算 | 寫什麼 |
|----|---------|------|-------|
| 1. frontmatter（name + description） | 常駐 system prompt | 250 字元（唯一閘門，另兩個口徑不換算，見 `references/frontmatter-and-description.md` 的〈Description 寫作（最重要的一節）〉） | 何時觸發 + 做什麼 |
| 2. SKILL.md 全檔 | 觸發後載入 | < 5k tokens；另須符合官方 < 500 行 | 核心工作流 + 路由 |
| 3. references/ + scripts/ + assets/ | Claude 按需 read / exec | 目錄總量無上限；單檔判斷標準見〈第 3 層的單檔判斷標準是讀取方式〉 | 細節、範例、模板、可執行腳本 |

**第 2 層與第 3 層都沒有 hook 會擋你，寫錯不會有人告訴你。** 唯一有執法的是第 1 層的 250 字元（`skill-description-length-check-hook.py`）。`file-size-guardian-hook.py` 掃的是 pm-rules / rules / references 三個目錄，**不掃 `.claude/skills/`**——所以第 2 層與第 3 層完全依賴撰寫者自查，量錯或不量，結果一樣。

**三個預算的適用對象各不相同，先認對象再量。** 第 2 層的兩個數字只管 `SKILL.md` **全檔**這一個檔，**含 frontmatter**——觸發後整份檔案會原樣再讀入一次，量測不扣除它。第 3 層的「無上限」講的是**目錄總量**（官方："no context penalty until accessed"），**不是單檔無上限**；單檔判斷標準見下方〈第 3 層的單檔判斷標準是讀取方式〉。

**Action**：第 2 層的主判斷標準是分段 token 估算，直接與 5k 比較。

```bash
python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();a=sum(1 for c in t if ord(c)<128);print(round(a/4+(len(t)-a)/1.3),'tokens (est)')" .claude/skills/<name>/SKILL.md
wc -l .claude/skills/<name>/SKILL.md   # 官方 500 行，超標即須外移
```

上面那行指令已經做完分段加總（繁中與 ASCII 的 chars/token 差三倍，不能用單一比例算），直接跑就好。**任何寫在文件裡的量測值都是當時的**——要現值就跑指令。換算常數的來源與校準記錄見 `CHANGELOG.md`。

### 超標了怎麼辦——不是刪，也不是硬搬

第 2 層超標時，**先問這個 skill 是不是在做太多事，再問要搬什麼**。順序反過來會把該分家的內容硬塞進同一個 skill 的 references，換來一份走不完的正文加一堆沒人讀的檔。

| 診斷 | 處置 |
|------|------|
| 正文塞了論證與實證敘事（「為什麼判斷標準是這樣」「一次實測發現…」） | 壓縮成主張句，敘事移入 `CHANGELOG.md` 或 ticket。這是最常見的一種，也該最先做 |
| 正文含選路之後才用到的細節 | 外移到對應的 reference，正文留路由。判斷標準見 `references/splitting-an-existing-skill.md` 的〈外移什麼、留什麼〉：問**這段用在讀者選路之前還是之後**。**「反正讀者一次只查一列」不是外移理由。** 每一張判斷標準表、路由表、分類表都符合這個描述，照它推下去整份正文都該外移——它分不出任何東西，當不了訊號 |
| 正文承載了兩個以上不相干的工作流 | **依 SRP 拆成多個 skill，彼此指名互相引用**，不是把一個 skill 拆成更多檔。見下段 |
| 上述三項都不成立，內容全是選路前必需且已無冗餘 | **超標是設計問題，不是編輯問題。** 不得為了達標而刪判斷條件或把它搬進 references——那會讓 agent 選不了路，而預算數字漂亮 |

**SRP 的單位是 skill，不只是檔案。** 正文超長最常見的成因是這個 skill 承擔了兩件事——把兩件事的細節各自外移，職責數量沒有變，正文仍要同時交代兩條路。這與元件庫同構：一個元件一份契約、組合關係由容器承載，而不是把所有元件塞進同一份條目再靠參數分岔。

| | 拆成兩個 skill | 拆成多個檔案 |
|---|--------------|-------------|
| **什麼時候** | 讀者要**換任務**：做完這件事才做那件事，或根本是不同的人在做 | 同一個任務的**不同階段或分支** |
| **做什麼** | 建立第二個 skill 目錄（新的 `SKILL.md` 加它自己的 `references/`），兩邊各自完整、以指名方式互相引用（「做完 X 之後走 `Y` skill」） | 在同一個 skill 內新增 reference，入口檔留路由 |
| **判錯的代價** | 該拆 skill 卻拆了檔案 → 一份正文要同時服務兩種讀者，誰都走不完 | 該拆檔案卻拆了 skill → 兩個互相依賴到無法單獨使用，每次用都要開兩份 |

**拆過頭與塞太滿違反的是同一條判斷標準。** 拆到讀者接不住線索，與塞到讀者讀不完，都是「agent 照正文走不完」；預算只是其中一端的代理指標，不是目標。為了達標而外移的內容正是造成閱讀割裂的那一批——一次實測，為壓進預算切成七份的 skill 過了三輪高階 reviewer 仍留五類缺陷（見 `CHANGELOG.md`）。**預算合格不代表拆分可用，兩者分別驗**（`references/splitting-an-existing-skill.md`〈兩種驗證，方法不同〉）。

**行數是官方合規項，不是體量判斷標準。** 每行字元數沒有上界，兩者在長行處脫鉤（實測有 245 行通過而 token 逾兩倍預算的檔）。**兩個都量、取較嚴者；行數通過只代表官方那一項沒違反。**

**第 3 層的單檔判斷標準是讀取方式，不是行數。** 判別依據是〈按需讀取〉路由表那一列的措辭：明令「讀這一份再繼續」者為整份執行，其餘為選段查閱（本 skill 的 references 現況全部是後者）。

| 讀取方式 | 量什麼 | 門檻 |
|---------|-------|------|
| 整份執行 | 全檔分段估算 | 5k tokens——它與 SKILL.md 一樣是整份進 context |
| 選段查閱 | 最大單節的分段估算 | 5k tokens |

**機械複製動作不算整份執行的判斷依據。** 模板／範本類檔案常見消費方式是複製（如 `cp`）一份到工作目錄後，逐欄位或逐章節查閱填寫——複製本身是一次性機械動作，不等於讀入做整體推理；此類檔案的讀取方式判定為選段查閱，量測其最大單節而非全檔。

**判定條件（三項皆須成立，缺一即仍判整份執行）**：

| 條件 | 說明 |
|---|---|
| 1. 消費流程已明寫 | 該 skill 的路由表或前置步驟文件已明寫此檔為「依欄位／章節查閱」，不是撰寫者事後片面宣稱 |
| 2. 有可定位的分段結構 | 章節或欄位可依編號或名稱直接對應查閱起點，不需通讀全文才能定位 |
| 3. 消費動作不要求跨節推理 | 讀者查閱單一章節或欄位即可完成當下任務，不需要比對其他章節內容才能下判斷 |

**Consequence**：不設判定條件，任何長文都能以「反正是查閱用」自稱豁免整份執行門檻，選段查閱的例外會變成迴避門檻的漏洞——那正是本判斷標準要防的另一端。

---

## 按需讀取

本檔留下的是路由與判斷標準——三層載入的預算、判斷內容去留的兩問、發布前的檢查清單。細節依你當下在做什麼取一份讀。

| 何時讀 | 檔案 | 涵蓋章節 |
|--------|------|---------|
| 寫或修 frontmatter：name、description、擴展欄位、觸發控制、命名 | `references/frontmatter-and-description.md` | 〈YAML Frontmatter〉〈Description 寫作（最重要的一節）〉〈命名規則〉〈觸發控制矩陣〉 |
| 寫或修 SKILL.md 正文：骨架、內容品質、引用形式、什麼不該放 | `references/writing-the-body.md` | 〈嚴禁清單 — 什麼不該放進 Skill〉〈Body 寫作〉（含〈外部引用：指名身分，不用檔案路徑〉）〈Claude Code 特有功能〉〈一則完整走查：兩個判斷標準只有一個附了可執行動作〉 |
| 從零建一個新 skill、判斷它屬哪一類型、決定內容該放 `scripts/`／`references/`／`assets/`、要廢止或遷移既有 skill、或引入他人的 skill | `references/creating-and-adopting-skills.md` | 〈檔案結構〉〈三類 bundled resource 的分工〉〈Skill 建立流程〉〈Skill 類型速查〉〈廢止與遷移〉〈安全考量〉 |
| 既有 skill 超出第 2 層預算、要外移內容 | `references/splitting-an-existing-skill.md` | 〈為什麼需要專屬程序〉〈補範例後超標：觸發條件與處置順序〉〈外移什麼、留什麼〉〈拆分特有的必查項〉〈兩種驗證，方法不同〉〈拆分特有的高頻缺陷〉〈結構約定〉〈收尾〉〈一則最小走查〉〈走完之後〉〈相關〉 |
| 決定工作流該給多少自由度或要不要設預設值、設計多步驟工作流、要進階範本、規劃測試方法、或 skill 行為不如預期 | `references/patterns-and-troubleshooting.md` | 〈Degrees of Freedom — 自由度匹配脆弱性〉〈Opinionated Defaults — 預設路徑引導正確做法〉〈Skill 設計模式〉（**控制流形狀**，要模板來這裡）〈選擇方法：Problem-first vs Tool-first〉〈測試方法〉〈迭代回饋指引〉〈常見問題排除〉 |
| 設計某個 skill 的範例、或判斷某處文字約束是否需要配範例 | `references/chained-examples.md` | 〈三段鏈式格式〉〈各段允許與禁止內容〉〈「何處需要範例」判斷標準〉〈「缺範例」與「缺引導」的分界〉〈完整示範〉〈語言專屬 skill 的例外：違規／修正程式碼對照〉〈與既有範例規格的相容判定〉 |
| 某個設計取捨說不出理由、想理解工具設計哲學與 agent 視角的演進，或需要可貼用的進階設計模式（評估驅動開發、Feedback Loop 等）與程式碼片段 | `references/seeing-like-an-agent.md` | 〈核心哲學〉〈Claude Code 團隊的演進教訓〉〈進階 Skill 設計模式〉（**設計方法論**，不是控制流模板）〈觀察 Claude 如何使用 Skill〉〈反模式〉 |

> **維護本表時**（讀者選路不需要這一段）：「涵蓋章節」欄的字串要與目標檔的 `##` 標題逐字相同且**雙向齊全**——每個名字都在目標檔存在（無死名），且目標檔的每個 `##` 都在這一欄出現（無孤兒節）。**兩個方向各驗一次**：只驗死名會漏掉無人指向的新節。


## 發布前檢查清單

### 結構

- [ ] 資料夾 kebab-case（推薦 gerund）
- [ ] `SKILL.md` 大小寫正確
- [ ] 無 `README.md`（任何層級，含子目錄）
- [ ] 無 `INSTALLATION_GUIDE.md` / `QUICK_REFERENCE.md`（`CHANGELOG.md` 不在此列，見 `references/writing-the-body.md` 的〈嚴禁清單〉）
- [ ] SKILL.md 全檔（含 frontmatter）通過兩個門檻（5k tokens 與 500 行）；各 reference 通過第 3 層的單檔判斷標準。門檻的適用對象、量測指令與分段估算表見〈Progressive Disclosure — 三層載入〉
- [ ] skill 帶 CLI 入口點時，另走 `skill-cli-sync-check` 規則。**不涵蓋**：本清單不問「CLI 行為變更後 SKILL.md 與 pm-rules 是否同步」，走完本清單全綠不代表那件事被問過

### YAML

- [ ] `---` 分隔符存在
- [ ] `name` kebab-case 且與資料夾同名
- [ ] `description` 第三人稱、< 250 **字元**、含觸發詞（量測指令見 `references/frontmatter-and-description.md`）
- [ ] 無角括號、無多行語法、無自訂屬性
- [ ] 引號閉合

### Body

- [ ] 無「When to Use This Skill」段（觸發資訊只放 description）
- [ ] 指令具體可操作、含錯誤處理
- [ ] 含至少 1 個範例
- [ ] 新增或修改範例的【驗證】段時，`chained-examples.md`〈驗證段機械檢查：依據句可溯性〉的逐問句表由非撰寫者複核「引文位置在範例之外？」與「判定詞逐詞對照」兩欄；撰寫者自檢無鑑別力，不可省略此步驟
- [ ] 每份 reference 一跳可達（判斷標準與例外見 `references/writing-the-body.md` 的〈Body 寫作〉）。機械檢查如下，每個命中逐一判定——說明用的示意路徑與被討論的對象不算違規，其餘即是

```bash
# 在該 skill 的目錄下執行
LC_ALL=C comm -13 <(grep -o 'references/[a-z-]*\.md' SKILL.md | LC_ALL=C sort -u) \
                  <(grep -rho 'references/[a-z-]*\.md' references/ | LC_ALL=C sort -u)
```

- [ ] 100+ 行**且被選段查閱**的 reference 有 TOC。整份執行者不適用，**SKILL.md 自身也不適用**（它整份進 context，不存在選段查閱情境；理由見 `references/writing-the-body.md` 的〈Body 寫作〉）
- [ ] 術語一致
- [ ] 無時間敏感字串
- [ ] **外部引用以身分指名，不寫檔案路徑**（見 `references/writing-the-body.md` 的〈外部引用：指名身分，不用檔案路徑〉）。機械檢查：`grep -nE '\`\.claude/[^\`]*\`' SKILL.md`，每個命中須屬該節列出的例外之一。**該指令抓不到裸檔名與反引號後非緊接 `.claude/` 的寫法**，這兩類要人工核

### 讀者可用性（新寫與**改寫**皆須）

**這一組驗的是「agent 照正文走得完嗎」，不是格式。** 前三組全綠而這一組沒跑，等於只驗了合規、沒驗可用。

- [ ] 已跑低階 model 讀者探針（`multi-round-review` skill 的 2-B⁗ frame）。規則類文件另加一欄「照這一節工作，我的第一個具體動作是什麼」——skill 正是規則類文件，讀它並照它執行的本來就是模型，探針量到的是實際執行輸入而非近似值
- [ ] **入口檔單獨跑一批**：正文能不能獨立支撐操作，只有在讀者拿不到 references 時才現形
- [ ] 派發前先登記「這份正文要讓讀者帶走哪幾件事」，回報後取差集。讀者不知道自己漏了什麼，直接問「你讀懂了嗎」問不出來
- [ ] 每一項 finding 先歸因再處置：在原文 grep 那個讀法對應的字串，找得到即為文章自己這樣寫的，不是讀者誤讀
- [ ] **修完再跑一次。** 歧義的修法有效與否，只有另一批獨立讀者判定得了；作者與同源 reviewer 讀自己的修法時會自動補完，看不出差別

**改寫既有 skill 時這一組不可略過**——改寫比新寫更容易留下割裂，而改寫者對這份 skill 已有脈絡，正是最讀不出缺口的那種讀者。

### 觸發測試

**本組目前不是閘門**：四項對走 git 同步的專案皆無可執行程序，勾選只代表「已知有這件事」，不代表已驗證。查詢形態與判斷標準見 `references/patterns-and-troubleshooting.md`〈測試方法〉與〈迭代回饋指引〉；description 側的診斷見 `references/frontmatter-and-description.md` 的〈觸發品質診斷〉。

- [ ] 主關鍵字觸發成功
- [ ] 改述查詢仍觸發
- [ ] 無關主題不觸發


---

版本紀錄在同目錄的 `CHANGELOG.md`。
