---
name: data-prep
description: 读取 CUMCM 附件、做质量检查与可复现预处理，不覆盖 raw。在已选型且存在附件或必须外源数据时使用。禁止编造题外“权威数据”并写成实测。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N4
---

# data-prep

## 何时使用

必须使用：有附件；或模型需要整理字段。

禁止使用：把 raw 文件改掉；用题面没有的数字填表却不标「假设」。

## 循环

目标：`data/processed/` 可被代码读取；有质量报告；原始文件哈希或副本仍在 raw。

`max_rounds`: 3

## 步骤

1. 只读 `data/raw/` 与 `problem/` 附件。列出维度、类型、单位、缺失、重复、明显越界。
2. 不需要处理则写明原因，跳到输出。
3. 需要处理：方法必须写依据（缺失机制、异常定义）。禁止无说明的均值填充作为唯一策略。
4. 代码写在 `src/data_preprocess.py`（或 MATLAB 对等），路径用相对路径，固定输出到 `data/processed/`。
5. 报告写入 `results/tables/data-quality.md`：处理前后各给出可抽查的行数/统计。

## 验收

- [ ] raw 未被覆盖
- [ ] 报告写清每个被改动字段
- [ ] 代码不依赖本机绝对路径
- [ ] 无来源的新列必须标为衍生或假设

## 输出

`data.*`。`status=data_ready`。

## 下一跳

`assumption-set`。
