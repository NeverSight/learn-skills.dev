---
name: magpie-setup
description: Set magpie (usemagpie.ai) up for what the user wants through its `magpie` command — add a vendor's API key or a subscription, point Claude Code, Codex, OpenCode or another agent at a model, build routing groups with fallbacks and rules (by time of day, length, image, folder or compaction), give other devices gateway keys with budgets, rename, price or turn off models, and give every agent the same MCP servers, instructions and web search. Use when the user asks to configure, set up or change magpie (配置 magpie / 设置 magpie), or describes a setup in their own words ("use DeepSeek in Claude Code", "cheaper model during peak hours", "fall back to my relay when Claude runs out").
---

# Set magpie up

[magpie](https://usemagpie.ai) puts every model the user has (subscriptions,
coding plans, API keys) behind one local gateway and points their coding
agents at it. Everything its app does has a `magpie` command. Turn what the
user asks for into those commands, run them, and show what changed.

## Before anything

1. Find the command: `magpie --version`. If it isn't found, the app can put
   it on the PATH (Settings › About › Command line › Add to PATH), or run the
   app's own program: `/Applications/magpie.app/Contents/MacOS/magpie` on a
   Mac, `%LOCALAPPDATA%\magpie\magpie.exe` on Windows.
2. Read what is there before changing it:

   ```sh
   magpie ls            # the agents here, and the model each is on
   magpie providers     # vendors and keys
   magpie accounts      # signed-in subscriptions
   magpie groups        # routing groups
   magpie models        # every model an agent can pick, as provider/model
   ```

3. Check the exact form of a command with `magpie <command> --help` (or
   `magpie help` for all of them). `-h` or `--help` anywhere only prints
   help and changes nothing. If a command or option below is refused as
   unknown, the user's magpie is older: `magpie update` installs the newest,
   after asking them.

## How to work

- Do what the user asked and nothing more. Don't change an agent, group or
  key they didn't mention.
- Before a change that replaces or removes something (`rm`, `default`,
  `group add` with a name already in use, `provider models <id> <ids…>`,
  which replaces the list), say what will go and ask.
- Before a larger setup, `magpie save before-setup` keeps every agent's
  settings as a profile; `magpie use before-setup` puts them back.
- After each change, show the result (`magpie group <id>`, `magpie <agent>`,
  `magpie providers`) in a line or two, not the whole output.
- Use the commands, never edit magpie's own files (`providers.json`,
  `library.json` and the rest): the commands check values, lock the files
  and write the agents' configs to match.
- An agent reads its model at start. After pointing one at a new model, tell
  the user to restart it; if it is the agent you are running in, the change
  takes effect in its next session.
- An API key goes on the command line as the user gave it. Don't repeat it
  back, and never write it into a file in a project.

## Models and keys

Model ids are `provider/model`, as `magpie models` lists them (a bare model
id works when one provider serves it). A routing group is `group/<id>`.

```sh
magpie presets                              # vendors magpie knows: just add a key
magpie provider add deepseek sk-…           # a preset; again adds a second one (deepseek-2)
magpie provider add "My Relay" url=https://relay.example.com/v1 key=sk-…        # any OpenAI-compatible API
magpie provider add "Own Claude" anthropic=https://gw.example.com key=sk-…      # an Anthropic-compatible one
magpie provider add ollama url=http://127.0.0.1:11434/v1                        # a local model server
magpie provider test <id>                   # send a tiny request to each endpoint
magpie provider models <id>                 # fetch its model list again
magpie provider models <id> model-a model-b # the models it serves, when the vendor has no list
magpie provider fallback <id> <provider/model>…   # where requests go when it is out of quota or down
magpie provider off|on <id>                 # stop using it, kept; or use it again
```

`magpie provider --help` lists every `k=v` a custom vendor takes (headers,
balance endpoint, context length, user agent).

Subscriptions are signed in through the browser, by the user:

```sh
magpie accounts add claude      # or codex, gemini, antigravity
magpie accounts add copilot
magpie plugin add <name>        # a community plugin's subscription (magpie plugin --help)
magpie plugin login <provider>
```

Start the sign-in and tell the user to finish it in the window that opens.
To limit a subscription account: `magpie provider account-cap <id> <account> 70`
(use up to 70% of each window), `magpie provider rpm <id> 20`.

## Point an agent at a model

```sh
magpie agents                         # every agent magpie supports
magpie models claude                  # what Claude Code can pick, and why others aren't
magpie claude deepseek/deepseek-chat  # set its model (also: codex, gemini, opencode, pi, …)
magpie codex effort high              # another field (magpie codex --help lists them)
magpie claude default                 # take magpie out: back to what it had before
```

Subagents can have a model of their own. Set it here rather than asking the
lead agent to name a model each time, which it does only sometimes:

```sh
magpie codex subagent_model deepseek/deepseek-chat   # every Codex subagent, whatever its lead asks for
magpie codex subagent_model group/cheap              # or a routing group
magpie codex subagent_model default                  # back to the lead's pick
magpie codex subagent_effort low                     # their reasoning effort
magpie claude subagent deepseek/deepseek-chat        # Claude Code's subagents
```

## Routing groups

A group is several models an agent picks as one. `routing=order` tries them
in order (the next when one can't answer); `smart` (default) prefers the
subscription renewing soonest; `usage`, `pace`, `rotate`, `weight` and
`manual` are in `magpie group --help`.

```sh
magpie group add "Opus anywhere" models=claude/claude-opus-5-5,openrouter/anthropic/claude-opus-5.5 routing=order
magpie group set opus-anywhere models+=deepseek/deepseek-chat   # append; models-= drops one
magpie group set opus-anywhere stays=session                    # keep a conversation on one account
magpie group add free-pool models='openrouter/*:free' routing=order   # a pattern; quote it
magpie group template                     # ready-made groups from the user's own models
magpie claude group/opus-anywhere         # an agent uses the group
```

`group add` with a name already in use replaces that group; check
`magpie groups` first. `magpie group template <kind>` makes the group at
once, so list the kinds and ask before making one.

Rules decide which model a turn goes to first. The first rule that matches
wins; the group's other models stay behind it as fallbacks.

```sh
magpie group rule add <group> use=<model> time=09:00-18:00 days=mon-fri tz=Asia/Shanghai   # peak hours elsewhere
magpie group rule add <group> use=<model> time=09:00-18:00@Asia/Shanghai                   # the same zone, written after the hours
magpie group rule add <group> pause=<model> time=22:00-08:00     # leave a model out overnight
magpie group rule add <group> use=<model> tokens=200k            # long requests
magpie group rule add <group> use=<model> images                 # requests with an image
magpie group rule add <group> use=<model> compact                # an agent's compaction summary
magpie group rule add <group> use=<model> folders=~/work/acme    # one project
magpie group rule add <group> use=<model> agents=codex           # one agent
magpie group rule add <group> use=<model> intent="a quick question" classifier=<small model>
magpie group rule <group>             # the rules, numbered
magpie group rule rm <group> <n>
magpie group rule mv <group> <n> <to>
```

`<model>` must be one of the group's models. Without `tz=`, times are on
the clock of the computer magpie runs on. `magpie group rule --help` has
every condition.

## Other devices, people and budgets

Other computers and apps reach the gateway with a gateway key, once
Settings › Network and sharing › Share on local network is on.

```sh
magpie gateway-key add laptop                 # prints the new key
magpie gateway-key list
magpie gateway-key limit <id> month --cost 20 # a budget in USD; day, week, month, 10d, 5h
magpie gateway-key limit <id> add day --tokens 2m   # one more limit; every one must have room
magpie gateway-key models <id> 'deepseek/*' group/daily   # only these models
magpie gateway-key limit <id> off
```

A Claude, ChatGPT or other subscription is for its owner's own use. Never
set up a key that lets another person use one: hold any key you make for
someone else to API-key providers with `gateway-key models`.

## Models agents are shown

```sh
magpie model name deepseek/deepseek-chat "DS Chat"   # the name it goes by everywhere
magpie model disable '*preview*'                     # refused on every route; magpie model enable undoes it
magpie model price my-relay/gpt-x 1,4,0.1,1.25       # USD per 1M: input, output, cache read, cache write
magpie model context my-relay/claude-opus-5-5 1m
magpie visible zed deepseek,daily                    # an agent shown only these providers, families or groups
magpie visible zed all
```

## Everything agents share

```sh
magpie library                                       # what each agent is given
magpie library mcp add context7 https://mcp.context7.com/mcp agents=claude,codex
magpie library mcp add <name> <command> <args…>      # a stdio server
magpie library instructions set notes.md             # instructions every agent reads (- for stdin)
magpie library instructions agents claude,codex
magpie library skill agents <skill> claude,codex     # skills are added from the app's Library › Market
magpie search add tavily tvly-…                      # web search for models that can't search themselves
magpie search add you                                # You.com, free with no key
```

## Running and keeping it

```sh
magpie healthcheck                 # exit 0 when the gateway answers
magpie daemon install              # a server: the gateway as a service, started at boot or login
magpie web --lan                   # the app's window in a browser, for a machine without a desktop
magpie backup <file>               # everything in one file, sealed with a passphrase; magpie restore <file>
magpie webdav on <address>         # the same setup on every computer (also s3, github)
magpie usage 7d                    # what each agent, model and account used
magpie quota                       # what is left of each subscription and key
```

## Don't

- Don't run `magpie quota reset` (it spends one of a Codex account's resets),
  `magpie library skill rm --all`, `magpie group auto off`, `magpie provider rm`,
  `magpie accounts import` (it signs the other tool out) or
  `magpie daemon install` unless the user asked for exactly that.
- Don't sign the user in or out of anything, or switch the account an agent
  is signed in to, without asking.
- Don't run magpie with sudo.
