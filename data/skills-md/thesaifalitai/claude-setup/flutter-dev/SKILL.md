---
name: flutter-dev
description: >
  Expert Flutter and Dart development skill. ALWAYS trigger for ANY task involving Flutter, Dart,
  Flutter widgets, Flutter state management (Bloc/Riverpod/Provider/GetX), Flutter navigation
  (GoRouter/AutoRoute), Flutter animations, flutter pub, pubspec.yaml, Material Design 3,
  Cupertino widgets, Flutter testing, Flutter CI/CD (Fastlane/Codemagic), Flutter web, Flutter desktop,
  Dio HTTP client, Freezed data classes, Firebase Flutter, or cross-platform app development with Flutter.
  Also triggers for: "flutter app", "dart code", "flutter widget", "flutter project",
  "riverpod", "bloc pattern", "flutter navigation", "flutter package".
---

# Flutter & Dart Expert

You are a senior Flutter developer specializing in cross-platform mobile apps with clean architecture,
Riverpod/Bloc state management, and production deployments.

## Project Structure (Clean Architecture)

```
lib/
├── core/
│   ├── constants/          # App constants, endpoints
│   ├── errors/             # Failure classes
│   ├── network/            # Dio client setup
│   ├── router/             # GoRouter config
│   └── theme/              # Material 3 theme
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/      # JSON serializable (Freezed)
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/    # Pure Dart classes
│   │   │   ├── repositories/ # Abstract interfaces
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── pages/
│   │       ├── widgets/
│   │       └── providers/   # Riverpod providers
│   └── home/
├── shared/
│   ├── widgets/             # Reusable widgets
│   └── extensions/          # BuildContext extensions
└── main.dart
```

## Riverpod State Management

```dart
// providers/auth_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'auth_provider.g.dart';

@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  AuthState build() => const AuthState.initial();

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    final result = await ref.read(authRepositoryProvider).login(email, password);
    state = result.fold(
      (failure) => AuthState.error(failure.message),
      (user) => AuthState.authenticated(user),
    );
  }

  void logout() {
    ref.read(authRepositoryProvider).logout();
    state = const AuthState.unauthenticated();
  }
}

// Freezed state union
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(String message) = _Error;
}
```

## Freezed Data Models

```dart
// models/user_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String email,
    required String name,
    String? avatarUrl,
    @Default(false) bool isVerified,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}
```

## GoRouter Navigation

```dart
// core/router/app_router.dart
import 'package:go_router/go_router.dart';

final appRouter = GoRouter(
  initialLocation: '/splash',
  redirect: (context, state) {
    final isLoggedIn = ref.read(authNotifierProvider) is _Authenticated;
    final isAuthRoute = state.matchedLocation.startsWith('/auth');
    if (!isLoggedIn && !isAuthRoute) return '/auth/login';
    if (isLoggedIn && isAuthRoute) return '/home';
    return null;
  },
  routes: [
    GoRoute(path: '/splash', builder: (ctx, state) => const SplashPage()),
    ShellRoute(
      builder: (ctx, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/home', builder: (ctx, state) => const HomePage()),
        GoRoute(
          path: '/products/:id',
          builder: (ctx, state) =>
              ProductDetailPage(id: state.pathParameters['id']!),
        ),
      ],
    ),
    GoRoute(path: '/auth/login', builder: (ctx, state) => const LoginPage()),
  ],
);
```

## Dio HTTP Client

```dart
// core/network/dio_client.dart
class DioClient {
  late final Dio _dio;

  DioClient(String baseUrl, TokenStorage tokenStorage) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
    ));

    _dio.interceptors.addAll([
      AuthInterceptor(tokenStorage),
      RetryInterceptor(dio: _dio, retries: 3),
      LogInterceptor(requestBody: true, responseBody: true),
    ]);
  }

  Future<T> get<T>(String path, T Function(dynamic) fromJson) async {
    final response = await _dio.get(path);
    return fromJson(response.data);
  }
}

// interceptors/auth_interceptor.dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = tokenStorage.accessToken;
    if (token != null) options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      final refreshed = await _refreshToken();
      if (refreshed) {
        return handler.resolve(await _dio.fetch(err.requestOptions));
      }
    }
    handler.next(err);
  }
}
```

## Material 3 Theme

```dart
// core/theme/app_theme.dart
class AppTheme {
  static ThemeData get light => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF6366F1),
      brightness: Brightness.light,
    ),
    textTheme: GoogleFonts.interTextTheme(),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        minimumSize: const Size(double.infinity, 52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    ),
  );

  static ThemeData get dark => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF6366F1),
      brightness: Brightness.dark,
    ),
    textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
  );
}
```

## pubspec.yaml Dependencies

```yaml
dependencies:
  flutter_riverpod: ^2.5.1
  riverpod_annotation: ^2.3.5
  go_router: ^14.0.0
  freezed_annotation: ^2.4.1
  json_annotation: ^4.9.0
  dio: ^5.4.3+1
  retrofit: ^4.1.0
  flutter_secure_storage: ^9.0.0
  cached_network_image: ^3.3.1
  shimmer: ^3.0.0
  intl: ^0.19.0
  equatable: ^2.0.5

dev_dependencies:
  build_runner: ^2.4.9
  freezed: ^2.5.2
  json_serializable: ^6.8.0
  retrofit_generator: ^8.1.0
  riverpod_generator: ^2.4.0
  flutter_test:
    sdk: flutter
```

## Testing

```dart
// test/features/auth/auth_notifier_test.dart
void main() {
  group('AuthNotifier', () {
    late ProviderContainer container;
    late MockAuthRepository mockRepository;

    setUp(() {
      mockRepository = MockAuthRepository();
      container = ProviderContainer(
        overrides: [authRepositoryProvider.overrideWithValue(mockRepository)],
      );
    });

    tearDown(() => container.dispose());

    test('should emit authenticated state on successful login', () async {
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Right(tUser));

      final notifier = container.read(authNotifierProvider.notifier);
      await notifier.login('test@email.com', 'password');

      expect(
        container.read(authNotifierProvider),
        isA<_Authenticated>().having((s) => s.user, 'user', tUser),
      );
    });
  });
}
```

## Common Commands

```bash
# Create project
flutter create my_app --org com.mycompany

# Code generation
dart run build_runner build --delete-conflicting-outputs
dart run build_runner watch

# Run
flutter run --dart-define=API_URL=http://localhost:3000

# Build
flutter build apk --release --dart-define=API_URL=https://api.prod.com
flutter build ios --release
flutter build appbundle --release

# Test
flutter test
flutter test --coverage

# Analyze
flutter analyze
dart fix --apply
```
