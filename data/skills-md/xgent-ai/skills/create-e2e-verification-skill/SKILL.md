---
name: create-e2e-verification-skill
description: "用于为用户选定的旅程创建、维护 e2e-* 端到端验证 skill，或把验收命令固化成可复跑验证；不用于一次性验收、只写测试计划或只读咨询。未指定时提名候选，从真实入口运行并证明能发现故障。"
when_to_use: "用户会说「做个端到端验证 skill」「给这个应用做个验证 skill」「把验收命令固化成可复跑的验证」「这条用户路径最容易出事，固化成 E2E」「测试全过用户还是用不了，补真实验证」时。"
---

# Create E2E Verification Skill

局部测试检查写的人想到的局部情况，E2E 检查用户到底能不能做成事。本 skill 从真实入口验证用户选定的旅程，用户没指定时提名出事代价高、现有测试又碰不到的候选，并留下一份 `e2e-<area>` 项目 skill，让下一位 agent 能用它检查自己的改动。支持 Web、CLI/TUI、服务、桌面、移动端和库，具体工具由仓库与当前环境决定。

生成结果按 [模板](references/e2e-skill-template.md) 用 Odyssey（ODC）写，读者是中途接手、没见过本次工作的 agent；用户不懂模型语言也要能信任并使用结果。生成或实质修改后读 [生成结果验收](references/validate-generated-skill.md)，维护本生成器时读 [行为验收场景](evals/scenarios.md)。

```formal
INTENT:
  GOAL: generate_project_local_e2e_skill_for_selected_user_journeys
  SUCCESS: [existing_coverage_checked_against_commits,
            generated_skill_catches_a_real_break_from_real_entry,
            findings_reported_in_user_terms, scope_and_gaps_stated]
  NON_GOALS: [full_test_matrix, product_fixes_unless_requested, new_test_framework,
              global_tool_installation, release]

RULE @boundary:
  MUST: ["输出位置按 用户指定 → 项目明确采用的 skill 目录 → .agents/skills/e2e-<area>/，名称与目录一致且以 e2e- 开头",
         "维护已有 e2e-* 时原位修改，保留人工内容、调用策略与稳定 ID；已有测试 harness 能驱动时复用，不复制第二套启动与清理",
         "用户选几条写几条：同一 area 的旅程放进同一个 e2e-<area>，各场景可单独选择；不同 area 分开",
         "启动受阻先诊断；已授权范围内修复可直接继续，否则留下具体阻塞和恢复步骤"]
  MUST_NOT: ["只因请求含‘验证’就落盘：解释、测试规划与一次性验收走各自流程",
             "在生成文件留下对本生成器或未安装 skill 的隐式依赖"]

RULE @target_selection:
  MUST: ["用户点名旅程、区域或缺陷时从那里开始，不另换目标；只问观察不到的",
         "好目标是产品对用户的一项承诺：失败时伤害用户，现有测试又碰不到让它失败的情形",
         "优先看测试到不了的层：打包安装后的入口、跨进程、持久化与重启、权限、失败提示、按公开文档首次上手",
         =>["用户没点名", "从需求、文档、事故、近期修复、经验记录和现有测试取事实，提名 2–4 个候选由用户选择，每个写明出事代价、现有测试为什么碰不到和覆盖状态；真实候选不足时如实列出，不凑数"],
         =>["用户没点名且无人可问（如自主执行）", "选代价最高的一条，说明理由并列出其余候选"]]
  MUST_NOT: rank_easier_journey_above_costlier_one

RULE @existing_coverage:
  WHEN: before_nominating_or_starting_a_journey
  MUST: ["先读项目所有 e2e-*，按规则、场景和 COVERAGE 判断候选是否已覆盖，不按名字判断",
         "已覆盖时先沿场景入口核对 COVERAGE 是否漏了实际调用的文件，漏列的一并核查，需要更新 skill 时补全",
         "再按场景查 SYNC_COMMIT..HEAD 与未提交改动中涉及这些路径和判据来源文档的部分，读改动内容后判定",
         =>["没有对应的 e2e-*", "未覆盖：新建"],
         =>["无改动，或改动确认不影响场景", "仍有效：不重复生成，报告最后确认的提交；本轮状态记 not-run，不算通过"],
         =>["改动影响场景", "过期：按 @maintenance 原位更新，不新建"],
         =>["SYNC_COMMIT 缺失或不可达", "无法证明有效：按过期处理，重核该 skill 的全部场景"],
         =>["提名依据（事故、近期修复）晚于 SYNC_COMMIT 且不在覆盖路径内", "COVERAGE 可能漏文件：按过期核查，并补全 COVERAGE"],
         "未覆盖与过期的候选一起按代价排序，不额外加权；仍有效的不参与排序"]
  MUST_NOT: ["只凭已有 e2e-* 就认定不必做", "未核查提交就新建第二份"]

RULE @repository_facts:
  MUST: ["先读仓库规则、启动文档、包脚本、现有测试和相关入口，再做最小运行确认；能观察到的事实不交给用户填写",
         "确认用户入口：用户实际操作的页面、命令、API、设备界面或公开库接口，多个表面分别登记",
         "确认启动与就绪：工作目录、依赖、构建/启动命令、端口、配置、测试账号/数据及可观察的就绪条件",
         "确认驱动方式：优先复用现有 Playwright/Cypress、PTY、HTTP 客户端、设备自动化或公开 API 的最小消费者",
         "确认隔离与归属：如何分配独立端口、数据目录、浏览器 profile、账号和进程；无法隔离时限制串行并说明实例归属"]
  MUST_NOT: [readme_commands_as_verified_facts, invented_selectors_parameters_or_responses]

RULE @expected_behavior_source:
  MUST: "每条规则和判据指向已读的需求、公开契约或用户明确要求；没有权威预期时标待确认，只保存观察配方"
  MUST_NOT: ["以当前输出生成预期，让缺陷自证正确", "把源码阅读写成运行通过"]

RULE @journey_model:
  WHEN: journey_has_waiting_retry_cancel_recovery_multiple_entries_or_order_sensitive_steps
  MUST: ["读取已安装 phoenix-diagram skill 的 statechart 说明并按其流程检查模型；从中取得当前命令与字段",
         "变量写用户能观察或在意的状态，动作写用户操作与系统事件，规则写成用户认同的一句话承诺",
         "同一模型同时写成生成 skill 里的 ONTOLOGY / TRANSITION / REQUIREMENT，同名 ID 一一对应（对应表见模板）",
         "每个状态和动作指向可打开的代码或文档；代码里一步完成的事，模型也算一步",
         "先用最粗的 view 取得规则判定：一个用户状态一个标签，变量值不写进标签，规则 id 取短；回执没有规则判定时继续收粗 view，已有完整规则判定时布局诊断不影响结论",
         "用户要看图、或判定需要人裁决时，再细化 view 并按 phoenix-diagram 的完整交付流程出图"]
  MUST_NOT: ["为让检查通过放宽规则或删掉变量",
             "把 phoenix-diagram 的命令、选项或路径复制进生成 skill 或脚本；它们随版本变化，只按名称引用",
             "把 ODC 声明本身当成已验证的结果"]
  # 直线旅程没有这些情形，跳过模型，直接写场景。

RULE @statechart_unavailable:
  WHEN: "phoenix-diagram 未安装、其图型表没有 statechart，或按其停滞规则已停止修改模型"
  MUST: ["继续生成：手写 ONTOLOGY / TRANSITION / REQUIREMENT，用 counterexample_search 人工推演，并标明模型穷举 not-run",
         "交付时说明缺口与补上后能多得到什么"]
  MUST_NOT: [block_e2e_generation, install_tools_without_authorization,
             report_hand_reasoning_as_model_checked]

RULE @model_results:
  MUST: [=>["规则 breaks", "最短路径只是假设：按路径逐步在真实入口复现；复现前先假定模型有误。复现成立记为发现，不成立修模型"],
         =>["规则 holds", "只说明模型成立，代码是否如此仍由场景证明"],
         =>["not-checked 或 complete: false", "列出未判定的规则与原因，不算通过"],
         "statechart 只判定 Safety 规则与死锁；Liveness 写 REQUIREMENT 与 ASSUME，由真实场景观察，不标为模型已证",
         "交付说明模型省略了什么、隐藏了哪些步骤"]

RULE @scenarios:
  MUST: ["从用户真实要完成的任务写场景，不从验收行逐条翻译：谁、要做成什么、用什么真实或有代表性的输入",
         "一个场景是一段连续任务，不是一张断言清单；有模型时用尽量少的场景走完图上每条箭头，每条规则至少有一个场景逼近它的边界，走不到的列为未覆盖",
         "从用户实际入口经真实运行栈与本方依赖执行；只有范围外依赖未就绪时才在外部边界用替身，并标明未覆盖真实集成",
         "看用户实际得到的结果，涉及写入时再从第二个入口、重开进程或只读持久层确认；后续步骤可能掩盖错误状态时，在关键步骤后立即观察",
         "同一功能的按钮、快捷键、CLI 等入口分别记录覆盖；一个入口通过不算其他入口通过",
         "准备或观察用到的相邻入口只算依赖，不算已验收",
         "用项目已有工具或短脚本，每个场景一条命令，可单独选择"]
  MUST_NOT: ["另建验收框架、认证流水线或证据体系", "为本方代码造 fixture 或内存替身",
             "未知场景退回全量执行", "不够授权时驱动共享实例、真实支付、发消息或外部写入",
             "只因名字是 dry-run 或测试模式就认定没有副作用"]

RULE @findings:
  MUST: ["当前代码违反承诺时，用用户的话和复现步骤报告，状态记 failed",
         "产品缺陷、验证漂移、环境问题分开判断"]
  MUST_NOT: [weaken_rule_or_scenario_until_it_passes, change_product_code_without_request]

RULE @generated_skill:
  MUST: ["按模板写实：真实命令、路径和名词，不留占位；未跑通的部分明确写阻塞",
         "下一位 agent 只读它就能判断改动是否涉及本旅程、运行所选场景、区分缺陷与漂移、在有意变更时更新它",
         "记录每个场景覆盖的入口、文件与函数，以及最后确认过的提交；只有确认验证仍描述该提交的代码后才前移",
         "每轮证据写入项目约定目录，没有时写 artifacts/verification/e2e-<area>/<run-id>/，失败也保留",
         "SYNC_COMMIT 上已复现的产品缺陷写进 @known_findings，让下一位 agent 分清旧缺陷与新回归；其他运行结果和生成过程的验证层级只放证据目录与交付",
         "状态只用 passed / failed / blocked / not-run；只清理本轮创建的资源"]

WORKFLOW @prove_before_handoff:
  DO: ["按生成的 skill 完整跑一遍：选择场景 → 启动 → 只读体检 → 场景 → 取证 → 清理；检查实际动作没有超出所选场景及必要依赖",
       "在隔离副本对真实代码做一次临时破坏（去掉检查、调换步骤、成功但不落盘），用同一命令重跑，必须因目标行为失败",
       "当前代码已因目标缺陷失败时，再破坏分辨不出什么：改在隔离副本修好或退回缺陷前的提交，确认同一命令通过",
       "丢弃副本，确认检查回到原状：通过，或只因将要报告的发现而失败",
       "复杂生成且委派已获授权时，让无生成上下文的 agent 只凭成品和干净副本冷启动"]
  ON_FAILURE: "漏掉破坏或某步跑不通，修生成的 skill 或模型，不改破坏；语法错误、缺依赖导致的失败不算抓到"
  OUTPUT: [normal_run_evidence, broken_run_evidence, cleanup_result]

RULE @verification_status:
  MUST: ["没跑过的 skill 只算草稿，分层说明结构、作者实跑、破坏检测与冷启动各做到哪里",
         "不能在隔离副本安全注入故障时，标明破坏检测未执行及原因，不算已证明能发现故障",
         "只把坏数据传给判定函数只算校准断言，不称整条路径能发现故障"]
  MUST_NOT: [self_run_as_independent_verification, one_journey_as_whole_product_verified,
             break_code_in_user_workspace_or_shared_instance]

RULE @agi_mode_collaboration:
  MUST: ["agi-mode 负责结果契约与任务推进，生成的 e2e-* 负责操作项目并返回可核对的证据；本 skill 只在缺少可复用验证能力且创建/维护属于当前授权时介入",
         "agi-mode 将验收项映射到场景 ID、入口与必要边界，复用现有 e2e-* 并指出未映射项",
         "e2e-* 接收本轮范围、目标版本/环境、隔离条件和证据位置，只执行所选场景及必要依赖",
         "按场景与入口返回 passed / failed / blocked / not-run、实际观察、证据路径及清理状态；跳过、受阻和未执行不算通过",
         "多阶段任务已使用 agi-mode 证据契约时，读已安装 agi-mode 的 references/evidence-contract.md，把场景检查关联到现有 contract 和 receipts；它只验证记录一致性，不替代真实操作",
         "没有 agi-mode 时，生成的 skill 按同样的结果格式独立工作"]
  MUST_NOT: [require_generation_on_every_agi_mode_entry, copy_evidence_protocol,
             force_json_on_simple_tasks, derive_sdlc_completion_from_generator_smoke_run]

RULE @maintenance:
  WHEN: existing_e2e_skill_and_covered_code_or_expectation_source_changed
  MUST: ["从最后确认的提交起查看改动，只更新受影响的模型与场景并重跑",
         "每个场景给一个结果：in_sync（未受影响且通过）、updated（已改到描述新代码且通过）、bug（验证描述现状而代码违反承诺）、blocked（说明原因）"]
  MUST_NOT: [edit_product_code_during_maintenance, weaken_rule_to_clear_failure]

RULE @handoff:
  MUST: [journey_chosen_and_why, "每个候选的覆盖状态与依据提交", rules_in_one_user_sentence_each,
         "模型结果：逐条规则的判定与最短路径；或模型穷举 not-run 的原因",
         real_entry_findings_with_repro_steps, how_to_run, skill_path_and_evidence_path,
         break_detection_result, what_is_not_covered]
  SHOULD: suggest_second_target_only_when_a_close_one_was_found
```
