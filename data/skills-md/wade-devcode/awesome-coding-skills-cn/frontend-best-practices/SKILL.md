---
name: frontend-best-practices
description: 写 React/Vue 前端代码时使用。组件、状态、性能、可访问性的实战规范。
category: frontend
tags: [react, vue, 性能, 可访问性]
---

# 前端最佳实践

## 何时用

- 新建或拆分 React/Vue 组件时，动手前先对照核心规则过一遍。
- 发现某个组件既负责数据请求、又负责渲染逻辑、又管着多层子组件的状态时。
- 遇到页面交互卡顿、控制台出现"re-render 过多"警告，需要排查性能问题时。
- 准备提交包含新组件或重构现有组件的 PR，做最终自查时。

## 核心规则

### 1. 组件单一职责

**规则：** 一个组件只做一件事——要么负责展示，要么负责业务逻辑，要么负责布局；三者不要混在一起。单个组件文件超过 200 行就该警惕，超过 300 行必须拆分。

**为什么：** AI 倾向于把所有逻辑塞进一个"万能组件"：在同一个 `UserDashboard` 里既发接口请求、又做权限判断、又渲染三种不同的卡片、还内联着分页逻辑。这种组件无法独立测试，改一处牵连四处，新成员光是读懂就要半小时。

**怎么做：**
- 拆分时按职责划分：`useUserData`（数据层）、`UserCard`（展示层）、`UserDashboard`（组装层）各司其职。
- 遇到"这个组件到底在做什么"需要超过一句话解释的，就是该拆的信号。
- 展示组件只接收 props、不持有业务状态、不调接口，可以用纯函数组件写。

---

### 2. 状态就近放置

**规则：** 状态只提升到真正需要它的最近公共祖先，不默认丢进全局 store 或顶层组件。

**为什么：** AI 常犯的毛病：把一个弹窗的 `isOpen` 状态放进 Redux/Pinia，然后在四个不相关的地方订阅它；或者把一个表单的草稿数据提升到根组件，导致全页面每次输入都重渲染。全局化看起来"方便统一管理"，实则制造了隐式耦合，状态变更的影响范围变得不可预测。

**怎么做：**
- 先问：「只有这一个组件用这个状态吗？」——是，就放在组件内部。
- 「父子两个组件都用？」——提升到它们的最近公共父组件。
- 只有跨路由、跨页面确实需要共享时，才引入全局状态管理。
- prop drilling 超过两层才考虑 Context/Provide-Inject，不要一遇到跨层就上全局 store。

---

### 3. 避免无谓重渲染

**规则：** 传给子组件的对象和函数必须保持稳定引用；不在渲染函数体内直接创建新对象、新数组或新函数作为 prop 传下去。

**为什么：** AI 生成的代码里最常见的性能坑：在父组件渲染函数里写 `style={{ color: 'red' }}` 或 `onClick={() => handleClick(id)}`。每次父组件重渲染都会生成新的对象/函数引用，即使值没变，子组件（尤其是用 `React.memo` 或 Vue 响应式包裹的）也会被迫重渲染，列表里有几十个子组件时帧率肉眼可见地掉。

**怎么做：**
- React：用 `useMemo` 缓存计算结果和对象字面量，用 `useCallback` 缓存事件处理函数，对纯展示子组件用 `React.memo` 包裹。
- Vue：把衍生数据写成 `computed`，不要在 `<template>` 里内联方法调用返回新对象。
- 性能优化应有性能数据支撑，不要对每个变量无脑加 `useMemo`——有缓存本身也有开销。

---

### 4. 副作用收口

**规则：** 数据请求、事件订阅、定时器等副作用必须放进受控的 effect 中，并在清理函数里正确取消，不允许裸写在组件顶层或渲染路径上。

**为什么：** AI 常见的两类事故：一是在 React `useEffect` 里发请求但忘写 cleanup，组件卸载后请求回来仍然调用 `setState`，控制台报 "Can't perform a React state update on an unmounted component"；二是竞态条件——快速切换 tab 时，后发出的请求先返回，旧请求的结果覆盖了新结果，页面显示错误数据。

**怎么做：**
- React：用 `AbortController` 在 cleanup 里取消 fetch；或使用 `useSWR` / `React Query` 等库，它们内置了竞态处理。
- Vue：在 `onUnmounted` 钩子里清理订阅和定时器；用 `watchEffect` 时利用其返回的 stop 函数。
- 不要在渲染期间（组件函数体内非 hook 区域）直接发请求或修改外部状态。

---

### 5. 可访问性默认开

**规则：** 从一开始就用语义化 HTML 标签、保证键盘可聚焦、在需要的地方加 aria 属性——不把可访问性当事后补丁。

**为什么：** AI 倾向于用 `<div onClick={...}>` 代替 `<button>`，用 `<span>` 做标题，用绝对定位的层叠元素实现"选项卡"但完全没有键盘焦点管理。这类代码视觉上跑通，但屏幕阅读器用户、纯键盘用户完全无法使用，且在政府、医疗、教育等场景下可能面临合规风险。

**怎么做：**
- 可点击的交互元素用 `<button>` 或 `<a>`，不用裸 `<div>`/`<span>` 绑 onClick。
- 图片加有意义的 `alt`；装饰性图片用 `alt=""`。
- 表单每个 `<input>` 都通过 `<label htmlFor>` 或 `aria-label` 关联标签。
- 动态更新的区域（如加载状态、错误提示）加 `aria-live` 属性，让屏幕阅读器能播报变化。
- 用 Tab 键手动过一遍页面流程，确认焦点顺序合理且每个控件都可聚焦。

---

## 正例 / 反例

### React：避免内联对象导致的无谓重渲染

```tsx
// 反例 — 每次 UserList 重渲染，style 和 onSelect 都是全新引用
//         React.memo 形同虚设，UserCard 每次都重渲染
function UserList({ users }: { users: User[] }) {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <ul>
      {users.map((user) => (
        <UserCard
          key={user.id}
          user={user}
          style={{ padding: '8px', borderRadius: '4px' }}   // ❌ 每次渲染都是新对象
          onSelect={() => setSelected(user.id)}              // ❌ 每次渲染都是新函数
        />
      ))}
    </ul>
  );
}
```

```tsx
// 正例 — style 提到组件外，onSelect 用 useCallback 稳定化
//         UserCard 只在 user 数据真正变化时才重渲染
const cardStyle: React.CSSProperties = { padding: '8px', borderRadius: '4px' }; // ✅ 模块级常量，引用稳定

function UserList({ users }: { users: User[] }) {
  const [selected, setSelected] = useState<string | null>(null);

  const handleSelect = useCallback((id: string) => {      // ✅ 依赖不变则引用不变
    setSelected(id);
  }, []);

  return (
    <ul>
      {users.map((user) => (
        <UserCard
          key={user.id}
          user={user}
          style={cardStyle}
          onSelect={handleSelect}
        />
      ))}
    </ul>
  );
}
```

---

### React：副作用清理与竞态处理

```tsx
// 反例 — 没有清理，组件卸载后仍然 setState；快速切换时旧请求覆盖新结果
function UserProfile({ userId }: { userId: string }) {
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)          // ❌ 无 abort，无竞态保护
      .then((res) => res.json())
      .then((data) => setProfile(data));   // ❌ 组件已卸载时仍然执行
  }, [userId]);

  return <div>{profile?.name}</div>;
}
```

```tsx
// 正例 — AbortController 同时解决卸载后 setState 和竞态问题
function UserProfile({ userId }: { userId: string }) {
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    const controller = new AbortController();              // ✅ 每次 effect 创建新的 controller

    fetch(`/api/users/${userId}`, { signal: controller.signal })
      .then((res) => res.json())
      .then((data) => setProfile(data))
      .catch((err) => {
        if (err.name !== 'AbortError') throw err;         // ✅ 正常取消不报错
      });

    return () => controller.abort();                      // ✅ userId 变化或组件卸载时取消请求
  }, [userId]);

  return <div>{profile?.name}</div>;
}
```

---

### Vue：避免在模板中内联计算导致重复执行

```vue
<!-- 反例 — expensiveSort() 在每次渲染时都重新执行，没有缓存 -->
<template>
  <ul>
    <!-- ❌ 方法调用没有缓存，每次响应式更新都重新排序 -->
    <li v-for="item in expensiveSort(items)" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const items = ref<Item[]>([...]);

function expensiveSort(list: Item[]) {   // ❌ 每次渲染都执行，无缓存
  return [...list].sort((a, b) => a.score - b.score);
}
</script>
```

```vue
<!-- 正例 — 用 computed 缓存，只有 items 真正变化时才重新计算 -->
<template>
  <ul>
    <!-- ✅ sortedItems 是 computed，引用稳定，有缓存 -->
    <li v-for="item in sortedItems" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const items = ref<Item[]>([...]);

const sortedItems = computed(() =>          // ✅ 依赖 items 变化时才重新计算
  [...items.value].sort((a, b) => a.score - b.score)
);
</script>
```

---

### Vue：可访问性——交互元素语义化

```vue
<!-- 反例 — 用 div 模拟按钮，键盘无法聚焦，屏幕阅读器无法识别 -->
<template>
  <div class="btn-primary" @click="handleSubmit">  <!-- ❌ div 不可键盘聚焦，无 role -->
    提交
  </div>
</template>
```

```vue
<!-- 正例 — 使用语义化 button，天然支持键盘、焦点、屏幕阅读器 -->
<template>
  <button
    type="button"
    class="btn-primary"
    :disabled="isSubmitting"
    :aria-busy="isSubmitting"                <!-- ✅ 提交中时告知辅助技术 -->
    @click="handleSubmit"
  >
    {{ isSubmitting ? '提交中…' : '提交' }}
  </button>
</template>
```

---

## 自查清单

- [ ] 每个组件只做一件事，能用一句话说清楚它的职责；超过 300 行的已拆分。
- [ ] 所有状态都放在需要它的最近公共祖先，没有把局部状态无谓提升到全局 store。
- [ ] 传给子组件的对象字面量和函数均已用 `useMemo`/`useCallback`（React）或 `computed`（Vue）稳定化，没有在渲染函数里内联创建。
- [ ] 每个 `useEffect` / `watchEffect` 都有对应的清理逻辑（取消请求、清除订阅、清除定时器）。
- [ ] 所有可点击交互元素使用 `<button>` 或 `<a>`，没有用裸 `<div>`/`<span>` 绑 onClick。
- [ ] 表单 `<input>` 都通过 `<label>` 或 `aria-label` 关联了文字说明；图片有合适的 `alt`。
- [ ] 用 Tab 键手动走过一遍主要交互流程，焦点顺序正常，每个控件均可聚焦操作。
