---
name: data-analysis

description: 全链路数据分析技能，支持表格(CSV/Excel)、文档(PDF/DOCX/MD)及图像数据的处理。
    核心工作流强制遵循：1. 安全探查：仅读取元数据与少量样本，严禁全量加载以防Token溢出；2. 质量体检：自动检查缺失、重复与一致性；3. 代码执行：基于Python(Pandas/Matplotlib)进行清洗、统计与可视化；4. 结果验证与报告生成。
    适用场景：探索性分析(EDA)、多模态数据提取、图表绘制及生成数据洞察报告。
---

# 数据分析技能  

## 支持的输入数据类型  

1. 表格形式的数据：csv、xlsx  
2. 文本中包含的数据：docx、pdf、md  
3. 图片中包含的数据：png、jpg  

## 步骤一：数据读入与探查  

为了防止 Token 溢出和执行环境卡死，智能体 严禁 直接打印全量数据或将其加载到 Prompt 上下文中，只允许将必要的数据概要加载进上下文。  

### 1. 数据读入与保存  

对不同类型的数据应使用不同的读取方法：  

- csv: 直接使用pandas库读取
- xlsx: 使用pandas库或 \xlsx 工具读取
- docx: 使用 \docx 工具读取，并将其中待分析的目标数据提取出来保存为csv文件
- pdf: 使用 \pdf 工具读取，并将其中待分析的目标数据提取出来保存为csv文件  
- md: 直接读取，并将其中待分析的目标数据提取出来保存为csv文件
- png、jpg: 使用视觉工具读取，并将其中待分析的目标数据提取出来保存为csv文件  

### 2. 数据探查  

在编写正式分析代码前，必须先执行一段轻量级的探查代码。将代码保存至工作空间。  

**原则：** 

**只看样貌，不看全貌：** 仅获取元数据和少量样本。  

**元数据优先：** 必须获取列名（Columns）和数据类型（Dtypes）。  

**样本限制：** 严格限制读取行数（推荐n=5）。  

**探查全部文件：** 若有多份待分析的文件，需要对所有文件逐一探查，并检查文件间可能存在的关联，将具体关联方式保存为csv文档或md文件，供后续分析进行参考。  

**标准探查代码模式 (Python示例):** 

```python 

import pandas as pd

# 设定文件路径
file_path = 'target_data.csv'

try:
    # 1. 仅读取前5行，避免加载大文件占用内存
    # 注意：对于非CSV文件 (如 Parquet, Excel)，使用相应的 read_ function 并配合 head()
    if file_path.endswith('.csv'):
        df_preview = pd.read_csv(file_path, nrows=5)
    elif file_path.endswith('.parquet'):
        df_preview = pd.read_parquet(file_path).head(5)
    elif file_path.endswith(('.xls', '.xlsx')):
        df_preview = pd.read_excel(file_path, nrows=5)
    
    # 2. 输出关键元数据供智能体思考
    print("=== 数据预览 (前5行) ===")
    print(df_preview.to_markdown(index=False))
    
    print("\n=== 列信息与类型 ===")
    print(df_preview.info())
    
except Exception as e:
    print(f"摄入错误: {e}")
```

### 3.  编码与格式自适应  

编码回退：如果读取失败，尝试 \`encoding='gbk'\` 或 \`encoding='latin1'\`。  
分隔符：如果数据挤在一列，尝试 `sep=';'` 或 `sep='\t'`。  

## 步骤二：数据质量检查  

在进行任何分析前，必须先“体检”。这能避免“垃圾进，垃圾出”。检查结果需放在最后的报告中。  

以下是详细的检查清单：  

### 1. 完整性  

检查数据是否存在缺失，这会直接影响统计的偏差。  

**缺失值：**

检查字段中 NULL 、 NaN  或空字符串的比例。  
- 注意“伪缺失值”，例如用 -1 、 0 、 9999  或 "Unknown" 来代替缺失值的情况。  

**记录缺失：** 

- 数据量是否符合预期？（例如：昨天的日志应该有 100万条，实际只有 20万条）。
- 时间序列是否连续？（例如：是否缺失了某几天的交易数据）。  

**截断:**  

文本字段是否因为字符长度限制被截断（例如 JSON 字符串不完整）。  

### 2. 唯一性  

检查数据是否存在重复，这会导致指标被夸大。  

**完全重复:** 检查是否存在完全相同的行。  

**主键重复:** ID 字段是否唯一？（例如：同一个 UserID 不应该出现在用户表的两行中）。  

**业务实体重复:** 同一个业务对象是否因为大小写不同、空格不同而被记录了多次（例如 "Apple"和 "apple" ）。


### 3. 准确性与有效性  

检查数据是否符合定义的格式和现实世界的物理规则。  

**数据类型:** 
- 数值字段里是否混入了字符串？
- 日期字段是否真的是日期格式？  

**取值范围:** 
- 数值是否在合理范围内？（例如：年龄不应为负数或超过 150；折扣率不应大于 100% ）。
- 概率值是否在 0 到 1 之间？  

### 4. 一致性  

检查数据在不同维度或来源上是否统一。  

**单位统一:** 距离是米还是千米？金额是元还是分？  
**枚举值统一:** 同样的含义是否有多种表达？（例如： "Beijing" , "BJ" , "北京"  应该标准化为同一种）。  
**跨表一致性:** 两个表中相同含义的字段，数据是否对得上？（例如：订单表中的总金额是否等于详情表中各商品金额之和）。  

### 5. 关联性  

若多份文件间存在关联关系，检查关系是否断裂。  
**外键约束:** 事实表中的 ID 是否都能在维度表中找到？（例如：订单表里的 product_id ，在商品表中是否存在？如果不存在，就是“孤儿数据”）。  

**代码示例：**  

```python  
import pandas as pd
# --- 1. 完整性检查 (Completeness) ---
for col in COLS_CHECK_MISSING:
    # 检查 NULL/NaN
    missing_count = df[col].isnull().sum()
    # 检查空字符串 (如果是字符串列)
    empty_str_count = (df[col] == '').sum() if df[col].dtype == 'object' else 0
    total_missing = missing_count + empty_str_count
    if total_missing > 0:
        print(f"  -> 警告: 列 '{col}' 存在 {total_missing} 条缺失数据")
    else:
        print(f"  -> 通过: 列 '{col}' 无缺失")
# --- 2. 唯一性检查 (Uniqueness) ---
if df[COL_PRIMARY_KEY].duplicated().any():
    duplicate_count = df[COL_PRIMARY_KEY].duplicated().sum()
    print(f"  -> 警告: 主键 '{COL_PRIMARY_KEY}' 发现 {duplicate_count} 条重复记录")
    # 可选：查看重复样本
    # print(df[df[COL_PRIMARY_KEY].duplicated(keep=False)])
else:
    print(f"  -> 通过: 主键唯一")
# --- 3. 准确性检查 (Accuracy) ---
# 过滤出不符合规则的行
invalid_rows = df[df[COL_NUMERIC] < MIN_VALUE_THRESHOLD]
if not invalid_rows.empty:
    print(f"  -> 警告: 发现 {len(invalid_rows)} 条数据小于最小值 {MIN_VALUE_THRESHOLD}")
else:
    print(f"  -> 通过: 数值范围正常")
# --- 4. 一致性检查 (Consistency) ---
# 找出不在标准列表中的值
# fillna(False) 是为了处理空值情况，避免报错
invalid_mask = ~df[COL_CATEGORY].isin(VALID_CATEGORIES) & df[COL_CATEGORY].notnull()
invalid_cats = df.loc[invalid_mask, COL_CATEGORY].unique()
if len(invalid_cats) > 0:
    print(f"  -> 警告: 列 '{COL_CATEGORY}' 包含非标准值: {invalid_cats}")
else:
    print(f"  -> 通过: 枚举值一致")
# --- 5. 关联性检查 (Integrity) ---
# 注意：此步需要有一个参考表 (ref_df)
try:
    # 找出在当前表中存在，但在参考表(ref_df)中找不到的 ID
    # 同样排除了当前表外键为空的情况
    orphan_mask = ~df[COL_FOREIGN_KEY].isin(ref_df[COL_REF_KEY]) & df[COL_FOREIGN_KEY].notnull()
    orphan_count = orphan_mask.sum()
    if orphan_count > 0:
        print(f"  -> 警告: 发现 {orphan_count} 条“孤儿数据” (在维表中找不到对应记录)")
    else:
        print(f"  -> 通过: 外键关联完整")
except NameError:
    print("  -> 跳过: 未定义 ref_df (维表)，无法进行关联检查")
```

## 步骤三：确定工作流程  

根据任务需求确定具体的工作流程，优先使用用户指定的分析方法，不要使用与任务无关的分析方法。工作流程一般包含数据处理、分析和可视化呈现。  

### 核心分析方法  

#### 1. 统计分析  

* **描述性统计：** 均值、中位数、标准差、四分位数、百分位数  
* **推断性统计：** 假设检验、置信区间、P值  
* **相关性分析：** 皮尔逊 (Pearson)、斯皮尔曼 (Spearman)、肯德尔 (Kendall)、点二列 (Point-biserial) 相关系数​  
* **分布分析：** 正态性、偏度、峰度、Q-Q图  
* **高级统计检验：** 方差分析 (ANOVA)、t检验、卡方检验、非参数检验  

#### 2. 模式发现  

* 趋势分析与时间序列分解  
* 季节性模式检测与预测  
* 聚类与细分：K-means、层次聚类、DBSCAN  
* 关联规则挖掘与购物篮分析  
* 特征工程与特征选择  
* 降维技术：PCA (主成分分析)、t-SNE、UMAP  

#### 3. 商业智能  

* KPI 分析与仪表板设计  
* 客户细分与画像  
* 购物篮分析与推荐系统  
* 流失预测与客户生命周期价值 (CLV)  
* A/B 测试与实验设计  
* ROI (投资回报率) 分析与业务影响评估  
* 摘要与可落地的行动建议  

#### 4. 探索性技术  

* 单变量分析：分布、统计量、可视化
* 双变量分析：相关性、对比、关系
* 多变量分析：回归、聚类、分类
* 时间序列分析：趋势、季节性、预测
* 类别数据分析：频数、列联表、关联性
* 空间分析与地理模式
* 文本分析与自然语言处理 (NLP)  

### 核心可视化方法  

目标是通过深思熟虑的视觉设计，让数据变得易于理解、富有洞察力。每一个可视化都应该清晰明了，并帮助使用者做出更好的决策。  

#### 针对数值型数据  

* **分布：** 直方图、箱线图、小提琴图、密度图
* **比较：** 条形图、折线图、散点图
* **关系：** 散点图、相关性矩阵、热力图
* **构成：** 堆叠条形图、饼图、树状图
* **趋势：** 折线图、面积图、移动平均图  

#### 针对分类型数据  

* **频率：** 条形图、饼图、环形图（甜甜圈图）
* **比较：** 分组条形图、堆叠条形图
* **关系：** 热力图、马赛克图、平行集合图
* **构成：** 树状图、旭日图  

#### 针对时间序列数据  

* **趋势：** 折线图、面积图、平滑曲线
* **季节性：** 季节性分解、热力图
* **比较：** 多重折线图、分面图（Faceted plots）
* **分布：** 基于时间的箱线图、小提琴图  

#### 高级技巧  

* **交互式仪表盘**: 创建多面板仪表板、添加筛选器和控件  

* **动画可视化**: 展示随时间的变化、阐释复杂过程  

### 报告撰写  

根据用户的要求确定所需的报告类型，若无明确要求只需给出一份md格式的数据分析报告。  

#### 报告类型  

* **执行摘要：** 分析过程文档，为使用者提供任务执行的全部过程
* **商业数据分析报告：** 数据驱动的商业洞察，对数据分析的结果进行总结和剖析
* **仪表盘文档：** 交互式图表说明  

#### 报告格式  

markdown、pdf、docx

#### 报告风格和内容 

* **准确性:** 细致、严谨、语言清晰，确保所有统计数据和事实均正确无误
* **逻辑性:** 从数据到洞见的逻辑发展
* **专业性:** 理解关键发现和统计意义，识别数据中的模式和趋势
* **基于数据:** 围绕数据发现构建有深度的叙述
* **可执行的见解:** 明确的建议和后续步骤
* **视觉集成：** 如果是pdf或docx类型的报告，需要插入合适的图表，并确保视觉与文本的一致性，设计合适的布局  
* **可读性：** 不要使用类似“行业黑话”的难懂的词汇，避免不必要的细节，措辞简单易懂且书面化。
 
## 步骤四：规范代码生成与执行  

### 编程语言  

- Python: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Plotly, TensorFlow, PyTorch   
- R: Tidyverse, ggplot2, dplyr, caret, shiny, data.table​   
- SQL: PostgreSQL, MySQL, SQLite, BigQuery, Redshift, Snowflake   
- JavaScript: D3.js, Plotly.js, Chart.js, TensorFlow.js, Node.js  

#### 常用技术栈（Python）  

- 核心处理: \`pandas\`, \`numpy   
- 统计与挖掘: \`scipy\`, \`sklearn\` (如需)   
- 可视化: \`matplotlib\`, \`seaborn\` (静态); \`plotly\` (交互式)   
- 工具库: \`tabulate\` (美化打印), \`\xlsx\`工具, \`\pdf\`工具, \`\docx\`工具  

### 代码生成步骤  

#### 第一阶段：需求分析  

- 根据上一步骤确定的分析流程，明确分析目标和输出要求  
- 选择合适的编程语言（若无明确指定，默认为Python）  
- 选择库和框架  
- 考虑性能和可扩展性需求

#### 第二阶段：结构设计  

- 设计模块化代码结构，将复杂任务分解为小而专一的函数  
- 将复杂任务分解为可管理的功能  
- 规划可重用性和可维护性  
- 注意内存管理 ：高效处理大型数据集  

#### 第三阶段：实施  

- 编写简洁高效的代码
- 加入适当的错误处理
- 添加清晰简洁的注释
- 执行代码得到结果  

#### 错误处理  

- 数据加载错误：处理文件丢失、格式问题及编码问题。  
- 内存问题：实施分块 (chunking)或数据采样。  
- 性能问题：优化算法，使用缓存和并行处理。  
- 依赖问题：检查库版本，提供回退选项。  

## 步骤五：结果验证与输出  

在将结果呈现给用户之前，必须执行以下自检清单：  

### 完整性检查：  

- [ ] 所有的结果文件（.png/.html/.xlsx/.pdf等）是否已成功生成并在工作空间存在？  
- [ ] 关键的计算结果（如 KPI、统计量）是否非空且数值合理？  
- [ ] 输出文件（如 CSV）是否包含数据且表头正确？  
- [ ] 用户所需的所有结果文件是否都完整生成？  

### 格式一致性：  

- [ ] 图表是否有标题、轴标签和图例？
- [ ] 报告字体是否统一，标题层级关系是否明确？ 
- [ ] 报告中的图片是否位置合适，有清晰的标签和说明？ 

确认通过质量门控后，才可以交付。  

## 示例  

### 示例 1：基础销售数据趋势分析（结构化数据）

**用户指令：**
“帮我分析一下 `sales_2023.csv`，我想看下半年的销售趋势，另外数据里好像有些退款订单，记得处理一下。”

**智能体执行流：**

1.  **步骤一（数据探查）：**
    执行 `pd.read_csv('sales_2023.csv', nrows=5)`。
    **发现：** 列包含 `date`, `amount`, `status`, `product_id`。`date` 为字符串格式，需转换。

2.  **步骤二（质量检查）：**
    **完整性：** 检查 `amount` 是否有空值。
    **一致性：** 检查 `status` 字段，发现包含 "Refund" 和 "Completed"。
    **动作：** 过滤掉 `status == 'Refund'` 的行，只保留已完成订单。

3.  **步骤三 & 四（分析与执行）：**
    **处理：** 将 `date` 转为 datetime 对象，按月聚合 `amount`。
    **代码：** 使用 Pandas 进行 `resample('M').sum()`。
    **可视化：** 生成折线图 `sales_trend.png`，标注峰值月份。

4.  **步骤五（交付）：**
    输出简报和折线图：“2023下半年销售额在 11 月达到峰值（受大促影响），剔除 45 条退款记录后，总营收为 X 元。”

### 示例 2：跨文件关联分析（多模态/复杂场景）

**用户指令：**
“我有产品类目的定义文件 `categories.xlsx`，还有一份最近的用户反馈日志 `feedback.pdf`。请分析一下哪个产品类目的负面反馈最多。”

**智能体执行流：**

1.  **步骤一（数据读入）：**
    对于 `categories.xlsx`：使用 Pandas 读取前 5 行，确认包含 `product_id` 和 `category_name`。
    对于 `feedback.pdf`：调用 `\pdf` 工具提取文本，通过 LLM 结构化解析为 CSV 格式（包含 `product_id`, `sentiment`, `content`），保存为 `temp_feedback_parsed.csv`。

2.  **步骤二（关联性检查）：**
    **探查：** 读取 `temp_feedback_parsed.csv` 样本。
    **关联性：** 检查反馈表中的 `product_id` 是否都能在 `categories.xlsx` 中找到。
    **警告：** 发现 3 个 `product_id` 在类目表中不存在，标记为“未知类目”。

3.  **步骤三 & 四（分析与执行）：**
    **逻辑：** 将两张表基于 `product_id` 进行 Merge。
    **筛选：** 过滤 `sentiment == 'Negative'` 的记录。
    **统计：** 按 `category_name` 进行 `value_counts()`。
    **可视化：** 使用 Seaborn 绘制横向条形图 `negative_feedback_by_category.png`。

4.  **步骤五（交付）：**
    生成 Markdown 报告，输出可视化图片，指出“电子产品”类目负面反馈最高，主要集中在“电池续航”问题上（基于文本聚类发现）。
