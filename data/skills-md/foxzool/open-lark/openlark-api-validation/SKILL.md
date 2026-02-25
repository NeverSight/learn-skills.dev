---
name: openlark-api-validation
description: OpenLark API 覆盖率验证技能。用于验证各 crate 的 API 实现数量与覆盖率，基于 tools/validate_apis.py 脚本和 api_list_export.csv 对比实际代码实现。触发关键词：API 验证、API 覆盖率、验证 API 数量、检查 API 实现、API 统计
argument-hint: "[crate-name|path|bizTag]"
allowed-tools: Bash, Read, Edit, Write
---

# OpenLark API 覆盖率验证技能

## 🧭 技能路由指南

**本技能适用场景：**
- 需要统计某个 crate/bizTag 的 API 覆盖率
- 需要输出缺失 API 清单与完成率报告
- 需要对比 `api_list_export.csv` 与实际落盘实现

**其他技能：**
- 项目级规范体检（架构/API/导出/校验一体）→ `Skill(openlark-code-standards)`
- 新增/重构具体 API → `Skill(openlark-api)`
- 审查整体架构与公共 API 收敛 → `Skill(openlark-design-review)`

### 关键词触发映射

- 覆盖率、缺失 API、实现数量、CSV 对比、验证脚本、报告 → `openlark-api-validation`
- 新增 API、重构 API、Builder、Request/Response、mod.rs 导出 → `openlark-api`
- 代码规范、规范检查、风格一致性、体检 → `openlark-code-standards`
- 架构设计、public API、收敛方案、feature gating、兼容策略 → `openlark-design-review`
- validate、必填校验、validate_required、空白字符串、校验聚合 → `openlark-validation-style`

### 双向跳转规则

- 若发现缺失 API 的根因是架构分层/范式混乱，转 `openlark-design-review`。
- 若发现问题是具体 API 尚未实现，转 `openlark-api` 落地实现。
- 若需要把覆盖率问题归因到全仓规范一致性，转 `openlark-code-standards`。

## 🎯 技能用途

本技能用于验证 OpenLark 项目中各 crate 的 API 实现覆盖率，通过对比 `api_list_export.csv` 中的 API 定义与实际代码实现，生成详细的覆盖率报告。

## 📋 快速工作流

### 1. 验证单个 crate 的 API 覆盖率

```bash
# 验证 openlark-docs crate
python3 tools/validate_apis.py --crate openlark-docs

# 验证 openlark-communication crate
python3 tools/validate_apis.py --crate openlark-communication

# 验证 openlark-meeting crate
python3 tools/validate_apis.py --crate openlark-meeting
```

**输出位置：** `reports/api_validation/{crate}.md`

### 2. 列出所有可用的 crate 映射

```bash
# 查看所有 crate → bizTag 映射
python3 tools/validate_apis.py --list-crates
```

**示例输出：**
```
📄 映射文件: tools/api_coverage.toml

- openlark-analytics: src=crates/openlark-analytics/src biz_tags=[search, report]
- openlark-api: src=crates/openlark-api/src biz_tags=[auth, passport]
- openlark-application: src=crates/openlark-application/src biz_tags=[application]
...
```

### 3. 自定义验证范围

```bash
# 指定源码目录和业务标签
python3 tools/validate_apis.py \
  --csv api_list_export.csv \
  --src crates/openlark-docs/src \
  --filter ccm base baike \
  --output custom_report.md

# 包含旧版本 API
python3 tools/validate_apis.py --crate openlark-docs --include-old
```

### 4. 验证所有 crates（批量）

```bash
# 验证所有 crate 并生成报告
for crate in openlark-docs openlark-communication openlark-meeting openlark-hr; do
  echo "验证 $crate..."
  python3 tools/validate_apis.py --crate $crate
done
```

## 📊 报告解读

### 报告结构

生成的 Markdown 报告包含以下部分：

#### 一、总体统计
- **API 总数**：CSV 中定义的 API 数量
- **已实现**：已实现的 API 数量
- **未实现**：缺失的 API 数量
- **完成率**：实现百分比
- **额外文件**：代码中存在但 CSV 中未定义的文件

#### 二、模块统计
按 bizTag 分组的统计信息，展示各业务域的完成率。

#### 三、未实现的 API
详细列出所有未实现的 API，包括：
- API ID
- 预期文件路径
- API URL
- 文档链接

#### 四、额外的实现文件
列出不匹配 CSV 定义的额外文件（可能是辅助文件或需要更新 CSV）。

#### 五、已实现的 API
按模块分组列出所有已实现的 API。

### 示例报告片段

```markdown
## 一、总体统计

| 指标 | 数量 |
|------|------|
| **API 总数** | 254 |
| **已实现** | 240 |
| **未实现** | 14 |
| **完成率** | 94.5% |
| **额外文件** | 3 |

## 二、模块统计

| 模块 | API 数量 | 已实现 | 未实现 | 完成率 |
|------|---------|--------|--------|--------|
| BASE | 49 | 48 | 1 | 98.0% |
| BAIKE | 27 | 27 | 0 | 100.0% |
| CCM | 174 | 160 | 14 | 92.0% |
| MINUTES | 4 | 4 | 0 | 100.0% |
```

## 🔧 配置文件

### tools/api_coverage.toml

定义 crate → bizTag 映射关系，用于自动补全验证参数。

**格式：**
```toml
[crates.{crate_name}]
src = "crates/{crate_name}/src"
biz_tags = ["bizTag1", "bizTag2", ...]
```

**添加新 crate 映射：**
1. 编辑 `tools/api_coverage.toml`
2. 在 `[crates]` 下添加新条目
3. 运行 `--list-crates` 验证配置

## 🚨 常见问题

### 1. CSV 文件不存在

**错误：** `❌ 错误: CSV 文件不存在: api_list_export.csv`

**解决：**
- 确保 `api_list_export.csv` 在项目根目录
- 或使用 `--csv` 参数指定路径

### 2. 源码目录不存在

**错误：** `❌ 错误: 源码目录不存在: crates/xxx/src`

**解决：**
- 检查 crate 名称是否正确（使用 `--list-crates` 查看）
- 或使用 `--src` 参数手动指定路径

### 3. 完成率异常

**现象：** 完成率超过 100% 或有大量"额外文件"

**可能原因：**
- 命名规范不匹配（文件命名与 CSV 定义不一致）
- 存在辅助文件（service.rs、models.rs 等）
- CSV 定义过时

**解决：**
- 检查命名规范：`src/{bizTag}/{project}/{version}/{resource}/{name}.rs`
- 更新 CSV 文件
- 检查是否需要更新 `tools/api_coverage.toml` 映射

## 📝 命名规范

API 文件路径严格遵循以下规范：

```
src/{bizTag}/{project}/{version}/{resource}/{name}.rs
```

**规则：**
- `meta.resource` 中的 `.` 转换为 `/` 作为子目录
- `meta.name` 中的 `/` 转换为 `/` 作为子目录
- `meta.name` 中的 `:` 替换为 `_`（路径参数）
- 使用 snake_case 命名

**示例：**
| API | 文件路径 |
|-----|----------|
| `bizTag=ccm, project=drive, version=v1, resource=file, name=create` | `src/ccm/drive/v1/file/create.rs` |
| `bizTag=base, project=bitable, version=v1, resource=app.table, name=record/create` | `src/base/bitable/v1/app/table/record/create.rs` |

## 🔗 相关技能

- **添加新 API**：`Skill(openlark-api)`
- **设计审查**：`Skill(openlark-design-review)`
- **校验风格**：`Skill(openlark-validation-style)`

## 📚 工作流集成

### CI/CD 集成

在 CI 中添加 API 覆盖率检查：

```yaml
# .github/workflows/api-validation.yml
name: API Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate API Coverage
        run: |
          python3 tools/validate_apis.py --crate openlark-docs
          python3 tools/validate_apis.py --crate openlark-communication
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 tools/validate_apis.py --crate openlark-docs --output reports/api_validation/pre-commit.md
```

## 🎓 最佳实践

1. **定期验证**：每次添加新 API 后运行验证
2. **保持同步**：确保 CSV 文件与飞书官方文档同步
3. **更新映射**：添加新 crate 时及时更新 `api_coverage.toml`
4. **审查报告**：关注"额外文件"，可能需要更新 CSV 或重构代码
5. **100% 目标**：确保核心 API 实现率达到 100%
