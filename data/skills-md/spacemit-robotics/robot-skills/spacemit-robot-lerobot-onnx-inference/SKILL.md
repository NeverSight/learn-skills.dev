---
name: spacemit-robot-lerobot-onnx-inference
description: >-
  components/thirdparty/lerobot/examples/onnx_inference 的 ACT 与 SmolVLA
  ONNX 部署专项入口；用于模型下载、PC 导出/量化/FP16 图修复、数值对比、K3
  C++ benchmark、dry-run 和 SO-101 真机运行。
metadata:
  requires:
    bins: ["bash", "python3", "cmake", "curl"]
  sdk:
    module_paths:
      - components/thirdparty/lerobot/examples/onnx_inference
    primary_docs:
      - components/thirdparty/lerobot/examples/onnx_inference/README.md
      - components/thirdparty/lerobot/examples/onnx_inference/tools/README.md
      - components/thirdparty/lerobot/examples/onnx_inference/cpp/README.md
      - components/thirdparty/lerobot/examples/onnx_inference/python/README.md
      - components/thirdparty/lerobot/examples/onnx_inference/test.yaml
    build_hint: single_package_first
---

# SpacemiT ONNX inference

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用规则。
无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)，不要在 `robot-skills` 仓库里直接运行部署命令。

## 何时使用

- 用户要部署、验证或调试 `examples/onnx_inference` 下的 ACT / SmolVLA ONNX 示例。
- 用户要下载示例模型、从 PyTorch checkpoint 导出 ONNX、量化 ACT INT8、转换 SmolVLA FP16 或执行 FP16 图修复。
- 用户要在 K3 上跑 ACT / SmolVLA benchmark、数值对比、dry-run 或 SO-101 真机运行。

## 默认规则

- `build_hint`: `single_package_first`，但本目录主要使用自带 Python / C++ 脚本，不默认执行 `mm`。
- SDK 内模块路径：`$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference`。
- 测试入口优先使用 `scripts/test/robot-test`；只有测试失败、用户要手工复现或需要改模型导出流程时，才直接执行底层工具脚本。
- SmolVLA K3 fp16 路径必须使用补丁版 `spacemit-ort.riscv64.2.0.4_yyx`；默认下载源是 `https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/spacemit-ort-sdk/spacemit-ort.riscv64.2.0.4_yyx.tar.gz`。
- SmolVLA 已发布示例模型默认使用 `so101_smolvla_pick_green_cube_2cam_100k_fp16_surgeried`，C++ benchmark 参考性能约 `1127.5 ms`，`--denoise-steps 10`。
- PC 导出 SmolVLA 时使用 Python 3.12 环境和 `requirements-smolvla-pc.txt`；K3 只做 EP 运行、数值对比、benchmark 和真机验证。
- 不默认先读长 README；只有命令细节、参数语义或执行失败时，才回读 `primary_docs`、脚本源码或 CMake 文件。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK，至少包含 `build/`、`components/`、`application/`、`target/`。
2. 进入 SDK 根目录，先列测试：`./scripts/test/robot-test list components/thirdparty/lerobot/examples/onnx_inference`。
3. 若用户要求“跑测试 / CI 验证 / PR 验证”，优先跑 `pr` functional。
4. 若用户要求“测性能 / K3 benchmark / scheduled 测试”，必须跑 `scheduled` performance；该 scope 覆盖 ACT 和 SmolVLA，会真实下载或复用发布模型，构建 C++，并在 K3 上跑 SpaceMIT EP benchmark。
5. 遇到 K3 真机任务时，先确认目标机、登录用户、模型路径、SDK 路径、相机映射和 `/dev/ttyACM*`；不要凭旧板卡地址或相机编号下结论。
6. 根据用户意图选择 ACT 或 SmolVLA；不要把 ACT INT8 流程套到 SmolVLA，也不要把 SmolVLA FP16 图修复要求套到 ACT。
7. 修改或生成 ONNX 模型后，先跑 `compare_*_onnx.py` 做数值验证，再跑 benchmark；benchmark 不能替代数值正确性检查。

## Robot-test 用例

当用户说“测试 onnx_inference”“跑一下 ONNX CI”“测 SmolVLA K3 性能”时，直接按下面顺序执行：

```bash
cd "$SROBOTIS_ROOT"
./scripts/test/robot-test list components/thirdparty/lerobot/examples/onnx_inference
```

PR 轻量验证：

```bash
./scripts/test/robot-test run components/thirdparty/lerobot/examples/onnx_inference \
  --scope pr --category functional
```

K3 scheduled 性能测试会覆盖 ACT 和 SmolVLA：

```bash
./scripts/test/robot-test run components/thirdparty/lerobot/examples/onnx_inference \
  --scope scheduled --category performance
```

返回结果时至少包含测试名、scope、是否通过、日志路径、SmolVLA 平均推理耗时、阈值、EP SDK 路径、模型目录、benchmark 输入模式和失败点。
ACT 用例返回 `act_benchmark` 平均/中位/min/max 延迟；SmolVLA 用例返回完整推理平均/min/max 延迟。

性能用例常用环境变量：

- `SMOLVLA_PERF_ITERS`：正式计时轮数，默认 `3`。
- `SMOLVLA_PERF_WARMUP`：warmup 轮数，默认 `1`。
- `SMOLVLA_PERF_MAX_AVG_MS`：平均延迟阈值，默认 `1600`。
- `SMOLVLA_CALIBRATION`：SO-101 标定文件路径；缺 runtime metadata 时用于生成 `smolvla_runtime.txt`。
- `ACT_PERF_ITERS` / `ACT_PERF_WARMUP`：ACT benchmark 轮数和 warmup，默认 `20` / `3`。
- `ACT_PERF_MAX_AVG_MS`：ACT INT8 平均延迟阈值，默认 `500`。
- `ACT_CALIBRATION`：ACT norm stats 生成时使用的 SO-101 标定文件路径。

## SmolVLA 部署

### 下载示例模型与 EP SDK

```bash
cd "$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference"
mkdir -p models/pytorch models/onnx /tmp/smolvla_models

curl -L \
  https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/models/pytorch/so101_smolvla_pick_green_cube_2cam.tar.gz \
  -o /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam.tar.gz
curl -L \
  https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/models/onnx/so101_smolvla_pick_green_cube_2cam_100k_fp32.tar.gz \
  -o /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam_100k_fp32.tar.gz
curl -L \
  https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/models/onnx/so101_smolvla_pick_green_cube_2cam_100k_fp16_surgeried.tar.gz \
  -o /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam_100k_fp16_surgeried.tar.gz
curl -L \
  https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/spacemit-ort-sdk/spacemit-ort.riscv64.2.0.4_yyx.tar.gz \
  -o /tmp/smolvla_models/spacemit-ort.riscv64.2.0.4_yyx.tar.gz
```

解压后创建固定软链：

```bash
tar -xzf /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam.tar.gz -C models/pytorch
tar -xzf /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam_100k_fp32.tar.gz -C models/onnx
tar -xzf /tmp/smolvla_models/so101_smolvla_pick_green_cube_2cam_100k_fp16_surgeried.tar.gz -C models/onnx
tar -xzf /tmp/smolvla_models/spacemit-ort.riscv64.2.0.4_yyx.tar.gz -C ~

ln -sfn so101_smolvla_pick_green_cube_2cam_100k_fp32 models/onnx/smolvla-fp32
ln -sfn so101_smolvla_pick_green_cube_2cam_100k_fp16_surgeried models/onnx/smolvla-fp16-surgeried
mkdir -p models/pytorch/smolvla/checkpoints/100000
ln -sfn ../../../so101_smolvla_pick_green_cube_2cam/checkpoints/100000/pretrained_model \
  models/pytorch/smolvla/checkpoints/100000/pretrained_model
```

### PC 导出、FP16 转换与图修复

```bash
cd "$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference"
pip install -r requirements-smolvla-pc.txt

python tools/export_smolvla_4model_to_onnx.py \
  --checkpoint models/pytorch/smolvla/checkpoints/100000/pretrained_model \
  --output-dir models/onnx/smolvla-fp32 \
  --num-cameras 2 \
  --validate-load

python tools/convert_smolvla_fp32_to_fp16.py \
  --input-dir models/onnx/smolvla-fp32 \
  --output-dir models/onnx/smolvla-fp16

python tools/surgery_smolvla_fp16.py \
  --input-dir models/onnx/smolvla-fp16 \
  --output-dir models/onnx/smolvla-fp16-surgeried
```

图修复内容必须包含：

- `vision_encoder` self-attention 核心融合为 `VisionSelfAttnNHWC`，MLP GELU 近似子图替换为 ONNX `Gelu(approximate="tanh")`。
- `prefill_lm` / `denoise_step` RMSNorm 关键计算 fp32 化。
- `prefill_lm` / `denoise_step` scatter 写入算子降解。

### 数值验证

先做 CPU 对比，再在 K3 用 EP204 SDK 对比：

```bash
python tools/compare_smolvla_onnx.py \
  --fp32-dir models/onnx/smolvla-fp32 \
  --fp16-dir models/onnx/smolvla-fp16-surgeried \
  --cpu \
  --num-cameras 2 \
  --denoise-steps 10

python tools/compare_smolvla_onnx.py \
  --fp32-dir models/onnx/smolvla-fp32 \
  --fp16-dir models/onnx/smolvla-fp16-surgeried \
  --use-spacemit-ep \
  --spacemit-ort-dir ~/spacemit-ort.riscv64.2.0.4_yyx \
  --ep-threads 8 \
  --ep-affinity "8;9;10;11;12;13;14;15" \
  --num-cameras 2 \
  --denoise-steps 10
```

返回结果时至少报告 `finite fp32/fp16`、max/mean/p95/p99 diff、EP SDK 路径和 denoise steps。

### C++ benchmark 与真机

先导出 runtime metadata；首次部署或换机械臂前先校准 SO-101：

```bash
python tools/export_smolvla_runtime.py \
  --checkpoint models/pytorch/smolvla/checkpoints/100000/pretrained_model \
  --output models/onnx/smolvla_runtime.txt \
  --task "Place the green cube into the box" \
  --num-cameras 2 \
  --calibration ~/.cache/huggingface/lerobot/calibration/robots/so_follower/my_awesome_follower_arm.json
```

构建和 benchmark：

```bash
cd "$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference/cpp"
./build_smolvla_robot_cpp.sh EP204

DRY_RUN=1 WARMUP=4 ./run_smolvla_robot_pipeline.sh \
  --warmup-only --n-action-steps 50
```

真机前先 dry-run：

```bash
./run_smolvla_robot_pipeline.sh \
  --port /dev/ttyACM0 \
  --camera top=15 --camera wrist=13 \
  --dry-run --max-iters 1 --n-action-steps 25 --print-actions
```

dry-run 通过后再移除 `--dry-run` 真机运行。相机编号必须以当前 K3 实际 `/dev/video*` 为准，不要把文档示例编号当成固定值。

## ACT 部署

### 下载、导出与量化

```bash
cd "$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference"
pip install -r requirements-act-pc.txt

python tools/act_pytorch_to_onnx.py \
  --checkpoint models/pytorch/act/checkpoints/100000/pretrained_model \
  --output-dir models/onnx/act-fp32

python -m xslim \
  -i models/onnx/act-fp32/act.onnx \
  -o models/onnx/act-int8/act.q.onnx \
  --dynq
```

### 数值验证与 C++ benchmark

```bash
python tools/compare_act_onnx.py \
  --model-dir models/onnx/act-fp32 \
  --checkpoint models/pytorch/act/checkpoints/100000/pretrained_model \
  --cpu \
  --with-torch

python tools/export_norm_stats.py \
  --checkpoint models/pytorch/act/checkpoints/100000/pretrained_model \
  --output models/onnx/act-fp32/act_norm_stats.txt

python tools/make_act_test_inputs.py \
  --model-dir models/onnx/act-fp32 \
  --stats models/onnx/act-fp32/act_norm_stats.txt \
  --out-dir cpp/inputs

cd cpp
rm -rf build && mkdir build && cd build
cmake ..
make -j"$(nproc)"

./act_benchmark ../../models/onnx/act-int8/act.q.onnx \
  --images-npy ../inputs/images.npy \
  --state-npy ../inputs/state_deg.npy \
  -s -t 8 -a "8;9;10;11;12;13;14;15" \
  -n 20 -w 3
```

ACT 真机需要 `-DACT_ROBOT_HW=ON` 重新构建，并传入 `--stats`、`--port` 和训练时一致的 `--camera` 名称。

## 禁止事项

- 不要在 `robot-skills` 仓库目录里直接执行 SDK 部署、模型下载或 benchmark 命令。
- 不要把下载的模型、ONNX 产物、EP SDK、日志或相机 dump 提交到 SDK 或 `robot-skills`。
- 不要只跑 benchmark 就宣称数值正确；SmolVLA 必须配套 `compare_smolvla_onnx.py` 或 dry-run 数值检查。
- 不要为 SmolVLA FP16 添加额外环境变量；EP204 SDK 和图修复版模型是默认性能路径。
- 不要写死 K3 IP、root 密码、相机编号或串口编号；每次按用户最新信息和板端设备实际状态确认。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 进入目录 | `cd "$SROBOTIS_ROOT/components/thirdparty/lerobot/examples/onnx_inference"` |
| 列出 ONNX 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/thirdparty/lerobot/examples/onnx_inference` |
| PR 轻量验证 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/thirdparty/lerobot/examples/onnx_inference --scope pr --category functional` |
| K3 scheduled 性能测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/thirdparty/lerobot/examples/onnx_inference --scope scheduled --category performance` |
| 下载 SmolVLA EP204 SDK | `curl -L https://archive.spacemit.com/spacemit-ai/model_zoo/vla/smolvla/spacemit-ort-sdk/spacemit-ort.riscv64.2.0.4_yyx.tar.gz -o /tmp/smolvla_models/spacemit-ort.riscv64.2.0.4_yyx.tar.gz` |
| SmolVLA FP16 图修复 | `python tools/surgery_smolvla_fp16.py --input-dir models/onnx/smolvla-fp16 --output-dir models/onnx/smolvla-fp16-surgeried` |
| SmolVLA 数值对比 | `python tools/compare_smolvla_onnx.py --fp32-dir models/onnx/smolvla-fp32 --fp16-dir models/onnx/smolvla-fp16-surgeried --use-spacemit-ep --spacemit-ort-dir ~/spacemit-ort.riscv64.2.0.4_yyx --ep-threads 8 --ep-affinity "8;9;10;11;12;13;14;15" --num-cameras 2 --denoise-steps 10` |
| SmolVLA C++ 构建 | `cd cpp && ./build_smolvla_robot_cpp.sh EP204` |
| SmolVLA benchmark | `cd cpp && DRY_RUN=1 WARMUP=4 ./run_smolvla_robot_pipeline.sh --warmup-only --n-action-steps 50` |
| SmolVLA dry-run | `cd cpp && ./run_smolvla_robot_pipeline.sh --port /dev/ttyACM0 --camera top=15 --camera wrist=13 --dry-run --max-iters 1 --n-action-steps 25 --print-actions` |
| ACT INT8 benchmark | `cd cpp/build && ./act_benchmark ../../models/onnx/act-int8/act.q.onnx --images-npy ../inputs/images.npy --state-npy ../inputs/state_deg.npy -s -t 8 -a "8;9;10;11;12;13;14;15" -n 20 -w 3` |
