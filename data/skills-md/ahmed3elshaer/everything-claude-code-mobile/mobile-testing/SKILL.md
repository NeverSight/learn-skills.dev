---
name: mobile-testing
description: Android testing patterns with JUnit5, Mockk, Turbine, and Compose testing for unit, integration, and UI tests.
---

# Mobile Testing Patterns

Comprehensive testing for Android.

## Test Dependencies

```kotlin
// build.gradle.kts
dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("io.mockk:mockk:1.13.8")
    testImplementation("app.cash.turbine:turbine:1.0.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
    
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

## ViewModel Testing

```kotlin
class HomeViewModelTest {
    @MockK private lateinit var repository: HomeRepository
    private lateinit var viewModel: HomeViewModel

    @BeforeEach
    fun setup() {
        MockKAnnotations.init(this)
        viewModel = HomeViewModel(repository)
    }

    @Test
    fun `loads items successfully`() = runTest {
        coEvery { repository.getItems() } returns Result.success(listOf(item))

        viewModel.state.test {
            viewModel.onIntent(LoadItems)
            awaitItem().isLoading shouldBe true
            awaitItem().items shouldBe listOf(item)
        }
    }
}
```

## Repository Testing

```kotlin
class UserRepositoryTest {
    @MockK private lateinit var api: UserApi
    private lateinit var repository: UserRepository

    @Test
    fun `getUser returns mapped domain model`() = runTest {
        coEvery { api.getUser("1") } returns UserDto("1", "John")

        val result = repository.getUser("1")

        result.isSuccess shouldBe true
        result.getOrNull()?.name shouldBe "John"
    }
}
```

## Compose UI Testing

```kotlin
class HomeScreenTest {
    @get:Rule
    val rule = createComposeRule()

    @Test
    fun `displays items`() {
        rule.setContent {
            HomeContent(state = HomeState(items = listOf(item)))
        }

        rule.onNodeWithText(item.name).assertIsDisplayed()
    }
}
```

## Coverage Target: 80%

```bash
./gradlew koverHtmlReport
```

---

**Remember**: Test behavior, not implementation. Write tests first.
