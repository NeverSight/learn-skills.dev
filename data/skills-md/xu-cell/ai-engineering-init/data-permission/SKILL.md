---
name: data-permission
description: |
  通用行级数据权限设计指南。通过 AOP + MyBatis 拦截器模式实现数据隔离，支持部门权限、本人权限、自定义权限等多种隔离粒度。
  触发场景：
  - 为业务模块添加行级数据过滤
  - 设计部门级 / 本人级数据隔离
  - 扩展自定义数据权限类型
  - 临时忽略数据权限查全量数据
  - 排查数据权限不生效问题
  触发词：数据权限、行级权限、数据隔离、部门权限、本人权限、自定义权限、DataScope、DataPermission、数据过滤
  注意：如果项目有专属技能（如 `leniu-data-permission`），优先使用专属版本。
---

# 行级数据权限开发指南

> 通用模板。如果项目有专属技能（如 `leniu-data-permission`），优先使用。

## 设计原则

1. **对业务透明**：数据权限通过拦截器自动注入 SQL 条件，业务代码无需感知。
2. **声明式配置**：通过注解声明字段映射关系，框架自动拼接过滤条件。
3. **可扩展**：权限类型（部门、本人、自定义等）可通过枚举或策略模式扩展。
4. **安全兜底**：未配置权限范围时默认为"仅本人"，避免数据泄露。

---

## 权限类型设计

| 类型 | 标识 | SQL 效果 | 适用场景 |
|------|------|---------|---------|
| 全部数据 | 1 | 不拼接条件 | 超管、全局数据查看 |
| 自定义权限 | 2 | `dept_id IN (角色关联的部门ID)` | 跨部门协作 |
| 本部门 | 3 | `dept_id = ?` | 部门经理 |
| 本部门及以下 | 4 | `dept_id IN (当前部门及子部门)` | 上级部门 |
| 仅本人 | 5 | `created_by = ?` | 普通员工 |
| 部门及以下或本人 | 6 | `dept_id IN (...) OR created_by = ?` | 混合场景 |

---

## 实现模式

### 架构概览

```
Controller -> Service (加注解) -> Mapper -> MyBatis 拦截器
                                              |
                                    自动注入 WHERE 条件
                                              |
                                   [你的权限处理器] (查询当前用户权限范围)
```

### 步骤 1：定义注解

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface DataPermission {
    DataColumn[] value();
    String joinStr() default "AND";  // 多角色权限连接方式
}

@Target(ElementType.ANNOTATION_TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface DataColumn {
    String key() default "deptName";   // 占位符关键字
    String value() default "dept_id";  // 对应的表字段名
    String permission() default "";     // 拥有此权限则不过滤
}
```

### 步骤 2：实现 MyBatis 拦截器

```java
@Intercepts({@Signature(type = Executor.class, method = "query", args = {...})})
public class DataPermissionInterceptor implements Interceptor {

    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        // 1. 从线程上下文获取 @DataPermission 注解
        // 2. 获取当前用户的角色及数据权限范围
        // 3. 根据权限类型拼接 WHERE 条件
        // 4. 修改原始 SQL，追加过滤条件
        return invocation.proceed();
    }
}
```

### 步骤 3：在 Service / Mapper 上使用

```java
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private OrderMapper orderMapper;

    // 按部门 + 创建人过滤
    @DataPermission({
        @DataColumn(key = "deptName", value = "dept_id"),
        @DataColumn(key = "userName", value = "created_by")
    })
    @Override
    public List<OrderVo> listWithPermission(OrderQuery query) {
        return orderMapper.selectList(buildWrapper(query));
    }
}
```

### 步骤 4：确保数据库表有权限字段

```sql
CREATE TABLE biz_order (
    id           BIGINT       NOT NULL COMMENT '主键',
    -- 业务字段 ...
    dept_id      BIGINT       DEFAULT NULL COMMENT '所属部门',   -- 必须
    created_by   BIGINT       DEFAULT NULL COMMENT '创建人',     -- 必须
    created_time DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```

### 多表关联（使用表别名）

```java
// SQL: SELECT o.*, u.user_name FROM biz_order o LEFT JOIN sys_user u ON ...
@DataPermission({
    @DataColumn(key = "deptName", value = "o.dept_id"),
    @DataColumn(key = "userName", value = "o.created_by")
})
List<OrderVo> selectWithJoin(@Param("query") OrderQuery query);
```

### 临时忽略数据权限

```java
// 使用工具类忽略权限过滤，查全量数据
Long total = [你的权限工具类].ignore(() -> orderService.count());

// 无返回值
[你的权限工具类].ignore(() -> {
    configService.refreshAll();
    return null;
});
```

### 指定权限标识跳过过滤

```java
// 拥有 order:all 权限的角色不过滤
@DataPermission({
    @DataColumn(key = "deptName", value = "dept_id", permission = "order:all")
})
```

---

## 选型建议

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| MyBatis 拦截器 | 对业务透明、自动注入 | 依赖 MyBatis | 绝大多数 Java Web 项目 |
| AOP + SQL 改写 | 框架无关 | 需自行解析 SQL | 非 MyBatis 项目 |
| 数据库视图 | 完全透明 | 难以动态切换 | 权限固定的场景 |
| 应用层过滤 | 实现简单 | 性能差（全量查出再过滤） | 数据量小 |

### 多角色权限计算

- **SELECT 查询**：多角色权限用 `OR` 连接（并集，看到更多数据）
- **UPDATE / DELETE**：多角色权限用 `AND` 连接（交集，更安全）

---

## 常见错误

```java
// 1. 注解放在 Controller 层（无效，拦截器在 Mapper 执行前生效）
@Controller
public class OrderController {
    @DataPermission({...})  // 无效！应在 Service 或 Mapper 上
    public Result<?> list() { }
}

// 2. 表别名不匹配
@DataColumn(key = "deptName", value = "user.dept_id")  // SQL 中别名是 u
// 应为 value = "u.dept_id"

// 3. 在权限服务内部调用带权限的方法（死循环）
public String getDeptAndChild(Long deptId) {
    deptService.list(wrapper);  // 如果 list 也带 @DataPermission -> 死循环
    // 应直接用 Mapper 或 ignore() 包装
}

// 4. 忘记在表中添加部门/创建人字段
// 没有 dept_id / created_by 字段，权限 SQL 会报错

// 5. 超级管理员测试数据权限
// 超管通常跳过权限过滤，应使用普通用户账号测试

// 6. @DataPermission 注解为空
@DataPermission  // 空注解，无 @DataColumn 映射，不会生效
```

### 问题排查

| 检查项 | 可能原因 | 解决方案 |
|--------|---------|---------|
| 超级管理员？ | 超管自动跳过权限 | 用普通用户测试 |
| 角色数据范围？ | 范围为"全部数据" | 修改角色数据权限配置 |
| 注解位置？ | 不在 Service / Mapper 层 | 移动注解到正确位置 |
| 表别名？ | value 别名与 SQL 不一致 | 检查并修正别名 |
| Unknown column？ | 表中没有该字段 | 检查数据库表结构 |

**调试**：开启 SQL 日志查看拼接结果

```yaml
# MyBatis SQL 日志
logging:
  level:
    [你的Mapper包路径]: debug
```
