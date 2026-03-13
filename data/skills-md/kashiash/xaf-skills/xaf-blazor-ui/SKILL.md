---
name: xaf-blazor-ui
description: XAF Blazor UI platform - BlazorApplication setup in Program.cs, AddXaf/AddXafBlazor services, InvokeAsync thread safety (critical for Blazor Server), async controller actions pattern, Blazor-specific editors, embedding custom Razor components as ViewItems using IComponentContentHolder, JavaScript interop via IJSRuntime, Detail View layout customization (tabs/groups), programmatic navigation, error handling with UserFriendlyException, SignalR configuration. Use when building or customizing XAF Blazor Server applications.
---

# XAF: Blazor UI Platform

## Application Setup

```csharp
// Program.cs (minimal hosting model, .NET 8+)
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddXaf(builder.Configuration, b => {
    b.UseApplication<MyBlazorApplication>();
    b.AddObjectSpaceProviders(providers => {
        providers.UseEntityFramework(ef => {
            ef.DefaultDatabaseConnection("Default", p =>
                p.UseDbContext<MyDbContext>());
        });
        providers.AddNonPersistent();
    });
    b.Security
        .UseIntegratedMode(options => {
            options.RoleType = typeof(PermissionPolicyRole);
            options.UserType = typeof(ApplicationUser);
        })
        .AddPasswordAuthentication();
    b.AddModules(typeof(MyModule), typeof(ValidationModule));
});

builder.Services.AddDevExpressBlazor();

var app = builder.Build();
app.UseXaf();
app.UseStaticFiles();
app.UseAntiforgery();
app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
app.Run();
```

```csharp
// BlazorApplication.cs
public class MyBlazorApplication : BlazorApplication {
    public MyBlazorApplication() {
        DatabaseUpdateMode = DatabaseUpdateMode.UpdateDatabaseAlways;
    }
    protected override void OnSetupStarted() {
        base.OnSetupStarted();
        // Initial setup configuration
    }
}
```

---

## Thread Safety — InvokeAsync (CRITICAL)

**Blazor Server** runs on a circuit with a synchronization context. When updating UI from an async operation or background thread, **always use `InvokeAsync`**.

```csharp
// CORRECT: async void for action handlers — NO ConfigureAwait(false)!
private async void MyAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
    try {
        // Long-running work — await normally
        var result = await myService.DoWorkAsync(); // NO ConfigureAwait(false)!

        // UI updates must be on the Blazor circuit thread
        View.ObjectSpace.CommitChanges();
        View.Refresh();
        Application.ShowViewStrategy.ShowMessage("Done", InformationType.Success);
    }
    catch (Exception ex) {
        throw new UserFriendlyException(ex.Message);
    }
}

// If called from non-Blazor thread (e.g., background service):
await Application.InvokeAsync(() => {
    View.Refresh();
    // any UI update
});
```

**Why ConfigureAwait(false) breaks Blazor:** It resumes on a thread pool thread, outside the Blazor circuit, causing `InvalidOperationException` on UI updates.

---

## Blazor-Specific Editors

| Editor | Data Type | Notes |
|---|---|---|
| `DxTextBoxPropertyEditor` | `string` | DevExpress DxTextBox |
| `DxDateEditPropertyEditor` | `DateTime` | DevExpress DxDateEdit |
| `DxComboBoxPropertyEditor` | `enum` | DevExpress DxComboBox |
| `DxCheckBoxPropertyEditor` | `bool` | DevExpress DxCheckBox |
| `DxSpinEditPropertyEditor` | numeric | DevExpress DxSpinEdit |
| `DxLookupPropertyEditor` | reference | Popup lookup |
| `DxTagBoxPropertyEditor` | collection | Tag selection |
| `HtmlContentPropertyEditor` | `string` | Renders HTML |

---

## Custom Razor Component as ViewItem

Embed a Razor component in a Detail View:

### 1. Create the Razor component

```razor
@* MyCustomComponent.razor *@
@inject IServiceProvider ServiceProvider

<div class="my-component">
    <h4>@Title</h4>
    @if (Model != null) {
        <p>Current value: @Model.SomeProperty</p>
    }
</div>

@code {
    [Parameter] public string Title { get; set; }
    [Parameter] public MyObject Model { get; set; }
}
```

### 2. Create the ComponentModel

```csharp
using DevExpress.ExpressApp.Blazor;

public class MyCustomComponentModel : ComponentModelBase {
    private MyObject model;

    public MyObject Model {
        get => model;
        set => SetProperty(ref model, value);
    }

    public override Type ComponentType => typeof(MyCustomComponent);
}
```

### 3. Create the ViewItem

```csharp
using DevExpress.ExpressApp.Blazor.Editors;
using DevExpress.ExpressApp.Editors;
using DevExpress.ExpressApp.Model;

[ViewItem(typeof(IModelViewItem))]
public class MyCustomViewItem : BlazorViewItem {
    private MyCustomComponentModel componentModel;

    public MyCustomViewItem(IModelViewItem model, Type objectType)
        : base(model, objectType) { }

    protected override IComponentModel CreateComponentAdapter() {
        componentModel = new MyCustomComponentModel();
        return componentModel;
    }

    public override void Refresh() {
        base.Refresh();
        componentModel.Model = CurrentObject as MyObject;
    }
}
```

### 4. Register ViewItem in Module

```csharp
public override void ExtendModelInterfaces(ModelInterfaceExtenders extenders) {
    base.ExtendModelInterfaces(extenders);
    extenders.Add<IModelViewItem, IModelMyCustomViewItem>();
}
```

---

## JavaScript Interop

```csharp
public class JsInteropController : ViewController {
    [Autowired]
    IJSRuntime jsRuntime;

    private SimpleAction callJsAction;

    public JsInteropController() {
        callJsAction = new SimpleAction(this, "CallJsAction", PredefinedCategory.View);
        callJsAction.Execute += CallJsAction_Execute;
    }

    private async void CallJsAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
        await jsRuntime.InvokeVoidAsync("console.log", "Hello from XAF!");
        await jsRuntime.InvokeVoidAsync("alert", "Action executed");
    }
}
```

Or inject via DI in the controller constructor:
```csharp
[ActivatorUtilitiesConstructor]
public MyController(IServiceProvider serviceProvider) : base() {
    jsRuntime = serviceProvider.GetRequiredService<IJSRuntime>();
}
```

---

## Detail View Layout Customization

Layout is defined in Application Model: `Views > <ClassName>_DetailView > Layout`

Programmatic via controller:
```csharp
// Access layout groups in the model
var detailViewModel = (IModelDetailView)Application.Model.Views["Contact_DetailView"];
// Navigate Layout node and modify group positions, visibility, captions, etc.
```

For runtime layout customization, use a `ViewController`:
```csharp
protected override void OnViewControlsCreated() {
    base.OnViewControlsCreated();
    // Expand specific tab by index
    if (View is DetailView detailView) {
        var tabControl = detailView.Items.OfType<TabbedGroupViewItem>().FirstOrDefault();
        // tabControl?.Control.SelectedTabIndex = 1;
    }
}
```

---

## Programmatic Navigation

```csharp
// Navigate to object's Detail View
var showViewParams = Application.CreateDetailViewShowViewParameters(
    targetObject, objectSpace);
Application.ShowViewStrategy.ShowView(showViewParams, new ShowViewSource(Frame, null));

// Navigate to ListView
var lvId = Application.FindListViewId(typeof(Order));
var lv = Application.CreateListView(lvId, true);
Application.ShowViewStrategy.ShowView(
    new ShowViewParameters(lv), new ShowViewSource(Frame, null));

// Show popup message
Application.ShowViewStrategy.ShowMessage("Operation complete", InformationType.Success, 3000);
```

---

## Error Handling

```csharp
// User-friendly error (shown as dialog, not crash)
throw new UserFriendlyException("Invalid operation: " + reason);

// Validation error in actions
try {
    await DoSomethingAsync();
}
catch (Exception ex) when (ex is not UserFriendlyException) {
    throw new UserFriendlyException($"Error: {ex.Message}");
}
```

---

## SignalR Configuration

```csharp
// Increase timeout for long operations
builder.Services.AddSignalR(options => {
    options.ClientTimeoutInterval = TimeSpan.FromMinutes(5);
    options.HandshakeTimeout = TimeSpan.FromSeconds(30);
    options.MaximumReceiveMessageSize = 32 * 1024; // 32KB
});
```

---

## v24.2 vs v25.1 Notes

| Feature | v24.2 | v25.1 |
|---|---|---|
| .NET target | .NET 8 | .NET 8 / .NET 9 |
| Blazor render mode | Server | Server + enhanced SSR |
| DxGrid | v24.2 API | Enhanced column/toolbar API |
| InvokeAsync | Available | Available (same) |
| Report designer | Preview | Improved |

---

## Source Links

- Blazor Getting Started: https://docs.devexpress.com/eXpressAppFramework/402189/getting-started/in-depth-tutorial-blazor
- Blazor UI Customization: https://docs.devexpress.com/eXpressAppFramework/403372/ui-construction/blazor-ui-customization
- Custom Razor Components: https://docs.devexpress.com/eXpressAppFramework/404640/ui-construction/blazor-ui-customization/add-custom-razor-component
- BlazorApplication API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Blazor.BlazorApplication
- Blazor Editors: https://docs.devexpress.com/eXpressAppFramework/113610/ui-construction/view-items-and-property-editors/blazor-editors
