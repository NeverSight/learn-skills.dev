---
name: layerzero-messaging
description: >
  LayerZero V2 messaging on Hedera. Use when building OFT / OApp bridges between Hedera and
  EVM chains, configuring Endpoint V2 peers and ULN/DVN/executor wiring, sending with
  quoteSend + send, implementing HTS-backed OFT connectors (mint/burn via 0x167), or
  relaying educational lzReceive flows on testnet.
---

# LayerZero Messaging (Hedera)

**OFT pattern:** deploy paired Omnichain Fungible Tokens — a standard `OFT` on the EVM side and an **HTS connector OFT** on Hedera — then `setPeer` both ways and send with LayerZero V2 fees.

```text
OFT (EVM)  ←setPeer→  HTSConnectorOFT (Hedera)
  │ send / quoteSend          │ _debit burn / _credit mint (HTS 0x167)
  └──────── Endpoint V2 + ULN + DVN + Executor ────────┘
```

This skill focuses on **LayerZero V2 OApp/OFT + Hedera HTS**. Educational templates may use **simple workers** and a manual/UI `lzReceive` relay — not the same as production LayerZero Labs verification.

## Quick Reference

| Concept | Rule |
| ------- | ---- |
| Endpoint | `ILayerZeroEndpointV2` per chain |
| Peer | `setPeer(remoteEid, bytes32(uint256(uint160(remoteOApp))))` on **both** sides |
| Send | `quoteSend(SendParam, payInLzToken)` → `send{value: nativeFee}(SendParam, fee, refund)` |
| Receiver | `to` in `SendParam` is `bytes32` (padded address) |
| Hedera OFT | HTS-backed connector — create HTS token, burn on send, mint on receive |
| HTS fee | Deploy connector with native value to pay `createFungibleToken` |
| Approval | User must `approve(connector, amount)` on the **HTS token** before Hedera → EVM `send` |
| IDs | Use LayerZero **EIDs** in peers/`dstEid` — not EVM chain IDs |

See [references/hedera-endpoints.md](references/hedera-endpoints.md) for where to source Endpoint/ULN/DVN addresses. See [references/examples.md](references/examples.md) for wire and send sketches.

## Critical: Wire Both Directions

Incomplete peer config bricks the pathway. For each local OApp:

1. `setPeer(remoteEid, remoteOAppAsBytes32)`
2. `setSendLibrary` / `setReceiveLibrary` (ULN302)
3. `setConfig` — ExecutorConfig (type `1`) on send lib; UlnConfig (type `2`) on send + receive libs
4. `setEnforcedOptions` — e.g. `lzReceive` gas for msgType `1` (token send)

Verify with `peers(remoteEid)` on both chains before sending.

## Critical: Hedera HTS Connector Semantics

On Hedera, do **not** use a plain ERC-20 OFT as the primary path. Use an HTS-backed connector:

- Constructor creates fungible HTS via precompile `0x167` (supply key = connector)
- `_debit`: transfer HTS in → **burn**
- `_credit`: **mint** → transfer HTS out
- Amounts must fit `int64` for HTS mint/burn/transfer
- Associate the receiver account with the HTS token before EVM → Hedera receives

```solidity
// Deploy with value so createFungibleToken fee is paid
new HTSConnectorOFT{ value: htsCreateValue }(name, symbol, lzEndpoint, owner);
```

## Send Flow

```solidity
SendParam memory sendParam = SendParam({
    dstEid: remoteEid,
    to: bytes32(uint256(uint160(receiver))),
    amountLD: amountLD,
    minAmountLD: (amountLD * 9) / 10,
    extraOptions: OptionsBuilder.newOptions().addExecutorLzReceiveOption(lzReceiveGas, 0),
    composeMsg: "",
    oftCmd: ""
});

MessagingFee memory fee = IOFT(localOFT).quoteSend(sendParam, false);
IOFT(localOFT).send{ value: fee.nativeFee }(sendParam, fee, payable(refundTo));
```

**Hedera → EVM note:** forge fee simulation can disagree with Hedera JSON-RPC wei/tinybar scaling — often `quote` via `cast` + scaled native fee for that direction.

## Deploy Checklist (generic)

1. Deploy EVM `OFT` (optional premint)
2. Deploy Hedera HTS connector OFT with HTS create value
3. Deploy workers (Labs DVN/executor **or** educational simple workers)
4. Wire both OApps (`setPeer` + libraries + config + enforced options)
5. Associate Hedera account with `htsTokenAddress()`
6. Sync frontend config if applicable; fund relay key if using UI auto-relay
7. Send small amount; track on LayerZero Scan (testnet/mainnet as appropriate)

## Educational Relay

Some templates use **simple DVN/executor mocks** and an explicit `lzReceive` relay step. Treat that as a learning aid — production apps rely on LayerZero’s verification network, not a custom relayer key in the app server.

## Checklist

- [ ] Peers set both ways with correct EIDs (not EVM chain IDs)
- [ ] Send/receive libraries + ULN/executor config applied
- [ ] Hedera side is HTS connector; create fee paid; supply key is connector
- [ ] Receiver associated with HTS token before inbound transfers
- [ ] `quoteSend` native fee attached to `send`
- [ ] Receiver address encoded as `bytes32`
- [ ] Educational disclaimer: not audited / not for mainnet funds

## References

- [references/examples.md](references/examples.md) — OFT, HTS connector, wire, send
- [references/hedera-endpoints.md](references/hedera-endpoints.md) — EIDs vs chain IDs, where to source addresses
- [LayerZero V2 docs](https://docs.layerzero.network/v2)
- [LayerZero deployments metadata](https://metadata.layerzero-api.com/v1/metadata/deployments)
