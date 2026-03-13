---
name: charts-3d
description: Swift Charts 3D visualization with Chart3D container, SurfacePlot for 3D surface rendering from functions or data, Chart3DPose for viewing angle control (predefined poses and custom azimuth/inclination), Chart3DSurfaceStyle for gradient coloring, interactive rotation via @State binding, axis customization (labels, gridlines, value ranges), and visionOS volumetric rendering. Use when building data visualization with 3D surfaces, scientific plots, or immersive chart experiences.
---

# Swift Charts — 3D Visualization

## Basic 3D Surface Plot
```swift
import SwiftUI
import Charts

struct Surface3DView: View {
    var body: some View {
        Chart3D {
            SurfacePlot(x: "X", y: "Y", z: "Z") { x, y in
                sin(x) * cos(y)
            }
        }
    }
}
```

## Custom Viewing Angle
```swift
@State private var pose: Chart3DPose = .default

Chart3D {
    SurfacePlot(x: "X", y: "Y", z: "Z") { x, y in sin(x) * cos(y) }
}
.chart3DPose(pose)

// Predefined poses: .default, .front, .back, .top, .bottom, .left, .right
// Custom pose:
Chart3DPose(azimuth: .degrees(45), inclination: .degrees(30))
```

## Interactive Rotation
```swift
struct InteractiveChart: View {
    @State private var pose: Chart3DPose = .default

    var body: some View {
        Chart3D {
            SurfacePlot(x: "X", y: "Y", z: "Z") { x, y in sin(x) * cos(y) }
        }
        .chart3DPose($pose)  // Bind for user interaction (drag to rotate)
    }
}
```

## Surface Styling
```swift
Chart3D {
    SurfacePlot(x: "X", y: "Y", z: "Height") { x, y in
        sin(x) * cos(y)
    }
    .foregroundStyle(
        .linearGradient(
            colors: [.blue, .green, .yellow, .red],
            startPoint: .bottom, endPoint: .top
        )
    )
}
.chart3DSurfaceStyle(.wireframe)         // Wireframe only
.chart3DSurfaceStyle(.solid)             // Solid surface
.chart3DSurfaceStyle(.solidWithEdges)    // Solid + wireframe overlay
```

## Axis Customization
```swift
Chart3D {
    SurfacePlot(x: "Longitude", y: "Latitude", z: "Elevation") { x, y in
        elevation(at: x, y)
    }
}
.chartXAxisLabel("Longitude")
.chartYAxisLabel("Latitude")
.chartZAxisLabel("Elevation (m)")
.chartXScale(domain: -180...180)
.chartYScale(domain: -90...90)
```

## From Data Points
```swift
struct DataPoint3D: Identifiable {
    var x: Double, y: Double, z: Double
    var id = UUID()
}

Chart3D(dataPoints) { point in
    // Mark3D or other 3D mark types
}
```

## visionOS Volumetric Window
```swift
// visionOS only — renders chart as volumetric object
WindowGroup {
    Chart3D { SurfacePlot(x: "X", y: "Y", z: "Z") { x, y in sin(x) * cos(y) } }
}
.windowStyle(.volumetric)
.defaultSize(width: 0.5, height: 0.5, depth: 0.5, in: .meters)
```

## References

- [Swift Charts](https://developer.apple.com/documentation/Charts)
- [Chart3D](https://developer.apple.com/documentation/Charts/Chart3D)
- [WWDC 2025: Visualize 3D data with Swift Charts](https://developer.apple.com/videos/play/wwdc2025/)
