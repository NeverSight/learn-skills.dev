---
name: vensim-skill
description: "Build, lay out, check and simulate Vensim system dynamics models (.mdl). Use when the user wants a stock-and-flow or causal loop diagram in Vensim, needs an existing MDL tidied (overlapping labels, crossing arrows, messy views), wants polarity and R/B loop checks, or needs reproducible simulation, scenario, sensitivity, calibration or policy runs with publication-quality Python plots. Chinese variable names by default; Windows, macOS and Linux."
license: "Non-commercial only; commercial use, paid redistribution and commercial delivery are prohibited; see LICENSE"
metadata:
  version: "2.4.0"
---

# Vensim 建模、排版与仿真

从模型结构和方程出发生成或整理真实的 `.mdl`，用命令完成排版和检查，再做可复现的仿真和结果图。本工具是独立项目，不是 Ventana 官方产品。

## 硬性规则

1. **坐标交给命令，不手写。** 新模型用 `build` 从 JSON 生成，已有模型用 `layout`。不要自己算坐标、改草图记录或画示意图代替 MDL。排版规则（间距、弧度、绕行支路、回路标记位置）已经写在代码里，依据见 [APPEARANCE.md](references/APPEARANCE.md)。新模型的 JSON 从 [ev_adoption_zh.json](assets/templates/ev_adoption_zh.json) 复制起步，视图、links、feedback_loops 和命名都照它的写法。
2. **已有模型默认 `auto`。** 作者的版面合格就不动；只有一两处压字时只挪那几个变量；问题多时才重建。用户明确要求重画时才用 `--mode natural`。
3. **交付前 `visual --strict` 和 `check --strict` 必须通过**：`visual` 管几何（零交叉、不压字、文字不重叠、没有过短箭头、`<Time>` 预留区空着），`check` 管 Vensim 打开时的提示（缺单位、没有被使用的变量）。报告里列出的对象 ID 要逐个处理，不能靠删线、隐藏或改方程过关。原图里保留、`auto` 也消不掉的问题（如 Overshoot 的 1 处穿字），要在交付说明里写明对象 ID，不能算通过。
4. **排版不改模型。** 输出写新文件，方程区逐字节不变。唯一的结构改动是 natural 在不可平面处加的影子引用，报告里逐条列出，因果关系不变。
5. **视图只做关键的。** 定义变量约 40 个以内用一个视图；更大的模型按子系统分，每个视图 6–40 个定义变量，对应一条主要存量链或一组紧密相关的机制；跨视图引用用影子变量。不做一个变量一个视图、两三个变量的碎视图，也不把上百个变量挤在一起。
6. **图面朴素。** 存量画方框，流量画阀门和双线管道，其余变量只写名字。信息线统一黑色（`monochrome`），或 Vensim 传统纯蓝（`native-blue`）。图内只放变量、极性、延迟标记和核对过的 R/B，不加标题、水印、底色、说明框或装饰。
7. **新模型默认中文变量名。** 用户要求英文时用英文；Vensim 函数和 `INITIAL TIME` 等控制变量保持英文。修改已有模型时不改变量名。
8. **极性和回路按方程判断**，不按变量名或曲线涨跌猜。用 `feedback` 核对；非线性、查表关系说明适用范围，判断不了的标为待核对，不硬填符号。
9. **参数来自当前资料。** 时间范围、初值、参数、情景幅度、抽样次数和种子都按当前任务确定；示例和参考模型里的数值不能拿来填空。缺资料时列出缺项。
10. **结果图用 Python 出，默认无标题。** 坐标框细线、刻度朝内、无网格；颜色和线型同时区分曲线；超过 8 条曲线分组出图（`max_lines`），蒙特卡洛画分位带；数据不平滑、不删点。样式依据见 [RESULT_PLOTS.md](references/RESULT_PLOTS.md)。
11. **结构图从 Vensim 导出。** `preview` 生成的 HTML/SVG 用估算字宽，只用来定位问题。没有 Vensim 时交付 MDL 和检查报告，并写明“未在 Vensim 中核对”。
12. **如实报告。** 几何检查通过（`pass`）和已在 Vensim 中核对是两回事；没做的检查不能写成通过。内置引擎或 PySD 的结果不能说成 Vensim 原生运行。

## 工作顺序

1. 读模型或资料：`doctor` 看环境，`inspect`、`audit`、`check` 看结构和方程。截图只用来定位问题，不能据此猜方程。
2. 先修语义问题（未定义变量、断裂引用、缺初值、缺单位、没有被使用的变量），再排版。
3. 新模型：照模板写建模 JSON（格式见 [SPECIFICATIONS.md](references/SPECIFICATIONS.md)），`build` 生成 MDL，排版、极性和回路核对一起完成（二十几个变量约需 20 秒，不要中断）。输出里的每条“建议”都要处理：名字过长就精简，没声明的回路按给出的条目补进 `feedback_loops`，常量被移到别的视图就改 JSON；改完重新 `build`。
4. 已有模型：`layout` 输出新文件，`visual --strict` 检查；不合格时按报告里的对象 ID 处理，必要时用 `node_positions` 固定个别变量后重跑。
5. 在 Vensim 中打开每个视图，运行 Check Model 和 Units Check，导出结构图。
6. 仿真和实验：`simulate`、`experiment`、`convergence`；装了 PySD 时用 `crosscheck` 对照。结果图用 `graph` 或 `plot-data`。
7. 交付 MDL、CSV、运行清单（`.run.json`）、图件和检查报告；不交付 `preview` 调试图和临时文件。

## 命令

在 skill 目录执行；Windows 把 `./skill.sh` 换成 `skill.cmd`。需要 Python 3.10+。

```bash
./skill.sh doctor
./skill.sh build model.json --output work/model.mdl
./skill.sh audit work/model.mdl
./skill.sh check work/model.mdl --strict                                 # 缺单位、没人用的变量也算失败
./skill.sh fix work/model.mdl --output work/model_fixed.mdl --mark-supplementary  # 没人用的输出指标标 Supplementary
./skill.sh feedback work/model.mdl --spec model.json --strict
./skill.sh layout work/model.mdl --output work/model_layout.mdl          # 默认 auto
./skill.sh layout work/model.mdl --output work/redrawn.mdl --mode natural
./skill.sh visual work/model_layout.mdl --strict
./skill.sh simulate work/model_layout.mdl --output results/base.csv     # 不写 --var 导出全部变量
./skill.sh crosscheck work/model_layout.mdl --var 库存 --output results/crosscheck.json
./skill.sh experiment work/model_layout.mdl --spec experiment.json --output-dir results/runs --plot figures/runs.png
./skill.sh convergence work/model_layout.mdl --var 库存 --output results/convergence.json
./skill.sh calibrate work/model_layout.mdl --spec calibration.json --data observed.csv --output-dir results/fit
./skill.sh optimize work/model_layout.mdl --spec policy.json --output-dir results/policy
```

各命令加 `--help` 查看完整参数。输出文件已存在时命令会拒绝覆盖，重跑请换新文件名或新目录。

## 按需阅读

| 文件 | 什么时候读 |
| --- | --- |
| [APPEARANCE.md](references/APPEARANCE.md) | 排版、视图划分、排版模式和配置 |
| [FEEDBACK.md](references/FEEDBACK.md) | 箭头极性、R/B 回路判断与标注位置 |
| [SIMULATION.md](references/SIMULATION.md) | 支持的函数、时间设置、后端对照、批量实验、校准与政策搜索、研究报告要求 |
| [RESULT_PLOTS.md](references/RESULT_PLOTS.md) | 结果图样式与可调参数 |
| [SPECIFICATIONS.md](references/SPECIFICATIONS.md) | 建模、实验、校准 JSON 的字段 |
| [REFERENCES.md](references/REFERENCES.md) | 规则依据与已知边界 |
| [reference_models](assets/reference_models/README.md) | 7 个真实教材模型；遇到老化链、绕行支路、多视图时先看作者怎么画 |

内置引擎覆盖常见标量函数，数组、宏、外部数据交给 PySD 或 Vensim。`--keep-going` 产生的诊断结果不能出图或写进结论。

非商业许可，作者 传康KK（万能程序员），详见 [LICENSE](LICENSE)。
