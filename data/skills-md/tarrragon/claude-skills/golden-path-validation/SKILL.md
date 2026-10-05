---
name: golden-path-validation
description: "驗證一份 setup 指引 / runbook / onboarding / bootstrap 是否「陌生人每次照做都能完整重現」的方法：派無前置知識的冷讀代理人、在可拋棄乾淨環境實際照指引執行，抓文件 fact-check 放過、只有實機跑才現形的硬編假設 / 環境漂移 / verifier 自己的 bug。五階段：完整性稽核 → 自動化 verify → 冷讀代理人實機執行 → 乾淨環境 re-verify → 發現回收。觸發詞：驗證 setup 指引、runbook 驗證、onboarding 測試、bootstrap 測試、golden path / paved road 驗證、每次照做都能重現、冷讀測試、cold-read、陌生人照做、實機執行驗證、setup guide validation、原生非模擬、verifier 也要被驗。Trigger when validating that a follow-along setup/onboarding/bootstrap guide actually works for a newcomer, via cold-read agents executing it in disposable clean environments."
license: MIT
metadata:
  version: 1.3.2
  category: engineering-methodology
---

# Golden Path Validation：冷讀代理人實機驗證一份 setup 指引

一份 setup 指引 / runbook / onboarding 文件 / bootstrap 腳本,是否真的「陌生人每次照做都能完整重現」,靠作者自己讀不出來——作者知道太多沒寫進去的前提。這個 skill 的方法是:**派沒有前置知識的冷讀代理人,在可拋棄的乾淨環境裡實際照著指引執行,證明它成不成立**。文件層的 fact-check 會放過硬編假設、環境漂移、缺步驟;只有讓陌生人真的在乾淨機器上跑一次,這些才現形。

核心命題:**執行勝過審讀**。指引讀起來通順、每條指令看似正確,不代表照著跑得通。冷讀 + 實機執行同時抓兩種文件審查抓不到的東西——「陌生人看不懂 / 卡在哪」(理解層)與「照做會爆什麼」(執行層)。

## 適用情境

- 寫完 / 稽核完一份「照著做就能到位」的指引:安裝 runbook、onboarding、getting-started、bootstrap 腳本、paved road / golden path 的有序路徑
- 要在發布前證明「每次照做都能重現」、而不只是「作者跑得起來」
- 指引跨多種目標環境(發行版 / 架構 / 權限情境),要確認每種都走得通
- 有可拋棄的乾淨環境(容器 / VM / 一次性雲端機)可以重複起、重複丟

不適用:

- 純概念 / 敘事文件(沒有「照著執行」的步驟可跑)
- 一次性、不會有第二個人照做的私人筆記
- 需要真實外部狀態(付費帳號、實體硬體、線上服務)且無法在乾淨環境重現的流程——那類只能標 caveat、不能冷讀實測

## 方法(五階段)

### 階段 1:golden-path 完整性稽核(執行前)

先對指引本身做「陌生人每次照做都完整」的稽核,缺口就是後面測試的靶。逐項問:

- **起始前提有沒有講全**:陌生人在哪個狀態起步(有 shell?有網路?能變 root?)、要先有什麼工具才能開始(常見漏掉:clone repo 需要的工具、由 repo 自己安裝造成先有雞問題)。
- **是不是單一有序路徑**:是「照這個順序做」的 runbook,還是 reference 導向、逼讀者自己拼湊順序。
- **每步有沒有明確產物**:這一步決定什麼、走完手上有什麼。
- **完整涵蓋**:系統層 / 機密填寫 / 驗證步驟有沒有在主路徑裡,還是散在別段或缺席。
- **有沒有 escape hatch**:哪裡可以偏離、偏離後還能不能回到可重現狀態。

### 階段 2:把驗證自動化(若指引還沒有)

指引該有一步「怎麼確認成功了」。做成一支 read-only、可重跑的 verify 腳本,把「跑完到底成不成」變成機械判斷,而不是肉眼猜。**但 verifier 自己也是一隻會讀錯層的眼睛**(見 `references/principles/verify-the-verifier.md`):一個 naive 檢查可能對健康的環境給假陰性。先拿一個「已知正確」的環境跑 verifier、確認它報 pass,再信它的 fail。

### 階段 3:冷讀代理人實機執行測試(核心)

派多個 fresh 代理人(無你的對話脈絡),每個是一個剛發現這份指引的陌生人。關鍵紀律:

- **只照指引、不預讀內部**:真實使用者照 runbook 做、不會先研究底層腳本。代理人也一樣——只有指引本身卡住它、才去翻腳本,並記下「指引沒講、得翻腳本才知道」。
- **真的執行、不只讀**:在可拋棄的乾淨環境(每個目標一個 fresh 容器 / VM)實際跑,不是評論可讀性。怎麼起這種環境、bare vs provisioned 之分、容器專屬的坑、以及一個公開的 reference implementation,見 `references/disposable-environment.md`。
- **回報四層**:①理解——每步光看文字懂不懂要做什麼、哪裡要猜;②執行——實際跑發生什麼、哪裡失敗 / hang / 報錯、做了哪些指引沒寫的動作才過關;③verify 結果——PASS/FAIL 跟實際環境相不相符(抓 verifier 自己的誤報);④意想不到的狀況。
- **測完清乾淨、不動宿主機**。

代理人配置要涵蓋真實目標:每個發行版 / 架構 / 權限情境各一個執行型,外加一個純理解冷讀(不執行、只判「光讀懂不懂」)。**階段 1 稽核抓到的可疑步驟與缺口,派代理人時寫進 prompt、要它們特別留意那幾步**——把稽核發現當成測試的靶,而不是讓代理人從零盲測。詳細 agent prompt 結構見 `references/cold-read-agent-protocol.md`。

### 階段 4:修 + 乾淨環境 re-verify

修實測抓到的 bug 後,在**新的乾淨環境**重跑確認(不是在已被前一次執行汙染的那個)。跨代理人 convergence(多個代理人都中的同一個 bug)優先序最高。

環境保真度的兩條硬規則(見 `references/principles/native-not-emulated.md`):

- **在目標架構的原生環境跑**:模擬(qemu)會給假通過 / 假失敗——sandbox、seccomp、LSM、syscall 相關行為在模擬層跟原生不同。arch 敏感的驗證別信模擬環境的綠燈或紅燈。
- **隔離容器專屬 quirk**:容器的安全 profile 跟真機不同,有些失敗只在容器出現(真機不受影響)。別讓這種 quirk 遮住「真正的修復到底有沒有效」——用逃生閥(如放寬對應限制)把 quirk 隔離掉,才驗得到指引本身的修復。

### 階段 5:發現回收

實測抓到、會在別的情境重演的發現,回收進文件 / 觀念 / 可複用的 skill,不要只留在 commit message。通則性的洞見(如「執行勝過審讀」「原生非模擬」「verifier 也要被驗」)放進跨專案帶得走的地方 ROI 最高。

## 反覆陷阱

- **用審讀代替執行**:只讀指引、不實跑,就漏掉硬編假設(如寫死 `sudo` 在 root 環境 exit 127)、套件 / 相依隨時間漂移、verify 工具自己的 bug——這些都是文件 fact-check 過、實機才爆的。
- **代理人先讀內部再「照做」**:預讀腳本的代理人已經不是冷讀者,會腦補掉指引的缺口、測不出陌生人真正會卡的地方。
- **在模擬架構上測、卻信結果**:qemu 的假通過讓你以為過了、假失敗讓你追不存在的 bug。
- **把 verifier 當成不會錯**:naive 檢查對上真實部署形態(如目錄摺疊、多路徑)會假陰性,verifier 沒先被驗就上場。
- **在被汙染的環境修完就收工**:修完要在乾淨環境重跑,否則你驗的是「這個被手動補過的環境」、不是「陌生人的乾淨環境」。
- **容器 quirk 遮住真修復**:容器專屬的失敗(跟真機無關)蓋掉「指引的修復有沒有生效」,沒隔離就誤判修復無效。

## 跟其他 skill 的關係

- [`verification-driven-cli`](../verification-driven-cli/SKILL.md) 寫 CLI 工具教學文章、用 Docker fixture 逐工具驗證(偏「作者自己驗單一工具」);本 skill 偏「派陌生人端到端驗一整份 follow-along 指引」。兩者共享「執行勝過審讀」與「模擬環境不可信」的紀律。
- [`multi-round-review`](../multi-round-review/SKILL.md) 用多輪 frame 切換審查「文字寫得好不好」;本 skill 驗「照著做跑不跑得起來」。前者不執行、後者一定執行。可以先 frame 審查文字、再冷讀實測執行。

版本紀錄在同目錄的 `CHANGELOG.md`。
