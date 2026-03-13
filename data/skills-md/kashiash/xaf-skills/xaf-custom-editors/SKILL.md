---
name: xaf-custom-editors
description: XAF custom property and list editors - BlazorPropertyEditorBase with ComponentModelBase and Razor component, WinForms WinPropertyEditor/DXPropertyEditor with CreateControlCore/OnControlValueChanged/BreakLinksToControl, custom ListEditor implementation with all required members, attribute-based and manual EditorDescriptorsFactory registration, accessing editors from controllers. Use when building custom controls, third-party component wrappers, or specialized editors in DevExpress XAF Blazor or WinForms.
---

# XAF: Custom Property Editors & List Editors

## When to Build a Custom Editor

- Wrap a third-party control not natively supported by XAF
- Display data in a specialized way (color picker, rating stars, progress ring)
- Combine multiple properties into one visual component
- Use a platform-specific control (Blazor component library, WinForms control)

---

## Blazor Custom Property Editor

### Base Class

Inherit from `BlazorPropertyEditorBase` (namespace: `DevExpress.ExpressApp.Blazor.Editors`).

```csharp
using DevExpress.ExpressApp.Blazor.Editors;
using DevExpress.ExpressApp.Model;
using DevExpress.ExpressApp.Editors;

[PropertyEditor(typeof(int), "RatingPropertyEditor", false)]
public class RatingPropertyEditor : BlazorPropertyEditorBase {
    public RatingPropertyEditor(Type objectType, IModelMemberViewItem model)
        : base(objectType, model) { }

    protected override IComponentModel CreateComponentAdapter() {
        return new RatingComponentModel();
    }

    protected override IComponentModel CreateViewerComponentAdapter() {
        return new RatingComponentModel { ReadOnly = true };
    }

    protected override object GetControlValueCore() {
        return ((RatingComponentModel)ComponentModel).Value;
    }

    protected override void ReadValueToControl(object value) {
        if (ComponentModel is RatingComponentModel model)
            model.Value = value is int v ? v : 0;
    }
}
```

### ComponentModel (Blazor bridge)

```csharp
using DevExpress.ExpressApp.Blazor.Editors.Adapters;

public class RatingComponentModel : ComponentModelBase {
    private int value;
    private bool readOnly;

    public int Value {
        get => value;
        set {
            SetProperty(ref this.value, value);
            ValueChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    public bool ReadOnly {
        get => readOnly;
        set => SetProperty(ref readOnly, value);
    }

    public event EventHandler ValueChanged;
    public override Type ComponentType => typeof(RatingEditorComponent);
}
```

### Razor Component

```razor
@* RatingEditorComponent.razor *@
<div class="rating-editor">
    @for (int i = 1; i <= 5; i++) {
        int star = i;
        <span class="@(star <= Model.Value ? "star filled" : "star")"
              @onclick="() => OnStarClick(star)">★</span>
    }
</div>

@code {
    [Parameter]
    public RatingComponentModel Model { get; set; }

    private void OnStarClick(int star) {
        if (!Model.ReadOnly) Model.Value = star;
    }
}
```

### Registration via [PropertyEditor] Attribute

```csharp
// [PropertyEditor(typeof(PropertyType), "AliasString", isDefault)]
[PropertyEditor(typeof(int), "RatingPropertyEditor", false)]
// isDefault: true  → auto-applied to ALL int properties
// isDefault: false → must assign via [EditorAlias] or Application Model
```

Assign to a specific property:
```csharp
[EditorAlias("RatingPropertyEditor")]
public virtual int StarRating { get; set; }
```

---

## WinForms Custom Property Editor

### WinPropertyEditor (standard WinForms controls)

```csharp
using DevExpress.ExpressApp.Win.Editors;
using DevExpress.ExpressApp.Editors;
using DevExpress.ExpressApp.Model;

[PropertyEditor(typeof(int), "TrackBarPropertyEditor", false)]
public class TrackBarPropertyEditor : WinPropertyEditor {
    public TrackBarPropertyEditor(Type objectType, IModelMemberViewItem model)
        : base(objectType, model) { }

    protected override object CreateControlCore() {
        var trackBar = new TrackBar {
            Minimum = 0,
            Maximum = 100,
            TickFrequency = 10
        };
        trackBar.Scroll += TrackBar_Scroll;
        ControlBindingProperty = nameof(TrackBar.Value); // auto data binding
        return trackBar;
    }

    private void TrackBar_Scroll(object sender, EventArgs e) {
        OnControlValueChanged(); // notify XAF that value changed
    }

    protected override void BreakLinksToControl(bool unwireEventsOnly) {
        if (Control is TrackBar trackBar)
            trackBar.Scroll -= TrackBar_Scroll;
        base.BreakLinksToControl(unwireEventsOnly);
    }

    public new TrackBar Control => (TrackBar)base.Control;
}
```

### DXPropertyEditor (DevExpress controls with RepositoryItem)

```csharp
using DevExpress.XtraEditors;
using DevExpress.XtraEditors.Repository;
using DevExpress.ExpressApp.Win.Editors;

[PropertyEditor(typeof(int), "SpinEditPropertyEditor", false)]
public class SpinEditPropertyEditor : DXPropertyEditor {
    public SpinEditPropertyEditor(Type objectType, IModelMemberViewItem model)
        : base(objectType, model) { }

    protected override void SetupRepositoryItem(RepositoryItem item) {
        base.SetupRepositoryItem(item);
        if (item is RepositoryItemSpinEdit spinItem) {
            spinItem.MinValue = 0;
            spinItem.MaxValue = 999;
            spinItem.IsFloatValue = false;
        }
    }

    protected override object CreateControlCore() {
        return new SpinEdit();
    }
}
```

### Required Override Summary (WinForms)

| Member | Purpose |
|---|---|
| `CreateControlCore()` | Instantiate and configure control; return it |
| `OnControlValueChanged()` | Call from control's change event |
| `ControlBindingProperty` | Names control property for auto data binding |
| `BreakLinksToControl(bool)` | Unsubscribe events; base handles disposal |

---

## Custom List Editor

```csharp
using DevExpress.ExpressApp.Editors;
using DevExpress.ExpressApp.Model;

[ListEditor(typeof(object), isDefault: false)]
public class CardListEditor : ListEditor {
    private CardListControl control;

    public CardListEditor(IModelListView info) : base(info) { }

    protected override object CreateControlsCore() {
        control = new CardListControl();
        control.SelectionChanged += (s, e) => OnSelectionChanged();
        control.ItemDoubleClick += (s, e) => OnProcessSelectedItem();
        AssignDataSourceToControl(DataSource);
        return control;
    }

    protected override void AssignDataSourceToControl(IEnumerable dataSource) {
        if (control != null)
            control.DataSource = dataSource;
    }

    public override void Refresh() => control?.Refresh();

    public override IList GetSelectedObjects() =>
        control?.SelectedItems ?? new List<object>();

    public override SelectionType SelectionType => SelectionType.MultipleSelection;

    public override string[] RequiredProperties => Array.Empty<string>();

    public override object FocusedObject {
        get => control?.FocusedItem;
        set { if (control != null) control.FocusedItem = value; }
    }

    public override void Dispose() {
        control?.Dispose();
        control = null;
        base.Dispose();
    }
}
```

### Key ListEditor Members

| Member | Required | Purpose |
|---|---|---|
| `CreateControlsCore()` | Yes | Create and return the list control |
| `AssignDataSourceToControl(IEnumerable)` | Yes | Bind data to control |
| `Refresh()` | Yes | Reload/repaint control data |
| `GetSelectedObjects()` | Yes | Return currently selected objects |
| `SelectionType` | Yes | `None`, `SingleObject`, `MultipleSelection` |
| `RequiredProperties` | Yes | Property names the control needs |
| `FocusedObject` | Yes | Get/set the focused (current) object |
| `OnSelectionChanged()` | Call when selection changes | Fires `SelectionChanged` event |
| `OnProcessSelectedItem()` | Call on double-click | Opens Detail View |

---

## Manual Registration via EditorDescriptorsFactory

Override in your module (preferred for large apps — avoids attribute scanning):

```csharp
protected override void RegisterEditorDescriptors(EditorDescriptorsFactory factory) {
    base.RegisterEditorDescriptors(factory);

    factory.RegisterPropertyEditor(
        "RatingPropertyEditor",
        typeof(int),
        typeof(RatingPropertyEditor),
        isDefaultEditor: false);

    factory.RegisterListEditor(
        typeof(MyObject),
        typeof(CardListEditor),
        isDefaultEditor: true);
}
```

---

## Accessing Editors in Controllers

```csharp
// Property editor in DetailView
public class MyDetailViewController : ObjectViewController<DetailView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();
        var editor = View.FindItem("StarRating") as RatingPropertyEditor;
        if (editor?.ComponentModel is RatingComponentModel model) {
            // customize
        }
    }
}

// List editor in ListView
public class MyListViewController : ObjectViewController<ListView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();
        if (View.Editor is CardListEditor listEditor) {
            // access custom list editor members
        }
    }
}
```

---

## v24.2 vs v25.1 Notes

No breaking changes to the custom editor API between v24.2 and v25.1.
- Assembly version suffix changes (`v24.2.dll` → `v25.1.dll`)
- `DxGridListEditor` in Blazor: enhanced column API in v25.1
- .NET target: v24.2 supports .NET 8; v25.1 supports .NET 8 and .NET 9

---

## Source Links

- Custom Blazor Property Editor: https://docs.devexpress.com/eXpressAppFramework/113596/ui-construction/view-items-and-property-editors/implement-a-property-editor-based-on-a-custom-control-blazor
- Custom WinForms Property Editor: https://docs.devexpress.com/eXpressAppFramework/113576/ui-construction/view-items-and-property-editors/implement-a-property-editor-based-on-a-custom-control-winforms
- Custom List Editor: https://docs.devexpress.com/eXpressAppFramework/112729/ui-construction/list-editors/how-to-implement-a-list-editor
- BlazorPropertyEditorBase API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Blazor.Editors.BlazorPropertyEditorBase
- WinPropertyEditor API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Win.Editors.WinPropertyEditor
- ListEditor API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Editors.ListEditor
