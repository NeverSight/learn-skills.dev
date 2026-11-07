---
name: vision-scaffold
description: 生成算法 lane 的 K230 CanMV 视觉工程骨架（巡线提取/色块/数字识别 + 用 protocol.py 发帧给主控）。当用户要"搭K230视觉/CanMV工程""视觉骨架""巡线/识别脚手架"时使用。收发帧只用 contracts/protocol.py（与主控 protocol.h 同源）。阈值=占位待现场标定。
---

# vision-scaffold —— K230 视觉骨架（流水线 ⑧，算法 lane）

**lane**: 算法（DeepSeek/GLM 擅长代码）  ·  **门**: 语法检查 + 现场标阈值

K230 是独立板，可桌面独立开发。**发帧只用 `contracts/protocol.py`**（与主控 `protocol.h` 同源同签名，杜绝漂移）。

## 前置
`design/solution.md`（视觉要做什么）、`contracts/protocol.py`（已生成）。

## 生成结构（写到 `vision/`）
```
vision/
  README.md          # CanMV 烧录/运行(指向 env/vision.md), 镜像版本锁定提醒
  main.py            # 主循环: 取流 → 处理 → 用 protocol.py 发帧
  line_follow.py     # 巡线: 取一行/多行, 求中线偏差 error(int16)
  blob_track.py      # 色块/光点: find_blobs → cx,cy
  digit_recog.py     # 门牌数字: KPU/模板, 出 class_id+confidence
  protocol.py        # 从 ../contracts/ 复制(勿手改)
  config.py          # ★ 阈值/ROI/曝光 占位, 现场标定
```

## 步骤
1. `main.py`：CanMV 初始化（sensor/lcd），主循环里按当前任务调 line_follow/blob_track/digit_recog，把结果用 `protocol.line_error()/blob_xy()/target_class()` 经 UART 发出。硬件相关 import（sensor/image/lib）放运行时，保证**主机 `py_compile` 语法可过**。
2. `line_follow.py`：灰度/二值化取中线，输出 `error`（中线相对画面中心的偏差，int16）。阈值放 `config.py`。
3. `blob_track.py`：`find_blobs` 取最大色块 cx,cy。
4. `digit_recog.py`：KPU 模型或模板匹配，出 `class_id`+`confidence`；**连续 N 帧一致才采信**（防误识，呼应 KB08 FSM）。
5. `config.py`：所有阈值/ROI/曝光/串口波特(115200)集中放，标"现场标定"。
6. 复制 `contracts/protocol.py` 到 `vision/`。
7. **门**：`README` 写运行步骤 + **镜像版本须与队伍锁定一致**；阈值现场标（见 test-checklist）。

## 与主控对接
- 帧格式由 `contracts/protocol.py` 决定；改协议找 lead 改 `protocol.yaml` 重生成，**不要在 K230 端硬编**。
- 联调：K230 发 → 主控 `k230_uart.c` 的 `proto_parse_byte` 收，串口助手可旁观 `AA 55 .. 0D`。
