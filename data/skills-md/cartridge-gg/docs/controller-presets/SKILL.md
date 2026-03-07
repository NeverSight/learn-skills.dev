---
name: controller-presets
description: Interactively walk teams through creating a Cartridge Controller preset, including origin/AASA setup, session policies, themes, and mainnet vs sepolia configuration.
---

# Controller Presets

Guide teams through creating a preset for the Cartridge Controller.
A preset is a `config.json` committed to [cartridge-gg/presets](https://github.com/cartridge-gg/presets/tree/main/configs) that configures origin verification, session policies, theming, paymaster behavior, and optional iOS passkey support.

## Invocation

The user wants help creating or debugging a Controller preset.
Use `AskUserQuestion` to gather information interactively, one round at a time.

## Process

### Phase 1: Basics

Ask:
1. **Game/project name** — used as the directory name in `configs/<name>/`.
   Must be lowercase kebab-case (e.g. `dope-wars`, `loot-survivor`).
2. **Which networks?** — `SN_MAIN`, `SN_SEPOLIA`, or both.

Explain:
- Sepolia is paymastered by default — no paymaster setup needed for testnet.
- Mainnet requires a Slot paymaster (see `slot-paymaster` skill) to sponsor transactions.

### Phase 2: Origin Configuration

Ask for the production domain(s) where the game will be hosted.

Generate the `origin` field. Apply these rules:

| Rule | Correct | Wrong |
|------|---------|-------|
| No protocol prefix | `"game.example.com"` | `"https://game.example.com"` |
| Wildcard for subdomains | `"*.example.com"` | — |
| Wildcard does NOT match base domain | `*.example.com` matches `app.example.com` but NOT `example.com` | Assuming `*.example.com` covers `example.com` |
| Multiple origins use an array | `["example.com", "staging.example.com"]` | — |
| localhost is always allowed | Don't list it | Adding `"localhost"` to origins |

If they have a **Capacitor mobile app**, ask for the custom hostname and include it:
```json
{
  "origin": ["yourdomain.com", "my-custom-app"]
}
```
This authorizes `capacitor://my-custom-app` (iOS) and `https://my-custom-app` (Android).
The default `capacitor://localhost` is always allowed automatically.

IMPORTANT: If the user needs both `example.com` and `*.example.com`, they must list both explicitly.

### Phase 3: Session Policies

Ask for the contract addresses and entrypoints the game calls.
For each contract, collect:
- Contract address (hex, checksummed)
- Human-readable name and description
- Methods with entrypoints

Build the `chains` section. Example:
```json
{
  "chains": {
    "SN_MAIN": {
      "policies": {
        "contracts": {
          "0x123...abc": {
            "name": "Game World",
            "description": "Main game contract",
            "methods": [
              {
                "name": "Move Player",
                "description": "Move to a new position",
                "entrypoint": "move_player"
              }
            ]
          }
        }
      }
    }
  }
}
```

Key rules:
- **Entrypoints must be snake_case** and match the exact Cairo function name.
- **Chain IDs**: use `SN_MAIN` (not `SN_MAINNET`) and `SN_SEPOLIA` (not `SN_TESTNET`).
- **Contract addresses differ between networks** — confirm separate addresses for mainnet vs sepolia.
- **`approve` entrypoint triggers a CI warning** — the validator flags it. If the user genuinely needs ERC20 approval, acknowledge the warning.
- **VRF**: If the game uses Cartridge VRF, include the VRF provider contract (`0x051Fea4450Da9D6aeE758BDEbA88B2f665bCbf549D2C61421AA724E9AC0Ced8F`) with `request_random` entrypoint. The keychain auto-labels VRF contracts with Cartridge branding.

#### Method options

| Field | Default | Notes |
|-------|---------|-------|
| `isPaymastered` | `true` | Set to `false` to require users to pay their own gas for this method |
| `isEnabled` | `true` | Whether the method is pre-checked in the session approval UI |
| `isRequired` | `false` | If `true`, user cannot uncheck this method |
| `predicate` | — | Optional: conditional sponsorship based on contract state |

#### Paymaster predicates

For conditional sponsorship:
```json
{
  "entrypoint": "move_player",
  "is_paymastered": true,
  "predicate": {
    "address": "0x456...def",
    "entrypoint": "check_move_eligibility"
  }
}
```
The predicate contract is called first; the transaction is only sponsored if it returns true.

#### Message signing policies

If the game uses off-chain signed messages (EIP-712 style typed data), add a `messages` array alongside `contracts`:
```json
{
  "policies": {
    "contracts": { ... },
    "messages": [
      {
        "types": {
          "StarknetDomain": [...],
          "Message": [{ "name": "content", "type": "felt" }]
        },
        "primaryType": "Message",
        "domain": {
          "name": "MyGame",
          "version": "1",
          "chainId": "SN_MAIN",
          "revision": "1"
        }
      }
    ]
  }
}
```

### Phase 4: Theme

Ask if they want a custom theme. Collect:
- **Name**: display name for the game
- **Icon**: SVG or PNG file (will be optimized to 16–256px)
- **Cover**: PNG or JPG file (will be optimized to 768–1440px), optional
- **Primary color**: hex color for accent/branding

Cover supports light/dark variants:
```json
{
  "theme": {
    "name": "MyGame",
    "icon": "icon.svg",
    "cover": { "light": "cover-light.png", "dark": "cover-dark.png" },
    "colors": { "primary": "#F38332" }
  }
}
```

Asset files go in the same directory as `config.json`.
The build pipeline generates optimized WebP/PNG/JPG versions automatically — commit only the source files.

### Phase 5: Apple App Site Association (AASA)

Ask if they have a native iOS app that uses passkeys.

If yes, collect:
- **Team ID**: exactly 10 uppercase alphanumeric characters (from Apple Developer account)
- **Bundle ID**: reverse DNS format (e.g. `com.example.mygame`)

The app ID is `TEAMID.BUNDLEID`. Validation rules:
- Pattern: `/^[A-Z0-9]{10}\.[a-zA-Z0-9.-]+$/`
- Team ID must be exactly 10 characters
- All AASA entries across all presets are aggregated into a single file served at `https://x.cartridge.gg/.well-known/apple-app-site-association`
- The aggregated file must stay under 128 KB

```json
{
  "apple-app-site-association": {
    "webcredentials": {
      "apps": ["ABCDE12345.com.example.mygame"]
    }
  }
}
```

If no iOS app, skip this section entirely (don't include the key).

### Phase 6: Assemble and Validate

Assemble the complete `config.json` and present it to the user.

Run through validation checklist:
- [ ] Origins have no protocol prefix
- [ ] Chain IDs are `SN_MAIN` or `SN_SEPOLIA` (not `SN_MAINNET`/`SN_TESTNET`)
- [ ] Contract addresses are different for each network
- [ ] Entrypoints are snake_case matching Cairo function names
- [ ] AASA app IDs match `TEAMID.BUNDLEID` format (if present)
- [ ] Asset files (icon, cover) are referenced and will exist in the directory
- [ ] No `approve` entrypoint unless intentional

### Phase 7: Connector Integration

Show how to use the preset in their app:

```typescript
import Controller from "@cartridge/controller";

const controller = new Controller({
  preset: "<preset-name>",  // matches the directory name in configs/
  // Policies are loaded from the preset — do NOT also pass policies here
  // unless you set shouldOverridePresetPolicies: true
});
```

Explain policy precedence:
1. `shouldOverridePresetPolicies: true` + policies → uses inline policies
2. Preset has policies for current chain → uses preset policies (ignores inline)
3. Preset has no policies for current chain → falls back to inline policies
4. No preset → uses inline policies

### Phase 8: PR Submission

Guide the user to submit a PR to [cartridge-gg/presets](https://github.com/cartridge-gg/presets):
1. Create `configs/<name>/config.json`
2. Add asset files (icon, cover) to the same directory
3. CI runs `validate-configs.ts` — fix any errors before merge
4. After merge, configs are built and deployed to `https://static.cartridge.gg/presets/<name>/config.json`

## Mainnet vs Sepolia Reference

| Aspect | Sepolia | Mainnet |
|--------|---------|---------|
| Paymaster | Free, automatic | Requires Slot paymaster with budget |
| Chain ID in config | `SN_SEPOLIA` | `SN_MAIN` |
| Contract addresses | Sepolia deploy | Mainnet deploy |
| Recommended for | Development, testing | Production |

Teams often include both chains in a single preset — use separate contract addresses for each.

## Debugging Common Issues

**"Policies show as unverified"**
→ Origin mismatch. Check that `config.origin` matches the domain your app is served from (without protocol). If using wildcards, remember `*.example.com` does NOT match `example.com`.

**"Preset policies not loading"**
→ Check that the `preset` name in your Controller constructor matches the directory name in the presets repo exactly. The config is fetched from CDN at `https://static.cartridge.gg/presets/<name>/config.json`.

**"Wrong policies for my chain"**
→ Policies are selected by chain ID at runtime. Verify the chain ID in your config matches what your RPC returns. Use `SN_MAIN`/`SN_SEPOLIA`, not hex chain IDs.

**"Paymaster not sponsoring on mainnet"**
→ Sepolia is auto-sponsored. Mainnet requires creating a Slot paymaster, funding it with credits, and adding matching policies. See `slot-paymaster` skill.

**"AASA validation failing"**
→ Team ID must be exactly 10 uppercase alphanumeric chars. Bundle ID must be reverse DNS. Pattern: `ABCDE12345.com.example.app`.

**"CI warns about approve entrypoint"**
→ This is intentional — `approve` is flagged as a security concern. If your game genuinely needs ERC20 approval, the warning is acceptable but will require reviewer acknowledgment.
