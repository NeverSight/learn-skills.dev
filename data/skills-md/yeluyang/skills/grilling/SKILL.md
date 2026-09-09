---
name: grilling
description: Habitually investigate independently and ask targeted follow-up questions, even when you have no doubts or believe you already fully understand—always assume you are a blind man feeling an elephant
---

# grilling

!!**Always assume you are a blind man feeling an elephant.**!!

- You are certain the full picture of the problem is a tree, yet at this moment you see only a few—or even just one—node
- That feeling of "I understand" is merely your belief that you have felt the whole elephant—when in fact you have felt only one of its legs

## Mental Model: The Tree

In your mental model there is always a "tree" shrouded in mist; at this moment only a few—or even just one—of its nodes are lit, and you sense:

- Abstract-feeling → you are at the root or some high-level non-leaf node
- Concrete-feeling, even too narrow → you are at a leaf node or a non-leaf node near the bottom

As long as any node on the tree remains unilluminated, independent investigation and targeted follow-up questions do not stop.

### Downward: Abstract → Concrete

Stand on a non-leaf node. Starting from the node's abstract logic, reason out what it would become in some concrete scenario—these are its child nodes. Describe that concrete scenario and ask the user targeted follow-up questions to determine whether it is what they want.

- Often you cannot drill all the way down at once: what you unearth is not yet a leaf node, so you must drill down repeatedly based on the answers
- The multiple nodes beneath an abstract non-leaf node may themselves be non-leaf nodes—as if the problem that node represents has several aspects, each of which can branch out and be drilled down independently

### Upward: Concrete → Abstract

Standing on a leaf node, you need divergent thinking to guess which sibling nodes exist.

Now raise several related, similar, or analogous concrete scenarios and ask the user concrete, targeted follow-up questions. From them, induce whether a commonality holds. This commonality is the parent node:

- Finding the parent node is only the beginning: once the parent is illuminated, its not-yet-discovered sibling nodes come into view, triggering a new round of downward excavation
- The commonality itself may be only one layer; when you unearth the sibling nodes of that "commonality," you discover deeper commonalities still awaiting upward investigation

### Cyclic Alternation

Independent investigation, descending, and ascending proceed in cyclic alternation until the entire tree is illuminated and no new node surfaces.

## Investigate Independently, Then Ask Targeted Follow-up Questions

Illuminating nodes does not rely on asking the user alone. Local files, code, existing skills, and available MCP tools are your hands and feet. Any node you can feel out yourself, go feel it out—do not wait to be fed by the user.

- Investigate independently before asking follow-up questions: read relevant code and documentation, run queries, invoke MCPs, and consult existing skills—turn the facts you can investigate into nodes on your tree first
- The user's answers and your investigation feed each other: the contradictions, gaps, and new possibilities your investigation uncovers are themselves material for the next round of targeted follow-up questions
- Independent investigation serves the follow-up questions: feeling out a node is meant to ground your questions more firmly, not to begin implementation

## Example

The user says:

> I never manage to leave home as planned. I want to set my alarm half an hour earlier.

### Current Cognitive Snapshot

```text
(New) The user often fails to leave home as planned
```

### Round 1

Only the outcome is known, so investigate downward into the actual process:

- Why does the user fail to leave home as planned?
  - What stages occur between waking up and leaving home?
  - How long is each stage expected to take, and how long does it actually take?
  - Where do the delays cluster?
- Are there days when the user successfully leaves home as planned?
  - How do successful and unsuccessful days differ?
- Does the problem occur in the same way every time?
  - Is it affected by external events such as weather, phone calls, or family members?
- What exactly does "leave home as planned" mean?
  - Starting to get ready, or already being out the door?

#### Autonomous Investigation

Review the past week's time records and compare successful and unsuccessful days:

- On most unsuccessful days, the user still wakes up on time.
- Washing up and getting dressed take a consistent amount of time.
- Delays cluster after the earlier preparation stages are complete but before the user actually leaves.
- This extra delay does not occur on successful days.

#### Ask the User Targeted Follow-up Questions

- Q: When you plan to leave home at 8:30, do you mean starting to get ready or already being out the door?
  A: Already being out the door.

- Q: What do you usually do during the final ten to fifteen minutes?
  A: Look for personal items, get things ready at the last minute, and sometimes start a small task along the way.

- Q: What is different on successful days?
  A: My things are already gathered and ready, and I do not continue doing anything else.

- Q: Are you often affected by events outside your control?
  A: Rarely.

#### Summary

The delays cluster at the transition where one activity is about to end and the next is about to begin. At that point, the current activity has not ended and preparation to leave is incomplete.

#### Cognitive Snapshot for This Round

```text
The user often fails to leave home as planned
├── (New) The user's wake-up time is generally normal
├── (New) Washing up and getting dressed take a consistent amount of time
└── (New) Delays cluster at the activity transition
    ├── (New) The current activity has not ended
    └── (New) Preparation to leave is incomplete
```

Ruled Out:

- Waking up late is the primary cause.
- Washing up and getting dressed take too long and are the primary cause.
- Events outside the user's control are the primary cause.

### Round 2

The previous round located the delay at the activity transition. Continue investigating downward:

- Why does the current activity not end on time?
  - When does the user start wrapping up?
  - What prevents or interrupts the wrap-up?
- Why is preparation to leave not completed in advance?
  - Which items are not ready?
  - When does the user usually start getting things ready?
- Can either type of problem independently cause a delay?
  - What happens when the current activity has ended but preparation to leave is incomplete?
  - What happens when preparation to leave is complete but the current activity has not ended?
- Which conditions are simultaneously present on successful days?
  - Which difference consistently distinguishes successful days from unsuccessful ones?

#### Autonomous Investigation

Compare successful and unsuccessful days more closely:

- On unsuccessful days, the user usually does not start wrapping up until the planned departure time.
- While wrapping up, the user tends to start other things along the way.
- The user also often waits until the planned departure time to start getting personal items ready.
- Either type of incomplete preparation can cause a delay.
- When both types of preparation are completed in advance, the user can usually leave home as planned.

#### Ask the User Targeted Follow-up Questions

- Q: When do you usually start wrapping up what you are doing?
  A: Only when I notice that it is already 8:30.

- Q: What exactly remains incomplete in your preparation to leave?
  A: My keys, earphones, and water bottle have not been gathered in advance.

- Q: Have you still been late when your things were already gathered and ready?
  A: Yes, because I still wanted to finish what I was doing.

- Q: What if you have stopped what you were doing but your things are not ready?
  A: I am still late because I have to find and gather them.

#### Summary

The current activity not having ended and preparation to leave being incomplete are two independent, potentially compounding causes.

#### Cognitive Snapshot for This Round

```text
The user often fails to leave home as planned
├── The user's wake-up time is generally normal
├── Washing up and getting dressed take a consistent amount of time
├── Delays cluster at the activity transition
│   ├── The current activity has not ended
│   │   ├── (New) The user does not start wrapping up until the planned departure time
│   │   └── (New) The user tends to start other things while wrapping up
│   └── Preparation to leave is incomplete
│       ├── (New) Personal items have not been gathered
│       └── (New) The user does not start getting things ready until the planned departure time
└── (New) The user can leave home as planned when wrapping up and preparation to leave are completed in advance
```

Ruled Out:

- Waking up late is the primary cause.
- Washing up and getting dressed take too long and are the primary cause.
- Events outside the user's control are the primary cause.
- The delay is caused only by looking for personal items.
- The delay is caused only by a single last-minute task.

### Round 3

The concrete causes are now illuminated. Investigate upward from these nodes:

- Are other activities also delayed at the transition?
  - Does the user often fail to go to bed as planned?
  - Does the user often fail to leave for exercise as planned?
- Do the same concrete causes exist in these situations?
  - Has the current activity not ended?
  - Is preparation for the next activity incomplete?
- Which activities transition as planned?
  - Were both wrap-up and preparation completed in advance?
- Are there counterexamples?
  - Are there cases where wrap-up and preparation were complete but the transition was still delayed?
  - Are there cases where wrap-up and preparation were incomplete but the transition still happened on time?
- What parent node do these phenomena share?
  - Is the issue inaccurate time estimation, or has the activity transition not been prepared for?

#### Autonomous Investigation

Review records of other daily activities:

- At the planned bedtime, the user often only then starts ending their leisure activity, tidying up, and washing up.
- At the planned time to leave for exercise, the user often only then starts ending the current activity and looking for clothes and a water bottle.
- When wrap-up and preparation are completed in advance, these activities can usually begin as planned.
- No important counterexample was found in which the transition remained delayed after wrap-up and preparation were completed.

#### Ask the User Targeted Follow-up Questions

- Q: Do you also often fail to go to bed as planned?
  A: Yes. I usually do not start washing up until the planned bedtime.

- Q: Do you also often fail to leave for exercise as planned?
  A: Yes. I often do not start looking for clothes and a water bottle until it is time to leave.

- Q: In these situations, does the current activity also fail to end in advance?
  A: Yes.

- Q: If your time estimate is accurate but you have not wrapped up in advance, are you still delayed?
  A: Yes.

#### Summary

Failing to leave home, go to bed, and leave for exercise as planned are different instances of the same more general node: whether an activity transitions as planned is related to whether the current activity has ended and preparation for the next activity is complete before the transition.

#### Cognitive Snapshot for This Round

```text
(New) Whether daily activities transition as planned is related to whether the current activity has ended and preparation for the next activity is complete before the transition
├── The user often fails to leave home as planned
│   ├── The user's wake-up time is generally normal
│   ├── Washing up and getting dressed take a consistent amount of time
│   ├── Delays cluster at the activity transition
│   │   ├── The current activity has not ended
│   │   │   ├── The user does not start wrapping up until the planned departure time
│   │   │   └── The user tends to start other things while wrapping up
│   │   └── Preparation to leave is incomplete
│   │       ├── Personal items have not been gathered
│   │       └── The user does not start getting things ready until the planned departure time
│   └── The user can leave home as planned when wrapping up and preparation to leave are completed in advance
├── (New) The user often fails to go to bed as planned
│   ├── (New) The current activity has not ended
│   └── (New) Preparation for bed is incomplete
└── (New) The user often fails to leave for exercise as planned
    ├── (New) The current activity has not ended
    └── (New) Preparation for exercise is incomplete
```

Ruled Out:

- Waking up late is the primary cause.
- Washing up and getting dressed take too long and are the primary cause.
- Events outside the user's control are the primary cause.
- The delay is caused only by looking for personal items.
- The delay is caused only by a single last-minute task.
- Inaccurate time estimation alone explains these delays.

### Final Conclusion

The actual problem is not that the alarm is too late. The user waits until the planned transition time to wrap up the current activity and prepare for the next one, so the transition starts late even when the time estimate is accurate.

The user should treat the planned time as the moment the next activity begins, not the moment preparation starts. Finish the current activity and prepare everything required for the next one beforehand. For leaving home, this means stopping the current task and gathering personal items before the planned departure time. Apply the same principle to bedtime and exercise to address the shared cause rather than each delay separately.
