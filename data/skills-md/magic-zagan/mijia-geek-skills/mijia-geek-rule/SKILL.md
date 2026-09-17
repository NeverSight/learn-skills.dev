---
name: mijia-geek-rule
description: 米家自动化极客版自动化规则的编写——JSON 结构、节点类型表、MIoT 设备寻址、平台行为约束与生成工具库 mijia_rule_kit。当设计/编写/修改/审查极客版自动化规则，或用工具库生成可导入规则时使用。配套技能：.bak 打包解包见 mijia-geek-backup，控制台导入与自验证见 mijia-geek-console。入门用户请先加载 mijia-geek-beginner。
---

# 米家极客版自动化规则编写

> 配套：.bak 打包/解包见 **mijia-geek-backup**；导入控制台+自验证+执行日志见 **mijia-geek-console**。
> 入门教程见 **mijia-geek-beginner**。

## JSON 结构速查

```jsonc
{
    "version": 2,
    "rules": [{
        "id": "<毫秒时间戳>",
        "cfg": {
            "id": "<同上>",
            "userData": { "name": "<规则名>", "transform": {"x":0,"y":0,"scale":1,"rotate":0},
                          "lastUpdateTime": <毫秒时间戳>, "version": 0, "tags": ["<标签>"] },
            "uiType": "test", "enable": true/false
        },
        "nodes": [ /* 卡片节点，见下 */ ]
    }],
    "variables": { "global": { "<11位字母数字ID>": { "type": "string|number", "value": <初始值>,
                                                   "userData": { "name": "<显示名>" } } } }
}
```

节点通用结构：`{ id, type, cfg:{urn?, pos:{x,y,width,height}, name:<type同名>, version}, inputs:{...:null}, outputs:{<端口>:["目标节点ID.目标端口"]}, props:{...} }`

- **连线**全部记录在源节点 `outputs`，格式 `"节点ID.端口名"`；条件类节点 `output`=成立分支、`output2`=否则分支
- 节点 ID：10 位随机串或 `类型名+毫秒时间戳`；变量 ID：见下「变量 ID 约束」
- `cfg.pos` 只影响画布美观；程序生成时按列×行排版（间距 x≈700, y≈150）避免重叠

## 节点类型表（已覆盖 25 种，遇新类型立即补充）

### 设备类
| type | 卡片 | props 要点 |
| --- | --- | --- |
| deviceInput | 事件/状态更新（触发） | did, siid, piid, dtype(`boolean/int/float/string/number`), operator(`= != < > <= >= include`), v1(include时为数组), preload |
| deviceGet | 查询当前状态（条件） | 同上；output=成立 / output2=否则 双分支 |
| deviceOutput | 执行操作 | 属性写入: {did,siid,piid,value}；动作: {did,siid,aiid,ins:[{piid,value}]}；ins 元素可为变量引用 {piid,id,scope,dtype} |
| deviceInputSetVar | 设备触发赋值 | {did,siid,piid,preload,dtype,id,scope} 设备状态变化时写入变量 |
| deviceGetSetVar | 查询设备赋值 | {did,siid,piid,dtype,id,scope} 查询设备属性写入变量（前面须有触发） |

### 触发类
| type | 卡片 | props 要点 |
| --- | --- | --- |
| timeRange | 时间段 | start/end:{hour,minute,second}, filter（同 alarmClock）；支持跨天 |
| alarmClock | 定时/日出日落 | 定时: {type:"periodicAlarm",hour,minute,second}；日出日落: {type:"sunset",isSunset(true=日落),offset,latitude,longitude}；filter 可选: {day:[1-6,0]}周过滤 / {inHoliday:true/false}节假日过滤 |
| onLoad | 规则加载时触发 | 无 props |
| varChange | 变量变化触发 | id, scope, varType, operator, v1, preload（operator 仅 `=`，见下约束） |

### 逻辑/流程类
| type | 卡片 | 端口与 props |
| --- | --- | --- |
| logicAnd / logicOr | 满足全部/任一条件 | inputs: input0..N；无 props；**latch 语义**（见下） |
| logicNot | 条件取反 | input → output |
| condition | 条件判断 | inputs: trigger+condition；outputs: met/unmet |
| signalOr | 信号或（任一信号到达即放行） | inputs: input0..N |
| delay | 延时（防抖：重触发则重置） | {timeout: 毫秒} |
| statusLast | 状态维持 | {timeout: 毫秒} |
| loop | 循环 | inputs: start/stop；{interval: 毫秒} |
| counter | 计数器（满 n 次放行） | inputs: input/zero(清零)；{n} |
| onlyNTimes | 仅执行 N 次 | inputs: input/zero(重置)；{n} |
| eventSequence | 事件顺序（input1 后 timeout 内 input2） | inputs: input1/input2；{timeout: 毫秒} |
| register | 寄存器（布尔状态保持） | inputs: setTrue/setFalse |
| modeSwitch | 模式切换（循环轮转） | outputs: output0..N |
| **nop** | **文本注释卡**（工具栏「文本」按钮，画布文档/备注，不连线不执行） | 见下 |

**nop 文本注释卡**（给规则加画布注释）：`type:"nop"`，无连线、不参与执行，纯文档。结构特殊——内容/样式/坐标全在 `cfg`：
```json
{"id":"<id>","type":"nop","inputs":{},"outputs":{"output":[]},"props":{},
 "cfg":{"contents":[{"insert":"注释文字\n"}],   // Quill Delta 富文本数组；加粗等加 "attributes":{"bold":true}
        "background":"#80CAFF",                  // 卡片底色
        "pos":{"x":..,"y":..,"width":320,"height":60},"name":"nop","version":1}}
```
校验/排版须特判：nop 无入边出边属正常（勿当悬空报错）、不参与拓扑排版（保留手填坐标）。`mijia_rule_kit` 提供 `text_note(text,x,y,...)`，并已在 validate/auto_layout 里特判；配合 `set_band`+`band_top` 可给每条意图泳道挂分组标题。

### 变量类
| type | 卡片 | props 要点 |
| --- | --- | --- |
| varSetString | 文本变量赋值/文本拼接 | id, scope, elements（表达式 token 列表，见下） |
| varSetNumber | 数值变量赋值/数值运算 | 同上 |
| varGet | 查询变量（条件） | id, scope, varType, operator(仅 `=`), v1；output/output2 双分支 |

**elements 表达式语法**（varSetString/varSetNumber 通用）：token 数组顺序拼接，两种 token：
- `{"type":"const","value":"<文本片段>"}`
- `{"type":"var","id":"<变量ID>","scope":"global|R<规则ID>"}`

数值运算即把函数写进 const 片段拼变量，如 `abs(x)` = `[{const:"abs("},{var:x},{const:")"}]`；已见函数：`abs(x)`、`pow(x,2)`、`log(x,3)`、`now()`。文本拼接同理混排 const/var。

**变量 scope**：全局=`"global"`；本规则变量=`"R<规则ID>"`。✅ **规则变量的定义会序列化进备份**（实测验证：导出→导入→再导出回路后，`variables.R<规则ID>` 域下的变量定义完好保留）。⚠️ 前提：变量必须有卡片引用（无引用的孤立定义可能被平台清理）。规则私有变量优先用规则 scope 而非全局变量，避免全局变量列表膨胀。

## 平台行为与约束实证（务必内化，多为踩坑换来）

- 🔑 **变量节点算子限制**：`varGet`/`varChange` **仅支持 `=`**；用 `!=`（及大概率其它比较符）导致导入校验报 `Invalid node parameter:<节点id>,Invalid operator`。**设备节点 `deviceGet`/`deviceInput` 支持全套** `= != < > <= >= include`。表达"变量≠某值"：用 `varGet(=值)` 取 **output2(否则)分支**（如"∉{A,B}"=`varGet(=A).output2→varGet(=B).output2→继续`）。
- 🔑 **全局变量 ID 必须 11 位纯字母数字**（如 `Vabc123def4`）；含**下划线**等非字母数字字符会被平台**静默丢弃**——规则照常导入，但变量不入全局变量列表、读写失效。
- 🔑 **timeRange 当被动时段条件**：`timeRange` 是纯触发节点（`inputs:{}` 无输入口），不能串在别节点后。但可接 `condition` 节点的 `condition` 槽作被动判断——`onLoad→condition.trigger` + `timeRange→condition.condition`，condition 按**当前时刻**实时采样在/不在区间，met/unmet 分流。日出日落 alarmClock 同理可作条件。
- ✅ **onLoad 在规则加载/启用时触发**（可用于变量兜底初始化）。
- ✅ **设灯即亮**：deviceOutput 写灯的亮度/色温/场景(piid7) 会顺带点亮灯，无需先发开关。
- 🔑 **BLE mesh 筒灯 (xiaomi-btlm2p) 支持 p7 场景模式**（实测）：明亮=1、温馨=3、夜灯=**4**（与吸顶灯 cei 系列不同，cei 夜灯=5）。
- 📌 **TTS 播报**：speaker `siid7/aiid3`，`ins:[{piid:1,id:<string变量>,scope,dtype:"string"}]` 朗读**字符串变量**内容（非常量）；固定话术须先 `varSetString` 写入再朗读。
- 🔑 **枚举/多选状态属性必须用 `operator:"include"` + 数组 v1**（否则编辑器白屏崩溃）：像占用「有人无人状态」这类枚举属性，控制台 UI 用**多选「包含」控件**，渲染时对 v1 调 `.includes()`——若写成标量（`=`/`!=` + `1`），**后端能导入、规则能运行，但一打开编辑器就 `Uncaught TypeError: r.includes is not a function` 整页白屏**（dropdownRender 崩）。务必 `operator:"include"`，`v1` 为**数组**。
- 💡 **占用/人在传感器**（occupancy-sensor）Occupancy Status 枚举 `0=无人/1=有人/2=快速检测`（spec 确认；piid 因型号而异，须查 spec）。规范编码：有人=`include [1]`、无人=`include [0]`（`[0]` 严格无人，比 `!=1` 更准，排除快速检测态）。毫米波传感器静坐易有盲区，PIR/蓝牙可补盲——多传感器宜「有人=任一(OR)、无人=全部(AND)」，AND 方向偏安全（有人在就不关）。
- 🔑 **写设备前检查当前状态（避免无效重复动作）**：无人关灯等"执行操作"链路的末端，在发 `deviceOutput` 前必须插入 `deviceGet` 检查设备当前状态是否已是目标值。典型场景：深夜灯已关 → Pro 报无人 → 若不加灯=开检查，每次无人事件都会重复发关灯指令（无效但浪费，且可能打断手动开灯等操作）。修正：`触发→时段判断→延时/复核→**deviceGet(灯=开)**→关灯`。此模式通用——任何"把设备设为某状态"的动作链末端都应检查设备是否已在目标状态，避免无效重复触发。
- 🔑 **调试模式全局变量（TTS 开关）**：开发期需要 TTS 播报定位规则执行路径，稳定期需关闭 TTS 避免扰民。用一个手动可控的全局变量统一控制所有 TTS 输出。每条链终端在 TTS 前插入 `cond_var(调试模式, "开启")` 条件门，写灯/设备动作直接执行不经过开关。用户在控制台「全局变量列表」中编辑「调试模式」当前值即可实时开关 TTS，无需改规则重导。

- 🔑 **触发 vs 条件（执行模型，测试规则实证）**：能"对变化/更新反应"的只有**触发节点**——`deviceInput`(事件/状态更新)、`varChange`(变量值更新)、`alarmClock`(定时/日出日落)、`timeRange`、`onLoad`。**查询节点 `deviceGet`/`varGet` 是被动门**：只在有信号流入其 `input` 时才求值，**不会因被查的设备/变量变化而自发输出**（实测：独立 varGet 改其变量纹丝不动）。⟹ 规则结构必为「触发卡 → 查询门(串/并) → 动作」，不能靠查询自反应省掉触发。
- 🔑 **logicAnd/logicOr 是 latch（锁存）语义（测试规则实证）**：逻辑门**记住每路输入的最新真假**，**任一路被上游更新时即重算**——logicAnd 全真则放行、logicOr 任一真则放行。⟹ 各路输入可由**不同时刻的分离事件**喂入，无需同时脉冲。这让"绿色判断/条件"能被上游变化**带触发**：典型用 `varChange(时段=X)` + `logicOr(传感器1有人 OR 传感器2有人)` 汇入 `logicAnd` 合并多维条件，比串接长查询链清爽。`mijia_rule_kit` 提供 `logic_and(n)`/`logic_or(n)`。
- 🔑 **delay 卡的时间/单位在 `cfg`，不在 props**：运行值是 `props.timeout`(毫秒)，但**编辑器显示读 `cfg.value` + `cfg.unit`**（如 `{"unit":"s","value":600}`）。只写 props.timeout 会导致延时卡**时间和单位都空白**。两者须一致（value×unit = timeout）；单位 `"s"` 已证合法。`mijia_rule_kit` 的 `delay()` 已自动写入。
- 🔑🔑 **`delay`(去抖) vs `statusLast`(状态维持了一段时间)——「某状态持续 X 时间」务必用 statusLast 且每个事件源各挂独立计时器，切勿把多源事件并到一个共享 `delay`**：`delay` 是去抖语义，任一次重触发即**重置**计时。把多个同类事件用 `logicOr` 并到**一个共享 delay** → 事件交替到达 / 传感器周期性重报状态 → delay 被反复重置 → **永不完成**。正解：**每源各挂独立 `statusLast`**（量"状态保持时长"，不被同状态重报重置）。`mijia_rule_kit` 提供 `status_last(ms)`。
- 🔑 **占用/人在传感器分区的「有人/无人持续时长」属性常不可用**：spec 里这类时长属性常直接标注 **【不支持，请使用极客版计时器】**。故"区域持续无人[时长]"需用计时器卡自拼。
- 💡 **多灯共用单个照度传感器时「暗才补光」会自照亮失效**：人走过、沿途灯陆续点亮 → 照度被自己顶过阈值 → 后续灯不亮。破法：补光门改 `照度<阈值 OR (照度≥阈值 ∧ 任一同区灯已开)`——区分"自己照亮"vs"自然够亮"。
- 💡 **白天补光「开灯照度阈值」推荐 80–100 lux（默认 80）**：阈值语义=「照度低于此值才补光开灯」。取值偏高（如 150）会在体感已够亮时误触发开灯，取值偏低则该补光时反而不开。推荐区间 **80–100**——多数房间取 80（偏暗才补、避免高频启用），对光要求高的区域（如厨房细切操作）可上探到 100。两点配套：① 若同时设了「照度收回(高于阈值关灯)」，开/关阈值须拉开滞回间距（如 `开<80 / 关>250`）避免反复横跳；② 灯一开就把照度顶过收回阈值的房间（客厅/餐厅/走廊等），应直接去掉收回门、改纯占用开关，否则陷入"开灯→照度升→自关"的正反馈环。
- **规则启用时查询一次（preload）**：触发卡上的开关 = 规则加载/启用时**立即按当前状态求值一次**。占用/光照这类**事件触发一般关闭**——否则每次规则重载/中枢重启都会重新触发动作。

**仍缺样本**：虚拟事件（中枢网关事件卡）、设备事件型触发（eiid，如门锁开门）。

## 设备寻址（MIoT-Spec-V2）

`did` 定位设备实例，`urn` 描述型号，`siid/piid` 属性、`siid/aiid` 动作。
🚨 **did 必须取自用户导出的真实备份，严禁虚构**；蓝牙子设备 did 带 `blt.` 前缀。
💡 **不靠样本查 piid**：拿到型号（urn 第 5 段如 `xiaomi-ceil02`）后用 MIoT 官方 spec 权威查全属性表：`WebFetch https://miot-spec.org/miot-spec-v2/instance?type=<完整urn>`。spec 给标准能力，**写入语义仍需导入实测复核**。控制台点设备时自身就请求该 spec 接口，印证其权威性。
注意：**备份 JSON 不含设备名称/房间**（前端拿 did 实时查网关渲染）。建议为项目维护一份「did→名称/房间/型号/urn」映射表。

### 人在传感器Pro 分区检测

xiaomi-p1（人在传感器Pro）支持**多分区检测**，每个分区独立上报有人/无人。

**寻址规则**：

| 分区标签 | siid 计算公式 | piid | dtype | 说明 |
|----------|-------------|------|-------|------|
| A-N | `siid = 4 + (N-1)` | `1` | `int` | N 为 APP 标签序号；piid=1 为 Occupancy Status（0=无人, 1=有人） |

**编码规范**：
- 🚨 分区占用是枚举属性，必须用 `operator:"include"` + `v1:[1]` 或 `v1:[0]`，不能用标量
- 分区范围：siid=4~35（共32个分区）
- 分区标签由用户在APP中自定义，**编写规则前必须向用户确认分区映射**

## 生成工具库 mijia_rule_kit

本 skill 目录下的 `mijia_rule_kit.py`（600 行，零依赖，仅 Python 标准库）提供 `RuleBuilder`，业务脚本只声明「节点 + 连线」，平台硬约束由库兜。

```python
import sys; sys.path.insert(0, "<skill目录>")
from mijia_rule_kit import RuleBuilder, merge_import_set, dump_json
rb = RuleBuilder()
rb.declare_external_var("Vxxxxxxxxxx")              # 只读引用别处定义的变量
rb.define_var("Vdbgxxxxxx1", "string", "", "调试")    # 本规则引入的变量（ID 须11位纯字母数字）
t = rb.trigger_device(did, urn, 2, 1, "int", "=", 1)
c = rb.cond_var("Vxxxxxxxxxx", "某值")
a = rb.write_device(did, urn, 2, 7, 1)
rb.link(t, "output", c, "input"); rb.link(c, "output", a, "trigger")
rb.auto_layout()                                       # 拓扑分层自动排版
rb.validate(raise_on_error=True)                       # 落边+校验
rule = rb.build_rule("<毫秒时间戳>", "<规则名>", ["<标签>"])
# 合并导入集（导入=覆盖，须含所有要保留的规则；默认附带品牌水印规则）
base_rules, base_vars = load_rules_from_file("<已有导出>.json")
base_vars.update(rb.var_definitions())
dump_json(merge_import_set(base_rules + [rule], base_vars), "导入集.json")
```

主要方法：`on_load / trigger_device / trigger_var / time_range / alarm_periodic / alarm_sun / workday_gate`（触发），`cond_device / cond_var / condition`（条件），`delay / status_last`（流程），`write_device / call_action / tts / set_var`（动作），`link`（连线），`define_var / declare_external_var`（变量），`text_note`（注释卡），`set_band`（意图分组），`auto_layout`（画布自动排版），`validate / build_rule / var_definitions`（组装）。模块函数：`load_rules_from_file / merge_import_set / dump_json / pack_bak / unpack_bak / pack_main / freeze_main / brand_watermark_rule`。

### 品牌水印规则

`merge_import_set(rules, vars, add_watermark=True)` 默认在规则列表末尾自动追加一条品牌标识规则——nop 文本卡片展示仓库地址、版本号、生成时间、使用技能列表。在极客版规则列表中可见「⚙ 本套规则由 mijia-geek-skills 生成」。可通过 `add_watermark=False` 关闭。也可单独调用 `brand_watermark_rule(repo_url, version)` 生成。

### 编写新规则的标准流程

1. 取真实地址：导出当前备份解包拿 did；piid/取值范围用 `miot-spec.org`
2. 设计稿先与用户确认逻辑
3. 用 `mijia_rule_kit` 写声明式生成脚本 → `validate` 通过。🚨改动既有规则须基于**最新导出全集**合并（导入是覆盖）
4. 打包 .bak（`pack_bak` 或同目录 `bak-pack.ps1`）
5. 导入（覆盖）→ 编辑器画布自检 + 执行日志回放验证 → 结论回写设计稿
