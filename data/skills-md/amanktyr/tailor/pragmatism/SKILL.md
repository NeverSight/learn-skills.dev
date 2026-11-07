---
name: pragmatism
description: Enforces radical pragmatic simplicity, standard library utilization, zero-bloat software engineering, and the 7-step decision ladder across all major languages.
---

# Pragmatism & Anti-Bloat Skill

Activate this skill to eliminate over-engineered code, reject unnecessary packages, and write the minimal clean implementation that solves the requirement.

> **Engineering Motto:** *"Lazy, but never negligent. Simple, but never insecure."*

---

## 1. The 7-Step Decision Ladder (Mandatory Priority)

Before writing any new implementation or adding packages, work down this ladder and STOP at the first rung that provides a solution:

```
┌────────────────────────────────────────────────────────┐
│ 1. Does this need to exist? (YAGNI)                    │
│    -> If speculative or premature, REJECT IT.          │
├────────────────────────────────────────────────────────┤
│ 2. Already in this codebase?                           │
│    -> Search src/components/, src/lib/, src/utils/.    │
├────────────────────────────────────────────────────────┤
│ 3. Does the Standard Library do it?                    │
│    -> Use built-in crypto, fs, util, math, json, etc.  │
├────────────────────────────────────────────────────────┤
│ 4. Does a Native Platform / Browser API cover it?      │
│    -> Use <dialog>, <input type="date">, fetch, etc.   │
├────────────────────────────────────────────────────────┤
│ 5. Does an already-installed dependency solve it?      │
│    -> Reuse existing packages in package.json.         │
├────────────────────────────────────────────────────────┤
│ 6. Can it be written as a one-liner / inline helper?   │
│    -> If so, keep it concise (no 50-line wrappers).    │
├────────────────────────────────────────────────────────┤
│ 7. Only then: Write the minimum amount of clean code.  │
│    -> Enforce domain boundaries, types, and tests.     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Language Standard Library Replacement Catalog

Always prefer built-in standard library primitives over external packages:

### TypeScript & JavaScript (Node.js 18+ / Modern Browser)
| Proposed Package | Standard Library / Native Replacement |
| :--- | :--- |
| `uuid` / `nanoid` | `crypto.randomUUID()` |
| `lodash.clonedeep` / `clone-deep` | `structuredClone(value)` |
| `axios` / `node-fetch` / `got` | Native `fetch()` |
| `moment` / `dayjs` (simple formatting) | `Intl.DateTimeFormat` / native `Date` |
| `query-string` / `qs` | `new URLSearchParams(query)` |
| `mkdirp` / `rimraf` | `fs.mkdirSync(path, { recursive: true })` / `fs.rmSync(path, { recursive: true, force: true })` |
| `is-odd` / `is-number` / `left-pad` | Native arithmetic, `typeof`, `String.prototype.padStart()` |

### Python (Python 3.10+)
| Proposed Package | Standard Library Replacement |
| :--- | :--- |
| `requests` (simple scripts) | `urllib.request` or `http.client` |
| `pytz` | `zoneinfo.ZoneInfo` |
| `python-dateutil` (basic parsing) | `datetime.datetime.fromisoformat()` |
| `pathlib2` | Built-in `pathlib.Path` |
| `simplejson` | Built-in `json` |
| `attrs` (basic classes) | Built-in `@dataclass` or `typing.NamedTuple` |

### Go & Rust
| Ecosystem | Anti-Pattern Package | Native Alternative |
| :--- | :--- | :--- |
| **Go** | External router for simple microservices | Standard library `net/http` (Go 1.22+ enhanced routing) |
| **Go** | External logging library for simple CLIs | Standard library `log/slog` |
| **Rust** | Heavy async runtime for sync command-line tools | Standard library `std::fs`, `std::io`, `std::net` |

---

## 3. Intensity Modes

| Mode | Behavior & Operational Strictness |
| :--- | :--- |
| **`lite`** | Gentle guidance; implements requested code but politely flags simpler standard-library alternatives in review comments. |
| **`balanced`** *(default)* | Strictly enforces the decision ladder; rejects micro-packages, duplicates, and unvetted dependencies. |
| **`ultra`** | Hyper-minimalist; actively removes dead abstractions, rejects external packages if a 5-line inline helper works. |
| **`strict`** | Continuous integration (CI) mode; treats any redundant package or bypassed reuse check as an immediate hard failure. |

---

## 4. Strict Anti-Bloat & Zero-Slop Guardrails

* **Minimal Diff Discipline:** Implement strictly what is required to satisfy the prompt. Never refactor adjacent code, reformat untouched functions, or add unasked features.
* **No Speculative Abstractions:** Do not create abstract factory classes, generic type utilities, or 5-layer helper hierarchies for one-off operations.
* **No Mock / Dummy Data in Production:** Never inject fake user lists, mock arrays, or hardcoded dummy objects into real application files.
* **No Filler Comments:** Do not write comments that restate the obvious code (e.g. `// render button`, `// handle click`). Only document non-obvious *why* (business rules, security caveats).

---

## 5. The "Lazy, Not Negligent" Guardrails

Pragmatism must never be used as an excuse for cutting corners on critical system invariants:
* **Security & Validation:** Never skip input sanitization, CSRF defenses, or SQL parameterization.
* **Accessibility:** Native HTML elements must retain proper ARIA attributes, labels, and focus states.
* **Data Integrity:** Database transactions and atomic writes must be preserved across mutations.
* **Testing:** Always run targeted tests and verify exit code 0 before completing tasks.

