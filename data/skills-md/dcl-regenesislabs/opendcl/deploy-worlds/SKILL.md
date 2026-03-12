---
name: deploy-worlds
description: Deploy and publish a Decentraland scene to a World (personal 3D space). Use when user wants to deploy to a World, publish to a World, set up worldConfiguration, use a DCL NAME or ENS domain for deployment, or opt out of Places listing.
---

# Deploying to Decentraland Worlds

Worlds are personal 3D spaces not tied to LAND. They have no parcel limitations and are automatically listed on the Places page.

## Requirements

To publish to a World, the user must own either:
- A **Decentraland NAME** (e.g., `my-name.dcl.eth`)
- An **ENS domain** (e.g., `my-name.eth`)

The wallet signing the deployment must own the NAME, or have been granted permission via Access Control Lists (ACL).

## 1. Configure scene.json

Add a `worldConfiguration` section to `scene.json`:

```json
{
  "worldConfiguration": {
    "name": "my-name.dcl.eth"
  }
}
```

The `name` field must match a Decentraland NAME or ENS domain owned by the deploying wallet.

### Opt out of Places listing

All Worlds are automatically listed on the [Places page](https://places.decentraland.org). To opt out:

```json
{
  "worldConfiguration": {
    "name": "my-name.dcl.eth",
    "placesConfig": {
      "optOut": true
    }
  }
}
```

## 2. Deploy

**Use the `/deploy` command** — it auto-detects the `worldConfiguration` in scene.json and deploys to the Worlds content server automatically.

Alternatively, deploy manually via CLI:

```bash
npx @dcl/sdk-commands deploy --target-content https://worlds-content-server.decentraland.org
```

This will prompt the user to sign the deployment with their wallet. Validations run automatically to allow or reject the scene.

### Via Creator Hub

1. Open the scene project in Creator Hub
2. Click the **Publish** button (top-right corner)
3. Select **PUBLISH TO WORLD**
4. Choose which NAME or ENS domain to publish to

## 3. Access the World

Once deployed, the World is accessible at:

```
decentraland://?realm=NAME.dcl.eth
```

Replace `NAME` with the Decentraland NAME or ENS domain used for deployment.

From inside Decentraland, use the chatbox command:
```
/goto NAME.dcl.eth
```

## Full scene.json Example

```json
{
  "ecs7": true,
  "runtimeVersion": "7",
  "display": {
    "title": "My World",
    "description": "A personal 3D space"
  },
  "scene": {
    "parcels": ["0,0"],
    "base": "0,0"
  },
  "main": "bin/index.js",
  "worldConfiguration": {
    "name": "my-name.dcl.eth"
  }
}
```

## Key Differences from Genesis City

- **No parcel limitations** — Worlds are not constrained by LAND ownership
- **NAME/ENS required** — must own a Decentraland NAME or ENS domain instead of LAND
- **Different deploy target** — uses `--target-content https://worlds-content-server.decentraland.org`
- **Auto-listed on Places** — unless opted out via `placesConfig.optOut`
