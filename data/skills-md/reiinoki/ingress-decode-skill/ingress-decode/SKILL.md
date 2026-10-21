---
name: ingress-decode
description: >-
  分析和破解 Ingress Passcode 谜题，涵盖 passcode 格式、经典密码算法、keyword
  识别、多层解密链路、工具扫描与实战排错。用户要求解 Ingress 密文、判断候选
  passcode、识别相关编码，或复盘 Decode 解题过程时使用。
---
# Ingress Passcode Decode

## 1. 执行流程

1. 读取 `references/workflow.md`，保存原始题面，生成字符概况，并记录每层假设、参数和输出。
2. 来源已知时尽早读取 `references/passcode-format.md`，把格式作为分段线索；最终再用它验证，避免只按期望格式硬切。
3. 根据字符集和题面线索，按需读取 `references/cipher-patterns.md` 的相关算法章节。
4. 题面包含图片、动画、二维码、颜色、地图或页面隐藏信息时，读取 `references/image-clues.md`。
5. 需要完整复盘时读取 `references/examples.md`；先检查案例的验证状态。
6. 基础变换较多时运行 `scripts/quick_decode.py`，把输出当作候选而不是答案。需要 key 或自定义参数的算法要单独调用对应函数。
7. 返回解题链路、候选结果、可信度和仍未解释的线索；不能复现时明确标为未验证。

## 2. 按需资源

| 文件 | 读取时机 |
| --- | --- |
| `references/workflow.md` | 每次解题；包含标准流程、排错清单和记录模板 |
| `references/cipher-patterns.md` | 需要识别或执行 Atbash、ROT、Base64、Morse、盲文、键盘、矩阵等变换时 |
| `references/image-clues.md` | 需要检查图片、OCR、二维码、元数据、颜色、动画、地图或页面线索时 |
| `references/passcode-format.md` | 判断最终结构、keyword 和 Ingress lore 线索时 |
| `references/examples.md` | 需要完整案例、异常来源勘误或复盘方法时 |
| `scripts/quick_decode.py` | 需要批量运行基础变换或调用确定性函数时 |

## 3. 验证要求

- 保留原始字符、大小写、空格、换行和标点。
- 为每一步说明触发线索、使用规则、输入和输出。
- 用标准码表、可重复计算或脚本验证结果，不因结果可打印或像 passcode 就判定正确。
- 确认最终每一段都有来源，keyword 受题面支持，并记录未解释信息。
- 同一来源有多个 code 时，检查拆分、共享 key、跨题依赖和“一串多码”，不要默认各题独立。
- 不把 `references/examples.md` 中标为“未验证”的来源结论当作标准答案。

## 4. 工具

```powershell
python scripts/quick_decode.py "<密文>"
```

无参数运行可查看内置示例：

```powershell
python scripts/quick_decode.py
```
