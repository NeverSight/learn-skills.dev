---
name: plan-solution
description: 据已解析的题目（design/problem.yaml）定技术方案并推导系统需求。当用户要"定方案""选主控/视觉路线""出需求表""根据题目决定怎么做"时使用。产出 design/solution.md（技术方案 + 签字需求表 + 子系统清单），需用户签字确认后才进选材。
---

# plan-solution —— 方案 + 需求（流水线 ②）

**lane**: lead（推理重，建议 Claude）  ·  **needs**: 无  ·  **门**: 人工签字需求表

把题目变成"怎么做 + 要满足哪些硬指标"。**借鉴金奖经验，别凭空设计。**

## 前置
读 `design/problem.yaml`（没有就先跑 `/read-problem`）。重点看 `restrictions.camera_allowed` —— 决定视觉路线。

## 步骤
1. **查金奖经验/技术栈**（Read，不复制）：
   - `kb/10-典型赛题实战Playbook与Checklist.md` —— "典型赛题技术栈组合"表，找与本题 `category` 最近的一行作起点。
   - `kb/09-开源资源与备赛经验.md` —— 金奖做法/避坑。
   - `kb/06-PID及衍生控制算法.md`、`kb/08-软件架构与调试工程化.md` —— 控制结构。
2. **定方案**（逐子系统）：
   - 主控：默认 MSPM0G3507（KB03），需更强算力/FPU 再议 STM32G431。
   - 视觉：`camera_allowed=true` → K230 做识别/巡线；`=false` → 纯灰度/电磁，**显著标注本届不上 K230**。
   - 传感：循迹（灰度阵列/电磁/K230）、定位（编码器/IMU/TOF）按题目功能选。
   - 执行：电机+驱动（默认 TB6612+编码电机）、舵机（如需转向/云台）。
   - 控制结构：嵌套 PID（外环位置/航向 ← 视觉/IMU/灰度；内环速度 ← 编码器）+ FSM 跑流程。
3. **推导需求**（硬数字，给后续选材/供电/接线用）：
   - 电源轨与电压、每轨**最坏电流**（电机用堵转）、逻辑电平。
   - 接口清单与**数量**：要几路 PWM/UART/I2C/SPI/ADC/QEI（对照 MCU 能力表 `contracts/mcu/`）。
   - 每个外设及其接口、对端连接器。
4. 写 `design/solution.md`（模板见下）。
5. **人工门**：把"签字需求表"摊给用户逐项确认；用户没确认的硬指标**不要默认**，标 TODO。确认后更新 `STATUS.md` → ③/④，并提示可并行：lead 跑 `/setup-env`，随后 `/select-parts`。

## design/solution.md 模板
```markdown
# 方案与需求 —— <题目名>
来源: design/problem.yaml  | 类别: <category> | 摄像头: <允许/禁止>

## 技术方案
- 主控: MSPM0G3507（理由…）
- 视觉: K230 / 无（依据 camera_allowed）
- 传感: …  执行: …  控制结构: 嵌套PID + FSM
- 参考金奖技术栈: KB10 <哪一行>

## 子系统清单
| 子系统 | 方案 | 接口 | 备注 |

## 签字需求表（★用户逐项确认）
| # | 需求 | 指标 | 确认 |
|---|------|------|------|
| 电源 | 轨/电压/最坏电流 | … | ☐ |
| 接口数量 | PWMx? UARTx? I2C? ADCx? QEIx? | … | ☐ |
| 每外设接口+电平 | … | … | ☐ |
| 连接器 | … | … | ☐ |

## 待确认/风险（不擅自默认）
- …（源自 problem.yaml.ambiguities）
```

## 注意
- 需求表是后面 `select-parts`/`power-design`/`interconnect` 的输入契约，**数字要硬**。
- `camera_allowed=false` 时整条视觉链改纯灰度/电磁，务必在方案顶部红字提示。
