---
name: kuaipu-skill
description: 自动化快普系统登录、验证码识别、自动操作和审批流程查询等。
version: 0.2
author: 崔海亮
license: MIT
tags:
  - automation
  - login
  - approval
  - selenium
  - captcha
---
# 快普系统自动登录技能

该技能使用浏览器自动化和验证码识别技术，实现快普系统的自动登录和审批流程查询。

## 功能特性

- 自动读取配置文件中的登录信息
- 使用 Selenium 进行浏览器自动化操作
- 集成 ddddocr 进行验证码识别
- 完整的登录流程自动化
- 从主页提取业务催办列表
- 自动识别审批项目的当前审批人
- 空列表处理，显示"我的所有申请全部通过了"
- 保存操作过程的截图和HTML到项目目录

## 安装

### 自动从 SKILLS.sh 安装

```bash
npx skills add chldong/kuaipu-skill
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/chldong/kuaipu-skill.git
cd kuaipu-skill

# 安装依赖
uv pip install selenium==4.41.0 webdriver-manager==4.0.2 ddddocr==1.5.2

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写快普系统登录信息
```

## 使用方法

```bash
# 运行快普登录技能
kuaipu-skill login

# 查看登录状态
kuaipu-skill status

# 退出登录
kuaipu-skill logout

# 查看待审批流程
kuaipu-skill shenpi
```

## 配置说明

技能会自动读取 `.env` 文件中的以下配置：

- `kuaipu_url`: 快普系统登录地址
- `kuaipu_user`: 登录用户名
- `kuaipu_pass`: 登录密码

## 工作流程

### 登录流程

1. 读取配置文件中的登录信息
2. 打开快普系统登录页面
3. 自动填写用户名和密码
4. 识别并填写验证码
5. 提交登录表单
6. 验证登录是否成功
7. 保存登录状态（cookie）
8. 访问系统主页面

### 审批流程查询

1. 检查登录状态，如未登录则自动执行登录
2. 访问系统主页面
3. 查找主页上的"业务催办"方框
4. 提取业务催办列表的主题、时间和当前审批人
5. 显示催办列表信息
6. 如果催办列表为空，显示"我的所有申请全部通过了"

## 故障排除

- 确保 `.env` 文件配置正确
- 确保网络连接正常
- 确保 Chrome 浏览器已正确安装
- 如遇到验证码识别失败，可尝试多次运行
- **重要**：必须使用 ddddocr==1.5.2 版本，新版本存在导入冲突问题

## 项目结构

```
kuaipu-skill/
├── SKILL.md             # 技能配置文件
├── kuaipu-skill.sh      # Bash 执行脚本
├── kuaipu_skill.py      # Python 核心脚本
├── README.md            # 项目说明
└── .env.example         # 环境变量示例
```

## 版本变更

### v0.2 (2026-03-09)

- 新增业务催办列表提取功能
- 新增审批人识别功能
- 新增空列表处理
- 优化信息提取和格式化

### v0.1 (2026-02-11)

- 初始版本
- 实现自动登录功能
- 实现验证码识别
- 实现登录状态管理
