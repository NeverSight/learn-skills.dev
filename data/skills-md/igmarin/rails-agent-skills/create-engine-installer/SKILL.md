---
name: create-engine-installer
type: atomic
license: MIT
description: >
  Use when writing an install generator for a Rails engine (migrations, config).
  Trigger words: install generator, engine setup, copy migrations.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Create Engine Installer


## Validation Workflow (HARD-GATE)

When building or reviewing an install generator, follow these steps in order. **DO NOT ship a generator without completing steps 3 and 4.**

1. **GENERATE**: Run the generator against a clean host app. Show command + terminal output labeled **Observed output** for the first run. Confirm files are created in correct host paths (initializer at `config/initializers/`, migrations at `db/migrate/`, route mount in `config/routes.rb`).
2. **VERIFY**: Check output files exist in the correct host paths. List shell commands confirming the initializer, routes, and migrations exist.
3. **RERUN**: Run the generator a second time; confirm no duplicate files, routes, or initializer blocks are inserted. Show command + terminal output labeled **Observed output** demonstrating idempotent behavior (skipping/conflict resolution). Use unique, scenario-specific values rather than copying verbatim from templates.
4. **TEST**: Cover both single-run and rerun behavior in generator specs (see spec template below).
5. **DOCUMENT**: List what was generated vs. what the user must do manually, including required env vars, rollback steps, and any install docs — verified against what the generator actually produces.

Key implementation rules:
- Configure only in initializers (avoid boot-time mutation).
- Document all required env vars alongside rollback steps.
- Provide sensible defaults that are easy to edit.

## Idempotency Guards

All generator actions must be safe to run multiple times. Guard every file creation and injection at the point of use:

```ruby
def create_initializer
  return if File.exist?(File.join(destination_root, 'config/initializers/my_engine.rb'))
  create_file 'config/initializers/my_engine.rb', <<~RUBY
    MyEngine.configure do |config|
      config.user_class = "User"
    end
  RUBY
end

def mount_route
  # inject_into_file with force: false skips insertion if sentinel already present
  inject_into_file 'config/routes.rb',
    "\n  mount MyEngine::Engine, at: '/admin'\n",
    after: "Rails.application.routes.draw do",
    force: false
end
```

**Minimal rerun spec:**

```ruby
it 'does not duplicate the route mount on rerun' do
  2.times { run_generator }
  expect(File.read(file('config/routes.rb')).scan('mount MyEngine::Engine').size).to eq(1)
end
```

For larger installers, extract extended guard patterns and spec templates into a dedicated companion file alongside the generator (e.g. `lib/generators/my_engine/install/install_generator_patterns.rb`) to keep the generator lean and this skill focused on workflow. Reference that file explicitly in your generator's comments so future maintainers know where to find the shared patterns.

## Integration

| Skill | When to chain |
|-------|---------------|
| [create-engine](../create-engine/SKILL.md) | When designing the engine structure that installers will configure |
| [document-engine](../document-engine/SKILL.md) | When documenting install steps or upgrade instructions |
| [test-engine](../test-engine/SKILL.md) | When adding generator specs or dummy-app install coverage |
