---
name: i18n-locale-management
description: 指导 Vue3 微前端（主应用与微应用）中国际化（i18n）字典的模块化设计、简繁英三语镜像对齐、命名分层、Vite 自动化加载、微前端通信与业务消费规范；当新增业务模块、维护多语言字典、支持繁体中文/英文、重构页面文案或调用 $t/useI18n 时使用。
---

# 国际化字典与微前端语言管理

## 触发条件

维护 Vue3 主应用或微应用三语词典、国际化响应式配置、语言切换、生命周期桥接、请求头与日期数字展示时使用。组件库维护还应结合 component-development；组件 API、能力边界以当前源码和组件文档为准。

## 不适用场景

不负责后端实体翻译、业务术语决策、认证/权限规则变更或时区币种策略修改；这些内容遵循对应领域契约。

## 语言协议

| 应用代码 | 显示标签 | Ant Design Vue | Day.js | Accept-Language |
| --- | --- | --- | --- | --- |
| zh-CN | 简体中文 | zh_CN | zh-cn | zh-CN,zh;q=0.9 |
| zh-TW | 繁體中文 | zh_TW | zh-tw | zh-TW,zh;q=0.9 |
| en-US | English | en_US | en | en-US,en;q=0.9 |

Locale 请求头使用完整应用代码。门户 DTO 只传可序列化的 locale 与 localeRevision，不传 Vue Ref、函数或 i18n 实例。门户优先级高于持久化；独立运行时优先持久化，未设置时默认简体；浏览器协商仅在项目明确启用时使用。语言协商先判断语言再判断脚本及区域：en-HK 是英文，zh-Hant 是繁体，不能用 includes('hk') 直接决定语言。

繁体术语优先使用：儲存、重設、確定、編輯、刪除、載入、暫無資料。具体业务术语由产品词汇表统一，不机械进行逐字简繁替换。

## 硬约束（禁止/必须）

1. 三语模块文件、叶子键、数组结构、具名占位符保持一致。缺键回退只作为运行兜底，不能代替验收。
2. 业务词典位于 locales/lang/{locale}/{module}.ts，聚合入口只装配模块。common 模块可平铺 common、app、route 等明确命名空间；聚合应检查命名冲突。
3. 通用按钮使用项目现有 common.xxx 键；先检查实际词典。不得猜测 common.action.save、common.actions.save 或 common.create 存在。
4. 展示文本使用词条和具名参数；禁止拼接翻译片段。业务状态 code、接口字段、日期原值、币种、长整型标识不翻译。已有中文状态枚举可在展示层映射，但筛选/提交仍用原值。
5. 先确认应用切换策略。采用整页重载的业务允许静态 t() 配置，必须在语言初始化完成后再加载该模块；采用热切换的页面/组件才要求 Schema、columns、actionConfig 等响应式求值。不批量改造无热切换需求的旧业务。
6. 登录页热切换；包含旧微应用的系统内部默认采用确认后的平滑整页重载（路线 C）。确认取消时不改状态；确认重载后保留 URL 与认证，但不承诺保留未保存输入、撤销栈或组件实例。仅在明确选择热切换的场景中，禁止用 locale key 重建表单/路由/表格来掩盖同步缺陷。
7. 独立模式可见的菜单、登录页、404、空态同样需要翻译。路由保留稳定 path/name，渲染端读取 meta.i18nKey 或已注册的 title key；仅用于内部匹配且从不显示的元数据无需翻译。
8. 不将全部组件库动态导入当作语言适配。应用从 @yss-ui/components/locale 与其语言子路径导入；不能提交开发者本机绝对路径依赖。
9. 未经核验，不得宣称“全部组件完全支持”或“零运行时开销”。区分组件按钮、第三方引擎、业务配置、后端数据与插件词典。

## 切换策略与生命周期

- **登录页**：准备业务、Ant Design Vue、YSS UI 和日期资源，成功且请求仍最新时同步提交；失败保留旧状态和已输入凭据。未设置偏好时默认简体。
- **系统内路线 C**：统一确认未保存内容可能丢失；预检目标资源、显示过渡层、可靠持久化 locale，再重载当前完整 URL。不能先热更新旧界面/请求头再等待重载，避免旧页面在离开前发出混合语言请求。
- 遮罩必须同时覆盖旧文档切换阶段与新 HTML 引导阶段；依据门户/当前微应用 ready 或错误状态结束，并提供超时重试。固定 250ms 不能作为加载完成标准，也不能保证所有网络环境绝无白屏。
- 重载不清除 localStorage、IndexedDB、Service Worker 或 HTTP 缓存。门户启动显式刷新目标语言菜单/平台数据；各应用业务字典缓存按 locale 分区或定向失效。不清认证令牌、用户草稿或全部浏览器存储。
- 初始化顺序必须为：获取有效语言 → 加载词典并建立请求头 → 动态导入 App/路由/静态配置 → 挂载。仅把 await 写在静态 import 下方不能阻止依赖提前执行。
- 嵌入模式 mount 接收门户 locale；独立模式使用持久化偏好。其它标签页接到 storage 变化后，登录页热切换，系统内先确认重载，不能静默刷新有编辑内容的页面。
- 旧微应用最低接入要求是能在启动时读取标准语言、加载词典并为请求带头。重载不能翻译硬编码中文、补齐缺失键、修复过早执行的静态 t() 或自动改变第三方引擎语言。
- 新页面/组件若明确需要热切换，可以继续采用统一事务和版本化 update；仅该路径要求响应式业务配置、数据重取和状态保持。不要把可选能力升级为所有旧项目的交付要求。
- unmount 清理监听和在途操作；请求拦截器读当前文档已生效的内存语言，持久化偏好供下次启动读取。

## 组件库适配边界

YConfigProvider 只提供组件词典；不替代 Ant Design Vue ConfigProvider，不负责持久化或 HTTP。缺省继承父级/全局语言。YTable/YEditTable 在实际使用时加载、注册 VXE 词典；原生 VXE 可显式 await syncVxeLanguage。仅 setLanguage 而不注册词典不能完成翻译。

YFormily 自动切换内置校验词典并刷新已有错误，业务自定义校验应在执行时翻译。VXE 和 Formily 校验器是引擎单例，同一引擎不保证多种语言并存。微应用同步到统一门户语言。

YSheet 核心支持三语原生切换，extraLocales 必须补齐使用的扩展插件词典。YMonaco 自有按钮三语，当前 Monaco ESM 内核菜单保持英文；旧 nls 参数已废弃。图表标题、系列名和业务数据由应用生成，引擎 locale 按 YEcharts 文档配置。遇到未覆盖的引擎能力，明确限制和隔离/升级方案。

## 标准代码骨架

路线 C 的静态配置在词典初始化完成后再加载：

```typescript
// 引导入口：不能在这里静态导入 App 或业务 constant.ts。
await setAppLocale(getInitialLocale());
const { mountApplication } = await import('./bootstrap');
await mountApplication();
```

```typescript
// 此模块由 bootstrap/懒路由加载，不在语言初始化前导入。
import { t } from '@/locales';
export const columns = [{ field: 'name', title: t('user.name') }];
```

以下为明确要求热切换的组件/页面示例，非旧业务强制模板：


```typescript
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { createColumns, createSchema, createActionConfig } from './constant';

const { t } = useI18n();
const columns = computed(() => createColumns(t));
const schema = computed(() => createSchema(t));
const actions = computed(() => createActionConfig(handlers, t));
```

```typescript
import { getLocaleHeaders } from '@/locales/protocol';

axiosInstance.interceptors.request.use(config => {
  Object.assign(config.headers, getLocaleHeaders());
  return config;
});
```

上述函数以项目已有实现为准，不在业务页复制另一套语言运行时。

## 日期与数字

已有 Day.js 实例不会因为 dayjs.locale() 自动改变，应在展示时调用实例 locale() 或统一 formatDate。语言切换保持原始日期、业务时区、服务器传输格式不变。数字使用统一 formatNumber/Intl.NumberFormat，并显式指定小数位、币种；不得将高精度金额字符串或长整型 ID 转成 Number。货币、百分比和报表周期的业务语义由业务规则决定。

## 交付检查清单

- 运行项目 check:i18n，检查键、占位符、调用、协商、禁用存储、乱序请求、失败重试和卸载取消。
- 运行类型检查、组件回归及构建；模板还需普通、JSP、独立模式验证。
- 原浏览器验证简→繁→英→简；登录页保留输入；系统内确认取消不改状态、确认后重载保留 URL 和登录态；核对菜单/业务请求语言。热切换组件另验输入、校验、分页和 KeepAlive。
- 使用真实 tarball 验证 locale 子路径的 Node exports、类型和浏览器构建；检查语言入口没有静态引入 Monaco/Univer/VXE/Formily。
- 文档 Demo 必须使用真实 API；更新 packages/skills 后同步文档及受控投影，运行 Skills、文档和 LLM 资料一致性检查。
- 记录后端三语内容、第三方插件词典和本次未实测场景。静态缺键为零不代表所有动态键、硬编码文案或业务数据已覆盖。

## 失败兜底策略

缺键回退简体并由静态门禁阻止交付；资源失败保留上一完整语言并允许重试；卸载使在途结果失效。后端展示字段失败保留现有内容，不清理权限或编辑状态。第三方引擎不具备所需能力时明确边界，不能声称重载自动修复第三方翻译缺口。
