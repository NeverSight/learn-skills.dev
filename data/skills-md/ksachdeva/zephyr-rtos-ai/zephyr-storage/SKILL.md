---
name: zephyr-storage
description: Direct key-value storage using NVS (Non-Volatile Storage) and ZMS (Zephyr Memory Storage) subsystems in Zephyr OS. Use when storing data directly to flash with numeric IDs (not string keys), choosing between NVS and ZMS, configuring flash partitions for storage, calculating flash wear and device lifetime, or working with storage APIs (mount, read, write, delete). For high-level string-key persistence, use zephyr-settings skill instead.
---

# Zephyr Storage Skill

## Quick Decision: NVS vs ZMS

```
What hardware are you targeting?
├── Classical NOR flash (most MCUs) → Use NVS
├── RRAM/MRAM (no erase required) → Use ZMS
├── Need >64K unique IDs → Use ZMS (supports 32/64-bit IDs)
└── Unsure → Use NVS (battle-tested default)
```

| Feature | NVS | ZMS |
|---------|-----|-----|
| ID size | 16-bit (65K max) | 32-bit or 64-bit |
| Best for | Classical flash | RRAM, MRAM, large flash |
| Erase optimization | Standard | Single-write erase (256x faster on RRAM) |
| ATE size | 8 bytes | 16 bytes |
| Data CRC | Optional | Built-in (in ATE) |
| Small data optimization | No | Yes (data stored in ATE if <=8 bytes) |
| Status | Stable, widely used | Newer, recommended for new designs |

## When to Use This Skill vs zephyr-settings

| Use Case | Skill |
|----------|-------|
| Store data with **numeric IDs** | **zephyr-storage** (this skill) |
| Store data with **string keys** (e.g., `wifi/ssid`) | zephyr-settings |
| Direct flash control needed | **zephyr-storage** |
| Integration with Bluetooth/Shell settings | zephyr-settings |
| Maximum performance, minimal overhead | **zephyr-storage** |

## Basic Usage Pattern

Both NVS and ZMS follow the same pattern:

```c
#include <zephyr/fs/nvs.h>  // or <zephyr/fs/zms.h>

// 1. Define storage structure
static struct nvs_fs fs;  // or struct zms_fs

// 2. Configure and mount
fs.flash_device = FIXED_PARTITION_DEVICE(storage_partition);
fs.offset = FIXED_PARTITION_OFFSET(storage_partition);
fs.sector_size = /* flash page size */;
fs.sector_count = 3;  // minimum 2
nvs_mount(&fs);  // or zms_mount()

// 3. Read/Write/Delete
nvs_write(&fs, ID, data, len);
nvs_read(&fs, ID, buffer, len);
nvs_delete(&fs, ID);
```

## Kconfig Quick Reference

### NVS
```
CONFIG_FLASH=y
CONFIG_FLASH_PAGE_LAYOUT=y
CONFIG_FLASH_MAP=y
CONFIG_NVS=y

# Optional performance
CONFIG_NVS_LOOKUP_CACHE=y
CONFIG_NVS_LOOKUP_CACHE_SIZE=128

# Optional integrity
CONFIG_NVS_DATA_CRC=y
```

### ZMS
```
CONFIG_FLASH=y
CONFIG_FLASH_MAP=y
CONFIG_ZMS=y

# Optional: 64-bit IDs (default is 32-bit)
CONFIG_ZMS_ID_64BIT=y

# Optional performance
CONFIG_ZMS_LOOKUP_CACHE=y
CONFIG_ZMS_LOOKUP_CACHE_SIZE=128
```

## References

- **NVS Details**: [references/nvs.md](references/nvs.md) - API, Kconfig, wear leveling calculations
- **ZMS Details**: [references/zms.md](references/zms.md) - API, Kconfig, ATE formats, 64-bit IDs
- **Comparison**: [references/comparison.md](references/comparison.md) - Side-by-side feature comparison
- **Devicetree**: [references/devicetree.md](references/devicetree.md) - Partition configuration
- **Locations**: [references/locations.md](references/locations.md) - Source code and documentation paths

## Related Skills

- **zephyr-settings**: High-level persistence with string keys (uses NVS/ZMS as backend)
- **zephyr-devicetree**: Configure storage partitions
- **zephyr-kconfig**: Configure `CONFIG_NVS_*` and `CONFIG_ZMS_*` options
