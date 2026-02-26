---
name: go-integration-tests
description: Generate comprehensive Go integration tests using testify suite patterns with real database and infrastructure dependencies. Use when creating or updating integration test files, testing use cases against real databases, verifying end-to-end flows, or when asked to add integration test coverage for Go code.
---

# Go Integration Tests

Generate comprehensive Go integration tests using testify suite patterns with real database and infrastructure dependencies.

## Planning Phase

Before writing tests, identify:

1. **Test Location**: Tests go in `test/integration/` mirroring the source path from `internal/`
   - Example: `internal/modules/identity/usecase/user/user_register_usecase.go` → `test/integration/modules/identity/usecase/user/user_register_usecase_test.go`
2. **Dependencies**: Identify real dependencies (database, redis) vs mocked ones (email, external APIs, metrics)
3. **Test Cases**: Define scenarios covering happy paths, edge cases, error conditions, and DB state verification
4. **Naming**: Use descriptive names: `TestExecute_ValidInput_ReturnsUser`, `TestExecute_DuplicateEmail_ReturnsError`

## Implementation Patterns

### Pattern: Integration Test Suite

Use `suite.Suite` from testify with itestkit for containerized infrastructure.

**Key Rules:**
- Create suite struct with `sut` (System Under Test), `kit` (ITestKit), and `db` fields
- Implement `SetupSuite` to start containers and run migrations (runs once per suite)
- Implement `TearDownSuite` to stop containers (runs once per suite)
- Implement `SetupTest` to truncate tables, create fresh mock objects, and reinitialize sut (runs before each test)
- Use `//go:build integration` build tag at the top of the file
- Always use `_test` suffix for package name
- Use `suite` methods for assertions (e.g., `s.Equal(...)`, `s.NotZero(...)`)
- Use `s.Require()` for fatal assertions (e.g., `s.Require().NoError(err)`, `s.Require().ErrorIs(...)`)
- Never use `.AssertExpectations(s.T())` — testify does this automatically

**Full Example:**

```go
//go:build integration

package user_test

import (
	"context"
	"testing"
	"time"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"

	"github.com/cristiano-pacheco/bricks/pkg/itestkit"
	"github.com/cristiano-pacheco/bricks/pkg/validator"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/model"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/repository"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/usecase/user"
	identity_validator "github.com/cristiano-pacheco/pingo/internal/modules/identity/validator"
	"github.com/cristiano-pacheco/pingo/internal/shared/config"
	"github.com/cristiano-pacheco/pingo/internal/shared/database"
	"github.com/cristiano-pacheco/pingo/test/mocks"
)

// emailRecord captures emails sent during tests for assertion purposes.
type emailRecord struct {
	to      string
	subject string
	body    string
}

func TestMain(m *testing.M) {
	itestkit.TestMain(m)
}

type UserRegisterUseCaseTestSuite struct {
	suite.Suite
	kit            *itestkit.ITestKit
	db             *database.PingoDB
	sut            *user.UserRegisterUseCase
	emailSender    *mocks.MockEmailSender
	tokenGenerator *mocks.MockTokenGenerator
	cfg            config.Config
	sentEmails     []emailRecord
}

func TestUserRegisterUseCaseSuite(t *testing.T) {
	suite.Run(t, new(UserRegisterUseCaseTestSuite))
}

func (s *UserRegisterUseCaseTestSuite) SetupSuite() {
	s.kit = itestkit.New(itestkit.Config{
		PostgresImage:  "postgres:16-alpine",
		RedisImage:     "redis:7-alpine",
		MigrationsPath: "file://migrations",
		Database:       "pingo_test",
		User:           "pingo_test",
		Password:       "pingo_test",
	})

	err := s.kit.StartPostgres()
	s.Require().NoError(err)

	err = s.kit.RunMigrations()
	s.Require().NoError(err)

	s.db = &database.PingoDB{DB: s.kit.DB()}
}

func (s *UserRegisterUseCaseTestSuite) TearDownSuite() {
	if s.kit != nil {
		s.kit.StopPostgres()
	}
}

// SetupTest runs before every test. Create fresh mock objects here and reset
// any captured side-effect state. Then call createTestUseCase to wire everything up.
func (s *UserRegisterUseCaseTestSuite) SetupTest() {
	s.kit.TruncateTables(s.T())

	s.sentEmails = nil
	s.emailSender = mocks.NewMockEmailSender(s.T())
	s.tokenGenerator = mocks.NewMockTokenGenerator(s.T())
	s.cfg = s.createTestConfig(true)
	s.sut = s.createTestUseCase()
}

// createTestConfig accepts feature flags so individual tests can reconfigure the SUT.
func (s *UserRegisterUseCaseTestSuite) createTestConfig(registrationEnabled bool) config.Config {
	return config.Config{
		App: config.AppConfig{
			BaseURL: "http://test.example.com",
			Identity: config.IdentityConfig{
				Registration: config.RegistrationConfig{
					Enabled: registrationEnabled,
				},
			},
		},
	}
}

// createTestUseCase wires all dependencies and sets up mock expectations.
// Infrastructure mocks (metrics, logger) use .Maybe() so they satisfy calls
// without requiring them. Domain mocks (emailSender, tokenGenerator) use .Run()
// callbacks to capture side effects for later assertion.
func (s *UserRegisterUseCaseTestSuite) createTestUseCase() *user.UserRegisterUseCase {
	log := new(mocks.MockLogger)

	v, err := validator.New()
	s.Require().NoError(err)

	pwValidator := identity_validator.NewPasswordValidator()
	pwHasher := service.NewPasswordHasherService(s.cfg)

	useCaseMetrics := new(mocks.MockUseCaseMetrics)
	useCaseMetrics.On("ObserveDuration", mock.Anything, mock.Anything).Return().Maybe()
	useCaseMetrics.On("IncrementCount", mock.Anything).Return().Maybe()
	useCaseMetrics.On("IncSuccess", mock.Anything).Return().Maybe()
	useCaseMetrics.On("IncError", mock.Anything).Return().Maybe()

	s.tokenGenerator.On("GenerateToken").Return("test-token-12345", nil).Maybe()
	s.tokenGenerator.On("HashToken", mock.Anything).Return(func(token string) []byte {
		hash := make([]byte, len(token))
		copy(hash, token)
		return hash
	}).Maybe()

	// Capture emails for later assertion in test methods.
	s.emailSender.On("Send", mock.Anything, mock.Anything, mock.Anything, mock.Anything).
		Run(func(args mock.Arguments) {
			s.sentEmails = append(s.sentEmails, emailRecord{
				to:      args.String(1),
				subject: args.String(2),
				body:    args.String(3),
			})
		}).Return(nil).Maybe()

	userRepo := repository.NewUserRepository(s.db)
	tokenRepo := repository.NewIdentityTokenRepository(s.db)

	return user.NewUserRegisterUseCase(
		userRepo,
		tokenRepo,
		pwHasher,
		pwValidator,
		s.tokenGenerator,
		s.emailSender,
		v,
		s.cfg,
		log,
		useCaseMetrics,
	)
}

// findSentEmail is a suite helper for looking up captured emails by recipient.
func (s *UserRegisterUseCaseTestSuite) findSentEmail(email string) *emailRecord {
	for i := range s.sentEmails {
		if s.sentEmails[i].to == email {
			return &s.sentEmails[i]
		}
	}
	return nil
}

func (s *UserRegisterUseCaseTestSuite) TestExecute_ValidInput_ReturnsUser() {
	// Arrange
	ctx := context.Background()
	input := user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Password123!",
		FirstName: "John",
		LastName:  "Doe",
	}

	// Act
	output, err := s.sut.Execute(ctx, input)

	// Assert — output fields
	s.Require().NoError(err)
	s.NotZero(output.ID)
	s.Equal(input.Email, output.Email)
	s.Equal(input.FirstName, output.FirstName)
	s.Equal(input.LastName, output.LastName)
	s.Equal("pending_verification", output.Status)

	// Assert — DB state
	var savedUser model.UserModel
	err = s.db.DB.Where("id = ?", output.ID).First(&savedUser).Error
	s.Require().NoError(err)
	s.Equal(input.Email, savedUser.Email)
	s.Equal(input.FirstName, savedUser.FirstName)
	s.Equal(input.LastName, savedUser.LastName)
	s.NotEmpty(savedUser.PasswordHash)
	s.NotZero(savedUser.CreatedAt)
	s.NotZero(savedUser.UpdatedAt)

	// Assert — token persisted
	var savedToken model.IdentityTokenModel
	err = s.db.DB.Where("user_id = ? AND token_type = ?", output.ID, "email_verification").
		First(&savedToken).Error
	s.Require().NoError(err)
	s.True(savedToken.ExpiresAt.After(time.Now()))

	// Assert — email side effect
	email := s.findSentEmail(input.Email)
	s.Require().NotNil(email)
	s.Equal("Verify your email", email.subject)
	s.Contains(email.body, "test-token-12345")
}

func (s *UserRegisterUseCaseTestSuite) TestExecute_DuplicateEmail_ReturnsError() {
	// Arrange
	ctx := context.Background()
	input := user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Password123!",
		FirstName: "John",
		LastName:  "Doe",
	}

	// Act - First registration succeeds
	output1, err := s.sut.Execute(ctx, input)
	s.Require().NoError(err)
	s.NotZero(output1.ID)
	s.sentEmails = nil

	// Act - Second registration with same email
	_, err = s.sut.Execute(ctx, user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Different456!",
		FirstName: "Jane",
		LastName:  "Smith",
	})

	// Assert
	s.Require().Error(err)
	s.ErrorIs(err, errs.ErrDuplicateEmail)

	var count int64
	s.db.DB.Model(&model.UserModel{}).Where("email = ?", input.Email).Count(&count)
	s.Equal(int64(1), count)

	s.Nil(s.findSentEmail(input.Email))
}

func (s *UserRegisterUseCaseTestSuite) TestExecute_RegistrationDisabled_ReturnsError() {
	// Arrange - recreate sut with registration disabled
	s.cfg = s.createTestConfig(false)
	s.sut = s.createTestUseCase()
	ctx := context.Background()
	input := user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Password123!",
		FirstName: "John",
		LastName:  "Doe",
	}

	// Act
	_, err := s.sut.Execute(ctx, input)

	// Assert
	s.Require().Error(err)
	s.ErrorIs(err, errs.ErrRegistrationDisabled)

	var count int64
	s.db.DB.Model(&model.UserModel{}).Where("email = ?", input.Email).Count(&count)
	s.Equal(int64(0), count)

	s.Nil(s.findSentEmail(input.Email))
}
```

### Mock Rules for Integration Tests

**What to mock vs. what to use for real:**
- **Real**: database (via itestkit), Redis (via itestkit), any local service
- **Mock**: email/SMS senders, external HTTP APIs, token generators, metrics, logger

**Mock setup placement:**
- Create mock objects in `SetupTest` (fresh instance per test)
- Set `.On(...)` expectations inside `createTestUseCase`
- Use `.Maybe()` on infrastructure mocks (logger, metrics) — they may or may not be called
- Use `.Run()` callbacks on domain mocks (emailSender, tokenGenerator) to capture side effects for later assertion
- Always pass `mock.Anything` for context parameters

**Side-effect capture pattern** — when you need to assert on things like emails sent:

```go
// 1. Define a record type at the top of the file
type emailRecord struct {
	to      string
	subject string
	body    string
}

// 2. Add a slice field to the suite and a helper method
type MyTestSuite struct {
	suite.Suite
	sentEmails []emailRecord
	// ...
}

func (s *MyTestSuite) findSentEmail(to string) *emailRecord {
	for i := range s.sentEmails {
		if s.sentEmails[i].to == to {
			return &s.sentEmails[i]
		}
	}
	return nil
}

// 3. Reset and capture in SetupTest / createTestUseCase
func (s *MyTestSuite) SetupTest() {
	s.sentEmails = nil
	// ...
}

// In createTestUseCase:
s.emailSender.On("Send", mock.Anything, mock.Anything, mock.Anything, mock.Anything).
	Run(func(args mock.Arguments) {
		s.sentEmails = append(s.sentEmails, emailRecord{
			to:      args.String(1),
			subject: args.String(2),
			body:    args.String(3),
		})
	}).Return(nil).Maybe()
```

### Table-Driven Subtests

Use `s.Run()` when testing the same behavior with multiple inputs:

```go
func (s *UserRegisterUseCaseTestSuite) TestExecute_InvalidPassword_ReturnsError() {
	// Arrange
	ctx := context.Background()
	testCases := []struct {
		name     string
		email    string
		password string
	}{
		{"too short", "tooshort@example.com", "Short1!"},
		{"no uppercase", "nouppercase@example.com", "lowercase123!"},
		{"no digit", "nodigit@example.com", "NoDigitsHere!"},
	}

	for _, tc := range testCases {
		s.Run(tc.name, func() {
			input := user.UserRegisterInput{
				Email:     tc.email,
				Password:  tc.password,
				FirstName: "John",
				LastName:  "Doe",
			}

			// Act
			_, err := s.sut.Execute(ctx, input)

			// Assert
			s.Require().Error(err)
			s.ErrorIs(err, errs.ErrPasswordPolicyViolation)

			var count int64
			s.db.DB.Model(&model.UserModel{}).Where("email = ?", tc.email).Count(&count)
			s.Equal(int64(0), count)
		})
	}
}
```

## Test Structure Requirements

### (CRITICAL) Arrange-Act-Assert Pattern

Every test must follow AAA with explicit comments:

```go
// Arrange
// Act
// Assert
```

For multi-step tests (e.g., set up data then test), label each step clearly:

```go
// Act - First registration succeeds
// Assert - First registration succeeds
// Act - Second registration with same email
// Assert - Second registration fails
```

### Assertion depth

Always verify more than just the return value. Assert:
1. **Output fields** — all fields returned by the use case
2. **DB state** — query the database and verify the persisted record
3. **Side effects** — emails sent, tokens created, counts correct
4. **Negative state** — on error paths, verify nothing was persisted and no emails sent

### Code Style

- **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
- Maximum 120 characters per line
- Test names clearly state what is tested and what is expected
- Use inline struct slices for table-driven test cases (standard Go pattern)
- Add comments before complex assertions to explain what is being verified

## Test File Location

Integration tests mirror the source structure under `test/integration/`:

| Source File | Integration Test File |
|-------------|----------------------|
| `internal/modules/identity/usecase/user/user_register_usecase.go` | `test/integration/modules/identity/usecase/user/user_register_usecase_test.go` |
| `internal/modules/monitor/usecase/metric_usecase.go` | `test/integration/modules/monitor/usecase/metric_usecase_test.go` |

## Running Integration Tests

```bash
# Run all integration tests
make test-integration
```

## Completion

When tests are complete, respond with: **Integration Tests Done, Oh Yeah!**
