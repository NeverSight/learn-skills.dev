---
name: swiftui-patterns
description: SwiftUI UI patterns, state management, navigation, animations, and performance optimization.
---

# SwiftUI Patterns

Modern SwiftUI patterns for iOS 17+ development.

## View Composition

### Small, Focused Views

```swift
// ✅ Good: Single responsibility
struct AvatarView: View {
    let imageURL: URL?
    let size: CGFloat

    var body: some View {
        AsyncImage(url: imageURL) { image in
            image.resizable()
        } placeholder: {
            Color.gray.opacity(0.2)
        }
        .frame(width: size, height: size)
        .clipShape(Circle())
    }
}

struct UserRow: View {
    let user: User

    var body: some View {
        HStack {
            AvatarView(imageURL: user.avatarURL, size: 48)
            VStack(alignment: .leading) {
                Text(user.name).font(.headline)
                Text(user.email).font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}
```

## State Management

### @Observable (iOS 17+)

```swift
@Observable
class HomeViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        items = await api.fetchItems()
        isLoading = false
    }
}

struct HomeView: View {
    @State private var viewModel = HomeViewModel()

    var body: some View {
        List {
            if viewModel.isLoading {
                ProgressView()
            } else {
                ForEach(viewModel.items) { item in
                    Text(item.title)
                }
            }
        }
        .task {
            await viewModel.loadItems()
        }
    }
}
```

## Performance Patterns

### Lazy Containers

```swift
// ✅ LazyVStack for long lists
ScrollView {
    LazyVStack(spacing: 16) {
        ForEach(items) { item in
            ItemCard(item: item)
        }
    }
}

// ✅ LazyHStack for horizontal lists
ScrollView(.horizontal) {
    LazyHStack(spacing: 12) {
        ForEach(users) { user in
            UserAvatar(user: user)
        }
    }
}
```

### Equatable Views

```swift
struct ItemRow: View, Equatable {
    let item: Item

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.item.id == rhs.item.id
    }

    var body: some View {
        HStack {
            Text(item.title)
            Text(item.price)
        }
    }
}
```

## Navigation

### NavigationStack

```swift
enum Route: Hashable {
    case home
    case detail(String)
    case profile(userId: String)
}

struct AppNavigation: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .home:
                        HomeView()
                    case .detail(let id):
                        DetailView(id: id)
                    case .profile(let userId):
                        ProfileView(userId: userId)
                    }
                }
        }
    }
}
```

### Sheet Presentation

```swift
struct RootView: View {
    @State private var presentedItem: Item?
    @State private var showingSettings = false

    var body: some View {
        List(items) { item in
            Button(item.title) { presentedItem = item }
        }
        .sheet(item: $presentedItem) { item in
            DetailSheet(item: item)
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView()
        }
    }
}
```

## Gestures

### Custom Gestures

```swift
struct SwipeToDismiss: ViewModifier {
    @State private var offset: CGFloat = 0

    func body(content: Content) -> some View {
        content
            .offset(x: offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        if value.translation.width < 0 {
                            offset = value.translation.width
                        }
                    }
                    .onEnded { value in
                        if value.translation.width < -100 {
                            // Dismiss action
                        }
                        offset = 0
                    }
            )
    }
}
```

## Animations

### Spring Animations

```swift
struct AnimatedButton: View {
    @State private var isPressed = false

    var body: some View {
        Circle()
            .fill(isPressed ? Color.blue : Color.gray)
            .frame(width: 80, height: 80)
            .scaleEffect(isPressed ? 0.9 : 1.0)
            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isPressed)
            .onTapGesture {
                withAnimation {
                    isPressed.toggle()
                }
            }
    }
}
```

### Phase Animations

```swift
struct StaggerAnimation: View {
    let items: [String]

    var body: some View {
        VStack {
            ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                Text(item)
                    .transition(.scale.combined(with: .opacity))
            }
        }
    }
}

// Usage with stagger
.transition(.asymmetric(
    insertion: .scale.combined(with: .opacity),
    removal: .opacity
))
```

## Custom Modifiers

```swift
struct CardModifier: ViewModifier {
    var backgroundColor: Color = .white
    var cornerRadius: CGFloat = 12
    var shadowRadius: CGFloat = 4

    func body(content: Content) -> some View {
        content
            .padding()
            .background(backgroundColor)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .shadow(radius: shadowRadius)
    }
}

extension View {
    func cardStyle(
        backgroundColor: Color = .white,
        cornerRadius: CGFloat = 12,
        shadowRadius: CGFloat = 4
    ) -> some View {
        modifier(CardModifier(
            backgroundColor: backgroundColor,
            cornerRadius: cornerRadius,
            shadowRadius: shadowRadius
        ))
    }
}
```

## Shapes & Styles

### Custom Shapes

```swift
struct BlobShape: Shape {
    var cornerRadius: CGFloat = 40
    var animatableData: CGFloat = cornerRadius

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let points = [
            CGPoint(x: 0, y: 0),
            CGPoint(x: rect.width, y: 0),
            CGPoint(x: rect.width, y: rect.height),
            CGPoint(x: 0, y: rect.height)
        ]
        // Create blob shape
        return path
    }
}

// Usage
BlobShape(cornerRadius: 50)
    .fill(Color.blue.gradient)
```

### Gradients

```swift
Circle()
    .fill(
        LinearGradient(
            colors: [.blue, .purple],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
    )

// Angular gradient
Circle()
    .fill(AngularGradient(
        colors: [.red, .yellow, .green, .blue, .red],
        center: .center
    ))
```

## Grid Layouts

```swift
LazyVGrid(
    columns: [
        GridItem(.adaptive(minimum: 100), spacing: 16)
    ],
    spacing: 16
) {
    ForEach(items) { item in
        ItemCell(item: item)
    }
}
```

---

**Remember**: SwiftUI views are values. Compose them, transform them, and let the framework handle rendering.
