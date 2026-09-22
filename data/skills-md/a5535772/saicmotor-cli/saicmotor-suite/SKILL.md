---
name: saicmotor-suite
version: 1.0.0
description: "上汽内部业务系统 CLI 聚合入口：请假、考勤等。当用户需要操作上汽内部业务系统（请假、请年假、查余额、打卡记录、补卡、考勤）时使用。"
metadata:
  requires:
    bins: ["saicmotor"]
---

# saicmotor CLI

你是 AI Agent，通过 saicmotor 命令操作上汽内部业务系统。你的职责是先判断用户要使用哪个 `saicmotor-*` 子能力，再读取并遵循对应子能力的说明。

`saicmotor-suite` 不直接承载具体 API 操作步骤。除非对应子能力已被读取，否则不要仅根据本文件拼命令、猜参数或执行复杂操作。

## 使用流程

1. 根据用户意图从下方路由表选择一个或多个子能力。
2. 直接读取对应子能力的 `SKILL.md` 加载详细用法。
3. 仅使用本文件列出的路由与对应子能力入口，不要遍历或探测其他技能目录。
4. 如果目标能力未列出，返回无法路由的明确提示。
5. 按目标子能力的说明执行；认证、配置和通用排障优先遵循 `saicmotor-shared`。

多步任务可以组合多个子能力，但每一步都应由具体子能力驱动。

## 能力路由

| 用户意图 | 子能力 | 说明 |
|----------|--------|------|
| 请假、请年假、调休、查余额、提交请假 | [saicmotor-leave](../saicmotor-leave/SKILL.md) | 查年假余额、提交请假申请 |
| 考勤、打卡记录、补卡、迟到、早退 | [saicmotor-attendance](../saicmotor-attendance/SKILL.md) | 查打卡记录、申请补卡 |
| 登录、登出、配置、认证 | [saicmotor-shared](../saicmotor-shared/SKILL.md) | 认证怎么搞、login/logout、401 怎么办 |

## 命令探索

```bash
saicmotor --help                 # 列出所有可用系统
saicmotor leave --help           # 列出请假系统的命令
saicmotor attendance --help      # 列出考勤系统的命令
saicmotor auth login --help      # 查看登录参数
saicmotor auth --help            # 列出认证相关命令
```