---
name: xaf-controllers
description: XAF Controllers and Actions - ViewController, ObjectViewController<TView,TObject>, WindowController, ApplicationController, controller lifecycle (OnActivated/OnDeactivated/OnViewControlsCreated/OnViewShown), SimpleAction/PopupWindowShowAction/SingleChoiceAction/ParametrizedAction full patterns, async actions in Blazor (async void + InvokeAsync), DialogController (SaveOnAccept/CanCloseWindow/Accepting/Cancelling), chaining consecutive popups, ObjectChanged/CurrentObjectChanged event refresh patterns, Frame/NestedFrame, Active/Enabled collections. Use when creating custom actions, controllers, or view logic in DevExpress XAF.
---

# XAF: Controllers & Actions

## Controller Types

| Type | Base Class | Typical Use |
|---|---|---|
| `ViewController` | `Controller` | Any view; most common base |
| `ViewController<TView>` | `ViewController` | Constrained to specific view type |
| `ObjectViewController<TView, TObject>` | `ViewController<TView>` | View + business object type — no manual casting |
| `WindowController` | `Controller` | Window-level; not tied to a view |
| `ApplicationController` | `Controller` | Global; activates for all views |

**Generic shorthand:**
```csharp
// Instead of TargetViewType + TargetObjectType + casting:
public class MyController : ObjectViewController<DetailView, Employee> {
    // View is DetailView, ViewCurrentObject is Employee — no cast needed
}
```

Place controllers in the platform-agnostic Module project (not in Blazor/WinForms projects) unless platform-specific.

---

## Controller Lifecycle

| Method | When Called | Typical Use |
|---|---|---|
| `OnActivated()` | Controller becomes active | Subscribe to view/object events, set initial state |
| `OnDeactivated()` | Controller becomes inactive | **Unsubscribe events**, release resources |
| `OnViewControlsCreated()` | After all UI controls created | Access and modify native UI controls |
| `OnViewShown()` | After view shown to user | Logic requiring fully rendered view |

```csharp
public class MyController : ViewController {
    private bool _eventsSubscribed;

    protected override void OnActivated() {
        base.OnActivated();
        if (!_eventsSubscribed) {
            View.CurrentObjectChanged += View_CurrentObjectChanged;
            View.ObjectSpace.ObjectChanged += ObjectSpace_ObjectChanged;
            _eventsSubscribed = true;
        }
    }

    protected override void OnDeactivated() {
        Unsubscribe();
        base.OnDeactivated();
    }

    // Always override Dispose — OnDeactivated is not always called before disposal
    protected override void Dispose(bool disposing) {
        if (disposing) Unsubscribe();
        base.Dispose(disposing);
    }

    private void Unsubscribe() {
        if (!_eventsSubscribed) return;
        if (View != null) View.CurrentObjectChanged -= View_CurrentObjectChanged;
        if (View?.ObjectSpace != null) View.ObjectSpace.ObjectChanged -= ObjectSpace_ObjectChanged;
        _eventsSubscribed = false;
    }

    private void View_CurrentObjectChanged(object sender, EventArgs e) { }
    private void ObjectSpace_ObjectChanged(object sender, ObjectChangedEventArgs e) { }
}
```

> **Memory leak risk:** Not unsubscribing events is the #1 cause of memory leaks in XAF. Always pair `+=` in `OnActivated` with `-=` in **both** `OnDeactivated` and `Dispose(bool)`. See `xaf-memory-leaks` for full patterns including `WeakEventSubscription` and resource tracker.

---

## Action Types

| Type | Class | UI | Use Case |
|---|---|---|---|
| Simple | `SimpleAction` | Button | Trigger an operation |
| Parametrized | `ParametrizedAction` | Button + text input | Search, filter by user-typed value |
| Single Choice | `SingleChoiceAction` | Dropdown / radio list | Pick from predefined options |
| Popup Window | `PopupWindowShowAction` | Button opens modal | Select objects or confirm via popup |

---

## SimpleAction — Full Pattern

```csharp
public class ClearTasksController : ViewController {
    private SimpleAction clearTasksAction;

    public ClearTasksController() {
        TargetViewType = ViewType.DetailView;
        TargetObjectType = typeof(Employee);

        clearTasksAction = new SimpleAction(this, "ClearTasksAction", PredefinedCategory.View) {
            Caption = "Clear Tasks",
            ConfirmationMessage = "Are you sure?",
            ImageName = "Action_Clear",
        };
        clearTasksAction.Execute += ClearTasksAction_Execute;
    }

    private void ClearTasksAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
        var employee = (Employee)View.CurrentObject;
        while (employee.DemoTasks.Count > 0)
            employee.DemoTasks.Remove(employee.DemoTasks[0]);
        View.ObjectSpace.CommitChanges();
        View.ObjectSpace.Refresh();
    }
}
```

---

## SimpleAction — Async Pattern (Blazor Critical!)

```csharp
// CORRECT: async void, no ConfigureAwait(false) in Blazor Server
private async void MyAction_Execute(object sender, SimpleActionExecuteEventArgs e) {
    try {
        var result = await myService.DoWorkAsync(); // NO ConfigureAwait(false)!
        View.ObjectSpace.CommitChanges();
        View.Refresh();
        Application.ShowViewStrategy.ShowMessage("Success");
    }
    catch (Exception ex) {
        throw new UserFriendlyException($"Error: {ex.Message}");
    }
}

// If updating UI from non-Blazor thread, use InvokeAsync:
await InvokeAsync(() => {
    View.Refresh();
});
// InvokeAsync is available in BlazorApplication and BlazorController
```

---

## PopupWindowShowAction — Full Pattern

```csharp
public class PopupNotesController : ViewController {
    private PopupWindowShowAction showNotesAction;

    public PopupNotesController() {
        TargetObjectType = typeof(DemoTask);
        TargetViewType = ViewType.DetailView;

        showNotesAction = new PopupWindowShowAction(this, "ShowNotesAction", PredefinedCategory.Edit) {
            Caption = "Show Notes",
            AcceptButtonCaption = "Select",   // custom button captions
            CancelButtonCaption = "Back"
        };
        showNotesAction.CustomizePopupWindowParams += Action_CustomizePopupWindowParams;
        showNotesAction.Execute += Action_Execute;
    }

    private void Action_CustomizePopupWindowParams(
        object sender, CustomizePopupWindowParamsEventArgs e) {
        // Option 1: show existing objects list
        e.View = Application.CreateListView(typeof(Note), true);

        // Option 2: show new-object detail view
        // IObjectSpace os = Application.CreateObjectSpace(typeof(Note));
        // e.View = Application.CreateDetailView(os, os.CreateObject<Note>());
        // e.DialogController.SaveOnAccept = true;  // save on Accept click
    }

    private void Action_Execute(
        object sender, PopupWindowShowActionExecuteEventArgs e) {
        var task = (DemoTask)View.CurrentObject;
        foreach (Note note in e.PopupWindowViewSelectedObjects) {
            if (!string.IsNullOrEmpty(task.Description))
                task.Description += Environment.NewLine;
            task.Description += note.Text;
        }
        View.ObjectSpace.CommitChanges();
    }
}
```

---

## DialogController

`DialogController` is a `WindowController` that manages popup windows — provides Accept/Cancel buttons and controls popup lifecycle.

**Accessed via** `CustomizePopupWindowParamsEventArgs.DialogController` or `Frame.GetController<DialogController>()`.

### Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `AcceptAction` | `SimpleAction` | — | The Accept button action; customize caption/active state |
| `CancelAction` | `SimpleAction` | — | The Cancel button action |
| `SaveOnAccept` | `bool` | `true` | Save Detail View changes when Accept is clicked |
| `CanCloseWindow` | `bool` | `true` | Whether popup closes automatically after Accept/Cancel |

### Key Events

| Event | When | Use |
|---|---|---|
| `Accepting` | Before Accept default behavior | Validate input, set `e.Cancel = true` to block |
| `Cancelling` | Before Cancel default behavior | Cleanup before close |

### DialogController Customization Example

```csharp
private void Action_CustomizePopupWindowParams(
    object sender, CustomizePopupWindowParamsEventArgs e) {
    var os = Application.CreateObjectSpace(typeof(InputObject));
    var inputObj = os.CreateObject<InputObject>();
    e.View = Application.CreateDetailView(os, inputObj);

    // Don't auto-save — handle manually in Execute
    e.DialogController.SaveOnAccept = false;

    // Customize Accept button
    e.DialogController.AcceptAction.Caption = "Confirm";

    // Validate before accepting
    e.DialogController.Accepting += (s, args) => {
        if (string.IsNullOrEmpty(inputObj.Name)) {
            args.Cancel = true;
            Application.ShowViewStrategy.ShowMessage(
                "Name is required", InformationType.Error);
        }
    };

    // Keep window open until explicitly closed
    e.DialogController.CanCloseWindow = false;
    e.DialogController.Accepting += (s, args) => {
        if (IsValid(inputObj)) {
            e.DialogController.CanCloseWindow = true;
        }
    };
}
```

### Access DialogController from Popup's Own Controller

If you place a controller inside the popup view, get `DialogController` from the Frame:

```csharp
public class PopupInnerController : ViewController {
    protected override void OnActivated() {
        base.OnActivated();
        // Works only inside a popup window frame
        var dialogController = Frame.GetController<DialogController>();
        if (dialogController != null) {
            dialogController.AcceptAction.Caption = "Apply";
            dialogController.Accepting += DialogController_Accepting;
        }
    }

    private void DialogController_Accepting(object sender, DialogControllerAcceptingEventArgs e) {
        // Access popup object and validate
        var obj = View.CurrentObject as MyObject;
        if (obj == null || !obj.IsValid) {
            e.Cancel = true;
        }
    }
}
```

---

## Chaining Consecutive Popups

To open a second popup after the first one is accepted, trigger the second `PopupWindowShowAction.DoExecute()` (or show a view manually) inside the first action's `Execute` handler.

### Pattern: Two Sequential Popups

```csharp
public class ChainedPopupController : ViewController {
    private PopupWindowShowAction firstPopupAction;
    private PopupWindowShowAction secondPopupAction;

    public ChainedPopupController() {
        firstPopupAction = new PopupWindowShowAction(this, "FirstPopupAction", PredefinedCategory.Edit) {
            Caption = "Step 1: Choose Category"
        };
        firstPopupAction.CustomizePopupWindowParams += FirstPopup_CustomizeParams;
        firstPopupAction.Execute += FirstPopup_Execute;

        secondPopupAction = new PopupWindowShowAction(this, "SecondPopupAction", PredefinedCategory.Edit) {
            Caption = "Step 2: Choose Item"
        };
        secondPopupAction.CustomizePopupWindowParams += SecondPopup_CustomizeParams;
        secondPopupAction.Execute += SecondPopup_Execute;

        // Hide second action from UI — triggered programmatically
        secondPopupAction.Active.SetItemValue("Manual", false);
    }

    private Category _selectedCategory;

    private void FirstPopup_CustomizeParams(object sender, CustomizePopupWindowParamsEventArgs e) {
        e.View = Application.CreateListView(typeof(Category), true);
    }

    private void FirstPopup_Execute(object sender, PopupWindowShowActionExecuteEventArgs e) {
        _selectedCategory = e.PopupWindowViewCurrentObject as Category;
        if (_selectedCategory != null) {
            // Open second popup immediately after first closes
            secondPopupAction.DoExecute();
        }
    }

    private void SecondPopup_CustomizeParams(object sender, CustomizePopupWindowParamsEventArgs e) {
        // Filter items by category selected in first popup
        var os = Application.CreateObjectSpace(typeof(Item));
        var items = os.GetObjects<Item>(
            CriteriaOperator.Parse("Category = ?", _selectedCategory));
        e.View = Application.CreateListView(os, Application.FindListViewId(typeof(Item)), true);
    }

    private void SecondPopup_Execute(object sender, PopupWindowShowActionExecuteEventArgs e) {
        var selectedItem = e.PopupWindowViewCurrentObject as Item;
        // Use selectedItem — both popups completed
        View.ObjectSpace.CommitChanges();
    }
}
```

### Pattern: Popup Opened from ShowViewStrategy (manual)

```csharp
private void FirstPopup_Execute(object sender, PopupWindowShowActionExecuteEventArgs e) {
    var firstResult = e.PopupWindowViewCurrentObject as Category;

    // Manually show second popup view
    var os = Application.CreateObjectSpace(typeof(Item));
    var obj = os.CreateObject<Item>();
    obj.Category = os.GetObject(firstResult);

    var detailView = Application.CreateDetailView(os, obj);
    var showParams = new ShowViewParameters(detailView) {
        TargetWindow = TargetWindow.NewModalWindow,
        Context = TemplateContext.PopupWindow
    };

    // Add a DialogController to the new popup window
    var dc = new DialogController();
    dc.SaveOnAccept = true;
    showParams.Controllers.Add(dc);

    Application.ShowViewStrategy.ShowView(showParams, new ShowViewSource(Frame, null));
}
```

**Important:**
- `secondAction.DoExecute()` — works cleanly when using `PopupWindowShowAction`
- `TargetWindow.NewModalWindow` with `ShowViewStrategy.ShowView` — for custom views without a pre-configured action
- Do NOT call `DoExecute()` inside `CustomizePopupWindowParams` — always in `Execute`

---

## View Refresh Patterns

### ObjectSpace.ObjectChanged — React to Property Changes

Fires when a persistent object's property value changes (tracked via `INotifyPropertyChanged`).

```csharp
protected override void OnActivated() {
    base.OnActivated();
    View.ObjectSpace.ObjectChanged += ObjectSpace_ObjectChanged;
}

private void ObjectSpace_ObjectChanged(object sender, ObjectChangedEventArgs e) {
    // e.Object      — the modified object
    // e.PropertyName — name of changed property (null if indeterminate)
    // e.OldValue    — previous value (XPO: only if passed to SetPropertyValue/OnChanged)
    // e.NewValue    — new value (EF Core: requires INotifyPropertyChanging + INotifyPropertyChanged)

    if (e.Object is OrderLine line && e.PropertyName == nameof(OrderLine.Quantity)) {
        line.TotalPrice = line.Quantity * line.UnitPrice;
    }
}

protected override void OnDeactivated() {
    View.ObjectSpace.ObjectChanged -= ObjectSpace_ObjectChanged;
    base.OnDeactivated();
}
```

**Note:** For XPO, `OldValue`/`NewValue` are only populated if the model calls `SetPropertyValue` or `OnChanged` with explicit old/new values. For EF Core, implement both `INotifyPropertyChanging` and `INotifyPropertyChanged` to get those values.

### View.CurrentObjectChanged — React to Navigation

Fires when the user navigates to a different record (focused object changes), not when properties change.

```csharp
protected override void OnActivated() {
    base.OnActivated();
    View.CurrentObjectChanged += View_CurrentObjectChanged;
}

private void View_CurrentObjectChanged(object sender, EventArgs e) {
    var current = View.CurrentObject as Employee;
    // Update action state or side-panel based on new current object
    myAction.Enabled.SetItemValue("HasObject", current != null);
}
```

### Refresh Reference

| Method | Scope | Use When |
|---|---|---|
| `ObjectSpace.ReloadObject(obj)` | Single object | Reload one object from DB (e.g., after external change) |
| `ObjectSpace.Refresh()` | All objects in OS | Full refresh; prompts save if uncommitted changes exist |
| `View.Refresh()` | UI display only | Redraw view after programmatic data change |
| `View.ObjectSpace.CommitChanges()` + `Refresh()` | Commit + reload | Standard post-save pattern |

```csharp
// Reload single object without affecting whole ObjectSpace
ObjectSpace.ReloadObject(View.CurrentObject);
View.Refresh();

// Full ObjectSpace refresh (may prompt user to save changes)
View.ObjectSpace.Refresh();

// Commit and refresh after action
ObjectSpace.CommitChanges();
View.ObjectSpace.Refresh();
```

### ObjectSpace.ModifiedChanged — React to Dirty State

```csharp
View.ObjectSpace.ModifiedChanged += (s, e) => {
    // ObjectSpace.IsModified changed
    saveAction.Enabled.SetItemValue("IsModified", View.ObjectSpace.IsModified);
};
```

---

## SingleChoiceAction — Full Pattern

```csharp
public class SetTaskController : ViewController {
    private SingleChoiceAction setTaskAction;

    public SetTaskController() {
        TargetObjectType = typeof(DemoTask);

        setTaskAction = new SingleChoiceAction(this, "SetTaskAction", PredefinedCategory.Edit) {
            Caption = "Set Task",
            ItemType = SingleChoiceActionItemType.ItemIsOperation,
            SelectionDependencyType = SelectionDependencyType.RequireMultipleObjects
        };

        var setPriorityItem = new ChoiceActionItem("Set Priority", null);
        setTaskAction.Items.Add(setPriorityItem);
        foreach (Priority value in Enum.GetValues(typeof(Priority))) {
            setPriorityItem.Items.Add(new ChoiceActionItem(value.ToString(), value));
        }

        setTaskAction.Execute += SetTaskAction_Execute;
    }

    private void SetTaskAction_Execute(object sender, SingleChoiceActionExecuteEventArgs e) {
        if (e.SelectedChoiceActionItem.Data is Priority priority) {
            foreach (DemoTask task in e.SelectedObjects.OfType<DemoTask>())
                task.Priority = priority;
            View.ObjectSpace.CommitChanges();
            View.ObjectSpace.Refresh();
        }
    }
}
```

---

## ParametrizedAction

```csharp
public class FindController : ViewController {
    private ParametrizedAction findAction;

    public FindController() {
        findAction = new ParametrizedAction(this, "FindByName", PredefinedCategory.View, typeof(string)) {
            Caption = "Find",
            NullValuePrompt = "Enter name..."
        };
        findAction.Execute += FindAction_Execute;
    }

    private void FindAction_Execute(object sender, ParametrizedActionExecuteEventArgs e) {
        var searchText = e.ParameterCurrentValue as string;
        if (string.IsNullOrEmpty(searchText)) return;

        var obj = ObjectSpace.FindObject<Contact>(
            CriteriaOperator.Parse("Contains([Name], ?)", searchText));
        if (obj != null)
            View.SelectObject(obj);
    }
}
```

---

## Activation Conditions

```csharp
// Active: action shown only if all values are true
MyAction.Active.SetItemValue("HasPermission", security.CanCreate(typeof(Order)));
MyAction.Active.SetItemValue("IsCorrectView", View is DetailView);

// Enabled: action visible but grayed out if any value is false
MyAction.Enabled.SetItemValue("HasSelection", View.SelectedObjects.Count > 0);
```

---

## Frame & NestedFrame

```csharp
// Access nested frame (e.g., in a MasterDetail view)
if (Frame is NestedFrame nestedFrame) {
    var parentController = nestedFrame.ParentFrame
        .GetController<ParentViewController>();
}

// Find controller in current frame
var refreshCtrl = Frame.GetController<RefreshController>();
refreshCtrl?.RefreshAction.DoExecute();
```

---

## Common Patterns

```csharp
// Show message
Application.ShowViewStrategy.ShowMessage("Operation complete", InformationType.Success);

// Navigate to object detail view
var showViewParams = Application.CreateDetailViewShowViewParameters(obj, objectSpace);
Application.ShowViewStrategy.ShowView(showViewParams, new ShowViewSource(Frame, null));

// Navigate programmatically to ListView
var listView = Application.CreateListView(typeof(Order), true);
Application.ShowViewStrategy.ShowView(
    new ShowViewParameters(listView), new ShowViewSource(Frame, null));

// Find objects
var obj = ObjectSpace.FindObject<Contact>(
    CriteriaOperator.Parse("Email = ?", "user@example.com"));
var selected = View.SelectedObjects.OfType<Employee>().ToList();
```

---

## Related Skills

- `xaf-memory-leaks` — full disposal patterns, WeakEventSubscription, ObjectSpace lifetime, diagnostic tools

## Source Links

- Controllers: https://docs.devexpress.com/eXpressAppFramework/112623/ui-construction/controllers-and-actions/controllers
- Actions: https://docs.devexpress.com/eXpressAppFramework/112622/ui-construction/controllers-and-actions/actions
- DialogController: https://docs.devexpress.com/eXpressAppFramework/112805/ui-construction/controllers-and-actions/dialog-controller
- DialogController API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.SystemModule.DialogController
- PopupWindowShowAction How-To: https://docs.devexpress.com/eXpressAppFramework/113539/ui-construction/controllers-and-actions/actions/how-to-create-and-use-a-popup-window-action
- Add Actions to Popup: https://docs.devexpress.com/eXpressAppFramework/112804/ui-construction/controllers-and-actions/add-actions-to-a-popup-window
- ObjectChanged Event: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.IObjectSpace.ObjectChanged
- Execute Logic on Property Change: https://docs.devexpress.com/eXpressAppFramework/403621/data-manipulation-and-business-logic/create-read-update-and-delete-data/execute-business-logic-when-a-property-is-changed-and-track-modifications-in-objects
- Refresh Objects: https://docs.devexpress.com/eXpressAppFramework/403622/data-manipulation-and-business-logic/create-read-update-and-delete-data/refresh-objects-and-rollback-changes
