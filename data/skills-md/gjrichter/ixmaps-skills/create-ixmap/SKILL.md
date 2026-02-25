---
name: create-ixmap
description: Creates interactive maps using ixMaps framework. Use when the user wants to create a map, visualize geographic data, or display data with bubble charts, choropleth maps, pie charts, or bar charts on a map.
argument-hint: "[filename] [options]"
allowed-tools: Write, Read, AskUserQuestion
---

# Create ixMap Skill

This skill helps you create interactive maps using the ixMaps framework quickly and easily.

Creates a complete HTML file with an interactive ixMaps visualization. You can specify the map type, data, and visualization style through simple parameters.

## Usage

```
/create-ixmap [options]
```

## Parameters

The skill accepts parameters in natural language. You can specify:

- **filename**: Output HTML filename (default: "map.html")
- **title**: Map title
- **data**: Data as JSON array or URL to data file
- **maptype**: Base map style (VT_TONER_LITE, OpenStreetMap, CartoDB - Positron, etc.)
- **center**: Map center coordinates {lat, lng}
- **zoom**: Initial zoom level
- **viztype**: Visualization type (BUBBLE, CHOROPLETH, PIE, BAR, DOT)
- **colorscheme**: Color array for visualization

## Examples

```bash
# Create a simple bubble map of Italian cities
/create-ixmap filename=citta_italia.html title="Città Italiane"

# Create a choropleth map
/create-ixmap viztype=CHOROPLETH data=regions.csv center={lat:42,lng:12} zoom=6

# Create with custom colors
/create-ixmap colorscheme=["#ff0000","#00ff00"] maptype=OpenStreetMap
```

## Instructions for Claude

When this skill is invoked, you should:

1. **Parse the parameters** from the user's request (either from command arguments or from conversational context)

2. **Gather required information** by asking the user if needed:
   - What data should be displayed? (cities, regions, points of interest)
   - What should the visualization show? (population, values, categories)
   - Any specific styling preferences?

3. **Generate the HTML file** with:
   - Complete HTML5 structure
   - ixMaps CDN script included
   - Responsive styling
   - Data embedded inline or loaded from URL
   - Proper ixMaps configuration using fluent API
   - Appropriate visualization type and styling

4. **Use the template structure**:
```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>[TITLE]</title>
    <script src="https://cdn.jsdelivr.net/gh/gjrichter/ixmaps-flat@master/ixmaps.js"></script>
    <style>
        body { margin: 0; padding: 0; }
        #map { width: 100%; height: 100vh; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Data
        const data = [DATA];

        // Create map
        ixmaps.Map("map", {
            mapType: "[MAPTYPE]",  // e.g., "white", "VT_TONER_LITE", "CartoDB - Positron"
            mode: "info"           // Enable tooltips on mouseover (optional)
        })
        .options({
            objectscaling: "dynamic",
            normalSizeScale: "1000000",
            basemapopacity: 0.6,
            flushChartDraw: 1000000
        })
        .view({
            center: { lat: [LAT], lng: [LNG] },
            zoom: [ZOOM]
        })
        .legend("[LEGEND_TITLE]")  // Optional: custom legend title
        .layer(
            ixmaps.layer("data_layer")
                .data({ obj: data, type: "json" })
                .binding({ geo: "lat|lon", value: "[VALUE_FIELD]", title: "[TITLE_FIELD]" })
                .style({
                    colorscheme: [COLORS],
                    scale: 1,
                    opacity: 0.7,
                    showdata: "true"
                })
                .meta({
                    tooltip: "{{theme.item.chart}}{{theme.item.data}}"
                })
                .type("[VIZ_TYPE]")
                .title("[LAYER_TITLE]")
                .define()
        );
    </script>
</body>
</html>
```

**IMPORTANT - Data Source Specific Rules:**

**For GeoJSON data sources:**
- Type MUST be `FEATURE` or `FEATURE|CHOROPLETH` (for colored regions)
- For simple features: use `value: "$item$"` in binding
- For categorical coloring by text field: use `value: "fieldname"` and add `|CATEGORICAL` to type
- Property field names are referenced directly (e.g., `title: "NAME_ENGL"`), NOT with "properties." prefix
- Style MUST include: `showdata: "true"`
- Meta MUST include: `{ tooltip: "{{theme.item.chart}}{{theme.item.data}}" }`
- Example for simple GeoJSON:
```javascript
.data({ url: "path/to/data.geojson", type: "geojson" })
.binding({ geo: "geometry", value: "$item$", title: "name" })
.style({ colorscheme: ["#0066cc"], showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("FEATURE")
```
- Example for categorical coloring:
```javascript
.data({ url: "path/to/data.geojson", type: "geojson" })
.binding({ geo: "geometry", value: "category_field", title: "name" })
.style({ colorscheme: ["100", "tableau"], showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("FEATURE|CHOROPLETH|CATEGORICAL")
```

**For TopoJSON data sources:**
- Same rules as GeoJSON apply
- Type can be `type: "topojson"` in the data configuration
- For simple features: use `value: "$item$"` in binding
- For categorical coloring by text field: use `value: "fieldname"` and add `|CATEGORICAL` to type
- Property field names are referenced directly (e.g., `title: "NAME_ENGL"`), NOT with "properties." prefix
- Example for simple TopoJSON:
```javascript
.data({ url: "path/to/data.json", type: "topojson" })
.binding({ geo: "geometry", value: "$item$", title: "NAME_ENGL" })
.style({ colorscheme: ["#0066cc"], showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("FEATURE")
```
- Example for categorical coloring:
```javascript
.data({ url: "path/to/data.json", type: "topojson" })
.binding({ geo: "geometry", value: "NAME_ENGL", title: "NAME_ENGL" })
.style({ colorscheme: ["100", "tableau"], showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("FEATURE|CHOROPLETH|CATEGORICAL")
```

**For point data (CSV/JSON with lat/lon):**
- Use standard chart types: `CHART|BUBBLE|SIZE|VALUES`, `CHART|PIE`, `CHART|DOT`, etc.
- For simple points without data values: `CHART|DOT` with static colorscheme
- For categorical coloring by text field: `CHART|DOT|CATEGORICAL` with dynamic colorscheme
- For aggregated data (with |AGGREGATE): Use `value: "$item$"` to count items
- Binding uses: `{ geo: "lat|lon", value: "fieldname", title: "titlefield" }` or just `{ geo: "coordinate_field", title: "titlefield" }` if coordinates are in single field
- Style MUST include: `showdata: "true"`
- Meta MUST include: `{ tooltip: "{{theme.item.chart}}{{theme.item.data}}" }`
- Example for simple points:
```javascript
.data({ obj: data, type: "json" })
.binding({ geo: "lat|lon", title: "name" })
.style({ colorscheme: ["#0066cc"], scale: 1, showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("CHART|DOT")
```
- Example for categorical points:
```javascript
.data({ url: "data.csv", type: "csv" })
.binding({ geo: "coordinate_geografiche", value: "category_field", title: "name" })
.style({ colorscheme: ["100", "tableau"], scale: 1, showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("CHART|DOT|CATEGORICAL")
```
- Example for sized bubbles:
```javascript
.data({ obj: data, type: "json" })
.binding({ geo: "lat|lon", value: "population", title: "name" })
.style({ colorscheme: ["#0066cc"], showdata: "true" })
.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })
.type("CHART|BUBBLE|SIZE|VALUES")
```

5. **Default values** if not specified:
   - filename: "ixmap.html"
   - maptype: "VT_TONER_LITE"
   - center: {lat: 42.5, lng: 12.5} (Italy)
   - zoom: 6
   - viztype: "CHART|BUBBLE|SIZE|VALUES"
   - colorscheme: ["#0066cc"]
   - flushChartDraw: 1000000 (instant rendering)

5b. **Valid mapType values** (IMPORTANT - use exact names):
   - `"VT_TONER_LITE"` - Clean, minimal base map (default)
   - `"white"` - Plain white background (no base map tiles)
   - `"OpenStreetMap"` - Standard OSM
   - `"CartoDB - Positron"` - Light CartoDB style (note the spaces and dash)
   - `"CartoDB - Dark_Matter"` - Dark CartoDB style (note the spaces and dash)
   - `"Stamen Terrain"` - Terrain with hill shading
   - **CRITICAL**: CartoDB map types require spaces around the dash: `"CartoDB - Positron"` NOT `"CartoDB Positron"`

5c. **Map Options Rules** (CRITICAL):
   - When using `objectscaling: "dynamic"`, you MUST also include `normalSizeScale` with a reasonable scale value
   - `normalSizeScale` value should be a string representing the scale (e.g., `"1000000"`, `"500000"`, `"2000000"`)
   - The scale value depends on your data range - adjust to make symbols appear at reasonable sizes
   - Example: `.options({ objectscaling: "dynamic", normalSizeScale: "1000000", basemapopacity: 0.6 })`
   - **Animation control**: `flushChartDraw: 1000000` disables animated rendering for instant display
     - Set to `1` for smooth animation (renders charts one by one)
     - Set to `100` for faster animation (renders charts in batches of 100)
     - Set to `1000000` to disable animation (renders all charts at once)
   - Example: `.options({ objectscaling: "dynamic", normalSizeScale: "1000000", basemapopacity: 0.6, flushChartDraw: 1000000 })`

5d. **Legend Configuration** (IMPORTANT):
   - Use `.legend()` method on the map object to set a custom legend title
   - The method takes a string directly: `.legend("Legend Title")`
   - Call it after `.view()` and before `.layer()`
   - Example: `.legend("Ambiti territoriali Lombardia")`
   - The legend will automatically show categorical values for CATEGORICAL themes

5e. **Mouse Mode Configuration** (IMPORTANT):
   - To enable tooltips on mouseover, set `mode: "info"` in the Map constructor options
   - Add it directly to the Map() options object, NOT in `.options()` method
   - Example:
   ```javascript
   ixmaps.Map("map", {
       mapType: "white",
       mode: "info"  // Enables tooltip display on hover
   })
   ```

6. **Data handling**:
   - If user provides inline data as JSON array, embed it directly
   - If user provides a CSV/JSON file URL, use `.data({url: "...", type: "..."})`
   - If user describes data (e.g., "Italian cities"), create sample data
   - Ensure data has required fields: lat, lon, and at least one value field

7. **Binding Rules** (CRITICAL):
   - **ALWAYS** include `.binding()` method for every layer
   - For GeoJSON/TopoJSON simple features: `{ geo: "geometry", value: "$item$", title: "fieldname" }`
   - For GeoJSON/TopoJSON categorical coloring: `{ geo: "geometry", value: "fieldname", title: "fieldname" }` (value points to the field to colorize by)
   - For point data with values: `{ geo: "lat|lon", value: "fieldname", title: "titlefield" }`
   - For point data without values (simple dots): `{ geo: "lat|lon", title: "titlefield" }` (no value needed)
   - For point data categorical coloring: `{ geo: "coordinate_field", value: "category_field", title: "titlefield" }`
   - **For aggregated data (with |AGGREGATE)**: Use `value: "$item$"` to count items, not a specific field
   - Geographic coordinates can be in separate fields (`geo: "lat|lon"`) or single field (`geo: "coordinate_geografiche"`)
   - Use `"$item$"` as value for:
     - GeoJSON/TopoJSON when displaying the geometry itself without data-based coloring
     - Point data with `|AGGREGATE` type when counting items (not summing a field)
   - Use a field name as value (e.g., `"NAME_ENGL"`, `"tipologia_infrastruttura"`) when you want to color by that field's categorical values
   - Property fields in GeoJSON/TopoJSON are referenced directly by name (e.g., `"NAME_ENGL"`), NOT `"properties.NAME_ENGL"`

7b. **Style Rules** (IMPORTANT):
   - **ALWAYS** include `showdata: "true"` in the `.style()` object
   - This enables data display on the map elements
   - Use `colorscheme` to define fill colors (array of color values)
   - `fillcolor` does NOT exist - colors are defined by `colorscheme`
   - For static colors: use array of hex colors, e.g., `["#0066cc"]` or `["#ffffcc", "#ff0000"]`
   - For categorical coloring: use dynamic colorscheme with `["count", "palette_name"]`, e.g., `["100", "tableau"]` - ixMaps calculates exact number needed
   - Available palette names: `"tableau"`, `"paired"`, `"set1"`, `"set2"`, `"set3"`, `"pastel1"`, `"dark2"`, etc.
   - For borders/lines, use `linecolor` and `linewidth` (NOT strokecolor/strokewidth)
   - For chart sizing:
     - `scale`: Scaling parameter where 1 = no scaling (e.g., `scale: 1.5` makes charts 50% larger)
     - `normalsizevalue`: The data value that corresponds to a 30 pixel chart size (e.g., `normalsizevalue: 1000` means value of 1000 = 30px)
     - **IMPORTANT**: Only use `normalsizevalue` when you know the expected maximum value. With `|AGGREGATE`, avoid using it since maximum counts are unknown
     - `symbolsize` does NOT exist - use `scale` or `normalsizevalue` instead
   - **Grid aggregation**: Use `gridwidth: "5px"` in style (NOT in type string)
   - Example static: `.style({ colorscheme: ["#0066cc"], linecolor: "#ffffff", linewidth: 1, showdata: "true" })`
   - Example categorical: `.style({ colorscheme: ["100", "tableau"], scale: 1, showdata: "true" })`
   - Example with sizing: `.style({ colorscheme: ["#0066cc"], normalsizevalue: 1000, showdata: "true" })`
   - Example with grid: `.style({ colorscheme: ["#ff0000"], gridwidth: "5px", scale: 1.5, showdata: "true" })`

7c. **Meta Rules** (IMPORTANT):
   - **ALWAYS** include `.meta()` method after `.style()` and before `.type()`
   - Default tooltip template: `{ tooltip: "{{theme.item.chart}}{{theme.item.data}}" }`
   - Only customize if the user explicitly requests different tooltip content
   - The tooltip template supports custom HTML with field placeholders using `{{FIELD_NAME}}` syntax
   - Custom tooltip examples:
     - Title only: `{ tooltip: "<h3>{{AMBITO}}</h3>" }`
     - Title + paragraph: `{ tooltip: "<h3>{{AMBITO}}</h3><p>{{LISTA_COMUNI}}</p>" }`
     - Multiple fields: `{ tooltip: "<strong>{{name}}</strong><br>Population: {{population}}" }`
   - To strip the chart from tooltip and show only data: `{ tooltip: "{{theme.item.data}}" }`
   - Field names reference GeoJSON properties directly (no "properties." prefix needed)

8. **Methods that DO NOT exist** (NEVER use):
   - `.tooltip()` - Does not exist in ixMaps API
   - To show information on hover, use the `title` property in `.binding()` instead

9. **Validation**:
   - Check that data has geographical coordinates (lat/lon or geometry)
   - Verify color scheme is valid array
   - Ensure visualization type matches data structure
   - VERIFY `.binding()` is always present with required properties

10. **After creation**:
   - Confirm the file was created
   - Explain what the map shows
   - Suggest how to open it (in browser)
   - Offer to modify or enhance the map

## Supported Visualization Types

### For Point Data (CSV/JSON with lat/lon coordinates):
- **CHART|DOT** - Simple dots at locations (uniform size and color)
- **CHART|DOT|CATEGORICAL** - Dots colored by categorical field values
- **CHART|BUBBLE|SIZE|VALUES** - Proportional circles sized by data values
- **CHART|PIE** - Pie charts at locations
- **CHART|BAR|VALUES** - Bar charts
- **NOTE**: All chart types MUST include the `CHART|` prefix

### For GeoJSON/TopoJSON Geometry Data:
- **FEATURE** - Simple geographic features (polygons, lines) with uniform or single color
- **FEATURE|CHOROPLETH** - Color-coded regions with numeric data values
  - Add `|EQUIDISTANT` for equal intervals: `FEATURE|CHOROPLETH|EQUIDISTANT`
  - Add `|QUANTILE` for quantiles: `FEATURE|CHOROPLETH|QUANTILE`
- **FEATURE|CHOROPLETH|CATEGORICAL** - Color-coded regions by categorical/text field values
  - Use with dynamic colorscheme: `["100", "tableau"]`
  - ixMaps automatically calculates the exact number of colors needed

## Aggregation

### Point Data Aggregation with Grid

ixMaps can aggregate point data into a grid for density visualization:

**Type**: Add `|AGGREGATE` to chart types
- `CHART|BUBBLE|SIZE|AGGREGATE` - Aggregate bubbles sized by count
- `CHART|DOT|AGGREGATE` - Aggregate dots
- `CHART|GRID|AGGREGATE` - Square grid cells

**Grid Size**: Define in `.style()` using `gridwidth`
- `gridwidth: "5px"` - 5 pixel grid cells
- `gridwidth: "10px"` - 10 pixel grid cells
- Grid size adapts to zoom level

**Value Binding**: Use `"$item$"` for counting
- `value: "$item$"` counts items in each grid cell
- Don't use specific field names when just counting
- Avoid `normalsizevalue` with aggregation (unknown max count)

**Example - Aggregate with 5px grid:**
```javascript
ixmaps.layer("incidents")
    .data({ obj: data, type: "json" })
    .binding({
        geo: "lat|lon",
        value: "$item$",  // Count items in each cell
        title: "location"
    })
    .style({
        colorscheme: ["#ffeb3b", "#ff9800", "#f44336"],
        gridwidth: "5px",  // 5px grid cells
        scale: 1.5,
        opacity: 0.7,
        showdata: "true"
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"
    })
    .type("CHART|BUBBLE|SIZE|AGGREGATE")
    .title("Aggregated Points")
    .define()
```

## Complete Examples

### Example 1: Point data with bubbles (CSV/JSON)
```javascript
ixmaps.layer("cities")
    .data({ obj: cityData, type: "json" })
    .binding({
        geo: "lat|lon",
        value: "population",
        title: "name"
    })
    .style({
        colorscheme: ["#0066cc"],
        showdata: "true"  // REQUIRED
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"  // REQUIRED
    })
    .type("CHART|BUBBLE|SIZE|VALUES")
    .title("Italian Cities by Population")
    .define()
```

### Example 2: GeoJSON with choropleth coloring
```javascript
ixmaps.layer("regions")
    .data({ url: "regions.geojson", type: "geojson" })
    .binding({
        geo: "geometry",
        value: "$item$",  // REQUIRED for GeoJSON
        title: "region_name"  // Property name directly, not properties.region_name
    })
    .style({
        colorscheme: ["#ffffcc","#ff0000"],
        opacity: 0.7,
        showdata: "true"  // REQUIRED
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"  // REQUIRED
    })
    .type("FEATURE|CHOROPLETH|EQUIDISTANT")
    .title("Regions")
    .define()
```

### Example 3: Simple GeoJSON features (no data values)
```javascript
ixmaps.layer("boundaries")
    .data({ url: "boundaries.geojson", type: "geojson" })
    .binding({
        geo: "geometry",
        value: "$item$",  // Still REQUIRED even without data
        title: "name"  // Property name directly
    })
    .style({
        colorscheme: ["#cccccc"],
        fillopacity: 0.3,
        linecolor: "#666666",
        linewidth: 1,
        showdata: "true"  // REQUIRED
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"  // REQUIRED
    })
    .type("FEATURE")
    .title("Administrative Boundaries")
    .define()
```

### Example 4: TopoJSON data (European countries - simple)
```javascript
ixmaps.layer("european_countries")
    .data({
        url: "https://s3.eu-central-1.amazonaws.com/maps.ixmaps.com/topojson/CNTR_RG_10M_2020_4326.json",
        type: "topojson"
    })
    .binding({
        geo: "geometry",
        value: "$item$",  // Simple feature display
        title: "NAME_ENGL"  // Property name directly, NOT properties.NAME_ENGL
    })
    .style({
        colorscheme: ["#6ba3d9"],
        fillopacity: 0.6,
        linecolor: "#ffffff",
        linewidth: 1.5,
        showdata: "true"
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"
    })
    .type("FEATURE")
    .title("European Countries (2020)")
    .define()
```

### Example 5: TopoJSON with categorical coloring
```javascript
ixmaps.layer("european_countries")
    .data({
        url: "https://s3.eu-central-1.amazonaws.com/maps.ixmaps.com/topojson/CNTR_RG_10M_2020_4326.json",
        type: "topojson"
    })
    .binding({
        geo: "geometry",
        value: "NAME_ENGL",  // Colorize by country name
        title: "NAME_ENGL"
    })
    .style({
        colorscheme: ["100", "tableau"],  // Dynamic colorscheme - ixMaps calculates exact count
        fillopacity: 0.7,
        linecolor: "#ffffff",
        linewidth: 1.5,
        showdata: "true"
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"
    })
    .type("FEATURE|CHOROPLETH|CATEGORICAL")
    .title("European Countries by Name")
    .define()
```

### Example 6: CSV point data with categorical coloring
```javascript
ixmaps.layer("edilizia_tipologia")
    .data({
        url: "https://data.s3.tebi.io/test%20only/infrastruttura-edilizia.csv",
        type: "csv"
    })
    .binding({
        geo: "coordinate_geografiche",  // Single field with coordinates
        value: "tipologia_infrastruttura",  // Colorize by infrastructure type
        title: "nome_infrastruttura"
    })
    .style({
        colorscheme: ["100", "tableau"],  // Dynamic colorscheme
        scale: 1.5,  // Scale factor for chart size
        opacity: 0.8,
        showdata: "true"
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"
    })
    .type("CHART|DOT|CATEGORICAL")  // Must include CHART| prefix
    .title("Infrastruttura per Tipologia")
    .define()
```

### Example 7: Complete map with white background, legend, and custom tooltip
```javascript
// Map with all modern features
ixmaps.Map("map", {
    mapType: "white",  // White background
    mode: "info"       // Enable tooltips on mouseover
})
.view({
    center: { lat: 45.65, lng: 9.5 },
    zoom: 8
})
.legend("Ambiti territoriali Lombardia")  // Custom legend title
.layer(
    ixmaps.layer("ambiti_territoriali")
        .data({
            url: "https://s3.fr-par.scw.cloud/ixmaps.data/test%20only/lombardia_ambiti_territoriali_confini_wgs84.geojson",
            type: "geojson"
        })
        .binding({
            geo: "geometry",
            value: "AMBITO",
            title: "AMBITO"
        })
        .style({
            colorscheme: ["100", "tableau"],
            fillopacity: 0.7,
            linecolor: "#ffffff",
            linewidth: 2,
            showdata: "true"
        })
        .meta({
            tooltip: "<h3>{{AMBITO}}</h3><p>{{LISTA_COMUNI}}</p>"  // Custom HTML tooltip
        })
        .type("FEATURE|CHOROPLETH|CATEGORICAL")
        .title("Ambiti territoriali Lombardia")
        .define()
);
```

### Example 8: Point data aggregation with grid (incident density)
```javascript
ixmaps.layer("incident_density")
    .data({
        url: "https://example.com/incidents.geojson",
        type: "geojson"
    })
    .binding({
        geo: "lat|lon",
        value: "$item$",  // Count incidents in each grid cell
        title: "via"
    })
    .style({
        colorscheme: ["#ffeb3b", "#ff9800", "#f44336", "#b71c1c"],
        gridwidth: "5px",  // 5 pixel grid aggregation
        scale: 1.5,
        opacity: 0.7,
        showdata: "true"
    })
    .meta({
        tooltip: "{{theme.item.chart}}{{theme.item.data}}"
    })
    .type("CHART|BUBBLE|SIZE|AGGREGATE")
    .title("Incident Density (5px grid)")
    .define()
```

**Map options with animation control:**
```javascript
ixmaps.Map("map", { mapType: "CartoDB - Positron" })
    .options({
        objectscaling: "dynamic",
        normalSizeScale: "1000000",
        basemapopacity: 0.7,
        flushChartDraw: 1000000  // Instant rendering (set to 1 for animation)
    })
```

## Notes

- The skill always creates a standalone HTML file that works without a server
- All dependencies are loaded from CDN
- Maps are fully interactive with zoom, pan, and hover information
- Data can be inline (for small datasets) or external URL (for large datasets)
- **CRITICAL**: Always use `.binding()` with appropriate `geo` and `value` properties
- **CRITICAL**: Always include `showdata: "true"` in `.style()`
- **CRITICAL**: Always include `.meta({ tooltip: "{{theme.item.chart}}{{theme.item.data}}" })`
- **CRITICAL**: For aggregation, use `value: "$item$"` and `gridwidth` in style, avoid `normalsizevalue`
- **NEVER** use `.tooltip()` - it doesn't exist in the ixMaps API

## Layer Method Chain Order

The correct order for layer methods is:
1. `.data()` - Define data source
2. `.binding()` - Map data fields to map properties
3. `.filter()` - Optional data filter
4. `.type()` - Visualization type
5. `.style()` - Visual styling (MUST include `showdata: "true"`)
6. `.meta()` - Metadata and tooltip configuration
7. `.title()` - Layer title
8. `.define()` - Finalize layer definition