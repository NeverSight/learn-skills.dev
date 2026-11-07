---
name: killerpdf-portable-editor
description: KillerPDF is a portable, single-EXE Windows PDF editor built with C#/WPF and PDFium — supports viewing, annotating, merging, splitting, signing, and printing PDFs with no installer, account, or telemetry.
triggers:
  - edit a PDF in C# WPF
  - portable PDF editor Windows no installer
  - merge split PDF dotnet wpf
  - annotate PDF without Adobe
  - KillerPDF setup and usage
  - add text boxes signatures to PDF C#
  - PDF freehand drawing highlight overlay dotnet
  - build KillerPDF from source
---

# KillerPDF Portable PDF Editor Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

KillerPDF is a single-EXE (~6 MB zipped), portable Windows PDF editor for .NET Framework 4.8. It renders PDFs via PDFium (Docnet.Core), supports inline text editing, annotations, freehand drawing, highlights, signatures, merge/split, full-text search, and printing — all without Adobe, accounts, or telemetry.

---

## What KillerPDF Does

| Capability | Details |
|---|---|
| Rendering | High-quality PDFium rendering via Docnet.Core |
| Annotation | Text boxes, freehand draw, highlight overlays |
| Editing | Inline text editing with font matching |
| Pages | Merge multiple PDFs, split selected pages, drag-and-drop reorder |
| Signatures | Draw/save reusable signatures, click to place |
| Search | Full-text search with highlighting, drag-select to copy |
| Print | Annotations flattened into output |
| Distribution | Single EXE, no runtime, no admin rights |

---

## Getting the Binary

```powershell
# Download latest prebuilt release
Invoke-WebRequest -Uri "https://github.com/SteveTheKiller/KillerPDF/releases/latest/download/KillerPDF.zip" -OutFile "KillerPDF.zip"
Expand-Archive -Path "KillerPDF.zip" -DestinationPath ".\KillerPDF"
.\KillerPDF\KillerPDF.exe
```

No installer, no admin rights required. Just unzip and run.

---

## Building from Source

### Requirements

- Windows 10/11 x64
- .NET 8 SDK or later (to build; output targets .NET Framework 4.8)
- Git

### Clone and Build

```powershell
git clone https://github.com/SteveTheKiller/KillerPDF.git
cd KillerPDF
dotnet publish -c Release
```

Output lands in `bin/Release/net48/publish/`. The publish step produces:
- `KillerPDF.exe` — single Costura-bundled executable
- `KillerPDF-<version>-src.zip` — GPL3 corresponding source archive

### Project Structure

```
KillerPDF/
├── App.xaml / App.xaml.cs          # Application entry, theming
├── MainWindow.xaml / .cs           # Primary WPF window, toolbar, page canvas
├── PdfDocument.cs                  # PDFium wrapper (Docnet.Core), load/save/render
├── PageViewModel.cs                # Page data binding, annotation layer
├── AnnotationCanvas.cs             # Custom Canvas for drawing/annotation
├── SignatureManager.cs             # Save/load/place signatures
├── MergeWindow.xaml / .cs          # Merge multiple PDFs UI
├── SplitWindow.xaml / .cs          # Page selection and split UI
├── SearchPanel.xaml / .cs          # Full-text search UI
├── PrintHelper.cs                  # Flatten annotations and print
├── Models/
│   ├── Annotation.cs               # Base annotation model
│   ├── TextBoxAnnotation.cs
│   ├── DrawingAnnotation.cs
│   └── HighlightAnnotation.cs
└── Resources/
    └── Icons/                      # SVG/PNG toolbar icons
```

---

## Key Dependencies

```xml
<!-- KillerPDF.csproj (simplified) -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net48</TargetFramework>
    <UseWPF>true</UseWPF>
    <AssemblyName>KillerPDF</AssemblyName>
  </PropertyGroup>

  <ItemGroup>
    <!-- PDFium rendering -->
    <PackageReference Include="Docnet.Core" Version="2.6.0" />
    <!-- Single-EXE bundling -->
    <PackageReference Include="Costura.Fody" Version="5.7.0" />
    <PackageReference Include="Fody" Version="6.8.0" />
  </ItemGroup>
</Project>
```

---

## Core Patterns and Code Examples

### Opening and Rendering a PDF Page

```csharp
using Docnet.Core;
using Docnet.Core.Models;
using System.Windows.Media.Imaging;
using System.Runtime.InteropServices;

public class PdfDocument : IDisposable
{
    private IDocLib _docLib;
    private IDocReader _docReader;
    private readonly string _filePath;

    public int PageCount { get; private set; }

    public void Open(string filePath, string password = "")
    {
        _filePath = filePath;
        _docLib = DocLib.Instance;
        _docReader = string.IsNullOrEmpty(password)
            ? _docLib.GetDocReader(filePath, new PageDimensions(1080, 1920))
            : _docLib.GetDocReader(filePath, password, new PageDimensions(1080, 1920));
        PageCount = _docReader.GetPageCount();
    }

    public BitmapSource RenderPage(int pageIndex, double dpi = 150)
    {
        using var pageReader = _docReader.GetPageReader(pageIndex);
        int width  = pageReader.GetPageWidth();
        int height = pageReader.GetPageHeight();
        var rawBytes = pageReader.GetImage(); // BGRA byte array

        var bitmap = new WriteableBitmap(width, height, dpi, dpi,
            System.Windows.Media.PixelFormats.Bgra32, null);
        bitmap.WritePixels(
            new System.Windows.Int32Rect(0, 0, width, height),
            rawBytes, width * 4, 0);
        bitmap.Freeze();
        return bitmap;
    }

    public string GetPageText(int pageIndex)
    {
        using var pageReader = _docReader.GetPageReader(pageIndex);
        return pageReader.GetText();
    }

    public void Dispose()
    {
        _docReader?.Dispose();
        _docLib?.Dispose();
    }
}
```

### Annotation Model Hierarchy

```csharp
// Models/Annotation.cs
public abstract class Annotation
{
    public Guid Id { get; } = Guid.NewGuid();
    public int PageIndex { get; set; }
    public System.Windows.Rect Bounds { get; set; }
    public double Opacity { get; set; } = 1.0;

    public abstract UIElement ToUIElement();
    public abstract void FlattenToPdfPage(PdfPage page);
}

// Models/TextBoxAnnotation.cs
public class TextBoxAnnotation : Annotation
{
    public string Text { get; set; } = "";
    public string FontFamily { get; set; } = "Arial";
    public double FontSize { get; set; } = 12;
    public System.Windows.Media.Color Color { get; set; }
        = System.Windows.Media.Colors.Black;

    public override UIElement ToUIElement()
    {
        var tb = new TextBox
        {
            Text = Text,
            FontFamily = new System.Windows.Media.FontFamily(FontFamily),
            FontSize = FontSize,
            Foreground = new System.Windows.Media.SolidColorBrush(Color),
            Background = System.Windows.Media.Brushes.Transparent,
            BorderThickness = new Thickness(0),
            AcceptsReturn = true,
            Width = Bounds.Width,
            Height = Bounds.Height,
            Opacity = Opacity,
        };
        Canvas.SetLeft(tb, Bounds.X);
        Canvas.SetTop(tb, Bounds.Y);
        return tb;
    }

    public override void FlattenToPdfPage(PdfPage page)
    {
        // Write text at PDF coordinates using PdfSharp or iTextSharp
        // KillerPDF uses PDFium for reading and a lightweight writer for output
    }
}

// Models/HighlightAnnotation.cs
public class HighlightAnnotation : Annotation
{
    public System.Windows.Media.Color HighlightColor { get; set; }
        = System.Windows.Media.Colors.Yellow;

    public override UIElement ToUIElement()
    {
        var rect = new System.Windows.Shapes.Rectangle
        {
            Fill = new System.Windows.Media.SolidColorBrush(
                System.Windows.Media.Color.FromArgb(
                    (byte)(Opacity * 128),
                    HighlightColor.R, HighlightColor.G, HighlightColor.B)),
            Width = Bounds.Width,
            Height = Bounds.Height,
        };
        Canvas.SetLeft(rect, Bounds.X);
        Canvas.SetTop(rect, Bounds.Y);
        return rect;
    }

    public override void FlattenToPdfPage(PdfPage page) { /* flatten */ }
}
```

### Freehand Drawing on the Annotation Canvas

```csharp
// AnnotationCanvas.cs — custom WPF Canvas
public class AnnotationCanvas : Canvas
{
    private Polyline _currentStroke;
    private List<Point> _points = new();
    public System.Windows.Media.Color PenColor { get; set; }
        = System.Windows.Media.Colors.Red;
    public double PenThickness { get; set; } = 2.0;
    public bool IsDrawingMode { get; set; }

    protected override void OnMouseLeftButtonDown(MouseButtonEventArgs e)
    {
        if (!IsDrawingMode) return;
        _points.Clear();
        _currentStroke = new Polyline
        {
            Stroke = new SolidColorBrush(PenColor),
            StrokeThickness = PenThickness,
            StrokeLineJoin = PenLineJoin.Round,
            StrokeStartLineCap = PenLineCap.Round,
            StrokeEndLineCap = PenLineCap.Round,
        };
        Children.Add(_currentStroke);
        CaptureMouse();
        AddPoint(e.GetPosition(this));
    }

    protected override void OnMouseMove(MouseEventArgs e)
    {
        if (!IsDrawingMode || _currentStroke == null
            || e.LeftButton != MouseButtonState.Pressed) return;
        AddPoint(e.GetPosition(this));
    }

    protected override void OnMouseLeftButtonUp(MouseButtonEventArgs e)
    {
        if (!IsDrawingMode || _currentStroke == null) return;
        ReleaseMouseCapture();
        // Commit stroke as DrawingAnnotation
        var ann = new DrawingAnnotation { Points = _points.ToList(),
            Color = PenColor, Thickness = PenThickness };
        AnnotationCommitted?.Invoke(this, ann);
        _currentStroke = null;
    }

    private void AddPoint(Point p)
    {
        _points.Add(p);
        _currentStroke.Points.Add(p);
    }

    public event EventHandler<DrawingAnnotation> AnnotationCommitted;
}
```

### Signature Manager

```csharp
// SignatureManager.cs
public class SignatureManager
{
    private readonly string _sigDir;

    public SignatureManager()
    {
        // Signatures stored next to EXE — portable, no AppData
        _sigDir = Path.Combine(
            Path.GetDirectoryName(
                System.Reflection.Assembly.GetExecutingAssembly().Location)!,
            "Signatures");
        Directory.CreateDirectory(_sigDir);
    }

    // Save ink strokes as PNG
    public void Save(string name, RenderTargetBitmap bitmap)
    {
        var encoder = new PngBitmapEncoder();
        encoder.Frames.Add(BitmapFrame.Create(bitmap));
        using var fs = File.OpenWrite(Path.Combine(_sigDir, name + ".png"));
        encoder.Save(fs);
    }

    // Load all saved signatures
    public IEnumerable<(string Name, BitmapImage Image)> LoadAll()
    {
        foreach (var file in Directory.EnumerateFiles(_sigDir, "*.png"))
        {
            var img = new BitmapImage(new Uri(file));
            img.Freeze();
            yield return (Path.GetFileNameWithoutExtension(file), img);
        }
    }

    // Place signature as Image UIElement on canvas
    public Image PlaceSignature(BitmapImage sigImage, Point position,
        double scale = 1.0)
    {
        var img = new Image
        {
            Source = sigImage,
            Width  = sigImage.PixelWidth  * scale,
            Height = sigImage.PixelHeight * scale,
            Opacity = 0.9,
        };
        Canvas.SetLeft(img, position.X);
        Canvas.SetTop(img, position.Y);
        return img;
    }
}
```

### Merging PDFs

```csharp
// MergeWindow.xaml.cs (core merge logic)
public static void MergePdfs(IEnumerable<string> inputPaths, string outputPath)
{
    // KillerPDF uses PDFium C++ API via P/Invoke or a lightweight wrapper
    // Conceptual pattern using PdfSharp (or equivalent internal helper):
    using var output = new PdfDocument(); // PdfSharp or internal writer
    foreach (var path in inputPaths)
    {
        using var input = PdfReader.Open(path, PdfDocumentOpenMode.Import);
        for (int i = 0; i < input.PageCount; i++)
            output.AddPage(input.Pages[i]);
    }
    output.Save(outputPath);
}
```

### Splitting Pages

```csharp
public static void SplitPages(string inputPath, IEnumerable<int> pageIndices,
    string outputPath)
{
    using var input = PdfReader.Open(inputPath, PdfDocumentOpenMode.Import);
    using var output = new PdfDocument();
    foreach (var idx in pageIndices)
        output.AddPage(input.Pages[idx]);
    output.Save(outputPath);
}
```

### Full-Text Search

```csharp
// SearchPanel.xaml.cs
public List<(int PageIndex, System.Windows.Rect Rect)> Search(
    string query, PdfDocument doc)
{
    var results = new List<(int, System.Windows.Rect)>();
    var docLib = DocLib.Instance;
    using var reader = docLib.GetDocReader(doc.FilePath,
        new PageDimensions(1080, 1920));

    for (int i = 0; i < reader.GetPageCount(); i++)
    {
        using var page = reader.GetPageReader(i);
        var text = page.GetText();
        if (!text.Contains(query, StringComparison.OrdinalIgnoreCase))
            continue;

        // Get character bounding boxes for highlighting
        var chars = page.GetCharacters();
        // Match positions and build highlight Rects
        // (KillerPDF uses character-level positions from PDFium)
        int idx = text.IndexOf(query, StringComparison.OrdinalIgnoreCase);
        while (idx >= 0 && idx + query.Length <= chars.Count)
        {
            var first = chars[idx];
            var last  = chars[idx + query.Length - 1];
            var rect = new System.Windows.Rect(
                first.Box.Left, first.Box.Top,
                last.Box.Right - first.Box.Left,
                last.Box.Bottom - first.Box.Top);
            results.Add((i, rect));
            idx = text.IndexOf(query, idx + 1,
                StringComparison.OrdinalIgnoreCase);
        }
    }
    return results;
}
```

### Printing with Flattened Annotations

```csharp
// PrintHelper.cs
public static void PrintDocument(BitmapSource[] renderedPages, string docTitle)
{
    var pd = new PrintDialog();
    if (pd.ShowDialog() != true) return;

    var doc = new FixedDocument();
    foreach (var page in renderedPages)
    {
        var pageContent = new PageContent();
        var fixedPage   = new FixedPage
        {
            Width  = pd.PrintableAreaWidth,
            Height = pd.PrintableAreaHeight,
        };
        var img = new Image
        {
            Source  = page,
            Width   = pd.PrintableAreaWidth,
            Height  = pd.PrintableAreaHeight,
            Stretch = System.Windows.Media.Stretch.Uniform,
        };
        fixedPage.Children.Add(img);
        ((IAddChild)pageContent).AddChild(fixedPage);
        doc.Pages.Add(pageContent);
    }

    var xpsWriter = PrintQueue.CreateXpsDocumentWriter(
        pd.PrintQueue);
    xpsWriter.Write(doc);
}

// Flatten annotations: render page + annotation canvas to BitmapSource
public static BitmapSource FlattenPage(BitmapSource pdfPageBitmap,
    AnnotationCanvas canvas, int width, int height)
{
    var visual = new DrawingVisual();
    using (var ctx = visual.RenderOpen())
    {
        ctx.DrawImage(pdfPageBitmap,
            new System.Windows.Rect(0, 0, width, height));
        // Render canvas children over PDF
        var canvasBrush = new VisualBrush(canvas);
        ctx.DrawRectangle(canvasBrush, null,
            new System.Windows.Rect(0, 0, width, height));
    }
    var rtb = new RenderTargetBitmap(width, height, 96, 96,
        System.Windows.Media.PixelFormats.Pbgra32);
    rtb.Render(visual);
    rtb.Freeze();
    return rtb;
}
```

---

## MainWindow Integration Pattern

```csharp
// MainWindow.xaml.cs — typical usage wiring
public partial class MainWindow : Window
{
    private PdfDocument _doc = new();
    private SignatureManager _sigManager = new();
    private int _currentPage = 0;

    private void OpenFile_Click(object sender, RoutedEventArgs e)
    {
        var dlg = new OpenFileDialog { Filter = "PDF files|*.pdf" };
        if (dlg.ShowDialog() != true) return;
        _doc.Open(dlg.FileName);
        _currentPage = 0;
        ShowPage(_currentPage);
    }

    private void ShowPage(int index)
    {
        PageImage.Source = _doc.RenderPage(index, dpi: 150);
        AnnotLayer.Children.Clear(); // AnnotationCanvas reset
    }

    private void DrawMode_Click(object sender, RoutedEventArgs e)
    {
        AnnotLayer.IsDrawingMode = !AnnotLayer.IsDrawingMode;
        AnnotLayer.PenColor = SelectedColor; // from color picker
        AnnotLayer.PenThickness = PenSizeSlider.Value;
    }

    private void AddTextBox_Click(object sender, RoutedEventArgs e)
    {
        var ann = new TextBoxAnnotation
        {
            PageIndex = _currentPage,
            Bounds = new Rect(50, 50, 200, 40),
            Text = "Double-click to edit",
        };
        AnnotLayer.Children.Add(ann.ToUIElement());
    }

    private void PlaceSignature_Click(object sender, RoutedEventArgs e)
    {
        if (SignatureList.SelectedItem is not (string _, BitmapImage sig)) return;
        var placed = _sigManager.PlaceSignature(sig,
            new Point(100, 100), scale: 0.5);
        AnnotLayer.Children.Add(placed);
    }

    private void Save_Click(object sender, RoutedEventArgs e)
    {
        // Flatten and save — render each page with its annotation canvas
        // then write combined output PDF
    }

    private void Print_Click(object sender, RoutedEventArgs e)
    {
        var pages = Enumerable.Range(0, _doc.PageCount)
            .Select(i => PrintHelper.FlattenPage(
                _doc.RenderPage(i, 150), AnnotLayer, 1080, 1920))
            .ToArray();
        PrintHelper.PrintDocument(pages, "KillerPDF Document");
    }
}
```

---

## XAML Layout Snippet

```xml
<!-- MainWindow.xaml (simplified) -->
<Window x:Class="KillerPDF.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="clr-namespace:KillerPDF"
        Title="KillerPDF" Width="1200" Height="800"
        Background="#1E1E1E">
  <DockPanel>
    <!-- Toolbar -->
    <ToolBar DockPanel.Dock="Top" Background="#2D2D2D">
      <Button Content="Open"   Click="OpenFile_Click"/>
      <Button Content="Save"   Click="Save_Click"/>
      <Button Content="Merge"  Click="Merge_Click"/>
      <Button Content="Split"  Click="Split_Click"/>
      <Separator/>
      <Button Content="Text"   Click="AddTextBox_Click"/>
      <Button Content="Draw"   Click="DrawMode_Click"/>
      <Button Content="Highlight" Click="AddHighlight_Click"/>
      <Button Content="Sign"   Click="PlaceSignature_Click"/>
      <Separator/>
      <Button Content="Search" Click="ToggleSearch_Click"/>
      <Button Content="Print"  Click="Print_Click"/>
    </ToolBar>

    <!-- Page display + annotation overlay -->
    <ScrollViewer VerticalScrollBarVisibility="Auto">
      <Grid>
        <Image x:Name="PageImage" Stretch="Uniform"/>
        <!-- Custom canvas sits on top of PDF page image -->
        <local:AnnotationCanvas x:Name="AnnotLayer"
            Background="Transparent"
            AnnotationCommitted="AnnotLayer_AnnotationCommitted"/>
      </Grid>
    </ScrollViewer>
  </DockPanel>
</Window>
```

---

## Configuration

KillerPDF is intentionally config-free for end users. For contributors:

| Setting | Where |
|---|---|
| Default DPI for rendering | `PdfDocument.RenderPage(dpi:)` parameter |
| Pen defaults | `AnnotationCanvas.PenColor`, `.PenThickness` |
| Signature storage path | `SignatureManager._sigDir` (next to EXE) |
| Single-EXE bundling | `FodyWeavers.xml` (Costura config) |
| Build target framework | `KillerPDF.csproj` `<TargetFramework>net48</TargetFramework>` |

No registry writes, no `%APPDATA%` usage — everything lives alongside the EXE.

---

## Common Patterns

### Drag-and-Drop Page Reordering

```csharp
// Bind a ListBox of page thumbnails; handle drag events
private void PageList_PreviewMouseMove(object sender, MouseEventArgs e)
{
    if (e.LeftButton == MouseButtonState.Pressed && _dragItem != null)
        DragDrop.DoDragDrop(PageList, _dragItem, DragDropEffects.Move);
}

private void PageList_Drop(object sender, DragEventArgs e)
{
    if (e.Data.GetData(typeof(PageViewModel)) is not PageViewModel src) return;
    var target = (PageViewModel)((ListBoxItem)e.OriginalSource
        .FindAncestor<ListBoxItem>()).DataContext;
    int from = Pages.IndexOf(src);
    int to   = Pages.IndexOf(target);
    Pages.Move(from, to);
}
```

### Color Picker for Annotations

```csharp
// Simple popup color picker; or use a third-party WPF color picker NuGet
private void ColorButton_Click(object sender, RoutedEventArgs e)
{
    var picker = new ColorPickerDialog { SelectedColor = AnnotLayer.PenColor };
    if (picker.ShowDialog() == true)
        AnnotLayer.PenColor = picker.SelectedColor;
}
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `DllNotFoundException: pdfium.dll` | PDFium native missing from bundle | Run `dotnet publish` (not just `build`); Costura bundles natives on publish |
| Blank page rendered | Wrong `PageDimensions` or index out of range | Verify `pageIndex < PageCount`; use reasonable dimensions like `(1080, 1920)` |
| High memory on large PDFs | Holding all pages rendered simultaneously | Render on demand; dispose `IPageReader` after each render |
| Annotations lost on save | Flattening step skipped | Call `FlattenPage` for every page before writing output PDF |
| Build error `net48` SDK missing | Building with old SDK | Install .NET 8 SDK; it can cross-target to net48 |
| Signatures not found | EXE moved without `Signatures/` folder | `Signatures/` folder must stay next to EXE; it's created automatically on first run |
| WPF designer crash | Costura not compatible with design-time | Ignore design-time errors; run normally to test |

---

## License Note

KillerPDF is **GPLv3**. Any fork, modification, or redistribution — including commercial rebrands — must be released under GPLv3 with source available. The build pipeline automatically produces a `KillerPDF-<version>-src.zip` for GPL compliance.

```
GPLv3 — https://github.com/SteveTheKiller/KillerPDF/blob/main/LICENSE
```
