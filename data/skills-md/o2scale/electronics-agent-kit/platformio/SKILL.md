---
name: platformio
description: PlatformIO embedded development platform expertise. Project setup, configuration, building, debugging, and library management for Arduino, ESP-IDF, STM32, and more.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# PlatformIO Reference

> Complete reference for PlatformIO embedded development.

---

## 1. Installation

```bash
# Install via pip
pip install platformio

# Or via installer script
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py -o get-platformio.py
python3 get-platformio.py
```

---

## 2. Project Structure

```
project/
├── platformio.ini        # Project configuration
├── src/
│   └── main.cpp         # Main source file
├── include/             # Header files
├── lib/                 # Project-specific libraries
├── test/                # Unit tests
└── .pio/                # Build output (gitignored)
```

---

## 3. Configuration (platformio.ini)

### Basic Structure

```ini
; Global options
[platformio]
default_envs = esp32dev
src_dir = src
include_dir = include

; Environment definition
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

### Common Platforms

| Platform | Board Examples | Frameworks |
|----------|----------------|------------|
| `espressif32` | esp32dev, esp32-s3-devkitc-1 | arduino, espidf |
| `espressif8266` | esp12e, d1_mini | arduino |
| `ststm32` | nucleo_f446re, bluepill_f103c8 | arduino, stm32cube |
| `raspberrypi` | pico | arduino |
| `atmelavr` | uno, nanoatmega328 | arduino |

### ESP32 Examples

```ini
; ESP32 with Arduino
[env:esp32-arduino]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
upload_speed = 921600
lib_deps = 
    bblanchon/ArduinoJson@^7.0.0

; ESP32-S3 with PSRAM
[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
board_build.mcu = esp32s3
board_build.f_cpu = 240000000L
build_flags = 
    -DBOARD_HAS_PSRAM
    -mfix-esp32-psram-cache-issue

; ESP32 with ESP-IDF
[env:esp32-idf]
platform = espressif32
board = esp32dev
framework = espidf
monitor_speed = 115200
board_build.partitions = partitions.csv
```

### STM32 Examples

```ini
; Nucleo F446RE
[env:nucleo_f446re]
platform = ststm32
board = nucleo_f446re
framework = arduino
upload_protocol = stlink

; Blue Pill
[env:bluepill]
platform = ststm32
board = bluepill_f103c8
framework = arduino
upload_protocol = stlink
```

### RP2040 Examples

```ini
; Raspberry Pi Pico
[env:pico]
platform = raspberrypi
board = pico
framework = arduino

; Pico W with WiFi
[env:picow]
platform = raspberrypi
board = rpipicow
framework = arduino
```

---

## 4. CLI Commands

### Building

```bash
# Build default environment
pio run

# Build specific environment
pio run -e esp32dev

# Build with verbose output
pio run -v

# Clean build
pio run -t clean

# Full clean (remove .pio)
pio run -t cleanall
```

### Uploading

```bash
# Build and upload
pio run -t upload

# Upload to specific environment
pio run -e esp32dev -t upload

# Upload using specific port
pio run -t upload --upload-port /dev/ttyUSB0
```

### Serial Monitor

```bash
# Start monitor
pio device monitor

# With specific baud rate
pio device monitor -b 115200

# With specific port
pio device monitor -p /dev/ttyUSB0

# Monitor with filters
pio device monitor --filter esp32_exception_decoder
```

### Testing

```bash
# Run all tests
pio test

# Run tests for specific environment
pio test -e native

# Run specific test
pio test -f test_foo

# Verbose test output
pio test -v
```

### Device Management

```bash
# List connected devices
pio device list

# List available boards
pio boards

# Search boards
pio boards esp32
```

### Library Management

```bash
# Search libraries
pio pkg search "json"

# Install library
pio pkg install --library "bblanchon/ArduinoJson"

# Install specific version
pio pkg install --library "bblanchon/ArduinoJson@^7.0.0"

# List installed libraries
pio pkg list

# Update libraries
pio pkg update
```

---

## 5. Build Flags

### Common Flags

```ini
build_flags = 
    -DDEBUG                    ; Define DEBUG macro
    -DVERSION=\"1.0.0\"        ; String define (escaped quotes)
    -I include/extra           ; Additional include path
    -Wall                      ; Enable all warnings
    -Wextra                    ; Extra warnings
    -O2                        ; Optimization level
```

### ESP32-Specific

```ini
build_flags = 
    -DCORE_DEBUG_LEVEL=3       ; Debug output level (0-5)
    -DBOARD_HAS_PSRAM          ; Enable PSRAM
    -DCONFIG_ASYNC_TCP_RUNNING_CORE=1
```

### Conditional Flags

```ini
build_flags = 
    ${env.build_flags}         ; Inherit from parent
    $BUILD_FLAGS               ; From environment variable
```

---

## 6. Library Dependencies

### Syntax

```ini
lib_deps = 
    ; Library by owner/name
    bblanchon/ArduinoJson@^7.0.0
    
    ; Library by name only
    Adafruit Unified Sensor
    
    ; GitHub repository
    https://github.com/me/mylib.git
    
    ; Specific branch/tag
    https://github.com/me/mylib.git#develop
    
    ; Local library
    file:///path/to/library
```

### Version Constraints

```ini
lib_deps = 
    library@1.2.3              ; Exact version
    library@^1.2.3             ; Compatible (>=1.2.3 <2.0.0)
    library@~1.2.3             ; Approximate (>=1.2.3 <1.3.0)
    library@>=1.0.0            ; Minimum version
```

---

## 7. Multiple Environments

### Shared Configuration

```ini
[env]
; Shared across all environments
monitor_speed = 115200
lib_deps = 
    bblanchon/ArduinoJson@^7.0.0

[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
build_flags = 
    -DBOARD_HAS_PSRAM
```

### Platform-Specific Overrides

```ini
[env:debug]
extends = env:esp32dev
build_type = debug
build_flags = 
    -DDEBUG=1
    -g3

[env:release]
extends = env:esp32dev
build_type = release
build_flags = 
    -DNDEBUG
    -O2
```

---

## 8. Testing

### Test Structure

```
test/
├── test_main.cpp           ; Native tests
├── test_embedded/
│   └── test_gpio.cpp      ; On-device tests
└── unity.h                 ; Unity test framework (included)
```

### Test File

```cpp
#include <unity.h>

void setUp(void) {
    // Runs before each test
}

void tearDown(void) {
    // Runs after each test
}

void test_addition(void) {
    TEST_ASSERT_EQUAL(4, 2 + 2);
}

void test_string(void) {
    TEST_ASSERT_EQUAL_STRING("hello", "hello");
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_addition);
    RUN_TEST(test_string);
    UNITY_END();
}
```

### Native Testing

```ini
[env:native]
platform = native
test_framework = unity
```

---

## 9. Debugging

### Configuration

```ini
[env:debug]
platform = espressif32
board = esp32dev
framework = arduino
debug_tool = esp-prog
debug_init_break = tbreak setup
```

### Debug Commands

```bash
# Start debugger
pio debug

# Start with GDB
pio debug --interface=gdb
```

---

## 10. Custom Scripts

### Extra Scripts

```ini
[env:esp32dev]
extra_scripts = 
    pre:scripts/pre_build.py
    post:scripts/post_build.py
```

### Script Example

```python
# scripts/pre_build.py
Import("env")

def before_build(source, target, env):
    print("Before build!")

env.AddPreAction("buildprog", before_build)
```

---

## 11. Common Issues

| Issue | Solution |
|-------|----------|
| Upload failed | Check port, try lower upload_speed |
| Library not found | Use full `owner/name` format |
| Build error | Clean with `pio run -t clean` |
| Wrong board | Verify board ID with `pio boards` |

---

> **Note:** PlatformIO supports 1000+ boards. Use `pio boards <search>` to find your board.
