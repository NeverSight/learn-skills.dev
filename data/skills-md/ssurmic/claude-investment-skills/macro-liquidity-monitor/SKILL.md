---
name: macro-liquidity-monitor
description: USD funding / repo-plumbing liquidity radar. Tracks SOFR-IORB spread, SOFR tail, ON RRP buffer, bank reserves vs LCLoR, TGA drain/add, net liquidity, and SRF takeup (the funding-stress alarm). Outputs a tightness regime 🟢 ABUNDANT / 🟡 AMPLE / 🟠 TIGHTENING / 🔴 STRESS with the two lenses — "too loose → bubble" and "too tight → funding stress". All data from NY Fed Markets API + FRED (no API key). Runs on-demand or daily via GitHub Actions with Telegram push on regime change. Triggers in English ("liquidity check", "is liquidity tight", "SOFR IORB spread", "RRP balance", "when does liquidity tighten", "repo stress") or Chinese ("流动性怎么样", "流动性紧不紧", "什么时候收紧", "SOFR IORB 利差", "RRP 还剩多少", "回购市场压力", "美元流动性").
---

# Macro Liquidity Monitor — USD Funding & Repo Plumbing

## The one question this answers

**Is the banking system's overnight funding loose, normal, tightening, or stressed — and what's the next pressure point?**

This is NOT the equity-warning radar (`macro-warning`). That one watches valuation /
VIX / sentiment. This one watches the **plumbing**: where overnight cash actually
clears, how much buffer is left, and whether anyone is tapping the Fed's backstop.

Two lenses, both served by the same data:
- **"Too loose → bubble"** (the SLR-relief / deregulation worry): watch for SOFR
  printing *below* IORB while the RRP buffer is gone — cash with nowhere to go.
- **"Too tight → funding stress"** (a repo crisis): watch for SOFR *above* IORB,
  reserves near LCLoR, and SRF takeup spiking.

## When to invoke

- Manual: "流动性怎么样 / liquidity check / SOFR-IORB / when does liquidity tighten".
- Twice-daily batch (GitHub Actions, weekdays): **08:30 ET** morning preview
  (prior-day SOFR/EFFR) + **16:30 ET** post-close confirm (same-day ON RRP + SRF).
  Both push a Telegram digest; a 🔔 REGIME CHANGED banner is prepended on a band flip
  (tracked via committed `state.json`).
- Around month-end / quarter-end and big Treasury-issuance / debt-ceiling weeks.

## ⭐ Canonical data pull: `scripts/liquidity_pull.py`

Only dependency is `requests`. No API key. Run it:

```bash
PY=/tmp/.insider_venv/bin/python; [ -x "$PY" ] || PY=python3
$PY ~/.claude/skills/macro-liquidity-monitor/scripts/liquidity_pull.py            # human card
$PY ~/.claude/skills/macro-liquidity-monitor/scripts/liquidity_pull.py --json-only
$PY ~/.claude/skills/macro-liquidity-monitor/scripts/liquidity_pull.py --telegram # send if regime changed
TEST_MODE=1 $PY .../liquidity_pull.py --telegram --force   # print the Telegram msg, don't send
```

## Data sources (all public, no key)

| Metric | Series / endpoint | Source | Freshness |
|---|---|---|---|
| **SOFR** + p1/p99 + volume | `markets.newyorkfed.org/api/rates/secured/sofr/last/N.json` | NY Fed | prior day ~8am ET |
| **EFFR** (unsecured) | `.../rates/unsecured/effr/...` | NY Fed | prior day ~8am ET |
| **ON RRP** ops + counterparties | `.../rp/reverserepo/all/results/...` | NY Fed | same day ~1:15pm ET |
| **SRF takeup** (stress alarm) | `.../rp/repo/all/results/...` (sum same-day "Repo") | NY Fed | same day |
| **IORB** (admin ceiling) | FRED `IORB` | FRED CSV | daily |
| **ON RRP level** ($B) | FRED `RRPONTSYD` | FRED CSV | next day |
| **Bank reserves** ($M, weekly) | FRED `WRESBAL` | FRED CSV | Thu, Wed-dated |
| **TGA** ($M, weekly) | FRED `WTREGEN` | FRED CSV | weekly |
| **Fed balance sheet** ($M) | FRED `WALCL` | FRED CSV | Thu, Wed-dated |

> FRED rejects a Chrome User-Agent — the script calls FRED with the default
> requests UA (`browser=False`). NY Fed needs the browser UA.

**No public feed → manual event flags:** SLR / eSLR rule changes, GSE balance shifts,
debt-ceiling / issuance calendar. These are the *structural* drivers; note them in the
wiki page `investing/wiki/dollar-liquidity-plumbing.md` when they happen.

## The 0-100 Liquidity Score (higher = more abundant / looser)

Additive from a neutral **50**. SOFR−IORB is the spine; the rest nudge it:

| Component | Effect on score |
|---|---|
| **SOFR − IORB spread** (spine) | `−spread_bp × 2.5`, clamped −30…+35 (SOFR below IORB = loose = up) |
| **SRF takeup** | <$1B: 0 · $1–10B: −15 · >$10B: −35 |
| **Reserves vs LCLoR** | >$3.4T: +8 · $3.1–3.4T: +4 · $2.9–3.1T: 0 · <$2.9T: −10 |
| **TGA weekly flow** | draining: +5 · flat: 0 · building $25–150B: −5 · >$150B: −10 |
| **SOFR p99 − IORB** (tail) | <10bp: 0 · 10–25: −3 · >25: −8 |
| **Net-liq 13wk momentum** ⭐ | >+$300B: +12 · +$100–300B: +6 · ±$100B: 0 · −$100–300B: −6 · <−$300B: −12 |

Bands → **🟢 ABUNDANT** (≥80) · **🟡 AMPLE** (60–79) · **⚪ BALANCED** (45–59)
· **🟠 TIGHTENING** (25–44) · **🔴 STRESS** (<25). **Override:** SRF ≥ $10B, or
SOFR > IORB+5bp with RRP < $10B, forces 🔴.

> ⭐ **The forward-looking factor.** A 2yr backtest (`scripts/backtest_liquidity.py`)
> showed every *level* gauge here is coincident (≈0 correlation to next-week returns),
> but the **13-week CHANGE in net liquidity** (WALCL−TGA−RRP) leads forward-3m returns
> (corr **+0.26 SPX / +0.33 NDX**). The net-liquidity *level* is a spurious −0.71 trap.
> So this row is the one that tilts the score toward what's *coming*; the rest describe
> what *is*. Regime-bucketed fwd-3m: 🟢/🟡 ≈ +4–6%, 🔴 ≈ NDX −1% (value is downside avoidance).

> **Why an empty ON RRP does NOT drag the score down:** that cash already flowed into
> the system (loose), so it isn't *current* tightness. An empty buffer is a forward
> **fragility flag** — surfaced as a trigger, not subtracted from the abundance number.
> The per-layer `layers{}` block still scores RRP 0–3 as evidence.

## How to read it (the mental model)

1. **SOFR − IORB is the headline.** SOFR is what the market pays to borrow cash
   against Treasuries overnight; IORB is what the Fed pays banks. SOFR far *below*
   IORB = so much cash banks lend it out below the risk-free admin rate = **too loose**.
   SOFR climbing to/above IORB = cash is getting scarce = **tightening**.
2. **ON RRP is the shock absorber.** It was $2.5T in 2023; near $0 now. With the
   sponge empty, any drain (TGA rebuild, QT) hits **reserves directly**, so SOFR
   spikes get sharper and faster. This is the key fragility today.
3. **TGA + WALCL set the direction.** Treasury issuing debt and rebuilding its TGA
   account *drains* reserves; spending it *adds*. QT (WALCL falling) drains. Net
   liquidity ≈ WALCL − TGA − RRP.
4. **SRF takeup > a few $B = the alarm.** Dealers only tap the Fed's backstop when
   private repo is too tight. Quarter-ends produce transient spikes; a persistent
   one means genuine scarcity.

## Output contract

`scoring.liquidity_score` (0-100), `scoring.regime`, `scoring.score_detail{}`,
`scoring.layers{...}`, `scoring.triggers[]`, `scoring.headline_metrics{liquidity_score,
sofr,iorb,spread_bp,effr,rrp_bn,reserves_t,tga_bn,srf_bn,net_liquidity_bn}`,
`calendar{month_end,days_to_month_end,is_quarter_end_month}`.

## Hard rules

1. Never claim timing certainty — say "tightening risk rising", not "crunch on X date".
2. Always show SOFR−IORB and the RRP buffer; they're the two that matter most.
3. Tag the data date — the plumbing moves daily and month/quarter-ends distort it.
4. Distinguish a **month/quarter-end technical spike** from a **structural drain**.
5. Cite the series — every number above has a verifiable NY Fed / FRED source.

## Companion

- `investing/wiki/dollar-liquidity-plumbing.md` — the methodology + standing read.
- `macro-warning` — equity-valuation/sentiment regime (different question).
- SLR / deregulation context lives in the wiki page as a manual event log.
