---
name: zephyr-spi
description: "Comprehensive Zephyr SPI subsystem expertise for serial peripheral communication. Use when: (1) Configuring SPI controllers or devices via devicetree or Kconfig, (2) Implementing synchronous SPI transfers with spi_transceive/spi_read/spi_write, (3) Implementing asynchronous SPI with spi_transceive_cb or spi_transceive_signal, (4) Setting up SPI modes (CPOL, CPHA, word size, bit order), (5) Managing chip select via GPIO or hardware CS, (6) Using scatter-gather buffers for multi-part transactions, (7) Choosing between sync and async APIs for a use case, (8) Troubleshooting SPI communication issues (clock polarity, CS timing, data corruption)."
---

# Zephyr SPI

Expert guidance for Zephyr's SPI driver subsystem covering synchronous and asynchronous transfer APIs, devicetree configuration, and common usage patterns.

## Table of Contents

1. [API Selection](#api-selection)
2. [Getting Device Reference](#getting-device-reference)
3. [Common Workflows](#common-workflows)
4. [Configuration](#configuration)
5. [Error Handling](#error-handling)
6. [Troubleshooting](#troubleshooting)

---

## API Selection

Zephyr provides two SPI access methods. Choose based on requirements:

| API | Kconfig | Use Case | Blocking? |
|-----|---------|----------|-----------|
| **Synchronous** | (default) | Simple transfers, blocking until complete | Yes |
| **Asynchronous** | `CONFIG_SPI_ASYNC` | Non-blocking, callback/signal on completion | No |

### Decision Tree

```
Simple blocking transfer? → Synchronous (spi_transceive)
Need non-blocking transfer? → Async (spi_transceive_cb / spi_transceive_signal)
High throughput with minimal CPU? → Async with DMA-capable driver
Multiple concurrent SPI operations? → Async with proper buffer management
```

---

## Getting Device Reference

### From Devicetree (Preferred - for SPI Devices)

Use `SPI_DT_SPEC_GET` to get a complete SPI specification including bus, config, and CS:

```c
#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>

/* Define the SPI device from devicetree */
#define MY_SPI_DEVICE DT_NODELABEL(my_spi_device)

static const struct spi_dt_spec spi_dev = SPI_DT_SPEC_GET(
    MY_SPI_DEVICE,
    SPI_OP_MODE_MASTER | SPI_WORD_SET(8) | SPI_TRANSFER_MSB
);

/* Runtime check (in main or init) */
if (!spi_is_ready_dt(&spi_dev)) {
    printk("SPI device not ready\n");
    return -ENODEV;
}
```

### Direct Controller Access (Less Common)

```c
/* Get SPI controller directly */
const struct device *spi = DEVICE_DT_GET(DT_NODELABEL(spi0));

if (!device_is_ready(spi)) {
    return -ENODEV;
}

/* Manual config setup */
struct spi_config spi_cfg = {
    .frequency = 1000000U,  /* 1 MHz */
    .operation = SPI_OP_MODE_MASTER | SPI_WORD_SET(8),
    .slave = 0,
    .cs = {0},  /* No GPIO CS, use hardware CS */
};
```

---

## Common Workflows

### 1. Basic Transceive (Simultaneous TX/RX)

```c
#include <zephyr/drivers/spi.h>

uint8_t tx_buf[] = {0x9F, 0x00, 0x00, 0x00};  /* Read ID command + dummy bytes */
uint8_t rx_buf[4];

struct spi_buf tx = {.buf = tx_buf, .len = sizeof(tx_buf)};
struct spi_buf rx = {.buf = rx_buf, .len = sizeof(rx_buf)};
struct spi_buf_set tx_set = {.buffers = &tx, .count = 1};
struct spi_buf_set rx_set = {.buffers = &rx, .count = 1};

int ret = spi_transceive_dt(&spi_dev, &tx_set, &rx_set);
if (ret < 0) {
    printk("SPI transceive error: %d\n", ret);
}
/* rx_buf now contains response */
```

### 2. Write Only (No RX)

```c
uint8_t cmd[] = {0x06};  /* Write enable command */

struct spi_buf tx = {.buf = cmd, .len = sizeof(cmd)};
struct spi_buf_set tx_set = {.buffers = &tx, .count = 1};

int ret = spi_write_dt(&spi_dev, &tx_set);
```

### 3. Read Only (TX Ignored)

```c
uint8_t data[16];

struct spi_buf rx = {.buf = data, .len = sizeof(data)};
struct spi_buf_set rx_set = {.buffers = &rx, .count = 1};

int ret = spi_read_dt(&spi_dev, &rx_set);
```

### 4. Scatter-Gather (Multi-Buffer Transfer)

Use multiple buffers for command + address + data in a single CS assertion:

```c
uint8_t cmd = 0x03;           /* Read command */
uint8_t addr[3] = {0x00, 0x10, 0x00};  /* 24-bit address */
uint8_t data[64];

struct spi_buf tx_bufs[] = {
    {.buf = &cmd, .len = 1},
    {.buf = addr, .len = 3},
    {.buf = NULL, .len = 64},  /* NULL = send zeros while receiving */
};
struct spi_buf rx_bufs[] = {
    {.buf = NULL, .len = 1},   /* NULL = ignore received data */
    {.buf = NULL, .len = 3},
    {.buf = data, .len = 64},
};

struct spi_buf_set tx_set = {.buffers = tx_bufs, .count = 3};
struct spi_buf_set rx_set = {.buffers = rx_bufs, .count = 3};

int ret = spi_transceive_dt(&spi_dev, &tx_set, &rx_set);
```

### 5. Async Transfer with Callback

Requires `CONFIG_SPI_ASYNC=y`:

```c
#include <zephyr/drivers/spi.h>

static volatile bool transfer_done;
static int transfer_result;

void spi_callback(const struct device *dev, int result, void *userdata)
{
    transfer_result = result;
    transfer_done = true;
}

int async_transfer(void)
{
    uint8_t tx_data[] = {0x01, 0x02, 0x03};
    uint8_t rx_data[3];

    struct spi_buf tx = {.buf = tx_data, .len = sizeof(tx_data)};
    struct spi_buf rx = {.buf = rx_data, .len = sizeof(rx_data)};
    struct spi_buf_set tx_set = {.buffers = &tx, .count = 1};
    struct spi_buf_set rx_set = {.buffers = &rx, .count = 1};

    transfer_done = false;

    int ret = spi_transceive_cb(spi_dev.bus, &spi_dev.config,
                                 &tx_set, &rx_set, spi_callback, NULL);
    if (ret < 0) {
        return ret;
    }

    /* Do other work while transfer is in progress */

    /* Wait for completion (or use k_poll) */
    while (!transfer_done) {
        k_yield();
    }

    return transfer_result;
}
```

- **Full async API details**: See [references/async.md](references/async.md)

---

## Configuration

### Kconfig Essentials

```kconfig
CONFIG_SPI=y                    # Enable SPI driver subsystem
CONFIG_SPI_ASYNC=y              # Enable async API (callback/signal)
CONFIG_SPI_SLAVE=y              # Enable slave mode (experimental)
CONFIG_SPI_EXTENDED_MODES=y     # Enable dual/quad/octal line modes
CONFIG_SPI_SHELL=y              # Enable SPI shell for debugging
```

- **Full Kconfig reference**: See [references/kconfig.md](references/kconfig.md)

### Devicetree Essentials

#### SPI Controller

```dts
&spi0 {
    status = "okay";
    pinctrl-0 = <&spi0_default>;
    pinctrl-names = "default";
    cs-gpios = <&gpio0 4 GPIO_ACTIVE_LOW>;  /* CS on GPIO0 pin 4 */

    my_spi_device: sensor@0 {
        compatible = "vendor,sensor";
        reg = <0>;                      /* CS index (matches cs-gpios) */
        spi-max-frequency = <1000000>;  /* 1 MHz max */
        /* Optional SPI mode settings */
        spi-cpol;                       /* Clock idle high (Mode 2 or 3) */
        spi-cpha;                       /* Sample on second edge (Mode 1 or 3) */
    };
};
```

#### SPI Mode Quick Reference

| Mode | CPOL | CPHA | DTS Properties |
|------|------|------|----------------|
| 0 | 0 | 0 | (default) |
| 1 | 0 | 1 | `spi-cpha` |
| 2 | 1 | 0 | `spi-cpol` |
| 3 | 1 | 1 | `spi-cpol; spi-cpha` |

- **Full devicetree reference**: See [references/devicetree.md](references/devicetree.md)

### Operation Flags

Common flags for `spi_config.operation`:

| Flag | Description |
|------|-------------|
| `SPI_OP_MODE_MASTER` | Controller/master mode (default) |
| `SPI_OP_MODE_SLAVE` | Peripheral/slave mode |
| `SPI_MODE_CPOL` | Clock polarity (idle high) |
| `SPI_MODE_CPHA` | Clock phase (sample on second edge) |
| `SPI_WORD_SET(n)` | Word size in bits (typically 8) |
| `SPI_TRANSFER_MSB` | MSB first (default) |
| `SPI_TRANSFER_LSB` | LSB first |
| `SPI_HOLD_ON_CS` | Keep CS active after transaction |
| `SPI_LOCK_ON` | Lock bus for multiple transactions |
| `SPI_CS_ACTIVE_HIGH` | CS is active high (unusual) |

---

## Error Handling

### Return Values

| Value | Meaning |
|-------|---------|
| `0` | Success (master mode) |
| `> 0` | Frames received (slave mode) |
| `-ENOTSUP` | Unsupported config (check operation flags) |
| `-EINVAL` | Invalid parameter in spi_config |
| `-EBUSY` | Bus locked by another caller |
| `-errno` | Other failure |

### Releasing Locked Bus

If using `SPI_LOCK_ON` or `SPI_HOLD_ON_CS`, release when done:

```c
spi_release_dt(&spi_dev);
```

---

## Troubleshooting

### Quick Reference

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| No data on bus | Wrong pins | Verify pinctrl in devicetree |
| Garbled data | Mode mismatch | Check CPOL/CPHA match device datasheet |
| CS not toggling | GPIO not configured | Add `cs-gpios` to controller node |
| `-ENOTSUP` | Unsupported operation | Check driver supports requested features |
| `-EBUSY` | Bus locked | Call `spi_release()` or remove `SPI_LOCK_ON` |
| Slow transfer | Low frequency | Increase `spi-max-frequency` in DTS |
| RX data offset | TX/RX length mismatch | Ensure buffer lengths account for command bytes |

### Debug Checklist

1. **Device ready?** Check `spi_is_ready_dt(&spec)`
2. **Pins correct?** Verify pinctrl (SCK, MOSI, MISO, CS)
3. **Mode match?** CPOL/CPHA must match peripheral device
4. **Frequency valid?** Some devices have min/max limits
5. **CS polarity?** Most devices are active-low (default)
6. **Word size?** Most devices use 8-bit words

---

## References

- [references/api.md](references/api.md) — Full API function reference
- [references/async.md](references/async.md) — Async API with callback/signal patterns
- [references/kconfig.md](references/kconfig.md) — All SPI Kconfig options
- [references/devicetree.md](references/devicetree.md) — Devicetree properties and examples

## Source Locations

Key files in Zephyr source tree:
- `include/zephyr/drivers/spi.h` — Public API header
- `drivers/spi/` — Driver implementations
- `dts/bindings/spi/spi-controller.yaml` — Controller DTS binding
- `dts/bindings/spi/spi-device.yaml` — Device DTS binding
- `samples/drivers/spi_*` — Sample applications
