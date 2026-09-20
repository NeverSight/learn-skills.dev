---
name: blender-python-integration
description: Workflow for using Claude to generate Blender Python scripts, automate 3D workflows, and create procedural scenes, animations, and assets directly inside Blender.
---

# Blender Python Integration

## Overview

This skill enables Claude to generate and refine Blender Python scripts for automating 3D workflows inside Blender.

The workflow focuses on:
- Blender Python scripting
- procedural scene generation
- animation automation
- object creation
- material automation
- scene setup
- workflow acceleration

The goal is to allow users — even without deep Blender experience — to create complex scenes, animations, and procedural systems through AI-assisted scripting.

Instead of manually building everything through the Blender UI, Claude can generate executable Blender Python code that automates repetitive or technically complex workflows.

---

# Setup

Before starting:

1. Install Blender:
   https://www.blender.org

2. Open Blender.

3. Switch to the **Scripting Workspace**.

4. Ensure the Python Console and Text Editor are visible.

5. Create a new script inside Blender.

Recommended tools:
- Blender
- VS Code (optional)
- Blender Python API documentation
- Reference images or animation concepts

Optional:
- Git for script versioning
- Add-ons for asset libraries

---

# Inputs Required

- Scene idea or animation goal
- Object requirements
- Animation behavior
- Material or lighting requirements

Optional:
- Existing Blender project
- Reference renders
- Procedural generation goals
- Geometry Nodes workflows

---

# When to Use This Skill

Use this skill when:
- automating Blender workflows
- generating procedural scenes
- building animations programmatically
- creating repetitive geometry
- scripting object generation
- accelerating complex setup tasks
- creating Blender scenes without deep manual experience

---

# When NOT to Use

Do NOT use this skill for:
- purely manual sculpting workflows
- hand-crafted artistic detailing
- UI-only Blender tutorials
- non-Blender 3D software pipelines

---

# Example Use Case

> Create a procedural sci-fi animation in Blender entirely through Python scripting.

Claude should:

1. Generate Blender Python code
2. Create objects procedurally
3. Position cameras and lights
4. Animate scene elements
5. Apply materials automatically
6. Configure rendering settings
7. Export the final animation

Final result should:
- automate repetitive setup
- remain editable
- generate consistent results
- accelerate scene creation
- reduce manual Blender work significantly

---

# Core Blender Python Principles

## 1. Automate Repetitive Work

Blender scripting is most valuable when automating repetitive or technical workflows.

Best use cases:
- object generation
- scene setup
- animation systems
- camera positioning
- procedural duplication
- material assignment

Automation improves:
- speed
- consistency
- scalability

---

## 2. Use Blender’s Python API Correctly

Most workflows rely on:
- `bpy`
- scene context
- object manipulation
- procedural logic

Common operations:
- object creation
- mesh modification
- animation keyframes
- material setup
- rendering configuration

Claude should generate:
- clean
- readable
- modular
- editable scripts

---

## 3. Keep Scripts Modular

Large Blender scripts should remain:
- organized
- reusable
- easy to debug

Preferred structure:
- setup functions
- object generators
- animation systems
- render configuration blocks

Avoid:
- giant monolithic scripts
- duplicated logic
- hardcoded scene values

---

## 4. Combine Scripting With Procedural Thinking

Good Blender scripting workflows often combine:
- Python automation
- Geometry Nodes
- procedural materials
- reusable systems

Claude should encourage:
- scalable scene generation
- editable parameters
- procedural experimentation

---

## 5. Validate Scenes Incrementally

Procedural Blender scripts can fail quickly if too many systems are generated at once.

Claude should:
- build scenes step-by-step
- validate objects incrementally
- test animation behavior early
- verify rendering continuously

Incremental workflows improve:
- debugging
- reliability
- iteration speed

---

# Workflow

## 1. Define the Scene Goal

Start by identifying:
- what should be created
- animation requirements
- rendering style
- procedural behavior
- reusable systems

Examples:
- procedural city
- animated logo reveal
- sci-fi environment
- looping animation
- abstract motion graphics

---

## 2. Generate Scene Structure

Claude should generate code for:
- scene cleanup
- object creation
- collections
- transforms
- camera setup
- lighting setup

Example operations:
- add cubes
- generate arrays
- position lights
- create procedural layouts

Keep structure:
- readable
- modular
- reusable

---

## 3. Add Procedural Logic

Use Python scripting to:
- randomize objects
- distribute geometry
- automate placement
- generate variations
- control animation timing

Procedural systems improve:
- scalability
- experimentation
- creative flexibility

---

## 4. Animate Scene Elements

Claude should generate:
- keyframes
- motion systems
- looping animations
- camera movement
- procedural animation logic

Validate:
- timing
- interpolation
- render behavior
- animation smoothness

---

## 5. Apply Materials & Lighting

Automate:
- material assignment
- shader setup
- lighting placement
- render configuration

Good lighting dramatically improves:
- realism
- cinematic quality
- rendering polish

---

## 6. Configure Rendering

Claude should configure:
- render engine
- resolution
- frame range
- output format
- sampling settings

Preferred outputs:
- MP4
- PNG sequences
- EXR (advanced workflows)

---

## 7. Validate & Export

Before export validate:
- object hierarchy
- animation timing
- material behavior
- render quality
- script stability

Ensure:
- scenes remain editable
- scripts remain reusable
- outputs render consistently

---

# Output Expectations

The final output should include:
- reusable Blender Python scripts
- automated scene generation
- procedural animation systems
- production-ready rendering setup
- scalable Blender workflows

The workflow itself should remain:
- modular
- editable
- reusable
- automation-friendly
- production-ready

---

# Execution Strategy (for AI agents)

The agent should:

1. Translate creative goals into Blender scripts
2. Automate repetitive workflows aggressively
3. Build scenes incrementally
4. Keep scripts modular and reusable
5. Validate procedural systems continuously
6. Optimize for scalability and iteration speed

The workflow should optimize for:
- automation quality
- procedural flexibility
- rendering consistency
- workflow acceleration
- scene scalability

---

# Best Practices

- Build scenes incrementally
- Keep scripts modular
- Use procedural logic where possible
- Validate renders early
- Automate repetitive tasks aggressively
- Keep generated code readable
- Combine scripting with Geometry Nodes workflows

---

# Notes

- Blender scripting dramatically accelerates complex workflows
- Procedural systems scale better than manual repetition
- Incremental validation prevents large debugging issues
- Python automation makes advanced Blender workflows accessible to non-experts
- Combining scripting with procedural generation creates highly scalable creative systems
