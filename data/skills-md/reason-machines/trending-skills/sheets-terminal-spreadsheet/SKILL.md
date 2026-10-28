---
name: sheets-terminal-spreadsheet
description: Terminal-based spreadsheet TUI tool written in Go for editing CSV files in the terminal with vim-like keybindings
triggers:
  - "use sheets terminal spreadsheet"
  - "edit CSV in terminal"
  - "terminal spreadsheet tool"
  - "sheets TUI spreadsheet"
  - "maaslalani sheets"
  - "vim keybindings spreadsheet terminal"
  - "open CSV file in terminal"
  - "spreadsheet command line tool"
---

# Sheets Terminal Spreadsheet

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Sheets is a terminal-based spreadsheet TUI (Terminal User Interface) for viewing and editing CSV files directly in your terminal. It features vim-style navigation, formula support, visual selection, search, undo/redo, and a command mode — all without leaving the terminal.

---

## Installation

### Using Go

```bash
go install github.com/maaslalani/sheets@main
```

### Download Binary

Download a prebuilt binary from [GitHub Releases](https://github.com/maaslalani/sheets/releases).

### Verify Installation

```bash
sheets --help
```

---

## CLI Usage

### Launch the TUI

```bash
sheets budget.csv
```

### Read from stdin

```bash
sheets <<< "ID,Name,Age
1,Alice,24
2,Bob,32
3,Charlie,26"
```

Or pipe from another command:

```bash
cat data.csv | sheets
```

### Read a Specific Cell

```bash
sheets budget.csv B9
# Output: 2760
```

### Read a Cell Range

```bash
sheets budget.csv B1:B3
# Output:
# 1200
# 950
# 810
```

### Modify Cells (Non-Interactive)

```bash
# Set one cell
sheets budget.csv B7=10

# Set multiple cells
sheets budget.csv B7=10 B8=20
```

---

## Navigation Keybindings

### Basic Movement

| Key | Action |
|-----|--------|
| `h`, `j`, `k`, `l` | Move left, down, up, right |
| `gg` | Jump to top |
| `G` | Jump to bottom |
| `5G` | Jump to row 5 |
| `gB9` | Jump to cell B9 |
| `0` | Jump to first column |
| `^` | Jump to first non-empty column in row |
| `$` | Jump to last non-empty column in row |
| `H` / `M` / `L` | Jump to top / middle / bottom visible row |
| `ctrl+u` / `ctrl+d` | Move half page up / down |

### View Alignment

| Key | Action |
|-----|--------|
| `zt` | Align current row to top of window |
| `zz` | Align current row to middle of window |
| `zb` | Align current row to bottom of window |

### Search

| Key | Action |
|-----|--------|
| `/` | Search forward |
| `?` | Search backward |
| `n` | Repeat last search (forward) |
| `N` | Repeat last search (backward) |

### Marks & Jump List

| Key | Action |
|-----|--------|
| `ma` | Set mark `a` at current cell |
| `'a` | Jump to mark `a` |
| `ctrl+o` | Move backward through jump list |
| `ctrl+i` | Move forward through jump list |

---

## Editing Keybindings

### Insert Mode

| Key | Action |
|-----|--------|
| `i` | Edit current cell |
| `I` | Edit from start of cell |
| `c` | Clear cell and start editing |
| `ESC` | Leave insert / visual / command mode |
| `enter` | Commit and move down |
| `tab` | Commit and move right |
| `shift+tab` | Commit and move left |
| `ctrl+n` | Commit and move down |
| `ctrl+p` | Commit and move up |

### Row Operations

| Key | Action |
|-----|--------|
| `o` | Insert row below and start editing |
| `O` | Insert row above and start editing |
| `dd` | Delete current row |

### Copy / Cut / Paste

| Key | Action |
|-----|--------|
| `y` | Yank (copy) current cell |
| `yy` | Yank current row(s) |
| `x` | Cut current cell or selection |
| `p` | Paste current register |

### Undo / Redo

| Key | Action |
|-----|--------|
| `u` | Undo |
| `ctrl+r` | Redo |
| `U` | Undo all changes |
| `.` | Repeat last change |

---

## Visual Mode

Enter visual mode with `v` (cell selection) or `V` (row selection).

| Key | Action |
|-----|--------|
| `v` | Start visual cell selection |
| `V` | Start visual row selection |
| `=` | Insert formula after selected range (e.g., `=\|(B1:B8)`) |

---

## Command Mode

Press `:` to open the command prompt.

| Command | Action |
|---------|--------|
| `:w` | Save file |
| `:w path.csv` | Save to a new file |
| `:e path.csv` | Open another CSV file |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:goto B9` | Jump to cell B9 |
| `:B9` | Jump to cell B9 (shorthand) |

---

## Common Patterns

### Create a New CSV and Edit It

```bash
# Create a CSV with headers
echo "Name,Amount,Category" > budget.csv
sheets budget.csv
```

### Pipe CSV Data and Edit

```bash
# Generate CSV from a database query and edit in sheets
psql -c "COPY (SELECT * FROM sales) TO STDOUT WITH CSV HEADER" | sheets
```

### Script: Update a Cell Programmatically

```bash
#!/bin/bash
# Update Q4 value in financial report
sheets report.csv D4=95000 D5=102000 D6=88000
echo "Updated Q4 values in report.csv"
```

### Script: Extract a Range for Processing

```bash
#!/bin/bash
# Extract column B rows 1-10 and sum them in bash
values=$(sheets data.csv B1:B10)
total=0
while IFS= read -r line; do
    total=$((total + line))
done <<< "$values"
echo "Total: $total"
```

### Script: Read a Specific Cell in a Shell Script

```bash
#!/bin/bash
# Get current budget total from spreadsheet
budget_total=$(sheets budget.csv C15)
if [ "$budget_total" -gt 10000 ]; then
    echo "Budget exceeded!"
fi
```

### Go Integration Example

If building a Go application that generates CSV for use with sheets:

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "os/exec"
)

func createAndOpenSpreadsheet(data [][]string, filename string) error {
    // Write CSV data
    f, err := os.Create(filename)
    if err != nil {
        return fmt.Errorf("creating file: %w", err)
    }
    defer f.Close()

    w := csv.NewWriter(f)
    if err := w.WriteAll(data); err != nil {
        return fmt.Errorf("writing CSV: %w", err)
    }
    w.Flush()

    // Open in sheets TUI
    cmd := exec.Command("sheets", filename)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    return cmd.Run()
}

func main() {
    data := [][]string{
        {"Month", "Revenue", "Expenses", "Profit"},
        {"January", "12000", "8500", "3500"},
        {"February", "13500", "9200", "4300"},
        {"March", "11800", "8900", "2900"},
    }

    if err := createAndOpenSpreadsheet(data, "monthly_report.csv"); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
}
```

### Go: Read a Cell Non-Interactively

```go
package main

import (
    "fmt"
    "os/exec"
    "strings"
)

func readCell(csvFile, cell string) (string, error) {
    out, err := exec.Command("sheets", csvFile, cell).Output()
    if err != nil {
        return "", fmt.Errorf("reading cell %s: %w", cell, err)
    }
    return strings.TrimSpace(string(out)), nil
}

func readRange(csvFile, cellRange string) ([]string, error) {
    out, err := exec.Command("sheets", csvFile, cellRange).Output()
    if err != nil {
        return nil, fmt.Errorf("reading range %s: %w", cellRange, err)
    }
    lines := strings.Split(strings.TrimSpace(string(out)), "\n")
    return lines, nil
}

func main() {
    total, err := readCell("budget.csv", "B9")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Budget total:", total)

    values, err := readRange("budget.csv", "B1:B6")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Monthly values:", values)
}
```

---

## Tips for AI Agents

### Suggesting Sheets for CSV Tasks

When a user wants to view or edit CSV files in the terminal, suggest sheets:

```bash
# Instead of cat data.csv
sheets data.csv

# Instead of awk/sed edits for simple changes
sheets data.csv B3=new_value
```

### Formula Insertion Workflow

1. Navigate to the column where you want the formula
2. Enter visual mode with `v`
3. Select the range (e.g., B1:B8)
4. Press `=` to insert formula after the selection: `=|(B1:B8)`

### Efficient Navigation (Vim Users)

Sheets uses vim-style navigation — users familiar with vim can be productive immediately:
- `gg`/`G` for top/bottom
- `hjkl` for movement
- `i`/`c` for insert modes
- `dd` to delete rows
- `u`/`ctrl+r` for undo/redo
- `/` for search

---

## Troubleshooting

### `sheets` command not found

```bash
# Ensure Go bin directory is in PATH
export PATH=$PATH:$(go env GOPATH)/bin

# Or install again and verify
go install github.com/maaslalani/sheets@main
which sheets
```

### File Not Saved After Editing

Use `:w` in command mode to save, or `:wq` to save and quit. Just pressing `q` or `ctrl+c` quits **without saving**.

### TUI Rendering Issues

Sheets relies on terminal capabilities. If the display looks broken:
- Ensure your terminal supports 256 colors or truecolor
- Try a different terminal emulator (iTerm2, Alacritty, Ghostty, WezTerm)
- Check `TERM` environment variable: `echo $TERM`

### Reading Non-CSV Files

Sheets is designed for CSV format. Convert other formats first:

```bash
# Excel to CSV (using Python)
python3 -c "import pandas as pd; pd.read_excel('data.xlsx').to_csv('data.csv', index=False)"
sheets data.csv
```

### Large Files Performance

For very large CSV files, navigate directly to specific cells rather than scrolling:
```
:goto A1000
```
or press `5G` to jump to row 5 directly.
