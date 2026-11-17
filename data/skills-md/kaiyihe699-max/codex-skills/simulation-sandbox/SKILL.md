---
name: simulation-sandbox
description: Generate runnable simulation sandboxes from rule systems or simulation ideas. Use when Codex needs to turn agent-based or system-dynamics rules such as crowd evacuation, virus spread, city traffic, price competition, ecology, or other research-toy models into HTML canvas simulators, Python notebooks, CSV outputs, animations, or reproducible experiment artifacts.
---

# Simulation Sandbox

Use this skill to turn a user-described rule system into runnable simulation artifacts. Favor small, inspectable research-toy models over opaque frameworks.

## Workflow

1. Capture the model.
   - If the user gives rules, preserve them.
   - If the user gives only a domain idea, infer a minimal toy rule system and state assumptions.
   - Ask only when the model's domain, outputs, or risk level is genuinely ambiguous.

2. Normalize rules to the JSON DSL.
   - Read `references/dsl.md` when designing, editing, or explaining the rule format.
   - Keep units and probabilities explicit.
   - Prefer deterministic seeds for reproducible runs.

3. Generate artifacts.
   - Use the bundled generator for supported models:
   - Run commands from the skill directory, or use the absolute path to `scripts/build_simulation.py`.

```bash
python scripts/build_simulation.py --rules path/to/rules.json --out path/to/output
```

   - For a quick demo, use a preset:

```bash
python scripts/build_simulation.py --preset virus --out path/to/output
```

   - Use `--formats html,csv,notebook,json` to choose outputs.
   - Use `--steps` and `--seed` for controlled experiments.

4. Extend when needed.
   - For unsupported models, first map the idea to the closest DSL pattern.
   - If the bundled script cannot represent the rules faithfully, create a scoped custom simulator using the same artifact pattern: self-contained HTML replay or canvas engine, CSV time series, notebook analysis, and rule JSON.

5. Validate before handoff.
   - Run the generator and confirm it exits successfully.
   - Inspect the CSV header and first rows.
   - Open or screenshot the HTML when visual output matters.
   - Check generated notebooks are valid JSON.

## Output Standards

- Put final user-facing deliverables in the requested output folder.
- Return direct links to the HTML, notebook, CSV, and rule JSON when created.
- Describe assumptions and toy-model limitations plainly. Do not imply scientific validity unless the model has been validated.
- Make the first artifact runnable without external services.
- Prefer visible animation or replay over static charts when the user asks for a sandbox, simulator, or "research toy."

## Resources

- `scripts/build_simulation.py`: deterministic generator for HTML canvas replay, CSV, notebook, and JSON artifacts.
- `assets/presets.json`: starter rule systems for virus, evacuation, traffic, market, and ecosystem examples.
- `references/dsl.md`: compact DSL schema and modeling conventions.
