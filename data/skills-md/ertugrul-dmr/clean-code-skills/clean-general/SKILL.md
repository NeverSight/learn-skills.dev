---
name: clean-general
description: Use when writing, fixing, editing, or reviewing Python code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles

## Critical Rules

**G5: DRY (Don't Repeat Yourself)**

Every piece of knowledge has one authoritative representation.

```python
# Bad - duplication
tax_rate = 0.0825
ca_total = subtotal * 1.0825
ny_total = subtotal * 1.07

# Good - single source of truth
TAX_RATES = {"CA": 0.0825, "NY": 0.07}
def calculate_total(subtotal: float, state: str) -> float:
    return subtotal * (1 + TAX_RATES[state])
```

**G16: No Obscured Intent**

Don't be clever. Be clear.

```python
# Bad - what does this do?
return (x & 0x0F) << 4 | (y & 0x0F)

# Good - obvious intent
return pack_coordinates(x, y)
```

**G23: Prefer Polymorphism to If/Else**

```python
# Bad - will grow forever
def calculate_pay(employee):
    if employee.type == "SALARIED":
        return employee.salary
    elif employee.type == "HOURLY":
        return employee.hours * employee.rate
    elif employee.type == "COMMISSIONED":
        return employee.base + employee.commission

# Good - open/closed principle
class SalariedEmployee:
    def calculate_pay(self): return self.salary

class HourlyEmployee:
    def calculate_pay(self): return self.hours * self.rate

class CommissionedEmployee:
    def calculate_pay(self): return self.base + self.commission
```

**G25: Replace Magic Numbers with Named Constants**

```python
# Bad
if elapsed_time > 86400:
    ...

# Good
SECONDS_PER_DAY = 86400
if elapsed_time > SECONDS_PER_DAY:
    ...
```

**G30: Functions Should Do One Thing**

If you can extract another function, your function does more than one thing.

**G36: Law of Demeter (Avoid Train Wrecks)**

```python
# Bad - reaching through multiple objects
output_dir = context.options.scratch_dir.absolute_path

# Good - one dot
output_dir = context.get_scratch_dir()
```

## Enforcement Checklist

When reviewing AI-generated code, verify:
- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Polymorphism over conditionals (G23)
- [ ] Functions do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
