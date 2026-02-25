---
name: 4d-check-syntax
description: Check syntax and compile a 4D project to find errors and type issues. Use this skill when the user wants to compile, check syntax, or validate a 4D project. Creates a _compile method if not present, then runs it using tool4d. Returns compilation errors in JSON format for easy parsing.
license: Apache 2.0
---

# 4D Syntax Checker

Compile a 4D project to check for syntax errors and type mismatches.

## Prerequisites

Uses the **4d-run** skill to execute the compilation method. Ensure tool4d is available:
- Install [4D-Analyzer extension](https://marketplace.visualstudio.com/items?itemName=4D.4d-analyzer) in VS Code/Antigravity, OR
- Set `TOOL4D` environment variable to point to tool4d executable

## The _compile Method

Compilation requires a `_compile` method in the project. If not present, copy `assets/_compile.4dm` to `Project/Sources/Methods/_compile.4dm`.

## Compilation Output

### Success

```json
{"success":true,"errors":[]}
```

### Errors

```json
{
  "success": false,
  "errors": [
    {
      "message": "Syntax error",
      "isError": true,
      "code": {
        "type": "classFunction",
        "className": "MyClass",
        "functionName": "myMethod",
        "path": "[class]/MyClass/myMethod",
        "file": "[object File]"
      },
      "line": 10,
      "lineInFile": 42
    }
  ]
}
```

### Error Properties

- `message`: Error description
- `isError`: true for errors, false for warnings
- `code.type`: "projectMethod", "classFunction", etc.
- `code.className`: Class name (for class methods)
- `code.functionName`: Function name
- `line`: Line within the function
- `lineInFile`: Absolute line in the file

## Workflow

1. **Check for _compile method**: Look in `Project/Sources/Methods/_compile.4dm`
2. **Create if missing**: Write the _compile method using the template above
3. **Find tool4d**: Use 4d-run skill to locate tool4d
4. **Run compilation**: Execute `_compile` method with `--dataless`
5. **Parse results**: Extract JSON from ALERT output

## Running Compilation

```bash
"<tool4d_path>" --project="<project_path>" --startup-method=_compile --dataless 2>&1
```

Output format:
```
{"success":true,"errors":[]}
```

The JSON is output directly to system standard output via LOG EVENT.

## Common Compilation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Syntax error" | Invalid 4D syntax | Check line for typos |
| "Object syntax is not valid" | Invalid object property access | Use `[index]` for 4D.Blob properties |
| "Cannot make an assignment with those types" | Type mismatch | Check variable types |
| "Undeclared property 'X' used" | Missing property declaration | Add `property X : Type` to class |
| "The variable $X has not been explicitly declared" | Missing var declaration | Add `var $X : Type` |
| "signed integer overflow handling differs" | PCH cache issue | Not a code error, can ignore |

## Integration Example

```bash
# Find tool4d
TOOL4D=$(".claude/skills/4d-run/scripts/find_tool4d.sh")

# Run compilation and parse JSON result
OUTPUT=$("$TOOL4D" --project="/path/to/Project/MyProject.4DProject" --startup-method=_compile --dataless 2>&1)

# The JSON is output directly via LOG EVENT
echo "$OUTPUT" | jq .
```
