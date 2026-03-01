---
name: alicloud-data-lake-dlf-next-test
description: Minimal smoke test for DlfNext skill. Validate metadata discovery and one read-only API call.
---

Category: test

# DlfNext 最小可用测试

## 前置条件

- 已配置 AK/SK 与 region。
- 目标技能：`skills/data-lake/alicloud-data-lake-dlf-next/`。

## 测试步骤

1) 执行 `python scripts/list_openapi_meta_apis.py`。
2) 选取一个只读 API 执行最小请求。
3) 保存结果到 `output/alicloud-data-lake-dlf-next-test/`。

## 期望结果

- 元数据与只读查询链路均可用。
