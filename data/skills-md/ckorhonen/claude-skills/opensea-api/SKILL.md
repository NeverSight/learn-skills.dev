---
name: opensea-api
description: Interact with the OpenSea NFT marketplace API. Use when fetching NFT metadata, collection info, listings, offers, events, or building NFT applications with OpenSea's REST and Stream APIs.
---

# OpenSea API

## Overview

Interact with OpenSea's NFT marketplace through their REST API and real-time Stream API. Fetch NFT metadata, collection information, listings, offers, and events across multiple blockchains including Ethereum, Polygon, Base, Arbitrum, and more.

## When to Use

- Fetching NFT metadata, traits, and ownership information
- Getting collection details and statistics
- Retrieving active listings and offers
- Tracking NFT events (sales, transfers, listings)
- Building NFT dashboards and analytics tools
- Real-time monitoring of marketplace activity
- Integrating NFT data into applications

## Prerequisites

- OpenSea API key (free tier available)
- `curl` for HTTP requests
- `jq` for JSON parsing (`brew install jq` on macOS, `apt install jq` on Linux)
- For Stream API: Node.js with `@opensea/stream-js` or Python with `opensea-stream`

## Getting an API Key

1. Visit [OpenSea Developer Portal](https://docs.opensea.io/reference/api-keys)
2. Create a developer account
3. Generate an API key
4. Set the environment variable:

```bash
export OPENSEA_API_KEY="your-api-key"
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) for persistence:

```bash
echo 'export OPENSEA_API_KEY="your-api-key"' >> ~/.zshrc
```

## API Base URL

```
https://api.opensea.io
```

All requests require the API key in the header:

```bash
-H "X-API-KEY: $OPENSEA_API_KEY"
```

## Rate Limits

| Request Type | Rate Limit |
|--------------|------------|
| GET requests | 4/second per API key |
| POST requests | 2/second per API key |

For higher limits, apply at the [OpenSea Developer Portal](https://docs.opensea.io/reference/api-keys#rate-limits).

## Supported Blockchains

| Chain | API Name |
|-------|----------|
| Ethereum | `ethereum` |
| Polygon | `matic` |
| Arbitrum | `arbitrum` |
| Optimism | `optimism` |
| Base | `base` |
| Avalanche | `avalanche` |
| Blast | `blast` |
| Zora | `zora` |
| Solana | `solana` |

## Quick Start

Fetch an NFT:

```bash
curl -X GET "https://api.opensea.io/api/v2/chain/ethereum/contract/0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D/nfts/1" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

Get collection info:

```bash
curl -X GET "https://api.opensea.io/api/v2/collections/boredapeyachtclub" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## NFT Endpoints

### Get Single NFT

Fetch metadata, traits, ownership, and rarity for a single NFT.

```bash
curl -X GET "https://api.opensea.io/api/v2/chain/{chain}/contract/{contract_address}/nfts/{token_id}" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Example:**

```bash
# Get Bored Ape #1
curl -X GET "https://api.opensea.io/api/v2/chain/ethereum/contract/0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D/nfts/1" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Response includes:**
- `identifier` - Token ID
- `name` - NFT name
- `description` - NFT description
- `image_url` - Image URL
- `metadata_url` - Token URI
- `owners` - Current owner(s)
- `traits` - Array of trait objects
- `rarity` - Rarity information

### List NFTs by Collection

Fetch multiple NFTs for a collection with pagination.

```bash
curl -X GET "https://api.opensea.io/api/v2/collection/{collection_slug}/nfts?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Parameters:**
- `limit` - Max results (1-200, default 50)
- `next` - Cursor for pagination

**Example:**

```bash
# Get first 50 Pudgy Penguins
curl -X GET "https://api.opensea.io/api/v2/collection/pudgypenguins/nfts?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### List NFTs by Contract

Fetch NFTs for a specific contract address.

```bash
curl -X GET "https://api.opensea.io/api/v2/chain/{chain}/contract/{contract_address}/nfts?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### List NFTs by Account

Fetch NFTs owned by a wallet address.

```bash
curl -X GET "https://api.opensea.io/api/v2/chain/{chain}/account/{address}/nfts?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Example:**

```bash
# Get NFTs owned by an address on Ethereum
curl -X GET "https://api.opensea.io/api/v2/chain/ethereum/account/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045/nfts?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## Collection Endpoints

### Get Collection

Fetch collection details including description, fees, and social links.

```bash
curl -X GET "https://api.opensea.io/api/v2/collections/{collection_slug}" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Response includes:**
- `collection` - Collection slug
- `name` - Collection name
- `description` - Description
- `image_url` - Collection image
- `banner_image_url` - Banner image
- `owner` - Collection owner address
- `total_supply` - Total NFTs in collection
- `created_date` - Creation date
- `fees` - Creator fees and platform fees

**Example:**

```bash
curl -X GET "https://api.opensea.io/api/v2/collections/azuki" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get Collection Stats

Fetch floor price, volume, and other statistics.

```bash
curl -X GET "https://api.opensea.io/api/v2/collections/{collection_slug}/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Response includes:**
- `total` - All-time stats (volume, sales, average_price, etc.)
- `intervals` - Stats by time period (1d, 7d, 30d)

**Example:**

```bash
curl -X GET "https://api.opensea.io/api/v2/collections/boredapeyachtclub/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get Collection Traits

Fetch all traits and their value counts for a collection.

```bash
curl -X GET "https://api.opensea.io/api/v2/traits/{collection_slug}" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## Listings Endpoints

### Get Best Listing for NFT

Fetch the cheapest active listing for a specific NFT.

```bash
curl -X GET "https://api.opensea.io/api/v2/listings/collection/{collection_slug}/nfts/{token_id}/best" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Example:**

```bash
# Get best listing for Bored Ape #1234
curl -X GET "https://api.opensea.io/api/v2/listings/collection/boredapeyachtclub/nfts/1234/best" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get All Listings for NFT

Fetch all active listings for a specific NFT.

```bash
curl -X GET "https://api.opensea.io/api/v2/orders/{chain}/seaport/listings?asset_contract_address={contract}&token_ids={token_id}" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get All Listings for Collection

Fetch all active listings for a collection.

```bash
curl -X GET "https://api.opensea.io/api/v2/listings/collection/{collection_slug}/all?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## Offers Endpoints

### Get Best Offer for NFT

Fetch the highest active offer for a specific NFT.

```bash
curl -X GET "https://api.opensea.io/api/v2/offers/collection/{collection_slug}/nfts/{token_id}/best" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get All Offers for Collection

Fetch all active offers (individual and collection offers).

```bash
curl -X GET "https://api.opensea.io/api/v2/offers/collection/{collection_slug}/all?limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get Trait Offers

Fetch offers for NFTs with specific trait values.

```bash
curl -X GET "https://api.opensea.io/api/v2/offers/collection/{collection_slug}/traits" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## Events Endpoints

### Get Events by NFT

Fetch events (sales, transfers, listings) for a specific NFT.

```bash
curl -X GET "https://api.opensea.io/api/v2/events/chain/{chain}/contract/{contract}/nfts/{token_id}?event_type=sale&limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Event Types:**
- `sale` - NFT was sold
- `transfer` - NFT was transferred
- `listing` - NFT was listed for sale
- `offer` - Offer was made on NFT
- `cancel` - Listing/offer was cancelled

**Example:**

```bash
# Get sales history for Bored Ape #1234
curl -X GET "https://api.opensea.io/api/v2/events/chain/ethereum/contract/0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D/nfts/1234?event_type=sale" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get Events by Collection

Fetch events for an entire collection.

```bash
curl -X GET "https://api.opensea.io/api/v2/events/collection/{collection_slug}?event_type=sale&limit=50" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### Get Events by Account

Fetch events for a specific wallet address.

```bash
curl -X GET "https://api.opensea.io/api/v2/events/accounts/{address}?event_type=sale" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

## Account Endpoints

### Get Account

Fetch an OpenSea account profile.

```bash
curl -X GET "https://api.opensea.io/api/v2/accounts/{address}" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

**Response includes:**
- `address` - Wallet address
- `username` - OpenSea username
- `profile_image_url` - Profile image
- `banner_image_url` - Banner image
- `bio` - User bio
- `social_media_accounts` - Linked social accounts

## Stream API (Real-time WebSocket)

### Overview

The Stream API provides real-time events via WebSocket. Use it for:
- Push notifications for NFT activity
- Live activity feeds
- Real-time price monitoring

### Supported Events

| Event | Description |
|-------|-------------|
| `item.listed` | NFT listed for sale |
| `item.sold` | NFT was sold |
| `item.transferred` | NFT transferred between wallets |
| `item.metadata_updated` | NFT metadata changed |
| `item.cancelled` | Listing/offer cancelled |
| `item.received_bid` | Bid received on NFT |

### JavaScript/TypeScript Setup

```bash
npm install @opensea/stream-js
```

```typescript
import { OpenSeaStreamClient, Network } from '@opensea/stream-js';

const client = new OpenSeaStreamClient({
  network: Network.MAINNET,
  token: process.env.OPENSEA_API_KEY,
});

// Subscribe to collection events
client.onItemListed('boredapeyachtclub', (event) => {
  console.log('New listing:', event);
  console.log('Price:', event.payload.base_price);
  console.log('Token ID:', event.payload.item.nft_id);
});

client.onItemSold('boredapeyachtclub', (event) => {
  console.log('Sale:', event);
  console.log('Price:', event.payload.sale_price);
});

// Subscribe to all events globally
client.onItemListed('*', (event) => {
  console.log('Global listing:', event);
});
```

### Python Setup

```bash
pip install opensea-stream
```

```python
import asyncio
from opensea_stream import OpenSeaStreamClient

async def main():
    client = OpenSeaStreamClient(api_key=os.environ['OPENSEA_API_KEY'])

    async def handle_listing(event):
        print(f"New listing: {event}")

    await client.subscribe_to_collection(
        collection_slug='boredapeyachtclub',
        event_type='item.listed',
        callback=handle_listing
    )

asyncio.run(main())
```

## Seaport Protocol (Orders)

OpenSea uses the Seaport protocol for all orders. To create or fulfill orders programmatically:

### JavaScript SDK

```bash
npm install opensea-js
```

```typescript
import { OpenSeaSDK, Chain } from 'opensea-js';
import { ethers } from 'ethers';

const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const sdk = new OpenSeaSDK(wallet, {
  chain: Chain.Mainnet,
  apiKey: process.env.OPENSEA_API_KEY,
});

// Create a listing
const listing = await sdk.createListing({
  asset: {
    tokenId: '1234',
    tokenAddress: '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D',
  },
  startAmount: 10, // 10 ETH
  expirationTime: Math.round(Date.now() / 1000 + 60 * 60 * 24 * 7), // 7 days
});

// Fulfill a listing (buy)
const order = await sdk.api.getOrder({
  side: 'ask',
  assetContractAddress: '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D',
  tokenId: '1234',
});
await sdk.fulfillOrder({ order });

// Make an offer
const offer = await sdk.createOffer({
  asset: {
    tokenId: '1234',
    tokenAddress: '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D',
  },
  startAmount: 5, // 5 WETH
});
```

## Helper Scripts

### Fetch NFT Metadata

```bash
./scripts/fetch_nft.sh ethereum 0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D 1234
```

### Get Collection Stats

```bash
./scripts/collection_stats.sh boredapeyachtclub
```

### Monitor Collection Activity

```bash
./scripts/monitor_collection.sh boredapeyachtclub
```

### Get NFTs by Wallet

```bash
./scripts/wallet_nfts.sh ethereum 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

## Common Use Cases

### Check Floor Price

```bash
curl -s "https://api.opensea.io/api/v2/collections/boredapeyachtclub/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.total.floor_price'
```

### Get Recent Sales

```bash
curl -s "https://api.opensea.io/api/v2/events/collection/boredapeyachtclub?event_type=sale&limit=10" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.asset_events[] | {token_id: .nft.identifier, price: .payment.quantity}'
```

### Find Cheapest Listings

```bash
curl -s "https://api.opensea.io/api/v2/listings/collection/boredapeyachtclub/all?limit=10" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.listings | sort_by(.price.current.value) | .[0:5]'
```

### Export Collection Traits to JSON

```bash
curl -s "https://api.opensea.io/api/v2/traits/boredapeyachtclub" \
  -H "X-API-KEY: $OPENSEA_API_KEY" > traits.json
```

### Get Owner's Portfolio Value

```bash
./scripts/wallet_nfts.sh ethereum 0xYOUR_ADDRESS | jq '[.nfts[].floor_price] | add'
```

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | Check API key permissions |
| 404 | Not Found | Verify contract/token/collection exists |
| 429 | Rate Limited | Reduce request frequency |
| 500 | Server Error | Retry with backoff |

### Retry with Exponential Backoff

```bash
#!/usr/bin/env bash
max_retries=4
retry_count=0
base_delay=2

while [ "$retry_count" -lt "$max_retries" ]; do
  response=$(curl -s -w "%{http_code}" -o /tmp/response.json \
    "https://api.opensea.io/api/v2/collections/boredapeyachtclub" \
    -H "X-API-KEY: $OPENSEA_API_KEY")

  if [ "$response" = "200" ]; then
    cat /tmp/response.json
    exit 0
  elif [ "$response" = "429" ]; then
    delay=$((base_delay ** (retry_count + 1)))
    echo "Rate limited. Retrying in ${delay}s..." >&2
    sleep "$delay"
    retry_count=$((retry_count + 1))
  else
    echo "Error: HTTP $response" >&2
    exit 1
  fi
done
echo "Max retries exceeded" >&2
exit 1
```

## Troubleshooting

### "Invalid API Key"

```bash
# Verify your key is set
echo $OPENSEA_API_KEY

# Test with a simple request
curl -I "https://api.opensea.io/api/v2/collections/boredapeyachtclub" \
  -H "X-API-KEY: $OPENSEA_API_KEY"
```

### "Rate Limit Exceeded"

- Reduce request frequency to under 4/second
- Add delays between requests
- Use the Stream API for real-time data instead of polling
- Apply for rate limit increase

### "Collection/NFT Not Found"

- Verify the collection slug (check OpenSea URL)
- Ensure the contract address is correct
- Check if the NFT exists on the specified chain

### Stream API Connection Issues

```typescript
// Add error handling and reconnection
client.onError((error) => {
  console.error('Stream error:', error);
});

// The client automatically reconnects, but you can also:
client.disconnect();
client.connect();
```

## Best Practices

- **Cache responses** - NFT metadata rarely changes, cache aggressively
- **Use pagination** - Always handle `next` cursor for large datasets
- **Prefer Stream API** - Use WebSocket for real-time data instead of polling
- **Handle rate limits** - Implement exponential backoff for 429 errors
- **Validate input** - Check addresses and token IDs before API calls
- **Secure API keys** - Never expose keys in frontend code; use a backend proxy
- **Use appropriate chain** - Always specify the correct blockchain for multi-chain NFTs

## Resources

- [OpenSea Developer Documentation](https://docs.opensea.io/)
- [API Reference](https://docs.opensea.io/reference/api-overview)
- [Stream API Overview](https://docs.opensea.io/reference/stream-api-overview)
- [Seaport Protocol](https://docs.opensea.io/docs/seaport)
- [OpenSea JS SDK](https://github.com/ProjectOpenSea/opensea-js)
- [Stream JS SDK](https://github.com/ProjectOpenSea/stream-js)
