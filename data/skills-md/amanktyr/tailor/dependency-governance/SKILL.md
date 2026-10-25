---
name: dependency-governance
description: Evaluates new and installed packages, npm install, pip install, package audit, micro-packages, supply-chain security, maintenance status, and license compatibility.
---

# Dependency Governance Skill

Activate this skill before installing, proposing, or upgrading any external package (`/dependency-check <package>` or `tailor dependencies --check <package>`).

> **Operational Directive:** *Every external package is a liability in security, bundle size, and maintenance. Treat additions as exceptional.*

---

## 1. Automated Rejection Table for Trivial Micro-Packages

Always reject external packages for operations natively supported by standard language primitives:

| Proposed Package | Recommendation | Preferred Native Alternative |
| :--- | :--- | :--- |
| `is-odd` / `is-even` | **REJECT** | `(n % 2 !== 0)` / `(n % 2 === 0)` |
| `left-pad` / `pad` | **REJECT** | `String.prototype.padStart()` |
| `is-number` / `is-string` | **REJECT** | `typeof x === 'number'` / `typeof x === 'string'` |
| `clone-deep` / `lodash.clonedeep` | **REJECT** | `structuredClone(obj)` |
| `deepmerge` / `object-assign` | **REJECT** | Object spread `{ ...a, ...b }` or small typed helper |
| `is-promise` | **REJECT** | `Boolean(x && typeof x.then === 'function')` |
| `array-flatten` | **REJECT** | `Array.prototype.flat(Infinity)` |

---

## 2. Redundancy & Modern Alternative Checks

| Proposed Package | Check Existing In Workspace | Modern Framework Alternative |
| :--- | :--- | :--- |
| `axios` | Check if `got`, `node-fetch`, or native `fetch` exists | Native global `fetch()` |
| `moment` | Check if `date-fns`, `dayjs`, or `luxon` exists | `date-fns` or `Intl.DateTimeFormat` |
| `uuid` | Check if `nanoid` or `cuid` exists | `crypto.randomUUID()` |
| `crypto-js` | Check if native `crypto` exists | `node:crypto` or Web Crypto API |

---

## 3. Supply-Chain Security & License Matrix

Before approving any non-trivial package, verify:
1. **Security Vulnerabilities:** Run `npm audit`, `pip-audit`, or `cargo audit`.
2. **Maintenance Activity:** Confirm active commits and releases within the past 12 months.
3. **License Classification:**
   - **Permissive (Approved):** `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `0BSD`, `CC0-1.0`.
   - **Copyleft (Requires Review):** `GPL-2.0`, `GPL-3.0`, `AGPL-3.0`, `SSPL`, `LGPL-3.0`.
4. **Documentation:** Record confirmed packages in `.ai/DEPENDENCIES.md`.

---

## 4. Mandatory Package Addition Protocol

Before running any install command (`npm install <pkg>`, `pip install <pkg>`, `cargo add <pkg>`), execute this decision flow:

1. **[ ] Can it be solved with native standard library?** (See Section 1 replacement table). If yes, **REJECT**.
2. **[ ] Is an equivalent package already installed?** (Check `dependencies` in `package.json`). If yes, **REUSE**.
3. **[ ] Can it be implemented as a clean 5-15 line helper?** If yes, implement inline in `src/utils/` and **REJECT** the package.
4. **[ ] Security & License Gate:** If an external package is strictly required, run `tailor dependencies --check <package>` and verify permissive license.
5. **[ ] Memory Recording:** Record the justification in `.ai/DEPENDENCIES.md` and commit the lockfile.

