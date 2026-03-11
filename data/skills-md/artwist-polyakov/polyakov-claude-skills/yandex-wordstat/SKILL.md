---
name: yandex-wordstat
description: |
  Анализ поискового спроса через Yandex Wordstat API.
  Используй когда нужно: исследовать спрос, семантическое ядро,
  частотность запросов, сезонность или региональный спрос.
  Топ до 2000 запросов, ассоциации, динамика, экспорт CSV.
  Поиск упущенного спроса: анализ XLSX-выгрузки из Яндекс Директ,
  сегментация фраз, расширение семантики, сравнение OR-запросов.
  Triggers: упущенный спрос.
---

# yandex-wordstat

Analyze search demand and keyword statistics using Yandex Wordstat API.

## Config

Requires `YANDEX_WORDSTAT_TOKEN` in `config/.env`.
See `config/README.md` for token setup instructions.

## Philosophy

1. **Skepticism to non-target demand** — high numbers don't mean quality traffic
2. **Creative semantic expansion** — think like a customer
3. **Always clarify region** — ask user for target region before analysis
4. **Show operators in reports** — include Wordstat operators for verification
5. **VERIFY INTENT via web search** — always check what people actually want to buy

## CRITICAL: Intent Verification

**Before marking ANY query as "target", verify intent via WebSearch!**

### The Problem

Query "каолиновая вата для дымохода" looks relevant for chimney seller, but:
- People search this to BUY COTTON WOOL, not chimneys
- They already HAVE a chimney and need insulation material
- This is NOT a target query for chimney sales!

### Verification Process

For every promising query, ASK YOURSELF:
1. **What does the person want to BUY?** (not just "what are they interested in")
2. **Will they buy OUR product from this search?**
3. **Or are they looking for something adjacent/complementary?**

### MANDATORY: Use WebSearch

**Always run WebSearch** to check:
```
WebSearch: "каолиновая вата для дымохода" что ищут покупатели
```

Look at search results:
- What products are shown?
- What questions do people ask?
- Is this informational or transactional intent?

### Red Flags (likely NOT target)

- Query contains "для [вашего продукта]" — they need ACCESSORY, not your product
- Query about materials/components — they DIY, not buy finished product
- Query has "своими руками", "как сделать" — informational, not buying
- Query about repair/maintenance — they already own it

### Examples

| Query | Looks like | Actually | Target? |
|-------|------------|----------|---------|
| каолиновая вата для дымохода | chimney buyer | cotton wool buyer | ❌ NO |
| дымоход купить | chimney buyer | chimney buyer | ✅ YES |
| утепление дымохода | chimney buyer | insulation DIYer | ❌ NO |
| дымоход сэндвич цена | chimney buyer | chimney buyer | ✅ YES |
| потерпевший дтп | lawyer client | news reader | ❌ NO |
| юрист после дтп | lawyer client | lawyer client | ✅ YES |

### Workflow Update

1. Find queries in Wordstat
2. **WebSearch each promising query to verify intent**
3. Mark as target ONLY if intent matches the sale
4. Report both target AND rejected queries with reasoning

## Workflow

### STOP! Before any analysis:

1. **ASK user about region and WAIT for answer:**
   ```
   "Для какого региона анализировать спрос?
   - Вся Россия (по умолчанию)
   - Москва и область
   - Конкретный город (какой?)"
   ```
   **НЕ ПРОДОЛЖАЙ пока пользователь не ответит!**

2. **ASK about business goal:**
   ```
   "Что именно вы продаёте/рекламируете?
   Это важно для фильтрации нецелевых запросов."
   ```

### After getting answers:

3. **Check connection**: `bash scripts/quota.sh`
4. **Run analysis** using appropriate script
5. **Verify intent via WebSearch** for each promising query
6. **Present results** with target/non-target separation

## Scripts

### quota.sh
Check API connection.
```bash
bash scripts/quota.sh
```

### top_requests.sh
Get top search phrases. Supports up to 2000 results and CSV export.
```bash
bash scripts/top_requests.sh \
  --phrase "юрист дтп" \
  --regions "213" \
  --devices "all"

# Extended: 500 results exported to CSV
bash scripts/top_requests.sh \
  --phrase "юрист дтп" \
  --limit 500 \
  --csv report.csv

# Max results with comma separator
bash scripts/top_requests.sh \
  --phrase "юрист дтп" \
  --limit 2000 \
  --csv full_report.csv \
  --sep ","
```

| Param | Required | Default | Values |
|-------|----------|---------|--------|
| `--phrase` | yes | - | text with operators |
| `--regions` | no | all | comma-separated IDs |
| `--devices` | no | all | all, desktop, phone, tablet |
| `--limit` | no | API default (50) | 1-2000 (maps to API numPhrases) |
| `--csv` | no | - | path to output CSV file |
| `--sep` | no | ; | CSV separator (; for RU Excel) |

#### Result types: Top Requests vs Associations

The output contains two sections (both in stdout and CSV):

- **top** (`topRequests`) — queries that **contain the words** from your phrase, sorted by frequency. These are direct variations of the search query. Example: phrase "юрист дтп" → "юрист по дтп", "консультация юриста по дтп".
- **assoc** (`associations`) — queries **similar by meaning** but not necessarily containing the same words, sorted by similarity. These are semantically related searches. Example: phrase "юрист дтп" → "юридическая ответственность", "адвокат аварии".

**For analysis:** `top` results are your primary keyword pool. `assoc` results are useful for semantic expansion but often contain noise — always verify intent before including them.

#### CSV export details

CSV format: UTF-8 with BOM, columns: `n;phrase;impressions;type`.
When `--csv` is set, stdout shows first 20 rows per section; full data goes to file.

#### Working with large CSV exports

When `--limit` is set to a high value (e.g. 500-2000), use CSV export and read the file in chunks:
```bash
# Export 2000 results
bash scripts/top_requests.sh --phrase "query" --limit 2000 --csv data.csv

# Read first 50 rows (header + data)
head -n 51 data.csv

# Read rows 51-100
tail -n +52 data.csv | head -50

# Count total rows
wc -l < data.csv

# Filter only associations
grep ";assoc$" data.csv
```

This approach lets the agent process large datasets without flooding stdout.

### dynamics.sh
Get search volume trends over time.
```bash
bash scripts/dynamics.sh \
  --phrase "юрист дтп" \
  --period "monthly" \
  --from-date "2025-01-01"
```

| Param | Required | Default | Values |
|-------|----------|---------|--------|
| `--phrase` | yes | - | text |
| `--period` | no | monthly | daily, weekly, monthly |
| `--from-date` | yes | - | YYYY-MM-DD |
| `--to-date` | no | today | YYYY-MM-DD |
| `--regions` | no | all | region IDs |
| `--devices` | no | all | all, desktop, phone, tablet |

### regions_stats.sh
Get regional distribution.
```bash
bash scripts/regions_stats.sh \
  --phrase "юрист дтп" \
  --region-type "cities"
```

| Param | Required | Default | Values |
|-------|----------|---------|--------|
| `--phrase` | yes | - | text |
| `--region-type` | no | all | cities, regions, all |
| `--devices` | no | all | all, desktop, phone, tablet |

### regions_tree.sh
Show common region IDs.
```bash
bash scripts/regions_tree.sh
```

### search_region.sh
Find region ID by name.
```bash
bash scripts/search_region.sh --name "Москва"
```

## Wordstat Operators

### Quotes `"query"`
Shows demand ONLY for this exact phrase (no additional words).

```
"юрист дтп" → "юрист дтп", "юристы дтп"
             but NOT "юрист по дтп"
```

### Exclamation `!word`
Fixes exact word form.

```
!юрист → "юрист по дтп", "юрист москва"
         but NOT "юристы", "юриста"
```

### Combination `"!word !word"`
Exact phrase + exact forms.

```
"!юрист !по !дтп" → only "юрист по дтп"
```

### Minus `-word`
Exclude queries with this word.

```
юрист дтп -бесплатно -консультация
```

### Grouping `(a|b|c)`
Multiple variants in one query.

```
(юрист|адвокат) дтп → combined demand
```

### Stop words
**Always fix prepositions with `!`:**

```
юрист !по дтп    ← correct
юрист по дтп     ← "по" ignored!
```

## Analysis Strategy

1. **Broad query**: `юрист дтп` — see total volume
2. **Narrow with quotes**: `"юрист дтп"` — exact phrase only
3. **Fix forms**: `"!юрист !по !дтп"` — exact match
4. **Clean with minus**: `юрист дтп -бесплатно -онлайн`
5. **Expand**: synonyms, related terms, client problems

## Popular Region IDs

| Region | ID |
|--------|-----|
| Россия | 225 |
| Москва | 213 |
| Москва и область | 1 |
| Санкт-Петербург | 2 |
| Екатеринбург | 54 |
| Новосибирск | 65 |
| Казань | 43 |

Run `bash scripts/regions_tree.sh` for full list.

## Limits

- **10 requests/second**
- **1000 requests/day**

## Example Session

```
User: Найди запросы для рекламы дымоходов

Claude: Для какого региона анализировать спрос?
        И уточните — вы продаёте готовые дымоходы или
        материалы для их изготовления/утепления?

User: Москва, продаём готовые сэндвич-дымоходы

Claude: [Запускает анализ для региона 213]

        Нашёл запросы. Проверяю интент через веб-поиск...

        ✅ ЦЕЛЕВЫЕ (покупают дымоходы):
        - "дымоход сэндвич купить" — 450 показов
        - "дымоход для бани цена" — 380 показов

        ❌ НЕ ЦЕЛЕВЫЕ (покупают другое):
        - "каолиновая вата для дымохода" — ищут утеплитель, не дымоход
        - "монтаж дымохода своими руками" — DIY, не покупатели
        - "чистка дымохода" — уже владеют, сервисный запрос
```

### Key Points

1. **ВСЕГДА спрашивай регион и жди ответа**
2. **ВСЕГДА уточняй что именно продаёт клиент**
3. **ВСЕГДА проверяй интент через WebSearch**
4. **Разделяй отчёт на целевые/нецелевые с объяснением**

## Расширенные сценарии

### Поиск упущенного спроса
Анализ рекламной кампании Яндекс Директ для нахождения фраз, не покрытых текущей семантикой.
Требования: XLSX-выгрузка из Яндекс Директ (лист «Тексты»).
Подробнее: [MISSED_DEMAND.md](references/MISSED_DEMAND.md)
