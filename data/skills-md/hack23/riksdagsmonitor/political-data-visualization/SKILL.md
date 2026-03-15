---
name: political-data-visualization
description: CSS-only data visualization (charts, heat maps, progress bars) for political metrics on static websites
license: Apache-2.0
---

# Political Data Visualization

## Purpose

Create compelling, accessible data visualizations using pure HTML/CSS (no JavaScript) to display political metrics, voting patterns, parliamentary activity, and democratic accountability indicators for riksdagsmonitor.

## Core Principles

1. **CSS-Only**: No JavaScript frameworks - pure HTML/CSS for reliability and security
2. **Accessibility First**: WCAG 2.1 AA compliant, screen reader friendly
3. **Semantic Markup**: Use `<table>` with ARIA for complex data
4. **Progressive Disclosure**: Show summary, reveal details on interaction
5. **Color-Blind Safe**: Multiple visual cues beyond color (patterns, labels, icons)
6. **Responsive Design**: Adapt visualizations to mobile/tablet/desktop
7. **Performance**: Minimal CSS, no external libraries, fast rendering

## Visualization Types

### Progress Bars (Voting Discipline, Party Cohesion)
```css
/* Semantic HTML */
<div class="progress" role="progressbar" aria-valuenow="87" aria-valuemin="0" aria-valuemax="100">
  <span class="progress-label">Party Cohesion: 87%</span>
  <div class="progress-bar" style="--value: 87%"></div>
</div>

/* CSS implementation */
.progress {
  position: relative;
  width: 100%;
  height: 2rem;
  background: var(--dark-bg);
  border-radius: 0.5rem;
  overflow: hidden;
  border: 2px solid var(--primary-cyan);
}

.progress-bar {
  height: 100%;
  width: var(--value);
  background: linear-gradient(90deg, var(--primary-magenta), var(--primary-cyan));
  transition: width 0.5s ease-in-out;
}

.progress-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--light-text);
  font-weight: bold;
  z-index: 1;
}
```

### Bar Charts (MPs by Party, Committee Activity)
```css
/* Horizontal bar chart */
<div class="bar-chart">
  <div class="bar-row">
    <span class="bar-label">S (Social Democrats)</span>
    <div class="bar" style="--value: 30%; --color: var(--party-s)">
      <span class="bar-value">107 MPs</span>
    </div>
  </div>
  <div class="bar-row">
    <span class="bar-label">M (Moderates)</span>
    <div class="bar" style="--value: 19%; --color: var(--party-m)">
      <span class="bar-value">68 MPs</span>
    </div>
  </div>
</div>

/* CSS */
.bar-chart {
  display: grid;
  gap: 1rem;
}

.bar-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  align-items: center;
  gap: 1rem;
}

.bar {
  position: relative;
  height: 2.5rem;
  width: var(--value);
  max-width: 100%;
  background: var(--color);
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
}

.bar-value {
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 767px) {
  .bar-row {
    grid-template-columns: 1fr;
  }
  
  .bar-label {
    font-size: 0.875rem;
  }
}
```

### Heat Maps (Voting Patterns, Committee Attendance)
```css
/* Grid-based heat map */
<div class="heat-map">
  <div class="heat-cell" style="--intensity: 1.0" title="100% attendance">
    <span class="sr-only">100% attendance</span>
  </div>
  <div class="heat-cell" style="--intensity: 0.75" title="75% attendance">
    <span class="sr-only">75% attendance</span>
  </div>
  <div class="heat-cell" style="--intensity: 0.5" title="50% attendance">
    <span class="sr-only">50% attendance</span>
  </div>
</div>

/* CSS */
.heat-map {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(2rem, 1fr));
  gap: 0.25rem;
}

.heat-cell {
  aspect-ratio: 1;
  background: color-mix(
    in srgb,
    var(--primary-magenta) calc(var(--intensity) * 100%),
    var(--dark-bg)
  );
  border: 1px solid var(--mid-bg);
  border-radius: 0.25rem;
  cursor: help;
  transition: transform 0.2s;
}

.heat-cell:hover,
.heat-cell:focus {
  transform: scale(1.2);
  z-index: 1;
  outline: 2px solid var(--primary-cyan);
}
```

### Donut Charts (Coalition Breakdown, Vote Distribution)
```css
/* CSS-only donut chart using conic-gradient */
<div class="donut-chart" style="
  --s: 107;
  --m: 68;
  --sd: 73;
  --total: 349;
  --s-pct: calc(var(--s) / var(--total) * 100);
  --m-pct: calc(var(--m) / var(--total) * 100);
  --sd-pct: calc(var(--sd) / var(--total) * 100);
" role="img" aria-label="Coalition distribution: S 107, M 68, SD 73 of 349 MPs">
  <div class="donut-hole">
    <span class="donut-total">349</span>
    <span class="donut-label">MPs</span>
  </div>
</div>

/* CSS */
.donut-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    var(--party-s) 0% var(--s-pct),
    var(--party-m) var(--s-pct) calc(var(--s-pct) + var(--m-pct)),
    var(--party-sd) calc(var(--s-pct) + var(--m-pct)) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.donut-hole {
  width: 60%;
  height: 60%;
  border-radius: 50%;
  background: var(--dark-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.donut-total {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-cyan);
}

.donut-label {
  font-size: 0.875rem;
  color: var(--light-text);
}
```

### Timeline Visualizations (Legislative Process, MP Career)
```css
/* Vertical timeline */
<ol class="timeline">
  <li class="timeline-item">
    <time datetime="2024-09-15">2024-09-15</time>
    <div class="timeline-content">
      <h3>Motion Submitted</h3>
      <p>MP submitted motion to committee</p>
    </div>
  </li>
  <li class="timeline-item">
    <time datetime="2024-10-20">2024-10-20</time>
    <div class="timeline-content">
      <h3>Committee Review</h3>
      <p>Committee issued report</p>
    </div>
  </li>
</ol>

/* CSS */
.timeline {
  list-style: none;
  padding: 0;
  margin: 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 2rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--primary-cyan);
}

.timeline-item {
  position: relative;
  padding-left: 5rem;
  padding-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 1.5rem;
  top: 0.25rem;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background: var(--primary-magenta);
  border: 3px solid var(--dark-bg);
  box-shadow: 0 0 0 3px var(--primary-cyan);
}

.timeline-item time {
  position: absolute;
  left: 0;
  top: 0;
  font-size: 0.875rem;
  color: var(--primary-cyan);
}
```

## Party Color Palette

```css
:root {
  /* Swedish political parties (official colors) */
  --party-s: #E8112d;    /* Socialdemokraterna (Red) */
  --party-m: #52BDEC;    /* Moderaterna (Blue) */
  --party-sd: #DDDD00;   /* Sverigedemokraterna (Yellow) */
  --party-c: #009933;    /* Centerpartiet (Green) */
  --party-v: #DA291C;    /* Vänsterpartiet (Red) */
  --party-kd: #000077;   /* Kristdemokraterna (Dark Blue) */
  --party-l: #006AB3;    /* Liberalerna (Blue) */
  --party-mp: #83CF39;   /* Miljöpartiet (Green) */
}
```

## Accessibility Requirements

### Screen Reader Support
```html
<!-- Always include sr-only labels for data -->
<div class="progress-bar" style="--value: 87%">
  <span class="sr-only">87% party cohesion</span>
</div>

<!-- Data tables for complex visualizations -->
<table class="data-table" role="table">
  <caption>MPs by Party Distribution</caption>
  <thead>
    <tr>
      <th scope="col">Party</th>
      <th scope="col">MPs</th>
      <th scope="col">Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Socialdemokraterna (S)</th>
      <td>107</td>
      <td>30.7%</td>
    </tr>
  </tbody>
</table>

<!-- Hide visual chart from screen readers, show data table -->
<div aria-hidden="true" class="visual-chart">...</div>
```

### Color Contrast
```css
/* Ensure 4.5:1 contrast ratio minimum */
.bar-label {
  color: var(--light-text); /* #e0e0e0 on #0a0e27 = 12.6:1 ✅ */
}

/* Use patterns for color-blind accessibility */
.bar-striped {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgba(255,255,255,0.1) 10px,
    rgba(255,255,255,0.1) 20px
  );
}
```

### Keyboard Navigation
```css
/* Make interactive elements focusable */
.heat-cell {
  cursor: pointer;
  position: relative;
}

.heat-cell:focus {
  outline: 2px solid var(--primary-cyan);
  outline-offset: 2px;
  z-index: 1;
}

/* Tooltip on focus/hover */
.heat-cell::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--dark-bg);
  color: var(--light-text);
  padding: 0.5rem;
  border-radius: 0.25rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

.heat-cell:hover::after,
.heat-cell:focus::after {
  opacity: 1;
}
```

## When to Use

- **Dashboard Design**: Political metrics overview
- **Party Analysis**: MP distribution, voting patterns, coalition strength
- **Voting Records**: Vote outcomes, party discipline, cross-party votes
- **Committee Activity**: Productivity metrics, attendance rates
- **MP Profiles**: Career timeline, voting record, committee assignments
- **Electoral Analysis**: Historical results, trends, forecasts
- **Risk Assessment**: 45 risk rules visualization, severity indicators
- **Transparency Metrics**: Democratic accountability scores

## Examples

### Good Pattern: Responsive Voting Discipline Dashboard
```html
<section class="voting-dashboard">
  <h2>Voting Discipline by Party (2024/25)</h2>
  
  <div class="party-grid">
    <div class="party-card">
      <h3>Socialdemokraterna (S)</h3>
      <div class="progress" role="progressbar" aria-valuenow="89" aria-valuemin="0" aria-valuemax="100">
        <span class="progress-label">89% Cohesion</span>
        <div class="progress-bar" style="--value: 89%; --color: var(--party-s)"></div>
      </div>
      <p class="stat">92 unanimous votes, 8 rebels</p>
    </div>
    
    <!-- Repeat for other parties -->
  </div>
</section>

<style>
.party-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.party-card {
  background: var(--mid-bg);
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid var(--primary-cyan);
}
</style>
```

### Anti-Pattern: JavaScript-Dependent Charts
```html
<!-- ❌ BAD: Requires JavaScript library -->
<script src="https://cdn.example.com/charts.js"></script>
<canvas id="chart"></canvas>
<script>
  new Chart(document.getElementById('chart'), {...});
</script>

<!-- ✅ GOOD: Pure CSS visualization -->
<div class="bar-chart" role="img" aria-label="MPs by party">
  <!-- CSS-only bars -->
</div>
```

### Anti-Pattern: Inaccessible Visualizations
```html
<!-- ❌ BAD: No screen reader support -->
<div class="donut" style="background: conic-gradient(...)"></div>

<!-- ✅ GOOD: Full accessibility -->
<div class="donut" role="img" aria-label="Coalition: S 107, M 68, SD 73 MPs">
  <!-- Visual chart -->
</div>
<table class="sr-only">
  <caption>Coalition Distribution</caption>
  <!-- Data table for screen readers -->
</table>
```

## Remember

- **CSS-only** - no JavaScript libraries
- **Accessibility mandatory** - WCAG 2.1 AA, screen reader support
- **Semantic HTML** - use `<table>` for data, proper ARIA roles
- **Responsive** - adapt to mobile/tablet/desktop
- **Color-blind safe** - use patterns, labels, icons beyond color
- **Performance** - minimal CSS, fast rendering
- **Party colors** - use official colors for Swedish parties
- **Progressive disclosure** - summary view, details on interaction
- **Data tables** - always provide for screen readers
- **Tooltip support** - title attribute + CSS hover/focus

## References

- [CSS-Tricks: Chart.css](https://chartscss.org/)
- [A11Y: Accessible Data Visualizations](https://www.a11yproject.com/posts/accessible-data-visualizations/)
- [MDN: conic-gradient()](https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/conic-gradient)
- [Web.dev: Building an accessible progress bar](https://web.dev/building-a-progress-bar-component/)
- [WCAG 2.1: Level AA](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_customize&levels=aa)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Maintained by**: Hack23 AB
