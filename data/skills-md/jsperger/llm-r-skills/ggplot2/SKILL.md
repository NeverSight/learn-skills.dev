---
name: ggplot2
description: Use when working with R ggplot2 package, especially ggplot2 4.0+ features. Covers S7 migration (@ property access), theme defaults with ink/paper/accent, element_geom(), from_theme(), theme shortcuts (theme_sub_*), palette themes, labels with dictionary/attributes, discrete scale improvements (palette, continuous.limits, minor_breaks, sec.axis), position aesthetics (nudge_x/nudge_y, order), facet_wrap dir/space/layout, boxplot/violin/label styling, stat_manual(), stat_connect(), coord reversal.
---

# ggplot2 Reference

ggplot2 is an R package for producing visualizations using a grammar of graphics. You compose plots from data, mappings, layers, scales, facets, coordinates, and themes.

## Core Components

### Data and Mapping

```r
ggplot(data = mpg, mapping = aes(x = cty, y = hwy))
```

- **Data**: Tidy data frame (rows = observations, columns = variables)
- **Mapping**: `aes()` links data columns to visual properties (x, y, colour, size, etc.)

### Layers

Layers display data using geometry, statistical transformation, and position adjustment:

```r
ggplot(mpg, aes(cty, hwy)) +
  geom_point() +
  geom_smooth(formula = y ~ x, method = "lm")
```

### Scales

Control how data maps to visual properties and create legends/axes:

```r
ggplot(mpg, aes(cty, hwy, colour = class)) +
  geom_point() +
  scale_colour_viridis_d()
```

### Facets

Split data into panels by variables:

```r
ggplot(mpg, aes(cty, hwy)) +
  geom_point() +
  facet_grid(year ~ drv)
```

### Coordinates

Interpret position aesthetics (Cartesian, polar, map projections):

```r
ggplot(mpg, aes(cty, hwy)) +
  geom_point() +
  coord_fixed()
```

### Theme

Control non-data visual elements:

```r
ggplot(mpg, aes(cty, hwy, colour = class)) +
  geom_point() +
  theme_minimal() +
  theme(legend.position = "top")
```

---

# ggplot2 4.0 Features

ggplot2 4.0.0 (September 2025) introduced S7 classes and major new features.

## S7 Migration

Access properties with `@` instead of `$`:

```r
# ggplot2 4.0+
ggplot()@data

# Deprecated (still works temporarily)
ggplot()$data
```

Stricter type validation:

```r
element_text(hjust = "foo")
#> Error: @hjust must be <NULL>, <integer>, or <double>, not <character>
```

## Theme-Based Layer Defaults

### Ink, Paper, and Accent

Built-in themes accept `ink` (foreground), `paper` (background), `accent` (highlight):

```r
ggplot(mpg, aes(displ, hwy)) +
  geom_point() +
  geom_smooth(method = "lm", formula = y ~ x) +
  theme_gray(paper = "cornsilk", ink = "navy", accent = "tomato")
```

### element_geom() and from_theme()

Set layer defaults via `theme(geom)`:

```r
ggplot(mpg, aes(class, displ)) +
  geom_boxplot(aes(colour = from_theme(accent))) +
  theme(geom = element_geom(
    accent = "tomato",
    paper = "cornsilk",
    bordertype = "dashed",
    borderwidth = 0.2,
    linewidth = 2,
    linetype = "solid"
  ))
```

### Theme Palettes

Set default palettes in themes:

```r
theme(
  palette.colour.continuous = c("chartreuse", "forestgreen"),
  palette.shape.discrete = c("triangle", "triangle open")
)
```

## Theme Shortcuts

New `theme_sub_*()` functions reduce verbosity:

| Shortcut | Prefix replaced |
|----------|-----------------|
| `theme_sub_axis()` | `axis.*` |
| `theme_sub_axis_x()` | `axis.*.x` |
| `theme_sub_axis_bottom()` | `axis.*.x.bottom` |
| `theme_sub_legend()` | `legend.*` |
| `theme_sub_panel()` | `panel.*` |
| `theme_sub_plot()` | `plot.*` |
| `theme_sub_strip()` | `strip.*` |

```r
# Concise
theme_sub_axis_x(
  ticks = element_line(colour = "red"),
  ticks.length = unit(5, "mm")
) +
theme_sub_panel(
  widths = unit(5, "cm"),
  spacing.x = unit(5, "mm")
)
```

### Margin Helpers

```r
margin_auto(1)           # all sides = 1
margin_auto(1, 2)        # t/b=1, l/r=2
margin_auto(1, 2, 3)     # t=1, l/r=2, b=3
margin_part(r = 20)      # partial (NA inherits)
```

### Panel Sizes

```r
theme_sub_panel(widths = unit(c(2, 3, 4), "cm"))  # per-panel
theme_sub_panel(widths = unit(9, "cm"))           # total area
```

## Labels

### Label Attributes

Variables with `"label"` attribute auto-populate axis labels:

```r
attr(df$bill_dep, "label") <- "Bill depth (mm)"
ggplot(df, aes(bill_dep, bill_len)) + geom_point()
```

### Dictionary Labels

```r
dict <- c(species = "Species", bill_dep = "Bill depth (mm)")
ggplot(penguins, aes(bill_dep, bill_len, colour = species)) +
  geom_point() +
  labs(dictionary = dict)
```

### Function Labels

```r
scale_colour_discrete(name = toupper)
guides(x = guide_axis(title = tools::toTitleCase))
labs(y = \(x) paste0(x, " variable"))
```

Label hierarchy (lowest to highest): `aes()` < `labs(dictionary)` < column attribute < `labs()` < `scale_*(name)` < `guide_*(title)`

### Named Breaks

```r
scale_colour_discrete(breaks = c(
  "Pygoscelis adeliae" = "Adelie",
  "Pygoscelis papua" = "Gentoo"
))
```

## Discrete Scale Improvements

```r
# Palette for spacing
scale_x_discrete(palette = scales::pal_manual(c(1:3, 5:7)))

# Consistent limits across facets
scale_x_discrete(continuous.limits = c(1, 5))

# Minor breaks
scale_x_discrete(
  minor_breaks = scales::breaks_width(1, offset = 0.5),
  guide = guide_axis(minor.ticks = TRUE)
)

# Secondary axis
scale_x_discrete(sec.axis = dup_axis(
  name = "Counts",
  breaks = seq_len(7),
  labels = paste0("n = ", table(mpg$class))
))
```

## Position Aesthetics

### Nudge Aesthetics

```r
geom_text(aes(nudge_x = sign(value) * 3, label = value))
```

### Dodge Order

```r
ggplot(data, aes(x, y, fill = group)) +
  geom_boxplot(position = position_dodge(preserve = "single")) +
  aes(order = group)
```

## Facets

### Wrapping Directions

8 direction options for `facet_wrap(dir)`:

| dir | Start | Fill |
|-----|-------|------|
| `"lt"` | top-left | left-to-right |
| `"tl"` | top-left | top-to-bottom |
| `"lb"` | bottom-left | left-to-right |
| `"bl"` | bottom-left | bottom-to-top |
| `"rt"` | top-right | right-to-left |
| `"tr"` | top-right | top-to-bottom |
| `"rb"` | bottom-right | right-to-left |
| `"br"` | bottom-right | bottom-to-top |

### Free Space

```r
facet_wrap(~ island, scales = "free_x", space = "free_x")
```

### Layer Layout

```r
geom_point(colour = "grey", layout = "fixed_rows")  # repeat in rows
geom_point(layout = NULL)                            # use facet vars
annotate("text", label = "X", layout = 6)            # specific panel
```

Options: `NULL`, `"fixed"`, `<integer>`, `"fixed_cols"`, `"fixed_rows"`

## Styling

### Boxplot Parts

```r
geom_boxplot(
  whisker.linetype = "dashed",
  box.colour = "black",
  median.linewidth = 2,
  staplewidth = 0.5,
  staple.colour = "grey50"
)
```

### Violin Quantiles

```r
geom_violin(
  quantiles = c(0.1, 0.9),
  quantile.linetype = 1,
  quantile.colour = "red"
)
```

### Labels

```r
geom_label(
  aes(linetype = factor(vs), linewidth = factor(am)),
  text.colour = "black",
  border.colour = "blue"
)
```

### Varying Fill

```r
geom_area(aes(fill = continuous_var))  # gradient (R 4.1+)
```

## New Stats

### stat_manual()

```r
make_centroids <- function(df) {
  transform(df, xend = mean(x), yend = mean(y))
}
stat_manual(geom = "segment", fun = make_centroids)
```

### stat_connect()

```r
geom_line(stat = "connect")           # stairstep
geom_ribbon(stat = "connect", alpha = 0.4)

# Custom connection shape
smooth <- cbind(x = seq(0, 1, length.out = 20)[-1],
                y = scales::rescale(plogis(x, 0.5, 0.1)))
stat_connect(connection = smooth)
```

## Coord Reversal

```r
coord_cartesian(reverse = "x")   # "y", "xy", "none"
coord_sf(reverse = "y")
coord_radial(reverse = "theta")  # "r", "thetar", "none"
```

## Deprecations

| Old | New |
|-----|-----|
| `fatten` | `median.linewidth` / `middle.linewidth` |
| `draw_quantiles` | `quantiles` |
| `geom_errorbarh()` | `geom_errorbar(orientation = "y")` |
| `coord_trans()` | `coord_transform()` |
| `borders()` | `annotation_borders()` |
| `facet_wrap(as.table)` | `facet_wrap(dir)` |
| `theme_get/set/update/replace()` | `get/set/update/replace_theme()` |
| `last_plot()` | `get_last_plot()` |
| `layer_data/grob/scales()` | `get_layer_data/grob()`, `get_panel_scales()` |
