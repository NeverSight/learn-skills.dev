---
name: hop-sdk-skills
version: 1.0.0
description: 汇元开放平台代码生成技能，通过调用 Python 脚本获取 API 方法详细信息，结合 reference/hyw-demo 项目结构自动生成完整的 Maven 项目代码。
author: zhangxw

# 技能触发说明
# 用户可以通过以下方式触发此技能：
# 1. 直接提及 API 方法名称：如 "pay.heepay.bank.apply"、"网银支付"
# 2. 使用相关业务词汇：如 "支付代码"、"上传代码"、"订单代码"
# 3. 明确的指令：如 "生成 API 代码"、"帮我写支付接口代码"

tags:
  - 代码生成
  - 开放平台代码
  - Java 代码生成
  - pay.heepay.bank.apply
  - 网银支付
  - bank.apply
  - heepay
  - pay
  - customer.file.upload
  - 文件上传
  - mall.order.pay.apply
  - 商城支付
  - order.pay
  - 入网申请
  - 小微商户
  - 商户开户
  - 企业入驻
  - 发票开具
  - 投诉处理
  - 余额支付
  - 快捷支付
  - 骏卡支付
  - 商城订单
trigger_patterns:
  - "生成.*代码"
  - ".*API.*代码"
  - ".*支付.*代码"
  - ".*上传.*代码"
  - ".*订单.*代码"
  - ".*入网.*代码"
  - ".*申请.*代码"
  - ".*小微.*代码"
  - ".*商户.*代码"
  - ".*开户.*代码"
  - ".*发票.*代码"
  - ".*投诉.*代码"
  - ".*查询.*代码"
  - ".*通知.*代码"
  - ".*短信.*代码"
  - ".*鉴权.*代码"
  - ".*转账.*代码"
  - ".*提现.*代码"
  - ".*余额.*代码"
  - ".*快捷.*代码"
  - ".*骏卡.*代码"
  - ".*商城.*代码"
  - "pay\\.heepay\\.bank\\.apply"      # 核心支付方法
  - "customer\\.file\\.upload"         # 核心上传方法
  - "mall\\.order\\.pay\\.apply"       # 核心订单方法
parameters:
  - api_method (string): API 方法编码，例如 `pay.heepay.bank.apply`
dependencies:
  - python-dotenv
  - requests
---

# AI 助手代码生成指南

**重要：** 当用户请求生成 API 代码时，你必须按照以下步骤执行：

## 🎯 技能触发条件

当用户提到以下任何一种情况时，自动激活此技能：
- 提及具体的 API 方法名称（如：pay.heepay.bank.apply、customer.file.upload）
- 使用业务相关词汇（如：支付、上传、订单、网银）
- 明确的代码生成请求（如：生成代码、写接口代码、API 调用代码）

## 📖 核心参考文档

在开始代码生成之前，**必须仔细研究 `reference/hyw-demo/` 目录中的完整 Maven 项目**：

**重要说明**：reference 目录位于技能项目的根目录下，完整路径为：`{项目根目录}/reference/`

### 项目结构参考（reference/hyw-demo/）

```
hyw-demo/
├── pom.xml                                          # Maven 配置（含 SDK 本地依赖）
├── lib/
│   └── hop-java-sdk-1.0.0-SNAPSHOT.jar             # 汇元 HOP SDK
├── src/main/java/com/hyw/demo/
│   ├── Application.java                             # Spring Boot 启动类
│   ├── config/HywConfig.java                        # 商户配置（固定模板）
│   └── vo/                                          # 所有请求/响应/嵌套对象
│       ├── PayHeepayBankApplyRequest.java
│       ├── PayHeepayBankApplyResponse.java
│       └── GoodsInfo.java
├── src/main/resources/logback.xml
└── src/test/java/com/hyw/demo/
    └── PayHeepayBankApplyTest.java                   # 接口测试类
```

**执行要求：**
- ✅ 生成的代码将直接输出到用户指定的完整项目中
- ✅ 多次生成会追加到同一个项目（vo/ 追加类、test/ 追加测试类、controller/ 追加方法、static/ 追加页面）
- ✅ 代码结构、命名规范、注解使用必须与 reference/hyw-demo 中的示例保持一致

## 步骤 1: 询问用户输出路径

在生成代码之前，**必须先询问用户**希望将项目生成到电脑的哪个路径。

示例对话：
> 请问您希望将生成的 Maven 项目放到哪个目录？（例如：`D:\projects\hyw-demo` 或 `C:\Users\xxx\Desktop`）

用户指定路径后，使用该路径作为输出目录的父路径，项目将生成在 `{用户指定路径}/hyw-demo/` 下。

如果用户未指定路径，则默认生成到技能项目根目录下的 `generated/hyw-demo/`。

## 步骤 2: 调用 Python 脚本获取 API 方法信息

```bash
python script/main.py <api_method> --generate-code --output-dir <用户指定的路径>
```

这会返回完整的 JSON 响应，包含：
- `data.info`: 方法基本信息
- `data.request_fields`: 请求参数字段列表（数组）
- `data.response_fields`: 响应字段列表（数组）

**注意：** 添加 `--generate-code` 参数后，Python 脚本会自动生成完整的 Maven 项目到用户指定的目录。

## 步骤 3: 分析 API 信息并规划代码结构

### 3.1 固定包路径（与 hyw-demo 项目一致）

生成的所有代码都放在固定的包路径下：
- **请求/响应/嵌套对象**: `com.hyw.demo.vo` → `src/main/java/com/hyw/demo/vo/`
- **配置类**: `com.hyw.demo.config` → `src/main/java/com/hyw/demo/config/`（固定模板）
- **控制器**: `com.hyw.demo.controller` → `src/main/java/com/hyw/demo/controller/`（自动生成）
- **测试页面**: `src/main/resources/static/`（自动生成）
- **测试类**: `com.hyw.demo` → `src/test/java/com/hyw/demo/`

### 3.2 确定类名
- **请求类**: `{request_model_class_info.name}.java`（例：`BankPayApplyRequest.java`）
- **响应类**: `{response_model_class_info.name}.java`（例：`BankPayApplyResponse.java`）
- **子对象类**: 遍历所有字段，如果有 `type_class_info`，则需要生成对应的子对象类
- **测试类**: `{基础名}Test.java`（例：`BankPayApplyTest.java`）

## 步骤 4: 生成 Java 代码

**重要：** 代码生成器会自动完成以下工作：

1. **初始化项目骨架**：首次生成时自动从 `reference/hyw-demo/` 复制 pom.xml、Application.java、logback.xml、lib/、HywConfig.java
2. **生成 VO 类**：请求类、响应类、嵌套对象全部放入 `src/main/java/com/hyw/demo/vo/`
3. **生成测试类**：每个 API 生成独立的测试类到 `src/test/java/com/hyw/demo/`
4. **验证测试类**：自动生成后自动验证测试类的正确性（字段完整性、类型匹配、语法检查等）
5. **生成 HTML 测试页面**：在 `src/main/resources/static/` 下生成测试页面，启动项目后可在浏览器中测试
6. **生成 TestController**：处理前端测试页面的 API 请求，接口路径为 `/api/{camelCaseMethod}`
7. **更新 index.html**：自动维护接口测试入口页面，列出所有已生成的接口

**重要要求：**
- ✅ **必须导入**：`import com.fasterxml.jackson.annotation.JsonProperty;`
- ✅ **每个字段必须添加 `@JsonProperty("原始json_name")` 注解**（非常重要！）
- ✅ 生成的代码结构、命名规范、注解使用必须与 reference/hyw-demo 中的示例保持一致

## 步骤 5: 输出项目路径和文件清单

生成完成后，告诉用户项目位置和生成的文件：

```
已为您生成完整的 Maven 项目：

📁 项目目录：{用户指定的路径}/hyw-demo/

已生成 / 更新的文件：
1. src/main/java/com/hyw/demo/vo/BankPayApplyRequest.java - 请求类（12 个字段，8 个必填）
2. src/main/java/com/hyw/demo/vo/BankPayApplyResponse.java - 响应类（12 个字段）
3. src/main/java/com/hyw/demo/vo/GoodsInfo.java - 嵌套对象（4 个字段）
4. src/test/java/com/hyw/demo/BankPayApplyTest.java - 接口测试类
5. src/main/resources/static/pay_heepay_bank_apply.html - 接口测试页面
6. src/main/resources/static/index.html - 接口测试入口页
7. src/main/java/com/hyw/demo/controller/TestController.java - 接口测试控制器

 快速开始：
1. 使用 IDE 打开项目
2. 右键 pom.xml → Add as Maven Project
3. 修改 HywConfig.java 中的商户配置（appId、私钥等）
4. 运行测试类中的方法，或启动项目后访问 http://localhost:8825 使用浏览器测试

💡 多次生成说明：
- 再次调用会追加到同一个项目中
- vo/ 目录会添加新的请求/响应类
- test/ 目录会添加新的测试类
- static/ 目录会添加新的测试页面，index.html 自动更新
- controller/ 会追加新的接口方法
```

## 验证清单

### 代码生成器自动验证
- [ ] 所有请求字段都有对应的 setter 调用
- [ ] 嵌套对象正确初始化（new 对象 + 设置字段）
- [ ] 括号匹配，无语法错误
- [ ] 字段类型与赋值匹配（String 类型不会赋值纯数字）
- [ ] 必要的 import 语句存在

### 人工验证
- [ ] 所有 request_fields 和 response_fields 都已生成对应的 Java 字段
- [ ] 每个字段都添加了 `@JsonProperty("原始json_name")` 注解
- [ ] 字段类型正确映射（String→String, Int→Integer, Bool→Boolean）
- [ ] 嵌套对象生成了独立的 Java 类
- [ ] 项目骨架完整（pom.xml、lib/、Application.java、logback.xml）
- [ ] 生成了测试类
- [ ] 生成了 HTML 测试页面和 TestController
- [ ] 多次生成时代码正确追加到同一项目

## 技术实现说明

代码生成器的具体实现可在 `script/code_generator.py` 文件中查看，主要包括：

1. **项目骨架初始化**：首次生成时从 reference/hyw-demo/ 复制静态文件（pom.xml、lib/、Application.java 等）
2. **Java 代码生成**：根据 API 字段信息生成请求/响应/嵌套对象类，全部放入 vo/ 包
3. **测试类生成**：为每个 API 生成独立的测试类
4. **测试类验证**：生成后自动验证测试类的正确性（字段完整性、类型匹配、语法检查）
5. **HTML 测试页面生成**：在 `src/main/resources/static/` 下生成每个接口的测试页面，含表单和 AJAX 请求
6. **TestController 生成**：Spring Boot 控制器，接口路径为 `/api/{camelCaseMethod}`，处理前端测试页面的请求
7. **index.html 维护**：自动更新接口测试入口页面，列出所有已生成的接口链接

### 输出项目结构

```
generated/hyw-demo/
├── pom.xml
├── lib/
│   └── hop-java-sdk-1.0.0-SNAPSHOT.jar
├── src/main/java/com/hyw/demo/
│   ├── Application.java
│   ├── config/HywConfig.java
│   ├── controller/TestController.java  ← 接口测试控制器
│   └── vo/                    ← 请求/响应/嵌套对象
├── src/main/resources/
│   ├── logback.xml
│   └── static/                ← 测试页面
│       ├── index.html
│       └── {api_method}.html
└── src/test/java/com/hyw/demo/  ← 测试类
```

### 调用方式

```bash
# 基本用法
python script/main.py <api_method>

# 示例
python script/main.py pay.heepay.bank.apply

# 生成代码（默认输出到 generated/hyw-demo/）
python script/main.py pay.heepay.bank.apply --generate-code

# 生成代码到指定路径
python script/main.py pay.heepay.bank.apply --generate-code --output-dir D:\projects

# 高级选项
python script/main.py pay.heepay.bank.apply --info-only    # 仅查看方法信息
python script/main.py pay.heepay.bank.apply --fields-only  # 仅查看请求参数字段
```

### 返回数据结构

Python 脚本返回的 JSON 包含三个核心部分：
- `data.info` - 方法基本信息（名称、描述、版本、类信息等）
- `data.request_fields` - 请求字段列表（数组，包含字段名、类型、验证规则等）
- `data.response_fields` - 响应字段列表（数组）

### OpenClaw 集成

```yaml
command: python script/main.py {{api_method}}
env:
  # 环境配置已在 .env/.env.test/.env.prod 中定义
```

**注意：** 使用 OpenClaw 时无需手动安装 Python 依赖，由 OpenClaw 自动处理。

## 业务规则
1. **方法编码**：`api_method` 参数必须传入，否则无法执行脚本。例如：`pay.heepay.bank.apply`
2. **项目生成**：代码生成器会自动创建完整的 Maven 项目，包含 pom.xml、SDK 依赖、配置类等。生成前会询问用户输出路径
3. **代码规范**：生成的代码必须与 reference/hyw-demo 项目中的示例代码结构、命名、注解保持一致

## 依赖项

- Python 3.7+
- requests（脚本调用的 API）

**注意：** 如果通过 OpenClaw 使用，无需手动安装依赖，由 OpenClaw 自动处理。

---

## 开放平台部分接口方法说明
- 以下的API方法是开放平台提供的接口方法， 也就是脚本调用时候需要传入的方法编码。
- 用户可能会输入API方法名称或者API方法描述来触发脚本调用。
- 如果没有匹配到用户需要生成的方法， 可以让用户手动输入API方法编码。
---

|API方法名称| API方法编码                                      |API描述|
|---|----------------------------------------------|---|
|文件上传| customer.file.upload                         |商户入网、资料审核等场景的附件上传接口|
|企业入网申请| customer.enter.enterprise.apply              |企业资质商户提交入网开通申请|
|个体入网申请| customer.enter.individual.apply              |个体工商户资质商户提交入网开通申请|
|小微入网申请| customer.enter.micro.apply                   |小微企业/个人小微商户提交入网开通申请|
|商户信息变更| customer.enter.modify.apply                  |已入网商户修改基础信息、资质资料申请|
|汇元业务开通| customer.business.open                       |商户申请开通汇付宝旗下各类支付业务权限|
|通道业务开通| customer.channel.open                        |商户申请开通指定支付通道的交易权限|
|商户入网结果查询| customer.info.enter.query                    |查询商户入网申请的审核状态与结果|
|商户信息查询| customer.info.query                          |查询已入网商户的基础信息、资质与业务开通状态|
|商户通道风险查询| com.heepay.risk.mchlist.query                |查询商户对应支付通道的风险管控状态|
|数据字典查询| customer.dictionary.query                    |查询平台通用枚举值、参数字典信息|
|交易限制子商户查询| com.account.merchant.sub.limit.trade.list    |查询已被限制交易权限的子商户明细清单|
|商户入网通知| customer.notify.enter.notify                 |平台异步推送商户入网审核结果通知|
|商户资料检查通知| fund.trade.merchant.info.check.notify        |平台异步推送商户资料完整性核查结果通知|
|短信发送| extend.trade.sms.send.submit                 |发送身份验证、业务通知类短信|
|短信发送查询| extend.trade.sms.send.query                  |查询短信发送状态、送达结果|
|身份鉴权| extend.trade.auth.id.card.certify            |个人/商户法人身份证实名核验|
|身份鉴权查询| extend.trade.auth.id.card.certify.query      |查询身份证实名核验的结果状态|
|发票授信额度查询| extend.trade.invoice.credit.limit.query      |查询商户电子发票开具的授信额度|
|发票查询| extend.trade.invoice.digital.query           |查询已开具电子发票的明细与状态|
|发票开具| extend.trade.invoice.digital.submit          |提交电子发票开具申请|
|发票下载| extend.trade.invoice.file.url.get            |获取已开具电子发票的下载链接|
|获取人脸核验二维码| extend.trade.invoice.face.auth.qr.code.get   |生成发票业务人脸核验二维码|
|人脸核验结果查询| extend.trade.invoice.face.auth.result.query  |查询发票业务人脸核验的结果|
|开票监控| extend.trade.invoice.monitor                 |监控发票开具进度与异常状态|
|发票红冲| extend.trade.invoice.red.submit              |提交已开发票红冲作废申请|
|红冲查询| extend.trade.invoice.red.query               |查询发票红冲操作的处理结果|
|发票短信验证| extend.trade.invoice.sms.verify              |发票业务短信验证码核验|
|发票用户登录| extend.trade.invoice.user.login              |发票管理系统用户登录接口|
|发票用户登记| extend.trade.invoice.user.register.submit    |发票管理系统用户注册登记|
|投诉列表查询| com.heepay.complaint.recordlist.query        |查询商户交易投诉的列表数据|
|投诉留言提交| com.heepay.complaint.submit.message          |商户针对投诉提交回复留言|
|投诉明细查询| com.heepay.complaint.detaillist.query        |查询单条投诉的详细信息与处理记录|
|投诉图片上传| com.heepay.complaint.upload.image            |上传投诉处理相关的凭证图片|
|投诉处理完成| com.heepay.complaint.complete                |标记投诉工单为处理完成状态|
|网银支付申请| pay.heepay.bank.apply                        |发起网银跳转支付的订单申请|
|支付结果通知| pay.heepay.trade.status.notify               |平台异步推送支付订单最终状态通知|
|退款结果通知| fund.heepay.refund.status.notify             |平台异步推送退款订单处理结果通知|
|华为直连支付| pay.heepay.direct.huaweipay.apply            |发起华为钱包直连支付申请|
|骏卡直接支付| pay.heepay.junka.submit                      |使用骏卡直接完成订单支付|
|骏卡批量支付| pay.heepay.junka.batch.submit                |批量发起骏卡支付订单|
|骏卡收银台支付| pay.heepay.junka.apply                       |跳转骏卡收银台完成支付|
|骏卡用户注册| com.account.personal.merch.api.user.register |注册骏卡支付专属用户账号|
|余额支付申请| pay.heepay.balpay.apply                      |发起商户/用户余额支付订单申请|
|余额确认支付| pay.heepay.balpay.confirm                    |验证短信后确认余额支付|
|余额支付短验重发| pay.heepay.balpay.sms.resend                 |重新发送余额支付验证码短信|
|余额直接支付| pay.heepay.balpay.submit                     |无需验证码直接发起余额支付|
|订单关闭| pay.heepay.order.close                       |主动关闭未支付的交易订单|
|银联聚分期申请| pay.heepay.qrcode.installment.apply          |发起银联聚分期二维码分期支付申请|
|聚合码支付申请| pay.heepay.qrcode.apply                      |云闪付、微信、支付宝一码付支付申请|
|客户端用户标识获取| pay.heepay.qrcode.authcode.openid.page       |前端获取支付用户唯一标识|
|商家主扫支付| pay.heepay.qrcode.submit                     |商家扫描用户付款码完成收款|
|付款码用户标识获取| pay.heepay.qrcode.authcode.openid.query      |解析付款码获取用户支付标识|
|易收款支付申请| pay.heepay.easy.apply                        |发起银行转账大额易收款支付申请|
|易收款挂起通知| pay.heepay.acs.verifyfail.notify             |易收款汇款单核验异常挂起推送|
|快捷支付签约| pay.heepay.quick.sign.apply                  |银行卡快捷支付签约绑定申请|
|快捷签约查询| pay.heepay.quick.sign.query                  |查询银行卡快捷签约状态|
|快捷解约申请| pay.heepay.quick.sign.close                  |解除银行卡快捷支付签约关系|
|快捷支付申请| pay.heepay.quick.apply                       |发起快捷支付订单申请|
|快捷确认支付| pay.heepay.quick.confirm                     |验证短信后确认快捷支付|
|快捷短验重发| pay.heepay.quick.sms.resend                  |重新发送快捷支付验证码|
|快捷直接支付| pay.heepay.quick.submit                      |协议快捷支付，无需验证码直接扣款|
|快捷签约通知| pay.heepay.quick.sign.status.notify          |异步推送快捷签约结果通知|
|余额转账| fund.heepay.transit.balance.apply            |商户账户余额内部转账申请|
|转账代付查询| fund.heepay.transit.query                    |查询转账、代付订单的处理状态|
|转账代付对账| fund.heepay.transit.check                    |转账代付订单对账文件获取与核对|
|商户提现申请| fund.trade.merchant.fetch.cash.submit        |商户账户余额提现到银行卡申请|
|银行卡对应卡bin查询| com.heepay.bank.card.bin.query               |查询银行卡归属行、卡种等信息|
|付款协议文件上传| fund.heepay.transit.contract.file.upload     |上传代付、转账业务协议附件|
|代付申请| fund.heepay.transit.bank.apply               |商户发起批量/单笔代付到银行卡|
|代付状态通知| fund.heepay.transit.status.notify            |异步推送代付订单处理结果通知|
|商户余额查询| fund.trade.merchant.balance.query            |查询商户可用账户余额|
|商户在途余额查询| fund.heepay.settle.unsettle.query            |查询商户未结算、在途资金余额|
|余额变动通知| fund.trade.merchant.balance.history.notify   |异步推送商户余额变动通知|
|骏卡购买| mall.800j.junka.buy.submit                   |提交骏卡购买订单申请|
|购卡单查询| mall.800j.junka.buy.query                    |查询骏卡购买订单状态与卡密信息|
|商城订单支付| mall.order.pay.apply                         |商城商品订单支付申请|
|订单支付查询| mall.order.pay.query                         |订单支付查询|

**参考文档：**
- 汇元开放平台接口文档：https://open.heepay.com/www/index.html#/document/detail?type=20&docType=1&id=51001310013001
