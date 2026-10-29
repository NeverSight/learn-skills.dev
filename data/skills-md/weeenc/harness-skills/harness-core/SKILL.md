---
name: harness-core
description: Harness 核心骨架模板 — 参数化模板化技能（被 apply-harness 渲染到各语言包）+ 通用技能 + 模板
---

# Harness 核心骨架

本技能提供跨语言通用的 Harness 骨架模板与通用技能，包括：

- `agents/owner.md` — 参数化的 Owner Agent 定义（含 `{{LANGUAGE}}` 等占位符）
- `templates/changes/_TEMPLATE/` — 变更追踪模板（默认卡片 + 六阶段 report.md；保留 legacy 模板）
- `templates/wiki/` — 领域知识文档模板（业务模型 / 接口协议 / 数据模型 / 架构决策 / ADR-FORMAT）
- `templates/CONTEXT.md` + `CONTEXT-FORMAT.md` — 领域语言词典模板与编写规范
- `skills/` — 技能模板与跨语言通用技能
  - **模板化技能**（被 `apply-harness` 渲染到各语言包）：`harness-me` / `handoff` / `diagnosing-bugs` / `coding-skill` / `unit-test-write`，含 `{{LANG_TAG}}`、`{{BUILD_CMD}}` 等占位符
  - **跨语言通用技能**（直接复制）：
    - `domain-modeling`（领域语言维护）/ `research`（外部事实查证）/ `resolving-merge-conflicts`（合并冲突解决）
    - **流水线机制**（harness-* 前缀）：
      - `harness-status` — 变更状态总览（聚合 changes 进度/待办）
      - `harness-loop-run` — 自主收敛循环引擎（编码→测试→评审到 ci 停机交人）
      - `harness-quality` — 质量闸门与报告（真实 check + flow→test 对账 + 人签字放行）
      - `harness-relate` — 变更关系链管理（六类关系 + impact 影响分析）
    - **工程能力**：
      - `harness-e2e` — 端到端测试（主链路/降级链路）
      - `harness-db-design` — 数据库设计（表结构/索引/约束/迁移设计）
      - `harness-api-mock` — API Mock 数据生成（忠于契约、分支齐全）
      - `harness-refactor` — 重构（行为不变、测试保护、小步）
    - **交付与治理**：
      - `harness-retro` — 迭代复盘（历史留档聚合趋势报告）
      - `harness-ship` — 发布工作流（版本/tag/CI/CD，不可逆操作留人）
      - `harness-changelog` — 变更日志（可追溯条目，带 change ID 链接）
      - `harness-standard` — 规范库管理（新增/修订/归档，重大约束留人审批）
  - **跨语言封装组件**（直接复制，按需加载）：
    - `redis-cache-wrapper` — 多级缓存封装（穿透/击穿/雪崩防护 + 分布式锁 + 热 key 探测）
    - `database-migration-toolkit` — 数据库迁移工具封装（迁移/回滚/数据回填/兼容性检查）
    - `kafka-toolkit` — Kafka 工具封装（消费者封装/DLQ/生产者封装/Lag 监控）
    - `k8s-release-toolkit` — K8s 发布工具封装（Deployment/HPA/探针/灰度/回滚）
    - `performance-toolkit` — 性能诊断工具封装（诊断脚本/火焰图/GC/慢SQL/线程 dump）
    - `security-toolkit` — 安全工具封装（脱敏/加密/输入校验/鉴权/日志脱敏）
    - `rocketmq-toolkit` — RocketMQ 工具封装（事务消息/顺序消息/延迟消息/DLQ）
    - `http-client-toolkit` — HTTP 客户端工具封装（连接池/超时/重试/熔断/traceId）
    - `logging-toolkit` — 日志工具封装（traceId/MDC/脱敏/动态级别/文件策略）
    - `scheduler-toolkit` — 分布式调度工具封装（分布式锁/幂等/重试/补偿/手动触发）
    - `oss-toolkit` — 对象存储工具封装（统一接口/分片上传/预签名/图片处理/CDN）
    - `excel-toolkit` — Excel 工具封装（模板导出/大数据量分批/导入校验/动态列）
    - `eventbus-toolkit` — 事件总线工具封装（同步/异步/事务事件/事件追踪）

被 `apply-harness` 技能在初始化项目时调用。
---


