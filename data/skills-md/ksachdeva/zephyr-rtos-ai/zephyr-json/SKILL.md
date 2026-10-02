---
name: zephyr-json
description: JSON serialization and deserialization in Zephyr RTOS using the descriptor-based JSON library. Use when encoding C structs to JSON strings, parsing JSON into C structs, working with nested objects or arrays, handling cloud/IoT protocols (MQTT, HTTP, CoAP payloads), or implementing REST APIs on embedded devices.
---

# Zephyr JSON

Zephyr's JSON library provides compile-time descriptor-based serialization without dynamic memory allocation. It maps C struct fields to JSON keys using static descriptors.

## Quick Start

```c
#include <zephyr/data/json.h>

// 1. Define your data structure
struct sensor_data {
    const char *device_id;
    int32_t temperature;
    bool active;
};

// 2. Create descriptors mapping struct fields to JSON keys
static const struct json_obj_descr sensor_descr[] = {
    JSON_OBJ_DESCR_PRIM(struct sensor_data, device_id, JSON_TOK_STRING),
    JSON_OBJ_DESCR_PRIM(struct sensor_data, temperature, JSON_TOK_NUMBER),
    JSON_OBJ_DESCR_PRIM(struct sensor_data, active, JSON_TOK_TRUE),
};

// 3. Encode to JSON
struct sensor_data data = {.device_id = "sensor-01", .temperature = 25, .active = true};
char buffer[128];
int ret = json_obj_encode_buf(sensor_descr, ARRAY_SIZE(sensor_descr), &data, buffer, sizeof(buffer));
// buffer: {"device_id":"sensor-01","temperature":25,"active":true}

// 4. Decode from JSON
char json[] = "{\"device_id\":\"sensor-02\",\"temperature\":30,\"active\":false}";
struct sensor_data parsed;
int64_t result = json_obj_parse(json, strlen(json), sensor_descr, ARRAY_SIZE(sensor_descr), &parsed);
```

## Kconfig

```kconfig
# Required
CONFIG_JSON_LIBRARY=y

# Optional: Enable float/double support (requires full libc)
CONFIG_JSON_LIBRARY_FP_SUPPORT=y
```

## Token Types Quick Reference

| Token Type | C Type | JSON Type |
|------------|--------|-----------|
| `JSON_TOK_STRING` | `const char *` | `"string"` |
| `JSON_TOK_STRING_BUF` | `char[]` | `"string"` (copies to buffer) |
| `JSON_TOK_NUMBER` | `int32_t` | `42` |
| `JSON_TOK_INT` | `int8_t`, `int16_t` | `-128` |
| `JSON_TOK_UINT` | `uint8_t`, `uint16_t`, `uint32_t` | `255` |
| `JSON_TOK_INT64` | `int64_t` | `9223372036854775807` |
| `JSON_TOK_UINT64` | `uint64_t` | `18446744073709551615` |
| `JSON_TOK_TRUE` / `JSON_TOK_FALSE` | `bool` | `true`/`false` |
| `JSON_TOK_FLOAT_FP` | `float` | `3.14` (requires FP_SUPPORT) |
| `JSON_TOK_DOUBLE_FP` | `double` | `3.14159` (requires FP_SUPPORT) |
| `JSON_TOK_OBJECT_START` | nested struct | `{...}` |
| `JSON_TOK_ARRAY_START` | array | `[...]` |

## Common Patterns

### Nested Objects

```c
struct inner {
    int value;
};

struct outer {
    const char *name;
    struct inner nested;
};

static const struct json_obj_descr inner_descr[] = {
    JSON_OBJ_DESCR_PRIM(struct inner, value, JSON_TOK_NUMBER),
};

static const struct json_obj_descr outer_descr[] = {
    JSON_OBJ_DESCR_PRIM(struct outer, name, JSON_TOK_STRING),
    JSON_OBJ_DESCR_OBJECT(struct outer, nested, inner_descr),
};
// {"name":"test","nested":{"value":42}}
```

### Arrays of Primitives

```c
struct data {
    int values[10];
    size_t values_len;  // Tracks actual count
};

static const struct json_obj_descr data_descr[] = {
    JSON_OBJ_DESCR_ARRAY(struct data, values, 10, values_len, JSON_TOK_NUMBER),
};
// {"values":[1,2,3,4,5]}
```

### Arrays of Objects

```c
struct item {
    const char *name;
    int qty;
};

struct order {
    struct item items[5];
    size_t items_len;
};

static const struct json_obj_descr item_descr[] = {
    JSON_OBJ_DESCR_PRIM(struct item, name, JSON_TOK_STRING),
    JSON_OBJ_DESCR_PRIM(struct item, qty, JSON_TOK_NUMBER),
};

static const struct json_obj_descr order_descr[] = {
    JSON_OBJ_DESCR_OBJ_ARRAY(struct order, items, 5, items_len,
                             item_descr, ARRAY_SIZE(item_descr)),
};
// {"items":[{"name":"apple","qty":3},{"name":"banana","qty":2}]}
```

### Named Fields (JSON key differs from C field)

Use `*_NAMED` variants when JSON keys aren't valid C identifiers:

```c
struct config {
    int api_version;     // JSON: "api-version"
    bool is_enabled;     // JSON: "is_enabled!"
};

static const struct json_obj_descr config_descr[] = {
    JSON_OBJ_DESCR_PRIM_NAMED(struct config, "api-version", api_version, JSON_TOK_NUMBER),
    JSON_OBJ_DESCR_PRIM_NAMED(struct config, "is_enabled!", is_enabled, JSON_TOK_TRUE),
};
```

### String Buffers vs Pointers

```c
struct example {
    const char *ptr_string;    // Points into original JSON buffer
    char buf_string[32];       // Copies data (survives buffer reuse)
};

static const struct json_obj_descr example_descr[] = {
    JSON_OBJ_DESCR_PRIM(struct example, ptr_string, JSON_TOK_STRING),
    JSON_OBJ_DESCR_PRIM(struct example, buf_string, JSON_TOK_STRING_BUF),
};
```

**Use `JSON_TOK_STRING_BUF` when**: JSON buffer will be reused or freed after parsing.

## Important Notes

1. **Input modification**: `json_obj_parse()` modifies the input buffer (null-terminates strings in place)
2. **No UTF-8 validation**: The library does not validate UTF-8 encoding
3. **Escape handling**: Escape sequences are preserved as-is (e.g., `\t` stays as `\t`)
4. **Descriptor limit**: Maximum 63 fields per descriptor array
5. **Return value**: `json_obj_parse()` returns a bitmap of decoded fields (bit N = field N decoded)

## References

- **API Details**: [references/api.md](references/api.md) - Complete function signatures and return values
- **Kconfig Options**: [references/kconfig.md](references/kconfig.md) - Configuration options and dependencies
- **Source Locations**: [references/locations.md](references/locations.md) - Header, implementation, and sample paths

## Related Skills

- **zephyr-net-socket**: HTTP/CoAP communication (JSON payloads)
- **zephyr-settings**: Persistent storage (JSON config files)
- **zephyr-cbor**: Alternative binary serialization (smaller, faster than JSON)