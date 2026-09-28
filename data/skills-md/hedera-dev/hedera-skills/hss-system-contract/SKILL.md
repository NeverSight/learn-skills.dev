---
name: hss-system-contract
description: Hedera Schedule Service (HSS) smart contract development. Use when creating or interacting with scheduled transactions from Solidity via the Schedule Service system contract at 0x16b (e.g. scheduleNative for token creation, scheduleCall for generalized contract calls, authorizeSchedule, signSchedule, deleteSchedule, or querying scheduled token info).
---

# Hedera Schedule Service (HSS) System Contract

The Hedera Schedule Service system contract at **`0x16b`** exposes functions for creating and managing scheduled transactions from within Solidity. It supports:

- **HIP-755**: Authorizing and signing schedules from contracts
- **HIP-756**: Scheduling native HTS token creation (createFungibleToken, createNonFungibleToken, etc.)
- **HIP-1215**: Generalized scheduled contract calls — schedule arbitrary calls to any contract (or self) for DeFi automation, vesting, DAO operations

## Quick Reference

**Contract address:** `0x16b`

**Imports:**

```solidity
import {HederaScheduleService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/HederaScheduleService.sol";
import {IHRC1215ScheduleFacade} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/IHRC1215ScheduleFacade.sol";
```

`HederaScheduleService` is an abstract contract (like `HederaTokenService` for HTS). Inherit it to get `internal` helper functions that handle the low-level calls to `0x16b`. `HederaResponseCodes` is available transitively.

**Response codes:** SUCCESS = 22 (`HederaResponseCodes.SUCCESS`). See [references/api.md](references/api.md) for full function list and [Hedera response codes](https://github.com/hashgraph/hedera-protobufs/blob/main/services/response_code.proto).

## Critical: Inheritance Pattern

**`IHederaScheduleService` is an empty interface.** Functions are defined in `IHRC755`, `IHRC756`, `IHRC1215` and wrapped as `internal` helpers in `HederaScheduleService`. Your contract must **inherit** `HederaScheduleService`:

```solidity
contract MyScheduler is HederaScheduleService {
    error ScheduleFailed();

    function doSchedule() external {
        (int64 rc, address scheduleAddr) = scheduleCall(target, expiry, gasLimit, 0, data);
        if (rc != HederaResponseCodes.SUCCESS) revert ScheduleFailed();
    }
}
```

## Critical: Non-Reverting Behavior (HIP-1215)

The `scheduleCall`, `scheduleCallWithPayer`, and `executeCallOnPayerSignature` functions **do not revert**. On failure they return `(responseCode, address(0))`. Always check:

```solidity
error ScheduleFailed();

(int64 rc, address scheduleAddr) = scheduleCall(target, expiry, gasLimit, 0, data);
if (rc != HederaResponseCodes.SUCCESS || scheduleAddr == address(0)) {
    revert ScheduleFailed();
}
```

## Capacity and Throttling (HIP-1215)

Scheduled calls are throttled per second. Use `hasScheduleCapacity(expirySecond, gasLimit)` before scheduling to avoid `SCHEDULE_EXPIRY_IS_BUSY`:

```solidity
bool capacity = hasScheduleCapacity(expirySecond, gasLimit);
if (!capacity) {
    // Retry with a later expiry or different gas limit
    // See HIP-1215 findAvailableSecond() pattern for exponential backoff + jitter
}
```

## Common Concepts

- **Scheduled transaction**: Wraps a Hedera transaction (native HTS call or EVM contract call) for deferred execution when signature thresholds are met.
- **Payer**: Account responsible for paying fees. With `scheduleCall`, the calling contract is the payer. With `scheduleCallWithPayer` / `executeCallOnPayerSignature`, a separate payer can be specified.
- **authorizeSchedule**: Signs the schedule with the calling contract's key (ContractKey format `0.0.<ContractId>`).
- **signSchedule**: Adds protobuf-encoded signatures from EOAs or other keys.
- **Expiration**: Schedules that fail to collect all required signatures before `expirySecond` are automatically removed from the network.

## Usage Patterns

### Schedule Native Token Creation (HIP-756)

> **Note:** The payer must have sufficient HBAR when the schedule executes (for the token creation fee).

```solidity
import {HederaScheduleService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/HederaScheduleService.sol";
import {IHederaTokenService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-token-service/IHederaTokenService.sol";

contract ScheduledTokenCreator is HederaScheduleService {
    error FailToSchedule();

    function scheduleTokenCreate(
        IHederaTokenService.HederaToken memory token,
        int64 initialSupply,
        int32 decimals,
        address payer
    ) external returns (address scheduleAddr) {
        bytes memory callData = abi.encodeCall(
            IHederaTokenService.createFungibleToken,
            (token, initialSupply, decimals)
        );
        int64 rc;
        (rc, scheduleAddr) = scheduleNative(
            address(0x167), callData, payer
        );
        if (rc != HederaResponseCodes.SUCCESS) revert FailToSchedule();
    }
}
```

### Schedule Arbitrary Contract Call (HIP-1215)

```solidity
import {HederaScheduleService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/HederaScheduleService.sol";

contract Scheduler is HederaScheduleService {
    error FailToSchedule();
    event ScheduleCreated(address);

    function scheduleFutureCall(
        address target,
        uint256 expirySecond,
        uint256 gasLimit,
        bytes memory callData
    ) external returns (address scheduleAddr) {
        if (!hasScheduleCapacity(expirySecond, gasLimit)) revert FailToSchedule();

        int64 rc;
        (rc, scheduleAddr) = scheduleCall(
            target,
            expirySecond > 0 ? expirySecond : block.timestamp + 5,
            gasLimit,
            0,
            callData
        );
        if (rc != HederaResponseCodes.SUCCESS) {
            revert FailToSchedule();
        }
        emit ScheduleCreated(scheduleAddr);
    }
}
```

### Contract Signs Schedule (HIP-755)

```solidity
import {HederaScheduleService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/HederaScheduleService.sol";

contract ScheduleSigner is HederaScheduleService {
    error FailToAuthorize();
    error FailToSign();

    function signAsContract(address scheduleAddr) external {
        int64 rc = authorizeSchedule(scheduleAddr);
        if (rc != HederaResponseCodes.SUCCESS) revert FailToAuthorize();
    }

    function signWithSignatureMap(address scheduleAddr, bytes memory sigMap) external {
        int64 rc = signSchedule(scheduleAddr, sigMap);
        if (rc != HederaResponseCodes.SUCCESS) revert FailToSign();
    }
}
```

### Delete Schedule

```solidity
import {HederaScheduleService} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/HederaScheduleService.sol";
import {IHRC1215ScheduleFacade} from "@hashgraph/smart-contracts/contracts/system-contracts/hedera-schedule-service/IHRC1215ScheduleFacade.sol";

contract ScheduleManager is HederaScheduleService {
    error FailToDeleteSchedule();

    // Option 1: Internal helper (inheriting HederaScheduleService)
    function deleteScheduleExample(address scheduleAddr) external {
        int64 rc = deleteSchedule(scheduleAddr);
        if (rc != HederaResponseCodes.SUCCESS) {
            revert FailToDeleteSchedule();
        }
    }

    // Option 2: Redirect — call deleteSchedule() on the schedule's address
    // (works for contracts and EOAs)
    function deleteScheduleProxy(address scheduleAddr) external {
        int64 rc = IHRC1215ScheduleFacade(scheduleAddr).deleteSchedule();
        if (rc != HederaResponseCodes.SUCCESS) {
            revert FailToDeleteSchedule();
        }
    }
}
```

## Costs

- Schedule transaction fees match HAPI ScheduleCreate, with a **20% markup** for system contract usage.
- Includes gas, storage, and consensus fees. Expired transactions incur no extra fees beyond initial scheduling/signature costs.

## References

- **API Reference**: [references/api.md](references/api.md) — Full function signatures, selectors, and usage notes
- **HIP-755**: [Schedule Service System Contract](https://hips.hedera.com/hip/hip-755)
- **HIP-756**: [Contract Scheduled Token Create](https://hips.hedera.com/hip/hip-756)
- **HIP-1215**: [Generalized Scheduled Contract Calls](https://hips.hedera.com/hip/hip-1215)
- **Source**: [hedera-smart-contracts/hedera-schedule-service](https://github.com/hashgraph/hedera-smart-contracts/tree/main/contracts/system-contracts/hedera-schedule-service)
