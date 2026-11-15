---
name: portal-app-init
description: 用 ODC DSL 为目标 Portal App 仓库增补或合并 AGENTS.md 中的门户约定，缺文件时创建。覆盖技能索引、共享 onebox、私有 npm、前端验收与 API/性能规则；不创建或维护 PRODUCT.md、DESIGN.md。
---

# Portal App Init

只维护目标 App 仓库的 `AGENTS.md`。读取[门户约定素材](assets/portal-conventions.md)，按语义补缺、合并，不整份覆盖。产品与设计文档交给其他工具。

**本文 `formal` 代码围栏中的内容是以 DSL 形式编写的执行指令，必须按各条规则的义务强度、适用条件与明确例外遵循。`formal` 代码围栏仅用于排版，不表示这些指令是示例或可选参考。**

```formal
RULE @target_scope:
  MUST: [user_supplied_target_first, default_current_app_repository,
         "完整读取目标 AGENTS.md、适用的上级及嵌套规则与相关引用，确认实际作用域。",
         "从现有 manifest、README、配置确认 Portal App 形态；用户已说明接入目标时，不以缺 manifest 阻止补约定。"]
  MUST_NOT: [skill_installation_directory_as_implicit_target,
             create_or_modify_product_or_design_documents,
             create_or_mirror_claude_md, unrelated_configuration_changes,
             initialize_onebox_or_install_packages_or_publish]

RULE @dsl_composition:
  MUST: ["读取当前安装的 use-prompt-dsl 及其语言规范，按 compose 编写直接嵌入的 RULE 片段。",
         preserve_obligation_strength_conditions_exceptions_and_scope,
         brief_syntax_explanation_in_target,
         "目标首个 formal 围栏前保留本 skill 的围栏外执行声明；已有等义声明则合并，语言随目标。"]
  PREFER: self_descriptive_literals
  MUST_NOT: [outer_wrappers, forced_ontology_or_workflow_blocks,
             cryptic_abbreviations, require_dsl_reload_for_ordinary_coding]
  ON_UNMET: ["缺 use-prompt-dsl 时说明缺失并建议安装，暂停 DSL 写入，不自动安装。"]

RULE @merge:
  MUST: [read_portal_conventions_material,
         create_agents_md_when_missing,
         "已有 AGENTS.md 时逐项比较语义：保留有效规则，原位合并重复项，只补缺失约定。",
         preserve_project_facts_commands_and_local_exceptions,
         "仅将本次新增或合并的 Portal 约定写成 ODC，不借机重写无关编码原则。",
         "实质冲突按当前用户指令与适用范围处理；无法判定时只询问冲突项，继续无冲突部分。"]
  MUST_NOT: [skip_existing_agents_md, wholesale_replacement,
             duplicate_covered_rules, infer_facts_from_missing_files,
             rewrite_complete_target_for_diff]

RULE @applicability:
  MUST: [include_six_skill_index,
         "带前端的项目合并前端规则；确定无前端的 service 不加 UI 规则，形态未知则保留有前端时的条件。",
         "API、SQL、Redis、worker 规则保留各自适用条件，不为纯前端项目引入后端任务。",
         "私有 npm 访问直接指向 xgent-app-release 的 references/private-npm.md，无需加载整个发布 skill。"]
  MUST_NOT: [copy_portal_monorepo_source_paths,
             inject_initialization_workflow_into_target,
             require_missing_product_or_design_documents]

RULE @references:
  MUST: ["按目标环境实际安装位置生成可用链接；仓内 skill 用相对路径，仓外可用技能名加相对该 skill 的资源路径。",
         "素材中相对链接以素材自身为基准，写入目标时必须重新定位。",
         "目标环境缺相关 skill 时保留用途索引并报告缺失、提示安装；不伪造路径或声称已使用。"]
  MUST_NOT: [assume_author_machine_paths, load_all_indexed_skills,
             automatic_skill_installation]

RULE @verification:
  MUST: [recheck_target_before_write, preserve_concurrent_edits,
         reread_result_and_diff,
         "逐项核对素材覆盖、条件、强度、重复与冲突，以及实际路径和引用是否可用。",
         "确认 PRODUCT.md、DESIGN.md 及无关文件未改，完整目标再次使用本 skill 不应产生重复内容。"]
  MUST_NOT: [static_text_regression_tests, unrelated_builds_or_runtime_checks]

RULE @delivery:
  MUST: [report_created_merged_added_or_unchanged_content,
         disclose_unresolved_conflicts_missing_skills_and_unverified_items]
```
