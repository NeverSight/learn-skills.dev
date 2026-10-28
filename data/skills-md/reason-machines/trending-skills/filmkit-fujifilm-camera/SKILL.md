---
name: filmkit-fujifilm-camera
description: Browser-based preset manager and RAW converter for Fujifilm X-series cameras using WebUSB and PTP protocol
triggers:
  - "work with filmkit"
  - "fujifilm camera presets"
  - "manage fuji camera profiles"
  - "webusb fujifilm connection"
  - "fujifilm raw conversion browser"
  - "filmkit preset management"
  - "fuji x-series ptp protocol"
  - "filmkit camera integration"
---

# FilmKit Fujifilm Camera Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

FilmKit is a browser-based, zero-install preset manager and RAW converter for Fujifilm X-series cameras. It uses WebUSB to communicate via PTP (Picture Transfer Protocol) — the same protocol as Fujifilm X RAW STUDIO — so the camera's own image processor handles RAW-to-JPEG conversion. It runs entirely client-side (hosted on GitHub Pages) and supports desktop and Android.

---

## What FilmKit Does

- **Preset Management**: Read, edit, and write custom film simulation presets directly on-camera (slots D18E–D1A5 via PTP `GetDevicePropValue` / `SetDevicePropValue`)
- **Local Preset Library**: Save presets locally, drag-and-drop between camera and local storage
- **RAW Conversion & Live Preview**: Send RAF files to the camera, receive full-quality JPEGs back
- **Preset Detection**: Loading a RAF file auto-detects which preset was used to shoot it
- **Import/Export**: Presets as files, links, or text paste
- **Mobile Support**: Works on Android via Chrome's WebUSB support

---

## Requirements

- **Chromium-based browser** (Google Chrome, Edge, Brave) on desktop or Android — WebUSB is required
- **Fujifilm X-series camera** connected via USB (tested on X100VI; likely works on X-T5, X-H2, X-T30, etc.)
- **Linux udev rule** (if running Chrome in Flatpak):

```bash
# /etc/udev/rules.d/99-fujifilm.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="04cb", MODE="0666"
```

Reload rules after adding:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

---

## Installation / Setup (Development)

FilmKit is a static TypeScript app. To run locally:

```bash
git clone https://github.com/eggricesoy/filmkit.git
cd filmkit
npm install
npm run dev
```

Build for production:
```bash
npm run build
```

The built output is a static site — no server required. Open in Chrome at `http://localhost:5173` (or wherever Vite serves it).

---

## Architecture Overview

### PTP over WebUSB

FilmKit speaks PTP (Picture Transfer Protocol) directly over USB bulk transfers. Key operations:

| PTP Operation | Purpose |
|---|---|
| `GetDevicePropValue` | Read a camera preset property |
| `SetDevicePropValue` | Write a camera preset property |
| `InitiateOpenCapture` | Start RAW conversion session |
| `SendObject` | Send RAF file to camera |
| `GetObject` | Retrieve converted JPEG from camera |

### Preset Property Codes

Fujifilm X-series cameras expose film simulation parameters as device properties in the range `0xD18E`–`0xD1A5`:

```typescript
// Example property codes (from QUICK_REFERENCE.md)
const PROP_FILM_SIMULATION = 0xD18E;
const PROP_GRAIN_EFFECT     = 0xD18F;
const PROP_COLOR_CHROME     = 0xD190;
const PROP_WHITE_BALANCE    = 0xD191;
const PROP_COLOR_TEMP       = 0xD192;
const PROP_DYNAMIC_RANGE    = 0xD193;
const PROP_HIGHLIGHT_TONE   = 0xD194;
const PROP_SHADOW_TONE      = 0xD195;
const PROP_COLOR            = 0xD196;
const PROP_SHARPNESS        = 0xD197;
const PROP_HIGH_ISO_NR      = 0xD198; // Non-linear encoding!
const PROP_CLARITY          = 0xD199;
```

### Native Profile Format

The camera's native `d185` profile is **625 bytes** and uses different field indices/encoding from RAF file metadata. FilmKit uses a **patch-based approach**:

```typescript
// Conceptual patch approach
function applyPresetPatch(baseProfile: Uint8Array, changes: PresetChanges): Uint8Array {
  // Copy base profile byte-for-byte
  const patched = new Uint8Array(baseProfile);
  
  // Only overwrite fields the user changed
  // This preserves EXIF sentinel values in unchanged fields
  for (const [fieldIndex, encodedValue] of Object.entries(changes)) {
    writeFieldToProfile(patched, parseInt(fieldIndex), encodedValue);
  }
  
  return patched;
}
```

---

## Key Code Patterns

### WebUSB Connection

```typescript
// Request access to the Fujifilm camera
async function connectCamera(): Promise<USBDevice> {
  const device = await navigator.usb.requestDevice({
    filters: [{ vendorId: 0x04CB }] // Fujifilm vendor ID
  });
  
  await device.open();
  await device.selectConfiguration(1);
  await device.claimInterface(0);
  
  return device;
}
```

### Sending a PTP Command

```typescript
// PTP command packet structure
function buildPTPCommand(
  operationCode: number,
  transactionId: number,
  params: number[] = []
): ArrayBuffer {
  const paramCount = params.length;
  const length = 12 + paramCount * 4;
  const buffer = new ArrayBuffer(length);
  const view = new DataView(buffer);
  
  view.setUint32(0, length, true);        // Length
  view.setUint16(4, 0x0001, true);        // Type: Command
  view.setUint16(6, operationCode, true); // Operation code
  view.setUint32(8, transactionId, true); // Transaction ID
  
  params.forEach((p, i) => {
    view.setUint32(12 + i * 4, p, true);
  });
  
  return buffer;
}

// Send a PTP operation and read response
async function ptpTransaction(
  device: USBDevice,
  operationCode: number,
  transactionId: number,
  params: number[] = [],
  outData?: ArrayBuffer
): Promise<{ responseCode: number; data?: ArrayBuffer }> {
  const endpointOut = 0x02; // Bulk OUT
  const endpointIn  = 0x81; // Bulk IN
  
  // Send command
  const cmd = buildPTPCommand(operationCode, transactionId, params);
  await device.transferOut(endpointOut, cmd);
  
  // Send data phase if present
  if (outData) {
    await device.transferOut(endpointOut, outData);
  }
  
  // Read data response (if expected)
  const dataResult = await device.transferIn(endpointIn, 512);
  
  // Read response packet
  const respResult = await device.transferIn(endpointIn, 32);
  const respView = new DataView(respResult.data!.buffer);
  const responseCode = respView.getUint16(6, true);
  
  return { responseCode, data: dataResult.data?.buffer };
}
```

### Reading a Preset Property

```typescript
async function getDevicePropValue(
  device: USBDevice,
  propCode: number,
  txId: number
): Promise<DataView> {
  const PTP_OP_GET_DEVICE_PROP_VALUE = 0x1015;
  
  const { data } = await ptpTransaction(
    device,
    PTP_OP_GET_DEVICE_PROP_VALUE,
    txId,
    [propCode]
  );
  
  if (!data) throw new Error(`No data for prop 0x${propCode.toString(16)}`);
  
  // PTP data container: 12-byte header, then payload
  return new DataView(data, 12);
}

// Example: read film simulation
const filmSimView = await getDevicePropValue(device, 0xD18E, txId++);
const filmSimValue = filmSimView.getUint16(0, true);
console.log('Film simulation code:', filmSimValue);
```

### Writing a Preset Property

```typescript
async function setDevicePropValue(
  device: USBDevice,
  propCode: number,
  value: number,
  byteSize: 1 | 2 | 4,
  txId: number
): Promise<void> {
  const PTP_OP_SET_DEVICE_PROP_VALUE = 0x1016;
  
  // Build data container
  const dataLength = 12 + byteSize;
  const dataBuffer = new ArrayBuffer(dataLength);
  const view = new DataView(dataBuffer);
  
  view.setUint32(0, dataLength, true); // Length
  view.setUint16(4, 0x0002, true);     // Type: Data
  view.setUint16(6, PTP_OP_SET_DEVICE_PROP_VALUE, true);
  view.setUint32(8, txId, true);
  
  if (byteSize === 1) view.setUint8(12, value);
  else if (byteSize === 2) view.setUint16(12, value, true);
  else if (byteSize === 4) view.setUint32(12, value, true);
  
  await ptpTransaction(
    device,
    PTP_OP_SET_DEVICE_PROP_VALUE,
    txId,
    [propCode],
    dataBuffer
  );
}

// Example: set White Balance to Color Temperature mode
await setDevicePropValue(device, 0xD191, 0x0012, 2, txId++);
// Now safe to set Color Temperature value
await setDevicePropValue(device, 0xD192, 4500, 2, txId++);
```

### HighIsoNR Special Encoding

HighIsoNR uses a **non-linear proprietary encoding** — do not write raw values directly:

```typescript
// HighIsoNR encoding map (reverse-engineered via Wireshark)
const HIGH_ISO_NR_ENCODE: Record<number, number> = {
  [-4]: 0x00,
  [-3]: 0x01,
  [-2]: 0x02,
  [-1]: 0x03,
  [0]:  0x04,
  [1]:  0x08,
  [2]:  0x0C,
  [3]:  0x10,
  [4]:  0x14,
};

function encodeHighIsoNR(userValue: number): number {
  const encoded = HIGH_ISO_NR_ENCODE[userValue];
  if (encoded === undefined) throw new Error(`Invalid HighIsoNR value: ${userValue}`);
  return encoded;
}

// Usage
await setDevicePropValue(device, 0xD198, encodeHighIsoNR(2), 1, txId++);
```

### Conditional Writes (Monochrome Film Simulations)

Monochrome film simulations reject Color property writes — guard against this:

```typescript
const MONOCHROME_SIMULATIONS = new Set([
  0x0009, // ACROS
  0x000A, // ACROS+Ye
  0x000B, // ACROS+R
  0x000C, // ACROS+G
  0x0012, // Monochrome
  0x0013, // Monochrome+Ye
  0x0014, // Monochrome+R
  0x0015, // Monochrome+G
  0x001A, // Eterna Cinema BW
]);

async function writePreset(device: USBDevice, preset: Preset, txId: number): Promise<number> {
  const isMonochrome = MONOCHROME_SIMULATIONS.has(preset.filmSimulation);
  
  await setDevicePropValue(device, 0xD18E, preset.filmSimulation, 2, txId++);
  
  if (!isMonochrome) {
    await setDevicePropValue(device, 0xD196, preset.color, 2, txId++);
  }
  
  await setDevicePropValue(device, 0xD198, encodeHighIsoNR(preset.highIsoNR), 1, txId++);
  // ... write other properties
  
  return txId;
}
```

### RAW Conversion Flow

```typescript
async function convertRAW(
  device: USBDevice,
  rafData: ArrayBuffer,
  preset: Preset,
  txId: number
): Promise<ArrayBuffer> {
  // 1. Write preset properties to camera
  txId = await writePreset(device, preset, txId);
  
  // 2. Initiate open capture / conversion session
  await ptpTransaction(device, 0x101C, txId++); // InitiateOpenCapture
  
  // 3. Send the RAF file
  const sendObjectOp = 0x100D;
  await ptpTransaction(device, sendObjectOp, txId++, [], rafData);
  
  // 4. Poll for completion and get JPEG back
  const getObjectOp = 0x1009;
  const { data: jpegData } = await ptpTransaction(device, getObjectOp, txId++);
  
  if (!jpegData) throw new Error('No JPEG returned from camera');
  return jpegData;
}
```

---

## Preset Import/Export Format

Presets are exported as structured data (JSON or encoded strings). When importing:

```typescript
interface FilmKitPreset {
  name: string;
  filmSimulation: number;
  grainEffect: number;
  colorChrome: number;
  whiteBalance: number;
  colorTemperature?: number; // Only used when WB = Color Temp mode (0x0012)
  dynamicRange: number;
  highlightTone: number;
  shadowTone: number;
  color: number;
  sharpness: number;
  highIsoNR: number;       // User-facing value (-4 to +4), encode before writing
  clarity: number;
}

// Export preset as shareable link
function exportPresetAsLink(preset: FilmKitPreset): string {
  const encoded = btoa(JSON.stringify(preset));
  return `https://filmkit.eggrice.soy/?preset=${encoded}`;
}

// Import preset from link/text
function importPreset(input: string): FilmKitPreset {
  // Handle URL with ?preset= param
  try {
    const url = new URL(input);
    const param = url.searchParams.get('preset');
    if (param) return JSON.parse(atob(param));
  } catch {}
  
  // Handle raw base64 or JSON
  try { return JSON.parse(atob(input)); } catch {}
  try { return JSON.parse(input); } catch {}
  
  throw new Error('Invalid preset format');
}
```

---

## Capturing USB Traffic for New Camera Support

To help add support for a new Fujifilm X-series camera:

1. Install [Wireshark](https://www.wireshark.org/) with USBPcap
2. Capture on USB bus: `USBPcap1:\\.\USBPcap1`
3. Filter: `usb.transfer_type == 0x02` (bulk transfers = PTP traffic)
4. Perform these actions in X RAW STUDIO while capturing:
   - Profile read (connect and let app read camera state)
   - Preset save (change all preset values, save to a slot)
   - RAW conversion (load RAF, convert with a preset)
5. Save each capture as `.pcapng`
6. Open a GitHub issue with: camera model, firmware version, all three `.pcapng` files, and the parameter values used

---

## Troubleshooting

### WebUSB Not Available
- Must use Chrome or Chromium-based browser (Firefox does not support WebUSB)
- On Android, use Chrome (not Firefox for Android)
- Check `chrome://flags` — ensure "Disable WebUSB" is not enabled

### Camera Not Detected
- Ensure the camera is in USB mode (MTP or PTP, not Mass Storage)
- On Linux without Flatpak: check that your user is in the `plugdev` group: `sudo usermod -aG plugdev $USER`
- On Linux with Flatpak Chrome: add udev rule for vendor `04cb` and reload

### Permission Denied on Linux
```bash
# Check if udev rule is applied
lsusb | grep -i fuji
# Should show Fujifilm device

# Verify permissions
ls -la /dev/bus/usb/$(lsusb | grep -i fuji | awk '{print $2"/"$4}' | tr -d ':')
# Should show rw-rw-rw- or similar open permissions
```

### PTP Transaction Errors
- Ensure no other app (X RAW STUDIO, Capture One, etc.) is connected to the camera simultaneously
- Only one WebUSB consumer can hold the interface at a time
- Disconnect and reconnect the camera if the interface gets stuck

### Preset Write Rejected
- Writing `Color` property on a monochrome film simulation will be rejected — this is expected behavior (see conditional writes above)
- Writing `Color Temperature` requires WB mode set to `0x0012` first
- `HighIsoNR` must use the non-linear encoded value, not the raw user-facing value

### Debug Log
In the FilmKit UI, scroll to the **Debug** section at the bottom of the right sidebar → click **Copy Log** → paste into a GitHub issue for bug reports.

---

## Key Links

- **Live App**: https://filmkit.eggrice.soy
- **Protocol Reference**: [`QUICK_REFERENCE.md`](https://github.com/eggricesoy/filmkit/blob/main/QUICK_REFERENCE.md)
- **Related Projects**: [rawji](https://github.com/pinpox/rawji), [fudge](https://github.com/petabyt/fudge), [libgphoto2](http://www.gphoto.org/)
- **Fuji X Weekly Presets**: https://fujixweekly.com/
