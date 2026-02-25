---
name: java-test-generator
description: |
  Generate comprehensive JUnit 5 test cases for Java code with proper mocking and coverage.
  Use when writing tests, creating unit tests, generating test cases, adding JUnit tests,
  setting up Mockito mocks, writing parameterized tests, or achieving test coverage.
  Works with .java files, generates test classes following naming conventions,
  includes edge cases, boundary conditions, and uses Arrange-Act-Assert pattern.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Java Test Generator

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Testing Best Practices](#testing-best-practices)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Generates comprehensive, well-structured JUnit 5 test cases for Java code with proper mocking using Mockito, edge case coverage, parameterized tests, and adherence to testing best practices.

## When to Use

Use this skill when you need to:
- Generate JUnit 5 test cases for Java classes
- Create unit tests with Mockito mocking
- Write parameterized tests for multiple input scenarios
- Add test coverage for new or existing code
- Test service layers with dependency mocking
- Generate tests following Arrange-Act-Assert pattern
- Create tests for edge cases and boundary conditions
- Test exception handling scenarios
- Verify mock interactions with Mockito
- Generate tests for Spring Boot components
- Achieve high test coverage (>80%)
- Bootstrap test suites for new features

## Quick Start
Generate tests for any Java class instantly:

```bash
# Generate tests for a service class
Generate tests for UserService.java

# Generate tests for multiple classes
Generate tests for all classes in src/main/java/com/example/service/
```

## Instructions

### Step 1: Analyze Source Code
Read the target Java class and understand:
- Class purpose and responsibilities
- Public methods that need testing
- Dependencies (fields, constructor parameters)
- Return types and exception handling
- Business logic and edge cases
- Validation logic

Use Grep to find related classes if context is needed:
```bash
grep "class UserService" src/main/java/**/*.java
```

### Step 2: Identify Test Scenarios
For each public method, identify:

**Happy Path Tests:**
- Valid inputs producing expected outputs
- Typical use cases

**Edge Cases:**
- Boundary values (min, max, zero, empty)
- Null inputs (if not using @NonNull)
- Empty collections
- Special characters in strings

**Error Cases:**
- Invalid inputs
- Constraint violations
- Exception scenarios

**State-Based Tests:**
- Different object states
- Conditional branch coverage

**Integration Points:**
- Dependency interactions
- Method call verification

### Step 3: Generate Test Class Structure
Create test class following conventions:

**Naming:** [ClassName]Test.java (e.g., UserServiceTest.java)
**Location:** Mirror source structure in src/test/java/

**Structure Template:**
```java
@ExtendWith(MockitoExtension.class)
class ClassNameTest {
    // Mocks for dependencies
    @Mock
    private DependencyClass mockDependency;

    // System under test
    @InjectMocks
    private ClassUnderTest classUnderTest;

    // Test data builders
    private TestDataBuilder testDataBuilder;

    @BeforeEach
    void setUp() {
        // Common test setup
    }

    @Nested
    @DisplayName("methodName() tests")
    class MethodNameTests {
        // Group related tests
    }
}
```

### Step 4: Write Individual Test Methods
Follow the Arrange-Act-Assert (AAA) pattern:

```java
@Test
@DisplayName("should return user when valid ID provided")
void shouldReturnUser_WhenValidIdProvided() {
    // Arrange
    String userId = "123";
    User expectedUser = new User(userId, "John Doe");
    when(mockRepository.findById(userId)).thenReturn(Optional.of(expectedUser));

    // Act
    Optional<User> result = userService.getUser(userId);

    // Assert
    assertThat(result).isPresent();
    assertThat(result.get()).isEqualTo(expectedUser);
    verify(mockRepository).findById(userId);
}
```

**Test Method Naming Conventions:**
- `shouldDoSomething_WhenCondition()` format
- Or `should_DoSomething_When_Condition()` for readability
- Descriptive names that explain the scenario

### Step 5: Add Parameterized Tests for Multiple Inputs
Use `@ParameterizedTest` for testing multiple similar scenarios:

```java
@ParameterizedTest
@ValueSource(strings = {"", "  ", "\t", "\n"})
@DisplayName("should throw exception for blank names")
void shouldThrowException_ForBlankNames(String invalidName) {
    assertThrows(IllegalArgumentException.class,
        () -> userService.createUser(invalidName));
}

@ParameterizedTest
@CsvSource({
    "john@example.com, true",
    "invalid-email, false",
    "@example.com, false",
    "john@, false"
})
@DisplayName("should validate email correctly")
void shouldValidateEmail_Correctly(String email, boolean expected) {
    boolean result = validator.isValidEmail(email);
    assertThat(result).isEqualTo(expected);
}
```

### Step 6: Add Exception Testing
Test exception scenarios explicitly:

```java
@Test
@DisplayName("should throw UserNotFoundException when user not found")
void shouldThrowUserNotFoundException_WhenUserNotFound() {
    // Arrange
    String userId = "999";
    when(mockRepository.findById(userId)).thenReturn(Optional.empty());

    // Act & Assert
    assertThrows(UserNotFoundException.class,
        () -> userService.getUser(userId));
    verify(mockRepository).findById(userId);
}
```

### Step 7: Add Verification for Mock Interactions
Verify dependencies are called correctly:

```java
@Test
@DisplayName("should save user to repository")
void shouldSaveUser_ToRepository() {
    // Arrange
    User newUser = new User("John Doe", "john@example.com");

    // Act
    userService.createUser(newUser);

    // Assert
    verify(mockRepository).save(newUser);
    verifyNoMoreInteractions(mockRepository);
}
```

### Step 8: Generate Test Data Builders (Optional)
For complex objects, create builder methods:

```java
private User createTestUser(String id, String name) {
    return User.builder()
        .id(id)
        .name(name)
        .email(name.toLowerCase() + "@example.com")
        .createdAt(LocalDateTime.now())
        .build();
}
```

### Step 9: Add Coverage for Edge Cases
Include boundary and special cases:

```java
@Nested
@DisplayName("Edge case tests")
class EdgeCaseTests {
    @Test
    @DisplayName("should handle empty list")
    void shouldHandleEmptyList() {
        List<User> emptyList = Collections.emptyList();
        List<String> result = userService.extractNames(emptyList);
        assertThat(result).isEmpty();
    }

    @Test
    @DisplayName("should handle null optional")
    void shouldHandleNullOptional() {
        when(mockRepository.findById(anyString())).thenReturn(Optional.empty());
        Optional<User> result = userService.getUser("123");
        assertThat(result).isEmpty();
    }
}
```

## Examples

### Example 1: Generate Tests for Simple Service

**Source Code:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public Optional<User> getUser(String id) {
        return userRepository.findById(id);
    }

    public User createUser(String name, String email) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be blank");
        }
        User user = new User(name, email);
        return userRepository.save(user);
    }
}
```

**Generated Test:**
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService Tests")
class UserServiceTest {

    @Mock
    private UserRepository mockRepository;

    @InjectMocks
    private UserService userService;

    @Nested
    @DisplayName("getUser() tests")
    class GetUserTests {

        @Test
        @DisplayName("should return user when ID exists")
        void shouldReturnUser_WhenIdExists() {
            // Arrange
            String userId = "123";
            User expectedUser = new User("John Doe", "john@example.com");
            when(mockRepository.findById(userId))
                .thenReturn(Optional.of(expectedUser));

            // Act
            Optional<User> result = userService.getUser(userId);

            // Assert
            assertThat(result).isPresent();
            assertThat(result.get()).isEqualTo(expectedUser);
            verify(mockRepository).findById(userId);
        }

        @Test
        @DisplayName("should return empty when ID not found")
        void shouldReturnEmpty_WhenIdNotFound() {
            // Arrange
            String userId = "999";
            when(mockRepository.findById(userId))
                .thenReturn(Optional.empty());

            // Act
            Optional<User> result = userService.getUser(userId);

            // Assert
            assertThat(result).isEmpty();
            verify(mockRepository).findById(userId);
        }

        @Test
        @DisplayName("should handle null ID")
        void shouldHandleNullId() {
            // Act
            Optional<User> result = userService.getUser(null);

            // Assert
            assertThat(result).isEmpty();
            verify(mockRepository).findById(null);
        }
    }

    @Nested
    @DisplayName("createUser() tests")
    class CreateUserTests {

        @Test
        @DisplayName("should create user with valid inputs")
        void shouldCreateUser_WithValidInputs() {
            // Arrange
            String name = "John Doe";
            String email = "john@example.com";
            User userToSave = new User(name, email);
            User savedUser = new User(name, email);
            savedUser.setId("123");
            when(mockRepository.save(any(User.class)))
                .thenReturn(savedUser);

            // Act
            User result = userService.createUser(name, email);

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo("123");
            verify(mockRepository).save(any(User.class));
        }

        @ParameterizedTest
        @NullAndEmptySource
        @ValueSource(strings = {"  ", "\t", "\n"})
        @DisplayName("should throw exception for invalid names")
        void shouldThrowException_ForInvalidNames(String invalidName) {
            // Act & Assert
            assertThrows(IllegalArgumentException.class,
                () -> userService.createUser(invalidName, "john@example.com"));
            verifyNoInteractions(mockRepository);
        }

        @Test
        @DisplayName("should accept null email")
        void shouldAcceptNullEmail() {
            // Arrange
            String name = "John Doe";
            User savedUser = new User(name, null);
            when(mockRepository.save(any(User.class)))
                .thenReturn(savedUser);

            // Act
            User result = userService.createUser(name, null);

            // Assert
            assertThat(result).isNotNull();
            verify(mockRepository).save(any(User.class));
        }
    }
}
```

### Example 2: Generate Tests with Complex Mocking

**Source Code:**
```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    public Order processOrder(OrderRequest request) {
        Order order = createOrder(request);
        Payment payment = paymentService.processPayment(
            order.getTotalAmount()
        );
        if (payment.isSuccessful()) {
            order.setStatus(OrderStatus.CONFIRMED);
            Order savedOrder = orderRepository.save(order);
            notificationService.sendOrderConfirmation(savedOrder);
            return savedOrder;
        } else {
            throw new PaymentFailedException("Payment failed");
        }
    }
}
```

**Generated Test:**
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderService Tests")
class OrderServiceTest {

    @Mock
    private OrderRepository mockOrderRepository;

    @Mock
    private PaymentService mockPaymentService;

    @Mock
    private NotificationService mockNotificationService;

    @InjectMocks
    private OrderService orderService;

    @Captor
    private ArgumentCaptor<Order> orderCaptor;

    private OrderRequest testRequest;

    @BeforeEach
    void setUp() {
        testRequest = OrderRequest.builder()
            .customerId("CUST-123")
            .items(List.of(new OrderItem("ITEM-1", 2, 10.00)))
            .build();
    }

    @Nested
    @DisplayName("processOrder() tests")
    class ProcessOrderTests {

        @Test
        @DisplayName("should process order successfully with successful payment")
        void shouldProcessOrder_WithSuccessfulPayment() {
            // Arrange
            Payment successfulPayment = new Payment("PAY-123", true);
            when(mockPaymentService.processPayment(anyDouble()))
                .thenReturn(successfulPayment);
            Order savedOrder = new Order();
            savedOrder.setId("ORD-123");
            savedOrder.setStatus(OrderStatus.CONFIRMED);
            when(mockOrderRepository.save(any(Order.class)))
                .thenReturn(savedOrder);

            // Act
            Order result = orderService.processOrder(testRequest);

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo("ORD-123");
            assertThat(result.getStatus()).isEqualTo(OrderStatus.CONFIRMED);

            // Verify interactions in correct order
            InOrder inOrder = inOrder(
                mockPaymentService,
                mockOrderRepository,
                mockNotificationService
            );
            inOrder.verify(mockPaymentService).processPayment(20.00);
            inOrder.verify(mockOrderRepository).save(orderCaptor.capture());
            inOrder.verify(mockNotificationService)
                .sendOrderConfirmation(savedOrder);

            // Verify captured order state
            Order capturedOrder = orderCaptor.getValue();
            assertThat(capturedOrder.getStatus())
                .isEqualTo(OrderStatus.CONFIRMED);
        }

        @Test
        @DisplayName("should throw exception when payment fails")
        void shouldThrowException_WhenPaymentFails() {
            // Arrange
            Payment failedPayment = new Payment("PAY-456", false);
            when(mockPaymentService.processPayment(anyDouble()))
                .thenReturn(failedPayment);

            // Act & Assert
            assertThrows(PaymentFailedException.class,
                () -> orderService.processOrder(testRequest));

            // Verify
            verify(mockPaymentService).processPayment(20.00);
            verifyNoInteractions(mockOrderRepository);
            verifyNoInteractions(mockNotificationService);
        }

        @Test
        @DisplayName("should handle payment service exception")
        void shouldHandlePaymentServiceException() {
            // Arrange
            when(mockPaymentService.processPayment(anyDouble()))
                .thenThrow(new RuntimeException("Service unavailable"));

            // Act & Assert
            assertThrows(RuntimeException.class,
                () -> orderService.processOrder(testRequest));

            // Verify
            verifyNoInteractions(mockOrderRepository);
            verifyNoInteractions(mockNotificationService);
        }
    }
}
```

### Example 3: Generate Parameterized Tests for Validation

**Source Code:**
```java
public class EmailValidator {
    public boolean isValid(String email) {
        if (email == null || email.isBlank()) {
            return false;
        }
        return email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
    }
}
```

**Generated Test:**
```java
@DisplayName("EmailValidator Tests")
class EmailValidatorTest {

    private EmailValidator validator;

    @BeforeEach
    void setUp() {
        validator = new EmailValidator();
    }

    @Nested
    @DisplayName("Valid email tests")
    class ValidEmailTests {

        @ParameterizedTest
        @ValueSource(strings = {
            "user@example.com",
            "john.doe@example.com",
            "user+tag@example.co.uk",
            "123@example.com",
            "user_name@example.com"
        })
        @DisplayName("should return true for valid emails")
        void shouldReturnTrue_ForValidEmails(String email) {
            assertThat(validator.isValid(email)).isTrue();
        }
    }

    @Nested
    @DisplayName("Invalid email tests")
    class InvalidEmailTests {

        @ParameterizedTest
        @NullAndEmptySource
        @ValueSource(strings = {
            "  ",
            "\t",
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
            "user @example.com",
            "user@example",
            "user@@example.com"
        })
        @DisplayName("should return false for invalid emails")
        void shouldReturnFalse_ForInvalidEmails(String email) {
            assertThat(validator.isValid(email)).isFalse();
        }
    }

    @Nested
    @DisplayName("Edge case tests")
    class EdgeCaseTests {

        @Test
        @DisplayName("should handle very long email")
        void shouldHandleVeryLongEmail() {
            String longEmail = "a".repeat(100) + "@example.com";
            boolean result = validator.isValid(longEmail);
            assertThat(result).isTrue();
        }

        @ParameterizedTest
        @CsvSource({
            "user@example.com, true",
            "USER@EXAMPLE.COM, true",
            "User@Example.Com, true"
        })
        @DisplayName("should handle different cases")
        void shouldHandleDifferentCases(String email, boolean expected) {
            assertThat(validator.isValid(email)).isEqualTo(expected);
        }
    }
}
```

## Requirements

### Dependencies
Add to pom.xml or build.gradle:

**Maven:**
```xml
<dependencies>
    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>

    <!-- Mockito -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>

    <!-- AssertJ (recommended) -->
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>3.24.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Gradle:**
```groovy
testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
testImplementation 'org.mockito:mockito-core:5.5.0'
testImplementation 'org.mockito:mockito-junit-jupiter:5.5.0'
testImplementation 'org.assertj:assertj-core:3.24.2'
```

### Import Statements
Generated tests include:

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
```

## Testing Best Practices

**Naming:**
- Test class: [ClassName]Test
- Test method: should[ExpectedBehavior]_When[Condition]
- Use @DisplayName for readable test names

**Structure:**
- Follow Arrange-Act-Assert pattern
- Use @Nested classes to group related tests
- One assertion concept per test method

**Mocking:**
- Mock external dependencies only
- Use @InjectMocks for class under test
- Verify interactions when behavior matters
- Use ArgumentCaptor for complex verifications

**Coverage:**
- Test happy paths first
- Add edge cases and boundary conditions
- Test exception scenarios explicitly
- Aim for high branch coverage, not just line coverage

**Maintainability:**
- Keep tests simple and focused
- Use test data builders for complex objects
- Extract common setup to @BeforeEach
- Avoid test interdependence

## Output Format

When generating tests, provide:

1. **File location** for the test class
2. **Complete test class** with all imports
3. **Explanation** of test scenarios covered
4. **Coverage report** showing what's tested
5. **Run command** to execute tests

Example output structure:
```markdown
## Generated Test: UserServiceTest

**Location:** src/test/java/com/example/service/UserServiceTest.java

**Test Coverage:**
- getUser() - 3 test cases (happy path, not found, null ID)
- createUser() - 4 test cases (valid input, blank name, null email, special chars)

**Edge Cases Covered:**
- Empty/null/blank strings
- Null optional handling
- Exception scenarios

**Run Tests:**
```bash
mvn test -Dtest=UserServiceTest
# or
gradle test --tests UserServiceTest
```
```

## Error Handling

If test generation cannot be completed:

1. **Source file not found:** Use Glob to search for the file
2. **Missing dependencies:** Identify which fields need mocking
3. **Complex business logic:** Ask for clarification on expected behavior
4. **Unable to determine test scenarios:** Request example use cases

Always fail-fast with clear error messages rather than generating incomplete tests.
