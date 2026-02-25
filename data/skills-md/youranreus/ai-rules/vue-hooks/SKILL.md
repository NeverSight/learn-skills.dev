---
name: vue-hooks
description: 指导构建 Vue3 组件的 hooks 函数。
---

## 构建Vue3 组件的 hooks 函数

你需要按照如下要求构建一个 Vue3 组件的 hooks 函数

### 1) 入参

hooks 函数的入参应该包含组件的 props 和 emits。例如：

```ts
export function useMyComponent(props: IProps, emits: IEmits) {
  // 组件逻辑
}
```

IProps 和 IEmits 是组件的 props 和 emits 类型定义。应该从 types.ts 文件中引入。

### 2) 文件内容与规范

文件应该按照如下规则与顺序编写：

#### 2.1) 状态定义区

hooks 函数中应该包含组件的状态定义，以及相关的操作行为。避免hooks外部直接对状态进行操作。例如：

```ts
export function useMyComponent(props: IProps, emits: IEmits) {
  const visible = ref(false);
  
  const handleVisibleChange = (value: boolean) => {
    visible.value = value;
  };

  // 业务逻辑
  // ...

  return {
    visible: readonly(visible),
    handleVisibleChange,
  };
}
```

要求：
1. 状态定义区应该在 hooks 函数的顶部。
2. 对于复杂状态的类型，应该使用 TypeScript 类型定义，并提取到 types.ts 文件中。
3. 状态返回值应该是 readonly，避免外部直接修改状态。
4. 状态应该有相对应的操作行为，如果没有的话设置一个简单的set方法即可。

#### 2.2) 业务逻辑区

hooks 函数中应该包含组件的业务逻辑。例如：

```ts
export function useMyComponent(props: IProps, emits: IEmits) {
  const visible = ref(false);
  
  const handleVisibleChange = (value: boolean) => {
    visible.value = value;
  };

  // 业务逻辑
  const handleOpenDialog = () => {
    handleVisibleChange(true);
    // 具体逻辑...
  };

  const onXXX = () => {
    // 具体逻辑...
    emit('xxx');
  }

  return {
    // ...状态定义
    handleOpenDialog,
    onXXX,
  };
}
```

要求：
1. 业务逻辑区应该在状态定义区下方。
2. 业务逻辑中需要操作状态的地方，应该调用相关的操作行为。
3. 业务逻辑中，避免出现与当前状态无相关的函数，如果只是单纯的工具函数，应该提取到 utils.ts 文件中。
4. 相关的业务逻辑应该被集中编写

#### 2.3) 声明周期函数区

如果组件需要在生命周期的某个阶段执行一些逻辑，应该在声明周期函数区中实现，并导出在组件中使用。例如：

```ts
export function useMyComponent(props: IProps, emits: IEmits) {
  // 状态声明
  // ...

  // 业务逻辑
  // ...

  const handleMounted = () => {
    handleInit();
    // 具体逻辑...
  };

  return {
    // ...状态定义
    // ...业务逻辑
    handleMounted,
  };
}
```

要求：
1. 声明周期函数区应该在业务逻辑区下方。
2. 声明周期函数中，应该是对业务逻辑的组合调用，避免在其中进行复杂的逻辑处理。

#### 2.4) hooks的拆分

如果一个 hooks 函数的业务逻辑比较复杂，应该考虑将其拆分成多个 hooks 函数。每个 hooks 函数负责处理一个独立的业务逻辑。例如

```ts
export function useMyComponent(props: IProps, emits: IEmits) {
  const logicA = useMyComponentLogicA(props, emits);
  const logicB = useMyComponentLogicB(props, emits);

  const handleMounted = () => {
    logicA.handleInit();
    logicB.handleInit();
    // 具体逻辑...
  };

  return {
    // 导出逻辑A
    ...logicA,
    // 导出逻辑B
    ...logicB,

    // ... 其余导出
    handleMounted,
  };
}
```

1. 其中每一个 hooks 函数都应该符合以上的要求。
2. hooks统一存放在 `hooks` 目录下。