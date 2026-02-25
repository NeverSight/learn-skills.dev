---
name: ascend-docker
description: Create Docker containers for Huawei Ascend NPU development with proper device mappings and volume mounts. Use when setting up Ascend development environments in Docker, running CANN applications in containers, or creating isolated NPU development workspaces. Supports privileged mode (default), basic mode, and full mode with profiling/logging. Auto-detects available NPU devices.
keywords:
    - ascend
    - docker
    - npu
    - development
    - 开发环境
    - 容器化
    - 昇腾
---

# Ascend Docker Container

Create Docker containers configured for Huawei Ascend NPU development.

## Quick Start

```bash
# Privileged mode (default, auto-detect all devices)
./scripts/run-ascend-container.sh <image> <container_name>

# Basic mode with specific devices
./scripts/run-ascend-container.sh <image> <container_name> --mode basic

# Full mode with selected devices
./scripts/run-ascend-container.sh <image> <container_name> --mode full --device-list "0,1,2,3"
```

## Device Selection

The script auto-detects available NPU devices from `/dev/davinci*`. Use `--device-list` to select specific devices:

```bash
# Use all detected devices (default)
./scripts/run-ascend-container.sh <image> <container_name>

# Use specific devices
./scripts/run-ascend-container.sh <image> <container_name> --device-list "0,1,2,3"

# Use device range
./scripts/run-ascend-container.sh <image> <container_name> --device-list "0-3"

# Combine ranges and individual devices
./scripts/run-ascend-container.sh <image> <container_name> --device-list "0-3,7,10-11"
```

**Check available devices:**
```bash
ls /dev/davinci* | grep -oE 'davinci[0-9]+$'
```

## Container Modes

### 1. Privileged Mode (Default)

Maximum permissions, suitable when no specific requirements.

```bash
docker run -itd --privileged --name=<CONTAINER_NAME> --ipc=host --net=host \
  --device=/dev/davinci_manager \
  --device=/dev/devmm_svm \
  --device=/dev/hisi_hdc \
  -v /usr/local/sbin:/usr/local/sbin:ro \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
  -v /home:/home \
  -w /home \
  <IMAGE> \
  /bin/bash
```

### 2. Basic Mode

Specific device mapping with network host, for inference workloads.

```bash
docker run -itd --net=host \
  --name=<CONTAINER_NAME> \
  --device=/dev/davinci_manager \
  --device=/dev/hisi_hdc \
  --device=/dev/devmm_svm \
  --device=/dev/davinci0 \
  --device=/dev/davinci1 \
  ... \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
  -v /usr/local/sbin:/usr/local/sbin:ro \
  -v /etc/localtime:/etc/localtime \
  -v /home:/home \
  <IMAGE> \
  /bin/bash
```

### 3. Full Mode

With profiling, logging, dump, and add-ons support.

```bash
docker run -itd --ipc=host \
  --name=<CONTAINER_NAME> \
  --device=/dev/davinci_manager \
  --device=/dev/devmm_svm \
  --device=/dev/hisi_hdc \
  --device=/dev/davinci0 \
  --device=/dev/davinci1 \
  ... \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
  -v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
  -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
  -v /usr/local/sbin/:/usr/local/sbin/ \
  -v /var/log/npu/conf/slog/slog.conf:/var/log/npu/conf/slog/slog.conf \
  -v /var/log/npu/slog/:/var/log/npu/slog \
  -v /var/log/npu/profiling/:/var/log/npu/profiling \
  -v /var/log/npu/dump/:/var/log/npu/dump \
  -v /var/log/npu/:/usr/slog \
  -v /etc/localtime:/etc/localtime \
  -v /home:/home \
  <IMAGE> \
  /bin/bash
```

## Mode Comparison

| Feature | Privileged | Basic | Full |
|---------|------------|-------|------|
| Network mode | host | host | - |
| IPC mode | host | - | host |
| Device access | All (via privileged) | Selected devices | Selected devices |
| Profiling support | ✓ | ✗ | ✓ |
| Dump support | ✓ | ✗ | ✓ |
| Logging (slog) | ✓ | ✗ | ✓ |
| Security | Lowest | Higher | Higher |

## Device Parameters

| Device | Purpose |
|--------|---------|
| `/dev/davinci_manager` | NPU device manager |
| `/dev/devmm_svm` | Device memory management |
| `/dev/hisi_hdc` | HDC communication device |
| `/dev/davinci<N>` | Individual NPU devices (0, 1, 2, ...) |

## Volume Parameters

| Volume | Purpose |
|--------|---------|
| `/usr/local/Ascend/driver` | Ascend driver libraries |
| `/usr/local/sbin` | NPU management tools (npu-smi) |
| `/usr/local/Ascend/add-ons` | Additional Ascend components |
| `/var/log/npu/slog` | System logs |
| `/var/log/npu/profiling` | Profiling data |
| `/var/log/npu/dump` | Dump data |
| `/etc/localtime` | Timezone sync |
| `/home` | User workspace |

## Common Images

```bash
ascendhub.huawei.com/public-ascendhub/ascend-pytorch:24.0.RC1
ascendhub.huawei.com/public-ascendhub/ascend-mindspore:24.0.RC1
ascendhub.huawei.com/public-ascendhub/ascend-toolkit:24.0.RC1
```

## Container Management

```bash
docker exec -it <container_name> bash
docker stop <container_name>
docker start <container_name>
docker rm -f <container_name>
```

## Post-Setup

For self-built images, configure environment variables:

```bash
echo 'source /usr/local/Ascend/ascend-toolkit/set_env.sh' >> ~/.bashrc
source ~/.bashrc
```

## Official References

- [Ascend Docker Guide](https://www.hiascend.com/document/detail/zh/300Vtest/300VG/300V_0032.html)
