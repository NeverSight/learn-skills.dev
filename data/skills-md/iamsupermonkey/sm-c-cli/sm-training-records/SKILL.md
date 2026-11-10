---
name: sm-training-records
description: SUPERMONKEY（超级猩猩）运动记录：查询并汇总当前用户近一年内的运动记录、上课记录和训练历史，以及查询私教训练详情。当用户询问“我在超级猩猩的运动记录 / 上课记录 / 训练记录”“我在超级猩猩这个月或某个月上过什么课”“我在超级猩猩近几个月运动了多少次”“我在超级猩猩去过哪些门店 / 跟哪些教练上过课”“查看某次私教训练详情”，或要求按指定时间范围查询其在超级猩猩的个人运动历史时使用。
metadata:
  requires:
    bins: ['sm-c-cli']
  cliHelp: 'sm-c-cli training-records --help'
---

# SUPERMONKEY 运动记录

访问运动记录过程中，如出现 HTTP 401，或 `msg` 提示未授权、授权无效、token / 令牌失效，立即读取 [`../sm-shared/SKILL.md`](../sm-shared/SKILL.md)，按照其中的授权登录与身份检查规则引导用户完成授权；不要自行编造或复制一套授权流程。授权恢复后，再重新执行尚未完成的操作。

通过 `sm-c-cli training-records` 查询当前用户的运动记录。当前提供两个 Shortcut：

- `+list`：按月份查询运动记录列表。
- `+personal-detail`：获取某条私教训练记录的详情。

## Shortcut：+list（查询运动记录列表）

```text
sm-c-cli training-records +list --year-month "YYYY-MM"
```

参数：

- `--year-month`（必填）：查询年月，格式必须为 `YYYY-MM`。

所有参数值统一加双引号。即使用户没有指定时间，CLI 参数仍然必填；此时传入当前月。

## 时间解析与查询窗口

- 仅支持查询从当前月往前推一年的运动记录，起止月份均包含在内。
- 使用当前会话的日期与时区解析“本月”“上个月”“近三个月”“去年”等相对时间，不要写死当前日期。
- 用户没有指定时间时，只查询当前月。
- 用户指定单个月份时，只调用该月份一次。
- 用户指定日期范围或多个月份时，列出与目标日期范围相交的所有自然月，并为每个月分别调用一次 CLI；一次命令只能传一个月份。
- 用户指定“近 N 个月”时，包含当前月，并向前取 `N - 1` 个自然月。例如当前是 2026 年 7 月，“近三个月”拆分为 `2026-05`、`2026-06`、`2026-07`。
- 用户请求完全早于近一年窗口或完全晚于今天时，不要调用 CLI，直接说明仅支持查询近一年内的运动记录。
- 用户请求与支持窗口部分重叠时，只查询重叠部分，并明确告知未查询的超出范围部分。

### 跨月查询流程

1. 把用户时间要求换算成明确的起止日期；未指定时间时，使用当前月。
2. 将起止日期裁剪到“当前日期往前一年至今天”的支持窗口。
3. 按时间升序生成所有相交月份的 `YYYY-MM` 列表。
4. 每个月分别执行一次：

   ```text
   sm-c-cli training-records +list --year-month "<YYYY-MM>"
   ```

5. 合并所有成功响应中的 `data.list`，再按 `startTime` 升序排列。
6. 如果用户指定的是精确日期范围，而不是完整自然月，从 `startTime` 中提取日期并再次过滤合并结果，只保留起止日期内的记录。边界月份也必须执行这一步。

不要把多个年月拼进同一个 `--year-month`，也不要为了跨月查询省略某个月份。

## 使用示例

查询当前月（用户未指定时间）：

```text
sm-c-cli training-records +list --year-month "<当前 YYYY-MM>"
```

查询指定月份：

```text
sm-c-cli training-records +list --year-month "2026-06"
```

查询 2026 年 5 月至 7 月时，分别执行：

```text
sm-c-cli training-records +list --year-month "2026-05"
sm-c-cli training-records +list --year-month "2026-06"
sm-c-cli training-records +list --year-month "2026-07"
```

## 返回字段

stdout 是 `{ code, data, msg }` 信封；成功时 `data.list` 是运动记录数组。主要字段：

| 字段                    | 含义                                                      |
| ----------------------- | --------------------------------------------------------- |
| `trainingId`            | 训练记录 id                                               |
| `startTime` / `endTime` | 开始 / 结束时间，运动日期从 `startTime` 提取              |
| `boxName`               | 门店名称                                                  |
| `className`             | 课程名称                                                  |
| `trainerStageName`      | 教练昵称                                                  |
| `trainingType`          | 运动类型：`团体课`、`训练营`、`私教`、`甄选商品` 或 `SGO` |
| `checkin`               | 签到状态：`未签到` 或 `已签到`                            |

向用户展示结果时，优先使用日期、时间、门店、课程、教练、运动类型和签到状态等人类可读信息；除非用户明确要求，不展示 `trainingId` 等内部字段。

CLI 返回的每条记录还包含必填的 `orderType` 和可选的 `orderId`。这两个字段仅作为后续获取详情时的请求参数保留在内部上下文中，不向用户展示；`orderId` 缺失时不要猜测或补造。

## Shortcut：+personal-detail（获取私教训练详情）

只有先通过 `+list` 获得目标训练记录，并确认该记录的 `trainingType` 为 `私教` 时，才能调用 `+personal-detail`。其他值均不得调用详情命令。

详情请求的 `trainingId`、`orderType` 和可选的 `orderId` 必须全部取自同一条满足门禁的列表记录，不要采用用户猜测的值、拼接不同记录的值，或自行补造缺失的 `orderId`。

```text
sm-c-cli training-records +personal-detail --order-type "<orderType>" --training-id "<trainingId>" [--order-id "<orderId>"]
```

参数：

- `--order-type`（必填）：使用目标列表记录的 `orderType`；只要求是数字，不限制具体取值。
- `--training-id`（必填）：使用目标列表记录的正整数 `trainingId`。
- `--order-id`（可选）：目标列表记录存在 `orderId` 时原样传入；不存在时省略整个 flag。

查询流程：

1. 根据用户给出的时间、课程、门店、教练等线索调用 `+list`，定位目标记录。
2. 如果无法唯一定位，先向用户展示候选私教记录并请其选择，不要调用详情命令。
3. 检查目标记录的 `trainingType`。仅当值为 `私教` 时继续。
4. 从该记录读取 `orderType`、`trainingId` 和可选的 `orderId`，执行 `+personal-detail`。
5. 如果目标记录不是私教，明确告知该命令只支持私教训练详情，不要尝试调用。

详情成功响应的 `data` 包含训练时间、门店、教练、课程合照、训练计划、训练部位强度和训练模块等信息。向用户展示时按其问题提取有用字段；除非用户明确要求，不展示内部 ID。

需要解释训练计划、模块、负载组、动作或组数时，必须读取 [`references/personal-training-detail.md`](references/personal-training-detail.md)，按其中的返回层级、字段语义和空值边界组织回答。

## 结果汇总

- 用户只要求“记录列表”时，按时间展示合并后的记录。
- 用户询问运动次数时，以过滤后的记录条数为准。
- 用户询问常去门店、常上课程、教练或运动类型时，基于过滤后的记录分组统计，不要根据单个月份外推。
- 空列表是成功结果，告知用户所查时间内暂无运动记录，不要描述为查询失败。

## 错误处理

- 信封中 `code === 0` 表示成功；`code !== 0` 表示失败，把 `msg` 如实转述给用户，不要自行编造原因。
- 退出码非 0 时，先读取 stdout 信封中的 `msg`，再参考 stderr 补充信息。
- 跨月查询中只有部分月份失败时，可以展示成功月份的数据，但必须明确标注结果不完整，并列出失败月份；不要把部分结果描述为完整统计。
- 所有月份都失败时，直接告知查询失败。
- 不要猜测、补造或伪造任何运动记录。
