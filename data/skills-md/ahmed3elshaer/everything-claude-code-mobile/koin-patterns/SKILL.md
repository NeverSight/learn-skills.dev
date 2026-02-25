---
name: koin-patterns
description: Koin dependency injection patterns for Android with modules, scopes, and ViewModel injection.
---

# Koin Dependency Injection

Pragmatic DI for Kotlin with Koin.

## Module Setup

```kotlin
// AppModule.kt
val appModule = module {
    // Singletons
    single<AppDatabase> { Room.databaseBuilder(...).build() }
    single { get<AppDatabase>().userDao() }
    
    // Factories (new instance each time)
    factory { DateFormatter() }
}

// NetworkModule.kt
val networkModule = module {
    single<HttpClient> {
        HttpClient(OkHttp) {
            install(ContentNegotiation) {
                json(Json { ignoreUnknownKeys = true })
            }
        }
    }
    
    single<AuthApi> { AuthApiImpl(get()) }
    single<UserApi> { UserApiImpl(get()) }
}

// FeatureModule.kt
val homeModule = module {
    // Repository
    single<HomeRepository> { HomeRepositoryImpl(get(), get()) }
    
    // Use Cases
    factory { GetItemsUseCase(get()) }
    factory { GetItemUseCase(get()) }
    
    // ViewModel
    viewModel { HomeViewModel(get()) }
}
```

## Application Setup

```kotlin
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        
        startKoin {
            androidContext(this@MyApp)
            modules(
                appModule,
                networkModule,
                homeModule,
                detailModule
            )
        }
    }
}
```

## ViewModel Injection

```kotlin
// In Compose
@Composable
fun HomeScreen(viewModel: HomeViewModel = koinViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    // ...
}

// With parameters
@Composable
fun DetailScreen(itemId: String) {
    val viewModel: DetailViewModel = koinViewModel { parametersOf(itemId) }
    // ...
}

// ViewModel definition with params
viewModel { params ->
    DetailViewModel(
        itemId = params.get(),
        repository = get()
    )
}
```

## Scopes

```kotlin
// Activity scope
val activityModule = module {
    scope<MainActivity> {
        scoped { NavigationController() }
    }
}

// Usage
class MainActivity : AppCompatActivity(), KoinScopeComponent {
    override val scope: Scope by activityScope()
    
    val nav: NavigationController by inject()
}
```

## Qualifiers

```kotlin
val networkModule = module {
    single(named("auth")) { createAuthClient() }
    single(named("default")) { createDefaultClient() }
}

// Usage
class UserApi(
    @Named("auth") private val client: HttpClient
)
```

## Testing

```kotlin
class HomeViewModelTest : KoinTest {
    
    @get:Rule
    val koinRule = KoinTestRule.create {
        modules(testModule)
    }
    
    private val testModule = module {
        single<HomeRepository> { mockk() }
        viewModel { HomeViewModel(get()) }
    }
    
    private val viewModel: HomeViewModel by inject()
    private val repository: HomeRepository by inject()
    
    @Test
    fun `loads items`() = runTest {
        coEvery { repository.getItems() } returns Result.success(listOf())
        // ...
    }
}
```

---

**Remember**: Koin is pragmatic. Keep modules organized, use scopes for lifecycle.
