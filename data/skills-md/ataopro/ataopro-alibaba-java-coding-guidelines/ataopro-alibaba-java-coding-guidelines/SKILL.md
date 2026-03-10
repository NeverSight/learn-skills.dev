---
name: ataopro-alibaba-java-coding-guidelines
description: 阿里巴巴Java开发手册（阿里开发规范），用于代码规范检查和指导开发。当用户需要检查Java代码是否符合阿里开发规范时调用此技能。
author: ataopro
version: 1.1.0
date: 2026-02-20
copyright: Copyright © 2026 ataopro. All rights reserved.
repository: https://github.com/ataopro/ataopro-alibaba-java-coding-guidelines
tags: [java, coding-guidelines, alibaba, code-review, best-practices]
---

# 阿里巴巴Java开发手册

本技能基于阿里巴巴Java开发手册（简称：阿里开发规范），用于Java代码规范检查、指导开发和代码审查。

## 触发场景

当用户表达以下意图时，此技能将被自动激活：

### 1. 代码规范检查
- "检查代码规范"
- "帮我检查Java代码"
- "代码审查"
- "查看代码是否符合阿里规范"
- "检查代码是否有问题"
- "帮我review一下这段代码"

### 2. 指定开发规范
- "使用阿里开发规范"
- "用阿里巴巴规范开发"
- "按阿里开发手册来"
- "遵循阿里开发规范"
- "阿里开发规范"
- "按照规范来写"

### 3. 优化建议
- "优化Java代码"
- "代码改进建议"
- "如何写出规范的Java代码"
- "这段代码怎么改更好"

---

## 核心规则速查

### 1. 命名风格 【强制】

| 规则 | 正例 | 反例 |
|------|------|------|
| 类名 | `UserDO`, `CacheServiceImpl`, `OrderDTO` | `userDo`, `User_Do` |
| 方法名/变量 | `getUserById`, `localValue`, `inputUserId` | `get_user_by_id` |
| 常量 | `MAX_STOCK_COUNT`, `DEFAULT_TIMEOUT` | `MAX_COUNT`, `maxStockCount` |
| 布尔变量 | `deleted`, `active`, `isValid`(仅boolean) | `isDeleted`(POJO中) |
| 包名 | `com.alibaba.open.util` | `com.Alibaba.Open.util` |

**关键规则：**
- 禁止下划线或美元符号开头/结尾
- 禁止拼音英文混合
- 抽象类以 `Abstract` 或 `Base` 开头
- 异常类以 `Exception` 结尾
- 测试类以 `Test` 结尾

### 2. 常量定义 【强制】

```java
// ❌ 反例 - 魔法值
String key = "Id#taobao_" + tradeId;
cache.put(key, value);

// ✅ 正例
private static final String KEY_PREFIX = "Id#taobao_";
String key = KEY_PREFIX + tradeId;
```

```java
// ❌ 反例 - 小写l易混淆
Long a = 2l;

// ✅ 正例
Long a = 2L;
```

### 3. OOP规约 【强制】

#### equals调用顺序
```java
// ❌ 反例 - 可能抛NPE
object.equals("test");

// ✅ 正例 - 推荐
"test".equals(object);
Objects.equals(object, "test");
```

#### 包装类比较
```java
// ✅ 正例 - 使用equals
Integer a = 128;
Integer b = 128;
a.equals(b);  // true

// ❌ 反例 - == 比较
a == b;  // false (超出-128~127范围)
```

#### POJO类规范
```java
// ❌ 反例 - 使用基本类型
public class User {
    private int id;        // 基本类型
    private boolean isActive; // is前缀
    private Date gmtCreate = new Date(); // 默认值
}

// ✅ 正例
public class User {
    private Long id;           // 包装类型
    private Boolean active;    // 无is前缀
    private Date gmtCreate;    // 无默认值
}
```

#### 访问控制从严
```java
// 工具类
public final class StringUtils {
    private StringUtils() {}  // 私有构造
}

// 方法可见性
private void internalMethod() {}     // 仅内部使用
protected void hookMethod() {}       // 供子类调用
public void publicApi() {}           // 对外暴露
```

### 4. 集合处理 【强制】

#### hashCode与equals
```java
// ❌ 反例 - 只重写equals
@Override
public boolean equals(Object o) { ... }

// ✅ 正例 - 配对重写
@Override
public boolean equals(Object o) { ... }
@Override
public int hashCode() { ... }
```

#### subList不可强转
```java
// ❌ 反例
ArrayList list = subList; // ClassCastException

// ✅ 正例
List list = subList;
```

#### Arrays.asList()不可修改
```java
// ❌ 反例
String[] str = {"a", "b"};
List list = Arrays.asList(str);
list.add("c"); // UnsupportedOperationException

// ✅ 正例 - 需要可修改列表
List<String> list = new ArrayList<>(Arrays.asList(str));
```

#### foreach中禁止remove
```java
// ❌ 反例 - ConcurrentModificationException
for (String item : list) {
    list.remove(item);
}

// ✅ 正例
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (condition) {
        it.remove();
    }
}

// ✅ JDK8+ 推荐
list.removeIf(item -> condition);
```

#### Map遍历
```java
// ❌ 反例 - keySet遍历两次
for (String key : map.keySet()) {
    Object value = map.get(key);
}

// ✅ 正例 - entrySet一次遍历
for (Map.Entry<String, Object> entry : map.entrySet()) {
    String key = entry.getKey();
    Object value = entry.getValue();
}

// ✅ JDK8+ 推荐
map.forEach((k, v) -> { ... });
```

### 5. 并发处理 【强制】

#### 线程池创建
```java
// ❌ 反例 - 可能导致OOM
ExecutorService executor = Executors.newFixedThreadPool(10);
ExecutorService executor = Executors.newCachedThreadPool();

// ✅ 正例
ExecutorService executor = new ThreadPoolExecutor(
    10,                          // corePoolSize
    50,                          // maximumPoolSize
    60L, TimeUnit.SECONDS,       // keepAliveTime
    new LinkedBlockingQueue<>(100), // workQueue
    new ThreadFactory() {
        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r);
            t.setName("custom-pool-" + t.getId());
            return t;
        }
    },
    new ThreadPoolExecutor.AbortPolicy()
);
```

#### SimpleDateFormat线程不安全
```java
// ❌ 反例 - 线程不安全
private static final DateFormat DF = new SimpleDateFormat("yyyy-MM-dd");

// ✅ 方案1: ThreadLocal
private static final ThreadLocal<DateFormat> DF = 
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// ✅ 方案2: JDK8+ 推荐
private static final DateTimeFormatter DTF = 
    DateTimeFormatter.ofPattern("yyyy-MM-dd");
LocalDate date = LocalDate.parse("2024-01-01", DTF);
```

#### Random多线程
```java
// ❌ 反例 - 线程竞争
Random random = new Random();
int randomValue = random.nextInt(100);

// ✅ 正例
int randomValue = ThreadLocalRandom.current().nextInt(100);
```

### 6. 控制语句 【强制】

```java
// ❌ 反例 - 无大括号
if (condition)
    doSomething();

// ✅ 正例
if (condition) {
    doSomething();
}

// ❌ 反例 - switch无default
switch (status) {
    case 1: doThing(); break;
    case 2: doOther(); break;
}

// ✅ 正例 - 必须有default
switch (status) {
    case 1: doThing(); break;
    case 2: doOther(); break;
    default: logger.warn("Unknown status: {}", status);
}
```

### 7. 注释规范 【强制】

```java
/**
 * 根据用户ID获取用户信息
 *
 * @param userId 用户ID，不能为空
 * @return 用户信息，如果不存在返回null
 * @throws IllegalArgumentException if userId is null
 */
public UserDO getUserById(Long userId) {
    // 单行注释
    if (userId == null) {
        throw new IllegalArgumentException("userId不能为空");
    }
    // TODO(zhangsan: 2024-01-01) 等需求确认后实现缓存
    // FIXME(张三: 2024-01-15) 高并发下有性能问题，需要优化
    return userDAO.selectById(userId);
}
```

### 8. MySQL规约 【强制】

| 规则 | 说明 |
|------|------|
| 主键命名 | `id` 或 `{表名}_id` |
| 索引命名 | `idx_字段名`, `uniq_字段名` |
| 布尔字段 | `is_xxx` / `xxx_status` |
| 时间字段 | `gmt_create`, `gmt_modified` |
| 删除标记 | `is_deleted` (0/1) |

```sql
-- ✅ 正例
CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    status TINYINT DEFAULT 0 COMMENT '0-正常 1-禁用',
    gmt_create DATETIME DEFAULT CURRENT_TIMESTAMP,
    gmt_modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted TINYINT DEFAULT 0
);

CREATE INDEX idx_username ON user(username);
CREATE UNIQ INDEX uniq_phone ON user(phone);
```

### 9. 异常处理 【强制】

```java
// ❌ 反例
try {
    doSomething();
} catch (Exception e) {
    // 捕获所有异常
}

// ❌ 反例 - 吞掉异常
try {
    doSomething();
} catch (Exception e) {
    // 什么都不做
}

// ✅ 正例
try {
    doSomething();
} catch (SpecificException e) {
    logger.error("业务错误描述", e);
    throw new BusinessException("用户友好的错误信息");
}

// ✅ 正例 - try-with-resources
try (Connection conn = dataSource.getConnection()) {
    // 自动关闭
}
```

### 10. 日志规约 【强制】

```java
// ❌ 反例
logger.info("用户登录: " + userId);
logger.debug("debug info");
logger.error(e.getMessage()); // 丢失堆栈

// ✅ 正例 - 包含上下文
logger.info("用户登录成功, userId={}, ip={}", userId, ip);
logger.warn("库存不足, skuId={}, available={}", skuId, available);
logger.error("调用下游服务失败, service=order, error={}", e.getMessage(), e);

// 正确的日志级别
logger.error("系统异常", e);           // ERROR: 影响功能
logger.warn("业务校验失败", e);        // WARN: 需关注但不影响
logger.info("订单创建成功, orderId={}", orderId); // INFO: 关键节点
logger.debug("请求参数: {}", params);  // DEBUG: 调试信息
```

---

## 代码格式规范

### 缩进与空格
```java
// ✅ 缩进4个空格，运算符左右各一空格，关键词与括号间有空格
public static void main(String[] args) {
    String say = "hello";
    int flag = 0;
    
    if (flag == 0) {
        System.out.println(say);
    } else if (flag == 1) {
        System.out.println("world");
    } else {
        System.out.println("ok");
    }
}

// ✅ 方法参数逗号后有空格
method("a", "b", "c");
```

### 换行规则
```java
// ✅ 超120字符换行，缩进4空格
StringBuffer sb = new StringBuffer();
sb.append("zi").append("xin")...
   .append("huang")...
   .append("huang")...
   .append("huang");

// ✅ 多参数换行
method(args1, args2, args3, 
       args4, args5);
```

---

## 快速检查清单

代码提交前逐项检查：

### 基础规范
- [ ] 命名符合规范（类名、方法名、常量等）
- [ ] 包名全小写，无复数形式
- [ ] 无下划线/美元符号开头结尾

### 代码质量
- [ ] 无魔法值，使用常量定义
- [ ] equals/hashCode配对重写
- [ ] equals调用顺序正确
- [ ] 包装类比较使用equals
- [ ] POJO属性使用包装类型，无默认值

### 集合操作
- [ ] subList正确使用
- [ ] Arrays.asList不可修改
- [ ] foreach中正确remove
- [ ] Map使用entrySet遍历

### 并发安全
- [ ] 线程池正确创建
- [ ] SimpleDateFormat线程安全
- [ ] Random使用ThreadLocalRandom
- [ ] 多线程共享资源加锁

### 控制语句
- [ ] switch有default
- [ ] if/while有花括号
- [ ] 无多层嵌套（用卫语句）

### 注释与日志
- [ ] 类/方法有Javadoc注释
- [ ] 日志有上下文信息
- [ ] 异常处理正确

---

## 配套工具

### IDE插件
- **IDEA**: Alibaba Java Coding Guidelines
- **Eclipse**: Alibaba Java Coding Guidelines

### Maven插件
```xml
<!-- CheckStyle -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <configuration>
        <configLocation>checkstyle.xml</configLocation>
    </configuration>
</plugin>

<!-- SpotBugs -->
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
</plugin>
```

### CheckStyle规则
参考阿里规范配置checkstyle.xml：
- 驼峰式命名
- 大括号换行规则
- 缩进4空格

---

## 相关资源

- 阿里巴巴Java开发手册: https://developer.aliyun.com/article/1589859
- Alibaba Java Coding Guidelines插件: https://plugins.jetbrains.com/plugin/10032-alibaba-java-coding-guidelines
- GitHub仓库: https://github.com/ataopro/ataopro-alibaba-java-coding-guidelines

---

## 更新日志

### v1.1.0 (2026-02-20)
- 新增代码格式规范详解
- 增加MySQL建表规范示例
- 增加异常处理最佳实践
- 增加日志规范示例
- 完善快速检查清单

### v1.0.0 (2026-02-20)
- 初始版本
- 基于阿里巴巴Java开发手册整理
- 包含10大章节核心规范

---

**版权声明**: 本技能内容整理自阿里巴巴Java开发手册，仅供学习参考使用。
**作者**: ataopro
**版本**: 1.1.0
**许可证**: MIT
