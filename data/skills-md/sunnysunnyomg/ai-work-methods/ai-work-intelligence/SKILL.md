---
name: ai-work-intelligence
description: Use when deciding which parts of a task need model judgment, deterministic code, human choice, or an exception path, especially when exploration is becoming repeatable automation.
---

# AI 与程序边界

按不确定性、变化、可核验性和错误代价拆分工作，不按“AI任务”整块分配。

先尝试单次判断、小程序或已有流程。AI探索歧义与变化；规则和输入输出稳定的重复部分交给程序；用户保留未确定价值取舍。固定流程也能含AI，Agent也能用脚本。

固化前用正常和反例样本检查真实输出。稳定运行不等于理解正确：否定、相近实体和高代价语义需要相应能力与审核。只在异常或边界触发时回到模型判断，不把每次LLM复核设为必经步骤。

要把探索变自动化，读 [automation.md](references/automation.md)；存在语义歧义或降级选择，读 [judgment.md](references/judgment.md)。

形成可执行分工：哪段代码运行、例外何时触发、由谁判断、怎样确认输出。失败有限恢复；缺真实事实就保留未知，不补造结果。不反向调用入口。
