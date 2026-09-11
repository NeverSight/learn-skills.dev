---
name: efgp-operation
description: 鼎新 EFGP 流程管理系统（efgpcn.digiwin.com/NaNaWeb）浏览器自动化操作，覆盖自动登录、会议室预订（含视讯会议 Zoom 账号订阅）、请假、查考勤、补考勤等门户功能。当用户提到 EFGP、EasyFlow、订会议室/会议申请/视讯会议/Zoom账号、请假、考勤、补考勤，或要求操作 efgpcn.digiwin.com 网站时必须使用本 Skill；即使用户只说"帮我订个会议室""查一下考勤"也应触发。
---

# EFGP 操作 Skill

通过 playwright-cli 自动化操作鼎新 EFGP 流程管理系统（https://efgpcn.digiwin.com/NaNaWeb/）。

## 路径约定（项目内）

| 用途 | 路径 |
|---|---|
| 本 Skill | `<项目>\.agents\skills\efgp-operation\SKILL.md` |
| 浏览器用户数据（登录态/记住的密码） | `<项目>\.agents\efgp\.efgp-profile\` |
| 个性化配置（楼层/人数/选房规则） | `<项目>\.agents\efgp\efgp-personalization.md` |
| 过程产物（快照 yaml、截图 png） | `<项目>\.playwright-cli\`（操作成功后清空） |

- playwright-cli 的快照默认写入当前目录的 `.playwright-cli\`；截图/自定义快照一律显式指定到该目录，例如 `screenshot --filename=.playwright-cli\meeting-success.png`、`snapshot --filename=.playwright-cli\xxx.yaml`。
- `.agents\efgp\`（含凭证与用户偏好）和 `.playwright-cli\`（快照可能含敏感页面内容）都必须加入 `.gitignore`。

## 首次使用 / 个性化配置缺失时

如果 `<项目>\.agents\efgp\efgp-personalization.md` 不存在，**不要凭空假设**，先向用户收集并创建该文件：

1. 询问并记录：**办公楼层**、**常规参会人数**。所属区域、资源使用区由 GP 系统自动处理，无需询问；也不采集工号、姓名、登录代号、分机等个人信息——登录后表单会自动带出，配置文件不保留。
2. 引导首次登录（让浏览器记住密码，以后才能自动登录）：
   - 用 **headed 有头模式**打开门户：`playwright-cli -s=efgp open --headed --profile=<项目>\.agents\efgp\.efgp-profile "https://efgpcn.digiwin.com/NaNaWeb/"`
   - 打开后会自动产生第二个标签页（EasyFlow GP / 流程管理系统），`tab-select 1` 切换过去。
   - 请用户在弹出的浏览器窗口中手动输入账号密码，并在浏览器提示时选择**保存密码**。
3. 明确告知用户隐私边界：**Skill 不会记录账号和密码**（密码只保存在浏览器自己的密码管理器中）；但登录成功后页面会显示用户姓名/工号，这些会出现在过程快照里——快照仅用于操作过程，任务成功后会被删除，Skill 本身不留存。

## 打开门户

```powershell
playwright-cli -s=efgp open --profile=<项目>\.agents\efgp\.efgp-profile "https://efgpcn.digiwin.com/NaNaWeb/GP/Logout?hdnMethod=login"
```

若该地址进入"错误处理页面"，改从门户根地址 `https://efgpcn.digiwin.com/NaNaWeb/` 进入。打开后如产生多个标签页，用 `tab-select` 切换到目标页。

## 登录

EFGP 是服务器端会话（JSESSIONID），浏览器关闭后服务器侧会话即失效，**Cookie/state-save 无法恢复登录**。实际有效的"自动登录"链路是：浏览器密码管理器自动填充账密（首次使用时用户手动登录并选择保存密码）→ CLI 点击"登入"。

- 打开登录页后账密应已自动填充，直接点"登入"单元格。
- 点击后可能弹 confirm："此浏览器已存在登入资讯…"——用下面的弹窗钩子自动处理，或 `dialog-accept`。
- 登录成功标志：页面出现"目前使用者: …"。
- 若账密未自动填充（profile 被换/清空），按"首次使用"流程让用户重新登录一次并保存密码。

## 关键稳定性措施：注册弹窗自动处理钩子

EFGP 大量使用老式 `alert/confirm`。playwright-cli 默认把对话框挂起等待人工处理，后续命令全部超时甚至导致浏览器崩溃。**在任何表单操作之前**先注册自动接受钩子：

```powershell
playwright-cli -s=efgp run-code "async page => { const ctx = page.context(); const attach = p => p.on('dialog', async d => { const msg = d.message(); await d.accept(); try { await p.evaluate(m => { (window.__dlgMsgs = window.__dlgMsgs || []).push(m); }, msg); } catch(e){} }); ctx.pages().forEach(attach); ctx.on('page', attach); }"
```

弹窗内容会记录到页面的 `window.__dlgMsgs`，操作后用 `eval "JSON.stringify(window.__dlgMsgs||[])"` 读取，确认系统是否有冲突提示等警告。（注意：`window` 在 run-code 的 Node 上下文中不可用，写回消息要用 `p.evaluate`。）

## 菜单搜索模式

左侧导航 iframe（`ifmNavigator`）的"搜寻功能/流程"搜索框：

- 搜索词要**简短**且用系统中实际存在的叫法：搜"会议"能命中"001会议申请/异动单"；搜"会议室"（无论简繁）都查不到。
- 请假、考勤、补考勤同理：先搜单字/双字关键词（如"假""勤"），从结果列表点对应流程链接。

## 会议室预订交互约定

### 用户必须输入（缺什么问什么，不要自行假设）

| 输入项 | 说明 |
|---|---|
| **时间** | 会议日期 + 起止时间（如"下周一 10:00-12:00"，需换算成具体日期） |
| **是否需要 Zoom 网络会议** | 决定会议形态（一般会议/视讯会议）、召集方、是否订阅视讯账号 |

以下项用户没给时自动给默认值：**会议主题**默认"内部会议"；**会议性质**默认"內部會議"；**参会人数**默认取个性化配置中的"常规参会人数"。

### 预订完成后必须输出

| 输出项 | 说明 |
|---|---|
| **会议室** | 代号 + 名称（含楼层、座位数），如 NJM8003 南京18楼8003会议室（6座） |
| **会议主题** | 实际填写的主题 |
| **时间** | 日期 + 起止时间 |
| **Zoom** | 订阅的视讯账号（如 CZoom-28）；用户没要 Zoom 时此项给空 |
| **会议性质** | 实际所选类型（如 内部会议） |
| **会议室遵循提示** | 附上"谁使用、谁复原"等使用责任提醒（设施关闭/桌椅复位/用具归库/白板擦净/环境扫视/有借有还） |
| 流程序号 | 发起成功后的序号（如 MeetingApply00392151），便于用户追踪 |

## 会议室预订完整流程（会议申请/异动单）

表单位于双层嵌套 iframe（`ifmFucntionLocation` → `ifmAppLocation`）。快照 ref 每次打开会变，**优先使用元素 ID 定位**；ref 失效时先重新 snapshot。

1. **读取个性化配置** `.agents\efgp\efgp-personalization.md`，获取用户办公楼层、常规参会人数、选房规则。
2. **会议形态**：勾选"视讯会议"radio（需要订阅视讯时）。
3. **视讯会议召集方**：勾"是"（选视讯会议后才解除禁用；是=可开窗选视讯账号并接收主持人金钥邮件）。
4. **会议主题**：`#txaSubject`。
5. **起始/结束时间**：日期 `#dateStart_txt`（格式 yyyy/MM/dd），时分下拉 `#drpStartHour` `#drpStartMin` `#drpEndHour` `#drpEndMin`（分钟为 10 分钟步进）。
6. **会议类型**：`#drpMeetingType` 选"內部會議"（选项为繁体）。
7. **视讯账号**：点 `#btnVideo_CN` 弹出查询窗（新标签页，其 URL 内嵌 SQL 已按表单时段过滤空闲账号），`tab-select` 切过去，点击第一行账号单元格（如 CZoom-28），弹窗自动关闭并回填。
8. **会议室**：点 `#btnRoom_CN` 弹出房间查询窗（新标签页）。列表每页 10 条，用"下一頁"翻页；按个性化配置的选房优先级规则挑房（同楼层 + 座位数贴合人数）。点击目标行"会议室代号"单元格即选中并回填。
   - 若列表无合适/无空闲房间，回表单点"CN查询"按钮查看借用状况，向用户推荐附近空闲时段，确认后再订。
9. **加入明细**：点"新增"按钮把房间加入明细表格（必须这一步，否则发起时校验不过）。换房时先点明细行选中再点"删除"，然后重复 8-9。
10. **是否知晓**：勾选底部"会议室遵循谁使用谁复原…"radio。
11. **发起**：点左上角"发起"图片按钮（`img[alt=发起]`）。成功标志：页面显示"你的流程已经发起成功了!"及流程序号（如 MeetingApply00392151）。
12. **截图留证**到 `.playwright-cli\meeting-success.png`，按上文"预订完成后必须输出"的约定格式向用户汇报，并把本次预订追加到个性化配置的"历史预订参考"表。
13. **清理过程产物**：确认发起成功后，删除 `.playwright-cli\` 下的全部文件（快照可能含页面敏感信息，不长期保留）。
14. **关闭浏览器**：`playwright-cli -s=efgp close`，结束会话（登录态已保存在 `.agents\efgp\.efgp-profile\`，不影响下次自动登录）。

## 故障处理

| 症状 | 原因与对策 |
|---|---|
| 页面标题"错误处理页面" | 直接访问了深层链接或 jsessionid 过期 → 回到门户根地址重建会话 |
| 命令超时后 "Session closed" | 弹窗挂起导致守护进程崩溃 → 先注册弹窗钩子再操作；崩溃后用同 profile 重新 open，从门户根重新进入（账密自动填充，点登入即可） |
| 登录页账密未自动填充 | profile 目录被换/清空 → 按"首次使用"流程让用户手动登录一次并让浏览器记住密码，再 state-save |
| 快照 ref 失效（Ref not found） | 表单重绘后 ref 变化 → 重新 `snapshot` 获取最新 ref |
| PowerShell 报"禁止运行脚本"| 执行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

## 安全注意

- Skill 不记录用户账号密码；密码仅存于浏览器密码管理器（`.agents\efgp\.efgp-profile\`），该目录与 `efgp-auth.json`、`.playwright-cli\` 均不得提交版本库。
