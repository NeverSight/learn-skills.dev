---
name: power-design
description: 设计多路隔离供电系统并校验余量。当用户要"设计供电/电源""算电流预算""选稳压/DCDC""分电源轨"时使用。按电机堵转电流（不是标称）算每轨负载，产出 design/power.yaml + power.md，并用 tools/power_budget.py 做确定性校验，需人工批准。
---

# power-design —— 供电系统（流水线 ⑤）

**lane**: 任何模型（正确性交 `power_budget.py`）  ·  **门**: 人工批 + power_budget PASS

电源是 1 号翻车点：电机堵转瞬态把 MCU 拉掉电复位。**一切按最坏情况算。**

## 前置
`design/solution.md`（需求）+ `design/bom.csv`（选了哪些件/稳压）。

## 步骤
1. **分轨**（典型 4 轨，按方案裁剪）：
   - `VM_motor` —— 电池直供电机驱动（不稳压，加保险/铺铜）。
   - `V5_servo` —— 舵机独立 5~6V 高电流轨（**勿挂逻辑轨**，堵转>1A）。
   - `V3V3_logic` —— MCU + 模拟传感器，AMS1117 或 buck。
   - `V5_k230` —— K230 独立 5V（耗流远大于 MCU）。
2. **派负载**（Read KB `04/05` 取电流；电机/舵机标 `stall: true` 用堵转电流）。稳压器从 `bom.csv` 取，没有就提示在配件表/`jlc_search` 选。
3. 写 `design/power.yaml`（schema 见 `tools/power_budget.py` 头注；参考 `examples/sending-medicine-2023/power.yaml`）。
4. **跑确定性门**：`python tools/power_budget.py design/power.yaml`。FAIL（某轨欠流）就换更大稳压或加 buck，重跑直到 PASS。
5. 写 `design/power.md`（人类可读：分轨图 + 预算表 + 选的稳压 + 注意），更新 `STATUS.md`。
6. **人工门**：用户确认稳压选型与电池容量。

## 关键纪律
- 电机/舵机一律 `stall: true`；逻辑用标称。默认余量 30%。
- 电机 VM 与逻辑 GND **分开回流**再单点汇合（接线阶段落实）。
- power_budget PASS 是必要非充分——电池容量/放电倍率、保险、铺铜宽度仍需人工核（接线阶段）。
