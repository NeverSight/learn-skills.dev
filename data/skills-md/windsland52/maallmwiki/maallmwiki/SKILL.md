---
name: maallmwiki
description: 把 MaaFramework 事实问题路由到版本锁定的原始出处——字段语义与默认值、参数版本支持、API 签名、JSON schema、协议行为与版本变更。任何 MaaFW 事实核查（"这个字段什么意思/默认值多少/哪个版本引入"）或其他 MaaFW skill 指示"路由 MaaLLMWiki"时使用；回答必须引用 pinned 出处，禁止凭记忆作答。Use for any MaaFramework factual question — field semantics and defaults, version support, API signatures, schemas, protocol behavior and version changes — and whenever another MaaFW skill says to route through MaaLLMWiki. Answers must cite the version-pinned upstream source, never model memory.
---

# MaaLLMWiki 知识路由

MaaLLMWiki 是面向模型的**源目录与版本路由层**：索引上游官方文档、schema 与源码，并把每条引用锁定到不可变 commit（40 位 SHA）。它不复制、不替代原始内容——回答事实问题必须**回源**到它指向的原始出处。目录内容托管在 https://github.com/Windsland52/MaaLLMWiki ，本文所有相对路径均相对该仓库根。

本 skill 是标准路由流程；MaaTutorial 的 maafw-* 开发 skill 中"路由 MaaLLMWiki"指的就是执行本流程。

## 路由步骤

1. **定版本**：以被开发项目实际使用的 MaaFW 版本为准（运行时/依赖声明/用户陈述）。版本未知 → 用最新稳定版并**明确声明该假设**；已知版本不在目录中 → 取相邻已有版本并标注差距。可用版本清单见 `generated/maa-framework/index.md`（预发布见 `prereleases.md`；目录没有 `latest`，必须先选版本）。
2. **进目录**：`generated/maa-framework/<版本>/`。
3. **按域选索引**：
    | 要查什么 | 索引位置 |
    | --- | --- |
    | 协议/文档（3.1 Pipeline 协议、3.3 Project Interface V2、2.x 集成、4.x 构建） | `documentation/zh-cn.md` / `en-us.md`——按上游文档编号列条目，每条链到 pinned commit 的原文 |
    | Python / NodeJS 绑定 API（随框架版本） | `bindings/` |
    | Go / Rust 绑定 API（独立 pin） | `generated/maa-framework-go/`、`generated/maa-framework-rs/` 的 `<版本>/api.md` |
    | 原生 API | `native-api/` |
    | JSON Schema | `schemas.md` |

    注册了哪些信息源见 `sources/repositories.yaml`。
4. **回源作答**：打开条目给出的 pinned commit 链接读**原文**再回答；引用时注明上游文档 + MaaFW 版本 + commit。禁止把目录索引本身当作字段语义的出处，禁止把链接换成移动分支（main / master）。
5. **主题级定位**（不知道文档编号时）：查 `sources/maa-framework/source-map.yaml`——主题 → 按版本适用的变体 → 原始路径（文档 / schema / 源码文件）+ 符号 + 字面搜索词，可直接跳到源码级出处。跨版本**行为变更**查 `sources/maa-framework/semantic-changes.yaml`（每条对应已注册 release）。
6. **消费通道**（按连通性择优）：
    - 本地 Git 检出：一次克隆长期可用，弱网环境最稳；
    - raw 直链：`https://raw.githubusercontent.com/Windsland52/MaaLLMWiki/main/<相对路径>`，如 `generated/maa-framework/5.14.2/documentation/zh-cn.md`；
    - GitHub 不通畅时：jsDelivr CDN 镜像同一相对路径——`https://cdn.jsdelivr.net/gh/Windsland52/MaaLLMWiki@main/<相对路径>`（`@main` 有最长 12h 缓存延迟，索引场景可接受；`@tag`/`@commit` 引用为不可变缓存，与版本锁定原则一致）；
    - 其他 GitHub 加速代理同理可用；
    - 正式产物：GitHub Releases 的 catalog zip（经 Releases API 发现最新版本，一次下载本地解压，manifest 记录每个文件的 SHA-256）。

    不引入 chunking / embedding / vector / MCP——目录就是分层 markdown，直接读。

## 硬规则

- **两个版本维度**：MaaFW 目标版本 ≠ Wiki 自身 Git revision，引用时说清对象。
- **不可达即未验证**：目录或上游拿不到 → 回答显式标注"未验证"，不用记忆补；宁可少答。
- **内容边界**：本仓库只做路由，不收项目实践/教程/日志/诊断——开发实践在 MaaTutorial，项目事实在各项目仓库。
