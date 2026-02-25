---
name: cinematic-slides
description: "Create cinematic HTML presentations with AI video backgrounds, deployed to GitHub Pages. Use for: slides, presentation, deck, cinematic slides, video presentation, animated slides, live presentation."
enhancedBy:
  - presentation-architect: "Design slide structure and narrative"
  - image-generation: "Generate poster images and videos for each slide"
  - gh-pages-deploy: "Deploy final presentation to GitHub Pages"
  - whatsapp: "Send the live URL after deployment"
---

# Cinematic Slides

End-to-end pipeline: idea -> structured slides -> HTML -> AI images -> AI videos -> GitHub Pages.

Produces a single-file HTML presentation with looping AI video backgrounds per slide, keyboard navigation, and fullscreen 1920x1080 layout.

## Pipeline

### Step 1: Content Architecture

Use **presentation-architect** skill to create the slide plan:
- Get topic, audience, tone from user
- Output: structured markdown with slide-by-slide content, headlines, descriptions, visual direction
- Each slide needs a **visual prompt** describing the background mood/scene

### Step 2: Build HTML Presentation

Create a single `index.html` (or `slides.html`) with:

**Layout specs:**
- 1920x1080 fixed slides, centered with CSS transform scaling
- `position: fixed` slides, toggle `.active` class
- Keyboard navigation (left/right arrows + click)
- Slide counter at bottom
- RTL direction for Hebrew content
- Google Fonts (Heebo for Hebrew, or as needed)

**Per-slide CSS pattern:**
```css
#slideN {
  background: [gradient-overlay], url('presentation/slide-N.jpg') center/cover no-repeat;
}
```

**Video background CSS (global):**
```css
.slide-video {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  z-index: 0;
  opacity: 0.25;
}
.slide > *:not(.slide-video) {
  position: relative;
  z-index: 1;
}
```

**Per-slide video element:**
```html
<video class="slide-video" autoplay muted loop playsinline>
  <source src="presentation/videos/slide-N.mp4" type="video/mp4">
</video>
```

**Navigation JS:**
```js
// Arrow keys: Right/Down = next, Left/Up = previous (standard, NOT RTL-flipped)
// Click/touch also advances
// Auto-scale to viewport
```

**Preload images** in `<head>` with `<link rel="preload" as="image">` for each slide.

### Step 3: Generate Images

Use **image-generation** skill for each slide:
- One image per slide based on visual prompt from Step 1
- Save to `presentation/slide-NN-name.jpg`
- Default aspect ratio: 16:9 (matches 1920x1080)
- Run all generations in parallel

### Step 4: Generate Videos

Use **image-generation** skill (video mode) for each slide:
- Image-to-video from each slide's poster image
- **Always use "static camera, no movement, rock steady tripod shot"** in prompt
- Add subtle ambient effects only (light shifts, particles, shimmer)
- Save to `presentation/videos/slide-NN.mp4`
- Run all generations in parallel

### Step 5: Deploy

Use **gh-pages-deploy** skill:
- Copy HTML as `index.html` + `presentation/` folder (images + videos) to deploy directory
- Push to GitHub Pages
- Return live URL

### Step 6: Share (optional)

Use **whatsapp** skill to send the live URL if requested (WAME).

## Video Background Guidelines

- **Static camera only** - no pans, zooms, or Ken Burns effects
- **Opacity 0.25** on video element - keeps text clearly readable over dark backgrounds
- **Gradient overlay** on background image as fallback while video loads
- **autoplay muted loop playsinline** - silent infinite loop
- Ambient motion only: light shifts, floating particles, subtle glow

## File Structure

```
project-folder/
  slides.html              # Main presentation (renamed to index.html on deploy)
  presentation/
    slide-01-name.jpg      # Poster images
    slide-02-name.jpg
    ...
    videos/
      slide-01.mp4         # Video backgrounds
      slide-02.mp4
      ...
```

## User Input

Minimum needed from user:
- **Topic/idea** - what the presentation is about
- **Audience** - who is watching
- **Language** - Hebrew (default) or English
- **Slide count** - approximate number (default: 8-12)
- **Repo name** - for GitHub Pages URL (default: derived from topic)

Everything else is handled by the pipeline.

## Quick Reference

| Step | Skill Used | Output |
|------|-----------|--------|
| Content | presentation-architect | Slide plan markdown |
| HTML | (direct) | Single-file HTML presentation |
| Images | image-generation | One JPG per slide |
| Videos | image-generation (video) | One MP4 per slide |
| Deploy | gh-pages-deploy | Live URL |
| Share | whatsapp (optional) | Message sent |
