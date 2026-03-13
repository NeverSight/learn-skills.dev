---
name: de-ai-writing
description: "去除中文文档中的 AI 味，输出更具体、更有立场、可核验的表达。Use when 用户要求“去AI味/改写成人话/减少模板感/降低宣传腔/清理空话”，或需要对文章、汇报、方案、邮件进行诊断+改写，支持 quick/standard/deep 与多种风格。"
---

# De-AI Writing

把“语气替换”升级成“信息升级”：先诊断 AI 味症状，再补足事实与取舍，最后按指定风格改写。

## Quick Start

1. 先拿原文（粘贴文本或文件）。
2. 运行诊断脚本，定位高风险句式。
3. 进行最少量采访，补齐事实缺口。
4. 按目标风格改写，保留原意，禁止编造。
5. 用自检清单做最后一轮精炼。

## Workflow

### Phase 1: Intake

让用户提供：
- 原文（100 字以上效果更稳定）
- 文档类型（汇报/方案/邮件/文章）
- 受众（老板/客户/同事/大众）
- 目标动作（读完希望对方做什么）
- 目标风格（见下方风格模式）

如果信息不足，先问 5-10 个问题，不要直接改写。

### Phase 2: Diagnose

执行：

```bash
python3 skills/de-ai-writing/scripts/ai_taste_lint.py \
  --input-file /path/to/input.txt \
  --mode standard \
  --format markdown
```

没有文件时可用：

```bash
python3 skills/de-ai-writing/scripts/ai_taste_lint.py \
  --text "待分析文本" \
  --mode quick \
  --format json
```

根据报告提取前 3 个问题作为本轮改写重点。

### Phase 3: Fill Gaps (Interview)

针对缺口补充事实，不超过 10 问。优先拿到：
- 关键数字（目标值、现状值、时间）
- 选择与取舍（选 A 不选 B 的原因）
- 风险与代价（可接受/不可接受）
- 可核验来源（数据口径、时间范围）

缺口数据拿不到时，用 `【缺口：...】` 标注，不得虚构。

### Phase 4: Rewrite

按“事实优先 + 立场明确 + 句式有节奏”改写。

硬规则：
- 不新增用户未提供的事实、数字、引述。
- 删掉含糊归因（如“专家认为”）或补齐来源。
- 删宣传词和空泛形容词，换成可核验描述。
- 每段至少有一个“推进句”：结论/取舍/动作。

### Phase 5: Self Check

用 `references/self-checklist.md` 自检，不通过就继续压缩和改写。

## 风格模式（可选）

- `务实简洁`：短句优先，结论先行，信息密度高。
- `专业克制`：术语准确，语气稳健，适合对外文档。
- `强结论`：立场鲜明，明确建议与不建议。
- `叙事说明`：强调背景-冲突-选择-结果，适合复盘。

改写前先确认模式；未指定时默认 `务实简洁`。

## Output Contract

始终输出三段内容：

1. `改写正文`
2. `修改理由清单`
3. `缺口与风险`

格式：

```markdown
## 改写正文
[最终版本]

## 修改理由清单
- 原句问题 -> 修改动作 -> 预期收益

## 缺口与风险
- 【缺口：...】
- 可能影响：...
```

## References

按需读取，不要一次性全部加载：
- 规则：`references/symptom-rules.md`
- 提示词模板：`references/prompt-pack.md`
- 终检清单：`references/self-checklist.md`
