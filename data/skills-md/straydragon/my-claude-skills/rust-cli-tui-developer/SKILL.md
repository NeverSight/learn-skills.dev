---
name: rust-cli-tui-developer
description: Expert guidance for Rust CLI and TUI development with official examples from clap, inquire, and ratatui libraries. Use when building command-line interfaces, terminal user interfaces, or console applications in Rust. Provides structured patterns, best practices, and real code implementations from official sources.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Rust CLI/TUI Developer

Expert guidance for building modern command-line interfaces and terminal user interfaces in Rust, using the most popular libraries: **clap** for CLI argument parsing, **inquire** for interactive prompts, and **ratatui** for rich terminal UIs.

This skill provides structured patterns, best practices, and real implementations from the official source code of these libraries.

## 🚀 Quick Start Library Selection

### Choose Your Library Stack

| Need | Primary Library | Complementary | Use Case |
|------|----------------|---------------|----------|
| **CLI Arguments** | `clap` | - | Command-line parsing, help generation |
| **Interactive Prompts** | `inquire` | - | User input, menus, selections |
| **Rich Terminal UI** | `ratatui` | `crossterm` | Complex layouts, real-time updates |
| **Full App** | `clap` + `inquire` + `ratatui` | - | Complete interactive console applications |

### Library Integration Workflow

1. **Add dependencies using cargo add**:
   ```bash
   # For CLI argument parsing
   cargo add clap --features derive

   # For interactive prompts and user input
   cargo add inquire

   # For rich terminal interfaces
   cargo add ratatui

   # For cross-platform terminal handling
   cargo add crossterm
   ```

2. **Explore official examples**:
   - **CLI patterns**: See `@source/clap/examples/` for comprehensive usage examples
   - **Interactive workflows**: Check `@source/inquire/examples/` for prompt patterns
   - **TUI patterns**: Review `@source/ratatui/examples/apps/` for complete applications

3. **Combine libraries** based on your application needs - start simple and add complexity incrementally.

## 📚 Official Resources

### Primary Documentation Sources
This skill includes complete official source code via git submodules in the `source/` directory:

- **`@source/clap/`** - Complete clap CLI parser library with examples
- **`@source/inquire/`** - Interactive prompt library with demo applications
- **`@source/ratatui/`** - Rich TUI framework with example applications

### Quick Navigation to Official Examples
- **CLI Examples**: `@source/clap/examples/`
- **Interactive Prompts**: `@source/inquire/examples/`
- **TUI Applications**: `@source/ratatui/examples/`

## 🛠️ Library-Specific Guides

### 1. Clap - Command Line Argument Parsing

**Core Capabilities**
- **Derive macros** for automatic argument parsing with minimal boilerplate
- **Subcommand support** for complex CLI interfaces like git or cargo
- **Argument validation** with custom parsers and validation functions
- **Help generation** with automatic --help and --version support
- **Configuration overrides** through environment variables and config files

**Key Patterns to Explore**
- Basic argument parsing with derive macros: `@source/clap/examples/derive_ref/`
- Advanced subcommand structures: `@source/clap/examples/tutorial_derive/04_04_subcommands.rs`
- Custom validation and parsing: `@source/clap/examples/tutorial_derive/04_02_validate.rs`
- Complex argument relationships: `@source/clap/examples/tutorial_derive/04_03_relations.rs`

**Common Use Cases**
- Simple flag-based tools (similar to `ls`, `grep`)
- Package managers with subcommands (similar to `cargo`, `npm`)
- Configuration-driven applications
- Data processing pipelines with multiple input sources

### 2. Inquire - Interactive Prompts

**Interactive Input Capabilities**
- **Text input** with validation, placeholders, and help messages
- **Single selection** from predefined options with search functionality
- **Multi-selection** with checkbox-style interface
- **Confirmation prompts** for yes/no decisions
- **Custom types** with validation and formatting
- **Form builders** for complex multi-field input flows

**Key Patterns to Explore**
- Basic input types and validation: `@source/inquire/examples/text_simple.rs`, `@source/inquire/examples/select.rs`
- Multi-select and complex selections: `@source/inquire/examples/multiselect.rs`, `@source/inquire/examples/enum_comprehensive.rs`
- Custom validation and types: `@source/inquire/examples/custom_type.rs`, `@source/inquire/examples/date.rs`
- Complex form workflows: `@source/inquire/examples/form.rs`, `@source/inquire/examples/expense_tracker.rs`
- Password and secure input: `@source/inquire/examples/password_simple.rs`, `@source/inquire/examples/password_full_featured.rs`

**Common Use Cases**
- Configuration wizards and setup flows
- Database connection configuration
- API client initialization
- User onboarding sequences
- Data filtering and selection interfaces

### 3. Ratatui - Terminal User Interfaces

**Rich Terminal UI Capabilities**
- **Layout system** with flexible constraints and responsive design
- **Widget library** for common UI components (lists, tables, charts, etc.)
- **Event handling** with keyboard and mouse support
- **Real-time updates** with animation and progress indicators
- **Cross-platform** terminal management with crossterm backend
- **Custom widgets** through extensible widget traits

**Key Patterns to Explore**
- Basic layout and widget usage: `@source/ratatui/examples/apps/advanced-widget-impl/`
- Complex application structure: `@source/ratatui/examples/apps/async-github/`
- Data visualization and charts: `@source/ratatui/examples/apps/chart/`
- Custom drawing and graphics: `@source/ratatui/examples/apps/canvas/`
- Color themes and styling: `@source/ratatui/examples/apps/color-explorer/`
- Constraint-based layouts: `@source/ratatui/examples/apps/constraint-explorer/`
- Real-time data display: `@source/ratatui/examples/apps/calendar-explorer/`

**Common Use Cases**
- System monitoring dashboards
- Log viewers and search interfaces
- Database query tools
- File managers and explorers
- Development IDEs and editors
- Data analysis and visualization tools
- Game interfaces and interactive applications

## 🏗️ Complete Application Patterns

### Application Architecture Overview

**CLI App with Configuration**
- **Structure**: Main CLI with subcommands for different operations
- **Configuration**: JSON/TOML config files with CLI overrides
- **Features**: Logging, error handling, validation
- **Examples**: Study `@source/clap/examples/cargo-example.rs` for patterns

**Interactive CLI with Prompts**
- **Flow**: CLI args → interactive prompts → confirmation → execution
- **Features**: Progressive disclosure, validation, defaults, help text
- **State Management**: Collect information step-by-step with back/forward navigation
- **Examples**: Explore `@source/inquire/examples/form.rs` for complex flows

**Full TUI Application**
- **Architecture**: Event loop with state management and UI rendering
- **Components**: Multiple screens/widgets with navigation between them
- **State**: Application state separated from rendering logic
- **Examples**: Study `@source/ratatui/examples/apps/async-github/` for async patterns

### Integration Patterns

**Library Combination Strategies**
1. **CLI-first**: Start with clap, add inquire for interactive configuration
2. **Progressive Enhancement**: CLI → CLI + prompts → full TUI
3. **Hybrid Apps**: CLI for automation, interactive mode for manual use

**Common Integration Points**
- Configuration validation (clap + inquire)
- Progress indication (clap + ratatui)
- Setup wizards (inquire + ratatui)
- Admin interfaces (clap + ratatui)

### Development Workflow

**Start Simple, Add Complexity**
1. **Phase 1**: Basic CLI with clap
2. **Phase 2**: Add interactive prompts where needed
3. **Phase 3**: Add TUI for complex operations
4. **Phase 4**: Advanced features (async, plugins, etc.)

**Example-Based Learning**
- Study `@source/clap/examples/` for CLI patterns
- Review `@source/inquire/examples/` for interaction flows
- Analyze `@source/ratatui/examples/apps/` for complete applications

### Real-World Application Types

**Development Tools**
- Package managers (cargo, npm-style)
- Build systems and generators
- Code analysis and linting tools
- Database migration tools

**System Administration**
- Log analysis and filtering tools
- Configuration management utilities
- System monitoring dashboards
- Deployment automation tools

**Data Processing**
- ETL pipelines with interactive configuration
- Data validation and cleaning tools
- Report generation utilities
- File processing batch tools

**Interactive Applications**
- Text editors and IDEs
- File managers
- Game interfaces
- Educational tools

Focus on understanding the patterns from the official examples rather than copying specific implementations. The source code provides the most up-to-date and comprehensive examples of best practices.

## 🎯 Best Practices

### CLI Design Principles

1. **Follow POSIX conventions**: Use `-` for short options, `--` for long options
2. **Provide helpful defaults**: Make reasonable default choices
3. **Clear help text**: Explain what each option does
4. **Consistent interface**: Follow established patterns from tools like `git`, `cargo`
5. **Error handling**: Provide clear error messages and exit codes

### Interactive Prompt Guidelines

1. **Progressive disclosure**: Start simple, add complexity as needed
2. **Provide defaults**: Make it easy to accept reasonable choices
3. **Validation**: Give immediate feedback on invalid input
4. **Escape hatches**: Always allow users to exit or skip
5. **Context preservation**: Remember previous answers when possible

### TUI Development Tips

1. **Responsive layouts**: Handle terminal resizing gracefully
2. **Keyboard shortcuts**: Provide intuitive key bindings
3. **Visual hierarchy**: Use colors and borders to organize information
4. **Performance**: Update efficiently, don't block the main thread
5. **Accessibility**: Consider users with different needs

## 🔧 Development Workflow

### Setting Up Your Development Environment

```bash
# Create new Rust project
cargo new my-cli-app
cd my-cli-app

# Add dependencies to Cargo.toml
cargo add clap --features derive
cargo add inquire
cargo add ratatui crossterm

# For development
cargo add --dev anyhow # Better error handling
cargo add --dev pretty_assertions # Better test output
```

### Testing Your CLI

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use clap::Parser;

    #[test]
    fn test_cli_parsing() {
        let cli = Cli::try_parse_from(&["my-app", "--verbose", "build"]).unwrap();
        assert!(matches!(cli.command, Commands::Build { .. }));
        assert_eq!(cli.verbose, 1);
    }

    #[test]
    fn test_help_generation() {
        // This tests that help doesn't panic
        let _ = Cli::try_parse_from(&["my-app", "--help"]);
    }
}
```

### Building for Distribution

```toml
# Cargo.toml release profile
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = "abort"
strip = true
```

```bash
# Build optimized binary
cargo build --release

# Cross-compile for different targets (requires target toolchains)
cargo build --target x86_64-unknown-linux-musl --release
cargo build --target aarch64-apple-darwin --release
```

## 🚀 Deployment and Distribution

### Installation Options

```bash
# Install from crates.io
cargo install my-cli-app

# Install from git repository
cargo install --git https://github.com/user/my-cli-app.git

# Local development installation
cargo install --path .
```

### Distribution with GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Build binary
        run: cargo build --release --target x86_64-unknown-linux-musl

      - name: Upload release asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: target/x86_64-unknown-linux-musl/release/my-cli-app
          asset_name: my-cli-app-linux
          asset_content_type: application/octet-stream
```

## 📖 Learning Resources

### Official Documentation Paths
- **Clap Guide**: `@source/clap/docs/guide/`
- **Clap Examples**: `@source/clap/examples/`
- **Inquire Examples**: `@source/inquire/examples/`
- **Ratatui Examples**: `@source/ratatui/examples/`

### Community Resources
- [Rust CLI Working Group](https://github.com/rust-cli)
- [Awesome Rust CLI](https://github.com/rust-cli/awesome-rust-cli)
- [Rust TUI Resources](https://github.com/rhysd/awesome-tui-rs)

---

This skill provides comprehensive guidance for Rust CLI and TUI development. Start with the **🚀 Quick Start Library Selection** section to choose the right libraries for your use case, then explore the detailed examples from the official source code included in the `source/` directory.