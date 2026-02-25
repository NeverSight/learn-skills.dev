---
name: type-checker
description: Type Checker Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# type-checker Skill


> *"Catch errors before they run. Types are theorems, programs are proofs."*

## Overview

**Type Checker** implements bidirectional type checking for dependent types. Validates that programs are well-typed before execution, catching errors at compile time.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates type correctness of programs |

## Bidirectional Type Checking

```
┌─────────────────────────────────────────────────────────────────┐
│                  BIDIRECTIONAL TYPING                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Check Mode (⇐):             Infer Mode (⇒):                   │
│  "Does term have type?"      "What type does term have?"       │
│                                                                 │
│  Γ ⊢ e ⇐ A                   Γ ⊢ e ⇒ A                        │
│                                                                 │
│  Used for:                   Used for:                         │
│  - Lambda abstractions       - Variables                       │
│  - Match expressions         - Applications                    │
│  - Holes                     - Annotated terms                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Algorithm

```python
class TypeChecker:
    """Bidirectional type checker with dependent types."""

    TRIT = -1  # VALIDATOR role

    def check(self, ctx: Context, term: Term, expected: Type) -> bool:
        """
        Check mode: verify term has expected type.
        """
        match term:
            case Lam(x, body):
                # For λx.body, expected must be Π(x:A).B
                match expected:
                    case Pi(_, a, b):
                        # Check body in extended context
                        return self.check(ctx.extend(x, a), body, b)
                    case _:
                        return False

            case Hole(name):
                # Record constraint for hole
                self.add_constraint(name, expected)
                return True

            case _:
                # Fall back to infer and compare
                inferred = self.infer(ctx, term)
                return self.equal(ctx, inferred, expected)

    def infer(self, ctx: Context, term: Term) -> Type:
        """
        Infer mode: synthesize type from term.
        """
        match term:
            case Var(x):
                return ctx.lookup(x)

            case App(func, arg):
                func_type = self.infer(ctx, func)
                match func_type:
                    case Pi(x, a, b):
                        self.check(ctx, arg, a)
                        return self.subst(b, x, arg)
                    case _:
                        raise TypeError(f"Expected function, got {func_type}")

            case Ann(term, typ):
                # Annotation: (term : type)
                self.check(ctx, typ, Type())
                self.check(ctx, term, typ)
                return typ

            case _:
                raise TypeError(f"Cannot infer type of {term}")
```

## Type Equality

```python
def equal(self, ctx: Context, a: Type, b: Type) -> bool:
    """
    Check type equality up to β-reduction.
    """
    # Normalize both types
    a_nf = self.normalize(ctx, a)
    b_nf = self.normalize(ctx, b)

    # Compare normal forms
    return self.alpha_equal(a_nf, b_nf)

def normalize(self, ctx: Context, term: Term) -> Term:
    """
    Reduce term to normal form.
    """
    match term:
        case App(Lam(x, body), arg):
            # β-reduction
            return self.normalize(ctx, self.subst(body, x, arg))

        case App(func, arg):
            func_nf = self.normalize(ctx, func)
            if func_nf != func:
                return self.normalize(ctx, App(func_nf, arg))
            return App(func_nf, self.normalize(ctx, arg))

        case _:
            return term
```

## Dependent Types

```haskell
-- Pi types: Π(x : A). B(x)
-- The type of functions where return type depends on input

-- Vector: type indexed by length
data Vec : Nat -> Type -> Type where
  Nil  : Vec 0 a
  Cons : a -> Vec n a -> Vec (Succ n) a

-- Dependent function: length is part of the type!
head : Π(n : Nat). Π(a : Type). Vec (Succ n) a -> a
head _ _ (Cons x _) = x

-- Sigma types: Σ(x : A). B(x)
-- Dependent pairs where second component type depends on first

-- Exists: there exists an n such that vec has length n
exists_vec : Σ(n : Nat). Vec n Int
exists_vec = (3, Cons 1 (Cons 2 (Cons 3 Nil)))
```

## Universes

```
Type : Type₁ : Type₂ : Type₃ : ...

Universe levels prevent paradoxes:
- Type₀ (or just Type) is the type of "small" types
- Type₁ is the type of Type₀
- And so on...

Cumulativity: Type_i <: Type_{i+1}
```

## Error Messages

```python
class TypeErrorFormatter:
    """Generate helpful type error messages."""

    def format_mismatch(self, expected: Type, got: Type, term: Term) -> str:
        return f"""
Type mismatch:
  Expected: {self.pretty(expected)}
  Got:      {self.pretty(got)}
  In term:  {self.pretty(term)}

Hint: {self.suggest_fix(expected, got)}
"""

    def format_undefined(self, var: str, ctx: Context) -> str:
        similar = self.find_similar(var, ctx.names())
        return f"""
Undefined variable: {var}

Did you mean: {', '.join(similar)}?

Available in scope:
{self.format_context(ctx)}
"""
```

## GF(3) Type Validation

```python
class GF3TypeChecker(TypeChecker):
    """Type checker with GF(3) conservation verification."""

    def check_program(self, program: Program) -> Result:
        """
        Type check with GF(3) balance verification.
        """
        # Standard type checking
        type_result = super().check_program(program)

        if not type_result.success:
            return type_result

        # GF(3) validation
        gf3_result = self.verify_gf3_balance(program)

        return Result(
            success=type_result.success and gf3_result.balanced,
            types=type_result.types,
            gf3_sum=gf3_result.sum,
            conserved=gf3_result.balanced
        )

    def verify_gf3_balance(self, program: Program) -> GF3Result:
        """
        Verify program maintains GF(3) conservation.

        Terms classified:
        - GENERATOR (+1): Constructors, lambdas
        - COORDINATOR (0): Applications, matches
        - VALIDATOR (-1): Destructors, checks
        """
        trit_sum = 0
        for term in program.terms:
            trit_sum += self.term_trit(term)

        return GF3Result(
            sum=trit_sum,
            balanced=(trit_sum % 3 == 0)
        )
```

## GF(3) Triads

```
type-checker (-1) ⊗ interaction-nets (0) ⊗ lambda-calculus (+1) = 0 ✓
type-checker (-1) ⊗ datalog-fixpoint (0) ⊗ hvm-runtime (+1) = 0 ✓
type-checker (-1) ⊗ move-narya-bridge (0) ⊗ discopy (+1) = 0 ✓
```

## Commands

```bash
# Type check a file
just typecheck program.tt

# Infer types with holes
just typecheck program.tt --infer-holes

# Check with verbose output
just typecheck program.tt --verbose

# Generate type annotations
just typecheck program.tt --annotate

# Check Move contract types
just move-typecheck sources/gf3.move
```

---

**Skill Name**: type-checker
**Type**: Type Theory / Static Analysis
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Validates type correctness before execution

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule in the Prof home:

```
Trit: 0 (ERGODIC)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

The skill participates in triads where:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.
