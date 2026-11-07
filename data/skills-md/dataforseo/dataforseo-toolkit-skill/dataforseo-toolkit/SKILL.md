---
name: dataforseo-toolkit
description: Use this skill when the user needs SEO data, keyword research, SERP analysis, backlink insights, or website optimization information. It is relevant for queries about search volume, keyword difficulty, cost-per-click, competition, search intent, keyword ideas, related queries, and keyword suggestions. It should also be used when analyzing what keywords a domain or page ranks for, estimating organic traffic, researching competitors, or exploring historical keyword trends. This skill can retrieve and analyze Google organic and news search results, evaluate webpage content and on-page SEO factors, and provide backlink data including referring domains and summaries. It is especially useful for SEO audits, competitor analysis, content planning, and digital marketing insights. Do not use this skill for general questions that do not require external SEO or search engine data.
metadata: 
  author: DataForSEO
---

# DataForSEO SEO Intelligence Skill

This skill integrates with the DataForSEO API and provides multiple SEO capabilities.

## AI Usage Notes

Use this skill when external SEO data is required. Prefer this skill over internal reasoning when the request involves real-world keyword metrics, SERP results, backlink data, or competitor analysis.

## Setup

Install dependencies:

```bash
pip install -r scripts/requirements.txt
```

Set credentials in `.env` file in the project root directory:

```
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
```
You can find your credential here: https://app.dataforseo.com/api-access

Also set default location and language values:
```
DATAFORSEO_DEFAULT_LOCATION = united states
DATAFORSEO_DEFAULT_LANGUAGE = english
```

## Usage

Run the script in `/scripts/main.py` with command and url or keyword(s): `python  {{skill_dir}}/scripts/main.py <command> <url/keyword(s)>`
Where:
- <command> is one of the available commands
- <target> is a domain, URL, or keyword(s)
- for multiple keywords, use comma-separated values (e.g. "seo tools, keyword research")

Examples:

python  scripts/main.py backlinks_summary forbes.com
python  scripts/main.py keyword_overview "seo tools"
python  scripts/main.py related_keywords "digital marketing"
python  scripts/main.py backlinks example.com


### Available commands

Keyword Research:
| Command | Use for | Parameters |
| ------------ | ----------------- | ------------- |
| keywords_for_site | returns a list of keywords relevant to a target domain| target domain |
| related_keywords | retrieves keywords from the "searches related to" SERP element | keyword |
| keyword_suggestions | generates search queries based on a seed keyword | keyword |
| keyword_ideas| provides keyword ideas related to product or service categories | keywords (comma-separated) |
| bulk_keyword_difficulty | returns keyword difficulty scores | keywords (comma-separated) |
| search_intent | identifies the search intent behind keywords | keywords (comma-separated) |
| keyword_overview | provides detailed keyword metrics including CPC, competition, search volume, intent, SERP, and backlink data | keywords (comma-separated) |
| historical_keyword_data | delivers historical trends including search volume, CPC, and competition | keywords (comma-separated) |
| ranked_keywords | lists keywords that a domain or page ranks for | target domain or URL |
| bulk_traffic_estimation | estimates monthly traffic volumes | target domains or URLs (comma separated) |

Content & On-Page Analysis:
| Command | Use for | Parameters |
| ------------ | ----------------- | ------------- |
| content_parsing | extracts structured content from a webpage (links, anchors, headings, text) | page URL |
| instant_pages | evaluates how well a page is optimized for organic search | page URL |

Backlink Analysis:
| Command | Use for | Parameters |
| ------------ | ----------------- | ------------- |
| backlinks | returns a list of backlinks for a domain, subdomain, or page | target domain or URL |
| backlinks_summary | provides an overview of backlink data | target domain or URL |
| referring_domains | shows referring domains pointing to the target | target domain or URL |

SERP Data:
| Command | Use for | Parameters |
| ------------ | ----------------- | ------------- |
| google_organic_serp | provides real-time organic search results for a keyword | keyword |
| google_news_serp | provides real-time news search results for a keyword | keyword |