---
name: remix-rest-snippets
description: REST client snippets for Remix agent publishing
metadata:
  tags: remix, rest, snippets
---

## TypeScript (REST)

```ts
const baseUrl = 'https://api.remix.gg'
const headers = {
  Authorization: `Bearer ${process.env.REMIX_API_KEY!}`,
  'Content-Type': 'application/json',
}

const openApiSpec = await fetch(`${baseUrl}/docs/json`, {
  method: 'GET',
  headers,
}).then((r) => r.json())

const createRes = await fetch(`${baseUrl}/v1/games`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ name: 'Neon Dash' }),
})
const createJson = await createRes.json()
if (!createJson.success) throw new Error(createJson.error.message)

const gameId = createJson.data.game.id as string
const versionId = createJson.data.game.version.id as string

const updateRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/versions/${versionId}/code`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({ code: html }),
  },
)
const updateJson = await updateRes.json()
if (!updateJson.success) throw new Error(updateJson.error.message)

const validateRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/versions/${versionId}/validate`,
  { method: 'GET', headers },
)
const validateJson = await validateRes.json()
if (!validateJson.success) throw new Error(validateJson.error.message)
if (!validateJson.data.valid) {
  throw new Error(`Blocked: ${validateJson.data.blockers.map((b: { code: string }) => b.code).join(', ')}`)
}

const statusRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/versions/${versionId}/status`,
  { method: 'GET', headers },
)
const statusJson = await statusRes.json()
if (!statusJson.success) throw new Error(statusJson.error.message)

const readinessRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/launch-readiness?versionId=${versionId}`,
  { method: 'GET', headers },
)
const readinessJson = await readinessRes.json()
if (!readinessJson.success) throw new Error(readinessJson.error.message)
```

## Image Generation

```ts
const imageRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/images/generate`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({ prompt: 'A neon cityscape background' }),
  },
)
const imageJson = await imageRes.json()
if (!imageJson.success) throw new Error(imageJson.error.message)
```

## Sprite Generation

```ts
const spriteRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/sprites/generate`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({ prompt: 'A pixel art character running' }),
  },
)
const spriteJson = await spriteRes.json()
if (!spriteJson.success) throw new Error(spriteJson.error.message)
```

## Shop Items

```ts
// List items
const itemsRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/items`,
  { method: 'GET', headers },
)
const itemsJson = await itemsRes.json()

// Create item
const createItemRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/items`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({ name: 'Speed Boost', price: 100 }),
  },
)
const createItemJson = await createItemRes.json()

// Delete item
const itemId = createItemJson.data.item.id
const deleteItemRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/items/${itemId}`,
  { method: 'DELETE', headers },
)
```

## Asset Upload

```ts
const formData = new FormData()
formData.append('file', fileBlob, 'icon.png')

const assetRes = await fetch(
  `${baseUrl}/v1/games/${gameId}/assets`,
  {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.REMIX_API_KEY!}` },
    body: formData,
  },
)
const assetJson = await assetRes.json()
if (!assetJson.success) throw new Error(assetJson.error.message)
```

## Game Update

```ts
const gameUpdateRes = await fetch(
  `${baseUrl}/v1/games/${gameId}`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({ isMultiplayer: true }),
  },
)
const gameUpdateJson = await gameUpdateRes.json()
if (!gameUpdateJson.success) throw new Error(gameUpdateJson.error.message)
```
