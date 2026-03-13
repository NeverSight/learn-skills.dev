---
name: treebuy-best-present
description: "依一句話描述找合適的小樹購禮物。Use when: (1) 用戶說「幫我找禮物」「推薦適合的商品」「送○○什麼好」，(2) 需要依對象/場合/預算篩選多樣商品，(3) 想從 treebuy.com 找禮物選項。Triggers on: 找禮物, 推薦禮物, 送禮, 生日禮物, 母親節禮物, 小樹購禮物, best present, gift recommendation。"
---

# treebuy-best-present

**PREREQUISITE:** Read [../treebuy-shared/SKILL.md](../treebuy-shared/SKILL.md) for installation, authentication, and security rules.

依一句話描述，從小樹購（treebuy.com）找出類別多樣的合適禮物。

## 安裝

```bash
npx skills add https://github.com/nandemo-agent/treebuy-cli --skill treebuy-best-present
```

## Agent Workflow

### Step 1 — 分析用戶描述

從用戶描述解析：
- **對象**：媽媽、男友、同事、朋友…
- **場合**：生日、母親節、婚禮、過年…
- **喜好/興趣**：咖啡、登山、美妝…
- **預算**：明確金額 or 從描述推測

### Step 1.5 — 關係敏感情境檢查（必做）

若描述包含以下語境（例如：減肥、體重、身材、健康焦慮），先套用「低壓力送禮原則」：

1. **優先推薦支持型禮物**：舒壓、睡眠、補水、健康飲食工具、日常陪伴感。
2. **避免羞辱感禮物**：除非用戶明確指定，避免把「體脂秤、減脂課程、塑身工具」放在首選。
3. **文案避免評價外貌**：不要使用「該瘦了、控制身材」等語句。
4. **給選擇，不下指令**：用「可以考慮」而不是「你應該買」。

> 目標：讓禮物傳達「支持與陪伴」，不是「被要求改變」。

### Step 2 — 組出搜尋關鍵字（agent 自行思考）

生成 5–8 組不重疊類別的繁中搜尋關鍵字，確保涵蓋多種面向：

| 面向 | 範例關鍵字 |
|------|-----------|
| 美妝保養 | 保養品、香水、護手霜 |
| 食品飲品 | 茶葉禮盒、咖啡豆、零食禮盒 |
| 生活家居 | 香氛蠟燭、馬克杯、保溫杯 |
| 配件服飾 | 絲巾、皮夾、帽T |
| 健康運動 | 按摩器、運動水壺、保健食品 |

> 類別不要重疊，讓推薦結果多樣。

### Step 3 — 呼叫 CLI

```bash
treebuy-cli best-present "<用戶原始描述>" \
  --keywords "<kw1>,<kw2>,<kw3>,..." \
  --budget <number> \
  --count <number> \
  --json
```

**旗標說明：**

| 旗標 | 說明 | 預設 |
|------|------|------|
| `--keywords` | 逗號分隔，最多 10 組，每組 ≤ 30 字 | （不設則用規則式） |
| `--budget` | 單件預算上限（NT$） | 從描述解析 |
| `--count` | 推薦幾件 | 5 |
| `--json` | 完整 JSON 輸出（含 meta） | — |
| `--ndjson` | 每筆一行 NDJSON | — |
| `--fields` | 只輸出指定欄位（作用於 recommendations[]） | 全部 |

### Step 4 — 輸出規範（user-facing 回覆）

**MUST** 每筆推薦包含以下資訊：

| 欄位 | 說明 |
|------|------|
| `name` | 商品名稱（主體） |
| `selling_price` | 售價（NT$） |
| `product_url` | 可點擊的商品頁連結 |
| `reason` | 一句話推薦理由，連結用戶的需求/場合/對象 |

**SHOULD**：`sku` 置於次要資訊，不作為回覆主體。

#### ✅ Good response

```
1. 光影香氛蠟燭（NT$ 499）
   送媽媽的母親節禮物，溫暖氛圍感十足，適合居家放鬆。
   👉 https://treebuy.com/product/S251021874L1

2. 棉質絲巾（NT$ 580）
   實用又有質感，媽媽日常搭配或外出都適合。
   👉 https://treebuy.com/product/S23020356755
```

#### ❌ Bad response

```
1. SKU: S251021874L1, price: 499, category: 119
2. S23020356755 - 棉質絲巾 - 580元
```

---

### Step 5 — agent 自行補上 reason

CLI 輸出的 `recommendations[]` 不含 `reason`，由 agent 根據以下資訊生成：
- 用戶的原始描述（對象/場合/喜好）
- 商品的 `name`、`brand`、`selling_price`
- 來源 `source_keyword`（反映搜尋意圖）

**reason 撰寫原則：**
- 繁中，≤ 30 字
- 明確連結用戶需求（「送媽媽」「適合登山」「婚禮伴手禮」）
- 不要空泛（避免「品質不錯」「值得購買」）

---

## 完整範例

```bash
# 範例 1：母親節禮物
treebuy-cli best-present "我想送我媽一個母親節禮物，預算 1000" \
  --keywords "保養品,香氛蠟燭,茶葉禮盒,按摩器,限定禮盒" \
  --budget 1000 --count 5 --json

# 範例 2：登山愛好者
treebuy-cli best-present "朋友喜歡登山，預算 2000" \
  --keywords "登山背包,保溫水壺,運動襪,能量補給,登山帽" \
  --budget 2000 --json

# 範例 3：只看 name/price/url
treebuy-cli best-present "送同事禮物 500 元以內" \
  --keywords "馬克杯,茶葉,零食禮盒,文具,手帕" \
  --budget 500 --fields name,selling_price,product_url --ndjson
```

## 推薦排序策略（建議）

預設可用以下權重排序候選商品：

- `fit_to_context`（是否符合對象/場合）：40%
- `emotional_safety`（是否低壓力、無羞辱感）：30%
- `price_fit`（是否貼近預算）：20%
- `novelty`（是否有驚喜感）：10%

若是「親密關係 + 健康/身材」情境，將 `emotional_safety` 提高至 45%。

## 錯誤處理

- `--keywords` 驗證失敗 → stderr + exit 1（不 silently fallback）
- 找不到符合預算的商品 → stderr + exit 1
- 單一 keyword 搜尋失敗 → 跳過（不影響其他 keyword）

## Output Fields 參考

`recommendations[]` 的可用欄位（供 `--fields` 篩選）：

| 欄位 | 型別 | 說明 |
|------|------|------|
| `sku` | string | 商品 SKU（次要資訊） |
| `name` | string | 商品名稱 |
| `selling_price` | number | 售價 |
| `product_url` | string | 商品頁連結（`treebuy.com/product/<sku>`） |
| `source_keyword` | string | 來源關鍵字 |
| `category_key` | string | 商品分類 key |
| `in_stock` | boolean | 是否有庫存 |
| `brand` | string | 品牌 |
| `image_url` | string | 商品圖片 URL |
