---
name: framer-motion
description: Framer Motion animations - motion components, variants, gestures, layout animations. Use when adding UI animations, transitions, or interactive motion effects.
---

# Framer Motion

## Basic Animation

```tsx
import { motion } from 'framer-motion'

function AnimatedBox() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      Hello World
    </motion.div>
  )
}
```

## Animate Properties

```tsx
<motion.div
  animate={{
    x: 100,
    y: 50,
    scale: 1.2,
    rotate: 180,
    opacity: 0.5,
    backgroundColor: '#ff0000',
    borderRadius: '50%',
  }}
  transition={{
    duration: 0.5,
    ease: 'easeInOut',
    delay: 0.2,
  }}
/>
```

## Transition Types

```tsx
// Spring (default)
transition={{ type: 'spring', stiffness: 100, damping: 10 }}

// Tween
transition={{ type: 'tween', duration: 0.5, ease: 'easeInOut' }}

// Inertia
transition={{ type: 'inertia', velocity: 50 }}

// Ease presets
ease: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut' | 'circIn' | 'circOut' | 'backIn' | 'backOut' | 'anticipate'
```

## Variants

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
}

function List({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

## Hover, Tap, Focus

```tsx
<motion.button
  whileHover={{ scale: 1.05, backgroundColor: '#3b82f6' }}
  whileTap={{ scale: 0.95 }}
  whileFocus={{ boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.5)' }}
>
  Click me
</motion.button>
```

## Drag

```tsx
<motion.div
  drag                    // Enable both axes
  drag="x"                // Horizontal only
  dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
  dragElastic={0.2}       // Elasticity outside constraints
  dragMomentum={true}     // Continue after release
  onDragStart={(e, info) => console.log(info.point)}
  onDrag={(e, info) => console.log(info.delta)}
  onDragEnd={(e, info) => console.log(info.velocity)}
/>
```

## Scroll Animations

```tsx
import { motion, useScroll, useTransform } from 'framer-motion'

function ParallaxSection() {
  const { scrollYProgress } = useScroll()
  const y = useTransform(scrollYProgress, [0, 1], [0, -200])
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [1, 0.5, 0])

  return (
    <motion.div style={{ y, opacity }}>
      Parallax Content
    </motion.div>
  )
}

// Scroll-triggered animation
function ScrollTriggered() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6 }}
    >
      Appears on scroll
    </motion.div>
  )
}
```

## Layout Animations

```tsx
function LayoutExample() {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      style={{
        width: isExpanded ? 300 : 100,
        height: isExpanded ? 200 : 100,
      }}
      transition={{ layout: { duration: 0.3 } }}
    />
  )
}

// Shared layout
import { LayoutGroup } from 'framer-motion'

function Tabs() {
  const [selected, setSelected] = useState(0)

  return (
    <LayoutGroup>
      {tabs.map((tab, i) => (
        <button key={tab} onClick={() => setSelected(i)}>
          {tab}
          {selected === i && (
            <motion.div layoutId="underline" className="underline" />
          )}
        </button>
      ))}
    </LayoutGroup>
  )
}
```

## AnimatePresence (Exit Animations)

```tsx
import { AnimatePresence, motion } from 'framer-motion'

function Modal({ isOpen, onClose }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.2 }}
        >
          <ModalContent onClose={onClose} />
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

## useAnimate Hook

```tsx
import { useAnimate } from 'framer-motion'

function SequenceAnimation() {
  const [scope, animate] = useAnimate()

  const handleClick = async () => {
    await animate(scope.current, { scale: 1.2 })
    await animate(scope.current, { rotate: 180 })
    await animate(scope.current, { scale: 1, rotate: 0 })
  }

  return (
    <motion.div ref={scope} onClick={handleClick}>
      Click for sequence
    </motion.div>
  )
}
```

## Motion Values

```tsx
import { motion, useMotionValue, useTransform } from 'framer-motion'

function MotionValueExample() {
  const x = useMotionValue(0)
  const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])
  const background = useTransform(
    x,
    [-200, 0, 200],
    ['#ff0000', '#00ff00', '#0000ff']
  )

  return (
    <motion.div
      drag="x"
      style={{ x, opacity, background }}
    />
  )
}
```

## Stagger Children

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3,
    },
  },
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map((i) => (
    <motion.li key={i} variants={item} />
  ))}
</motion.ul>
```

## Loading Skeleton

```tsx
function Skeleton() {
  return (
    <motion.div
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 1.5, repeat: Infinity }}
      className="bg-gray-200 rounded h-4"
    />
  )
}
```

## Number Counter

```tsx
import { motion, useSpring, useTransform } from 'framer-motion'

function Counter({ value }) {
  const spring = useSpring(0, { stiffness: 100, damping: 30 })
  const display = useTransform(spring, (v) => Math.round(v))

  useEffect(() => {
    spring.set(value)
  }, [value, spring])

  return <motion.span>{display}</motion.span>
}
```
