---
name: xaf-office
description: XAF Office/Document Management Modules - FileAttachmentsModule with IFileData/FileAttachment patterns (XPO and EF Core), SpreadsheetModule for Excel editing with ISpreadsheetValueStorage, RichTextModule for Word-like editing with IRichTextDocumentProvider and mail merge, PdfViewerModule for PDF display, platform differences (Blazor vs WinForms), programmatic document manipulation. Use when adding file attachments, spreadsheet editing, rich text editing, or PDF viewing to DevExpress XAF applications.
---

# XAF: Office / Document Management Modules

## Available Modules

| Module | Class | File Type | Platforms |
|---|---|---|---|
| File Attachments | `FileAttachmentsModule` | any file | Blazor, WinForms |
| Spreadsheet | `SpreadsheetModule` | .xlsx | Blazor, WinForms |
| Rich Text | `RichTextModule` | .docx, .rtf | Blazor, WinForms |
| PDF Viewer | `PdfViewerModule` | .pdf | Blazor, WinForms |

---

## File Attachments Module

### NuGet Packages

```xml
<PackageReference Include="DevExpress.ExpressApp.FileAttachments" Version="25.1.*" />
<PackageReference Include="DevExpress.ExpressApp.FileAttachments.Blazor" Version="25.1.*" />
<!-- or for WinForms: -->
<PackageReference Include="DevExpress.ExpressApp.FileAttachments.Win" Version="25.1.*" />
```

### Setup

```csharp
// Module:
RequiredModuleTypes.Add(typeof(FileAttachmentsModule));

// Blazor Program.cs:
b.AddModule<FileAttachmentsModule>();
b.AddModule<FileAttachmentsBlazorModule>();
```

### IFileData Interface

```csharp
public interface IFileData {
    string FileName { get; set; }
    int Size { get; }
    void LoadFromStream(string fileName, Stream stream);
    void SaveToStream(Stream stream);
}
```

### XPO Pattern — Single File Attachment

```csharp
// Option 1: Built-in FileData (recommended)
using DevExpress.Persistent.BaseImpl;

public class Document : BaseObject {
    public Document(Session session) : base(session) { }

    private FileData attachment;
    [Aggregated]
    public FileData Attachment {
        get => attachment;
        set => SetPropertyValue(nameof(Attachment), ref attachment, value);
    }

    // EditorAlias auto-detected from IFileData
}
```

### EF Core Pattern — Single File Attachment

```csharp
using DevExpress.Persistent.BaseImpl.EF;

public class Document : BaseObject {
    // FileAttachment is the EF Core equivalent of FileData
    public virtual FileAttachment Attachment { get; set; }
}

// DbContext:
public DbSet<FileAttachment> FileAttachments { get; set; }
```

### XPO Pattern — Multiple File Attachments (Collection)

```csharp
public class Employee : BaseObject {
    public Employee(Session session) : base(session) { }

    [Aggregated]
    [Association("Employee-Documents")]
    public XPCollection<FileData> Documents => GetCollection<FileData>(nameof(Documents));
}
```

### EF Core Pattern — Multiple Files

```csharp
public class Employee : BaseObject {
    public virtual IList<FileAttachment> Documents { get; set; }
        = new ObservableCollection<FileAttachment>();
}
```

### Programmatic File Access

```csharp
// Load from stream
var attachment = objectSpace.CreateObject<FileData>();
using (var stream = File.OpenRead("report.pdf")) {
    attachment.LoadFromStream("report.pdf", stream);
}
employee.Attachment = attachment;
objectSpace.CommitChanges();

// Save to stream
using (var stream = new MemoryStream()) {
    employee.Attachment.SaveToStream(stream);
    File.WriteAllBytes("output.pdf", stream.ToArray());
}
```

---

## Spreadsheet Module

### Setup

```xml
<PackageReference Include="DevExpress.ExpressApp.Spreadsheet" Version="25.1.*" />
<PackageReference Include="DevExpress.ExpressApp.Spreadsheet.Blazor" Version="25.1.*" />
```

```csharp
b.AddModule<SpreadsheetModule>();
b.AddModule<SpreadsheetBlazorModule>();
```

### Business Object with Embedded Spreadsheet

```csharp
// XPO
public class Budget : BaseObject {
    public Budget(Session session) : base(session) { }

    // Store spreadsheet as byte array
    private byte[] spreadsheetData;
    [EditorAlias("SpreadsheetPropertyEditor")]
    [Size(SizeAttribute.Unlimited)]
    public byte[] SpreadsheetData {
        get => spreadsheetData;
        set => SetPropertyValue(nameof(SpreadsheetData), ref spreadsheetData, value);
    }
}

// EF Core
public class Budget : BaseObject {
    [EditorAlias("SpreadsheetPropertyEditor")]
    public virtual byte[] SpreadsheetData { get; set; }
}
```

### Programmatic Spreadsheet Manipulation

```csharp
using DevExpress.Spreadsheet;

// Read spreadsheet data from XAF object
byte[] data = budget.SpreadsheetData;
using var workbook = new Workbook();
using var stream = new MemoryStream(data);
workbook.LoadDocument(stream, DocumentFormat.Xlsx);

var sheet = workbook.Worksheets[0];
sheet.Cells["B2"].Value = 1234.56;
sheet.Cells["B3"].Formula = "=B2*1.23";

// Save back
using var outputStream = new MemoryStream();
workbook.SaveDocument(outputStream, DocumentFormat.Xlsx);
budget.SpreadsheetData = outputStream.ToArray();
objectSpace.CommitChanges();
```

---

## Rich Text Module

### Setup

```xml
<PackageReference Include="DevExpress.ExpressApp.RichTextEdit" Version="25.1.*" />
<PackageReference Include="DevExpress.ExpressApp.RichTextEdit.Blazor" Version="25.1.*" />
```

```csharp
b.AddModule<RichTextEditModule>();
b.AddModule<RichTextEditBlazorModule>();
```

### Business Object with Rich Text

```csharp
// XPO
public class Article : BaseObject {
    public Article(Session session) : base(session) { }

    private byte[] content;
    [EditorAlias("RichTextPropertyEditor")]
    [Size(SizeAttribute.Unlimited)]
    public byte[] Content {
        get => content;
        set => SetPropertyValue(nameof(Content), ref content, value);
    }
}

// EF Core
public class Article : BaseObject {
    [EditorAlias("RichTextPropertyEditor")]
    public virtual byte[] Content { get; set; }
}
```

### Mail Merge

```csharp
using DevExpress.XtraRichEdit;
using DevExpress.XtraRichEdit.API.Native;

// Load template from byte[] stored in XAF object
using var server = new RichEditDocumentServer();
using var templateStream = new MemoryStream(article.Content);
server.LoadDocument(templateStream, DocumentFormat.OpenXml);

// Execute mail merge
server.Document.MailMerge.DataSource = contacts; // your data list
server.Document.MailMerge.Execute();

// Export result
using var outputStream = new MemoryStream();
server.SaveDocument(outputStream, DocumentFormat.OpenXml);
var mergedBytes = outputStream.ToArray();
```

---

## PDF Viewer Module

### Setup

```xml
<PackageReference Include="DevExpress.ExpressApp.PdfViewer" Version="25.1.*" />
<PackageReference Include="DevExpress.ExpressApp.PdfViewer.Blazor" Version="25.1.*" />
```

```csharp
b.AddModule<PdfViewerModule>();
b.AddModule<PdfViewerBlazorModule>();
```

### Business Object with PDF

```csharp
// XPO
public class Contract : BaseObject {
    public Contract(Session session) : base(session) { }

    private byte[] pdfContent;
    [EditorAlias("PdfViewerPropertyEditor")]
    [Size(SizeAttribute.Unlimited)]
    public byte[] PdfContent {
        get => pdfContent;
        set => SetPropertyValue(nameof(PdfContent), ref pdfContent, value);
    }
}
```

---

## Blazor vs WinForms Differences

| Feature | Blazor | WinForms |
|---|---|---|
| File upload | DxUpload component | OpenFileDialog |
| Spreadsheet editor | Browser-based DevExpress Spreadsheet | XtraSpreadsheet (Win control) |
| Rich text editor | Browser-based Rich Text editor | XtraRichEdit (Win control) |
| PDF viewer | Browser-based PDF viewer | XtraPdfViewer (Win control) |
| Module class | `*BlazorModule` | `*WindowsFormsModule` |

---

## Auto-Added Document Actions

When an Office module property is present in Detail View, XAF automatically adds:
- **Save** (document) action
- **Export** / **Print** action (module-dependent)
- **Load** (from file) action

No extra controller code needed for basic file operations.

---

## Source Links

- Document Management: https://docs.devexpress.com/eXpressAppFramework/113986/document-management
- File Attachments: https://docs.devexpress.com/eXpressAppFramework/113549/document-management/file-attachments-module
- Spreadsheet: https://docs.devexpress.com/eXpressAppFramework/400552/document-management/spreadsheet-document
- Rich Text: https://docs.devexpress.com/eXpressAppFramework/400315/document-management/rich-text-document
- FileData (XPO): https://docs.devexpress.com/eXpressAppFramework/DevExpress.Persistent.BaseImpl.FileData
- FileAttachment (EF Core): https://docs.devexpress.com/eXpressAppFramework/DevExpress.Persistent.BaseImpl.EF.FileAttachment
- IFileData API: https://docs.devexpress.com/eXpressAppFramework/DevExpress.Persistent.Base.IFileData
