---
name: arcgis-utility-networks
description: Work with ArcGIS Utility Networks for modeling and analyzing connected infrastructure including network tracing, associations visualization, and topology validation. Use for electric, gas, water, and telecom network analysis.
---

# ArcGIS Utility Networks

Use this skill for utility networks: tracing, associations, topology validation, and network analysis for connected infrastructure.

## Import Patterns

### ESM (npm)

```javascript
// Core network class
import UtilityNetwork from "@arcgis/core/networks/UtilityNetwork.js";

// Widgets
import UtilityNetworkTrace from "@arcgis/core/widgets/UtilityNetworkTrace.js";
import UtilityNetworkAssociations from "@arcgis/core/widgets/UtilityNetworkAssociations.js";
import UtilityNetworkValidateTopology from "@arcgis/core/widgets/UtilityNetworkValidateTopology.js";

// Support
import TileInfo from "@arcgis/core/layers/support/TileInfo.js";
import WebMap from "@arcgis/core/WebMap.js";
import MapView from "@arcgis/core/views/MapView.js";
import esriConfig from "@arcgis/core/config.js";
```

### CDN (dynamic import)

```javascript
const UtilityNetwork = await $arcgis.import(
  "@arcgis/core/networks/UtilityNetwork.js",
);
const UtilityNetworkTrace = await $arcgis.import(
  "@arcgis/core/widgets/UtilityNetworkTrace.js",
);
const UtilityNetworkAssociations = await $arcgis.import(
  "@arcgis/core/widgets/UtilityNetworkAssociations.js",
);
```

## Key Concepts

Utility networks model connected infrastructure (electric, gas, water, telecom). Key concepts:

- **Network tracing** — Follow connectivity through the network
- **Associations** — Connectivity, containment, and structural attachment relationships
- **Subnetworks** — Isolated portions of the network
- **Topology** — Network connectivity validation

## Map Components Approach

### Utility Network Trace Component

```html
<arcgis-map item-id="471eb0bf37074b1fbb972b1da70fb310">
  <arcgis-utility-network-trace slot="top-right"></arcgis-utility-network-trace>
</arcgis-map>
```

### Utility Network Associations Component

```html
<arcgis-map item-id="e53b1054b29f4579baf878dcf2effe7a">
  <arcgis-utility-network-associations
    slot="top-right"
  ></arcgis-utility-network-associations>
</arcgis-map>
```

### Utility Network Validate Topology Component

```html
<arcgis-map item-id="YOUR_WEBMAP_ID">
  <arcgis-utility-network-validate-topology
    slot="top-right"
  ></arcgis-utility-network-validate-topology>
</arcgis-map>
```

### Utility Network Trace Analysis Component

```html
<arcgis-map item-id="YOUR_WEBMAP_ID">
  <arcgis-utility-network-trace-analysis
    slot="top-right"
  ></arcgis-utility-network-trace-analysis>
</arcgis-map>
```

## Components Summary

| Component                                  | Purpose                   |
| ------------------------------------------ | ------------------------- |
| `arcgis-utility-network-trace`             | Interactive trace UI      |
| `arcgis-utility-network-associations`      | Association visualization |
| `arcgis-utility-network-trace-analysis`    | Detailed trace analysis   |
| `arcgis-utility-network-validate-topology` | Topology validation       |

## Core API Approach

### UtilityNetworkTrace Widget

```javascript
esriConfig.portalUrl = "https://www.arcgis.com";

const webmap = new WebMap({
  portalItem: { id: "YOUR_WEBMAP_ID" },
});

const view = new MapView({
  container: "viewDiv",
  map: webmap,
});

const utilityNetworkTrace = new UtilityNetworkTrace({
  view: view,
  showSelectionAttributes: true,
  selectOnComplete: true,
});

view.ui.add(utilityNetworkTrace, "top-right");
```

### UtilityNetworkTrace Properties

| Property                  | Type       | Description                              |
| ------------------------- | ---------- | ---------------------------------------- |
| `view`                    | MapView    | Map view (required)                      |
| `flags`                   | MapPoint[] | Starting points and barriers             |
| `selectedTraces`          | string[]   | Global IDs of traces to select on load   |
| `showSelectionAttributes` | boolean    | Show results as organized list           |
| `selectOnComplete`        | boolean    | Auto-select features on trace completion |
| `enableResultArea`        | boolean    | Show result area graphics                |
| `resultAreaColor`         | Color      | Color for aggregated trace geometry      |

### UtilityNetworkTrace Events

| Event                 | Description                             |
| --------------------- | --------------------------------------- |
| `trace-complete`      | Fires after a trace completes           |
| `result-area-added`   | Fires when adding result area graphic   |
| `result-area-removed` | Fires when removing result area graphic |

### UtilityNetworkAssociations Widget

```javascript
view.when(async () => {
  await webMap.load();

  if (webMap.utilityNetworks.length > 0) {
    const utilityNetwork = webMap.utilityNetworks.getItemAt(0);
    await utilityNetwork.load();

    const unAssociations = new UtilityNetworkAssociations({
      view,
      utilityNetwork,
    });

    view.ui.add(unAssociations, "top-right");
  }
});
```

### Association Types

- **Connectivity** — Electrical/flow connections between features
- **Containment** — Features contained inside other features
- **Structural Attachment** — Features attached to structures

### Associations Visible Elements

```javascript
const unAssociations = new UtilityNetworkAssociations({
  view,
  utilityNetwork,
  visibleElements: {
    maxAllowableAssociationsSlider: true,
    connectivityAssociationsSettings: {
      arrowsToggle: false,
      capSelect: false,
      colorPicker: true,
      stylePicker: true,
      widthInput: true,
    },
    structuralAttachmentAssociationsSettings: {
      arrowsToggle: false,
      capSelect: false,
      colorPicker: true,
      stylePicker: true,
      widthInput: true,
    },
  },
});
```

## Accessing Utility Networks

### Get Utility Network from WebMap

```javascript
await webMap.load();

if (webMap.utilityNetworks && webMap.utilityNetworks.length > 0) {
  const utilityNetwork = webMap.utilityNetworks.getItemAt(0);
  await utilityNetwork.load();

  console.log("Title:", utilityNetwork.title);
  console.log("Dataset name:", utilityNetwork.datasetName);
  console.log("Domain networks:", utilityNetwork.domainNetworks);
  console.log("Network attributes:", utilityNetwork.networkAttributes);
  console.log("Terminal configs:", utilityNetwork.terminalConfigurations);
}
```

### UtilityNetwork Properties

| Property                         | Type     | Description                            |
| -------------------------------- | -------- | -------------------------------------- |
| `title`                          | string   | Network title                          |
| `datasetName`                    | string   | Dataset name                           |
| `domainNetworks`                 | object[] | Domain networks in the utility network |
| `networkAttributes`              | object[] | Network attributes                     |
| `terminalConfigurations`         | object[] | Terminal configurations                |
| `sharedNamedTraceConfigurations` | object[] | Shared trace configurations            |

### UtilityNetwork Methods

| Method                                    | Description                                           |
| ----------------------------------------- | ----------------------------------------------------- |
| `load()`                                  | Load utility network metadata                         |
| `trace(traceParams)`                      | Execute trace synchronously                           |
| `submitTraceJob(traceParams)`             | Execute trace asynchronously                          |
| `queryAssociations(params)`               | Query associations                                    |
| `synthesizeAssociationGeometries(extent)` | Get association geometries                            |
| `loadAssociationsTable()`                 | Load associations table (recommended before querying) |

## Network Tracing

### Trace Types

| Trace Type | Description                      |
| ---------- | -------------------------------- |
| Connected  | Find all connected features      |
| Upstream   | Trace toward sources             |
| Downstream | Trace away from sources          |
| Subnetwork | Find features in same subnetwork |
| Isolation  | Find isolation points            |
| Loops      | Find loops in network            |

### Execute Trace Programmatically

```javascript
const utilityNetwork = webMap.utilityNetworks.getItemAt(0);
await utilityNetwork.load();

const traceResult = await utilityNetwork.trace(traceParams);

// For long-running traces
const jobInfo = await utilityNetwork.submitTraceJob(traceParams);
```

### Query Associations

```javascript
await utilityNetwork.loadAssociationsTable();

const result = await utilityNetwork.queryAssociations(queryParams);
```

## High Zoom Level Support

Associations are only visible at very high zoom levels. Configure additional LODs:

```javascript
const tileInfo = TileInfo.create({
  spatialReference: { wkid: 102100 },
  numLODs: 32,
});

const view = new MapView({
  container: "viewDiv",
  map: webMap,
  zoom: 25,
  constraints: {
    lods: tileInfo.lods,
    snapToZoom: false,
  },
});
```

## Complete Example

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <link
      rel="stylesheet"
      href="https://js.arcgis.com/5.0/esri/themes/light/main.css"
    />
    <script type="module" src="https://js.arcgis.com/5.0/"></script>
    <script
      type="module"
      src="https://js.arcgis.com/map-components/5.0/arcgis-map-components.esm.js"
    ></script>
    <style>
      html,
      body {
        height: 100%;
        margin: 0;
      }
    </style>
  </head>
  <body>
    <arcgis-map item-id="YOUR_WEBMAP_ID">
      <arcgis-utility-network-trace
        slot="top-right"
      ></arcgis-utility-network-trace>
      <arcgis-utility-network-associations
        slot="bottom-right"
      ></arcgis-utility-network-associations>
    </arcgis-map>
  </body>
</html>
```

## Common Pitfalls

1. **Authentication required**: Utility network services typically require authentication — configure `esriConfig.portalUrl` and credentials.

2. **WebMap required**: Utility networks must be accessed through a WebMap — they cannot be created client-side.

3. **High zoom for associations**: Associations only display at very high zoom levels — use `TileInfo.create({ numLODs: 32 })` and set `snapToZoom: false`.

4. **Load order**: Must load WebMap first, then load UtilityNetwork before creating widgets.

5. **Enterprise portals**: Often hosted on ArcGIS Enterprise — set `esriConfig.portalUrl` to the portal URL.

6. **Topology validation**: Network topology must be enabled and validated before accurate tracing results.

7. **Named trace configurations**: Trace widget requires shared named trace configurations (Enterprise 10.9+).

## Reference Samples

- `utility-network-trace` — Running utility network traces
- `utility-network-associations` — Viewing associations
- `widgets-untrace` — Utility network trace widget

## Related Skills

- `arcgis-layers` — Layer configuration and WebMap loading
- `arcgis-authentication` — Portal authentication setup
- `arcgis-widgets-ui` — Widget placement and UI customization
