---
name: readme-generator
description: Auto-generates professional README.md files for Arduino/ESP32/RP2040 projects following open-source best practices. Use when user wants to document their project for GitHub, needs help writing a README, or says "make my project shareable". Follows awesome-readme standards with sections for Overview, Hardware, Software, Setup, Usage, Troubleshooting, and Contributing.
---

# README Generator

Creates professional, beginner-friendly README files for maker projects.

## Resources

This skill includes bundled tools:

- **scripts/generate_readme.py** - Full README generator with wiring diagrams and templates

## Quick Start

**Interactive mode:**
```bash
uv run --no-project scripts/generate_readme.py --interactive
```

**Quick generation:**
```bash
uv run --no-project scripts/generate_readme.py --project "Weather Station" --board "ESP32" --output README.md
```

**Scan existing project:**
```bash
uv run --no-project scripts/generate_readme.py --scan /path/to/arduino/project --output README.md
```

## When to Use
- "Help me document this project"
- "I want to share this on GitHub"
- "Write a README for my project"
- User has working project, needs documentation
- Before publishing to GitHub/Instructables

## Information Gathering

### Ask User For:
```
1. Project name and one-line description
2. What problem does it solve / why did you build it?
3. Main features (3-5 bullet points)
4. Hardware components used
5. Software libraries required
6. Any photos/videos/GIFs available?
7. License preference (MIT recommended for open source)
8. Target audience (beginners/intermediate/advanced)
```

### Auto-Extract From Code:
- Pin assignments from config.h
- Library includes
- WiFi/Bluetooth features
- Sensor types

---

## README Template

Generate using this structure (based on awesome-readme best practices):

```markdown
# 🎯 [Project Name]

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Platform](https://img.shields.io/badge/platform-ESP32-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> One-line description of what this project does and why it's useful.

![Project Photo/GIF](images/project-demo.gif)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Components](#hardware-components)
- [Wiring Diagram](#wiring-diagram)
- [Software Dependencies](#software-dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🔍 Overview

[2-3 paragraphs explaining:]
- What the project does
- Why you built it / what problem it solves
- Who it's for (target audience)

### Demo

[Embed video or GIF showing project in action]

## ✨ Features

- ✅ Feature 1 - brief description
- ✅ Feature 2 - brief description
- ✅ Feature 3 - brief description
- 🚧 Planned: Feature 4 (coming soon)

## 🔧 Hardware Components

| Component | Quantity | Purpose | Notes |
|-----------|----------|---------|-------|
| [MCU Board] | 1 | Main controller | [version/variant] |
| [Sensor 1] | 1 | [function] | [I2C address, etc.] |
| [Display] | 1 | User interface | [resolution] |
| ... | ... | ... | ... |

**Estimated Cost:** $XX-XX

### Where to Buy

- [Component 1](link) - Amazon/AliExpress
- [Component 2](link) - Adafruit/SparkFun

## 📐 Wiring Diagram

![Wiring Diagram](images/wiring-diagram.png)

### Pin Connections

| MCU Pin | Component | Pin | Function |
|---------|-----------|-----|----------|
| GPIO21 | BME280 | SDA | I2C Data |
| GPIO22 | BME280 | SCL | I2C Clock |
| GPIO4 | LED | Anode | Status indicator |
| ... | ... | ... | ... |

## 💻 Software Dependencies

### Required Software

- [Arduino IDE](https://www.arduino.cc/en/software) (v2.0+) or [PlatformIO](https://platformio.org/)
- [Board package] - [installation link]

### Required Libraries

| Library | Version | Purpose | Install via |
|---------|---------|---------|-------------|
| [Library1] | >=1.0.0 | [function] | Library Manager |
| [Library2] | >=2.3.0 | [function] | Library Manager |
| ... | ... | ... | ... |

## 📦 Installation

### Option 1: Arduino IDE

1. **Install Arduino IDE**
   - Download from [arduino.cc](https://www.arduino.cc/en/software)
   
2. **Add Board Support** (if using ESP32/RP2040)
   ```
   File → Preferences → Additional Board Manager URLs:
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
   Then: Tools → Board → Boards Manager → Search "[board]" → Install

3. **Install Required Libraries**
   - Sketch → Include Library → Manage Libraries
   - Search and install each library from the table above

4. **Clone or Download This Repository**
   ```bash
   git clone https://github.com/[username]/[repo-name].git
   ```
   Or download ZIP and extract

5. **Open the Project**
   - Open `[project-name].ino` in Arduino IDE

### Option 2: PlatformIO (Recommended for Advanced Users)

1. Install [VS Code](https://code.visualstudio.com/) + [PlatformIO extension](https://platformio.org/install/ide?install=vscode)

2. Clone and open:
   ```bash
   git clone https://github.com/[username]/[repo-name].git
   cd [repo-name]
   code .
   ```

3. PlatformIO will automatically install dependencies from `platformio.ini`

## ⚙️ Configuration

Before uploading, customize `config.h`:

```cpp
// === NETWORK SETTINGS ===
#define WIFI_SSID     "your-wifi-name"
#define WIFI_PASSWORD "your-wifi-password"

// === HARDWARE PINS ===
#define LED_PIN       4
#define SENSOR_SDA    21
#define SENSOR_SCL    22

// === FEATURE FLAGS ===
#define ENABLE_OLED   true
#define ENABLE_WIFI   true
#define DEBUG_MODE    true
```

### Environment-Specific Settings

| Setting | Development | Production |
|---------|-------------|------------|
| DEBUG_MODE | true | false |
| SERIAL_BAUD | 115200 | 9600 |
| SLEEP_INTERVAL | 10s | 300s |

## 🚀 Usage

### Basic Operation

1. **Power On** - Connect USB or battery
2. **Wait for Boot** - Status LED blinks during initialization
3. **[Normal Operation]** - Description of what happens

### LED Status Indicators

| LED State | Meaning |
|-----------|---------|
| Solid Green | Normal operation |
| Blinking Blue | WiFi connecting |
| Red Flash | Error (check serial) |

### Serial Monitor

Open Serial Monitor at 115200 baud to see:
```
[BOOT] Project Name v1.0.0
[INFO] Initializing sensors...
[OK] BME280 found at 0x76
[INFO] Connecting to WiFi...
[OK] Connected: 192.168.1.100
[DATA] Temp: 23.5°C, Humidity: 45%
```

### Web Interface (if applicable)

Navigate to `http://[device-ip]` to access:
- Real-time sensor readings
- Configuration panel
- Data export

## ❓ Troubleshooting

### Common Issues

<details>
<summary><b>Upload fails: "Failed to connect"</b></summary>

**ESP32:** Hold BOOT button while clicking Upload, release when "Connecting..." appears.

**Arduino:** Check correct COM port selected in Tools → Port.
</details>

<details>
<summary><b>Sensor not detected</b></summary>

1. Check wiring (SDA/SCL not swapped?)
2. Run I2C scanner sketch to verify address
3. Add pull-up resistors (4.7kΩ) if not on module
4. Check voltage compatibility (3.3V vs 5V)
</details>

<details>
<summary><b>WiFi won't connect</b></summary>

1. Verify SSID/password in config.h (case-sensitive!)
2. 2.4GHz only (ESP32 doesn't support 5GHz)
3. Check router isn't blocking new devices
4. Try moving closer to router
</details>

<details>
<summary><b>Random resets</b></summary>

1. Power supply too weak - use 500mA+ source
2. Add 100µF capacitor near MCU
3. Check for short circuits
4. Disable brownout detector (ESP32)
</details>

### Still Stuck?

1. Check [Issues](https://github.com/[username]/[repo]/issues) for similar problems
2. Open a new issue with:
   - Hardware setup (board, sensors)
   - Error messages (full serial output)
   - Steps to reproduce

## 🤝 Contributing

Contributions are welcome! Here's how:

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include serial output and hardware details

### Suggesting Features

1. Open an issue with `[Feature Request]` prefix
2. Describe use case and expected behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Use meaningful variable names
- Comment complex logic
- Follow existing formatting
- Test on actual hardware before PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) [year] [author]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- [Library/Project] - for [what it provides]
- [Person/Tutorial] - inspiration/guidance
- [Community] - testing and feedback

## 📬 Contact

**[Your Name]** - [@twitter_handle](https://twitter.com/handle) - email@example.com

Project Link: [https://github.com/[username]/[repo-name]](https://github.com/[username]/[repo-name])

---

⭐ If this project helped you, please give it a star!
```

---

## Section Guidelines

### Good vs Bad Examples

**Project Description:**
```
❌ Bad: "An Arduino project with sensors"
✅ Good: "Battery-powered environmental monitor that tracks temperature, 
         humidity, and air quality, sending alerts when thresholds are exceeded"
```

**Features:**
```
❌ Bad: "Has WiFi"
✅ Good: "📶 WiFi connectivity with automatic reconnection and OTA updates"
```

**Installation Steps:**
```
❌ Bad: "Install the libraries and upload"
✅ Good: Step-by-step with screenshots, version numbers, exact menu paths
```

### Visual Assets

**Recommended:**
- Project photo (hero image)
- Wiring diagram (Fritzing or hand-drawn)
- Demo GIF (< 5MB, 10-15 seconds)
- Schematic (KiCad export)

**Creating GIFs:**
- Use ScreenToGif (Windows) or Peek (Linux)
- Optimize with ezgif.com
- Keep under 5MB for GitHub

### Badges

```markdown
<!-- Status badges -->
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- Platform badges -->
![Arduino](https://img.shields.io/badge/platform-Arduino-00979D?logo=arduino)
![ESP32](https://img.shields.io/badge/platform-ESP32-blue)
![Raspberry Pi](https://img.shields.io/badge/platform-RPi_Pico-C51A4A)

<!-- Social badges -->
![GitHub stars](https://img.shields.io/github/stars/user/repo)
![GitHub forks](https://img.shields.io/github/forks/user/repo)
```

---

## File Structure Recommendation

```
project-name/
├── README.md              # Main documentation
├── LICENSE                # MIT license file
├── .gitignore            # Ignore build files
├── src/
│   ├── main.ino          # Main sketch
│   └── config.h          # User configuration
├── lib/                  # Local libraries (optional)
├── docs/
│   ├── WIRING.md         # Detailed wiring guide
│   ├── API.md            # API documentation (if applicable)
│   └── CHANGELOG.md      # Version history
├── images/
│   ├── project-photo.jpg
│   ├── wiring-diagram.png
│   └── demo.gif
├── hardware/             # PCB/enclosure files (optional)
│   ├── schematic.pdf
│   └── enclosure.stl
└── examples/             # Additional example sketches
    └── basic/
```

---

## Quick README Checklist

Before publishing, verify:

```
□ Project name is clear and memorable
□ One-line description explains the "what" and "why"
□ Hero image/GIF shows project in action
□ All hardware components listed with links
□ Wiring diagram included
□ All libraries listed with versions
□ Step-by-step installation instructions
□ Configuration section explains all settings
□ Usage section shows expected output
□ Troubleshooting covers common issues
□ License file present
□ Contact information included
□ No broken links
□ Spelling/grammar checked
```
