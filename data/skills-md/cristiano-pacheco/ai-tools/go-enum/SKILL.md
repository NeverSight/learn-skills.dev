---
name: go-enum
description: Generate Go enums following GO modular architecture conventions (string-based enums with validation, constructor, and String method). Use when creating type-safe string enumerations in internal/modules/<module>/enum/ or when user asks to create an enum, add an enum type, or define enum constants.
---

# Go Enum

Generate type-safe Go enums following GO modular architecture conventions.

## Pattern

Place enums in `internal/modules/<module>/enum/<name>_enum.go`.

Each enum file contains:
1. String constants for each enum value
2. Validation map for O(1) lookups
3. Enum struct type
4. Constructor with validation (`New<Type>Enum`)
5. `String()` method
6. Private validation function (`validate<Type>`)

**Note**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead. For enum files, the private `validate<Type>` function is acceptable because the enum struct is a simple value wrapper without complex methods.

## Example — Enum File

For an enum named "ContactType" with values "email" and "webhook" in the `monitor` module:

```go
package enum

import "github.com/cristiano-pacheco/pingo/internal/modules/monitor/errs"

const (
	ContactTypeEmail   = "email"
	ContactTypeWebhook = "webhook"
)

var validContactTypes = map[string]struct{}{
	ContactTypeEmail:   {},
	ContactTypeWebhook: {},
}

type ContactTypeEnum struct {
	value string
}

func NewContactTypeEnum(value string) (ContactTypeEnum, error) {
	if err := validateContactType(value); err != nil {
		return ContactTypeEnum{}, err
	}
	return ContactTypeEnum{value: value}, nil
}

func (e ContactTypeEnum) String() string {
	return e.value
}

func validateContactType(contactType string) error {
	if _, ok := validContactTypes[contactType]; !ok {
		return errs.ErrInvalidContactType
	}
	return nil
}
```

## Example — Error Entry

Errors live in `internal/modules/<module>/errs/errs.go` and use `errs.New` from the bricks package:

```go
package errs

import (
	"net/http"

	"github.com/cristiano-pacheco/bricks/pkg/errs"
)

var (
	ErrInvalidContactType = errs.New("MONITOR_01", "Invalid contact type", http.StatusBadRequest, nil)
)
```

`errs.New` signature: `errs.New(code string, message string, httpStatus int, metadata any)`

- **code**: `<MODULE>_<NN>` — uppercase module prefix, two-digit sequential number (e.g., `MONITOR_01`, `IDENTITY_25`). Read the existing errs.go to find the next available number.
- **message**: Sentence case, starting with uppercase (e.g., `"Invalid contact type"`). Keep it short and user-safe.
- **httpStatus**: Use `http.StatusBadRequest` for invalid enum values.
- **metadata**: Always `nil` for enum validation errors.

## Generation Steps

1. **Identify enum details**:
   - Enum name (e.g., `ContactType`, `UserStatus`, `PKCEMethod`)
   - Possible values (e.g., `["email", "webhook"]`, `["active", "inactive"]`)
   - Target module (e.g., `monitor`, `identity`)

2. **Add error to `internal/modules/<module>/errs/errs.go`**:
   - Read the file to find the next available sequential error code number
   - Add: `ErrInvalid<EnumName> = errs.New("<MODULE>_<NN>", "Invalid <enum name>", http.StatusBadRequest, nil)`
   - Ensure `net/http` and `github.com/cristiano-pacheco/bricks/pkg/errs` are imported

3. **Create the enum file** at `internal/modules/<module>/enum/<snake_case_name>_enum.go`:
   - Import: `github.com/cristiano-pacheco/pingo/internal/modules/<module>/errs`
   - Follow the structure above with all six components

## Naming Conventions

- **File**: `<snake_case>_enum.go` (e.g., `contact_type_enum.go`, `user_status_enum.go`)
- **Constants**: `<EnumName><Value>` (e.g., `ContactTypeEmail`, `UserStatusActive`)
- **Validation map**: `valid<EnumName>s` (unexported, plural, e.g., `validContactTypes`)
- **Struct**: `<EnumName>Enum` (e.g., `ContactTypeEnum`)
- **Constructor**: `New<EnumName>Enum(value string) (<EnumName>Enum, error)`
- **Validator**: `validate<EnumName>(value string) error` (unexported, singular)
- **Error**: `ErrInvalid<EnumName>` in `internal/modules/<module>/errs/errs.go`

## Implementation Checklist

- [ ] Read `internal/modules/<module>/errs/errs.go` to find the next sequential error code
- [ ] Add `ErrInvalid<EnumName>` to `internal/modules/<module>/errs/errs.go`
- [ ] Create `internal/modules/<module>/enum/<snake_case_name>_enum.go`
- [ ] Define all string constants
- [ ] Create validation map (`map[string]struct{}`) with all constants
- [ ] Define enum struct with private `value string` field
- [ ] Implement constructor `New<EnumName>Enum(value string) (<EnumName>Enum, error)`
- [ ] Implement `String() string` method
- [ ] Implement `validate<EnumName>(value string) error` private function

## Usage Pattern

```go
// Validate and wrap an input value
contactType, err := enum.NewContactTypeEnum(input)
if err != nil {
    return err
}
fmt.Println(contactType.String()) // "email"

// Use constants directly when value is known at compile time
const defaultType = enum.ContactTypeEmail
```

When finished the enum implementation, ensure to test the constructor with valid and invalid values to confirm validation works as expected.

Run `make lint` and `make nilaway` to ensure code quality and no nil pointer issues.