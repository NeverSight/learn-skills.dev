---
name: cocos-creator-files
description: Use whenever editing, reading, generating, or reasoning about files inside a Cocos Creator 3.x project — .prefab, .scene, .meta, .anim, .mtl, .effect, Marionette .animgraph/.animask/.animgraphvari, 3D assets (.pmtl/.terrain/.mesh/FBX meta), .fnt, .plist, .pac, .atlas (Spine), DragonBones, .tmx/.tsx (TiledMap), AssetBundle directory configuration, and project directories (library/temp/build/profiles/settings/native) or build output. Trigger on Chinese or English mentions of cocos creator / cocos prefab / 預製件 / 場景 / 動畫 / 材質 / 著色器 / 圖集 / AssetBundle / meta file / UUID / fileId. Also trigger when the user asks to add a node, rename a prefab, adjust material parameters, tweak shader uniforms, insert animation keyframes, change bundle priority, write a .gitignore for a Cocos project, or fix broken __id__/__uuid__ references. The skill provides the golden safety rules (what's hand-editable vs. tool-generated vs. forbidden), the JSON + __id__ cross-reference protocol, the five look-alike id systems (uuid / compressed uuid / fileId / classid / shortId), and per-format editing playbooks so Claude doesn't corrupt UUIDs or reference graphs.
---

# Cocos Creator Files

> 教 Claude 如何安全地讀取、修改、新增 Cocos Creator 3.x（規則以 **3.8.7 引擎源碼**驗證）專案下的各種檔案。本 skill 的核心價值：避免 agent「自信地破壞」序列化資產——最常見的失敗模式是動了 `__id__` 但沒更新所有指標、改了 `.meta` 的 `uuid` 造成全專案斷鏈、或填錯 fileId 造成**靜默失效**（不報錯、跑起來才壞）。

---

## 何時觸發

- 使用者明確提到 Cocos Creator、Cocos 專案、或要你動 `assets/` 下的檔案
- 要改 `.prefab` / `.scene` / `.anim` / `.mtl` / `.effect` / `.meta` / `.animgraph` / `.animask` / `.pmtl` / `.terrain` / `.fnt` / `.plist` / `.pac` / `.atlas` / `.tmx`
- 看到 `__type__: "cc.*"`、`__id__`、`__uuid__` 的 JSON 結構
- 使用者說「加一個節點/預製件」、「調材質顏色」、「改 shader 參數」、「新增關鍵幀」、「設 AssetBundle 優先度」、「專案要進版控」
- 遇到 `library/` `temp/` `build/` `profiles/` `settings/` `native/` `local/` 時要判斷「要不要碰」

**即使使用者只說「改個顏色」或「加個按鈕到 prefab」，也應觸發**——這些看似簡單的操作，背後常涉及序列化圖的一致性維護。

---

## 三條黃金守則（記熟這三條，能避開 90% 的災難）

### 守則 1：`.meta` 是資源的身分證，不是設定檔
- **絕不修改** `uuid`、`ver`、`importer` 三個欄位（`ver` 是該 importer 自己的 schema 版本號，手動調高不會讓匯入器「升級」）
- `.meta` 必須與主檔同步搬移、同步改名、同步刪除
- 只有 `userData` 下的設定可以安全手改（例如 AssetBundle 參數）——但 `userData` 內部仍有分級，細節見 `references/meta-files.md`
- 如果需要給「新檔案」生成 `.meta`，**優先讓 Cocos Creator 編輯器自動產生**。只有在非互動批次工作才考慮手動產生

### 守則 2：序列化資產靠 `__id__` 互相引用；是不是「JSON 陣列」看結構不是看副檔名
- 判斷通則：**root 底下有沒有巢狀 CCClass 物件需要互相指涉**。
  - `.prefab` / `.scene` 因 Node/Component 樹恆為 **JSON 陣列**，位置索引 = `__id__` 的值
  - `.mtl` 欄位都是原始值或外部 uuid 引用，幾乎恆為**單一 JSON 物件**
  - `.anim` 空白樣板是單一物件；一旦有 track/keyframe 資料就變陣列
- 物件彼此用 `{ "__id__": N }` 指向同陣列內其他元素；外部資源引用用 `{ "__uuid__": "...", "__expectedType__": "cc.XXX" }`
- **改葉節點屬性（改數字、改字串、改 enum）安全**
- **動結構（新增/刪除/重排節點）高風險**，因為會牽動所有後面索引。若非必要，請使用者回編輯器操作；若必須用程式操作，讀 `references/serialized-assets.md` 的「結構性修改 SOP」（在場景放/覆寫 prefab 實例則見 `references/prefab-instances.md`）

### 守則 3：分清楚「可重建的生成物」與「長得像生成物的例外」
| 目錄 | 等級 | 版控 | 說明 |
|---|:---:|:---:|---|
| `library/` `temp/` | 🚫 不讀不改 | 不進 | 匯入快取/編譯暫存，疑似損壞可整刪重建 |
| `build/` | 🚫 不改 | 不進 | 發布輸出，每次 build 覆蓋（產物結構見 `references/build-output.md`） |
| `local/` | 🚫 | 不進 | 個人面板佈局快取，可安全整刪 |
| `profiles/` | ⚠️ | 不進 | 存**構建面板配置**與場景配置，官方不建議刪除——**別當快取整砍**，除非確定要重置構建設定 |
| `settings/` | ✅ 經編輯器面板改 | **要進** | 專案設定（`settings/v2/**`）；內部 schema 未經完整驗證，優先用編輯器面板 |
| `native/` | ✅ 可手動編輯 | **要進** | 唯一「長得像產物但必須進版控、允許手編」的目錄（原生工程與客製碼），規則與 `build/` 完全相反 |

如果使用者要你修改 `library/`/`temp/`/`build/` 的檔案，先停下來確認意圖——通常他真正想改的是 `assets/` 裡的原始檔。

---

## 判讀檔案的 3 步流程

### 1. 看副檔名 + 首行判型別
| 副檔名 | 首行/首物件長相 | 屬於哪類 |
|---|---|---|
| `.meta` | `{ "ver": "...", "importer": "..." }` | Meta 檔 |
| `.prefab` | `[ { "__type__": "cc.Prefab", ...` | 序列化資產（JSON 陣列） |
| `.scene` | `[ { "__type__": "cc.SceneAsset", ...` | 序列化資產（JSON 陣列） |
| `.anim` | `[ { "__type__": "cc.AnimationClip", ...`；空白樣板則是單一物件 | 序列化資產 |
| `.mtl` | `{ "__type__": "cc.Material", ...` | 序列化資產（單一物件） |
| `.animgraph` / `.animask` / `.animgraphvari` | 含 `cc.animation.*` 的 `__type__` | Marionette 動畫圖（見 `references/marionette.md`） |
| `.pmtl` | `{ "__type__": "cc.PhysicsMaterial"` 系 | 物理材質（見 `references/3d-physics-assets.md`） |
| `.effect` | `CCEffect %{` | Shader（YAML+GLSL） |
| `.fnt` | `info face="..." size=...` | 位圖字型（BMFont 純文字） |
| `.plist` | `<?xml ...` + `<plist>` | **雙重身份**：根層有 `frames`+`metadata`＝圖集🔒；`maxParticles` 等扁平參數＝2D 粒子⚠️ |
| `.pac` | `{ "__type__": "cc.SpriteAtlas" }` | Auto Atlas 佔位（參數在 `.pac.meta`） |
| `.atlas` | 純文字，第一行為 `.png` 檔名 | **Spine** atlas（非 Cocos 原生） |
| `.tmx` / `.tsx` | XML，`<map ...>` / `<tileset ...>` | TiledMap（見 `references/generated-assets.md`） |
| `.terrain` / `.mesh`+`.bin` | 二進位或 JSON+二進位強耦合 | 3D 資產，勿手改（見 `references/3d-physics-assets.md`） |
| `.ftpp` | `{ "meta": {...}, "images": [...] }` | Free Texture Packer 專案 `[未驗證]` |
| `.bmfc` | INI 風格或 XML | BMFont 產生器設定 `[未驗證]` |

### 2. 到下面的**速查表**查等級

### 3. 需要細節時，讀對應 reference
| 你在做什麼 | 讀這個 |
|---|---|
| 動 `.prefab` / `.scene` / `.anim` / `.mtl` 結構或屬性 | `references/serialized-assets.md` |
| 在場景放/覆寫 prefab 實例、手刻多實例測試場景、鑄 fileId | `references/prefab-instances.md` |
| 分不清 uuid / 壓縮 uuid / fileId / classid / shortId | `references/ids-and-uuids.md` |
| 動 `.meta`、或設定 AssetBundle | `references/meta-files.md` |
| 動 `.effect` shader、或材質套 effect（含 Surface Shader） | `references/shaders.md` |
| 動 Marionette `.animgraph` / `.animask` / `.animgraphvari` | `references/marionette.md` |
| 動 3D/物理資產（FBX meta、`.pmtl`、`.terrain`、`.mesh`、cubemap、3D 粒子欄位） | `references/3d-physics-assets.md` |
| 遇到 `.pac` / `.plist` / `.fnt` / `.atlas` / DragonBones / `.tmx` / `.labelatlas` | `references/generated-assets.md` |
| 處理 `library/` / `build/` 產物、library 損壞救援 | `references/build-output.md` |
| 動 `package.json` / `settings/` / `cc.config.json` / `build-templates/` | `references/project-config.md` |
| 要整張能改/不能改的分級表 | `references/decision-matrix.md` |

---

## 速查表：這個檔我能碰嗎？

| 檔名模式 | 可手改？ | 操作原則 |
|---|:---:|---|
| `assets/**/*.ts` | ✅ | 一般 TypeScript 編輯，但新增檔案務必產生 `.meta` |
| `assets/**/*.mtl` | ✅ | 改 `_props`、`_defines`、`_techIdx` 安全；**三個陣列不需要等長、不需要等於 pass 數**——`_props`/`_defines` 依 `propertyIndex` 定址、`_states` 依 pass 位置，缺項引擎自動補 `{}` 不報錯 |
| `assets/**/*.effect` | ✅ | YAML + GLSL 雙區塊；**絕不手寫 `void main()`**（框架自動包）；entry 寫法依架構分層（冒號語法 vs Surface Shader），見 `references/shaders.md` |
| `assets/**/*.prefab` | ⚠️ | 只改葉節點屬性（數字、字串、顏色）相對安全；新增/刪除節點建議回編輯器 |
| `assets/**/*.scene` | ⚠️ | 同 prefab；除非專門處理渲染環境，**不要動 `_globals`**；放/覆寫 prefab 實例見 `references/prefab-instances.md` |
| `assets/**/*.anim` | ⚠️ | 改 `_times`/`_values` 對齊升冪索引 OK（反序列化不驗證不變量，改完務必實際播放一次）；動軌道綁定請回編輯器 |
| `assets/**/*.{animgraph,animask,animgraphvari}` | ⚠️ | 變數預設值/transition 參數可改；動狀態機拓撲回編輯器（見 `references/marionette.md`） |
| `assets/**/*.meta` | 🔒 | **僅改 `userData`**，絕不動 `uuid` / `ver` / `importer` |
| `assets/**/*.{png,mp3,ogg,wav,jpg,webp}` | ❌ | 二進位資源不手改內容；要換就整檔換，並保留原 `.meta` 的 UUID |
| 音訊/影片的 `.meta` `userData` | ❓ | 欄位細節未經證實 `[未驗證]`，優先用編輯器面板 |
| `assets/**/*.plist` | 🔒/⚠️ | **先分流**：圖集 plist 🔒（手改 `<frame>` 會破壞索引，改圖重跑打包工具）；2D 粒子 plist ⚠️ 可安全改參數 |
| `assets/**/*.fnt` | 🔒 | 改**原始** `.fnt` 純文字（xoffset/xadvance 微調）安全且持久；改已匯入的 `.meta` `_fntConfig` 會被 reimport 覆蓋 |
| `assets/**/*.pac` | 🔒 | Auto Atlas 佔位，真正參數在 `.pac.meta` 的 `userData`；「重新產生」的工具就是 Cocos 編輯器本身 |
| `assets/**/*.atlas` | 🔒 | **Spine** 格式（3.8 與 4.2 格式不同）；修圖需重跑 Spine 匯出 |
| `assets/**/*.pmtl` | ✅ | 物理材質，欄位少且純 JSON，最安全的 3D 手改對象 |
| `assets/**/*.{terrain,mesh,bin,FBX,gltf}` | ❌ | 二進位/強耦合結構，回 DCC 工具或編輯器 |
| `assets/**/*.{tmx,tsx}` | ⚠️ | Tiled 工具產出 XML；手改後需回編輯器 reimport（XML 會整份內嵌進 library 產物） |
| `project.manifest` / `version.manifest`（熱更新） | ⚠️ | 常見手改對象（改伺服器位址/版本號），但 schema 未經本 skill 驗證 `[未驗證]`——改前備份 |
| `package.json` / `tsconfig.json` / `buildConfig_*.json` | ✅ | 可編輯；動 `creator.version` 要先與使用者確認 |
| `library/**` `temp/**` `build/**` `local/**` | 🚫 | 禁止編輯、禁止 commit；疑似損壞可整刪重建 |
| `profiles/**` | ⚠️ | 不進版控但**別當快取整砍**（存構建面板配置） |
| `settings/**` `native/**` | ✅ | **要進版控**；`settings/` 優先經編輯器面板改、`native/` 允許手動編輯 |

**圖例**：✅ 可改｜⚠️ 謹慎（看情況）｜🔒 僅改指定欄位｜❌ 內容不改，要換就整檔換｜🚫 禁止觸碰｜❓ 未驗證

---

## 工作流：6 種最常見情境 SOP

### 情境 A：使用者說「改 prefab 裡某個 Label 的文字/顏色」
1. `Read` 該 `.prefab`
2. 搜尋 `"__type__": "cc.Label"` 找到目標元件
3. 就地改 `_string`（文字）或 `_color`（內嵌 `cc.Color` 物件）
4. **不動** `__id__`、`_parent`、`_children`
5. 提醒使用者回編輯器讓它 refresh prefab（觸發 meta 更新）

### 情境 B：使用者說「新增一個節點到 prefab」
1. **預設拒絕程式化操作**，改建議使用者回編輯器拖拉，因為：
   - 需要在陣列末端 append 新 Node + 相關 Component + 對應的 `cc.PrefabInfo`/`cc.CompPrefabInfo`
   - 要更新父節點的 `_children` 加入新 `__id__`
   - 要為新節點產生穩定的 `fileId`（否則 prefab 實例化會亂）
2. 若使用者堅持程式化修改，閱讀 `references/serialized-assets.md` 的「結構性修改 SOP」

### 情境 C：使用者說「調材質顏色/透明度」
1. `Read` `.mtl` 檔（單一 JSON 物件）
2. 改 `_props[<propertyIndex>]` 內的 uniform 值（如 `_color`）——多數 effect 所有 pass 共用 `propertyIndex` 0
3. 若要切換 shader 分支，改 `_defines[<propertyIndex>].<DEFINE>` 的 `true/false`
4. **絕不動** `_effectAsset.__uuid__`（除非使用者明確要換 shader）
5. **陣列長度與 pass 數不同是正常現象**（官方出貨的 standard-material.mtl 就是 6 pass 配空 `_defines`）——不要「補齊」陣列；除非要新增某個 propertyIndex 的非預設覆寫值，才加對應槽位
6. 細節見 `references/shaders.md`

### 情境 D：使用者說「改 shader 的顏色預設值/新增一個 pass」
1. `Read` `.effect`，認出 `CCEffect %{...}%`（YAML）和 `CCProgram name %{...}%`（GLSL）區塊
2. 改 uniform 預設值：動 YAML 的 `properties.<name>.value`
3. 新增 pass 前先判斷架構（讀 CCProgram 的 `#include` 內容）：冒號語法 shader 的 entry 回傳 `vec4`；Surface Shader 則走 `surf()`/chunk 骨架——**兩種都絕不手寫 `void main()`**（框架自動包）；遇到不認得的骨架不要硬改，見 `references/shaders.md`
4. 若新增 `#pragma define-meta` 或 `#if` 分支，記得同步 define 名稱
5. 新 pass 若沿用既有 `propertyIndex`，各 `.mtl` 通常**不需要**跟著改

### 情境 E：使用者說「把這個資料夾變成 AssetBundle / 調 bundle 優先度」
1. `Read` 該資料夾的 `.meta`（`importer: "directory"`）
2. 在 `userData` 裡設：
   ```json
   {
     "isBundle": true,
     "bundleName": "MyBundle",
     "priority": 1,
     "compressionType": { "web-mobile": "merge_all_json" },
     "inlineSpriteFrames": { "web-mobile": true },
     "isRemoteBundle": { "web-mobile": false }
   }
   ```
3. `priority` 範圍 0–20（內建 `main`=7、`resources`=8、`start-scene`=20、`internal`=21 固定不可調）。**不同**優先級的共享資源存進最高優先級那個；**相同**優先級則各 bundle 各自複製一份、不去重 `[社群]`。低優先級 bundle 只存 redirect 記錄——目標 bundle 未先 `loadBundle()` 會直接拋 `Please load bundle X first` 例外
4. `compressionType` 值：`none` / `merge_depend`（預設）/ `merge_all_json` / `zip` / `subpackage`
5. 3.8+ 的 Bundle 設定可能已由「專案設定 → Bundle 配置」面板接管，手改 `.meta` 前先確認專案用哪一套；細節見 `references/meta-files.md`

### 情境 F：使用者說「在場景放好幾個同一個 prefab 的實例 / 改某顆實例上的某個屬性」
1. 場景裡的 prefab 實例是**摺疊**的（`cc.Node` + `cc.PrefabInfo` + `cc.PrefabInstance` 三件組），不展開
2. 改某顆實例的值 = 在它的 `PrefabInstance.propertyOverrides` 加一筆 override，**不是**去改 prefab 本體
3. ⚠️ 最易踩雷：override 的 `cc.TargetInfo.localID` —— 改**節點** transform 填該節點的 fileId、改**元件** @property 填該元件的 `cc.CompPrefabInfo.fileId`（填錯只會**靜默失效**、不報錯）；巢狀 prefab 要用多元素路徑陣列
4. 新增實例還要同步更新父節點 `_children` 與場景 `root:null` PrefabInfo 的 `nestedPrefabInstanceRoots`（漏登錄＝雙向靜默失效）；新 fileId 用 `scripts/compress_uuid.js` 鑄
5. 完整三件組形狀、id 種類、唯一性規則與手刻 SOP 見 `references/prefab-instances.md`

---

## 常見錯誤模式（Claude 常犯的）

每次動手前掃一遍這份清單，確認自己沒踩到：

1. **憑記憶改 UUID** — 永遠不要更動 `.meta` 的 `uuid`，也不要「猜」一個 UUID 填進 `__uuid__`
2. **刪 JSON 陣列中間元素但沒重排 `__id__`** — 陣列 index 變動後，所有指向後面元素的 `__id__` 都要更新
3. **在 `.effect` 裡寫 `void main()`** — 無論冒號語法還是 Surface Shader，使用者路徑都不該手寫 main；Cocos 一律自動包
4. **把 `.mtl` 的 `_defines`/`_props`/`_states` 「補齊」到 pass 數** — 三陣列長度與 pass 數不同是**正常現象**，硬補反而引入垃圾覆寫；`_props`/`_defines` 依 `propertyIndex` 定址、`_states` 依 pass 位置
5. **手改 `.plist`(圖集) / `.fnt`(已匯入 meta) / `.atlas`(Spine) 的座標** — 這些來自打包工具，會被重打包/reimport 覆蓋；改原始檔或改工具設定重跑
6. **在 `library/` 下 edit** — 那是生成物；你改了也會被下次 refresh 覆蓋掉
7. **新增 `.ts` 沒有伴生 `.meta`** — 會造成引擎找不到 class 註冊
8. **複製 `.prefab` 連 `.meta` 一起複製** — 真正的災難是**資產 uuid 衝突**（`.meta` 的 uuid 必須重生）；prefab 內部的節點/元件 fileId 只需「同一份 prefab 資產內」唯一，跨資產相同不會互相干擾。要留意 fileId 唯一性的場景是：同一場景放多顆同 prefab 實例時，每顆 `PrefabInstance.fileId` 必須互不相同
9. **改 `creator.version`** — 這是專案鎖定的 Cocos 版本；動前先問使用者
10. **五種「長得像 uuid 的字串」混用** — 標準 uuid(36)／壓縮 uuid(22)／fileId(22，不透明 token)／classid(23，`keep=5` 為經驗值未經樣本驗證)／子資產 shortId(5，`6c48a`=texture、`f9941`=spriteFrame，**固定慣例值不能捏造**)。全表見 `references/ids-and-uuids.md`
11. **prefab 實例的「元件 override」把 `localID` 填成節點 fileId** — 元件 @property 的 override 要填**該元件的 `cc.CompPrefabInfo.fileId`**；填成節點 fileId 會讓覆寫**靜默失效**（見 `references/prefab-instances.md`）
12. **鏡射既有測試場景去測「另一個」prefab，只換了 `asset.__uuid__`** — 綁在「被嵌入 prefab 根節點」上的 `cc.PrefabInfo.fileId` 與節點 override 的 `cc.TargetInfo.localID` 也必須換成 **B 的根節點 fileId**；漏換 → 靜默失效。撈根節點 fileId 別用「第一個 cc.PrefabInfo」（多節點 prefab 它可能在陣列最後）。詳見 `references/prefab-instances.md` §9

---

## 3.8.x 版本敏感行為（使用者專案可能停在 3.8.0–3.8.6）

| 版本切點 | 變更 | 影響 |
|---|---|---|
| 3.8.5 | 移除 tilemap 自動 extrude `[社群]` | 升級後 TiledMap 出現黑邊縫隙 |
| 3.8.6 | library 產物 `.cconb` → `.bin` `[社群]` | 判讀 library 檔名時注意 |
| 3.8.6→3.8.7 | auto-atlas 對 Sprite 掛圖行為緊縮 `[社群/源碼]` | `.pac` 相關行為跨版本不同 |
| 3.8.x | Spine 3.8 與 4.2 **二擇一**（專案級設定） | `.skel`/`.atlas` 格式必須匹配所選 runtime |

對非 3.8.7 的專案套用本 skill 規則時，遇到上表領域先確認版本。

## 本 skill 的已知邊界（誠實聲明）

以下格式**未經源碼/樣本驗證**，不要憑印象指導手改，優先導回編輯器面板並提醒使用者備份：音訊/影片 `.meta` 的 `userData` 細節、熱更新 manifest schema、壓縮紋理 preset 內部結構、`settings/v2/packages/*.json` 逐檔 schema。此外：編輯器**存檔端**（writer）閉源，所有「編輯器重存會不會正規化你手改的內容」的描述皆屬實測歸納而非源碼保證。

---

## 重要：給 `Edit` 工具的檢查清單

在對 Cocos 序列化檔案呼叫 `Edit` 之前，心算跑一次：

- [ ] 我改的是葉節點屬性（數值、字串、布林、顏色）還是結構？
- [ ] 如果是陣列 index 有變動，我有更新**所有**相關的 `__id__` 嗎？
- [ ] 我有沒有不小心碰到 `uuid` / `__uuid__`？
- [ ] （材質）`_props`/`_defines` 的 index 對到正確的 `propertyIndex` 了嗎？`_states` 的 index 對到 pass 位置了嗎？（**不要**去「補齊」長度）
- [ ] （prefab/scene）我填的 fileId/localID 指得到目標嗎？填錯不報錯、只會靜默失效
- [ ] 這個檔屬於生成物目錄嗎？

任何一項不確定——**停下來跟使用者確認，而不是猜**。修改 Cocos 檔案的成本不對稱：改對沒感覺，改壞整個專案開不起來。

---

## 推薦閱讀順序

第一次觸發本 skill 時，建議先掃過：
1. 這份 SKILL.md（你現在在讀）
2. `references/decision-matrix.md` — 完整的能改/不能改分級表
3. 若任務涉及任何 id 字串：`references/ids-and-uuids.md`

接著根據當前任務再挑對應 reference 深讀即可。
