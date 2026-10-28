---
name: awawausb-webusb-firefox
description: WebUSB extension for Firefox using native messaging to enable USB device access from web pages
triggers:
  - add WebUSB support to Firefox
  - access USB devices from Firefox browser
  - install awawausb extension
  - native stub setup for WebUSB Firefox
  - configure native messaging for USB
  - WebUSB native manifest Firefox
  - build awawausb from source
  - troubleshoot Firefox WebUSB devices
---

# awawausb — WebUSB Extension for Firefox

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`awawausb` adds WebUSB (`navigator.usb`) to Firefox via a two-part system: a browser extension (`.xpi`) and a native stub binary (compiled Rust) that communicates over native messaging.

## Architecture

```
Web Page (navigator.usb)
    ↕  WebExtension API
Firefox Extension (extension/)
    ↕  Native Messaging (stdio, JSON-framed)
Native Stub Binary (native-stub/ — Rust)
    ↕  OS USB APIs (WinUSB / libusb / IOKit)
USB Device
```

## Installation (End Users)

### 1. Install the Extension

- **Signed release**: Download `.xpi` from GitHub Releases, open in Firefox.
- **Developer/testing**: `about:debugging` → "This Firefox" → "Load Temporary Add-on…" → select `extension/manifest.json`.

### 2. Install the Native Stub

Download and unzip the release archive for your platform, then run:

```bash
# Linux / macOS
./install.sh

# Windows
install.bat
```

Supported platforms: macOS x86_64/ARM64, Linux x86_64/aarch64, Windows AMD64/ARM64.

## Building from Source

```bash
# Clone
git clone https://github.com/ArcaneNibble/awawausb
cd awawausb/native-stub

# Default build (host platform)
cargo build --release
```

### Platform Notes

| Platform | Notes |
|----------|-------|
| macOS | Should "just work"; vendored `.tbd` files included |
| Linux | Uses musl libc by default for static binaries; glibc builds work but untested |
| Windows | Uses mingw-w64 UCRT (`*-windows-gnullvm`); MSVC not supported |

### Cross-compiling (Linux → Windows example)

```bash
# Install mingw-w64, then:
rustup target add x86_64-pc-windows-gnullvm
cargo build --release --target x86_64-pc-windows-gnullvm
```

## Manual Native Manifest Setup

After building, tell Firefox where the native stub binary is by placing a JSON manifest file in the correct location.

### Manifest Content

```json
{
  "name": "awawausb_native_stub",
  "description": "Allows WebUSB extension to access USB devices",
  "path": "/absolute/path/to/awawausb-native-stub",
  "type": "stdio",
  "allowed_extensions": ["awawausb@arcanenibble.com"]
}
```

On Windows, `path` can be just `"awawausb-native-stub.exe"` (no absolute path required).

### Manifest Locations

**macOS**
```
# Global
/Library/Application Support/Mozilla/NativeMessagingHosts/awawausb_native_stub.json

# User-local
~/Library/Application Support/Mozilla/NativeMessagingHosts/awawausb_native_stub.json
```

**Linux**
```
# Global
/usr/lib/mozilla/native-messaging-hosts/awawausb_native_stub.json
/usr/lib64/mozilla/native-messaging-hosts/awawausb_native_stub.json

# User-local
~/.mozilla/native-messaging-hosts/awawausb_native_stub.json
```

**Windows** (registry keys)
```
# Global
HKLM\SOFTWARE\Mozilla\NativeMessagingHosts\awawausb_native_stub

# User-local
HKCU\SOFTWARE\Mozilla\NativeMessagingHosts\awawausb_native_stub
```

The registry value should be the full path to the manifest `.json` file.

#### Quick Linux user-local setup script

```bash
#!/usr/bin/env bash
STUB_PATH="$(pwd)/native-stub/target/release/awawausb-native-stub"
MANIFEST_DIR="$HOME/.mozilla/native-messaging-hosts"
mkdir -p "$MANIFEST_DIR"

cat > "$MANIFEST_DIR/awawausb_native_stub.json" <<EOF
{
  "name": "awawausb_native_stub",
  "description": "Allows WebUSB extension to access USB devices",
  "path": "$STUB_PATH",
  "type": "stdio",
  "allowed_extensions": ["awawausb@arcanenibble.com"]
}
EOF

echo "Native manifest written to $MANIFEST_DIR/awawausb_native_stub.json"
```

#### Quick macOS user-local setup

```bash
#!/usr/bin/env bash
STUB_PATH="$(pwd)/native-stub/target/release/awawausb-native-stub"
MANIFEST_DIR="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
mkdir -p "$MANIFEST_DIR"

cat > "$MANIFEST_DIR/awawausb_native_stub.json" <<EOF
{
  "name": "awawausb_native_stub",
  "description": "Allows WebUSB extension to access USB devices",
  "path": "$STUB_PATH",
  "type": "stdio",
  "allowed_extensions": ["awawausb@arcanenibble.com"]
}
EOF
```

#### Windows PowerShell setup

```powershell
$stubPath = "C:\path\to\awawausb-native-stub.exe"
$manifestPath = "C:\ProgramData\Mozilla\awawausb_native_stub.json"

$manifest = @{
    name = "awawausb_native_stub"
    description = "Allows WebUSB extension to access USB devices"
    path = $stubPath
    type = "stdio"
    allowed_extensions = @("awawausb@arcanenibble.com")
} | ConvertTo-Json

Set-Content -Path $manifestPath -Value $manifest

# Register for current user
New-Item -Path "HKCU:\SOFTWARE\Mozilla\NativeMessagingHosts\awawausb_native_stub" -Force
Set-ItemProperty -Path "HKCU:\SOFTWARE\Mozilla\NativeMessagingHosts\awawausb_native_stub" `
    -Name "(Default)" -Value $manifestPath
```

## Using WebUSB in Web Pages

Once installed, `navigator.usb` is available. Usage is identical to Chrome's WebUSB API:

```javascript
// Request a device (requires user gesture)
async function connectDevice() {
  try {
    const device = await navigator.usb.requestDevice({
      filters: [
        { vendorId: 0x1234 },                          // by vendor
        { vendorId: 0x5678, productId: 0x9abc },       // by vendor+product
        { classCode: 0xff }                             // by class
      ]
    });

    await device.open();
    await device.selectConfiguration(1);
    await device.claimInterface(0);

    // Send data
    const data = new Uint8Array([0x01, 0x02, 0x03]);
    await device.transferOut(1, data);

    // Receive data
    const result = await device.transferIn(1, 64);
    console.log('Received:', new Uint8Array(result.data.buffer));

    await device.close();
  } catch (err) {
    console.error('USB error:', err);
  }
}

// List previously-authorized devices
async function listDevices() {
  const devices = await navigator.usb.getDevices();
  devices.forEach(d => {
    console.log(`${d.manufacturerName} ${d.productName} (${d.vendorId}:${d.productId})`);
  });
}

// Watch for connect/disconnect
navigator.usb.addEventListener('connect', e => {
  console.log('Device connected:', e.device);
});
navigator.usb.addEventListener('disconnect', e => {
  console.log('Device disconnected:', e.device);
});
```

> **Note**: The WebUSB API is only available on the main page — not in Web Workers.

## System Requirements

| OS | Requirement |
|----|-------------|
| macOS | 10.15+; macOS 12 recommended |
| Windows | Windows 10+ (WinUSB driver required for target device) |
| Linux | Kernel 4.8+; udev daemon; `/dev` and `/sys` mounted |

### Linux udev Rules (if device access is denied)

```
# /etc/udev/rules.d/99-webusb.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="5678", MODE="0666", GROUP="plugdev"
```

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Windows: Switching to WinUSB Driver

If a device isn't listed, it may not use WinUSB. Use [Zadig](https://zadig.akeo.ie/):
1. Open Zadig, select the device
2. Choose "WinUSB" as the driver
3. Click "Replace Driver"

> ⚠️ Switching to WinUSB removes the device from other Windows subsystems (e.g., a printer will no longer appear as a printer).

## Troubleshooting

### Check Extension Debugging Page

Click the awawausb toolbar button (under the Extensions icon) → use "List devices" to see all USB devices the extension can see.

- Device listed but page can't use it → likely a permissions/origin issue in the web page.
- Device NOT listed → OS-level configuration problem (driver, udev rules, permissions).

### Native Stub Not Found

Symptoms: extension toolbar shows an error; no devices listed.

1. Verify the manifest file exists at the correct path for your OS.
2. Verify `"path"` in the manifest points to the actual binary.
3. Verify the binary is executable: `chmod +x /path/to/awawausb-native-stub`
4. Check Firefox's browser console (`about:debugging` → inspect extension) for native messaging errors.

### Linux: Device Not Detected

```bash
# Verify udev is running and broadcasting on NETLINK_KOBJECT_UEVENT group 2
udevadm monitor --udev --subsystem-match=usb

# Check kernel version
uname -r  # must be >= 4.8
```

### Build Fails on Linux (musl)

```bash
# Install musl target
rustup target add x86_64-unknown-linux-musl
# Install musl toolchain (Debian/Ubuntu)
sudo apt install musl-tools
cargo build --release --target x86_64-unknown-linux-musl
```

### Shared Home Directory / Roaming Profiles

The native manifest uses absolute paths, which breaks when the same home directory is used across machines with different CPU architectures. Workarounds:
- Use a wrapper script at a fixed path that `exec`s the correct binary based on `uname -m`.
- Use separate per-machine manifest directories if your OS supports it.

## Known Limitations

- No Web Worker support (API only on main page).
- No Android support (no native messaging on Android Firefox).
- Windows requires WinUSB driver on target device.
- Linux requires udev-compatible daemon for hotplug detection.
