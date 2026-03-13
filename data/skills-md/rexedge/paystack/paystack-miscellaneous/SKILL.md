---
name: paystack-miscellaneous
description: >-
  Paystack Miscellaneous API — supporting endpoints for fetching bank lists, country
  data, and address verification states. Use this skill whenever you need bank codes
  for transfers or account resolution, listing supported countries and their currencies,
  fetching states for address verification (AVS), looking up bank slugs for DVA
  providers, or filtering banks by payment capabilities. Also use when you see
  references to /bank endpoint, bank_code lookups, /country endpoint, or
  /address_verification/states.
---

# Paystack Miscellaneous

Supporting APIs for bank lists, countries, and address verification.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/bank` | List banks |
| GET | `/country` | List supported countries |
| GET | `/address_verification/states` | List states for AVS |

## List Banks

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `country` | string | No | `ghana`, `kenya`, `nigeria`, `south africa` |
| `use_cursor` | boolean | No | Enable cursor pagination |
| `perPage` | integer | No | Records per page (default: 50, max: 100) |
| `pay_with_bank_transfer` | boolean | No | Filter banks supporting transfers |
| `pay_with_bank` | boolean | No | Filter banks supporting direct pay |
| `enabled_for_verification` | boolean | No | Filter banks supporting verification (SA) |
| `currency` | string | No | Filter by currency |
| `type` | string | No | `mobile_money` or `ghipss` (Ghana only) |
| `gateway` | string | No | `emandate` or `digitalbankmandate` |
| `next` / `previous` | string | No | Cursor pagination tokens |
| `include_nip_sort_code` | boolean | No | Include NIP institution code (Nigeria) |

```typescript
// All Nigerian banks
const banks = await paystackRequest("/bank?country=nigeria");
// banks.data[0]: { name, slug, code, longcode, gateway, pay_with_bank, active, country, currency, type }

// Banks that support bank transfer payment
const transferBanks = await paystackRequest(
  "/bank?country=nigeria&pay_with_bank_transfer=true"
);

// Ghana mobile money providers
const mobileMoney = await paystackRequest(
  "/bank?country=ghana&type=mobile_money"
);

// South African banks with verification support
const saBanks = await paystackRequest(
  "/bank?country=south%20africa&enabled_for_verification=true"
);
```

### Common Bank Codes (Nigeria)

| Bank | Code | Slug |
| --- | --- | --- |
| Access Bank | 044 | access-bank |
| GTBank | 058 | guaranty-trust-bank |
| First Bank | 011 | first-bank-of-nigeria |
| UBA | 033 | united-bank-for-africa |
| Zenith Bank | 057 | zenith-bank |
| Wema Bank | 035 | wema-bank |

## List Countries

```typescript
const countries = await paystackRequest("/country");
// countries.data[0]:
// {
//   id: 1,
//   name: "Nigeria",
//   iso_code: "NG",
//   default_currency_code: "NGN",
//   relationships: { currency: { data: ["NGN", "USD"] } }
// }
```

## List States (AVS)

Get states for address verification. The `country` param is the country code returned from the charge response (used during Address Verification challenges).

```typescript
const states = await paystackRequest(
  "/address_verification/states?country=CA"
);
// states.data[0]: { name: "Alberta", slug: "alberta", abbreviation: "AB" }
```
