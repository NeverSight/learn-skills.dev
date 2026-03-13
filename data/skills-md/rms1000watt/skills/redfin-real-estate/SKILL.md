---
name: redfin-real-estate
description: Query Redfin.com for real estate prices and property listings in any area. Use this skill when the user wants to find homes for sale, get property prices, or search real estate listings by location with filters.
---

# Redfin Real Estate Query Skill

This skill enables querying Redfin.com for real estate property data using web scraping.

## When to Use This Skill

Use this skill when the user wants to:
- Find homes for sale in a specific city, zip code, or address
- Get current property prices and listings
- Search for real estate with filters (price range, beds, baths, property type)
- Look up property details like square footage, year built, listing status

## Prerequisites

Before using, ensure dependencies are installed:
```bash
pip install selenium beautifulsoup4 webdriver-manager pandas
```

## Usage

### Basic Syntax
```
Find homes for sale in [location]
Find properties in [location] under $[price]
Search [location] with [beds]+ beds and [baths]+ baths
Show me [property type] listings in [location]
```

### Important: Use Zipcodes
**For best results, use zipcodes instead of city names.** Redfin's URL structure works best with zipcodes.

```
✅ Good:  --location "78701"
✅ Good:  --location "90210" 
❌ Less reliable: --location "Austin TX"
```

### Examples
```
# Using zipcode (recommended)
Find homes for sale in 78701
Find properties in 78701 under $500000
Search 78701 with 3 beds

# City names may not work as well
Find homes for sale in Austin TX   (may not return results)
```

### Parameters
| Argument | Description | Example |
|----------|-------------|---------|
| `--location` | **Zipcode** (recommended) or city | `--location "78701"` |
| `--min-price` | Minimum price | `--min-price 300000` |
| `--max-price` | Maximum price | `--max-price 500000` |
| `--min-beds` | Minimum bedrooms | `--min-beds 3` |
| `--min-baths` | Minimum bathrooms | `--min-baths 2` |
| `--property-type` | house, condo, townhouse, land, multi-family | `--property-type condo` |
| `--limit` | Number of results (default: 10) | `--limit 20` |

**Note:** Price and bed/bath filters work best with zipcode-based searches. City name searches may return limited or no filtered results.

The scraper uses:
- Selenium with Chrome headless browser
- BeautifulSoup for HTML parsing
- Pandas for data formatting
- Human-like delays to avoid blocking

### Script Location
```
~/.agents/skills/redfin-real-estate/scripts/scraper.py
```

### Running the Scraper

The agent should run the scraper with appropriate parameters. Example invocation:
```bash
python ~/.agents/skills/redfin-real-estate/scripts/scraper.py --location "78701" --limit 10
```

### Available Command Line Arguments
| Argument | Description | Example |
|----------|-------------|---------|
| `--location` | **Zipcode** (recommended) or city name | `--location "78701"` |
| `--min-price` | Minimum price | `--min-price 300000` |
| `--max-price` | Maximum price | `--max-price 500000` |
| `--min-beds` | Minimum bedrooms | `--min-beds 3` |
| `--min-baths` | Minimum bathrooms | `--min-baths 2` |
| `--property-type` | house, condo, townhouse, land, multi-family | `--property-type condo` |
| `--limit` | Number of results (default: 10) | `--limit 20` |

## Output Format

Results display as a formatted table in the terminal:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        REDFIN PROPERTY SEARCH RESULTS                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Address                    │ Price       │ Beds │ Baths │ Sqft   │ Year ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  123 Main St, Austin, TX   │ $450,000    │ 3     │ 2     │ 1,850  │ 2015 ║
║  456 Oak Ave, Austin, TX    │ $525,000    │ 4     │ 3     │ 2,200  │ 2018 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Limitations

1. **Terms of Service**: Web scraping Redfin technically violates their ToS. Use responsibly.
2. **Rate Limiting**: Redfin may block IP addresses that make too many requests. The scraper includes delays to mitigate this.
3. **Dynamic Content**: Site structure changes may occasionally break the scraper.
4. **No Guarantee**: This is an unofficial method with no uptime guarantees.
5. **Filters**: Price/bed/bath filters work best with zipcode-based searches. City name searches may return limited results.
6. **Use Zipcodes**: For reliable results, always use zipcodes (e.g., "78701") instead of city names.

## Error Handling

If scraping fails:
- Check internet connection
- Redfin may be blocking requests (wait and retry)
- Site structure may have changed (may need script updates)
- Verify location format is valid

## Best Practices

1. Add delays between requests (built into script)
2. Don't make excessive queries in short time period
3. Use specific locations rather than broad searches
4. Filter results server-side with parameters when possible
