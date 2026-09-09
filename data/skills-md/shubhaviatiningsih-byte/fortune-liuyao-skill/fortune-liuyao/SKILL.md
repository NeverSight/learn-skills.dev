---
name: fortune-liuyao
description: 当用户提出六爻占卜、六爻排盘、文王纳甲、京房八宫、三枚硬币起卦、手动输入六次爻值，或询问事业、感情、财富、学业等六爻问题时使用；英文 Liuyao、Six Lines Divination、Wenwang Najia、I Ching coin casting 也应触发。完成确定性排盘、领域方法加载、当前对话中的完整综合解读、包含卦盘与解读的 HTML 完整报告、标准分享图及事实一致性检查；对高风险医疗、生死、胎儿性别、失踪定位等问题只提供现实帮助。
---

# Fortune 六爻

只执行以下主流程：

**理解问题与语义路由 → 选择起卦方式 → 运行统一入口 → 完整解读 → 审计事实并生成最终 HTML → 按宿主能力生成标准分享图**

确定性脚本负责起卦、历法、排盘、规则事实和展示文件；当前 Agent 负责理解问题、选择领域、调用宿主交互控件，以及依据返回的 `prompt` 完成传统综合判断。锁定盘面事实，不限制无法确定性验证的吉凶、应期和传统推断。

## 1. 理解问题并选择领域

完整阅读 [domain-routing.md](references/domain-routing.md)，根据用户原问题的语义选择以下一个领域，传给统一入口的 `--category`：

`general`、`career`、`wealth`、`relationship`、`academic`、`travel`、`home`、`legal_risk`、`relationship_family`

不要用关键词表代替语义理解。领域只决定加载哪套分析方法，不属于确定性盘面事实。

- 能识别核心事项和用户希望判断的结果：直接继续，不追问可合理留空的信息。
- 问题包含多个需要不同判断主线的独立事项：只问用户本次最想判断哪一个。
- 无法识别所问事项、判断对象或目标结果：暂停起卦，只问一个最必要的澄清问题。
- 问题清晰但领域边界不明确：使用 `general`，不要为了分类追问。

问题清晰度、敏感分流放行、领域路由、脚本状态和校验通过都属于内部过程，成功时不要展示给用户。排盘前不要发送“我会使用本 Skill”“问题已归入某领域”“现在开始运行”等前言；直接执行所需工具。首次面向用户的成功消息从卦盘和解读开始。

### 性别或关系视角

排盘以及事业、财富、学业、出行、住宅、纠纷等领域不需要性别。家庭或代占问题优先理解提问者与被问者的实际关系。

仅当问题属于恋爱或婚姻、用户没有说明视角，并且准备采用“男问妻财、女问官鬼”的传统异性婚恋取用时，才用一个可跳过的问题询问男方、女方或不按性别取用。分别传入 `--perspective male`、`female` 或 `unspecified`。同性关系、非二元身份或用户不愿提供时使用 `unspecified`，结合关系角色与世应分析。

胎儿性别、母婴安危和怀孕结果不是可澄清字段，按安全边界处理。

## 2. 选择并完成起卦

先按 [safety-boundaries.md](references/safety-boundaries.md) 判断；统一入口还会执行确定性分流。被阻止时不排盘，友好转向就医、报警、求助热线或专业咨询等现实帮助。

用户尚未指定起卦方式时，立即使用宿主 Agent 的单选控件提供：

1. 自动起卦
2. 逐爻弹窗
3. 输入硬币或爻值

宿主不支持选择控件时，只发一条简短文字选项。用户选定后立即执行，不再追加“是否开始”。不要另建网页或本地服务模拟弹窗。

用户选择“输入硬币或爻值”后，必须先主动显示这一段计数说明，再等待输入：

> 系统不会根据硬币图案自动判断正反。本 Skill 默认把有面额数字／文字的一面记为“正”，把国徽、花卉等图案面记为“反”；六次保持不变。正面记 3，反面记 2，三枚相加：6=老阴（动）、7=少阳、8=少阴、9=老阳（动）。连续投六次，第一次是初爻，第六次是上爻。请按顺序反馈六次结果，例如：`正反反 / 正正反 / ……`，并备注：`正=字／面额面，反=国徽／花卉面`；也可以直接发送六个爻值。

若用户已经直接给出六轮硬币或六个爻值，不重复教学，直接按其输入继续；若用户声明了不同正反面约定，不得静默改写，须让用户确认最终六个爻值。

### 逐爻弹窗状态机

第一次弹窗显示“生成初爻”。用户点击后运行：

```powershell
python scripts/cast_one_line.py --position 1
```

保存该结果，立即在下一弹窗显示已生成的初爻及“生成二爻”。依次把 `--position` 增加到 6。

- 两次弹窗之间不发送说明、路由、分析或阶段总结。
- 每个位置只运行一次；保存并复用已生成结果，禁止重摇。
- 第六爻完成后不再询问确认，直接把六个值按初爻至上爻传给 `--method lines`。
- 宿主每次提交都要恢复 Agent，允许短暂延迟，但恢复后立即调用下一弹窗。
- 宿主不支持选择控件时，不模拟六轮文字确认；改为让用户一次输入六轮硬币或六个爻值。

硬币换算与顺序完整阅读 [manual-coin-casting.md](references/manual-coin-casting.md)。

## 3. 运行唯一生成入口

先在后台探测当前宿主可用的 Python 命令：Windows 依次尝试 `python`、`py -3`，再检查 Codex 常见内置运行时 `$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`；macOS/Linux 依次尝试 `python3`、`python`。使用第一个能返回 Python 3.10+ 的命令继续，并把后续示例中的 `python` 全部替换成该命令；不向用户展示成功的环境探测过程。

如果所有命令都不存在，停止排盘并只提示：“当前 Agent 环境缺少运行排盘引擎所需的 Python 3.10+。请安装 Python 后重试，或换用自带 Python 运行环境的 Agent。”不要让模型临时心算排盘。

再用已探测到的命令运行一次自检，例如：

```powershell
python scripts/run_liuyao.py --selfcheck
```

只有返回 `READY` 才继续。返回 `NOT_READY` 时，只说明缺少的运行条件，不生成半张盘，也不让 Agent 临时重算历法或纳甲。`lunar_python` 已随 Skill 内置，不要求用户执行 `pip install`；若自检仍报告内置依赖缺失，说明安装包不完整，应重新安装 Skill。

自动起卦示例：

```powershell
python scripts/run_liuyao.py `
  --question "未来三个月能否找到合适工作" `
  --category career `
  --method auto `
  --output session.json
```

逐爻或已知爻值使用：

```powershell
python scripts/run_liuyao.py --question "用户原问题" --category general --method lines --lines "7,8,8,6,7,8" --output session.json
```

用户提供六轮硬币时使用 `--method coins --coins "正反反/正正反/反反反/正反反/正正正/正正反"`。

统一入口一次返回：

- `result`：确定性卦盘、规则事实、问题上下文和起卦审计；
- `prompt`：当前 Agent 应直接使用的完整解读上下文；
- `artifacts.html` 与 `artifacts.markdown`：从同一份结果同步生成的展示文件路径；
- `schemaVersion`：输出契约版本。

JSON 和 Markdown 是脚本与 Agent 之间用于保存、复核和事实审计的内部契约。不要向用户粘贴或附加 `session.json`、原始 JSON、`prompt` 或 Markdown 文件；最终用户在当前对话中直接阅读完整解读，HTML 只作为可选卦盘附件。只有用户明确要求导出原始排盘数据时才交付 JSON。

不要再依次调用 `build_chart.py`、`build_model_packet.py` 和 `render_chart.py` 拼接默认流程。它们只作为内部组件和诊断工具。

## 4. 完整解读

最终聊天回复是主要且完整的用户交付物。无论 HTML 是否能够交付或打开，都必须直接在当前对话中给出完整文字解读：

- 统一入口此时生成的 `artifacts.html` 是待合并解读的临时卦盘，不要立即把它作为最终附件交付。
- 不向用户交付 `artifacts.markdown`；Markdown 只供内部渲染、复核和事实审计。
- 不得让用户打开 Markdown、JSON 或原始提示词查看解读。
- 不得把完整文字解读设计成 HTML 的失败降级；它在所有成功排盘中都是必需输出。

完整阅读 [interpretation-modes.md](references/interpretation-modes.md)，直接使用返回的 `prompt` 在当前对话中完成综合解读。不要把 `prompt` 发送给另一个模型，不要求用户提供模型 API 密钥。最终回复不得只给“解读核心”、一句话总结、几条压缩结论或要求用户打开附件查看全文，除非用户明确要求简版。

发送前静默检查：已经直接回答所问，解释了用神、世应、月日和关键动变如何支持结论，覆盖了会实质改变判断的其他结构；用户询问期限时已经回答时间趋势；已经给出现实建议，并以简短“总结与行动”收束；无法确定性验证的内容保持为传统推断。只在内部完成检查，不向用户展示清单、路由、安全分流、脚本状态或审计结果。

传统健康、吉凶、应期和取象可以作为传统推断表达，但不得伪装成确定性盘面字段、医疗诊断或现实专业意见。

## 5. 审计并生成完整 HTML

把完整解读保存为 Markdown 或文本后，运行最终报告入口。它会先审计明确盘面事实；只有审计通过才把同一份完整解读合并进卦盘 HTML：

```powershell
python scripts/render_final_report.py --session session.json --report report.md --output fortune-liuyao-report.html --audit-output fact-audit.json
```

退出码 `2` 时，根据审计清单修正对应事实后重新运行；不要删除或压缩无法确定性验证的传统判断。成功后在聊天中直接发送完整解读；宿主支持文件交付时，同时附上包含卦盘和完整解读的 `fortune-liuyao-report.html`。不要交付统一入口生成的临时卦盘 HTML。HTML 无法交付或打开时只省略附件，聊天中的完整报告保持不变。校验通过时保持静默，不向用户展示 `accepted=true` 或内部清单。

## 6. 生成标准分享图

宿主提供图片生成能力时，成功排盘默认再生成一张可保存、可转发的 1080 × 1440 PNG；没有图片模型但提供浏览器或 HTML 截图能力时，优先从同一份确定性 HTML 渲染 PNG。两种能力都不存在时安静省略图片，只交付 HTML 和聊天中的完整解读，不得伪造已经生成图片。用户明确要求“排盘图片”“分享图”“小红书竖图”时，完整阅读 [share-card-contract.md](references/share-card-contract.md)，并以 [standard-share-card.png](assets/standard-share-card.png) 作为视觉锚点。

分享图只从同一份 `result` 提取问题、时间、干支、节气、卦名、六爻、六神、世应、动变与神煞；不得凭视觉模板补写盘面字段。生成后逐项对照 `result` 检查本卦、变卦、六爻顺序、世应和动爻。发现文字、爻象或标记错误时重新生成，不在位图上覆盖修字。分享图用于保存与传播，不替代完整 HTML 或聊天解读，也不得自动发布到社交平台。

## 7. 同一卦的后续追问

用户在当前对话继续追问同一事项时，完整阅读 [follow-up-dialogue.md](references/follow-up-dialogue.md)。默认沿用最近一次成功排盘及原起卦时的月日、爻值、世应、用神主线和首次结论，不重新起卦、不重新询问起卦方式，也不因当前日期变化重算原盘。后续回答直接回应新问题，以相关原盘依据和现实行动收束；不机械重复完整报告，不自动重做 HTML 或分享图。只有事项、对象、目标或时间范围发生实质变化，或用户明确坚持提出新问题时，才进入新的起卦流程。

最终原样附上：

> 本内容基于玄学体系生成，仅供文化爱好与思维参考，不构成任何重大人生决策的专业建议。

## 按需读取

- 本地运行与错误边界：[runtime-contract.md](references/runtime-contract.md)
- 领域分类：[domain-routing.md](references/domain-routing.md)
- 领域分析方法：[interpretation-modes.md](references/interpretation-modes.md)
- 硬币起卦：[manual-coin-casting.md](references/manual-coin-casting.md)
- 安全边界：[safety-boundaries.md](references/safety-boundaries.md)
- 展示规则：[frontend-contract.md](references/frontend-contract.md)
- 标准分享图：[share-card-contract.md](references/share-card-contract.md)
- 同卦追问：[follow-up-dialogue.md](references/follow-up-dialogue.md)
