---
name: unused-code-audit
description: |
  证明某个目录、文件、导出符号、函数、组件、常量、hook、类型或 helper 是否“没有真实消费者”，再决定是否删除。用于死代码清理、未使用代码检测、未使用导出审计、删除安全检查和消费者搜索；只回答消费关系和删除安全性，不判断“仍被使用但是否有必要”，这类问题使用 necessary-code-audit。
---

# 未使用代码审计

## 原则

把每个自动化结果都当作候选，而不是证明。只有在用法、入口、副作用和公共 API 风险都被排除后，才删除。

优先做小而有证据的删除。不要仅因为类型或导出名没有直接 import，就收缩公共 API；生成声明和推断出的消费者类型仍可能依赖它。

本技能回答“还有人在消费它吗？”。它不回答更广义的“它是否仍有必要？”。对于“被使用但不必要”的代码，切换到 `necessary-code-audit`。

不要在发现第一个未使用符号后停止。对于用户指定的目录或功能，必须审计作用域内所有文件、导出、本地 helper 和 re-export 路径后再报告完成。

不要把注释作为未使用代码删除或重写，除非相关代码被删除，或注释已经过期/误导。

本技能属于三个清理技能之一：

- 用 `unused-code-audit` 证明代码是否仍有消费者。
- 代码被使用但可能不必要时，用 `necessary-code-audit`。
- 目标涉及页面状态、查询、变更、权限、错误或用户可见行为时，用 `page-flow-cleanup-audit`。

## 边界

本技能只回答“是否存在真实消费者，以及在零消费者时能否安全删除”。

适合本技能：

- 文件、导出、类型、常量、组件、hook、helper 是否无人 import 或引用。
- re-export、barrel export、type-only import、动态字符串 key、框架入口和副作用是否构成真实消费。
- 删除零消费者代码后，清理直接 export、孤立 import/type 和残留路径。

不适合本技能单独完成：

- 某个 helper 有调用方但只是薄 wrapper；改用 `necessary-code-audit`。
- 公共 API 仍被 import，但可能只是历史兼容面；改用 `necessary-code-audit` 判断是否迁移调用方并收缩公共面。
- 防御分支、fallback、默认值、可选字段是否有领域意义；改用 `necessary-code-audit`。
- 页面状态、权限、query/mutation、source-of-truth 是否应清理；改用 `page-flow-cleanup-audit`。

协作规则：

- 搜索发现候选仍有真实消费者时，停止“未使用”结论；若它看起来仍不必要，移交 `necessary-code-audit`。
- 不要因为“调用方可以改写”就把已使用代码判定为 unused。那是必要性问题，不是 unused 问题。
- 本技能可以删除零消费者代码，但不负责迁移有消费者的调用方，除非迁移只是删除同一文件内新孤立的直接引用。

## 基线

- 先检查工作区状态：`git status --short --untracked-files=all`。
- 检查目标作用域的 unstaged 和 staged 变更：`git diff --name-status -- <scope>`、`git diff --cached --name-status -- <scope>`。
- 构建目标作用域文件清单，优先用 `rg --files <scope>`。
- 信任自动 unused 结果前，检查 import、export、manifest、框架入口、生成文件和直接消费者。
- 删除前建立影响面图：定义包 exports、同包消费者、下游 package/app import，以及可能 import 公共面的脚本/测试。

## 深度门槛

完成 unused-code audit 前必须：

1. 列出请求作用域内每个文件和导出符号。
2. 当本地 helper 只能通过导出聚合或公共函数触达时，也纳入检查。
3. 搜索精确符号、import path、file stem、barrel export、type-only import、属性访问、字符串 key 和测试/脚本用法。
4. 将结果明确分为“无消费者，可按删除标准继续”和“有消费者，退出 unused 判断并转 necessary-code-audit”。
5. 只对无消费者候选继续检查公共入口、框架约定、副作用和动态引用。
6. 编辑后再次搜索删除名称和旧路径，捕获孤立导出和陈旧 import。
7. 公共面变更时，运行定义包验证和受影响下游 package/app 验证。

不要要求用户再次提示，才在同一请求作用域内从一个候选继续到下一个候选。

## 候选分类

删除前分类：

- `文件`：模块、route、样式、setup、生成入口或副作用文件。
- `运行时导出`：函数、组件、hook、class、常量、store 或工厂。
- `公共类型/API`：导出的 interface/type/config，被声明文件或工厂返回类型使用。
- `成员`：属性、方法、action、enum member 或配置字段。
- `本地 helper`：单文件内非导出 helper。

分类决定风险等级。公共 API、框架入口、副作用文件和持久化数据需要更强证据。

## 证据

按以下顺序收集证据：

1. 结构：
   - 目录或功能作用域的文件清单。
   - 公共入口、re-export 文件、框架约定、生成文件和类型声明。
   - 可用时使用语言工具、编译诊断、依赖分析或 IDE 引用。
   - package export map 和 workspace manifest，用于确定下游 typecheck 目标。

2. 文本搜索：
   - 用 `rg` 搜索精确符号名、file stem、import path、别名和大小写变体。
   - 搜索定义位置和所有可能消费者根目录，不只搜索要删除的文件或文件夹。
   - 对成员搜索直接访问、解构、索引访问、回调、配置对象和 type-only 引用。
   - 当共享符号看似未使用时，搜索重复本地常量或 helper 逻辑；这只能说明可能需要 `necessary-code-audit` 推动复用，不能证明当前符号仍被消费。

3. 候选扫描：
   - 如果有本地 unused-export 脚本或依赖分析器，可以用来生成候选。
   - 工具支持 scoped root 时传入目标根目录。
   - 自动化输出只作为线索，不作为证明。

## 误报

除非排除以下情况，否则保留代码：

- re-export、别名、wrapper export 或同文件聚合用法。
- 框架约定：entrypoint、layout、metadata、middleware、loading/error 文件和生成文件。
- 公共模块导出、公共入口文件、生成声明或外部推断类型。
- 通过字符串、registry、map、config 数组、content metadata 或依赖注入的动态用法。
- 副作用：样式、polyfill、provider、setup 模块、storage key、analytics、subscription 和初始化。
- 导出的聚合体内部消费了导出的子部分。

## 删除标准

全部满足才删除：

- 结构检查和文本搜索都显示没有真实消费者，允许的 re-export 引用除外。
- 候选不是框架入口、副作用模块、生成产物或公共 API 必需项。
- 请求作用域允许删除。
- 编辑是外科式的：只删除候选、直接 export 和新孤立的 import/type。

## 验证

- 对每个删除符号、file stem 和 import path 做残留 `rg`。
- 运行最窄相关 typecheck。
- 公共 API 变更时，先验证定义模块，再 build 或 typecheck 受影响消费者。
- 当公共 helper/常量被另一个 package/app 替换时，也 typecheck 那些消费者。
- 运行 `git diff --check -- <scope>`；如果有 staged 变更，也运行 `git diff --cached --check -- <scope>`。
- 如果验证失败，说明失败是否由本次删除导致，还是无关工作区状态。

## 报告

报告三类内容：

- 已删除：删除了什么，以及证据。
- 已移交：哪些候选仍有消费者，因此不属于 unused，应由 `necessary-code-audit` 判断必要性。
- 已保留：重要误报候选，以及保留原因。
- 已验证：运行的命令、结果、无关 dirty 文件或失败。
