---
name: mql5-foundry
description: "Comprehensive MQL5 development patterns covering Expert Advisors, custom indicators, panel UIs, order management, compilation, and docs research. Use for ANY MQL5 coding - EAs, indicators, scripts, panels, debugging, compiling, or looking up API docs. Merged from 5 skills: mql-developer, mql5-indicator-patterns, mql5-trade-manager, mql5-x-compile, mql5-docs-research."
allowed-tools: Read, Grep, Edit, Write, Bash
---

# MQL5 Foundry

Complete MQL5 workshop: EA architecture, indicator patterns, panel UIs, compilation, and docs research.

---

## Quick Navigation

| Section | For... |
|---------|--------|
| [1. General MQL5 Development](#1-general-mql5-development) | EA architecture, project structure, coding style, MQL4 vs MQL5 |
| [2. Indicator Development](#2-indicator-development) | Buffers, OnCalculate, display scale, bar detection, complete template |
| [3. Panel EA Patterns](#3-panel-ea-patterns) | Edit field safety, OBJ_BUTTON latch, panel drag, chart line drag, multi-TP, RR lock |
| [4. Compilation & Build](#4-compilation--build) | Windows (MetaEditor/build.ps1) and macOS (Wine X:) compilation |
| [5. Docs Research](#5-docs-research) | MQL5 API error lookup workflow |
| [Quick Reference](#quick-reference) | All cheatsheets in one place |

---

## 1. General MQL5 Development

### MQL4 vs MQL5 Key Differences

| Aspect | MQL4 | MQL5 |
|--------|------|------|
| Paradigm | Procedural (C-like) | Full OOP (C++-like) |
| Trade model | Orders only (`OrderSend`) | Orders + Deals + Positions (`CTrade`) |
| Account model | Hedging only | Netting + Hedging |
| Indicator buffers | Max 8 | Max 512 |
| Draw styles | 6 basic | 18 (basic + color) |
| Standard Library | Minimal | Comprehensive |
| Database | None | SQLite built-in |
| Sockets | None | TCP + TLS |
| OpenCL | No | Yes |

### Critical Gotchas

- **Double comparison**: Never use `==` with doubles. Use `NormalizeDouble()` or tolerance
- **4-digit vs 5-digit brokers**: 1 pip = 1 point (4-digit) or 10 points (5-digit). Always detect via `SYMBOL_DIGITS`
- **Reverse loop for closing**: Iterate `PositionsTotal()-1` down to `0` when closing positions
- **ECN brokers**: Some require two-step: `OrderSend()` without SL/TP, then modify
- **Filling policy**: Always detect via `SYMBOL_FILLING_MODE`, never hardcode FOK
- **WebRequest**: Synchronous/blocking, not available in indicators or Strategy Tester
- **Array indexing**: Series arrays index 0 = newest bar. Use `ArraySetAsSeries()` to control

### Project Structure

```
MQL5/
├── Experts/
│   └── MyEA/
│       └── MyEA.mq5
├── Indicators/
│   └── MyIndicator.mq5
├── Scripts/
│   └── MyScript.mq5
├── Include/
│   ├── Core/
│   │   ├── CTradeManager.mqh
│   │   ├── CRiskManager.mqh
│   │   └── CSignalBase.mqh
│   ├── Communication/
│   │   ├── CHttpClient.mqh
│   │   └── CJsonHelper.mqh
│   ├── UI/
│   │   └── CPanel.mqh
│   └── Utils/
│       ├── CTimeFilter.mqh
│       └── CSymbolHelper.mqh
└── Libraries/
```

### Code Style

- Prefix member variables with `m_` (e.g., `m_magicNumber`)
- Prefix global variables with `g_` (e.g., `g_isInitialized`)
- Always use `input` for user parameters (not `extern`)
- Normalize prices: `NormalizeDouble(price, Digits)`
- Always check return values of trade operations

---

## 2. Indicator Development

### Display Scale

**Problem**: Blank indicator window for small values (< 1.0 range).

**Fix**: Always set explicit scale in `OnInit()`:

```cpp
IndicatorSetDouble(INDICATOR_MINIMUM, 0.0);
IndicatorSetDouble(INDICATOR_MAXIMUM, 0.1);
```

Required for any indicator whose values span a range smaller than 1.0 (scores, probabilities, normalized metrics).

### Buffer Architecture

**Two-buffer pattern** (visible + hidden):

```cpp
#property indicator_buffers 2
#property indicator_plots   1

double BufVisible[];  // Plot buffer
double BufHidden[];   // Tracking buffer

int OnInit() {
   SetIndexBuffer(0, BufVisible, INDICATOR_DATA);        // Visible
   SetIndexBuffer(1, BufHidden, INDICATOR_CALCULATIONS); // Hidden
   return INIT_SUCCEEDED;
}
```

Buffer types:
- `INDICATOR_DATA` — visible plot on chart
- `INDICATOR_CALCULATIONS` — hidden, for internal tracking

### Bar Recalculation (Rolling Window)

**Problem**: Current bar updates tick-by-tick — naive implementations double-count values.

**Solution** — new bar detection + value replacement:

```cpp
static double sum = 0.0;
static int last_processed_bar = -1;

int OnCalculate(...) {
   for(int i = start; i < rates_total; i++) {
      bool is_new_bar = (i > last_processed_bar);
      double current = GetValue(i);

      if(is_new_bar) {
         if(i >= window_size) {
            int idx_out = i - window_size;
            sum -= BufHidden[idx_out];
         }
         sum += current;
      } else {
         if(i == last_processed_bar && BufHidden[i] != EMPTY_VALUE) {
            sum -= BufHidden[i];
         }
         sum += current;
      }

      BufHidden[i] = current;
      last_processed_bar = i;
      BufVisible[i] = sum / window_size;
   }
   return rates_total;
}
```

### Complete Indicator Template

```cpp
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   1
#property indicator_label1    "My Indicator"
#property indicator_type1     DRAW_LINE
#property indicator_color1    clrOrange
#property indicator_width1    2

input int InpPeriod = 20;
input int InpWindow = 30;

double BufVisible[];
double BufHidden[];
int hBase = INVALID_HANDLE;

int OnInit() {
   SetIndexBuffer(0, BufVisible, INDICATOR_DATA);
   SetIndexBuffer(1, BufHidden, INDICATOR_CALCULATIONS);

   int StartCalcPosition = InpPeriod + InpWindow - 1;
   PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartCalcPosition);
   PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE);

   IndicatorSetDouble(INDICATOR_MINIMUM, 0.0);
   IndicatorSetDouble(INDICATOR_MAXIMUM, 1.0);

   hBase = iSomeIndicator(_Symbol, _Period, InpPeriod);
   if(hBase == INVALID_HANDLE) return INIT_FAILED;
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason) {
   if(hBase != INVALID_HANDLE) IndicatorRelease(hBase);
}

int OnCalculate(const int rates_total, const int prev_calculated,
                const datetime &time[], ...) {
   int StartCalcPosition = InpPeriod + InpWindow - 1;
   if(rates_total <= StartCalcPosition) return 0;

   static double base[];
   ArrayResize(base, rates_total);
   ArraySetAsSeries(base, false);
   if(CopyBuffer(hBase, 0, 0, rates_total, base) < rates_total)
      return prev_calculated;

   ArraySetAsSeries(BufVisible, false);
   ArraySetAsSeries(BufHidden, false);

   int start = (prev_calculated == 0) ? StartCalcPosition : prev_calculated - 1;
   if(start < StartCalcPosition) start = StartCalcPosition;

   if(prev_calculated == 0) {
      for(int i = 0; i < start; i++) {
         BufVisible[i] = EMPTY_VALUE;
         BufHidden[i] = EMPTY_VALUE;
      }
   }

   static double sum = 0.0;
   static int last_processed_bar = -1;

   if(prev_calculated == 0 || start == StartCalcPosition) {
      sum = 0.0;
      last_processed_bar = StartCalcPosition - 1;
      for(int j = start - InpWindow + 1; j <= start; j++)
         sum += base[j];
   }

   for(int i = start; i < rates_total && !IsStopped(); i++) {
      bool is_new_bar = (i > last_processed_bar);
      if(is_new_bar && i >= InpWindow) {
         int idx_out = i - InpWindow;
         sum -= base[idx_out];
      }
      double current = base[i];
      if(is_new_bar) {
         sum += current;
      } else {
         if(i == last_processed_bar && BufHidden[i] != EMPTY_VALUE)
            sum -= BufHidden[i];
         sum += current;
      }
      last_processed_bar = i;
      BufHidden[i] = current;
      BufVisible[i] = sum / InpWindow;
   }
   return rates_total;
}
```

### Indicator Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Blank window | Scale not set for small values | Set INDICATOR_MINIMUM/MAXIMUM |
| Values drifting | Rolling window not reset | Use new bar detection + hidden buffer |
| Misaligned plot | Wrong PLOT_DRAW_BEGIN | Calculate: underlying_warmup + own_warmup |
| Reversed indexing | Series mode enabled | `ArraySetAsSeries(buffer, false)` |
| Buffer values wrong | Wrong INDICATOR_DATA type | Use INDICATOR_CALCULATIONS for hidden |
| Compile error on buffer | Buffer count mismatch | Match `indicator_buffers` with SetIndexBuffer calls |
| Not updating | OnCalculate return wrong | Return `rates_total` to signal success |
| Performance issue | Recalculating all bars | Only recalculate from `prev_calculated` |

### Debugging Checklist

1. **Scale**: Added `IndicatorSetDouble(INDICATOR_MINIMUM/MAXIMUM)`? Range appropriate?
2. **Buffers**: `indicator_buffers >= indicator_plots`? Hidden buffers for old values? `ArraySetAsSeries(buffer, false)`?
3. **Warmup**: `PLOT_DRAW_BEGIN` correct? Early bars initialized to `EMPTY_VALUE`?
4. **Recalculation**: `is_new_bar` logic? Old value subtracted before adding new? `last_processed_bar` tracking?
5. **Data flow**: Base handle valid? `CopyBuffer` returning expected count? No `EMPTY_VALUE` in calculated range?

---

## 3. Panel EA Patterns

### Module Architecture

```
Constants.mqh → Types.mqh → Helpers.mqh → Panel_Int.mqh → Panel.mqh
                                                              ↓
                               Orders.mqh ← Engine.mqh ← Drawing.mqh
```

Include order matters. Types before helpers before panel. Engine depends on Orders.

### Global State Pattern

Each include module binds to globals declared in the main EA:

```cpp
// In main EA
PanelConfig m_cfg;
PanelState  m_state;

// In each .mqh
extern PanelConfig  m_cfg;
extern PanelState   m_state;
```

### Naming Conventions

| Category | Prefix | Example |
|----------|--------|---------|
| Panel objects | `TP_` | `TP_ed_entry`, `TP_btn_buy` |
| Chart lines | `HL_ENTRY_`, `HL_SL_`, `HL_TP_` | `HL_ENTRY_0` |
| TREND handles | `HL_TRE_EN_`, `HL_TRE_SL_`, `HL_TRE_TP_` | `HL_TRE_EN_0` |
| Label backgrounds | `TP_LBL_XX_BG` | `TP_LBL_TP_BG` |
| Label text | `TP_LBL_XX_TX` | `TP_LBL_TP_TX` |

Chart line prefixes **must differ** from panel object prefixes so bulk delete doesn't destroy chart lines.

### Pip / Point Handling

```cpp
int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
g_pipSize = (digits == 3 || digits == 5) ? g_point * 10.0 : g_point;

double TM_NormalizePrice(double price) {
    int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    if(tickSize > 0)
        price = MathRound(price / tickSize) * tickSize;
    return NormalizeDouble(price, digits);
}
```

### Edit Field Safety

**Never** call `ObjectSetString(..., OBJPROP_TEXT, ...)` on an edit field during active editing:

```cpp
void TM_SafeSetEdit(string name, string text) {
    if(m_state.activeEditField == name)
        return;
    ObjectSetString(0, name, OBJPROP_TEXT, text);
}
```

Track `activeEditField` in `CHARTEVENT_OBJECT_BEGINEDIT` and clear in `CHARTEVENT_OBJECT_ENDEDIT`.

### OBJ_BUTTON Double-Fire Latch

Buttons fire `CHARTEVENT_OBJECT_CLICK` on both mouse-down AND mouse-up:

```cpp
bool mouseDown = false;

if(ObjectGetInteger(0, sparam, OBJPROP_TYPE) == OBJ_BUTTON) {
    if(mouseDown) { mouseDown = false; return; }
    mouseDown = true;
}
```

### Panel Drag via MOUSE_MOVE

Do NOT rebuild panel during drag — shift all objects by delta:

```cpp
void TM_ShiftAllByDelta(int dx, int dy) {
    for(int i = ObjectsTotal(0) - 1; i >= 0; i--) {
        string name = ObjectName(0, i);
        if(TM_StringStartsWith(name, TP_PREFIX))
            TM_ShiftObject(name, dx, dy);
    }
}
void TM_ShiftObject(const string name, int dx, int dy) {
    int x = (int)ObjectGetInteger(0, name, OBJPROP_XDISTANCE);
    int y = (int)ObjectGetInteger(0, name, OBJPROP_YDISTANCE);
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x + dx);
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y + dy);
}
```

Use `CHARTEVENT_MOUSE_MOVE` with bit 0 of `sparam`. Save position to `GlobalVariableSet` per ChartID on drag-end.

### Chart Line Drag Pattern

HLINE/TREND drag has three phases:
1. **DRAG start**: `CHARTEVENT_OBJECT_DRAG` → set `chartLineDragging = true`
2. **During drag**: Poll price via `ObjectGetDouble()` in `OnTimer()` at 1s intervals
3. **Drag end**: `CHARTEVENT_OBJECT_CHANGE` → apply final values

### String Helpers (MQL5 compat)

```cpp
bool TM_StringStartsWith(const string &text, const string &prefix) {
    if(StringLen(text) < StringLen(prefix)) return false;
    return StringCompare(StringSubstr(text, 0, StringLen(prefix)), prefix) == 0;
}
```

Always iterate objects in **reverse** when deleting:

```cpp
void TM_DeleteByPrefix(const string prefix) {
    for(int i = ObjectsTotal(0) - 1; i >= 0; i--) {
        string name = ObjectName(0, i);
        if(TM_StringStartsWith(name, prefix))
            ObjectDelete(0, name);
    }
}
```

### Config Persistence

```cpp
void TM_SaveConfig(const PanelConfig &cfg) {
    int h = FileOpen("Config.dat", FILE_WRITE | FILE_BIN);
    if(h == INVALID_HANDLE) return;
    FileWriteStruct(h, cfg);
    FileClose(h);
}
bool TM_LoadConfig(PanelConfig &cfg) {
    int h = FileOpen("Config.dat", FILE_READ | FILE_BIN);
    if(h == INVALID_HANDLE) return false;
    bool ok = FileReadStruct(h, cfg);
    FileClose(h);
    return ok;
}
```

### Position Iteration

Always check `ticket == 0` after `PositionGetTicket()`:

```cpp
for(int i = 0; i < PositionsTotal(); i++) {
    ulong ticket = PositionGetTicket(i);
    if(ticket == 0) continue;
    if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
    if(PositionGetInteger(POSITION_MAGIC) != TP_MAGIC) continue;
}
```

### Trade Object Init

```cpp
CTrade g_trade;
void TM_OrdersInit() {
    g_trade.SetExpertMagicNumber(TP_MAGIC);
    g_trade.SetDeviationInPoints(30);
    g_trade.SetTypeFilling(ORDER_FILLING_RETURN);
}
```

### Pending Order Broker Compatibility

Some brokers reject SL/TP on pending orders. Retry without them:

```cpp
if(!g_trade.OrderSend(req, res)) {
    if((slPrice != 0 || tpPrice != 0) && (res.retcode == 10016 || GetLastError() == 4752)) {
        req.sl = 0;  req.tp = 0;
        g_trade.OrderSend(req, res);
    }
}
```

### SL/TP Wrong-Side Validation

```cpp
bool TM_ValidateSLTP(ENUM_TRADE_DIR dir, double entry, double sl, double tp) {
    if(dir == TD_BUY) {
        if(sl > 0.0 && sl >= entry) return false;
        if(tp > 0.0 && tp <= entry) return false;
    } else {
        if(sl > 0.0 && sl <= entry) return false;
        if(tp > 0.0 && tp >= entry) return false;
    }
    return true;
}
```

### 3-TP Architecture

TP1 is broker-level. TP2/TP3 tracked locally:

```cpp
void TM_CheckMultiTP() {
    for(int i = 0; i < 3; i++) {
        if(!m_cfg.tpLevels[i].isActive) continue;
        if(m_cfg.tpLevels[i].isHit) continue;
        double targetDist = m_cfg.tpLevels[i].pipsDist * g_pipSize;
        bool hit = (posType == POSITION_TYPE_BUY)
            ? ((ask - entry) >= targetDist)
            : ((entry - bid) >= targetDist);
        if(hit) {
            double closeVol = TM_NormalizeLot(vol * m_cfg.tpLevels[i].allocPct / 100.0);
            g_engineTrade.PositionClosePartial(ticket, closeVol);
            m_cfg.tpLevels[i].isHit = true;
        }
    }
}
```

### Multi-TP Allocation Cycling

Keep active levels summing to exactly 100%:

```cpp
void TM_EnsureAlloc100() {
    int active = 0, sum = 0;
    for(int i = 0; i < 3; i++) {
        if(m_cfg.tpLevels[i].isActive) { active++; sum += m_cfg.tpLevels[i].allocPct; }
        else m_cfg.tpLevels[i].allocPct = 0;
    }
    if(sum == 100) return;
    if(sum == 0) { return; }
    int newSum = 0;
    for(int i = 0; i < 3; i++) {
        if(!m_cfg.tpLevels[i].isActive) continue;
        int scaled = (int)MathRound((double)m_cfg.tpLevels[i].allocPct * 100.0 / sum);
        m_cfg.tpLevels[i].allocPct = scaled;
        newSum += scaled;
    }
    for(int i = 2; i >= 0; i--)
        if(m_cfg.tpLevels[i].isActive) { m_cfg.tpLevels[i].allocPct += 100 - newSum; break; }
}
```

### RR Lock (Forward/Reverse)

When RR locked, dragging SL recalculates TP (forward), dragging TP recalculates SL (reverse):

```cpp
// Forward: SL -> TP
double tpDist = slDist * m_cfg.rrLockedValue;
double newTp  = (tradeDir == TD_BUY) ? entry + tpDist : entry - tpDist;

// Reverse: TP -> SL
double slDist = tpDist / m_cfg.rrLockedValue;
double newSl  = (tradeDir == TD_BUY) ? entry - slDist : entry + slDist;
```

### Prop Firm Config Backup

```cpp
// Before entering prop firm screen:
m_state.m_cfgBackup = m_cfg;
TM_BuildPropFirmScreen();

// On "Back":
m_cfg = m_state.m_cfgBackup;
TM_BuildPanel();
```

### Color Definitions (Dark Theme)

Use `C'R,G,B'` syntax (not hex):

```cpp
#define CLR_SURFACE_BASE    C'13,13,26'    // #0D0D1A
#define CLR_SURFACE_PANEL   C'21,21,33'    // #151521
#define CLR_SURFACE_RAISED  C'28,28,46'    // #1C1C2E
#define CLR_BUY             C'0,191,165'   // #00BFA5
#define CLR_SELL            C'255,82,82'   // #FF5252
#define CLR_ACCENT          C'108,92,231'  // #6C5CE7
```

### Layout Column System

```cpp
#define PANEL_WIDTH        320
#define ROW_HEIGHT         32
#define HEADER_HEIGHT      36
#define PANEL_PADDING      12
#define COL_LABEL_W        70
#define COL_EDIT_W         70
#define COL_PIPS_W         80
#define COL_BTN_W          60
```

### Timer-Based Label Refresh

Use `EventSetTimer(1)` for 1-second label updates, not OnTick:

```cpp
void OnTimer() {
    if(m_state.isVisible)
        TM_RefreshLabels();
}
```

### Object Label Efficiency

Only set text if changed:

```cpp
void TM_SetText(string name, string text) {
    string cur = ObjectGetString(0, name, OBJPROP_TEXT);
    if(cur != text)
        ObjectSetString(0, name, OBJPROP_TEXT, text);
}
```

### Account Stats & Day Rollover

```cpp
MqlDateTime tm;
TimeCurrent(tm);
int today = tm.year * 10000 + tm.mon * 100 + tm.day;
if(m_state.lastDayOfYear != today) {
    m_state.lastDayOfYear = today;
    m_state.dailyStartBalance = AccountInfoDouble(ACCOUNT_BALANCE);
    m_state.todayTrades = 0;
}
```

### Daily Limit Check

```cpp
if(breachLoss || breachTarget) {
    TM_CloseAllPositions();
    m_state.blocked = true;
}
```

### Panel EA Common Mistakes

| Mistake | Fix |
|---------|-----|
| `plot()` inside local scope | MQL5 is not Pine. Use `ObjectCreate` for chart objects |
| `ObjectSetString` on active edit | Guard with `activeEditField` check |
| Same prefix for panel + chart lines | Use separate prefixes so bulk delete is safe |
| Rebuilding panel during drag | Shift all objects by delta instead |
| Not iterating in reverse when deleting | Deleted positions shift indices below |
| Using hex `#RRGGBB` | MQL5 uses `C'R,G,B'` syntax |
| SL/TP not normalized to tick size | Always call `TM_NormalizePrice()` before trade functions |
| Not checking `ticket == 0` after `PositionGetTicket` | Returns 0 at end of list |

---

## 4. Compilation & Build

### Windows

**Via MetaEditor GUI**: Open `.mq5` in MetaEditor -> F5 or Compile button.

**Via build script** (`build.ps1` — tm/ project style): The script compiles `.mq5` files by calling MetaEditor64.exe from the command line.

### macOS (Wine X: Drive)

**Prerequisite** — map X: drive:

```bash
BOTTLE="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5"
cd "$BOTTLE/dosdevices"
ln -s "../drive_c/Program Files/MetaTrader 5/MQL5" "x:"
```

**Compile**:

```bash
WINE="/Applications/MetaTrader 5.app/Contents/SharedSupport/wine/bin/wine64"
WINEPREFIX="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5"
WINEPREFIX="$WINEPREFIX" "$WINE" "C:/Program Files/MetaTrader 5/MetaEditor64.exe" \
    /log /compile:"X:\\Indicators\\Custom\\File.mq5" /inc:"X:"
```

**Critical**: Wine returns exit code 1 even on success. Ignore it — verify `.ex5` file exists and check per-file `.log`.

### Verification

Check `.ex5` file was created with recent timestamp. Check per-file log for "0 errors, 0 warnings". The `.log` file is in the same directory as the `.mq5` file.

---

## 5. Docs Research

### Scope

Use only official MQL5 documentation:
- https://www.mql5.com/en/docs
- https://www.mql5.com/ja/docs (Japanese)

Do not use forums, blogs, or third-party sites.

### Workflow

1. Normalize error or question into keywords (error code, function/class names, 2-5 keywords)
2. Search official docs via site search
3. Open most relevant pages to confirm function signatures, parameter types, return values
4. Produce response with:
   - Summary of the cause
   - Doc links (JA first, EN second)
   - Specific guidance from docs
   - Next checks if ambiguity remains

### Guardrails

- If error cannot be mapped to docs, state that clearly and propose best-effort hypothesis
- Never invent API signatures or behavior not documented
- Keep response concise and actionable

---

## Quick Reference

### Essential Code Snippets

```cpp
// Pip/point detection
int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
double pipSize = (digits == 3 || digits == 5) ? _Point * 10.0 : _Point;

// Price normalization
double NormalizePrice(double price) {
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    if(tickSize > 0) price = MathRound(price / tickSize) * tickSize;
    return NormalizeDouble(price, (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS));
}

// New bar detection
static int last_processed_bar = -1;
bool is_new_bar = (i > last_processed_bar);

// SL/TP wrong-side check
bool ValidateSLTP(ENUM_TRADE_DIR dir, double entry, double sl, double tp) {
    if(dir == TD_BUY)  return !(sl > 0 && sl >= entry) && !(tp > 0 && tp <= entry);
    return !(sl > 0 && sl <= entry) && !(tp > 0 && tp >= entry);
}

// Trade init
CTrade trade;
trade.SetExpertMagicNumber(MAGIC);
trade.SetDeviationInPoints(30);
trade.SetTypeFilling(ORDER_FILLING_RETURN);

// Safe edit field update
if(m_state.activeEditField == name) return;
ObjectSetString(0, name, OBJPROP_TEXT, text);

// Config save/load
int h = FileOpen("cfg.dat", FILE_WRITE | FILE_BIN);
FileWriteStruct(h, cfg); FileClose(h);
// Load:
FileReadStruct(h, cfg);

// Object reverse delete
for(int i = ObjectsTotal(0)-1; i >= 0; i--)
    if(StringFind(ObjectName(0, i), prefix) == 0)
        ObjectDelete(0, ObjectName(0, i));
```

### Type Conversion Quick Ref

| Task | Code |
|------|------|
| Check if position is ours | `PositionGetInteger(POSITION_MAGIC) == MY_MAGIC` |
| Get position direction | `(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE)` |
| Get position volume | `PositionGetDouble(POSITION_VOLUME)` |
| Get current ask | `SymbolInfoDouble(_Symbol, SYMBOL_ASK)` |
| Get current bid | `SymbolInfoDouble(_Symbol, SYMBOL_BID)` |
| Get point value | `SymbolInfoDouble(_Symbol, SYMBOL_POINT)` |
| Get tick size | `SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE)` |
| Get contract size | `SymbolInfoDouble(_Symbol, SYMBOL_TRADE_CONTRACT_SIZE)` |
| Get tick value | `SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE)` |
