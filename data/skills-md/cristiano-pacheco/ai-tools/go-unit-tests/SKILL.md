---
name: go-unit-tests
description: Generate comprehensive Go unit tests following testify patterns and best practices. Use when creating or updating Go test files, writing test suites for structs with dependencies, testing standalone functions, working with mocks, or when asked to add test coverage for Go code.
---

# Go Unit Tests

Generate comprehensive Go unit tests following testify patterns and the Arrange-Act-Assert methodology.

## Before Writing Tests

Identify the following before writing any code:

1. **Pattern** — Use a test suite (Pattern 1) for structs with dependencies; use standalone functions (Pattern 2) for simple functions or value objects
2. **Dependencies** — Which dependencies need mocks; which can use real instances
3. **Test cases** — Happy path, error conditions, and edge cases

## Pattern 1: Test Suite (structs with dependencies)

Use `suite.Suite` from testify when the system under test is a struct with injected dependencies.

**Rules:**
- Suite struct holds `sut` (System Under Test) and mock fields
- `SetupTest()` runs before each test — use it to initialize mocks and the sut
- `SetupSuite()` + `TearDownSuite()` run once per suite — use only for expensive setup (e.g. generating RSA keys, creating temp files)
- Always use `_test` suffix for the package name
- For assertions: `s.Require().Error/NoError/ErrorIs` stops the test immediately on failure; `s.Equal/Empty/True/False` continues after failure — use `Require()` for preconditions and error checks, plain assertions for value comparisons
- Never call `.AssertExpectations(s.T())` — mockery v2 auto-registers cleanup when you pass `s.T()` to the mock constructor, so calling it manually is redundant

**Basic suite example:**

```go
package service_test

import (
	"testing"

	"github.com/example/project/internal/modules/identity/service"
	"github.com/stretchr/testify/suite"
)

type PasswordHasherServiceTestSuite struct {
	suite.Suite
	sut *service.PasswordHasherService
}

func (s *PasswordHasherServiceTestSuite) SetupTest() {
	s.sut = service.NewPasswordHasherService()
}

func TestPasswordHasherServiceSuite(t *testing.T) {
	suite.Run(t, new(PasswordHasherServiceTestSuite))
}

func (s *PasswordHasherServiceTestSuite) TestHash_ValidPassword_ReturnsHash() {
	// Arrange
	password := "SecureP@ssw0rd"

	// Act
	hash, err := s.sut.Hash(password)

	// Assert
	s.Require().NoError(err)
	s.NotEmpty(hash)
}

func (s *PasswordHasherServiceTestSuite) TestVerify_WrongPassword_ReturnsFalse() {
	// Arrange
	password := "SecureP@ssw0rd"
	hash, err := s.sut.Hash(password)
	s.Require().NoError(err)

	// Act
	ok, err := s.sut.Verify(hash, "WrongPassword1!")

	// Assert
	s.Require().NoError(err)
	s.False(ok)
}
```

**Suite with mocks example:**

```go
package user_test

import (
	"context"
	"errors"
	"testing"

	"github.com/example/project/internal/modules/identity/errs"
	"github.com/example/project/internal/modules/identity/usecase/user"
	"github.com/example/project/test/mocks"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"
)

type UserCreateUseCaseTestSuite struct {
	suite.Suite
	sut                *user.UserCreateUseCase
	userRepoMock       *mocks.MockUserRepository
	passwordHasherMock *mocks.MockPasswordHasher
	useCaseMetricsMock *mocks.MockUseCaseMetrics
}

func (s *UserCreateUseCaseTestSuite) SetupTest() {
	s.userRepoMock = mocks.NewMockUserRepository(s.T())
	s.passwordHasherMock = mocks.NewMockPasswordHasher(s.T())
	s.useCaseMetricsMock = mocks.NewMockUseCaseMetrics(s.T())

	s.sut = user.NewUserCreateUseCase(
		s.userRepoMock,
		s.passwordHasherMock,
		s.useCaseMetricsMock,
	)
}

func TestUserCreateUseCaseSuite(t *testing.T) {
	suite.Run(t, new(UserCreateUseCaseTestSuite))
}

func (s *UserCreateUseCaseTestSuite) TestExecute_ValidInput_CreatesUser() {
	// Arrange
	ctx := context.Background()
	input := user.UserCreateInput{
		Email:    "test@example.com",
		Password: "SecureP@ssw0rd",
	}

	s.userRepoMock.On("FindByEmail", mock.Anything, input.Email).
		Return(model.UserModel{}, errs.ErrRecordNotFound)
	s.passwordHasherMock.On("Hash", input.Password).Return([]byte("hash"), nil)
	s.userRepoMock.On("Create", mock.Anything, mock.AnythingOfType("model.UserModel")).
		Return(model.UserModel{ID: 1, Email: input.Email}, nil)
	s.useCaseMetricsMock.On("ObserveDuration", "user_create", mock.Anything).Maybe()
	s.useCaseMetricsMock.On("IncSuccess", "user_create").Maybe()

	// Act
	output, err := s.sut.Execute(ctx, input)

	// Assert
	s.Require().NoError(err)
	s.Equal(uint64(1), output.ID)
	s.Equal("test@example.com", output.Email)
}

func (s *UserCreateUseCaseTestSuite) TestExecute_DuplicateEmail_ReturnsError() {
	// Arrange
	ctx := context.Background()
	input := user.UserCreateInput{
		Email:    "existing@example.com",
		Password: "SecureP@ssw0rd",
	}

	s.userRepoMock.On("FindByEmail", mock.Anything, input.Email).
		Return(model.UserModel{ID: 1}, nil)
	s.useCaseMetricsMock.On("ObserveDuration", "user_create", mock.Anything).Maybe()
	s.useCaseMetricsMock.On("IncError", "user_create").Maybe()

	// Act
	output, err := s.sut.Execute(ctx, input)

	// Assert
	s.Require().ErrorIs(err, errs.ErrDuplicateEmail)
	s.Equal(uint64(0), output.ID)
}
```

**Suite with one-time setup example:**

Use `SetupSuite` + `TearDownSuite` when initialization is expensive and safe to share across all tests (e.g. generating RSA keys, creating temp directories).

```go
type JWTServiceTestSuite struct {
	suite.Suite
	sut    *service.JWTService
	keyDir string
}

func (s *JWTServiceTestSuite) SetupSuite() {
	dir, err := os.MkdirTemp("", "jwt_test_keys")
	s.Require().NoError(err)
	s.keyDir = dir
	// ... generate keys, configure sut ...
}

func (s *JWTServiceTestSuite) TearDownSuite() {
	if s.keyDir != "" {
		_ = os.RemoveAll(s.keyDir)
	}
}
```

## Pattern 2: Standalone Functions

Use individual top-level test functions for standalone functions, value objects, validators, or enums. No suite needed.

**Rules:**
- One top-level `TestFunctionName_Scenario_ExpectedResult` per scenario
- Use `require.Error/NoError/ErrorIs` for error checks; `assert.Equal/Empty/True` for value comparisons
- Use table-driven tests (`tests []struct{ ... }` + `t.Run`) when testing the same function with many similar inputs (e.g. validating multiple valid/invalid values)

**Single-scenario example:**

```go
package validator_test

import (
	"testing"

	"github.com/example/project/internal/modules/identity/errs"
	"github.com/example/project/internal/modules/identity/validator"
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
	assert.ErrorIs(t, err, errs.ErrPasswordPolicyViolation)
}
```

**Table-driven example:**

```go
package enum_test

import (
	"testing"

	"github.com/example/project/internal/modules/identity/enum"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewUserStatusEnum_ValidValues(t *testing.T) {
	tests := []struct {
		name  string
		value string
	}{
		{"pending_verification", enum.UserStatusPendingVerification},
		{"active", enum.UserStatusActive},
		{"locked", enum.UserStatusLocked},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Act
			e, err := enum.NewUserStatusEnum(tt.value)

			// Assert
			require.NoError(t, err)
			assert.Equal(t, tt.value, e.String())
		})
	}
}

func TestNewUserStatusEnum_InvalidValue_ReturnsError(t *testing.T) {
	// Arrange
	invalidValue := "invalid_status"

	// Act
	e, err := enum.NewUserStatusEnum(invalidValue)

	// Assert
	require.ErrorIs(t, err, errs.ErrInvalidUserStatus)
	assert.Equal(t, enum.UserStatusEnum{}, e)
}
```

## Mock Rules

- Mocks live in `test/mocks/` and are generated by mockery v2 or v3 — never write them by hand
- Import as `"github.com/example/project/test/mocks"` — no alias needed
- Always pass `s.T()` to the mock constructor: `mocks.NewMockUserRepository(s.T())`
- Always pass `mock.Anything` for `context.Context` parameters
- Use `mock.AnythingOfType("pkg.TypeName")` when you need to match by type without checking exact value
- Use `.Maybe()` on mock expectations that may or may not be called (e.g. metrics, logging decorators)

## Arrange-Act-Assert

Every test must have explicit `// Arrange`, `// Act`, `// Assert` comments. Mock expectations (`.On(...)`) belong in the Arrange block.

```go
// Arrange
input := "test"
s.repoMock.On("Find", mock.Anything, input).Return(result, nil)

// Act
output, err := s.sut.Execute(ctx, input)

// Assert
s.Require().NoError(err)
s.Equal("expected", output.Name)
```

## Code Style

- **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
- Never use inline struct literals in assertions — always assign to a variable first
- Maximum 120 characters per line
- Test function names must describe what is being tested: `TestMethod_Scenario_ExpectedOutcome`

## Completion

before completeing the tests run `make lint` to verify that the code follows the project's style guidelines.

When tests are complete, respond with: **Tests Done, Oh Yeah!**
