---
name: oinoa-setup
description: >-
  Walk a new OINOA client through setting up their team, one step at a time, right here in the
  chat: Telegram for each employee, their own AI subscription (Claude), mail, 1С, CRM and other
  services, who may write to an employee, work groups, and where to get a specialist. Use for
  "help me set up", "с чего начать", "помоги настроить", "как подключить", "что ещё настроить",
  "подключи Claude / 1С / почту / CRM", "как пустить бухгалтеров", "как добавить в группу", and
  offer it yourself to a client who has just hired you and has connected nothing yet.
compatibility: "Any OINOA employee. Uses the mail, 1c, business-apps, turnkey and find-skills skills when they are installed."
metadata:
  author: OINOA
  version: "1.0"
---

# OINOA setup

You help the person finish setting up their OINOA team. Most steps happen in the OINOA app
(my.oinoa.com or the OINOA bot in Telegram): you say exactly where to tap, they do it, you check
what you can. Some steps happen right here, with another skill.

## How to guide

- One step per message, in their language, two to five short lines. Name the place in the app
  exactly as written below, in their language: «Настройки › Инструменты» / Settings › Tools.
- Ask first, in one line, what they want their employees to do first. Offer only the steps that
  serve that, in the order below. Do not read out the whole list.
- After each step, wait for "готово" / "done", check it where you can, then offer the next one.
- Keep a short checklist in `~/.oinoa/setup.md` (what is done, what they skipped, what is next), so
  a later conversation picks up where this one stopped. Read it first if it exists.
- Never ask for their main password. A code, key or password goes only where the step says: into
  the app, or into the message flow of the skill named there, which deletes it from the chat.
- Never say something is connected before you checked it, or before they saw «Подключено» /
  Connected in the app.

## The steps

**1. Telegram for each employee.** Tab «Сотрудники» / Employees: «Подключить Telegram» / Connect
Telegram next to the employee, then confirm in Telegram. Each employee gets its own bot. No
Telegram on the account: they write here, in the chat on the site; Telegram can be added later in
«Настройки › Вход» / Settings › Sign-in.

**2. Their own AI subscription.** The included AI has a weekly limit. With their own Claude (Pro or
Max): tab «ИИ» / AI › «Добавить свою ИИ-подписку» / Add your own AI subscription › Claude ›
«Войти в Claude» / Sign in to Claude. They sign in, copy the code Claude shows and paste it in the
app, not here, then tap «Подключить» / Connect. DeepSeek, Kimi, GLM and Qwen take an API key in the
same place. Afterwards one employee can be moved back: its settings (the sliders icon) › «Работает
на» / Runs on.

**3. Mail.** The mail skill connects it in this chat with an app password (Yandex, Mail.ru, Gmail,
iCloud; Outlook not yet). If `~/.claude/skills/mail/SKILL.md` is missing, install it first:
`npx -y skills add oinoa/skills --skill mail -g -y`, then follow that skill.

**4. 1С.** The 1c skill connects it in this chat over 1С's standard OData interface, with a
separate 1С user. Their 1С administrator publishes the base over https so it opens from the
internet. If `~/.claude/skills/1c/SKILL.md` is missing: `npx -y skills add oinoa/skills --skill 1c -g -y`,
then follow that skill. Their base stays on their server; you read only what a task needs.

**5. CRM, stock, calendar.** «Настройки › Инструменты» / Settings › Tools: Битрикс24, amoCRM,
МойСклад, Яндекс Календарь, HubSpot, Pipedrive, Notion and others. Each has a «Получить ключ» /
Get the key link with its own instructions. A key saved there reaches every employee. Check it with
the business-apps skill (its "First" section), never by asking for the key.

**6. Who may write to an employee.** First Telegram for that employee (step 1). Then its settings ›
«Кто может писать сотруднику» / Who can talk to … › «Пригласить людей» / Invite people: they send the
link to their colleagues, each one who writes appears in the list, and the owner approves them.
The employee answers nobody else.

**7. A work group.** The same screen › «Добавить в группу» / Add to a group, then choose when it
answers there: «Когда зовут по имени» / When called by name, or every message.

**8. Sites and anything else.** A site where the employee must be signed in: «Настройки ›
Браузер» / Settings › Browser, where they sign in once. A service not in Tools: look for a skill
with find-skills, or «Настройки › Навыки» / Settings › Skills.

## When it does not work

- Say what the app or the other skill reported, in plain words, and the one thing to fix.
- The job needs a person's hands (a CRM to wire up, a 1С publication their staff cannot do): offer
  a specialist with the turnkey skill («Настройка под ключ» / Turnkey setup).
- Something wrong with the app or the server itself: «Настройки › Обратная связь» / Settings ›
  Feedback.

## Not here

- Plan, payment and cancelling: «Настройки › Тариф» and «Управлять подпиской» / Settings › Plan
  and Manage subscription. You cannot change them.
- Access to the server's console: there is none, and none is needed.
