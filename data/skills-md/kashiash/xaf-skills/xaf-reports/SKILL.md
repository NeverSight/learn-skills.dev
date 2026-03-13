---
name: xaf-reports
description: XAF Reports Module (XtraReports v2) - ReportsModuleV2 setup for Blazor and WinForms, report storage (DB/filesystem/custom IReportStorageWebExtension), creating predefined reports in code (PredefinedReportsUpdater), data sources (CollectionDataSource/EntityServerModeSource), report parameters, programmatic export (PDF/Excel/Word), in-app designer, PrintAction, security permissions for report design vs view. Use when working with DevExpress XtraReports integration in XAF.
---

# XAF: Reports Module (XtraReports)

## Setup

### NuGet Packages

```xml
<!-- Core -->
<PackageReference Include="DevExpress.ExpressApp.ReportsV2" Version="25.1.*" />
<!-- Blazor -->
<PackageReference Include="DevExpress.ExpressApp.ReportsV2.Blazor" Version="25.1.*" />
<!-- WinForms -->
<PackageReference Include="DevExpress.ExpressApp.ReportsV2.Win" Version="25.1.*" />
```

### Blazor Program.cs

```csharp
b.AddModule<ReportsModuleV2>(options => {
    options.ReportStoreMode = ReportStoreModes.XML; // or DB
    options.EnableInplaceReports = true; // show designer in browser
});

// Required for Blazor report viewer
services.AddDevExpressBlazorReporting();
```

### WinForms

```csharp
// In WinApplication.cs
Application.Modules.Add(new ReportsModuleV2 {
    ReportStoreMode = ReportStoreModes.XML
});
Application.Modules.Add(new ReportsWindowsFormsModuleV2());
```

---

## Report Storage

### Database Storage (default)

Reports stored in `ReportDataV2` persistent objects. Requires `DbSet<ReportDataV2>` (EF Core) or auto-added by XPO.

```csharp
// EF Core DbContext
public DbSet<ReportDataV2> ReportDataV2 { get; set; }
```

### XML / Filesystem Storage

```csharp
options.ReportStoreMode = ReportStoreModes.XML;
// Reports stored as .repx files in defined folder
```

### Custom Storage

```csharp
public class MyReportStorage : IReportStorageWebExtension {
    public bool CanSetData(string url) => true;
    public bool IsValidUrl(string url) => true;
    public byte[] GetData(string url) { /* load from DB/API */ }
    public Dictionary<string, string> GetUrls() { /* list all reports */ }
    public void SetData(XtraReport report, string url) { /* save */ }
    public string SetNewData(XtraReport report, string defaultUrl) { /* create new */ }
}

// Register:
ReportStorageWebExtension.RegisterExtensionGlobal(new MyReportStorage());
```

---

## Creating Predefined Reports in Code

```csharp
// 1. Define the report class (code-first)
public class ContactListReport : XtraReport {
    public ContactListReport() {
        // Report layout defined here or loaded from .repx
        var band = new DetailBand();
        var label = new XRLabel { DataBindings = { new XRBinding("Text", null, "FullName") } };
        band.Controls.Add(label);
        Bands.Add(band);
    }
}

// 2. Register via PredefinedReportsUpdater
public class MyPredefinedReportsUpdater : PredefinedReportsUpdater {
    public MyPredefinedReportsUpdater(
        IObjectSpaceFactory objectSpaceFactory,
        ITypesInfo typesInfo,
        Version currentApplicationVersion)
        : base(objectSpaceFactory, typesInfo, currentApplicationVersion) { }

    public override void AddPredefinedReports() {
        AddPredefinedReport<ContactListReport>(
            "Contact List",          // display name
            typeof(Contact),         // data type (for navigation)
            isInplaceReport: false); // true = shows inside Detail View
    }
}

// 3. Register the updater in Module.cs
public override void Setup(ApplicationModulesManager moduleManager) {
    base.Setup(moduleManager);
    if (Application != null) {
        Application.SetupComplete += (s, e) => {
            Application.ServiceProvider
                .GetRequiredService<PredefinedReportsUpdater>()
                .UpdatePredefinedReports();
        };
    }
}
```

---

## Data Sources

### CollectionDataSource (in-memory, from ObjectSpace)

```csharp
public class MyReport : XtraReport {
    public MyReport(IObjectSpace objectSpace) {
        var contacts = objectSpace.GetObjects<Contact>();
        DataSource = contacts;
        DataMember = "";
    }
}
```

### EntityServerModeSource (server-side processing — EF Core)

```csharp
using DevExpress.Data.Linq;

public class MyLargeReport : XtraReport {
    public MyLargeReport(IDbContextFactory<MyDbContext> factory) {
        var ctx = factory.CreateDbContext();
        DataSource = new EntityServerModeSource {
            KeyExpression = "ID",
            QueryableSource = ctx.Contacts.Where(c => c.Active)
        };
    }
}
```

---

## Report Parameters

```csharp
public class OrdersByDateReport : XtraReport {
    public OrdersByDateReport() {
        var fromDate = new Parameter {
            Name = "FromDate",
            Description = "From Date",
            Type = typeof(DateTime),
            Value = DateTime.Today.AddMonths(-1)
        };
        Parameters.Add(fromDate);

        // Use in filter:
        FilterString = "[OrderDate] >= ?FromDate";
    }
}
```

---

## Triggering Print Preview from Controller

```csharp
using DevExpress.ExpressApp.ReportsV2;

public class PrintOrderController : ObjectViewController<DetailView, Order> {
    private SimpleAction printAction;

    public PrintOrderController() {
        printAction = new SimpleAction(this, "PrintOrder", PredefinedCategory.View) {
            Caption = "Print"
        };
        printAction.Execute += PrintAction_Execute;
    }

    private void PrintAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
        var order = (Order)View.CurrentObject;
        var reportController = Frame.GetController<ReportServiceController>();

        // Show print preview
        reportController.ShowInReportDesignerAction.DoExecute(
            ObjectSpace.FindObject<ReportDataV2>(r => r.DisplayName == "Order Report"));
    }
}
```

---

## Programmatic Export

```csharp
using DevExpress.XtraReports.UI;
using DevExpress.ExpressApp.ReportsV2;

public async Task ExportReportToPdf(IObjectSpace objectSpace, string outputPath) {
    var reportData = objectSpace.FindObject<ReportDataV2>(
        CriteriaOperator.Parse("DisplayName = ?", "Contact List"));

    var report = ReportDataProvider.ReportsStorage.LoadReport(reportData);
    report.DataSource = objectSpace.GetObjects<Contact>();

    using var stream = new FileStream(outputPath, FileMode.Create);
    report.ExportToPdf(stream);
}

// Export options:
report.ExportToPdf(stream);
report.ExportToXlsx(stream);
report.ExportToDocx(stream);
report.ExportToHtml(stream);
```

---

## Security Permissions

| Permission | Role Capability |
|---|---|
| Read `ReportDataV2` | View/print reports |
| Write `ReportDataV2` | Edit reports in designer |
| Create `ReportDataV2` | Create new reports |
| Delete `ReportDataV2` | Delete reports |

```csharp
// Users can view but not design reports
role.AddTypePermission<ReportDataV2>(SecurityOperations.ReadOnlyAccess,
    SecurityPermissionState.Allow);

// Designers can create and edit
role.AddTypePermission<ReportDataV2>(SecurityOperations.FullAccess,
    SecurityPermissionState.Allow);
```

---

## In-App Report Designer

- **Blazor:** Embedded via `DxReportDesigner` component; requires `EnableInplaceReports = true`
- **WinForms:** Native XtraReport Designer hosted within application

---

## v24.2 vs v25.1 Notes

- v24.2: `ReportsModuleV2` stable API
- v25.1: Enhanced Blazor viewer performance; .NET 9 support; improved parameter UI

---

## Source Links

- Reports Module: https://docs.devexpress.com/eXpressAppFramework/113591/shape-export-print-data/reports
- Create Reports: https://docs.devexpress.com/eXpressAppFramework/113792/shape-export-print-data/reports/create-reports
- Print Preview: https://docs.devexpress.com/eXpressAppFramework/113788/shape-export-print-data/reports/print-preview
- PredefinedReportsUpdater: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.ReportsV2.PredefinedReportsUpdater
- IReportStorageWebExtension: https://docs.devexpress.com/XtraReports/DevExpress.XtraReports.Web.Extensions.ReportStorageWebExtension
