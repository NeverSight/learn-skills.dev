---
name: read_file
description: 文件读取技能，从文件中读取内容
version: 1.0.0
category: system
tags:
  - file
  - read
  - 读文件
  - 读取文件
  - 查看文件
os:
  - darwin
  - linux
enabled: true
timeout: 30
command: ./read_file_cli.sh
parameters:
  path:
    type: string
    description: 目标文件路径（绝对路径或相对路径）
    required: true
  encoding:
    type: string
    description: 文件编码，默认为 utf-8
    required: false
---

# 文件读取技能

从指定的文件中读取内容并返回。

## 功能说明

- 支持读取文本文件内容
- 使用系统 cat 命令实现
- 支持绝对路径和相对路径

## 示例

读取文件:

```json
{
  "name": "read_file",
  "parameters": {
    "path": "/Users/ray/test.txt"
  }
}
```

## 输出格式

```json
{
  "success": true,
  "path": "/Users/ray/test.txt",
  "content": "Hello, World!",
  "bytes_read": 13
}
```

## 注意事项

- 确保有足够的文件系统权限
- 大文件读取可能需要较长时间
- 仅支持文本文件，二进制文件可能无法正确显示
