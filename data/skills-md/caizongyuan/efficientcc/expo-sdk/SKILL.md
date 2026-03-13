---
name: expo-sdk
description: This skill should be used when users need to work with Expo SDK and Expo Router for building React Native applications. It provides comprehensive guidance on navigation patterns, media handling (camera, image, video, audio), data storage (SQLite, filesystem, SecureStore), authentication, device features (location, notifications, biometrics), and third-party integrations (Stripe, linking, sharing).
---

# Expo SDK

## Core Functionality

Expo SDK provides a comprehensive toolkit for building React Native applications with file-based routing through Expo Router. This skill covers navigation patterns, media handling, data persistence, authentication, device hardware integration, and third-party service integration.

## When to Use

This skill should be used when users need to work with Expo SDK and Expo Router for building React Native applications. It provides comprehensive guidance on navigation patterns, media handling (camera, image, video, audio), data storage (SQLite, filesystem, SecureStore), authentication, device features (location, notifications, biometrics), and third-party integrations (Stripe, linking, sharing).

## Module Overview

### Navigation Module
- **Functionality**: Comprehensive file-based routing system with support for stack, tabs, drawer, and modal navigators. Includes dynamic routes, protected routes, redirects, and deep linking capabilities.
- **Key APIs**: `useRouter`, `Link`, `Stack`, `Tabs`, `Drawer`, `Modal`, `Redirect`, `useLocalSearchParams`, `router.navigate`, `router.push`, `router.back`, `router.replace`, `router.setParams`
- **Detailed documentation**: `references/navigation.mdx`, `references/stack.mdx`, `references/tabs.mdx`, `references/drawer.mdx`, `references/modals.mdx`, `references/redirects.mdx`

### Authentication Module
- **Functionality**: Client-side authentication patterns using React Context, protected routes, session management, and SecureStore integration for secure credential storage.
- **Key APIs**: `Stack.Protected`, `useSession`, `SessionProvider`, `SecureStore.setItemAsync`, `SecureStore.getItemAsync`, `Redirect`
- **Detailed documentation**: `references/authentication.mdx`, `references/authentication-rewrites.mdx`, `references/protected.mdx`

### Media Module
- **Functionality**: Camera access and preview, image loading with caching, image manipulation, media library access, video playback, audio recording and playback, and Live Photo support.
- **Key APIs**: `CameraView`, `useCameraPermissions`, `Image`, `useVideoPlayer`, `VideoView`, `useAudioPlayer`, `useAudioRecorder`, `ImageManipulator`, `MediaLibrary.getAssetsAsync`, `launchImageLibraryAsync`
- **Detailed documentation**: `references/camera.mdx`, `references/image.mdx`, `references/video.mdx`, `references/audio.mdx`, `references/imagepicker.mdx`, `references/imagemanipulator.mdx`, `references/media-library.mdx`

### Storage Module
- **Functionality**: SQLite database operations with async/await patterns, filesystem access for file operations, and encrypted key-value storage for sensitive data.
- **Key APIs**: `SQLite.openDatabaseAsync`, `execAsync`, `runAsync`, `getFirstAsync`, `getAllAsync`, `prepareAsync`, `withTransactionAsync`, `FileSystem.downloadFileAsync`, `File`, `Directory`, `SecureStore.setItemAsync`, `SecureStore.getItemAsync`
- **Detailed documentation**: `references/sqlite.mdx`, `references/filesystem.mdx`, `references/securestore.mdx`

### Device Module
- **Functionality**: Geolocation tracking with background support, push and local notifications, biometric authentication (Face ID, Touch ID, fingerprint), and background task management.
- **Key APIs**: `Location.requestForegroundPermissionsAsync`, `Location.getCurrentPositionAsync`, `Location.watchPositionAsync`, `Notifications.scheduleNotificationAsync`, `Notifications.addNotificationReceivedListener`, `LocalAuthentication.authenticateAsync`
- **Detailed documentation**: `references/location.mdx`, `references/notifications.mdx`, `references/local-authentication.mdx`, `references/task-manager.mdx`

### Integration Module
- **Functionality**: Deep linking and universal links, file sharing between apps, Stripe payment integration, Apple Handoff for cross-device continuity, clipboard access, and native intent handling.
- **Key APIs**: `Linking.openURL`, `Linking.createURL`, `Sharing.shareAsync`, `initStripe`, `PaymentSheet`, `Clipboard.setStringAsync`, `Clipboard.getStringAsync`
- **Detailed documentation**: `references/linking.mdx`, `references/sharing.mdx`, `references/stripe.mdx`, `references/apple-handoff.mdx`, `references/clipboard.mdx`

## Workflow

### Navigation and Routing
1. Define file-based routes using `app/` directory structure with special notation (square brackets for dynamic routes, parentheses for route groups, underscore for layouts)
2. Use `useRouter()` for imperative navigation (`router.push()`, `router.back()`, `router.replace()`)
3. Use `<Link>` component for declarative navigation
4. Implement layouts with `_layout.tsx` files to configure navigators (Stack, Tabs, Drawer)
5. Reference detailed navigation patterns in `references/navigation.mdx` and `references/notation.mdx`

### Authentication Implementation
1. Create authentication context with `useSession` hook for session state management
2. Use `Stack.Protected` or `Tabs.Protected` for protected route groups
3. Store credentials securely using `SecureStore` API
4. Implement redirects for unauthenticated users using `<Redirect>` component
5. Reference complete authentication guides in `references/authentication.mdx`

### Media Handling
1. Request permissions using `useCameraPermissions` or `MediaLibrary.usePermissions`
2. Use `<CameraView>` component for camera functionality
3. Load images with `<Image>` component for optimized caching and performance
4. Implement video playback with `useVideoPlayer` hook and `<VideoView>` component
5. Reference media APIs in `references/camera.mdx`, `references/image.mdx`, `references/video.mdx`

### Data Persistence
1. For structured data: Use `SQLite.openDatabaseAsync()` with async/await for database operations
2. For secure credentials: Use `SecureStore.setItemAsync()` and `getItemAsync()`
3. For file operations: Use `FileSystem` API for downloads, uploads, and directory management
4. Reference storage solutions in `references/sqlite.mdx`, `references/securestore.mdx`, `references/filesystem.mdx`

### Device Features
1. Location: Request foreground/background permissions, then use `Location.getCurrentPositionAsync()` or `Location.watchPositionAsync()`
2. Notifications: Configure with `Notifications.setNotificationHandler()`, then schedule with `Notifications.scheduleNotificationAsync()`
3. Biometrics: Use `LocalAuthentication.authenticateAsync()` for fingerprint/Face ID authentication
4. Reference device-specific guides in `references/location.mdx`, `references/notifications.mdx`, `references/local-authentication.mdx`

### Third-Party Integration
1. Deep linking: Configure linking in `app.config.js`, use `Linking.openURL()` or `<Link>` component
2. Stripe payments: Initialize with `initStripe()`, use `PaymentSheet` for payment flow
3. Sharing: Use `Sharing.shareAsync()` to share files and content
4. Reference integration guides in `references/stripe.mdx`, `references/linking.mdx`, `references/sharing.mdx`

## Common Patterns

### Dynamic Routes
Use square brackets in file names (e.g., `[id].tsx`) and access parameters with `useLocalSearchParams()` hook.

### Protected Routes
Wrap authenticated screens with `<Stack.Protected>` or use client-side redirects based on session context.

### Modal Presentation
Create files inside `../modal/` directory or use `<Modal>` from React Native for custom presentations.

### Background Tasks
Define tasks with `TaskManager.defineTask()` and configure location updates or notifications in background.

## Resource References

### Navigation & Routing
- File-based routing basics: `references/navigation.mdx`
- Route notation reference: `references/notation.mdx`
- Stack navigator: `references/stack.mdx`
- Tabs navigator: `references/tabs.mdx`
- Modals: `references/modals.mdx`
- Redirects: `references/redirects.mdx`

### Authentication
- Protected routes (SDK 53+): `references/authentication.mdx`
- Authentication patterns (SDK 52): `references/authentication-rewrites.mdx`
- Protected components: `references/protected.mdx`

### Media Handling
- Camera: `references/camera.mdx`
- Image loading: `references/image.mdx`
- Video playback: `references/video.mdx`
- Audio: `references/audio.mdx`
- Image picker: `references/imagepicker.mdx`
- Media library: `references/media-library.mdx`

### Storage & Data
- SQLite database: `references/sqlite.mdx`
- File system: `references/filesystem.mdx`
- Secure storage: `references/securestore.mdx`

### Device Features
- Location services: `references/location.mdx`
- Notifications: `references/notifications.mdx`
- Biometric auth: `references/local-authentication.mdx`
- Background tasks: `references/task-manager.mdx`

### Integration
- Stripe payments: `references/stripe.mdx`
- Deep linking: `references/linking.mdx`
- Sharing: `references/sharing.mdx`
- Apple Handoff: `references/apple-handoff.mdx`
- Clipboard: `references/clipboard.mdx`

For complete API specifications, advanced configurations, and platform-specific considerations, refer to the detailed documentation in the `references/` directory.
