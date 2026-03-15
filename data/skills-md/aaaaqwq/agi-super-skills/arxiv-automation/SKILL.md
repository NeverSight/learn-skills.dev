---
name: arxiv-automation
description: "Search and monitor arXiv papers. Query by topic, author, or category. Track new papers, download PDFs, and summarize abstracts for research workflows."
---

# arXiv Automation

Search, monitor, and analyze academic papers from arXiv.

## Capabilities

- Search papers by keyword, author, category
- Monitor new submissions in specific categories
- Download PDFs for analysis
- Extract and summarize abstracts
- Track citation-worthy papers

## Usage

### Search Papers (arXiv API)

```python
import urllib.request, urllib.parse, xml.etree.ElementTree as ET

def search_arxiv(query, max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    })
    url = base_url + params
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in root.findall("atom:entry", ns):
        papers.append({
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip()[:200],
            "link": entry.find("atom:id", ns).text,
            "published": entry.find("atom:published", ns).text,
            "authors": [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        })
    return papers

# Example: search for LLM agent papers
papers = search_arxiv("all:LLM AND all:agent", max_results=5)
for p in papers:
    print(f"{p['title']}\n  {p['link']}\n  {', '.join(p['authors'][:3])}\n")
```

### Monitor Categories

Common CS categories:
| Category | Description |
|----------|-------------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language (NLP) |
| cs.LG | Machine Learning |
| cs.CV | Computer Vision |
| cs.SE | Software Engineering |

RSS feeds: `http://arxiv.org/rss/{category}` (e.g., `http://arxiv.org/rss/cs.AI`)

### Download PDF

```python
# arXiv ID format: 2401.12345
arxiv_id = "2401.12345"
pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
```

## Rate Limits

- arXiv API: max 1 request per 3 seconds
- Be respectful of arXiv's resources
- Use RSS feeds for monitoring (less load than API queries)

## Integration

Combine with `pdf` skill for PDF text extraction and analysis.
Combine with `rss-automation` for periodic monitoring of new papers.
