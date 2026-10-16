---
name: kaiwu-coding-skill
metadata:
  version: "0.3.6"
description: "使用 QBoson Kaiwu SDK（Enterprise/Community）将组合优化问题建模为 QUBO/Ising，处理约束、精度、版本兼容与求解结果。适用于选址、调度、路径、覆盖、布尔规则、Max-Cut、混合离散连续优化，或修复 kaiwu 建模/求解 API。PyTorch 能量模型与 RBM/BM/DBN、QVAE、QDiffusion 使用独立的 kpp-coding-skill。"
---

# Kaiwu 建模与求解

先确认目标解释器、发行版和版本；题目已给出且已安装授权时直接采用，不重复安装或询问。
未安装时使用目标环境的 `python -m pip install kaiwu`（Enterprise）或
`python -m pip install kaiwu-community`（仅建模）。二者导入名都为 `kaiwu`。
本地 Enterprise 求解需要已有授权；云端 CIM 只在用户要求且提供凭据时使用。

## 先保证模型等价

区分原业务目标、可行域和求解能量。用简短公式说明变量、目标和全部约束，代码应表达同一模型。
原目标最大化时可以取负构造 QUBO，报告值仍按原目标计算。

| 原要求 | 二次编码；P 为正的硬约束罚系数 |
|---|---|
| 恰好一个／等式 | `P * (sum(x) - c)**2` |
| 至多一个 | `P * sum(x[i]*x[j] for i<j)` |
| 两文字 OR：至少一真 | `P * (1-a)*(1-b)`；不是 `(a+b-1)**2` |
| 带权软 OR | 权重乘违反指示；单文字为 `1-a`，两文字为 `(1-a)*(1-b)` |
| 整数资源上限 `load <= C` | `P*(load+s-C)**2`，非负整数松弛 s 覆盖所有 `0..C` |
| 至少一个（多变量） | `P*(sum(x)-1-s)**2`，s 覆盖 `0..n-1` |

布尔正文字真值为 x，负文字为 `1-x`。OR 的违反指示仅在所有文字为假时为 1；
不能用 `1-sum(literals)`（可能为负），也不能用 `sum(1-literals)**2`（改变偏好）。
三个以上文字的乘积是高阶项，不能直接当二次模型；需适当辅助变量与等价降阶。

松弛变量可直接用 `Integer('slack', min_value=0, max_value=C)`，也可用二进制权重编码。
例如上限 C=5，权重 `[1,2,2]` 可以恰好表示 0..5；C=0 不创建松弛比特。
一般 C>0 取 `k=C.bit_length()-1`，权重 `[2**j for j in range(k)] + [C-(2**k-1)]`。
容量允许剩余，不能把 `(load-C)**2` 当作上限约束。

罚系数应覆盖原目标可能改善的范围：若硬罚项最小非零值为 1，取 P 大于原目标上、下界之差。
带权软规则可取大于权重总和；非负分配成本可取大于每项成本上界之和。
过大系数会拉大动态范围、增加采样难度，应写明依据，不能靠无限增大 P 修复错误模型。
存在可证明的局部修复界时优先使用更紧的界。例如非负加权顶点覆盖，目标为
`sum(w[i]*x[i])`、罚项为 `P*sum((1-x[u])*(1-x[v]))`：取 `P>max(w)` 即可。
权重为非负整数时，默认直接取 `P=max(w)+1`，不凭感觉再加大罚系数。
因为任一未覆盖边可增加一个端点，目标增加不超过 `max(w)`，罚项至少减少 P，且不会新增违反。
这只适用于这种单调覆盖约束，不能套用到容量、互斥或等式约束；必须说明修复不会破坏其他约束。

## Enterprise 1.4.0：直接采用这个 API 流程

下面是可运行的三选一示例，只展示 SDK 调用与解码；替换目标、罚项及原业务校验来处理实际问题。
不要发明 `kaiwu.seed`、`QuboModel.add_variable`、`vartype` 或 `iterations_per_temperature` 等接口。

```python
import numpy as np
from kaiwu.core import (ndarray, Binary, QuboModel, PenaltyMethodConstraint,
                        qubo_matrix_to_ising_matrix, qubo_model_to_ising_model,
                        get_sol_dict, get_val)
from kaiwu.classical import SimulatedAnnealingOptimizer

x = ndarray(3, 'x', Binary)
original = 3*x[0] + 2*x[1] + 4*x[2]
model = QuboModel()
model.set_objective(original + 10*(x.sum()-1)**2)
model.set_constraint_handler(PenaltyMethodConstraint)  # 传类，不实例化
q = model.get_matrix()
h, offset = qubo_matrix_to_ising_matrix(q)  # offset 是常数，不是变量字典
variables = qubo_model_to_ising_model(model).get_variables()
solver = SimulatedAnnealingOptimizer(
    initial_temperature=100, alpha=0.99, cutoff_temperature=0.001,
    iterations_per_t=100, size_limit=32, rand_seed=20261001)
pool = np.asarray(solver.solve(h))
valid = []
for row in pool:
    sol = get_sol_dict(row[:-1]*row[-1], variables)
    bits = [int(round(get_val(x[i], sol))) for i in range(3)]
    if sum(bits) == 1:  # 实际问题须在这里重算全部原业务约束
        valid.append((int(round(get_val(original, sol))), bits))
if not valid:
    raise RuntimeError('SDK 候选中没有可行解')
cost, decision = min(valid)
print({'bits': decision, 'objective': cost, 'feasible': True})
```

已核实的 SA 参数：`initial_temperature, alpha, cutoff_temperature, iterations_per_t,
size_limit, flag_evolution_history, verbose, rand_seed, process_num`。
不要传 `seed`、`time_limit`、`num_reads`。控制运行时间需在外层管理批次，不能伪造构造参数。
示例的 bits 是二进制决策，不等于每种任务的 solution 字段。
任务约定 RESULT=JSON 时使用 `json.dumps`；覆盖题的 solution 是选中站点编号，
布尔配置题的 solution 才是按业务顺序的0/1列表。不得照抄示例打印方式而忽略当前输出协议。
中小型受约束问题可增加 `iterations_per_t`，或使用多批次、不同 `rand_seed` 的 SDK 候选；
同时记录实际耗时并遵守用户时限。示例参数是起点，不保证每个问题达到最优。

若罚系数使 Ising 矩阵幅值远大于示例温度，初温 100 可能不足以探索。
在任务未固定参数时，可先取 `initial_temperature=max(100, 2*np.max(np.abs(h)))`；
对数十个变量的本地受约束题可用 `iterations_per_t=200, size_limit=128` 作为起点，
再依据实际候选质量和时限判断。不要直接复用小示例的温度和解池大小却宣称保证最优。

对百个以上变量、题目没有固定采样参数的优化交付，不能只运行小示例的低采样配置就结束。
以质量为目标、约40秒执行预算时，128～512个变量且耦合稀疏（非零比例低于10%）的默认批次
为 `iterations_per_t=(200,800,2400)`、`size_limit=128`。其他参数保持一致，始终使用指定种子，
原矩阵只编译一次。变量更多、矩阵稠密或预算更短时，从 `(200,400,800)` 等小批次开始实测。
每批后按实际耗时与下一批迭代数比例预估开销，至少留20%的余量和2秒解码输出时间。
预计本批能在剩余时间内完成时继续默认批次，不能仅因已经找到可行解或上一批未改善而提前停止；
预计超时则立即返回已有最佳可行候选，不为了跑完固定批次数而超时。整个程序只保留一个统一截止时间。
在用户执行时限内，对所有实际返回候选重新计算原业务目标，保留代价最低的可行候选；
这属于程序内有预算的求解策略，不是让模型根据失败反馈重写代码。不要拿第一条可行候选当最佳结果。
软偏好不是硬约束：没有硬约束时不要人为引入大罚系数，也不额外添加题目未要求的平衡限制。

**按规模和复杂程度调整默认参数。** 上述数值是经验起点，不是所有问题的固定配方。
先看变量数、非零耦合数、系数范围和硬约束强度，再结合执行时限安排单批规模。
稠密矩阵或很多辅助变量会增加每次求解开销；先用小批次实测，预留编译、解码和输出时间。
增加迭代、放慢降温或扩大解池并不保证更好的业务结果；累计保留此前最佳可行 SDK 候选，
比较候选的可行比例、原业务代价和实际用时后决定是否继续，不能覆盖掉更好的旧候选。
优先修正错误建模或过大的罚系数，再调参数；记录使用的参数和停止条件，不许声称保证最优。

**先遵守任务指定的实验参数。** 若题目固定随机种子，每次创建求解器都显式使用同一个指定的
`rand_seed`，不要递增、另造种子列表或用时间产生种子；上面的多种子建议只用于任务允许的情形。
在固定种子下，只有题目允许时才调整温度、迭代数等参数；记录真实配置，不把重试结果替换成首次交付。

`solve` 返回未按能量排序的自旋池，末列是参考自旋；遍历每一行，先乘参考自旋归一化，
再用 **Ising 模型**的变量字典解码。用 `get_val` 访问变量，不猜内部字符串键。
只有从实际候选解码并通过原题校验的决策才能输出；不可用穷举、硬编码答案或第三方求解器替换 SDK。

自己加在目标里的罚项不等于已登记约束：没有 `add_constraint` 时，
`verify_constraint` 返回 0 也不能证明原题可行。无论是否登记，都从决策重算全部业务约束。
若调用 `verify_constraint`，先解包 `unsatisfied, details = model.verify_constraint(sol)`。
业务成本与 QUBO／Ising 能量分开打印，不能把罚项、常数偏移或最大化负号当业务指标。

带权软规则的报告口径服从题目：若要求“最小化违反代价”，报告
`sum(weight for rule in soft if not satisfied(rule))`，选候选也取这个值最小的合法方案。
“满足权重和”与“违反代价”相加等于软权重总和，两者优化方向相反，不能混用字段名 objective。
输出前按最终 bits 重新计算原目标；即使决策相同，报告相反口径的数值也属于交付错误。

## 版本与专题资料：只读取相关部分

| API | Enterprise 1.3.1 | Enterprise 1.4.0 |
|---|---|---|
| QuboModel | `kaiwu.qubo` | `kaiwu.core` |
| 两个 QUBO/Ising 转换器 | `kaiwu.conversion` | `kaiwu.core` |
| ndarray/Binary/Integer/quicksum/get_val/get_sol_dict/PenaltyMethodConstraint | `kaiwu.core` | `kaiwu.core` |
| 数组取值 | 逐元素 `get_val` 或 `get_array_val` | `get_val` 支持数组；没有 `get_array_val` |
| PrecisionReducer | `kaiwu.cim` | `kaiwu.preprocess` |
| 罚函数法求解器 | `kaiwu.solver.PenaltyMethodSolver` | `kaiwu.hybrid.PenaltyMethodOptimizer` |

版本已知时直接导入对应模块。明确要求跨版本或无法确认时，仅对实际迁移的导入做兼容分支。
`quicksum` 跨版本传 list；`ndarray((n,m), 'x', Binary)` 用位置参数。
Community 不能假定具有本地经典求解器。

- 1.3.x 或更完整签名：[Enterprise API](references/kaiwu_enterprise.md)、[API 总览](references/api_reference.md)。
- 1.3.x TSP 历史示例：[SDK 范例](references/examples.md)；迁移至 1.4.x 必须按上表更换导入。
- 精度处理：`PrecisionReducer` 是优化器装饰器，版本间默认值变化，显式写 `only_feasible_solution`；
  `perform_precision_adaption_split` 返回 `(split_matrix, last_var_idx)`，按映射还原并验证原矩阵能量。
- 其他接口：[模块索引](references/module_docs.md)、[Community](references/kaiwu_community.md)。
- 同时含连续量与离散决策：先写完整耦合约束；Kaiwu 求离散候选，固定离散量后用连续／流子问题裁决。
  不把大量连续量整体二进制展开，不删除“未启用则流量为零”等耦合约束。

## 交付与验证

从零生成时给完整脚本；修改已有代码时给必要改动。遵守题目数据、输出协议与时限，优先保证代码完整。
执行条件允许时先检查导入，再实际编译、求解、解码、核对原业务；任务禁止运行时不声称已运行。

数学自查关注两点：每个合法业务状态是否能取辅助变量使硬罚项为零；此时能量是否等于原目标加常数。
可在独立开发验证中用真值表或小实例穷举查编码错误，但不得把该枚举结果混作 SDK 返回结果。
只有拿到参考界或独立证明才宣称最优；否则报告已找到可行解、实际目标值和未证明最优的限制。

## 补充：代码交付规范

以下规则约束新增和修改的 SDK 代码；保留上文的建模与版本要求。

- **保持单一职责。** 将建模、SDK 求解、候选解码、原业务校验分别组织为清楚的步骤；规模较小时用一个脚本和少量函数即可。不要为了调用一次 SDK 引入通用框架、插件注册、多层继承或大量转发包装。删除本次改动产生的死代码、重复分支和未用依赖。
- **使用已确认的接口。** 已知 SDK 版本时直接导入相应 API，不扫描整个包、轮流尝试猜测的类名和参数。确需兼容已有多个版本时，只围绕实际迁移的接口写窄分支，不把业务错误伪装成版本兼容问题。
- **异常必须有明确处理结果。** 只在输入、授权、外部调用等实际边界捕获能处理的具体异常；无法恢复就保留原因并失败退出。禁止 `except Exception: pass`、多层重复捕获、无限重试，以及出错后返回假的可行解或“成功”默认值。固定内部计算不添加无意义的 `try/except`。
- **按真实边界校验。** 对外部数据检查所需的维度、取值范围和约束一致性；内部已经验证的数据不层层重复检查，不为一个本地小脚本附加与任务无关的安全框架。密钥从已有环境或配置读取，不硬编码、不写入日志；不要用 `eval`、`exec` 或拼接 shell 命令解析数据。安装、联网和云端提交遵守当前任务的授权范围。
- **让求解开销可控。** 根据变量规模和时限设置温度衰减、每温度迭代数与解池大小，避免一开始就堆极大参数。外层检查截止时间不能中断一次已经阻塞的 `solve`，因此单批次也必须足够小；使用单调时钟管理批次，记录实际耗时。达到调用、时间或费用上限后停止，不靠重复重连拖延。
- **减少无效计算。** 重用不变的矩阵、数据和变量映射；候选逐批解码和筛选，不无界积累重复解，不用巨大中间数组替代清楚的计算。不得为追求速度删掉真实约束、改变原目标或用非 SDK 答案替换求解结果。
- **让索引与单位明确。** 输入编号和数组下标在入口统一转换；正负文字用 `idx = abs(literal) - 1` 定位，再决定是否取反。区分业务目标、罚项与能量偏移，使用能说明含义的变量名，不在多个函数中各写一套相互矛盾的换算。
- **只做能说明正确性的验证。** 检查代表性可行/不可行边界、原业务目标和实际 SDK 候选来源；不把只匹配实现文字的测试当作证明。交付完整、可运行的必要代码，明确实际验证过什么；不能运行时直接说明，不伪造运行记录。
