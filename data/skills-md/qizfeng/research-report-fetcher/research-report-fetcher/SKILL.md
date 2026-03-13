---
name: "research-report-fetcher"
description: "从指定机构、公众号或数据源通过爬虫和api的方式获取研究报告并添加到数据库。Invoke when user asks to fetch research reports from an institution, WeChat public account, or any research source, or when user wants to add reports from a specific source."
---

# Research Report Fetcher

This skill helps you fetch research reports from various sources (institutions, WeChat public accounts, academic databases, etc.) and add them to the research report database.

## When to Use

- User asks to fetch reports from a specific institution (e.g., "从某某券商获取研究报告")
- User asks to fetch reports from a WeChat public account (e.g., "从因子动物园公众号获取报告")
- User asks to add reports from any research source
- User wants to expand the research report database with new sources

## Workflow

### 1. Understand the Source

First, gather information about the source:
- What is the institution/account name?
- What type of reports do they publish? (quantitative, financial, academic)
- What is their website or API endpoint?
- Do they have a public API or do you need to web scrape?

### 2. Search for Available Reports

Use web search to find:
- Recent reports from the source
- Report structure and format
- Access methods (API, RSS, direct download)

### 3. Create a Fetch Script

Create a Node.js script in `/scripts/` directory to:
- Connect to the data source
- Fetch report metadata (title, abstract, date, author, etc.)
- Download or generate report content
- Insert into the SQLite database
 
### 4. Script Template

```javascript
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, '../data/reports.db');
const db = new Database(dbPath);

async function main() {
  console.log('开始从 [SOURCE_NAME] 获取研究报告...\n');
  
  // Define reports to add
  const reports = [
    {
      title: "Report Title",
      abstract: "Report abstract...",
      keywords: ["keyword1", "keyword2"],
      author: "Author Name",
      publishDate: "2024-01-01",
      institution: "Institution Name",
      content: "Full report content...",
      downloadUrl: "https://example.com/download.pdf",
      shareUrl: "https://example.com/share"
    }
    // Add more reports...
  ];
  
  // Insert reports into database
  let addedCount = 0;
  for (const report of reports) {
    try {
      const insert = db.prepare(`
        INSERT INTO reports (title, abstract, keywords, author, publish_date, institution, content, download_url, share_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);
      
      insert.run(
        report.title,
        report.abstract,
        JSON.stringify(report.keywords),
        report.author,
        report.publishDate,
        report.institution,
        report.content,
        report.downloadUrl,
        report.shareUrl
      );
      
      addedCount++;
      console.log(`✓ 添加: ${report.title}`);
    } catch (error) {
      console.error(`✗ 添加失败: ${report.title}`, error.message);
    }
  }
  
  console.log(`\n成功添加 ${addedCount} 篇报告`);
  
  // Show statistics
  const totalReports = db.prepare('SELECT COUNT(*) as count FROM reports').get();
  console.log(`数据库中总报告数: ${totalReports.count}`);
  
  db.close();
}

main().catch(console.error);
```

### 5. Handle Different Source Types

#### For Institutions with APIs:
- Use axios or fetch to call their API
- Parse JSON/XML responses
- Handle pagination if needed

#### For WeChat Public Accounts:
- Search for their published articles
- Extract report content from web pages
- Use cheerio for HTML parsing if needed

#### For Academic Databases:
- Use arXiv API, SSRN, or other academic APIs
- Follow their API documentation
- Respect rate limits

### 6. Quality Control

Before adding reports, ensure they meet quality standards:
- Reports should be about quantitative investment/finance
- Titles and abstracts should clearly describe research content
- Content should have clear structure (introduction, methodology, results)
- Remove duplicates before insertion

**IMPORTANT - URL Validation (Required):**
- All download_url and share_url must be REAL and VALID URLs
- DO NOT use placeholder URLs like "https://example.com/..."
- Always verify URLs are accessible before adding to database
- If real URLs cannot be obtained, use alternative sources or search for accessible versions
- For WeChat articles, try to find the original article link or author's other published platforms
- For academic papers, use arXiv, SSRN, or other open access sources

**URL Verification Steps:**
1. Test download_url with curl -I to check HTTP status
2. Verify share_url points to accessible content
3. If URL returns 404 or is inaccessible, remove the report or find alternative source
4. Document all URL sources for transparency

### 7. Run and Verify

1. Run the script: `node scripts/fetch-[source]-reports.js`
2. Verify reports were added successfully
3. Check the website to see new reports displayed
4. Run deduplication if needed

## Examples

### Example 1: Fetch from a Securities Firm
```javascript
// scripts/fetch-citic-reports.js
const reports = [
  {
    title: "量化投资因子挖掘研究",
    abstract: "本文系统研究了量化投资中的因子挖掘方法论...",
    keywords: ["量化投资", "因子挖掘", "多因子模型"],
    author: "中信建投证券金融工程团队",
    publishDate: "2024-06-15",
    institution: "中信建投证券",
    // ... other fields
  }
];
```

### Example 2: Fetch from WeChat Public Account
```javascript
// scripts/fetch-factor-zoo-reports.js
const reports = [
  {
    title: "因子动物园：量化因子框架研究",
    abstract: "本文针对日益膨胀的因子动物园问题...",
    keywords: ["因子动物园", "因子压缩", "量化投资"],
    author: "石川、刘洋溢、连祥斌",
    publishDate: "2024-12-15",
    institution: "因子动物园公众号",
    // ... other fields
  }
];
```

## Database Schema

The reports table has the following structure:
- `id`: INTEGER PRIMARY KEY
- `title`: TEXT - Report title
- `abstract`: TEXT - Report abstract/summary
- `keywords`: TEXT (JSON array) - Keywords/tags
- `author`: TEXT - Author name(s)
- `publish_date`: TEXT (YYYY-MM-DD) - Publication date
- `institution`: TEXT - Source institution/account
- `content`: TEXT - Full report content
- `download_url`: TEXT - PDF download link
- `share_url`: TEXT - Share/view link

## Best Practices

1. **Always check for duplicates** before adding new reports
2. **Use consistent date format** (YYYY-MM-DD)
3. **Store keywords as JSON array** in the keywords field
4. **Include meaningful content** not just placeholder text
5. **Set proper institution name** for filtering and organization
6. **Validate URLs** before storing them
7. **Handle errors gracefully** and log them for debugging

## Common Issues

### Duplicate Reports
Use the `find-and-remove-duplicates.js` script to clean up duplicates after adding new reports.

### Invalid Dates
Ensure all dates are in YYYY-MM-DD format. Use `formatDate()` helper function.

### Missing Fields
All fields except `id` are required. Make sure to provide default values if data is unavailable.

### Database Locked
If you get "database is locked" error, ensure no other process is accessing the database.

## Available Fetch Scripts

The skill includes three ready-to-use fetch scripts in the `/scripts/` directory:

### 1. WeChat Public Account Fetcher
**File:** `scripts/fetch-wechat-public-account.js`

Fetches research reports from a specified WeChat public account.

```bash
node scripts/fetch-wechat-public-account.js "公众号名称"
```

**Features:**
- Supports custom public account name via command line argument
- Validates all download and share URLs before adding
- Skips invalid URLs automatically and reports them
- Includes sample quantitative research reports

### 2. Institution Fetcher
**File:** `scripts/fetch-institution-reports.js`

Fetches research reports from a specified institution (securities firm, fund, etc.).

```bash
node scripts/fetch-institution-reports.js "机构名称"
```

**Features:**
- Supports custom institution name via command line argument
- Includes sample reports for various topics (quantitative investment, machine learning, commodities, options, etc.)
- URL validation ensures only valid links are added
- Comprehensive report content with research background and methodology

### 3. Data Source Fetcher
**File:** `scripts/fetch-data-source.js`

Fetches research papers from academic data sources.

```bash
# Usage
node scripts/fetch-data-source.js <source_type> <search_terms> [max_results]

# Examples
node scripts/fetch-data-source.js arxiv "quantitative investment, machine learning" 5
node scripts/fetch-data-source.js ssrn "factor investing"
node scripts/fetch-data-source.js nber "asset pricing"
```

**Supported Data Sources:**
- `arxiv` - arXiv Open-Access Archive
- `ssrn` - Social Science Research Network
- `repec` - Research Papers in Economics
- `nber` - National Bureau of Economic Research
- `cepr` - Center for Economic Policy Research

**Features:**
- Supports multiple academic data sources
- Customizable search terms
- Configurable maximum results
- Automatic report generation with proper database format
