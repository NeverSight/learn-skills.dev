---
name: struct-offset-analyzer
description: 静态分析 C 结构体成员偏移量，通过代码阅读计算内存布局
---

# struct-offset-analyzer

静态分析 C 语言结构体成员在内存中的偏移量，无需运行代码即可精确计算。

## 使用场景

- 逆向工程中需要定位结构体成员
- 调试时需要确认内存布局
- 安全研究中分析数据结构
- 二进制分析中理解结构体字段位置

## 工作流程

### 1. 定位结构体定义

```bash
# 搜索结构体定义
grep -n "struct xxx_st {" **/*.h
grep -n "typedef struct" **/*.h
```

### 2. 收集类型信息

查找所有成员类型的定义：
- 嵌套结构体
- 枚举类型
- typedef 别名
- 常量定义（如 `#define EVP_MAX_MD_SIZE 64`）

### 3. 计算对齐规则

| 类型 | 大小 (64-bit) | 对齐要求 |
|------|---------------|----------|
| char/unsigned char | 1 | 1 |
| short | 2 | 2 |
| int/uint32_t | 4 | 4 |
| long/size_t/指针 | 8 | 8 |
| unsigned char[N] | N | 1 (无需填充) |
| 枚举 | 通常 4 | 4 |
| 结构体 | 取决于成员 | 按最大成员对齐 |

**关键规则**：
- 成员偏移必须是其大小的整数倍
- `unsigned char` 数组是 1 字节对齐，**不需要填充**
- 结构体整体大小对齐到最大成员的大小
- 填充字节计入偏移

### 4. 输出偏移表

使用 16 进制表示偏移量，格式：

```
| 偏移(0x) | 成员 | 类型 | 大小 |
|----------|------|------|------|
| 0x00 | field1 | int | 4 |
| 0x04 | *(padding)* | - | 4 |
| 0x08 | field2 | void * | 8 |
```

## 常用搜索模式

```bash
# 查找结构体成员定义
grep -n "struct xxx_st" **/*.h

# 查找类型定义
grep -n "typedef.*XXX" **/*.h

# 查找常量定义
grep -n "#define.*SIZE" **/*.h

# 查找枚举定义
grep -n "typedef enum" **/*.h
```

## 示例：OpenSSL ssl_st 分析

分析 `client_app_traffic_secret` 成员偏移：

1. 定位结构体：`ssl/ssl_local.h:1068`
2. 查找常量：`EVP_MAX_MD_SIZE = 64` (`include/openssl/evp.h:19`)
3. 计算布局，注意 `unsigned char` 数组无需填充
4. 结果：偏移 0x33c (828 字节)

## 注意事项

- 确认目标平台（32-bit vs 64-bit）
- 注意条件编译（#ifdef）可能影响结构体布局
- 检查 #pragma pack 指令可能改变对齐
- 联合体（union）成员共享偏移