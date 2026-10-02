---
name: zephyr-fs
description: File system support in Zephyr OS including VFS API, LittleFS, FAT, ext2, and FCB. Use when working with file I/O operations, mounting filesystems, reading/writing files, directory operations, formatting storage, choosing between filesystem types, configuring flash partitions for filesystems, or implementing persistent file-based storage. For key-value storage with numeric IDs, use zephyr-storage instead. For string-key settings persistence, use zephyr-settings instead.
---

# Zephyr File System Skill

## Quick Decision: Choose Your File System

```
What storage medium and use case?
├── Internal flash (MCU) + power-loss safety → LittleFS
├── SD card / USB / PC compatibility needed → FAT
├── Large block device + Linux compatibility → ext2
├── Log-style append-only data on flash → FCB
├── Key-value pairs (not files) → See zephyr-storage skill
└── Virtualized environment (QEMU) → VirtioFS
```

| Feature | LittleFS | FAT | ext2 | FCB |
|---------|----------|-----|------|-----|
| Storage type | Flash | Disk (SD/USB) | Block device | Flash |
| Power-loss safe | Yes | No | No | Yes |
| Wear leveling | Yes | No | No | Yes |
| PC compatible | No | Yes | Linux only | No |
| Best for | Embedded flash | Removable media | Large storage | Logs/journals |

## VFS API (Common to All File Systems)

All file systems use the same API from `<zephyr/fs/fs.h>`.

### Basic File Operations

```c
#include <zephyr/fs/fs.h>

struct fs_file_t file;
fs_file_t_init(&file);  // MUST initialize before use

// Open file (create if needed)
int rc = fs_open(&file, "/lfs/data.txt", FS_O_CREATE | FS_O_RDWR);

// Write data
const char *data = "Hello";
fs_write(&file, data, strlen(data));

// Seek to beginning
fs_seek(&file, 0, FS_SEEK_SET);

// Read data
char buf[32];
ssize_t bytes = fs_read(&file, buf, sizeof(buf));

// Close file
fs_close(&file);
```

### Open Flags

| Flag | Description |
|------|-------------|
| `FS_O_READ` | Open for read |
| `FS_O_WRITE` | Open for write |
| `FS_O_RDWR` | Read and write |
| `FS_O_CREATE` | Create if not exists |
| `FS_O_APPEND` | Append mode |
| `FS_O_TRUNC` | Truncate to zero |

### Directory Operations

```c
struct fs_dir_t dir;
struct fs_dirent entry;

fs_dir_t_init(&dir);  // MUST initialize before use
fs_opendir(&dir, "/lfs");

while (fs_readdir(&dir, &entry) == 0 && entry.name[0] != 0) {
    if (entry.type == FS_DIR_ENTRY_DIR) {
        printk("[DIR]  %s\n", entry.name);
    } else {
        printk("[FILE] %s (%zu bytes)\n", entry.name, entry.size);
    }
}
fs_closedir(&dir);

// Create directory
fs_mkdir("/lfs/newdir");

// Delete file or empty directory
fs_unlink("/lfs/oldfile.txt");

// Rename/move
fs_rename("/lfs/old.txt", "/lfs/new.txt");
```

### Mount and Volume Operations

```c
// Mount filesystem
fs_mount(&mount_point);

// Unmount
fs_unmount(&mount_point);

// Get volume stats
struct fs_statvfs stat;
fs_statvfs("/lfs", &stat);
printk("Total: %lu blocks, Free: %lu blocks\n", stat.f_blocks, stat.f_bfree);

// Format filesystem (requires CONFIG_FILE_SYSTEM_MKFS=y)
fs_mkfs(FS_LITTLEFS, (uintptr_t)FIXED_PARTITION_ID(storage_partition), NULL, 0);
```

## Kconfig Quick Reference

### Core File System

```kconfig
CONFIG_FILE_SYSTEM=y              # Enable VFS
CONFIG_FILE_SYSTEM_SHELL=y        # Shell commands (ls, cd, cat, etc.)
CONFIG_FILE_SYSTEM_MKFS=y         # Enable formatting
```

### LittleFS

```kconfig
CONFIG_FILE_SYSTEM_LITTLEFS=y
CONFIG_FS_LITTLEFS_NUM_FILES=4    # Max open files
CONFIG_FS_LITTLEFS_NUM_DIRS=4     # Max open directories
CONFIG_FS_LITTLEFS_CACHE_SIZE=64  # Cache per file (RAM usage)
CONFIG_FS_LITTLEFS_BLOCK_CYCLES=512  # Wear leveling cycles
```

### FAT

```kconfig
CONFIG_FAT_FILESYSTEM_ELM=y
CONFIG_FS_FATFS_LFN=y             # Long file names
CONFIG_FS_FATFS_EXFAT=y           # exFAT support
CONFIG_FS_FATFS_MKFS=y            # Format support
```

### ext2

```kconfig
CONFIG_FILE_SYSTEM_EXT2=y
CONFIG_EXT2_MAX_BLOCK_SIZE=4096
```

### FCB

```kconfig
CONFIG_FCB=y
CONFIG_FLASH_MAP=y
```

## Devicetree Fstab (Automount)

Define mount points in devicetree for automatic mounting:

```dts
/ {
    fstab {
        compatible = "zephyr,fstab";
        lfs1: lfs1 {
            compatible = "zephyr,fstab,littlefs";
            mount-point = "/lfs";
            partition = <&storage_partition>;
            automount;
            read-size = <16>;
            prog-size = <16>;
            cache-size = <64>;
            lookahead-size = <32>;
            block-cycles = <512>;
        };
    };
};
```

Access automounted filesystem:

```c
#define PARTITION_NODE DT_NODELABEL(lfs1)
FS_FSTAB_DECLARE_ENTRY(PARTITION_NODE);
struct fs_mount_t *mp = &FS_FSTAB_ENTRY(PARTITION_NODE);
// mp is already mounted, use directly
```

## References

- **LittleFS**: [references/littlefs.md](references/littlefs.md) - Flash-based filesystem configuration and usage
- **FAT**: [references/fat.md](references/fat.md) - SD card and removable media
- **FCB**: [references/fcb.md](references/fcb.md) - Flash Circular Buffer for logs
- **API Reference**: [references/api.md](references/api.md) - Complete VFS API
- **Locations**: [references/locations.md](references/locations.md) - Source code and sample paths

## Related Skills

- **zephyr-storage**: Direct key-value storage (NVS/ZMS) with numeric IDs
- **zephyr-settings**: High-level settings with string keys
- **zephyr-devicetree**: Configure storage partitions
