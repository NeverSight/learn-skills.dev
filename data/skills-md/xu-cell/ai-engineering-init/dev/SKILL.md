---
name: dev
description: |
  当需要从零开始开发新功能、完整开发流程时自动使用此 Skill。

  触发场景：
  - 需要从零开始开发一个新功能
  - 需要设计数据库表并生成代码
  - 需要完整的开发流程引导
  - 需要配置代码生成器并生成后端代码

  触发词：开发功能、dev、新功能、功能开发、从零开发、完整开发、开发新模块
---

# /dev - 开发新功能（RuoYi-Vue-Plus 纯后端版）

智能代码生成器配置助手，专为 RuoYi-Vue-Plus 三层架构（Controller→Service→Mapper）设计。

## 🎯 核心优势
- ✅ **纯后端专注**：无前端，专注后端 CRUD 代码生成
- ✅ **包名适配**：`org.dromara.*`
- ✅ **智能推断**：模块 → 表前缀 → 包名 → 图标自动识别
- ✅ **全自动配置**：代码生成器配置完整（gen_table + gen_table_column）
- ✅ **菜单权限**：自动生成完整的菜单和权限配置

## 🚀 执行流程

### 第一步：需求确认

```
请告诉我要开发的功能：

1. **功能名称**？（如：广告管理、反馈管理）
2. **所属模块**？（system/business/其他）
```

**自动推断**：

| 模块 | 表前缀 | 包名 | 上级菜单 |
|------|--------|------|---------|
| system | `sys_` | `org.dromara.system` | 系统管理 |
| business | `b_` | `org.dromara.business` | 业务管理 |
| 其他（如 demo） | `demo_` | `org.dromara.demo` | [模块]管理 |

---

### 第二步：功能重复检查（强制执行）⭐⭐⭐⭐⭐

**⚠️ 重要**：检查功能是否已存在，避免重复开发

```bash
# 1. 检查后端代码
Grep pattern: "[功能名]Service" path: ruoyi-modules/ output_mode: files_with_matches
Grep pattern: "[功能名]Controller" path: ruoyi-modules/ output_mode: files_with_matches

# 2. 检查数据库表
SHOW TABLES LIKE '[表前缀]%';

# 3. 检查菜单
SELECT menu_name FROM sys_menu WHERE menu_name LIKE '%[功能名]%';
```

---

### 第三步：数据库现状分析（自动执行）

从 `ruoyi-admin/src/main/resources/application-dev.yml` 动态读取数据库配置。

---

### 第四步：智能表结构设计

#### 智能字段命名和推断

| 字段后缀 | 推断结果 | 控件类型 | 查询方式 |
|---------|---------|---------|---------|
| `xxx_name` | 名称 | input | LIKE |
| `xxx_title` | 标题 | input | LIKE |
| `xxx_content` | 内容 | editor | 富文本 |
| `status` | 状态 | select | EQ + sys_normal_disable |
| `xxx_type` | 分类 | select | EQ + 自定义字典 |
| `is_xxx` | 是否 | radio | EQ + sys_boolean_flag |
| `xxx_amount` / `xxx_price` | 金额 | numberInput | EQ |
| `xxx_time` / `xxx_date` | 时间 | datetime | BETWEEN |

#### 标准表结构模板

```sql
CREATE TABLE [表前缀]_[功能名] (
    id              BIGINT(20)   NOT NULL COMMENT '主键ID',
    tenant_id       VARCHAR(20)  DEFAULT '000000' COMMENT '租户ID',

    -- 业务字段
    xxx_name        VARCHAR(100) NOT NULL COMMENT '名称',
    xxx_type        CHAR(1)      DEFAULT '1' COMMENT '类型',
    status          CHAR(1)      DEFAULT '1' COMMENT '状态(0停用 1正常)',

    -- 审计字段
    create_by       BIGINT(20)   DEFAULT NULL COMMENT '创建人',
    create_time     DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by       BIGINT(20)   DEFAULT NULL COMMENT '更新人',
    update_time     DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    remark          VARCHAR(500) DEFAULT NULL COMMENT '备注',
    del_flag        CHAR(1)      DEFAULT '0' COMMENT '删除标志',

    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx表';
```

---

### 第五步：生成方案并确认（仅此一次确认）

```markdown
## 📋 代码生成方案

### 基本配置
- **功能名称**：广告管理
- **模块**：business
- **表名**：b_ad
- **Java类名**：Ad
- **包名**：org.dromara.business
- **接口路径**：/business/ad

### 菜单配置
- **上级菜单**：业务管理 (menu_id: 1001)
- **菜单顺序**：20
- **菜单图标**：ad (自动匹配)

**确认开始生成？**
```

---

### 第六步：自动执行生成（无需确认）

用户确认后，AI 自动执行：
1. 建表 SQL
2. 创建字典（如需要）
3. 生成代码生成器配置 SQL

---

### 第七步：完成报告

```markdown
## 🎉 代码生成方案配置完成！

### 已完成
- ✅ 数据库表创建：b_ad
- ✅ 业务字典创建：b_ad_type（3 个字典项）
- ✅ 菜单配置：广告管理（自动导入启用）
- ✅ 代码生成配置：表 + 11 个字段

## 🚀 下一步：前往代码生成器生成代码

1. **登录系统后台**：http://localhost:8080
2. **导航**：系统工具 → 代码生成
3. **查找表**：找到 `b_ad` 表
4. **生成代码**：点击【生成代码】按钮
5. **重启服务**：代码生成后需重启后端服务

### 生成后的文件结构

\`\`\`
ruoyi-system/
├── controller/business/AdController.java
├── domain/Ad.java
├── domain/bo/AdBo.java
├── domain/vo/AdVo.java
├── mapper/AdMapper.java
├── service/IAdService.java
└── service/impl/AdServiceImpl.java
\`\`\`
```

---

## ⚠️ AI 执行规则

1. ✅ **仅后端**：三层架构（Controller→Service→Mapper）
2. ✅ **包名**：必须是 `org.dromara.*`
3. ✅ **一次确认**：第五步确认后全自动执行
4. ✅ **tenant_id**：框架自动处理，所有权限配置为 0
5. ✅ **检查功能重复**：禁止重复开发相同功能
6. ✅ **智能字段推断**：根据字段名后缀自动推断控件和查询方式
7. ✅ **字典智能处理**：检查字典存在性，不存在则创建
