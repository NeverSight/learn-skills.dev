---
name: chinese-copyright-application
description: 用于生成中国软件著作权申请材料的完整工具包。支持从项目代码、文档等自动提取信息，生成软件著作权登记申请表、源代码文档（前后各30页）、用户手册和设计说明书，并自动转换为PDF文件。适用于微信小程序、Web应用、移动App、桌面应用等各类软件项目。当用户需要申请中国软件著作权时使用此skill。
---

# 中国软件著作权申请材料生成

## 快速开始

1. 询问著作权人的名称
2. 分析项目结构和配置文件
3. 提取项目基本信息（名称、版本、描述等）
4. 生成申请材料：
   - 软件著作权登记申请表
   - 源代码文档（前后各30页）
   - 用户手册
   - 设计说明书
5. 生成PDF文件

## 工作流程

### 1. 著作权人信息收集

- 询问用户著作权人的名称
- 确保在每一个生成的文档开头都包含著作权人名称

### 2. 项目信息收集

从以下位置收集项目信息：

**微信小程序项目：**
- `app.json` - 获取软件名称（navigationBarTitleText）
- `project.config.json` - 获取appid、libVersion
- `package.json` - 获取版本号、描述、作者
- `README.md` - 获取详细描述、功能特性

**Web/Node.js项目：**
- `package.json` - 获取名称、版本、描述、作者
- `README.md` - 获取详细描述、功能特性

**其他项目：**
- 查找配置文件（如 `pom.xml`, `build.gradle`, `Cargo.toml` 等）
- 查找 README 文档

### 3. 生成申请表

使用 [application-form-template.md](references/application-form-template.md) 模板生成申请表。

**格式要求：**
- 软件全称：应当有辨识度，应该叫"xxx软件"
- 版本号：保留两位，例如"1.0"、"1.1"等

**必填字段：**
- 软件全称
- 软件简称
- 版本号
- 开发完成日期
- 首次发表日期
- 著作权人
- 开发者
- 软件性质（原创/修改/衍生）
- 软件分类
- 代码行数
- 开发的硬件环境
- 运行的硬件环境
- 开发该软件的操作系统
- 软件开发环境/开发工具
- 该软件的运行平台/操作系统
- 软件运行支撑环境/支持软件
- 编程语言
- 源程序量
- 开发目的
- 面向领域/行业
- 软件的主要功能
- 软件的技术特点

### 4. 生成源代码文档

**要求：**
- 前后各30页，每页50行
- 总共3000行源代码
- 如果代码不足3000行，全部提供

**提取策略：**
1. 优先提取核心业务逻辑代码
2. 按文件重要性排序（主要文件在前）
3. 每个文件添加文件头注释（文件名、路径、行数）
4. 格式化为标准页格式（每页50行，添加页码）

**代码文件优先级：**
- 主要业务逻辑文件（如 `app.js`, `main.js`, `index.js`）
- 工具函数文件（`utils/`, `helpers/`）
- 页面/组件文件（`pages/`, `components/`）
- 配置文件（`config/`）

### 5. 生成用户手册

使用 [user-manual-template.md](references/user-manual-template.md) 模板。

**内容结构：**
1. 软件简介
2. 功能概述
3. 安装/使用说明
4. 主要功能说明
5. 操作步骤
6. 注意事项

**信息来源：**
- README.md 的功能特性部分
- 代码注释
- 界面截图（如果有）

### 6. 生成设计说明书

使用 [design-doc-template.md](references/design-doc-template.md) 模板。

**内容结构：**
1. 软件概述
2. 需求分析
3. 总体设计
4. 详细设计
5. 数据结构设计
6. 接口设计
7. 算法设计
8. 界面设计

**信息来源：**
- 项目结构分析
- 代码逻辑分析
- 数据流分析
- 组件/模块关系

## 输出格式

所有文档以 Markdown 格式生成，并自动转换为 PDF 文件。所有输出文件将放置在专门的文件夹中。

**输出文件夹：**
- `copyright-application-materials/`

**输出文件：**
- `copyright-application-materials/软件著作权登记申请表.md`
- `copyright-application-materials/软件著作权登记申请表.pdf`
- `copyright-application-materials/源代码文档.md`
- `copyright-application-materials/源代码文档.pdf`
- `copyright-application-materials/用户手册.md`
- `copyright-application-materials/用户手册.pdf`
- `copyright-application-materials/设计说明书.md`
- `copyright-application-materials/设计说明书.pdf`

## 特殊处理

### 微信小程序小程序

- 软件分类：移动应用软件-小程序
- 平台：微信小程序平台
- 技术特点：微信小程序原生框架

### Web应用

- 软件分类：应用软件-Web应用
- 平台：浏览器
- 技术特点：前端框架 + 后端技术

### 移动App

- 软件分类：移动应用软件-App
- 平台：iOS/Android
- 技术特点：原生/跨平台框架

## 参考文档

- [申请表模板](references/application-form-template.md)
- [用户手册模板](references/user-manual-template.md)
- [设计说明书模板](references/design-doc-template.md)
- [申请要求](references/requirements.md)
