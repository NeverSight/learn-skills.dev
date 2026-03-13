---
name: time-value-of-money
description: "Calculate present value, future value, NPV, IRR, loan payments, and amortization schedules across all compounding conventions. Use when the user asks about discounting cash flows, valuing an annuity or perpetuity, comparing investments with different timing, building a mortgage amortization table, or evaluating whether a project is worth pursuing. Also trigger when users mention 'what is it worth today', 'how much will I have in 20 years', 'monthly payment on a loan', 'discount rate', 'Gordon growth model', 'effective annual rate', 'continuous compounding', or ask how to compare a lump sum versus a stream of payments."
---

# Time Value of Money

## Purpose
This skill enables Claude to perform present value, future value, and discounted cash flow calculations across all standard compounding conventions. It covers annuities, perpetuities, amortization schedules, NPV, and IRR, providing the foundational building blocks for virtually all financial valuation and planning tasks.

## Layer
0 — Mathematical Foundations

## Direction
both (retrospective for valuing past cash flows, prospective for projecting future values)

## When to Use
- Discounting future cash flows
- Building amortization tables
- Comparing investments with different timing
- Calculating loan payments
- NPV or IRR analysis

## Core Concepts

### Future Value (FV)
The value of a present sum after earning interest for `n` periods at rate `r` per period.

$$FV = PV \times (1 + r)^n$$

Future value grows exponentially with time, which is the mathematical basis of compound interest.

### Present Value (PV)
The current worth of a future sum, discounted back at rate `r` for `n` periods. This is the inverse of future value.

$$PV = \frac{FV}{(1 + r)^n}$$

Present value is the cornerstone of all valuation: a dollar today is worth more than a dollar tomorrow because of the opportunity cost of capital.

### Compounding Conventions
Interest can compound at different frequencies. The nominal annual rate `r_nom` compounded `m` times per year produces different effective yields.

**Discrete compounding (m times per year):**

$$FV = PV \times \left(1 + \frac{r_{nom}}{m}\right)^{m \times t}$$

**Continuous compounding:**

$$FV = PV \times e^{r \times t}$$

**Effective Annual Rate (EAR):**

$$EAR = \left(1 + \frac{r_{nom}}{m}\right)^m - 1$$

For continuous compounding: `EAR = e^(r_nom) - 1`

Common frequencies:
| Frequency | m |
|-----------|---|
| Annual | 1 |
| Semi-annual | 2 |
| Quarterly | 4 |
| Monthly | 12 |
| Daily | 365 |
| Continuous | infinity |

### Ordinary Annuity
A series of equal payments made at the **end** of each period for `n` periods.

**Present Value:**

$$PV = PMT \times \frac{1 - (1 + r)^{-n}}{r}$$

**Future Value:**

$$FV = PMT \times \frac{(1 + r)^n - 1}{r}$$

### Annuity Due
A series of equal payments made at the **beginning** of each period. Each cash flow is one period closer than in an ordinary annuity, so values are scaled by `(1 + r)`.

**Present Value:**

$$PV = PMT \times \frac{1 - (1 + r)^{-n}}{r} \times (1 + r)$$

**Future Value:**

$$FV = PMT \times \frac{(1 + r)^n - 1}{r} \times (1 + r)$$

### Growing Annuity
A finite series of payments that grow at a constant rate `g` per period, where `g != r`.

**Present Value:**

$$PV = \frac{PMT}{r - g} \times \left[1 - \left(\frac{1 + g}{1 + r}\right)^n\right]$$

This is widely used in equity valuation (e.g., multi-stage dividend discount models) and salary/pension projections.

### Perpetuity
An infinite stream of equal payments.

$$PV = \frac{PMT}{r}$$

### Growing Perpetuity
An infinite stream of payments growing at constant rate `g`, where `g < r` for convergence.

$$PV = \frac{PMT}{r - g}$$

This is the Gordon Growth Model when applied to dividends.

### Net Present Value (NPV)
The sum of all discounted cash flows, including the initial investment. A positive NPV indicates value creation.

$$NPV = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

Typically, `CF_0` is a negative outflow (initial investment), and subsequent `CF_t` are inflows.

### Internal Rate of Return (IRR)
The discount rate `r` that makes the NPV of all cash flows exactly zero.

$$0 = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

IRR is solved numerically (Newton-Raphson or bisection) since there is no closed-form solution for general cash flow streams. For conventional cash flows (one sign change), a unique IRR exists.

### Amortization
Each payment on an amortizing loan is split into an interest component and a principal component:

- **Interest portion:** `Interest_t = Balance_{t-1} * r`
- **Principal portion:** `Principal_t = PMT - Interest_t`
- **Remaining balance:** `Balance_t = Balance_{t-1} - Principal_t`

Over time, the interest portion decreases and the principal portion increases.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Future Value | `FV = PV * (1 + r)^n` | Compound a lump sum forward |
| Present Value | `PV = FV / (1 + r)^n` | Discount a future lump sum |
| EAR | `(1 + r_nom/m)^m - 1` | Compare rates across compounding frequencies |
| Continuous FV | `FV = PV * e^(r*t)` | Continuous compounding |
| Ordinary Annuity PV | `PMT * [1 - (1+r)^(-n)] / r` | Loan payments, lease valuation |
| Annuity Due PV | `PMT * [1 - (1+r)^(-n)] / r * (1+r)` | Rent, insurance (paid in advance) |
| Growing Annuity PV | `PMT/(r-g) * [1 - ((1+g)/(1+r))^n]` | Salary streams, growing dividends |
| Perpetuity PV | `PMT / r` | Preferred stock, consol bonds |
| Growing Perpetuity PV | `PMT / (r - g)` | Gordon Growth Model |
| NPV | `sum(CF_t / (1+r)^t)` | Project/investment evaluation |
| IRR | `solve: sum(CF_t / (1+r)^t) = 0` | Return metric for uneven cash flows |

## Worked Examples

### Example 1: Monthly Mortgage Payment
**Given:** A $300,000 mortgage at a 6.5% annual interest rate, fixed for 30 years, with monthly payments (ordinary annuity).

**Calculate:** The monthly payment amount.

**Solution:**

First, convert the annual rate to a monthly rate and years to months:
```
r_monthly = 0.065 / 12 = 0.00541667
n = 30 * 12 = 360 months
```

Using the ordinary annuity present value formula, solve for PMT:
```
PV = PMT * [1 - (1 + r)^(-n)] / r

300,000 = PMT * [1 - (1.00541667)^(-360)] / 0.00541667
```

Compute the annuity factor:
```
(1.00541667)^360 = 6.99179
(1.00541667)^(-360) = 0.143010
1 - 0.143010 = 0.856990
0.856990 / 0.00541667 = 158.2108
```

Solve for PMT:
```
PMT = 300,000 / 158.2108 = $1,896.20
```

The monthly mortgage payment is **$1,896.20**.

Over 30 years, total payments = `360 * $1,896.20 = $682,632`, meaning total interest paid is `$682,632 - $300,000 = $382,632`.

### Example 2: NPV of a Project with Uneven Cash Flows
**Given:** A project requires an initial investment of $50,000 and produces the following cash flows:
- Year 1: $12,000
- Year 2: $15,000
- Year 3: $18,000
- Year 4: $22,000
- Year 5: $25,000

The required rate of return (discount rate) is 10%.

**Calculate:** The NPV and whether the project should be accepted.

**Solution:**

Discount each cash flow to present value:
```
PV(CF_0) = -50,000 / (1.10)^0 = -50,000.00
PV(CF_1) =  12,000 / (1.10)^1 =  10,909.09
PV(CF_2) =  15,000 / (1.10)^2 =  12,396.69
PV(CF_3) =  18,000 / (1.10)^3 =  13,524.21
PV(CF_4) =  22,000 / (1.10)^4 =  15,026.30
PV(CF_5) =  25,000 / (1.10)^5 =  15,523.03
```

Sum all present values:
```
NPV = -50,000.00 + 10,909.09 + 12,396.69 + 13,524.21 + 15,026.30 + 15,523.03
NPV = +$17,379.32
```

Since NPV is **positive ($17,379.32)**, the project creates value and should be accepted. It earns more than the 10% required rate of return.

To find the IRR, we would solve for the rate where NPV = 0. Numerically, the IRR for this cash flow stream is approximately **21.0%**, well above the 10% hurdle rate.

## Common Pitfalls
- Mismatching rate and period frequency: if payments are monthly, the discount rate must be a monthly rate. Divide the annual nominal rate by 12, do not take the 12th root of `(1 + annual rate)` unless converting from EAR.
- Forgetting the sign convention for cash flows in IRR: outflows (investments) must be negative and inflows (returns) positive, or vice versa, but the convention must be consistent. Incorrect signs produce meaningless IRR results.
- Confusing nominal vs effective rates: a 12% nominal rate compounded monthly produces an EAR of 12.68%, not 12%. Always clarify the compounding basis.
- Off-by-one errors in annuity due vs ordinary annuity: an annuity due shifts all payments one period earlier. Forgetting the `(1 + r)` adjustment factor will undervalue annuity-due streams.
- Multiple IRR solutions with non-conventional cash flows: when cash flows change sign more than once (e.g., initial outflow, inflows, then a large terminal outflow), Descartes' rule allows up to as many positive real IRR solutions as there are sign changes. In such cases, use NPV profiling or the Modified IRR (MIRR) instead.

## Cross-References
- **return-calculations** (core plugin, Layer 0): CAGR is a special case of compound growth; MWR/IRR uses the same NPV=0 framework
- **statistics-fundamentals** (core plugin, Layer 0): Discount rate estimation often relies on regression (CAPM beta) and distributional assumptions

## Reference Implementation
See `scripts/time_value_of_money.py` for computational helpers.
