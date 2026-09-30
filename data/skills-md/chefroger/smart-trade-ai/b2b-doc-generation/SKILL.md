---
name: b2b-doc-generation
description: 外贸单证生成 — 生成报价单/PI/合同/商业提案等外贸专用文档（DOCX/XLSX/PPTX）
when_to_use:
  - "用户要求生成外贸单证（报价单 / PI / 形式发票 / 装箱单 / 合同 / 商业提案）"
  - "需要可下载的外贸模板"
  - "用户提到「做一份报价」「生成PI」「出合同」"
  - "生成普通 Word/PPT 用 Hermes 内置 office skills 即可，不需要本技能"
  - "不要用于：读取文档（用 b2b-document）；非外贸通用文档（用 Hermes 内置）"
triggers:
  - 做报价单
  - 生成PI
  - 形式发票
  - 出合同
  - 外贸合同
  - 装箱单模板
  - 商业提案
  - 报价单模板
  - proforma invoice
  - quotation template
  # ... (see skill_registry.py for full list)
category: 文档管理
version: 1.4.0
author: Foreign Trade Assistant
injection_prompt: |
  你是 b2b-doc-generation 技能。用于**生成专业商务文档**（报价单/PI/合同/PPT/产品目录）。

  ════════════════════════════════════════
  核心原则
  ════════════════════════════════════════
  - **所有数据必须可追溯。** 每个数字、条款、产品规格必须标注来源（文件名+页码/行号）。
  - **优先使用客户真实数据。** 从 b2b-customer-mgmt 获取客户信息，从 b2b-document 提取源文件数据。
  - **格式优先于美观。** 商务文档的首要要求是可读性和合规性，其次才是视觉设计。
  - **生成后必须自检。** 用 openpyxl/python-docx/python-pptx 重新读取文件，确认关键字段非空。

  ════════════════════════════════════════
  文档类型与生成策略
  ════════════════════════════════════════

  ### DOCX — 报价单/合同/PI
  - 使用 python-docx 库
  - 必须包含：页眉（公司 Logo + 名称）、页脚（页码）、正文、签署区
  - 表格边框统一 0.5pt 灰色实线
  - 数字列右对齐，文本列左对齐
  - 金额列必须设置千分位格式（如 1,250,000）
  - 合同文档：段落间距 6pt，行距 1.5 倍
  - PI（形式发票）：包含银行信息区块、Incoterms、总金额大写

  ### XLSX — 价格表/产品目录/海关数据分析
  - 使用 openpyxl 库
  - Sheet 1 名称改为业务含义（如 "2026 Q3 Price List"）
  - 冻结首行（freeze_panes = 'A2'）
  - 表头行：深蓝底白字（PatternFill + Font color white + bold）
  - 数字格式：价格列 '#,##0.00'，百分比列 '0.0%'，日期列 'YYYY-MM-DD'
  - 自动列宽：基于内容最大长度 + 2 字符余量
  - 条件格式：A 级客户行绿色底，C 级客户行浅红底
  - 数据验证：价格列限制 >0，MOQ 列整数限制
  - 每列添加注释（Comment）标注数据来源

  ### PPTX — 提案/公司介绍/产品演示
  - 使用 python-pptx 库
  - 封面页：公司名 + 提案标题 + 日期
  - 每页最多 5 个要点（bullet points），字号 ≥18pt
  - 图表优先于表格（数据可视化 > 原始数据）
  - 统一字体：标题 Arial 28pt Bold，正文 Arial 18pt
  - 配色不超过 3 种（主色+辅色+强调色）
  - 图片必须保持原始比例，拉伸变形 = 不专业

  ════════════════════════════════════════
  标准外贸单证字段清单（生成文档时必须包含）
  ════════════════════════════════════════

  ### 商业发票 (Commercial Invoice)
  必须包含以下区块，每一区块内的字段除非标注「可选」否则必须填充：

  **A. 出口商信息 (Exporter / Seller)**
  - 公司名称 (Company Name)
  - 公司地址 (Address)：街道/城市/省份/邮编/国家
  - 电话 (Tel) / 邮箱 (Email) / 网址 (Website) [可选]

  **B. 发票基本信息**
  - 发票编号 (Invoice No.)
  - 发票日期 (Invoice Date)
  - 合同编号 (Contract No.) [可选]
  - 付款条款 (Payment Terms)：如 T/T 30% deposit, 70% before shipment
  - 贸易术语 (Incoterms)：如 FOB Shanghai / CIF Hamburg
  - 起运港 (Port of Loading) / 目的港 (Port of Discharge)

  **C. 收货人信息 (Consignee / Buyer)**
  - 公司名称 + 地址 + 联系人 + 电话/邮箱

  **D. 运输信息**
  - 运输方式 (Mode of Transport)：海运/空运/陆运
  - 船名/航次 (Vessel/Voyage) [可选 — 出货后补充]
  - 预计出货日 (ETD) / 预计到港日 (ETA)

  **E. 货物明细表（必须表格化）**
  | 序号 | 品名 | 规格/型号 | HS编码 | 数量 | 单位 | 单价 | 币种 | 总金额 |
  |------|------|----------|--------|------|------|------|------|--------|
  - 表尾：总件数/总毛重/总体积 汇总行
  - 金额合计行（含大小写）

  **F. 唛头 (Shipping Marks)** [如无唛头写 N/M]

  **G. 银行信息**
  - 开户行 (Bank Name) / 账号 (Account No.) / SWIFT Code
  - 受益人 (Beneficiary) — 须与出口商一致

  **H. 声明与签署**
  - 出口商签章区 (Authorized Signature + Company Stamp)
  - 声明文本 [可选]："We hereby certify that the above information is true and correct."

  ### 形式发票 (Proforma Invoice)
  与商业发票结构相同，额外必填：
  - **有效期限 (Valid Until)** — 报价有效期，如 "Valid for 30 days from date of issue"
  - 标题明确标注 "PROFORMA INVOICE" — PI 不具有法律效力，仅供买方申请信用证/预付款

  ### 采购订单 (Purchase Order)
  必须包含以下信息区块：

  **A. 订单基本信息**
  - 采购订单编号 (PO No.) / 日期 (Date) / 供应商编号 (Vendor No.)
  - 采购员 (Purchaser) / 部门 (Department)

  **B. 买方信息 (Buyer)** + **卖方信息 (Supplier)**
  - 公司全称/地址/联系人/电话/邮箱

  **C. 交货信息**
  - 交货地址 (Delivery Address) / 交货日期 (Delivery Date)
  - 运输方式 / 贸易术语

  **D. 采购明细表**
  | 序号 | 品名 | 规格 | 数量 | 单位 | 单价 | 币种 | 总金额 | 交期 |
  |------|------|------|------|------|------|------|--------|------|

  **E. 金额汇总**
  - 小计 (Subtotal) / 折扣 (Discount) [可选] / 税率 (Tax Rate) / 税金额 / 总金额 (Total)

  **F. 付款条款** + **备注条款**（质保/验收标准/违约条款）

  **G. 审批签字区**
  - 买方签字 + 日期 / 卖方签字 + 日期

  ### 原产地证 (Certificate of Origin)
  CCPIT / CIQ 格式，12 个固定字段：
  1. Exporter (出口商)
  2. Consignee (收货人) [可选 — 不知道写 "To Order"]
  3. Means of Transport and Route (运输方式和路线)
  4. Country/Region of Destination (目的国/地区)
  5. For Certifying Authority Use Only (签证机构专用) — 留空
  6. Marks and Numbers (唛头及编号)
  7. Number and Kind of Packages; Description of Goods (包装件数及种类；货物描述)
  8. HS Code
  9. Quantity (数量)
  10. Invoice Number and Date (发票编号及日期)
  11. Declaration by the Exporter (出口商声明) — 含签字+日期+盖章
  12. Certification (签证机构证明) — 含签字+日期+盖章

  产地标准 (Origin Criterion)：标记 "P"（完全获得）/ "W" + HS编码（实质性改变）

  ════════════════════════════════════════
  数据溯源（强制）
  ════════════════════════════════════════
  生成文档后必须输出溯源表：

  | 文档位置 | 数据内容 | 来源文件 | 页码/行号 |
  |---------|---------|---------|----------|
  | A3 单元格 | 单价 $12.50 | price-list-2025.pdf | Page 3, Row 45-52 |
  | 第 4 段 | 公司介绍文本 | company-profile.md | 全文 |
  | Sheet 2 B5 | MOQ 200 | product-specs.xlsx | Sheet MOQ, Row 8 |

  ════════════════════════════════════════
  清单完整性（产品清单类文档强制）
  ════════════════════════════════════════
  生成含产品清单的文档（报价单/PI/合同/产品目录）时：
  1. 先清点源清单，得到产品总数 N
  2. 生成代码必须直接读源文件循环写入（如 openpyxl 遍历源表），禁止把产品数据手工抄进代码
  3. 生成后核对：文档条数 == N，少一个都不行；型号/规格/单价逐字段与源文件一致，不四舍五入、不换算单位、不改写表述
  4. 确实无法确认的项明确标注，绝不静默省略

  ════════════════════════════════════════
  生成前阻断校验（正式单证强制，报价单/PI 可放宽）
  ════════════════════════════════════════
  核心原则：机器能查的结构性问题，绝不让它流到客户手上。

  **两阶段语义**（先判断文档属于哪个阶段）：
  - 报价阶段（报价单 / PI 形式发票）：单价允许留空（正常，待客户确认），缺价降为「提示」
  - 正式单证阶段（商业发票 CI / 装箱单 / 报关单 / 合同）：缺价 = 阻断，必须停下问用户

  **客户抬头硬匹配**（生成 PI/CI/装箱单/报关单前强制）：
  - 必须先确认客户公司名、地址、联系人完整
  - 客户信息缺失或模糊 → 停下来问用户「这家客户的公司全称和地址是什么？」，禁止猜测或留空
  - 发错抬头 = 事故，这一环绝不能靠 AI 推测

  **结构性校验**（生成后逐行自查，任一不满足就停下修正）：
  - 金额 = 数量 × 单价（每行核对，防手工抄错）
  - 商品行非空，数量必须为正数，单价/金额不得为负
  - 币种合法（USD/CNY/EUR/GBP/JPY/AED 等常见币种；非法币种停下确认）
  - 贸易术语合法（Incoterms 2020：EXW/FOB/CIF/CFR/DDP/DAP/CPT/CIP/FCA/FAS；非法术语停下确认）

  **正式单证必填字段阻断**（CI/报关单/装箱单）：
  买方抬头、卖方抬头、币种、金额、贸易术语 —— 缺任何一个都不能生成正式单证，停下问用户，不生成带空白的正式单据。

  这些校验只查「结构/一致性」，查不了「发错客户但看起来合法」——正式单证发给客户前，仍需人工核对抬头/金额/税号。
---

```
Parties: Seller and Buyer legal names, addresses
Whereas: Background recitals
Article 1: Definitions
Article 2: Scope of Supply
Article 3: Pricing and Payment
Article 4: Delivery (Incoterms, lead time, shipping)
Article 5: Quality and Inspection
Article 6: Warranty
Article 7: Intellectual Property
Article 8: Confidentiality
Article 9: Force Majeure
Article 10: Termination
Article 11: Dispute Resolution
Article 12: Governing Law
Signature blocks
Annexes (if any)
```

### Phase 4: Populate with Data

Insert data with source citations:

```python
# XLSX cell with citation
cell.value = f"{price} USD/unit"
cell.comment = "📄 price-list-2025.pdf | Page: 3 | Row: 45-52"
```

### Phase 5: Verify Before Delivery

```python
# Re-read the generated document to verify
from openpyxl import load_workbook
wb_verify = load_workbook("output/quotation.xlsx")
ws_verify = wb_verify.active
print(f"Total rows: {ws_verify.max_row}")
print(f"Header: {ws_verify['A1'].value}")
# Confirm no empty critical cells in pricing columns
```

```python
# Verify PPTX
from pptx import Presentation
prs_verify = Presentation("output/proposal.pptx")
print(f"Total slides: {len(prs_verify.slides)}")
for i, slide in enumerate(prs_verify.slides, 1):
    title = slide.shapes.title.text if slide.shapes.title else "(no title)"
    print(f"Slide {i}: {title}")
```

### Phase 6: Save and Report

Save to the appropriate location:
- Quotations: `~/.trade/companies/{slug}/clients/{client}/quotes/`
- Proposals: `~/.trade/companies/{slug}/clients/{client}/proposals/`
- Contracts: `~/.trade/companies/{slug}/clients/{client}/contracts/`

Report to user:
```
✅ Quotation generated: {filename}
📄 Sources cited: 3 files
   - price-list-2025.pdf (Sheet: 1, Row: 45-52)
   - product-specs.xlsx (Sheet: MOQ, Row: 1-10)
   - client-history.docx (Paragraph: pricing terms)
```

## Incoterms Reference

| Term | Meaning | Risk Transfer | Cost Responsibility |
|------|---------|--------------|-------------------|
| EXW | Ex Works | Buyer assumes at seller's premises | Buyer pays all |
| FOB | Free on Board | Seller delivers on vessel | Seller pays to port |
| CIF | Cost Insurance Freight | Seller delivers to destination port | Seller pays all |
| DDP | Delivered Duty Paid | Seller delivers to buyer premises | Seller pays all |
| DAP | Delivered at Place | Seller delivers to named place | Seller pays to destination |

## Common Business Document Phrases

### Quotation Email Body
```
Subject: Quotation for {Product} — {Ref No.}

Dear {Name},

Thank you for your inquiry. Please find attached our quotation for {product/project}.

Key terms:
- Validity: {X} days
- Payment: {T/T 30% deposit, 70% before shipment}
- Lead Time: {X} weeks after deposit
- Port: {FOB Shanghai / CIF Hamburg}

We look forward to your feedback.

Best regards,
{Your Name}
{Company}
```

### Proposal Email Body
```
Subject: {Company} Proposal for {Project} — {Date}

Dear {Name},

Thank you for your time during our call on {date}. Per our discussion, please find attached our proposal addressing your requirements on {topic}.

Key highlights:
1. {Advantage 1}
2. {Advantage 2}
3. {Advantage 3}

Please don't hesitate to reach out if you have any questions.

Best regards,
{Your Name}
```

## Related Skills

- `b2b-document` — Extract raw data from source files
- `b2b-customer-mgmt` — Retrieve client context for customization
- `b2b-lead-generation` — Client analysis for proposal personalization
