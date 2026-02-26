---
name: SwiftUI Programming Skill
description: Expertise in SwiftUI for building declarative user interfaces, including SF Symbols integration and best practices.
version: 1.0
activation: Activate for queries on SwiftUI development, declarative UI building, SF Symbols usage, or SwiftUI component creation.
---

# SwiftUI Programming Skill

This skill provides comprehensive guidance on developing user interfaces using SwiftUI, Apple's modern framework for building apps across all Apple platforms. It emphasizes declarative programming, state management, and integration with system features like SF Symbols.

## Best Practices

1. **Declarative Syntax**: Use SwiftUI's declarative approach to describe what the UI should look like, not how to build it.

2. **State Management**: Leverage `@State`, `@ObservedObject`, `@EnvironmentObject` for managing view state.

3. **Composition**: Build complex views by composing simpler views.

4. **Accessibility**: Always consider accessibility features from the start.

5. **Performance**: Use appropriate modifiers and avoid unnecessary view updates.

6. **SF Symbols**: Utilize Apple's symbol library for consistent iconography.

## SwiftUI Guidelines

- Prefer built-in components over custom implementations when possible.
- Use SwiftUI's layout system (HStack, VStack, ZStack) effectively.
- Implement dark mode support automatically with Color and system colors.
- Handle orientation changes gracefully.
- Use `@AppStorage` for simple user preferences.

## Examples

### Example 1: Basic View with Toolbar

**User Prompt:** "Create a SwiftUI view with a navigation bar and toolbar items using SF Symbols."

**Expected Output:**
```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationView {
            Text("Hello, World!")
                .navigationTitle("My App")
                .toolbar {
                    ToolbarItem(placement: .navigationBarLeading) {
                        Button(action: {
                            // Action for leading button
                        }) {
                            Image(systemName: "line.horizontal.3")
                        }
                    }
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button(action: {
                            // Action for trailing button
                        }) {
                            Image(systemName: "plus")
                        }
                    }
                }
        }
    }
}
```

### Example 2: State Management with @State

**User Prompt:** "Show how to create a toggle button that changes the background color using SwiftUI."

**Expected Output:**
```swift
import SwiftUI

struct ToggleView: View {
    @State private var isOn = false
    
    var body: some View {
        ZStack {
            (isOn ? Color.blue : Color.gray)
                .edgesIgnoringSafeArea(.all)
            
            VStack {
                Text(isOn ? "Light Mode" : "Dark Mode")
                    .foregroundColor(.white)
                    .font(.largeTitle)
                
                Toggle("Toggle Mode", isOn: $isOn)
                    .padding()
                    .toggleStyle(SwitchToggleStyle(tint: .white))
            }
        }
    }
}
```

### Example 3: Using SF Symbols with Custom Styling

**User Prompt:** "How can I display an SF Symbol with custom colors and effects in SwiftUI?"

**Expected Output:**
```swift
import SwiftUI

struct SymbolView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "star.fill")
                .font(.system(size: 50))
                .foregroundColor(.yellow)
            
            Image(systemName: "heart.fill")
                .font(.system(size: 50))
                .foregroundColor(.red)
                .shadow(radius: 5)
            
            Image(systemName: "moon.fill")
                .font(.system(size: 50))
                .foregroundColor(.blue)
                .background(Circle().fill(Color.white).shadow(radius: 3))
                .clipShape(Circle())
        }
    }
}
```

### Example 4: List with Navigation

**User Prompt:** "Generate a SwiftUI list that navigates to detail views."

**Expected Output:**
```swift
import SwiftUI

struct Item: Identifiable {
    let id = UUID()
    let name: String
}

struct ListView: View {
    let items = [Item(name: "Item 1"), Item(name: "Item 2"), Item(name: "Item 3")]
    
    var body: some View {
        NavigationView {
            List(items) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    Text(item.name)
                }
            }
            .navigationTitle("Items")
        }
    }
}

struct DetailView: View {
    let item: Item
    
    var body: some View {
        Text("Detail for \(item.name)")
            .navigationTitle(item.name)
    }
}
```

### Example 5: Form with Validation

**User Prompt:** "Create a SwiftUI form for user input with basic validation."

**Expected Output:**
```swift
import SwiftUI

struct FormView: View {
    @State private var name = ""
    @State private var email = ""
    @State private var isValid = false
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Personal Information")) {
                    TextField("Name", text: $name)
                    TextField("Email", text: $email)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }
                
                Section {
                    Button("Submit") {
                        // Submit action
                    }
                    .disabled(!isValid)
                }
            }
            .navigationTitle("User Form")
            .onChange(of: name) { _ in validateForm() }
            .onChange(of: email) { _ in validateForm() }
        }
    }
    
    private func validateForm() {
        isValid = !name.isEmpty && email.contains("@")
    }
}
```