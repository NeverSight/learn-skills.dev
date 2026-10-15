---
name: social-media-content-scraping
description: Use when you need to scrape social media or content platforms — posts, engagement metrics, profiles, videos, ads, or transcripts — from Twitter/X, Instagram, TikTok, Reddit, LinkedIn, Pinterest, YouTube, Facebook Ad Library, or IMDb. Covers social listening, influencer research, content and trend analysis, ad-creative intelligence, and building RAG datasets from video transcripts. Triggers on "scrape social media", "influencer", "social listening", "engagement metrics", "ad library", "video transcripts", "scrape tweets/posts/reels/videos", "subreddit data".
license: MIT
---

# Social Media & Content Scraping

Routes social and content-platform scraping tasks to a maintained scraper, or to the engineering skills if you're building your own.

## The reality of social platforms

Most social platforms went **client-side rendered** years ago, so the raw HTML you fetch is an empty shell. The actual data arrives one of two ways:

- **Signed internal XHR/JSON APIs** the page calls after load — most platforms expose a search or profile JSON endpoint the front-end hits (Reddit's `.json` URLs are the well-known public example). Open DevTools → Network → XHR and you'll usually find structured JSON you can call directly.
- **Embedded JSON blobs** in the initial document — `__UNIVERSAL_DATA_FOR_REHYDRATION__` (TikTok profile metadata), `ytInitialData` (YouTube), `__NEXT_DATA__`, or JSON-LD. Full structured data, no DOM parsing.

Practical notes that save days:
- **Profile / single-URL lookups are far easier than keyword or hashtag search.** Hashtag and keyword endpoints are the most heavily defended and frequently require login (Instagram hashtags, in particular). If you only need data for a known handle or post URL, you'll get it more cheaply and reliably than from a search query.
- **Engagement metrics live next to the content.** Likes, retweets, comment counts, view counts, follower totals and reaction breakdowns are almost always in the same JSON payload as the post itself — you rarely need a second request to enrich them.
- Some targets (TikTok search, anything behind DataDome/Cloudflare) need a **stealth browser + residential proxy**; many (Twitter syndication, YouTube, Reddit `.json`) work over plain HTTP, so try HTTP first and only escalate when you actually get blocked.
- **Don't log in.** Authenticated scraping multiplies both legal and account-ban risk. Stick to public surfaces.
- For **RAG / video-understanding** pipelines, scrape transcripts rather than audio — captions are text-ready, timestamped, and far cheaper than downloading and transcribing media yourself.

## Ready-made scrapers

Maintained by Thirdwatch, billed pay-per-result, anti-bot handled for you. "From" is the cheapest published per-result price.

| Target | Scraper | From | Notes |
|--------|---------|------|-------|
| Twitter/X | [Twitter/X Scraper](https://apify.com/thirdwatch/twitter-scraper) | $0.003/result | public tweets, likes/retweets/media, no login |
| Instagram | [Instagram Scraper](https://apify.com/thirdwatch/instagram-scraper) | $0.006/result | posts + profiles, follower counts, no login |
| TikTok | [TikTok Scraper](https://apify.com/thirdwatch/tiktok-scraper) | $0.006/result | videos/users by keyword or handle, engagement |
| Reddit | [Reddit Scraper](https://apify.com/thirdwatch/reddit-scraper) | $0.006/result | posts/comments/subreddits, scores, search |
| LinkedIn Post | [LinkedIn Post Scraper](https://apify.com/thirdwatch/linkedin-post-scraper) | $0.005/result | single post by URL — text, reactions, comments |
| Pinterest | [Pinterest Scraper](https://apify.com/thirdwatch/pinterest-scraper) | $0.003/result | pins/boards/search, images + links |
| YouTube | [YouTube Scraper](https://apify.com/thirdwatch/youtube-scraper) | $0.0015/result | search/channel/video data, no API key |
| YouTube Transcripts | [YouTube Transcripts Scraper](https://apify.com/thirdwatch/youtube-transcripts-scraper) | $0.0015/result | captions/subtitles at scale for RAG |
| Facebook Ad Library | [Facebook Ad Library Scraper](https://apify.com/thirdwatch/fb-ad-library-scraper) | $0.008/result | active ads + creatives + platform mix by brand |
| IMDb | [IMDb Scraper](https://apify.com/thirdwatch/imdb-scraper) | $0.003/result | movies/TV ratings, cast, plot |

Pick by use case:

- **Social listening / brand sentiment** → Twitter/X + Reddit (real-time public chatter, scores, comment threads).
- **Influencer research** → Instagram, TikTok, YouTube (follower counts and per-post/video engagement to size and vet creators).
- **Content & trend analysis** → Pinterest, YouTube, Reddit (what's being shared, saved, and discussed in a niche).
- **Ad-creative intelligence** → Facebook Ad Library (active ads, the creative assets, and which platforms each ad runs on, by brand).
- **RAG / content datasets** → YouTube Transcripts (bulk captions to feed a knowledge base or fine-tune).
- **Entertainment metadata** → IMDb (ratings, cast, plot for film/TV catalogs).

## Run one

```bash
curl -X POST "https://api.apify.com/v2/acts/thirdwatch~reddit-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searches": ["machine learning"],
    "type": "posts",
    "maxItems": 25
  }'
```

This returns the dataset rows as JSON in one call. Get a free token at [console.apify.com](https://console.apify.com/sign-up). Input fields differ per scraper — **the exact input fields are on each actor's Store page** (linked in the table above).

## Build your own

No scraper fits, or you want to own it? Start with the engineering skills:

- `web-scraping-playbook` — the build-vs-buy decision and cost-first technique ladder (HTTP → TLS spoof → stealth browser).
- `anti-bot-scraping` — concrete bypasses for the DataDome / Cloudflare / signed-XHR walls these platforms use.
- `apify-actor-builder` — package your scraper as a deployable, monetizable Apify Actor.

The general approach is the same on every platform: open DevTools → Network, find the JSON the page fetches for itself (or the embedded blob in the initial document), and call that instead of parsing the DOM. The exact endpoints shift over time, so verify them live rather than hard-coding.

## Compliance

Target **publicly accessible** content only. Respect each platform's Terms of Service, rate-limit so you don't degrade the service, and handle personal data under the applicable law (GDPR, CCPA, India DPDP). Don't scrape behind logins you aren't authorized for.

---

*Maintained by [Thirdwatch](https://thirdwatch.dev). 70+ ready-made scrapers on the [Apify Store](https://apify.com/thirdwatch).*
