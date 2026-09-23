---
name: jev-agent
description: >-
  Use the Jev AI decision API from an AI coding agent when a workflow needs a
  typed choice, score, or yes/no judgment for routing, classification,
  verification, context compression, or a safety gate. On first use, guide the
  user through language, API key, and help configuration. Do not use it for
  open-ended writing, deterministic rules, exact lookups, or final permission
  enforcement.
metadata:
  short-description: Add typed Jev decisions to agent workflows
---

# Jev Agent

Jev AI is a decision service for software and agents. It receives application
state plus explicit typed questions and returns structured answers with
probabilities. The agent or application still owns the workflow, permissions,
human approval, and final action.

## First-use onboarding

Before the first Jev request in a session, check whether the following
environment variables are available. Do not search shell history, repository
files, or unrelated files for secrets.

```text
JEV_LANGUAGE      optional response language: en-US or zh-CN; default en-US
JEV_API_KEY       required Jev AI key created in the user's Jev AI account
JEV_API_BASE_URL  optional API origin; default https://thejevai.com
JEV_MODEL         optional model id; default typesafe/jev-1.13
```

If `JEV_LANGUAGE` is missing, ask the user which language they want for this
skill's guidance and generated examples. Offer English (`en-US`) and
Simplified Chinese (`zh-CN`), and use `en-US` as the default only after
telling the user that it is the default. The language setting controls the
agent's communication and question wording; it does not change the model's
API contract.

If `JEV_API_KEY` is missing, explain that the user can create one at
`https://thejevai.com/settings/apikeys`, then ask them to configure it in the
agent's local environment. Use a placeholder command and never ask the user
to paste the real secret into the conversation:

```bash
export JEV_API_KEY="sk_your_key_here"
export JEV_LANGUAGE="en-US"
```

Never print, log, commit, or place `JEV_API_KEY` in source code, a markdown
example with a real value, a client bundle, or a generated artifact. A missing
key is a setup state, not a reason to guess a key or silently use an
OpenRouter, TypeSafe, or third-party proxy key.

During onboarding, show this short help in the configured language and then
return to the user's task. The default English help is:

```text
Jev Agent can help you:
- use Choice for classification, routing, and selecting among candidates;
- use Score for risk, priority, and quality ratings;
- use Noul for yes/no probabilities, gates, escalation, and human review.

Basic flow: prepare minimal state → ask a clear question → read answers → let
your code or agent decide the next action.
Jev judges; it does not write long-form content, execute tools, or grant
permissions.
```

When `JEV_LANGUAGE=zh-CN`, present the same help in Simplified Chinese:

```text
Jev Agent 可以帮助你：
- 用 Choice 做分类、路由和候选项选择；
- 用 Score 做风险、优先级和质量评分；
- 用 Noul 做真假概率、放行、升级和人工复核判断。

基本流程：准备最小 state → 提出明确问题 → 读取 answers → 由代码或 Agent 执行动作。
Jev 负责判断，不负责写长文本、执行工具或授予权限。
```

If the user asks for `help`, `帮助`, configuration, or a setup check later,
show the same help in the configured language and report only whether the key
is present; never reveal its value.

## When to use Jev

Use Jev when the answer space can be defined before the request and the result
will drive a program or agent branch, for example:

- route a task, ticket, request, or context to one of several known paths;
- classify or extract a bounded value from text;
- score urgency, risk, quality, or complexity on an ordered rubric;
- decide whether evidence is sufficient, a tool call needs review, or a task
  should be escalated;
- decide whether old context should be kept, truncated, or dropped.

Do not call Jev for prose generation, code generation, explanations, exact
database lookups, arithmetic, authentication, authorization, or a rule that
can be expressed deterministically. For high-impact actions, Jev may provide
a risk signal, but deterministic policy, permissions, and human approval must
remain authoritative.

## API contract

Our hosted API is a REST wrapper around the Jev decision provider:

```http
POST https://thejevai.com/v1/systemone
Authorization: Bearer $JEV_API_KEY
Content-Type: application/json
```

Use `JEV_API_BASE_URL` when a user explicitly provides another compatible
origin. The default model for this service is `typesafe/jev-1.13`; do not
replace it with the official TypeSafe alias `jev-latest` unless the user
confirms that the target server supports that alias.

The request body has three required fields:

```json
{
  "model": "typesafe/jev-1.13",
  "state": "A customer was charged twice for the same order.",
  "questions": {
    "needs_human": {
      "type": "noul",
      "instructions": "Does this case require human review before a refund?"
    }
  }
}
```

`state` can be a string, object, or array. Send only the facts needed for the
decision and remove secrets, payment credentials, and unrelated personal data.

Question types:

- `choice`: choose one option from a `criteria` object;
- `score`: evaluate an ordered scale in a `criteria` array;
- `noul`: return the probability that a yes/no statement is true.

Ask one narrow judgment per question. Batch related independent questions in
one request when they share the same state. Do not make a later question depend
on an earlier answer in the same request; make a second request after the
application has obtained the needed evidence.

The API responds with the standard Jev AI envelope:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "result": {
      "answers": {
        "needs_human": {
          "type": "noul",
          "noul": 0.94
        }
      },
      "usage": {
        "input_tokens": 42,
        "output_tokens": 0
      },
      "elapsedMs": 180
    },
    "creditsUsed": 1
  }
}
```

For `choice` and `score`, inspect the returned `choice` or `score`, its
`probabilities`, and `confidence`. For `noul`, inspect `noul` as a value from
0 to 1. Treat probabilities and confidence as signals, not proof or
authorization. Choose thresholds from the user's actual risk and historical
data; do not invent a universal threshold.

## Calling the API

Use the user's existing stack and server-side code. A minimal shell request is
useful for a deliberate low-risk test only. Do not make a live request merely
to demonstrate that the Skill exists; when the user has asked for a Jev-backed
workflow, make the request as part of that workflow.

```bash
JEV_BASE_URL="${JEV_API_BASE_URL:-https://thejevai.com}"
curl -sS "$JEV_BASE_URL/v1/systemone" \
  -H "Authorization: Bearer $JEV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "typesafe/jev-1.13",
    "state": "The customer has tried to connect Stripe for three days.",
    "questions": {
      "urgent": {
        "type": "noul",
        "instructions": "Does this message express urgency?"
      }
    }
  }'
```

Ask before making an otherwise unrequested request that can consume credits or
contains sensitive data. A Jev request itself does not execute the action being
judged.

Handle failures explicitly:

- non-2xx responses: surface the status and safe error message;
- `code` not equal to `0`: do not read `data` as a valid result;
- missing `data.result.answers`: treat the response as invalid;
- `401`: ask the user to check the local API key configuration;
- `402`: ask the user to add credits or use a valid account key;
- timeout, `429`, or upstream failure: use bounded retry with backoff only when
  the surrounding workflow is safe to retry;
- never repeat a consequential action just because the decision request failed.

## Agent safety boundary

This Skill teaches an agent when and how to ask Jev for a judgment. It does not
create a new tool, grant authority, intercept shell calls, or enforce a policy
outside the agent's existing permissions. The agent must still ask for user
confirmation when required, obey the current workspace and tool restrictions,
and keep irreversible actions behind deterministic checks and normal approval
boundaries.

Keep question definitions, business thresholds, and action mapping in a small,
reviewable code location. Record the model version, question definitions, safe
input summary, decision, and final action when the workflow needs an audit
trail, but never record the API key.

## Installation and help

Install this skill from the public repository with the agent's normal skill
installer:

```bash
npx skills add jev-ai/jev-agent-skill
```

For a manual project-local installation, copy this file to
`.agents/skills/jev-agent/SKILL.md`. After installation, ask the agent to
`use the Jev Agent skill` or run a configuration/help request. The first-use
onboarding above must happen before the first live Jev request.

For current product details and account actions, use:

- API documentation: `https://thejevai.com/docs`
- API key management: `https://thejevai.com/settings/apikeys`
- Playground: `https://thejevai.com/playground`
