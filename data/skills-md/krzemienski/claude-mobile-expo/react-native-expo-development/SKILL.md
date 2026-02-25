---
name: react-native-expo-development
description: Use when developing React Native components, installing packages via expo-mcp, implementing screens, or following RN best practices - integrates expo-mcp workflows (add_library, search_documentation) with production patterns from Gifted Chat and Stream
---

# React Native + Expo Development with expo-mcp

## Overview

React Native/Expo development using **expo-mcp for ALL package operations** and production patterns from 13k-star libraries.

**Core principle:** Use expo-mcp "Add package" (NOT npm install). Search docs before implementing. Apply production patterns.

**Announce at start:** "I'm using the react-native-expo-development skill for React Native development."

## When to Use

- Installing ANY Expo package (Phase 4)
- Implementing React Native components
- Implementing screens
- Searching Expo/RN documentation
- Working with Zustand, React Navigation, Reanimated
- Following performance best practices

## expo-mcp Integration (MANDATORY)

### Package Installation (NEVER npm install)

**❌ WRONG**:
```bash
npm install zustand
npm install @react-native-async-storage/async-storage
```

**✅ CORRECT**:
```
"Add zustand and show me how to set up a store with AsyncStorage persistence"
"Add @react-native-async-storage/async-storage"
"Add react-native-syntax-highlighter for code display"
"Add react-native-markdown-display for message rendering"
```

**Why**: expo-mcp provides:
- Correct version for Expo SDK
- Automatic usage documentation
- Setup examples
- Compatibility verification

### Documentation Search

Before implementing features:

```
"Search Expo docs for navigation patterns"
"Search Expo docs for AsyncStorage persistence"
"Search Expo docs for deep linking setup"
```

expo-mcp searches with natural language, returns relevant sections

### Testing Integration

Add testID to ALL interactive elements:

```typescript
<TouchableOpacity testID="send-button" onPress={handleSend}>
<TextInput testID="message-input" />
<Pressable testID="settings-button">
<FlatList testID="message-list">
```

Then test with expo-mcp:
```
"Find view with testID 'send-button' and verify it's enabled"
"Tap button with testID 'send-button'"
"Take screenshot and verify message sent"
```

## Production Patterns

### Message UI (from react-native-gifted-chat)

```typescript
// MessageBubble component structure
interface MessageBubbleProps {
  message: Message;
  isUser: boolean;
}

export const MessageBubble = React.memo<MessageBubbleProps>(
  ({message, isUser}) => {
    return (
      <View testID={`message-${message.id}`} style={[
        styles.bubble,
        isUser ? styles.userBubble : styles.assistantBubble
      ]}>
        <Text testID={`message-text-${message.id}`}>{message.content}</Text>
        <Text style={styles.timestamp}>{formatTime(message.timestamp)}</Text>
      </View>
    );
  },
  (prev, next) => prev.message.id === next.message.id
);
```

### FlatList Optimization (from Context7 docs)

```typescript
<FlatList
  testID="message-list"
  data={messages}
  renderItem={renderMessage}
  keyExtractor={(item) => item.id}
  inverted={true} // For chat (newest at bottom)
  windowSize={10}
  maxToRenderPerBatch={10}
  removeClippedSubviews={true}
  initialNumToRender={10}
/>

const renderMessage = useCallback((info: ListRenderItemInfo<Message>) => (
  <MessageBubble message={info.item} isUser={info.item.role === 'user'} />
), []);
```

### Zustand Store with AsyncStorage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      settings: {...},
      updateSettings: (settings) => set({settings}),
    }),
    {
      name: 'claude-code-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        settings: state.settings,
        // Don't persist messages (too large)
      })
    }
  )
);
```

### Optimistic UI (from stream-chat-react-native)

```typescript
const sendMessage = (text: string) => {
  const optimisticMessage = {
    id: `temp-${Date.now()}`,
    text,
    status: 'sending'
  };
  
  addMessage(optimisticMessage); // Show immediately
  
  websocket.send({type: 'message', message: text});
  // Update when confirmed
};
```

## Component Best Practices

### Structure with testID

```typescript
interface ComponentProps {
  data: Data;
  onPress: () => void;
}

export const Component = React.memo<ComponentProps>(({data, onPress}) => {
  const handlePress = useCallback(() => {
    onPress();
  }, [onPress]);
  
  return (
    <TouchableOpacity testID="component-container" onPress={handlePress}>
      <Text testID="component-text">{data.text}</Text>
    </TouchableOpacity>
  );
});
```

### Styling

**Use StyleSheet.create** (NOT inline):

```typescript
import {COLORS, SPACING, TYPOGRAPHY} from '../constants/theme';

const styles = StyleSheet.create({
  container: {
    padding: SPACING.base,
    backgroundColor: COLORS.backgroundGradient.start,
  },
  text: {
    fontSize: TYPOGRAPHY.fontSize.md,
    color: COLORS.textPrimary,
  },
});
```

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "npm install works" | WRONG. expo-mcp ensures compatibility. |
| "I know RN already" | WRONG. Patterns prevent bugs, use them. |
| "Inline styles are faster" | WRONG. StyleSheet enables optimization. |
| "Skip testIDs" | WRONG. Required for expo-mcp testing. |

## Red Flags

- "npm install is fine" → WRONG. Use expo-mcp.
- "Don't need patterns" → WRONG. 13k stars prove value.
- "testID is optional" → WRONG. Required for autonomous testing.

## Integration

- **Use WITH**: `@claude-mobile-metro-manager` (Metro required)
- **Use FOR**: All Phase 4 implementation
- **Enables**: expo-mcp autonomous testing in Gate 4A
