---
name: zephyr-cbor
description: CBOR (Concise Binary Object Representation) encoding and decoding in Zephyr RTOS using the zcbor library. Use when encoding C data to CBOR binary format, decoding CBOR payloads into C variables, generating type-safe C code from CDDL schemas, working with CoAP/LwM2M/SUIT/SMP payloads, or implementing efficient binary serialization for IoT protocols.
---

# Zephyr CBOR (zcbor)

Zephyr integrates the [zcbor](https://github.com/NordicSemiconductor/zcbor) library for CBOR encoding/decoding.

## ⭐ Recommended: Code Generation from CDDL Schema

For any non-trivial message format, **use zcbor's code generator** instead of hand-writing zcbor calls. It generates type-safe C structs and encode/decode functions from a [CDDL](https://datatracker.ietf.org/doc/html/rfc8610) schema — less error-prone, easier to maintain, and handles unions/optionals automatically.

### 1. Write a CDDL schema

CDDL supports two container styles — choose based on whether field order matters:

- **Group/tuple** `(...)` — ordered sequence, no keys on wire (more compact)
- **Map** `{...}` — key-value pairs, order-independent (more flexible)

```cddl
; my-api.cddl

; Integer constants for a discriminated union
cmd_get_status = 1
cmd_set_config = 2

command_id /= cmd_get_status
command_id /= cmd_set_config

; Enum values
status_idle   = 0
status_active = 1
status_error  = 2

device_status /= status_idle
device_status /= status_active
device_status /= status_error

; Tuple (ordered, compact — no keys on wire)
set_config_params = (
    threshold: uint .size 2,
    enabled:   bool,
)

; Map (key-value, order-independent)
status_response = {
    status_code: device_status,
    uptime_ms:   uint,
    ? error_msg: tstr,
}

; Top-level message with optional params
My_Command = (
    command_id: command_id,
    ? params:   set_config_params,
)
```

### 2. Generate C code

```bash
pip install zcbor

zcbor code --decode --encode \
  --short-names \
  -c my-api.cddl \
  -t My_Command \
     status_response \
  --output-c src/cbor/my-api.c \
  --output-h include/cbor/my-api.h \
  --output-h-types include/cbor/my-api_types.h \
  --include-prefix "cbor/" \
  --default-max-qty 3
```

Key flags:

| Flag | Purpose |
|------|---------|
| `--decode` / `--encode` | Generate decode and/or encode functions |
| `-t <types>` | Root types to generate entry-point functions for |
| `--short-names` | Shorten generated symbol names (avoids very long identifiers) |
| `--output-c/h/h-types` | Output paths for `.c`, `.h`, and `_types.h` |
| `--include-prefix` | Prefix added to `#include` paths inside generated `.c` files |
| `--default-max-qty N` | Max array/list entries (affects struct array sizes) |
| `--file-header <file>` | Prepend a custom copyright/license header to generated files |

> zcbor splits `my-api.c` into `my-api_decode.c` / `my-api_encode.c` automatically. Do **not** hand-edit generated files — regenerate from `.cddl` when the schema changes.

**CMake integration** — trigger regeneration when the `.cddl` changes:

```cmake
set(zcbor_command
    zcbor code --decode --encode --short-names
    -c ${CMAKE_CURRENT_LIST_DIR}/my-api.cddl
    -t My_Command status_response
    --output-c     ${CMAKE_CURRENT_LIST_DIR}/src/cbor/my-api.c
    --output-h     ${CMAKE_CURRENT_LIST_DIR}/include/cbor/my-api.h
    --output-h-types ${CMAKE_CURRENT_LIST_DIR}/include/cbor/my-api_types.h
    --include-prefix "cbor/"
    --default-max-qty 3
)

add_custom_command(
    OUTPUT
        ${CMAKE_CURRENT_LIST_DIR}/src/cbor/my-api_decode.c
        ${CMAKE_CURRENT_LIST_DIR}/src/cbor/my-api_encode.c
        ${CMAKE_CURRENT_LIST_DIR}/include/cbor/my-api_decode.h
        ${CMAKE_CURRENT_LIST_DIR}/include/cbor/my-api_encode.h
        ${CMAKE_CURRENT_LIST_DIR}/include/cbor/my-api_types.h
    COMMAND ${zcbor_command}
    DEPENDS ${CMAKE_CURRENT_LIST_DIR}/my-api.cddl
    COMMENT "Regenerating CBOR code from CDDL schema"
)
```

### 3. Use the generated API

zcbor naming conventions for generated symbols:

- **Structs**: `struct <TypeName>` (e.g. `struct My_Command`)
- **Union choice enums**: `<union_name>_<value_name>_m_c` (e.g. `command_id_cmd_get_status_m_c`)
- **Union choice field**: `<union_name>_choice` (e.g. `command_id_choice`)
- **Optional fields**: `bool <field>_present` alongside the field
- **Repeated fields**: `<field>_m[N]` array + `size_t <field>_m_count`
- **Single-field groups** are flattened into their parent struct

```c
#include "cbor/my-api_decode.h"   /* cbor_decode_My_Command() */
#include "cbor/my-api_encode.h"   /* cbor_encode_status_response() */
#include "cbor/my-api_types.h"    /* struct My_Command, device_status_r, ... */

/* --- Decode --- */
struct My_Command cmd = {0};
size_t consumed;

int err = cbor_decode_My_Command(buf, buf_len, &cmd, &consumed);
if (err != ZCBOR_SUCCESS) {
    return err;
}

switch (cmd.command_id_choice) {
    case command_id_cmd_get_status_m_c:
        break;
    case command_id_cmd_set_config_m_c:
        if (cmd.params_present) {
            uint32_t threshold = cmd.params.threshold;
            bool     enabled   = cmd.params.enabled;
        }
        break;
}

/* --- Encode --- */
struct status_response resp = {
    .status_code.device_status_choice = device_status_status_active_m_c,
    .uptime_ms   = k_uptime_get_32(),
    .error_msg_present = false,
};
uint8_t out[64];
size_t  out_len;
cbor_encode_status_response(out, sizeof(out), &resp, &out_len);
```

### When to use code generation vs. manual

| Scenario | Approach |
|----------|----------|
| Complex/nested schema, multiple message types | ✅ Code generation (recommended) |
| Schema changes over time | ✅ Code generation — regenerate, don't edit |
| Simple one-off encode/decode, few fields | Manual API fine |
| CoAP/LwM2M/SUIT (pre-defined schemas) | ✅ Code generation — schemas already exist |

---

## Manual API

For simple cases. All operations use a `zcbor_state_t` state machine and return `bool` (true=success).

### Kconfig

```kconfig
CONFIG_ZCBOR=y
```

### Quick Start: Encoding

```c
#include <zcbor_encode.h>

uint8_t buf[64];
ZCBOR_STATE_E(zse, 0, buf, sizeof(buf), 1);  // 0 backups, 1 top-level element

bool ok = zcbor_map_start_encode(zse, 2)
       && zcbor_tstr_put_lit(zse, "temp")
       && zcbor_int32_put(zse, 22)
       && zcbor_tstr_put_lit(zse, "unit")
       && zcbor_tstr_put_lit(zse, "C")
       && zcbor_map_end_encode(zse, 2);

size_t len = zse->payload - buf;  // bytes written
```

### Quick Start: Decoding

```c
#include <zcbor_decode.h>

ZCBOR_STATE_D(zsd, 0, buf, buf_len, 1, 0);  // 0 backups, 1 element, 0 flags

int32_t temp;
struct zcbor_string unit;

bool ok = zcbor_map_start_decode(zsd)
       && zcbor_tstr_expect_lit(zsd, "temp")
       && zcbor_int32_decode(zsd, &temp)
       && zcbor_tstr_expect_lit(zsd, "unit")
       && zcbor_tstr_decode(zsd, &unit)
       && zcbor_map_end_decode(zsd);
```

## References

- **[references/api.md](references/api.md)** — Type quick reference, complete function signatures, state initialization, error codes. Read when working with manual encode/decode functions.
- **[references/patterns.md](references/patterns.md)** — Common patterns: lists, unordered maps, byte strings, nested CBOR, multi-decode. Read when implementing specific data structures.
- **[references/kconfig.md](references/kconfig.md)** — All `CONFIG_ZCBOR_*` options. Read when configuring zcbor features beyond `CONFIG_ZCBOR=y`.
- **[references/locations.md](references/locations.md)** — Header paths, sample locations, upstream links. Read when locating source files.

## Related Skills

- **zephyr-net-socket**: CoAP/UDP transport for CBOR payloads
- **zephyr-bluetooth-le**: SMP over BLE uses CBOR
- **zephyr-json**: Alternative text-based serialization

