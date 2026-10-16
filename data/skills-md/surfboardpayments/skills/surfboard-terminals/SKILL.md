---
name: surfboard-terminals
description: "Register, configure, and manage Surfboard payment terminals: device registration codes, linking and delinking stores, hierarchical configuration, multi-merchant terminals, ordering and returning hardware, and the Android SoftPOS and Tap to Pay on iPhone SDKs. Use when provisioning devices, changing terminal settings, or integrating a SoftPOS SDK."
---

# Terminals and devices

Read `surfboard-payments` first.

## What needs registering, and what does not

| Terminal | Registration |
|---|---|
| Physical device (SurfTouch, SurfPad, SurfPrint, SurfMini, SurfAlone…) | Yes, via a registration code |
| `SelfHostedPage` | Yes |
| `PaymentPage` on an online store | **No, already provisioned** |
| `MerchantInitiated` on an online store | **No, already provisioned** |

Fetch the store's terminals before registering anything. Registering a terminal that
already exists is the most common wasted cycle in an online integration.

## Registering a physical device

1. Get a registration code from the device, or from the Terminals API
2. Register it against a `storeId`
3. Receive a `terminalId`, which is what goes in `terminal$id`

`references/guides/device-registration.md`.

## Configuration is hierarchical

```
partner  →  merchant  →  store  →  terminal
```

Settings such as WiFi, language, auto-sleep, tipping, and receipt behaviour can be set at any
level, and the more specific level overrides the broader one. Set sensible defaults at
partner level and override narrowly. Setting everything per terminal is how fleets
become unmanageable.

`references/guides/terminal-device-management.md`.

## Multi-merchant terminals

One physical device serving several merchants: food halls, markets, shared counters.
The terminal routes each transaction to the right merchant.

`references/guides/multi-merchant-terminals.md`.

## Logistics

Ordering, shipping, tracking, and returning hardware is an API, not an email thread.
Order during onboarding or later; returns go through the same route.

`references/guides/terminal-logistics.md`.

## SoftPOS SDKs

Turn a phone into a terminal, no hardware.

| Platform | Guide |
|---|---|
| iOS, Tap to Pay on iPhone | `references/guides/tap-to-pay-iphone.md` |
| Android | `references/guides/android-softpos-sdk.md` |

Tap to Pay on iPhone ships as a prebuilt `tap_to_pay_apple.xcframework` and needs an
Apple entitlement, which is a request to Apple with its own lead time. Flag that to the
user early, because it is a schedule risk rather than a code problem. Availability is limited to
Sweden, Denmark, Finland, Norway, UK, and France.

## Demo has limits

Demo terminals run in payment page mode only. A full hardware integration has to be
verified against real devices, which means Live credentials and certification. See
`surfboard-go-live`. Do not tell the user a terminal integration is proven when it has
only run in Demo.

## Bundled guides

`references/guides/` holds: device registration, terminal and device management, terminal
logistics, multi-merchant terminals, Android SoftPOS SDK, Tap to Pay on iPhone.
