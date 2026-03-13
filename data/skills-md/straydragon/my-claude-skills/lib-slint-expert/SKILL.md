---

name: lib-slint-expert

description: Comprehensive Slint GUI development expert based on official source code. Covers Rust integration, component design, layouts, styling, animations, cross-platform deployment, and performance optimization. Use when working with Slint UI toolkit, building native GUI applications, or when mentioning Slint, GUI development, or Rust user interfaces. Built with official documentation and examples.

allowed-tools: Read, Write, Edit, Glob, Grep, Bash

---

# Slint GUI Expert

A comprehensive guide for developing modern GUI applications using Slint with Rust. This skill is built directly from the official Slint repository and covers everything from basic component creation to advanced performance optimization and cross-platform deployment.

## 🎯 Getting Started with Official Tutorial

The best way to start is by following the official tutorial:

1. **Start Here**: `@source/docs/astro/src/content/docs/tutorial/quickstart.mdx`
2. **Basic Project**: Use `templates/basic-app/`
3. **Example Study**: Review `@source/examples/memory/`
4. **Reference**: Browse `@source/examples/gallery/`

### Quick Start with Template

```bash
# Use our pre-configured template
cp -r templates/basic-app/ my-first-slint-app/
cd my-first-slint-app/
cargo run
```

## Quick Start

### Basic Slint Application

```rust
// Cargo.toml
[dependencies]
slint = "1.13"

// main.rs
slint::slint! {
    export component AppWindow inherits Window {
        Text {
            text: "Hello, Slint!";
            color: #3498db;
            font-size: 24px;
            horizontal-alignment: center;
        }
    }
}

fn main() -> Result<(), slint::PlatformError> {
    let app = AppWindow::new()?;
    app.run()
}
```

### Project Structure

```
my-slint-app/
├── Cargo.toml
├── build.rs
└── src/
    ├── main.rs
    └── ui/
        └── main.slint
```

## Core Concepts

### 1. Component Architecture

**Component Definition**
```slint
export component Button inherits Rectangle {
    property <string> text: "Click me";
    property <color> background-color: #3498db;
    property <bool> enabled: true;

    callback clicked();

    background: background-color;
    border-radius: 8px;

    Text {
        text: root.text;
        color: enabled ? white : #cccccc;
        horizontal-alignment: center;
        vertical-alignment: center;
    }

    TouchArea {
        enabled: root.enabled;
        clicked => { root.clicked(); }
    }
}
```

**Rust Integration**
```rust
slint::include_modules!();

fn main() -> Result<(), slint::PlatformError> {
    let main_window = MainWindow::new()?;

    let window_weak = main_window.as_weak();
    main_window.on_submit_clicked(move || {
        let window = window_weak.unwrap();
        println!("Submit button clicked!");
    });

    main_window.run()
}
```

### 2. Layout Systems

**VerticalLayout**
```slint
export component LoginScreen inherits Window {
    VerticalLayout {
        spacing: 20px;
        padding: 40px;

        Text {
            text: "Login";
            font-size: 32px;
            font-weight: bold;
        }

        TextInput {
            placeholder-text: "Username";
        }

        TextInput {
            placeholder-text: "Password";
            input-type: password;
        }

        Button {
            text: "Login";
            clicked => { /* login logic */ }
        }
    }
}
```

**GridLayout**
```slint
export component Dashboard inherits Window {
    GridLayout {
        spacing: 10px;
        padding: 20px;

        Row[1, 2, 3] {
            Column[1] {
                Text { text: "Revenue"; }
                Text { text: "$10,234"; font-size: 24px; }
            }
        }
    }
}
```

### 3. Data Binding and State Management

**Properties and Bindings**
```slint
export component Counter inherits Window {
    property <int> count: 0;
    property <string> status: count > 10 ? "High" : "Low";

    VerticalLayout {
        Text {
            text: "Count: " + count;
            font-size: 24px;
        }

        Button {
            text: "+";
            clicked => { count += 1; }
        }
    }
}
```

**Rust State Integration**
```rust
use slint::{SharedString, ModelRc, VecModel};

fn main() -> Result<(), slint::PlatformError> {
    let app = MainWindow::new()?;

    let items = VecModel::from(vec![
        SharedString::from("Item 1"),
        SharedString::from("Item 2"),
    ]);

    app.set_items(ModelRc::new(items));

    app.run()
}
```

### 4. Styling and Themes

**Custom Styling**
```slint
export component ThemedApp inherits Window {
    @theme.primary := #3498db;
    @theme.secondary := #2ecc71;

    background: @theme.background;

    Text {
        text: "Themed Application";
        color: @theme.text;
    }

    Button {
        text: "Primary Action";
        background: @theme.primary;
    }
}
```

### 5. Animations

**Property Animations**
```slint
export component AnimatedButton inherits Rectangle {
    property <color> hover-color: #3498db;
    property <length> scale: 1.0;

    background: hover-color;
    border-radius: 8px;

    animate scale { duration: 200ms; easing: ease-out; }
    animate hover-color { duration: 300ms; }

    TouchArea {
        mouse-entered => {
            root.scale = 1.1;
            root.hover-color = #2980b9;
        }

        mouse-exited => {
            root.scale = 1.0;
            root.hover-color = #3498db;
        }
    }
}
```

## 📚 Official Resources and Learning Materials

### 🎯 Primary Learning Path (Recommended)
1. **Official Tutorial**: `@source/docs/astro/src/content/docs/tutorial/` - Complete memory game tutorial
2. **Working Examples**: `@source/examples/memory/` - Tutorial implementation
3. **Component Reference**: `@source/examples/gallery/` - All UI components
4. **Language Guide**: `@source/docs/astro/src/content/docs/guide/language/` - Complete syntax reference

### 📖 Official Documentation
This skill includes the complete official Slint repository as a git submodule in the `source/` directory:

- **🎓 Tutorial**: `@source/docs/astro/src/content/docs/tutorial/` - Step-by-step learning
- **📋 Language**: `@source/docs/astro/src/content/docs/guide/language/` - Complete language specification
- **🔧 API**: `@source/api/rs/slint/` - Rust API documentation
- **💎 Examples**: `@source/examples/` - Extensive working examples
- **🎨 UI Libraries**: `@source/ui-libraries/` - Material & Fluent components

### 🛠️ Skill-Specific Resources
- **[docs/](docs/README.md)** - Navigation guide for official documentation
- **[examples/](examples/README.md)** - Curated learning paths with official examples
- **[templates/](templates/README.md)** - Ready-to-use project templates
- **[SOURCE_STRUCTURE.md](SOURCE_STRUCTURE.md)** - Complete skill structure mapping

## Quick Reference

### Essential APIs
- `slint::slint!{}` - Define .slint components inline
- `slint::include_modules!()` - Include .slint files from build
- `Component::new()?` - Create component instances
- `window.as_weak()` - Get weak reference for callbacks
- `ModelRc::new(VecModel::from(...))` - Create data models

### Project Structure
```
my-app/
├── Cargo.toml
├── build.rs
├── src/
│   ├── main.rs
│   └── ui/
│       └── main.slint
└── assets/
    ├── icons/
    └── images/
```

### Common Patterns
- Use properties for component configuration
- Prefer composition over inheritance
- Use weak references for callbacks to avoid cycles
- Implement proper error handling in Rust integration

## Troubleshooting

**Common Issues:**
- Compilation errors: Check `.slint` syntax and Rust integration
- Performance issues: Optimize layout complexity and data models
- Memory leaks: Use weak references and proper cleanup
- Platform-specific bugs: Test on target platforms early

**Debug Techniques:**
- Use `slint::debug_log!()` for logging
- Enable debug mode in build configuration
- Test with different rendering backends
- Profile memory usage and rendering performance

> See [references/ADVANCED.md](references/ADVANCED.md) for advanced topics including custom components, performance optimization, and cross-platform development.
> See [references/PATTERNS.md](references/PATTERNS.md) for common UI patterns like forms, navigation, and async operations.
