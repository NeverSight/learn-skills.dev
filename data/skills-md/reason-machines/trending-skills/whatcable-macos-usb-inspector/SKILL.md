---
name: whatcable-macos-usb-inspector
description: macOS menu bar app that identifies USB-C cable capabilities and charging diagnostics using IOKit
triggers:
  - "add whatcable feature"
  - "decode USB-C cable info"
  - "read IOKit USB port data"
  - "parse power delivery PDO"
  - "add port summary logic"
  - "whatcable menu bar app"
  - "USB-C e-marker decoding swift"
  - "thunderbolt cable detection macos"
---

# WhatCable macOS USB-C Inspector

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

WhatCable is a macOS 14+ menu bar app (Swift/SwiftUI) that reads IOKit services to surface what each USB-C cable plugged into your Mac can actually do — speed, power rating, e-marker data, PDO profiles, and connected device identity — in plain English.

## Project Structure

```
Sources/WhatCable/
├── WhatCableApp.swift          # App entry point, menu bar setup
├── ContentView.swift           # Main popover UI
├── PortSummary.swift           # Plain-English logic per port
├── PDVDO.swift                 # PD VDO bit-twiddling / spec decoding
├── IOKitReader.swift           # IOKit service queries
└── ...
scripts/
└── build-app.sh                # Universal binary + notarisation
```

## Install / Build

```bash
# Run locally (development)
swift run WhatCable

# Build distributable universal app (arm64 + x86_64)
./scripts/build-app.sh
# → dist/WhatCable.app
# → dist/WhatCable.zip
```

Requires Swift 5.9 / Xcode 15+, macOS 14 (Sonoma) or later.

### Signed + Notarised Build

```bash
cp .env.example .env
# Edit .env:
# DEVELOPER_ID="Developer ID Application: Your Name (TEAMID)"
# NOTARY_PROFILE="WhatCable-notary"

# Store notarytool credentials once
xcrun notarytool store-credentials "WhatCable-notary" \
    --apple-id "$APPLE_ID" \
    --team-id "$TEAM_ID" \
    --password "$APP_SPECIFIC_PASSWORD"

./scripts/build-app.sh
```

## Key Concepts

### IOKit Service Families

| Service | Purpose |
|---|---|
| `AppleHPMInterfaceType10/11/12` (M3+) | Per-port state, transports, plug orientation, e-marker presence |
| `AppleTCControllerType10` (M1/M2) | Same, older HPM interface |
| `IOPortFeaturePowerSource` | Full PDO list + live negotiated PDO |
| `IOPortTransportComponentCCUSBPDSOP` | PD Discover Identity VDOs (SOP = partner, SOP' = cable e-marker) |

### USB PD VDO Decoding (PDVDO.swift)

The core bit-twiddling follows USB Power Delivery 3.x spec. Cable e-marker VDOs encode speed and current in specific bit fields.

```swift
// Example: decode cable speed from Passive Cable VDO
struct PassiveCableVDO {
    let raw: UInt32

    // Bits [5:3] — USB SuperSpeed signalling support
    var usbSSSignalling: UInt8 {
        UInt8((raw >> 3) & 0b111)
    }

    var dataRate: String {
        switch usbSSSignalling {
        case 0b000: return "USB 2.0 only"
        case 0b001: return "USB 3.2 Gen 1 (5 Gbps)"
        case 0b010: return "USB 3.2 Gen 2 (10 Gbps)"
        case 0b011: return "USB 3.2 Gen 2x2 / USB4 Gen 2 (20 Gbps)"
        case 0b100: return "USB4 Gen 3 (40 Gbps)"
        default:    return "Unknown"
        }
    }

    // Bits [6:5] — VBUS current handling
    var currentCapability: String {
        switch (raw >> 5) & 0b11 {
        case 0b00: return "USB Type-C Default (≤3A)"
        case 0b01: return "3A"
        case 0b10: return "5A"
        default:   return "Reserved"
        }
    }
}
```

### Reading IOKit Properties

```swift
import IOKit

func readPortProperties(serviceName: String) -> [String: Any]? {
    var iterator: io_iterator_t = 0
    let matchDict = IOServiceMatching(serviceName)
    guard IOServiceGetMatchingServices(kIOMainPortDefault,
                                       matchDict, &iterator) == KERN_SUCCESS else {
        return nil
    }
    defer { IOObjectRelease(iterator) }

    var service = IOIteratorNext(iterator)
    var results: [String: Any] = [:]
    while service != 0 {
        defer {
            IOObjectRelease(service)
            service = IOIteratorNext(iterator)
        }
        if let props = copyProperties(service) {
            results.merge(props) { _, new in new }
        }
    }
    return results.isEmpty ? nil : results
}

private func copyProperties(_ service: io_service_t) -> [String: Any]? {
    var propsRef: Unmanaged<CFMutableDictionary>?
    guard IORegistryEntryCreateCFProperties(service, &propsRef,
                                             kCFAllocatorDefault, 0) == KERN_SUCCESS,
          let props = propsRef?.takeRetainedValue() as? [String: Any] else {
        return nil
    }
    return props
}
```

### Port Summary Plain-English Logic (PortSummary.swift)

```swift
enum PortHeadline: String {
    case thunderbolt    = "Thunderbolt / USB4"
    case usbDevice      = "USB device connected"
    case chargingOnly   = "Charging only"
    case slowCable      = "Slow USB / charge-only cable"
    case nothing        = "Nothing connected"
}

struct PortSummary {
    let headline: PortHeadline
    let chargingDiagnostic: String?
    let dataRate: String?
    let currentRating: String?
    let negotiatedPDO: PDO?
    let allPDOs: [PDO]

    static func from(ioKitProps: [String: Any]) -> PortSummary {
        let hasThunderbolt = ioKitProps["Thunderbolt"] as? Bool ?? false
        let hasUSB3       = ioKitProps["USB3"] as? Bool ?? false
        let isConnected   = ioKitProps["Connected"] as? Bool ?? false
        let emarkerPresent = ioKitProps["CableEMarker"] as? Bool ?? false

        let headline: PortHeadline
        if !isConnected {
            headline = .nothing
        } else if hasThunderbolt {
            headline = .thunderbolt
        } else if hasUSB3 {
            headline = .usbDevice
        } else if emarkerPresent {
            headline = .chargingOnly
        } else {
            headline = .slowCable
        }

        // Parse PDOs for charging diagnostic
        let pdos = parsePDOs(from: ioKitProps)
        let negotiated = pdos.first(where: { $0.isActive })
        let diagnostic = buildChargingDiagnostic(pdos: pdos, negotiated: negotiated)

        return PortSummary(
            headline: headline,
            chargingDiagnostic: diagnostic,
            dataRate: emarkerPresent ? decodeDataRate(ioKitProps) : nil,
            currentRating: emarkerPresent ? decodeCurrentRating(ioKitProps) : nil,
            negotiatedPDO: negotiated,
            allPDOs: pdos
        )
    }
}
```

### PDO Parsing (Power Data Objects)

```swift
struct PDO {
    let voltage: Double    // Volts
    let maxCurrent: Double // Amps
    let maxWatts: Double   // voltage * maxCurrent
    let isActive: Bool

    static func parse(raw: UInt32, isActive: Bool) -> PDO? {
        // Fixed supply PDO: bits [19:10] = max current (10mA units),
        //                   bits [29:20] = voltage (50mV units)
        let currentRaw = (raw >> 10) & 0x3FF
        let voltageRaw = (raw >> 20) & 0x3FF
        guard voltageRaw > 0 else { return nil }

        let voltage = Double(voltageRaw) * 0.05
        let current = Double(currentRaw) * 0.01
        return PDO(
            voltage: voltage,
            maxCurrent: current,
            maxWatts: voltage * current,
            isActive: isActive
        )
    }
}

func parsePDOs(from props: [String: Any]) -> [PDO] {
    guard let pdoArray = props["PDOs"] as? [UInt32],
          let activePDOIndex = props["ActivePDOIndex"] as? Int else {
        return []
    }
    return pdoArray.enumerated().compactMap { idx, raw in
        PDO.parse(raw: raw, isActive: idx == activePDOIndex)
    }
}
```

### SwiftUI Popover Pattern (ContentView.swift)

```swift
import SwiftUI

struct ContentView: View {
    @StateObject private var model = CableModel()

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HeaderView()
            Divider()
            ScrollView {
                VStack(alignment: .leading, spacing: 12) {
                    ForEach(model.ports) { port in
                        PortRowView(port: port)
                    }
                }
                .padding()
            }
        }
        .frame(width: 360)
        .onAppear { model.refresh() }
    }
}

struct PortRowView: View {
    let port: PortSummary

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Label(port.headline.rawValue, systemImage: iconName(for: port.headline))
                .font(.headline)

            if let diagnostic = port.chargingDiagnostic {
                Text(diagnostic)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            if let rate = port.dataRate {
                Text("Speed: \(rate)")
                    .font(.caption)
            }
        }
        .padding(.vertical, 6)
    }

    func iconName(for headline: PortHeadline) -> String {
        switch headline {
        case .thunderbolt:  return "bolt.fill"
        case .usbDevice:    return "cable.connector"
        case .chargingOnly: return "battery.100.bolt"
        case .slowCable:    return "exclamationmark.triangle"
        case .nothing:      return "circle.dashed"
        }
    }
}
```

### Menu Bar App Setup (WhatCableApp.swift)

```swift
import SwiftUI

@main
struct WhatCableApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        // No WindowGroup — pure menu bar app
        Settings { SettingsView() }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    var popover = NSPopover()

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory) // hide from Dock by default

        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "cable.connector",
                                   accessibilityDescription: "WhatCable")
            button.action = #selector(togglePopover)
            button.sendAction(on: [.leftMouseUp, .rightMouseUp])
        }

        popover.contentViewController = NSHostingController(rootView: ContentView())
        popover.behavior = .transient
    }

    @objc func togglePopover(_ sender: NSStatusBarButton) {
        if popover.isShown {
            popover.performClose(sender)
        } else {
            if let button = statusItem?.button {
                popover.show(relativeTo: button.bounds, of: button,
                             preferredEdge: .minY)
            }
        }
    }
}
```

### Charging Diagnostic Helper

```swift
func buildChargingDiagnostic(pdos: [PDO], negotiated: PDO?) -> String? {
    guard let active = negotiated else { return nil }
    let maxAvailable = pdos.map(\.maxWatts).max() ?? 0

    let activeW = active.maxWatts
    let ratio = maxAvailable > 0 ? activeW / maxAvailable : 1.0

    if ratio < 0.5 {
        return String(format: "Charging at %.0fW (charger can do up to %.0fW)", activeW, maxAvailable)
    } else if ratio < 0.9 {
        return String(format: "Cable is limiting charging speed (%.0fW of %.0fW available)", activeW, maxAvailable)
    } else {
        return String(format: "Charging well at %.0fW", activeW)
    }
}
```

## Common Patterns

### Adding a New Port Property

1. Read the raw value from IOKit props in `IOKitReader.swift`
2. Decode it (bit-fields) in `PDVDO.swift` or a dedicated decoder
3. Expose it on `PortSummary` struct
4. Display it in `PortRowView` or a detail expansion in `ContentView.swift`

### Handling Different Mac Generations

```swift
let hpmServiceNames = [
    "AppleHPMInterfaceType12",  // M3-era
    "AppleHPMInterfaceType11",
    "AppleHPMInterfaceType10",
    "AppleTCControllerType10",  // M1 / M2
]

func findHPMService() -> io_service_t {
    for name in hpmServiceNames {
        let service = IOServiceGetMatchingService(
            kIOMainPortDefault,
            IOServiceMatching(name)
        )
        if service != IO_OBJECT_NULL { return service }
    }
    return IO_OBJECT_NULL
}
```

### Debug / Engineer Mode (⌥-click)

```swift
@State private var showRawProps = false

// In button handler:
if NSEvent.modifierFlags.contains(.option) {
    showRawProps.toggle()
}

// In view:
if showRawProps, let props = port.rawIOKitProperties {
    RawPropertiesView(props: props)
}
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| No ports shown | IOKit service name mismatch | Try all `hpmServiceNames` variants; check `ioreg -l` output |
| E-marker data missing | Cable has no e-marker chip | Expected for cables < 60W; only marked cables have VDOs |
| PDO list empty | Device not PD-capable or port is source-only | Check `IOPortFeaturePowerSource` presence in `ioreg` |
| Build fails on Intel | Architecture flag missing | Use `./scripts/build-app.sh` for universal build |
| Gatekeeper warning | Ad-hoc signature only | Set `DEVELOPER_ID` in `.env` and re-run build script |
| Wrong wattage shown | PD 3.2 EPR AVS PDO format | EPR PDOs use different bit layout; check PD 3.2 spec §6.4.1 |

### Inspect IOKit Live

```bash
# Dump all HPM interface properties
ioreg -l -n AppleHPMInterfaceType10 | less

# Watch for USB-C connect/disconnect events
ioreg -w 0 -l -c IOUSBDevice | grep -E "Product|Vendor|Speed"

# Check power delivery objects
ioreg -l | grep -A 20 IOPortFeaturePowerSource
```

### Key IOKit Property Names to Watch

```swift
// Connection state
"Connected"              // Bool
"PlugOrientation"        // Int (0 = unflipped, 1 = flipped)

// Transports
"USB2"                   // Bool
"USB3"                   // Bool  
"Thunderbolt"            // Bool
"DisplayPort"            // Bool

// E-marker
"CableEMarker"           // Bool
"CableVDO"               // UInt32 — raw passive cable VDO
"ActiveCableVDO1"        // UInt32 — active cable VDO

// Power
"PDOs"                   // [UInt32]
"ActivePDOIndex"         // Int
"NegotiatedWatts"        // Double
```
