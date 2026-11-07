---
name: find-repos
description: Finds and evaluates open-source reference repositories with GitHub CLI plus web search, and traces real implementations from code literals with Grep MCP. Use when users ask for reference projects, competing implementations, GitHub repositories, code usage examples, or 准备从零实现常见通用功能时。
metadata:
  author: chaochun
  version: "1.0"
  source: dulk-dev/my-skills
---

# Find Repos

用 GitHub CLI + WebSearch 找项目，用 Grep MCP 找代码。默认给出经过评估的候选，不自动 clone 仓库。

## Search channels

- **`gh search repos`**：结构化索引，直接拿 owner/repo、stars、license、pushedAt；适合成熟项目的精确检索。
- **WebSearch**：覆盖面互补——GitHub 索引之外的页面（GitHub Topics、中文社区、博客评测、marketplace）、同义词措辞变体、以及口碑验证。两者结果合并去重。
- **Grep MCP**：按代码字面量反查实现。

## When to suggest

当用户即将从零实现常见、通用且已有成熟开源方案的功能时，可以主动建议先找参考：

> 这个功能已有不少开源实现。要不要先找几个高质量项目对比，再决定怎么做？

每次会话最多建议一次。用户拒绝后不再提；原创研究、私有业务逻辑或用户已指定实现时不建议。未经用户同意，不执行主动建议中的搜索。

## Choose a workflow

- 用户描述目标、品类或功能：走「找参考仓库」。
- 用户提供代码字面量、函数调用、报错文本或正则：走「按代码找实现」。
- 两种线索都有：先用 Grep 定位真实代码，再用 GitHub CLI/WebSearch 补充仓库信息并评估。

## Find reference repositories

1. 提炼 2～4 组搜索词。同一批需求准备**两套措辞**：一套给 `gh search`（关键词式），一套给 WebSearch（场景/问题式，含同义词变体与中文词）。例如「查看多家 coding agent 的用量/额度」→ gh: `"claude codex cursor usage quota"`，web: `"track Claude Code Codex Cursor usage quota tool github"`。
2. 检查 `gh --version` 和 `gh auth status`。缺失时按当前系统的官方方式引导安装或登录，不索取、打印或保存令牌。
3. 用 `gh search repos` 搜索候选，默认排除 archived；先保证相关性，再按 stars 或更新时间缩小范围。
4. 用 WebSearch 补充搜索，触发条件（满足其一）：
   - gh 结果为空、过少或明显漏掉已知方向（用不同措辞重搜一遍）；
   - 需求跨越 GitHub 之外的信息源——中文社区、GitHub Topics 聚合页、博客/评测、marketplace、skill 站；
   - 需要验证已发现候选的口碑（搜「<项目名> 评测 / review / alternatives / 推荐」）。
   WebSearch 摘要可能夸大或过时，只作为线索，不做评估依据。
5. 合并去重后，用 `gh repo view` 或 GitHub API 补齐每个候选的描述、stars、最近更新、license 和关键目录信息。对 WebSearch 发现的候选，额外核对 README 宣称与实际实现是否一致（如声称支持 N 个 provider，看源码目录是否真的实现了）。
6. 按以下顺序评估：
   - 相关性：是否直接解决用户的问题。
   - 活跃度：近期是否仍有提交、发布或 issue 维护。
   - 人气：stars 仅用于同类候选间相对比较。
   - 可借鉴性：license、代码边界、文档和实现复杂度是否适合参考。
7. 输出 3～5 个最佳候选，并明确推荐一个。

示例命令：

```sh
gh search repos "rag language:go stars:>1000" --archived=false --limit 20 \
  --json fullName,description,stargazersCount,pushedAt,url,license
```

## Find implementations from code

1. 确认 Grep MCP 已配置，并能调用 `searchGitHub`。
2. 搜索真实代码字面量，不使用自然语言问句。优先选择有辨识度的函数调用、错误文本、配置键或连续代码片段。
3. 从精确字面量开始；结果过少再缩短 query，结果过多再加 `repo`、`path`、`language`，必要时启用 `matchCase` 或 `useRegexp`。
4. 单次结果最多 10 条且无分页。需要更多覆盖时，改写查询，不要把前 10 条当成完整结果集。
5. 遇到限流或瞬时错误，等待后重试一次；仍失败则进入 fallback。
6. 汇总命中的仓库与文件位置，再用 GitHub CLI 补充仓库维度信息并执行同一套评估。

Grep MCP 端点为 `https://mcp.grep.app`，无需认证。常见配置形态：

```json
{
  "mcpServers": {
    "grep": {
      "url": "https://mcp.grep.app"
    }
  }
}
```

不同 Agent 的配置文件位置和字段可能不同，应按其 MCP 文档适配，并用一次真实字面量查询验收。

## Output

| 仓库 | 匹配理由 | Stars | 最近更新 | License |
|---|---|---:|---|---|
| owner/repo | 一句话说明与需求的直接关系 | 1.2k | YYYY-MM-DD | MIT |

表格后补充：

- **推荐**：选择一个，并说明最关键的取舍。
- **风险**：指出停止维护、无 license、过度复杂或匹配不完整等问题。无 license 不代表可以自由复用代码。
- **下一步**：询问是否需要 clone 推荐仓库并阅读关键实现。只有用户明确同意后才能 clone。

## Fallback

- `gh` 不可用或未登录：只用 WebSearch + 公开 GitHub API/网页完成候选搜索，仍按上述流程评估；任务完成后附上安装建议。
- Grep MCP 不可用：不要把网页 REST 接口描述为可靠替代。给出可复制的精确查询词和筛选条件，引导用户在 `grep.app` 网页手动搜索，并继续评估用户提供的结果。
- 任一工具失败时，明确说明降级造成的覆盖范围限制，不编造 stars、活跃度、license 或搜索结果。
