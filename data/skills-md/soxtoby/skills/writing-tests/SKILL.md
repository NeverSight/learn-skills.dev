---
name: writing-tests
description: General advice for writing tests. Use when writing any tests, reviewing test code for style consistency, or when the user asks to follow the testing style guide.
---

# Layout
- Setup and teardown should be above any tests.

# Naming
- Test should what class or function they're testing, what the test scenario is, and what the expected outcome is, in that order.
- For nested tests, don't repeat the target and scenario in inner test names.
- The variable for the system under test should be named `sut`, or `_sut` for private fields if that matches the codebase convention.
- When there's a single result from the system under test, the variable for the result should be named `result`.

# Implementation
- Tests should focus on inputs and outputs rather than internal implementation details.
- Prefer real classes or fake implementations over mocks.
- When desired behavior changes, test for the new behavior, but avoid testing that the old behavior no longer exists.

# Structure
- Where possible, keep code inside a test in Arrange-Act-Assert structure, using whitespace to separate each section, or comments if whitespace is not sufficient. If the Act and Assert are short enough, they can be combined into one statement (e.g. `sut.method().shouldBe(expected)`).
- If a test requires a lot of setup or low-level details, it can obscure the logical flow of the test, and well-named helper methods should be used.

# EasyAssertions

This applies to C# tests using the EasyAssertions library.
- Chain assertions with `.And` and `.And()` where possible.
- `.And` should always be used immediately for an assertion and never stored in a variable. It should be on the same line as the assertion it is chaining to.
- One assertion per line. e.g.
  ```csharp
  // Chained assertions over multiple lines
  _sut.GetTextCollectionProvider(_packageName, CancellationToken.None)
      .ShouldComplete()
      .And.ShouldBeA<DataSourceGeneratedSettingTextCollectionProvider>()
      .And.TextCollection(CultureInfo.GetCultureInfo("en-US")).Get("TestLabel").ShouldBe("Package label");
  
  // Single short assertion can be on one line
  _sut.Version.ShouldBe("1.0.0");
  ```