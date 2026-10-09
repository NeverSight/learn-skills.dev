---
name: arcgis-imagery
description: Work with raster and imagery data using ImageryLayer, ImageryTileLayer, pixel filtering, raster functions, multidimensional data, and oriented imagery. Use for satellite imagery, elevation data, and scientific raster datasets.
---

# ArcGIS Imagery

Use this skill for raster imagery, pixel-level operations, raster functions, multidimensional data, and oriented imagery viewers.

## Import Patterns

### ESM (npm)

```javascript
import ImageryLayer from "@arcgis/core/layers/ImageryLayer.js";
import ImageryTileLayer from "@arcgis/core/layers/ImageryTileLayer.js";
import OrientedImageryLayer from "@arcgis/core/layers/OrientedImageryLayer.js";
import RasterFunction from "@arcgis/core/layers/support/RasterFunction.js";
import MosaicRule from "@arcgis/core/layers/support/MosaicRule.js";
import DimensionalDefinition from "@arcgis/core/layers/support/DimensionalDefinition.js";
import MultidimensionalSubset from "@arcgis/core/layers/support/MultidimensionalSubset.js";
```

### CDN (dynamic import)

```javascript
const ImageryLayer = await $arcgis.import(
  "@arcgis/core/layers/ImageryLayer.js",
);
const ImageryTileLayer = await $arcgis.import(
  "@arcgis/core/layers/ImageryTileLayer.js",
);
const RasterFunction = await $arcgis.import(
  "@arcgis/core/layers/support/RasterFunction.js",
);
```

## ImageryLayer

ImageryLayer connects to ArcGIS Image Services for dynamic raster data.

### Basic ImageryLayer

```javascript
const imageryLayer = new ImageryLayer({
  url: "https://sampleserver6.arcgisonline.com/arcgis/rest/services/ScientificData/SeaTemperature/ImageServer",
});

map.add(imageryLayer);
```

### ImageryLayer with Popup

```javascript
const imageryLayer = new ImageryLayer({
  url: "...",
  popupTemplate: {
    title: "Raster Value",
    content: "{Raster.ServicePixelValue}",
  },
});
```

### Key ImageryLayer Properties

| Property         | Type           | Description                                |
| ---------------- | -------------- | ------------------------------------------ |
| `url`            | string         | ImageServer REST endpoint                  |
| `format`         | string         | Output format (`"jpgpng"`, `"tiff"`, etc.) |
| `bandIds`        | number[]       | Which bands to display                     |
| `rasterFunction` | RasterFunction | Server-side processing                     |
| `mosaicRule`     | MosaicRule     | Raster combination rules                   |
| `pixelFilter`    | Function       | Client-side pixel processing               |
| `renderingRule`  | object         | Client-side rendering rules (JSON)         |

## ImageryTileLayer

ImageryTileLayer provides fast tiled access to imagery, including Cloud-Optimized GeoTIFF (COG).

### Basic ImageryTileLayer

```javascript
const imageryTileLayer = new ImageryTileLayer({
  url: "https://tiledimageservices.arcgis.com/...",
});

map.add(imageryTileLayer);
```

### Cloud Optimized GeoTIFF (COG)

```javascript
const imageryTileLayer = new ImageryTileLayer({
  url: "https://example.com/image.tif",
  title: "COG Layer",
});
```

## Raster Functions

### Apply Raster Function

```javascript
// Hillshade
const hillshadeFunction = new RasterFunction({
  functionName: "Hillshade",
  functionArguments: {
    azimuth: 315,
    altitude: 45,
    zFactor: 1,
  },
});

imageryLayer.rasterFunction = hillshadeFunction;
```

### Common Raster Functions

```javascript
// Stretch
const stretchFunction = new RasterFunction({
  functionName: "Stretch",
  functionArguments: {
    stretchType: 3,
    numberOfStandardDeviations: 2,
  },
});

// Colormap
const colormapFunction = new RasterFunction({
  functionName: "Colormap",
  functionArguments: {
    colormap: [
      [1, 255, 0, 0],
      [2, 0, 255, 0],
      [3, 0, 0, 255],
    ],
  },
});

// NDVI
const ndviFunction = new RasterFunction({
  functionName: "NDVI",
  functionArguments: {
    visibleBandID: 3,
    infraredBandID: 4,
  },
});
```

### RasterFunction Properties

| Property            | Type   | Description                 |
| ------------------- | ------ | --------------------------- |
| `functionName`      | string | Name of the raster function |
| `functionArguments` | object | Parameters for the function |
| `outputType`        | string | Output pixel type           |

**Common function names:** `Hillshade`, `Stretch`, `Colormap`, `NDVI`, `GVITINDEX`, `SAVI`, `Pansharpening`, `Convolution`, `MLClassify`

## Mosaic Rules

```javascript
const mosaicRule = new MosaicRule({
  mosaicMethod: "center", // "center", "northwest", "nadir", "lock-raster", "by-attribute"
  mosaicOperator: "first", // "first", "last", "min", "max", "mean", "sum", "blend"
  lockRasterIds: [1, 2, 3], // Lock to specific rasters
  multidimensionalDefinition: [], // For multidimensional data
});

imageryLayer.mosaicRule = mosaicRule;
```

## Multidimensional Data

### DimensionalDefinition

```javascript
// Define dimensions (depth, time, etc.)
const dimInfo = [];

// Depth dimension
dimInfo.push(
  new DimensionalDefinition({
    dimensionName: "StdZ",
    values: [0],
    isSlice: true,
  }),
);

// Time dimension
dimInfo.push(
  new DimensionalDefinition({
    dimensionName: "StdTime",
    values: [1396828800000],
    isSlice: true,
  }),
);

const mosaicRule = new MosaicRule({
  multidimensionalDefinition: dimInfo,
});

const layer = new ImageryLayer({
  url: "...",
  mosaicRule: mosaicRule,
});
```

### Accessing Multidimensional Info

```javascript
await imageryLayer.load();

const dimensions = imageryLayer.multidimensionalInfo.dimensions;
dimensions.forEach((dim) => {
  console.log("Dimension:", dim.name);
  console.log("Values:", dim.values);
  console.log("Unit:", dim.unit);
});
```

### ImageryTileLayer Multidimensional

```javascript
const layer = new ImageryTileLayer({
  url: "...",
  multidimensionalSubset: {
    dimensions: [
      {
        name: "StdTime",
        values: [
          /* epoch ms */
        ],
      },
      {
        name: "StdZ",
        values: [
          /* depth values */
        ],
      },
    ],
  },
  multidimensionalDefinition: [
    new DimensionalDefinition({
      dimensionName: "StdTime",
      values: [1609459200000],
    }),
  ],
});
```

**Common dimension names:** `StdTime`, `StdZ`, `StdPlev`, `StdDepth`

## Pixel Filtering

### Custom Pixel Filter

```javascript
const imageryLayer = new ImageryLayer({
  url: "...",
  pixelFilter: processPixels,
});

function processPixels(pixelData) {
  if (!pixelData || !pixelData.pixelBlock) return;

  const pixelBlock = pixelData.pixelBlock;
  const pixels = pixelBlock.pixels;
  let mask = pixelBlock.mask;
  const numPixels = pixelBlock.width * pixelBlock.height;

  const minVal = pixelBlock.statistics[0].minValue;
  const maxVal = pixelBlock.statistics[0].maxValue;
  const factor = 255 / (maxVal - minVal);

  const band = pixels[0];
  const rBand = new Uint8Array(numPixels);
  const gBand = new Uint8Array(numPixels);
  const bBand = new Uint8Array(numPixels);

  if (!mask) {
    mask = new Uint8Array(numPixels);
    mask.fill(1);
    pixelBlock.mask = mask;
  }

  for (let i = 0; i < numPixels; i++) {
    if (mask[i] === 0) continue;
    const normalized = (band[i] - minVal) * factor;
    rBand[i] = normalized;
    gBand[i] = 0;
    bBand[i] = 255 - normalized;
  }

  pixelData.pixelBlock.pixels = [rBand, gBand, bBand];
  pixelData.pixelBlock.statistics = null;
  pixelData.pixelBlock.pixelType = "u8";
}
```

### Masking Pixels by Value

```javascript
let minThreshold = 0;
let maxThreshold = 100;

function maskPixels(pixelData) {
  if (!pixelData || !pixelData.pixelBlock) return;

  const pixelBlock = pixelData.pixelBlock;
  const pixels = pixelBlock.pixels[0];
  let mask = pixelBlock.mask;

  if (!mask) {
    mask = new Uint8Array(pixels.length);
    mask.fill(1);
    pixelBlock.mask = mask;
  }

  for (let i = 0; i < pixels.length; i++) {
    mask[i] = pixels[i] >= minThreshold && pixels[i] <= maxThreshold ? 1 : 0;
  }
}

// Update thresholds and redraw
function updateThresholds(min, max) {
  minThreshold = min;
  maxThreshold = max;
  imageryLayer.redraw();
}
```

### PixelBlock Structure

| Property     | Type         | Description                                                  |
| ------------ | ------------ | ------------------------------------------------------------ |
| `pixels`     | TypedArray[] | One array per band                                           |
| `mask`       | Uint8Array   | 0 = transparent, 1 = opaque                                  |
| `statistics` | object[]     | `{ minValue, maxValue }` per band                            |
| `width`      | number       | Pixel block width                                            |
| `height`     | number       | Pixel block height                                           |
| `pixelType`  | string       | `"u8"`, `"u16"`, `"u32"`, `"s16"`, `"s32"`, `"f32"`, `"f64"` |

## Band Combinations

```javascript
// Select specific bands
imageryLayer.bandIds = [4, 3, 2]; // NIR, Red, Green (False color)

// Common band combinations
// Natural color: [1, 2, 3] (R, G, B)
// False color: [4, 3, 2] (NIR, R, G)
// SWIR: [7, 5, 4] (SWIR, NIR, R)
```

## Identify (Query Pixel Values)

```javascript
view.on("click", async (event) => {
  const result = await imageryLayer.identify({
    geometry: event.mapPoint,
    returnGeometry: false,
    returnCatalogItems: true,
  });

  console.log("Pixel value:", result.value);
  console.log("Catalog items:", result.catalogItems);
});
```

## Raster Statistics

```javascript
await imageryLayer.load();

const stats = imageryLayer.serviceRasterInfo.statistics;
console.log("Min:", stats[0].min);
console.log("Max:", stats[0].max);
console.log("Mean:", stats[0].avg);
console.log("StdDev:", stats[0].stddev);
```

## Oriented Imagery

### OrientedImageryLayer

```javascript
const oiLayer = new OrientedImageryLayer({
  url: "https://services.arcgis.com/.../FeatureServer/0",
});

map.add(oiLayer);
```

### OrientedImageryViewer Widget

```javascript
import OrientedImageryViewer from "@arcgis/core/widgets/OrientedImageryViewer.js";

const oiViewer = new OrientedImageryViewer({
  view: view,
});

view.ui.add(oiViewer, "top-right");
```

### Imagery Components

| Component                        | Purpose                              |
| -------------------------------- | ------------------------------------ |
| `arcgis-oriented-imagery-viewer` | View and navigate oriented imagery   |
| `arcgis-video-player`            | Play video feeds from video services |

## Common Pitfalls

1. **Pixel filter performance**: Complex pixel filters run on every render — optimize loops and minimize allocations.

2. **Band array indices**: Band IDs are 1-based in services but 0-based in `bandIds` arrays.

3. **Coordinate systems**: Imagery may need reprojection to match the view's spatial reference.

4. **Memory with large images**: Use `ImageryTileLayer` for large datasets; it tiles automatically.

5. **Pixel type conversion**: Be careful when changing `pixelType` in pixel filters — mismatches cause artifacts.

6. **Redraw after filter changes**: Call `imageryLayer.redraw()` after modifying external variables used in `pixelFilter`.

## Reference Samples

- `layers-imagerylayer` — Basic ImageryLayer
- `layers-imagery-pixelvalues` — Querying pixel values
- `layers-imagery-rasterfunction` — Raster function processing
- `layers-imagery-multidimensional` — Multidimensional imagery
- `layers-imagerytilelayer` — ImageryTileLayer
- `layers-imagerytilelayer-cog` — Cloud-Optimized GeoTIFF
- `layers-imagery-renderer` — Imagery renderers
- `layers-imagery-clientside` — Client-side imagery processing
- `layers-orientedimagerylayer` — Oriented imagery

## Related Skills

- `arcgis-time-animation` — Time-aware imagery animation
- `arcgis-layers` — Common layer patterns
- `arcgis-smart-mapping` — Auto-generated renderers
- `arcgis-custom-rendering` — Custom tile layer rendering
