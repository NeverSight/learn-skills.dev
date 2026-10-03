---
name: accel-skill-template
description: 深度学习平台初始化完成后的落盘规则与模板：把验证过的平台知识固化进固定通用名的 accel 三件套与宿主机层。Use when an accelerator platform setup just finished and needs to be distilled, when specializing or updating the accel-* trio's content for the local platform, or when asked to 落盘/沉淀/固化/特化/回流. 三件套正文随平台改写、名称永不变；宿主机层骨架模板在这里。
---

# accel-skill-template：固定三件套 + 宿主机层

## 何时落盘

- 一轮平台初始化**全部走完且验证阶梯通过**后（通常由 accel-init 阶段 5 交棒到这里）。
- 事后补充/修订：某条规则被新事实推翻、版本行过期、新增 fork 兼容结论时。
- 不在方案还没跑通时预写——只允许出现**已验证**的内容，未验证的标 `(未验证)` 或不写。

## 槽位与命名（skill 名称永不变）

| 槽位 | skill 名（固定） | 装什么 | 落在哪 |
| --- | --- | --- | --- |
| 系统层 | `accel-platform-install` | 驱动/SDK/工具链安装：兼容集、用户态布局、下载验签、验证阶梯 | 仓库分发 + 本机改写 |
| Python 层 | `accel-pytorch-python` | 双源纪律、版本匹配矩阵、环境变量、安装流程、验证、常见失败 | 同上 |
| 代码层 | `accel-pytorch-code-porting` | API 映射表、设备探测、AMP、分布式、第三方包兼容、迁移清单 | 同上 |
| 宿主机层 | `<host>-environment`（本机命名） | 本机 conda/uv 路径、硬件表、存储卷、缓存、已装栈的事实记录 | **只留本机**，永不回流 |

平台名（musa/cuda/cann/rocm）只出现在三件套的**内容**里；skill 名称与触发词永远平台无关。三件套每件头部自带「如何特化」改写指引——初始化时**就地改写正文**，不新建平台名 skill，也不把分发版名字改掉。

## 改写规则

0. **两层填空**：三件套正文填平台通用值（版本行/命令/坑），产物回流仓库成为新分发版——本机不留唯一副本；本机值（路径/主机名）只进宿主机层。
1. 按各件头部指引逐节改写；对本平台无意义的节整节删，不要留空标题。
2. 版本匹配矩阵写"查到的当前行 + 查询命令"，附来源链接与日期，不写死会过期又不给重查命令的结论。
3. 验证节贴真实命令与关键输出行（脱去 PID/作业名/私有数据），写明"预期无输出/预期某行出现"。
4. 失败模式只收录真实踩过的，每条带症状→原因→处置。
5. description 平台无关、触发词丰富；与相邻 skill 的分工写清楚。

## 回流仓库流程

1. 用 `platform-environment-skill-audit` 审计三件套：用户名/路径/IP/凭据/验证产物泄露、"本机当通用"的越界。
2. 修正后推 `brilliantrough/agent-skills`（旧平台实例进 git 历史，不并存）。
3. 新机器经 setup 脚本拿到的是最新分发版；**已装机器不追新版**（只装一次），显式刷新属人工动作。
4. 宿主机层即使审计通过也**不回流**——它的价值就是绑定本机。

## 模板文件

- [templates/host-environment.md](templates/host-environment.md)：宿主机层骨架（硬件表 / 存储卷扩容 / 多 Python 环境防混淆 / 缓存 / 已装平台栈 factbook），参考实例：服务器上的 local-python-environment、昇腾机的 system-profile。
