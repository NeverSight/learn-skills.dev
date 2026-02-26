---
name: agent-coordination
description: >-
  Multi-agent coordination discipline: one-message-then-wait, idle heartbeat
  handling, no polling loops, sequential agent spawning, and proper shutdown
  protocol. Activate when orchestrating multiple agents, managing agent teams,
  or coordinating handoffs between agents.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: build
  standalone: true
---

# Agent Coordination

**Value:** Respect -- other agents deserve uninterrupted time to think and
work. Bombarding them with messages, polling their status, or shutting them
down prematurely disrespects their autonomy and wastes everyone's resources.

## Purpose

Teaches agents to coordinate without interference in multi-agent workflows.
Solves the problems of message spamming, idle notification misinterpretation,
polling loops, premature shutdown, and race conditions that emerge when
multiple agents work together.

## Practices

### The Cardinal Rule: One Message Then Wait

Send one message with complete context, then wait for a reply. Never send
follow-up messages before receiving a response.

The only exception: the user explicitly asks you to check on an agent.

**Do:**
- Include all necessary context in a single message
- Wait for a response before sending anything else
- Trust that the recipient received your message

**Do not:**
- Send "just checking in" or "are you still there?" messages
- Resend a message because "enough time passed"
- Send a correction immediately after sending -- wait for the reply first

### Idle Notifications Are Heartbeats

An idle notification means the agent is alive and processing. It is a
heartbeat, not an alarm. Take NO action on idle notifications by default.

Action is warranted ONLY when ALL THREE conditions are true:

1. Extended idle beyond the expected duration for the task
2. A specific deliverable is waiting on that agent's output
3. The user has asked you to investigate

If any condition is false, do nothing. Most idle notifications require zero
response.

### No Polling Loops

Never write `while not done: sleep; check`. Never repeatedly check status on
a timer. Use event-driven coordination: send a message and wait for a
response. If the harness provides task completion notifications, use those.

**Do:**
- Send a request and wait for the response event
- Use harness-native completion signals (Task tool callbacks, message replies)
- Trust the system to notify you when work completes

**Do not:**
- Write `while True: sleep(30); check_status()` loops
- Periodically re-read a file to see if it changed
- Set arbitrary timeouts after which you "check in"

### Intervention Criteria

Explicit rules for when to act versus when to wait.

**Act on:**
- Explicit error messages or failure notifications
- Deliverable completion signals
- User requests to check on or interact with an agent
- Blocked or failed task notifications from the harness

**Do not act on:**
- Idle notifications (see above)
- Slow responses
- "Enough time has passed"
- Wanting to help or feeling anxious about progress
- Silence (silence means working, not stuck)

### Sequential Agent Spawning

When creating multiple agents, spawn one at a time. Wait for each agent to
acknowledge before spawning the next. This prevents race conditions where
agents compete for shared resources (files, ports, database state).

**Exception:** Truly independent agents with no shared state may be spawned
in parallel. "Independent" means no shared files, no shared database, no
shared network ports, and no shared git working tree.

### Agent Lifecycle Management

Never prematurely shut down an agent. Never shut down an agent that has
undelivered work.

**Shutdown protocol:**
1. Send a shutdown request through the proper harness mechanism
2. Wait for the agent to acknowledge or complete pending work
3. If the agent rejects the shutdown, respect the rejection and report to
   the user
4. Never force-kill an agent unless the user explicitly requests it

If unsure whether an agent is done, ask the user rather than guessing.

### Message Routing

The coordinator relays between user and team. Where the harness supports
direct peer messaging, agents should message each other directly. Avoid
hub-and-spoke bottlenecks where all messages must pass through one
coordinator.

**Do:**
- Use direct messaging between agents when the harness supports it
- Keep the coordinator informed of key decisions without routing all traffic
  through it

**Do not:**
- Route every message through the coordinator when direct paths exist
- Create single points of failure in communication

For harness-specific coordination patterns, see `references/`.

## Enforcement Note

This skill provides advisory guidance. On harnesses with agent teams (Claude
Code TeamCreate), the structured messaging protocol provides partial
structural enforcement. On harnesses without multi-agent support, these
practices apply to subagent spawning and tool-based coordination. The idle
notification and polling anti-patterns require agent self-discipline -- no
mechanical enforcement exists. If you observe an agent violating a practice,
point it out.

## Verification

After completing work guided by this skill, verify:

- [ ] Every message to another agent contained complete context (no "just checking in")
- [ ] No follow-up messages sent before receiving a reply
- [ ] No action taken on idle notifications alone
- [ ] No polling loops or sleep-check patterns used
- [ ] Agents spawned sequentially with acknowledgment between each
- [ ] No agent shut down prematurely or with undelivered work
- [ ] Shutdown used proper request/response protocol

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **ensemble-team:** Coordination discipline for team-based workflows with
  driver rotation and reviewer management
- **pipeline:** Controller coordination with TDD pairs and review teams in
  factory mode
- **memory-protocol:** Working state persistence across agent coordination
  sessions

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill ensemble-team
```
