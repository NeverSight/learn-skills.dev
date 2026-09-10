---
name: lieflat-charts
version: 2.0.0-enhanced
description: 兼顾编辑叙事、基础图表、快速汇报、后端监控与大型关系数据的模板驱动图表 Skill。完整保留 48 张原 Lieflat 模板，并新增 28 张 Ops/原生 SVG 模板；根据数据语义、阅读时间、阈值、SLO、多系列、层级和下钻需求生成单文件 HTML 或 Grafana 面板方案。
---

# Lieflat Charts Enhanced — 76 张模板图表 Skill

本 Skill 由两个完整体系组成：

- **Editorial 48**：Lupi Editorial 15、Lupi Basics 12、Glance 18、Interactive 3。
- **Ops 28**：状态、时序、分布、柱状、雷达、关系、矩形树、旭日与明细。

所有模板的示例位置、使用场景和建议统一收录在 `docs/ALL_TEMPLATES_GUIDE.md`；数据契约索引见 `catalog.md`。原体系规则完整保留在 `docs/EDITORIAL_SKILL.md`，Ops 细则见 `docs/OPS_SKILL.md` 和 `docs/OPS_DESIGN_GUIDE.md`。

## 零、先路由场景，再选图

### A. 后端监控与运营数据

只要请求包含以下任一特征，默认先进入 **O1–O28**：

- Prometheus、PromQL、Grafana、SQL 聚合、日志、Trace；
- 服务健康、流量、错误、延迟、容量、SLO、实例状态；
- 多 Pod、多实例、多区域、多版本、多租户；
- 服务依赖、故障影响面、资源占用、层级钻取。

默认优先级：

1. O1/O3/O5/O7：状态、阈值、容量、SLO；
2. O2/O4/O6/O8/O17/O18：时序、百分位、范围、事件、多系列；
3. O11/O12/O19/O20：TopN、堆叠、分组、正负偏差；
4. O9/O10/O13/O14：热力、状态、分布、相关性；
5. O21/O22：多维画像和基线；
6. O16/O23/O24：依赖、关系和分层调用链；
7. O25/O26/O27/O28：资源占比和层级路径；
8. O15：明细表和下钻。

### B. 年报、论文、长文和数据故事

默认完整审计 **Lupi Editorial → Lupi Basics**。只有两组都不适配，或用户明确要求 dashboard、周报、汇报、三秒快读，才进入 Glance。

### C. 周报、领导汇报和三秒快读

优先 Glance；如果数据来自后端监控且涉及阈值、百分位、SLO 或多实例，则优先 Ops，不要为了风格牺牲指标语义。

### D. 大型网络和多段路径

- 小网络：G6/G11；
- 编辑海报网络：L6；
- 大型环形/力导网络：B1/B2；
- 多阶段路径：B3；
- 运维依赖和影响面：O16/O23/O24。

## 一、模板复用硬约束

1. 必须先在 `catalog.md` 与 `docs/ALL_TEMPLATES_GUIDE.md` 中锁定编号。
2. 必须复用对应 Gallery 的真实代码骨架，不得只模仿外观。
3. Editorial 模板从对应卡片和同名脚本注释块复制；Ops 模板从 `templates/ops-native.js` 复制对应 O 编号配置。
4. 允许替换数据、标题、旁注、单位、阈值、变量和必要布局；不得退回图表库默认样式。
5. 一张图只承担一个主要判断；需要多个独立结论时拆为多个面板。
6. 用户要求 Grafana 时，必须同时给出 Panel、查询、Unit、Legend、Threshold、Variables、Transform 和 Data link。

## 二、数据语义硬规则

1. Counter 默认使用 `rate()` 或 `increase()`；除非累计值本身就是业务结论。
2. Gauge 展示当前值或窗口 max/avg，不对 Gauge 使用 `rate()`。
3. 延迟优先 p50/p95/p99；平均值不能替代尾延迟。
4. Histogram bucket 用于分位数、热力图和直方图，不得从平均值伪造分布。
5. 阈值必须来自 SLO、容量、告警规则或明确基线。
6. 零值与无数据不同；缺失值保留 gap 或标记 `NO DATA`。
7. 堆叠只用于可加总数据；百分位、CPU 与内存等不可堆叠。
8. 不同单位不共轴；默认拒绝双 Y 轴。
9. TopN 必须保留 `Other` 或标明覆盖比例。
10. 时间轴写明范围、时区、采样步长和聚合口径。

## 三、多组数据可辨识规则

多组数据禁止只靠颜色区分：

- **1 组**：隐藏冗余图例；
- **2–5 组**：线型 + 符号/实心空心/边框/直接标签；
- **6–8 组**：默认选中 Top5，滚动图例，允许 isolate；
- **9–24 组**：O18 small multiples、分页或变量筛选；
- **25–80 个实体**：聚合、TopN + Other 或只聚焦异常邻域；
- **>80 个实体**：拒绝一次性铺满，先聚合或改专用分析工具。

Ops 新增模板采用原项目单色体系：状态通过粗细、描边、虚线、实心/空心和文字表达；不得把颜色作为唯一通道。

### 折线图

- 默认 `smooth: false`，防止隐藏尖峰；
- 高密度数据使用 `sampling: 'min-max'`；
- 1–5 条叠加，6–8 条 Top5，更多改 small multiples；
- 同一轴只放同单位、可直接比较的系列；
- 折线末端优先直接标注系列名。

### 柱状图

- 分组柱最多 4 组；
- 类别超过 8 个优先横向；超过 20 个必须 TopN 或筛选；
- 组间距大于组内距，图例顺序与柱顺序一致；
- 正负差值突出零线。

### 雷达图

- 维度建议 5–8，最多 10；实体最多 3；
- 所有维度必须同方向并归一化，`indicator.max` 必须有真实含义；
- 使用低透明填充，主要依靠轮廓、线型和符号识别；
- 超过 3 个实体改 small multiples 或平行坐标。

### 关系图

- 节点形状表示角色，大小表示权重，描边/外圈表示状态；
- 边宽表示流量，箭头表示方向，边型表示关系类型；
- 10–40 节点可直接展示，40–80 默认聚焦异常邻域，超过 80 先聚合；
- 开启 roam、拖拽和 adjacency focus，但首屏必须先可读。

### 矩形树图和旭日图

- 面积或角度只能编码一个可加总值；
- 一级分类使用黑/纸反相，子层仅改变灰阶明度；
- 推荐 2–4 层，小项合并为 Other；
- Treemap 适合空间利用与资源占比，Sunburst 适合层级路径；
- 需要精确排名时补 TopN 柱状图。

## 四、标准工作流

1. 识别数据来源和指标类型。
2. 明确读者、场合、阅读时间和要回答的问题。
3. 在 `catalog.md` 中锁定 1–3 个候选模板。
4. 根据数据量、多系列数量、标签长度和是否需要下钻确定最终模板。
5. 从 Gallery 复制真实实现，替换顶部数据和文案。
6. 为每张图补齐标题、副标题、单位、来源、时间范围和必要注释。
7. 监控 Dashboard 按 RED + USE 组织：状态 → 请求/错误/延迟 → 资源 → 定位 → 关联。
8. 运行 `node scripts/validate.mjs`。

## 五、示例入口

| 体系 | 数量 | 示例 |
|---|---:|---|
| Lupi Editorial | 15 | `templates/lupi-gallery.html` |
| Lupi Basics | 12 | `templates/basics-gallery.html` |
| Glance | 18 | `templates/glance-gallery.html` |
| Interactive | 3 | `templates/big-*.html` |
| Ops | 28 | `templates/ops-gallery.html` + `templates/ops-native.js` |

## 六、交付形式

默认交付无需构建、双击可打开的单文件 HTML。

1. 新增 Ops O1–O28 不依赖任何图表库，可完全离线运行；
2. 原有 Glance/Interactive 模板保持原实现，其中部分页面通过 CDN 加载 ECharts/Chart.js；
3. 如需让原有模板离线运行，可用 `scripts/fetch-vendor.mjs` 下载运行时，再将对应 HTML 的脚本地址改成本地路径；
4. 交付说明必须明确所选原有模板是否需要联网。

## 七、交付前自检

- 是否选对数据契约，而不是只选了好看的轮廓？
- Counter、Gauge、Histogram 和 State 是否处理正确？
- 多系列是否至少使用两种非颜色识别编码？
- 是否超过系列、节点、层级或类别上限？
- 单位、时间范围、时区和步长是否明确？
- 阈值是否有真实来源？
- 是否区分 0 与 NO DATA？
- 是否保留 Other 或覆盖比例？
- 是否能从异常下钻到实例、日志、Trace、事件或层级节点？
- 是否复用了对应模板的真实实现？
- `node scripts/validate.mjs` 是否通过？
