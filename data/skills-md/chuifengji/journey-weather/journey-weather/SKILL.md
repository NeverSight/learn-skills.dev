---
name: journey-weather
description: 按目的地、路线变体、起止日期和自定义每日行程，匹配真实地点的多模型天气并生成精致的全屏地形地图 HTML。适用于徒步、穿越、自驾接驳和旅行天气规划，支持地区与主题并列筛选、正反穿、额外要求和 GPX。
---

# 旅迹天气

把真实行程变成可逐日、逐地点查看天气的地图。生成便携 HTML 与可再编辑的 `plan.json`，明确展示模型缺测、远期趋势和路径证据。

## 理解行程

- 地区（省份）和主题是**并列筛选**，然后选择目的地、线路及变体。主题可以跨省，不强制先选省。
- 从会话提取起止日期、集散点、天数、方向、露营条件、每日徒步上限及其他要求。沿用已确认条件；缺少结束日期可声明合理的示例天数并继续，不把假设说成用户决定。
- 每天使用真实地名、坐标、到达与离开时间、抵达方式、住宿地点。徒步小时数和里程若非可靠轨迹计算，标记为规划预算。
- 同名垭口或营地尚无法定位时，保留该日程节点，设置 `coordinateStatus: unresolved`、空坐标和 `coordinateNote`。该点不请求天气、相邻轨迹断开，不借用城市或另一个同名点的数据。
- “小环线”可能对应多种垭口与节点组合。说明采用的变体，不仅凭同名拼接行程。

## 生成流程

本目录是 Skill 根目录。命令中的 `<skill>` 替换为本文件所在目录，`<output>` 使用工作区交付目录。需要 Python 3.10+、curl、现代 WebGL 浏览器；核心脚本不依赖 pip 包。

1. 查看线路：

   ```sh
   python3 <skill>/scripts/journey.py catalog --province 四川 --theme 高山湖泊
   ```

   两个条件均可省略，提供两个时取交集。当前是贡嘎与冷嘎措种子目录，不是全国数据库。未收录的目的地：读 [行程结构](references/schema.md)，检索官方公告、实际节点和坐标来源，创建自定义 JSON，不为了维持有限目录而拒绝其他省份。

2. 生成已收录变体：

   ```sh
   python3 <skill>/scripts/journey.py plan --route gongga-small-loop-lenggacuo --start 2026-09-30 --variant 6d --direction forward --out <output>/plan.json
   ```

   可用 `--end YYYY-MM-DD` 代替天数，或添加 `--requirements '不露营，每日徒步不超过 5 小时'`。命令列出约束冲突，**不会自动声称满足任意自然语言要求**。自行落实拍照、住宿、交通接续、体力限制等；硬性要求无法满足时给出可行替代，并明确保留冲突。

3. 校验并获取每个地点的预报：

   ```sh
   python3 <skill>/scripts/journey.py validate <output>/plan.json
   python3 <skill>/scripts/journey.py build --plan <output>/plan.json --out <output>
   ```

   通过 Open-Meteo 获取 ECMWF IFS、NOAA GFS、DWD ICON 的独立模式预报。解释覆盖、差异或新增数据源前，读 [预报与证据规则](references/weather-and-evidence.md)。不把模型当成观测或保证准确率。`--offline` 只读同坐标、时区缓存，无缓存则空缺；网络失败可回退带原时间的缓存，不伪造刷新成功。

4. 用户有 GPX 时可添加 `--gpx PATH --gpx-day day-2`，保持独立轨迹段断开。无精确轨迹保留虚线示意，不伪造 GPS 点。GPX 不证明通行许可。

5. 打开并检查结果：

   ```sh
   python3 <skill>/scripts/journey.py serve --dir <output> --port 4174
   ```

   用浏览器工具打开 `http://127.0.0.1:4174/`。至少检查桌面和手机、逐日切换、真实地点、模型缺测、编辑与保存。交付 `index.html`、`plan.json` 和 `行程与天气.md`，附实际页面预览；有打开文件或浏览器能力时直接展示。

## 视觉与叙述

- **只用 HTML/CSS/JS 与真实地图数据**，不调用图片生成工具。卫星和地形是有来源的地图瓦片。
- 全屏路线地图是主体，日程、天气和来源融入轻量浮层。保留地图留白、细线、少量暖色及清晰数字层级，手机可横向浏览日期。
- 标题使用目的地和实际地名。禁止“沿山而行”“把晴朗留给山间”等泛化口号，不用“山林、湖边、群山”替代地名。
- 不保证晴天、日照金山或通行。管控不确定时提供查证日期和具体待确认路段，不笼统宣称整个地区关闭或开放。
- 区分预报、事实与规划假设。远期趋势不渲染成精确小时建议；出发前刷新预报，但无用户要求时不自动创建提醒或发送消息。

## 复用

- 浏览器可编辑所有天的地点、时间、接驳、住宿、要求与日期，支持 JSON 导入导出。`保存行程` 仅保存当前浏览器；导出 JSON 可交给 Skill 重新构建持久 HTML。
- 小时降水保留 mm 数值与前一小时累计区间；另外显示各模型的天气类型（小雨、中雨、阵雨、雪等）。用 weather_code 解释，缺测不猜测；类型为所标时刻的状态，不能从小时总量或气温硬推，也不能套用 24 小时雨量等级。
- 露营行程同时生成 `overnights.json`，页面“营地夜间”对比当日 18:00 至次日 08:00 的最低温、累计降水和最大阵风；各变量覆盖不足时不输出完整夜间统计。
- 新路线先放在用户输出 JSON。明确要扩充目录时，才将已查证节点及变体加入 `assets/catalog.json`；已知路径放在 `assets/segments.geojson`，保存端点和来源。
- 修改数据逻辑后运行 `python3 <skill>/scripts/test_journey.py` 和 `node <skill>/scripts/test_weather_meaning.js`。第三方资源见 [资源来源](references/asset-sources.md)。
