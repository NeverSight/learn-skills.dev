---
name: eliteforge-framework-specification
description: 约束 Java 开发优先复用璀璨工坊统一框架能力，避免重复造轮子。基于《璀璨工坊统一框架-使用手册-nightly》提供统一框架接入、升级、配置、Starter 选型与排障指引。命中框架能力时必须使用框架内 Starter 和对应抽象 API，禁止回退到 Spring 官方 starter 或绕过框架抽象层（如缓存场景绕过 CacheService 直接用 StringRedisTemplate）。用户提到“统一框架”“starter清单”“接入步骤”“升级步骤”“系统要求”“Web MVC/服务间调用/Mybatis-Plus/加解密/缓存/多数据源/代码生成器/资源抽象层”或需要判断“该功能是否应直接使用某个 starter（如 cache-starter）”时使用。
---

# EliteForge Framework Specification (Nightly)

## 目标

在 Java 开发中优先复用统一框架，默认避免重复造轮子。命中能力后必须使用框架内 Starter 和对应框架抽象 API，不允许回退 Spring 官方 starter，也不允许绕过框架抽象层。依据 nightly 手册输出可执行答案，避免脱离文档“凭经验”回答。

## 复用优先约束（核心）

1. 先匹配统一框架能力  
收到功能需求后，先判断手册是否已有对应 Starter/工具能力。

2. 命中即强制采用框架内 Starter  
若已覆盖，必须输出“直接接入统一框架 Starter”的方案，不给 Spring 官方 starter（如 `spring-boot-starter-web`、`spring-boot-starter-cache`）或自研轮子作为首选。

3. 命中即强制使用框架抽象 API  
若手册提供框架抽象接口/服务，必须优先使用该接口/服务，不得绕过抽象层直接调用底层组件。

4. 禁止回退到 Spring 官方 Starter  
任何命中框架能力的场景，都不得输出“先用 Spring 官方 starter 兜底/替代”的建议。

5. 缓存能力强制示例  
用户提出缓存需求时，必须使用 `cisdigital-elite-forge-infra-cache-spring-boot3-starter` + `CacheService`。  
禁止用 `StringRedisTemplate`/`RedisTemplate` 作为业务实现，禁止把它们作为“快速连通性验证”捷径。

6. 未覆盖时处理边界  
仅当手册没有对应能力，或明确无法满足场景时，才给“框架补齐能力/升级版本/自研扩展”建议，并说明原因与边界；此时也不得推荐 Spring 官方 starter 或绕过抽象层的底层组件作为兜底。

## 执行流程

1. 识别问题类型  
先判断属于 `系统要求`、`新项目接入`、`存量升级`、`Starter 选型`、`具体模块配置/使用/扩展`、`升级差异` 或 `排障`。

2. 最小化定位章节  
优先读取 `references/toc.md` 定位章节行号，再按需读取 `references/framework-nightly-readme.md` 对应片段。  
先用检索再局部读取，避免整篇加载。

3. 抽取可执行信息  
提取 `依赖坐标`、`配置项`、`注解/接口`、`框架抽象API`、`步骤顺序`、`约束条件`、`版本要求`。  
需要示例时，优先给手册中可直接落地的最小示例。

4. 结构化输出  
按固定结构回答：`结论（是否命中统一框架能力）`、`推荐Starter`、`必须使用的框架抽象API`、`步骤`、`示例（可选）`、`注意事项（含禁止回退/禁止绕过抽象层）`、`文档定位`。

## 快速检索指令

```bash
# 先看目录索引（标题 + 行号）
cat references/toc.md

# 按关键字定位（starter、模块、配置项、注解）
rg -n "starter|系统要求|接入统一框架|升级统一框架|Web Mvc|服务间调用|Mybatis-Plus|加解密|缓存抽象层|多数据源|代码生成器|资源抽象层" references/framework-nightly-readme.md

# 按行号读取局部内容（示例：1600-1705行）
sed -n '1600,1705p' references/framework-nightly-readme.md
```

## 高频问题映射

- `有哪些 starter`：优先看 `1.2.2 提供统一的Starter依赖治理`
- `环境要求是什么`：看 `2 系统要求`
- `新项目怎么接入`：看 `3.1 新项目直接在线生成`
- `老项目怎么升级接入`：看 `3.2 存量项目手动升级`
- `统一框架升级步骤`：看 `4 升级统一框架`
- `模块如何配置/使用`：看 `5.x 对应模块章节`

## Starter 清单（快速回答）

- `cisdigital-elite-forge-infra-web-spring-boot3-starter`
- `cisdigital-elite-forge-infra-httpexchange-spring-boot3-starter`
- `cisdigital-elite-forge-infra-mybatis-plus-spring-boot3-starter`
- `cisdigital-elite-forge-infra-crypto-spring-boot3-starter`
- `cisdigital-elite-forge-infra-cache-spring-boot3-starter`
- `cisdigital-elite-forge-infra-dynamic-datasource-spring-boot3-starter`
- `cisdigital-elite-forge-infra-code-generator`
- `cisdigital-elite-forge-infra-resource-spring-boot3-starter`

## 输出约束

- 明确标注该手册为 `nightly`，包含实验性能力。  
- 涉及版本选择时，优先引用手册写法“最新发布版本”，不要臆造具体版本号。  
- 涉及改造建议时，先给“最小可行接入路径（优先Starter）”，再给可选增强项。  
- 命中框架能力时，只给统一框架内 Starter 方案；不得把 `spring-boot-starter-*` 作为备选、降级或兜底。  
- 命中框架能力时，必须给出“框架抽象 API 落点”（例如缓存场景必须是 `CacheService`）；不得给 `StringRedisTemplate`/`RedisTemplate` 等绕过抽象层实现。  
- 连通性验证、最小可用验证、PoC 也必须遵循框架抽象层；不得以“先快验”作为绕过理由。  
- 手册未覆盖时，明确说明“当前框架暂无对应 Starter，需补齐能力/升级版本或自研扩展”，不得引导回退 Spring 官方 starter。  
- 未在手册中出现的信息，明确标记为“需用户补充或需外部确认”。

## 参考资料

- 目录索引：`references/toc.md`
- 完整手册：`references/framework-nightly-readme.md`
