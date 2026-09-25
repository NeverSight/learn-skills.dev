---
name: finding-tests
description: Locates existing tests for a given C# class and method using the test coverage data supplied by IDE. Triggers ONLY for C# production code (`.cs` files in a Rider .NET solution) when generating new tests, adding test coverage, finding existing tests, or when the user mentions uncovered lines, test files, or test suites. Must be used before writing or editing C# test code when finding already existing tests is necessary. Do NOT invoke for non-C# languages — the underlying tool only understands C# symbols and will not return useful results.
allowed-tools: execute_tool
---

# Finding Existing Tests

**Applies to: C# code only.**
If the production code in question is not C# - do not use this skill. Skip it silently and use the host's normal test-discovery approach. The underlying coverage tool only understands C# symbols.

Always use the `findTests` tool via `execute_tool` to locate existing tests for a given C# class and method. This tool queries the IDE code coverage data directly and is:

- **Precise** — returns exact test locations without false positives
- **Token-efficient** — no need for glob, grep, or directory listing guesses
- **Fast** — a single call replaces multiple rounds of searching

## `findTests`

Find existing tests for a given production class and method. Supply the production code's class name, namespace, and file path — the tool returns the path of the single test file most relevant to the given method.

### Syntax

```
execute_tool(command="findTests --className <value> --classNamespace <value> --filePath <value> [--methodName <value>] [--methodArguments <value>]")
```

### Parameters

| Parameter | Type | Required | Description                                                                                        |
|-----------|------|----------|----------------------------------------------------------------------------------------------------|
| `--className` | `string` | Yes      | Name of the class                                                                                  |
| `--classNamespace` | `string` | Yes      | Namespace of the given class                                                                       |
| `--filePath` | `string` | Yes      | Absolute file path to file with the given class                                                    |
| `--methodName` | `string` | No        | Name of the method                                                                                 |
| `--methodArguments` | `string` | No       | Names and types of the method arguments — use to target a specific overload (e.g. `"TextReader reader, Type objectType"`) |

**String parameters:** Quote values containing spaces: `--filePath '/Users/dev/MyProject/src/Services/OrderService.cs'`

### Examples

#### 1. Class only — no method name
User says: "Find the tests for the `JsonSerializer` class"

```json
{"tool":"execute_tool","arguments":{"command":"findTests --className JsonSerializer --classNamespace Newtonsoft.Json --filePath /projects/Newtonsoft.Json/Src/Newtonsoft.Json/JsonSerializer.cs"}}
```

#### 2. With method name
User says: "Find tests for the `Deserialize` method in `JsonSerializer`"

```json
{"tool":"execute_tool","arguments":{"command":"findTests --className JsonSerializer --classNamespace Newtonsoft.Json --filePath /projects/Newtonsoft.Json/Src/Newtonsoft.Json/JsonSerializer.cs --methodName Deserialize"}}
```

#### 3. With method name and arg names — specific overload
User says: "Find tests for the `Deserialize(TextReader reader, Type objectType)` overload in `JsonSerializer`"

```json
{"tool":"execute_tool","arguments":{"command":"findTests --className JsonSerializer --classNamespace Newtonsoft.Json --filePath /projects/Newtonsoft.Json/Src/Newtonsoft.Json/JsonSerializer.cs --methodName Deserialize --methodArguments 'TextReader reader, Type objectType'"}}
```

#### 4. Generic class and method
User says: "Find tests for the `ReadJson<TResult>` method in `JsonConverter<T>`"

```json
{"tool":"execute_tool","arguments":{"command":"findTests --className 'JsonConverter<T>' --classNamespace Newtonsoft.Json --filePath /projects/Newtonsoft.Json/Src/Newtonsoft.Json/JsonConverter.cs --methodName 'ReadJson<TResult>'"}}
```

#### 5. Paths with spaces
```json
{"tool":"execute_tool","arguments":{"command":"findTests --className DnsClient --classNamespace My.Network.Clients --filePath '/Users/dev/MyProject/src/Network Clients/DnsClient.cs' --methodName ResolveAsync"}}
```

### Pitfalls

- Every `--param` MUST be followed by a value (no bare flags)
- Values with spaces must be quoted: `--filePath '/Users/dev/MyProject/my folder/file.cs'`
- Omit optional parameters entirely rather than passing empty strings
- All file paths must be absolute

## Rules

1. **C# only.** Before invoking `findTests`, verify the production file is `.cs`. If it is any other language, do not invoke this skill or its tool — skip silently and fall back to standard test discovery.
2. **Prefer `findTests` over glob, grep, or directory listing** to find tests in C# code. These are wasteful and imprecise. If `execute_tool` is unavailable, fall back to grep/glob as a last resort and inform the user.
3. If `findTests` reports no tests exist, trust that result — do not retry with alternative search tools.
4. After finding tests, read them to understand the project's testing conventions before making any changes.

## Troubleshooting

### execute_tool not available
If `execute_tool` is not available, inform the user and fall back to grep/glob only as a last resort.

### `findTests` via `execute_tool` timeout
If calling `findTests` via `execute_tool` times out, inform the user and fall back to your standard test discovery method.
You may stop trying `findTests` if it timeouts for three times in a row.

### No tests found
If `findTests` returns empty results, trust the result. Do not retry with alternative search methods.
