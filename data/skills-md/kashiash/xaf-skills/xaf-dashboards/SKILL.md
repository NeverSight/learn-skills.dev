---
name: xaf-dashboards
description: XAF Analytics & Dashboards Module - DashboardsModule/DashboardsBlazorModule/DashboardsWinModule setup, DashboardData persistent object storage, IXafDashboardStorage custom storage, dashboard viewer and designer in UI, data sources for business objects (EF Core and XPO), DashboardDataProvider customization, predefined dashboards, view/design security permissions. Use when integrating DevExpress Dashboard analytics into XAF applications.
---

# XAF: Analytics & Dashboards Module

## Setup

### NuGet Packages

```xml
<!-- Core -->
<PackageReference Include="DevExpress.ExpressApp.Dashboards" Version="25.1.*" />
<!-- Blazor -->
<PackageReference Include="DevExpress.ExpressApp.Dashboards.Blazor" Version="25.1.*" />
<!-- WinForms -->
<PackageReference Include="DevExpress.ExpressApp.Dashboards.Win" Version="25.1.*" />
```

### Blazor Program.cs

```csharp
b.AddModule<DashboardsModule>();
b.AddModule<DashboardsBlazorModule>();

// Register dashboard services
builder.Services.AddDevExpressDashboards();

// In app configuration:
app.UseXaf();
app.MapControllers();
// DevExpress dashboard endpoint
app.MapDevExpressDashboardRoute("api/dashboard");
```

### EF Core DbContext (add DashboardData table)

```csharp
public class ApplicationDbContext : DbContext {
    public DbSet<DashboardData> Dashboards { get; set; }
    // ...
}
```

### WinForms

```csharp
Application.Modules.Add(new DashboardsModule());
Application.Modules.Add(new DashboardsWindowsFormsModule());
```

---

## DashboardData — Persistent Storage

`DashboardData` is the built-in persistent object for storing dashboards in the database.

```csharp
// Fields:
// Title (string)       - display name in navigation
// Content (string)     - dashboard layout as XML
// IsSynchronized (bool) - internal sync flag
```

Create a dashboard in code (predefined):
```csharp
public class MyModule : ModuleBase {
    public override void PopulateAdditionalExportedTypes(
        string containerAssemblyName, List<Type> exportedTypes) {
        base.PopulateAdditionalExportedTypes(containerAssemblyName, exportedTypes);
    }
}

// Seed in Updater.cs
public override void UpdateDatabaseAfterUpdateSchema() {
    base.UpdateDatabaseAfterUpdateSchema();

    if (ObjectSpace.FindObject<DashboardData>(null) == null) {
        var dashboard = ObjectSpace.CreateObject<DashboardData>();
        dashboard.Title = "Sales Overview";
        dashboard.Content = File.ReadAllText("SalesOverview.xml"); // exported .xml
        ObjectSpace.CommitChanges();
    }
}
```

---

## Custom Dashboard Storage

```csharp
public class MyDashboardStorage : IXafDashboardStorage {
    private readonly IObjectSpaceFactory _factory;

    public MyDashboardStorage(IObjectSpaceFactory factory) {
        _factory = factory;
    }

    public IEnumerable<DashboardInfo> GetAvailableDashboardsInfo() {
        using var os = _factory.CreateObjectSpace(typeof(DashboardData));
        return os.GetObjects<DashboardData>()
            .Select(d => new DashboardInfo { ID = d.ID.ToString(), Name = d.Title })
            .ToList();
    }

    public XDocument LoadDashboard(string dashboardID) {
        using var os = _factory.CreateObjectSpace(typeof(DashboardData));
        var data = os.GetObjectByKey<DashboardData>(Guid.Parse(dashboardID));
        return XDocument.Parse(data.Content);
    }

    public void SaveDashboard(string dashboardID, XDocument dashboard) {
        using var os = _factory.CreateObjectSpace(typeof(DashboardData));
        var data = os.GetObjectByKey<DashboardData>(Guid.Parse(dashboardID));
        data.Content = dashboard.ToString();
        os.CommitChanges();
    }

    public string AddDashboard(XDocument dashboard, string dashboardName) {
        using var os = _factory.CreateObjectSpace(typeof(DashboardData));
        var data = os.CreateObject<DashboardData>();
        data.Title = dashboardName;
        data.Content = dashboard.ToString();
        os.CommitChanges();
        return data.ID.ToString();
    }
}
```

---

## Data Sources in Dashboards

### EF Core ObjectDataSource

```csharp
// Register in DashboardsModule configuration
b.AddModule<DashboardsModule>(options => {
    options.DashboardDataType = typeof(DashboardData);
});

// Make business objects available as dashboard data sources:
// The module auto-discovers XAF business objects via metadata
// No extra code needed — types registered in modules appear in designer
```

### Custom Data Source Provider

```csharp
public class MyDashboardDataProvider : DashboardDataProvider {
    readonly IObjectSpaceFactory _factory;

    public MyDashboardDataProvider(IObjectSpaceFactory factory) {
        _factory = factory;
    }

    public override object GetDataSource(string dataSourceName, IDictionary<string, object> parameters) {
        using var os = _factory.CreateObjectSpace(typeof(SalesData));
        return os.GetObjects<SalesData>()
            .Select(s => new { s.Date, s.Amount, s.Region })
            .ToList();
    }
}

// Register:
services.AddSingleton<DashboardDataProvider, MyDashboardDataProvider>();
```

---

## Dashboard Viewer in UI

XAF automatically adds dashboards to the **Navigation** under a "Dashboards" group. Users open dashboards from the navigation item — no extra code needed.

---

## Dashboard Designer

- **Blazor:** Integrated designer available in-browser when user has `Write` permission on `DashboardData`
- **WinForms:** Native XtraDashboard Designer hosted within application

```csharp
// Enable designer for all authenticated users:
role.AddTypePermission<DashboardData>(SecurityOperations.FullAccess, SecurityPermissionState.Allow);

// Viewers only (no design access):
role.AddTypePermission<DashboardData>(SecurityOperations.ReadOnlyAccess, SecurityPermissionState.Allow);
```

---

## Security Permissions

| Permission | Capability |
|---|---|
| Read `DashboardData` | View dashboards |
| Write `DashboardData` | Edit dashboards in designer |
| Create `DashboardData` | Create new dashboards |
| Delete `DashboardData` | Delete dashboards |

---

## Export / Print

Dashboard viewer provides built-in export toolbar:
- PDF export
- Excel/XLSX export
- Image export
- Print

No additional code needed — built into the viewer component.

---

## v24.2 vs v25.1 Notes

| Feature | v24.2 | v25.1 |
|---|---|---|
| Blazor designer | Preview quality | Production stable |
| .NET target | .NET 8 | .NET 8 / .NET 9 |
| AI-assisted creation | Experimental | Enhanced |

---

## Source Links

- Dashboards Module: https://docs.devexpress.com/eXpressAppFramework/117449/analytics
- XAF Dashboards: https://docs.devexpress.com/eXpressAppFramework/117449/analytics/dashboards
- DashboardData API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Dashboards.DashboardData
- IXafDashboardStorage: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Dashboards.IXafDashboardStorage
- DevExpress Dashboard Docs: https://docs.devexpress.com/Dashboard/15960
