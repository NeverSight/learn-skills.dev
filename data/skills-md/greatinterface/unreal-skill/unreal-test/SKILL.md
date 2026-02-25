---
name: unreal-test
description: 用于生成或改写 Unreal Engine CQTest 自动化测试代码。适用于选择测试类型、套用模板/Helper、组织 Latent Actions、整理测试步骤与断言时使用。
---

# Unreal Engine CQTest 测试代码生成

## Skill 定位
用于快速选择测试类型、套用模板与 Helper，并给出 CQTest 结构化写法与 Latent Actions 使用建议。

## 前置准备
- CQTest 模块已添加到项目 Build.cs 的依赖列表中
- 需要时启用 Code Quality Unreal Test Plugin（可选，仅供参考）
- 项目已配置好编译环境
```c#
public class TestsRuntime : ModuleRules
{
	public TestsRuntime(ReadOnlyTargetRules Target) : base(Target)
	{
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"CQTest",
				"CQTestEnhancedInput",
			}
		);
		

		if (Target.bBuildEditor)
		{
			PrivateDependencyModuleNames.AddRange(
				new string[] {
					"EngineSettings",
					"LevelEditor",
					"UnrealEd"
			});
		}
	}
}
```

## 快速选择
- 基础断言 → `TEST`（模板：`basic-test-template.cpp`）
- 结构化测试 → `TEST_CLASS`（模板：`test-class-template.cpp`）
- Actor → `ActorTestHelper`（模板：`actor-test-template.*`）
- Animation → `AnimationTestHelper`（模板：`animation-test-template.*`）
- Input → `InputTestHelper`（模板：`input-test-template.*`）
- Network → `PIENetworkComponent`（模板：`network-test-template.*`）
- Map → `MapTestSpawner`（模板：`map-test-template.cpp`）

## 使用流程
1. 选择测试类型与模板
2. 替换命名空间、类名、测试方法名
3. 填充 BEFORE_EACH/AFTER_EACH 与断言
4. 需要多帧逻辑时引入 Latent Actions
5. 在 Unreal Editor 的 Sessions Frontend 运行测试

## 资源索引
- **CQTest 核心概念**：[references/cqtest-framework.md](references/cqtest-framework.md)
- **测试组件说明**：[references/test-components.md](references/test-components.md)
- **测试类型详解**：[references/test-types.md](references/test-types.md)
- **Latent Actions**：[references/latent-actions.md](references/latent-actions.md)
- **最佳实践**：[references/best-practices.md](references/best-practices.md)
- **模板与 Helper**：见 `assets/templates/` 与 `assets/helpers/`

## 注意事项
- 优先使用 Latent Actions（FWaitUntil）而非固定延时（FWaitDelay）以提高稳定性
- 确保每个测试独立，避免依赖执行顺序
- 使用 AFTER_EACH 正确清理资源，避免泄漏
- 涉及网络或 Blueprint 的测试需指定 `EAutomationTestFlags::EditorContext`
- 测试命名建议：`测试场景_预期行为`
- 使用 `TEST_CLASS` 的 Setup/Teardown 机制减少重复代码
- 测试地图不要放在 `/Maps` 目录，避免被默认烘焙；可放到 `DirectoriesToNevercook` 标记的目录
