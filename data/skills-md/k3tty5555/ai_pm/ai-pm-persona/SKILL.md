---
name: ai-pm-persona
description: >-
  产品分身技能。分析你的历史需求文档，学习你的写作风格、措辞习惯和结构偏好。让 AI 生成的 PRD 越来越像你写的。
  当用户说「学习我的风格」「让PRD像我写的」「分析我的文档」「风格设置」「个性化PRD」
  「我想让输出更像我的语气」「训练分身」「风格模仿」时，立即使用此技能。
argument-hint: "[命令: analyze/list/apply/reset] [PRD文件路径 | 风格名]"
allowed-tools: Read Write Edit Bash(mkdir) Bash(ls) Bash(grep)
---

# ai-pm-persona - 产品分身

> 学习你个人的 PRD 写作风格，而不是模仿通用 PM 范式

## 角色说明

- 产品分身学习的是**你自己的**写作风格，不是通用最佳实践
- 分析你历史写的 PRD，提取个人化特征（用词、句式、结构偏好）
- 越用越准：分析的文档越多，风格画像越精准

## 命令路由

| 命令 | 说明 |
|------|------|
| `analyze [PRD文件路径]` | 分析该文件的写作风格，保存为风格档案 |
| `list` | 列出所有已保存的风格档案 |
| `apply [风格名]` | 将指定风格设为当前生效风格 |
| `show` | 展示当前生效风格的特征摘要 |
| `reset` | 清除当前风格设置，恢复默认 |

## 风格分析维度

分析时覆盖以下五个维度：

1. **用词偏好** - 正式 / 口语化 / 专业术语使用频率
2. **句式长度** - 短句 / 长句比例（以标点断句统计）
3. **章节结构** - 习惯的章节顺序和命名方式
4. **举例习惯** - 是否常用举例、举例的详细程度
5. **措辞风格** - 主动 / 被动语态、确定性措辞 / 模糊措辞比例

## analyze 执行步骤

收到 `analyze [路径]` 指令后：

1. 读取指定 PRD 文件（支持 .md / .txt）
2. 逐一分析上述五个维度，形成量化 / 定性描述
3. 从文档中提取 3-5 个最具代表性的原句作为示例
4. 提示用户为本次风格档案命名（默认用文件名）
5. 将档案保存到 `templates/prd-styles/{风格名}/style-profile.json`
6. 输出分析摘要，供用户确认

## 风格档案格式

存储路径：`templates/prd-styles/{风格名}/style-profile.json`

```json
{
  "name": "风格名",
  "source_files": ["文件路径"],
  "analyzed_at": "日期",
  "features": {
    "tone": "正式 / 口语化",
    "sentence_length": "短 / 中 / 长",
    "structure_preference": "章节偏好描述",
    "example_frequency": "高 / 中 / 低",
    "writing_traits": ["特征1", "特征2"]
  },
  "sample_sentences": ["代表性句子1", "代表性句子2"]
}
```

## apply 执行步骤

收到 `apply [风格名]` 指令后：

1. 确认 `templates/prd-styles/{风格名}/style-profile.json` 存在
2. 将风格名写入全局激活配置 `templates/prd-styles/.active-persona`
3. 输出确认：已激活风格 `{风格名}`，后续 PRD 生成将参照此风格

## list 执行步骤

扫描 `templates/prd-styles/` 目录，列出所有含 `style-profile.json` 的子目录，展示：
- 风格名称
- 来源文件数量
- 分析日期
- 当前是否生效（标记 ★）

## show 执行步骤

读取 `templates/prd-styles/.active-persona` 获取当前生效风格名，
加载对应 `style-profile.json`，以可读格式输出五维特征 + 代表性句子示例。

## reset 执行步骤

删除 `templates/prd-styles/.active-persona` 文件，
输出确认：已恢复默认风格，后续 PRD 将使用系统内置模板。

## 与主技能集成

`ai-pm` 在生成 PRD（Phase 5）时：
1. 检查 `templates/prd-styles/.active-persona` 是否存在
2. 若存在，加载对应风格档案，调整措辞和结构偏好
3. 若不存在，使用 `templates/prd-styles/default/style-config.json`

