---
name: mapkit-geo
description: MapKit and GeoToolbox framework patterns for location-based features. Covers PlaceDescriptor (standardized place representation across mapping services), PlaceRepresentation (.coordinate, .address), SupportingPlaceRepresentation for third-party service IDs (Google Places, Here, Foursquare), MKMapItem ↔ PlaceDescriptor conversion, Map view with annotations and overlays, geocoding, local search, and place sharing. Use when building location features, implementing maps, working with place data, or integrating with third-party mapping services.
---

# MapKit & GeoToolbox

## PlaceDescriptor (GeoToolbox)

Standardized place representation that works across mapping services.

```swift
import GeoToolbox
import MapKit

// From address
let place = PlaceDescriptor(
    representations: [.address("121 James's St\nDublin 8\nIreland")],
    commonName: "Obelisk Fountain"
)

// From coordinates
let tower = PlaceDescriptor(
    representations: [.coordinate(CLLocationCoordinate2D(latitude: 48.8584, longitude: 2.2945))],
    commonName: "Eiffel Tower"
)

// Multiple representations
let statue = PlaceDescriptor(
    representations: [
        .coordinate(CLLocationCoordinate2D(latitude: 40.6892, longitude: -74.0445)),
        .address("Liberty Island, New York, NY 10004")
    ],
    commonName: "Statue of Liberty"
)

// From MKMapItem
let descriptor = PlaceDescriptor(item: mapItem)

// Access properties
let coord = descriptor.coordinate       // CLLocationCoordinate2D?
let address = descriptor.address         // String?
let name = descriptor.commonName         // String?
```

## Third-Party Place IDs (SupportingPlaceRepresentation)
```swift
// Attach third-party identifiers
let place = PlaceDescriptor(
    representations: [.coordinate(coord)],
    supportingRepresentations: [
        SupportingPlaceRepresentation(service: .googleMaps, identifier: "ChIJ..."),
        SupportingPlaceRepresentation(service: .here, identifier: "here:..."),
        SupportingPlaceRepresentation(service: .foursquare, identifier: "4b...")
    ],
    commonName: "My Place"
)

// Extract specific service ID
func getGooglePlaceID(from descriptor: PlaceDescriptor) -> String? {
    descriptor.supportingRepresentations
        .first(where: { $0.service == .googleMaps })?
        .identifier
}
```

## Convert PlaceDescriptor → MKMapItem
```swift
func convertToMapItem(descriptor: PlaceDescriptor) async throws -> MKMapItem? {
    if let coord = descriptor.coordinate {
        let placemark = MKPlacemark(coordinate: coord)
        let item = MKMapItem(placemark: placemark)
        item.name = descriptor.commonName
        return item
    }
    if let address = descriptor.address {
        let geocoder = CLGeocoder()
        let placemarks = try await geocoder.geocodeAddressString(address)
        if let first = placemarks.first {
            return MKMapItem(placemark: MKPlacemark(placemark: first))
        }
    }
    return nil
}
```

## SwiftUI Map
```swift
import MapKit

struct MapView: View {
    @State private var position: MapCameraPosition = .automatic
    let places: [PlaceDescriptor]

    var body: some View {
        Map(position: $position) {
            ForEach(places.indices, id: \.self) { i in
                if let coord = places[i].coordinate {
                    Marker(places[i].commonName ?? "Place", coordinate: coord)
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic))
    }
}
```

## References

- [GeoToolbox](https://developer.apple.com/documentation/GeoToolbox)
- [MapKit for SwiftUI](https://developer.apple.com/documentation/mapkit/mapkit_for_swiftui)
