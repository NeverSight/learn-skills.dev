---
name: image-carousel
description: Creates image carousels with hover-activated auto-advance, touch swipe support, and animated progress indicators. Use when building image galleries, product showcases, or any multi-image display with navigation.
---

# Image Carousel Pattern

Build smooth image carousels that auto-advance on hover with touch swipe support and animated progress indicators.

## Core Features

- **Hover-activated**: Auto-advance starts only when user hovers (not on page load)
- **Touch swipe**: Mobile-friendly swipe navigation with threshold detection
- **Progress indicators**: Glassmorphic pill indicators with animated fill
- **Pause on interaction**: Manual navigation pauses auto-advance temporarily

## State Management

```tsx
const [currentIndex, setCurrentIndex] = useState(0);
const [isHovered, setIsHovered] = useState(false);
const [progressKey, setProgressKey] = useState(0);  // Forces animation restart
const [isPaused, setIsPaused] = useState(false);
const [touchStart, setTouchStart] = useState<number | null>(null);
```

## Core Implementation

```tsx
"use client";

import { useState, useEffect } from "react";
import Image from "next/image";

const images = [
  "/images/image-1.jpeg",
  "/images/image-2.jpeg",
  "/images/image-3.jpeg",
];

function ImageCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isHovered, setIsHovered] = useState(false);
  const [progressKey, setProgressKey] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [touchStart, setTouchStart] = useState<number | null>(null);

  // Auto-advance effect - only when hovered and not paused
  useEffect(() => {
    if (!isHovered || isPaused) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % images.length);
      setProgressKey((prev) => prev + 1);
    }, 3000);
    return () => clearInterval(interval);
  }, [isHovered, isPaused]);

  // Touch handlers
  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStart(e.touches[0].clientX);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStart === null) return;

    const touchEnd = e.changedTouches[0].clientX;
    const diff = touchStart - touchEnd;
    const threshold = 50;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        // Swipe left - next image
        setCurrentIndex((prev) => (prev + 1) % images.length);
      } else {
        // Swipe right - previous image
        setCurrentIndex((prev) => (prev - 1 + images.length) % images.length);
      }
      setProgressKey((prev) => prev + 1);
      setIsPaused(true);
      setTimeout(() => setIsPaused(false), 3000);
    }
    setTouchStart(null);
  };

  return (
    <div
      className="relative h-full w-full group touch-pan-y"
      onMouseEnter={() => {
        setIsHovered(true);
        setProgressKey((prev) => prev + 1);
      }}
      onMouseLeave={() => setIsHovered(false)}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* Images with fade transition */}
      {images.map((src, index) => (
        <Image
          key={src}
          src={src}
          alt={`Image ${index + 1}`}
          fill
          className={`object-cover transition-opacity duration-700 ease-in-out ${
            index === currentIndex ? "opacity-100" : "opacity-0"
          }`}
        />
      ))}

      {/* Glassmorphic indicator container */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2">
        <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-black/20 backdrop-blur-md border border-white/10">
          {images.map((_, index) => (
            <button
              key={index}
              onClick={() => {
                setCurrentIndex(index);
                setIsPaused(true);
                setProgressKey((prev) => prev + 1);
                setTimeout(() => setIsPaused(false), 3000);
              }}
              className="relative cursor-pointer"
            >
              {/* Background pill */}
              <div
                className={`h-2 rounded-full transition-all duration-300 ${
                  index === currentIndex
                    ? "w-6 bg-white"
                    : "w-2 bg-white/40 hover:bg-white/60"
                }`}
              />
              {/* Animated progress fill - only when hovered and not paused */}
              {index === currentIndex && isHovered && !isPaused && (
                <div
                  key={progressKey}
                  className="absolute inset-0 h-2 rounded-full bg-white/50 origin-left animate-carousel-progress"
                  style={{ animationDuration: "3000ms" }}
                />
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
```

## Required CSS (add to globals.css)

```css
/* Carousel progress animation */
@keyframes carousel-progress {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.animate-carousel-progress {
  animation: carousel-progress linear forwards;
}
```

## Key Behaviors

### Auto-Advance Logic
| State | Behavior |
|-------|----------|
| Not hovered | No auto-advance |
| Hovered + not paused | Auto-advance every 3s |
| Hovered + paused | No auto-advance (resumes after 3s) |

### Touch Swipe
- Threshold: 50px minimum swipe distance
- Left swipe: Next image
- Right swipe: Previous image
- After swipe: Pause auto-advance for 3s

### Progress Indicator
- Expands from dot (w-2) to pill (w-6) when active
- Shows animated fill overlay only when hovering and not paused
- `progressKey` forces animation restart on index change

## Indicator Sizing

| Context | Active Width | Inactive Width | Height |
|---------|-------------|----------------|--------|
| Preview (compact) | `w-4` | `w-1.5` | `h-1.5` |
| Detail page | `w-6` | `w-2` | `h-2` |

## Timing Configuration

| Duration | Use |
|----------|-----|
| `3000ms` | Auto-advance interval |
| `3000ms` | Pause duration after manual interaction |
| `700ms` | Image fade transition |
| `300ms` | Indicator pill expansion |

## Checklist

- [ ] `touch-pan-y` on container for proper scroll behavior
- [ ] Images use `fill` prop with `object-cover`
- [ ] `progressKey` state for animation restart
- [ ] Pause timeout clears and resumes correctly
- [ ] `animate-carousel-progress` keyframes added to globals.css
