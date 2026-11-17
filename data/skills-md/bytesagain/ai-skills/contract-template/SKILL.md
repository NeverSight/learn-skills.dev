---
version: "2.0.0"
name: contract-template
description: "Contract and agreement template generator. 合同模板、合同范本、协议书、contract template、劳动合同、employment contract、劳动协议、保密协议NDA、non-disclosure agreement、租赁合同、租房合同、lease agr."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# contract-template

合同和协议模板生成器。劳动合同、保密协议、合作协议、租赁合同。

## 为什么用这个 Skill？ / Why This Skill?

- **标准条款**：内置常见合同必备条款（甲乙方信息、权利义务、违约责任、争议解决等）
- **即填即用**：生成的模板留有明确的填写位置，直接填信息就能用
- **多种类型**：劳动合同、NDA、服务协议、租赁合同，覆盖常见场景
- Compared to asking AI directly: structured legal templates with standard clauses, fill-in-the-blank format, and proper legal formatting

## Usage

Run the script at `scripts/contract.sh`:

| Command | Description |
|---------|-------------|
| `contract.sh labor "甲方" "乙方"` | 劳动合同模板 |
| `contract.sh nda "甲方" "乙方"` | 保密协议NDA |
| `contract.sh service "甲方" "乙方" "服务内容"` | 服务协议 |
| `contract.sh rental "房东" "租客" "地址"` | 租赁合同 |
| `contract.sh help` | 显示帮助信息 |

## Examples

```bash
# 劳动合同
bash scripts/contract.sh labor "北京科技有限公司" "张三"

# 保密协议
bash scripts/contract.sh nda "甲方公司" "乙方公司"

# 服务协议
bash scripts/contract.sh service "委托方" "服务方" "软件开发与维护"

# 租赁合同
bash scripts/contract.sh rental "李四" "王五" "北京市朝阳区XX路XX号"
```
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com
