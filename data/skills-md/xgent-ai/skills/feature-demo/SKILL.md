---
name: feature-demo
description: "用于把开发计划或 git 范围内新增的 Web 功能录成操作视频并生成模板报告，用户要求时发布到 SPMS；不用于验收、写测试或非 Web 界面录屏。先在运行中的系统上核对，再回放固定脚本录制。"
when_to_use: "用户会说「这次加了什么，录个演示」「vibe coding 完不知道怎么用」「按这份计划录 demo」「UI 改了，重录一下」「把演示发到 SPMS」时。"
---

# Feature Demo

代码写得快之后，开发者常说不清系统多了什么、怎么用。本 skill 从计划和实际改动找出新增功能，在运行中的系统上走通，录成短视频，再灌进统一模板，生成一份报告。读者是要使用这些功能的开发者：可以用技术名词，节奏紧凑；页面讲新增能力、入口、操作和必要限制，不展示制作与发布过程。

```formal
INTENT:
  GOAL: show_developers_what_was_added_and_how_to_use_it
  SUCCESS: [every_user_visible_addition_is_recorded_or_listed_with_reason,
            each_video_replays_a_script_that_asserted_real_results,
            report_states_how_to_use_and_limits_in_the_shared_template]
  NON_GOALS: [acceptance, regression_tests, product_fixes_unless_requested,
              voiceover, native_or_cli_recording]

RULE @boundary:
  MUST: ["输出位置按 用户指定 → 项目已有演示目录 → docs/demos/；每批放在 <演示目录>/<批次>/，批次用计划代号（计划文件名去掉日期），没有计划时用 <日期>-<短 SHA>",
         "把 scripts/record-demo.mjs、scripts/render-report.mjs 和 scripts/publish-report.mjs 复制到演示目录，生成物不依赖本 skill；同批演示共用的登录和定位器放 <批次>/shared.mjs",
         "已有同名演示时原位更新脚本并重录，保留人工内容"]
  MUST_NOT: ["给目标项目添加依赖或修改产品代码，除非用户要求",
             "把一次录制通过说成验收通过；演示只证明这条路径在这次录制时走得通"]

RULE @find_additions:
  MUST: ["范围按 用户给定的 git 范围 → 计划完成记录里的提交 → 当前分支相对默认分支的改动；都无法判断时询问",
         "计划取 R-* 需求、§9 场景和实施进度作素材；计划内容只是意图，功能是否存在以 git diff 和实际运行为准",
         "对照后分三类：已实现且可见；计划有但没实现或走不通；改动里有但计划没写。后两类也要报告",
         "细小修复合并成一行列在报告，不单独录制"]
  MUST_NOT: "只读计划就写功能清单"

RULE @environment:
  MUST: ["先读项目的启动说明、已有 e2e-* 与登记的账号来源，复用它们的启动和登录方式",
         "录制前确认实例归属、版本与本次基线一致：看实际监听进程的启动命令，比对运行产物与本地构建的哈希、服务启动时间与最后改动时间；核验依据记入 <批次>/maintenance.md；跑的是验收 harness 或测试运行时而非正式入口时，在对应功能 note 简短说明演示条件；不一致就重新构建或报告阻塞，不换一个能跑的旧版本录。拿不到 SHA 级证据时在维护记录写明依据",
         =>[writes_not_authorized, "看起来只读的操作也可能写。在 setup 里用 page.context().route 中止并打印非 GET 请求，只放行登录、换票等已核实必要的路径；录制输出出现拦截记录就作废这次录制"],
         "凭据只从项目登记的来源经环境变量传入，交付时只写变量名；没有登记的来源时向用户要",
         "只清理本轮启动的服务和创建的数据"]
  MUST_NOT: ["未授权时在共享实例上写数据、花费真实额度、发消息或调用外部写接口；这类步骤缺授权时先问，或只录不产生副作用的部分并在报告写明",
             "为本方代码造替身；只有范围外依赖未就绪时才在外部边界用替身，并在视频字幕和报告写明",
             "让故障注入或调试用的数据入镜；普通测试数据可以用，并在报告写明"]

WORKFLOW @write_demo:
  DO: ["每个功能一个 <slug>.demo.mjs，走一段连续的真实任务，通常不超过 8 步、一分钟内；格式见下",
       "缺授权不能实跑的结果可以用已有数据展示，比如打开历史记录；字幕和报告写明这是历史结果，没有实跑",
       "默认视口下进入了和计划不同的布局分支时，设 viewport 或切到对应形态，别让演示展示错误的分支",
       "应用要异步加载时设 ready，等内容出现后再开录",
       "用真实运行的页面确定定位器，不凭读代码猜；角色和可见名称优先，应用在 iframe 里时用 frameLocator",
       "字幕写这一步做什么和为什么，界面上看得到的不重复；一句话，语言跟随用户",
       "see 和 gone 写这步操作产生的、功能特有的结果；承诺是具体按钮或入口时就断言操作这个入口的结果"]

RULE @precheck:
  # 录制脚本证明 Playwright 走得通；录制前核对看的是运行中的系统此刻真实渲染成什么样。
  WHEN: "宿主技能目录（如 .claude/skills/phoenix-ui/、.agents/skills/phoenix-ui/ 或用户级同名目录）里有 scripts/phoenix-ui，且 <它> capture --help 退出 0"
  MUST: ["录制前把每个待录功能的演示步骤写成 capture 状态文件，定位沿用演示里的角色与可见名称；对运行中的系统执行 <phoenix-ui> capture <入口+path> --viewport <演示视口> --states <文件> --block-writes [--allow-write <已核实必要的路径>] --out <批次>/precheck/<slug>/，查看关键状态截图、控制台错误与失败请求",
         "报告有被拦截的写请求时按 @environment 的写入规则处理：缺授权先问，或只录不产生副作用的部分；有拦截记录不算核对通过",
         "核对失败按报告里的失败步骤与原因归为产品缺陷、脚本漂移或环境问题，按 @failed_step 处理",
         =>[app_in_iframe_or_step_target_in_shadow_dom, "该功能不做录制前核对，照原流程录制"]]
  MUST_NOT: ["把预检截图当视频或验收", "把 capture 写进演示脚本或录制器", "为核对安装、下载或提示安装 Phoenix"]
  # 找不到、退出 4（engine 缺失或版本不符）或未知命令都视为不可用：本规则不适用，流程与原来一致。

RULE @recording:
  MUST: ["Playwright 用项目已有的 1.64 及以上版本；没有时用 npm i --prefix <项目外目录> playwright-core 装到项目外，设 PLAYWRIGHT_ROOT 指向它，并告知会下载浏览器",
         "只回放固定脚本，步骤失败就停，不产出视频"]
  MUST_NOT: ["让模型在录制时现场决定操作", "加长等待或放宽断言，只为让失败的步骤通过"]

RULE @failed_step:
  MUST: ["先看 <slug>.failed.png，判断是产品缺陷、脚本漂移还是环境问题；做过录制前核对时同时对照 precheck/<slug>/capture-report.json 的失败步骤与截图",
         "产品缺陷用用户的话和复现步骤报告，功能写入报告的「没有录制」节，不修产品，不绕开这一步",
         "脚本漂移修脚本后重录；环境问题修环境或记为阻塞"]

RULE @review_video:
  # 脚本通过只说明断言成立，看不出字幕挡住结果或画面露出真实数据。
  MUST: ["每步时刻后约 0.3 秒抽一帧，再加每秒一帧快速扫一遍全程，闪现的中间状态只有这样才看得到；亲自看这些帧。有 ffmpeg 用 ffmpeg，没有就逐段播放或说明未检查",
         "检查：结果在画面内且没被字幕挡住（被挡时设 captionAt: 'top'）；停留够看清；没有密钥、真实客户数据、调试文本或故障注入数据；页面不是加载中",
         "问题改脚本后重录"]

RULE @charts:
  # 视频演示一条路径，图说明这条路径在全局的位置。
  MUST: ["已安装 phoenix-diagram 时读它的 skill，为有分支、等待或多页面流转的功能各生成一张图，放进批次目录并写入 chart；整批有共同主线时再加 overviewChart",
         "页面流转用 workflow；功能的核心是状态变化时才用 statechart，它要先写清规则，规则判定记录写进 maintenance.md，只把影响使用的状态约束写进 limits",
         "图从 @find_additions 核对过的实际行为来画，不只照抄计划",
         =>[phoenix_diagram_unavailable, "不生成图，交付时说明，录制和报告照常"]]
  MUST_NOT: ["未经用户同意安装图解引擎", "把图嵌进别的 HTML 文件；每张图保持独立文件"]

RULE @report:
  MUST: ["读 references/report-format.md，按模板写 <批次>/report.json，不手写 HTML",
         "每个功能写清解决什么、入口和操作、限制；不可录的功能进 sections，也写用法，并标明是否实跑过",
         "三类功能的后两类和细小修复进 sections；只收录影响读者使用或理解功能的内容，详情见 report-format 的内容边界",
         "发布与录制记录、版本核验、哈希和进程、工具检查、账号来源与重录命令放 <批次>/maintenance.md，不放 report.json 的正文，也不换标题塞进 sections、summary、note 或 limits；维护记录不自动发布",
         "运行 render-report.mjs 生成 index.html；报错就改数据，不改生成结果",
         "meta 只填协议要求的简短来源、版本和演示条件；做过录制前核对时，在 maintenance.md 写工具版本、capture 结果和证据路径；precheck/ 不列进读者交付",
         "在浏览器打开 index.html（headless 也可以），确认桌面与窄屏下首屏能找到功能和视频、正文易读、没有横向溢出；每个视频有时长且能播放，展开的图正常显示"]

RULE @publish:
  # 发布让没有本地环境的同事在 SPMS 项目报告里直接看；同一 batchId 再发布原位替换，链接不变。
  WHEN: user_explicitly_asks_to_publish_to_spms
  MUST: ["目标项目 id、SPMS MCP 地址与 Agent 令牌从项目登记的来源取得，没有登记时向用户要；令牌经 SPMS_TOKEN 环境变量传入，地址经 SPMS_MCP_URL，交付时只写变量名",
         "在批次目录外运行 SPMS_MCP_URL=… SPMS_TOKEN=… node <演示目录>/publish-report.mjs <批次>/report.json --project <项目 id>；脚本先按模板与上限校验，只上传 report.json 引用的视频和图",
         "回报报告编号、报告链接和结果；结果是替换时，转告被替换报告的原标题和上次更新时间，提醒用户同一链接已是新内容",
         "失败时如实转述脚本给出的原因（字段错误、未上传的文件、令牌或项目权限、SPMS 或文件服务连不上），批次目录保持原样；上传地址过期或不确定是否已发布时重新运行整个脚本"]
  MUST_NOT: ["未经用户明确要求就发布", "改动批次目录里的文件来让发布通过，或绕过脚本手工上传"]

RULE @handoff:
  MUST: ["给出 index.html 和 report.json 的路径，简述新增能力与用法；基线、环境证据和重录方法指向 maintenance.md，不复述执行日志",
         "列出发现的产品问题、未录制项及原因、用到的额度或写入",
         "仅有实际可见范围或分享风险时在交付消息中提醒；看报告只需要 report.json、index.html、视频和图，.mjs 与 maintenance.md 仅供维护；未经要求不提交视频"]
  MUST_NOT: commit_or_publish_without_request
```

## 演示文件

```js
export default {
  title: '任务筛选',
  path: '/tasks',                         // 相对 --url，录制从这里开始
  // 可选：应用在 iframe 里时用 frameLocator；这个元素出现后才开录
  ready: page => page.getByRole('heading', { name: '任务' }),
  // 可选：录制前执行，用于登录和准备数据，不进入视频
  setup: async page => {
    await page.goto('/login');
    await page.getByLabel('邮箱').fill(process.env.DEMO_USER);
    await page.getByLabel('密码').fill(process.env.DEMO_PASSWORD);
    await page.getByRole('button', { name: '登录' }).click();
    await page.waitForURL('**/tasks');
  },
  steps: [
    {
      caption: '筛选弹窗列出全部已有任务',
      do: page => page.getByRole('button', { name: '筛选' }).click(),
      see: page => page.getByRole('heading', { name: '筛选任务' }),
    },
    {
      caption: '点完成回到列表',
      do: page => page.getByRole('button', { name: '完成' }).click(),
      gone: page => page.getByRole('heading', { name: '筛选任务' }),
    },
  ],
};
```

| 字段 | 说明 |
| --- | --- |
| `viewport`（顶层） | 录制尺寸，如 `{ width: 1600, height: 900 }`，默认 1280×720 |
| `ready`（顶层） | 返回定位器：开录前等它出现，默认不等 |
| `caption` | 这一步的字幕，必填 |
| `captionAt` | 设为 `'top'` 时字幕放在顶部，默认底部 |
| `do` | 这一步的操作；省略时只展示 `see` 指向的内容，可用来滚动到页面下方的结果 |
| `see` / `gone` | 返回定位器：操作后应出现 / 应消失的元素，至少写一个。操作前结果已成立时录制器判失败；`see` 通过后自动滚入画面 |
| `timeout` | 等结果出现的毫秒数，默认 15000，慢操作才设 |
| `hold` | 结果出现后的停留毫秒数，默认 1200 |

## 命令

```bash
# 应用已运行；在项目根目录执行
node docs/demos/record-demo.mjs docs/demos/<批次>/<slug>.demo.mjs --url http://127.0.0.1:3000
node docs/demos/render-report.mjs docs/demos/<批次>/report.json
```

录制退出码：0 成功，1 某一步失败或运行出错，2 参数、演示文件或 Playwright 版本不合法。生成报告退出码：0 成功，2 数据不合法。
