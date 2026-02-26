---
name: openfoodfacts-cli
description: Search and retrieve food product data (nutrition, ingredients, Nutriscore) from OpenFoodFacts using the `off` CLI. Use when the user asks about food products, nutritional information, barcodes, or wants to look up grocery items.
---

# OpenFoodFacts CLI

A command-line tool to query the [OpenFoodFacts](https://world.openfoodfacts.org/) database. Install with:

```bash
npm install -g openfoodfacts-cli
```

The binary is called `off`.

## Commands

### Search products

```bash
off search <query> [--page <n>] [--page-size <n>] [--sort-by <field>]
```

- `<query>`: product name or keyword (quote multi-word queries)
- `--page`: page number, starts at 1 (default: 1)
- `--page-size`: results per page (default: 10)
- `--sort-by`: sort field, prefix with `-` for descending (e.g. `-popularity`)

**Output**: ASCII table with columns: Barcode, Name, Brand, Nutriscore, kcal, Fat, Carbs, Prot, Salt. Shows total count and pagination info. Missing values display as `-`.

### Get product by barcode

```bash
off get <ean>
```

- `<ean>`: product barcode (typically 13 digits, e.g. `3017620422003`)

**Output**: same table format as search, single row.

## Examples

```bash
# Search for a product
off search nutella

# Multi-word query
off search "organic chocolate" --page-size 5

# Paginate
off search pasta --page 2

# Sort by field
off search snacks --sort-by -popularity

# Get specific product
off get 3017620422003
```

## Output format

Both commands produce a fixed-width ASCII table:

```
Found 42 results (page 1/5)
Barcode        Name                                      Brand                      Nutriscore  kcal  Fat   Carbs  Prot  Salt
-------------  ----------------------------------------  -------------------------  ----------  ----  ----  -----  ----  ----
3017620422003  Nutella                                   Ferrero                    E           539   30.9  57.5   6.3   0.1
...
Use --page 2 to see next page
```

- Names truncated at 40 chars, brands at 25 chars (with ellipsis)
- Integers show no decimals, decimals show 1 decimal place
- Nutriscore: A-E uppercase, `-` if unknown
- Exit code 1 on error, 0 on success

## Error handling

- Search with no results: prints `No products found.`
- Invalid barcode / not found: prints `Product not found.`
- API errors: prints error message and exits with code 1

## Tips for agents

1. Always quote multi-word search queries
2. Check pagination output to know if more pages are available
3. Use `off get` when you have an exact barcode, `off search` for discovery
4. Nutritional values are per 100g
5. The database is community-maintained; some products may have incomplete data
