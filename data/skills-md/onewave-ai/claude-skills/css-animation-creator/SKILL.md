---
name: css-animation-creator
description: Create professional CSS animations, transitions, micro-interactions, and complex motion design. Use when adding animations, hover effects, loading states, page transitions, scroll animations, or any motion design work.
---

# CSS Animation Creator

## Instructions

When creating animations:

1. **Understand the purpose** - Feedback, delight, guidance, or storytelling
2. **Choose the right technique** - CSS transitions, keyframes, or JS libraries
3. **Optimize for performance** - GPU-accelerated properties only
4. **Respect accessibility** - Honor prefers-reduced-motion
5. **Keep timing natural** - Use appropriate easing and duration

## Animation Principles

### The 12 Principles (Disney) Applied to UI

| Principle | UI Application |
|-----------|----------------|
| **Squash & Stretch** | Button press, elastic effects |
| **Anticipation** | Hover states before action |
| **Staging** | Focus attention on important elements |
| **Follow Through** | Overshoot then settle |
| **Ease In/Out** | Natural acceleration/deceleration |
| **Arcs** | Curved motion paths |
| **Secondary Action** | Supporting animations |
| **Timing** | Duration conveys weight/importance |
| **Exaggeration** | Emphasis for clarity |
| **Appeal** | Pleasing, polished motion |

### Timing Guidelines

| Animation Type | Duration | Easing |
|----------------|----------|--------|
| Micro-interaction | 100-200ms | ease-out |
| Button/hover | 150-250ms | ease |
| Modal open | 200-300ms | ease-out |
| Modal close | 150-200ms | ease-in |
| Page transition | 300-500ms | ease-in-out |
| Loading loop | 1000-2000ms | linear/ease-in-out |
| Attention grab | 500-1000ms | elastic |

---

## CSS Transitions

### Basic Syntax

```css
.element {
  /* Single property */
  transition: opacity 0.3s ease;

  /* Multiple properties */
  transition:
    transform 0.3s ease,
    opacity 0.3s ease,
    background-color 0.2s ease;

  /* Shorthand: property duration timing-function delay */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) 0s;
}
```

### Easing Functions

```css
/* Built-in */
transition-timing-function: linear;
transition-timing-function: ease;        /* Default - slow start, fast middle, slow end */
transition-timing-function: ease-in;     /* Slow start */
transition-timing-function: ease-out;    /* Slow end */
transition-timing-function: ease-in-out; /* Slow start and end */

/* Custom cubic-bezier */
/* Material Design standard */
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

/* Decelerate (entering) */
transition-timing-function: cubic-bezier(0, 0, 0.2, 1);

/* Accelerate (exiting) */
transition-timing-function: cubic-bezier(0.4, 0, 1, 1);

/* Bounce effect */
transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Elastic */
transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

### Tailwind Transitions

```tsx
// Duration
<div className="transition duration-150" />  // 150ms
<div className="transition duration-300" />  // 300ms
<div className="transition duration-500" />  // 500ms

// Timing function
<div className="transition ease-linear" />
<div className="transition ease-in" />
<div className="transition ease-out" />
<div className="transition ease-in-out" />

// Specific properties (better performance)
<div className="transition-opacity" />
<div className="transition-transform" />
<div className="transition-colors" />
<div className="transition-shadow" />
<div className="transition-all" />

// Combined
<button className="transition-all duration-200 ease-out hover:scale-105 hover:shadow-lg">
  Hover me
</button>
```

---

## Keyframe Animations

### Basic Syntax

```css
@keyframes animationName {
  0% { /* starting state */ }
  50% { /* midpoint state */ }
  100% { /* ending state */ }
}

.element {
  animation: animationName 1s ease-in-out infinite;
  /* name | duration | timing | iteration-count */

  /* Full syntax */
  animation-name: animationName;
  animation-duration: 1s;
  animation-timing-function: ease-in-out;
  animation-delay: 0s;
  animation-iteration-count: infinite; /* or number */
  animation-direction: normal; /* reverse, alternate, alternate-reverse */
  animation-fill-mode: forwards; /* none, forwards, backwards, both */
  animation-play-state: running; /* paused */
}
```

### Essential Animations Library

#### Fade Animations

```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Fade In Up */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Down */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Left */
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Fade In Right */
@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Fade In Scale */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Fade Out */
@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}
```

#### Scale Animations

```css
/* Scale In */
@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

/* Scale In Bounce */
@keyframes scaleInBounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Pop */
@keyframes pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Heartbeat */
@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  14% { transform: scale(1.3); }
  28% { transform: scale(1); }
  42% { transform: scale(1.3); }
  70% { transform: scale(1); }
}
```

#### Bounce Animations

```css
/* Bounce */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
}

/* Bounce In */
@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

/* Bounce In Down */
@keyframes bounceInDown {
  0% {
    opacity: 0;
    transform: translateY(-100px);
  }
  60% {
    opacity: 1;
    transform: translateY(20px);
  }
  80% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

/* Rubber Band */
@keyframes rubberBand {
  0% { transform: scaleX(1); }
  30% { transform: scaleX(1.25) scaleY(0.75); }
  40% { transform: scaleX(0.75) scaleY(1.25); }
  50% { transform: scaleX(1.15) scaleY(0.85); }
  65% { transform: scaleX(0.95) scaleY(1.05); }
  75% { transform: scaleX(1.05) scaleY(0.95); }
  100% { transform: scaleX(1) scaleY(1); }
}
```

#### Rotate Animations

```css
/* Spin */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Spin Reverse */
@keyframes spinReverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

/* Swing */
@keyframes swing {
  20% { transform: rotate(15deg); }
  40% { transform: rotate(-10deg); }
  60% { transform: rotate(5deg); }
  80% { transform: rotate(-5deg); }
  100% { transform: rotate(0deg); }
}

/* Wobble */
@keyframes wobble {
  0% { transform: translateX(0); }
  15% { transform: translateX(-15px) rotate(-5deg); }
  30% { transform: translateX(12px) rotate(3deg); }
  45% { transform: translateX(-9px) rotate(-3deg); }
  60% { transform: translateX(6px) rotate(2deg); }
  75% { transform: translateX(-3px) rotate(-1deg); }
  100% { transform: translateX(0); }
}

/* Flip */
@keyframes flipX {
  0% { transform: perspective(400px) rotateX(90deg); opacity: 0; }
  40% { transform: perspective(400px) rotateX(-20deg); }
  60% { transform: perspective(400px) rotateX(10deg); opacity: 1; }
  80% { transform: perspective(400px) rotateX(-5deg); }
  100% { transform: perspective(400px) rotateX(0deg); }
}
```

#### Slide Animations

```css
/* Slide In Up */
@keyframes slideInUp {
  from {
    transform: translateY(100%);
    visibility: visible;
  }
  to { transform: translateY(0); }
}

/* Slide In Down */
@keyframes slideInDown {
  from {
    transform: translateY(-100%);
    visibility: visible;
  }
  to { transform: translateY(0); }
}

/* Slide In Left */
@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
    visibility: visible;
  }
  to { transform: translateX(0); }
}

/* Slide In Right */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    visibility: visible;
  }
  to { transform: translateX(0); }
}

/* Slide Out */
@keyframes slideOutUp {
  from { transform: translateY(0); }
  to {
    transform: translateY(-100%);
    visibility: hidden;
  }
}
```

#### Attention Seekers

```css
/* Shake */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

/* Shake Horizontal (stronger) */
@keyframes shakeX {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
  20%, 40%, 60%, 80% { transform: translateX(10px); }
}

/* Jello */
@keyframes jello {
  0%, 11.1%, 100% { transform: none; }
  22.2% { transform: skewX(-12.5deg) skewY(-12.5deg); }
  33.3% { transform: skewX(6.25deg) skewY(6.25deg); }
  44.4% { transform: skewX(-3.125deg) skewY(-3.125deg); }
  55.5% { transform: skewX(1.5625deg) skewY(1.5625deg); }
  66.6% { transform: skewX(-0.78125deg) skewY(-0.78125deg); }
  77.7% { transform: skewX(0.390625deg) skewY(0.390625deg); }
  88.8% { transform: skewX(-0.1953125deg) skewY(-0.1953125deg); }
}

/* Flash */
@keyframes flash {
  0%, 50%, 100% { opacity: 1; }
  25%, 75% { opacity: 0; }
}

/* Tada */
@keyframes tada {
  0% { transform: scale(1) rotate(0); }
  10%, 20% { transform: scale(0.9) rotate(-3deg); }
  30%, 50%, 70%, 90% { transform: scale(1.1) rotate(3deg); }
  40%, 60%, 80% { transform: scale(1.1) rotate(-3deg); }
  100% { transform: scale(1) rotate(0); }
}
```

---

## Loading Animations

### Spinners

```tsx
// Simple spinner
<div className="w-8 h-8 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin" />

// Dual ring
<div className="relative w-12 h-12">
  <div className="absolute inset-0 border-4 border-blue-200 rounded-full" />
  <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 rounded-full animate-spin" />
</div>

// Gradient spinner
<div className="w-10 h-10 rounded-full animate-spin"
  style={{
    background: 'conic-gradient(from 0deg, transparent, #3b82f6)',
    mask: 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px))'
  }}
/>
```

```css
/* Pulsing ring */
@keyframes pingRing {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.ping-ring {
  position: relative;
}

.ping-ring::before {
  content: '';
  position: absolute;
  inset: 0;
  border: 2px solid currentColor;
  border-radius: 50%;
  animation: pingRing 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}
```

### Dots Loading

```tsx
// Bouncing dots
<div className="flex gap-1">
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]" />
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]" />
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" />
</div>

// Pulsing dots
<div className="flex gap-1">
  {[0, 1, 2].map((i) => (
    <div
      key={i}
      className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"
      style={{ animationDelay: `${i * 0.15}s` }}
    />
  ))}
</div>
```

```css
/* Scaling dots */
@keyframes dotScale {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.dot-loader {
  display: flex;
  gap: 4px;
}

.dot-loader span {
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  animation: dotScale 1.4s ease-in-out infinite;
}

.dot-loader span:nth-child(1) { animation-delay: -0.32s; }
.dot-loader span:nth-child(2) { animation-delay: -0.16s; }
.dot-loader span:nth-child(3) { animation-delay: 0s; }
```

### Skeleton Loaders

```tsx
// Basic skeleton
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
  <div className="h-4 bg-gray-200 rounded w-5/6" />
</div>

// Card skeleton
<div className="animate-pulse">
  <div className="bg-gray-200 h-48 rounded-t-lg" />
  <div className="p-4 space-y-3">
    <div className="h-4 bg-gray-200 rounded w-3/4" />
    <div className="h-4 bg-gray-200 rounded w-1/2" />
  </div>
</div>

// Shimmer effect
<div className="relative overflow-hidden bg-gray-200 rounded">
  <div className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/60 to-transparent" />
</div>
```

```css
/* Shimmer keyframe */
@keyframes shimmer {
  100% { transform: translateX(100%); }
}
```

### Progress Bars

```tsx
// Indeterminate progress
<div className="h-1 w-full bg-gray-200 rounded overflow-hidden">
  <div className="h-full bg-blue-600 w-1/3 animate-[progress_1s_ease-in-out_infinite]" />
</div>

// Striped progress
<div className="h-2 w-full bg-gray-200 rounded overflow-hidden">
  <div
    className="h-full bg-blue-600 transition-all duration-300"
    style={{
      width: `${progress}%`,
      backgroundImage: 'linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%)',
      backgroundSize: '1rem 1rem',
      animation: 'progress-stripes 1s linear infinite'
    }}
  />
</div>
```

```css
@keyframes progress {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}

@keyframes progress-stripes {
  from { background-position: 1rem 0; }
  to { background-position: 0 0; }
}
```

---

## Micro-interactions

### Button Effects

```tsx
// Press effect
<button className="transition-transform duration-100 active:scale-95">
  Click me
</button>

// Ripple effect (React)
function RippleButton({ children, ...props }) {
  const [ripples, setRipples] = useState([]);

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setRipples([...ripples, { x, y, id: Date.now() }]);
    setTimeout(() => setRipples(r => r.slice(1)), 600);
  };

  return (
    <button className="relative overflow-hidden" onClick={handleClick} {...props}>
      {ripples.map(ripple => (
        <span
          key={ripple.id}
          className="absolute bg-white/30 rounded-full animate-[ripple_0.6s_ease-out]"
          style={{
            left: ripple.x,
            top: ripple.y,
            transform: 'translate(-50%, -50%)'
          }}
        />
      ))}
      {children}
    </button>
  );
}
```

```css
@keyframes ripple {
  from {
    width: 0;
    height: 0;
    opacity: 0.5;
  }
  to {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}
```

### Hover Effects

```tsx
// Lift effect
<div className="transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
  Card content
</div>

// Glow effect
<button className="transition-shadow duration-300 hover:shadow-[0_0_20px_rgba(59,130,246,0.5)]">
  Glow button
</button>

// Border animation
<div className="relative group">
  <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg blur opacity-0 group-hover:opacity-75 transition duration-300" />
  <div className="relative bg-white rounded-lg p-6">Content</div>
</div>

// Underline animation
<a className="relative inline-block after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-current after:transition-all after:duration-300 hover:after:w-full">
  Animated link
</a>

// Fill animation
<a className="relative overflow-hidden group">
  <span className="relative z-10 transition-colors duration-300 group-hover:text-white">
    Hover me
  </span>
  <span className="absolute inset-0 bg-blue-600 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300" />
</a>
```

### Icon Animations

```tsx
// Rotate on hover
<button className="group">
  <SettingsIcon className="transition-transform duration-500 group-hover:rotate-180" />
</button>

// Bounce on hover
<button className="group">
  <ArrowIcon className="transition-transform group-hover:translate-x-1 group-hover:animate-bounce" />
</button>

// Scale + rotate
<button className="group">
  <PlusIcon className="transition-all duration-300 group-hover:scale-110 group-hover:rotate-90" />
</button>
```

### Form Interactions

```tsx
// Input focus effect
<div className="relative">
  <input
    className="peer w-full border-b-2 border-gray-300 focus:border-blue-600 outline-none py-2 transition-colors"
    placeholder=" "
  />
  <label className="absolute left-0 top-2 text-gray-500 transition-all peer-focus:-top-4 peer-focus:text-sm peer-focus:text-blue-600 peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-sm">
    Email
  </label>
</div>

// Checkbox animation
<label className="flex items-center gap-2 cursor-pointer">
  <div className="relative">
    <input type="checkbox" className="peer sr-only" />
    <div className="w-5 h-5 border-2 rounded transition-colors peer-checked:bg-blue-600 peer-checked:border-blue-600" />
    <CheckIcon className="absolute inset-0 m-auto w-3 h-3 text-white opacity-0 scale-0 transition-all peer-checked:opacity-100 peer-checked:scale-100" />
  </div>
  Label text
</label>

// Toggle switch
<button
  role="switch"
  aria-checked={enabled}
  onClick={() => setEnabled(!enabled)}
  className={cn(
    "relative w-11 h-6 rounded-full transition-colors",
    enabled ? "bg-blue-600" : "bg-gray-200"
  )}
>
  <span className={cn(
    "absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform",
    enabled && "translate-x-5"
  )} />
</button>
```

### Success/Error States

```tsx
// Success checkmark
<div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
  <svg className="w-8 h-8 text-green-600" viewBox="0 0 24 24">
    <path
      className="animate-[draw_0.5s_ease-out_forwards]"
      fill="none"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray="24"
      strokeDashoffset="24"
      d="M5 13l4 4L19 7"
    />
  </svg>
</div>

// Error shake
<input className="animate-[shake_0.5s_ease-in-out] border-red-500" />
```

```css
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

---

## Page Transitions

### CSS-only Transitions

```css
/* View Transitions API (Chrome 111+) */
@view-transition {
  navigation: auto;
}

::view-transition-old(root) {
  animation: fadeOut 0.3s ease-out;
}

::view-transition-new(root) {
  animation: fadeIn 0.3s ease-in;
}

/* Specific element transitions */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 0.5s;
}
```

### Framer Motion

```tsx
import { motion, AnimatePresence } from 'framer-motion';

// Fade transition
const pageVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

function PageWrapper({ children }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        variants={pageVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

// Slide transition
const slideVariants = {
  initial: { opacity: 0, x: 20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -20 },
};

// Scale + fade
const scaleVariants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 1.05 },
};

// Shared layout animations
function Gallery({ items, selectedId }) {
  return (
    <>
      {items.map(item => (
        <motion.div key={item.id} layoutId={item.id}>
          <img src={item.src} />
        </motion.div>
      ))}

      <AnimatePresence>
        {selectedId && (
          <motion.div layoutId={selectedId} className="modal">
            <img src={items.find(i => i.id === selectedId).src} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

### Staggered Animations

```tsx
// Framer Motion stagger
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

function StaggeredList({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}

// CSS stagger with custom properties
<ul className="stagger-list">
  {items.map((item, i) => (
    <li
      key={item.id}
      style={{ '--i': i } as React.CSSProperties}
      className="animate-fadeInUp opacity-0"
    >
      {item.name}
    </li>
  ))}
</ul>
```

```css
.stagger-list li {
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: calc(var(--i) * 0.1s);
}
```

---

## Scroll Animations

### Intersection Observer

```tsx
function useInView(options = {}) {
  const ref = useRef(null);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsInView(true);
        if (options.once) observer.disconnect();
      }
    }, { threshold: 0.1, ...options });

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return [ref, isInView];
}

// Usage
function AnimatedSection() {
  const [ref, isInView] = useInView({ once: true });

  return (
    <div
      ref={ref}
      className={cn(
        "transition-all duration-700",
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
      )}
    >
      Content
    </div>
  );
}
```

### Scroll-triggered with Framer Motion

```tsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxSection() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);

  return (
    <motion.div ref={ref} style={{ y, opacity }}>
      Parallax content
    </motion.div>
  );
}

// Scroll-linked progress
function ScrollProgress() {
  const { scrollYProgress } = useScroll();

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-blue-600 origin-left"
      style={{ scaleX: scrollYProgress }}
    />
  );
}
```

### CSS Scroll-driven Animations

```css
/* Native scroll-driven animations (Chrome 115+) */
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}

/* Scroll progress indicator */
.progress-bar {
  transform-origin: left;
  animation: grow linear;
  animation-timeline: scroll();
}

@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

---

## Accessibility

### Reduced Motion

```css
/* Global reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Per-element control */
.animated-element {
  animation: bounce 1s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
  }
}
```

```tsx
// Tailwind motion-safe/motion-reduce
<div className="motion-safe:animate-bounce motion-reduce:animate-none">
  Respects preferences
</div>

// React hook
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedComponent() {
  const prefersReducedMotion = usePrefersReducedMotion();

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: prefersReducedMotion ? 0 : 0.3
      }}
    />
  );
}
```

---

## Tailwind Animation Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        // Fade
        'fade-in': 'fadeIn 0.5s ease forwards',
        'fade-in-up': 'fadeInUp 0.5s ease forwards',
        'fade-in-down': 'fadeInDown 0.5s ease forwards',
        'fade-out': 'fadeOut 0.3s ease forwards',

        // Slide
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-in-up': 'slideInUp 0.3s ease-out',
        'slide-in-down': 'slideInDown 0.3s ease-out',

        // Scale
        'scale-in': 'scaleIn 0.2s ease-out',
        'pop': 'pop 0.3s ease-out',

        // Attention
        'shake': 'shake 0.5s ease-in-out',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'heartbeat': 'heartbeat 1.5s ease-in-out infinite',

        // Loading
        'shimmer': 'shimmer 2s infinite',
        'progress': 'progress 1s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideInUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        slideInDown: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0)' },
          '100%': { transform: 'scale(1)' },
        },
        pop: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-5px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(5px)' },
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
        heartbeat: {
          '0%, 100%': { transform: 'scale(1)' },
          '14%': { transform: 'scale(1.3)' },
          '28%': { transform: 'scale(1)' },
          '42%': { transform: 'scale(1.3)' },
          '70%': { transform: 'scale(1)' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        progress: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(400%)' },
        },
      },
    },
  },
};
```

---

## Performance Best Practices

### GPU-Accelerated Properties

```css
/* GOOD - GPU accelerated */
transform: translateX(100px);
transform: scale(1.1);
transform: rotate(45deg);
opacity: 0.5;

/* BAD - Triggers layout/paint */
left: 100px;
top: 50px;
width: 200px;
height: 100px;
margin: 20px;
padding: 10px;
border-width: 2px;
font-size: 16px;
```

### will-change (Use Sparingly)

```css
/* Only when needed for complex animations */
.complex-animation {
  will-change: transform, opacity;
}

/* Remove after animation */
.complex-animation.done {
  will-change: auto;
}
```

### Contain for Isolation

```css
.animated-section {
  contain: layout style paint;
}
```

### Animation Performance Checklist

- [ ] Only animate `transform` and `opacity`
- [ ] Use `will-change` only when necessary
- [ ] Keep animations under 300ms for UI feedback
- [ ] Test on low-end devices
- [ ] Use `contain` for isolated sections
- [ ] Reduce animation during scroll
- [ ] Pause off-screen animations
