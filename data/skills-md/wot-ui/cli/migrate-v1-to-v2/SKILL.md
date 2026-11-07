---
name: migrate-v1-to-v2
description: 将用户项目从 Wot UI v1 迁移到 v2。用户要求升级 wot-design-uni 到 @wot-ui/ui、替换旧组件/旧 API、迁移表单校验体系、迁移图标名称，或修复因 v2 不兼容变更导致的编译错误、空图标和运行时报错时调用。
---

# 从 v1 迁移到 v2 技能

本技能用于辅助用户将项目从 `Wot UI v1` (`wot-design-uni`) 迁移到 `Wot UI v2` (`@wot-ui/ui`)。

完整迁移指南：[中文](https://wot-ui.cn/guide/migration-v2.html) / [English](https://wot-ui.cn/en-US/guide/migration-v2.html)。

---

## 职责边界

- 扫描 v1 用法、替换包名/路径、迁移组件 API、迁移表单校验体系与内置图标名称、修复不兼容变更。
- **不负责**新建业务页面或重构业务逻辑，仅做最小必要的兼容性替换。
- **不负责**安装依赖，由用户自行在终端执行。

---

## 首次交互确认

在开始任何操作前，先向用户确认以下三点（如果上下文已可推断则跳过对应问题）：

1. **安装方式**：npm 还是 uni_modules？（影响导入路径和 easycom 配置）
2. **目标**：
   - A. **全量迁移**（项目尚未升级）→ 按阶段一～七执行
   - B. **升级后修错误**（已升级但遇到编译/运行时报错）→ 先读 `errors.md` 定位问题
3. **目标平台**：H5 / 微信小程序 / 支付宝小程序？（影响样式隔离和 easycom 验证方式）

---

## 快速通道

根据用户描述的问题，直接加载对应子文件：

| 关键词 | 子文件 |
| --- | --- |
| 错误信息 / 编译报错 / 找不到模块 / is not defined / 升级后异常 | `errors.md` |
| 表单 / Form / schema / zodAdapter / FormRules / 校验 / 必填星号 | `form.md` |
| 包名 / easycom / Volar / vite 插件 / 国际化 / 路径替换 / uni_modules | `infra.md` |
| Sass / 主题 / Design Token / CSS 变量 / 样式覆盖 / 深色模式 / ConfigProvider | `styles.md` |
| Dialog / MessageBox / Empty / StatusTip / Cascader / ColPicker / Keyboard / NumberKeyboard / Button / Tag / Radio / Checkbox / Search / Grid / Fab / Badge / Slider / Tabs / Steps / Swiper / Tooltip / Popover / Collapse / Cell / Input / Textarea / PickerView / ImgCropper / CountTo / Segmented | `components.md` |
| Icon / 图标 / wd-icon / icon / iconClass / activeIcon / inactiveIcon / prefixIcon / suffixIcon / 空图标 | `components.md` 的“图标迁移”与 `icons.json` |

---

## 核心变更速查表

| 类型 | v1 | v2 |
| --- | --- | --- |
| npm 包名 | `wot-design-uni` | `@wot-ui/ui` |
| uni_modules 目录 | `wot-design-uni` | `wot-ui` |
| 弹框组件 | `wd-message-box` | `wd-dialog` |
| 弹框 Hook | `useMessage` | `useDialog` |
| 缺省提示 | `wd-status-tip` | `wd-empty` |
| 多列选择器 | `wd-col-picker` | `wd-cascader` |
| 数字键盘 | `wd-number-keyboard` | `wd-keyboard` |
| 表单校验 | `rules` / `FormRules` | `schema` / `FormSchema` |
| 按钮变体 | `plain` / `type="text"` / `type="icon"` | `variant` / 图标按钮 |
| 按钮危险色 | `type="error"` | `type="danger"` |
| 标签变体 | `plain` | `variant="plain"` |
| 单选/复选形态 | `shape` / `inline` / `cell` | `type` / `direction` / 手动组合 `wd-cell` |
| 搜索框浅色样式 | `light` | `variant="light"` |
| GridItem 点击 | `@itemclick` | `@click` |
| 工具函数路径 | `components/common/util` | `common/util` |
| 内置图标名称 | v1 图标集合 | 按 `icons.json` 中的人工审核结果迁移 |

---

## 迁移流程

推荐顺序：依赖升级 → 路径替换 → Form 页面 → 高影响组件 → 中低影响组件 → 图标与低影响属性 → 样式与主题 → 回归测试。

每完成一个阶段后与用户确认再进入下一阶段。

### 阶段一：扫描与诊断

1. 确定用户的安装方式（`npm` 还是 `uni_modules`）。
2. 确认项目配置：`pages.json` easycom、`tsconfig.json` 类型声明、Vite 插件自动导入。
3. 搜索 v1 旧用法：

   ```bash
   rg "wot-design-uni|wd-message-box|useMessage|wd-status-tip|wd-col-picker|wd-number-keyboard|wd-icon|icon-class|iconClass|active-icon|activeIcon|inactive-icon|inactiveIcon|prefix-icon|prefixIcon|suffix-icon|suffixIcon|@itemclick|shape=|inline|\scell\b|\slight\b|type=\"error\"|type=\"icon\"|type=\"text\"|\splain\b|classPrefix|components/common/util|hide-label|hide-min-max|autoLineWidth|disabled-color|setRoate|useContentSlot|useMoreSlot|\bshow="
   ```

4. 如果项目有表单，额外搜索：

   ```bash
   rg "wd-form|FormRules|:rules=|rules=|errorType|resetOnChange"
   ```

5. 向用户汇报发现的清单，按影响程度排序：
   - **高影响**：Form（结构+校验体系）、Dialog（原 MessageBox）、ColPicker、NumberKeyboard
   - **中影响**：Button、Tag、Radio/Checkbox、Search、Grid、Fab、内置图标名称
   - **低影响**：camelCase 属性名、Badge/Slider/Tabs/Steps/Swiper 等属性微调

### 阶段二：依赖与路径替换

详见 `infra.md`（包名、easycom、Volar、Vite 插件、国际化）和 `styles.md`（Sass 升级）。读完后回到**阶段三**继续。

### 阶段三：高影响组件迁移

详见 `components.md`（MessageBox→Dialog、StatusTip→Empty、ColPicker→Cascader、NumberKeyboard→Keyboard）。

Form 表单体系详见 `form.md`。读完后回到**阶段四**继续。

### 阶段四：中影响组件迁移

详见 `components.md`（Button、Tag、Radio/Checkbox、Search、Grid、Fab）。读完后回到**阶段五**继续。

### 阶段五：低影响属性与图标迁移

详见 `components.md`（Badge、Slider、Tabs、Steps、Swiper、Tooltip、Popover、Collapse、DatetimePickerView、ImgCropper、CountTo、Segmented、PickerView、图标迁移、camelCase 属性名）。迁移图标时必须读取 `icons.json`，只替换确认映射；“无对应”和动态绑定项保留给人工决策。读完后回到**阶段六**继续。

### 阶段六：样式与主题迁移

详见 `styles.md`（主题文件引入、全局变量覆盖、ConfigProvider、样式覆盖优先级、深色模式）。读完后进入**阶段七**回归验证。

### 阶段七：回归验证

- [ ] H5 和目标小程序端是否能正常编译
- [ ] `easycom` 是否能正确解析所有 `wd-*` 组件
- [ ] `Toast`、`Dialog`、`Notify` 等函数式调用是否已在页面中声明实例
- [ ] 表单提交、单字段校验、重置、隐藏字段和异步校验是否正常
- [ ] 选择器类表单项的回显文本和提交值是否正确
- [ ] `Button` 的 `type`、`variant`、`round` 和高度是否符合预期
- [ ] `Tag` 的 `variant` 是否已从 `plain` 迁移
- [ ] `Radio`/`Checkbox` 的 `shape`、`inline`、`cell` 是否已迁移
- [ ] `Search` 的 `light` 是否已迁移为 `variant="light"`
- [ ] `GridItem` 点击事件是否已从 `itemclick` 迁移到 `click`
- [ ] `Cell`、`Input`、`Textarea` 的表单相关属性是否已迁移到 `wd-form-item`
- [ ] `PickerView`、`ImgCropper`、`CountTo` 等实例方法是否仍可正常调用
- [ ] `Badge`、`Slider`、`Tabs`、`Steps`、`Swiper` 等旧属性是否已迁移
- [ ] `Dialog` 点击遮罩关闭、Prompt 返回值和按钮配置是否符合预期
- [ ] 深色模式、主题变量、品牌色覆盖是否生效
- [ ] 弹层在小程序端是否存在样式隔离问题
- [ ] 自定义覆盖样式是否仍然生效
- [ ] 所有静态内置图标名是否按 `icons.json` 处理，且没有对业务字符串做全局替换
- [ ] “无对应”、动态绑定和 `iconClass` / `activeIcon` / `inactiveIcon` / `prefixIcon` / `suffixIcon` 是否已经单独列出并人工确认
- [ ] 图标的业务语义和视觉结果是否正确，名称大小写是否保持准确
- [ ] 图标按钮高度变化是否影响页面布局
