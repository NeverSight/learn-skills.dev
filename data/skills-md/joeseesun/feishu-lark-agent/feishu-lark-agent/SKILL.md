---
name: feishu-lark-agent
description: |
  Comprehensive Feishu/Lark workspace agent. Handles messages, docs, bitable (multi-dimensional tables), calendar, and tasks via Feishu Open API.

  Trigger when user says anything involving:
  - 飞书消息：发消息、发飞书、查消息、回复消息、搜索消息、查看群聊
  - 飞书文档：创建文档、查看文档、读取文档、飞书doc
  - 多维表格/Bitable：查记录、添加记录、更新记录、删除记录
  - 日历：飞书日历、查日程、创建日程、添加日历
  - 任务：飞书任务、创建任务、查看任务、完成任务
  - 用户：查飞书用户、找联系人
---

# Feishu Lark Agent

Zero-dependency Python CLI for Feishu/Lark Open API.

## Run

```bash
source ~/.zshrc && python3 ~/.claude/skills/feishu-lark-agent/feishu.py <category> <action> [--key value ...]
```

## Environment Variables

```bash
FEISHU_APP_ID=cli_xxx          # required
FEISHU_APP_SECRET=xxx          # required
FEISHU_OWNER_OPEN_ID=ou_xxx    # optional — auto-grants doc edit + cal invite to this user
```

When `FEISHU_OWNER_OPEN_ID` is set:
- `doc create` → automatically grants full_access to that user
- `cal add` → automatically adds that user as calendar attendee

---

## Commands

### Messages (`msg`)

```bash
msg send  --email <email> | --to <open_id> | --chat <chat_id>  --text "..." | --file /path
msg history --chat <chat_id> [--limit 20]
msg reply --to <message_id> --text "..."
msg search --query "关键词" [--limit 20]
msg chats  [--limit 50]
```

### Users (`user`)

```bash
user get --email <email>          # returns open_id, name, etc.
user get --id <open_id>
user search --name "张三"
```

### Documents (`doc`)

```bash
doc create --title "会议记录" [--folder <token>] [--file /path/to/content.md]
doc get    --id <document_id>     # document_id from URL: feishu.cn/docx/DOC_ID
doc list   [--folder <token>] [--limit 50]
```

### Bitable (`table`)

App token is in URL: `feishu.cn/base/APP_TOKEN`

```bash
table fields  --app <token> --table <id>
table records --app <token> --table <id> [--filter 'AND(CurrentValue.[状态]="进行中")'] [--limit 100]
table add     --app <token> --table <id> --data '{"字段":"值"}'
table update  --app <token> --table <id> --record <recXXX> --data '{"字段":"新值"}'
table delete  --app <token> --table <id> --record <recXXX>
table tables  --app <token>
```

Always run `table fields` first to see available field names before writing records.

### Calendar (`cal`)

> ⚠️ Bot uses tenant token — cannot access user's personal calendar. Use the bot's own calendar ID (not `primary`). Get it with:
> ```bash
> python3 -c "import sys,os,json; sys.path.insert(0,'~/.claude/skills/feishu-lark-agent'.replace('~',os.path.expanduser('~'))); import feishu; print(json.dumps(feishu.api('GET','/calendar/v4/calendars',params={'page_size':50}),indent=2,ensure_ascii=False))"
> ```

```bash
cal list   --calendar <id> [--days 7]
cal add    --calendar <id> --title "..." --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM" [--location "..."] [--desc "..."] [--attendees "a@x.com,b@x.com"]
cal delete --calendar <id> --id <event_id>
```

### Tasks (`task`)

```bash
task list   [--completed true] [--limit 50]
task add    --title "..." [--due "YYYY-MM-DD"] [--note "..."]
task done   --id <task_guid>
task delete --id <task_guid>
```

---

## Key Workflows

**Send to person by name** (only have name, not ID):
1. `user search --name "张三"` → get open_id
2. `msg send --to <open_id> --text "..."`

**Add Bitable record** (unknown fields):
1. `table fields --app ... --table ...` → see field names and types
2. `table add --app ... --table ... --data '{...}'`

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `99991671` | App not authorized | Enable permission in Feishu Open Platform |
| `230006` | No calendar access | Enable `calendar:calendar` permission |
| `1254043` | Bitable not found | Check app_token in URL |
| `191001` | Invalid calendar_id | Don't use `primary`; get real calendar ID (see above) |
| `Missing FEISHU_APP_ID` | Env not loaded | `source ~/.zshrc` |
