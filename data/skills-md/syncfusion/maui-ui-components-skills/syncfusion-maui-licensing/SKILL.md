---
name: syncfusion-maui-licensing
description: Sets up and validates Syncfusion .NET MAUI licensing, including license key registration, generation, and error resolution. Use when encountering trial license warnings ("This application was built using a trial version"), licensing errors, license key registration, unlock key vs license key confusion, build server or CI/CD licensing, NuGet package licensing requirements, platform mismatch errors, or version mismatch errors.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Licensing for Syncfusion .NET MAUI

Comprehensive guide for managing Syncfusion .NET MAUI licenses, from generation to registration and troubleshooting.

## When to Use This Skill

Use this skill immediately when you encounter:

**Licensing Errors:**
- "This application was built using a trial version" message
- "The included Syncfusion license key is invalid" error
- License validation failures
- Platform mismatch errors
- Version mismatch errors
- Trial expired messages

**License Key Tasks:**
- Generating license keys from Syncfusion account
- Registering license keys in applications
- Understanding trial vs licensed installations
- Differentiating unlock key from license key
- Configuring licensing for build servers
- Setting up CI/CD license validation

**Common Scenarios:**
- Initial app setup with Syncfusion components
- Resolving license warnings during development
- Deploying applications with proper licensing
- Upgrading from trial to licensed version
- Managing licenses for multiple projects
- Troubleshooting "Could not load Syncfusion.Licensing.dll" errors

## Licensing System Overview

Starting with version **20.2.0.x**, Syncfusion introduced a new licensing system that applies to:
- NuGet packages from nuget.org
- Evaluation installers
- Trial licenses

**Key Points:**
- License keys are **version and platform specific**
- Registration is required for NuGet packages and trial installers
- Licensed installers do NOT require license key registration
- License validation is **offline** (no internet required)
- License keys are different from installer unlock keys

## Documentation and Navigation Guide

### Understanding Licensing

**When to Read:** First-time setup, understanding licensing requirements, or clarifying trial vs licensed installations.

📄 **Read:** [references/licensing-overview.md](references/licensing-overview.md)
- Licensing system introduction (v20.2.0.x changes)
- When license key registration is required
- Trial vs licensed installation differences
- Unlock key vs license key distinction
- Build server licensing scenarios
- NuGet package licensing requirements
- Version and platform specificity

### Generating License Keys

**When to Read:** Need to obtain a new license key, working with trial licenses, or managing license for different versions/platforms.

📄 **Read:** [references/license-generation.md](references/license-generation.md)
- Accessing License & Downloads section
- Accessing Trial & Downloads section
- Using Claim License Key feature
- Generating keys for active licenses
- Generating keys for active trials
- Handling expired licenses (temporary 5-day keys)
- Setting up accounts for NuGet.org users
- Platform and version-specific key generation

### Registering License Keys

**When to Read:** Need to register a license key in your application, choosing registration location, or implementing proper licensing.

📄 **Read:** [references/license-registration.md](references/license-registration.md)
- RegisterLicense() method syntax
- Registration in App.xaml.cs constructor
- Registration in MauiProgram.cs
- Syncfusion.Licensing.dll reference requirements
- Best practices for registration location
- Multiple registration scenarios
- Complete code examples for each approach

### Troubleshooting Licensing Errors

**When to Read:** Encountering license validation errors, trial expiration messages, platform/version mismatches, or assembly loading issues.

📄 **Read:** [references/licensing-errors.md](references/licensing-errors.md)
- License key not registered error
- Invalid key error messages
- Trial expired errors
- Platform mismatch errors
- Version mismatch errors
- "Could not load Syncfusion.Licensing.dll" issues
- Solutions for each error type
- Version-specific error variations
- Copy Local configuration for assemblies

### Advanced Topics and FAQ

**When to Read:** Setting up CI/CD pipelines, programmatic license validation, offline deployment questions, or upgrading from trial.

📄 **Read:** [references/licensing-faq.md](references/licensing-faq.md)
- CI/CD license validation (Azure Pipelines, GitHub Actions, Jenkins)
- ValidateLicense() method for programmatic checks
- Unit testing with license validation
- Internet connection requirements (offline validation)
- Upgrading from trial to licensed version
- NuGet.org user account registration
- Where to obtain license keys
- Common frequently asked questions

## Quick Start Guide

### Step 1: Generate License Key

1. Log in to your Syncfusion account
2. Navigate to [License & Downloads](https://www.syncfusion.com/account/downloads) (licensed) or [Trial & Downloads](https://www.syncfusion.com/account/manage-trials/downloads) (trial)
3. Generate a license key for **.NET MAUI** platform and your specific version
4. Copy the generated license key

### Step 2: Register License Key

Choose one of these registration methods:

**Option A: Register in App.xaml.cs**

```csharp
public App()
{
    // Register Syncfusion license
    string licenseKey = Environment.GetEnvironmentVariable("SYNCFUSION_LICENSE_KEY");
    if (!string.IsNullOrEmpty(licenseKey))
    {   
        Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense(licenseKey);
    }
    
    InitializeComponent();
    
    MainPage = new AppShell();
}
```

**Option B: Register in MauiProgram.cs**

```csharp
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        // Register the Syncfusion license key
       string licenseKey = Environment.GetEnvironmentVariable("SYNCFUSION_LICENSE_KEY");
        if (!string.IsNullOrEmpty(licenseKey))
        {   
            Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense(licenseKey);
        }
 
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .ConfigureSyncfusionCore()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            });

        return builder.Build();
    }
}
```

### Step 3: Verify Registration

Run your application. If properly registered, you should NOT see any licensing warning messages.

## Common Patterns

### Pattern 1: Initial Setup for New Projects

**Scenario:** Starting a new .NET MAUI project with Syncfusion components from NuGet.

**Steps:**
1. Install Syncfusion NuGet packages
2. Generate license key for MAUI platform + your version
3. Register license key in MauiProgram.cs before ConfigureSyncfusionCore()
4. Ensure Syncfusion.Licensing package is installed
5. Build and run to verify no licensing warnings

### Pattern 2: Resolving "Trial Version" Warning

**Scenario:** Application shows "This application was built using a trial version" message.

**Solution:**
1. Verify you have a valid license key (not expired)
2. Check the license key is for correct platform (MAUI)
3. Check the license key version matches your package version
4. Register the license key before InitializeComponent() or before ConfigureSyncfusionCore()
5. Clean and rebuild the application

### Pattern 3: Version Mismatch Error

**Scenario:** Error message shows "included Syncfusion license ({Registered Version}) is invalid for version {Required version}"

**Solution:**
1. Check your NuGet package versions (all should be same version)
2. Generate new license key for the exact version you're using
3. Replace old license key with new one
4. Clean solution and rebuild

### Pattern 4: Build Server / CI/CD Setup

**Scenario:** Need to validate licensing during continuous integration.

**Approaches:**
- Use LicenseKeyValidator utility in CI pipeline
- Implement ValidateLicense() method with unit tests
- Configure environment variables for license key
- Fail build if validation fails

**Read:** [references/licensing-faq.md](references/licensing-faq.md) for detailed CI/CD setup instructions.

### Pattern 5: Multiple Projects in Solution

**Scenario:** Solution has multiple MAUI projects using Syncfusion components.

**Solution:**
1. Register license key in each project's App.xaml.cs or MauiProgram.cs
2. Use same license key across all projects (if same version)
3. Ensure all projects reference Syncfusion.Licensing.dll
4. Consider using shared constant for license key string

## Key Concepts

### License Key vs Unlock Key

- **Unlock Key:** Used to unlock the Syncfusion installer during installation
- **License Key:** Required in your application code when using NuGet packages or trial installer
- These are **different** keys with different purposes

### Version and Platform Specificity

License keys are tied to:
- **Platform:** MAUI, WPF, Blazor, etc. (use MAUI license for MAUI apps)
- **Version:** Major.Minor.Patch (e.g., 26.2.4)

A MAUI 26.2.4 license key will NOT work for:
- Different platform (e.g., Blazor)
- Different version (e.g., 26.1.0 or 27.0.0)

### When License Registration is Required

**Required:**
- NuGet packages from nuget.org
- Trial installer assemblies
- Evaluation scenarios

**NOT Required:**
- Licensed installer assemblies (license embedded in assemblies)

### Offline Validation

- License validation happens **offline** during application execution
- No internet connection required for validation
- Apps can be deployed to systems without internet access

## Common Use Cases

### Use Case 1: First-Time Developer Setup

**User:** "I just installed Syncfusion MAUI components from NuGet and I'm getting a trial license warning."

**Solution:**
1. Read [references/licensing-overview.md](references/licensing-overview.md) to understand licensing requirements
2. Read [references/license-generation.md](references/license-generation.md) to generate appropriate key
3. Read [references/license-registration.md](references/license-registration.md) to register in your app

### Use Case 2: Deployment Issues

**User:** "My app works fine in development but shows licensing errors when deployed."

**Solution:**
1. Verify Syncfusion.Licensing.dll is included in deployment
2. Check Copy Local is set to True for Syncfusion assemblies
3. Read [references/licensing-errors.md](references/licensing-errors.md) for "Could not load" troubleshooting

### Use Case 3: Trial to Licensed Upgrade

**User:** "I purchased a license, how do I remove the trial warning?"

**Solution:**
1. Read [references/licensing-faq.md](references/licensing-faq.md) - "Upgrading from Trial" section
2. Generate new licensed key (not trial key)
3. Replace trial key with licensed key in RegisterLicense() call
4. Clean and rebuild application

### Use Case 4: CI/CD Integration

**User:** "How do I validate licensing in Azure DevOps pipeline?"

**Solution:**
Read [references/licensing-faq.md](references/licensing-faq.md) for complete CI/CD setup including:
- Azure Pipelines (YAML and Classic)
- GitHub Actions
- Jenkins
- Unit test approach with ValidateLicense()

## Important Notes

- Always register license key **before** InitializeComponent() in App.xaml.cs or **before** ConfigureSyncfusionCore() in MauiProgram.cs
- Keep license keys secure (don't commit to public repositories)
- Use the same license key for all Syncfusion packages in your project
- Ensure all Syncfusion packages are the same version
- License validation errors are shown at runtime, not compile time