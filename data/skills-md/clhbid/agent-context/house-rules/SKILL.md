---
name: house-rules
description: The clhbid house rules. Use when writing, testing or reviewing code in a clhbid repo.
---

# House rules

Write the code, and everything that describes it, with the `writing-lean` skill.

- **Test our code, not the dependency.** Test the behaviour our code adds, and take the package as
  given: import its values rather than copying its tables, and leave its behaviour to its own tests.
- **Single source of truth.** Take each value from where it is defined: the Tailwind scale
  (`max-w-7xl`, not `max-w-[1468px]`), a shared constant, or the package's own types.
- **Spec style.** Set up and tear down in the test framework's hooks. Arrange, act, then assert,
  and assert the whole result, so an extra item fails the test.
- **Fake the clock** whenever a spec depends on the time, so it passes at any hour and in any time
  zone.
