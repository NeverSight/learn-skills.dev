---
name: java-code-review
description: Java代码审查工具，基于阿里Java开发手册检查代码规范。当用户说"审查代码"、"检查代码规范"、"代码review"、"代码检查"、"规范审查"、"review这段代码"、"检查这段代码是否符合阿里规范"、或提交了Java代码要求检查时触发。适用于PR review、代码提交前检查、或日常代码审查。
version: 1.0.0
---

# Java代码审查 - 阿里Java开发手册

## 审查范围

本skill基于阿里Java开发手册（泰山版）对Java代码进行全方位规范审查，覆盖：

**编程规约**：
- 命名风格、常量定义、代码格式、OOP规约
- 日期时间、集合处理、并发处理、控制语句
- 注释规约、异常处理、日志规约

**MySQL规约**：建表规范、SQL查询规范

**工程规约**：应用分层、二方库依赖

**安全规约**：密码加密、SQL注入防护、XSS防护等

## 审查流程

### 1. 确定审查范围
- 如果用户指定了具体文件/目录，审查该范围
- 如果用户未指定，寻找项目中的Java文件（优先`*.java`，排除`target/`、`build/`、`*.class`）

### 2. 加载规则
按需加载references目录下的规则文件：
- 编程规约：命名(01)、常量(02)、格式(03)、OOP(04)、日期(05)、集合(06)、并发(07)、控制(08)、注释(09)、异常(10)、日志(11)
- MySQL规约：12-mysql-orms.md
- 工程规约：13-engineering.md
- 安全规约：14-security.md

### 3. 执行审查
对每个Java文件执行规则检查，识别违规模式和具体位置。

### 4. 输出报告
生成结构化的违规报告。

## 审查输出格式

```
## Java代码审查报告

**审查时间**：YYYY-MM-DD
**审查范围**：<文件或目录路径>
**审查依据**：阿里Java开发手册（泰山版）

---

### 审查概要

| 指标 | 数值 |
|------|------|
| 审查文件数 | X |
| 违规规则数 | Y |
| 违规总数 | Z |
| 严重违规 | N |
| 警告级别 | M |
| 提示级别 | P |

---

### 违规详情

#### [严重/警告/提示] 规则ID 规则名称
**规则**：阿里Java开发手册要求的规则描述
**严重程度**：严重 / 警告 / 提示
**文件**：<文件名>:<行号>
**违规代码**：
```java
<违规代码片段>
```
**修复建议**：
```java
<符合规范的写法>
```

---

### 规则覆盖统计

| 规则类别 | 检查规则数 | 违规数 |
|----------|-----------|--------|
| 命名风格 (NC) | X | Y |
| 常量定义 (CT) | X | Y |
| 代码格式 (CF) | X | Y |
| OOP规约 (OP) | X | Y |
| 日期时间 (DT) | X | Y |
| 集合处理 (CL) | X | Y |
| 并发处理 (CC) | X | Y |
| 控制语句 (CS) | X | Y |
| 注释规约 (CM) | X | Y |
| 异常处理 (EH) | X | Y |
| 日志规约 (LG) | X | Y |
| MySQL建表 (MS) | X | Y |
| MySQL查询 (MQ) | X | Y |
| 工程规约 (EG) | X | Y |
| 安全规约 (SE) | X | Y |

---

## 规则ID编码规范

- **NC-XXX**: Naming Conventions（命名风格）
- **CT-XXX**: Constants（常量定义）
- **CF-XXX**: Code Format（代码格式）
- **OP-XXX**: OOP Rules（OOP规约）
- **DT-XXX**: Date Time（日期时间）
- **CL-XXX**: Collections（集合处理）
- **CC-XXX**: Concurrency（并发处理）
- **CS-XXX**: Control Statements（控制语句）
- **CM-XXX**: Comments（注释规约）
- **EH-XXX**: Exception Handling（异常处理）
- **LG-XXX**: Logging（日志规约）
- **MS-XXX**: MySQL ORM（MySQL建表）
- **MQ-XXX**: MySQL Query（MySQL查询）
- **EG-XXX**: Engineering（工程规约）
- **SE-XXX**: Security（安全规约）

## 严重程度定义

| 级别 | 说明 |
|------|------|
| **严重** | 影响系统正确性、安全性或性能的违规，必须修复 |
| **警告** | 影响可维护性或可能导致问题的代码，建议修复 |
| **提示** | 代码风格建议，可选修复 |

## 关键检查逻辑

### 命名风格检查
- 抽象类必须以`Abstract`/`Base`开头
- 枚举类必须以`Enum`结尾
- 常量必须全大写加下划线
- Boolean类型变量不应使用`is`/`has`/`can`/`will`前缀
- 接口类名不加I前缀

### 魔法值检查
- 禁止在代码中直接使用未定义常量（3字符以上字符串需定义常量）
- Long类型常量必须使用大写L后缀

### OOP规约检查
- 静态方法不可通过实例调用
- Object的equals使用Objects.equals()避免NPE
- POJO类属性使用BigDecimal而非float/double
- 多线程操作时数据必须使用ThreadLocal封闭

### 异常处理检查
- 不可捕获RuntimeException/Error
- finally块中不可使用return
- finally中必须释放资源，使用try-with-resources更佳
- 应用异常不可被吞掉

### MySQL规约检查
- 布尔字段不可使用`is_xxx`命名
- 字段必须设置为NOT NULL并提供默认值
- 价格字段使用DECIMAL而非DOUBLE
- 禁止使用`select *`
- 禁止使用物理外键
- `count(*)`不可用`count(列名)`替代
- 禁止使用truncate table

### 安全规约检查
- 密码必须加密存储
- 敏感数据不可打印到日志
- 必须使用SQL参数绑定防止注入
- 文件上传必须验证类型和大小
- 必须开启CSRF防护

### 日志规约检查
- 日志对象必须使用`private static final`定义
- 必须使用占位符`{}`而非字符串拼接
- 禁止使用System.out/System.err

## 规则文件索引

当需要详细规则时，读取对应的references文件：
- references/01-naming-conventions.md - 完整命名规则
- references/02-constants.md - 常量定义规则
- references/03-code-format.md - 格式规则
- references/04-oop-rules.md - OOP规则
- references/05-date-time.md - 日期时间规则
- references/06-collections.md - 集合规则
- references/07-concurrency.md - 并发规则
- references/08-control-statements.md - 控制语句规则
- references/09-comments.md - 注释规则
- references/10-exception-handling.md - 异常规则
- references/11-logging.md - 日志规则
- references/12-mysql-orms.md - MySQL建表和SQL规则
- references/13-engineering.md - 工程规约
- references/14-security.md - 安全规约

## 示例

**输入**："帮我审查一下src目录下的Java代码"
**处理**：读取src目录下所有.java文件，按规则审查，输出违规报告

**输入**："检查这段代码是否符合阿里Java开发手册规范" + [代码片段]
**处理**：对代码片段执行规则检查，输出违规报告

## 审查完成

共发现X处违规，其中Y处严重违规需要优先修复。建议按以下顺序处理：
1. 严重违规（影响系统正确性、安全性）
2. 警告级别（影响可维护性）
3. 提示级别（代码风格建议）
