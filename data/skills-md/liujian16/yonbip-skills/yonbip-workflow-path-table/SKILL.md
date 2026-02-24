---
name: yonbip-workflow-path-table
description: Converts natural language business approval workflow descriptions into YonBIP-standard Excel workflow path tables to import workflow definition into YonBIP. Use when user provides approval rules in natural language and needs workflow path tables.
---

# YonBIP Workflow Path Table Generator

Converts natural language business approval workflow descriptions into YonBIP-standard Excel workflow path tables.

## Core Principle: Dynamic Column Extraction

**CRITICAL: Do NOT assume any fixed columns.** Every table structure must be derived from the user's description:

1. **Condition Columns**: Extract all condition dimensions mentioned
   - Examples: 费用类型, 金额, 供应商类型, 部门, 地区, 采购类别, etc.
2. **Role Columns**: Extract ALL roles mentioned in the approval chains
   - Examples: 部门主管, 财务经理, 总经理, 行政主管, 采购专员, 法律顾问, etc.
3. **Build table structure** based ONLY on what's actually in the description

## Core Principle: Mutually Exclusive Conditions

**每一行的条件组合必须是唯一的、互斥的。** 任意给定输入只能匹配唯一一行。

### 为什么互斥很重要？

YonBIP 系统需要根据条件确定唯一的审批路径。如果两行的条件有重叠，系统无法判断应该走哪条路径。

### 互斥规则

1. **同一列的值必须互斥**：对于每个条件列，任意两行的值不能同时匹配同一输入
   - ✅ `< 1000` 和 `>= 1000` 互斥
   - ❌ `全部` 和 `>= 5000` 重叠（"全部"包含">= 5000"）
   - ❌ `< 5000` 和 `>= 3000` 重叠（3000-5000 同时匹配两者）

2. **行组合必须互斥**：即使单列值不互斥，组合后也必须互斥
   - ✅ `行政类采购 | < 5000` 和 `生产类采购 | < 5000` 互斥（采购类别不同）
   - ❌ `行政类采购 | 全部` 和 `行政类采购 | >= 5000` 重叠

3. **使用分区而非叠加**：不要用"全部"叠加更具体的条件
   - ❌ 错误：先写"全部"的规则，再叠加">= 5000"的规则
   - ✅ 正确：按金额区间分区：`< 5000` 和 `>= 5000`

### 金额区间的标准分区方式

```
< 1000           →  小于1000
[1000, 5000)     →  1000到5000以下（含1000，不含5000）
>= 5000          →  5000及以上
```

这种分区方式确保每个金额值都能匹配唯一一行。

## Workflow

**Dry Run Mode**: If user specifies `--dryrun` flag:
- Skip Step 0 (clarification)
- Skip Step 4 (Excel generation)
- Only output the markdown table

### Step 0: Understand and Clarify (理解与澄清)

**Skip in --dryrun mode**: If the `--dryrun` flag is set, skip this entire step and proceed directly to Step 1.

After receiving the user's approval rules, first analyze the content:

1. **Understand**: Parse the natural language and identify:
   - The main business scenario (费用类型、采购类型等)
   - Key conditions mentioned (金额区间、供应商类型等)
   - Approval roles and their sequences

2. **Check for Ambiguities**: Determine if the rules are complete and unambiguous:
   - Incomplete condition coverage (是否有遗漏的场景?)
   - Unclear role definitions (角色名称是否明确?)
   - Boundary conditions not specified (边界值如何处理?)
   - Multiple interpretations possible (是否有歧义?)

3. **Decision Point**:
   - **If rules are clear**: Skip directly to Step 1 (no user interaction needed)
   - **If ambiguities exist**: Proceed to clarification

4. **Interactive Clarification** (only if ambiguities exist):
   - First, present your understanding of the rules
   - Then, ask specific questions using AskUserQuestion tool:
     - Present specific questions with clear options
     - Allow "Other" for custom input
     - Wait for user response before proceeding
   - Example: "我理解您的规则是...，但有以下疑问：..."

5. **Proceed to Step 1**: Once the rules are clear (either no ambiguities or user has clarified), proceed to extract and structure the data.

**Typical scenarios requiring clarification:**

1. **条件覆盖不完整**：
   - 规则："1000元以下走A，5000元以上走B"
   - 问题："1000-5000元之间如何处理？"

2. **角色不明确**：
   - 规则："主管审批"
   - 问题："是部门主管还是业务主管？"

3. **边界值歧义**：
   - 规则："1000元以下"和"1000-5000元"
   - 问题："正好1000元走哪条路径？"

4. **默认值/兜底规则**：
   - 规则：只说明了特定场景
   - 问题："其他未说明的场景如何处理？"

### Step 1: Extract and Structure

Analyze the natural language and identify:

**A. All Condition Dimensions (前几列)**

- What categories/dimensions determine the approval path?
- Common patterns: 费用类型, 金额区间, 供应商性质, 部门类型, etc.

**B. All Approval Roles (后几列)**

- Who are the approvers? List ALL unique roles mentioned
- Preserve the exact role names from the description
- Do NOT add roles that aren't mentioned

**C. Approval Logic (表格内容)**

- Map out each scenario's approval sequence
- Use numbers (1, 2, 3...) for approval order
- Use `n/a` for non-participating roles
- Use `N:[condition]` for conditional approvals

### Step 2: Generate Markdown Table

Build the table with extracted columns:

```
| [条件列1] | [条件列2] | ... | [角色1] | [角色2] | [角色3] | ... |
|----------|----------|-----|---------|---------|---------|-----|
| 值A      | 条件X    | ... | 1       | n/a     | 2       | ... |
```

**Validate mutual exclusivity before presenting:**

Check that no two rows have overlapping conditions. If overlap exists:
1. Identify the overlapping rows
2. Refactor using proper partitioning (e.g., split "全部" into specific ranges)
3. Ensure each input matches exactly one row

**Present to user for confirmation.**

### Step 3: User Confirmation

Ask: "请确认以上流程路径表是否正确？如需修改请直接告诉我。"

Wait for approval or modifications.

### Step 4: Generate Excel

After confirmation, use the conversion script to generate Excel file.

write the markdown file to same folder of the Excel file.

**Script location:** `scripts/md_to_excel.py` (within this skill directory)

**Usage:**

```bash
python3 ${SKILL_DIR}/scripts/md_to_excel.py <input.md> <output.xlsx> --condition-cols <N>
```

**Parameters:**

- `--condition-cols N`: 指定前 N 列为"条件"列（如：费用类型、金额区间），其余列为"环节"列（审批角色）

The script will:

- Parse the Markdown table structure
- Add explanation row ("条件" | "环节")
- Apply YonBIP standard formatting (headers, borders, alignment)
- Convert `n/a` to empty cells
- Generate `.xlsx` file

## Examples

### Example 1: 招待费（简单场景）

**Input:**

```
招待费审批规则：1000元以下只需部门主管审批；1000-5000元需要部门主管和财务经理；5000元以上则需要部门主管、财务经理和总经理。
```

**Extracted:**

- Condition columns: 费用类型, 金额
- Role columns: 部门主管, 财务经理, 总经理

**Output:**
| 费用类型 | 金额 | 部门主管 | 财务经理 | 总经理 |
|---------|------|---------|---------|--------|
| 招待费 | < 1000 | 1 | n/a | n/a |
| 招待费 | [1000, 5000) | 1 | 2 | n/a |
| 招待费 | >= 5000 | 1 | 2 | 3 |

### Example 2: 采购审批（多条件+多角色）

**Input:**

```
行政类采购：无论金额，部门负责人(1)→行政主管(2)。超过5000元增加财务总监(3)。
生产类采购：<20000：部门负责人(1)→采购专员(2)→财务总监(3)。
≥20000：部门负责人(1)→采购经理(2)→财务总监(3)→总经理(4)。
新合作方需增加法律顾问。
```

**Extracted:**

- Condition columns: 采购类别, 金额, 供应商类型
- Role columns: 部门负责人, 行政主管, 采购专员, 采购经理, 财务总监, 总经理, 法律顾问

**Output:**
| 采购类别 | 金额 | 供应商类型 | 部门负责人 | 行政主管 | 采购专员 | 采购经理 | 财务总监 | 总经理 | 法律顾问 |
|---------|------|-----------|-----------|---------|---------|---------|---------|--------|---------|
| 行政类采购 | < 5000 | 全部 | 1 | 2 | n/a | n/a | n/a | n/a | n/a |
| 行政类采购 | >= 5000 | 全部 | 1 | 2 | n/a | n/a | 3 | n/a | n/a |
| 生产类采购 | < 20000 | 全部 | 1 | n/a | 2 | n/a | 3 | n/a | n/a |
| 生产类采购 | >= 20000 | 老合作方 | 1 | n/a | n/a | 2 | 3 | 4 | n/a |
| 生产类采购 | >= 20000 | 新合作方 | 1 | n/a | n/a | 2 | 3 | 4 | 5 |

**Note:** 条件互斥 - 每行代表唯一的条件组合，没有重叠。

### Example 3: 差旅费（标准YonBIP角色）

**Input:**

```
差旅费5000元以下走主管和财务；5000-10000增加经理；10000以上全审。
```

**Extracted:**

- Condition columns: 费用类型, 金额
- Role columns: 业务主管, 财务专员, 业务经理, 业务总经理, 总裁 (注意：按出现顺序提取)

**Output:**
| 费用类型 | 金额 | 业务主管 | 财务专员 | 业务经理 | 业务总经理 | 总裁 |
|---------|------|---------|---------|---------|-----------|------|
| 差旅费用 | < 5000 | 1 | 2 | n/a | n/a | n/a |
| 差旅费用 | [5000, 10000) | 1 | 3 | 2 | n/a | n/a |
| 差旅费用 | >= 10000 | 1 | 4 | 2 | 3 | 5 |

## Value Formatting

### Condition Values

- **金额**: `< 5000`, `>= 10000`, `[5000, 10000)`, `全部`
- **类别**: 具体类别名称 (如: 差旅费用, 行政类采购)
- **通用**: `全部` 表示不限制

### Approval Nodes

- **1, 2, 3...**: Approval sequence order
- **n/a**: Role does not participate
- **N:[condition]**: Nth step with additional condition
  - Example: `2:[金额>=500]` = 2nd approver AND amount >= 500

## Common Patterns

**Threshold phrases:**

- "X元以下" → `< X`
- "X元以内" → `<= X`
- "X-Y元" → `[X, Y)`
- "X元以上" → `>= X`

**Chain phrases:**

- "走A和B" → A then B (sequential)
- "增加C" → Add C to chain
- "全审/全部" → All roles participate

**Condition phrases:**

- "如果是X且Y" → Add condition columns
- "满足XX条件" → `N:[XX]`
- "需XX审批" → Add XX role

## Common Mistakes to Avoid

### ❌ 错误：条件重叠

```
| 采购类别 | 金额 | ... |
|---------|------|-----|
| 行政类采购 | 全部   | ... |  ← 与下一行重叠
| 行政类采购 | >= 5000 | ... |  ← "全部"包含了">= 5000"
```

问题：一个6000元的行政类采购会同时匹配两行。

### ✅ 正确：互斥分区

```
| 采购类别 | 金额 | ... |
|---------|------|-----|
| 行政类采购 | < 5000  | ... |  ← 不包含5000
| 行政类采购 | >= 5000 | ... |  ← 从5000开始
```

### ❌ 错误：区间边界重叠

```
| 金额 | ... |
|------|-----|
| < 5000   | ... |
| >= 3000  | ... |  ← 3000-5000 重叠
```

### ✅ 正确：边界明确

```
| 金额 | ... |
|------|-----|
| < 3000      | ... |
| [3000, 5000) | ... |
| >= 5000     | ... |
```

### ❌ 错误：使用"全部"叠加具体条件

当用户说"超过5000元需要额外审批"时，不要生成：
```
| 金额 | 财务总监 |
|------|---------|
| 全部 | n/a |     ← 错误：与下一行重叠
| >= 5000 | 3 |   ← 被上面包含
```

### ✅ 正确：分区覆盖所有情况

```
| 金额 | 财务总监 |
|------|---------|
| < 5000 | n/a |
| >= 5000 | 3 |
```
