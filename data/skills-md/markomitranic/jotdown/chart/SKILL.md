---
name: chart
description: Use only when working on the docs site. Put a chart of real numbers on a docs page with the `<Chart />` block, a bar, line, area, pie or radar chart in the brand's palette. Use whenever a page compares, ranks, breaks down or tracks numbers, or when a paragraph carries three sentences of figures.
---
# Chart

A number the reader should compare belongs in a chart, not a sentence. A page
draws one with `<Chart />`, a block the framework provides: shadcn's chart
component on Recharts, painted with the brand's `--chart-1` to `--chart-5`, with
a tooltip on hover and a legend when there is more than one series.

```mdx
<Chart
  type="bar"
  x="month"
  data={[
    { month: "Apr", saves: 186, builds: 80 },
    { month: "May", saves: 305, builds: 200 }
  ]}
  series={{ saves: "Studio saves", builds: "Publication builds" }}
  caption="Studio saves and publication builds per month, from the studio's commit log."
/>
```

## Pick the type from the question

| The reader asks | Type | Props |
| --- | --- | --- |
| how do these compare? which is biggest? | `bar` | `horizontal` when the labels are long or there are more than eight |
| how did it change over time? | `line` | one to three series |
| how did the total and its parts change over time? | `area` | `stacked` |
| what are the parts of this total? | `bar`, `stacked` | a pie only for two to four parts of one whole |
| how do two or three things score on the same criteria? | `radar` | three to eight criteria |

Before and after is a `bar` with two series, before and after. A ranking is a
`bar` with the rows sorted, biggest first. If none of these is the question,
it is not this block: a waterfall, a sankey, a slopegraph or a chart that needs
annotation on a mark is drawn by the `figure` skill.

## Write the data

- **`x`** names the field that labels each row: the month, the page, the host.
- **`data`** is an array of rows, one object per label. Numbers are numbers,
  never strings, and every row carries every series.
- **`series`** maps each field to plot to its label, in the order the colours
  go: the first is `--chart-1`. Put the series the page is about first. Five at
  most; past that the colours stop being told apart.
- **`unit`** is appended to the value axis, `unit="ms"`. Use it whenever the
  numbers have one.
- **`caption`** says what the chart shows and where the numbers came from.
- Props are literal values, as everywhere on a page. Nothing is computed, so
  sort, round and total the numbers before they go in.

A pie plots its one series and colours each row. Every other type colours each
series.

## Keep it honest

- Real numbers only. A chart of made-up data is a figure pretending to be
  evidence; if the numbers are illustrative, say so in the caption.
- Round to what the reader needs. 212 ms, not 211.73 ms.
- One chart, one point. If the caption needs "and", it is two charts.
- The prose beside it says the takeaway in words: "May had twice the saves of
  July." The chart is the proof, not the only place the point is made.

## Check it

A chart renders in the browser, so the figure render script does not draw it.
Open the page in the studio or the local preview, in both colour modes, and
hover a mark to see the tooltip. A prop that is not a literal fails the page
when it compiles, and the page says why where it stands.
