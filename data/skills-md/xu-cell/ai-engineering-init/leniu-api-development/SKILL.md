---
name: leniu-api-development
description: |
  leniu-yunshitang-core 项目 API 接口开发规范。基于四层架构的 API 开发指南。

  触发场景：
  - 设计 leniu 项目 API 接口
  - 编写 leniu Controller 层代码
  - 配置接口权限和参数校验
  - 接口返回值类型选择
  - 多端路由规划（Web/Mobile/Android）

  适用项目：leniu-tengyun-core（云食堂项目）

  触发词：API接口、Controller、LeResult、LeResponse、LeRequest、接口开发、路由前缀、分页查询、接口权限
---

# leniu API 接口开发规范

## HTTP 方法与路径规范

| 操作 | HTTP 方法 | 路径示例 | 返回类型 |
|------|---------|---------|---------|
| 分页查询 | POST | `/query`, `/page-*` | `Page<VO>` / `PageVO<VO>` |
| 获取详情 | POST/GET | `/{id}`, `/get-*`, `/info` | VO |
| 新增 | POST | `/add` | `void` |
| 修改 | POST/PUT | `/update`, `/modify-*` | `void` |
| 删除 | DELETE/POST | `/delete`, `/batch/delete` | `void` |
| 列表（不分页） | POST | `/list-all`, `/type-list` | `List<VO>` |
| 导出 | POST | `/export`, `/export-async/*` | `void` |
| 导入 | POST | `/import-excel` | `void` |
| 树形查询 | POST | `/tree` | `List<Tree<Long>>` |

---

## Controller 标准模板

```java
@Api(tags = "模块-功能描述")
@RestController
@RequiresAuthentication
@RequestMapping("/api/v2/web/module")
public class XxxWebController {

    @Autowired
    private XxxBusiness xxxBusiness;

    @PostMapping("/add")
    @ApiOperation(value = "功能-新增")
    public void add(@Validated(InsertGroup.class) @RequestBody LeRequest<XxxDTO> request) {
        xxxBusiness.add(request.getContent());
    }

    @PostMapping("/update")
    @ApiOperation(value = "功能-修改")
    public void update(@Validated(UpdateGroup.class) @RequestBody LeRequest<XxxDTO> request) {
        xxxBusiness.update(request.getContent());
    }

    @PostMapping("/query")
    @ApiOperation(value = "功能-分页查询")
    public Page<XxxVO> query(@Validated @RequestBody LeRequest<XxxQueryParam> request) {
        return xxxBusiness.page(request.getContent());
    }

    @PostMapping("/delete")
    @ApiOperation(value = "功能-删除")
    public void delete(@RequestBody LeRequest<Long> request) {
        xxxBusiness.delete(request.getContent());
    }
}
```

---

## 请求/响应封装

### 请求：LeRequest<T>

所有接口入参统一用 `LeRequest<T>` 包装，通过 `request.getContent()` 获取实际参数。

```java
@PostMapping("/query")
public Page<XxxVO> query(@RequestBody LeRequest<XxxQueryParam> request) {
    return xxxService.page(request.getContent());
}
```

### 响应类型选择

| 场景 | 返回类型 | 示例 |
|------|---------|------|
| 分页 | `Page<VO>` / `PageVO<VO>` | `return xxxService.page(param);` |
| 单值包装 | `LeResponse<T>` | `return LeResponse.succ(value);` |
| 复杂对象 | 直接返回 VO | `return xxxService.getDetail(id);` |
| 报表+合计行 | `ReportBaseTotalVO<VO>` | `return service.pageSummary(param);` |
| 写操作 | `void` | 无返回值 |

```java
// LeResponse 用法
@PostMapping("/get-config")
public LeResponse<String> getConfig(@RequestBody LeRequest<Long> request) {
    return LeResponse.succ(xxxService.getConfig(request.getContent()));
}
```

---

## 参数校验

### 分组校验（新增/修改区分）

```java
// 分组接口定义
public interface InsertGroup {}
public interface UpdateGroup {}

// Controller 使用
@PostMapping("/add")
public void add(@Validated(InsertGroup.class) @RequestBody LeRequest<XxxDTO> request) {}

@PostMapping("/update")
public void update(@Validated(UpdateGroup.class) @RequestBody LeRequest<XxxDTO> request) {}
```

### DTO 校验示例

```java
// 必须用 jakarta.validation（JDK 21）
import jakarta.validation.constraints.*;

@Data
public class XxxDTO {
    @NotNull(message = "ID不能为空", groups = {UpdateGroup.class})
    private Long id;

    @NotBlank(message = "名称不能为空", groups = {InsertGroup.class, UpdateGroup.class})
    @Size(max = 100, message = "名称长度不能超过100个字符")
    private String name;
}
```

### 简单校验（无分组）

```java
@PostMapping("/query")
public Page<XxxVO> query(@Validated @RequestBody LeRequest<XxxQueryParam> request) {}

@PostMapping("/check")
public LeResponse<Boolean> check(@Valid @RequestBody LeRequest<XxxDTO> request) {}
```

---

## 认证注解

| 注解 | 用途 | 包路径 |
|------|------|--------|
| `@RequiresAuthentication` | 需要登录（类/方法级） | `net.xnzn.framework.secure.filter.annotation` |
| `@RequiresGuest` | 允许游客访问（方法级覆盖） | `net.xnzn.framework.secure.filter.annotation` |

```java
@RequiresAuthentication   // 类级别：所有方法默认需登录
public class XxxController {

    @RequiresGuest        // 方法级别覆盖：此接口游客可访问
    @PostMapping("/public-list")
    public List<XxxVO> publicList() {}
}
```

---

## 常见场景

### 带 Redisson 分布式锁的导入

```java
@PostMapping("/import-excel")
@ApiOperation(value = "Excel导入")
public void importExcel(@RequestParam(value = "file") MultipartFile file) {
    RLock lock = redissonClient.getLock("import:lock:" + TenantContextHolder.getTenantId());
    if (!lock.tryLock(5, 60, TimeUnit.SECONDS)) {
        throw new LeException("正在处理中，请稍后再试");
    }
    try {
        xxxService.importExcel(file);
    } finally {
        if (lock.isLocked() && lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }
}
```

### 批量删除

```java
@PutMapping("/batch/delete")
@ApiOperation(value = "批量删除")
public void batchDelete(@RequestBody LeRequest<List<Long>> request) {
    xxxService.batchDelete(request.getContent());
}
```

### 树形结构查询

```java
@PostMapping("/tree")
@ApiOperation(value = "树形结构查询")
public List<Tree<Long>> getTree(@RequestBody LeRequest<XxxQueryParam> request) {
    return xxxService.getTree(request.getContent());
}
```

### 同步导出

```java
@SneakyThrows
@PostMapping("/export")
@ApiOperation(value = "导出")
public void export(@RequestBody LeRequest<XxxParam> request, HttpServletResponse response) {
    XxxParam param = request.getContent();
    List<XxxVO> list = xxxService.listAll(param);
    EasyExcelUtil.writeExcelByDownLoadIncludeWrite(response, "文件名",
            XxxVO.class, "标题", list, param.getExportCols());
}
```

### 异步导出（大数据量）

```java
@PostMapping("/export-async/xxx")
@ApiOperation(value = "异步导出")
public void exportAsync(@RequestBody LeRequest<XxxParam> request) {
    XxxParam param = request.getContent();
    exportApi.startExcelExportTaskByPage(
            "文件名", I18n.getMessage("title.key"),
            XxxVO.class, param.getExportCols(), param.getPage(), null,
            () -> PageVO.of(xxxService.listAll(param)));
}
```

---

## 路径命名规范

| 模式 | 示例 | 说明 |
|------|------|------|
| 标准前缀 | `/api/v2/web/module` | 按端区分 |
| 报表前缀 | `/summary/xxx` | 报表/统计类 |
| 查询接口 | `/page/detail`, `/query` | 分页查询 |
| 枚举接口 | `/type-list`, `/state-list` | 枚举数据 |
| 导出接口 | `/export`, `/export-async/xxx` | 同步/异步 |
| 导出 Controller 独立 | `XxxExportWebController` | 与查询分离 |

---

## 检查清单

- [ ] 认证注解：`@RequiresAuthentication` 或 `@RequiresGuest`
- [ ] 文档注解：`@Api` + `@ApiOperation`
- [ ] 参数校验：`@Validated(InsertGroup/UpdateGroup.class)` 或 `@Valid`
- [ ] 请求封装：`LeRequest<T>`
- [ ] 返回类型：分页 `Page<VO>`、单值 `LeResponse<T>`、写操作 `void`
- [ ] 路径命名：`/add`、`/update`、`/query`、`/delete`
- [ ] 敏感操作加分布式锁
- [ ] 跨模块依赖用 `@Lazy` 避免循环依赖

---

## 错误对比

```java
// ❌ 不使用参数封装
public Long add(@RequestBody XxxDTO dto) {}
// ✅ 使用 LeRequest
public void add(@RequestBody LeRequest<XxxDTO> request) { xxxService.add(request.getContent()); }

// ❌ 不使用分组校验
public void add(@Valid @RequestBody LeRequest<XxxDTO> request) {}
// ✅ 使用分组
public void add(@Validated(InsertGroup.class) @RequestBody LeRequest<XxxDTO> request) {}

// ❌ javax.validation（JDK 21 必须 jakarta）
import javax.validation.constraints.NotNull;
// ✅
import jakarta.validation.constraints.NotNull;

// ❌ 缺少认证注解
@RestController
public class XxxController {}
// ✅
@RestController @RequiresAuthentication
public class XxxController {}
```

---

## 真实代码示例

详见 `references/real-examples.md`，包含：
- ReportAnalysisController（报表模块）
- OrderInfoExportWebController（订单导出）
- OrderInfoWebController（订单查询）
- AttendanceLeaveInfoController（考勤请假）
- AllocCanteenController（食堂档口）
- MgrMenuController（菜单权限）

---

## 相关技能

| 需要了解 | Skill |
|---------|-------|
| Service 层 | `leniu-service-development` |
| Entity 设计 | `leniu-entity-design` |
| 数据库设计 | `leniu-database-ops` |
| CRUD 开发 | `leniu-crud-development` |
