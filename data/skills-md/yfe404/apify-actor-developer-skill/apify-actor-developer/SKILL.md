---
name: apify-actor-developer
description: Build and monetize Apify Actors (web scrapers, automation tools, AI agents). Use when user wants to create an Actor, scraper, crawler, web automation, publish to Apify Store, set up pay-per-event/pay-per-result pricing, or integrate with Crawlee. Covers full lifecycle from development to monetization.
---

# Apify Actor Developer

Build, test, deploy, and monetize Apify Actors - serverless cloud applications for web scraping, data extraction, and automation.

## Prerequisites

Ensure these are available:
- Node.js 18+ or Python 3.9+
- Apify CLI: `npm install -g apify-cli`
- Logged in: `apify login`

## Workflow

### Phase 1: Project Initialization

1. **Create Actor from template**:
   ```bash
   # JavaScript templates
   apify create my-actor -t js-start                      # Basic starter
   apify create my-actor -t js-crawlee-cheerio            # Fast HTTP scraping
   apify create my-actor -t js-crawlee-playwright-chrome  # Browser automation
   apify create my-actor -t js-crawlee-puppeteer-chrome   # Puppeteer-based
   apify create my-actor -t js-langchain                  # LangChain AI
   apify create my-actor -t js-langgraph-agent            # LangGraph agent

   # TypeScript templates
   apify create my-actor -t ts-start                      # Basic starter
   apify create my-actor -t ts-crawlee-cheerio            # Fast HTTP scraping
   apify create my-actor -t ts-crawlee-playwright-chrome  # Browser automation
   apify create my-actor -t ts-crawlee-puppeteer-chrome   # Puppeteer-based
   apify create my-actor -t ts-mcp-proxy                  # MCP server proxy

   # Python templates
   apify create my-actor -t python-start                  # Basic starter
   apify create my-actor -t python-crawlee-beautifulsoup  # BeautifulSoup crawler
   apify create my-actor -t python-crawlee-playwright     # Playwright crawler
   apify create my-actor -t python-playwright             # Playwright scraper
   apify create my-actor -t python-selenium               # Selenium scraper
   apify create my-actor -t python-scrapy                 # Scrapy integration
   apify create my-actor -t python-crewai                 # CrewAI agents
   apify create my-actor -t python-langgraph              # LangGraph agents
   apify create my-actor -t python-pydanticai             # PydanticAI
   apify create my-actor -t python-mcp-proxy              # MCP server proxy
   ```

2. **Project structure created**:
   ```
   my-actor/
   ├── .actor/
   │   ├── actor.json           # Actor metadata and configuration
   │   ├── input_schema.json    # Input UI and validation
   │   ├── dataset_schema.json  # Output structure (optional)
   │   └── pay_per_event.json   # PPE monetization config (optional)
   ├── src/
   │   └── main.js              # Main entry point (or main.py)
   ├── README.md                # Documentation (becomes Store page)
   ├── Dockerfile               # Build configuration
   └── package.json             # Dependencies (or requirements.txt)
   ```

### Phase 2: Define Actor Configuration

3. **Configure `.actor/actor.json`**:
   ```json
   {
     "actorSpecification": 1,
     "name": "my-scraper",
     "title": "My Web Scraper",
     "description": "Scrapes data from websites efficiently",
     "version": "1.0",
     "buildTag": "latest",
     "input": "./input_schema.json",
     "storages": {
       "dataset": "./dataset_schema.json"
     }
   }
   ```

4. **Design input schema** (`.actor/input_schema.json`):
   ```json
   {
     "title": "My Scraper Input",
     "type": "object",
     "schemaVersion": 1,
     "description": "Configure the scraper settings. <a href='https://example.com/guide' target='_blank'>See full guide</a>",
     "properties": {
       "startUrls": {
         "title": "Start URLs",
         "type": "array",
         "description": "URLs to start scraping from",
         "editor": "requestListSources",
         "prefill": [{ "url": "https://example.com" }]
       },
       "maxItems": {
         "title": "Max Items",
         "type": "integer",
         "description": "Maximum number of items to scrape (0 = unlimited)",
         "default": 100,
         "minimum": 0,
         "editor": "number"
       },
       "proxyConfig": {
         "title": "Proxy Configuration",
         "type": "object",
         "description": "Select proxies for anti-blocking",
         "editor": "proxy",
         "prefill": { "useApifyProxy": true },
         "sectionCaption": "Advanced Settings",
         "sectionDescription": "Configure proxy and performance options"
       }
     },
     "required": ["startUrls"]
   }
   ```

   **Input schema editor types**:
   - `textfield` - Single line text
   - `textarea` - Multi-line text
   - `javascript` / `python` - Code with syntax highlighting
   - `number` - Numeric input with min/max validation
   - `select` - Dropdown (requires `enum` or `enumSuggestedValues`)
   - `requestListSources` - URL list for Crawlee
   - `proxy` - Apify proxy configuration
   - `datepicker` - Date selection (absolute/relative)
   - `checkbox` - Boolean toggle
   - `json` - Raw JSON editor
   - `keyValue` - Key-value pairs
   - `stringList` - Array of strings
   - `hidden` - Hidden field

### Phase 3: Implement Actor Logic

5. **JavaScript/TypeScript Actor** (`src/main.js`):
   ```javascript
   import { Actor } from 'apify';
   import { CheerioCrawler } from 'crawlee';

   await Actor.init();

   // Get input
   const { startUrls, maxItems = 100, proxyConfig } = await Actor.getInput();

   // Configure proxy
   const proxyConfiguration = await Actor.createProxyConfiguration(proxyConfig);

   let itemCount = 0;

   const crawler = new CheerioCrawler({
     proxyConfiguration,
     maxRequestsPerCrawl: maxItems || undefined,

     async requestHandler({ $, request, enqueueLinks }) {
       // Extract data
       const title = $('h1').text().trim();
       const description = $('meta[name="description"]').attr('content');

       // Save to dataset
       await Actor.pushData({
         url: request.url,
         title,
         description,
         scrapedAt: new Date().toISOString(),
       });

       itemCount++;
       if (maxItems && itemCount >= maxItems) return;

       // Follow links
       await enqueueLinks({
         globs: ['https://example.com/**'],
       });
     },
   });

   await crawler.run(startUrls);

   await Actor.exit(`Scraped ${itemCount} items`);
   ```

6. **Python Actor** (`src/main.py`):
   ```python
   import asyncio
   from apify import Actor

   async def main():
       async with Actor:
           # Get input
           actor_input = await Actor.get_input() or {}
           start_urls = actor_input.get('startUrls', [])
           max_items = actor_input.get('maxItems', 100)

           item_count = 0

           # Simple example without Crawlee
           for url_obj in start_urls:
               url = url_obj.get('url')

               # Your scraping logic here
               await Actor.push_data({
                   'url': url,
                   'status': 'scraped',
               })

               item_count += 1
               if max_items and item_count >= max_items:
                   break

           await Actor.set_status_message(f'Scraped {item_count} items')

   if __name__ == '__main__':
       asyncio.run(main())
   ```

7. **Python with Crawlee** (`src/main.py`):
   ```python
   import asyncio
   from apify import Actor
   from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

   async def main():
       async with Actor:
           actor_input = await Actor.get_input() or {}
           start_urls = [url['url'] for url in actor_input.get('startUrls', [])]

           crawler = PlaywrightCrawler(
               max_requests_per_crawl=actor_input.get('maxItems', 100),
           )

           @crawler.router.default_handler
           async def request_handler(context: PlaywrightCrawlingContext):
               page = context.page
               title = await page.title()

               await Actor.push_data({
                   'url': context.request.url,
                   'title': title,
               })

               await context.enqueue_links()

           await crawler.run(start_urls)

   if __name__ == '__main__':
       asyncio.run(main())
   ```

### Phase 4: Local Testing

8. **Test locally**:
   ```bash
   # Run with default input
   apify run

   # Run with purged storage (fresh start)
   apify run --purge

   # View results
   cat storage/datasets/default/*.json
   ```

9. **Validate input schema**:
   ```bash
   apify validate-schema .actor/input_schema.json
   ```

### Phase 5: Deploy to Apify Platform

10. **Push to Apify**:
    ```bash
    apify push
    ```

    This uploads code, builds Docker image, and creates/updates the Actor.

11. **Alternative: GitHub integration**:
    - Connect GitHub repo in Apify Console
    - Auto-builds on push to main branch
    - Better for collaboration and version control

### Phase 6: Write README Documentation

12. **Create compelling README.md**:
    ```markdown
    # My Web Scraper

    Scrape data from websites efficiently with anti-blocking and proxy support.

    ## Features
    - Fast parallel scraping with Crawlee
    - Automatic proxy rotation
    - Structured JSON/CSV output
    - Handles JavaScript-rendered pages

    ## Input

    | Parameter | Type | Required | Description |
    |-----------|------|----------|-------------|
    | startUrls | array | Yes | URLs to start scraping |
    | maxItems | integer | No | Max items (default: 100) |

    ## Output

    ```json
    {
      "url": "https://example.com/page",
      "title": "Page Title",
      "description": "Meta description",
      "scrapedAt": "2024-01-15T10:30:00Z"
    }
    ```

    ## Usage

    ### Via Apify Console
    1. Click "Start" on the Actor page
    2. Enter your start URLs
    3. Click "Run"

    ### Via API
    ```bash
    curl -X POST "https://api.apify.com/v2/acts/YOUR_ACTOR/runs" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"startUrls": [{"url": "https://example.com"}]}'
    ```

    ## Integrations
    - Zapier, Make, n8n support
    - Webhooks for notifications
    - Schedule runs via cron

    ## Cost Estimation
    ~$X per 1,000 results using datacenter proxies.
    ```

### Phase 7: Monetization Setup

13. **Choose pricing model**:

    **Option A: Pay-Per-Event (PPE)** - Most flexible, recommended
    - Charge for custom events (pages scraped, API calls, etc.)
    - You earn 80% revenue minus platform costs
    - AI/MCP compatible, priority store placement

    **Option B: Pay-Per-Result (PPR)**
    - Charge per dataset item produced
    - Simpler to implement
    - You earn 80% revenue minus platform costs

    **Option C: Rental**
    - Monthly subscription fee
    - Users pay their own platform costs
    - You earn 80% of rental fee

14. **Implement PPE charging** (`.actor/pay_per_event.json`):
    ```json
    {
      "schemaVersion": 1,
      "events": [
        {
          "name": "apify-actor-start",
          "priceUsd": 0.00005,
          "description": "Actor initialization"
        },
        {
          "name": "page-scraped",
          "priceUsd": 0.002,
          "description": "Per page scraped"
        },
        {
          "name": "result-saved",
          "priceUsd": 0.001,
          "description": "Per result saved to dataset"
        }
      ]
    }
    ```

15. **Charge events in code**:
    ```javascript
    // JavaScript - Option 1: Charge with pushData
    await Actor.pushData({ title, url }, 'result-saved');

    // JavaScript - Option 2: Charge separately
    await Actor.charge({ eventName: 'page-scraped', count: 1 });
    ```

    ```python
    # Python
    await Actor.push_data({'title': title, 'url': url}, 'result-saved')
    await Actor.charge(event_name='page-scraped', count=1)
    ```

16. **Configure in Apify Console**:
    - Go to Actor -> Publication -> Monetization
    - Set up billing details for payouts
    - Choose pricing model via wizard
    - Set event prices

### Phase 8: Publish to Store

17. **Publication checklist**:
    - [ ] Comprehensive README with examples
    - [ ] Well-designed input schema with prefills
    - [ ] Clear title and description
    - [ ] Actor icon/image
    - [ ] Category selection
    - [ ] Test runs successful
    - [ ] Monetization configured

18. **SEO optimization**:
    - Use keywords in title and description
    - Add "use cases" section
    - Include integration examples
    - Mention specific websites/platforms supported

## Apify SDK Reference

### Core Methods

```javascript
// Initialize/Exit
await Actor.init();
await Actor.exit('Success message');
await Actor.fail('Error message');

// Input/Output
const input = await Actor.getInput();
await Actor.pushData({ key: 'value' });
await Actor.setValue('key', 'value');  // Key-value store
const value = await Actor.getValue('key');

// Storage
const dataset = await Actor.openDataset('name');
const kvStore = await Actor.openKeyValueStore('name');
const requestQueue = await Actor.openRequestQueue('name');

// Platform features
const proxyConfig = await Actor.createProxyConfiguration(input.proxy);
await Actor.setStatusMessage('Processing...');

// PPE charging
await Actor.charge({ eventName: 'my-event', count: 1 });
```

### Crawlee Crawler Types

| Crawler | Use Case | Speed | JS Rendering |
|---------|----------|-------|--------------|
| CheerioCrawler | Static HTML | Fastest | No |
| PlaywrightCrawler | Dynamic pages | Medium | Yes |
| PuppeteerCrawler | Dynamic pages | Medium | Yes |
| HttpCrawler | API calls | Fastest | No |
| JSDOMCrawler | Light DOM parsing | Fast | Partial |

## All Available Templates

### JavaScript
- `js-start` - Basic starter
- `js-crawlee-cheerio` - Cheerio crawler
- `js-crawlee-playwright-chrome` - Playwright browser
- `js-crawlee-puppeteer-chrome` - Puppeteer browser
- `js-crawlee-playwright-camoufox` - Camoufox (anti-detect)
- `js-langchain` - LangChain integration
- `js-langgraph-agent` - LangGraph agent
- `js-standby` - HTTP server (Standby mode)
- `js-empty` - Empty project

### TypeScript
- `ts-start` - Basic starter
- `ts-crawlee-cheerio` - Cheerio crawler
- `ts-crawlee-playwright-chrome` - Playwright browser
- `ts-crawlee-puppeteer-chrome` - Puppeteer browser
- `ts-mcp-proxy` - MCP server proxy
- `ts-mcp-empty` - Empty MCP server
- `ts-standby` - HTTP server
- `ts-empty` - Empty project

### Python
- `python-start` - Basic starter
- `python-crawlee-beautifulsoup` - BeautifulSoup crawler
- `python-crawlee-playwright` - Playwright crawler
- `python-crawlee-parsel` - Parsel crawler
- `python-playwright` - Playwright scraper
- `python-selenium` - Selenium scraper
- `python-scrapy` - Scrapy integration
- `python-crewai` - CrewAI agents
- `python-langgraph` - LangGraph agents
- `python-pydanticai` - PydanticAI
- `python-mcp-proxy` - MCP server proxy
- `python-standby` - HTTP server
- `python-empty` - Empty project

## Pricing Strategy Tips

1. **Research competitors** - Check similar Actors in Store
2. **Calculate costs** - Run tests, check Analytics tab
3. **Start competitive** - Most prices: $1-10 per 1,000 results
4. **Use PPE for flexibility** - Charge for what users actually use
5. **Offer free tier** - Low maxItems for testing

## Maintenance Commitment

Reserve ~2 hours/week for:
- Bug fixes and user support
- Keeping up with website changes
- Responding to Issues tab
- Improving documentation

## Examples

### Example 1: Simple Product Scraper
```javascript
import { Actor } from 'apify';
import { CheerioCrawler } from 'crawlee';

await Actor.init();
const { startUrls } = await Actor.getInput();

const crawler = new CheerioCrawler({
  async requestHandler({ $, request }) {
    const products = [];
    $('.product').each((_, el) => {
      products.push({
        name: $(el).find('.name').text(),
        price: $(el).find('.price').text(),
        url: request.url,
      });
    });
    await Actor.pushData(products);
  },
});

await crawler.run(startUrls);
await Actor.exit();
```

### Example 2: AI Agent Actor (Python with CrewAI)
```python
import asyncio
from apify import Actor
from crewai import Agent, Task, Crew

async def main():
    async with Actor:
        input_data = await Actor.get_input()
        query = input_data.get('query')

        researcher = Agent(
            role='Researcher',
            goal='Find accurate information',
            backstory='Expert researcher',
        )

        task = Task(
            description=query,
            agent=researcher,
        )

        crew = Crew(agents=[researcher], tasks=[task])
        result = crew.kickoff()

        await Actor.push_data({'query': query, 'result': str(result)})

if __name__ == '__main__':
    asyncio.run(main())
```

## Resources

- Apify SDK JS: https://docs.apify.com/sdk/js
- Apify SDK Python: https://docs.apify.com/sdk/python
- Crawlee: https://crawlee.dev
- Actor Templates: https://apify.com/templates
- Apify Academy: https://docs.apify.com/academy
- Store Optimization: https://docs.apify.com/academy/actor-marketing-playbook
