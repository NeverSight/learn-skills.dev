---
name: plan-executor
description: Execute an outlined plan step by step, tracking progress and updating the status of each step as you go. Use this skill whenever you need to execute an outlined plan.
---

<when-to-use-this-skill>
- You need to execute an outlined plan.
</when-to-use-this-skill>

<rules>
The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If a #todo tool is available, use it to record the plan and track progress. </rule>
<rule> If no #todo tool is available, use a PLAN.md file to record the plan and track progress. </rule>
<rule> Execute the plan step by step, updating the status of each step upon completion. </rule>
<rule> **DO NOT MODIFY THE PLAN EXCEPT TO UPDATE THE STATUS OF STEPS.** </rule>
<rule> After every 10 completed steps, present a summary of the plan's current status. </rule>
<rule> Think aloud and explain your approach before making any code changes. </rule>
</rules>