---
name: preview-leaflet
description: Create interactive maps with markers, routes, and geographic data using Leaflet
user-invocable: true
commands:
  - preview-leaflet
---

# Preview Leaflet Skill

Interactive map visualization viewer using Leaflet library for geographic data, markers, routes, and custom overlays.

## Agent Usage

When the user asks to create a map visualization, write the Leaflet code and pipe it to the script. Use the Bash tool to execute this skill's `run.sh` script:

```bash
# Pipe Leaflet code
cat route.js | ./run.sh

# Or from a file
./run.sh city-map.leaflet
```

The script handles all HTML generation and **automatically opens the result in the browser**. Do NOT open the file manually to avoid duplicate tabs.

## Usage

```bash
# Preview a Leaflet map file
/preview-leaflet city-map.leaflet

# Or use .map extension
/preview-leaflet route.map

# Pipe Leaflet code (preferred for temporary content)
cat route.js | /preview-leaflet
echo "const map = L.map('map').setView([51.505, -0.09], 13);" | /preview-leaflet
```

**Best Practice:** For temporary or generated maps, prefer piping over creating temporary files. This avoids cluttering your filesystem and the content is automatically cleaned up.

## Options

The script works with sensible defaults but supports these flags for flexibility:

- `-o, --output PATH` - Custom output path
- `--no-browser` - Skip browser, output file path only

## Features

- **Interactive maps** with pan and zoom
- **Markers and popups** for locations
- **Routes and paths** with polylines
- **Shapes and areas** with polygons and circles
- **Multiple tile layers** (OpenStreetMap, CartoDB, etc.)
- **Tooltips** on hover
- **Fit bounds** to show all points
- **Reset view** button
- **Code viewer** toggle
- **Responsive design** adapts to window size

## When to Use This Skill

Use this skill when the user wants to:

- Visualize geographic data on maps
- Plot locations with markers
- Draw routes between points
- Show service areas or regions
- Create interactive location-based visualizations

## Leaflet Code Requirements

Your code should:

1. Initialize the map with `L.map('map').setView([lat, lng], zoom)`
2. Add a tile layer (provides map imagery)
3. Add markers, paths, or other features

## Execution Context

Your code runs with:

- **Leaflet v1.9.4** available as `L`
- **Map container** `#map` sized and ready in DOM

## Complete Example - Simple Map with Marker

```javascript
// Initialize map centered on London
const map = L.map('map').setView([51.505, -0.09], 13);

// Add OpenStreetMap tiles (REQUIRED - map is blank without this)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18,
}).addTo(map);

// Add a marker
L.marker([51.505, -0.09]).addTo(map).bindPopup('Hello World!').openPopup();
```

## Complete Example - Route with Multiple Points

```javascript
// Initialize map
const map = L.map('map').setView([40.7128, -74.006], 12);

// Add tiles (REQUIRED)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18,
}).addTo(map);

// Define route points
const route = [
  [40.7128, -74.006], // New York
  [40.758, -73.9855], // Times Square
  [40.7614, -73.9776], // Central Park
];

// Draw route
L.polyline(route, {
  color: 'red',
  weight: 3,
}).addTo(map);

// Add markers
route.forEach((point, i) => {
  L.marker(point)
    .addTo(map)
    .bindPopup(`Stop ${i + 1}`);
});

// Fit map to show all points
map.fitBounds(L.latLngBounds(route), { padding: [50, 50] });
```

## Common Patterns

### Markers

```javascript
// Simple marker
L.marker([51.5, -0.09]).addTo(map);

// With popup
L.marker([51.5, -0.09]).addTo(map).bindPopup('Location name');

// Circle marker (fixed pixel size)
L.circleMarker([51.5, -0.09], {
  radius: 8,
  fillColor: '#3498db',
  color: 'white',
  weight: 2,
  fillOpacity: 0.9,
}).addTo(map);
```

### Lines and Shapes

```javascript
// Polyline (route/path)
L.polyline(
  [
    [51.5, -0.09],
    [51.51, -0.08],
    [51.52, -0.07],
  ],
  {
    color: 'red',
    weight: 3,
  }
).addTo(map);

// Polygon (area)
L.polygon(
  [
    [51.5, -0.09],
    [51.51, -0.08],
    [51.52, -0.09],
  ],
  {
    color: 'blue',
    fillOpacity: 0.5,
  }
).addTo(map);

// Circle (fixed radius in meters)
L.circle([51.5, -0.09], {
  radius: 500, // meters
  color: 'red',
  fillOpacity: 0.5,
}).addTo(map);
```

### Popups and Tooltips

```javascript
// HTML in popup
marker.bindPopup(`
  <div>
    <h3>Location Name</h3>
    <p>Description here</p>
  </div>
`);

// Tooltip (shows on hover)
marker.bindTooltip('Tooltip text', {
  permanent: false,
  direction: 'top',
});

// Permanent tooltip (always visible)
marker.bindTooltip('Always visible', {
  permanent: true,
  direction: 'right',
});
```

### View Control

```javascript
// Set view (instant)
map.setView([51.5, -0.09], 13);

// Fly to (animated)
map.flyTo([51.5, -0.09], 13, {
  duration: 2, // seconds
});

// Fit bounds to show all features
const bounds = L.latLngBounds([
  [51.49, -0.1],
  [51.51, -0.08],
]);
map.fitBounds(bounds, {
  padding: [50, 50],
});
```

## Tile Layers (Map Styles)

### OpenStreetMap (free, default)

```javascript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18,
}).addTo(map);
```

### CartoDB Light (clean, minimal)

```javascript
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap, © CartoDB',
  maxZoom: 18,
}).addTo(map);
```

### CartoDB Dark

```javascript
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap, © CartoDB',
  maxZoom: 18,
}).addTo(map);
```

## Complete Example - Multiple Locations

```javascript
// Initialize map
const map = L.map('map').setView([37.7749, -122.4194], 10);

// Add tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
}).addTo(map);

// Locations data
const locations = [
  { name: 'San Francisco', coords: [37.7749, -122.4194], type: 'city' },
  { name: 'Oakland', coords: [37.8044, -122.2712], type: 'city' },
  { name: 'Berkeley', coords: [37.8715, -122.273], type: 'city' },
];

// Add markers
locations.forEach((loc) => {
  const color = loc.type === 'city' ? 'blue' : 'red';

  L.circleMarker(loc.coords, {
    radius: 8,
    fillColor: color,
    color: 'white',
    weight: 2,
    fillOpacity: 0.8,
  })
    .addTo(map)
    .bindPopup(`<strong>${loc.name}</strong><br/>Type: ${loc.type}`);
});

// Fit map to show all locations
const allCoords = locations.map((loc) => loc.coords);
map.fitBounds(L.latLngBounds(allCoords), { padding: [50, 50] });
```

## Coordinate Format

Leaflet uses `[latitude, longitude]` format:

- **Latitude**: -90 to 90 (South to North)
- **Longitude**: -180 to 180 (West to East)

**Examples:**

- New York: `[40.7128, -74.0060]`
- London: `[51.5074, -0.1278]`
- Tokyo: `[35.6762, 139.6503]`
- Sydney: `[-33.8688, 151.2093]`

**Common mistake:** Reversing coordinates to `[lng, lat]` - always use `[lat, lng]`!

## Built-in Features

- **Pan/zoom** - Click and drag to pan, scroll to zoom
- **Zoom buttons** - +/- controls in top-left
- **Reset view** - Button to restore initial view
- **Code viewer** - Toggle to show/hide source
- **Responsive** - Automatically resizes with window

## Zoom Levels

- **1**: World view
- **5**: Continent
- **10**: City
- **15**: Streets
- **18**: Buildings

## Best Practices

1. **Always add tile layer** - Map is blank without it
2. **Use appropriate zoom** - 1 (world) to 18 (street level)
3. **Use fitBounds() for multi-point maps** - Shows all features
4. **Embed data in code** - Include coordinates directly
5. **Verify coordinate order** - `[lat, lng]` not `[lng, lat]`

## Troubleshooting

### Map appears blank/gray

- Ensure tile layer is added with `.addTo(map)`
- Check coordinates are valid (`[lat, lng]` format)
- Verify internet connection (tiles load from CDN)
- Check browser console for 404 errors on tiles

### Markers don't appear

- Check coordinate format: `[latitude, longitude]`
- Ensure `.addTo(map)` is called on marker
- Verify coordinates are in current view
- Try using fitBounds() to see all markers

### Tiles don't load

- Check internet connection
- Verify tile URL is correct
- Look for 404 errors in browser console
- Try a different tile provider

### Wrong location shown

- Verify coordinates are correct
- Check coordinate order (lat first, lng second)
- Ensure zoom level is appropriate

## Technical Details

### File Requirements

- File extension: `.leaflet`
- Maximum size: 10MB (configurable)
- Valid JavaScript code
- Self-contained (no external data files)

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- Requires internet connection for tiles
- CDN-dependent: Leaflet v1.9.4

## Output

The skill generates a standalone HTML file at:

```
/tmp/preview-skills/preview-leaflet-{filename}.html
```

## Development

This skill is standalone and includes all dependencies:

- Shared libraries bundled in `lib/`
- Templates bundled in `templates/`
- External CDN dependencies: Leaflet v1.9.4

To modify the skill:

1. Edit `config.sh` for configuration
2. Edit `templates/scripts/leaflet-renderer.js` for behavior
3. Edit `templates/styles/leaflet.css` for styling
4. Run `run.sh` to test changes

## Learn More

- Leaflet Documentation: https://leafletjs.com/
- Leaflet Tutorials: https://leafletjs.com/examples.html
- Tile Providers: https://leaflet-extras.github.io/leaflet-providers/preview/
