---
name: kalodata
description: >
  Use for TikTok Shop market data: trending products, top creators, shop/product
  sales and revenue, viral videos, livestreams, category rankings — 选品、带货达人、
  店铺/商品销量、爆款视频、直播带货、TikTok 小店数据. Answers come from KaloData via the bundled
  `kalo` CLI (Python, zero install). Use whenever the user researches TikTok Shop, even if
  they never say "kalodata".
---

# KaloData TikTok Shop analytics (`kalo`)

TikTok Shop e-commerce analytics from KaloData — rankings and details for products, shops, creators, videos, livestreams and categories.

## Run

The CLI ships inside this skill (`scripts/kalo.py`, Python 3.11+ stdlib only — nothing to install):

```sh
python3 <this-skill-dir>/scripts/kalo.py product rank --region US
```

All examples below write `kalo` as shorthand for `python3 <this-skill-dir>/scripts/kalo.py`.

Output is TOON (token-oriented) on stdout; add `--json` to any command for raw JSON.
Errors are structured on stdout with actionable `help:` lines. Exit codes: 0 ok, 1 error, 2 usage.

## Setup — check this before the first query

Every command needs a KaloData API key (sent as the `secret-key` header). Before the first
query of a session run `kalo config` and look at `api_key`. If it says `missing`, stop — don't
guess a key and don't retry the query. Walk the user through these three steps and wait:

1. **Get a key** — sign in at https://www.kalodata.com/open-center/account and click
   *generate key*. No account yet? Register at https://www.kalodata.com/open-center/home first.
   If they already call the KaloData API on credit-based billing, that same key works here —
   no new key needed.
2. **Save it** — `kalo config set --key <API_KEY>` (stored in `~/.config/kalodata/config.toml`,
   mode 0600), or set `KALODATA_API_KEY` in the environment.
3. **Credits** — every query spends Kalo Credits. Measured costs per call:

   | call | credits |
   |---|---|
   | any rank or detail lookup | 0.2 |
   | `product images` | 0.01 |
   | `creator images` | 0.1 |
   | `product specs` | 0.1 |
   | `video url` | 0.5 |
   | `product comments` (only when the upstream cache refreshes) | 1 |
   | `credit balance`, `credit logs` | free |

   Costs were measured against production; rank/detail lookups bill 0.2 flat under this skill's
   `source-type: SKILL` header. A playbook fans out into many calls, so it lands at 1–2 credits.
   `kalo credit` shows the remaining balance; top up at https://www.kalodata.com/pricing.

Don't announce or ask about credit costs for queries the user asked for — just run them. Bring
up cost only when the balance may not cover a big fan-out (a data-gathering playbook, dozens of detail lookups:
check `kalo credit` first), or when the user asks.

## Commands

| command | what |
|---|---|
| `kalo product rank` | top products; --category --keyword --price --launch --shop --creator |
| `kalo product detail <id...>` | price range, shop id, revenue trend, product description |
| `kalo product comments <id...>` | review insight: pain points, positives, usage scenarios (1 credit per refresh) |
| `kalo product specs <id...>` | selling points (highlights) and spec attributes; --lang zh-CN translates |
| `kalo product images <id...>` | product gallery image URLs |
| `kalo shop rank` | top shops; --type BRAND\|RETAILER --keyword |
| `kalo shop detail <id...>` | revenue split, top product ids |
| `kalo creator rank` | top creators; --followers --engagement --product |
| `kalo creator detail <id\|@handle...>` | contact email/handle, GPM, trend; handle match is fuzzy — verify the returned creator_handle |
| `kalo creator images <id...>` | avatar URLs, up to 100 creator ids |
| `kalo video rank` | top shoppable videos; --product --creator --keyword --ai |
| `kalo video detail <id...>` | full video metrics + trend |
| `kalo video url <id...>` | playable mp4 URLs |
| `kalo live rank` | top livestreams; --keyword |
| `kalo live detail <id...>` | viewers, GPM, top product ids |
| `kalo category rank` | top categories; --level 1\|2\|3 |
| `kalo category detail <id...>` | category revenue split + trend |
| `kalo category search <kw>` | resolve category ids by keyword |
| `kalo credit` | remaining credit balance for this key |
| `kalo credit logs` | what credits were spent on; --range --type --page |
| `kalo config` | show/set credentials and defaults |

## Conventions

- All list commands take --region --range --page (1-5) --limit (5-100) --sort --asc --fields --json
- Regions: US GB ID TH VN PH MY SG JP MX DE IT FR ES BR; ranges like last7Day, last30Day, yyyy-MM, or yyyy-MM-dd~yyyy-MM-dd
- Numeric ranges are "min-max" with both ends numeric, e.g. --revenue 1000-50000
- Add --images on product/shop rank or product detail to include image URLs; creator avatars come from `kalo creator images` (creator rank has no image column)
- Signed media URLs (`product images`, `creator images`, `video url`) expire about 5 minutes after
  the call — hand them to the user or download them now, never cache them
- Run `kalo <command> --help` for per-command flags and examples

## Typical flows

- Trending research: `kalo product rank --region US --range last7Day` → `kalo product detail <id>` → `kalo video rank --product <id>`
- Creator scouting: `kalo creator rank --category <id> --followers 10000-1000000` → `kalo creator detail <id>` (has contact email)
- Category drilldown: `kalo category search "beauty"` → `kalo category detail <id>` → `kalo shop rank --category <id>`

## Playbooks

For complex analysis — product/creator diagnosis, category sourcing research, creator
recommendation, viral-video methodology, shot-by-shot script writing — read
[references/playbooks.md](references/playbooks.md) first and follow its mandatory steps
(always benchmark against same-category / same-price-band / same-follower-tier peers
before drawing conclusions).
