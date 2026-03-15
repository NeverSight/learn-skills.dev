---
name: leniu-security-guard
description: |
  leniu-tengyun-core / leniu-yunshitang 项目安全权限控制规范。包含认证注解体系、TokenManager API、数据权限校验、SQL注入防护。

  触发场景：
  - 配置接口认证注解（@RequiresAuthentication/@RequiresGuest/@RequiresPermissions）
  - 使用 TokenManager 获取用户信息或校验权限
  - 防 SQL 注入（MyBatis #{} 参数化查询）
  - 数据归属校验（防越权）
  - VO 敏感字段脱敏处理

  适用项目：
  - leniu-tengyun-core：/Users/xujiajun/Developer/gongsi_proj/leniu-api/leniu-tengyun-core
  - leniu-yunshitang：/Users/xujiajun/Developer/gongsi_proj/leniu-api/leniu-tengyun/leniu-yunshitang

  触发词：安全认证、权限注解、TokenManager、SQL注入防护、数据脱敏、接口安全、RequiresAuthentication
---

# leniu-security-guard

## 认证注解

所有注解包路径：`net.xnzn.framework.secure.filter.annotation.*`

| 注解 | 用途 |
|------|------|
| `@RequiresAuthentication` | 需要登录认证（最常用，类/方法级） |
| `@RequiresGuest` | 允许游客访问（公开接口） |
| `@RequiresPermissions` | 需要指定权限码 |
| `@RequiresRoles` | 需要指定角色 |
| `@RequiresUser` | 需要用户登录 |
| `@RequiresHeader` | 需要指定请求头 |

### Controller 认证示例

```java
import net.xnzn.framework.secure.filter.annotation.RequiresAuthentication;
import net.xnzn.framework.secure.filter.annotation.RequiresGuest;
import net.xnzn.framework.secure.filter.annotation.RequiresPermissions;
import net.xnzn.framework.secure.filter.annotation.RequiresRoles;

// 类级别：整个 Controller 需要登录
@RestController
@RequestMapping("/api/v2/web/xxx")
@RequiresAuthentication
public class XxxWebController { }

// 方法级别：允许游客访问
@GetMapping("/public/info")
@RequiresGuest
public LeResponse<String> getPublicInfo() { }

// 需要特定权限
@GetMapping("/admin/users")
@RequiresPermissions("system:user:list")
public LeResponse<List<User>> listUsers() { }

// AND 逻辑（默认）：需要所有权限
@RequiresPermissions(value = {"system:user:add", "system:user:edit"}, logical = Logical.AND)

// OR 逻辑：需要任一权限
@RequiresPermissions(value = {"system:user:add", "system:user:edit"}, logical = Logical.OR)

// 需要指定角色
@RequiresRoles("admin")

// 需要所有角色
@RequiresRoles(value = {"admin", "manager"}, logical = Logical.AND)
```

> **注意**：`@RequiresPermissions` 不指定 `value` 时，自动使用 `@RequestMapping` 路径作为权限码。

---

## TokenManager API

```java
import net.xnzn.framework.secure.token.TokenManager;
```

### 用户信息

```java
// 登录状态
TokenManager.isLogin();

// 用户 ID
Long userId = TokenManager.getSubjectId().orElse(null);

// 用户名
String userName = TokenManager.getSubjectName().orElse(null);

// 附加数据
Map<String, String> userData = TokenManager.getSubjectData();
String orgId = userData.get("orgId");
```

### 权限/角色校验

```java
// 单个权限
TokenManager.hasPermission("system:user:add");

// 多个权限（AND）
TokenManager.hasPermission("system:user:add", "system:user:edit");

// 任一权限（OR）
TokenManager.hasAnyPermission("system:user:add", "system:user:edit");

// 角色
TokenManager.hasRole("admin");
TokenManager.hasAnyRole("admin", "manager");
```

### 附加数据管理

```java
// 添加
TokenManager.attachData("orgId", "12345");

// 批量添加
TokenManager.attachData(Map.of("orgId", "12345", "deptId", "67890"));

// 获取
String orgId = TokenManager.getSubjectData().get("orgId");

// 移除
TokenManager.removeData("orgId", "deptId");
```

### 登出与缓存

```java
// 登出
TokenManager.logout();

// 强制下线
TokenManager.revokeAuthenticate();

// 撤销旧 Token（保留最近 N 个）
TokenManager.revokeAuthenticate(userId, 3);

// 清除权限/角色缓存
TokenManager.clearPermission(userId);
TokenManager.clearRole(userId);
TokenManager.clearRoleAndPermission(userId);
TokenManager.clearAllRoleAndPermission();
```

---

## WebContext

```java
import net.xnzn.framework.secure.WebContext;

HttpServletRequest request = WebContext.get().getRequest().orElse(null);
HttpServletResponse response = WebContext.get().getResponse().orElse(null);
Optional<AccessToken> token = WebContext.get().getAccessToken();

// 属性存取
WebContext.get().setAttribute("key", "value");
Object value = WebContext.get().getAttribute("key");
WebContext.reset();
```

---

## 数据权限校验（防越权）

```java
@Transactional(rollbackFor = Exception.class)
public void delete(Long id) {
    Order order = orderMapper.selectById(id);
    Assert.notNull(order, () -> new LeException("订单不存在"));

    // 校验数据归属
    Long currentUserId = TokenManager.getSubjectId()
        .orElseThrow(() -> new LeException("用户未登录"));
    if (!order.getUserId().equals(currentUserId)) {
        throw new LeException("无权操作该订单");
    }

    orderMapper.deleteById(id);
}
```

### 最小权限原则

```java
@RequiresAuthentication
@RequiresPermissions("order:view")
public PageVO<OrderVO> pageList(OrderPageParam param) {
    Long userId = TokenManager.getSubjectId()
        .orElseThrow(() -> new LeException("用户未登录"));
    param.setUserId(userId);  // 限制只查自己的数据
    return orderService.pageList(param);
}
```

---

## SQL 注入防护

### MyBatis XML 必须用 `#{}`

```xml
<!-- 正确：参数化查询 -->
<select id="selectByName" resultType="User">
    SELECT id, name, mobile FROM user WHERE name = #{name}
</select>

<!-- 错误：${} 有注入风险 -->
<select id="selectByName" resultType="User">
    SELECT * FROM user WHERE name = '${name}'
</select>
```

### 禁止 SELECT *

```xml
<!-- 错误 -->
SELECT * FROM user WHERE status = #{status}

<!-- 正确：明确指定字段 -->
SELECT id, name, mobile, status FROM user WHERE status = #{status}
```

---

## VO 敏感字段处理

```java
@Data
public class UserVO {
    @JsonIgnore
    private String password;  // 密码绝不返回

    @JsonSerialize(using = MobileSerializer.class)
    private String mobile;    // 手机号脱敏

    @JsonSerialize(using = IdCardSerializer.class)
    private String idCard;    // 身份证脱敏
}
```

### 日志脱敏

```java
// 错误：记录敏感信息
log.info("用户登录, username:{}, password:{}", username, password);

// 正确：不记录密码
log.info("用户登录, username:{}", username);
```

---

## 输入验证

```java
@Data
public class UserParam {
    @NotBlank(message = "用户名不能为空")
    @Pattern(regexp = "^[a-zA-Z0-9_]{4,20}$", message = "用户名格式不正确")
    private String username;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度必须在6-20之间")
    private String password;

    @NotBlank(message = "手机号不能为空")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String mobile;

    @Email(message = "邮箱格式不正确")
    private String email;
}
```

---

## 限流防护

```java
// Redis 计数器限流
public void checkRateLimit(Long userId, String api, int limit, int seconds) {
    String key = String.format("rate:%d:%s", userId, api);
    Integer count = RedisUtil.incr(key, (long) seconds);
    if (count > limit) {
        throw new LeException("请求过于频繁，请稍后重试");
    }
}
```

---

## 注意事项

1. 权限和角色数据自动缓存到 Redis，通过 `clearPermission/clearRole` 手动清除
2. `TokenManager` 方法需在已登录上下文中使用
3. `@RequiresGuest` 用于公开接口，不需要登录
4. MyBatis XML 中必须使用 `#{}` 而非 `${}`
5. VO 中密码字段必须 `@JsonIgnore`，手机号等用序列化脱敏
6. 限流 key 格式：`rate:{userId}:{api}`
