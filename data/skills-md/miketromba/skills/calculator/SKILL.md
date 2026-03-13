---
name: calculator
description: Perform mathematical calculations (add, subtract, multiply, divide). Use when you need to do any numerical calculations — never do mental math. Supports batch operations.
---

# Calculator

Perform mathematical calculations with precision. Use this skill for ANY numerical calculations — never do mental math.

## Usage

Run the bundled script with JSON operations:

```bash
bun .cursor/skills/calculator/scripts/cli.ts '<json_operations>'
```

## Input Format

Pass a JSON array of operations, where each operation has:
- `operator`: One of `add`, `subtract`, `multiply`, `divide`
- `operands`: Array of numbers (minimum 2)

### Examples

Single calculation:
```bash
bun .cursor/skills/calculator/scripts/calculator.ts '[{"operator":"add","operands":[1,2,3]}]'
```

Multiple calculations (batched):
```bash
bun .cursor/skills/calculator/scripts/calculator.ts '[{"operator":"add","operands":[10,20]},{"operator":"multiply","operands":[5,6,2]},{"operator":"divide","operands":[100,4]}]'
```

## Output

Returns JSON with results for each operation:

```json
{
  "results": [
    { "operation": "add(10, 20)", "result": 30 },
    { "operation": "multiply(5, 6, 2)", "result": 60 },
    { "operation": "divide(100, 4)", "result": 25 }
  ]
}
```

## When to Use

- **Always** for any numerical calculation, no matter how simple
- Percentage calculations
- Unit conversions
- Aggregating numbers
- Any math where precision matters

## Operation Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `add` | Sum all operands | `add(1,2,3)` → 6 |
| `subtract` | Subtract from first | `subtract(10,3,2)` → 5 |
| `multiply` | Product of all | `multiply(2,3,4)` → 24 |
| `divide` | Divide sequentially | `divide(100,2,5)` → 10 |
