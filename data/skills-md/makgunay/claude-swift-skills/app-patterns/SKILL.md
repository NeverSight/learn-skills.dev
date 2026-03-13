---
name: app-patterns
description: "Reusable UI patterns for macOS/iOS utility apps built with SwiftUI and Liquid Glass. Includes complete implementations for: Spotlight-style quick access panels with keyboard navigation, NavigationSplitView sidebar + detail layouts, floating editor panels, compact grid palettes with hover morphing, Settings forms with glass sections, toast/notification overlays, variable placeholder systems (detection, input UI, syntax highlighting, autocomplete), template pickers, rich multi-format clipboard copy (plain + HTML + RTF), and diff views. Also covers anti-patterns (glass overload, glass on dark backgrounds). Use when building prompt managers, clipboard utilities, text expanders, launchers, snippet tools, or any keyboard-driven macOS utility. Use alongside liquid-glass for the design system and appkit-bridge for NSPanel/NSStatusItem."
---

# App UI Patterns

Reusable UI patterns for utility apps — prompt managers, clipboard tools, text expanders, and launchers. All patterns use Liquid Glass and assume macOS 26+ / iOS 26+.

## Pattern Index

| Pattern | When to Use | Key Skill Dependencies |
|---------|-------------|----------------------|
| Spotlight Quick Access | Hotkey → search → select → action | global-hotkeys, appkit-bridge |
| Category Sidebar | Main app window, content browsing | swiftui-core |
| Floating Editor | Edit content in overlay panel | appkit-bridge |
| Compact Palette | Grid selection without search | liquid-glass |
| Settings Form | App preferences | macos-app-structure |
| Toast Notification | Ephemeral feedback after actions | — |
| Variable System | `{{placeholder}}` detection, input, highlighting | — |
| Template Picker | Create from predefined templates | — |
| Rich Copy | Multi-format clipboard (plain + HTML + RTF) | pasteboard-textinsertion |
| Diff View | Version comparison | — |

## Pattern 1: Spotlight-Style Quick Access

The core pattern for hotkey-triggered search → select → action.

See `references/spotlight-panel.md` for complete implementation.

### Key Behaviors
- Search field auto-focuses on appear
- Arrow keys navigate results, Enter selects, Escape dismisses
- ⌘Enter for alternate action (e.g., copy instead of paste)
- Selection morphs between rows via `.glassEffectID`
- Results scroll to keep selection visible
- Empty state shown when search has no matches

### Structure
```swift
struct QuickAccessPanel: View {
    @State private var query = ""
    @State private var selectedIndex = 0
    @FocusState private var searchFocused: Bool
    @Namespace private var selection

    var body: some View {
        VStack(spacing: 0) {
            // Search bar with glass
            searchBar
                .glassEffect(.regular, in: .rect(cornerRadius: 14))
            // Results list with morphing selection
            resultsList
                .glassEffect(.clear, in: .rect(cornerRadius: 14))
        }
        .frame(width: 600)
        .onAppear { searchFocused = true }
        .onKeyPress { handleKeyPress($0) }
    }
}
```

### Keyboard Handling
```swift
func handleKeyPress(_ press: KeyPress) -> KeyPress.Result {
    switch press.key {
    case .upArrow:
        selectedIndex = max(0, selectedIndex - 1)
        return .handled
    case .downArrow:
        selectedIndex = min(filtered.count - 1, selectedIndex + 1)
        return .handled
    case .escape:
        onDismiss()
        return .handled
    case .return where press.modifiers.contains(.command):
        copyToClipboard(filtered[safe: selectedIndex])
        return .handled
    default:
        return .ignored
    }
}
```

## Pattern 2: Category Sidebar

Three-column NavigationSplitView for the main app window.

```swift
struct MainView: View {
    @State private var selectedCategory: Category?
    @State private var selectedPrompt: Prompt?

    var body: some View {
        NavigationSplitView {
            CategorySidebar(selection: $selectedCategory)
        } content: {
            PromptList(category: selectedCategory, selection: $selectedPrompt)
        } detail: {
            if let prompt = selectedPrompt {
                PromptEditor(prompt: prompt)
            } else {
                ContentUnavailableView("Select a Prompt", systemImage: "text.quote")
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

### Sidebar with Glass Selection Morphing
```swift
struct CategorySidebar: View {
    @Binding var selection: Category?
    @Namespace private var categorySelection

    var body: some View {
        GlassEffectContainer {
            List(selection: $selection) {
                Section("Categories") {
                    ForEach(categories) { category in
                        Label(category.name, systemImage: category.icon)
                            .tag(category)
                            .listRowBackground(
                                selection == category ?
                                    RoundedRectangle(cornerRadius: 8)
                                        .glassEffect(.regular.tint(category.color.opacity(0.3)))
                                        .glassEffectID("category", in: categorySelection)
                                    : nil
                            )
                    }
                }
                Section("Smart Lists") {
                    Label("Favorites", systemImage: "star")
                    Label("Recent", systemImage: "clock")
                }
            }
        }
    }
}
```

## Pattern 3: Floating Editor Panel

For editing content in an overlay. Pairs with `appkit-bridge` NSPanel.

```swift
struct FloatingEditorView: View {
    @Bindable var prompt: Prompt
    @State private var isPreviewExpanded = false
    @Namespace private var editor

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Title field
                TextField("Prompt title", text: $prompt.title)
                    .textFieldStyle(.plain)
                    .font(.title3)
                    .padding(12)
                    .glassEffect(.clear, in: .rect(cornerRadius: 10))

                // Content editor
                TextEditor(text: $prompt.content)
                    .font(.body)
                    .scrollContentBackground(.hidden)
                    .padding(12)
                    .frame(minHeight: 200)
                    .glassEffect(.clear, in: .rect(cornerRadius: 10))

                // Expandable preview
                Button {
                    withAnimation(.spring(response: 0.3)) {
                        isPreviewExpanded.toggle()
                    }
                } label: {
                    HStack {
                        Image(systemName: "eye")
                        Text("Preview")
                        Spacer()
                        Image(systemName: "chevron.right")
                            .rotationEffect(.degrees(isPreviewExpanded ? 90 : 0))
                    }
                }
                .buttonStyle(.glass)

                if isPreviewExpanded {
                    Text(prompt.content)
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .glassEffect(.regular.tint(.green.opacity(0.2)), in: .rect(cornerRadius: 10))
                        .transition(.opacity.combined(with: .move(edge: .top)))
                }
            }
            .padding()
        }
        .frame(width: 500, height: isPreviewExpanded ? 600 : 450)
    }
}
```

## Pattern 4: Compact Grid Palette

Grid selection with hover morphing. Good for quick access without search.

```swift
struct PromptPalette: View {
    let prompts: [Prompt]
    @State private var hoveredPrompt: Prompt?
    @Namespace private var hover
    var onSelect: (Prompt) -> Void

    var body: some View {
        GlassEffectContainer(spacing: 8) {
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 120))], spacing: 8) {
                ForEach(prompts) { prompt in
                    VStack(spacing: 8) {
                        Image(systemName: prompt.icon)
                            .font(.title)
                            .foregroundStyle(prompt.categoryColor)
                        Text(prompt.title)
                            .font(.caption).fontWeight(.medium)
                            .lineLimit(2).multilineTextAlignment(.center)
                    }
                    .frame(width: 100, height: 80).padding(8)
                    .glassEffect(.regular, in: .rect(cornerRadius: 12))
                    .scaleEffect(hoveredPrompt == prompt ? 1.05 : 1.0)
                    .onHover { isHovered in
                        withAnimation(.easeOut(duration: 0.15)) {
                            hoveredPrompt = isHovered ? prompt : nil
                        }
                    }
                    .onTapGesture { onSelect(prompt) }
                    .background {
                        if hoveredPrompt == prompt {
                            RoundedRectangle(cornerRadius: 12)
                                .glassEffect(.regular.tint(.accentColor.opacity(0.3)))
                                .glassEffectID("hover", in: hover)
                        }
                    }
                }
            }
            .padding()
        }
        .glassEffect(.clear, in: .rect(cornerRadius: 16))
    }
}
```

## Pattern 5: Settings Form with Glass Sections

```swift
struct SettingsView: View {
    @AppStorage("hotkeyModifiers") var hotkeyModifiers: Int = 0
    @AppStorage("hotkeyKey") var hotkeyKey: Int = 49
    @AppStorage("launchAtLogin") var launchAtLogin = false
    @AppStorage("showInDock") var showInDock = false

    var body: some View {
        Form {
            Section {
                HotkeyRecorder(modifiers: $hotkeyModifiers, key: $hotkeyKey)
            } header: {
                Label("Global Hotkey", systemImage: "keyboard")
            }
            .listRowBackground(
                RoundedRectangle(cornerRadius: 10)
                    .glassEffect(.clear).padding(.vertical, 2)
            )

            Section {
                Toggle("Launch at Login", isOn: $launchAtLogin)
                Toggle("Show in Dock", isOn: $showInDock)
            } header: {
                Label("Behavior", systemImage: "gearshape")
            }
            .listRowBackground(
                RoundedRectangle(cornerRadius: 10)
                    .glassEffect(.clear).padding(.vertical, 2)
            )
        }
        .formStyle(.grouped)
        .frame(width: 450, height: 350)
    }
}
```

## Pattern 6: Toast Notification

Ephemeral feedback overlay with auto-dismiss.

```swift
struct ToastView: View {
    let message: String
    let icon: String

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: icon).font(.title3)
            Text(message).fontWeight(.medium)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .glassEffect(.regular.tint(.green.opacity(0.3)), in: .capsule)
    }
}

// Toast hosting in parent view
struct ContentView: View {
    @State private var showToast = false
    @State private var toastMessage = ""

    var body: some View {
        ZStack(alignment: .bottom) {
            MainContent()
            if showToast {
                ToastView(message: toastMessage, icon: "checkmark.circle")
                    .transition(.move(edge: .bottom).combined(with: .opacity))
                    .padding(.bottom, 40)
            }
        }
        .animation(.spring(response: 0.3), value: showToast)
    }

    func showToast(_ message: String) {
        toastMessage = message
        showToast = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) { showToast = false }
    }
}
```

## Variable Placeholder System

### Detection & Expansion
```swift
extension Prompt {
    /// Extract {{variable}} names from content
    var detectedVariables: [String] {
        let pattern = #"\{\{(\w+)\}\}"#
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(content.startIndex..., in: content)
        let matches = regex?.matches(in: content, range: range) ?? []
        return matches.compactMap { match in
            Range(match.range(at: 1), in: content).map { String(content[$0]) }
        }
    }

    /// Fill variables and return expanded content
    func filled(with values: [String: String]) -> String {
        var result = content
        for (name, value) in values {
            result = result.replacingOccurrences(of: "{{\(name)}}", with: value)
        }
        return result
    }
}
```

### Variable Input UI
```swift
struct QuickVariablePopover: View {
    let variables: [String]
    @State private var values: [String: String] = [:]
    @FocusState private var focusedField: String?
    var onComplete: ([String: String]) -> Void

    var body: some View {
        VStack(spacing: 12) {
            ForEach(Array(variables.enumerated()), id: \.element) { index, variable in
                HStack {
                    Text(variable.capitalized)
                        .frame(width: 100, alignment: .trailing)
                        .foregroundStyle(.secondary)
                    TextField("", text: binding(for: variable))
                        .textFieldStyle(.plain).padding(8)
                        .glassEffect(.clear, in: .rect(cornerRadius: 8))
                        .focused($focusedField, equals: variable)
                        .onSubmit {
                            if index < variables.count - 1 {
                                focusedField = variables[index + 1]
                            } else { onComplete(values) }
                        }
                }
            }
            HStack {
                Spacer()
                Button("Fill & Copy") { onComplete(values) }
                    .buttonStyle(.glassProminent)
                    .keyboardShortcut(.return, modifiers: .command)
            }
        }
        .padding().frame(width: 350)
        .onAppear { focusedField = variables.first }
    }

    func binding(for variable: String) -> Binding<String> {
        Binding(get: { values[variable] ?? "" }, set: { values[variable] = $0 })
    }
}
```

### Syntax Highlighting for Variables
```swift
struct HighlightedPromptView: View {
    let content: String

    var body: some View {
        Text(attributedContent).textSelection(.enabled)
    }

    var attributedContent: AttributedString {
        var attributed = AttributedString(content)
        let pattern = #"\{\{(\w+)\}\}"#
        if let regex = try? NSRegularExpression(pattern: pattern) {
            let range = NSRange(content.startIndex..., in: content)
            for match in regex.matches(in: content, range: range).reversed() {
                if let swiftRange = Range(match.range, in: content),
                   let attrRange = Range(swiftRange, in: attributed) {
                    attributed[attrRange].foregroundColor = .accentColor
                    attributed[attrRange].backgroundColor = .accentColor.opacity(0.1)
                    attributed[attrRange].font = .body.monospaced()
                }
            }
        }
        return attributed
    }
}
```

## Rich Multi-Format Copy

Copy as plain text + HTML + RTF so paste works well in any app.

```swift
#if os(macOS)
func copyRich(_ content: String) {
    let pasteboard = NSPasteboard.general
    pasteboard.clearContents()

    // Plain text
    pasteboard.setString(content, forType: .string)

    // HTML (for rich text apps like Mail, Pages)
    let html = convertToHTML(content)
    if let htmlData = html.data(using: .utf8) {
        pasteboard.setData(htmlData, forType: .html)
    }

    // RTF
    let attributed = NSAttributedString(
        string: content,
        attributes: [.font: NSFont.systemFont(ofSize: 14), .foregroundColor: NSColor.textColor]
    )
    if let rtfData = try? attributed.data(
        from: NSRange(location: 0, length: attributed.length),
        documentAttributes: [.documentType: NSAttributedString.DocumentType.rtf]
    ) {
        pasteboard.setData(rtfData, forType: .rtf)
    }
}
#endif
```

## Anti-Patterns

### ❌ Glass Overload
```swift
// Too much glass — confusing and poor performance
VStack {
    header.glassEffect()
    content.glassEffect()  // ❌ Content shouldn't be glass
    footer.glassEffect()
}
.glassEffect()  // ❌ Nested glass
```

### ✅ Targeted Glass
```swift
VStack {
    header.glassEffect()    // ✅ Navigation/chrome only
    content                 // ✅ Content is clear
    actionBar.glassEffect() // ✅ Floating actions
}
```

### ❌ Glass on Dark Backgrounds
```swift
ZStack {
    Color.black
    Text("Hard to see").glassEffect()  // ❌ Glass needs varied background
}
```

### ✅ Rich Backgrounds
```swift
ZStack {
    Image("wallpaper").resizable()
    Text("Easy to read").glassEffect()  // ✅ Glass shines on varied imagery
}
```
