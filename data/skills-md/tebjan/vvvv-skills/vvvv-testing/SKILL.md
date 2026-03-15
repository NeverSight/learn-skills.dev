---
name: vvvv-testing
description: "Set up and run automated tests for vvvv gamma packages and C# nodes -- VL.TestFramework with NUnit for library/package authors (CI-ready), test .vl patches with assertion nodes, and lightweight agent-driven test workflows. Use when writing tests for vvvv packages, setting up test infrastructure, creating test patches, running automated compilation checks, or integrating vvvv tests into CI/CD."
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Testing vvvv gamma Projects

## Two Testing Approaches

| Approach | Use Case | Setup |
|----------|----------|-------|
| **VL.TestFramework** (NUnit) | Package/library authors, CI integration | .csproj test project with NUnit |
| **Agent test workflow** | Quick verification, ad-hoc debugging | Create test .vl patch, launch vvvv, check results |

## VL.TestFramework (NUnit)

### Test Project Setup

Create a test .csproj referencing VL.TestFramework:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0-windows</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="NUnit" Version="4.*" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\path\to\VL.TestFramework.csproj" />
    <!-- OR if using installed vvvv: -->
    <!-- Reference VL.TestFramework.dll from vvvv install dir -->
  </ItemGroup>
</Project>
```

### Minimal Test Class

```csharp
using NUnit.Framework;
using VL.TestFramework;

[TestFixture]
public class MyPackageTests
{
    TestEnvironment testEnvironment;

    // Important: Don't use async Task here (NUnit sync context issue)
    [OneTimeSetUp]
    public void Setup()
    {
        var assemblyPath = typeof(MyPackageTests).Assembly.Location;
        var searchPaths = new[] { "path/to/your/package" };
        testEnvironment = TestEnvironmentLoader.Load(assemblyPath, searchPaths);
    }

    [OneTimeTearDown]
    public void TearDown()
    {
        testEnvironment?.Dispose();
        testEnvironment = null;
    }

    [Test]
    public async Task MyPatchCompilesWithoutErrors()
    {
        await testEnvironment.LoadAndTestAsync("path/to/MyPatch.vl");
    }

    [Test]
    public async Task MyPatchCompilesAndRuns()
    {
        await testEnvironment.LoadAndTestAsync(
            "path/to/MyPatch.vl",
            runEntryPoint: true);
    }
}
```

### Key API

- `TestEnvironmentLoader.Load(assemblyPath, searchPaths)` -- Create test environment. One per test class (expensive).
- `testEnvironment.LoadAndTestAsync(filePath)` -- Load .vl document, check for compilation errors.
- `testEnvironment.LoadAndTestAsync(filePath, runEntryPoint: true)` -- Also execute the entry point (Create + Update + Dispose).
- `testEnvironment.GetPackages()` -- Discover all packages and their source/help/test files.
- `testEnvironment.Host.LoadAndCompileAsync(filePath)` -- Load and compile without running (for custom assertions).
- `testEnvironment.Host.GetTargetCompilationAsync(filePath)` -- Get the C# compilation for inspection.

For the full API reference, see [test-framework-reference.md](test-framework-reference.md).

### Test Discovery Conventions

The VL.TestFramework automatically discovers tests:

- **Test documents**: `.vl` files in `tests/` folders under package directories
- **Help patches**: `.vl` files in `help/` folders (tested for compilation only)
- **Test nodes**: Process or operation nodes ending in `Test` or `Tests` within test documents are individually compiled and executed

File discovery pattern:
```
VL.MyPackage/
  tests/
    MyFeatureTest.vl      <-- auto-discovered test document
    IntegrationTests.vl   <-- auto-discovered test document
  help/
    HowTo Use Feature.vl  <-- tested for compilation errors
```

### Running Tests

```shell
# Run all tests
dotnet test

# Run specific test
dotnet test --filter "MyPatchCompilesWithoutErrors"

# Via Nuke build system (if available)
./build.ps1 --target Test
```

## Test Nodes (VL Patch Assertions)

Use these nodes inside .vl test patches to assert behavior. Available under `VL.Lib.Basics.Test.TestNodes`:

```csharp
// In VL patches, these are available as nodes:
TestNodes.Assert(condition, "message")           // General assertion
TestNodes.AreEqual(expected, actual)             // Value equality
TestNodes.AreNotEqual(expected, actual)          // Value inequality
TestNodes.IsNotNull(input)                       // Null check
TestNodes.AreSequenceEqual(expected, actual)     // Collection equality
TestNodes.AssertElementHasError(elementGuid)     // Verify element has compile error
TestNodes.AssertElementHasNoError(elementGuid)   // Verify element has no compile error
```

Assertions throw `AssertionException` on failure, which the test runner catches and reports.

## Agent Test Workflow

For quick verification without a full NUnit project:

### 1. Create a Test Patch

Create a `.vl` file that exercises the feature under test. Include TestNodes for assertions. Name it with a `Test` suffix for auto-discovery. To understand the .vl XML file structure (document hierarchy, element IDs, node references, pins, pads, links), consult the **vvvv-fileformat** skill.

### 2. Compile-Check via VL.TestFramework

Write a minimal C# script or test that loads and compiles the patch:

```csharp
var env = TestEnvironmentLoader.Load(assemblyPath, searchPaths);
await env.LoadAndTestAsync("path/to/MyTest.vl", runEntryPoint: true);
env.Dispose();
```

### 3. Launch vvvv for Manual Verification

Use the **vvvv-debugging** skill to set up a launch configuration that opens the test patch:

```shell
vvvv.exe --stoppedonstartup --debug --log -o "path/to/MyTest.vl"
```

- `--stoppedonstartup` pauses runtime so you can inspect initial state
- `--log` enables logging to `%USERPROFILE%\Documents\vvvv\gamma\vvvv.log`
- Parse the log file for errors after vvvv exits

### 4. Check Results

After vvvv exits, check:
- Exit code (0 = success)
- Log file for `ERROR` or `EXCEPTION` entries
- Any `AssertionException` in the output

## CI Integration

### Nuke Build System

Most vvvv repos use Nuke. The test target:

```csharp
Target Test => _ => _
    .Executes(() =>
    {
        DotNetTest(_ => _
            .SetProjectFile(Solution)
            .SetConfiguration(Configuration));
    });
```

Run with: `./build.ps1` or `./build.sh` (defaults to Publish target; use `--target Test` for tests).

### GitHub Actions Example

```yaml
- name: Run vvvv tests
  run: dotnet test --configuration Release --logger "trx"
```

### Performance Notes

- Create one `TestEnvironment` per test class (`[OneTimeSetUp]`), not per test
- Documents are unloaded after each test to free memory
- Use `preCompilePackages: false` (default) for faster test iteration
- Set `preCompilePackages: true` for production-fidelity testing
