---
name: slidev-components
description: Leverage Vue components in Slidev slides. Use this skill to add interactivity with built-in components or create custom ones.
---

# Slidev Components

This skill covers using Vue components in Slidev, including all built-in components and how to create custom interactive elements for your presentations.

## When to Use This Skill

- Adding interactive elements to slides
- Using built-in Slidev components
- Creating custom Vue components
- Building reusable presentation elements
- Adding dynamic content

## Using Components

Components can be used directly in Markdown:

```markdown
# My Slide

<MyComponent />

<Counter :start="5" />
```

## Built-in Components

### Arrow

Draws an arrow between points.

```markdown
<Arrow x1="10" y1="20" x2="100" y2="200" />

<Arrow
  x1="10"
  y1="20"
  x2="100"
  y2="200"
  color="#f00"
  width="3"
/>
```

**Props**:
- `x1`, `y1`: Start coordinates
- `x2`, `y2`: End coordinates
- `color`: Arrow color
- `width`: Line width

### VDragArrow

Draggable arrow (useful for presentations).

```markdown
<VDragArrow />
```

### AutoFitText

Automatically adjusts font size to fit container.

```markdown
<AutoFitText :max="200" :min="50" modelValue="My Text" />
```

**Props**:
- `max`: Maximum font size
- `min`: Minimum font size
- `modelValue`: Text content

### LightOrDark

Renders different content based on theme.

```markdown
<LightOrDark>
  <template #light>
    <img src="/logo-dark.png" />
  </template>
  <template #dark>
    <img src="/logo-light.png" />
  </template>
</LightOrDark>
```

### Link

Navigation link to other slides.

```markdown
<Link to="42">Go to slide 42</Link>

<Link to="/intro">Go to intro</Link>
```

### SlideCurrentNo / SlidesTotal

Display slide numbers.

```markdown
Slide <SlideCurrentNo /> of <SlidesTotal />
```

### Toc (Table of Contents)

Generates a table of contents.

```markdown
<Toc />

<Toc maxDepth="2" />

<Toc mode="onlyCurrentTree" />
```

**Props**:
- `maxDepth`: Maximum heading depth
- `mode`: Display mode (`all`, `onlyCurrentTree`, `onlySiblings`)

### Transform

Applies CSS transforms.

```markdown
<Transform :scale="1.5">
  <div>Scaled content</div>
</Transform>

<Transform :scale="0.8" :rotate="10">
  Rotated and scaled
</Transform>
```

**Props**:
- `scale`: Scale factor
- `rotate`: Rotation in degrees

### Tweet

Embeds a tweet.

```markdown
<Tweet id="1234567890" />

<Tweet id="1234567890" scale="0.8" />
```

### Youtube

Embeds a YouTube video.

```markdown
<Youtube id="dQw4w9WgXcQ" />

<Youtube id="dQw4w9WgXcQ" width="560" height="315" />
```

**Props**:
- `id`: YouTube video ID
- `width`, `height`: Dimensions

### SlidevVideo

Embeds a video file.

```markdown
<SlidevVideo v-click autoplay controls>
  <source src="/video.mp4" type="video/mp4" />
</SlidevVideo>
```

**Props**:
- `autoplay`: Auto-play on slide enter
- `controls`: Show video controls
- `loop`: Loop video

### RenderWhen

Conditional rendering based on context.

```markdown
<RenderWhen context="slide">
  Only visible in slide view
</RenderWhen>

<RenderWhen context="presenter">
  Only visible in presenter view
</RenderWhen>
```

**Context options**: `slide`, `presenter`, `previewNext`, `print`

### VDrag

Makes elements draggable.

```markdown
<VDrag>
  <div class="p-4 bg-blue-500 text-white">
    Drag me!
  </div>
</VDrag>

<VDrag :initialX="100" :initialY="50">
  Positioned draggable
</VDrag>
```

## Animation Components

### VClick

Reveals on click.

```markdown
<v-click>

Revealed on first click

</v-click>

<v-click at="2">

Revealed on second click

</v-click>
```

### VClicks

Reveals children sequentially.

```markdown
<v-clicks>

- First item
- Second item
- Third item

</v-clicks>
```

**Props**:
- `depth`: Depth for nested lists
- `every`: Items per click

### VAfter

Reveals with the previous element.

```markdown
<v-click>First</v-click>
<v-after>Appears with first</v-after>
```

### VSwitch

Switches between content based on clicks.

```markdown
<v-switch>
  <template #1>Step 1 content</template>
  <template #2>Step 2 content</template>
  <template #3>Step 3 content</template>
</v-switch>
```

## Creating Custom Components

### Basic Component

Create `components/Counter.vue`:

```vue
<script setup>
import { ref } from 'vue'

const props = defineProps({
  start: {
    type: Number,
    default: 0
  }
})

const count = ref(props.start)
</script>

<template>
  <div class="counter">
    <button @click="count--">-</button>
    <span class="count">{{ count }}</span>
    <button @click="count++">+</button>
  </div>
</template>

<style scoped>
.counter {
  display: flex;
  align-items: center;
  gap: 1rem;
}
button {
  padding: 0.5rem 1rem;
  font-size: 1.5rem;
  cursor: pointer;
}
.count {
  font-size: 2rem;
  min-width: 3rem;
  text-align: center;
}
</style>
```

Usage:

```markdown
# Interactive Counter

<Counter :start="10" />
```

### Component with Slots

```vue
<!-- components/Card.vue -->
<script setup>
defineProps({
  title: String,
  color: {
    type: String,
    default: 'blue'
  }
})
</script>

<template>
  <div :class="`card card-${color}`">
    <h3 v-if="title">{{ title }}</h3>
    <slot />
  </div>
</template>

<style scoped>
.card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin: 1rem 0;
}
.card-blue { background: #3b82f6; color: white; }
.card-green { background: #22c55e; color: white; }
.card-red { background: #ef4444; color: white; }
</style>
```

Usage:

```markdown
<Card title="Important" color="red">
  This is a red card with important content.
</Card>
```

### Component with Slidev Context

```vue
<!-- components/ProgressBar.vue -->
<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const { currentSlideNo, total } = useNav()

const progress = computed(() =>
  (currentSlideNo.value / total.value) * 100
)
</script>

<template>
  <div class="progress-bar">
    <div
      class="progress"
      :style="{ width: `${progress}%` }"
    />
  </div>
</template>

<style scoped>
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #e5e7eb;
}
.progress {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}
</style>
```

### Code Demo Component

```vue
<!-- components/CodeDemo.vue -->
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  code: String,
  language: {
    type: String,
    default: 'javascript'
  }
})

const output = ref('')
const error = ref('')

const run = () => {
  try {
    output.value = eval(props.code)
    error.value = ''
  } catch (e) {
    error.value = e.message
    output.value = ''
  }
}
</script>

<template>
  <div class="code-demo">
    <pre><code>{{ code }}</code></pre>
    <button @click="run">Run</button>
    <div v-if="output" class="output">{{ output }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>
```

## Composables

### useNav

Access navigation state:

```vue
<script setup>
import { useNav } from '@slidev/client'

const {
  currentSlideNo,  // Current slide number
  total,           // Total slides
  next,            // Go to next
  prev,            // Go to previous
  go               // Go to specific slide
} = useNav()
</script>
```

### useSlideContext

Access slide context:

```vue
<script setup>
import { useSlideContext } from '@slidev/client'

const {
  $slidev,         // Global context
  $clicks,         // Current click count
  $page            // Current page number
} = useSlideContext()
</script>
```

## Global Components

### global-top.vue

Appears above all slides:

```vue
<!-- global-top.vue -->
<template>
  <div class="absolute top-4 right-4">
    <img src="/logo.png" class="h-8" />
  </div>
</template>
```

### global-bottom.vue

Appears below all slides:

```vue
<!-- global-bottom.vue -->
<template>
  <footer class="absolute bottom-4 left-4 text-sm opacity-50">
    © 2025 My Company
  </footer>
</template>
```

## Component Patterns

### Progress Indicator

```markdown
<div class="fixed bottom-4 right-4 text-sm">
  <SlideCurrentNo /> / <SlidesTotal />
</div>
```

### Social Links

```vue
<!-- components/SocialLinks.vue -->
<template>
  <div class="flex gap-4">
    <a href="https://twitter.com/..." target="_blank">
      <carbon-logo-twitter class="text-2xl" />
    </a>
    <a href="https://github.com/..." target="_blank">
      <carbon-logo-github class="text-2xl" />
    </a>
  </div>
</template>
```

### QR Code

```vue
<!-- components/QRCode.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import QRCodeLib from 'qrcode'

const props = defineProps({
  url: String,
  size: { type: Number, default: 200 }
})

const qrDataUrl = ref('')

onMounted(async () => {
  qrDataUrl.value = await QRCodeLib.toDataURL(props.url, {
    width: props.size
  })
})
</script>

<template>
  <img :src="qrDataUrl" :width="size" :height="size" />
</template>
```

## Best Practices

1. **Keep Components Simple**: Focus on single responsibilities
2. **Use Props**: Make components configurable
3. **Style Scoped**: Avoid global style pollution
4. **Document Usage**: Add comments showing how to use
5. **Test Interactivity**: Verify components work in presenter mode

## Output Format

When creating components, provide:

```
COMPONENT: [name]
PURPOSE: [what it does]

FILE: components/[Name].vue
---
<script setup>
[script content]
</script>

<template>
[template content]
</template>

<style scoped>
[styles]
</style>
---

USAGE IN SLIDES:
```markdown
<[Name] prop="value" />
```

PROPS:
- [propName]: [type] - [description]
```
