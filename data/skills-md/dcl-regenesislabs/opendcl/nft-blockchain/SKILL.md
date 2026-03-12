---
name: nft-blockchain
description: Display NFT artwork and interact with blockchain from Decentraland scenes. Show NFTs using NftShape with frame styles, check player wallet with getPlayer, sign messages with signedFetch, interact with smart contracts using eth-connect and createEthereumProvider, and handle MANA transactions. Use when user wants NFTs, blockchain, wallet, smart contracts, Web3, or crypto.
---

# NFT and Blockchain in Decentraland

## Display NFT Artwork

Show an NFT from Ethereum in a decorative frame:

```typescript
import { engine, Transform, NftShape, NftFrameType } from '@dcl/sdk/ecs'
import { Vector3, Color4 } from '@dcl/sdk/math'

const nftFrame = engine.addEntity()
Transform.create(nftFrame, {
  position: Vector3.create(8, 2, 8),
  rotation: Quaternion.fromEulerDegrees(0, 0, 0)
})

NftShape.create(nftFrame, {
  urn: 'urn:decentraland:ethereum:erc721:0x06012c8cf97bead5deae237070f9587f8e7a266d:558536',
  color: Color4.White(),
  style: NftFrameType.NFT_CLASSIC
})
```

### NFT URN Format

```
urn:decentraland:ethereum:erc721:<contractAddress>:<tokenId>
```

- Works with any ERC-721 NFT on Ethereum mainnet
- The image is loaded automatically from the NFT's metadata

### Available Frame Styles

```typescript
NftFrameType.NFT_CLASSIC            // Simple classic frame
NftFrameType.NFT_BAROQUE_ORNAMENT   // Ornate baroque
NftFrameType.NFT_DIAMOND_ORNAMENT   // Diamond pattern
NftFrameType.NFT_MINIMAL_WIDE       // Minimal wide border
NftFrameType.NFT_MINIMAL_GREY       // Minimal grey border
NftFrameType.NFT_BLOCKY             // Pixelated/blocky
NftFrameType.NFT_GOLD_EDGES         // Gold edge trim
NftFrameType.NFT_GOLD_CARVED        // Carved gold
NftFrameType.NFT_GOLD_WIDE          // Wide gold border
NftFrameType.NFT_GOLD_ROUNDED       // Rounded gold
NftFrameType.NFT_METAL_MEDIUM       // Medium metal
NftFrameType.NFT_METAL_WIDE         // Wide metal
NftFrameType.NFT_METAL_SLIM         // Slim metal
NftFrameType.NFT_METAL_ROUNDED      // Rounded metal
NftFrameType.NFT_PINS               // Pinned to wall
NftFrameType.NFT_MINIMAL_BLACK      // Minimal black
NftFrameType.NFT_MINIMAL_WHITE      // Minimal white
NftFrameType.NFT_TAPE               // Taped to wall
NftFrameType.NFT_WOOD_SLIM          // Slim wood
NftFrameType.NFT_WOOD_WIDE          // Wide wood
NftFrameType.NFT_WOOD_TWIGS         // Twig/branch wood
NftFrameType.NFT_CANVAS             // Canvas style
NftFrameType.NFT_NONE               // No frame
```

## Check Player Wallet

```typescript
import { getPlayer } from '@dcl/sdk/src/players'

function checkWallet() {
  const player = getPlayer()
  if (player && !player.isGuest) {
    console.log('Player wallet address:', player.userId)
    // userId is the Ethereum wallet address
  } else {
    console.log('Player is guest (no wallet)')
  }
}
```

Always check `isGuest` before attempting any blockchain interaction — guest players don't have a connected wallet.

## Signed Requests

Send authenticated requests to a backend, signed with the player's wallet:

```typescript
import { signedFetch } from '@dcl/sdk/signed-fetch'

executeTask(async () => {
  try {
    const response = await signedFetch('https://example.com/api/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'claimReward',
        amount: 100
      })
    })

    const result = await response.json()
    console.log('Result:', result)
  } catch (error) {
    console.log('Request failed:', error)
  }
})
```

`signedFetch` automatically includes a cryptographic signature proving the player's identity. Your backend can verify this signature to authenticate requests.

## MANA Transactions

```typescript
import { manaUser } from '@dcl/sdk/ethereum'

executeTask(async () => {
  try {
    // Check MANA balance
    const balance = await manaUser.balance()
    console.log('MANA balance:', balance)

    // Send MANA to another address
    const result = await manaUser.send('0x123...abc', 100) // 100 MANA
    console.log('MANA sent:', result)
  } catch (error) {
    console.log('MANA transaction failed:', error)
  }
})
```

## Smart Contract Interaction

Requires the `eth-connect` package:

```bash
npm install eth-connect
```

### Store ABI in a Separate File

```typescript
// contracts/myContract.ts
export default [
  {
    "constant": true,
    "inputs": [{ "name": "_owner", "type": "address" }],
    "name": "balanceOf",
    "outputs": [{ "name": "balance", "type": "uint256" }],
    "type": "function"
  }
  // ... rest of ABI
]
```

### Create Contract Instance

```typescript
import { RequestManager, ContractFactory } from 'eth-connect'
import { createEthereumProvider } from '@dcl/sdk/ethereum-provider'
import { abi } from '../contracts/myContract'

executeTask(async () => {
  try {
    // Create web3 provider
    const provider = createEthereumProvider()
    const requestManager = new RequestManager(provider)

    // Create contract at a specific address
    const factory = new ContractFactory(requestManager, abi)
    const contract = await factory.at('0x2a8fd99c19271f4f04b1b7b9c4f7cf264b626edb') as any

    // Read data (no gas required)
    const balance = await contract.balanceOf('0x123...abc')
    console.log('Balance:', balance)
  } catch (error) {
    console.log('Contract interaction failed:', error)
  }
})
```

### Write Operations (Require Gas)

```typescript
executeTask(async () => {
  try {
    const userData = getPlayer()
    if (userData.isGuest) return

    // Write operation — prompts the player to sign the transaction
    const writeResult = await contract.transfer(
      '0xRecipientAddress',
      100,
      {
        from: userData.userId,
        gas: 100000,
        gasPrice: await requestManager.eth_gasPrice()
      }
    )
    console.log('Transaction hash:', writeResult)
  } catch (error) {
    console.log('Transaction failed:', error)
  }
})
```

### Gas Price and Balance Checking

```typescript
import { RequestManager } from 'eth-connect'
import { createEthereumProvider } from '@dcl/sdk/ethereum-provider'

executeTask(async () => {
  const provider = createEthereumProvider()
  const requestManager = new RequestManager(provider)

  const gasPrice = await requestManager.eth_gasPrice()
  console.log('Current gas price:', gasPrice)

  const balance = await requestManager.eth_getBalance('0x123...abc', 'latest')
  console.log('Account balance:', balance)
})
```

## Testing with Sepolia

For development, use the Sepolia testnet:

1. Set MetaMask to Sepolia network
2. Get test ETH from a Sepolia faucet
3. Deploy your contracts to Sepolia
4. Contract addresses differ between mainnet and testnet — use environment checks

### Custom RPC Calls

Use `sendAsync` for low-level Ethereum RPC calls not covered by eth-connect helpers:

```typescript
import { sendAsync } from '~system/EthereumController'

const result = await sendAsync({ method: 'eth_blockNumber', params: [] })
console.log('Current block:', result.body)
```

### Opening URLs and NFT Dialogs

Use restricted actions to open external links and NFT detail views:

```typescript
import { openExternalUrl, openNftDialog } from '~system/RestrictedActions'

openExternalUrl({ url: 'https://opensea.io/collection/...' })
openNftDialog({ urn: 'urn:decentraland:ethereum:erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d:558536' })
```

## Best Practices

- **Always check `isGuest`** before any blockchain interaction — guest players can't sign transactions
- Use `executeTask(async () => { ... })` for all async blockchain calls
- Store ABI files separately (e.g., `contracts/`) — don't inline large ABIs
- Handle errors gracefully — blockchain operations can fail (rejected by user, insufficient gas, network issues)
- `eth-connect` must be installed as a dependency: `npm install eth-connect`
- Use `signedFetch` for backend authentication instead of raw `fetch` — it proves the player's identity
- Read operations (view/pure functions) don't require gas; write operations prompt the user to sign
- Test on Sepolia before deploying to mainnet
- NFT URNs only work with Ethereum mainnet ERC-721 tokens
