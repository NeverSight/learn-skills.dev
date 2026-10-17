---
name: prism-plot
description: 接收 CSV、TSV、Excel、JSON 或用户粘贴的数据，使用本机 GraphPad Prism 和绘图模板生成图表，导出 PDF、PNG 等格式并保留可编辑 Prism 项目。用于用户明确要求用 Prism 绘图、套用 Prism 模板或批量导出的任务。
---

# GraphPad Prism 绘图与导出

使用真正的 Prism 生成图表。入口是本目录的 `scripts/prism_plot.py`，通过 Windows 命令行执行 `.pzc` 脚本。每次在用户的输出目录下创建独立运行文件夹，保留原始输入记录、数据整理说明、可编辑 `.prism` 项目、执行脚本、导出图和 `manifest.json`。默认使用 Prism 10+ 的 `.prism` 格式；兼容旧版时可选 `--project-format pzfx`。

源项目是默认交付文件，每次运行只保留一份最终源项目。输出目录下创建 `<数据文件名>-<运行时间及唯一编号>` 文件夹，Prism 直接在该文件夹保存 `<数据文件名>.prism`（或所选 `.pzfx`），与同名 PDF、PNG、可选 `statistics.txt` 和 `manifest.json` 并列；不在外层再创建项目副本。中间项目、规范化输入、执行脚本、日志及完成标记放在该文件夹的 `_work` 子目录。多次运行创建不同文件夹，不覆盖往次结果。清单的 `deliverable_project` 与 `project` 指向同一份最终源项目，`deliverable_project_sha256` 记录其校验值。

`.prism` 必须由 Prism 的 `Save` 实际生成并校验压缩包及原生内容，不能改扩展名代替转换；`_work/verification.pzfx` 仅用于精确输入核对，是中间文件。选择 `.pzfx` 交付时直接核对最终项目，不另存一份核对副本。`--prepare-only` 的待执行项目也放在 `_work`，不生成或宣称最终源项目。执行失败时保留清单和诊断文件，不把未完成结果标为成功。

通过界面绘图或另外整理交付文件夹时，也使用同样结构：同一交付文件夹中保留一份最终 Prism 源项目及对应导出图，中间文件归入 `_work`，不要通过额外复制项目制造内外两份源文件。保留真实的 `.pzfx`、`.pzf` 或 `.prism` 格式，不把纯数据 XML 改名当作完整绘图项目。源项目必须保存本次请求的原始数据、图形、Prism 分析配置及结果和显著性标注，不能仅交付无分析或无标注的替代项目。

## Prism 原生分析和导出

统计检验由 Prism 执行，p 值和显著性以 Prism 结果表为准。Python 等外部脚本可以生成模拟数据、整理输入或核对文件，不代替 Prism 计算交付结果。比较括号和星号在 Prism 图内使用关联分析的 Pairwise Comparisons 添加并保存，随数据重算；不把外部计算的星号作为静态文本贴上去。

交付图片和 PDF 必须由 Prism 的导出命令或导出界面直接生成。标题、坐标范围、字体、误差条及版面均在 Prism 内调整；不通过外部裁切 PDF、重绘图表、叠加标注或渲染 PDF 来替代请求的原生导出。可读取导出文件做检查或完整复制到交付目录，但不修改内容。

需要统计检验时，先核对配对关系、检验类型、单双侧、误差定义以及比较对象，使用包含对应原生分析和图形标注的匹配模板。优先全程脚本执行：替换模板数据后，Prism 执行 `RecalcAll`，重新计算已有分析并更新关联星号；通过 `--results-index` 导出指定原生结果表，随后导出图形和保存源项目。无需每次操作电脑界面。只有首次缺少匹配模板时，才需要在 Prism 中配置分析和标注并保存；用户明确要求不用电脑控制时，使用已有模板，缺少模板则说明这一具体限制，不自行操作界面。`.pzc` 不支持从零任意设置统计分析；当前处理器也没有仅凭 `--layout column` 自动创建 t 检验的能力。缺少原生分析配置或执行能力时，应明确报告未完成，不转用外部统计或图片加工交付。模板创建步骤及脚本验收见 [references/native-statistics.md](references/native-statistics.md)。

## 从输入到成图

先检查用户输入的实际数据结构和绘图要求。可直接接收 CSV、TSV、XLSX、JSON；用户粘贴的表格先写成 UTF-8 CSV 或 JSON。对于 XLSX，仅绘图时无需另外生成 Excel 文档；用 `uv run --with openpyxl` 运行处理器。不要更改源数据文件。

技能自带模板的数据表统一显示 **3 位小数**，包括 XY 表的数值 X、Y 列和旧版兼容模板。此设置仅控制显示，不将原始值取整或舍入后写入项目；统计检验使用完整原始值，p 值及坐标轴的显示格式单独保留。交付时核对保存后的数据表小数位数。

按数据语义选择布局：

- `column`：各列为各组，行是独立观测值。组间样本数不同可留空。
- `xy`：第一列为数值 X，后续每列为一条 Y 序列。缺测 Y 留空，但 X 不能空。

默认保留所有观测值和组名，不补零、不删除离群值、不把重复测量当作独立样本。图形未指定时，独立组原始值优先列散点图；时间或剂量曲线优先 XY 图。对于需要汇总原始观测值的图形，用户未指定时默认使用 **Mean ± SEM（均值 ± 均值标准误）**，同时保留各个观测点；不再为默认误差条方式额外询问用户。用户明确指定 SD、置信区间、中位数、箱线图或其他展示方式时遵从其要求。

Mean ± SEM 的均值和误差条由 Prism 根据原始观测值计算，使用实际设置为 Mean with SEM 的匹配模板。模板已有 Mean with SD、Median 或其他设置时，不以继承模板为由覆盖这个默认值；先选用或配置匹配模板，再执行。当前处理器不会通过 `.pzc` 自动切换误差条类型，不能只改清单或图注把 SD 称为 SEM。仅有每个 X 的单个值、缺少足够重复值或输入已经是汇总数据时，不编造 SEM，也不把输入 SD 当成 SEM；核对输入实际含义和可用模板。配对结构、显著性检验、拟合及汇总数据的含义仍需用户信息或明确的表头支持，不从列名猜测检验。必要的歧义可询问，其他步骤继续完成。

## 模板与能力边界

自带 12 个已由本机 Prism 10.3.1 保存的配置：Welch t（SEM/SD）、普通独立样本 t、配对 t、Mann–Whitney、Wilcoxon、三组单因素 ANOVA + Tukey，以及散点 SEM、柱状加点 SEM、箱线图、两组配对连线、XY 曲线。使用 `profiles` 查看实际目录；完整选择表、输入范围和维护方法见 [references/template-library.md](references/template-library.md)。新目录使用 `.pzfx` 模板，目标为 D1/G1、统计模板 R1，只保留目标图和必要分析。旧 `.prism` 模板保留用于历史路径兼容，其 G3/R3 序号仍需按旧配置使用。

Prism 脚本可导入数据、修改标题及坐标范围、导出图，但不能任意创建图形或修改全部样式。`.pzfx` 的 XML 数据区适合 AI 替换原始值，图形和分析配置仍须保留。`.prism` 中分析参数和结果是 JSON，更适合检查和维护统计设置；本机已验证修改部分两样本 experimentalDesign 后由 Prism 重算的路径，但不承诺任意参数或版本可写。维护新模板时读取模板库说明，核对 Prism 保存后的真实方法与结果，不修改缓存结果代替重算。

用户提供的匹配 `.prism`/`.pzfx`/`.pzf`/`.pzt` 模板优先。非 `.pzfx` 模板先由 Prism 转存 XML 项目以填写数据，保留原生配置；已在本机 Prism 10.3.1 实测 `.prism` 输入和输出。未提供时，处理器尝试本机 `Portfolio/Graphs to explore` 的 `column-scatter`、`box-whisker`、`scatter-bars`、`xy-line` 四种现成模板；它们是否适合当前数据必须由实际模板检查和导出预览确认，不能把官方演示图当作通用出版模板。这些文件来自用户已有 Prism 安装，不随 skill 分发。

使用模板前检查实际表格类型、X 格式、子列数、数据集数量及图形；需要汇总和误差条时核对其原生设置，默认应为 Mean with SEM，用户指定其他方式时按指定值核对。处理器只支持原始 Column 数据和单 Y 子列的 XY 数据；拒绝不匹配的分组表、均值/误差表或额外数据集，避免部分数据漏画。较少的数据集会清空剩余模板列，预览时检查是否有空的图例或组位。多数据表模板必须明确指定 `--table-index`，并核对 `--graph-index` 是否引用该表；其他表不会被改写。

如果现有模板不能表达要求，先判断能否沿用已经验证的 `.prism` 参数修改路径，再让 Prism 重算、保存并验收新的完整模板；需要未知图形样式或尚未验证的分析时，在用户允许的电脑操作能力中创建真实模板。没有可用路径时说明缺少匹配模板，并请求用户保存一份模板。不要编造图形二进制区、用别的软件画图后称为 Prism 导出，或宣称只写出数据 XML 就已生成图形。

## 执行

常用分析优先使用 `--analysis welch-t|student-t|paired-t|mann-whitney|wilcoxon|anova-tukey`，默认 Mean ± SEM；Welch 可通过 `--error-bars sd` 切换为 SD。只绘图用 `--graph scatter-sem|bar-sem|box-minmax|paired-lines|xy-line`，不自动检验。处理器选择布局、模板和真实序号并记录清单，检查样本要求、容量、配对单边缺测、SHA256，以及保存后 `.prism` 的实际方法。两种参数入口互斥，不与自定义模板、旧 preset 或手动序号混用。未登记的方法、样式或误差线组合报错，不回退。坐标范围仍须检查或显式设置。

新增方法或图形时先保存完整原生模板并验收，再登记 [assets/analysis-profiles.json](assets/analysis-profiles.json) 或 [assets/graph-profiles.json](assets/graph-profiles.json)。目录已支持双侧两样本、完整配对和三组普通 ANOVA + Tukey 的验证；其他设计仍需扩展真实参数和数据检查，不能只改标签。ANOVA 同时导出总体检验 `statistics.txt` 和调整后比较 `comparisons.txt`。这是处理器选择配置，不是 `.pzc` 新增 Analyze 或 SetErrorBars 命令。

下面示例中的脚本路径应替换为当前 skill 的绝对路径；输出目录可按用户要求指定，默认放在输入旁边的 `prism-output`。

```powershell
uv run python "<skill>/scripts/prism_plot.py" doctor
uv run python "<skill>/scripts/prism_plot.py" profiles
uv run --with openpyxl python "<skill>/scripts/prism_plot.py" plot --input "D:\two-groups.xlsx" --analysis welch-t --output "D:\figures"
uv run --with openpyxl python "<skill>/scripts/prism_plot.py" plot --input "D:\two-groups.xlsx" --analysis welch-t --error-bars sd --output "D:\figures"
uv run --with openpyxl python "<skill>/scripts/prism_plot.py" plot --input "D:\two-groups.xlsx" --layout column --template "<skill>/assets/welch-mean-sem.prism" --table-index 1 --graph-index 3 --results-index 3 --output "D:\figures"
uv run python "<skill>/scripts/prism_plot.py" plot --input "D:\data.csv" --layout column --preset column-scatter --title "实验结果" --y-title "响应值" --output "D:\figures"
uv run --with openpyxl python "<skill>/scripts/prism_plot.py" plot --input "D:\data.xlsx" --sheet "Data" --layout column --template "D:\my-template.pzfx" --formats pdf png --output "D:\figures"
uv run python "<skill>/scripts/prism_plot.py" plot --input "D:\timecourse.csv" --layout xy --preset xy-line --x-title "Time (s)" --y-title "Signal" --formats pdf png --output "D:\figures"
uv run python "<skill>/scripts/prism_plot.py" plot --input "D:\two-groups.csv" --layout column --template "D:\welch-template.pzfx" --graph-index 3 --results-index 3 --output "D:\figures"
uv run python "<skill>/scripts/prism_plot.py" plot --input "D:\two-groups.csv" --layout column --template "D:\welch-template.prism" --graph-index 3 --results-index 3 --color-scheme Floral --title "Welch t test" --y-interval 20 --dpi 600 --project-format prism --output "D:\figures"
```

`--prism-exe` 或 `PRISM_EXE` 可指定 Prism 可执行文件。`doctor` 只检查安装和路径，不代表导出成功。`.pzfx` 模板可先用 `inspect-template --template <path>` 检查。指定 `--prepare-only` 仅准备项目和脚本、不启动 Prism；仅支持 `.pzfx` 模板。

Windows 默认通过可执行文件执行脚本，也支持 `--backend ole` 调用官方 `Prism.command.RunCommand`，无需电脑控制。CLI 转发失败时先看日志，确认原因后可显式用 OLE；OLE 使用系统注册版本，可能与 `--prism-exe` 不同。初始化失败、无完成标记或超时均保留诊断，不连续创建实例或关闭用户的 Prism 窗口。模板首次创建可以使用用户授权的界面配置，正常数据替换、重算和导出走原生脚本。

默认导出 PDF 和 300 dpi PNG。按用户要求可用 `--formats pdf png tif eps emf svg`；SVG 依赖 Prism 版本，老版本报未知命令时保留错误证据并改用用户允许的格式。栅格 `--dpi` 允许 100、300、600、1200。可用 `--x-min/--x-max/--y-min/--y-max` 显式设定范围。未设定时继承模板的坐标设置，必须核对预览是否截断数据；不要声称继承的范围必然自动适配。

需要美化时可用 `--color-scheme` 选择本机 Prism 已有方案，如 `Floral`、`Colorblind Safe`、`Waves`；用短标题、恰当的坐标范围及 `--x-interval/--y-interval` 主刻度间距改善可读性。600 dpi 用于提高栅格导出分辨率，PDF 保留矢量图。配色不改变检验与误差条含义，不把提高 DPI 称为字体或线宽美化。字体、字号、轴线宽、点大小、横纵比例及组名角度由模板控制，当前 `.pzc` 不能任意调整；不修改不透明图形二进制配置，也不后处理图片冒充原生样式。详细样式选择及脚本限制见 [references/appearance.md](references/appearance.md)。

`--results-index N` 使用 `GoTo R N` 和 `ExportTable` 将选中的原生结果表导出为制表符文本 `statistics.txt`，路径记录为清单的 `results_export`；它不会创建或更改统计分析类型。示例中的 G3/R3 仅适用于对应模板，必须核对实际序号。读取结果表核对检验名称、p 值、样本数和显著性；仅存在非空文件不能证明选对了分析。

## 完成标准和失败处理

检查 `manifest.json` 的状态、完成标记、每个请求导出文件的存在和格式签名，并读取输出项目核对数据值、组名和空值。打开 PNG 预览检查图形类型、图例、坐标范围、模板残留文字和全部数据集是否画出。核对并在交付说明或清单中记录实际汇总与误差条定义：默认 Mean ± SEM，用户指定时记录其指定方式；不能从外观或误差条较短推断已经使用 SEM。预览有裁剪、错误标签或示例标注时修正匹配模板或坐标设置后再交付；不要仅根据退出码或文件存在认定图正确。

执行超时或 Prism 退出而无完成标记时，说明实际错误、保留运行目录和 `.log`，不能报告成功。不自动关闭用户已有的 Prism 窗口或终止其进程。处理器不修改注册表、授权信息或 Prism 安装文件；自动重试前先查明失败原因。让用户手动在 Prism 中选择“运行脚本”可用于诊断，但不能把等待用户执行说成已完成。

交付时优先给出本次运行文件夹内源项目的可点击路径，同时给出同层图、实际导出格式、使用的模板和必要的数据整理说明；注明项目内实际保存的图形、分析和标注，区分“已实测 Prism 导出”“仅准备完成”和“执行失败”。整理文件夹时保留唯一的最终源项目，不把它当作可丢弃的中间文件，不为方便点击另建项目副本。

官方命令和输入格式的补充信息见 [references/prism-automation.md](references/prism-automation.md)，仅在调整模板或命令时阅读。
