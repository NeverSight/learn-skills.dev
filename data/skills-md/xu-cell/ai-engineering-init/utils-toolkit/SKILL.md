---
name: utils-toolkit
description: |
  后端工具类使用指南。包含对象转换、字符串处理、集合操作、树结构构建、日期时间、JSON、参数校验等通用工具类选型与使用规范。

  触发场景：
  - 对象转换（BO/VO/Entity）
  - 字符串处理、集合流操作
  - 树结构构建
  - JSON 序列化/反序列化
  - 日期时间处理
  - 参数校验

  触发词：工具类、对象转换、BeanUtils、StringUtils、集合操作、树结构、DateUtils、JsonUtils、convert、字符串处理、日期时间

  注意：
  - 对象转换工具需要根据项目实际选型统一使用，禁止混用多种方案。
  - 本指南为通用 Java 后端工具类指南，适配各类 Spring Boot 项目。
---

# 后端工具类大全

## 快速索引

| 功能 | 推荐方案 | 备选方案 | 常用方法 |
|------|---------|---------|---------|
| **对象转换** | `[你的对象转换工具]` | MapStruct / BeanUtils / ModelMapper | `convert()` / `copyProperties()` |
| 字符串 | Hutool `StrUtil` | Apache Commons `StringUtils` / Guava `Strings` | `isBlank()`, `format()` |
| 集合/流 | Hutool `CollUtil` + Java Stream | Guava `Collections2` | `isEmpty()`, `filter()`, `toList()` |
| 树结构 | Hutool `TreeUtil` | 自定义递归构建 | `build()` |
| 日期时间 | `java.time` API | Hutool `DateUtil` | `LocalDateTime.now()`, `format()` |
| 参数校验 | Jakarta Validation | Hutool `Validator` | `@NotNull`, `@NotBlank` |
| JSON | Jackson `ObjectMapper` | Gson / Hutool `JSONUtil` | `toJsonString()`, `parseObject()` |
| 业务异常 | `[你的异常类]` | 自定义 RuntimeException | `throw new [YourException]()` |
| 登录用户 | `[你的用户上下文工具]` | SecurityContextHolder / 自定义 ThreadLocal | `getUserId()`, `getUsername()` |
| Spring容器 | `ApplicationContext` | 自定义 `SpringUtils` | `getBean()` |

---

## 1. 对象转换

### 选型对比

| 方案 | 性能 | 易用性 | 特点 |
|------|------|--------|------|
| **MapStruct** | 极高（编译期生成） | 中（需定义接口） | 类型安全、零反射 |
| **Hutool BeanUtil** | 中（反射） | 高（一行调用） | 简单场景首选 |
| **Spring BeanUtils** | 中（反射） | 高 | Spring 内置，无额外依赖 |
| **ModelMapper** | 低 | 高（约定优于配置） | 深度映射、复杂场景 |

### 通用用法

```java
// 方案 A: Hutool BeanUtil（简单场景推荐）
import cn.hutool.core.bean.BeanUtil;

XxxVo vo = BeanUtil.copyProperties(entity, XxxVo.class);
List<XxxVo> voList = BeanUtil.copyToList(entityList, XxxVo.class);

// 方案 B: MapStruct（高性能场景推荐）
// 1. 定义 Mapper 接口
@Mapper(componentModel = "spring")
public interface XxxConverter {
    XxxVo toVo(XxxEntity entity);
    List<XxxVo> toVoList(List<XxxEntity> entities);
}

// 2. 注入使用
@Resource
private XxxConverter xxxConverter;
XxxVo vo = xxxConverter.toVo(entity);
```

---

## 2. 字符串操作

### Hutool StrUtil

```java
import cn.hutool.core.util.StrUtil;

// 判空
StrUtil.isBlank(str);       // null / "" / " " -> true
StrUtil.isNotBlank(str);

// 格式化（占位符 {}）
StrUtil.format("用户 {} 不存在", userId);

// 分割/拼接
List<String> list = StrUtil.split("1,2,3", ',');
String joined = String.join(",", list);
```

### Apache Commons StringUtils

```java
import org.apache.commons.lang3.StringUtils;

StringUtils.isBlank(str);
StringUtils.substringBefore(str, "-");
StringUtils.leftPad("5", 3, '0');   // "005"
```

### Guava Strings

```java
import com.google.common.base.Strings;

Strings.isNullOrEmpty(str);
Strings.padStart("5", 3, '0');   // "005"
```

---

## 3. 集合与流操作

### Hutool CollUtil

```java
import cn.hutool.core.collection.CollUtil;

CollUtil.isEmpty(list);       // null 或空 -> true
CollUtil.isNotEmpty(list);
```

### Java Stream API

```java
// 过滤
List<User> active = users.stream()
    .filter(u -> "1".equals(u.getStatus()))
    .toList();

// 提取属性
List<Long> ids = users.stream()
    .map(User::getId)
    .toList();

Set<Long> deptIds = users.stream()
    .map(User::getDeptId)
    .collect(Collectors.toSet());

// 转 Map
Map<Long, User> userMap = users.stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));

Map<Long, String> nameMap = users.stream()
    .collect(Collectors.toMap(User::getId, User::getName));

// 分组
Map<Long, List<User>> grouped = users.stream()
    .collect(Collectors.groupingBy(User::getDeptId));

// 拼接字符串
String names = users.stream()
    .map(User::getName)
    .collect(Collectors.joining(","));
```

---

## 4. 树结构构建

### Hutool TreeUtil

```java
import cn.hutool.core.lang.tree.Tree;
import cn.hutool.core.lang.tree.TreeUtil;
import cn.hutool.core.lang.tree.TreeNodeConfig;

List<Tree<Long>> tree = TreeUtil.build(list, 0L, (item, treeNode) -> {
    treeNode.setId(item.getId());
    treeNode.setParentId(item.getParentId());
    treeNode.setName(item.getName());
    treeNode.setWeight(item.getOrderNum());
    treeNode.putExtra("icon", item.getIcon());
});
```

### 自定义递归构建

```java
public List<TreeNode> buildTree(List<TreeNode> nodes, Long parentId) {
    return nodes.stream()
        .filter(n -> Objects.equals(n.getParentId(), parentId))
        .peek(n -> n.setChildren(buildTree(nodes, n.getId())))
        .sorted(Comparator.comparingInt(TreeNode::getSort))
        .toList();
}
```

---

## 5. 日期时间 - java.time API

```java
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.Duration;
import java.time.temporal.ChronoUnit;

// 获取当前时间
LocalDateTime now = LocalDateTime.now();
LocalDate today = LocalDate.now();

// 格式化
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = now.format(fmt);

// 解析
LocalDateTime parsed = LocalDateTime.parse("2026-01-24 15:30:00", fmt);

// 时间差
long days = ChronoUnit.DAYS.between(start, end);
Duration duration = Duration.between(start, end);
long hours = duration.toHours();

// 日期加减
LocalDateTime tomorrow = now.plusDays(1);
LocalDateTime lastMonth = now.minusMonths(1);
```

### Hutool DateUtil（兼容旧 Date 类型）

```java
import cn.hutool.core.date.DateUtil;

// 自动识别多种格式
Date date = DateUtil.parse("2026-01-24 15:30:00");
String formatted = DateUtil.formatDateTime(date);

// 时间差
long between = DateUtil.between(start, end, DateUnit.DAY);
```

---

## 6. 参数校验

### Jakarta Validation（JDK 17+ 推荐）

```java
import jakarta.validation.constraints.*;

public class XxxDTO {
    @NotNull(message = "ID不能为空", groups = {UpdateGroup.class})
    private Long id;

    @NotBlank(message = "名称不能为空", groups = {InsertGroup.class, UpdateGroup.class})
    @Size(max = 100, message = "名称长度不能超过100个字符")
    private String name;

    @Min(value = 0, message = "数量不能为负数")
    private Integer quantity;
}
```

### Controller 层使用

```java
@PostMapping("/add")
public void add(@Validated(InsertGroup.class) @RequestBody XxxDTO dto) { }

@PutMapping("/update")
public void edit(@Validated(UpdateGroup.class) @RequestBody XxxDTO dto) { }
```

---

## 7. JSON 操作

### Jackson（Spring Boot 默认）

```java
import com.fasterxml.jackson.databind.ObjectMapper;

// 推荐封装为项目统一的 JsonUtils
public class JsonUtils {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static String toJsonString(Object obj) {
        return MAPPER.writeValueAsString(obj);
    }

    public static <T> T parseObject(String json, Class<T> clazz) {
        return MAPPER.readValue(json, clazz);
    }

    public static <T> List<T> parseArray(String json, Class<T> clazz) {
        return MAPPER.readValue(json,
            MAPPER.getTypeFactory().constructCollectionType(List.class, clazz));
    }
}
```

### Hutool JSONUtil

```java
import cn.hutool.json.JSONUtil;

String json = JSONUtil.toJsonStr(obj);
User user = JSONUtil.toBean(json, User.class);
```

---

## 8. 对象判空

```java
import cn.hutool.core.util.ObjectUtil;

ObjectUtil.isNull(obj);       // null -> true
ObjectUtil.isNotNull(obj);
ObjectUtil.defaultIfNull(obj, defaultValue);
```

---

## 工具类选择速查

| 需求 | 推荐工具 | 说明 |
|------|---------|------|
| BO/Entity/VO 转换 | `[你的对象转换工具]` | 项目统一选型 |
| 字符串判空 | `StrUtil.isBlank()` | Hutool |
| 集合判空 | `CollUtil.isEmpty()` | Hutool |
| 对象判空 | `ObjectUtil.isNull()` | Hutool |
| 提取集合属性 | `Stream.map().toList()` | Java Stream |
| 集合转 Map | `Collectors.toMap()` | Java Stream |
| 构建树 | `TreeUtil.build()` | Hutool |
| 日期格式化 | `LocalDateTime.format()` | java.time |
| 抛业务异常 | `throw new [你的异常类]()` | 项目自定义 |
| 获取登录用户 | `[你的用户上下文工具]` | 项目自定义 |
| Excel 导出 | EasyExcel / Apache POI | 按需选型 |
| 生成 ID | `IdUtil.getSnowflakeNextId()` | Hutool |

---

## 禁止事项

```java
// ❌ 禁止使用 Map 传递业务数据
public Map<String, Object> getXxx() { ... }
// ✅ 正确：使用 VO/DTO
public XxxVO getXxx() { ... }

// ❌ 禁止频繁创建 ObjectMapper
ObjectMapper mapper = new ObjectMapper();
// ✅ 正确：使用单例或项目统一封装的 JsonUtils

// ❌ 禁止混用多种对象转换工具
// ✅ 正确：项目统一选型，保持一致
```
