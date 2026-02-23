---
name: flutter-best-practices
description: Comprehensive Flutter development guidelines covering architecture, state management, performance optimization, testing, and cross-platform best practices. Use when building, refactoring, or reviewing Flutter applications for mobile, web, and desktop platforms. Covers widget patterns, Riverpod/BLoC state management, navigation with go_router, Firebase integration, platform channels, custom painting, animations, CI/CD, and production deployment.
---

# Flutter Best Practices

Expert guidelines for building production-ready Flutter applications across mobile, web, and desktop platforms.

## Quick Start

When starting a new Flutter project or reviewing code:

1. **Architecture**: Use feature-first folder structure with clean separation of concerns
2. **State Management**: Prefer Riverpod for new projects; use BLoC for complex async flows
3. **Navigation**: Use go_router for deep linking and web support
4. **Testing**: Follow the testing pyramid - unit → widget → integration
5. **Performance**: Use `const` constructors, `ListView.builder`, and proper disposal patterns

## Architecture Patterns

### Three-Layer Architecture

Organize code into distinct layers for maintainability:

```
lib/
├── features/
│   └── feature_name/
│       ├── presentation/     # UI widgets, screens
│       ├── domain/           # Business logic, use cases, entities
│       └── data/             # Repositories, data sources, models
├── core/
│   ├── theme/               # AppTheme, colors, typography
│   ├── router/              # GoRouter configuration
│   └── utils/               # Shared utilities
└── main.dart
```

**Principles:**
- **Dependency Rule**: Higher layers depend on lower layers only
- **Feature API Interface**: Hide implementation details behind interfaces
- **Repository Pattern**: Abstract data access for testability

### Widget Architecture

**Widget Types Decision Tree:**

| Scenario | Use |
|----------|-----|
| Static UI, no changing state | `StatelessWidget` |
| Interactive UI with local state | `StatefulWidget` |
| Data shared down the tree | `InheritedWidget` / Riverpod |
| Complex reusable UI component | Custom widget class |

**StatefulWidget Lifecycle (Critical):**

```dart
class _MyWidgetState extends State<MyWidget> {
  @override
  void initState() {
    super.initState();
    // One-time initialization (controllers, subscriptions)
  }
  
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Called when InheritedWidget dependencies change
  }
  
  @override
  Widget build(BuildContext context) {
    // Keep fast and synchronous - no heavy computation
    return Container();
  }
  
  @override
  void dispose() {
    // CRITICAL: Dispose controllers, cancel subscriptions
    _controller.dispose();
    _subscription?.cancel();
    super.dispose();
  }
}
```

**Golden Rule**: Always dispose controllers, scroll controllers, text controllers, and cancel stream subscriptions.

## State Management

### Riverpod (Recommended for New Projects)

**Setup:**
```dart
// main.dart
void main() {
  runApp(ProviderScope(child: MyApp()));
}

// providers.dart
final counterProvider = StateProvider<int>((ref) => 0);

final userProvider = FutureProvider<User>((ref) async {
  return await ref.watch(authRepositoryProvider).getCurrentUser();
});

@riverpod
class TodoList extends _$TodoList {
  @override
  List<Todo> build() => [];
  
  void add(Todo todo) => state = [...state, todo];
  void toggle(String id) {
    state = state.map((t) => 
      t.id == id ? t.copyWith(completed: !t.completed) : t
    ).toList();
  }
}
```

**Usage Patterns:**

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch for UI updates
    final count = ref.watch(counterProvider);
    final asyncUser = ref.watch(userProvider);
    final todos = ref.watch(todoListProvider);
    
    // Read for one-time access (callbacks)
    void onPressed() {
      ref.read(todoListProvider.notifier).add(newTodo);
    }
    
    return asyncUser.when(
      data: (user) => Text(user.name),
      loading: () => CircularProgressIndicator(),
      error: (err, stack) => ErrorWidget(err),
    );
  }
}
```

**Key Methods:**
- `ref.watch(provider)`: Rebuild widget when provider changes
- `ref.read(provider)`: Get value once (use in callbacks, not build)
- `ref.listen(provider)`: Listen for changes and perform side effects

### BLoC Pattern (For Complex Async Flows)

**When to use BLoC:**
- Complex event-driven architectures
- Apps with heavy business logic separation requirements
- Teams familiar with reactive programming

```dart
// Events
abstract class CounterEvent {}
class CounterIncrementPressed extends CounterEvent {}

// States
class CounterState {
  final int count;
  CounterState(this.count);
}

// BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState(0)) {
    on<CounterIncrementPressed>((event, emit) {
      emit(CounterState(state.count + 1));
    });
  }
}

// Usage
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) {
    return Text('Count: ${state.count}');
  },
)
```

### State Selection Guide

| Use Case | Solution |
|----------|----------|
| Simple local widget state | `StatefulWidget` + `setState()` |
| Single value shared across widgets | `StateProvider` |
| Async data (API calls) | `FutureProvider` |
| Stream-based data | `StreamProvider` |
| Complex state with business logic | `StateNotifier` / BLoC |
| Global app state | Riverpod with scoped providers |

## Navigation

### go_router (Recommended)

**Setup:**
```dart
final _router = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    // Auth guard
    final isLoggedIn = authState.isAuthenticated;
    final isLoggingIn = state.matchedLocation == '/login';
    
    if (!isLoggedIn && !isLoggingIn) return '/login';
    if (isLoggedIn && isLoggingIn) return '/';
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) => DetailScreen(
            id: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => LoginScreen(),
    ),
  ],
);

// In MaterialApp
MaterialApp.router(routerConfig: _router);
```

**Navigation:**
```dart
// Navigate
context.go('/details/123');
context.push('/details/123');  // Preserves navigation stack
context.pop();

// With query parameters
context.goNamed('details', queryParameters: {'tab': 'reviews'});
```

**Deep Linking Setup:**

Android (`AndroidManifest.xml`):
```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW"/>
  <category android:name="android.intent.category.DEFAULT"/>
  <category android:name="android.intent.category.BROWSABLE"/>
  <data android:scheme="https" android:host="yourdomain.com"/>
</intent-filter>
```

iOS (`info.plist`):
```xml
<key>FlutterDeepLinkingEnabled</key>
<true/>
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>yourscheme</string>
    </array>
  </dict>
</array>
```

## Widget Patterns

### Layout Essentials

```dart
// Common layout patterns
Column(           // Vertical layout
  mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [...],
)

Row(              // Horizontal layout
  children: [
    Expanded(flex: 2, child: ...),  // Takes 2/3 space
    Expanded(flex: 1, child: ...),  // Takes 1/3 space
  ],
)

Stack(            // Overlapping widgets
  children: [
    Positioned.fill(child: Background()),
    Align(alignment: Alignment.bottomCenter, child: ...),
  ],
)

// Responsive layouts
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return DesktopLayout();
    }
    return MobileLayout();
  },
)
```

### List Optimization

**ALWAYS use builder for large/infinite lists:**

```dart
// Good - lazy loading, only builds visible items
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ListTile(
    title: Text(items[index].title),
  ),
)

// For grids with images
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: crossAxisCount,
  ),
  itemCount: items.length,
  itemBuilder: (context, index) => ImageCard(items[index]),
)

// With custom scroll effects
CustomScrollView(
  slivers: [
    SliverAppBar(
      expandedHeight: 200,
      flexibleSpace: FlexibleSpaceBar(title: Text('Title')),
    ),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(...),
        childCount: items.length,
      ),
    ),
  ],
)
```

### Form Handling

```dart
class _MyFormState extends State<MyForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  
  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _nameController,
            decoration: InputDecoration(labelText: 'Name'),
            validator: (value) {
              if (value?.isEmpty ?? true) return 'Required';
              return null;
            },
          ),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                _formKey.currentState!.save();
                // Process form
              }
            },
            child: Text('Submit'),
          ),
        ],
      ),
    );
  }
}
```

## Performance Optimization

### Critical Performance Rules

| Rule | Implementation | Priority |
|------|---------------|----------|
| Use `const` constructors | `const Text('Hello')` | Critical |
| Use builders for lists | `ListView.builder` | Critical |
| Dispose controllers | `controller.dispose()` | Critical |
| Cache expensive operations | `compute()` for heavy work | High |
| Use `RepaintBoundary` | Wrap animated widgets | Medium |
| Avoid clipping | Minimize `Clip` widgets | Medium |

### Memory Management

```dart
// Always check mounted before setState in async
void _loadData() async {
  final data = await fetchData();
  if (mounted) {  // CRITICAL
    setState(() => _data = data);
  }
}

// Limit image cache for memory-constrained apps
PaintingBinding.instance.imageCache.maximumSize = 100;
PaintingBinding.instance.imageCache.maximumSizeBytes = 50 * 1024 * 1024;

// Use weak references for long-lived callbacks
final weakRef = WeakReference(object);
```

### Isolate Usage

Offload heavy computation from UI thread:

```dart
// Heavy computation
final result = await compute(parseJson, largeJsonString);

// For complex parsing
Future<List<Model>> parseModels(String jsonString) async {
  return compute((str) {
    final decoded = json.decode(str) as List;
    return decoded.map((e) => Model.fromJson(e)).toList();
  }, jsonString);
}
```

### DevTools Profiling

Enable these flags for debugging:

```dart
// In main.dart for debugging
void main() {
  // Visualize widget rebuilds
  debugRepaintRainbowEnabled = true;
  
  // Show paint bounds
  debugPaintSizeEnabled = true;
  
  runApp(MyApp());
}
```

**Key DevTools Views:**
- **Widget Rebuild Counts**: Identify excessive rebuilds
- **Performance**: Frame timing, shader compilation
- **Memory**: Heap snapshots, allocation tracking
- **Network**: API call monitoring

## Testing

### Testing Pyramid

```
       ▲ Integration (Full flows)
      ╱ ╲
     ╱   ╲ Widget (UI components)
    ╱     ╲
   ╱       ╲
  ╱_________╲
 Unit (Logic, pure Dart)
```

### Unit Testing

```dart
test('can calculate total price', () {
  // Arrange
  final cart = Cart(items: [
    Item(price: 10, quantity: 2),
    Item(price: 5, quantity: 1),
  ]);
  
  // Act
  final total = cart.total;
  
  // Assert
  expect(total, equals(25));
});

// With Riverpod
test('counter increments', () {
  final container = ProviderContainer();
  addTearDown(container.dispose);
  
  final notifier = container.read(counterProvider.notifier);
  notifier.state = 5;
  notifier.state++;
  
  expect(container.read(counterProvider), equals(6));
});
```

### Widget Testing

```dart
testWidgets('displays user name', (WidgetTester tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      home: UserProfile(user: User(name: 'John')),
    ),
  );
  
  // Act & Assert
  expect(find.text('John'), findsOneWidget);
  expect(find.byType(CircularProgressIndicator), findsNothing);
});

testWidgets('tapping button increments counter', (tester) async {
  await tester.pumpWidget(MyApp());
  
  await tester.tap(find.byIcon(Icons.add));
  await tester.pumpAndSettle();
  
  expect(find.text('1'), findsOneWidget);
});
```

### Golden Tests (Visual Regression)

```dart
testGoldens('UserProfile renders correctly', (tester) async {
  final builder = GoldenBuilder.grid(columns: 2)
    ..addScenario('Light', UserProfile(user: mockUser))
    ..addScenario('Dark', Theme(data: darkTheme, child: UserProfile(user: mockUser)));
  
  await tester.pumpWidgetBuilder(builder.build());
  await screenMatchesGolden(tester, 'user_profile');
});

// Update goldens: flutter test --update-goldens --tags=golden
```

### Integration Testing

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('full login flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    
    await tester.enterText(find.byType(TextField).first, 'user@example.com');
    await tester.enterText(find.byType(TextField).last, 'password');
    await tester.tap(find.byType(ElevatedButton));
    await tester.pumpAndSettle();
    
    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

## Networking

### HTTP Service Pattern

```dart
class ApiService {
  final Dio _dio;
  
  ApiService({Dio? dio}) : _dio = dio ?? Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: Duration(seconds: 5),
    receiveTimeout: Duration(seconds: 3),
  )) {
    _dio.interceptors.add(AuthInterceptor());
    _dio.interceptors.add(LogInterceptor());
  }
  
  Future<List<User>> getUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List)
      .map((json) => User.fromJson(json))
      .toList();
  }
}

// With Riverpod
final apiServiceProvider = Provider<ApiService>((ref) {
  return ApiService();
});

final usersProvider = FutureProvider<List<User>>((ref) async {
  final api = ref.watch(apiServiceProvider);
  return api.getUsers();
});
```

### JSON Serialization

```dart
// With freezed (recommended)
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @Default([]) List<String> tags,
    DateTime? createdAt,
  }) = _User;
  
  factory User.fromJson(Map<String, dynamic> json) => 
      _$UserFromJson(json);
}

// Manual approach
class User {
  final String id;
  final String name;
  
  User({required this.id, required this.name});
  
  factory User.fromJson(Map<String, dynamic> json) => User(
    id: json['id'] as String,
    name: json['name'] as String,
  );
  
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
  };
}
```

## Firebase Integration

### Firebase Setup

```bash
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# Configure project
flutterfire configure --project=your-project-id
```

### Cloud Messaging (Push Notifications)

```dart
class NotificationService {
  final FirebaseMessaging _messaging;
  
  NotificationService(this._messaging);
  
  Future<void> initialize() async {
    // Request permissions
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );
    
    // Get FCM token
    final token = await _messaging.getToken();
    await _saveToken(token);
    
    // Listen to token refresh
    _messaging.onTokenRefresh.listen(_saveToken);
    
    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);
    
    // Handle background/terminated
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);
    final initialMessage = await _messaging.getInitialMessage();
    if (initialMessage != null) {
      _handleNotificationTap(initialMessage);
    }
  }
  
  @pragma('vm:entry-point')
  static Future<void> _firebaseMessagingBackgroundHandler(
    RemoteMessage message,
  ) async {
    await Firebase.initializeApp();
    // Handle background message
  }
}

// Register in main
FirebaseMessaging.onBackgroundMessage(
  NotificationService._firebaseMessagingBackgroundHandler,
);
```

## Cross-Platform Considerations

### Platform Detection

```dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

bool get isWeb => kIsWeb;
bool get isMobile => !kIsWeb && (Platform.isIOS || Platform.isAndroid);
bool get isDesktop => !kIsWeb && (Platform.isWindows || Platform.isMacOS || Platform.isLinux);

// Conditional UI
if (Platform.isIOS) {
  return CupertinoButton(child: Text('Done'), onPressed: () {});
}
return ElevatedButton(child: Text('Done'), onPressed: () {});
```

### Adaptive Layouts

```dart
// Using flutter_adaptive_scaffold
AdaptiveLayout(
  primaryNavigation: SlotLayout(config: {
    Breakpoints.mediumAndUp: SlotLayout.from(
      builder: (_) => NavigationRail(destinations: [...]),
    ),
  }),
  bottomNavigation: SlotLayout(config: {
    Breakpoints.small: SlotLayout.from(
      builder: (_) => BottomNavigationBar(items: [...]),
    ),
  }),
  body: SlotLayout(config: {
    Breakpoints.small: SlotLayout.from(builder: (_) => MobileBody()),
    Breakpoints.mediumAndUp: SlotLayout.from(builder: (_) => DesktopBody()),
  }),
)
```

### Platform Channels

**Flutter side:**
```dart
class PlatformChannelService {
  static const MethodChannel _channel = 
      MethodChannel('com.example.app/channel');
  
  Future<String?> getNativeData() async {
    try {
      final result = await _channel.invokeMethod<String>('getNativeData');
      return result;
    } on PlatformException catch (e) {
      print('Error: ${e.message}');
      return null;
    }
  }
}
```

## Animations

### Implicit Animations

```dart
// Simple animations that trigger on value change
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: isExpanded ? 200 : 100,
  height: isExpanded ? 200 : 100,
  color: isExpanded ? Colors.red : Colors.blue,
  child: child,
)

AnimatedOpacity(
  duration: Duration(milliseconds: 200),
  opacity: isVisible ? 1.0 : 0.0,
  child: child,
)
```

### Explicit Animations

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    );
    _animation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    );
    _controller.forward();
  }
  
  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: ScaleTransition(
        scale: _animation,
        child: child,
      ),
    );
  }
}
```

### Hero Animations

```dart
// Source page
Hero(
  tag: 'image-${item.id}',
  child: Image.network(item.imageUrl),
)

// Destination page (same tag)
Hero(
  tag: 'image-${item.id}',
  child: Image.network(item.imageUrl),
)
```

## Production Deployment

### Build Commands

```bash
# Android App Bundle (recommended for Play Store)
flutter build appbundle --release --obfuscate --split-debug-info=symbols/

# Android APK
flutter build apk --release --split-per-abi

# iOS
flutter build ios --release

# Web
flutter build web --release

# Desktop
flutter build windows --release
flutter build macos --release
flutter build linux --release
```

### Code Obfuscation

**Always obfuscate for production:**

```bash
flutter build appbundle \
  --obfuscate \
  --split-debug-info=symbols/
```

Store symbol files for crash symbolication.

### CI/CD Pipeline (GitHub Actions Example)

```yaml
name: Flutter CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
      
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test
      - run: flutter build apk --release
```

## References

For detailed guides on specific topics:

- **State Management Deep Dive**: See [references/state-management.md](references/state-management.md)
- **Testing Patterns**: See [references/testing.md](references/testing.md)
- **Performance Optimization**: See [references/performance.md](references/performance.md)
- **Platform Integration**: See [references/platform-channels.md](references/platform-channels.md)
