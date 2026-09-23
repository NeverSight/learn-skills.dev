---
name: personal-finance-cn
description: 中文个人财务管理技能。记录收支、分析账单（支付宝/微信/CSV）、生成月度报告、追踪储蓄目标，全程人民币。
version: "1.0.0"
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "emoji": "💰", "user-invocable": true, "homepage": "https://github.com/Allen091080/personal-finance-cn", "tags": ["finance", "chinese", "life", "accounting"]}}
---

# 个人财务管理（中文版）

帮你记账、分析账单、生成报告、追踪储蓄目标。支持支付宝/微信账单 CSV 直接导入，全程人民币，无需任何 API Key。

## 适用场景

| 场景 | 用这个？ |
|------|---------|
| 记录一笔收入或支出 | ✅ 是 |
| 导入支付宝/微信账单分析消费 | ✅ 是 |
| 生成月度收支报告和图表 | ✅ 是 |
| 设置储蓄目标并追踪进度 | ✅ 是 |
| 分析哪类支出占比最高 | ✅ 是 |
| 预测下月支出 | ✅ 是 |
| 查汇率/股票 | ❌ 否，用专门的金融技能 |

## 数据文件格式

账单数据默认存储在 `~/finance/ledger.csv`，格式如下：

```csv
日期,类型,金额,分类,备注,账户
2026-03-01,支出,38.50,餐饮,午餐,微信支付
2026-03-01,收入,15000.00,工资,3月工资,招商银行
2026-03-02,支出,299.00,购物,运动鞋,支付宝
```

### 支持的分类

**支出**：餐饮、购物、交通、住房、娱乐、医疗、教育、通讯、旅行、其他支出
**收入**：工资、奖金、兼职、投资收益、其他收入

## 如何使用

### 1. 初始化账本

```bash
python3 {baseDir}/scripts/finance.py init
```

### 2. 记录一笔账

```bash
# 记录支出
python3 {baseDir}/scripts/finance.py add --type 支出 --amount 38.5 --category 餐饮 --note "午餐" --account 微信支付

# 记录收入
python3 {baseDir}/scripts/finance.py add --type 收入 --amount 15000 --category 工资 --note "3月工资" --account 招商银行
```

### 3. 导入支付宝/微信账单

```bash
# 支付宝账单（下载后直接导入）
python3 {baseDir}/scripts/finance.py import --file ~/Downloads/alipay_record.csv --source alipay

# 微信支付账单
python3 {baseDir}/scripts/finance.py import --file ~/Downloads/wechat_pay.csv --source wechat
```

### 4. 生成月度报告

```bash
# 当月报告
python3 {baseDir}/scripts/finance.py report --month 2026-03

# 指定月份
python3 {baseDir}/scripts/finance.py report --month 2026-02 --chart
```

### 5. 查询收支统计

```bash
# 本月支出分类汇总
python3 {baseDir}/scripts/finance.py summary --month 2026-03

# 查看支出最高的10笔
python3 {baseDir}/scripts/finance.py top --type 支出 --limit 10

# 查看储蓄趋势（近6个月）
python3 {baseDir}/scripts/finance.py trend --months 6
```

### 6. 设置储蓄目标

```bash
# 设置目标：6个月内存 30000 元
python3 {baseDir}/scripts/finance.py goal --name "旅行基金" --target 30000 --deadline 2026-09-01

# 查看目标进度
python3 {baseDir}/scripts/finance.py goal --status
```

## 与 AI Agent 对话示例

```
用户：帮我记一笔账，今天午饭花了45块，用的支付宝
Agent：✅ 已记录：2026-03-14 支出 ¥45.00 餐饮「午饭」支付宝

用户：分析一下我这个月的消费情况
Agent：[运行 report 命令，输出图表和文字分析]

用户：我这个月餐饮花了多少？
Agent：[查询餐饮分类，返回总额和每笔明细]
```

## 重要规则

1. **所有金额单位为人民币（¥/CNY）**，不做多币种转换
2. **数据文件路径默认 `~/finance/ledger.csv`**，可通过 `--file` 参数指定
3. **生成图表时设置中文字体**：
   ```python
   import matplotlib; matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   plt.rcParams['font.family'] = 'PingFang HK'  # macOS
   ```
4. **导入外部账单前先备份**：`cp ~/finance/ledger.csv ~/finance/ledger.bak.csv`
5. **隐私优先**：所有数据存本地，不上传任何云端
