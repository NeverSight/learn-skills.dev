---
name: stitch-to-page-conversion
description: Convert Google Stitch exports (HTML/Images) into project-specific React pages and design similar layouts.
triggers:
  - "convert stitch export"
  - "create page from image"
  - "implement design from html export"
  - "dựng trang từ thiết kế stitch"
---

# Stitch-to-Page Conversion Guidelines

This skill enables the agent to transform design exports from Google Stitch (or similar tools) into functional, high-quality React pages that follow the project's architecture and design system.

## Workflow

### 1. Analysis phase
- **Image Analysis**: Review provided screenshots or reference images to identify layout structure (grids, sections), typography (font sizes, weights), color schemes (hex codes, gradients), and spacing (paddings, margins).
- **HTML/CSS Analysis**: Extract semantic structure from exported HTML. Identify key styles in the CSS and map them to the project's styling tool (e.g., Tailwind CSS).
- **Design Intent**: Understand the purpose of each section (Hero, Features, Testimonials, etc.) to choose the most appropriate components and structure.

### 2. Component Mapping
- Identify existing components in `components/` that can be reused or extended.
- If a new component is needed, design it to be modular and consistent with the project's "Rich Aesthetics" guidelines (vibrant colors, smooth transitions, premium feel).

### 3. Page Implementation
- Create a new page component in `pages/` (or the appropriate directory).
- Use **Semantic HTML** (header, main, section, footer).
- Apply **Advanced Aesthetics**: Use gradients, hover effects, and micro-animations to make the interface feel "alive".
- Ensure **Responsiveness**: Implement mobile-first designs with appropriate breakpoints.

### 4. Pattern Generalization
- Extract reusable logic and style patterns from the Stitch export.
- Use these patterns to build "similar designs" for other pages as requested, ensuring a cohesive look and feel across the entire application.

## Quality Standards
- **Performance**: Optimize image loading (use Next.js Image or similar) and minimize layout shifts.
- **Clean Code**: Follow React/TypeScript best practices. Use descriptive names and clear structures.
- **Visual Accuracy**: The generated page should be a "pixel-perfect" or "premium-enhanced" version of the reference design.
