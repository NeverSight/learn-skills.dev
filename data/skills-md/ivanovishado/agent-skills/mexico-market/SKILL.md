---
name: mexico-market
description: "Mexico-specific product and payments knowledge for marketplaces. Use when building payment flows, pricing pages, or user experiences for Mexican users. Covers SPEI bank transfers, OXXO cash payments, WhatsApp communication patterns, pricing psychology for Mexico, and cultural UX considerations. Triggers on 'Mexico payments', 'SPEI', 'OXXO', 'Mexican market', 'WhatsApp Mexico', or 'pesos pricing'."
---

# Mexico Market Skill

This skill provides Mexico-specific product, payments, and UX knowledge for building marketplaces and consumer applications targeting Mexican users.

## Payment Methods in Mexico

### SPEI (Sistema de Pagos Electronicos Interbancarios)

SPEI is Mexico's real-time bank transfer system. It is:

- **Instant**: Transfers complete in seconds (legally within 30 seconds)
- **Free or very cheap**: Banks typically charge $0-10 MXN per transfer
- **Universal**: Every Mexican bank supports it
- **Trusted**: Government-backed, used for large transactions

**Key insight**: SPEI should be the PRIMARY payment method for B2C apps in Mexico, not cards.

#### SPEI Implementation

```
Guest pays via SPEI:
1. Platform displays CLABE (18-digit bank account number)
2. Guest adds unique reference number (booking ID)
3. Guest initiates transfer from their bank app
4. Platform receives funds instantly (webhook or polling)
5. Platform confirms payment via WhatsApp
```

**CLABE format**: 18 digits = 3 (bank) + 3 (plaza) + 11 (account) + 1 (checksum)

### Cards (via OpenPay/Conekta/Stripe)

Card penetration in Mexico is lower than US/EU, but growing. Cards are:

- **Recommended: OpenPay** – 2.9% + $2.50 MXN per transaction (lowest)
- **Alternative: Conekta** – 3.4% + $3.00 MXN per transaction
- **Fallback: Stripe** – 3.6% + $3.00 MXN per transaction
- **Convenient**: No friction for users with cards
- **Risky**: Higher chargeback rates in Mexico

### OXXO (Cash Payments)

OXXO is Mexico's largest convenience store chain (20,000+ stores). OXXO payments:

- **Accessibility**: Reaches unbanked population (~40% of adults)
- **Trust**: Cash-preferred users trust OXXO
- **Delay**: 24-72 hours settlement
- **Fees**:
  - **OpenPay (Paynet)**: 2.9% + $2.50 MXN
  - **Conekta (OXXO Pay)**: 2.6% + $3.00 MXN (lowest)
  - **Stripe**: 3.6% + $3.00 MXN

**OXXO flow**:

1. Platform generates voucher (OpenPay/Conekta)
2. User receives barcode via WhatsApp/email
3. User pays at OXXO counter
4. Platform receives confirmation (24-72h)

---

## Pricing Display Strategy

In Mexico, showing "upcharges" irks customers. Instead, display SPEI as discounted from a base price that includes all fees. This matches gas station patterns (cash discount) and feels like a reward, not a penalty.

### Strategy: Card-Inclusive Base, SPEI Discount

1. **Base price** = Owner price + platform fee (10%) + card processing fees
2. **Card payment** = Base price (no surprise, clean checkout)
3. **SPEI** = Base price minus card fees (real discount)
4. **OXXO** = Base price (included in base, no upcharge shown)

> [!IMPORTANT]
> **Never show upcharges**. Mexican users respond negatively to "+3% for card". Instead, show SPEI as "Ahorra $X" from the base price.

### Display Pattern

```
Depósito: $5,700 MXN

🏦 Transferencia SPEI:         $5,500 ← ¡Ahorra $200!
💳 Tarjeta de crédito/débito:  $5,700
🏪 OXXO:                       $5,700
```

**Key UX notes:**

- Lead with SPEI (cheapest, platform-preferred)
- Card and OXXO show same price (base includes both fees)
- No asterisks, no "comisión extra" language

### Why This Works

1. **Round base**: $5,700 includes OpenPay card fees, clean mental accounting
2. **SPEI incentive**: Real savings (not fake discount) build trust
3. **No upcharge psychology**: Card users don't feel penalized
4. **OXXO simplicity**: Same as card, no confusion about extra fees

### Implementation

```typescript
const PLATFORM_FEE_PERCENT = 0.1; // 10% platform commission
const OPENPAY_CARD_PERCENT = 0.029; // 2.9%
const OPENPAY_CARD_FIXED = 2.5; // MXN
const OPENPAY_SPEI_FIXED = 8; // MXN flat fee

const calculatePaymentOptions = (ownerPrice: number) => {
  // Calculate platform fee (10% to owner)
  const platformFee = Math.ceil(ownerPrice * PLATFORM_FEE_PERCENT);
  const subtotal = ownerPrice + platformFee;

  // Card fee baked into base price
  const cardFee = Math.ceil(subtotal * OPENPAY_CARD_PERCENT + OPENPAY_CARD_FIXED);
  const basePrice = subtotal + cardFee; // e.g., $5,700

  // SPEI is truly discounted (only $8 flat fee, absorbed by platform)
  const speiPrice = subtotal; // e.g., $5,500
  const speiSavings = cardFee; // e.g., $200

  return {
    spei: {
      price: speiPrice,
      label: `Transferencia SPEI`,
      savings: speiSavings,
      savingsLabel: `¡Ahorra $${speiSavings}!`,
    },
    card: {
      price: basePrice,
      label: "Tarjeta de crédito/débito",
    },
    oxxo: {
      price: basePrice,
      label: "OXXO",
    },
  };
};

// Example: $5,000 terrace
// Owner gets: $5,000
// Platform gets: $500 (10%)
// Card fee: ~$200 (2.9% + $2.50)
// Guest pays: $5,700 (card/OXXO) or $5,500 (SPEI)
```

> [!NOTE]
> **Fee constants**: Use OpenPay rates (2.9% + $2.50 cards, $8 SPEI). Update if provider changes. SPEI $8 fee is absorbed by platform margin.

---

## WhatsApp in Mexico

WhatsApp is the dominant communication channel in Mexico. ~90% of smartphone users have WhatsApp.

### WhatsApp-First Design Principles

1. **Notifications**: All critical notifications via WhatsApp, email as backup
2. **No app downloads**: Users resist downloading new apps
3. **LLM chatbots**: Natural language over structured menus
4. **Voice notes**: Many users prefer voice over typing

### WhatsApp Business API Considerations

- **Template messages**: Pre-approved templates for outbound messages
- **Session messages**: Free within 24h of user-initiated conversation
- **Utility vs Marketing**: Utility templates cheaper than marketing
- **Meta fee changes**: July 2025 switched to per-template billing

### Common WhatsApp Flows

```
Booking confirmation:
  "¡Hola, [Nombre]! Tu reserva en [Terraza] para el [Fecha] está confirmada.
   Depósito: $[Amount] MXN
   Dirección: [Address]
   Contacto del propietario: [Phone]"

Payment reminder:
  "¡Recordatorio! Tu pago de $[Amount] vence mañana.
   Paga aquí: [Link]"

Owner notification:
  "¡Nueva solicitud de reserva!
   Fecha: [Date]
   Invitados: [Count]
   Responde SÍ para aprobar o NO para rechazar."
```

---

## Cultural UX Considerations

### Trust Signals

Mexican users value:

- **Phone verification**: More trusted than email-only
- **WhatsApp contact**: Direct line to support builds trust
- **Payment security badges**: Visa/Mastercard/Stripe logos
- **Clear cancellation policies**: Mexicans are risk-averse with online payments

### Price Psychology

> [!NOTE]
> **Research finding**: Charm pricing (.99) works for discount perception but can hurt quality perception. For premium services like terrace rentals, **round numbers signal quality and trust**.

- **Round numbers for premium**: $5,000 > $4,999 for quality perception
- **IVA included**: Mexican law requires all taxes in displayed price
- **MSI (Meses Sin Intereses)**: Interest-free installments are HUGE in Mexico
- **"Ahorra" framing**: Savings language resonates strongly
- **Peso formatting**: $5,000 MXN (comma as thousands separator)

### Language Notes

- **Tú vs Usted**: Default to "tú" for consumer apps (informal)
- **Regionalism**: "Rentar" (rent) not "alquilar" in Mexico
- **Avoid Spain Spanish**: Use Mexican vocabulary and expressions

---

## API Pricing Reference (2026)

> [!TIP]
> **Last verified**: February 2026. Check official pricing pages for updates.

### OpenPay Mexico (Recommended)

- Card transaction: 2.9% + $2.50 MXN + IVA
- SPEI: $8 MXN + IVA per transaction
- OXXO (Paynet): 2.9% + $2.50 MXN + IVA
- MSI: 3-months +4.8%, 6-months +7.8%, 12-months +13.8%
- Payouts: Free weekly, $8 MXN manual
- **Reference**: [openpay.mx/comisiones](https://www.openpay.mx/comisiones)

### Conekta Mexico (OXXO Alternative)

- Card transaction: 3.4% + $3 MXN + IVA
- SPEI: $12.50 MXN + IVA
- OXXO: 2.6% + $3 MXN + IVA (lowest)
- MSI: 3-months +5.4%, 12-months +14.1%
- **Reference**: [conekta.com/pricing](https://www.conekta.com/pricing)

### Stripe Mexico (Fallback)

- Card transaction: 3.6% + $3 MXN + IVA
- International cards: +0.5%
- SPEI: $7 MXN + IVA
- OXXO: 3.6% + $3 MXN + IVA
- **Reference**: [stripe.com/mx/pricing](https://stripe.com/mx/pricing)

### Twilio WhatsApp (Post-July 2025)

- Per-message fee: $0.005 USD
- Utility template (within 24h): Free Meta fee
- Marketing template: ~$0.03-0.05 USD Meta fee

### Google Maps (Post-March 2025)

- $200 monthly credit discontinued
- Dynamic Maps: 10,000 free/month, then $7/1,000
- Geocoding: 5,000 free/month, then $5/1,000

---

## Quick Reference

| Need               | Solution                                |
| ------------------ | --------------------------------------- |
| Primary payment    | SPEI via OpenPay ($8 MXN flat)          |
| Card processing    | OpenPay (2.9% + $2.50, lowest)          |
| Cash accessibility | OXXO via OpenPay or Conekta             |
| Platform fee       | 10% charged to owner                    |
| Notifications      | WhatsApp (primary), email (backup)      |
| Trust building     | Phone verification, WhatsApp contact    |
| Price display      | Base = card price, SPEI = "¡Ahorra $X!" |
| Language           | Mexican Spanish, informal "tú"          |

### Provider Selection (MVP)

| Method | Provider | Fee             | Notes               |
| ------ | -------- | --------------- | ------------------- |
| Card   | OpenPay  | 2.9% + $2.50    | Lowest, BBVA-backed |
| SPEI   | OpenPay  | $8 flat         | Absorbed by margin  |
| OXXO   | OpenPay  | 2.9% + $2.50    | Same as card        |
| MSI    | OpenPay  | +4.8% to +13.8% | 3-12 months         |

**Future optimization**: Add Conekta for OXXO (2.6% vs 2.9%) if volume justifies dual integration.
