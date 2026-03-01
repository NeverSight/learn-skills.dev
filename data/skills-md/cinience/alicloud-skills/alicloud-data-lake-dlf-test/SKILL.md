---
name: alicloud-data-lake-dlf-test
description: Minimal smoke test for DataLake skill. Validate metadata discovery and one read-only API call.
---

Category: test

# DataLake 最小可用测试

## 前置条件

- 已配置 AK/SK 与 region。
- 目标技能：`skills/data-lake/alicloud-data-lake-dlf/`。

## 测试步骤

1) 执行 `python scripts/list_openapi_meta_apis.py`。
2) 选取一个只读 API 执行最小请求。
3) 保存结果到 `output/alicloud-data-lake-dlf-test/`。

## 期望结果

- 元数据拉取成功。
- 只读 API 返回成功或明确权限错误。
