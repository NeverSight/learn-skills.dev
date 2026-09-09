---
name: upgrade-scenic-project-deps
description: 根据 one-travel-gz 子应用 scenic tickets 项目的依赖升级规范，自动为同类 Vue + Vite + pnpm monorepo 项目升级 @foundbyte/eslint-plugin、@keyblade/vite-plugin-vue-pro，新增 eslint-plugin-unicorn、eslint-plugin-perfectionist（import 排序）与 unplugin-version-injector，并同步 ESLint / Stylelint / Vite / VS Code / Dockerfile 配置。
---

#  scenic tickets 项目依赖升级规范

本 skill 用于将当前项目的依赖与配置同步到 `one-travel-gz/man-subapp-scenictickets` 在 commit `b25e2597`（升级版本）时的状态。
适用项目特征：pnpm workspace、Vue 3 + Vite、使用 `@foundbyte/eslint-plugin` / `@keyblade/vite-plugin-vue-pro` / `@keyblade/works-ui-plugin` 的 PC/小程序混合子应用。

## 何时使用

当用户要求：
- "升级依赖版本"
- "同步 scenic tickets 的依赖"
- "添加版本号自动注入"
- "升级 eslint / stylelint 配置"
- "让这个项目和 man-subapp-scenictickets 保持一致"

## 升级清单

执行前先读取当前项目的 `package.json`、`web/package.json`（或对应子包）、`eslint.config.ts`、`web/vite.config.ts`、`.vscode/settings.json`、`Dockerfile`、`.stylelintrc.cjs`、`.stylelintignore`，确认项目结构相似后再执行。

### 1. 根目录 package.json

将 `@foundbyte/eslint-plugin` 升级到最新可用 alpha：

```json
"@foundbyte/eslint-plugin": "^1.1.5-alpha.1"
```

在 `devDependencies` 中新增：

```json
"eslint-plugin-unicorn": "^63.0.0",
"eslint-plugin-perfectionist": "^4.15.1"
```

同时新增 Stylelint 相关依赖（注意版本需与当前项目保持一致）：

```json
"stylelint": "^15.11.0",
"stylelint-config-html": "^1.1.0",
"stylelint-config-standard-less": "^2.0.0"
```

如果根目录原本没有 `pnpm.overrides`，按如下格式追加（修正 JSON 结构，确保 `dependencies` 后紧跟 `, "pnpm": {}`）：

```json
"pnpm": {
  "overrides": {
    "@arco-design/web-vue": "2.58.0-beta.1"
  }
}
```

### 2. web/package.json

升级：

```json
"@keyblade/vite-plugin-vue-pro": "^1.0.15"
```

新增：

```json
"unplugin-version-injector": "^2.1.1"
```

### 3. 新增 Stylelint 配置

在根目录创建 `.stylelintignore`：

```text
node_modules
sub_modules
dist
*.min.css
*.min.scss
```

在根目录创建 `.stylelintrc.cjs`，内容以 `stylelint-config-standard-less` 为基础，并针对 Vue / UniApp / Less 做兼容配置。关键规则如下：

```js
module.exports = {
  extends: ['stylelint-config-standard-less'],
  overrides: [
    {
      files: ['*.vue', '**/*.vue'],
      extends: ['stylelint-config-html'],
      rules: {
        'selector-pseudo-class-no-unknown': [true, { ignorePseudoClasses: ['deep', 'global', 'slotted'] }],
        'selector-pseudo-element-no-unknown': [true, { ignorePseudoElements: ['v-deep', 'v-global', 'v-slotted'] }],
        'function-no-unknown': [true, { ignoreFunctions: ['v-bind'] }],
      },
    },
  ],
  rules: {
    'color-function-notation': null,
    'alpha-value-notation': null,
    'unit-no-unknown': [true, { ignoreUnits: ['rpx'] }],
    'selector-pseudo-class-no-unknown': [true, { ignorePseudoClasses: ['deep', 'global'] }],
    'selector-pseudo-element-no-unknown': [true, {
      ignorePseudoElements: [
        'scrollbar', 'scrollbar-thumb', 'scrollbar-track',
        '-webkit-scrollbar', '-webkit-scrollbar-thumb', '-webkit-scrollbar-track',
      ],
    }],
    'selector-class-pattern': null,
    'selector-id-pattern': null,
    'import-notation': null,
    'no-empty-source': null,
    'no-duplicate-selectors': null,
    'no-descending-specificity': null,
    'block-no-empty': null,
    'property-no-unknown': [true, { ignoreProperties: ['overflow-scrolling'] }],
    'selector-type-no-unknown': [true, { ignoreTypes: ['page'] }],
    'font-family-no-missing-generic-family-keyword': null,
    'font-family-name-quotes': null,
    'indentation': 2,
    'no-eol-whitespace': true,
    'no-missing-end-of-source-newline': true,
    'string-quotes': 'single',
    'number-leading-zero': 'always',
    'declaration-block-trailing-semicolon': 'always',
    'block-opening-brace-space-before': 'always',
    'block-opening-brace-newline-after': 'always',
    'block-closing-brace-newline-before': 'always',
    'block-closing-brace-newline-after': 'always',
    'declaration-colon-space-after': 'always',
    'declaration-colon-space-before': 'never',
    'function-comma-space-after': 'always-single-line',
    'function-comma-space-before': 'never',
    'selector-list-comma-newline-after': 'always',
  },
}
```

Stylelint 相关依赖必须安装到根目录 `devDependencies` 中：

```json
"stylelint": "^15.11.0",
"stylelint-config-html": "^1.1.0",
"stylelint-config-standard-less": "^2.0.0"
```

> 版本说明：`stylelint@15` 仍然保留部分已废弃的 stylistic 规则（如 `indentation`、`string-quotes` 等），所以本项目统一使用 15.x，不要直接升级到 16.x，否则上述规则会失效。

### 4. 更新 eslint.config.ts

- 将 `import path from 'node:path'` 移到文件顶部。
- 引入 `eslint-plugin-unicorn`：

```ts
import eslintPluginUnicorn from 'eslint-plugin-unicorn'
```

- 引入 `eslint-plugin-perfectionist`：

```ts
import pluginPerfectionist from 'eslint-plugin-perfectionist'
```

- 在 plugins 中注册：

```ts
plugins: {
  '@stylistic': pluginStylistic,
  '@foundbyte': pluginFoundByte,
  'unicorn': eslintPluginUnicorn,
  'perfectionist': pluginPerfectionist,
},
```

- 在 `globalIgnores` 中新增 `.agents/**`：

```ts
globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**', 'scripts/**', '.agents/**'])
```

- 删除 `@vue/eslint-config-prettier/skip-formatting` 相关注释/导入。
- 调整 `max-lines` 为更宽松的策略：

```ts
'max-lines': ['error', { max: 600, skipBlankLines: true, skipComments: true }]
```

- 新增 unicorn 文件名规范：

```ts
'unicorn/filename-case': ['error', { case: 'kebabCase', ignore: ['App.vue'] }]
```

- 新增 @foundbyte 插件规则：

```ts
'@foundbyte/require-json-parse-type': ['error', { declarationTypes: ['const', 'let'] }],
'@foundbyte/no-restricted-literal-types': ['error', { forbidden: ['null', 'undefined', ''], allowInUnions: true }],
```

- 关闭显式 any：

```ts
'@typescript-eslint/no-explicit-any': 'off'
```

- 新增 import 排序规则（`perfectionist/sort-imports`）：第三方/@别名/~/ → 相对路径(层级少在前) → 类型 → 最后 .vue 组件：

```ts
'perfectionist/sort-imports': [
  'error',
  {
    type: 'natural',
    order: 'asc',
    groups: [
      'external', // 第三方包
      'internal', // @/、~/ 开头的别名路径
      'sibling', // ./ 当前目录（层级最少）
      'index', // ./index
      'parent-1', // ../ 一层
      'parent-2', // ../../ 两层
      'parent-3', // ../../../ 三层
      'parent-4', // ../../../../ 四层
      'parent', // 更深的 ../（兜底）
      'type', // import type 类型导入
      { newlinesBetween: 'always' },
      'vue-component', // .vue 后缀的组件
    ],
    customGroups: [
      {
        // 放最前面优先匹配：所有 .vue 引用都进 vue-component 组，不参与路径分组
        groupName: 'vue-component',
        elementNamePattern: '.*\\.vue$',
      },
      // 类型引用(import type)优先匹配 type 组，这里用 customGroup 把它们也按路径深度归组
      { groupName: 'sibling', elementNamePattern: '^\\./' },
      { groupName: 'parent-1', elementNamePattern: '^\\.\\./(?!\\.)' },
      { groupName: 'parent-2', elementNamePattern: '^\\.\\./\\.\\./(?!\\.)' },
      { groupName: 'parent-3', elementNamePattern: '^(\\.\\./){3}(?!\\.)' },
      { groupName: 'parent-4', elementNamePattern: '^(\\.\\./){4}(?!\\.)' },
    ],
    internalPattern: ['^@/', '^~/'],
    newlinesBetween: 'never',
  },
],
```

### 5. 更新 web/vite.config.ts

引入插件：

```ts
import versionInjector from 'unplugin-version-injector/vite'
```

为 `KeybladeVitePluginVuePro` 增加 `logPageRoute` 配置：

```ts
KeybladeVitePluginVuePro({
  logPageRoute: { basePath: 'src/views', outputPrefix: 'web' },
})
```

在 plugins 数组中加入版本注入插件：

```ts
versionInjector({
  formatDate: (date: Date) => {
    return date.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })
  },
})
```

### 6. 更新 .vscode/settings.json

- 在 `explorer.fileNesting.patterns.package.json` 值末尾追加 `.stylelintignore, .stylelintrc.cjs`。
- 将 `editor.defaultFormatter` 改为 `esbenp.prettier-vscode`，但保留 `[vue]` 使用 `dbaeumer.vscode-eslint`。
- 新增 stylelint 校验范围并关闭 VS Code 内置 CSS 校验：

```json
"stylelint.validate": ["less", "vue"],
"css.validate": false,
"less.validate": false,
"scss.validate": false
```

- 在 `editor.codeActionsOnSave` 中增加：

```json
"source.fixAll.stylelint": "explicit"
```

- 删除 `[less]` 中 `editor.defaultFormatter` 的 Prettier 覆盖（现在由顶层 defaultFormatter 统一处理）。
- 可选追加 Windows 终端默认 Git Bash：

```json
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

### 7. 更新 Dockerfile

在 `WORKDIR /app` 之后、安装 pnpm 之前新增：

```dockerfile
RUN apk add --no-cache curl
```

说明：`@foundbyte/security-monitor-usage` 依赖通过 curl 获取外网 IP。

### 8. 同步 pnpm-lock.yaml

修改完 package.json 后，运行：

```bash
pnpm install --no-frozen-lockfile
```

确保 lock 文件反映新的依赖树。

## 验证步骤

完成升级后执行：

```bash
# 1. 检查依赖安装
pnpm install

# 2. 检查 ESLint 配置加载
pnpm eslint --config eslint.config.ts .

# 3. 检查 Stylelint 配置加载
pnpm stylelint --config .stylelintrc.cjs "web/src/**/*.{vue,less,css}"

# 4. 检查开发构建是否通过
pnpm -C web dev

# 5. 检查版本注入是否生效（打开页面控制台查看 __version__ / buildInfo）
```

## 常见风险

1. `@foundbyte/eslint-plugin` 的新规则 `@foundbyte/require-json-parse-type` 和 `@foundbyte/no-restricted-literal-types` 可能在现有代码中引发大量 error，升级后需要按项目实际情况逐步修复或临时关闭。
2. `eslint-plugin-unicorn` 的 `filename-case` 规则会强制文件名使用 kebab-case，如果项目存在大量 camelCase / PascalCase 文件，需要批量重命名或在规则中增加 `ignore` 项。
3. Stylelint 新增后，保存时可能会对历史 Vue/Less 文件进行大量格式化改动，建议先全量跑一次 `pnpm stylelint --fix` 再提交。
4. `perfectionist/sort-imports` 会对所有文件的 import 顺序做强制重排（含自动 fix），升级后需要全量执行 `pnpm eslint --fix`，并人工检查被移动的 import 是否引入副作用顺序问题（项目内 import 均为无副作用的纯导入时安全）。
5. `@keyblade/vite-plugin-vue-pro` 从 1.0.10 升级到 1.0.15 会附带 `@foundbyte/security-monitor-usage@1.0.7-alpha.0`，构建时需要外网 curl，因此 Dockerfile 必须同步安装 curl。

## 备注

本 skill 对应原项目 commit `b25e2597`（作者：tianmi，2026-08-31）。后续若目标项目继续升级，应以目标项目的最新提交为准。

历史同步记录：
- `ff33ad1`（2026-08-26）：新增 `@foundbyte/no-restricted-literal-types` 规则，`@foundbyte/eslint-plugin` 升级至 `^1.1.5-alpha.1`。
- `213ec73`（2026-09-09）：新增 `eslint-plugin-perfectionist@^4.15.1` 及 `perfectionist/sort-imports` import 排序规则。

在目标项目中执行时，若结构不同（如无 `web/` 子包、非 Vue 项目、使用 npm/yarn），应仅抽取适用的子集，不要机械照搬。
