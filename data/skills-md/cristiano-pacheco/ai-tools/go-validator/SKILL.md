---
name: go-validator
description: Generate Go validator implementations following GO modular architecture conventions (interface-first design, Fx DI, stateless validation). Use when creating validation logic in internal/modules/<module>/validator/ - password validation, email validation, input sanitization, business rule validation, or any domain validation that encapsulates validation rules and returns typed errors.
---

# Go Validator

Generate validator files for GO modular architecture conventions.

## Two-File Pattern

Every validator requires two files:

1. **Port interface**: `internal/modules/<module>/ports/<validator_name>_validator.go`
2. **Validator implementation**: `internal/modules/<module>/validator/<validator_name>_validator.go`

### Port File Structure

The port file contains only the interface definition with its documentation comment.

**Example structure:**
```go
package ports

// PasswordValidator validates password strength according to security policies.
type PasswordValidator interface {
	Validate(password string) error
}
```

### Validator File Structure

The validator implementation file follows this order:

1. **Package declaration and imports**
2. **Constants** - validation rules, thresholds, limits
3. **Struct definition** - the validator implementation struct
4. **Interface assertion** - compile-time check with `var _ ports.XxxValidator = (*XxxValidator)(nil)`
5. **Constructor** - `NewXxxValidator` function
6. **Methods** - validation methods (e.g., `Validate`)

**Example structure:**
```go
package validator

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

// 2. Constants
const (
	minLength = 8
	maxLength = 128
)

// 3. Struct definition
type PasswordValidator struct{}

// 4. Interface assertion
var _ ports.PasswordValidator = (*PasswordValidator)(nil)

// 5. Constructor
func NewPasswordValidator() *PasswordValidator {
	return &PasswordValidator{}
}

// 6. Methods
func (v *PasswordValidator) Validate(password string) error {
	// validation logic
	return nil
}
```

## Port Interface Structure

**Location**: `internal/modules/<module>/ports/<validator_name>_validator.go`

```go
package ports

// PasswordValidator validates password strength according to security policies.
type PasswordValidator interface {
	Validate(password string) error
}
```

## Validator Variants

### Stateless validator (no dependencies)

Most validators are stateless utilities with no external dependencies.

```go
package validator

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

type EmailValidator struct{}

var _ ports.EmailValidator = (*EmailValidator)(nil)

func NewEmailValidator() *EmailValidator {
	return &EmailValidator{}
}

func (v *EmailValidator) Validate(email string) error {
	// Validation logic
	return nil
}
```

### Stateful validator (with dependencies)

Use when validation requires external data or configuration.

```go
package validator

import (
	"context"

	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

type UsernameValidator struct {
	userRepo ports.UserRepository
	minLen   int
	maxLen   int
}

var _ ports.UsernameValidator = (*UsernameValidator)(nil)

func NewUsernameValidator(
	userRepo ports.UserRepository,
	minLen int,
	maxLen int,
) *UsernameValidator {
	return &UsernameValidator{
		userRepo: userRepo,
		minLen:   minLen,
		maxLen:   maxLen,
	}
}

func (v *UsernameValidator) Validate(ctx context.Context, username string) error {
	if len(username) < v.minLen {
		return errs.ErrUsernameTooShort
	}

	// Check uniqueness using repository
	exists, err := v.userRepo.ExistsByUsername(ctx, username)
	if err != nil {
		return err
	}
	if exists {
		return errs.ErrUsernameAlreadyExists
	}

	return nil
}
```

### Multi-field validator

Use when validation involves multiple related fields.

Port interface:

```go
package ports

// RegistrationValidator validates all fields for user registration.
type RegistrationValidator interface {
	ValidateEmail(email string) error
	ValidatePassword(password string) error
	ValidatePasswordMatch(password, confirmPassword string) error
}
```

Implementation:

```go
package validator

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

type RegistrationValidator struct{}

var _ ports.RegistrationValidator = (*RegistrationValidator)(nil)

func NewRegistrationValidator() *RegistrationValidator {
	return &RegistrationValidator{}
}

func (v *RegistrationValidator) ValidateEmail(email string) error {
	// Email validation logic
	return nil
}

func (v *RegistrationValidator) ValidatePassword(password string) error {
	// Password validation logic
	return nil
}

func (v *RegistrationValidator) ValidatePasswordMatch(password, confirmPassword string) error {
	if password != confirmPassword {
		return errs.ErrPasswordMismatch
	}
	return nil
}
```

## Validation Constants

Define validation rules as constants at the package level for clarity and maintainability.

```go
const (
	minPasswordLength = 8
	maxPasswordLength = 128
	minUsernameLength = 3
	maxUsernameLength = 32
)
```

## Error Handling

Validators MUST return typed domain errors from the module's `errs` package.
When adding new custom errors, translations are mandatory in locale files.

```go
// In internal/modules/<module>/errs/errs.go
var (
	ErrPasswordTooShort         = errors.New("password must be at least 8 characters")
	ErrPasswordMissingUppercase = errors.New("password must contain at least one uppercase letter")
	ErrPasswordMissingLowercase = errors.New("password must contain at least one lowercase letter")
	ErrPasswordMissingDigit     = errors.New("password must contain at least one digit")
	ErrPasswordMissingSpecial   = errors.New("password must contain at least one special character")
)
```

For every new custom error added to `internal/modules/<module>/errs/errs.go`:
- Add the translation key to `locales/en.json`
- Add the same translation key to every other existing locale file (e.g., `locales/pt_BR.json`)

## Context Usage

Validators that perform I/O operations (database lookups, API calls) MUST accept `context.Context` as the first parameter.

```go
// Stateless validator - no context needed
func (v *PasswordValidator) Validate(password string) error

// Stateful validator with I/O - context required
func (v *UsernameValidator) Validate(ctx context.Context, username string) error
```

## Naming

- Port interface: `XxxValidator` (in `ports` package)
- Implementation struct: `XxxValidator` (in `validator` package, same name — disambiguated by package)
- Constructor: `NewXxxValidator`, returns a pointer of the struct implementation
- Validation method: `Validate` for single-purpose validators, or descriptive names for multi-purpose validators

## Fx Wiring

Add to `internal/modules/<module>/fx.go`:

**Stateless validator:**
```go
fx.Provide(
	fx.Annotate(
		validator.NewPasswordValidator,
		fx.As(new(ports.PasswordValidator)),
	),
),
```

**Stateful validator with dependencies:**
```go
fx.Provide(
	fx.Annotate(
		validator.NewUsernameValidator,
		fx.As(new(ports.UsernameValidator)),
	),
),
```

The stateful validator's dependencies (e.g., `ports.UserRepository`) are automatically injected by Fx. Constructor parameters that are primitive types (e.g., `minLen`, `maxLen`) should be provided via configuration or fx.Supply.

## Dependencies

Validators depend on interfaces only. Common dependencies:

- `ports.XxxRepository` — for uniqueness checks or data lookups
- `ports.XxxService` — for external validation services
- Configuration values — passed as constructor parameters

## Testing

Validators MUST have comprehensive unit tests covering:

1. Valid input passes validation
2. Each invalid condition returns the correct error
3. Edge cases (empty strings, boundary values, special characters)

Test file location: `internal/modules/<module>/validator/<validator_name>_validator_test.go`

```go
package validator_test

import (
	"testing"

	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/validator"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestPasswordValidator_ValidPassword_Passes(t *testing.T) {
	// Arrange
	v := validator.NewPasswordValidator()

	// Act
	err := v.Validate("SecureP@ssw0rd")

	// Assert
	require.NoError(t, err)
}

func TestPasswordValidator_TooShort_ReturnsError(t *testing.T) {
	// Arrange
	v := validator.NewPasswordValidator()

	// Act
	err := v.Validate("Ab1!")

	// Assert
	require.Error(t, err)
	assert.ErrorIs(t, err, errs.ErrPasswordTooShort)
}
```

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Two files**: Port interface in `ports/`, implementation in `validator/`
2. **Interface in ports**: Interface lives in `ports/<name>_validator.go`
3. **Interface assertion**: Add `var _ ports.XxxValidator = (*XxxValidator)(nil)` below the struct
4. **Constructor**: MUST return pointer `*XxxValidator`
5. **Stateless by default**: Only add dependencies when validation requires external data
6. **Context when needed**: Accept `context.Context` only for validators performing I/O
7. **Typed errors**: Return domain errors from module's `errs` package
8. **Error translations**: Every new custom error must have entries in `locales/en.json` and all other existing locale files
9. **Constants**: Define validation rules as package-level constants
10. **No comments on implementations**: Do not add redundant comments above methods in the implementations
11. **Add detailed comment on interfaces**: Provide comprehensive comments on the port interfaces to describe their purpose and validation rules
12. **Comprehensive tests**: Test valid cases and all invalid conditions

## Workflow

1. Create port interface in `ports/<name>_validator.go`
2. Create validator implementation in `validator/<name>_validator.go`
3. Define validation constants
4. Add typed errors to module's `errs/errs.go` if needed
5. Add translations for each new custom error in `locales/en.json` and all other existing locale files
6. Create comprehensive unit tests in `validator/<name>_validator_test.go`
7. Add Fx wiring to module's `fx.go`
8. Run `make test` to verify tests pass
9. Run `make lint` to verify code quality
10. Run `make nilaway` for static analysis
