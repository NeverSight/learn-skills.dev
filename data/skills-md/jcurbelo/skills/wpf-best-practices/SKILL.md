---
name: wpf-best-practices
description: Best practices for building WPF desktop applications with C# and .NET. Use when working on WPF projects, .NET desktop apps, XAML UI, MVVM architecture, system tray apps, or any C# project using Windows Presentation Foundation.
---

# WPF Best Practices

You are an expert in C#, .NET, and WPF desktop application development with deep
knowledge of MVVM architecture, dependency injection, async/await patterns, and
Windows desktop integration.

## C# Code Style

### Basic Principles

- Use English for all code and documentation
- Always declare types for variables and functions (parameters and return values)
- Enable nullable reference types project-wide
- Use file-scoped namespaces — no braces, no nesting
- Write concise, maintainable code — avoid over-engineering

### File-Scoped Namespaces

Always use file-scoped namespaces:

```csharp
namespace MyApp.Services;

public class SettingsService
{
    // No extra indentation level
}
```

### Nullable Reference Types

Always enabled in csproj (`<Nullable>enable</Nullable>`):

```csharp
public class AppNotification
{
    public string Title { get; set; } = "";       // Non-nullable with default
    public string Message { get; set; } = "";
    public string? Channel { get; set; }           // Explicitly nullable
    public string[]? Tags { get; set; }
}
```

### Naming Conventions

- **PascalCase** for types, interfaces, properties, methods, events, constants
- **camelCase** for local variables and parameters
- **_camelCase** for private fields
- **IPascalCase** for interfaces (prefix with `I`)
- **UPPERCASE** for environment variables only
- Prefix boolean properties/fields with `Is`, `Has`, `Can`, `Should`

```csharp
public class ConnectionService
{
    private readonly ILogger _logger;
    private readonly string _serverUrl;
    private bool _isConnected;

    public bool IsConnected => _isConnected;
    public bool CanReconnect { get; private set; }
}
```

### Modern C# Features

Use switch expressions:

```csharp
public string StatusIcon => Status switch
{
    ConnectionStatus.Connected    => "🟢",
    ConnectionStatus.Connecting   => "🟡",
    ConnectionStatus.Disconnected => "🔴",
    _                             => "⚪"
};
```

Use range/slice operators:

```csharp
private static string Capitalize(string s) =>
    string.IsNullOrEmpty(s) ? s : char.ToUpper(s[0]) + s[1..];
```

Avoid redundant default initializers:

```csharp
// Good
private bool _disposed;
private int _retryCount;

// Bad — redundant
private bool _disposed = false;
private int _retryCount = 0;
```

---

## Project Structure

```
MyApp/
├── MyApp.sln                    # Solution file
├── src/
│   ├── MyApp/                   # Main WPF application
│   │   ├── App.xaml             # Application entry, resource dictionaries
│   │   ├── App.xaml.cs          # DI setup, app lifecycle, crash handlers
│   │   ├── Views/               # XAML windows and user controls
│   │   ├── ViewModels/          # MVVM presentation logic
│   │   ├── Models/              # Data classes and enums
│   │   ├── Services/            # Business logic (DI singletons)
│   │   │   └── Interfaces/      # Service contracts
│   │   ├── Utilities/           # Helpers (encryption, screen, JSON)
│   │   └── Constants/           # App-wide constants
│   └── MyApp.Shared/            # Cross-platform shared library
│       └── MyApp.Shared.csproj
├── tests/
│   └── MyApp.Tests/             # xUnit test project
│       └── MyApp.Tests.csproj
└── .github/
    └── workflows/               # CI/CD
```

### Project File Configuration

WPF app csproj:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net10.0-windows</TargetFramework>
    <UseWPF>true</UseWPF>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
```

Shared library csproj (cross-platform):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <InternalsVisibleTo Include="MyApp.Tests" />
  </ItemGroup>
</Project>
```

---

## MVVM Pattern

### ViewModelBase

Every ViewModel should inherit from a shared base:

```csharp
namespace MyApp.ViewModels;

public abstract class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    protected bool SetProperty<T>(ref T field, T value,
        [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        OnPropertyChanged(name);
        return true;
    }
}
```

Usage:

```csharp
public class MainViewModel : ViewModelBase
{
    private string _title = "";
    public string Title
    {
        get => _title;
        set => SetProperty(ref _title, value);
    }

    private bool _isLoading;
    public bool IsLoading
    {
        get => _isLoading;
        set => SetProperty(ref _isLoading, value);
    }
}
```

### RelayCommand

Use a simple `RelayCommand` for XAML command bindings:

```csharp
namespace MyApp.ViewModels;

public class RelayCommand : ICommand
{
    private readonly Action<object?> _execute;
    private readonly Func<object?, bool>? _canExecute;

    public RelayCommand(Action<object?> execute, Func<object?, bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged
    {
        add => CommandManager.RequerySuggested += value;
        remove => CommandManager.RequerySuggested -= value;
    }

    public bool CanExecute(object? parameter) => _canExecute?.Invoke(parameter) ?? true;
    public void Execute(object? parameter) => _execute(parameter);
}

public class RelayCommand<T> : ICommand
{
    private readonly Action<T?> _execute;
    private readonly Func<T?, bool>? _canExecute;

    public RelayCommand(Action<T?> execute, Func<T?, bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged
    {
        add => CommandManager.RequerySuggested += value;
        remove => CommandManager.RequerySuggested -= value;
    }

    public bool CanExecute(object? parameter) =>
        _canExecute?.Invoke(parameter is T t ? t : default) ?? true;
    public void Execute(object? parameter) =>
        _execute(parameter is T t ? t : default);
}
```

### AsyncRelayCommand

For async operations bound to UI:

```csharp
namespace MyApp.ViewModels;

public class AsyncRelayCommand : ICommand
{
    private readonly Func<object?, Task> _execute;
    private readonly Func<object?, bool>? _canExecute;
    private bool _isExecuting;

    public AsyncRelayCommand(Func<object?, Task> execute,
        Func<object?, bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged
    {
        add => CommandManager.RequerySuggested += value;
        remove => CommandManager.RequerySuggested -= value;
    }

    public bool CanExecute(object? parameter) =>
        !_isExecuting && (_canExecute?.Invoke(parameter) ?? true);

    public async void Execute(object? parameter)
    {
        if (_isExecuting) return;
        _isExecuting = true;
        CommandManager.InvalidateRequerySuggested();

        try
        {
            await _execute(parameter);
        }
        finally
        {
            _isExecuting = false;
            CommandManager.InvalidateRequerySuggested();
        }
    }
}
```

### Data Binding in XAML

```xml
<Window x:Class="MyApp.Views.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="{Binding Title}">
    <Grid>
        <TextBlock Text="{Binding StatusText}"
                   Visibility="{Binding IsLoading,
                     Converter={StaticResource BoolToVisibilityConverter}}" />
        <Button Content="Save"
                Command="{Binding SaveCommand}"
                IsEnabled="{Binding CanSave}" />
    </Grid>
</Window>
```

Code-behind should only set the DataContext:

```csharp
public partial class MainWindow : Window
{
    public MainWindow(MainViewModel viewModel)
    {
        InitializeComponent();
        DataContext = viewModel;
    }
}
```

---

## Dependency Injection

Use `Microsoft.Extensions.DependencyInjection` for all service wiring.

### Setup in App.xaml.cs

```csharp
namespace MyApp;

public partial class App : Application
{
    private ServiceProvider? _serviceProvider;

    protected override void OnStartup(StartupEventArgs e)
    {
        var services = new ServiceCollection();
        ConfigureServices(services);
        _serviceProvider = services.BuildServiceProvider();

        var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();

        base.OnStartup(e);
    }

    private static void ConfigureServices(IServiceCollection services)
    {
        // Services — singletons for app-wide state
        services.AddSingleton<ISettingsService, SettingsService>();
        services.AddSingleton<IConnectionService, ConnectionService>();

        // HTTP clients
        services.AddHttpClient("AppClient", client =>
        {
            client.DefaultRequestHeaders.Add("User-Agent", "MyApp/1.0");
            client.Timeout = TimeSpan.FromSeconds(10);
        });

        // ViewModels — transient, created per window
        services.AddTransient<MainViewModel>();

        // Windows
        services.AddTransient<MainWindow>();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        (_serviceProvider as IDisposable)?.Dispose();
        base.OnExit(e);
    }
}
```

### Service Pattern

Always define an interface. Inject via constructor. Never use a service locator.

```csharp
// Interface
namespace MyApp.Services.Interfaces;

public interface ISettingsService
{
    string GetValue(string key, string defaultValue = "");
    void SetValue(string key, string value);
    void Save();
}

// Implementation
namespace MyApp.Services;

public class SettingsService : ISettingsService
{
    private readonly string _settingsPath;
    private Dictionary<string, string> _settings = new();

    public SettingsService()
    {
        _settingsPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "MyApp", "settings.json");
        Load();
    }

    public string GetValue(string key, string defaultValue = "") =>
        _settings.TryGetValue(key, out var value) ? value : defaultValue;

    public void SetValue(string key, string value) =>
        _settings[key] = value;

    public void Save()
    {
        var dir = Path.GetDirectoryName(_settingsPath)!;
        Directory.CreateDirectory(dir);
        var json = JsonSerializer.Serialize(_settings,
            new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(_settingsPath, json);
    }

    private void Load()
    {
        try
        {
            if (!File.Exists(_settingsPath)) return;
            var json = File.ReadAllText(_settingsPath);
            _settings = JsonSerializer.Deserialize<Dictionary<string, string>>(json) ?? new();
        }
        catch { _settings = new(); }
    }
}
```

### Anti-Pattern: Service Locator

Never resolve services from a static provider. Always inject through the constructor:

```csharp
// BAD — service locator
public class MyViewModel
{
    public void DoSomething()
    {
        var service = App.ServiceProvider.GetService<IMyService>();
        service?.Execute();
    }
}

// GOOD — constructor injection
public class MyViewModel
{
    private readonly IMyService _myService;

    public MyViewModel(IMyService myService)
    {
        _myService = myService;
    }

    public void DoSomething() => _myService.Execute();
}
```

If circular dependencies arise, use `Lazy<T>`:

```csharp
private readonly Lazy<IMyService> _myService;

public MyViewModel(Lazy<IMyService> myService)
{
    _myService = myService;
}
```

---

## Async/Await Patterns

### Rules

- Never use `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` — they deadlock
  WPF's single-threaded STA dispatcher
- Always propagate `CancellationToken` through async methods
- Use `ConfigureAwait(false)` in library/service code (not in ViewModels or
  code-behind where you need the UI context)
- Never fire-and-forget without error handling

### UI Thread Marshaling

Use `Dispatcher` to update UI from background threads:

```csharp
// From any thread — safe UI update
private void OnDataReceived(object? sender, DataEventArgs e)
{
    Application.Current.Dispatcher.InvokeAsync(() =>
    {
        StatusText = e.Message;
        Items.Add(e.Item);
    });
}
```

For ViewModels that update from background threads:

```csharp
public class DashboardViewModel : ViewModelBase
{
    private readonly Dispatcher _dispatcher;

    public DashboardViewModel()
    {
        _dispatcher = Application.Current.Dispatcher;
    }

    public async Task RefreshAsync(CancellationToken ct = default)
    {
        var data = await _dataService.FetchAsync(ct).ConfigureAwait(false);

        _dispatcher.InvokeAsync(() =>
        {
            Items.Clear();
            foreach (var item in data)
                Items.Add(item);
        });
    }
}
```

### DispatcherTimer for Periodic Work

```csharp
private DispatcherTimer? _statusTimer;

private void StartStatusPolling()
{
    _statusTimer = new DispatcherTimer
    {
        Interval = TimeSpan.FromSeconds(5)
    };
    _statusTimer.Tick += async (s, e) =>
    {
        try
        {
            await RefreshStatusAsync();
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Status poll failed: {ex.Message}");
        }
    };
    _statusTimer.Start();
}
```

### Safe Fire-and-Forget

Never use bare `_ = Task.Run(...)`. Always wrap with error handling:

```csharp
namespace MyApp.Utilities;

internal static class AsyncHelper
{
    public static async void FireAndForget(Func<Task> operation, string context)
    {
        try
        {
            await operation();
        }
        catch (OperationCanceledException) { }
        catch (Exception ex)
        {
            Debug.WriteLine($"[{context}] Background task failed: {ex.Message}");
        }
    }
}

// Usage
AsyncHelper.FireAndForget(
    () => LoadDataAsync(),
    "MainViewModel.LoadData");
```

---

## System Tray Integration

WPF does not have built-in system tray support. Use `System.Windows.Forms.NotifyIcon`:

```csharp
namespace MyApp.Services;

public class SystemTrayService : IDisposable
{
    private readonly System.Windows.Forms.NotifyIcon _notifyIcon;

    public SystemTrayService()
    {
        _notifyIcon = new System.Windows.Forms.NotifyIcon
        {
            Text = "My App",
            Visible = true
        };

        // Load icon from resources
        var iconStream = Application.GetResourceStream(
            new Uri("pack://application:,,,/Resources/app.ico"))?.Stream;
        if (iconStream != null)
            _notifyIcon.Icon = new System.Drawing.Icon(iconStream);

        _notifyIcon.DoubleClick += (s, e) => ShowMainWindow();
        BuildContextMenu();
    }

    private void BuildContextMenu()
    {
        var menu = new System.Windows.Forms.ContextMenuStrip();
        menu.Items.Add("Show", null, (s, e) => ShowMainWindow());
        menu.Items.Add(new System.Windows.Forms.ToolStripSeparator());
        menu.Items.Add("Exit", null, (s, e) => Application.Current.Shutdown());
        _notifyIcon.ContextMenuStrip = menu;
    }

    private static void ShowMainWindow()
    {
        var window = Application.Current.MainWindow;
        if (window == null) return;

        window.Show();
        window.WindowState = WindowState.Normal;
        window.Activate();
    }

    public void Dispose()
    {
        _notifyIcon.Visible = false;
        _notifyIcon.Dispose();
    }
}
```

### GDI Handle Management

Always destroy GDI icon handles to prevent leaks:

```csharp
[DllImport("user32.dll", CharSet = CharSet.Auto)]
private static extern bool DestroyIcon(IntPtr handle);

public static System.Drawing.Icon CreateStatusIcon(System.Drawing.Color color)
{
    using var bitmap = new System.Drawing.Bitmap(16, 16);
    using var g = System.Drawing.Graphics.FromImage(bitmap);
    using var brush = new System.Drawing.SolidBrush(color);

    g.Clear(System.Drawing.Color.Transparent);
    g.FillEllipse(brush, 2, 2, 12, 12);

    var hIcon = bitmap.GetHicon();
    var icon = System.Drawing.Icon.FromHandle(hIcon);
    var result = (System.Drawing.Icon)icon.Clone();  // Clone to own the data

    DestroyIcon(hIcon);  // CRITICAL: release GDI handle
    return result;
}
```

Cache icons — don't recreate them on every state change:

```csharp
private static System.Drawing.Icon? _connectedIcon;
private static System.Drawing.Icon? _disconnectedIcon;

public void UpdateStatus(bool connected)
{
    _connectedIcon ??= CreateStatusIcon(System.Drawing.Color.Green);
    _disconnectedIcon ??= CreateStatusIcon(System.Drawing.Color.Red);
    _notifyIcon.Icon = connected ? _connectedIcon : _disconnectedIcon;
}
```

---

## Window Management

### Minimize to Tray

```csharp
public partial class MainWindow : Window
{
    protected override void OnStateChanged(EventArgs e)
    {
        if (WindowState == WindowState.Minimized)
            Hide();
        base.OnStateChanged(e);
    }

    protected override void OnClosing(CancelEventArgs e)
    {
        e.Cancel = true;  // Don't close, minimize to tray
        Hide();
    }
}
```

### Transparent Overlay Windows

For transparent floating windows (widgets, overlays):

```csharp
<Window AllowsTransparency="True"
        WindowStyle="None"
        Background="Transparent"
        Topmost="True"
        ShowInTaskbar="False">
    <!-- Content renders over desktop -->
</Window>
```

### Single Instance with Mutex

```csharp
private static Mutex? _mutex;

protected override void OnStartup(StartupEventArgs e)
{
    const string mutexName = "Global\\MyAppSingleInstance";
    _mutex = new Mutex(true, mutexName, out bool isNewInstance);

    if (!isNewInstance)
    {
        MessageBox.Show("Application is already running.");
        Shutdown();
        return;
    }

    // Continue startup...
}
```

### Global Hotkey Registration

```csharp
namespace MyApp.Services;

public class GlobalHotkeyService : IDisposable
{
    private const int HOTKEY_ID = 9001;

    [DllImport("user32.dll")]
    private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint mods, uint vk);

    [DllImport("user32.dll")]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    private readonly IntPtr _hwnd;

    public void Register(IntPtr windowHandle, uint modifiers, uint key)
    {
        RegisterHotKey(windowHandle, HOTKEY_ID, modifiers, key);
    }

    public void Dispose()
    {
        UnregisterHotKey(_hwnd, HOTKEY_ID);
    }
}
```

---

## Settings Patterns

### JSON Settings with Safe Load/Save

```csharp
namespace MyApp.Services;

public class SettingsManager
{
    private static readonly string SettingsDir = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
        "MyApp");
    private static readonly string SettingsFile =
        Path.Combine(SettingsDir, "settings.json");

    // Properties with defaults
    public string ServerUrl { get; set; } = "http://localhost:8080";
    public bool AutoStart { get; set; }
    public bool ShowNotifications { get; set; } = true;

    public SettingsManager() => Load();

    public void Load()
    {
        try
        {
            if (!File.Exists(SettingsFile)) return;
            var json = File.ReadAllText(SettingsFile);
            var loaded = JsonSerializer.Deserialize<SettingsData>(json);
            if (loaded != null)
            {
                ServerUrl = loaded.ServerUrl ?? ServerUrl;
                AutoStart = loaded.AutoStart;
                ShowNotifications = loaded.ShowNotifications;
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Failed to load settings: {ex.Message}");
        }
    }

    public void Save()
    {
        try
        {
            Directory.CreateDirectory(SettingsDir);
            var data = new SettingsData
            {
                ServerUrl = ServerUrl,
                AutoStart = AutoStart,
                ShowNotifications = ShowNotifications
            };
            var json = JsonSerializer.Serialize(data,
                new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText(SettingsFile, json);
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Failed to save settings: {ex.Message}");
        }
    }

    // Keep serialization shape separate from public API
    private class SettingsData
    {
        public string? ServerUrl { get; set; }
        public bool AutoStart { get; set; }
        public bool ShowNotifications { get; set; } = true;
    }
}
```

### Registry for Auto-Start

```csharp
public static void SetAutoStart(bool enable, string appName)
{
    using var key = Registry.CurrentUser.OpenSubKey(
        @"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", true);
    if (key == null) return;

    if (enable)
    {
        var exe = Environment.ProcessPath;
        key.SetValue(appName, $"\"{exe}\"");
    }
    else
    {
        key.DeleteValue(appName, throwOnMissingValue: false);
    }
}
```

### DPAPI Encryption for Sensitive Settings

```csharp
using System.Security.Cryptography;

public static string EncryptForCurrentUser(string plainText)
{
    var data = Encoding.UTF8.GetBytes(plainText);
    var encrypted = ProtectedData.Protect(data, null,
        DataProtectionScope.CurrentUser);
    return Convert.ToBase64String(encrypted);
}

public static string DecryptForCurrentUser(string encrypted)
{
    var data = Convert.FromBase64String(encrypted);
    var decrypted = ProtectedData.Unprotect(data, null,
        DataProtectionScope.CurrentUser);
    return Encoding.UTF8.GetString(decrypted);
}
```

---

## Error Handling

### Crash Handlers

Register all three crash handler layers in `App.xaml.cs`:

```csharp
public App()
{
    InitializeComponent();

    // WPF UI thread exceptions
    DispatcherUnhandledException += (s, e) =>
    {
        LogCrash("DispatcherUnhandled", e.Exception);
        e.Handled = true;
    };

    // CLR unhandled exceptions (all threads)
    AppDomain.CurrentDomain.UnhandledException += (s, e) =>
        LogCrash("DomainUnhandled", e.ExceptionObject as Exception);

    // Unobserved async Task exceptions
    TaskScheduler.UnobservedTaskException += (s, e) =>
    {
        LogCrash("UnobservedTask", e.Exception);
        e.SetObserved();
    };
}

private static readonly string CrashLogPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "MyApp", "crash.log");

private static void LogCrash(string source, Exception? ex)
{
    try
    {
        Directory.CreateDirectory(Path.GetDirectoryName(CrashLogPath)!);
        var msg = $"\n[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] {source}\n{ex}\n";
        File.AppendAllText(CrashLogPath, msg);
    }
    catch { }
}
```

### Run Marker for Unclean Exit Detection

```csharp
private static readonly string RunMarkerPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "MyApp", "running.marker");

protected override void OnStartup(StartupEventArgs e)
{
    if (File.Exists(RunMarkerPath))
    {
        Debug.WriteLine("Previous session did not exit cleanly");
        File.Delete(RunMarkerPath);
    }
    File.WriteAllText(RunMarkerPath, DateTime.Now.ToString("O"));

    // ... rest of startup

    base.OnStartup(e);
}

protected override void OnExit(ExitEventArgs e)
{
    try { File.Delete(RunMarkerPath); } catch { }
    base.OnExit(e);
}
```

### Empty Catch Blocks

Never use empty catch blocks. At minimum, log in DEBUG:

```csharp
// BAD
catch { }

// GOOD — use a safe execution wrapper
namespace MyApp.Utilities;

internal static class SafeExec
{
    public static void Try(Action action,
        [CallerMemberName] string? caller = null)
    {
        try { action(); }
        catch (Exception ex)
        {
            Debug.WriteLine($"[SafeExec:{caller}] {ex.Message}");
        }
    }

    public static async Task TryAsync(Func<Task> action,
        [CallerMemberName] string? caller = null)
    {
        try { await action(); }
        catch (Exception ex)
        {
            Debug.WriteLine($"[SafeExec:{caller}] {ex.Message}");
        }
    }
}
```

---

## Logging

### Thread-Safe File Logger

```csharp
namespace MyApp.Services;

public static class Logger
{
    private static readonly object _lock = new();
    private static readonly string _logFilePath;

    static Logger()
    {
        var dir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "MyApp");
        Directory.CreateDirectory(dir);
        _logFilePath = Path.Combine(dir, "app.log");

        // Rotate if > 5MB
        try
        {
            var fi = new FileInfo(_logFilePath);
            if (fi.Exists && fi.Length > 5 * 1024 * 1024)
            {
                var backup = Path.Combine(dir, "app.log.old");
                if (File.Exists(backup)) File.Delete(backup);
                File.Move(_logFilePath, backup);
            }
        }
        catch { }
    }

    public static void Info(string message)  => Log("INFO", message);
    public static void Warn(string message)  => Log("WARN", message);
    public static void Error(string message) => Log("ERROR", message);

    private static void Log(string level, string message)
    {
        var line = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] [{level}] {message}";
        lock (_lock)
        {
            try { File.AppendAllText(_logFilePath, line + Environment.NewLine); }
            catch { }
        }
#if DEBUG
        System.Diagnostics.Debug.WriteLine(line);
#endif
    }
}
```

### Logger Interface for DI

```csharp
public interface IAppLogger
{
    void Info(string message);
    void Debug(string message);
    void Warn(string message);
    void Error(string message, Exception? ex = null);
}
```

---

## Testing

### xUnit Project Setup

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="xunit" Version="2.*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="3.*" />
    <PackageReference Include="coverlet.collector" Version="6.*" />
  </ItemGroup>

  <ItemGroup>
    <Using Include="Xunit" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\MyApp.Shared\MyApp.Shared.csproj" />
  </ItemGroup>
</Project>
```

### Test Patterns

```csharp
public class SettingsTests : IDisposable
{
    private readonly string _tempDir;

    public SettingsTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(),
            $"myapp-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(_tempDir);
    }

    public void Dispose()
    {
        try { Directory.Delete(_tempDir, true); } catch { }
    }

    [Fact]
    public void GetValue_ReturnsDefault_WhenKeyMissing()
    {
        var settings = CreateSettings();
        var result = settings.GetValue("nonexistent", "fallback");
        Assert.Equal("fallback", result);
    }

    [Theory]
    [InlineData("key1", "value1")]
    [InlineData("key2", "value2")]
    public void SetValue_StoresAndRetrieves(string key, string value)
    {
        var settings = CreateSettings();
        settings.SetValue(key, value);
        Assert.Equal(value, settings.GetValue(key));
    }
}
```

Run tests:

```bash
dotnet test
dotnet test --filter "FullyQualifiedName~SettingsTests"
```

---

## Networking

### Exponential Backoff Reconnection

```csharp
private static readonly int[] BackoffMs = { 1000, 2000, 4000, 8000, 15000, 30000, 60000 };
private int _reconnectAttempts;

private async Task ReconnectWithBackoffAsync(CancellationToken ct)
{
    var index = Math.Min(_reconnectAttempts, BackoffMs.Length - 1);
    var delay = BackoffMs[index];

    Debug.WriteLine($"Reconnecting in {delay}ms (attempt {_reconnectAttempts + 1})");

    await Task.Delay(delay, ct);
    await ConnectAsync(ct);
    _reconnectAttempts++;
}

// Reset on successful connect
private void OnConnected()
{
    _reconnectAttempts = 0;
}
```

### Named HTTP Clients

Register once in DI, use everywhere:

```csharp
// Registration
services.AddHttpClient("AppApi", client =>
{
    client.DefaultRequestHeaders.Add("User-Agent", "MyApp/1.0");
    client.Timeout = TimeSpan.FromSeconds(10);
});

// Usage in services
public class ApiService
{
    private readonly IHttpClientFactory _httpClientFactory;

    public ApiService(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public async Task<string> GetDataAsync(CancellationToken ct = default)
    {
        using var client = _httpClientFactory.CreateClient("AppApi");
        var response = await client.GetAsync("/api/data", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadAsStringAsync(ct);
    }
}
```

---

## Deep Links & IPC

### URI Scheme Registration

```csharp
public static void RegisterUriScheme(string scheme, string friendlyName)
{
    var exePath = Environment.ProcessPath ?? "";

    using var key = Registry.CurrentUser.CreateSubKey(
        $@"Software\Classes\{scheme}");
    key.SetValue("", $"URL:{friendlyName}");
    key.SetValue("URL Protocol", "");

    using var iconKey = key.CreateSubKey("DefaultIcon");
    iconKey?.SetValue("", $"\"{exePath}\",1");

    using var commandKey = key.CreateSubKey(@"shell\open\command");
    commandKey?.SetValue("", $"\"{exePath}\" \"%1\"");
}
```

### Named Pipe IPC (Single Instance)

```csharp
private const string PipeName = "MyApp-IPC";

// Sender (second instance)
private static void SendToRunningInstance(string message)
{
    using var client = new NamedPipeClientStream(".", PipeName, PipeDirection.Out);
    client.Connect(1000);
    using var writer = new StreamWriter(client);
    writer.WriteLine(message);
    writer.Flush();
}

// Receiver (primary instance)
private void StartIpcServer()
{
    _ = Task.Run(async () =>
    {
        while (!_disposed)
        {
            try
            {
                using var server = new NamedPipeServerStream(PipeName, PipeDirection.In);
                await server.WaitForConnectionAsync();
                using var reader = new StreamReader(server);
                var message = await reader.ReadLineAsync();
                if (!string.IsNullOrEmpty(message))
                {
                    Application.Current.Dispatcher.InvokeAsync(
                        () => HandleIpcMessage(message));
                }
            }
            catch
            {
                await Task.Delay(1000);
            }
        }
    });
}
```

---

## Build & Packaging

### Build Commands

```bash
# Debug build
dotnet build

# Release build
dotnet build -c Release

# Self-contained single-file EXE
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true

# ARM64 build
dotnet publish -c Release -r win-arm64 --self-contained -p:PublishSingleFile=true
```

### MSIX Packaging

Add conditional MSIX support in csproj:

```xml
<!-- Unpackaged (traditional EXE) — default -->
<PropertyGroup Condition="'$(PackageMsix)' != 'true'">
  <WindowsPackageType>None</WindowsPackageType>
</PropertyGroup>

<!-- MSIX packaged (store/sideload) -->
<PropertyGroup Condition="'$(PackageMsix)' == 'true'">
  <WindowsPackageType>MSIX</WindowsPackageType>
  <AppxPackageSigningEnabled>false</AppxPackageSigningEnabled>
  <GenerateAppxPackageOnBuild>true</GenerateAppxPackageOnBuild>
</PropertyGroup>
```

Build MSIX:

```bash
dotnet publish -c Release -p:PackageMsix=true
```

### CI/CD with GitHub Actions

```yaml
name: Build and Test

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:

jobs:
  test:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-dotnet@v4
      with: { dotnet-version: 10.0.x }
    - run: dotnet restore
    - run: dotnet build -c Debug
    - run: dotnet test --no-build -c Debug

  build:
    needs: test
    runs-on: windows-latest
    strategy:
      matrix:
        rid: [win-x64, win-arm64]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-dotnet@v4
      with: { dotnet-version: 10.0.x }
    - run: >
        dotnet publish src/MyApp/MyApp.csproj
        -c Release -r ${{ matrix.rid }}
        --self-contained
        -p:PublishSingleFile=true
        -o publish
    - uses: actions/upload-artifact@v4
      with:
        name: myapp-${{ matrix.rid }}
        path: publish/
```

---

## Theme Detection

```csharp
public static class ThemeHelper
{
    public static bool IsDarkMode()
    {
        try
        {
            using var key = Registry.CurrentUser.OpenSubKey(
                @"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize");
            var value = key?.GetValue("AppsUseLightTheme");
            return value is int i && i == 0;
        }
        catch { return false; }
    }
}
```

---

## XAML Resources

### App-Level Resource Dictionary

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceDictionary Source="Themes/Colors.xaml" />
            <ResourceDictionary Source="Themes/Styles.xaml" />
        </ResourceDictionary.MergedDictionaries>

        <BooleanToVisibilityConverter x:Key="BoolToVisibilityConverter" />
    </ResourceDictionary>
</Application.Resources>
```

### Custom Styles

```xml
<!-- Themes/Styles.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <Style x:Key="PrimaryButton" TargetType="Button">
        <Setter Property="Background" Value="{StaticResource PrimaryBrush}" />
        <Setter Property="Foreground" Value="White" />
        <Setter Property="Padding" Value="16,8" />
        <Setter Property="BorderThickness" Value="0" />
        <Setter Property="Cursor" Value="Hand" />
        <Style.Triggers>
            <Trigger Property="IsMouseOver" Value="True">
                <Setter Property="Opacity" Value="0.9" />
            </Trigger>
            <Trigger Property="IsEnabled" Value="False">
                <Setter Property="Opacity" Value="0.5" />
            </Trigger>
        </Style.Triggers>
    </Style>
</ResourceDictionary>
```

---

## What NOT to Do

- Don't use `Dispatcher.Invoke` (synchronous) — use `Dispatcher.InvokeAsync`
- Don't call `.Result` or `.Wait()` on Tasks — deadlocks the UI thread
- Don't use `App.ServiceProvider` directly — inject through constructors
- Don't fire-and-forget with `_ = Task.Run(...)` — use `AsyncHelper.FireAndForget`
- Don't leave empty `catch { }` blocks — use `SafeExec.Try()` or log the error
- Don't use `System.Timers.Timer` for UI work — use `DispatcherTimer`
- Don't create GDI objects without disposing them — always call `DestroyIcon`
- Don't add NuGet packages without confirming with the user
- Don't modify XAML styles without visual verification
- Don't refactor more than what was asked — scope creep is the enemy
