---
name: Cross-Platform App Development Skill
description: Strategies for developing apps that work across multiple Apple platforms, including adaptive layouts and multi-view implementations.
version: 1.0
activation: Activate for queries on cross-platform development, multi-platform apps, adaptive layouts, or device-specific adaptations.
---

# Cross-Platform App Development Skill

This skill focuses on building applications that work seamlessly across Apple's ecosystem: iOS, iPadOS, macOS, watchOS, and tvOS. It emphasizes adaptive design, platform-specific optimizations, and shared codebases using SwiftUI.

## Best Practices

1. **Unified Codebase**: Use SwiftUI for maximum code sharing across platforms.

2. **Adaptive Layouts**: Design interfaces that adapt to different screen sizes and orientations.

3. **Platform-Specific Features**: Leverage unique capabilities of each platform while maintaining consistency.

4. **Environment Awareness**: Use environment values to detect platform, size classes, and capabilities.

5. **Progressive Enhancement**: Start with core functionality and add platform-specific features.

6. **Testing Across Platforms**: Regularly test on all target platforms.

## Cross-Platform Guidelines

- Use SwiftUI's built-in adaptive components (NavigationView, TabView, etc.)
- Leverage @Environment to access platform-specific information
- Implement custom view modifiers for platform-specific styling
- Use conditional compilation when necessary (#if os(iOS))
- Design for both mouse/keyboard and touch interactions
- Consider different input methods (remote control, watch crown, etc.)

## Examples

### Example 1: Adaptive Layout with Size Classes

**User Prompt:** "Create an adaptive layout that works on both iPhone and iPad."

**Expected Output:**
```swift
import SwiftUI

struct AdaptiveContentView: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    
    var body: some View {
        Group {
            if horizontalSizeClass == .compact {
                // iPhone portrait or small screens
                VStack {
                    HeaderView()
                    ContentListView()
                    FooterView()
                }
            } else {
                // iPad or wide screens
                HStack {
                    SidebarView()
                    VStack {
                        HeaderView()
                        ContentListView()
                    }
                    DetailView()
                }
            }
        }
    }
}

struct HeaderView: View {
    var body: some View {
        Text("App Header")
            .font(.largeTitle)
            .padding()
    }
}

struct ContentListView: View {
    var body: some View {
        List(1...10, id: \.self) { item in
            Text("Item \(item)")
        }
    }
}

struct SidebarView: View {
    var body: some View {
        Text("Sidebar")
            .frame(width: 200)
            .background(Color.gray.opacity(0.2))
    }
}

struct DetailView: View {
    var body: some View {
        Text("Detail View")
            .frame(maxWidth: .infinity)
            .background(Color.blue.opacity(0.1))
    }
}

struct FooterView: View {
    var body: some View {
        Text("Footer")
            .padding()
    }
}
```

### Example 2: Platform-Specific Code

**User Prompt:** "How do I implement platform-specific features in a shared SwiftUI codebase?"

**Expected Output:**
```swift
import SwiftUI

struct CrossPlatformView: View {
    var body: some View {
        VStack {
            Text("Shared Content")
            
            #if os(iOS)
            iOSOnlyView()
            #elseif os(macOS)
            MacOnlyView()
            #elseif os(watchOS)
            WatchOnlyView()
            #elseif os(tvOS)
            TVOnlyView()
            #endif
        }
    }
}

#if os(iOS)
struct iOSOnlyView: View {
    var body: some View {
        Button("iOS Specific Button") {
            // iOS specific action
        }
        .buttonStyle(.borderedProminent)
    }
}
#endif

#if os(macOS)
struct MacOnlyView: View {
    var body: some View {
        Button("macOS Specific Button") {
            // macOS specific action
        }
        .buttonStyle(.bordered)
    }
}
#endif

#if os(watchOS)
struct WatchOnlyView: View {
    var body: some View {
        Text("WatchOS Interface")
            .font(.caption)
    }
}
#endif

#if os(tvOS)
struct TVOnlyView: View {
    var body: some View {
        Button("TV Button") {
            // TV specific action
        }
        .font(.title)
        .padding()
    }
}
#endif
```

### Example 3: Environment-Based Adaptations

**User Prompt:** "Adapt a view based on the current platform and color scheme using environment values."

**Expected Output:**
```swift
import SwiftUI

struct EnvironmentAdaptiveView: View {
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    
    var body: some View {
        ZStack {
            (colorScheme == .dark ? Color.black : Color.white)
                .edgesIgnoringSafeArea(.all)
            
            VStack(spacing: platformSpacing) {
                Text(platformTitle)
                    .font(platformFont)
                    .foregroundColor(colorScheme == .dark ? .white : .black)
                
                HStack(spacing: horizontalSizeClass == .compact ? 10 : 20) {
                    ForEach(0..<3) { index in
                        RoundedRectangle(cornerRadius: 10)
                            .fill(Color.blue.opacity(0.3))
                            .frame(width: itemWidth, height: itemHeight)
                            .overlay(
                                Text("Item \(index + 1)")
                                    .foregroundColor(.primary)
                            )
                    }
                }
            }
            .padding()
        }
    }
    
    private var platformTitle: String {
        #if os(iOS)
        return "iOS App"
        #elseif os(macOS)
        return "macOS App"
        #elseif os(watchOS)
        return "watchOS App"
        #elseif os(tvOS)
        return "tvOS App"
        #else
        return "Cross-Platform App"
        #endif
    }
    
    private var platformFont: Font {
        #if os(watchOS)
        return .headline
        #elseif os(tvOS)
        return .largeTitle
        #else
        return .title
        #endif
    }
    
    private var platformSpacing: CGFloat {
        #if os(watchOS)
        return 8
        #else
        return 20
        #endif
    }
    
    private var itemWidth: CGFloat {
        horizontalSizeClass == .compact ? 80 : 120
    }
    
    private var itemHeight: CGFloat {
        #if os(watchOS)
        return 40
        #else
        return horizontalSizeClass == .compact ? 80 : 100
        #endif
    }
}
```

### Example 4: Navigation Adaptations

**User Prompt:** "Implement navigation that adapts to different platforms automatically."

**Expected Output:**
```swift
import SwiftUI

struct AdaptiveNavigationView: View {
    var body: some View {
        #if os(macOS)
        NavigationView {
            SidebarList()
            DetailView()
        }
        .frame(minWidth: 800, minHeight: 600)
        #else
        NavigationView {
            SidebarList()
            DetailView()
        }
        .navigationViewStyle(.stack) // For iOS, ensures stack navigation
        #endif
    }
}

struct SidebarList: View {
    @State private var selectedItem: String?
    
    var body: some View {
        List(selection: $selectedItem) {
            ForEach(["Item 1", "Item 2", "Item 3"], id: \.self) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    Text(item)
                }
            }
        }
        .listStyle(.sidebar)
        .navigationTitle("Items")
    }
}

struct DetailView: View {
    let item: String?
    
    var body: some View {
        ZStack {
            Color.gray.opacity(0.1)
                .edgesIgnoringSafeArea(.all)
            
            VStack {
                if let item = item {
                    Text("Detail for \(item)")
                        .font(.largeTitle)
                } else {
                    Text("Select an item")
                        .font(.title)
                        .foregroundColor(.secondary)
                }
            }
        }
        .navigationTitle(item ?? "Detail")
    }
}
```

### Example 5: GeometryReader for Dynamic Layouts

**User Prompt:** "Use GeometryReader to create a layout that adapts to available space."

**Expected Output:**
```swift
import SwiftUI

struct GeometryAdaptiveView: View {
    var body: some View {
        GeometryReader { geometry in
            VStack {
                Text("Available width: \(Int(geometry.size.width))")
                Text("Available height: \(Int(geometry.size.height))")
                
                if geometry.size.width > geometry.size.height {
                    // Landscape or wide layout
                    HStack {
                        Rectangle()
                            .fill(Color.red.opacity(0.3))
                            .frame(width: geometry.size.width * 0.4, height: 100)
                        
                        Rectangle()
                            .fill(Color.blue.opacity(0.3))
                            .frame(width: geometry.size.width * 0.4, height: 100)
                    }
                } else {
                    // Portrait or narrow layout
                    VStack {
                        Rectangle()
                            .fill(Color.red.opacity(0.3))
                            .frame(width: geometry.size.width * 0.8, height: 100)
                        
                        Rectangle()
                            .fill(Color.blue.opacity(0.3))
                            .frame(width: geometry.size.width * 0.8, height: 100)
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

// Advanced example: Multi-column layout
struct MultiColumnView: View {
    let items = Array(1...20)
    
    var body: some View {
        GeometryReader { geometry in
            ScrollView {
                LazyVGrid(columns: adaptiveColumns(for: geometry.size.width), spacing: 16) {
                    ForEach(items, id: \.self) { item in
                        ZStack {
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.blue.opacity(0.2))
                                .frame(height: 100)
                            
                            Text("Item \(item)")
                                .font(.headline)
                        }
                    }
                }
                .padding()
            }
        }
    }
    
    private func adaptiveColumns(for width: CGFloat) -> [GridItem] {
        if width > 800 {
            return Array(repeating: GridItem(.flexible(), spacing: 16), count: 4)
        } else if width > 600 {
            return Array(repeating: GridItem(.flexible(), spacing: 16), count: 3)
        } else if width > 400 {
            return Array(repeating: GridItem(.flexible(), spacing: 16), count: 2)
        } else {
            return [GridItem(.flexible())]
        }
    }
}
```