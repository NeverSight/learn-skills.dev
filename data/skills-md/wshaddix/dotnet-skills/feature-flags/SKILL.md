---
name: feature-flags
description: Microsoft.FeatureManagement patterns for feature toggles, gradual rollouts, and A/B testing in ASP.NET Core Razor Pages applications. Use when implementing feature toggles in ASP.NET Core applications, setting up gradual feature rollouts, or configuring A/B testing scenarios with feature flags.
---

## Rationale

Feature flags enable safe deployments, gradual rollouts, A/B testing, and quick rollback capabilities. Without proper feature flag patterns, teams risk deploying incomplete features or cannot respond quickly to production issues. These patterns provide a robust, maintainable approach to feature management in Razor Pages applications.

## Patterns

### Pattern 1: Configuration-Based Feature Flags

Use `appsettings.json` for simple feature toggles with environment-specific overrides.

```json
// appsettings.json
{
  "FeatureManagement": {
    "NewDashboard": false,
    "BetaFeature": false,
    "DarkMode": true,
    "PaymentV2": {
      "EnabledFor": [
        {
          "Name": "Microsoft.Targeting",
          "Parameters": {
            "Audience": {
              "Users": [ "admin@example.com" ],
              "Groups": [ "BetaTesters" ],
              "DefaultRolloutPercentage": 0
            }
          }
        }
      ]
    }
  }
}

// appsettings.Production.json
{
  "FeatureManagement": {
    "NewDashboard": true,
    "PaymentV2": {
      "EnabledFor": [
        {
          "Name": "Microsoft.Targeting",
          "Parameters": {
            "Audience": {
              "Users": [ "admin@example.com" ],
              "Groups": [ "BetaTesters" ],
              "DefaultRolloutPercentage": 25
            }
          }
        }
      ]
    }
  }
}
```

```csharp
// Program.cs - Basic setup
builder.Services.AddFeatureManagement();

// With custom configuration section
builder.Services.AddFeatureManagement(
    builder.Configuration.GetSection("FeatureManagement"));

// With feature filters
builder.Services.AddFeatureManagement()
    .AddFeatureFilter<TargetingFilter>()
    .AddFeatureFilter<PercentageFilter>()
    .AddFeatureFilter<TimeWindowFilter>();
```

### Pattern 2: Typed Feature Flags

Create strongly-typed feature flags for compile-time safety and discoverability.

```csharp
// Feature flag constants
public static class FeatureFlags
{
    public const string NewDashboard = "NewDashboard";
    public const string BetaFeature = "BetaFeature";
    public const string DarkMode = "DarkMode";
    public const string PaymentV2 = "PaymentV2";
    public const string ApiRateLimiting = "ApiRateLimiting";
    public const string AdvancedReporting = "AdvancedReporting";
}

// Feature-aware service interface
public interface IFeatureAwareService
{
    Task<bool> IsEnabledAsync(string featureName);
    Task<bool> IsEnabledAsync<TContext>(string featureName, TContext context);
}

public class FeatureService : IFeatureAwareService
{
    private readonly IFeatureManager _featureManager;

    public FeatureService(IFeatureManager featureManager)
    {
        _featureManager = featureManager;
    }

    public Task<bool> IsEnabledAsync(string featureName) =>
        _featureManager.IsEnabledAsync(featureName);

    public Task<bool> IsEnabledAsync<TContext>(string featureName, TContext context) =>
        _featureManager.IsEnabledAsync(featureName, context);
}

// Extension methods for easier usage
public static class FeatureManagerExtensions
{
    public static Task<bool> IsNewDashboardEnabledAsync(this IFeatureManager manager) =>
        manager.IsEnabledAsync(FeatureFlags.NewDashboard);

    public static Task<bool> IsPaymentV2EnabledAsync(this IFeatureManager manager, string userId) =>
        manager.IsEnabledAsync(FeatureFlags.PaymentV2, new TargetingContext { UserId = userId });
}
```

### Pattern 3: Razor Pages Integration

Use feature flags in Razor Pages for conditional UI rendering and routing.

```csharp
// PageModel with feature flag checks
public class DashboardModel : PageModel
{
    private readonly IFeatureManager _featureManager;

    public DashboardModel(IFeatureManager featureManager)
    {
        _featureManager = featureManager;
    }

    public bool UseNewDashboard { get; private set; }
    public bool IsDarkModeEnabled { get; private set; }

    public async Task OnGetAsync()
    {
        UseNewDashboard = await _featureManager.IsEnabledAsync(FeatureFlags.NewDashboard);
        IsDarkModeEnabled = await _featureManager.IsEnabledAsync(FeatureFlags.DarkMode);
    }
}

// View with conditional rendering
@page
@model DashboardModel
@inject IFeatureManager FeatureManager

@if (Model.UseNewDashboard)
{
    <partial name="_NewDashboard" model="Model" />
}
else
{
    <partial name="_LegacyDashboard" model="Model" />
}

@if (await FeatureManager.IsEnabledAsync(FeatureFlags.BetaFeature))
{
    <div class="alert alert-info">
        <strong>Beta:</strong> Try our new experimental features!
    </div>
}

@if (Model.IsDarkModeEnabled)
{
    <button id="theme-toggle" class="btn btn-outline-secondary">
        Toggle Dark Mode
    </button>
}
```

### Pattern 4: Feature Gate Action Filter

Use the built-in feature gate filter for controller/page-level feature control.

```csharp
// Controller/PageModel level feature gate
[FeatureGate(FeatureFlags.BetaFeature)]
public class BetaFeaturesModel : PageModel
{
    public void OnGet()
    {
        // This page is only accessible when BetaFeature is enabled
    }
}

// Alternative: Redirect to different page
[FeatureGate(FeatureFlags.NewDashboard, 
    RequirementType.All,  // All features must be enabled
    NoFeatureRedirect = "/Dashboard/Legacy")]
public class NewDashboardModel : PageModel
{
    // Redirects to legacy dashboard if NewDashboard is disabled
}

// Custom feature gate attribute for complex scenarios
public class PremiumFeatureAttribute : FeatureGateAttribute
{
    public PremiumFeatureAttribute() 
        : base(FeatureFlags.AdvancedReporting)
    {
    }
}

[PremiumFeature]
public class ReportsModel : PageModel
{
    // Premium feature page
}
```

### Pattern 5: Gradual Rollout with Targeting

Implement user-based and percentage-based rollouts safely.

```csharp
// Custom targeting context
public class FeatureTargetingContext : ITargetingContext
{
    public string? UserId { get; set; }
    public List<string> Groups { get; set; } = new();
}

// Targeting context accessor
public class HttpContextTargetingContextAccessor : ITargetingContextAccessor
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public HttpContextTargetingContextAccessor(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public ValueTask<TargetingContext> GetContextAsync()
    {
        var httpContext = _httpContextAccessor.HttpContext;
        
        if (httpContext?.User?.Identity?.IsAuthenticated != true)
        {
            return ValueTask.FromResult(new TargetingContext());
        }

        var context = new TargetingContext
        {
            UserId = httpContext.User.FindFirst(ClaimTypes.NameIdentifier)?.Value,
            Groups = httpContext.User.FindAll(ClaimTypes.Role)
                .Select(c => c.Value)
                .ToList()
        };

        return ValueTask.FromResult(context);
    }
}

// Registration
builder.Services.AddHttpContextAccessor();
builder.Services.AddSingleton<ITargetingContextAccessor, HttpContextTargetingContextAccessor>();
builder.Services.AddFeatureManagement()
    .AddFeatureFilter<TargetingFilter>();

// Usage in PageModel
public class CheckoutModel : PageModel
{
    private readonly IFeatureManager _featureManager;

    public CheckoutModel(IFeatureManager featureManager)
    {
        _featureManager = featureManager;
    }

    public async Task<IActionResult> OnPostAsync()
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "anonymous";
        
        if (await _featureManager.IsEnabledAsync(FeatureFlags.PaymentV2, new 
        {
            UserId = userId,
            Groups = User.FindAll(ClaimTypes.Role).Select(c => c.Value).ToList()
        }))
        {
            return await ProcessPaymentV2Async();
        }

        return await ProcessLegacyPaymentAsync();
    }
}
```

### Pattern 6: Time-Based Feature Flags

Enable features automatically during specific time windows.

```json
{
  "FeatureManagement": {
    "HolidayTheme": {
      "EnabledFor": [
        {
          "Name": "Microsoft.TimeWindow",
          "Parameters": {
            "Start": "2024-12-01T00:00:00Z",
            "End": "2025-01-02T00:00:00Z"
          }
        }
      ]
    },
    "MaintenanceMode": {
      "EnabledFor": [
        {
          "Name": "Microsoft.TimeWindow",
          "Parameters": {
            "Start": "2024-12-25T02:00:00Z",
            "End": "2024-12-25T04:00:00Z"
          }
        }
      ]
    }
  }
}
```

```csharp
// Time window filter usage
[FeatureGate(FeatureFlags.MaintenanceMode)]
public class MaintenanceModel : PageModel
{
    public IActionResult OnGet()
    {
        // Show maintenance page only during window
        return Page();
    }
}

// Custom time-based filter for recurring schedules
public class RecurringTimeFilter : IFeatureFilter
{
    public Task<bool> EvaluateAsync(FeatureFilterEvaluationContext context)
    {
        var settings = context.Parameters.Get<RecurringTimeSettings>();
        
        if (settings?.DaysOfWeek is null || settings.DaysOfWeek.Length == 0)
        {
            return Task.FromResult(true);
        }

        var now = DateTime.UtcNow;
        var dayOfWeek = now.DayOfWeek.ToString();
        
        return Task.FromResult(settings.DaysOfWeek.Contains(dayOfWeek));
    }
}

public class RecurringTimeSettings
{
    public string[] DaysOfWeek { get; set; } = Array.Empty<string>();
}
```

### Pattern 7: Middleware and Pipeline Integration

Integrate feature flags with middleware for request-level control.

```csharp
// Feature flag middleware
public class FeatureFlagMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<FeatureFlagMiddleware> _logger;

    public FeatureFlagMiddleware(RequestDelegate next, ILogger<FeatureFlagMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(
        HttpContext context, 
        IFeatureManager featureManager)
    {
        // Add feature flags to HttpContext.Items for views
        var flags = new Dictionary<string, bool>
        {
            [FeatureFlags.NewDashboard] = await featureManager.IsEnabledAsync(FeatureFlags.NewDashboard),
            [FeatureFlags.DarkMode] = await featureManager.IsEnabledAsync(FeatureFlags.DarkMode)
        };
        
        context.Items["FeatureFlags"] = flags;

        // Check for API rate limiting feature
        if (await featureManager.IsEnabledAsync(FeatureFlags.ApiRateLimiting))
        {
            _logger.LogDebug("API rate limiting is enabled");
        }

        await _next(context);
    }
}

// Extension method
public static class FeatureFlagMiddlewareExtensions
{
    public static IApplicationBuilder UseFeatureFlags(this IApplicationBuilder app)
    {
        return app.UseMiddleware<FeatureFlagMiddleware>();
    }
}

// Usage in Program.cs
app.UseFeatureFlags();

// View helper
public static class FeatureFlagHelpers
{
    public static bool IsFeatureEnabled(this IHtmlHelper helper, string featureName)
    {
        var flags = helper.ViewContext.HttpContext.Items["FeatureFlags"] 
            as Dictionary<string, bool>;
        
        return flags?.TryGetValue(featureName, out var enabled) == true && enabled;
    }
}

// View usage
@if (Html.IsFeatureEnabled(FeatureFlags.DarkMode))
{
    <script>/* Dark mode logic */</script>
}
```

## Anti-Patterns

```csharp
// ❌ BAD: Hard-coded feature checks scattered throughout code
if (Environment.IsDevelopment())
{
    ShowNewFeature();
}

// ✅ GOOD: Use feature manager
if (await _featureManager.IsEnabledAsync(FeatureFlags.NewFeature))
{
    ShowNewFeature();
}

// ❌ BAD: Checking features in tight loops
for (var item in items)
{
    if (await _featureManager.IsEnabledAsync(FeatureFlags.BatchProcessing))
    {
        ProcessBatch(item);
    }
}

// ✅ GOOD: Check once and cache result
var useBatchProcessing = await _featureManager.IsEnabledAsync(FeatureFlags.BatchProcessing);
foreach (var item in items)
{
    if (useBatchProcessing)
    {
        ProcessBatch(item);
    }
}

// ❌ BAD: Not handling missing configuration
public async Task<bool> IsNewFeatureEnabled()
{
    return await _featureManager.IsEnabledAsync("NewFeature"); // May throw!
}

// ✅ GOOD: Use constants and handle gracefully
public async Task<bool> IsNewFeatureEnabled()
{
    try
    {
        return await _featureManager.IsEnabledAsync(FeatureFlags.NewFeature);
    }
    catch (FeatureManagementException ex)
    {
        _logger.LogWarning(ex, "Feature flag check failed");
        return false; // Safe fallback
    }
}

// ❌ BAD: Tight coupling to feature manager in domain logic
public class OrderService
{
    private readonly IFeatureManager _featureManager; // Shouldn't be here!
    
    public async Task ProcessOrder(Order order)
    {
        if (await _featureManager.IsEnabledAsync("NewPricing"))
        {
            ApplyNewPricing(order);
        }
    }
}

// ✅ GOOD: Pass feature-driven behavior as configuration/strategy
public class OrderService
{
    private readonly IPricingStrategy _pricingStrategy;
    
    public OrderService(IPricingStrategy pricingStrategy)
    {
        _pricingStrategy = pricingStrategy;
    }
    
    public Task ProcessOrder(Order order)
    {
        _pricingStrategy.ApplyPricing(order);
        // ...
    }
}

// ❌ BAD: Not cleaning up old feature flags
// appsettings.json has 50+ old flags never cleaned up

// ✅ GOOD: Regular cleanup process
// 1. Document feature flag lifecycle
// 2. Remove flags after feature is fully rolled out
// 3. Use feature flag dashboard for tracking

// ❌ BAD: Inconsistent naming conventions
{
  "new_feature": true,
  "LegacyFeature": false,
  "AnotherFeature_V2": true
}

// ✅ GOOD: Consistent naming (PascalCase recommended)
{
  "NewFeature": true,
  "LegacyFeature": false,
  "AnotherFeatureV2": true
}

// ❌ BAD: Enabling features without monitoring
await _featureManager.IsEnabledAsync("ExpensiveFeature");
// No metrics on usage!

// ✅ GOOD: Instrument feature flag usage
public async Task<bool> IsEnabledWithMetrics(string featureName)
{
    var enabled = await _featureManager.IsEnabledAsync(featureName);
    
    _metrics.RecordFeatureFlagCheck(featureName, enabled);
    
    return enabled;
}
```

## References

- [Microsoft.FeatureManagement](https://learn.microsoft.com/en-us/azure/azure-app-configuration/feature-management-dotnet-reference)
- [Feature Management Overview](https://learn.microsoft.com/en-us/azure/azure-app-configuration/concept-feature-management)
- [Targeting Filter](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-targetingfilter-aspnet-core)
- [Percentage Filter](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-percentage-rollout)
- [Time Window Filter](https://learn.microsoft.com/en-us/azure/azure-app-configuration/howto-timewindow-filter)
