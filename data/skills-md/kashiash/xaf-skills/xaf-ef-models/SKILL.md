---
name: xaf-ef-models
description: XAF Entity Framework Core business object models - BaseObject base class, IXafEntityObject/IObjectSpaceLink/IOptimisticLock interfaces, virtual properties, DbContext setup with IDbContextFactory, one-to-many/many-to-many/one-to-one relations via navigation properties, EF Core migrations in XAF, computed columns, ObservableCollection. Use when defining business objects with EF Core ORM in DevExpress XAF.
---

# XAF: EF Core Business Object Models

## Setup

### NuGet Packages

```xml
<PackageReference Include="DevExpress.Persistent.BaseImpl.EFCore" Version="25.1.*" />
<PackageReference Include="DevExpress.ExpressApp.EFCore" Version="25.1.*" />
<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.*" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.*" />
<!-- For change tracking and lazy loading proxies -->
<PackageReference Include="Microsoft.EntityFrameworkCore.Proxies" Version="8.*" />
```

### DbContext (XAF style)

```csharp
using DevExpress.Persistent.BaseImpl.EF;
using Microsoft.EntityFrameworkCore;

public class ApplicationDbContext : DbContext {
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }

    public DbSet<Contact> Contacts { get; set; }
    public DbSet<Department> Departments { get; set; }
    // Required XAF built-in tables:
    public DbSet<ModelDifference> ModelDifferences { get; set; }
    public DbSet<ModelDifferenceAspect> ModelDifferenceAspects { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder) {
        base.OnModelCreating(modelBuilder);
        modelBuilder.HasChangeTrackingStrategy(
            ChangeTrackingStrategy.ChangingAndChangedNotificationsWithOriginalValues);
    }
}

// Required for migrations CLI
public class ApplicationDbContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext> {
    public ApplicationDbContext CreateDbContext(string[] args) {
        var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
        optionsBuilder.UseSqlServer("Server=(localdb)\\mssqllocaldb;Database=MyApp;Trusted_Connection=True;");
        optionsBuilder.UseChangeTrackingProxies();
        optionsBuilder.UseLazyLoadingProxies();
        return new ApplicationDbContext(optionsBuilder.Build());
    }
}
```

### XAF Application Setup (Program.cs)

```csharp
// CRITICAL: Use AddDbContextFactory, NOT AddDbContext
builder.Services.AddDbContextFactory<ApplicationDbContext>((sp, options) => {
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"));
    options.UseChangeTrackingProxies();  // REQUIRED for XAF property notifications
    options.UseLazyLoadingProxies();     // required for virtual navigation properties
});
```

---

## Base Interfaces / Classes

| Type | Purpose |
|---|---|
| `BaseObject` | **Use this.** Abstract base; Guid PK, all interfaces included |
| `IXafEntityObject` | OnCreated/OnLoaded/OnSaving lifecycle hooks |
| `IObjectSpaceLink` | Gives access to IObjectSpace from inside entity |
| `IOptimisticLock` | Optimistic concurrency (`LockToken` int column) |
| `IDeferredDeletion` | Soft-delete via GCRecord column |

**Always inherit from `BaseObject`** — it implements all interfaces automatically.

```csharp
// Minimal correct EF Core entity for XAF
using DevExpress.Persistent.BaseImpl.EF;

public class Contact : BaseObject {
    // Guid ID is in BaseObject — do NOT redefine it
    // All properties MUST be virtual for change-tracking + lazy loading proxies

    public virtual string FirstName { get; set; }
    public virtual string LastName { get; set; }
    public virtual string Email { get; set; }
    public virtual Department Department { get; set; }
}
```

**If you cannot inherit BaseObject** (existing hierarchy), implement manually:

```csharp
public class LegacyEntity : IXafEntityObject, IObjectSpaceLink, IOptimisticLock {
    [Key]
    public virtual Guid ID { get; set; } = Guid.NewGuid();

    [ConcurrencyCheck]
    public virtual int LockToken { get; protected set; }

    [NotMapped]
    IObjectSpace IObjectSpaceLink.ObjectSpace { get; set; }

    void IXafEntityObject.OnCreated() { ID = Guid.NewGuid(); }
    void IXafEntityObject.OnLoaded() { }
    void IXafEntityObject.OnSaving() { }
}
```

---

## Entity Configuration

### Data Annotations (simple cases)

```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class Product : BaseObject {
    [Required]
    [MaxLength(200)]
    public virtual string Name { get; set; }

    [Column("unit_price", TypeName = "decimal(18,2)")]
    public virtual decimal UnitPrice { get; set; }

    [NotMapped]   // Not stored in DB
    public virtual string DisplayLabel => $"{Name} (${UnitPrice})";
}
```

### Fluent API (OnModelCreating)

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder) {
    base.OnModelCreating(modelBuilder);
    modelBuilder.HasChangeTrackingStrategy(
        ChangeTrackingStrategy.ChangingAndChangedNotificationsWithOriginalValues);

    modelBuilder.Entity<Product>(entity => {
        entity.Property(e => e.Name).HasMaxLength(200).IsRequired();
        entity.Property(e => e.UnitPrice).HasColumnType("decimal(18,2)");
        entity.HasIndex(e => e.Name).IsUnique();
        entity.HasOne(e => e.Category)
              .WithMany(c => c.Products)
              .HasForeignKey("CategoryId")
              .OnDelete(DeleteBehavior.Restrict);
    });
}
```

---

## Relations

### One-to-Many

```csharp
public class Department : BaseObject {
    public virtual string Name { get; set; }
    // virtual + ObservableCollection required
    public virtual IList<Contact> Contacts { get; set; } = new ObservableCollection<Contact>();
}

public class Contact : BaseObject {
    public virtual string FullName { get; set; }
    public virtual Department Department { get; set; }
}
```

Fluent config if needed:
```csharp
modelBuilder.Entity<Contact>()
    .HasOne(c => c.Department)
    .WithMany(d => d.Contacts)
    .OnDelete(DeleteBehavior.SetNull);
```

### Many-to-Many (with explicit join entity — recommended in XAF)

```csharp
public class Employee : BaseObject {
    public virtual string Name { get; set; }
    public virtual IList<EmployeeTask> EmployeeTasks { get; set; }
        = new ObservableCollection<EmployeeTask>();
}

public class ProjectTask : BaseObject {
    public virtual string Title { get; set; }
    public virtual IList<EmployeeTask> EmployeeTasks { get; set; }
        = new ObservableCollection<EmployeeTask>();
}

// Explicit join entity (allows extra fields)
public class EmployeeTask : BaseObject {
    public virtual Employee Employee { get; set; }
    public virtual ProjectTask Task { get; set; }
    public virtual DateTime AssignedDate { get; set; }
}
```

### One-to-One

```csharp
public class Person : BaseObject {
    public virtual string Name { get; set; }
    public virtual PersonDetail Detail { get; set; }
}

public class PersonDetail : BaseObject {
    public virtual string Biography { get; set; }
    public virtual Person Person { get; set; }
}
```

Fluent config:
```csharp
modelBuilder.Entity<Person>()
    .HasOne(p => p.Detail)
    .WithOne(d => d.Person)
    .HasForeignKey<PersonDetail>("PersonId")
    .OnDelete(DeleteBehavior.Cascade);
```

---

## Lifecycle Hooks

```csharp
public class Order : BaseObject {
    public virtual string OrderNumber { get; set; }
    public virtual DateTime OrderDate { get; set; }
    public virtual OrderStatus Status { get; set; }

    public override void OnCreated() {
        base.OnCreated();
        OrderDate = DateTime.Now;
        Status = OrderStatus.New;
        OrderNumber = $"ORD-{DateTime.Now:yyyyMMdd}-{Guid.NewGuid().ToString()[..8].ToUpper()}";
    }

    public override void OnSaving() {
        base.OnSaving();
        if (((IObjectSpaceLink)this).ObjectSpace?.IsNewObject(this) == true)
            CreatedDate = DateTime.UtcNow;
        LastModified = DateTime.UtcNow;
    }

    public override void OnLoaded() {
        base.OnLoaded();
    }
}
```

---

## Migrations in XAF

```bash
# Package Manager Console
Add-Migration InitialCreate -Project YourDataProject -StartupProject YourStartupProject
Update-Database -Project YourDataProject -StartupProject YourStartupProject

# CLI
dotnet ef migrations add InitialCreate --project YourDataProject --startup-project YourStartupProject
dotnet ef database update --project YourDataProject --startup-project YourStartupProject
```

### Auto-migration on startup (via DatabaseVersionMismatch)

```csharp
public class MyModule : ModuleBase {
    public override void Setup(XafApplication application) {
        base.Setup(application);
        application.DatabaseVersionMismatch += (s, e) => {
            e.Updater.Update();
            e.Handled = true;
        };
    }
}
```

---

## Calculated Properties

```csharp
public class OrderLine : BaseObject {
    public virtual decimal UnitPrice { get; set; }
    public virtual int Quantity { get; set; }
    public virtual decimal Discount { get; set; }

    // NotMapped: pure C# calculation
    [NotMapped]
    public virtual decimal LineTotal => UnitPrice * Quantity * (1 - Discount);
}
```

DB-computed column (Fluent API):
```csharp
modelBuilder.Entity<OrderLine>()
    .Property(e => e.ComputedTotal)
    .HasComputedColumnSql("[UnitPrice] * [Quantity] * (1 - [Discount])", stored: true);
```

---

## EF Core vs XPO — Key Differences

| Aspect | XPO | EF Core |
|---|---|---|
| PK default | `int` (XPObject) or `Guid` (BaseObject) | `Guid` (BaseObject) |
| Change tracking | `SetPropertyValue()` method | Virtual properties + `UseChangeTrackingProxies()` |
| Collections | `XPCollection<T>` via `GetCollection<T>()` | `IList<T>` with `new ObservableCollection<T>()` |
| Session/Context | `Session` constructor arg | `IObjectSpaceLink.ObjectSpace` |
| Lifecycle hooks | `AfterConstruction`, `OnSaving`, `OnLoaded` | Same via `IXafEntityObject` |
| Associations | `[Association("name")]` both ends | Navigation properties |
| Cascade delete | `[Aggregated]` on collection | `DeleteBehavior.Cascade` Fluent API |
| Migrations | Auto schema update (no migrations) | EF Core migrations required |
| Lazy loading | Automatic | Requires `UseLazyLoadingProxies()` + virtual |
| DevExpress rec. | Mature, stable, legacy | **Recommended for new projects (v21.2+)** |

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Non-virtual properties | All properties **must** be `virtual` for proxies |
| `AddDbContext` instead of `AddDbContextFactory` | XAF requires `IDbContextFactory<T>` |
| Missing `UseChangeTrackingProxies()` | Breaks UI, Conditional Appearance, validation |
| Redefining `ID` / `Oid` | `BaseObject` already has `Guid ID` |
| `AsNoTracking()` in queries | Bypasses XAF security filters — never use |
| `List<T>` instead of `ObservableCollection<T>` | List views won't update automatically |
| No `IDesignTimeDbContextFactory` | `dotnet ef migrations add` fails |
| Missing `DbSet<T>` for built-in XAF types | Add ModelDifference, ModelDifferenceAspect, etc. |
| Circular cascade delete paths | Use `DeleteBehavior.Restrict` and handle manually |
| `IObjectSpace` stored in static field or singleton | Memory leak — use `IObjectSpaceFactory` + `using var os = ...` |
| Unbounded `GetObjects<T>()` without criteria | Loads entire table into memory — add `CriteriaOperator` or `Take()` |

---

## Related Skills

- `xaf-memory-leaks` — ObjectSpace disposal patterns, batch processing, CollectionSource lifecycle

## Source Links

- Business Model Design with EF Core: https://docs.devexpress.com/eXpressAppFramework/401369/business-model-design-orm/business-model-design-with-entity-framework-core
- EF Core Reference for XAF Developers: https://docs.devexpress.com/eXpressAppFramework/401644/business-model-design-orm/business-model-design-with-entity-framework-core/ef-core-reference-for-xaf-developers
- BaseObject (EF Core): https://docs.devexpress.com/eXpressAppFramework/DevExpress.Persistent.BaseImpl.EF.BaseObject
- IXafEntityObject: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.IXafEntityObject
- IObjectSpaceLink: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp.IObjectSpaceLink
- Property Change Notifications: https://docs.devexpress.com/eXpressAppFramework/117395/business-model-design-orm/property-changed-event-in-business-classes
