---
name: code-styleguide
description: Universal code style guidelines and principles for writing clean, maintainable code in any programming language. Use when writing or reviewing code, refactoring existing code, conducting code reviews, or establishing coding standards. Focuses on abstraction, KISS principles, SOLID principles, and avoiding over-engineering.
---

# Code Styleguide

## Overview

Universal code style guidelines that promote clean, maintainable, and readable code across all programming languages. These principles focus on simplicity, clarity, and avoiding unnecessary complexity while following proven software engineering best practices.

## Core Principles

### 1. KISS (Keep It Simple, Stupid)

**The simplest solution is usually the best solution.**

- Favor clear, straightforward code over clever tricks
- One function should do one thing well
- Prefer explicit code over implicit behavior
- Avoid premature optimization
- Write code, not documentation: minimize auxiliary files
- Never use emoji in code or comments

**Good:**
```python
def calculate_total_price(items):
    total = 0
    for item in items:
        total += item.price
    return total
```

**Avoid:**
```python
def calculate_total_price(items):
    return sum(item.price for item in items) if items else 0 or reduce(lambda x, y: x + y.price, items, 0)
```

### 2. Abstraction Levels

**Each level of abstraction should be consistent and purposeful.**

- Functions should operate at a single level of abstraction
- Hide complexity behind clear interfaces
- Use descriptive names that match the abstraction level

**Good:**
```python
def process_user_registration():
    user_data = validate_input()
    user = create_user(user_data)
    send_welcome_email(user)
    return user
```

**Avoid mixing abstraction levels:**
```python
def process_user_registration():
    if not email or '@' not in email:  # Low-level validation
        raise ValueError("Invalid email")
    user = User.create(email)  # High-level operation
    smtp.send(email, "Welcome!")  # Medium-level operation
```

### 3. SOLID Principles

#### Single Responsibility Principle (SRP)
**A class should have one, and only one, reason to change.**

```python
# Good: Separate concerns
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserValidator:
    def validate_email(self, email):
        return '@' in email and '.' in email
    
class EmailService:
    def send_welcome_email(self, user):
        # Email sending logic
```

#### Open/Closed Principle (OCP)
**Classes should be open for extension, closed for modification.**

```python
# Good: Use abstract base classes
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # Credit card processing logic
        
class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # PayPal processing logic
```

#### Liskov Substitution Principle (LSP)
**Objects of a superclass should be replaceable with objects of a subclass.**

#### Interface Segregation Principle (ISP)
**Clients should not be forced to depend on interfaces they don't use.**

#### Dependency Inversion Principle (DIP)
**Depend on abstractions, not concretions.**

### 4. Avoiding Over-Engineering

**Don't build what you don't need right now.**

- Start with the simplest solution that works
- Add complexity only when requirements demand it  
- Prefer composition over inheritance
- Avoid speculative generality
- Question every abstraction: does it solve a real problem?
- Resist the urge to make code "flexible" without concrete use cases

**Good (simple and direct):**
```python
class ConfigManager:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)
    
    def get(self, key):
        return self.config.get(key)
```

**Over-engineered:**
```python
class AbstractConfigurationStrategy(ABC):
    @abstractmethod
    def load_configuration(self): pass

class JSONConfigurationStrategy(AbstractConfigurationStrategy):
    # ... complex factory pattern implementation

class ConfigurationManager:
    def __init__(self, strategy: AbstractConfigurationStrategy):
        self.strategy = strategy
    # ... unnecessary abstractions for a simple config reader
```

### 5. Minimize Documentation Files

**Code should be self-documenting. Documentation is supplementary, not primary.**

- Avoid creating multiple CHANGELOG, or summary files
- Don't generate progress reports or status documents  
- Keep documentation in code (docstrings, inline comments)
- One README per project maximum
- No emoji in any output files

**Good:**
```python
def calculate_discount(price: float, customer_type: str) -> float:
    """Calculate discount based on customer type.
    
    Args:
        price: Original price
        customer_type: One of 'regular', 'premium', 'vip'
    
    Returns:
        Discounted price
    """
    discounts = {'regular': 0, 'premium': 0.1, 'vip': 0.2}
    return price * (1 - discounts.get(customer_type, 0))
```

**Avoid:**
- CHANGES.md documenting every modification
- SUMMARY.md repeating what code already shows
- Multiple README files at different levels
- Using emoji for status indicators or decorative purposes

## Naming Conventions

### Universal Rules
- Use descriptive, searchable names
- Avoid abbreviations and single-character variables (except loop counters)
- Use intention-revealing names
- Avoid mental mapping

**Good:**
```python
user_count = len(users)
is_valid_email = validate_email(email)
for user_index in range(user_count):
```

**Avoid:**
```python
uc = len(u)
flag = check(e)
for i in range(uc):
```

### Functions and Methods
- Use verb phrases for actions
- Use boolean-returning functions with `is_`, `has_`, `can_` prefixes
- Keep function names concise but descriptive

### Variables
- Use noun phrases for objects
- Use descriptive names for important variables
- Use conventional names for temporary variables

### Constants
- Use UPPER_SNAKE_CASE for constants
- Make the purpose clear from the name

## Code Organization

### File Structure
- One class per file (when practical)
- Group related functions together
- Separate concerns into different modules/packages
- Use consistent directory structures

### Function Design  
- Keep functions small (generally under 20 lines)
- Single responsibility per function
- Minimize function parameters (ideally ≤ 3)
- Avoid deep nesting (prefer early returns)

**Good:**
```python
def process_order(order):
    if not order.is_valid():
        return None
    
    if not order.has_payment():
        return None
        
    return fulfill_order(order)
```

**Avoid:**
```python
def process_order(order):
    if order.is_valid():
        if order.has_payment():
            # deep nesting continues...
            return fulfill_order(order)
        else:
            return None
    else:
        return None
```

## Error Handling

- Fail fast and fail clearly
- Use specific exception types
- Provide meaningful error messages
- Handle errors at appropriate levels

```python
# Good: Specific and clear
class InvalidEmailError(ValueError):
    def __init__(self, email):
        super().__init__(f"Invalid email format: {email}")

def validate_email(email):
    if '@' not in email:
        raise InvalidEmailError(email)
```

## Comments and Documentation

**Write self-documenting code first. Documentation lives in the code.**

- Code readability reduces documentation needs  
- Comment the "why", not the "what"
- Keep comments up-to-date or remove them
- Use docstrings for public APIs
- Never use emoji in comments or documentation
- Avoid creating separate documentation files

**Good comments explain intent:**
```python
# Retry up to 3 times to handle transient network issues
def fetch_user_data(user_id, max_retries=3):
```

**Avoid obvious comments:**
```python
# Increment counter by 1
counter += 1
```

**Avoid emoji decorations:**
```python
# Bad: Don't do this
# ✅ Success! This function works!
# 🚀 Super fast implementation
# ⚠️ Warning: Check this

# Good: Clear, professional comments
# Returns None if validation fails
# Optimized for large datasets
# Validates input before processing
```

## Testing Principles

- Write tests that document expected behavior
- Test behavior, not implementation
- Keep tests simple and focused
- Use descriptive test names

```python
def test_should_reject_user_with_invalid_email():
    invalid_email = "not-an-email"
    with pytest.raises(InvalidEmailError):
        create_user(email=invalid_email)
```

## When to Apply These Guidelines

**Use this skill when:**
- Writing new code in any language
- Reviewing code (yours or others')
- Refactoring existing code
- Establishing team coding standards  
- Teaching code quality principles
- Deciding between multiple implementation approaches

**Key decision points:**
- Is this the simplest solution that meets the requirements?
- Does each component have a single, clear responsibility?
- Would a new team member understand this code?
- Am I building for current needs or speculative future needs?
- Am I creating unnecessary documentation files?
- Is my code simple enough to not need separate explanatory documents?

## Output Guidelines

**When generating or modifying code:**

1. **Minimize file generation:**
   - Create only essential code files
   - Avoid generating summary or changelog files
   - Don't create duplicate documentation

2. **No emoji in output:**
   - Code files: absolutely no emoji
   - Comments: use plain text only
   - Documentation: professional language only
   - Log messages: text-based indicators only

3. **Self-documenting code over documents:**
   - Prefer clear naming over explanatory comments
   - Prefer docstrings over separate API docs
   - Prefer type hints over type documentation

**Good output structure:**
```
project/
├── src/
│   ├── main.py          # Main code
│   └── utils.py         # Helper functions
├── tests/
│   └── test_main.py     # Tests
└── README.md            # One README only
```

**Avoid:**
```
project/
├── src/
│   ├── main.py
│   └── utils.py
├── docs/
│   ├── CHANGES.md       # Unnecessary
│   ├── SUMMARY.md       # Unnecessary
│   └── API_GUIDE.md     # Unnecessary
├── README.md
└── NOTES.md             # Unnecessary
```
