---
name: xaf-winforms-ui
description: XAF WinForms UI platform - WinApplication setup, Ribbon vs Standard toolbar, WinForms-specific editors (XtraGrid, DevExpress controls), Detail View layout customization via Layout Manager, custom WinForms controls embedded in XAF views, background workers for thread-safe UI updates, splash screen customization, WinForms navigation (NavigationFrame), printing/preview in WinForms, ClickOnce/MSI deployment. Use when building or customizing XAF WinForms applications.
---

# XAF: WinForms UI Platform

## Application Setup

```csharp
// Program.cs
[STAThread]
static void Main() {
    Application.EnableVisualStyles();
    Application.SetCompatibleTextRenderingDefault(false);

    var winApplication = new MyWinApplication();
    winApplication.Setup();
    winApplication.Start();
}
```

```csharp
// WinApplication.cs
public class MyWinApplication : WinApplication {
    public MyWinApplication() {
        DatabaseUpdateMode = DatabaseUpdateMode.UpdateDatabaseAlways;
        CheckCompatibilityType = CheckCompatibilityType.DatabaseSchema;
    }

    protected override void OnSetupStarted() {
        base.OnSetupStarted();
        ConnectionString = ConfigurationManager.ConnectionStrings["Default"].ConnectionString;
    }
}
```

---

## Ribbon vs Standard Toolbar

### Switch to Ribbon

```csharp
// In WinApplication.cs constructor
UseOldTemplates = false; // uses Ribbon template by default

// Or explicitly set in Model Editor:
// Application > Options > FormStyle = Ribbon
```

### Customize Ribbon Categories

```csharp
// Via Application Model:
// ActionDesign > ActionToContainerMapping > ActionCategory → ContainerName
// NavigationItems > ... > Caption
```

### Custom Ribbon Button from Controller

```csharp
public class CustomRibbonController : WindowController {
    private SimpleAction customAction;

    public CustomRibbonController() {
        customAction = new SimpleAction(this, "CustomAction", "CustomCategory") {
            Caption = "Custom",
            ImageName = "Action_New",
            PaintStyle = ActionItemPaintStyle.CaptionAndImage
        };
        customAction.Execute += CustomAction_Execute;
    }
}
```

---

## WinForms-Specific Editors

| Data Type | WinForms Editor | DevExpress Control |
|---|---|---|
| string | `StringPropertyEditor` | `TextEdit` |
| int/decimal | `IntPropertyEditor` | `SpinEdit` |
| DateTime | `DateTimePropertyEditor` | `DateEdit` |
| bool | `BooleanPropertyEditor` | `CheckEdit` |
| enum | `EnumPropertyEditor` | `ComboBoxEdit` |
| reference | `LookupPropertyEditor` | `LookupEdit` |
| image | `ImagePropertyEditor` | `PictureEdit` |
| color | `ColorPropertyEditor` | `ColorEdit` |
| rich text | `RichTextPropertyEditor` | `RichEditControl` |
| file | `FileDataPropertyEditor` | custom with OpenFileDialog |

---

## Accessing DevExpress WinForms Controls

```csharp
using DevExpress.ExpressApp.Win.Editors;
using DevExpress.XtraGrid.Views.Grid;
using DevExpress.XtraEditors;

public class CustomizeWinFormsController : ObjectViewController<ListView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();

        // Access GridListEditor's underlying XtraGrid
        if (View.Editor is GridListEditor gridEditor) {
            GridView gridView = gridEditor.GridView;
            gridView.OptionsView.ShowGroupPanel = false;
            gridView.OptionsView.ShowFooter = true;

            // Configure column summaries
            foreach (GridColumn col in gridView.Columns) {
                if (col.FieldName == "Amount") {
                    col.Summary.Add(SummaryItemType.Sum, "Amount", "{0:C2}");
                }
            }
        }
    }
}

// Access DetailView editor control
public class DetailViewController : ObjectViewController<DetailView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();

        var nameEditor = View.FindItem("Name") as StringPropertyEditor;
        if (nameEditor?.Control is TextEdit textEdit) {
            textEdit.Properties.CharacterCasing = CharacterCasing.Upper;
        }
    }
}
```

---

## Layout Customization

### Via Model Editor (preferred)

Path: `Views > <ClassName>_DetailView > Layout`

Drag-and-drop property editors into groups, tabs, and columns.

### Programmatic Layout (from Controller)

```csharp
using DevExpress.ExpressApp.Win.Layout;
using DevExpress.XtraLayout;

public class LayoutController : ObjectViewController<DetailView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();

        // Access LayoutControl
        if (View.Control is DevExpress.ExpressApp.Win.Layout.XafLayoutControl layoutControl) {
            var root = layoutControl.Root;
            // Modify layout items, groups, visibility
        }
    }
}
```

---

## Background Workers (Thread Safety)

```csharp
public class LongOperationController : ViewController {
    private SimpleAction longAction;

    public LongOperationController() {
        longAction = new SimpleAction(this, "LongOp", PredefinedCategory.View) {
            Caption = "Run Long Operation"
        };
        longAction.Execute += LongAction_Execute;
    }

    private void LongAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
        var worker = new BackgroundWorker { WorkerReportsProgress = true };

        // Run on background thread
        worker.DoWork += (s, args) => {
            // Long-running work — NO access to UI or XAF objects here
            Thread.Sleep(3000);
            args.Result = "Done";
        };

        // Update UI on UI thread after completion
        worker.RunWorkerCompleted += (s, args) => {
            if (args.Error != null)
                throw new UserFriendlyException(args.Error.Message);

            View.ObjectSpace.Refresh();
            Application.ShowViewStrategy.ShowMessage(args.Result.ToString());
        };

        worker.RunWorkerAsync();
    }
}
```

**IMPORTANT:** Never access `IObjectSpace`, `View`, `Frame`, or XAF objects from the `DoWork` handler — they are not thread-safe.

---

## Splash Screen

```csharp
// Custom splash screen class
public class MySplashScreen : ISplashScreen {
    private SplashScreenForm form;

    public void Start() {
        form = new SplashScreenForm();
        form.Show();
    }

    public void Stop() {
        form?.Invoke(() => form.Close());
        form = null;
    }

    public void SetDisplayText(string displayText) {
        form?.Invoke(() => form.UpdateStatus(displayText));
    }
}

// Register in WinApplication.cs
protected override void CreateDefaultObjectSpaceProvider(CreateCustomObjectSpaceProviderEventArgs args) {
    base.CreateDefaultObjectSpaceProvider(args);
    SplashScreen = new MySplashScreen();
}
```

---

## WinForms Navigation

```csharp
// Default: NavigationFrame with accordion/tree navigation
// To change navigation style in Application Model:
// Application > Options > NavigationStyle = Tree | Accordion | NavBar

// Programmatic navigation from controller:
var detailView = Application.CreateDetailView(objectSpace, targetObject);
Application.ShowViewStrategy.ShowView(
    new ShowViewParameters(detailView), new ShowViewSource(Frame, null));
```

---

## Printing / Print Preview

```csharp
using DevExpress.ExpressApp.ReportsV2;

// Built-in print via XtraReports:
var reportController = Frame.GetController<ReportServiceController>();
reportController.ShowPreviewAction.DoExecute(reportData);

// Direct XtraGrid printing:
if (View.Editor is GridListEditor editor) {
    editor.GridView.ShowPrintPreview();
}
```

---

## Source Links

- WinForms Getting Started: https://docs.devexpress.com/eXpressAppFramework/402684/getting-started/in-depth-tutorial-winforms-webforms
- WinForms UI Customization: https://docs.devexpress.com/eXpressAppFramework/113072/ui-construction/windows-forms-ui-customization
- WinApplication API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Win.WinApplication
- GridListEditor API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Win.Editors.GridListEditor
