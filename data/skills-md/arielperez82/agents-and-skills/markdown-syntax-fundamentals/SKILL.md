---
name: markdown-syntax-fundamentals
description: Use when writing or editing markdown files. Covers headings, text formatting, lists, links, images, code blocks, and blockquotes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Markdown Syntax Fundamentals

Core markdown syntax for creating well-structured documents.

## Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

### Heading Best Practices

- Use a single H1 (`#`) per document as the title
- Don't skip heading levels (H2 to H4)
- Keep headings concise and descriptive
- Use sentence case or title case consistently

## Text Formatting

### Emphasis

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
~~strikethrough~~
```

### Inline Code

```markdown
Use `backticks` for inline code like `const x = 1`
```

## Lists

### Unordered Lists

```markdown
- Item one
- Item two
  - Nested item
  - Another nested item
- Item three

* Alternative marker
+ Also works
```

### Ordered Lists

```markdown
1. First item
2. Second item
   1. Nested numbered
   2. Another nested
3. Third item
```

### Task Lists (GitHub Flavored)

```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
```

## Links

### Basic Links

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title text")
```

### Reference Links

```markdown
[Link text][reference-id]

[reference-id]: https://example.com "Optional title"
```

### Automatic Links

```markdown
<https://example.com>
<email@example.com>
```

### Internal Links (Anchors)

```markdown
[Jump to section](#section-heading)
```

Anchor IDs are auto-generated from headings:

- Lowercase
- Spaces become hyphens
- Special characters removed

## Images

### Basic Images

```markdown
![Alt text](image.png)
![Alt text](image.png "Optional title")
```

### Reference Images

```markdown
![Alt text][image-id]

[image-id]: path/to/image.png "Optional title"
```

### Linked Images

```markdown
[![Alt text](image.png)](https://example.com)
```

## Code Blocks

### Fenced Code Blocks

````markdown
```javascript
function hello() {
  console.log("Hello, World!");
}
```
````

### Common Language Identifiers

- `javascript` / `js`
- `typescript` / `ts`
- `python` / `py`
- `bash` / `shell` / `sh`
- `json` / `yaml`
- `html` / `css`
- `sql`
- `markdown` / `md`

### Indented Code Blocks

```markdown
    // Four spaces or one tab
    function example() {
      return true;
    }
```

## Blockquotes

### Basic Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.

> Blockquotes can contain
>
> Multiple paragraphs.
```

### Nested Blockquotes

```markdown
> Outer quote
>> Nested quote
>>> Deeply nested
```

### Blockquotes with Other Elements

```markdown
> ## Heading in blockquote
>
> - List item
> - Another item
>
> ```code block```
```

## Horizontal Rules

```markdown
---
***
___
```

Use three or more hyphens, asterisks, or underscores.

## Escaping Characters

```markdown
\* Not italic \*
\# Not a heading
\[Not a link\]
\`Not code\`
```

Characters that can be escaped: `\` `` ` `` `*` `_` `{` `}` `[` `]` `(` `)` `#` `+` `-` `.` `!` `|`

## Line Breaks

```markdown
Line one with two trailing spaces
Line two (hard break)

Line one

Line two (paragraph break)
```

## Best Practices

1. **Consistent formatting**: Pick a style and stick to it
2. **Blank lines**: Add blank lines before and after:
   - Headings
   - Code blocks
   - Lists
   - Blockquotes
3. **Line length**: Consider wrapping at 80-120 characters for readability
4. **Alt text**: Always provide meaningful alt text for images
5. **Link text**: Use descriptive link text, not "click here"
6. **Code highlighting**: Always specify language for fenced code blocks
