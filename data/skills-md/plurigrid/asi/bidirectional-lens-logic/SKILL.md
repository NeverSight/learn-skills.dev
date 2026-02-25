---
name: bidirectional-lens-logic
description: Hedges' 4-kind lattice for bidirectional programming - covariant/contravariant/invariant/bivariant types with GF(3) correspondence
version: 1.0.0
---

# bidirectional-lens-logic

> The Logic of Lenses: 4-kind lattice for bidirectional programming

## Source

[Cybercat Institute: Foundations of Bidirectional Programming III](https://cybercat.institute/2024/09/12/bx-iii/)
— Jules Hedges, September 2024

## The 4-Kind Lattice

Variables have **temporal direction** — forwards or backwards in time:

```idris
Kind : Type
Kind = (Bool, Bool)  -- (covariant, contravariant)

--  Kind          Pair          Scoping Rules
-- ─────────────────────────────────────────────────
--  Covariant     (True, False)  delete, copy
--  Contravariant (False, True)  spawn, merge  
--  Bivariant     (True, True)   all four operations
--  Invariant     (False, False) none (linear)
```

## GF(3) Correspondence

The 4-kind lattice projects onto GF(3) via:

```
           BIVARIANT (True, True)
              ↙ 0 ↘
    COVARIANT       CONTRAVARIANT
   (True, False)    (False, True)
        +1              -1
              ↘   ↙
           INVARIANT (False, False)
              (linear, no trit)
```

| Kind | (cov, con) | Trit | Role | Operations |
|------|------------|------|------|------------|
| Covariant | (T, F) | +1 | Generator | delete, copy |
| Contravariant | (F, T) | -1 | Validator | spawn, merge |
| Bivariant | (T, T) | 0 | Coordinator | all four |
| Invariant | (F, F) | — | Linear | none |

## Tensor Product = GF(3) Multiplication

```idris
Tensor : Ty (covx, conx) -> Ty (covy, cony)
      -> Ty (covx && covy, conx && cony)
```

This IS the GF(3) multiplication table:

```
     | +1    0    -1
─────┼─────────────────
 +1  | +1   +1    0      (True && _ = depends)
  0  | +1    0   -1      (bivariant preserves)
 -1  |  0   -1   -1      (_ && True = depends)
```

When tensoring covariant (+1) with contravariant (-1):
- `covx && covy = True && False = False`
- `conx && cony = False && True = False`
- Result: (False, False) = **invariant/linear**

This is why **+1 ⊗ -1 = 0** gives us linear/invariant behavior!

## The Structure Datatype

Context morphisms with kind-aware operations:

```idris
data Structure : All Ty kas -> All Ty kbs -> Type where
  Empty  : Structure [] []
  Insert : Parity a b -> IxInsertion a as as' 
        -> Structure as bs -> Structure as' (b :: bs)
  
  -- Covariant operations (forward time)
  Delete : {a : Ty (True, con)} -> Structure as bs -> Structure (a :: as) bs
  Copy   : {a : Ty (True, con)} -> IxElem a as 
        -> Structure as bs -> Structure as (a :: bs)
  
  -- Contravariant operations (backward time)
  Spawn  : {b : Ty (cov, True)} -> Structure as bs -> Structure as (b :: bs)
  Merge  : {b : Ty (cov, True)} -> IxElem b bs 
        -> Structure as bs -> Structure (b :: as) bs
```

## CRDT Operation Mapping

```
Structure Op    CRDT Operation         Direction
─────────────────────────────────────────────────
Delete          crdt-stop-share-buffer  forward cleanup
Copy            crdt-share-buffer       forward duplicate
Spawn           (new user joins)        backward appearance
Merge           crdt-connect            backward unification
Insert          crdt-edit               linear (invariant)
```

## The Two NotIntro Rules

**Critical insight**: There are TWO introduction rules for negation, with **different operational semantics**:

```idris
NotIntroCov : {a : Ty (True, con)} -> Term (a :: as) Unit -> Term as (Not a)
NotIntroCon : {a : Ty (cov, True)} -> Term (a :: as) Unit -> Term as (Not a)
```

For bivariant types, **both rules apply but produce different results**!

This explains why GF(3) has:
- `+1` negates to `-1` via `NotIntroCov`
- `-1` negates to `+1` via `NotIntroCon`
- `0` can use either rule — but they're operationally distinct

## Negation Swaps Variance

```idris
Not : Ty (cov, con) -> Ty (con, cov)
```

- Covariant (+1) → Contravariant (-1)
- Contravariant (-1) → Covariant (+1)
- Bivariant (0) → Bivariant (0) [stable]
- Invariant → Invariant [stable]

## Integration with Open Games

The play/coplay structure of open games is precisely this bidirectionality:

```
        ┌───────────────┐
   X ──→│               │──→ Y      (covariant: forward play)
        │    Game G     │
   R ←──│               │←── S      (contravariant: backward coplay)
        └───────────────┘
```

- **X, Y**: Covariant types (strategies flow forward)
- **R, S**: Contravariant types (utilities flow backward)
- **Game G**: Invariant/linear (must use everything exactly once)

## Entropy-Sequencer Connection

The actionable information framework maps here:

```
H(I_{t+1} | I^t, u)     = covariant (forward prediction)
H(I_{t+1} | ξ, u)       = contravariant (backward from scene)
───────────────────────────────────────────────────────────
I(ξ; I_{t+1})           = invariant (linear combination)
```

## GF(3) Triad

| Trit | Skill | Role |
|------|-------|------|
| -1 | temporal-coalgebra | Contravariant observation |
| 0 | **bidirectional-lens-logic** | Bivariant coordination |
| +1 | free-monad-gen | Covariant generation |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Commands

```bash
# Typecheck bidirectional term
just bx-typecheck term.idr

# Evaluate with covariant semantics
just bx-eval-cov term.idr

# Evaluate with contravariant semantics  
just bx-eval-con term.idr

# Compare operational difference
just bx-compare term.idr
```

## Related Skills

- `entropy-sequencer` - Actionable information as bidirectional flow
- `open-games` - Play/coplay as cov/con
- `parametrised-optics-cybernetics` - Para(Lens) structure
- `polysimy-effect-chains` - Effect interpretation as context morphism
- `crdt` - Distributed state with bidirectional sync

## References

- Hedges, "Foundations of Bidirectional Programming I-III" (Cybercat Institute, 2024)
- Riley, "Categories of Optics"
- Ghani, Hedges et al., "Compositional Game Theory"
- Arntzenius, unpublished work on 4-element kind lattice



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
bidirectional-lens-logic (+) + SDF.Ch5 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch6: Layering
- Ch10: Adventure Game Example
- Ch7: Propagators

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
## Cat# Integration

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```