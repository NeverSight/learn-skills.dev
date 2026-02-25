---
name: ppt-brand-guidelines
description: PPT brand guidelines for VRL presentations. Use when creating slides, decks, or any presentation materials. Provides color palette, logo usage, and minimal design principles.
---

# VRL PPT Brand Guidelines

Modern, clean brand guidelines for VRL presentations featuring the lime green logo.

## Brand Identity

**Logo**: Lime green rounded square with dark lightning bolt icon
**Style**: Modern, tech-forward, bold yet clean

## Brand Colors

### Primary Palette

| Color | Hex | Role |
|-------|-----|------|
| **Lime Green** | `#BDFF00` | Brand color (from logo) |
| **Dark Navy** | `#1E293B` | Primary dark, backgrounds, text |
| **White** | `#FFFFFF` | Light backgrounds, text on dark |

### Supporting Colors

| Color | Hex | Role |
|-------|-----|------|
| **Slate Gray** | `#64748B` | Secondary text, muted elements |
| **Light Slate** | `#94A3B8` | Tertiary text, captions |
| **Off White** | `#F8FAFC` | Card backgrounds on white |

## Logo Usage

### CRITICAL RULES
- **NEVER apply CSS filters** to the logo (no brightness, invert, etc.)
- Logo is self-contained with lime green background - use AS-IS
- Logo works on both dark and light backgrounds without modification

### Placement
- **Title slide**: Centered, 70-80pt, above title
- **Closing slide**: Centered, 80pt
- **Content slides**: Optional, bottom-right, 24pt

## Typography

### Font
- **Primary**: Arial, Helvetica, sans-serif
- **Weights**: Bold for headers, Regular for body

### Scale
| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Hero Title | 42-48pt | Bold | White |
| Section Title | 24-28pt | Bold | Dark Navy |
| Subtitle | 14-16pt | Regular | Light Slate |
| Body | 11-13pt | Regular | Dark Navy or Slate |
| Caption | 9-10pt | Regular | Slate Gray |

## Slide Layouts

### 1. Title Slide (Hero)
**Background**: Dark Navy (#1E293B)

```
┌─────────────────────────────────────┐
│                                     │
│         [LOGO - as-is]              │
│                                     │
│     MAIN TITLE (white, 42pt)        │
│                                     │
│   subtitle (light slate, 14pt)      │
│                                     │
│         date (slate, 10pt)          │
└─────────────────────────────────────┘
```

**IMPORTANT**:
- NO CSS filters on logo
- NO accent lines between title elements
- Simple, clean vertical stack
- Generous spacing between elements

### 2. Content Slide
**Background**: White (#FFFFFF)

```
┌─────────────────────────────────────┐
│ HEADER (dark navy, 24pt, bold)      │
│                                     │
│  Content with clean layout          │
│  Cards use #F8FAFC background       │
│                                     │
└─────────────────────────────────────┘
```

- Header: Dark Navy, bold, left-aligned
- NO underlines or accent lines under headers
- Cards: Off White (#F8FAFC) with 8pt radius

### 3. Data/Stats Slide
- Large numbers: Lime Green (#BDFF00) or Dark Navy
- Labels: Slate Gray (#64748B)
- Clean grid layout

### 4. Table Slide
- Header: Dark Navy background, white text
- Body: Alternating white/#F8FAFC rows
- Highlight: Lime Green background for emphasis column

### 5. Closing Slide
**Background**: Dark Navy (#1E293B)
- Logo centered (as-is, no filters)
- Tagline in white
- Summary stats in Lime Green

## Design Rules

### DO
- Use logo AS-IS without any CSS filters
- Dark Navy (#1E293B) for hero/closing slides
- White for content slides
- Lime Green for key stats and highlights only
- Clean, simple layouts
- Generous whitespace (40%+)

### DON'T
- Apply brightness/invert filters to logo
- Use accent lines that overlap text
- Add decorative elements
- Use circular badges or icons
- Mix too many colors
- Add borders or frames

## CSS Guidelines

### Logo in HTML (Title/Closing slides)
```css
.logo {
  width: 70pt;
  height: 70pt;
  /* NO FILTER - use logo as-is */
}
.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

### Title Slide Body
```css
body {
  background: #1E293B;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
```

### Card Styling
```css
.card {
  background: #F8FAFC;
  padding: 18pt;
  border-radius: 8pt;
}
```

### Highlighted Card
```css
.card.highlight {
  background: #BDFF00;
  color: #1E293B;
}
```

## Example Slide Specs

### Title Slide
- Background: #1E293B
- Logo: 70pt, centered, NO FILTER
- Title: white, 42pt, bold
- Subtitle: #94A3B8, 14pt
- Date: #64748B, 10pt
- Spacing: 25pt between elements

### Content Slide
- Background: #FFFFFF
- Header: #1E293B, 24pt, bold
- Cards: #F8FAFC, 8pt radius, 18pt padding
- Body text: #1E293B, 11pt

## Assets

Logo file: `assets/logo.png` (lime green with lightning bolt - use as-is)
