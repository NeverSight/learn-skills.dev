---
name: writing-tidyverse-r
description: |
  Modern tidyverse patterns, style guide, and migration guidance for R development. Use this skill when writing R code with dplyr, reviewing tidyverse code, updating legacy R code to modern patterns, or enforcing consistent style. Covers native pipe usage, join_by() syntax, .by grouping, pick/across/reframe operations, tidy selection, stringr patterns, naming conventions, spacing, and migration from base R or older tidyverse APIs.
---

# Writing Tidyverse R

This skill covers modern tidyverse patterns for R 4.3+ and dplyr 1.1+, style guidelines, and migration from legacy patterns.

## Core Principles

1. **Use modern tidyverse patterns** - Prioritize dplyr 1.1+ features, native pipe, and current APIs
2. **Write readable code first** - Optimize only when necessary
3. **Follow tidyverse style guide** - Consistent naming, spacing, and structure

## Pipe Usage

**Always use native pipe `|>` instead of magrittr `%>%`**

R 4.3+ provides all needed features. See [pipe-examples.md](references/pipe-examples.md) for usage patterns.

## Join Syntax (dplyr 1.1+)

**Use `join_by()` instead of character vectors for joins**

Modern join syntax supports:
- Equality joins: `join_by(company == id)`
- Inequality joins: `join_by(company == id, year >= since)`
- Rolling joins: `join_by(company == id, closest(year >= since))`

See [join-examples.md](references/join-examples.md) for complete patterns.

## Multiple Match Handling

Use `multiple` and `unmatched` arguments for quality control:
- `multiple = "error"` - Expect 1:1 matches
- `multiple = "all"` - Allow multiple matches explicitly
- `unmatched = "error"` - Ensure all rows match

## Data Masking vs Tidy Selection

Understand the difference:
- **Data masking functions**: `arrange()`, `filter()`, `mutate()`, `summarise()`
- **Tidy selection functions**: `select()`, `relocate()`, `across()`

Key patterns:
- Use `{{}}` (embrace) for function arguments
- Use `.data[[]]` for character vectors
- Use `across()` for multiple columns

See [data-masking-examples.md](references/data-masking-examples.md) for patterns.

## Modern Grouping and Column Operations

**Use `.by` for per-operation grouping (dplyr 1.1+)**

This replaces the old `group_by() |> ... |> ungroup()` pattern.

Additional modern operations:
- `pick()` - Column selection inside data-masking functions
- `across()` - Apply functions to multiple columns
- `reframe()` - Multi-row summaries

See [grouping-examples.md](references/grouping-examples.md) for complete examples.

## String Manipulation with stringr

**Use stringr over base R string functions**

Benefits:
- Consistent `str_` prefix
- String-first argument order
- Pipe-friendly and vectorized

See [stringr-examples.md](references/stringr-examples.md) for common patterns and base R equivalents.

## Style Guide Essentials

### Object Names

- **Use snake_case for all names**
- **Variable names = nouns, function names = verbs**
- **Avoid dots except for S3 methods**

Good: `day_one`, `calculate_mean`, `user_data`
Avoid: `DayOne`, `calculate.mean`, `userData`

### Spacing and Layout

See [style-examples.md](references/style-examples.md) for proper spacing and pipe formatting.

### Naming and Arguments

- Use snake_case for variables and functions
- Prefix non-standard arguments with `.` (e.g., `.data`, `.by`)

## Anti-Patterns to Avoid

### Legacy Patterns

| Avoid | Use Instead |
|-------|-------------|
| `%>%` | `|>` |
| `by = c("a" = "b")` | `by = join_by(a == b)` |
| `sapply()` | `map_*()` |
| `group_by() |> ... |> ungroup()` | `.by` argument |

### Performance Anti-Patterns

- **Don't grow objects in loops** - Pre-allocate or use purrr
- **Don't use `sapply()`** - Type-unstable, use `map_*()` instead

See [anti-patterns.md](references/anti-patterns.md) for examples of what to avoid and correct alternatives.

## Migration Reference

### Base R to Modern Tidyverse

| Base R | Modern Tidyverse |
|--------|------------------|
| `subset(data, condition)` | `filter(data, condition)` |
| `data[order(data$x), ]` | `arrange(data, x)` |
| `aggregate(x ~ y, data, mean)` | `summarise(data, mean(x), .by = y)` |
| `sapply(x, f)` | `map(x, f)` |
| `grepl("pattern", text)` | `str_detect(text, "pattern")` |
| `gsub("old", "new", text)` | `str_replace_all(text, "old", "new")` |

### Old to New Tidyverse Patterns

| Old Pattern | New Pattern |
|-------------|-------------|
| `data %>% function()` | `data |> function()` |
| `group_by(x) |> summarise() |> ungroup()` | `summarise(..., .by = x)` |
| `by = c("a" = "b")` | `by = join_by(a == b)` |
| `gather()/spread()` | `pivot_longer()/pivot_wider()` |
| `map_dfr(x, f)` | `map(x, f) |> list_rbind()` |
| `separate(col, into = ...)` | `separate_wider_delim()` |

See [migration-examples.md](references/migration-examples.md) for complete migration patterns.

source: Sarah Johnson's gist https://gist.github.com/sj-io/3828d64d0969f2a0f05297e59e6c15ad
