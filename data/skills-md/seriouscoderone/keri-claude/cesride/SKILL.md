---
name: cesride
description: >
  Rust CESR primitives library for KERI protocol. Auto-activates when working with
  cesride imports, Matter/Indexer traits, CESR primitive types (Verfer, Diger, Signer,
  Salter, Siger, Cigar), Serder/Sadder serialization, or Rust CESR encoding/decoding.
  Covers the full API: primitive construction, cryptographic operations, SAD serialization,
  threshold logic, and error handling. Defers to cesr/spec/acdc for
  protocol theory; focuses on Rust API specifics.
---

# cesride — Rust CESR Primitives

## Overview

cesride is the Rust implementation of CESR (Composable Event Streaming Representation)
primitives for the KERI ecosystem. It provides typed wrappers around cryptographic
material (keys, signatures, digests) with qualified CESR encoding (qb64/qb2), plus
SAD serialization (Serder/Creder), counter-based stream framing, and threshold logic.

Key design: every primitive implements the `Matter` trait (or `Indexer` for indexed
signatures), giving uniform `qb64()`/`qb2()`/`raw()`/`code()` access. Construction
follows a consistent pattern across all types.

**Companion skills:** For CESR encoding theory and code tables, see **cesr**. For
KERI event semantics, see **spec**. For ACDC credential structure, see **acdc**.

## Quick Reference

| Type | Purpose | Trait | Reference |
|------|---------|-------|-----------|
| `Verfer` | Public verification key | Matter | cesr-primitives.md |
| `Signer` | Private signing key (auto-zeroized) | Matter | cesr-primitives.md |
| `Diger` | Cryptographic digest | Matter | cesr-primitives.md |
| `Cigar` | Unindexed signature | Matter | cesr-primitives.md |
| `Siger` | Indexed signature (multisig) | Indexer | cesr-primitives.md |
| `Salter` | Key derivation salt (auto-zeroized) | Matter | cesr-primitives.md |
| `Saider` | Self-Addressing Identifier (SAID) | Matter | cesr-primitives.md |
| `Prefixer` | KERI identifier prefix | Matter | cesr-primitives.md |
| `Seqner` | Sequence number (16-byte) | Matter | cesr-primitives.md |
| `Number` | Auto-sized unsigned integer | Matter | cesr-primitives.md |
| `Dater` | ISO 8601 timestamp | Matter | cesr-primitives.md |
| `Bexter` | Base64 text (Bext trait) | Matter | cesr-primitives.md |
| `Pather` | SAD path resolver (Bext trait) | Matter | cesr-primitives.md |
| `Serder` | KERI event serializer | Sadder | sad-serialization.md |
| `Creder` | ACDC credential serializer | Sadder | sad-serialization.md |
| `Counter` | Group framing construct | — | sad-serialization.md |
| `Tholder` | Signing threshold logic | — | threshold-utils.md |

## Import Guide

```rust
// Core traits
use cesride::core::matter::Matter;
use cesride::core::indexer::Indexer;
use cesride::core::sadder::Sadder;
use cesride::core::bexter::Bext;

// Primitives
use cesride::core::{Verfer, Diger, Signer, Salter, Cigar, Siger};
use cesride::core::{Saider, Prefixer, Seqner, Number, Dater, Bexter, Pather};

// Serialization
use cesride::core::{Serder, Creder, Counter};
use cesride::core::common::{versify, deversify, sniff};

// Code tables
use cesride::core::matter::tables as MatterCodex;
use cesride::core::indexer::tables as IndexerCodex;
use cesride::core::counter::tables as CounterCodex;

// Data model
use cesride::data::{Value, dat};
use cesride::error::{Error, Result};

// Crypto (raw bytes, no CESR)
use cesride::crypto::{sign, hash, salt, csprng};
```

## Reference Files

| File | Contents | Size |
|------|----------|------|
| references/cesr-primitives.md | All 13 typed Matter/Indexer primitives — constructors, methods, valid codes | 11KB |
| references/sad-serialization.md | Sadder/Serder/Creder traits, Counter API, Ids/Ilkage constants | 4KB |
| references/crypto.md | Raw cryptographic operations — sign/verify, hash, stretch, CSPRNG | 5KB |
| references/data-errors.md | Value enum, data::Number, Error (28 variants), dat! macro | 7KB |
| references/threshold-utils.md | Tholder (weighted/unweighted), B64 conversion utilities | 6KB |

## Common Constructor Pattern

All Matter primitives share the same constructor family:

```rust
Type::new(/* type-specific params */, code, raw, qb64b, qb64, qb2) -> Result<Self>
Type::new_with_raw(raw, code) -> Result<Self>
Type::new_with_qb64(qb64) -> Result<Self>
Type::new_with_qb64b(qb64b) -> Result<Self>
Type::new_with_qb2(qb2) -> Result<Self>
```

Construction dispatches: first non-None wins in order: raw → qb64b → qb64 → qb2.

## Usage Patterns

### 1. Generate Key Pair and Sign

```rust
let signer = Signer::new_with_defaults(Some(true), None)?; // Ed25519, transferable
let verfer = signer.verfer();
let cigar = signer.sign_unindexed(message)?;
assert!(verfer.verify(&cigar.raw(), message)?);
```

### 2. Derive Keys from Salt

```rust
let salter = Salter::new_with_defaults(Some("low"))?;
let signers = salter.signers(Some(3), None, Some("icp"), None, None, None, None)?;
```

### 3. Create and Verify SAID

```rust
let (saider, saidified_sad) = Saider::saidify(&sad, None, None, None, None)?;
assert!(saider.verify(&saidified_sad, None, None, None, None, None)?);
```

### 4. Build KERI Event

```rust
let serder = Serder::new_with_ked(&ked, None, None)?;
let said = serder.said()?;
let pre = serder.pre()?;
let raw = serder.raw();
```

### 5. Check Threshold Satisfaction

```rust
let tholder = Tholder::new_with_sith(&dat!([["1/2", "1/2"], ["1"]]))?;
assert!(tholder.satisfy(&[0, 1, 2])?);
```

## Anti-Patterns

**DON'T:** Store `Signer` or `Salter` raw bytes — they auto-zeroize on drop.
**DO:** Use `Salter::signers()` with hierarchical paths for deterministic key derivation.

**DON'T:** Use `Cigar` for multisig — it has no index information.
**DO:** Use `Siger` with `sign_indexed()` for multisig coordination.

**DON'T:** Construct version strings manually.
**DO:** Use `versify()`/`deversify()` for version string handling.

**DON'T:** Confuse `data::Number` (JSON numeric wrapper) with `core::Number` (CESR primitive).
**DO:** Use `core::Number` for CESR-encoded integers, `data::Number` for JSON values.

**DON'T:** Use `Counter` as a Matter primitive — it has its own encoding scheme.
**DO:** Use `Counter::new_with_code_and_count()` for stream framing.
