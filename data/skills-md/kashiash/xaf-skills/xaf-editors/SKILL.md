---
name: xaf-editors
description: XAF built-in property editors and list editors - editor type mapping by data type, EditorAliases constants, [EditorAlias] attribute, [ModelDefault] for DisplayFormat/EditMask, ObjectPropertyEditor for inline sub-forms, list editor types (GridListEditor, DxGridListEditor, TreeListEditor, ChartListEditor), GridListEditor WinForms customization, DxGridListEditor Blazor customization, IModelListView/IModelColumn properties. Use when working with built-in XAF editors or customizing grid/list views.
---

# XAF: Property Editors & List Editors

## Built-in Property Editors

XAF automatically selects a property editor based on the .NET type.

| Data Type | Editor Alias | WinForms Class | Blazor Class |
|---|---|---|---|
| `string` | `StringPropertyEditor` | StringPropertyEditor | StringPropertyEditor |
| `int`, `long`, `short` | `IntegerPropertyEditor` | IntPropertyEditor | IntPropertyEditor |
| `decimal` | `DecimalPropertyEditor` | DecimalPropertyEditor | DecimalPropertyEditor |
| `double` | `DoublePropertyEditor` | DoublePropertyEditor | DoublePropertyEditor |
| `bool` | `BooleanPropertyEditor` | BooleanPropertyEditor | BooleanPropertyEditor |
| `DateTime` | `DateTimePropertyEditor` | DateTimePropertyEditor | DateTimePropertyEditor |
| `TimeSpan` | `TimeSpanPropertyEditor` | TimeSpanPropertyEditor | TimeSpanPropertyEditor |
| `enum` | `EnumPropertyEditor` | EnumPropertyEditor | EnumPropertyEditor |
| reference (FK) | `LookupPropertyEditor` | LookupPropertyEditor | LookupPropertyEditor |
| reference (inline) | `ObjectPropertyEditor` | ObjectPropertyEditor | ObjectPropertyEditor |
| `byte[]` / image | `ImagePropertyEditor` | ImagePropertyEditor | ImagePropertyEditor |
| `Color` | `ColorPropertyEditor` | ColorPropertyEditor | ColorPropertyEditor |
| file attachment | `FileDataPropertyEditor` | FileDataPropertyEditor | FileDataPropertyEditor |
| criteria | `CriteriaPropertyEditor` | CriteriaPropertyEditor | CriteriaPropertyEditor |
| HTML string | `HtmlPropertyEditor` | RichTextPropertyEditor | HtmlPropertyEditor |

All alias constants: `DevExpress.ExpressApp.Editors.EditorAliases`

---

## [EditorAlias] Attribute

Apply on a business class property to explicitly assign an editor:

```csharp
using DevExpress.ExpressApp.Editors;

public class Product {
    // Force Lookup instead of default ObjectPropertyEditor
    [EditorAlias(EditorAliases.LookupPropertyEditor)]
    public virtual Category Category { get; set; }

    // Use a custom registered alias
    [EditorAlias("MyCustomRatingEditor")]
    public virtual int Rating { get; set; }
}
```

Common `EditorAliases` constants:
- `EditorAliases.StringPropertyEditor`
- `EditorAliases.LookupPropertyEditor`
- `EditorAliases.ObjectPropertyEditor`
- `EditorAliases.ImagePropertyEditor`
- `EditorAliases.BooleanPropertyEditor`
- `EditorAliases.DateTimePropertyEditor`
- `EditorAliases.CriteriaPropertyEditor`
- `EditorAliases.IntegerPropertyEditor`
- `EditorAliases.DecimalPropertyEditor`
- `EditorAliases.EnumPropertyEditor`

You can also override per-property in the Application Model:
`BOModel > <Class> > OwnMembers > <Property> > PropertyEditorType`

---

## DisplayFormat / EditMask

Configure via `[ModelDefault]` attribute:

```csharp
using DevExpress.ExpressApp.Model;

public class Invoice {
    [ModelDefault("DisplayFormat", "{0:C2}")]
    [ModelDefault("EditMask", "c2")]
    [ModelDefault("EditMaskType", "Numeric")]
    public virtual decimal Total { get; set; }

    [ModelDefault("DisplayFormat", "{0:dd MMM yyyy}")]
    [ModelDefault("EditMask", "d")]
    [ModelDefault("EditMaskType", "DateTime")]
    public virtual DateTime InvoiceDate { get; set; }
}
```

`EditMaskType` values: `Simple`, `RegEx`, `DateTime`, `Numeric`

Alternative: set in **Model Editor** at `Views > <View> > Items > <Property> > DisplayFormat / EditMask`

---

## Inline Detail View (ObjectPropertyEditor)

Display a related object as an embedded sub-form instead of a popup/lookup:

```csharp
[EditorAlias(EditorAliases.ObjectPropertyEditor)]
public virtual Address ShippingAddress { get; set; }
```

In the Application Model, set the `View` property on the nested item to choose which `DetailView` template to embed.

---

## List Editors

| Editor | Platform | Use Case |
|---|---|---|
| `GridListEditor` | WinForms | Default tabular grid (XtraGrid) |
| `DxGridListEditor` | Blazor | Default tabular grid (DxGrid) |
| `TreeListEditor` | WinForms | Hierarchical tree |
| `DxTreeListEditor` | Blazor | Hierarchical table |
| `ChartListEditor` | WinForms | Chart visualization |
| `DxChartListEditor` | Blazor | Chart visualization |
| `PivotGridListEditor` | WinForms | Pivot table |
| `SchedulerListEditor` | WinForms | Calendar/scheduling |
| `CategorizedListEditor` | WinForms | Grid + category tree |

### Change List Editor for a View

In Application Model: `Views > <ClassName>_ListView > EditorType`

Or via attribute on custom editor:
```csharp
[ListEditor(typeof(MyObject), isDefault: true)]
public class MyCustomListEditor : ListEditor { ... }
```

---

## Customizing GridListEditor (WinForms)

```csharp
using DevExpress.ExpressApp.Win.Editors;
using DevExpress.XtraGrid.Views.Grid;

public class CustomizeGridController : ObjectViewController<ListView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();
        if (View.Editor is GridListEditor gridEditor) {
            GridView gridView = gridEditor.GridView;
            gridView.OptionsView.ShowGroupPanel = false;
            gridView.OptionsBehavior.Editable = false;
            gridView.Columns["Name"].Width = 200;
            gridView.Columns["Name"].Fixed = DevExpress.XtraGrid.Columns.FixedStyle.Left;
            gridView.Columns["Name"].SortOrder = DevExpress.Data.ColumnSortOrder.Ascending;
        }
    }
}
```

---

## Customizing DxGridListEditor (Blazor)

```csharp
using DevExpress.ExpressApp.Blazor.Editors;

public class CustomizeBlazorGridController : ObjectViewController<ListView, MyObject> {
    protected override void OnViewControlsCreated() {
        base.OnViewControlsCreated();
        if (View.Editor is DxGridListEditor gridEditor) {
            gridEditor.GridModel.ShowGroupPanel = false;
            gridEditor.GridModel.PageSize = 50;
            gridEditor.GridModel.ShowFilterRow = true;
        }
    }
}
```

---

## ListView Customization via Application Model

`IModelListView` key properties:

| Property | Description |
|---|---|
| `EditorType` | Which list editor class to use |
| `DefaultSorting` | Default sort, e.g. `Name Asc` |
| `Criteria` | Default filter criteria |
| `AllowEdit` | Enable inline editing |
| `MasterDetailMode` | How detail views open |
| `Columns` | Per-column settings |

`IModelColumn` key properties:

| Property | Description |
|---|---|
| `Caption` | Column header text |
| `Width` | Column width in pixels |
| `Index` | Display order (0-based) |
| `Visible` | Show/hide column |
| `SortOrder` | `Ascending` / `Descending` |
| `GroupIndex` | Group row index (≥0 to group) |
| `Format` | Display format string |
| `PropertyEditorType` | Override editor for this column |

---

## Source Links

- Property Editors: https://docs.devexpress.com/eXpressAppFramework/113014/ui-construction/view-items-and-property-editors/property-editors
- View Items and Property Editors: https://docs.devexpress.com/eXpressAppFramework/113610/ui-construction/view-items-and-property-editors
- List Editors: https://docs.devexpress.com/eXpressAppFramework/113189/ui-construction/list-editors
- EditorAliases API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Editors.EditorAliases._members
- PropertyEditorAttribute: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Editors.PropertyEditorAttribute
- ListEditorAttribute: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.Editors.ListEditorAttribute
