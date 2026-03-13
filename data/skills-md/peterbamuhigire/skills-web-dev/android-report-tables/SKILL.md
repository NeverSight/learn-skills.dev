---
name: android-report-tables
description: "Report UI rule for Android: any report with potential for more than 25 rows must render as a table, not cards. Includes decision rules and Compose patterns."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Android Report Tables (25+ Rows)

When a report can exceed **25 rows**, it must be rendered as a **table**, not card lists. This prevents scroll fatigue and preserves scanability for business data.

## Scope

**Use for:** Reports, analytics lists, financial summaries, inventory reports, audit logs, and any dataset likely to exceed 25 rows.

**Do not use:** Small datasets (<=25 rows) or highly visual summaries where cards communicate state better.

## Rule (Mandatory)

- If a report **can** exceed 25 rows, use a **table layout**.
- Cards are acceptable only when the dataset is **guaranteed <=25 rows**.

## Existing ReportTable Composable

The project has a reusable `ReportTable<T>` at `core/ui/components/ReportTable.kt`:

```kotlin
ReportTable(
    columns = listOf(
        TableColumn(header = "#", weight = 0.4f) { "#${it.rank}" },
        TableColumn(header = "Name", weight = 1.5f) { it.fullName ?: "-" },
        TableColumn(header = "Inv", weight = 0.4f) { it.totalInvoices.toString() },
        TableColumn(header = "Amount", weight = 1.2f) { "$currency ${fmt.format(it.totalAmount)}" }
    ),
    rows = report.rows,
    onRowClick = { /* optional */ },
    pageSize = 25
)
```

Features:
- Generic `<T>` with `TableColumn<T>` definitions (header, weight, value lambda)
- Built-in client-side pagination (25/page default)
- Header row with `surfaceVariant` background
- `Modifier.weight()` for proportional column sizing
- Empty state with string resource

## Date Display (Mandatory)

**All dates in report tables MUST be human-readable.** Never display raw API dates like `2026-02-14`. Always format to short readable form: **`d MMM yyyy`** (e.g., `14 Feb 2026`).

### Standard Date Formatter Pattern
```kotlin
val apiDateFmt = remember { SimpleDateFormat("yyyy-MM-dd", Locale.US) }
val displayDateFmt = remember { SimpleDateFormat("d MMM yyyy", Locale.US) }
val formatDate: (String) -> String = { raw ->
    try { displayDateFmt.format(apiDateFmt.parse(raw)!!) } catch (_: Exception) { raw }
}

// Usage in TableColumn:
TableColumn("Date", minWidth = 100.dp) { formatDate(it.date) }
TableColumn("Oldest", minWidth = 100.dp) { it.oldestDate?.let { formatDate(it) } ?: "-" }
```

### Rules
- API sends dates as `yyyy-MM-dd` — this is for transport only, never for display
- Tables, cards, summaries, and any user-facing text must use `d MMM yyyy`
- Chart axes may use shorter formats like `MMM d` (e.g., `Feb 14`) for space
- Nullable dates: format if present, show `-` if null

## Portrait Responsiveness Standards

### Column Priority (Phone Portrait)
- **3-4 columns max** for portrait without horizontal scroll
- Abbreviate headers: "#" not "Rank", "Inv" not "Invoices", "Amt" not "Amount", "Bal" not "Balance"
- Use `weight` ratios: narrow columns (0.3-0.5f), name columns (1.3-1.5f), amount columns (1.0-1.2f)

### Weight Guidelines
| Column Type | Weight | Examples |
|-------------|--------|----------|
| Index/Rank | 0.3-0.5f | #, Rank |
| Short text | 0.4-0.6f | Code, Qty, Inv |
| Name/Description | 1.3-1.5f | Product, Distributor |
| Currency amount | 1.0-1.2f | Amount, Balance, Due |
| Date | 0.8-1.0f | Date |

### Horizontal Scroll (5+ columns)
When a table needs 5+ columns and cannot fit in portrait:
```kotlin
Column(Modifier.horizontalScroll(rememberScrollState())) {
    ReportTable(columns = ..., rows = ...)
}
```

### String Resources
Always use `stringResource(R.string.report_col_*)` for table headers. Never hardcode header text.

## Cards vs Tables Decision Matrix

| Criteria | Use Cards | Use Table |
|----------|-----------|-----------|
| Max rows <= 25 guaranteed | Yes | Optional |
| Max rows > 25 possible | No | **Required** |
| DPCs (5-20 items) | Yes | Optional |
| Daily summary (7 days) | Yes | Optional |
| Distributor lists | No | **Required** |
| Product lists | No | **Required** |
| Invoice lists | No | **Required** |
| Debtors lists | No | **Required** |
| Top 100 rankings | No | **Required** |

## Pagination Guidance

- Default to **client-side pagination** for up to a few hundred rows (25 per page).
- `ReportTable` handles pagination internally — no need for ViewModel pagination.
- For larger datasets (1000+), use server pagination via API offset/limit params.

## Pull-to-Refresh (Mandatory)

**Every screen that displays reports, statistics, or data** MUST support pull-to-refresh. Users expect to swipe down to reload current data.

### Implementation Pattern (PullToRefreshBox)
```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyReportScreen(viewModel: MyViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    var isRefreshing by remember { mutableStateOf(false) }

    LaunchedEffect(uiState.loading) {
        if (!uiState.loading) isRefreshing = false
    }

    PullToRefreshBox(
        isRefreshing = isRefreshing,
        onRefresh = { isRefreshing = true; viewModel.reload() },
        modifier = Modifier.fillMaxSize()
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // Report content
        }
    }
}
```

### Rules
- ViewModel MUST expose a public `reload()` / `refresh()` function
- Hub screens (Sales Hub, Network Hub, etc.) refresh their statistics/charts
- Report screens refresh their data (re-fetch from API)
- Dashboard refreshes KPI cards
- Use `PullToRefreshBox` (simpler API than the older `PullToRefreshContainer`)

## Screen Structure Pattern

Report screens with tables should use a scrollable `Column` (not `LazyColumn`), since `ReportTable` is not a lazy composable. Wrap in `PullToRefreshBox`:

```kotlin
PullToRefreshBox(
    isRefreshing = isRefreshing,
    onRefresh = { isRefreshing = true; viewModel.reload() },
    modifier = Modifier.fillMaxSize().padding(paddingValues)
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Filters
        // Summary cards
        // ReportTable (handles its own pagination)
    }
}
```

## Checklist

- [ ] If report can exceed 25 rows, use ReportTable composable
- [ ] Limit to 3-4 columns for portrait, abbreviate headers
- [ ] Use `Modifier.weight()` with appropriate ratios
- [ ] Use `stringResource()` for all header text
- [ ] Use `verticalScroll` Column wrapper (not LazyColumn)
- [ ] Let ReportTable handle pagination (remove ViewModel pagination logic)
- [ ] Pull-to-refresh on every screen with reports or statistics
