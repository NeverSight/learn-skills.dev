---
name: firmware-scaffold
description: 生成控制 lane 的固件工程骨架（4 层架构 + 时间片调度 + FSM + PID + VOFA + K230 协议）。当用户要"生成固件/工程骨架""搭固件框架""出 MSPM0/STM32 工程"时使用。复用知识库 08 的分层与调度，引脚据 contracts/pinmap.yaml，K230 收帧用 contracts/protocol.h。控制参数=占位待整定，外设 init 需人工核对。
---

# firmware-scaffold —— 固件骨架（流水线 ⑦，控制 lane）

**lane**: 控制（DeepSeek/GLM 擅长代码）  ·  **门**: 编译 + 外设 init 人工核对

复用 KB `kb/08-软件架构与调试工程化.md` 的 **4 层架构 + 裸机时间片调度 + FSM + VOFA**，**别另发明**。控制参数(PID/阈值)一律占位待整定。

## 前置
`design/solution.md`、`contracts/pinmap.yaml`（pinmux PASS 过）、`contracts/protocol.h`（已生成）。

## 生成结构（写到 `firmware/`）
```
firmware/
  README.md            # 编译/烧录说明(指向 env/control.md)，分层纪律
  app/    app_mission.c # FSM 跑流程(取药→巡线→识别→送达→返航→停)
          app_track.c   # 循迹决策(灰度质心/K230偏差 → 外环PID)
  middleware/ pid.{c,h} scheduler.{c,h} filter.{c,h} fsm.{c,h} vofa.{c,h}   # 与芯片无关, 可主机编译
  driver/ motor.{c,h} encoder.{c,h} imu.{c,h} k230_uart.{c,h} oled.{c,h}    # 调 DriverLib, 据 pinmap
  bsp/    pinmap.md     # 由 pinmap.yaml 导出的引脚配置表(导入 SysConfig 用)
          ti_msp_dl_config.placeholder  # 提示用 SysConfig 生成
  contracts/protocol.h  # 从 ../../contracts/ 复制或软链(K230 收帧, 勿手改)
  tests/  host_test.c   # 主机可编译: 验 pid + scheduler + protocol 往返
```

## 步骤
1. **中间件（可移植、可主机编译，先写实）**：`pid.c`（位置式+增量式，抗积分饱和）、`scheduler.c`（KB08 时间片表）、`fsm.c`、`vofa.c`（JustFloat）。这些不依赖 MCU，必须能 `cc` 过并跑通单测。
2. **驱动层（据 pinmap 出桩）**：`motor.c`(PWM+方向, 引脚取自 pinmap 的 motor* 信号)、`encoder.c`(QEI)、`k230_uart.c`(用 `protocol.h` 的 `proto_parse_byte`)、`imu.c`、`oled.c`。调 DriverLib 处标 `// TODO: SysConfig/DriverLib`。
3. **应用层**：`app_mission.c` 用 KB08 的 FSM 模板（状态/事件分离），`app_track.c` 外环 PID。
4. **bsp/pinmap.md**：把 `contracts/pinmap.yaml` 转成"引脚-功能-外设"表，供用户在 SysConfig 里照配（**生成 .syscfg 需在 CCS 内做**，这里出配置清单）。
5. **协议**：复制 `contracts/protocol.h` 到 `firmware/contracts/`（或软链），K230 收帧只用它。
6. **主机自测**：`tests/host_test.c` 编译运行，验 PID 阶跃、调度器节拍、protocol 往返。
7. **门**：`README` 写清编译/烧录（指 env/control.md）；提醒用户**逐项核对外设 init**（时钟树/PWM 频率/ADC 采样/中断优先级）对照参考手册；**所有 PID 增益/阈值是占位，须在真车整定**。

## 异构模型友好
中间件/驱动是纯代码活，DeepSeek/GLM lane 可跑；正确性交**编译 + host_test**。控制环时序与电机安全逻辑(限流/急停)建议人写人审。
