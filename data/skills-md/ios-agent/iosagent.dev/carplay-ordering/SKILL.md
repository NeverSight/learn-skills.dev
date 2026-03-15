---
name: carplay-ordering
description: >
  Guide for building CarPlay quick-ordering apps (food ordering, pickup, etc.) using the CarPlay framework.
  Use this skill whenever the user wants to build a CarPlay ordering app, integrate CarPlay templates
  for food/drink/pickup ordering, work with CPPointOfInterestTemplate, CPListTemplate, CPTabBarTemplate,
  or CPInterfaceController for ordering workflows. Also trigger when the user mentions CarPlay entitlements,
  Live Activities with CarPlay ordering, or push notification updates for order status.
  Covers the full lifecycle: entitlement setup, template hierarchy, map-based POI selection,
  order placement, Live Activity integration, and push token management.
---

# CarPlay Quick-Ordering App Integration

Build a CarPlay-enabled ordering app that displays custom ordering options in a vehicle using Apple's CarPlay framework.

## When to Use This Skill

- Building a food/drink ordering app with CarPlay support
- Integrating `CPPointOfInterestTemplate`, `CPListTemplate`, or `CPTabBarTemplate`
- Setting up CarPlay entitlements and provisioning profiles
- Implementing order status with Live Activities from a CarPlay context
- Handling map region changes and location-based search in CarPlay
- Managing push notifications for order status updates

## Prerequisites

- iOS 17.2+ / iPadOS 17.2+ / Mac Catalyst 17.2+ / macOS 14.0+
- Xcode 15.4+
- CarPlay quick-ordering entitlement (request at https://developer.apple.com/contact/carplay)

## Entitlement Setup

1. Log in to Apple Developer and create a provisioning profile with the CarPlay quick-ordering entitlement
2. Import the provisioning profile into Xcode
3. Create an `Entitlements.plist` (if not already present)
4. Add the CarPlay quick-ordering entitlement key as a Boolean
5. Ensure `CODE_SIGN_ENTITLEMENTS` in target build settings points to the `Entitlements.plist`

## Architecture Overview

The app connects to CarPlay via `CPTemplateApplicationSceneDelegate`. The template hierarchy is:

```
CPInterfaceController (root controller)
 └── CPTabBarTemplate
      └── CPPointOfInterestTemplate (map with ordering locations)
           └── CPListTemplate (order details/menu items)
```

Key classes and their roles:
- **`CPInterfaceController`** — Manages the template stack and presentation
- **`CPTabBarTemplate`** — Top-level tab container
- **`CPPointOfInterestTemplate`** — Map view showing up to 12 POI locations
- **`CPListTemplate`** — Displays menu items and order options
- **`CPTextButton`** — Action buttons (Order, Directions, Call)
- **`CPAlertTemplate`** — Alert dialogs (e.g., location permission prompts)
- **`CPSessionConfiguration`** — Session configuration delegate

## Connection Lifecycle

When CarPlay connects, implement `CPTemplateApplicationSceneDelegate`:

```swift
func interfaceControllerDidConnect(
    _ interfaceController: CPInterfaceController,
    scene: CPTemplateApplicationScene
) {
    carplayInterfaceController = interfaceController
    carplayScene = scene
    carplayInterfaceController?.delegate = self
    sessionConfiguration = CPSessionConfiguration(delegate: self)
    locationManager.delegate = self
    requestLocation()
    setupMap()
}
```

Set the root template as a `CPTabBarTemplate` containing a `CPPointOfInterestTemplate`:

```swift
func setupMap() {
    let poiTemplate = CPPointOfInterestTemplate(
        title: "Options",
        pointsOfInterest: [],
        selectedIndex: NSNotFound
    )
    poiTemplate.pointOfInterestDelegate = self
    poiTemplate.tabTitle = "Map"
    poiTemplate.tabImage = UIImage(systemName: "car")!

    let tabTemplate = CPTabBarTemplate(templates: [poiTemplate])
    carplayInterfaceController?.setRootTemplate(tabTemplate, animated: true) { done, error in
        self.search(for: "YourSearchTerm")
    }
}
```

> **Important:** A maximum of 12 POI locations can appear on the CarPlay display.

## Map Region Updates

Implement `CPPointOfInterestTemplateDelegate` to refresh results as the user pans the map:

```swift
extension TemplateManager: CPPointOfInterestTemplateDelegate {
    func pointOfInterestTemplate(
        _ aTemplate: CPPointOfInterestTemplate,
        didChangeMapRegion region: MKCoordinateRegion
    ) {
        boundingRegion = region
        search(for: "yourQuery")
    }
}
```

## POI Action Buttons

Each point of interest supports a primary and secondary button. Use the primary for ordering, and the secondary for navigation or calling:

```swift
// Primary: Order button
let orderButton = CPTextButton(title: "Order", textStyle: .normal) { button in
    self.showOrderTemplate(place: place)
}
place.primaryButton = orderButton

// Secondary: Directions (via Maps) or Call
if let address = place.summary,
   let encoded = address.addingPercentEncoding(withAllowedCharacters: .alphanumerics),
   let lon = place.location.placemark.location?.coordinate.longitude,
   let lat = place.location.placemark.location?.coordinate.latitude,
   let url = URL(string: "maps://?q=\(encoded)&ll=\(lon),\(lat)") {
    place.secondaryButton = CPTextButton(title: "Directions", textStyle: .normal) { _ in
        self.carplayScene?.open(url, options: nil, completionHandler: nil)
    }
} else if let phone = place.subtitle,
          let url = URL(string: "tel://" + phone.replacingOccurrences(of: " ", with: "")) {
    place.secondaryButton = CPTextButton(title: "Call", textStyle: .normal) { _ in
        self.carplayScene?.open(url, options: nil, completionHandler: nil)
    }
}
```

## Location Permission Handling

Handle authorization changes gracefully. If location is denied, present an alert and clear the root template:

```swift
func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
    switch manager.authorizationStatus {
    case .denied, .restricted, .notDetermined:
        let alert = CPAlertTemplate(
            titleVariants: ["Please enable location services."],
            actions: [
                CPAlertAction(title: "Ok", style: .default) { [weak self] _ in
                    self?.carplayInterfaceController?.setRootTemplate(
                        CPTabBarTemplate(templates: []),
                        animated: false,
                        completion: nil
                    )
                }
            ]
        )
        // Dismiss any existing presented template first
        if carplayInterfaceController?.presentedTemplate != nil {
            dismissAlertAndPopToRootTemplate {
                self.carplayInterfaceController?.presentTemplate(alert, animated: false, completion: nil)
            }
        } else {
            carplayInterfaceController?.presentTemplate(alert, animated: false, completion: nil)
        }
    default:
        dismissAlertAndPopToRootTemplate {
            self.setupMap()
        }
    }
}
```

## Order Status with Live Activities

After a user places an order, start a Live Activity to show status on the Lock Screen. Live Activities don't display in CarPlay but provide glanceable updates:

```swift
let attrs = OrderStatusAttributes(order: order)
let initialState = OrderStatusAttributes.ContentState(
    isPickedUp: false,
    isReady: false,
    isPreparing: false,
    isConfirmed: true
)

let activity = try Activity.request(
    attributes: attrs,
    content: .init(state: initialState, staleDate: Date(timeIntervalSinceNow: 60 * 30)),
    pushType: .token
)
```

### Listening for Updates

Set up listeners for content updates, state changes, and push token updates. This is critical because quick-ordering apps spend time in the background — use push notifications for updates:

```swift
// Content updates
Task { @MainActor in
    for await change in activity.contentUpdates {
        try saveOrderState(state: change.state)
        WidgetCenter.shared.reloadAllTimelines()
    }
}

// Activity state (ended/dismissed)
Task { @MainActor in
    for await state in activity.activityStateUpdates {
        if state == .dismissed || state == .ended {
            await activity.end(nil, dismissalPolicy: .immediate)
        }
        WidgetCenter.shared.reloadAllTimelines()
    }
}

// Push token for remote updates
Task { @MainActor in
    for await pushToken in activity.pushTokenUpdates {
        let tokenString = pushToken.reduce("") { $0 + String(format: "%02x", $1) }
        try await sendPushToken(order: order, pushTokenString: tokenString)
    }
}
```

### Push Notification JWT

For server-side push notifications to update Live Activities, create a JWT using P256 signing:

```swift
let privateKey = try P256.Signing.PrivateKey(pemRepresentation: pemString)
let header = try JSONEncoder().encode(header).urlSafeBase64EncodedString()
let payload = try JSONEncoder().encode(payload).urlSafeBase64EncodedString()
let toSign = Data((header + "." + payload).utf8)
let signature = try privateKey.signature(for: toSign)
let token = [header, payload, signature.rawRepresentation.urlSafeBase64EncodedString()]
    .joined(separator: ".")
```

## Key Design Considerations

- **12 POI limit** — CarPlay displays a maximum of 12 points of interest at once
- **Background updates** — Use push notifications, not foreground polling, since quick-ordering apps spend most time in background
- **Location is essential** — Handle all authorization states gracefully; the app depends on location for relevant results
- **Live Activities** — They don't render in CarPlay, but provide Lock Screen status updates
- **Stale dates** — Set reasonable stale dates on Live Activity content (e.g., 30 minutes for food orders)
- **Token management** — Cache and refresh JWTs; listen for push token changes on the activity

## See Also

- [`CPPointOfInterestTemplate`](https://developer.apple.com/documentation/carplay/cppointofinteresttemplate) — Map with selectable POIs
- [`CPInformationTemplate`](https://developer.apple.com/documentation/carplay/cpinformationtemplate) — Info display for orders, parking, charging
- [`CPTextButton`](https://developer.apple.com/documentation/carplay/cptextbutton) — Stylized action buttons
- [Apple CarPlay Entitlement Request](https://developer.apple.com/contact/carplay)
- [Sample Project Download](https://docs-assets.developer.apple.com/published/51654e33d2be/IntegratingCarPlayWithYourQuickOrderingApp.zip)
