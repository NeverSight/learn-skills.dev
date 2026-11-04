---
name: setup-env
description: 生成三个开发 lane（host/控制/算法）的开发环境与工具链清单，含 SDK/IDE/包、版本锁定、下载源、自检步骤、烧录与调试工具。当用户要"配环境""装工具链""出环境清单""锁版本""3 台机器环境一致"时使用。产出 env/manifest.yaml + env/{host,control,vision}.md。
---

# setup-env —— 环境/工具链全包（流水线 ③）

**lane**: lead 产出，三 lane 消费  ·  **needs**: 无（读 solution + KB）

目标：每个 lane 拿到一份"装什么 / 哪个版本 / 哪下 / 怎么验证"的清单，**3 台机器照同一份 manifest，环境可复现**，避免"我这能编译你那不行"。

## 步骤

1. **取方案**：读 `design/solution.md` 确定主控（MSPM0 / STM32）与视觉（K230 / 无）。没有 solution 就问用户：主控选哪个、用不用 K230。工具链由此驱动：
   - MSPM0 → CCS Theia + MSPM0 SDK + SysConfig + Arm GCC/TI clang + XDS110 驱动。
   - STM32 → STM32CubeMX/CubeIDE 或 Keil + HAL/LL + ST-Link 驱动。
   - K230 → CanMV IDE + K230 固件镜像 + MicroPython。
2. **查 KB 环境清单**（用 Read）：`kb/10-典型赛题实战Playbook与Checklist.md` 的"赛前软件环境"小节、`kb/09-开源资源与备赛经验.md`、`kb/07-K230视觉与主控通信.md`（CanMV/镜像）。对齐已验证的工具与版本。
3. **生成 `env/manifest.yaml`**（机器可读，schema 见下），按三 lane 分组，**每项锁版本 + 下载源 + 自检命令**，含**烧录/调试工具**（XDS110/ST-Link 驱动、VOFA+ 上位机、串口助手、逻辑分析仪）。
4. **生成 `env/{host,control,vision}.md`**：每 lane 一份人类可读安装指南（安装顺序、坑、自检通过判据）。host 指向 `requirements.txt` + `tools/bootstrap.sh`。
5. 更新 `STATUS.md`：各 lane 段贴各自 env 文档链接。

## env/manifest.yaml schema

```yaml
version:
lanes:
  host:        # 跑 skill 工具的机器（lead）
    - {name: , kind: runtime|pkg|tool, version: , source: , verify: , notes: }
  control:     # 控制 lane（固件）
    - {name: CCS Theia, kind: ide, version: , source: , verify: , notes: }
    - {name: MSPM0 SDK, kind: sdk, version: , source: , verify: }
    - {name: SysConfig, kind: tool, ...}
    - {name: XDS110 驱动, kind: tool, ...}
    - {name: VOFA+, kind: tool, ...}          # 调参上位机（JustFloat）
  vision:      # 算法 lane（K230）
    - {name: CanMV IDE, kind: ide, ...}
    - {name: K230 镜像, kind: firmware, version: , source: , verify: }
```

## 注意

- **锁版本**：能写确切版本就写确切版本；写不准的标 `version: "待核实"` 并放进自检步骤让用户填回——别瞎编版本号。
- 工具的官方下载源优先（TI / ST / 嘉楠官方），KB `kb/资源链接总表.md` 里有现成链接可引。
- `verify` 给一条能跑的自检（如 `arm-none-eabi-gcc --version`、CanMV 串口能进 REPL），让队友确认装对了。
- 本 skill 只到"清单+版本+自检+（后续 firmware-scaffold 生成对应工程）"，**不替用户在他本机执行安装动作**。
- 生成对应工具链的**工程**（SysConfig/CubeMX）属 `firmware-scaffold`（Build Pass C），这里只出环境。
