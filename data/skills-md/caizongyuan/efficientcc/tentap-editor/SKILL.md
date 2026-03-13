---
name: tentap-editor
description: This skill should be used when users need to implement or work with the TenTap rich text editor for React Native. It provides comprehensive guidance on installation, basic setup, advanced customization, API reference, and real-world examples for building rich text editing experiences in mobile applications.
---

# TenTap Editor

A typed, customizable, and extendable rich text editor for React Native built on Tiptap and Prosemirror. TenTap provides a bridge architecture that enables seamless communication between React Native and a web-based editor, offering powerful editing capabilities with native mobile performance.

## Core Functionality

TenTap Editor delivers comprehensive rich text editing capabilities through a WebView-based architecture that bridges React Native and Tiptap. It provides essential features including text formatting (bold, italic, underline, strikethrough), lists (bullet, ordered, task), headings, blockquotes, code blocks, images, links, colors, and highlights. The editor supports custom themes, dark mode, dynamic CSS injection, custom fonts, and full extensibility through custom bridge extensions.

## When to Use

Use TenTap when building mobile applications requiring rich text editing, including chat interfaces, email composers, content management systems, note-taking apps, social media platforms, document editors, or any application where users need to format text beyond plain input. It offers both simple plug-and-play usage for standard features and advanced customization for specialized requirements.

## Quick Start

### Installation

**React Native:**
```bash
yarn add @10play/tentap-editor react-native-webview
cd ios && pod install
```

**Expo:**
```bash
npx expo install @10play/tentap-editor react-native-webview
```

Note: Expo Go supports only basic usage. For advanced features, use Expo Dev Client.

### Basic Setup

The simplest implementation requires three components: `useEditorBridge` hook, `RichText` component, and `Toolbar` component.

```tsx
import { KeyboardAvoidingView, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RichText, Toolbar, useEditorBridge } from '@10play/tentap-editor';

export const BasicEditor = () => {
  const editor = useEditorBridge({
    autofocus: true,
    avoidIosKeyboard: true,
    initialContent: '<p>Start editing!</p>',
  });

  return (
    <SafeAreaView style={styles.fullScreen}>
      <RichText editor={editor} />
      <KeyboardAvoidingView
        behavior="padding"
        style={styles.keyboardAvoidingView}
      >
        <Toolbar editor={editor} />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  fullScreen: { flex: 1 },
  keyboardAvoidingView: {
    position: 'absolute',
    width: '100%',
    bottom: 0,
  },
});
```

This creates a fully functional rich text editor with standard formatting capabilities. See `references/Basic.tsx` for the complete working example.

## Core Concepts

### Bridge Architecture

TenTap uses a bridge pattern to communicate between React Native and the Tiptap editor running in a WebView:

- **EditorBridge**: Main interface providing all editor commands accessible from React Native
- **BridgeExtension**: Typed classes that extend editor functionality by wrapping Tiptap extensions
- **BridgeState**: Real-time state object reflecting the editor's current status

This architecture enables powerful features while maintaining type safety and minimizing WebView-Native communication overhead.

### Usage Patterns

**Simple Usage**: Pre-configured with `TenTapStarterKit` including all standard rich text features. Ideal for most use cases requiring standard formatting capabilities.

**Advanced Usage**: Custom bundling with Vite for full control over the web editor, custom Tiptap extensions, and specialized bridge implementations. Required when adding custom extensions beyond the pre-built bridges.

## Essential APIs

### useEditorBridge Hook

The primary hook for creating and configuring an EditorBridge instance.

**Key Configuration Options:**

- `bridgeExtensions`: Array of BridgeExtensions (default: `TenTapStarterKit`)
- `initialContent`: HTML string or JSON object for initial editor content
- `autofocus`: Auto-focus editor on mount (default: false)
- `avoidIosKeyboard`: Keep cursor visible above keyboard (default: false, works on both iOS and Android)
- `dynamicHeight`: WebView height matches content height (default: false)
- `theme`: Custom theme configuration for native components
- `editable`: Enable/disable editing (default: true)
- `customSource`: Custom HTML string for advanced setups
- `onChange`: Callback fired on content changes
- `DEV` / `DEV_SERVER_URL`: Development mode configuration for advanced setups

```tsx
const editor = useEditorBridge({
  autofocus: true,
  avoidIosKeyboard: true,
  initialContent: '<p>Hello, world!</p>',
  bridgeExtensions: [...TenTapStartKit, CustomBridge],
  onChange: () => {
    // Handle content changes (debounce recommended)
  },
});
```

See `references/useEditorBridge.md` for complete API documentation.

### EditorBridge API

The EditorBridge interface provides comprehensive editor control through the following methods:

**Content Management:**
- `getHTML()`: Promise returning HTML content
- `getText()`: Promise returning plain text content
- `getJSON()`: Promise returning JSON document structure
- `setContent(content)`: Set editor content from HTML or JSON

**Focus & Selection:**
- `focus(pos?)`: Focus editor at optional position
- `blur()`: Remove focus and close keyboard
- `setSelection(from, to)`: Set text selection range

**State Retrieval:**
- `getEditorState()`: Get current BridgeState snapshot
- `webviewRef`: Reference to underlying WebView

**Dynamic Styling:**
- `injectCSS(css, tag?)`: Inject or update CSS stylesheets
- `injectJS(js)`: Execute JavaScript in WebView

**Formatting Commands:**
- `toggleBold()`, `toggleItalic()`, `toggleUnderline()`, `toggleStrikethrough()`
- `toggleHeading(level)`: Set heading level (1-6)
- `toggleCode()`: Toggle inline code
- `toggleBlockquote()`: Toggle blockquote
- `toggleBulletList()`, `toggleOrderedList()`, `toggleTaskList()`
- `setColor(color)`, `unsetColor()`: Set/unset text color
- `setHighlight(color)`, `toggleHighlight(color)`, `unsetHighlight()`: Text highlighting
- `setLink(url)`: Insert/update link
- `setImage(src)`: Insert image

**List Management:**
- `lift()`: Outdent list item
- `sink()`: Indent list item

**History:**
- `undo()`, `redo()`: Navigate history

**Placeholder:**
- `setPlaceholder(text)`: Update placeholder text dynamically

See `references/EditorBridge.md` for complete API reference with all 30+ methods.

### State Management Hooks

**useBridgeState**: Subscribe to real-time editor state changes.

```tsx
const editorState = useBridgeState(editor);

// Access state properties
editorState.isFocused;      // Editor focus state
editorState.isEmpty;        // Whether editor is empty
editorState.isBoldActive;   // Bold formatting state
editorState.canToggleBold;  // Whether bold can be toggled
editorState.headingLevel;   // Current heading level
```

BridgeState includes 30+ properties tracking formatting states, capabilities, and editor status. See `references/BridgeState.md` for complete property listing.

**useEditorContent**: Efficiently retrieve editor content with built-in debouncing.

```tsx
const htmlContent = useEditorContent(editor, { type: 'html' });

// Alternative content types
const textContent = useEditorContent(editor, { type: 'text' });
const jsonContent = useEditorContent(editor, { type: 'json' });

// Custom debounce interval (default: 10ms)
const content = useEditorContent(editor, {
  type: 'html',
  debounceInterval: 100,
});
```

See `references/useEditorContent.md` for complete documentation.

## Components Reference

### RichText Component

The WebView component rendering the Tiptap editor.

**Props:**
- `editor`: EditorBridge instance (required)
- `exclusivelyUseCustomOnMessage`: Override internal onMessage handler (default: true)

Supports all standard React Native WebView props (not recommended unless necessary).

```tsx
<RichText editor={editor} />
```

### Toolbar Component

Pre-built toolbar with context menus for headings and links, plus 20+ toolbar items.

**Props:**
- `editor`: EditorBridge instance (required)
- `hidden`: Control toolbar visibility
- `items`: Array of ToolbarItem configurations (default: DEFAULT_TOOLBAR_ITEMS)
- `shouldHideDisabledToolbarItems`: Hide disabled items instead of graying out (default: false)

**Pre-built Toolbar Items:**
- Formatting: bold, italic, underline, strikethrough, code
- Lists: bulletList, orderedList, checkList
- Structure: quote, h1-h6
- Links: link
- History: undo, redo
- Lists: lift, sink

```tsx
<Toolbar
  editor={editor}
  hidden={!isKeyboardVisible}
  items={DEFAULT_TOOLBAR_ITEMS}
  shouldHideDisabledToolbarItems={true}
/>
```

### Custom Toolbar Items

Create custom toolbar items with the ToolbarItem interface:

```tsx
interface ToolbarItem {
  onPress: ({ editor, editorState }) => () => void;
  active: ({ editor, editorState }) => boolean;
  disabled: ({ editor, editorState }) => boolean;
  image: ({ editor, editorState }) => any;
}
```

See `references/Components.md` for complete component documentation and `references/CustomAndStaticToolbar/` for custom toolbar implementation examples.

## Bridge Extensions

TenTap provides 19 pre-built BridgeExtensions covering standard rich text features:

### Core Extensions
- **CoreBridge**: Document, paragraph, and text extensions
- **PlaceholderBridge**: Placeholder text support
- **DropCursorBridge**: Drag-and-drop cursor indicator

### Text Formatting
- **BoldBridge**: Bold text formatting
- **ItalicBridge**: Italic text formatting
- **UnderlineBridge**: Underline text formatting
- **StrikeBridge**: Strikethrough text formatting
- **CodeBridge**: Inline code formatting
- **ColorBridge**: Text color support
- **HighlightBridge**: Text background highlighting

### Structural Elements
- **HeadingBridge**: Heading levels 1-6
- **BlockquoteBridge**: Blockquote blocks
- **BulletListBridge**: Bulleted lists
- **OrderedListBridge**: Numbered lists
- **TaskListBridge**: Task/check lists
- **ListItemBridge**: List indentation control (lift/sink)

### Media & Links
- **ImageBridge**: Image insertion and manipulation
- **LinkBridge**: Hyperlink support

### History
- **HistoryBridge**: Undo/redo functionality

### Configuring Extensions

Use `configureExtension` to customize Tiptap extension settings:

```tsx
const editor = useEditorBridge({
  bridgeExtensions: [
    ...TenTapStartKit,
    PlaceholderBridge.configureExtension({
      placeholder: 'Type something amazing...',
    }),
    LinkBridge.configureExtension({
      openOnClick: false,
    }),
    HeadingBridge.configureExtension({
      levels: [1, 2, 3],
    }),
  ],
});
```

### Extending Document Schema

Use `extendExtension` to modify the document schema:

```tsx
CoreBridge.extendExtension({
  content: 'heading block+',
});
```

This configures the document to require a heading as the first node.

See `references/BridgeExtensions.md` and `references/configureExtensions.md` for complete extension reference and configuration examples.

## Customization Guide

### Theming

Apply custom themes to native components using the `theme` configuration:

```tsx
const editor = useEditorBridge({
  theme: {
    toolbar: {
      toolbarBody: {
        backgroundColor: '#474747',
        borderTopColor: '#C6C6C6B3',
        borderBottomColor: '#C6C6C6B3',
      },
    },
    webview: {
      backgroundColor: '#1C1C1E',
    },
    webviewContainer: {},
  },
});
```

### Dark Mode

Implement complete dark mode by combining native theme and web CSS:

```tsx
import { darkEditorTheme, darkEditorCss } from '@10play/tentap-editor';

const editor = useEditorBridge({
  bridgeExtensions: [
    ...TenTapStartKit,
    CoreBridge.configureCSS(darkEditorCss),
  ],
  theme: darkEditorTheme,
});
```

See `references/darkTheme.md` and `references/DarkEditor.tsx` for complete dark mode implementation.

### Custom CSS

Override or extend default CSS for any bridge extension:

```tsx
const customCodeCSS = `
code {
  background-color: #ffdede;
  border-radius: 0.25em;
  color: #cd4242;
  padding: 0.25em;
}
`;

const editor = useEditorBridge({
  bridgeExtensions: [
    ...TenTapStartKit,
    CodeBridge.configureCSS(customCodeCSS),
  ],
});
```

### Dynamic CSS Injection

Update CSS at runtime using the `injectCSS` method:

```tsx
// Update bridge-specific CSS
editor.injectCSS(newCSS, CodeBridge.name);

// Add new stylesheet without overriding
editor.injectCSS(customCSS, 'custom-tag');
```

### Custom Fonts

Integrate custom fonts by converting to base64 and configuring via CSS:

1. Convert font files using https://transfonter.org (check base64 option)
2. Export the stylesheet.css as a TypeScript string
3. Configure via CoreBridge CSS:

```tsx
import { customFont } from './font';

const editor = useEditorBridge({
  bridgeExtensions: [
    ...TenTapStartKit,
    CoreBridge.configureCSS(customFont),
  ],
});
```

See `references/customCss.md` and `references/CustomCss.tsx` for complete CSS and font customization examples.

## Advanced Setup

For custom Tiptap extensions or specialized editor behavior, use advanced setup with custom bundling.

### Overview

Advanced setup provides:
- Full control over Tiptap extensions
- Custom bridge implementations
- Specialized editor configurations
- Development server integration

### Process

1. **Create editor-web directory**: Separate folder for web editor code
2. **Configure TypeScript**: Set up web-specific tsconfig.json
3. **Create editor files**: index.html, AdvancedEditor.tsx, index.tsx
4. **Set up Vite**: Configure bundler with module aliases
5. **Add build scripts**: Package.json scripts for dev and production
6. **Import custom bundle**: Use generated HTML with `customSource` prop

### Complete Example

```tsx
// editor-web/AdvancedEditor.tsx
import { EditorContent } from '@tiptap/react';
import { useTenTap, TenTapStartKit } from '@10play/tentap-editor';
import { CounterBridge } from '../CounterBridge';

export const AdvancedEditor = () => {
  const editor = useTenTap({
    bridges: [...TenTapStartKit, CounterBridge],
    tiptapOptions: {
      extensions: [Document, Paragraph, Text],
    },
  });

  return <EditorContent editor={editor} />;
};

// In React Native app
import { editorHtml } from './editor-web/build/editorHtml';

const editor = useEditorBridge({
  customSource: editorHtml,
  // ... other config
});
```

### Creating Custom Bridges

Implement custom bridge extensions for specialized functionality:

```tsx
import { BridgeExtension } from '@10play/tentap-editor';
import { CharacterCount } from '@tiptap/extension-character-count';

export const CounterBridge = new BridgeExtension<
  typeof CharacterCount,
  { words: number; characters: number }
>({
  tiptapExtension: CharacterCount,
  extendEditorState: (editor) => ({
    words: editor.storage.characterCount.words(),
    characters: editor.storage.characterCount.characters(),
  }),
});
```

See `references/advancedSetup.md` and `references/Advanced/` for complete advanced setup instructions and working examples.

## Platform-Specific Considerations

### iOS Keyboard Handling

When using React Navigation headers on iOS, configure `KeyboardAvoidingView` with proper offsets:

```tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Platform } from 'react-native';

const HEADER_HEIGHT = 38;
const { top } = useSafeAreaInsets();
const keyboardVerticalOffset = HEADER_HEIGHT + top;

<KeyboardAvoidingView
  behavior="padding"
  keyboardVerticalOffset={Platform.OS === 'ios' ? keyboardVerticalOffset : undefined}
>
  <Toolbar editor={editor} />
</KeyboardAvoidingView>

// Add paddingBottom to RichText container on iOS
<View style={{ paddingBottom: Platform.OS === 'ios' ? HEADER_HEIGHT : 0 }}>
  <RichText editor={editor} />
</View>
```

See `references/navHeader.md` and `references/NavigationHeader.tsx` for complete iOS keyboard handling examples.

### Avoid iOS Keyboard Option

The `avoidIosKeyboard` option helps keep the cursor visible when the editor is full-screen:

```tsx
const editor = useEditorBridge({
  avoidIosKeyboard: true,  // Works on both iOS and Android
});
```

This automatically:
- Adds bottom padding equal to keyboard height
- Adjusts ProseMirror scroll threshold and margin
- Ensures cursor remains visible during typing

## Example Patterns

### Basic Editor Setup
**File**: `references/Basic.tsx`
Demonstrates the simplest implementation with useEditorBridge, RichText, Toolbar, and KeyboardAvoidingView for keyboard-aware editing.

**Key Concepts**: Hook-based initialization, component composition, iOS keyboard handling, initial content setup

### Dark Mode Editor
**File**: `references/DarkEditor.tsx`
Complete dark theme implementation combining `darkEditorTheme` native theme with `darkEditorCss` web styling, including conditional toolbar visibility based on keyboard and focus state.

**Key Concepts**: Theme configuration, CSS customization, state-driven UI, conditional rendering

### Extension Configuration
**File**: `references/ConfigureExtentions.tsx`
Shows how to configure PlaceholderBridge, LinkBridge, and DropCursorBridge with custom options, plus dynamic content manipulation and placeholder updates.

**Key Concepts**: Extension configuration, option customization, dynamic content updates

### Custom CSS Styling
**File**: `references/CustomCss.tsx`
Demonstrates CSS customization through bridge extensions, dynamic CSS injection using `injectCSS`, and targeting specific bridges with named tags.

**Key Concepts**: CSS configuration, dynamic styling, bridge-specific targeting

### React Navigation Integration
**File**: `references/NavigationHeader.tsx`
Proper toolbar positioning with React Navigation headers using safe area insets and keyboard vertical offset calculation.

**Key Concepts**: Safe area handling, keyboard avoidance, platform-specific logic

### Custom Toolbar Implementation
**Directory**: `references/CustomAndStaticToolbar/`
Build custom email composer interface with static always-visible toolbar and context-aware conditional toolbar, including state machine pattern for toolbar navigation and disabled state handling.

**Key Concepts**: Custom toolbar components, state management, conditional rendering, memoization

### Chat Interface Pattern
**File**: `references/EditorStickToKeyboardExample.tsx`
Chat-like interface with editor attached to keyboard, scrollable message list with WebView HTML rendering, and async content extraction.

**Key Concepts**: Keyboard avoidance, message rendering, content extraction, ScrollView management

### Advanced Rich Text Editor
**File**: `references/Advanced/AdvancedRichText.tsx`
Advanced implementation with custom bridge extensions (CounterBridge), real-time word/character counting, bridge state consumption, and custom HTML source integration.

**Key Concepts**: Custom extensions, state management, computed values, custom source

### Custom Bridge Extension
**File**: `references/Advanced/CounterBridge.ts`
Complete example of creating custom BridgeExtension integrating Tiptap's CharacterCount extension, including TypeScript module augmentation for extending BridgeState and EditorBridge interfaces.

**Key Concepts**: Extension creation, type augmentation, storage access, computed state

### Advanced Web Setup
**Directory**: `references/Advanced/editor-web/`
Full advanced setup with Vite bundling, custom bridge integration, module aliasing for Tiptap compatibility, content injection timing workaround, and React 18 createRoot pattern.

**Key Concepts**: Custom bundling, Vite configuration, bridge composition, module resolution, development workflow

## Resource References

### Documentation Files
- **`references/intro.md`**: Introduction, features, installation, basic usage
- **`references/mainConcepts.md`**: Bridge architecture, simple vs advanced usage patterns
- **`references/basic.md`**: Step-by-step basic editor tutorial
- **`references/customTheme.md`**: Native theme customization guide
- **`references/darkTheme.md`**: Dark mode implementation with theme + CSS
- **`references/customCss.md`**: CSS and font customization, dynamic injection
- **`references/configureExtensions.md`**: Extension configuration and schema extension
- **`references/navHeader.md`**: iOS keyboard handling with React Navigation
- **`references/advancedSetup.md`**: Complete advanced setup guide with Vite

### API References
- **`references/EditorBridge.md`**: Complete EditorBridge interface with 30+ methods
- **`references/BridgeExtensions.md`**: All 19 built-in extensions and configurations
- **`references/BridgeState.md`**: BridgeState properties and useBridgeState hook
- **`references/Components.md`**: RichText, Toolbar, and ToolbarItem components
- **`references/useEditorBridge.md`**: Hook configuration options and usage
- **`references/useEditorContent.md`**: Content retrieval hook with debouncing

### Example Source Code
**Basic Examples**:
- `Basic.tsx` - Simple editor implementation
- `DarkEditor.tsx` - Dark mode editor
- `ConfigureExtentions.tsx` - Extension configuration
- `CustomCss.tsx` - CSS customization
- `NavigationHeader.tsx` - React Navigation integration
- `EditorStickToKeyboardExample.tsx` - Chat interface pattern

**Advanced Examples**:
- `Advanced/AdvancedRichText.tsx` - Advanced editor with custom extensions
- `Advanced/CounterBridge.ts` - Custom bridge extension implementation
- `Advanced/editor-web/` - Complete advanced setup with Vite
  - `index.html` - HTML template
  - `AdvancedEditor.tsx` - Web editor component
  - `index.tsx` - Entrypoint with content injection
  - `tsconfig.json` - TypeScript configuration
  - `vite.config.ts` - Vite bundler configuration

**Custom Toolbar Examples**:
- `CustomAndStaticToolbar/CustomAndStaticToolbar.tsx` - Email composer with custom toolbars
- `CustomAndStaticToolbar/CustomRichText.tsx` - Custom RichText wrapper

**Utility Components**:
- `Icon.tsx` - Reusable SVG icon component
- `font.ts` - Custom font definition (base64)

## Best Practices

### Performance Optimization
- Use `useEditorContent` instead of direct `getHTML()` calls for better performance
- Implement debouncing for onChange handlers to reduce WebView-Native communication
- Avoid unnecessary re-renders by memoizing toolbar items and custom components
- Use `avoidIosKeyboard` option for better typing experience in full-screen editors

### State Management
- Leverage `useBridgeState` for reactive UI updates based on editor state
- Use `onChange` callback with debouncing for auto-save functionality
- Implement proper cleanup for custom bridges and extensions

### Extension Organization
- Spread `TenTapStartKit` before custom extensions to avoid duplication
- Group related configurations in separate files for maintainability
- Use TypeScript for type safety with custom bridges

### Platform Considerations
- Always test keyboard behavior on both iOS and Android
- Configure `keyboardVerticalOffset` when using navigation headers
- Use Platform-specific logic for platform-dependent features
- Test safe area insets on devices with notches

## Common Workflows

### Creating a Chat Interface
Combine keyboard avoidance, message rendering, and content extraction for real-time chat applications. See `references/EditorStickToKeyboardExample.tsx`.

### Building an Email Composer
Implement custom toolbars, formatting controls, and conditional rendering for email composition. See `references/CustomAndStaticToolbar/`.

### Adding Dark Mode Support
Integrate theme and CSS customization for complete dark mode implementation. See `references/DarkEditor.tsx` and `references/darkTheme.md`.

### Creating Custom Extensions
Extend editor functionality with custom bridge extensions and TypeScript augmentation. See `references/Advanced/CounterBridge.ts` and `references/Advanced/AdvancedRichText.tsx`.

### Implementing Auto-Save
Use `useEditorContent` with debouncing for efficient content synchronization.

```tsx
const content = useEditorContent(editor, { type: 'html' });

useEffect(() => {
  if (content) {
    debouncedSave(content);
  }
}, [content]);
```

## Additional Resources

- **Official Documentation**: https://10play.github.io/10tap-editor/docs/intro.html
- **Advanced Example Repository**: https://github.com/10play/10TapAdvancedExample
- **Tiptap Documentation**: https://tiptap.dev/docs/editor/introduction
- **React Native WebView**: https://github.com/react-native-webview/react-native-webview
