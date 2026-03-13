---
name: xaf-nonpersistent
description: XAF NonPersistent objects - [DomainComponent] attribute, NonPersistentBaseObject base class, AddNonPersistent() registration, ObjectsGetting/ObjectByKeyGetting events with DynamicCollection, PopupWindowShowAction for input dialogs using non-persistent objects, linking to persistent objects, refresh patterns, RemoveFromModifiedObjects, common pitfalls. Use when building custom data sources, API wrappers, input forms, or computed views without database persistence in DevExpress XAF.
---

# XAF: NonPersistent Objects

## What Are NonPersistent Objects

NonPersistent objects are business classes for which XAF generates full UI (List Views, Detail Views, Actions) but which are **not mapped to any database table**. They hold data loaded from external sources, computed at runtime, or used as temporary input forms.

- Decorated with `[DomainComponent]` attribute (NOT `[NonPersistent]` from XPO — different meaning!)
- Do **NOT** inherit from XPO persistent base classes (causes `SessionMixingException`)
- Managed by `NonPersistentObjectSpace`
- Must register `.AddNonPersistent()` in app builder

---

## Use Cases

- Display data from external REST APIs / stored procedures
- Intermediate input forms (collect parameters before executing an action)
- Computed aggregates / dashboards with no DB binding
- PopupWindowShowAction dialogs for user input
- Settings/configuration screens without persistence

---

## Base Classes

| Class | IObjectSpaceLink | Auto Key | Notes |
|---|---|---|---|
| `NonPersistentBaseObject` | Yes | Yes (Guid Oid) | **Recommended default** |
| `NonPersistentLiteObject` | No | Yes | Lightweight |
| `NonPersistentObjectImpl` | Yes | No | Manual key |

---

## Basic NonPersistent Object

```csharp
using DevExpress.ExpressApp;
using DevExpress.ExpressApp.DC;

[DomainComponent]
public class ContactSummary : NonPersistentBaseObject {
    private string name;
    private string email;
    private int orderCount;

    public string Name {
        get => name;
        set => SetPropertyValue(ref name, value);
    }

    public string Email {
        get => email;
        set => SetPropertyValue(ref email, value);
    }

    public int OrderCount {
        get => orderCount;
        set => SetPropertyValue(ref orderCount, value);
    }
}
```

`SetPropertyValue` (from `NonPersistentBaseObject`) triggers `INotifyPropertyChanged` automatically.

For Blazor, always declare an explicit key:
```csharp
[Browsable(false)]
[DevExpress.ExpressApp.Data.Key]
public Guid Oid { get; set; } = Guid.NewGuid();
```

---

## Registration

```csharp
// Startup.cs / Program.cs — MUST be after persistent providers
builder.ObjectSpaceProviders
    .AddSecuredEFCoreObjectSpaceProvider<MyDbContext>(...)  // persistent first
    .AddNonPersistent();                                     // non-persistent last
```

The type must be in the module's `ExportedTypes` or declared via `[DomainComponent]`.

---

## ObjectsGetting Event — Providing Data for List Views

Primary pattern for populating non-persistent collections:

```csharp
public class ContactSummaryController : WindowController {
    protected override void OnActivated() {
        base.OnActivated();
        Application.ObjectSpaceCreated += Application_ObjectSpaceCreated;
    }

    protected override void OnDeactivated() {
        Application.ObjectSpaceCreated -= Application_ObjectSpaceCreated;
        base.OnDeactivated();
    }

    private void Application_ObjectSpaceCreated(object sender, ObjectSpaceCreatedEventArgs e) {
        if (e.ObjectSpace is NonPersistentObjectSpace npos) {
            npos.ObjectsGetting += NonPersistentObjectSpace_ObjectsGetting;
        }
    }

    private void NonPersistentObjectSpace_ObjectsGetting(object sender, ObjectsGettingEventArgs e) {
        if (e.ObjectType != typeof(ContactSummary)) return;

        var npos = (NonPersistentObjectSpace)sender;
        var items = LoadDataFromApi(); // IList<ContactSummary>

        var collection = new DynamicCollection(npos, e.ObjectType, e.Criteria, e.Sorting, e.InTransaction);
        collection.FetchObjects += (s, args) => {
            args.Objects = items;
            args.ShapeData = true; // XAF applies criteria/sorting to the list
        };
        e.Objects = collection;
    }

    private IList<ContactSummary> LoadDataFromApi() {
        return new List<ContactSummary> {
            new ContactSummary { Name = "Alice", Email = "alice@example.com", OrderCount = 5 },
            new ContactSummary { Name = "Bob",   Email = "bob@example.com",   OrderCount = 2 }
        };
    }
}
```

`ShapeData = true` automatically applies `e.Criteria` and `e.Sorting` to your list.

---

## ObjectByKeyGetting — Single Object Fetch

Used when XAF needs to retrieve a single object by key (e.g., navigation to Detail View):

```csharp
npos.ObjectByKeyGetting += (sender, e) => {
    if (e.ObjectType != typeof(ContactSummary)) return;
    var key = (Guid)e.Key;
    e.Object = FetchSingleContact(key);
};
```

---

## ObjectDeleting / ObjectsDeleting

```csharp
npos.ObjectDeleting += (sender, e) => {
    if (e.Object is ContactSummary summary)
        ExternalCache.Remove(summary.Oid);
};

npos.ObjectsDeleting += (sender, e) => {
    foreach (ContactSummary obj in e.Objects.OfType<ContactSummary>())
        ExternalCache.Remove(obj.Oid);
};
```

---

## Using with PopupWindowShowAction

Classic pattern: show non-persistent form as popup to collect user input, then act on result:

```csharp
public class SendEmailController : ObjectViewController<ListView, Contact> {
    private PopupWindowShowAction sendEmailAction;

    public SendEmailController() {
        sendEmailAction = new PopupWindowShowAction(this, "SendEmail", "Edit") {
            Caption = "Send Email"
        };
        sendEmailAction.CustomizePopupWindowParams += Action_CustomizePopupWindowParams;
        sendEmailAction.Execute += Action_Execute;
    }

    private void Action_CustomizePopupWindowParams(
        object sender, CustomizePopupWindowParamsEventArgs e) {
        var os = Application.CreateObjectSpace(typeof(EmailParams));
        var emailParams = os.CreateObject<EmailParams>();

        // Pre-fill from current selection
        emailParams.To = View.SelectedObjects.OfType<Contact>()
            .Select(c => c.Email).FirstOrDefault();

        // Suppress "save changes" dialog
        ((NonPersistentObjectSpace)os).RemoveFromModifiedObjects(emailParams);

        e.View = Application.CreateDetailView(os, emailParams);
    }

    private void Action_Execute(object sender, PopupWindowShowActionExecuteEventArgs e) {
        var emailParams = (EmailParams)e.PopupWindowViewCurrentObject;
        EmailService.Send(emailParams.To, emailParams.Subject, emailParams.Body);
    }
}

[DomainComponent]
public class EmailParams : NonPersistentBaseObject {
    private string to, subject, body;
    public string To      { get => to;      set => SetPropertyValue(ref to, value); }
    public string Subject { get => subject; set => SetPropertyValue(ref subject, value); }
    [FieldSize(FieldSizeAttribute.Unlimited)]
    public string Body    { get => body;    set => SetPropertyValue(ref body, value); }
}
```

---

## Relations with Persistent Objects

```csharp
[DomainComponent]
public class OrderReport : NonPersistentBaseObject {
    // Reference to persistent Customer — load via nested IObjectSpace
    public Customer Customer { get; set; }
}

// In ObjectsGetting:
var persistentOs = Application.CreateObjectSpace(typeof(Customer));
var customer = persistentOs.GetObjectByKey<Customer>(customerId);
// assign to non-persistent object's property
```

---

## Refreshing NonPersistent Data

```csharp
// From a controller action — fires ObjectsGetting again
View.ObjectSpace.Refresh();

// Or via built-in Refresh action:
Frame.GetController<RefreshController>().RefreshAction.DoExecute();
```

---

## Suppressing "Save Changes" Dialog

```csharp
var os = Application.CreateObjectSpace(typeof(EmailParams));
var obj = os.CreateObject<EmailParams>();
// ... populate obj ...
((NonPersistentObjectSpace)os).RemoveFromModifiedObjects(obj);
e.View = Application.CreateDetailView(os, obj);
```

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Inheriting XPO base class + `[DomainComponent]` | Use only `[DomainComponent]` on a POCO |
| Missing explicit `[Key]` in Blazor | Blazor requires `[DevExpress.ExpressApp.Data.Key]` property |
| NonPersistent as FIRST object space provider | Always register **after** persistent providers |
| `ObjectsGetting` not firing | Check `AddNonPersistent()` is registered and type is in `ExportedTypes` |
| Unexpected save dialog | Call `RemoveFromModifiedObjects()` after programmatic creation |
| Collections of persistent objects mixing object spaces | Load them via nested `IObjectSpace` from the parent |

---

## Source Links

- NonPersistent Objects: https://docs.devexpress.com/eXpressAppFramework/116516/business-model-design-orm/non-persistent-objects
- NonPersistent in XAF UI: https://docs.devexpress.com/eXpressAppFramework/113471/business-model-design-orm/non-persistent-objects/non-persistent-objects-in-the-xaf-ui
- NonPersistentObjectSpace API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.NonPersistentObjectSpace
- DynamicCollection: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.DynamicCollection
