---
name: api-integration
description: 指导在 Vue3 业务列表、表单、详情和操作 Hook 中集成 Orval API，覆盖真实生成产物选择、mutator 响应契约、错误提示、加载状态、请求选项和长整型精度；当页面对接查询、新增、编辑、删除、详情或文件流接口时使用。
---

# API Integration Skill

## 触发条件

- 页面需要对接 Orval 生成的列表、详情、新增、编辑或删除接口。
- 需要处理分页映射、loading、长整型 ID、取消请求或特殊错误交互。
- 需要实现文件导出，并核对 Blob 与 mutator 返回结构。

## 不适用场景

- 仅调整静态布局或 Formily Schema，不涉及任何接口。
- 后端契约和 OpenAPI 尚未提供，无法核对真实方法与 DTO。

## 使用前必读

1. 读取当前微应用的 Orval 配置、生成后的 API 文件、`packages/src/api/mutator.ts` 和错误处理器；禁止根据旧示例猜测导出名和返回结构。
2. 如需文件导出，同时读取 `../file-export-download/SKILL.md`。
3. 如需 YSS UI 组件 API，MCP 可用时先调用 `get_component_docs` 精确查询；名称不确定或精确查询无结果时，用 `search_docs`、`list_components` 校正。
4. 仅在 MCP 不可用、调用失败或校正后仍无结果时，回退读取最新 `llms-full.txt`；文档与当前依赖版本不一致时，以当前源码、CodeGraph 和真实导出为准。

## 真实 mutator 响应契约

当前微应用模板的 `mutator.ts` 行为是：

- 普通 JSON 响应直接返回 `response.data`。
- 当 JSON 对象显式包含 `success === false` 时，拦截器调用全局业务错误提示并 `Promise.reject(error)`。
- HTTP 4xx/5xx 和网络错误由全局 `handleErrorResponse` 提示后继续 reject。
- Blob 成功响应返回 `{ data, headers }`；HTTP 错误中的 Blob JSON 由全局错误处理器解析。
- 当前 mutator **不会**检测 HTTP 200 Blob 内包装的 `success === false` JSON；这种契约必须先改为合理的 HTTP 错误状态，或在 mutator 中统一补齐，不得让每个业务 Hook 各自解析。

## 硬约束（禁止/必须）

- 禁止对普通 Orval 请求结果使用 `if (res?.success)` 或 `if/else` 判断业务成功；`success === false` 已被 reject，`await` 继续执行即为成功。
- 禁止在 `else` 或 `catch` 中重复调用 `message.error`、`notification.error` 或项目的错误 Toast。
- Hook 可在 `catch` 中清理局部数据、记录错误状态或阻止继续执行，但不重复展示错误。
- 只有显式传入 `skipBusinessError: true` 或 `skipErrorHandler: true` 时，业务代码才能在 `catch` 中实现自定义错误交互。
- 成功 Toast 必须放在 `await` 之后，不得放在 `finally` 或无条件分支中。
- loading 必须在 `finally` 中恢复；需要阻止未处理 reject 时，在 Hook 内捕获并仅维护状态。

## Orval 生成与导入

生成链路通常为：

```bash
pnpm generate:api
# orval → schema cleanup → 可选的导出扁平化 → prettier
```

必须先打开生成文件确认导出：

- 已存在模块级具名 API 函数时，优先具名导入。
- 如果当前产物只导出 `getXxxApi()` 工厂，在**模块顶层**创建一次实例；禁止每次 Hook 初始化或每次请求都重新调用工厂。
- 不得根据文档示例假定工厂一定名为 `getApi()`；Orval `title` 配置会影响真实名称。
- 请求/响应 DTO 必须从当前生成的 `schemas` 导入，禁止重复声明。

## 标准代码骨架

以当前模板的真实 `getApiApi()` 产物为例：

```typescript
import { reactive, ref } from 'vue';
import { getApiApi } from '@/api/generated/quality';
import type { QualityBusinessRuleVO, QualityRulePage } from '@/api/generated/quality/schemas';

const { pageQualityRule } = getApiApi();

/** 管理质量规则列表请求和分页状态。 */
export const useQualityRuleList = () => {
  const loading = ref(false);
  const dataList = ref<QualityBusinessRuleVO[]>([]);
  const query = reactive<QualityRulePage>({ pageIndex: 1, pageSize: 20, ruleName: '' });
  const total = ref(0);

  /** 加载规则列表。 */
  const fetchData = async (): Promise<void> => {
    loading.value = true;
    try {
      const res = await pageQualityRule(query);
      dataList.value = res.data ?? [];
      total.value = res.totalCount ?? 0;
    } catch {
      dataList.value = [];
      total.value = 0;
    } finally {
      loading.value = false;
    }
  };

  return { loading, dataList, query, total, fetchData };
};
```

> 如果所在项目已生成 `pageQualityRule` 具名导出，直接导入该函数，删除上面的工厂实例行。

## 长整型与数值类型

`JSONbig({ storeAsString: true })` 会把超出 JavaScript 安全整数范围的整数保留为字符串；**不会把所有普通 number 都转成字符串**。分页页码、状态值、普通小数和安全范围整数仍可按真实类型计算。

硬约束：

- ID、雪花 ID、长整型业务键一旦运行时为字符串，必须原样透传和比较，禁止 `Number()`、`parseInt()`、一元 `+` 或位运算转回 number。
- 优先修正 OpenAPI，将可能超过 `Number.MAX_SAFE_INTEGER` 的 ID 声明为 `string`；不得以 `as unknown as number` 长期掩盖错误契约。
- 普通数值计算按生成类型执行；金额或高精度计算使用 `decimal.js`/`big.js` 并以字符串入参。

```typescript
// ❌ 长整型 ID 会丢失精度
await detailQualityRule(Number(row.id));

// ✅ 保持 ID 的字符串契约
await detailQualityRule(row.id);

// ✅ 页码等普通数值仍使用 number
query.pageIndex = pagination.current;
```

## 自定义请求选项

Orval 配置 `options: true` 后，生成方法的最后一个可选参数会透传给 `customInstance`。必须先检查当前生成函数签名。

- `skipBusinessError?: boolean`：仅跳过 `success === false` 的全局业务提示，请求仍 reject。
- `skipErrorHandler?: boolean`：跳过业务错误与 HTTP/网络错误的全局提示，请求仍 reject。
- Axios 原生选项：`responseType`、`headers`、`timeout`、`signal`、`onUploadProgress`、`onDownloadProgress` 等均在该参数顶层传入。

```typescript
try {
  await addQualityRule(values, { skipBusinessError: true });
} catch (error) {
  // 只有显式跳过全局业务提示时，才在此实现自定义错误交互。
  showCustomError(error);
}

const controller = new AbortController();
await pageQualityRule(query, { signal: controller.signal, timeout: 120000 });
```

## 交付检查清单

- [ ] 已检查 Orval 配置、生成文件和 mutator 真实实现。
- [ ] 使用生成 DTO，未手写重复接口类型。
- [ ] 优先使用真实具名导出；只有工厂时仅在模块顶层创建一次。
- [ ] 没有 `if (res?.success)` 冗余分支，没有在 `else/catch` 重复错误 Toast。
- [ ] 成功后逻辑仅在 `await` 成功后执行，loading 在 `finally` 恢复。
- [ ] 长整型 ID 保持字符串，普通 number 没有被错误当成字符串。
- [ ] 特殊错误交互已显式传入 skip 选项，未默认关闭全局处理。
- [ ] 文件流已按 `file-export-download` 核对 Blob、响应头和错误链路。

## 失败兜底策略

- 生成导出与 skill 示例不同时，以生成文件为准并更新生成脚本，禁止绕过类型检查猜名调用。
- 接口字段不稳定时，在 Hook API 边界做最小映射，不把兼容逻辑散落到模板。
- HTTP 200 Blob 业务错误时，先修复后端状态码或 mutator 统一解析，禁止在业务 Hook 重复实现。
