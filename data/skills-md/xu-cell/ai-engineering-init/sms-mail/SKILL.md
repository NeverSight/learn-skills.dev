---
name: sms-mail
description: |
  通用短信邮件开发指南。涵盖抽象接口模式、多渠道切换策略、验证码流程、模板消息。
  触发场景：
  - 发送短信验证码
  - 发送邮件通知（文本/HTML/附件）
  - 配置短信服务商（阿里云/腾讯云等）
  - 配置邮件服务器（SMTP）
  - 实现多渠道消息通知
  触发词：短信、邮件、SMS、验证码、通知、邮件发送、短信发送、SMTP、模板消息、多渠道
  注意：如果项目有专属技能，优先使用专属版本。
---

# 短信与邮件开发指南

> 通用模板。如果项目有专属技能，优先使用。

## 设计原则

1. **接口抽象**：定义统一的发送接口，具体渠道通过策略模式实现，方便切换供应商。
2. **异步发送**：发送操作应异步执行，不阻塞主业务流程。
3. **结果校验**：每次发送必须检查返回结果，失败需记录日志并决策是否重试。
4. **安全防护**：验证码需限频限量、设置过期时间，防止短信轰炸和暴力破解。

---

## 实现模式

### 一、抽象接口设计

```java
// 统一短信发送接口
public interface SmsSender {
    SmsResult send(String phone, String templateId, Map<String, String> params);
    SmsResult batchSend(List<String> phones, String templateId, Map<String, String> params);
}

// 统一邮件发送接口
public interface MailSender {
    String sendText(String to, String subject, String content);
    String sendHtml(String to, String subject, String htmlContent);
    String sendWithAttachment(String to, String subject, String content, File... files);
}

// 发送结果
@Data
public class SmsResult {
    private boolean success;
    private String messageId;
    private String errorMessage;
}
```

### 二、短信服务

#### 多渠道策略模式

```java
// 阿里云实现
@Service("aliyunSmsSender")
public class AliyunSmsSender implements SmsSender {
    @Override
    public SmsResult send(String phone, String templateId, Map<String, String> params) {
        // 调用阿里云 SMS SDK
    }
}

// 腾讯云实现
@Service("tencentSmsSender")
public class TencentSmsSender implements SmsSender {
    @Override
    public SmsResult send(String phone, String templateId, Map<String, String> params) {
        // 调用腾讯云 SMS SDK
    }
}

// 工厂/路由
@Service
public class SmsService {

    @Autowired
    private Map<String, SmsSender> senderMap;

    @Value("${sms.default-channel:aliyunSmsSender}")
    private String defaultChannel;

    public SmsResult send(String phone, String templateId, Map<String, String> params) {
        SmsSender sender = senderMap.get(defaultChannel);
        if (sender == null) {
            throw new [你的异常类]("短信渠道未配置: " + defaultChannel);
        }
        SmsResult result = sender.send(phone, templateId, params);
        if (!result.isSuccess()) {
            log.error("短信发送失败: phone={}, error={}", phone, result.getErrorMessage());
        }
        return result;
    }
}
```

#### 配置示例

```yaml
sms:
  default-channel: aliyunSmsSender
  aliyun:
    access-key-id: ${ALIYUN_SMS_KEY:}
    access-key-secret: ${ALIYUN_SMS_SECRET:}
    sign-name: [你的签名]
  tencent:
    secret-id: ${TENCENT_SMS_ID:}
    secret-key: ${TENCENT_SMS_KEY:}
    sdk-app-id: "1400000000"
    sign-name: [你的签名]
```

#### 验证码短信完整示例

```java
@RestController
@RequestMapping("/captcha")
public class CaptchaController {

    @Autowired
    private SmsService smsService;

    @Autowired
    private StringRedisTemplate redisTemplate;

    @GetMapping("/sms")
    public Result<?> sendSmsCode(@RequestParam String phone) {
        // 1. 限频检查（60秒内只能发一次）
        String limitKey = "sms:limit:" + phone;
        if (Boolean.TRUE.equals(redisTemplate.hasKey(limitKey))) {
            return Result.fail("请60秒后重试");
        }

        // 2. 生成验证码
        String code = String.valueOf(ThreadLocalRandom.current().nextInt(100000, 999999));

        // 3. 存入 Redis（5分钟有效）
        String codeKey = "sms:code:" + phone;
        redisTemplate.opsForValue().set(codeKey, code, 5, TimeUnit.MINUTES);
        redisTemplate.opsForValue().set(limitKey, "1", 60, TimeUnit.SECONDS);

        // 4. 发送短信
        Map<String, String> params = new LinkedHashMap<>();
        params.put("code", code);
        SmsResult result = smsService.send(phone, "SMS_VERIFY_CODE", params);

        if (!result.isSuccess()) {
            redisTemplate.delete(codeKey);
            return Result.fail("短信发送失败");
        }
        return Result.ok("验证码已发送");
    }

    @PostMapping("/verify")
    public Result<Boolean> verify(@RequestParam String phone, @RequestParam String code) {
        String codeKey = "sms:code:" + phone;
        String cached = redisTemplate.opsForValue().get(codeKey);

        if (cached == null) return Result.fail("验证码已过期");
        if (!cached.equals(code)) return Result.fail("验证码错误");

        redisTemplate.delete(codeKey);
        return Result.ok(true);
    }
}
```

---

### 三、邮件服务

#### Spring Boot 原生邮件

```java
@Service
public class MailService {

    @Autowired
    private JavaMailSender mailSender;

    @Value("${spring.mail.username}")
    private String from;

    // 文本邮件
    public void sendText(String to, String subject, String content) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(from);
        message.setTo(to);
        message.setSubject(subject);
        message.setText(content);
        mailSender.send(message);
    }

    // HTML 邮件
    public void sendHtml(String to, String subject, String htmlContent) throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
        helper.setFrom(from);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(htmlContent, true);
        mailSender.send(message);
    }

    // 带附件邮件
    public void sendWithAttachment(String to, String subject, String content,
                                    File... attachments) throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
        helper.setFrom(from);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(content, true);
        for (File file : attachments) {
            helper.addAttachment(file.getName(), file);
        }
        mailSender.send(message);
    }

    // 群发
    public void sendHtml(List<String> toList, String subject, String htmlContent)
            throws MessagingException {
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
        helper.setFrom(from);
        helper.setTo(toList.toArray(new String[0]));
        helper.setSubject(subject);
        helper.setText(htmlContent, true);
        mailSender.send(message);
    }
}
```

#### 配置示例

```yaml
spring:
  mail:
    host: smtp.163.com
    port: 465
    username: system@example.com
    password: ${MAIL_PASSWORD}    # 授权码，非登录密码
    properties:
      mail:
        smtp:
          auth: true
          ssl:
            enable: true
          timeout: 10000
          connectiontimeout: 10000
```

常用 SMTP 服务器：

| 提供商 | Host | 端口(SSL) |
|--------|------|----------|
| 163 | smtp.163.com | 465 |
| QQ | smtp.qq.com | 465 |
| Gmail | smtp.gmail.com | 465 |
| 阿里企业邮箱 | smtp.qiye.aliyun.com | 465 |

---

### 四、多渠道消息通知

```java
@Service
public class MessageService {

    @Autowired
    private SmsService smsService;

    @Autowired
    private MailService mailService;

    // 可扩展：站内信、推送、企业微信等
    public void sendNotification(List<String> channels, String subject,
                                  String content, List<UserDTO> users) {
        for (UserDTO user : users) {
            try {
                if (channels.contains("sms") && StringUtils.hasText(user.getPhone())) {
                    Map<String, String> params = Map.of("content", content);
                    smsService.send(user.getPhone(), "SMS_NOTIFY", params);
                }
                if (channels.contains("email") && StringUtils.hasText(user.getEmail())) {
                    mailService.sendHtml(user.getEmail(), subject,
                        "<div style='padding:20px;'><h3>" + subject + "</h3><p>" + content + "</p></div>");
                }
            } catch (Exception e) {
                log.error("消息发送失败, channel={}, userId={}, error={}",
                    channels, user.getUserId(), e.getMessage());
                // 不抛出，继续发送其他用户
            }
        }
    }
}
```

---

## 选型建议

| 维度 | 自研抽象层 | SMS4j | 云 SDK 直接调用 |
|------|----------|-------|----------------|
| 灵活性 | 最高 | 高 | 中 |
| 开发成本 | 中 | 低 | 低 |
| 多渠道切换 | 需自行实现 | 内置支持 | 需改代码 |
| 维护成本 | 中 | 低（社区维护） | 低 |
| 适用场景 | 定制需求高 | 通用 | 单一渠道 |

---

## 常见错误

```java
// 1. 未配置就使用，NPE
SmsSender sender = senderMap.get("xxx");
sender.send(phone, template, params);  // sender 为 null -> NPE
// 应先判空

// 2. 模板参数名与模板定义不匹配
params.put("verifyCode", "123456");  // 模板中变量名是 code
// 应确认模板变量名

// 3. 不检查发送结果
smsService.send(phone, templateId, params);  // 发送可能失败
// 应检查 SmsResult.isSuccess()

// 4. 验证码无过期时间
redisTemplate.opsForValue().set("sms:code:" + phone, code);  // 永不过期
// 应设置 5-10 分钟过期

// 5. 无限频控制（短信轰炸）
// 应限制：同号码 60秒 1 次、每天最多 10 次

// 6. 邮件密码用登录密码而非授权码
// 大多数邮件服务商需要使用"授权码"而非"登录密码"

// 7. 同步发送阻塞主线程
// 短信/邮件发送应使用 @Async 异步执行
```
