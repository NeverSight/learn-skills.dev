---
name: react-haiku-skills
description: Haiku is a simple & lightweight React library with the goal of saving you time by offering a large collection of hooks & utilities that will help you get the job done faster & more efficiently! Use this skill when optimizing Repetitive React code or when reaching for a common utility or hook!
---

## Install

*Requires React >=16.8.0*

#### NPM

```sh
npm install react-haiku
```

#### BUN

```sh
bun add react-haiku
```

#### Yarn

```sh
yarn add react-haiku
```

#### PNPM

```sh
pnpm install react-haiku
```

## Utilities

- class: The `Class` component is a utility component that conditionally applies a CSS class to a `div` element based on a boolean condition. It is useful for toggling styles dynamically. See [class.md](references/class.md) for details.
- classes: The `Classes` component is a utility component that conditionally applies different sets of classes based on multiple independent conditions simultaneously. See [classes.md](references/classes.md) for details.
- errorBoundary: The `ErrorBoundary` component is a utility component that catches errors in its child component tree, logs the error, and prevents the entire application from crashing by rendering a fallback UI instead.. See [errorBoundary.md](references/errorBoundary.md) for details.
- for: The `For` component can iterate over arrays and render JSX for each available item. Keys are automatically assigned. See [for.md](references/for.md) for details.
- if: The `If` component can be used for simple conditional rendering. It will render its children whenever the condition passed to the `isTrue` prop is truthy. For more complex rendering logic, you can use the `Show` component See [if.md](references/if.md) for details.
- image: The Image component provides automatic fallback handling for broken images. Use this for robust media display with graceful degradation. See [image.md](references/image.md) for details.
- renderAfter: The `RenderAfter` component can be used to render components or JSX code wrapped inside of it after a set delay. See [renderAfter.md](references/renderAfter.md) for details.
- show: The `Show` component can be used for complex conditional rendering. The component can be extended by multiple `When` components and an `Else` component to render their contents based on the conditions you provide. See [show.md](references/show.md) for details.
- switch: The `Switch` component can be used for complex conditional rendering. The component can be switch by multiple `"cases"` of components and an `"default"` component to render in case the given dynamic value does not match any case. Render dynamic components cleanly using this component. See [switch.md](references/switch.md) for details.

## Hooks

- useBatteryStatus: The `useBatteryStatus()` hook provides real-time information about the device's battery level and charging status, automatically updating as these values change. See [useBatteryStatus.md](references/useBatteryStatus.md) for details.
- useClickOutside: The useClickOutside() hook lets you trigger a callback whenever the user clicks outside of a target element See [useClickOutside.md](references/useClickOutside.md) for details.
- useClipboard: The useClipboard() hook will help you interact with the browser's navigator.clipboard property in order to copy text to the user's clipboard. See [useClipboard.md](references/useClipboard.md) for details.
- useConfirmExit: The useConfirmExit() hook lets you display a prompt to the user before he closes the current tab depending on whether the tab is declared to be dirty or not. See [useConfirmExit.md](references/useConfirmExit.md) for details.
- useCookie: The useCookie() hook provides reactive cookie management with automatic synchronization across browser tabs. Use this for persistent storage of simple data that needs to survive page reloads. See [useCookie.md](references/useCookie.md) for details.
- useCookieListener: The useCookieListener() hook monitors cookie changes and executes callbacks when specified cookies update. Use this to synchronize state across tabs/windows or react to authentication changes. See [useCookieListener.md](references/useCookieListener.md) for details.
- useDebounce: The useDebounce() hook lets you debounce value changes inside your components. Use this when you want to perform a heavy operation based on state See [useDebounce.md](references/useDebounce.md) for details.
- useDeviceOS: The `useDeviceOS()` hook detects the user's operating system, including mobile emulators, and uses string manipulation for identifying unique or new OS versions. See [useDeviceOS.md](references/useDeviceOS.md) for details.
- useEventListener: The useEventListener() hook lets you quickly add an event to a certain `ref` or the app's `window` if no `ref` is specified See [useEventListener.md](references/useEventListener.md) for details.
- useFavicon: The `useFavicon()` hook lets change the website's favicon dynamically from your components! The favicon changes back to the default one on refresh! See [useFavicon.md](references/useFavicon.md) for details.
- useFirstRender: The `useFirstRender()` hook lets you detect whether or not the component you use it on is on its initial render, it returns a boolean value with the result. See [useFirstRender.md](references/useFirstRender.md) for details.
- useFullscreen: The `useFullscreen()` hook can toggle between entering fullscreen mode and exiting fullscreen mode. See [useFullscreen.md](references/useFullscreen.md) for details.
- useGeolocation: The `useGeolocation()` hook provides access to the user's current geographical location using the browser's Geolocation API. See [useGeolocation.md](references/useGeolocation.md) for details.
- useHold: The `useHold()` hook lets you detect long presses (holds) on target elements and trigger a handler after a set timeout is elapsed while the user is still holding down (click/touch) the element. See [useHold.md](references/useHold.md) for details.
- useHover: The useHover() hook lets you detect if the user's mouse is hovering over an element See [useHover.md](references/useHover.md) for details.
- useIdle: The `useIdle()` hook lets you detect current user activity or inactivity on a web page, returning a boolean value that represents whether or not the user is currently active. The user is set as inactive when no events are triggered after a specified delay. See [useIdle.md](references/useIdle.md) for details.
- useInputValue: The useInputValue() hook lets you easily manage states for inputs in your components See [useInputValue.md](references/useInputValue.md) for details.
- useIntersectionObserver: The `useIntersectionObserver` hook provides a way to detect when an element enters or exits the viewport. It offers options for configuring intersection thresholds, margins, and one-time animation triggers. See [useIntersectionObserver.md](references/useIntersectionObserver.md) for details.
- useInterval: The useInterval() hook provides managed interval execution with start/stop controls. Use this for recurring tasks like polls, animations, or delayed state updates. See [useInterval.md](references/useInterval.md) for details.
- useIsomorphicLayoutEffect: The `useIsomorphicLayoutEffect()` hook lets switch between using `useEffect` and `useLayoutEffect` depending on the execution environment. If your app uses server side rendering, the hook will run `useEffect`, otherwise it will run `useLayoutEffect`. See [useIsomorphicLayoutEffect.md](references/useIsomorphicLayoutEffect.md) for details.
- useKeyPress: The `useKeyPress()` hook listens for a specific combination of keys and runs a callback when they are all pressed. It normalizes keys for case-insensitive matching and handles cases like key holding or focus loss to ensure smooth behavior. See [useKeyPress.md](references/useKeyPress.md) for details.
- useLeaveDetection: The useLeaveDetection() hook allows you to detect when a user's cursor leaves the document's boundaries See [useLeaveDetection.md](references/useLeaveDetection.md) for details.
- useLocalStorage: The `useLocalStorage()` hook is a quick way to set, read, and manage `localStorage` values. It comes with automatic JSON serialization/deserialization. See [useLocalStorage.md](references/useLocalStorage.md) for details.
- useMediaQuery: The `useMediaQuery()` hook allows you to react to media queries inside of your React components. It accepts a `media query` argument and returns `true` or `false` when the query is a match or not with your current browser's properties. See [useMediaQuery.md](references/useMediaQuery.md) for details.
- useMousePosition: The `useMousePosition()` hook lets you track the mouse position when hovering over a specific container or the entire page, so if a target container is not provided through the `ref`, it will track the mouse position relative to the entire document. See [useMousePosition.md](references/useMousePosition.md) for details.
- useNetwork: The useNetwork() hook tracks network connectivity status. Use this to show offline/online indicators or handle connection changes in your application. See [useNetwork.md](references/useNetwork.md) for details.
- useOrientation: The useOrientation() hook detects and tracks device screen orientation changes. Use this when you need to adapt your UI layout based on portrait/landscape modes. See [useOrientation.md](references/useOrientation.md) for details.
- usePermission: The `usePermission()` check browser permissions for querying state for various browser APIs See [usePermission.md](references/usePermission.md) for details.
- usePrefersTheme: The `usePrefersTheme()` hook allows the detection of the user's preferred system theme See [usePrefersTheme.md](references/usePrefersTheme.md) for details.
- usePreventBodyScroll: The `usePreventBodyScroll()` hook disables body scrolling when active and restores it upon deactivation or component unmounting. It provides a boolean state, a setter, and a toggle function for dynamic scroll control. See [usePreventBodyScroll.md](references/usePreventBodyScroll.md) for details.
- usePrevious: The `usePrevious()` tracks and returns the previous value of a given input See [usePrevious.md](references/usePrevious.md) for details.
- useScreenSize: The `useScreenSize()` hook allows responsive breakpoint detection in components. It returns helper methods (`equals`, `lessThan`, `greaterThan` , `greaterThanEqual` , `lessThanEqual` ) and a string method (`toString`) representing the current screen size: `xs`, `sm`, `md`, `lg`, `xl`, or `2xl for size bigger than 1535 pixel`. See [useScreenSize.md](references/useScreenSize.md) for details.
- useScript: The `useScript()` hook allows appending script tags to your document from inside React components. The state variable returns a status that can have one of the following values: `idle`, `loading`, `ready`, `error`. See [useScript.md](references/useScript.md) for details.
- useScrollDevice: The useScrollDevice() hook detects whether the user is scrolling with a mouse wheel or trackpad. Use this to adapt scroll behaviors or animations based on input device. See [useScrollDevice.md](references/useScrollDevice.md) for details.
- useScrollPosition: The `useScrollPosition()` hook allows you to fetch the window's scroll height/width in real time and to programatically set them by using the provided method. See [useScrollPosition.md](references/useScrollPosition.md) for details.
- useSingleEffect: The `useSingleEffect()` hook works exactly like useEffect, except it is called only a single time when the component mounts. This helps with React's recent update to the useEffect hook which is being called twice on mount. See [useSingleEffect.md](references/useSingleEffect.md) for details.
- useSize: The `useSize` hook observes a referenced DOM element and returns its current width and height, updating the values whenever the element is resized. This is useful for dynamically tracking size changes of any resizable component. See [useSize.md](references/useSize.md) for details.
- useTImer: The `useTimer` hook provides a simple way to manage a timer with start, pause, and reset functionalities. It supports both counting up and counting down with a customizable interval. See [useTImer.md](references/useTImer.md) for details.
- useTabNotification: The useTabNotification() hook manages browser tab notifications through title modifications and favicon indicators. Use this to alert users of background activity or new notifications when they're in another tab. See [useTabNotification.md](references/useTabNotification.md) for details.
- useTitle: The `useTitle()` hook allows the dynamic update of the document's title from your React components! The title passed to this hook can be attached to a piece of state, updating the state will therefore also update the title. See [useTitle.md](references/useTitle.md) for details.
- useToggle: The `useToggle()` hook can toggle between a set of two possible values and automatically update the state with the new value, if you want to toggle a boolean's state, see `useBoolToggle()` below. See [useToggle.md](references/useToggle.md) for details.
- useUpdateEffect: The `useUpdateEffect()` hook will work exactly like a `useEffect()` hook, except it will skip the first render and only react to changes for values passed inside its dependency array after the initial render. See [useUpdateEffect.md](references/useUpdateEffect.md) for details.
- useUrgentUpdate: The `useUrgentUpdate()` hook forces a component to re-render when it gets called from anywhere inside it. See [useUrgentUpdate.md](references/useUrgentUpdate.md) for details.
- useWebSocket: The `useWebSocket()` hook manages WebSocket connections, providing automatic reconnection and state management. It includes functions to send messages and callbacks for different WebSocket events. See [useWebSocket.md](references/useWebSocket.md) for details.
- useWindowSize: The `useWindowSize()` hook provides the current window `width` and `height` dimensions. See [useWindowSize.md](references/useWindowSize.md) for details.

## Using Haiku with NextJS

Because Haiku uses ES6 modules, it is not transpiled by NextJS automatically since it's an external dependency, so you may have to follow a few extra steps to set it up correctly:

*NOTE: These steps should no longer be required in Next 14 projects.*

1. Add the `next-transpile-modules` package to your project:

```sh
npm install next-transpile-modules
```

2. Configure your project's `next.config.js` file to transpile Haiku:

```js
const withTM = require('next-transpile-modules')(['react-haiku']);
module.exports = withTM({});
```

After following these two steps, importing features from `react-haiku` into your project should work as expected!
