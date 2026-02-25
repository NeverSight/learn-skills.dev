---
name: html-parser-rule
description: 编写与测试 HTML 解析规则。用于从网页提取文章标题、链接、日期等信息。
---

# HTML Parser Rule Writer Skill

## Trigger Keywords
- "write html parser rule"
- "create html parser"
- "parse html source"
- "add html parser"
- "编写html解析规则"
- "创建html解析器"
- "添加html解析规则"

## Skill Description
This skill helps you write and test HTML parsing rules for article-flow project. It follows a systematic approach:
1. Fetch the HTML content and save locally
2. Write regex patterns step by step
3. Test each regex individually
4. Complete the full parsing rule
5. Run final integration test

## Instructions

### Step 1: Fetch HTML Content

When user provides a URL to parse, first fetch and save the HTML:

```bash
# Fetch HTML and save to temporary file
curl -L -H "User-Agent: Mozilla/5.0" "{URL}" > /tmp/source.html

# Show file size and first 100 lines to understand structure
wc -l /tmp/source.html
head -100 /tmp/source.html
```

Ask user to confirm the HTML looks correct and identify the article listing structure.

### Step 2: Identify Article Pattern

Examine the HTML structure and identify:
1. Article container element (div, article, li, etc.)
2. Title element and its pattern
3. Link element and its pattern
4. Date element and its pattern (if available)
5. Description element and its pattern (if available)

Show the user example HTML snippets and ask for confirmation.

### Step 3: Write Title Regex

Create and test the title extraction regex:

```typescript
// Example title regex
const titleRegex = /<h2[^>]*><a[^>]*>([^<]+)<\/a><\/h2>/g;
```

Test it immediately:
```bash
# Test title regex in Node.js
node -e "
const fs = require('fs');
const html = fs.readFileSync('/tmp/source.html', 'utf-8');
const titleRegex = /<h2[^>]*><a[^>]*>([^<]+)<\/a><\/h2>/g;
const matches = [...html.matchAll(titleRegex)];
console.log('Found', matches.length, 'titles:');
matches.slice(0, 5).forEach((m, i) => console.log(i+1, m[1]));
"
```

Wait for user confirmation before proceeding.

### Step 4: Write Link Regex

Create and test the link extraction regex:

```typescript
// Example link regex
const linkRegex = /<a[^>]*href="([^"]+)"[^>]*>.*?<\/a>/g;
```

Test it:
```bash
node -e "
const fs = require('fs');
const html = fs.readFileSync('/tmp/source.html', 'utf-8');
const linkRegex = /<a[^>]*href=\"([^\"]+)\"[^>]*>/g;
const matches = [...html.matchAll(linkRegex)];
console.log('Found', matches.length, 'links:');
matches.slice(0, 5).forEach((m, i) => console.log(i+1, m[1]));
"
```

Wait for user confirmation before proceeding.

### Step 5: Write Date Regex (if applicable)

If the source has date information, create and test:

```typescript
// Example date regex
const dateRegex = /<time[^>]*datetime="([^"]+)"[^>]*>/g;
```

Test it:
```bash
node -e "
const fs = require('fs');
const html = fs.readFileSync('/tmp/source.html', 'utf-8');
const dateRegex = /<time[^>]*datetime=\"([^\"]+)\"[^>]*>/g;
const matches = [...html.matchAll(dateRegex)];
console.log('Found', matches.length, 'dates:');
matches.slice(0, 5).forEach((m, i) => console.log(i+1, m[1]));
"
```

### Step 6: Write Description Regex (if applicable)

If the source has description/summary, create and test:

```typescript
// Example description regex
const descRegex = /<p class="excerpt">([^<]+)<\/p>/g;
```

Test it similarly.

### Step 7: Create Complete Parser

Now create the complete parser function in the html-parser.ts file:

```typescript
/**
 * Parse {SOURCE_NAME}
 */
private parseSourceName(html: string, source: DataSource): ContentItem[] {
  const items: ContentItem[] = [];
  
  // Your regex patterns
  const titleRegex = /pattern/g;
  const linkRegex = /pattern/g;
  const dateRegex = /pattern/g;
  const descRegex = /pattern/g;
  
  // Extract all matches
  const titles = [...html.matchAll(titleRegex)];
  const links = [...html.matchAll(linkRegex)];
  const dates = [...html.matchAll(dateRegex)];
  const descs = [...html.matchAll(descRegex)];
  
  // Combine into items
  const maxLength = Math.max(titles.length, links.length);
  for (let i = 0; i < maxLength; i++) {
    const title = titles[i]?.[1];
    const link = links[i]?.[1];
    const date = dates[i]?.[1];
    const desc = descs[i]?.[1];
    
    if (title && link) {
      items.push({
        title: this.decodeHtml(title.trim()),
        link: this.resolveUrl(link, source.url),
        source: source.name,
        sourceUrl: source.url,
        isoDate: date ? new Date(date).toISOString() : undefined,
        contentSnippet: desc ? this.decodeHtml(desc.trim()) : undefined
      });
    }
  }
  
  return items;
}
```

### Step 8: Register Parser

Add the parser to the parse() method's switch statement:

```typescript
case "source-name":
  return this.parseSourceName(html, source);
```

### Step 9: Update Domain Config

Add the source to the domain configuration:

```typescript
{
  name: "Source Name",
  url: "https://...",
  type: "html",
  parser: "source-name",
  tags: ["tag1", "tag2"]
}
```

### Step 10: Integration Test

Run the full collection to test:

```bash
cd packages/ai-digest
pnpm run collect
```

Check the report to verify:
1. Source status is "success"
2. Items found count is reasonable (> 0)
3. No errors in the log
4. Generated articles contain content from this source

### Step 11: Final Verification

Examine the output files:
```bash
# Check if articles from this source appear in output
grep "Source Name" outputs/$(date +%Y-%m-%d).en.md
```

If all tests pass, the parser rule is complete!

## Important Notes

1. **Always test each regex individually** before combining
2. **Use decodeHtml()** for title and description to handle HTML entities
3. **Use resolveUrl()** for links to handle relative URLs
4. **Handle missing fields gracefully** with optional chaining (?.)
5. **Verify the parser name matches** in both html-parser.ts and domain config
6. **Check the report** after running to see actual results

## Common Patterns

### Blog Post Listing
```typescript
// Often structured as:
// <article>
//   <h2><a href="...">Title</a></h2>
//   <time datetime="...">Date</time>
//   <p>Description</p>
// </article>
```

### News Site
```typescript
// Often structured as:
// <div class="article">
//   <a href="...">
//     <h3>Title</h3>
//   </a>
//   <span class="date">Date</span>
//   <div class="summary">Description</div>
// </div>
```

### Tech Site (like VentureBeat)
```typescript
// Often uses JSON-LD structured data:
const scriptRegex = /<script type="application\/ld\+json">(.*?)<\/script>/gs;
// Then parse the JSON
```

## Troubleshooting

### No matches found
- Check if HTML structure has changed
- Verify regex escaping
- Try broader patterns first, then narrow down

### Wrong content extracted
- Check capture groups in regex
- Verify you're using the right index (m[1], not m[0])
- Test with html.match() to see full matches

### Relative URLs not resolved
- Ensure you're using this.resolveUrl()
- Pass the source.url as base URL

### HTML entities not decoded
- Ensure you're using this.decodeHtml()
- Check for &amp;, &quot;, &lt;, &gt;, etc.

## Example Session

User: "编写html解析规则 https://venturebeat.com/"