---
name: leniu-data-permission
description: |
  leniu-tengyun-core 项目多租户数据权限控制规范。基于物理数据库隔离的双库架构，包含数据源切换、租户上下文、跨租户操作。

  触发场景：
  - 使用 @UseSystem 切换系统库操作
  - 使用 Executors.doInTenant/readInTenant 跨租户查询
  - 使用 TenantContextHolder 获取租户上下文
  - 配置双库数据源路由
  - 跨租户数据初始化

  触发词：多租户、数据权限、@UseSystem、Executors.doInTenant、readInSystem、TenantContextHolder、MERCHANT-ID、双库隔离、数据源切换
---

# leniu-data-permission

适用于 leniu-tengyun-core 项目的多租户数据权限控制。

## 双库架构

leniu-tengyun-core 采用物理数据库隔离的多租户架构，每个租户拥有独立的业务数据库：

```
系统库 (system)
├── 租户配置表
├── 系统字典表
└── ... 系统级配置

租户库 (tenant_1, tenant_2, ...)
├── 租户业务数据
└── ... 业务表（无 tenant_id 字段）
```

## 数据源切换

### 注解方式

| 注解 | 用途 |
|------|------|
| `@UseSystem` | 切换到系统库 |
| `@UseGlobalTs("dbName")` | 切换到全局时序库 |

```java
import net.xnzn.framework.data.mybatis.datasource.UseSystem;
import net.xnzn.framework.data.mybatis.datasource.UseGlobalTs;

@Service
public class TenantConfigService {

    // 操作系统库
    @UseSystem
    public TenantConfig getTenantConfig(Long tenantId) {
        return tenantConfigMapper.selectById(tenantId);
    }

    // 操作全局时序库
    @UseGlobalTs("ts_db_name")
    public List<TimeSeriesData> getTimeSeries(String key) {
        return timeSeriesMapper.selectList(...);
    }
}
```

### 编程方式

```java
import net.xnzn.framework.data.dataset.Executors;

// 在指定租户库中执行操作
Executors.doInTenant(tenantId, status -> {
    // 这里的操作会在 tenantId 对应的数据库中执行
    businessDataMapper.insert(data);
});

// 读取指定租户数据（不开启事务）
List<Data> data = Executors.readInTenant(tenantId, () -> {
    return businessDataMapper.selectList(...);
});

// 遍历所有租户执行任务
Executors.doInAllTenant(tenantId -> {
    // 对每个租户执行此操作
    businessDataMapper.delete(...);
});

// 遍历所有租户执行任务（出错继续）
Executors.doInAllTenant(true, tenantId -> {
    // 某个租户出错不影响其他租户
    businessDataMapper.update(...);
});

// 在系统库中执行操作
Executors.doInSystem(status -> {
    // 这里的操作会在系统库中执行
    systemConfigMapper.insert(config);
});

// 读取系统库数据
SystemConfig config = Executors.readInSystem(() -> {
    return systemConfigMapper.selectById(1);
});

// 在全局时序库中执行
Executors.doInGlobalTs("ts_db_name", false, () -> {
    timeSeriesMapper.insert(data);
});
```

## 租户上下文

### TenantContextHolder

```java
import net.xnzn.framework.data.tenant.TenantContextHolder;

// 获取当前租户 ID（来自请求头）
Long tenantId = TenantContextHolder.getTenantId();

// 设置租户 ID（一般由 Filter 自动设置）
TenantContextHolder.setTenantId(123L);

// 清除租户上下文
TenantContextHolder.clear();
```

### 租户请求头

默认租户 ID 请求头名称为 `MERCHANT-ID`（可配置）：

```http
GET /api/v2/users HTTP/1.1
MERCHANT-ID: 12345
```

## 数据源路由

### RoutingRule

```java
import net.xnzn.framework.data.dataset.rule.RoutingRule;

// 获取当前路由上下文
RoutingRule.Context context = RoutingRule.getContext();

// 重置路由规则
RoutingRule.reset();

// 使用系统库
RoutingRule.useSystem();

// 使用全局时序库
RoutingRule.useGlobalTs("ts_db_name");
```

### 路由规则加载

数据源规则从配置文件加载：

```yaml
spring:
  dataset:
    system:
      master:
        jdbc-url: jdbc:mysql://localhost:3306/system_db
        username: root
        password: xxx
      slave:
        - jdbc-url: jdbc:mysql://slave1:3306/system_db
        - jdbc-url: jdbc:mysql://slave2:3306/system_db
    global-ts:
      master:
        jdbc-url: jdbc:mysql://localhost:3306/ts_db
    business:
      tenant_1:
        master:
          jdbc-url: jdbc:mysql://localhost:3306/tenant_1
        slave:
          - jdbc-url: jdbc:mysql://slave1:3306/tenant_1
      tenant_2:
        master:
          jdbc-url: jdbc:mysql://localhost:3306/tenant_2
```

## 典型场景

### 跨租户查询

```java
@Service
public class CrossTenantService {

    // 查询多个租户的数据
    public Map<Long, List<Order>> getOrdersByTenants(List<Long> tenantIds) {
        Map<Long, List<Order>> result = new HashMap<>();
        for (Long tenantId : tenantIds) {
            List<Order> orders = Executors.readInTenant(tenantId, () ->
                orderMapper.selectList(new QueryWrapper<>())
            );
            result.put(tenantId, orders);
        }
        return result;
    }
}
```

### 系统配置读取

```java
@Service
public class SystemConfigService {

    @UseSystem
    public SystemConfig getConfig(String key) {
        return systemConfigMapper.selectOne(
            new QueryWrapper<SystemConfig>().eq("config_key", key)
        );
    }
}
```

### 租户数据初始化

```java
@Service
public class TenantInitService {

    // 为新租户初始化数据
    public void initTenant(Long tenantId) {
        Executors.doInTenant(tenantId, status -> {
            // 创建默认菜单
            defaultMenuService.createDefaultMenus();
            // 创建默认角色
            defaultRoleService.createDefaultRoles();
        });
    }
}
```

## TenantConfigProperties

```java
@Setter
@Getter
@ConfigurationProperties(prefix = "leniu.tenant")
public class TenantConfigProperties {
    // 请求头名称，默认 MERCHANT-ID
    private String carrierName = "MERCHANT-ID";

    // MDC 键名
    private String mdc = "tenantId";
}
```

## 与 RuoYi-Plus 的区别

| 特性 | RuoYi-Plus | leniu-tengyun-core |
|------|-----------|-------------------|
| 多租户方式 | 逻辑隔离（tenant_id 字段） | 物理隔离（独立数据库） |
| 租户切换 | `@TenantLine` 注解 | `@UseSystem` / `Executors.doInTenant()` |
| 租户上下文 | `TenantLineHelper.tenantId()` | `TenantContextHolder.getTenantId()` |
| 数据权限 | `@DataColumn` 注解 | 物理库隔离，无需字段 |
| 系统库操作 | `@TenantLine` 指定 "000000" | `@UseSystem` 或 `Executors.doInSystem()` |

## 注意事项

1. leniu 采用物理库隔离，表中无 `tenant_id` 字段
2. 默认操作租户库，需要访问系统库时必须明确切换
3. 跨租户操作需要使用 `Executors.doInTenant()` 或 `Executors.readInTenant()`
4. 事务会在方法执行结束后自动切回原来的数据源
5. `TenantContextHolderFilter` 自动从请求头解析租户 ID

---

## 报表场景下的数据权限使用

### 报表场景数据权限使用模式

在定制报表（leniu-yunshitang 仓库）中，数据权限通过以下三层协作实现：

**1. Service 层：获取权限参数**

```java
@Autowired
private MgrAuthV2Api mgrAuthApi;

@Autowired
private ReportDataPermissionService reportDataPermissionService;

// 在每个查询/导出方法中调用
MgrUserAuthPO authPO = mgrAuthApi.getUserAuthPO();
ReportDataPermissionParam dataPermission = reportDataPermissionService.getDataPermission(authPO);
```

**2. Mapper 接口：传递权限参数**

```java
List<XxxVO> listPage(@Param("param") XxxParam param,
                     @Param("authPO") MgrUserAuthPO authPO,
                     @Param("dataPermission") ReportDataPermissionParam dataPermission);

XxxVO getTotal(@Param("param") XxxParam param,
               @Param("authPO") MgrUserAuthPO authPO,
               @Param("dataPermission") ReportDataPermissionParam dataPermission);
```

**3. MyBatis XML：引入公共权限片段**

```xml
<!-- 在 baseWhere 的 SQL 片段末尾加入 -->
<sql id="baseWhere">
    <!-- 业务过滤条件... -->
    <include refid="net.xnzn.core.report.statistics.common.mapper.ReportDataPermissionMapper.dataPermission"/>
</sql>
```

**完整调用链示例：**

```java
public ReportBaseTotalVO<DzMealDetailVO> pageWithTotal(DzMealDetailParam param) {
    // 获取权限
    MgrUserAuthPO authPO = mgrAuthApi.getUserAuthPO();
    ReportDataPermissionParam dataPermission = reportDataPermissionService.getDataPermission(authPO);

    ReportBaseTotalVO<DzMealDetailVO> result = new ReportBaseTotalVO<>();
    // 查询合计行
    if (CollUtil.isEmpty(param.getExportCols())) {
        DzMealDetailVO totalLine = mapper.getTotal(param, authPO, dataPermission);
        result.setTotalLine(Optional.ofNullable(totalLine).orElse(new DzMealDetailVO()));
    }
    // 查询列表
    if (param.getPage() != null) {
        PageMethod.startPage(param.getPage());
    }
    List<DzMealDetailVO> list = mapper.listPage(param, authPO, dataPermission);
    result.setResultPage(PageVO.of(list));
    return result;
}
```

**注意：** 导出方法（exportXxx）中同样需要获取权限并传给 Mapper，不能省略。
