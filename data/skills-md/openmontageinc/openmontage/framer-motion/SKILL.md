---
name: framer-motion
description: Use when implementing Disney's 12 animation principles with Framer Motion in React applications
---

# Framer Motion Animation Principles

Implement all 12 Disney animation principles using Framer Motion's declarative React API.

## 1. Squash and Stretch

```jsx
<motion.div
  animate={{ scaleX: [1, 1.2, 1], scaleY: [1, 0.8, 1] }}
  transition={{ duration: 0.3, times: [0, 0.5, 1] }}
/>
```

## 2. Anticipation

```jsx
<motion.div
  variants={{
    idle: { y: 0, scaleY: 1 },
    anticipate: { y: 10, scaleY: 0.9 },
    jump: { y: -200 }
  }}
  initial="idle"
  animate={["anticipate", "jump"]}
  transition={{ duration: 0.5, times: [0, 0.2, 1] }}
/>
```

## 3. Staging

```jsx
<motion.div animate={{ filter: "blur(3px)", opacity: 0.6 }} /> {/* bg */}
<motion.div animate={{ scale: 1.1, zIndex: 10 }} /> {/* hero */}
```

## 4. Straight Ahead / Pose to Pose

```jsx
<motion.div
  animate={{
    x: [0, 100, 200, 300],
    y: [0, -50, 0, -30]
  }}
  transition={{ duration: 1, ease: "easeInOut" }}
/>
```

## 5. Follow Through and Overlapping Action

```jsx
<motion.div animate={{ x: 200 }} transition={{ duration: 0.5 }}>
  <motion.span
    animate={{ x: 200 }}
    transition={{ duration: 0.5, delay: 0.05 }} // hair
  />
  <motion.span
    animate={{ x: 200 }}
    transition={{ duration: 0.6, delay: 0.1 }} // cape
  />
</motion.div>
```

## 6. Slow In and Slow Out

```jsx
<motion.div
  animate={{ x: 300 }}
  transition={{
    duration: 0.6,
    ease: [0.42, 0, 0.58, 1] // easeInOut cubic-bezier
  }}
/>
// Or use: "easeIn", "easeOut", "easeInOut"
```

## 7. Arc

```jsx
<motion.div
  animate={{
    x: [0, 100, 200],
    y: [0, -100, 0]
  }}
  transition={{ duration: 1, ease: "easeInOut" }}
/>
```

## 8. Secondary Action

```jsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  <motion.span
    animate={{ rotate: [0, 10, -10, 0] }}
    transition={{ duration: 0.3 }}
  >
    Icon
  </motion.span>
</motion.button>
```

## 9. Timing

```jsx
const timings = {
  fast: { duration: 0.15 },
  normal: { duration: 0.3 },
  slow: { duration: 0.6 },
  spring: { type: "spring", stiffness: 300, damping: 20 }
};
```

## 10. Exaggeration

```jsx
<motion.div
  animate={{ scale: 1.5, rotate: 720 }}
  transition={{
    type: "spring",
    stiffness: 200,
    damping: 10 // low damping = overshoot
  }}
/>
```

## 11. Solid Drawing

```jsx
<motion.div
  style={{ perspective: 1000 }}
  animate={{ rotateX: 45, rotateY: 30 }}
  transition={{ duration: 0.5 }}
/>
```

## 12. Appeal

```jsx
<motion.div
  whileHover={{
    scale: 1.02,
    boxShadow: "0 20px 40px rgba(0,0,0,0.2)"
  }}
  transition={{ duration: 0.3 }}
/>
```

## Stagger Children

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(item => <motion.li variants={itemVariant} />)}
</motion.ul>
```

## Key Framer Motion Features

- `animate` - Target state
- `variants` - Named animation states
- `whileHover` / `whileTap` - Gesture animations
- `transition` - Timing and easing
- `AnimatePresence` - Exit animations
- `useAnimation` - Programmatic control
- `layout` - Auto-animate layout changes
