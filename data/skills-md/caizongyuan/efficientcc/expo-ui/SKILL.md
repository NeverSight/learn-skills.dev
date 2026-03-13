---
name: expo-ui
description: This skill should be used when users need to work with Expo UI (@expo/ui) for integrating SwiftUI components into React Native applications. It provides comprehensive guidance on installation, Host component, SwiftUI primitives, layouts, modifiers, native tabs navigation, and v10 preview features.
---

# Expo UI

## Core Functionality

Expo UI brings native SwiftUI components to React Native, providing a 1-to-1 mapping to SwiftUI views for building modern iOS, macOS, and tvOS interfaces. Use Expo UI to leverage SwiftUI's declarative syntax and native performance while maintaining React Native's flexibility.

> Available in SDK 54 and above.

## When to Use

Use this skill when:
- Building native iOS interfaces with SwiftUI components from React Native
- Integrating SwiftUI primitives like Button, Form, List, TextField, Picker
- Creating layouts with HStack, VStack, and Spacer
- Applying SwiftUI modifiers for styling and behavior
- Working with glass morphism effects and advanced form controls (v10 preview)
- Implementing native tab navigation with Expo Router
- Mixing SwiftUI components with React Native views

## Platform Support

**Supported Platforms:**
- iOS (primary platform)
- macOS
- tvOS

**Requirements:**
- SDK 54+
- Development builds (not available in Expo Go)
- iOS 26+ and Xcode 26+ for `glassEffect` modifier

> **Roadmap:** Android (Jetpack Compose) and Web (DOM) support planned for future releases.

## Version Notice

> ⚠️ **Version Conflict**: Official documentation is based on v9 (stable, ~0.2.0-beta.7). Local examples use v10 which may contain breaking changes. Always check TypeScript types for current API signatures.
>
> When using v10 preview features (marked with ⚠️), be aware that APIs may differ from v9 stable documentation.

## Installation

Install the package in your Expo project:

```bash
npx expo install @expo/ui
```

For existing React Native apps, ensure `expo` is installed first.

## Module Overview

### Getting Started Module
- **Focus:** Installation, SDK requirements, platform support
- **Key APIs:** @expo/ui, @expo/ui/swift-ui, Host component
- **Documentation:** `references/expo-ui-guide.md`

### Core Components Module
- **Functionality:** Basic SwiftUI primitives and Host container
- **Key APIs:** Host, Button, Text, Image, CircularProgress, LinearProgress
- **Documentation:** `references/expo-ui-api-reference.md`

### Layouts Module
- **Functionality:** SwiftUI layout system and container components
- **Key APIs:** HStack, VStack, Form, Section, List, Spacer
- **Documentation:** `references/expo-ui-guide.md`, `references/expo-ui-api-reference.md`

### Input Controls Module
- **Functionality:** User input and selection components
- **Key APIs:** Picker, Slider, Switch, TextField, ColorPicker, DateTimePicker
- **Documentation:** `references/expo-ui-api-reference.md`, `references/expo-ui-v10-examples.md`

### Advanced Components Module
- **Functionality:** Specialized UI components
- **Key APIs:** BottomSheet, ContextMenu, Gauge, CircularProgress, LinearProgress
- **Documentation:** `references/expo-ui-api-reference.md`

### Modifiers Module
- **Functionality:** SwiftUI modifier system for styling and behavior
- **Key APIs:** padding, frame, background, glassEffect, buttonStyle, controlSize
- **Documentation:** `references/expo-ui-guide.md`, `references/expo-ui-v10-examples.md`

### v10 Preview Module
- **Functionality:** Preview features in v10 (may contain breaking changes)
- **Key APIs:** GlassEffectContainer, LabeledContent, DisclosureGroup, ContentUnavailableView
- **Documentation:** `references/expo-ui-v10-examples.md`

### Interop Module
- **Functionality:** Integration between React Native and SwiftUI
- **Key APIs:** Host, UIHostingController, UIViewRepresentable
- **Documentation:** `references/expo-ui-guide.md`

## Core Concepts

### Host Component

The `<Host>` component bridges React Native (UIKit) and SwiftUI. Use `UIHostingController` to render SwiftUI views within React Native.

**Key characteristics:**
- Acts like `<svg>` in DOM or `<Canvas>` in react-native-skia
- Accepts `style` prop for flexbox layouts
- Use `matchContents` prop to size to children
- Required to enter SwiftUI context

**Basic usage:**

```jsx
import { CircularProgress, Host } from '@expo/ui/swift-ui';

<Host matchContents>
  <CircularProgress />
</Host>
```

**With flexbox layout:**

```jsx
<Host style={{ flex: 1, margin: 32 }}>
  <VStack spacing={32}>
    <Text>Hello, world!</Text>
    <Button onPress={handlePress}>Click</Button>
  </VStack>
</Host>
```

### Layout System

SwiftUI uses a different layout system than React Native's flexbox. Use these components for layouts:

**HStack and VStack:**
- Arrange children horizontally or vertically
- Use `spacing` prop for consistent gaps
- Supports nesting for complex layouts

```jsx
import { HStack, VStack, Spacer } from '@expo/ui/swift-ui';

<VStack spacing={16}>
  <HStack spacing={8}>
    <Text>Label</Text>
    <Spacer />
    <Switch value={enabled} onValueChange={setEnabled} />
  </HStack>
</VStack>
```

**Form and Section:**
- Group related controls together
- Automatically styled for iOS Settings appearance
- Use `<Section>` to create grouped content

```jsx
<Form>
  <Section>
    <Text>Settings</Text>
    <Switch label="Airplane Mode" value={mode} onValueChange={setMode} />
  </Section>
</Form>
```

**Important:** Flexbox styles only work on `<Host>` component, not inside SwiftUI context. Use `HStack`/`VStack` for layouts once inside SwiftUI.

### Modifiers System

SwiftUI modifiers customize appearance and behavior. Import from `@expo/ui/swift-ui/modifiers` and apply via `modifiers` prop.

```jsx
import { Text, Host } from '@expo/ui/swift-ui';
import { padding, frame, background } from '@expo/ui/swift-ui/modifiers';

<Text
  size={32}
  modifiers={[
    padding({ all: 16 }),
    frame({ width: 200, height: 100 }),
    background('#007aff')
  ]}>
  Styled Text
</Text>
```

**Common modifiers:**
- `padding()` - Add insets around content
- `frame()` - Set explicit dimensions
- `background()` - Set background color or content
- `clipShape()` - Clip to shapes (roundedRectangle, circle, etc.)

## Components

### Basic Components

#### Button

**Platform:** iOS, tvOS (borderless variant not available on Apple TV)

```jsx
import { Button, Host } from '@expo/ui/swift-ui';

<Host style={{ flex: 1 }}>
  <Button variant="default" onPress={handlePress}>
    Edit profile
  </Button>
</Host>
```

**Props:**
- `onPress?: () => void` - Callback when button is pressed
- `systemImage?: SFSymbol` - SF Symbol name (only used if children is a string)
- `role?: 'default' | 'cancel' | 'destructive'` - Button role (iOS only)
- `controlSize?: 'mini' | 'small' | 'regular' | 'large' | 'extraLarge'` - Control size
- `variant?: ButtonVariant` - Button style variant
- `children?: string | React.ReactNode` - Button content
- `color?: string` - Button color
- `disabled?: boolean` - Disabled state

**Variants:** default, bordered, borderless, borderedProminent, plain, glass, glassProminent, accessoryBar, accessoryBarAction, card, link

#### Text

**Platform:** iOS, macOS, tvOS

```jsx
import { Text, Host } from '@expo/ui/swift-ui';

<Host>
  <Text size={24} weight="bold" color="primary">
    Hello, world!
  </Text>
</Host>
```

**Props:**
- `children: string` - Text content (must be a string, not React.ReactNode)
- `size?: number` - Font size
- `weight?: 'ultraLight' | 'thin' | 'light' | 'regular' | 'medium' | 'semibold' | 'bold' | 'heavy' | 'black'` - Font weight
- `design?: 'default' | 'rounded' | 'serif' | 'monospaced'` - Font design
- `lineLimit?: number` - Maximum number of lines
- `color?: string` - Text color

**Important:** Text children must be a string. Use individual `size` and `weight` props instead of a `font` object.

#### Image

```jsx
import { Image, Host } from '@expo/ui/swift-ui';

<Host>
  <Image
    systemName="airplane"
    color="white"
    size={18}
    modifiers={[
      frame({ width: 28, height: 28 }),
      background('#ffa500'),
      clipShape('roundedRectangle')
    ]}
  />
</Host>
```

#### CircularProgress and LinearProgress

```jsx
import { CircularProgress, LinearProgress, Host } from '@expo/ui/swift-ui';

<Host style={{ width: 300 }}>
  <CircularProgress progress={0.5} color="blue" />
  <LinearProgress progress={0.7} color="orange" />
</Host>
```

### Form Controls

#### Switch (Toggle)

**Platform:** iOS, tvOS

```jsx
import { Switch, Host } from '@expo/ui/swift-ui';

<Host matchContents>
  <Switch
    checked={checked}
    onValueChange={setChecked}
    label="Play music"
    variant="switch"
    color="#ff0000"
  />
</Host>
```

**Variants:** switch (toggle), checkbox

#### TextField

**Platform:** iOS, tvOS

```jsx
import { TextField, Host } from '@expo/ui/swift-ui';

<Host matchContents>
  <TextField
    autocorrection={false}
    defaultValue="Enter text"
    onChangeText={setValue}
  />
</Host>
```

#### Picker

**Platform:** iOS (wheel not available on Apple TV)

```jsx
import { Picker, Host } from '@expo/ui/swift-ui';

<Host matchContents>
  <Picker
    options={['$', '$$', '$$$', '$$$$']}
    selectedIndex={selectedIndex}
    onOptionSelected={({ nativeEvent: { index } }) => setSelectedIndex(index)}
    variant="segmented"
  />
</Host>
```

**Variants:** segmented, wheel, menu

#### Slider

**Platform:** iOS (not available on Apple TV)

```jsx
import { Slider, Host } from '@expo/ui/swift-ui';

<Host style={{ minHeight: 60 }}>
  <Slider value={value} onValueChange={setValue} />
</Host>
```

#### ColorPicker

**Platform:** iOS (not available on Apple TV)

```jsx
import { ColorPicker, Host } from '@expo/ui/swift-ui';

<Host style={{ width: 400, height: 200 }}>
  <ColorPicker
    label="Select a color"
    selection={color}
    onValueChanged={setColor}
  />
</Host>
```

#### DateTimePicker

**Platform:** iOS (not available on Apple TV)

```jsx
import { DateTimePicker, Host } from '@expo/ui/swift-ui';

<Host matchContents>
  <DateTimePicker
    onDateSelected={setDate}
    displayedComponents="date"
    initialDate={date.toISOString()}
    variant="wheel"
  />
</Host>
```

**Components:** date (default) or hourAndMinute for time

### Advanced Components

#### BottomSheet

**Platform:** iOS

```jsx
import { BottomSheet, Host, Text } from '@expo/ui/swift-ui';

<Host style={{ position: 'absolute', width }}>
  <BottomSheet isOpened={isOpened} onIsOpenedChange={setIsOpened}>
    <Text>Hello, world!</Text>
  </BottomSheet>
</Host>
```

#### ContextMenu

**Platform:** iOS, tvOS

> Also known as DropdownMenu

```jsx
import { ContextMenu, Button, Picker, Host } from '@expo/ui/swift-ui';

<Host style={{ width: 150, height: 50 }}>
  <ContextMenu>
    <ContextMenu.Items>
      <Button systemImage="person.crop.circle" onPress={handleAction}>
        Hello
      </Button>
      <Picker label="Options" options={options} variant="menu" />
    </ContextMenu.Items>
    <ContextMenu.Trigger>
      <Button variant="bordered">Show Menu</Button>
    </ContextMenu.Trigger>
  </ContextMenu>
</Host>
```

#### Gauge

**Platform:** iOS (not available on Apple TV)

```jsx
import { Gauge, Host, PlatformColor } from '@expo/ui/swift-ui';

<Host matchContents>
  <Gauge
    min={{ value: 0, label: '0' }}
    max={{ value: 1, label: '1' }}
    current={{ value: 0.5 }}
    color={[
      PlatformColor('systemRed'),
      PlatformColor('systemYellow'),
      PlatformColor('systemGreen')
    ]}
    type="circularCapacity"
  />
</Host>
```

#### List

**Platform:** iOS, tvOS

```jsx
import { List, LabelPrimitive, Host } from '@expo/ui/swift-ui';

<Host style={{ flex: 1 }}>
  <List
    editModeEnabled={editMode}
    onSelectionChange={(items) => alert(`Selected: ${items.join(', ')}`)}
    moveEnabled={canMove}
    onMoveItem={(from, to) => alert(`Moved ${from} to ${to}`)}
    onDeleteItem={(index) => alert(`Deleted ${index}`)}
    listStyle="automatic"
  >
    {data.map((item, index) => (
      <LabelPrimitive
        key={index}
        title={item.text}
        systemImage={item.systemImage}
      />
    ))}
  </List>
</Host>
```

**Features:** Edit mode, move, delete, selection

## Modifiers

### Common Modifiers

Import from `@expo/ui/swift-ui/modifiers`:

```jsx
import { padding, frame, background, clipShape } from '@expo/ui/swift-ui/modifiers';
```

**Layout modifiers:**
- `padding({ all, horizontal, vertical, top, bottom, leading, trailing })` - Add spacing
- `frame({ width, height, minWidth, maxWidth, minHeight, maxHeight })` - Set dimensions
- `fixedSize()` - Prevent automatic sizing

**Styling modifiers:**
- `background(color or content)` - Set background
- `foregroundStyle(color)` - Set foreground color
- `clipShape(shape)` - Clip to shape (roundedRectangle, circle, capsule)
- `cornerRadius(radius)` - Round corners
- `font({ size, weight, design })` - Font styling (Note: Text component uses individual props: `size`, `weight`, `design`)

**Behavior modifiers:**
- `disabled(bool)` - Enable/disable interaction
- `animation(Animation.spring(), condition)` - Animate changes

### Glass Morphism Modifiers

> ⚠️ **v10 Preview**: `glassEffect` requires Xcode 26+ and iOS 26+. May differ from v9 APIs.

```jsx
import { glassEffect, glassEffectId, animation, Animation } from '@expo/ui/swift-ui/modifiers';

<Text
  size={16}
  weight="medium"
  modifiers={[
    padding({ all: 16 }),
    glassEffect({
      glass: { variant: 'clear' }
    })
  ]}>
  Glass effect text
</Text>
```

**Advanced glass effects with namespace:**

```jsx
import { Namespace } from '@expo/ui/swift-ui';

const namespaceId = useId();

<Namespace id={namespaceId}>
  <Image
    systemName="paintbrush.fill"
    modifiers={[
      glassEffect({ glass: { variant: 'clear' } }),
      glassEffectId('uniqueId', namespaceId),
      animation(Animation.spring({ duration: 0.8 }), isExpanded)
    ]}
  />
</Namespace>
```

### v10 Preview Modifiers ⚠️

> ⚠️ **v10 Preview**: These modifiers may have different APIs in v9 stable. Check TypeScript types.

**Button style modifiers:**
- `buttonStyle('glass' | 'glassProminent' | 'bordered' | 'borderless' | 'borderedProminent' | 'plain')`
- `controlSize('mini' | 'small' | 'regular' | 'large' | 'extraLarge')`
- `labelStyle('iconOnly' | 'titleAndIcon' | 'titleOnly')`

```jsx
<Button
  modifiers={[
    buttonStyle('glass'),
    controlSize('large')
  ]}>
  Glass Button
</Button>
```

**Form control modifiers:**
- `pickerStyle('menu' | 'segmented' | 'wheel')`
- `tag(value)` - Tag picker options for selection
- `font({ size })` - Font customization

```jsx
<Picker
  modifiers={[pickerStyle('menu')]}
  selection={selectedIndex}
  onSelectionChange={setSelectedIndex}>
  {options.map((option, index) => (
    <Text key={index} modifiers={[tag(index)]}>
      {option}
    </Text>
  ))}
</Picker>
```

## v10 Preview Features ⚠️

> ⚠️ **v10 Preview**: The following components and features are from v10 and may contain breaking changes from v9 stable APIs. Always check TypeScript types for current signatures.

### GlassEffectContainer

**Platform:** iOS/macOS

Container component for glass morphism effects with coordinated animations.

```jsx
import { GlassEffectContainer, Namespace } from '@expo/ui/swift-ui';

const namespaceId = useId();

<Host style={{ flex: 1 }}>
  <Namespace id={namespaceId}>
    <GlassEffectContainer
      spacing={30}
      modifiers={[
        padding({ all: 30 }),
        cornerRadius(20)
      ]}>
      <VStack spacing={25}>
        <Text>Glass content</Text>
      </VStack>
    </GlassEffectContainer>
  </Namespace>
</Host>
```

### LabeledContent

Wrapper for labeled form elements with multi-part label support.

```jsx
import { LabeledContent } from '@expo/ui/swift-ui';

<LabeledContent label="Name">
  <Text>John Doe</Text>
</LabeledContent>

<LabeledContent
  label={
    <>
      <Text>Title</Text>
      <Text>Subtitle</Text>
    </>
  }>
  <Text>Value</Text>
</LabeledContent>
```

### DisclosureGroup

Expandable/collapsible content sections.

```jsx
import { DisclosureGroup } from '@expo/ui/swift-ui';

<DisclosureGroup
  isExpanded={isExpanded}
  onStateChange={setIsExpanded}
  label="Show Details">
  <Text>Detailed content here</Text>
</DisclosureGroup>
```

### ContentUnavailableView

Empty state or placeholder view with icon, title, and description.

```jsx
import { ContentUnavailableView } from '@expo/ui/swift-ui';

<ContentUnavailableView
  title="No items"
  systemImage="tray"
  description="Add items to get started."
/>
```

### Enhanced Button Styles (v10)

```jsx
import { buttonStyle, controlSize, fixedSize } from '@expo/ui/swift-ui/modifiers';

<Button
  label="Glass"
  modifiers={[
    buttonStyle('glass'),
    controlSize('large'),
    fixedSize()
  ]}
/>

<Button
  label="Glass Prominent"
  modifiers={[
    buttonStyle('glassProminent'),
    controlSize('extraLarge')
  ]}
/>
```

### Enhanced Form Features (v10)

**ColorPicker with opacity:**

```jsx
<ColorPicker
  label="Select color"
  selection={color}
  supportsOpacity
  onValueChanged={setColor}
/>
```

**Picker with menu style and tags:**

```jsx
import { pickerStyle, tag } from '@expo/ui/swift-ui/modifiers';

<Picker
  label="Menu Picker"
  modifiers={[pickerStyle('menu')]}
  selection={selectedIndex}
  onSelectionChange={setSelectedIndex}>
  {options.map((option, index) => (
    <Text key={index} modifiers={[tag(index)]}>
      {option}
    </Text>
  ))}
</Picker>
```

## Interop with React Native

### Using React Native Components in SwiftUI

React Native components can be nested inside Expo UI components. Expo UI automatically creates a `UIViewRepresentable` wrapper.

```jsx
import { Text, Host, VStack } from '@expo/ui/swift-ui';
import { View } from 'react-native';

<Host>
  <VStack spacing={8}>
    <Text>SwiftUI Text</Text>
    <View style={{ width: 100, height: 100, backgroundColor: 'blue' }} />
  </VStack>
</Host>
```

**Important limitations:**
- SwiftUI controls layout properties (`center`, `bounds`, `frame`, `transform`) - don't set these directly on React Native views
- Once React Native components are rendered, the SwiftUI context is left
- Add a new `<Host>` wrapper to return to Expo UI components
- Best practice: Keep SwiftUI layouts self-contained with clear boundaries

### Platform-Specific Notes

**iOS-only components:**
- BottomSheet
- ColorPicker
- DateTimePicker (wheel variant)
- Gauge
- Slider
- Glass effects (iOS 26+, Xcode 26+)

**Apple TV exclusions:**
- Button borderless variant
- ColorPicker
- DateTimePicker
- Gauge
- Slider

**Common patterns:**
- Use `Platform.OS` checks for platform-specific code
- Provide fallbacks for unsupported platforms
- Test on tvOS for tvOS-specific behaviors (focus, remote control)

## Native Tabs with Expo Router

Native tabs provide platform-native tab navigation using system tab bars. Unlike JavaScript tabs, native tabs follow platform conventions and offer native performance.

> **Native tabs is experimental** (SDK 54+, API subject to change). For fully custom designs, consider JavaScript tabs instead.

### When to Use Native Tabs

Choose native tabs for:
- Platform-native navigation feel (iOS UITabBarController, Android Material Tabs)
- Native performance and system integration
- Platform-specific features (iOS 26+ liquid glass effects, minimize behavior)
- Standard tab patterns without extensive customization

Choose JavaScript/custom tabs for:
- Complete visual control over tab bar appearance
- Complex animations or custom layouts
- Consistent cross-platform appearance

### Installation

Ensure `expo-router` is installed and configured:

```bash
npx expo install expo-router
```

**app.json configuration:**
```json
{
  "expo": {
    "plugins": ["expo-router"]
  }
}
```

### Basic Usage

Create a tab layout using file-based routing:

**File structure:**
```
app/
├── _layout.tsx
├── index.tsx
└── settings.tsx
```

**app/_layout.tsx:**
```tsx
import { NativeTabs, Icon, Label } from 'expo-router/unstable-native-tabs';

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <Label>Home</Label>
        <Icon sf="house.fill" drawable="ic_home" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <Icon sf="gear" drawable="ic_settings" />
        <Label>Settings</Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

> Tabs are not automatically added. Explicitly define each tab with `NativeTabs.Trigger`.

### Customize Tab Items

**Icons:**

SF Symbols (iOS):
```tsx
<Icon sf={{ default: 'house', selected: 'house.fill' }} />
```

Android drawables:
```tsx
<Icon drawable="ic_home" />
```

Custom images:
```tsx
<Icon src={require('./assets/home.png')} />
<Icon src={{
  default: require('./assets/home.png'),
  selected: require('./assets/home-active.png')
}} />
```

**Labels:**
```tsx
<Label>Home</Label>           // Show label
<Label hidden />               // Hide label
```

**Badges:**
```tsx
<Badge>9+</Badge>              // Text badge
<Badge />                      // Dot badge (no text)
```

### Tab Bar Styling

**Global styling:**
```tsx
<NativeTabs
  backgroundColor="white"
  iconColor="blue"
  tintColor="purple"
  blurEffect="systemMaterial"
  labelStyle={{ fontSize: 12, fontWeight: '600' }}
  labelVisibilityMode="auto"
  minimizeBehavior="automatic"
>
```

**Per-tab styling:**
```tsx
<NativeTabs.Trigger name="page">
  <NativeTabs.Trigger.TabBar
    backgroundColor="white"
    iconColor="red"
  />
  <Label>Page</Label>
</NativeTabs.Trigger>
```

**Key props:**
- `backgroundColor`: Tab bar background color
- `iconColor`: Default icon color
- `tintColor`: Selected icon color
- `blurEffect`: iOS blur effect (`'systemMaterial'`, `'extraLight'`, `'dark'`, etc.)
- `labelStyle`: Typography settings
- `labelVisibilityMode`: Android label visibility (`'auto'` | `'selected'` | `'labeled'` | `'unlabeled'`)
- `minimizeBehavior`: iOS 26+ minimize behavior (`'automatic'` | `'never'` | `'onScrollDown'` | `'onScrollUp'`)
- `backBehavior`: Android back button behavior (`'history'` | `'none'` | `'initialRoute'`)

### Advanced Features

**Hide tabs conditionally:**
```tsx
const shouldHideMessagesTab = true;

<NativeTabs.Trigger name="messages" hidden={shouldHideMessagesTab} />
```

> Hidden tabs cannot be navigated to in any way.

**Disable pop to top (iOS):**
```tsx
<NativeTabs.Trigger name="index" disablePopToTop>
  <Label>Home</Label>
</NativeTabs.Trigger>
```

**Disable scroll to top (iOS):**
```tsx
<NativeTabs.Trigger name="index" disableScrollToTop>
  <Label>Home</Label>
</NativeTabs.Trigger>
```

**iOS 26+ search tab:**
```tsx
<NativeTabs.Trigger name="search" role="search">
  <Label>Search</Label>
</NativeTabs.Trigger>
```

**iOS 26+ tab bar minimize:**
```tsx
<NativeTabs minimizeBehavior="onScrollDown">
  <NativeTabs.Trigger name="index">
    <Label>Home</Label>
  </NativeTabs.Trigger>
</NativeTabs>
```

**Vector icons integration:**
```tsx
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { VectorIcon } from 'expo-router/unstable-native-tabs';
import { Platform } from 'react-native';

<NativeTabs.Trigger name="index">
  <Label>Home</Label>
  {Platform.select({
    ios: <Icon sf="house.fill" />,
    android: <Icon src={<VectorIcon family={MaterialIcons} name="home" />} />,
  })}
</NativeTabs.Trigger>
```

### Platform-Specific Considerations

**Android:**
- Limit of 5 tabs (Material Design constraint)
- Uses Material Tabs component
- Supports ripple effects and indicators

**iOS:**
- No tab limit (5 recommended for UX)
- Uses UITabBarController
- Supports blur effects and liquid glass (iOS 26+)
- Separate search tab support (iOS 26+)
- Role-based system tabs (search, bookmarks, contacts, etc.)

**tvOS:**
- Follows tvOS platform conventions
- Different tab bar positioning

**Known limitations:**
- No nested native tabs (can nest JavaScript tabs inside native tabs)
- Limited FlatList support for scroll-to-top and minimize-on-scroll
- Cannot measure tab bar height (varies by device: iPad, Vision Pro, etc.)
- For FlatList scroll edge issues, use `disableTransparentOnScrollEdge` prop

### Migration from JavaScript Tabs

Key differences:

| JavaScript Tabs | Native Tabs |
|-----------------|-------------|
| `Tabs.Screen` | `NativeTabs.Trigger` |
| Options object | Child components (`<Icon>`, `<Label>`) |
| Automatic tabs | Explicit trigger definition |
| Mock headers | Use nested `<Stack />` |

**Before (JavaScript tabs):**
```tsx
<Tabs.Screen
  name="home"
  options={{
    tabBarIcon: ({ focused, color, size }) => (
      <Icon name="home" color={color} size={size} />
    ),
  }}
/>
```

**After (Native tabs):**
```tsx
<NativeTabs.Trigger name="home">
  <Icon sf="house.fill" />
  <Label>Home</Label>
</NativeTabs.Trigger>
```

**Use Stacks inside tabs:**

Native tabs don't have mock headers. Nest Stack layouts:

```tsx
// app/home/_layout.tsx
import { Stack } from 'expo-router';

export default function HomeLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="details" options={{ title: 'Details' }} />
    </Stack>
  );
}
```

### Common Workflows

**Conditional tabs based on auth:**
```tsx
const { user } = useAuth();

return (
  <NativeTabs>
    <NativeTabs.Trigger name="index">
      <Label>Home</Label>
    </NativeTabs.Trigger>
    {user && (
      <NativeTabs.Trigger name="profile">
        <Label>Profile</Label>
      </NativeTabs.Trigger>
    )}
  </NativeTabs>
);
```

**Badge updates:**
```tsx
const [unreadCount, setUnreadCount] = useState(0);

<NativeTabs.Trigger name="messages">
  {unreadCount > 0 && (
    <Badge>{unreadCount > 99 ? '99+' : unreadCount}</Badge>
  )}
  <Label>Messages</Label>
</NativeTabs.Trigger>
```

## Common Workflows

### Build an iOS Settings Interface

```jsx
import {
  Form,
  Section,
  HStack,
  VStack,
  Button,
  Switch,
  Text,
  Image,
  Spacer,
  Host
} from '@expo/ui/swift-ui';
import { background, clipShape, frame } from '@expo/ui/swift-ui/modifiers';

function SettingsView() {
  const [airplaneMode, setAirplaneMode] = useState(true);

  return (
    <Host style={{ flex: 1 }}>
      <Form>
        <Section>
          <HStack spacing={8}>
            <Image
              systemName="airplane"
              color="white"
              size={18}
              modifiers={[
                frame({ width: 28, height: 28 }),
                background('#ffa500'),
                clipShape('roundedRectangle')
              ]}
            />
            <Text>Airplane Mode</Text>
            <Spacer />
            <Switch value={airplaneMode} onValueChange={setAirplaneMode} />
          </HStack>
        </Section>
      </Form>
    </Host>
  );
}
```

### Create a Progress View

```jsx
import { CircularProgress, LinearProgress, VStack, Host } from '@expo/ui/swift-ui';

function ProgressView() {
  return (
    <Host style={{ flex: 1, margin: 32 }}>
      <VStack spacing={32}>
        <CircularProgress progress={0.5} color="blue" />
        <LinearProgress progress={0.7} color="orange" />
      </VStack>
    </Host>
  );
}
```

### Build a Form with Validation

```jsx
import {
  Form,
  Section,
  TextField,
  Switch,
  Picker,
  Button,
  Host
} from '@expo/ui/swift-ui';

function FormView() {
  const [name, setName] = useState('');
  const [enabled, setEnabled] = useState(true);
  const [category, setCategory] = useState(0);

  return (
    <Host style={{ flex: 1 }}>
      <Form>
        <Section header="User Information">
          <TextField
            label="Name"
            defaultValue={name}
            onChangeText={setName}
          />
          <Switch
            label="Enabled"
            value={enabled}
            onValueChange={setEnabled}
          />
          <Picker
            label="Category"
            options={['General', 'Advanced', 'Expert']}
            selectedIndex={category}
            onOptionSelected={({ nativeEvent: { index } }) => setCategory(index)}
            variant="segmented"
          />
        </Section>
      </Form>
    </Host>
  );
}
```

## Resource References

For detailed API specifications, code examples, and implementation guides, refer to:

- **Installation and usage guide:** `references/expo-ui-guide.md`
  - Detailed installation steps
  - Host component explanation
  - Layout system (HStack, VStack)
  - Modifiers system
  - Common questions and FAQs

- **Complete API reference:** `references/expo-ui-api-reference.md`
  - All components with examples
  - Platform support details
  - Props and events documentation
  - Code snippets for each component

- **v10 preview features:** `references/expo-ui-v10-examples.md`
  - Glass morphism effects (GlassEffectContainer, glassEffect)
  - New button styles (glass, glassProminent)
  - Enhanced form components (LabeledContent, DisclosureGroup)
  - Breaking change warnings for v10

- **Native tabs guide:** `references/native-tabs-guide.md`
  - Native tabs installation and setup
  - Platform-specific behaviors (iOS, Android, tvOS)
  - Advanced features (iOS 26+ search, minimize behavior)
  - Migration from JavaScript tabs
  - Common patterns and workflows

- **Native tabs API reference:** `references/native-tabs-api.md`
  - Complete component API (NativeTabs, Icon, Label, Badge)
  - Props and types documentation
  - Platform-specific props
  - Vector icons integration
  - Known limitations and workarounds

## Best Practices

1. **Use Host boundaries wisely** - Wrap SwiftUI content in `<Host>` and keep SwiftUI layouts self-contained

2. **Prefer v9 stable APIs** - Use documented v9 APIs unless v10 features are specifically needed

3. **Check platform support** - Some components are iOS-only, provide fallbacks for tvOS

4. **Leverage TypeScript** - Always check TypeScript types for accurate API signatures, especially for v10

5. **Use modifiers for styling** - Apply modifiers via the `modifiers` prop rather than inline styles

6. **Test on real devices** - Some features (like glass effects) require specific iOS/Xcode versions

7. **Mind the layout transition** - Remember that flexbox stops working inside SwiftUI context

8. **Keep interop boundaries clear** - Minimize mixing React Native and SwiftUI for better performance
