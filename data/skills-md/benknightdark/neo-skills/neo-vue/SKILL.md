---
name: neo-vue
description: >
  Use this skill when building, debugging, refactoring, or reviewing Vue 3 applications,
  SFCs, Composition API, Pinia stores, Vue Router, Vite, or Vue+TypeScript code.
  Trigger when the project has *.vue files or the user mentions Vue, Pinia, Composition
  API, Router, reactivity, or component architecture.
license: MIT
compatibility: 支援 Vue 3.x (Composition API), Pinia 2.x, Vue Router 4.x, 以及 Vite 與 TypeScript。
metadata:
  author: Antigravity Team
  version: "1.1.0"
  pattern: tool-wrapper-reviewer
---

# Modern Vue 3 & Pinia 開發專家 (neo-vue)

本技能為 Agent 提供 Vue 3 (Composition API) 與 Pinia 狀態管理的開發與審查指南。它協助產出符合 Vue Style Guide 優先級 A/B 規則的程式碼，避開常見響應式陷阱，並生成一致、強型別的單一檔案元件（SFC）。

## Gotchas
*   **解構 reactive 物件導致響應性丟失**：禁止直接解構 `props` 或由 `reactive()` 定義的物件（例如：`const { name } = props` 或 `const { x } = state`），這會徹底失去 Vue 響應式追蹤！
    *   **防錯機制**：必須使用 `toRefs(props)` 或 `toRef(props, 'name')` 來保持其響應性。
*   **解構 Pinia Store 導致狀態響應性丟失**：直接解構 Pinia store 的 state（如 `const { user } = useAuthStore()`）會使 state 失去雙向響應！
    *   **防錯機制**：必須使用 `storeToRefs(store)` 來解構 state；而 action 則可以直接正常解構。
*   **v-model 手動繁瑣綁定**：在 Vue 3.4 之前，自定義雙向綁定需要手動宣告 `modelValue` 屬性並觸發 `update:modelValue` 事件，容易寫錯。
    *   **防錯機制**：在 Vue 3.4+ 專案中，優先使用 `defineModel()` 巨集宣告雙向綁定，降低屬性與事件不一致的風險。
*   **v-if 與 v-for 在同一節點混用**：在 Vue 3 中，`v-if` 的優先級高於 `v-for`，這意味著 `v-if` 的條件判斷**無法**存取到 `v-for` 迴圈中的變數，會直接導致編譯或執行期報錯！
    *   **防錯機制**：永遠使用 `<template>` 標籤包裹 `v-for`，再於內部子節點使用 `v-if`，或者預先使用 `computed` 計算屬性對陣列進行過濾。

## Workflow Checklist
Progress:
- [ ] 步驟 1：感知專案環境與依賴 (Perceive Setup & Tooling)
- [ ] 步驟 2：載入編碼規範與踩坑指南 (Load Guides & Best Practices)
- [ ] 步驟 3：架構推理與響應式規劃 (Reasoning & Architecture)
- [ ] 步驟 4：套用範本生成一致的程式碼 (Generate SFC & Stores)
- [ ] 步驟 5：程式碼健檢與自我校對 (Code Quality Review)

---

## Detailed Guidelines

### 步驟 1 — 感知專案環境與依賴 (Perceive)
1.  **檢查依賴配置**：讀取 `package.json`，確定 Vue 版本（確認為 Vue 3.x）以及是否安裝了 `pinia`、`vue-router`。
2.  **識別建置工具與語言**：確認是否為 Vite 專案，以及是否啟用了 TypeScript（`lang="ts"`）與 Scoped CSS。

### 步驟 2 — 載入編碼規範與踩坑指南 (Reason)
在進行 Vue 3 開發或審查前，**必須動態載入深度知識庫**：
1.  讀取 `references/coding-style.md` 以確認組件命名（必須為多字詞 PascalCase）、屬性定義等官方優先級規範。
2.  讀取 `references/anti-patterns.md` 以避開 props mutation、computed 副作用等反模式。
3.  讀取 `references/patterns.md` 以獲得 Composables 的合理拆分與 Pinia Setup Stores 的架構設計。

### 步驟 3 — 架構推理與響應式規劃 (Reason)
在編寫程式碼前，先思考以下設計：
1.  **Reactivity 選擇**：除非是多個屬性需要高度關聯的複雜物件，否則**優先使用 `ref()`** 而不是 `reactive()`，以確保存取 `.value` 的一致性並避免解構失活。
2.  **狀態下沉**：評估狀態是屬於組件局部狀態（用 `ref`）還是全局狀態（用 `Pinia Setup Store`）。

### 步驟 4 — 套用範本生成一致的程式碼 (Act)
1.  **SFC 結構**：新建立的元件必須使用 `<script setup>` 語法，並依專案設定優先加入 `lang="ts"`。
2.  **套用範本**：讀取並參考 `assets/Vue3SFCComponentTemplate.vue` 作為標準 Vue 3 元件的排版範例。
3.  **強制語言與風格**：所有程式碼註解、說明必須使用 **Traditional Chinese (Taiwan)**。專用術語需對齊（例如：元件、屬性、狀態管理、響應式、雙向綁定、計算屬性）。

### 步驟 5 — 程式碼健檢與自我校對 (Act)
1.  確認沒有在 `computed` 中做任何 state 修改或 API 調用等 Side Effects。
2.  確認沒有直接對 `props` 進行賦值與修改。
3.  確認 `v-for` 的 `key` 綁定使用了穩定的唯一 ID，而不是陣列索引 `index`。

---

## Output Templates

生成新元件時，依照以下一致結構輸出；更多實作細節請參閱 `assets/Vue3SFCComponentTemplate.vue`：

```vue
<template>
  <div class="vue-expert-component">
    <!-- 模板內容 -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 1. 定義屬性與事件 (Props, Emits, Models)
const props = defineProps<{
  title: string;
}>();

const emit = defineEmits<{
  (e: 'change', value: string): void;
}>();

// Vue 3.4+ 雙向綁定巨集
const modelValue = defineModel<string>();

// 2. 狀態定義 (State)
const count = ref(0);

// 3. 計算屬性 (Computed)
const doubleCount = computed(() => count.value * 2);

// 4. 方法定義 (Methods)
function handleAction() {
  emit('change', 'action-triggered');
}
</script>

<style scoped>
/* 必須使用 scoped 以免全域樣式污染，並優先選用 class 選擇器 */
.vue-expert-component {
  display: flex;
  flex-direction: column;
}
</style>
```
