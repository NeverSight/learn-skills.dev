---
name: remotion-data-viz
description: Data visualization and infographics for Remotion. Use for animated charts, counters, progress bars, SVG paths, recharts, and D3 integrations.
---

# Remotion Data Viz

Animated data visualizations as Remotion compositions — frame-deterministic, React-based, seekable.

For the composition contract see `remotion-core`. For animation primitives see `remotion-animation`.

## Core principle

Data visualizations in Remotion are **animated from frame 0 to durationInFrames**. All chart values are derived from `useCurrentFrame()` — there is no re-render on resize or data change, only a deterministic mapping of frame → visual state.

## Common patterns

### Animated counter

```tsx
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

type CounterProps = {
  from: number;
  to: number;
  durationInFrames: number;
  prefix?: string;
  suffix?: string;
};

const AnimatedCounter: React.FC<CounterProps> = ({from, to, durationInFrames, prefix = '', suffix = ''}) => {
  const frame = useCurrentFrame();
  const value = interpolate(frame, [0, durationInFrames], [from, to], {
    extrapolateRight: 'clamp',
    easing: (t) => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t, // ease-in-out-quad
  });

  return (
    <div style={{fontSize: 120, fontWeight: 700, color: '#fff', fontVariantNumeric: 'tabular-nums'}}>
      {prefix}{Math.round(value).toLocaleString()}{suffix}
    </div>
  );
};
```

### Bar chart reveal

```tsx
import {interpolate, useCurrentFrame} from 'remotion';

type BarProps = {label: string; value: number; maxValue: number; index: number; color: string};

const AnimatedBar: React.FC<BarProps> = ({label, value, maxValue, index, color}) => {
  const frame = useCurrentFrame();
  const STAGGER = 5;
  const DURATION = 40;

  const progress = interpolate(
    frame,
    [index * STAGGER, index * STAGGER + DURATION],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const barWidth = (value / maxValue) * 600 * progress;

  return (
    <div style={{marginBottom: 20}}>
      <div style={{color: '#ccc', fontSize: 24, marginBottom: 8}}>{label}</div>
      <div style={{height: 48, backgroundColor: '#1e1e2e', borderRadius: 8, overflow: 'hidden'}}>
        <div
          style={{
            height: '100%',
            width: barWidth,
            backgroundColor: color,
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            paddingLeft: 16,
          }}
        >
          <span style={{color: 'white', fontWeight: 700}}>{Math.round(value * progress).toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};
```

### Line chart draw (SVG)

```tsx
import {interpolate, useCurrentFrame} from 'remotion';

const LineChart: React.FC<{data: number[]; width: number; height: number}> = ({data, width, height}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames * 0.8], [0, 1], {extrapolateRight: 'clamp'});

  const maxVal = Math.max(...data);
  const points = data
    .slice(0, Math.ceil(data.length * progress))
    .map((v, i) => `${(i / (data.length - 1)) * width},${height - (v / maxVal) * height}`)
    .join(' ');

  return (
    <svg width={width} height={height}>
      <polyline
        points={points}
        fill="none"
        stroke="#6366f1"
        strokeWidth={4}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};
```

### Pie / donut reveal

```tsx
const DonutChart: React.FC<{segments: {value: number; color: string}[]; size: number}> = ({segments, size}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames * 0.7], [0, 1], {extrapolateRight: 'clamp'});
  const radius = size / 2 - 20;
  const cx = size / 2;
  const cy = size / 2;
  const total = segments.reduce((s, seg) => s + seg.value, 0);

  let cumulative = 0;
  const paths = segments.map((seg, i) => {
    const startAngle = (cumulative / total) * 2 * Math.PI - Math.PI / 2;
    cumulative += seg.value;
    const endAngle = (cumulative / total) * 2 * Math.PI * progress - Math.PI / 2;

    const x1 = cx + radius * Math.cos(startAngle);
    const y1 = cy + radius * Math.sin(startAngle);
    const x2 = cx + radius * Math.cos(endAngle);
    const y2 = cy + radius * Math.sin(endAngle);
    const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;

    return (
      <path
        key={i}
        d={`M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} Z`}
        fill={seg.color}
      />
    );
  });

  return <svg width={size} height={size}>{paths}</svg>;
};
```

## Using recharts

```bash
npm install recharts
```

> **Important:** recharts uses `requestAnimationFrame` and DOM measurements internally. Use `spring()` and `interpolate()` to compute chart data values before passing to recharts — do not rely on recharts' internal animation (it's not frame-deterministic).

```tsx
import {BarChart, Bar, XAxis, YAxis} from 'recharts';

const MyChart: React.FC = () => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, 60], [0, 1], {extrapolateRight: 'clamp'});

  const data = [
    {name: 'A', value: Math.round(1200 * progress)},
    {name: 'B', value: Math.round(800 * progress)},
    {name: 'C', value: Math.round(1600 * progress)},
  ];

  return (
    <BarChart width={600} height={400} data={data}>
      <XAxis dataKey="name" />
      <YAxis />
      <Bar dataKey="value" fill="#6366f1" isAnimationActive={false} />
    </BarChart>
  );
};
```

Always set `isAnimationActive={false}` on recharts components — their internal animation is not frame-deterministic.

## calculateMetadata for data-driven compositions

When the composition duration depends on the data length, use `calculateMetadata`:

```tsx
import {Composition} from 'remotion';

type DataVizProps = {data: {label: string; value: number}[]};

const dataViz = {
  component: DataVizScene,
  calculateMetadata: async ({props}: {props: DataVizProps}) => {
    const fps = 30;
    const framesPerBar = 20;
    const durationInFrames = props.data.length * framesPerBar + 60; // padding
    return {durationInFrames, fps};
  },
};
```

## References

| Task | Read |
| --- | --- |
| Animated counter, bar chart, line chart, pie patterns | `references/chart-patterns.md` |
| recharts integration (isAnimationActive, data binding) | `references/recharts.md` |
| D3 calculations (scale, path) with React rendering | `references/d3-in-remotion.md` |
| calculateMetadata for dynamic duration | `remotion-core/references/calculate-metadata.md` |
| spring/interpolate for data reveals | `remotion-keyframes` |
