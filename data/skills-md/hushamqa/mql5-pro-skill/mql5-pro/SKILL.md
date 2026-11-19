---
name: mql5-pro
description: Expert skill for writing, debugging, and optimizing MQL5 code for MetaTrader 5 — Expert Advisors (EAs), custom indicators, scripts, services, libraries, and GUI panels. Use this skill whenever the user mentions MQL5, MQL, MetaTrader 5, MT5, MetaEditor, .mq5/.mqh/.ex5 files, Expert Advisor, EA, trading robot, custom indicator, OnTick, OnCalculate, CTrade, OrderSend, Strategy Tester, backtest/optimization on MT5, chart panels/buttons in MetaTrader, or pastes code containing #property, OnInit, MqlTradeRequest, or iCustom. Also triggers for converting MQL4 code to MQL5, fixing MQL5 compile/runtime errors, position sizing and risk management code, trailing stops, grid/hedging EAs, ICT/SMC tooling for MT5 (FVG, Order Blocks, BOS, ChoCh, liquidity sweeps, premium/discount zones), funded/prop firm account protection, JSON WebRequest integration, account-based EA licensing, MT5 log reading for agentic/Claude Code workflows, converting TradingView Pine Script indicators or strategies to MQL5, Strategy Tester methodology (walk-forward, optimization, Monte Carlo, headless tester automation), and building graphical dashboards (CAppDialog, CCanvas, chart objects). If the task touches MetaTrader 5 programming in any form, always use this skill.
---

# MQL5 Professional Development

Expert reference for production-grade MQL5 on current MetaTrader 5 builds (as of mid-2026: build 5800+; compiler rules from build 5260+ apply). v10 — adds Pine Script→MQL5 conversion (`references/pine-to-mql5.md`) and Strategy Tester methodology + CLI automation (`references/testing.md`).

## Skill self-correction protocol (governing rule)

When code produced from this skill fails, and review with the user establishes that the cause is **wrong or outdated information in this skill itself** (not a typo, not a user-side environment issue, not a one-off mistake) — a wrong API signature, a non-existent enum/constant, an incorrect method name, a false compiler/runtime claim, an obsolete rule:

1. State explicitly that the root cause is a skill defect, name the exact file and line/section, and quote the wrong claim and the verified correct one.
2. Update the skill file IMMEDIATELY in the same turn — correct the erroneous text in place (and any duplicate of it elsewhere in the skill), then confirm what changed.
3. Verify the correction against an authoritative source (official MQL5 reference / a real compile) before writing it — never replace one guess with another. The fix must be 100% confirmed, not probable.
4. **Whole-skill consistency check before writing.** Search the ENTIRE skill (`SKILL.md` + every `references/*` + `assets/*`) for every other place that states, depends on, or contradicts the corrected fact. The correction is not done until:
   - every duplicate of the wrong claim is fixed identically,
   - no remaining rule, example, template, or cross-reference now conflicts with the corrected fact,
   - any rule that was logically built on the wrong fact is re-evaluated and adjusted.
   A fix that corrects one location while leaving a contradiction elsewhere is a regression — it makes the skill internally inconsistent, which is worse than the original single error.
5. Do not defer, do not merely note it for "later", do not wait for a second prompt. A confirmed skill error is fixed on the spot so it never recurs.

This applies to every file in the skill (`SKILL.md`, `references/*`, `assets/*`).

## Reference files — read before writing code

| File | Read when the task involves |
|---|---|
| `references/trading.md` | EAs, orders, positions, CTrade, retcodes, netting/hedging, risk/lot sizing, SL/TP validation, OnTradeTransaction, trailing stops, **funded/prop firm account protection** |
| `references/indicators.md` | Custom indicators, buffers, OnCalculate, prev_calculated, indicator handles, multi-timeframe/multi-symbol data, **ICT/SMC detection (FVG, OB, BOS, sweeps, P/D zones)** |
| `references/gui.md` | Panels, buttons, dashboards, drawings on candles (lines/zones/arrows/text), THEME color & METRICS dimension libraries, coordinate systems, CAppDialog, CCanvas, OnChartEvent |
| `references/advanced.md` | CArrayObj collections (grid/hedging sets), OnTimer state machines, WebRequest/Sockets/**JSON builder+extractor**, ONNX inference, settings persistence, multi-symbol EAs, position reversal, **account licensing/protection** |
| `references/pitfalls.md` | MQL4 contamination scan, compile errors (**StringTrimLeft/Right pitfall, BOM stripping**), runtime errors, tester/optimization issues, performance tuning, code-shortening, **MT5 log autonomous reading (agentic/Claude Code workflow)** |
| `references/module-integration.md` | ONLY when the user states this program will later be merged with other EAs/indicators/panels — manifests, per-module STATE structs, Common.mqh, single-handler dispatch, indicator buffer offsets, input/magic/object namespacing |
| `references/pine-to-mql5.md` | Converting TradingView Pine Script (v4–v6) indicators/strategies to MQL5: execution-model and indexing translation, `na`/`var`/`varip` semantics, `ta.*` mapping with formula-mismatch flags (MACD/stoch), `request.security` → non-repainting MTF, plots/drawings→buffers/objects, `strategy.*`→CTrade, value-verification protocol |
| `references/testing.md` | Strategy Tester methodology: modeling-mode selection, backtest validity requirements, TesterStatistics table, walk-forward analysis, optimization workflow, frames/Monte Carlo, multi-currency testing, headless tester+compile automation via CLI (tester.ini) |

## Ready-made templates — start from these, never from a blank file

| Template | Use as the base for |
|---|---|
| `assets/EA_Template.mq5` | Any Expert Advisor: new-bar gating, ATR-based SL/TP, risk-sized lots, margin pre-check, retry loop, OnTradeTransaction close detection, OnTester criterion |
| `assets/Indicator_Template.mq5` | Any indicator: correct prev_calculated loop, color line + arrow signals, non-repaint signal placement, warm-up handling |
| `assets/Panel_Template.mq5` | Any GUI panel: THEME/METRICS/TEXTS libraries, factories, SLayout grid, event routing, lot edit validation, full cleanup |

When building a deliverable: copy the closest template, replace the signal/UI sections, keep the infrastructure (normalization, retries, cleanup) intact. The templates already pass the deliverable checklist below.

For an EA with a panel: read `trading.md` + `gui.md` and merge `EA_Template` + `Panel_Template`. Always skim `pitfalls.md` before delivering final code.

## External tooling — use when available in the environment

This skill is self-contained knowledge; the tools below turn write→guess→deliver into write→compile→verify→deliver. Check which are connected/installed before starting, and prefer them over memory:

| Tool | Kind | Use for |
|---|---|---|
| `mql5-help` MCP server | MCP (docs) | Instant query over 4500+ official MQL5 reference documents — verify any API signature, enum, or constant before writing it (self-correction protocol step 3) |
| `mcp-metatrader5-server` (mt5mcp, via uvx) | MCP (terminal bridge) | Live market data, symbol specs (tick size, stops level, volume step), account info, and demo-account trade execution to validate order logic against a real server |
| `metaeditor64.exe /compile:"path.mq5" /log` | CLI | Headless compile; parse the UTF-16LE log (pitfalls.md §10) in a compile→fix→recompile loop — never deliver uncompiled code when this is available |
| `terminal64.exe /config:tester.ini` | CLI | Headless backtests and optimization runs (full recipe: testing.md §9) |
| MT5 Experts/Journal logs | Files | Autonomous runtime-error diagnosis (pitfalls.md §10) |

In environments without any of these (plain chat), compensate with the bundled `assets/` headers as the API source of truth and the mental compile pass in the deliverable checklist.

## Bundled standard library (`assets/`) — the local source of truth for verification

Besides the three templates, `assets/` ships a curated slice of the MetaTrader 5 standard Include tree — exactly the modules this skill teaches (GUI building, chart-element drawing, trade execution), and nothing else. These are verbatim copies of the corresponding `MQL5\Include\` files. Their purpose is to be the **authoritative local reference**: before writing any standard-library API, read the actual class/header here rather than relying on memory (this is the source the self-correction protocol's step 3 calls for; a real header beats a guess). What lives where:

| Path | What it is / read it to confirm |
|---|---|
| `assets/Controls/` (all `.mqh`) | The CAppDialog/Controls GUI library: `Dialog.mqh` (CDialog/CAppDialog), `Button/Edit/Label/Panel/Picture/BmpButton.mqh` (simple `CWndObj`-based controls), `CheckBox/ComboBox/SpinEdit.mqh` (`CWndContainer`-based), `ListView/CheckGroup/RadioGroup.mqh` (`CWndClient`-based), `Scrolls.mqh` (CScrollV/H), `DatePicker/DateDropList.mqh`, `Wnd/WndObj/WndContainer/WndClient.mqh` (base classes — the inheritance chain that decides which setters a control has), `Rect.mqh`. **`Defines.mqh` is the single source for every `CONTROLS_*` color/metric constant and every `ON_*`/`EVENT_MAP_*` macro** — when an event or override name is in doubt, grep this file, do not guess. |
| `assets/Controls/res/` | The fixed bitmap glyphs the controls draw from via `#resource`: `CheckBoxOn/Off`, `RadioButtonOn/Off`, `SpinInc/Dec`, `DropOn/Off`, `DateDropOn/Off`, scroll thumbs/arrows, and the dialog caption `Close`/`Turn`/`Restore`. **These BMPs are authored for the LIGHT control surface and are NOT recolored by Defines overrides** — the root cause of the dark-theme breakage documented in `gui.md` §8. |
| `assets/Canvas/Canvas.mqh` | `CCanvas` — pixel/antialiased custom rendering for dashboards (`gui.md` §10). The 2D canvas only; DirectX/3D/flame variants are intentionally omitted as out of scope. |
| `assets/ChartObjects/` (all) | OO wrappers over native chart objects — lines, channels, Fibo, Gann, Elliott, shapes, arrows, text/bmp controls, sub-charts, panels (OBJ_*). The class-based alternative to the raw `ObjectCreate` factory pattern in `gui.md` §4–§5 for **drawing elements on the chart**. |
| `assets/Charts/Chart.mqh` | `CChart` — chart-properties wrapper; required by `Controls/Dialog.mqh`. |
| `assets/Trade/` (all) | `Trade.mqh` (CTrade), `PositionInfo/OrderInfo/HistoryOrderInfo/DealInfo.mqh`, `SymbolInfo/AccountInfo/TerminalInfo.mqh` — the trade-execution and market-info classes used throughout `trading.md`. Confirm exact CTrade method signatures here. |
| `assets/Files/` | `File.mqh` (CFile base), `FileBin.mqh` (used by CCanvas), `FileTxt/FileBin/FileBMP/FilePipe.mqh` — file wrappers for settings persistence (`pitfalls.md` §9). |
| `assets/Tools/DateTime.mqh` | `CDateTime` — date/time decomposition helper. |

**Dependency note (why every kept file works together):** within `assets/` every relative (`"..."`) include resolves to another bundled file — the tree is internally consistent. The only headers referenced but intentionally NOT bundled are the universal base files `<Object.mqh>` and `<Arrays\ArrayObj/ArrayInt/ArrayLong/ArrayString.mqh>`; these exist in every MetaTrader installation under `MQL5\Include\` and resolve there at compile time. Nothing in the bundle depends on any module outside this list.

Note: deliverables follow the portable single-folder rule below — project files use quoted relative includes; only the standard library (this bundle + the base headers above) is referenced with angle brackets (`#include <Controls\Dialog.mqh>`), because it exists in every terminal.

## Language model — facts that prevent wrong code

MQL5 is C++-like but is NOT C++. Critical differences:

1. **No exceptions.** There is no `try/catch/throw`. Error handling = check return values + `GetLastError()` / `ResetLastError()`. Any generated code containing `try` will not compile.
2. **No pointer arithmetic, no raw memory.** Object pointers exist (`CObj *p = new CObj;`) and MUST be freed with `delete`. Check with `CheckPointer(p) != POINTER_INVALID`. Everything created with `new` leaks if not deleted (terminal logs "undeleted objects" on exit).
3. **No multiple inheritance.** Single inheritance + `interface` keyword.
4. **Strings are value types** (no char*). Use `StringFormat`, `StringSubstr`, `StringSplit`, `StringFind`. Char access: `StringGetCharacter` returns `ushort` (UTF-16).
5. **Arrays**: dynamic `double a[];` need `ArrayResize`. Default indexing is 0 = oldest. `ArraySetAsSeries(a, true)` flips to 0 = newest (MQL4 style). Passing arrays to functions: always by reference `void f(double &a[])`.
6. **input variables are constants** at runtime — copy to a working variable in `OnInit` if the value must be adjusted (e.g. clamping a lot size). `sinput` = input excluded from optimization. `input group "العنوان"` creates visual grouping in the inputs dialog.
7. **Supported and encouraged**: templates (`template<typename T>`), function/method overloading, operator overloading, default parameters, `typedef` for function pointers (`typedef bool(*TFilter)(ulong);`), `enum`, `struct`, `union`, `class`, `interface`, native `matrix`/`vector` types with OpenBLAS-backed methods, `complex` type.
8. **No true multithreading.** One thread per EA, indicators share one thread per symbol. Concurrency is simulated via `OnTimer`, `OnChartEvent`, `OnTradeTransaction`, and `OrderSendAsync`.
9. **`Sleep()` is forbidden in indicators** and ignored in the tester outside ticks. Never busy-wait in `OnCalculate`.
10. **Doubles**: never compare with `==`. Use `MathAbs(a-b) < _Point/2` (prices) or a domain epsilon. `NormalizeDouble(price, _Digits)` is NOT sufficient for instruments whose tick size ≠ point — round to tick size (see trading.md).

## ABSOLUTE RULE: MQL5 only — zero MQL4 contamination

This is the #1 cause of broken AI-generated MT5 code. MQL4 and MQL5 are different languages that share surface syntax. Mixing them produces code that either fails to compile or — worse — compiles and trades wrongly. Enforcement is strict and non-negotiable:

1. **Every line is written for MQL5, current build.** Never "adapt" an MQL4 snippet inline; rewrite it from the MQL5 model (positions/deals/handles), not transliterate it.
2. **Forbidden tokens — if any of these appear in generated code, the code is WRONG and must be rewritten:**

| Forbidden (MQL4) | Required (MQL5) |
|---|---|
| `start()`, `init()`, `deinit()` | `OnTick`/`OnCalculate`, `OnInit`, `OnDeinit` |
| `Bid`, `Ask` predefined variables | `SymbolInfoDouble(_Symbol, SYMBOL_BID/ASK)` or `SymbolInfoTick` |
| `Close[i]`, `Open[i]`, `High[i]`, `Low[i]`, `Time[i]`, `Volume[i]` predefined series | OnCalculate parameter arrays, or `iClose/iOpen/iHigh/iLow/iTime`, or `CopyRates/CopySeries` |
| `Bars` (variable) | `Bars(_Symbol,_Period)` function or `rates_total` |
| `OrderSend(sym,cmd,lots,price,slip,sl,tp,...)` 9+ args returning ticket | `OrderSend(MqlTradeRequest&, MqlTradeResult&)` or `CTrade` |
| `OrderSelect(i, SELECT_BY_POS, MODE_TRADES)` | `PositionGetTicket(i)` / `OrderGetTicket(i)` |
| `OrderClose`, `OrderModify`, `OrderDelete` (MQL4 forms) | `trade.PositionClose/PositionModify/OrderDelete(ticket)` |
| `OrderTicket()/OrderLots()/OrderType()/OrderProfit()` | `PositionGetInteger/Double/String(...)` after selection |
| `iMA(...,shift)` returning a double directly | handle in OnInit + `CopyBuffer` |
| `iCustom(...,buffer,shift)` returning a double | `iCustom` handle + `CopyBuffer` |
| `MarketInfo(symbol, MODE_*)` | `SymbolInfo*` functions |
| `IndicatorCounted()` | `prev_calculated` |
| `RefreshRates()` | unnecessary — quotes are fresh via SymbolInfo |
| `WindowFind`, `WindowRedraw` | `ChartWindowFind`, `ChartRedraw` |
| `Point`, `Digits` bare (MQL4 style) | `_Point`, `_Digits` (or per-symbol SymbolInfo) |
| `OP_BUY/OP_SELL/OP_BUYSTOP...` | `ORDER_TYPE_BUY/SELL/BUY_STOP...`, `POSITION_TYPE_BUY/SELL` |
| `SetIndexStyle/SetIndexArrow/SetIndexLabel` | `PlotIndexSetInteger/Double/String` |
| `ObjectCreate(name, type, win, t, p)` 5-arg | `ObjectCreate(chart_id, name, type, subwin, time, price)` — chart id first |
| `ObjectSet(name, prop, val)` | `ObjectSetInteger/Double/String(0, name, OBJPROP_*, val)` |
| `#property strict` | delete — MQL5 is always strict |
| `IsTesting()`, `IsOptimization()`, `IsVisualMode()` | `MQLInfoInteger(MQL_TESTER / MQL_OPTIMIZATION / MQL_VISUAL_MODE)` |
| `IsDemo()`, `IsConnected()`, `IsTradeAllowed()` | `AccountInfoInteger(ACCOUNT_TRADE_MODE)`, `TerminalInfoInteger(TERMINAL_CONNECTED / TERMINAL_TRADE_ALLOWED)` |

3. **Conceptual separation**: MQL4 = order-centric (one ticket does everything). MQL5 = order → deal → position. Any logic written in terms of "orders" doing position work is MQL4 thinking and gets redesigned, not patched.
4. **Mandatory pre-delivery scan**: before presenting any code, scan it against the forbidden-token table above and the checklist in `references/pitfalls.md` §MQL4 contamination scan. One hit = rewrite that section.
5. If the user pastes MQL4 code, the deliverable is a clean MQL5 rewrite — state this explicitly, never a hybrid.

## Compiler rules from recent builds (must-know)

- **Build 5260 method hiding rule**: a method in a derived class with the same NAME as a base method now HIDES all base overloads (C++ behavior). Restore them with `using Base::Method;` inside the derived class. Old code that relied on merged overload sets breaks. The compiler warns when a hidden base overload would have been a better match.
- **Struct inheritance**: assigning to `this` inside a struct operator is no longer accepted. Prefer composition over inheriting from `MqlDateTime`/`MqlRates` etc.: `struct MyDT { MqlDateTime dt; }`.
- **Build 5320**: Service programs (`#property service`) supported in CodeBase; last build supporting Win7/8.
- **Builds 5430–5572**: chart engine switched to Blend2D (anti-aliased rendering, OBJ_TEXT positioning quirks); **build 5640 rolled back to GDI**. Do not write code depending on either engine's rendering specifics.
- **Build 5570+**: CUDA support for ONNX, `ColorToPRGB()`, resource file limit raised to 1 GB, faster matrix/vector ops.
- **Build 5800**: MetaEditor saves UTF-8 without BOM by default; auto-selects AVX2 compilation. Keep Arabic strings/comments in UTF-8.

## Program types and their event skeletons

| Type | Required handler | Key extras |
|---|---|---|
| Expert Advisor | `OnTick` | `OnInit`, `OnDeinit`, `OnTimer`, `OnTrade`, `OnTradeTransaction`, `OnChartEvent`, `OnTester` |
| Indicator | `OnCalculate` | `OnInit` (buffers), `OnDeinit`, `OnChartEvent`, `OnTimer` |
| Script | `OnStart` | runs once; the only type allowed to `Sleep()` freely |
| Service | `OnStart` | `#property service`; no chart; runs at terminal start; loop + `Sleep` |
| Library | exported functions | `#property library` |

Minimal correct EA skeleton (new-bar driven, the default for any bar-based strategy):

```mql5
#include <Trade\Trade.mqh>

// ملاحظة: التعليق بعد input يظهر كاسم في نافذة الإعدادات — لذلك يبقى إنجليزياً
// الشرح العربي يوضع في سطر مستقل أعلاه مثل هذا السطر
input long   InpMagic   = 246810;     // Magic Number
input double InpRiskPct = 1.0;        // Risk Percent

CTrade trade;

int OnInit()
{
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetDeviationInPoints(10);
   trade.SetTypeFillingBySymbol(_Symbol);   // يختار وضع التعبئة الصحيح تلقائياً
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason) {}

bool IsNewBar()
{
   static datetime lastBar = 0;
   datetime cur = iTime(_Symbol, _Period, 0);
   if(cur == lastBar) return false;
   lastBar = cur;
   return true;
}

void OnTick()
{
   if(!IsNewBar()) return;
   // signal → risk check → trade. التفاصيل في references/trading.md
}
```

Rules encoded in this skeleton that must never be violated:
- Indicator handles are created ONCE in `OnInit`, read with `CopyBuffer` in `OnTick`, released with `IndicatorRelease` in `OnDeinit`. Creating handles per tick causes error 4806 and resource exhaustion.
- Every EA filters its own trades by magic number AND symbol when iterating positions.
- New-bar gating prevents the classic live-trading bug of order spam (backtest "on open prices" hides it; live ticks expose it).

## Architecture standard for non-trivial programs

Apply strict layering (mirrors the user's CONFIG/STATE/UI/EVENTS convention):

```mql5
//--- CONFIG: inputs + #define ثوابت لا تتغير بعد التحميل
//--- STATE : متغيرات global قابلة للتغير، تُجمع في struct واحد باسم البرنامج/الموديول
struct EAState { datetime lastBar; ulong activeTicket; int signalDir; };
EAState g_ea;   // اسم واحد فقط يدخل النطاق العام — لا متغيرات global مبعثرة
// إن صرّح المستخدم أن البرنامج سيُدمج لاحقاً مع برامج أخرى: سمِّ الـ struct باسم الموديول
// (struct RiskPanel_State { ... }; RiskPanel_State g_riskPanel;) واتبع references/module-integration.md
//--- CORE  : دوال المنطق الصافي — لا تلمس الرسم ولا التداول مباشرة
//--- TRADE : كل نداءات CTrade/OrderSend هنا فقط
//--- UI    : كل ObjectCreate/Canvas/Controls هنا فقط
//--- EVENTS: OnTick/OnChartEvent تستدعي طبقات أعلى فقط، بدون حسابات
```

- One generic function with parameters instead of duplicated near-identical functions (e.g. one `OpenTrade(ENUM_ORDER_TYPE type, ...)`, not `OpenBuy`+`OpenSell`).
- Naming convention (uniform): `CPascalCase` classes, `PascalCase` functions, `camelCase` locals, `m_camelCase` class members, `g_camelCase` globals, `Inp*` inputs, `UPPER_CASE` #defines/enum members. `g_camelCase` may be `g_moduleName` when a global is a module's STATE struct instance (see `references/module-integration.md`).
- Stateless helpers (price/lot normalization, new-bar check, formatting, retcode→string) get **generic project-neutral names**, never project-specific ones — so they move to a shared `Common.mqh` without renaming. The "one generic function" rule applies ACROSS programs, not only within one: do not write `CalculateLotForRiskPanel` when `CalculateLotBySL` already exists; reuse it.
- One function = one responsibility; if a function exceeds ~30 lines of logic, split it.
- Fail-fast: validate preconditions at the top of each function and return early — no deep nesting.
- **STATE seeded from CONFIG is the single source of truth at runtime.** `input` variables are runtime-constant (they never change after load — see Language model §6). Therefore any feature whose enable/disable flag or numeric value can change at runtime (panel buttons, mobile/chart-object commands, OnTradeTransaction-driven toggles) MUST be copied from its `Inp*` into a STATE field in `OnInit`, and every runtime check reads the STATE field ONLY. Never re-gate a live feature on its original input: `if(InpEnableTrail && g_s.trailing) ...` is wrong — because `Inp*` can never change at runtime, the `Inp*` term is a permanent AND-lock, so a user "enable" command sets `g_s.trailing=true` yet the feature stays dead while the command still appears to succeed (it logs/acknowledges). Correct: seed `g_s.trailing = InpEnableTrail;` in `OnInit`, then gate on `if(g_s.trailing)` alone. The input sets the INITIAL state; STATE owns it thereafter. The same applies to numeric overrides: `GetEffValue(){ return g_s.v>0 ? g_s.v : InpDefault; }` — read the accessor everywhere, never branch on the raw `Inp*` again.
// العطل الكلاسيكي: الإدخال يبقى بوابةً دائمة فوق الحالة فيُبطل أوامر التشغيل وقت التشغيل دون أي مؤشر فشل

## Portable single-folder projects — mandatory file layout

Any multi-file program ships as ONE self-contained folder that works from ANY location (the user can move/rename the folder and it still compiles and runs). Rules:

1. **All project files live in one folder** — the .mq5 plus every project .mqh side by side (or in subfolders OF that folder). Never scatter project files into `MQL5\Include\` or other MetaTrader directories.
```
MQL5\Experts\MyEA\            ← المجلد الواحد — انقله أين شئت داخل Experts ويعمل
   MyEA.mq5
   Config.mqh
   State.mqh
   Trade.mqh
   Signals.mqh
   UI\Panel.mqh               ← مجلدات فرعية داخل مجلد المشروع مسموحة
```
2. **Relative includes only** for project files: `#include "Config.mqh"`, `#include "UI\\Panel.mqh"` — quotes resolve relative to the including file, so the folder is location-independent. Angle brackets `#include <Trade\Trade.mqh>` are reserved EXCLUSIVELY for the platform's standard library (which exists in every terminal) — never for project files, because `<...>` resolves against `MQL5\Include\` and breaks the moment the project moves to another machine.
3. **Dependencies embedded, not referenced by path**: a required custom indicator is compiled into the EA as a resource so the .ex5 is fully self-contained — no `MQL5\Indicators\` path dependence:
```mql5
#resource "MyHelper.ex5"                          // الملف بجانب الـ .mq5 داخل مجلد المشروع
int h = iCustom(_Symbol, _Period, "::MyHelper.ex5", Param1);
```
Same for images and sounds: `#resource "img\\logo.bmp"` + `"::img\\logo.bmp"`, `PlaySound("::sfx\\alert.wav")`.
4. **Data files**: `FileOpen` with a bare relative name always resolves to the `MQL5\Files` sandbox regardless of where the program folder sits — already portable; never construct absolute paths.
5. **Result**: the compiled .ex5 alone is deliverable, and the source folder is a single zip that compiles anywhere under `MQL5\Experts\` (or `Indicators\`/`Scripts\`) with zero setup.

- All magic literals (thresholds, object prefixes, error strings) in CONFIG.
- **Language policy (strict)**: ALL program-visible text — UI labels, button captions, panel titles, input display names, log/Print messages, alerts, comments shown on chart — in ENGLISH. Arabic is allowed ONLY inside source-code comments (`//`, `/* */`) to explain the code. Identifiers always English.
- Modular projects: split into `.mqh` includes (one responsibility per file), all inside the project folder per the portable-layout rule above.

## Data access quick reference

```mql5
// أسعار حية — never use stale globals
double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
MqlTick tick; SymbolInfoTick(_Symbol, tick);          // أدق: bid/ask/last/time_msc معاً

// سلاسل زمنية — check the returned count, ALWAYS
double close1 = iClose(_Symbol, PERIOD_H1, 1);        // single value, shift 1 = آخر شمعة مغلقة
MqlRates rates[];
int n = CopyRates(_Symbol, PERIOD_CURRENT, 0, 100, rates);   // 0 = الشمعة الحالية
if(n < 100) return;                                   // البيانات غير جاهزة — انسحب وأعد المحاولة بالتيك التالي

// أسرع من CopyRates عند الحاجة لحقول محددة فقط (build 3950+)
datetime t[]; double c[];
CopySeries(_Symbol, PERIOD_CURRENT, 0, 100, COPY_RATES_TIME|COPY_RATES_CLOSE, t, c);
```

`iClose/iHigh/iTime/...` return 0 on missing data — guard against it. Multi-symbol/multi-TF data may not be synchronized on first access; the correct pattern (retry via timer, `BarsCalculated` check) is in indicators.md.

## Deliverable checklist before handing code to the user

1. **MQL4 contamination scan passed**: zero hits against the forbidden-token table above (full scan procedure in pitfalls.md).
2. Compiles with zero warnings (strict semantics are default in MQL5).
3. No `try/catch`, no `OrderSend` without retcode handling, no handle creation in `OnTick`/`OnCalculate`.
4. Volume normalized to `SYMBOL_VOLUME_STEP` and clamped to MIN/MAX; prices rounded to tick size; stops validated against `SYMBOL_TRADE_STOPS_LEVEL`/`FREEZE_LEVEL`.
5. **GUI built exclusively from the THEME color library + METRICS dimension library** (gui.md §2) — no raw color or pixel literal outside those blocks; every object created through a factory function, never duplicated creation blocks.
6. All chart objects use a unique prefix and are removed in `OnDeinit` via `ObjectsDeleteAll(0, PREFIX)`; `ChartRedraw()` after every UI batch.
7. `EventKillTimer()` in `OnDeinit` if `EventSetTimer` was used; `IndicatorRelease` for every handle; `delete` for every `new`.
8. All user-visible text in English; Arabic only in source comments.
9. Works on both netting and hedging accounts, or explicitly states the supported mode.
10. Tester-safe: no `MessageBox`/`Comment` spam in optimization, chart-dependent functions guarded by `MQLInfoInteger(MQL_TESTER)` checks where needed.
11. **Mental compile pass**: trace every identifier to its declaration, every function call to a real MQL5 signature (argument count/types/order), every enum to its MQL5 name; confirm all `new` have `delete`, all opened files close on every branch, and no function is defined but never called.
12. **Only if the user states this program will later be merged with other programs**: apply the `references/module-integration.md` §11 checklist (include guards, per-module STATE struct, manifest header, namespaced inputs/magic/objects/dialog-names, single-handler dispatch, idempotent OnDeinit, indicator buffer offsets) in addition to items 1–11. Do NOT apply it to standalone programs — it is pure overhead there.
