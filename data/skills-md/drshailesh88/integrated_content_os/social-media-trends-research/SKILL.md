---
name: social-media-trends-research
description: "Programmatic social media and marketing research using free tools: pytrends (Google Trends), yars (Reddit without API keys), and Perplexity MCP (Twitter/TikTok/Web). Use when finding trending topics in a niche, tracking keyword velocity and volume, monitoring Reddit discussions, discovering what's going viral, or researching content opportunities before writing. Zero-cost research stack with built-in rate limiting. Complements content-marketing-social-listening skill with executable code."
---

# Social Media Trends Research

## Overview

Programmatic trend research using three free tools:
- **pytrends**: Google Trends data (velocity, volume, related queries)
- **yars**: Reddit scraping without API keys
- **Perplexity MCP**: Twitter/TikTok/Web trends (via Claude's built-in MCP)

This skill provides executable code for trend research. Use alongside `content-marketing-social-listening` for strategy and `perplexity-search` for deep queries.

## Quick Setup

```bash
# Install dependencies (one-time)
pip install pytrends requests --break-system-packages
```

No API keys required. Reddit scraping uses public .json endpoints.

---

## Tool 1: pytrends (Google Trends)

### What It Provides
- Real-time trending searches by country
- Interest over time for keywords
- Related queries (rising = velocity indicators)
- Interest by region
- Related topics

### Basic Usage

```python
from pytrends.request import TrendReq
import time

# Initialize (no API key needed)
pytrends = TrendReq(hl='en-US', tz=330)  # tz=330 for India (IST)

# Get real-time trending searches
trending = pytrends.trending_searches(pn='india')
print(trending.head(20))
```

### Research Your Niche Keywords

```python
from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=330)

# Define your niche keywords (max 5 per request)
keywords = ['heart health', 'cardiology', 'cholesterol']

# Build payload
pytrends.build_payload(keywords, timeframe='now 7-d', geo='IN')

# Get interest over time
interest = pytrends.interest_over_time()
print(interest)

# CRITICAL: Wait between requests to avoid rate limiting
time.sleep(3)

# Get related queries (THIS IS GOLD - shows rising topics)
related = pytrends.related_queries()
for kw in keywords:
    print(f"\n=== Rising queries for '{kw}' ===")
    rising = related[kw]['rising']
    if rising is not None:
        print(rising.head(10))
```

### Find Viral/Breakout Topics

```python
from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=330)

def find_breakout_topics(keyword, geo=''):
    """Find topics with explosive growth (potential viral content)"""
    pytrends.build_payload([keyword], timeframe='today 3-m', geo=geo)
    time.sleep(3)  # Rate limiting
    
    related = pytrends.related_queries()
    rising = related[keyword]['rising']
    
    if rising is not None:
        # Filter for breakout topics (marked as "Breakout" or very high %)
        breakouts = rising[rising['value'] >= 1000]  # 1000%+ growth
        return breakouts
    return None

# Example usage
breakouts = find_breakout_topics('heart health', geo='IN')
print(breakouts)
```

### Rate Limiting Rules for pytrends

```python
import time

# SAFE: 1 request per 3-5 seconds for casual use
time.sleep(5)

# BULK RESEARCH: 1 request per 60 seconds
time.sleep(60)

# If you get rate limited (429 error): Wait 60-120 seconds, then continue
# If persistent issues: Wait 4-6 hours before resuming
```

### Useful Timeframes

| Timeframe | Use Case |
|-----------|----------|
| `'now 1-H'` | Last hour (real-time spikes) |
| `'now 4-H'` | Last 4 hours |
| `'now 1-d'` | Last 24 hours |
| `'now 7-d'` | Last 7 days (best for trends) |
| `'today 1-m'` | Last 30 days |
| `'today 3-m'` | Last 90 days (velocity analysis) |
| `'today 12-m'` | Last year (seasonal patterns) |

---

## Tool 2: Reddit (No API Keys - Public JSON Endpoints)

### What It Provides
- Search Reddit for any keyword
- Get hot/top/rising posts from subreddits
- Post engagement data (upvotes, comments)
- No authentication required

### Basic Usage

```python
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Search Reddit for your niche
url = "https://www.reddit.com/search.json?q=heart+health&limit=10&sort=relevance&t=week"
response = requests.get(url, headers=headers, timeout=10)
data = response.json()

# Display results
for child in data.get('data', {}).get('children', []):
    post = child.get('data', {})
    print(f"Title: {post.get('title')}")
    print(f"Subreddit: r/{post.get('subreddit')}")
    print(f"Score: {post.get('score')}")
    print("---")
```

### Get Hot Posts from Specific Subreddits

```python
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Define subreddits relevant to your niche
subreddits = ['cardiology', 'health', 'medicine']

for sub in subreddits:
    print(f"\n=== Hot in r/{sub} ===")
    try:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        for child in data.get('data', {}).get('children', [])[:5]:
            post = child.get('data', {})
            print(f"- [{post.get('score')}] {post.get('title')[:60]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(3)  # Rate limiting between requests
```

### Using the Bundled Reddit Scraper

A helper class is included in `scripts/reddit_scraper.py`:

```python
from scripts.reddit_scraper import SimpleRedditScraper

scraper = SimpleRedditScraper()

# Search
results = scraper.search("heart health tips", limit=20)
for post in results['posts']:
    print(f"[{post['score']}] r/{post['subreddit']}: {post['title']}")

# Get subreddit hot posts
results = scraper.get_subreddit("health", sort="hot", limit=10)
for post in results['posts']:
    print(f"[{post['score']}] {post['title']}")
```

### Rate Limiting Rules for Reddit

```python
import time

# SAFE: 1 request per 2-3 seconds
time.sleep(3)

# If you get 429 errors: Wait 5-10 minutes
# Never do more than 60 requests per hour
```

---

## Tool 3: Perplexity MCP (Twitter/TikTok/Web)

Use Claude's built-in Perplexity MCP for platforms you can't scrape directly.

### Query Templates for Trend Research

**Twitter/X Trends:**
```
"What are the most discussed [YOUR NICHE] topics on Twitter/X this week? 
Include specific examples of viral tweets and their engagement."
```

**TikTok Trends (works from India):**
```
"What [YOUR NICHE] content is trending on TikTok right now? 
Include hashtags, view counts, and content formats that are working."
```

**YouTube Trends:**
```
"What [YOUR NICHE] videos are getting the most views on YouTube this week? 
Include channel names, view counts, and video topics."
```

**LinkedIn Professional:**
```
"What [YOUR NICHE] topics are professionals discussing on LinkedIn this week? 
Include examples of high-engagement posts."
```

**General Viral Content:**
```
"What [YOUR NICHE] content has gone viral across social media in the past 7 days? 
Include platform, format, and why it resonated."
```

### Using Perplexity with perplexity-search Skill

If you have the perplexity-search skill installed:

```bash
python scripts/perplexity_search.py \
  "What cardiology topics are trending on Twitter and TikTok this week? Include specific viral posts and hashtags." \
  --model sonar-pro
```

---

## Combined Research Workflow

### Complete Trend Research Function

```python
from pytrends.request import TrendReq
import requests
import time
import json
from datetime import datetime

class TrendResearcher:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=330)
        self.reddit_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _reddit_request(self, url):
        """Make a Reddit API request."""
        try:
            response = requests.get(url, headers=self.reddit_headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def research_niche(self, keywords, subreddits=None, geo='IN'):
        """
        Complete trend research for a niche.
        
        Args:
            keywords: List of keywords (max 5)
            subreddits: List of subreddit names to monitor
            geo: Geographic region code
        
        Returns:
            Dictionary with all research data
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'keywords': keywords,
            'google_trends': {},
            'reddit': {},
            'recommendations': []
        }
        
        # 1. Google Trends - Interest Over Time
        print("📊 Fetching Google Trends data...")
        try:
            self.pytrends.build_payload(keywords[:5], timeframe='now 7-d', geo=geo)
            results['google_trends']['interest'] = self.pytrends.interest_over_time().to_dict()
            time.sleep(5)
            
            # Related queries (rising topics)
            related = self.pytrends.related_queries()
            results['google_trends']['rising_queries'] = {}
            for kw in keywords[:5]:
                rising = related[kw]['rising']
                if rising is not None:
                    results['google_trends']['rising_queries'][kw] = rising.head(10).to_dict()
            time.sleep(5)
        except Exception as e:
            results['google_trends']['error'] = str(e)
        
        # 2. Reddit Research
        print("👽 Fetching Reddit discussions...")
        if subreddits:
            for sub in subreddits[:5]:
                try:
                    url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
                    data = self._reddit_request(url)
                    posts = []
                    for child in data.get('data', {}).get('children', [])[:5]:
                        post = child.get('data', {})
                        posts.append({
                            'title': post.get('title', ''),
                            'score': post.get('score', 0),
                            'comments': post.get('num_comments', 0)
                        })
                    results['reddit'][sub] = posts
                    time.sleep(3)
                except Exception as e:
                    results['reddit'][sub] = {'error': str(e)}
        
        # 3. Keyword search on Reddit
        print("🔍 Searching Reddit for keywords...")
        for kw in keywords[:3]:
            try:
                url = f"https://www.reddit.com/search.json?q={kw}&limit=10&sort=relevance&t=week"
                data = self._reddit_request(url)
                posts = []
                for child in data.get('data', {}).get('children', [])[:5]:
                    post = child.get('data', {})
                    posts.append({
                        'title': post.get('title', ''),
                        'subreddit': post.get('subreddit', ''),
                        'score': post.get('score', 0),
                        'comments': post.get('num_comments', 0)
                    })
                results['reddit'][f'search_{kw}'] = posts
                time.sleep(3)
            except Exception as e:
                results['reddit'][f'search_{kw}'] = {'error': str(e)}
        
        # 4. Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _generate_recommendations(self, data):
        """Generate content recommendations from research data"""
        recommendations = []
        
        # From rising queries
        rising = data.get('google_trends', {}).get('rising_queries', {})
        for kw, queries in rising.items():
            if isinstance(queries, dict) and 'query' in queries:
                for query in list(queries['query'].values())[:3]:
                    recommendations.append({
                        'source': 'Google Trends',
                        'topic': query,
                        'reason': f"Rising search term related to '{kw}'"
                    })
        
        # From Reddit hot posts
        for sub, posts in data.get('reddit', {}).items():
            if isinstance(posts, list):
                for post in posts[:2]:
                    if post.get('score', 0) > 50:
                        recommendations.append({
                            'source': f'Reddit r/{sub}',
                            'topic': post.get('title', ''),
                            'reason': f"High engagement ({post.get('score')} upvotes)"
                        })
        
        return recommendations

# Usage Example
if __name__ == "__main__":
    researcher = TrendResearcher()
    
    results = researcher.research_niche(
        keywords=['heart health', 'cardiology', 'cholesterol'],
        subreddits=['cardiology', 'health', 'medicine'],
        geo='IN'
    )
    
    # Save results
    with open('trend_research.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Print recommendations
    print("\n🎯 CONTENT RECOMMENDATIONS:")
    for rec in results['recommendations']:
        print(f"- [{rec['source']}] {rec['topic']}")
        print(f"  Why: {rec['reason']}")
```

---

## Quick Reference Commands

### Daily Trend Check (5 minutes)

```python
from pytrends.request import TrendReq
import requests
import time

# Quick Google Trends check
pytrends = TrendReq(hl='en-US', tz=330)
pytrends.build_payload(['your keyword'], timeframe='now 1-d')
print(pytrends.related_queries()['your keyword']['rising'])

time.sleep(5)

# Quick Reddit check  
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://www.reddit.com/search.json?q=your+keyword&limit=10&t=day"
response = requests.get(url, headers=headers, timeout=10)
data = response.json()
for child in data.get('data', {}).get('children', [])[:5]:
    post = child.get('data', {})
    print(f"[{post.get('score')}] {post.get('title')}")
```

### Weekly Deep Dive

```python
# Use the TrendResearcher class above with:
# - 5 core keywords
# - 5 relevant subreddits
# - 90-day timeframe for velocity analysis

# Then use Perplexity MCP for:
# - Twitter trends in your niche
# - TikTok viral content
# - YouTube trending videos
# - LinkedIn discussions
```

---

## Integration with Writing Skills

After research, pass findings to your writing skills:

```
1. Run trend research (this skill)
2. Identify top 3-5 opportunities
3. Use content-marketing-social-listening for strategy
4. Use cardiology-content-repurposer or similar for content creation
5. Use authentic-voice for final polish
```

---

## Troubleshooting

### pytrends Issues

| Error | Solution |
|-------|----------|
| 429 Too Many Requests | Wait 60 seconds, then increase sleep time |
| Empty results | Check if keyword has search volume |
| Connection error | Check internet, retry in 5 minutes |

### Reddit Issues

| Error | Solution |
|-------|----------|
| 429 Rate Limited | Wait 10 minutes |
| Subreddit not found | Check subreddit name spelling |
| Empty results | Subreddit may be private or quarantined |
| Connection timeout | Increase timeout, check internet |

---

## Best Practices

1. **Always use rate limiting**: Sleep between requests
2. **Research in batches**: Do weekly deep dives, not constant polling
3. **Save results**: Cache research data locally
4. **Cross-reference**: Validate trends across multiple platforms
5. **Act fast**: Viral windows are short (24-72 hours)

---

## Platform Coverage Summary

| Platform | Tool | Cost | Risk |
|----------|------|------|------|
| Google Trends | pytrends | Free | Very Low |
| Reddit | requests (public JSON) | Free | Low |
| Twitter/X | Perplexity MCP | Free* | None |
| TikTok | Perplexity MCP | Free* | None |
| YouTube | Perplexity MCP | Free* | None |
| LinkedIn | Perplexity MCP | Free* | None |

*Uses Claude's built-in MCP or OpenRouter credits if using perplexity-search skill

---

## Bundled Resources

- `scripts/trend_research.py`: Main CLI tool for complete trend research
- `scripts/reddit_scraper.py`: Simple Reddit scraper class (no API keys)
