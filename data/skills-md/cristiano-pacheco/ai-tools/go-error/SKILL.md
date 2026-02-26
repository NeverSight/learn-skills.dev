---
name: go-error
description: Generate custom Go errors following GO modular architecture conventions using bricks errs.New(code, message, httpStatus, details). Use when creating new domain errors, extending internal/modules/<module>/errs/errs.go, or standardizing error codes/messages/statuses across modules.
---

# Go Error

Generate typed custom errors for module-level `errs` packages.

## Pattern

Place errors in:

`internal/modules/<module>/errs/errs.go`

Each module error file follows:

1. `package errs`
2. Imports:
   - `net/http`
   - `brickserrs "github.com/cristiano-pacheco/bricks/pkg/errs"`
3. `var (...)` block with exported error variables
4. Error creation via:
   - `brickserrs.New("<MODULE>_<NN>", "<message>", http.<Status>, nil)`
5. Optional helper constructors for validation errors that carry field-level details

## Example Structure

```go
package errs

import (
	"net/http"

	brickserrs "github.com/cristiano-pacheco/bricks/pkg/errs"
)

var (
	// ErrProfileValidationFailed is returned when profile validation fails.
	ErrProfileValidationFailed = brickserrs.New(
		"PROFILE_01",
		"profile validation failed",
		http.StatusBadRequest,
		nil,
	)
	// ErrProfileNotFound is returned when the profile is not found.
	ErrProfileNotFound = brickserrs.New("PROFILE_02", "profile not found", http.StatusNotFound, nil)
)

// NewProfileValidationError returns a structured validation error with field-level details.
func NewProfileValidationError(details []brickserrs.Detail) *brickserrs.Error {
	return brickserrs.New(
		ErrProfileValidationFailed.Code,
		ErrProfileValidationFailed.Message,
		ErrProfileValidationFailed.Status,
		details,
	)
}
```

## Generation Steps

1. **Identify error details**:
   - Target module (e.g., `catalog`, `profile`, `ai`, `export`)
   - Error variable name (`ErrProfileNotFound`)
   - Lowercase message (`"profile not found"`)
   - HTTP status (`http.StatusNotFound`)

2. **Find the next code**:
   - Open `internal/modules/<module>/errs/errs.go`
   - Extract existing codes for that module prefix
   - Allocate the next available sequential code:
     - Single digits are zero-padded: `CATALOG_01`, `CATALOG_02`, ..., `CATALOG_09`
     - Double digits are not padded: `CATALOG_10`, `CATALOG_11`, ...
   - Keep code uniqueness inside the module

3. **Add the new error**:
   - Insert into the module `var (...)` block
   - Keep domain-group ordering used by the file
   - Add a short doc comment when comments are already present in the file

4. **Add a helper constructor if needed**:
   - When the error is a validation error that carries field-level details, add a `NewXxxValidationError(details []brickserrs.Detail) *brickserrs.Error` function
   - Reuse the pre-defined variable's `.Code`, `.Message`, and `.Status` fields

5. **Validate usage path**:
   - Ensure new/updated usecases, validators, handlers, or enum constructors return the new typed error
   - Do not return raw `errors.New(...)` from business flows when a typed module error exists

6. **Update translations (mandatory)**:
   - Every new custom error must add a translation entry in `locales/en.json` under the `"errors"` key
   - Use the error code as key and a properly capitalized, user-facing sentence as value: `"PROFILE_02": "Profile not found"`
   - If additional locale files exist (for example `locales/pt_BR.json`), add the same key there too
   - Keep translation keys and structure consistent across all locale files
   - Do not merge a new custom error without the corresponding locale updates

## Naming Conventions

- **Variable**: `Err` + clear domain phrase in PascalCase
  - Example: `ErrProfileNotFound`, `ErrAIGenerationFailed`
- **Code**: `<MODULE>_<NN>`
  - `CATALOG_09`, `EXPORT_15`, `AI_07`
  - Always at least 2 digits; single digits are zero-padded
- **Message**:
  - All lowercase in `brickserrs.New()` — the locale file (`locales/en.json`) provides the user-facing capitalized form
  - Short and specific, no trailing punctuation
  - Examples: `"profile not found"`, `"invalid prompt type"`, `"ai provider unavailable"`
- **HTTP status**:
  - Validation errors: `http.StatusBadRequest`
  - Auth failures: `http.StatusUnauthorized` / `http.StatusForbidden`
  - Missing resources: `http.StatusNotFound`
  - Conflicts: `http.StatusConflict`
  - Rate limit: `http.StatusTooManyRequests`
  - Upstream/AI failures: `http.StatusBadGateway`
  - Capacity/availability: `http.StatusServiceUnavailable`
  - Infra/internal failures: `http.StatusInternalServerError`

## Implementation Checklist

- [ ] Open target `internal/modules/<module>/errs/errs.go`
- [ ] Compute next unique module code (zero-padded 2-digit format)
- [ ] Add exported `Err...` variable with `brickserrs.New(...)`
- [ ] Use all-lowercase message string
- [ ] Match existing domain-group ordering style
- [ ] Ensure message and status align with domain behavior
- [ ] Add `NewXxxValidationError(details []brickserrs.Detail)` helper if it is a validation error
- [ ] Replace raw error returns in calling code with typed `errs.Err...` where applicable
- [ ] Add translation for the new error in `locales/en.json` under `"errors"` with proper sentence-case value
- [ ] Add the same translation key in every other existing locale file (e.g., `locales/pt_BR.json`)
- [ ] Run `make lint` to catch style and static analysis issues
- [ ] Run `make nilaway` to ensure no nil pointer dereferences are introduced

## Usage Pattern

```go
if input.Phone == "" {
	return errs.ErrPhoneNumberRequired
}

if profile == nil {
	return errs.ErrProfileNotFound
}
```

## Critical Rules

- **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
- Do not create a new error package; use module-local `internal/modules/<module>/errs`
- Do not duplicate codes within the same module
- Do not return persistence or infrastructure-specific raw errors to transport when a typed domain error exists
- Keep error messages stable once exposed, unless migration/compatibility impact is accepted
- Every new custom error requires locale entries in `locales/en.json` and all other existing locale files
- Messages in `brickserrs.New()` are always lowercase; user-facing capitalization lives in the locale file
