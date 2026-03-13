---
name: write_file
description: 文件写入技能，将内容写入到指定文件
version: 1.0.0
category: general
tags:
  - file
  - write
  - 文件写入
  - 保存文件
os:
  - darwin
  - linux
enabled: true
timeout: 30
is_internal: true
parameters:
  filename:
    type: string
    description: 文件名，例如 "note.txt"、"data.json"
    required: true
  content:
    type: string
    description: 要写入文件的内容
    required: true
  path:
    type: string
    description: documents 下的子目录路径（可选），例如 "notes"、"reports/2024"
    required: false
---

# 写入文件技能

将内容写入到文件中，所有文件只能写入当前工作区的 documents 子目录。

## 功能特点

- 自动创建不存在的目录
- 支持自定义文件路径
- 返回写入文件的绝对路径
- 记录写入耗时

## 使用方法

### 写入到 documents 根目录

```json
{
  "name": "write_file",
  "parameters": {
    "filename": "note.txt",
    "content": "这是要写入的内容"
  }
}
```

### 写入到 documents 下的子目录

```json
{
  "name": "write_file",
  "parameters": {
    "filename": "data.json",
    "content": "{\"key\": \"value\"}",
    "path": "notes"
  }
}
```

### 写入到 documents 下的多级子目录

```json
{
  "name": "write_file",
  "parameters": {
    "filename": "report.txt",
    "content": "报告内容",
    "path": "reports/2024"
  }
}
```

## 输出格式

```json
{
  "file_path": "/Users/ray/projects/mindx/documents/note.txt",
  "content_length": 20,
  "elapsed_ms": 5
}
```

## 使用场景

- 需要保存笔记或文档时
- 需要导出数据到文件时
- 需要创建配置文件时
- 需要记录日志或结果时
