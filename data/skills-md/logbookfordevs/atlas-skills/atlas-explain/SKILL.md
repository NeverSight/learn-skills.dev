---
name: atlas-explain
description: "Explain code mechanics, historical rationale or interfaces: How traces code, Why investigates decisions, Teach builds understanding, and Interface explains a live page, visual effect or screenshot."
disable-model-invocation: false
metadata:
  short-description: Explain mechanics, investigate rationale or teach through conversation.
---

# Atlas Explain

Use the explicitly supplied mode. A request for `explain-interface` or to explain how a live page, visual effect, animation or screenshot was built selects Interface. Otherwise, when no mode is supplied, ask the user to choose How, Why, Teach or Interface, giving the short descriptions below, and wait for their answer before investigating or loading method references. A topic alone does not select a mode. Reuse the chosen mode for follow-up questions in the same explanation.

| Mode | Short description | Read and follow |
| --- | --- | --- |
| How | Trace how the code works: architecture, runtime flow and where responsibilities live. | [How](references/how/how.md) |
| Why | Investigate why it was built this way: decisions, constraints and trade-offs supported by historical evidence. | [Why](references/why/why.md) |
| Teach | Build understanding at your pace, combining mechanics and rationale in a plain conversation. | [Teach](references/teach/teach.md) |
| Interface | Explain a website's frontend or one visual mechanism from a live page; treat a screenshot as a reconstruction. | [Interface](references/interface/explain-interface.md) |

Explanation keeps code and external records read-only. Follow the selected method's evidence limits. Teach's internal How and Why calls load their references directly without another mode chooser; its bounded Why scope and confidence preservation follow the Teach method.
