---
name: regex
description: Regular expression mastery with syntax, common patterns, and language-specific usage. Use when user asks to "write a regex", "match pattern", "validate email", "extract data with regex", "parse string", "regex for phone number", or any regular expression tasks.
---

# Regular Expressions

Regex syntax, patterns, and recipes.

## Core Syntax

### Character Classes

```
.           Any character (except newline)
\d          Digit [0-9]
\D          Non-digit
\w          Word character [a-zA-Z0-9_]
\W          Non-word character
\s          Whitespace [ \t\n\r\f]
\S          Non-whitespace
[abc]       Character set (a, b, or c)
[^abc]      Negated set (not a, b, or c)
[a-z]       Range (a through z)
[a-zA-Z]    Multiple ranges
```

### Quantifiers

```
*           0 or more
+           1 or more
?           0 or 1
{3}         Exactly 3
{3,}        3 or more
{3,5}       3 to 5
*?          0 or more (lazy/non-greedy)
+?          1 or more (lazy)
??          0 or 1 (lazy)
```

### Anchors & Boundaries

```
^           Start of string (or line with m flag)
$           End of string (or line with m flag)
\b          Word boundary
\B          Non-word boundary
```

### Groups & References

```
(abc)       Capture group
(?:abc)     Non-capturing group
(?<name>abc) Named capture group
\1          Backreference to group 1
(?=abc)     Positive lookahead
(?!abc)     Negative lookahead
(?<=abc)    Positive lookbehind
(?<!abc)    Negative lookbehind
```

### Alternation & Escaping

```
a|b         Match a or b
\           Escape special character
\.          Literal dot
\*          Literal asterisk
```

### Flags

```
g           Global (all matches)
i           Case-insensitive
m           Multiline (^ and $ match line boundaries)
s           Dotall (. matches newline)
u           Unicode
x           Extended (ignore whitespace, allow comments)
```

## Common Patterns

### Validation

```
# Email (simplified)
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

# URL
^https?://[^\s/$.?#].[^\s]*$

# Phone (US)
^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$

# IP Address (IPv4)
^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$

# Date (YYYY-MM-DD)
^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$

# Time (HH:MM, 24hr)
^([01]\d|2[0-3]):[0-5]\d$

# UUID
^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$

# Hex color
^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$

# Strong password (8+ chars, upper, lower, digit, special)
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$

# Semantic version
^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([\da-zA-Z-]+(?:\.[\da-zA-Z-]+)*))?$

# Slug (URL-safe string)
^[a-z0-9]+(?:-[a-z0-9]+)*$
```

### Extraction

```
# Extract domain from URL
https?://([^/\s]+)

# Extract filename from path
[^/\\]+$

# Extract numbers from string
\d+\.?\d*

# Extract HTML tags
<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>

# Extract key=value pairs
(\w+)=([^\s&]+)

# Extract markdown links
\[([^\]]+)\]\(([^)]+)\)

# Extract CSV fields (handling quotes)
(?:^|,)(?:"([^"]*(?:""[^"]*)*)"|([^,]*))
```

## Language Usage

### JavaScript

```javascript
// Test
/^\d+$/.test("123");                    // true

// Match
"hello world".match(/(\w+)\s(\w+)/);   // ["hello world", "hello", "world"]

// Match all
[..."text 123 more 456".matchAll(/\d+/g)];  // [["123"], ["456"]]

// Replace
"hello".replace(/l/g, "r");            // "herro"
"John Smith".replace(/(\w+) (\w+)/, "$2, $1");  // "Smith, John"

// Split
"a,b,,c".split(/,+/);                  // ["a", "b", "c"]

// Named groups
const m = "2024-01-15".match(/(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/);
m.groups.year;  // "2024"
```

### Python

```python
import re

# Match (from start)
re.match(r'^\d+', '123abc')

# Search (anywhere)
re.search(r'\d+', 'abc123')

# Find all
re.findall(r'\d+', 'a1 b2 c3')          # ['1', '2', '3']

# Find all with groups
re.findall(r'(\w+)=(\w+)', 'a=1 b=2')   # [('a', '1'), ('b', '2')]

# Replace
re.sub(r'\d+', 'X', 'a1b2c3')           # 'aXbXcX'
re.sub(r'(\w+) (\w+)', r'\2 \1', 'John Smith')  # 'Smith John'

# Compile for reuse
pattern = re.compile(r'\b\w{4}\b')
pattern.findall('the quick brown fox')    # ['quick', 'brown']

# Named groups
m = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})', '2024-01')
m.group('year')  # '2024'

# Flags
re.findall(r'hello', 'Hello World', re.IGNORECASE)
```

### Bash/grep

```bash
# grep (basic regex)
grep "pattern" file.txt
grep -i "pattern" file.txt       # Case insensitive
grep -E "extended|regex" file.txt  # Extended regex
grep -P "\d{3}" file.txt          # Perl regex (GNU grep)

# sed
sed 's/old/new/g' file.txt
sed -E 's/([0-9]+)/[\1]/g' file.txt
```

## Reference

For more recipes and testing tips: `references/recipes.md`
