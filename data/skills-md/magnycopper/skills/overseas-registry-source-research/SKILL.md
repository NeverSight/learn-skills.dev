---
name: overseas-registry-source-research
description: Research official and third-party company registry, business registration, and related public-record data sources for a specific country or region, compare source and module combinations, and produce one evidence-backed report with reproducible validation artifacts. Use this whenever the user wants to map enterprise registry sources, assess official registries, tax or financial regulator sources, open-data portals, or commercial providers, choose executable acquisition modules, verify search and download constraints, or design a repeatable country-level business data collection plan with sample downloads and proof.
---

# 海外企业登记数据源调研

调研某个国家或地区的企业登记数据来源，并产出一份可执行、可复查、可落地的调研报告。

## 目标

- 优先找到时效性高的数据源
- 优先找到覆盖规模大的数据源
- 优先补齐企业关键维度覆盖
- 所有关键判断都给出可复查证据

## 不要使用本技能的场景

- 用户要抽取单个机构官网字段，优先使用 `homepage-info-extractor`
- 用户只要某个企业的单次查询结果，而不是国家级或地区级数据源调研

## 输入契约

输入参数：

- `country_or_region`: 必填，面向读者展示的国家或地区名称
- `country_or_region_slug`: 必填，用于文件名和目录名，只允许小写字母、数字、连字符
- `target_language`: 默认中文
- `generated_at`: 默认当天，格式 `YYYY-MM-DD`
- `sample_size`: 默认 `1000`
- `template_path`: 默认 `overseas-registry-source-research/assets/templates/registry-research-template.md`
- `time_limit_or_budget`: 可选，用于约束付费源和验证深度

## 输出契约

结果目录固定为：

- `results/<YYYYMMDD>/overseas-registry-source-research/`

最终主报告固定为：

- `<country-or-region-slug>-registry-source-research.md`

每个入选模块的必交付文件：

- `<country-or-region-slug>-<source-id>-<module-id>-download-sample.py`
- `<country-or-region-slug>-<source-id>-<module-id>-test-dataset-<sample_size>.<ext>` 或同名目录

可选文件：

- `<country-or-region-slug>-download-sample.py`

强约束：

- 使用固定模板 `assets/templates/registry-research-template.md`
- 模板已覆盖的内容，不要再拆成额外零散 Markdown
- `temp/` 仅作过程目录，不能替代最终交付目录
- 样本数据保持来源原始可下载格式，未经明确要求不要二次转成 CSV、JSON、Parquet 等格式

## 命名规则

- `source_id` 只用小写字母、数字、连字符，例如 `israel-companies-authority`
- `module_id` 只用小写字母、数字、连字符，例如 `company-search`
- 同一 `source_id` 下 `module_id` 必须唯一

## 术语和覆盖口径

统一使用以下术语：

- `数据源`：机构或平台级来源，例如工商主管机构、税务机构、开放数据平台、证券监管机构、第三方平台
- `模块`：同一数据源下的具体执行入口，例如 API、批量下载包、搜索页、文档服务

企业五维覆盖口径固定为：

- 主体识别
- 状态与生命周期
- 治理信息
- 财务信息
- 合规文档

## 执行顺序

按以下顺序执行，不要跳步。

### 1. 建立国家背景最小集

只收集与企业登记直接相关的信息：

- 登记制度与主管层级
- 企业注册关键流程
- 企业相关编号体系，包括国家级、地区级、税务级编号

### 2. 发现数据源

先官方，后第三方。官方来源至少检查以下类别；如果客观不存在，要明确给出证据：

1. 公司注册或工商主管机构
2. 税务主管机构
3. 政府开放数据平台
4. 证券或金融监管机构
5. 统计机构

对每个数据源都记录：

- 机构名称
- 职责范围
- 主域名
- 法律或许可边界

### 3. 先做模块全清单，再做模块筛选

对每个入选数据源，先列出所有与企业概念有关且可执行的模块，再逐个判断是否纳入。

不要：

- 只挑 1 到 2 个最容易下载的模块
- 把同一机构的多个模块拆成多个数据源
- 只因为下载不稳定或批量不方便，就忽略搜索类型模块

名称或编号检索模块规则：

- 若存在，必须实测并给出证据，即使最终不入选也要说明理由
- 若不存在，明确写出“未发现名称或编号检索模块”，并附检索证据

搜索能力评估规则：

- 写清支持哪些检索方式，例如名称、注册号、税号、地址、法人或高管
- 实测是否支持模糊搜索，例如前缀、包含、近似、同音
- 评估能否通过关键词枚举、编号段遍历、分页遍历等方式逼近全量
- 若判定不可行，附不可行证据，例如结果上限、验证码、频控、封禁策略、法务限制
- 即使不适合作为主下载路径，也要说明补充价值，例如断点补数、字段补齐、质量校验

### 4. 对每个入选模块完成验证闭环

每个入选模块都完成：

1. 访问链路实测，优先使用 Playwright MCP
2. 数据链路分析，包括请求参数、分页、返回结构、下载入口
3. 生成专属 Python 下载脚本
4. 下载 `sample_size` 样本并落盘
5. 输出字段级维度映射和增量贡献说明

不要只给结论，不给脚本和样本。

### 5. 收敛为最终组合

组合评分默认权重：

- 时效性 `0.4`
- 规模 `0.3`
- 覆盖度 `0.3`

输出限制：

- 主组合只能有一个
- 备组合最多一个

报告结构固定为：

1. 数据源总览
2. 按数据源展开模块
3. 组合结论与下载方案

## 证据规则

每条关键结论都附：

- 来源 URL
- 页面定位，例如栏目、按钮、参数、接口路径
- 访问前提，例如匿名、注册、付费、KYC、限频

显式标注：

- 无法确认时写 `未验证`
- 更新周期结论必须有页面或接口证据
- `合作洽谈` 只写 `Y` 或 `N`，并附价格页、条款页、访问限制页或商务页证据

风险等级口径：

- 低：访问稳定、限制轻、合规清晰
- 中：存在登录、限频、偶发反爬，或许可边界部分不清
- 高：强反爬、高门槛、许可不清，或法律风险高

## 输出模板

始终从 `assets/templates/registry-research-template.md` 开始填充报告。模板中的章节顺序、表格结构和检查项都视为固定契约。

## 提交前自检

- 是否只输出 1 个主报告 Markdown？
- 是否使用了固定模板？
- 是否先做数据源发现，再做模块入选？
- 是否对每个数据源先做企业相关模块全清单规划？
- 是否完成名称或编号检索模块验证，或证据化声明不存在？
- 是否对所有搜索类型模块说明了搜索方式、模糊搜索和碰撞逼近全量的可行性？
- 是否对每个入选模块完成实测、脚本和样本下载？
- 样本文件是否保持来源原始格式？
- 是否完成企业五维覆盖状态标注？
- 是否给出唯一主组合和最多一个备组合？
- 是否为所有关键判断附了可复查证据？
