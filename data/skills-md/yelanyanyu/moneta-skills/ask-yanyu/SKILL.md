---
name: ask-yanyu
description: 当用户想使用、选择、改进或质疑 Moneta 的单词解析、短语解析、写作审查及相关 skills 时，使用这个入口技能。它像 ask-matt 一样介绍可用路径，并只引导一个下一步。
---

# Ask Yanyu

这是 Moneta skills 的入口。

- 第一次在项目里使用 Moneta skills：使用 `/setup-moneta-skills`。
- 要生成或更新英语单词笔记：使用 `/word-disclosure`。
- 要解析词组：使用 `/phrase-disclosure`。如果这个 skill 还不存在，先建议创建它。
- 要做写作审查：使用 `/write-review`。如果这个 skill 还不存在，先建议创建它。
- 用户指出内容怪、不自然、AI 味、翻译腔：使用 `/moneta-critique`。
- 用户确认某个问题应当成为长期规则：使用 `/moneta-skills-improver`。它可以改 `skills/<skill-name>/SKILL.md` 和 `skills/<skill-name>/references/*.md`，例如 `skills/word-disclosure/references/ERROR_INDEX.md`、`STYLE.md`、`CORRECTIONS.md`、`SOURCES.md`。
- 用户说纠错样本太长、重复、需要压缩：使用 `/moneta-skills-improver`。
- Moneta skills 已经改进完：提醒用户 commit；需要同步到其他环境时提醒 push。

一次只引导一个下一步。不要让用户操心 corrections、references、skill sync 这些内部细节。
