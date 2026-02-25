---
name: react-hooks
description: >
  Generate production-ready custom React hooks for common UI patterns.
  Use when the user needs hooks for state management, DOM interactions,
  async operations, or responsive design in React applications.
  Covers: useToggle, useDebounce, useThrottle, useFetch, useAsync,
  useLocalStorage, useInterval, useKeyPress, useHover, useMediaQuery,
  useOnClickOutside, useOnScreen, useScrollToEnd, useScrolledPastThreshold,
  useWindowSize.
---

# React Hooks

A collection of 15 production-ready custom React hooks for common UI patterns.

## When to use

When the user asks to:
- Create or implement a custom React hook
- Add debouncing, throttling, or interval logic
- Handle DOM events (click outside, hover, key press, scroll, resize)
- Manage async data fetching
- Work with localStorage
- Detect screen size or media queries
- Track element visibility (intersection observer)

## Available Hooks

### State Hooks

#### useToggle
Boolean toggle with memoized callback.
```jsx
import { useState, useCallback } from 'react'

function useToggle(initialState = false) {
  const [state, setState] = useState(initialState)
  const toggle = useCallback(() => setState((prev) => !prev), [])
  return [state, toggle]
}
```
**Usage:** `const [isOpen, toggleOpen] = useToggle(false)`

#### useLocalStorage
Persist state to localStorage with JSON serialization.
```jsx
import { useState } from 'react'

function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.log(error)
      return initialValue
    }
  })

  function setValue(value) {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.log(error)
    }
  }

  return [storedValue, setValue]
}
```
**Usage:** `const [theme, setTheme] = useLocalStorage('theme', 'dark')`

### Timing Hooks

#### useDebounce
Debounce a value by a given delay.
```jsx
import { useState, useEffect } from 'react'

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}
```
**Usage:** `const debouncedSearch = useDebounce(searchTerm, 500)`

#### useThrottle
Throttle a function to execute at most once per delay period.
```jsx
import { useState, useEffect, useRef, useCallback } from 'react'

function useThrottle(fn, delay, dependencies) {
  const [state, setState] = useState(null)
  const timeoutRef = useRef(null)
  const lastExecutedRef = useRef(0)

  const callback = useCallback(
    (...args) => {
      const now = Date.now()
      const timeSinceLastExecution = now - lastExecutedRef.current

      if (!timeoutRef.current && timeSinceLastExecution > delay) {
        setState(fn(...args))
        lastExecutedRef.current = now
      } else if (!timeoutRef.current) {
        timeoutRef.current = setTimeout(() => {
          timeoutRef.current = null
          lastExecutedRef.current = Date.now()
        }, delay - timeSinceLastExecution)
      }
    },
    [fn, delay]
  )

  useEffect(() => {
    callback.dependencies = dependencies
    return () => clearTimeout(timeoutRef.current)
  }, [callback, dependencies])

  return callback
}
```

#### useInterval
Declarative setInterval with dynamic delay.
```jsx
import { useEffect, useRef } from 'react'

function useInterval(callback, delay) {
  const savedCallback = useRef()

  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  useEffect(() => {
    function tick() {
      savedCallback.current()
    }
    if (delay !== null) {
      const id = setInterval(tick, delay)
      return () => clearInterval(id)
    }
  }, [delay])
}
```
**Usage:** `useInterval(() => setCount(c => c + 1), 1000)`

### Async Hooks

#### useFetch
Fetch data from a URL with loading and error states.
```jsx
import { useState, useEffect } from 'react'

function useFetch(url) {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(err)
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [url])

  return { data, isLoading, error }
}
```
**Usage:** `const { data, isLoading, error } = useFetch('/api/users')`

#### useAsync
Run any async function with loading/error tracking.
```jsx
import { useState, useEffect } from 'react'

function useAsync(asyncFunction) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const response = await asyncFunction()
        setData(response)
      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [asyncFunction])

  return { data, loading, error }
}
```
**Usage:** `const { data, loading, error } = useAsync(fetchUserProfile)`

### DOM Hooks

#### useHover
Track hover state on a ref element.
```jsx
import { useState, useRef, useEffect } from 'react'

function useHover() {
  const [isHovered, setIsHovered] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const node = ref.current
    if (node) {
      const over = () => setIsHovered(true)
      const out = () => setIsHovered(false)
      node.addEventListener('mouseover', over)
      node.addEventListener('mouseout', out)
      return () => {
        node.removeEventListener('mouseover', over)
        node.removeEventListener('mouseout', out)
      }
    }
  }, [ref.current])

  return [ref, isHovered]
}
```
**Usage:** `const [hoverRef, isHovered] = useHover()`

#### useKeyPress
Detect if a specific key is currently pressed.
```jsx
import { useState, useEffect } from 'react'

function useKeyPress(targetKey) {
  const [isKeyPressed, setIsKeyPressed] = useState(false)

  useEffect(() => {
    const down = ({ key }) => { if (key === targetKey) setIsKeyPressed(true) }
    const up = ({ key }) => { if (key === targetKey) setIsKeyPressed(false) }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', up)
    return () => {
      window.removeEventListener('keydown', down)
      window.removeEventListener('keyup', up)
    }
  }, [targetKey])

  return isKeyPressed
}
```
**Usage:** `const isEscPressed = useKeyPress('Escape')`

#### useOnClickOutside
Run a handler when clicking outside a ref element.
```jsx
import { useEffect } from 'react'

function useOnClickOutside(ref, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (!ref.current || ref.current.contains(event.target)) return
      handler(event)
    }
    document.addEventListener('mousedown', listener)
    document.addEventListener('touchstart', listener)
    return () => {
      document.removeEventListener('mousedown', listener)
      document.removeEventListener('touchstart', listener)
    }
  }, [ref, handler])
}
```
**Usage:** `useOnClickOutside(dropdownRef, () => setOpen(false))`

#### useOnScreen
Detect if an element is visible in the viewport using IntersectionObserver.
```jsx
import { useState, useEffect, useRef } from 'react'

function useOnScreen(ref) {
  const [isIntersecting, setIsIntersecting] = useState(false)
  const observer = useRef(
    new IntersectionObserver(([entry]) => setIsIntersecting(entry.isIntersecting))
  )

  useEffect(() => {
    observer.current.disconnect()
    if (ref.current) observer.current.observe(ref.current)
    return () => observer.current.disconnect()
  }, [ref])

  return isIntersecting
}
```
**Usage:** `const isVisible = useOnScreen(sectionRef)`

### Scroll Hooks

#### useScrollToEnd
Detect if a scrollable container is scrolled to the bottom.
```jsx
import { useState, useEffect } from 'react'

function useScrollToEnd(ref) {
  const [isAtEnd, setIsAtEnd] = useState(false)

  useEffect(() => {
    const container = ref.current
    function handleScroll() {
      setIsAtEnd(
        container.scrollTop + container.clientHeight === container.scrollHeight
      )
    }
    container.addEventListener('scroll', handleScroll)
    return () => container.removeEventListener('scroll', handleScroll)
  }, [ref])

  return isAtEnd
}
```
**Usage:** `const isAtBottom = useScrollToEnd(chatContainerRef)`

#### useScrolledPastThreshold
Detect if the page has scrolled past a pixel threshold.
```jsx
import { useState, useEffect } from 'react'

function useScrolledPastThreshold(threshold) {
  const [scrolledPast, setScrolledPast] = useState(false)

  useEffect(() => {
    function handleScroll() {
      setScrolledPast(window.pageYOffset >= threshold)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [threshold])

  return scrolledPast
}
```
**Usage:** `const showBackToTop = useScrolledPastThreshold(500)`

### Responsive Hooks

#### useMediaQuery
Match against responsive breakpoints.
```jsx
import { useState, useEffect } from 'react'

const breakpoints = {
  sm: '(max-width: 576px)',
  md: '(min-width: 576px) and (max-width: 992px)',
  lg: '(min-width: 992px)',
}

function useMediaQuery(breakpoint) {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const mq = window.matchMedia(breakpoints[breakpoint])
    setMatches(mq.matches)
    const handler = (e) => setMatches(e.matches)
    mq.addListener(handler)
    return () => mq.removeListener(handler)
  }, [breakpoint])

  return matches
}
```
**Usage:** `const isMobile = useMediaQuery('sm')`

#### useWindowSize
Track the current window dimensions.
```jsx
import { useState, useEffect } from 'react'

function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  useEffect(() => {
    function handleResize() {
      setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return windowSize
}
```
**Usage:** `const { width, height } = useWindowSize()`

## Instructions for the agent

When the user asks for a hook:
1. Identify which hook(s) match their need from the list above.
2. Provide the hook implementation, adapting it to their project (TypeScript if they use TS, JavaScript otherwise).
3. Show a usage example in context.
4. If no hook above matches exactly, compose a solution using these hooks as building blocks.
