---
name: electron-dev
description: Build cross-platform desktop applications with Electron using best practices for security, performance, and user experience. Use this skill when developing system tools (file managers, screenshot tools, productivity apps) or when working with Electron projects. Triggers include requests to create Electron apps, implement file operations, system tray functionality, window management, IPC communication, or optimize Electron performance. Supports vanilla JavaScript, React, and Vue frameworks with comprehensive code templates that embed security and performance best practices directly in comments.
---

# Electron Development

Build production-ready Electron applications with security-first architecture, optimal performance, and excellent user experience.

## When to Use This Skill

Use this skill when you need to:
- Create new Electron applications from scratch
- Implement secure IPC communication between main and renderer processes
- Add file system operations (read, write, watch, drag & drop)
- Integrate system features (tray icons, global shortcuts, notifications)
- Manage windows (multi-window, frameless, modal dialogs)
- Optimize application performance
- Integrate React or Vue frameworks with Electron
- Follow Electron security best practices

## Quick Start

### Creating a New Project

For a complete, production-ready Electron project with all best practices:

```bash
# Copy the vanilla template to your working directory
cp -r assets/vanilla-template/* /path/to/your/project

# Install dependencies
cd /path/to/your/project
npm install

# Start development
npm run dev
```

The template includes:
- ✅ Secure main process with proper configuration
- ✅ Context-isolated preload script
- ✅ Example renderer with file operations, window controls, notifications
- ✅ System tray integration
- ✅ Global keyboard shortcuts
- ✅ Comprehensive comments explaining every best practice
- ✅ Cross-platform build configuration

### For Framework-Specific Projects

If you need React or Vue integration, consult `references/framework-guides.md` first for detailed setup instructions, then use the vanilla template as a reference for security and IPC patterns.

## Core Capabilities

### 1. Secure Architecture

Every code template in this skill implements Electron's security best practices:

**Security settings (always applied):**
```javascript
webPreferences: {
  contextIsolation: true,    // Isolates renderer from main process
  nodeIntegration: false,     // Prevents Node.js access in renderer
  sandbox: true,              // Sandboxes renderer process
  preload: path.join(__dirname, 'preload.js'),
}
```

**Why this matters:** These settings prevent remote code execution, protect against XSS attacks, and ensure malicious web content can't access system resources.

For comprehensive security guidance, see `references/security-guide.md`.

### 2. IPC Communication Patterns

All IPC communication goes through validated channels in the preload script:

**Three main patterns:**
1. **Request-Response** (invoke/handle): For operations that need a return value
2. **One-Way** (send/on): For notifications and events
3. **Streaming**: For real-time updates like file watching

Each pattern includes:
- Input validation in both preload and main process
- Structured error handling
- Proper cleanup functions
- Performance optimizations

For detailed IPC patterns and examples, see `references/ipc-patterns.md`.

### 3. File System Operations

The vanilla template demonstrates:
- Opening files via native dialog
- Reading file contents securely
- Writing files with user confirmation
- Watching files for changes
- Drag & drop support with visual feedback

All file operations include:
- Path validation (prevent path traversal)
- Error handling with user-friendly messages
- Performance considerations (streaming for large files)
- Cross-platform compatibility

### 4. System Integration

Templates show how to implement:
- **System tray**: With context menu and click handlers
- **Global shortcuts**: Cross-platform keyboard shortcuts
- **Native notifications**: With click handlers
- **Window management**: Minimize, maximize, close, multi-window
- **Custom title bars**: For frameless windows

All system integrations include platform-specific handling for macOS, Windows, and Linux.

### 5. Performance Optimization

Code templates implement performance best practices:
- Lazy window loading (show only when ready)
- Debouncing frequent operations
- Proper memory cleanup
- Efficient IPC batching
- Hardware acceleration

For comprehensive performance tips, see `references/performance-tips.md`.

## Workflow

### For New Projects

1. **Choose your framework**
   - Vanilla JavaScript: Use `assets/vanilla-template/` directly
   - React/Vue: Read `references/framework-guides.md` then adapt patterns

2. **Copy template to your project directory**
   ```bash
   cp -r assets/vanilla-template/* /your/project/
   ```

3. **Install dependencies**
   ```bash
   cd /your/project
   npm install
   ```

4. **Customize for your needs**
   - Update `package.json` (name, description, build config)
   - Modify UI in `src/renderer/`
   - Add IPC handlers in `src/main/main.js`
   - Expose APIs in `src/preload/preload.js`

5. **Test in development**
   ```bash
   npm run dev
   ```

6. **Build for distribution**
   ```bash
   npm run build          # All platforms
   npm run build:mac      # macOS only
   npm run build:win      # Windows only  
   npm run build:linux    # Linux only
   ```

### For Adding Features to Existing Projects

1. **Identify the feature type**
   - File operations → See template's file handling code
   - IPC communication → Check `references/ipc-patterns.md`
   - System integration → Review tray/shortcut examples
   - Performance issues → Consult `references/performance-tips.md`

2. **Find relevant code in template**
   - `src/main/main.js`: Main process examples
   - `src/preload/preload.js`: Secure API exposure
   - `src/renderer/renderer.js`: Renderer-side usage

3. **Copy and adapt the pattern**
   - All code includes detailed comments explaining why and how
   - Security and performance best practices are embedded
   - Cross-platform considerations are noted

4. **Test thoroughly**
   - Test on all target platforms
   - Verify security settings
   - Check performance with real data

## Code Examples

All code examples in this skill follow these principles:

**1. Comments explain WHY, not just WHAT**
```javascript
// ❌ BAD comment
// Create window
const win = new BrowserWindow({ show: false });

// ✅ GOOD comment (from template)
// UX: Hide window initially to prevent flickering
// Show only when ready-to-show event fires
const win = new BrowserWindow({ show: false });
```

**2. Security is non-negotiable**
```javascript
// Every IPC handler validates input
ipcMain.handle('file:read', async (event, filePath) => {
  // SECURITY: Validate that the path is absolute to prevent path traversal
  if (!path.isAbsolute(filePath)) {
    throw new Error('File path must be absolute');
  }
  // ... rest of implementation
});
```

**3. Performance is considered**
```javascript
// Debounce frequent operations
let debounceTimer;
ipcMain.handle('search', async (event, query) => {
  return new Promise((resolve) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const results = await searchDatabase(query);
      resolve(results);
    }, 300);
  });
});
```

**4. Cross-platform compatibility**
```javascript
// PLATFORM SPECIFIC: Handle tray click differently on different platforms
tray.on('click', () => {
  if (process.platform === 'win32') {
    // Windows: Click to show/hide
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  }
  // macOS: Tray doesn't typically toggle window visibility
});
```

## Reference Documentation

This skill includes comprehensive reference guides:

### references/ipc-patterns.md
Complete guide to IPC communication patterns:
- Request-response (invoke/handle)
- One-way communication (send/on)
- Streaming data
- Input validation strategies
- Channel whitelisting
- Error handling patterns
- Performance optimization
- Common pitfalls to avoid

**When to read**: Implementing any communication between main and renderer processes.

### references/security-guide.md
Comprehensive security best practices:
- Configuration checklist
- Content Security Policy setup
- Input validation (file paths, URLs, commands)
- Navigation and window security
- Safe handling of remote content
- Secure updates with code signing
- Dependency security
- Encryption for sensitive data
- Production security checklist

**When to read**: Before releasing to production, when handling user input, or dealing with external content.

### references/performance-tips.md
Performance optimization techniques:
- Startup optimization
- Main process performance
- Renderer process optimization
- Memory management
- IPC performance
- GPU acceleration
- Network optimization
- Profiling tools and techniques

**When to read**: When experiencing performance issues or optimizing for production.

### references/framework-guides.md
Integrating popular frameworks:
- React setup and configuration
- Vue integration
- TypeScript support
- State management (Redux, Pinia)
- Build process and hot reload
- Common issues and solutions

**When to read**: Building with React, Vue, or TypeScript.

## Project Templates

### assets/vanilla-template/
Complete Electron project with vanilla HTML/CSS/JavaScript:

**Structure:**
```
vanilla-template/
├── src/
│   ├── main/
│   │   └── main.js           # Main process with all features
│   ├── preload/
│   │   └── preload.js        # Secure IPC bridge
│   └── renderer/
│       ├── index.html        # UI with examples
│       ├── styles.css        # Modern styling
│       └── renderer.js       # Event handlers and logic
├── package.json              # Dependencies and build config
├── README.md                 # Project documentation
└── .gitignore
```

**Features demonstrated:**
- ✅ File operations (open, read, write, watch)
- ✅ Drag & drop support
- ✅ Window controls (minimize, maximize, close)
- ✅ System tray with context menu
- ✅ Global keyboard shortcuts
- ✅ Native notifications
- ✅ Custom title bar
- ✅ Cross-platform build configuration
- ✅ Development and production modes

**Every file includes:**
- Detailed comments explaining best practices
- Security considerations marked with "SECURITY:"
- Performance tips marked with "PERFORMANCE:"
- UX improvements marked with "UX:"
- Platform-specific code marked with "PLATFORM SPECIFIC:"

## Best Practices Summary

The code in this skill embodies these principles:

**Security (CRITICAL):**
- ✅ Always use contextIsolation: true
- ✅ Always use nodeIntegration: false
- ✅ Always validate inputs in main process
- ✅ Never expose full Node.js/Electron APIs to renderer
- ✅ Use Content Security Policy

**Performance:**
- ✅ Show windows only when ready
- ✅ Debounce/throttle frequent operations
- ✅ Batch IPC calls when possible
- ✅ Clean up event listeners
- ✅ Use streaming for large files

**User Experience:**
- ✅ Provide visual feedback for async operations
- ✅ Handle errors gracefully with user-friendly messages
- ✅ Support keyboard shortcuts
- ✅ Smooth window transitions
- ✅ Platform-appropriate behavior

**Code Quality:**
- ✅ Modular, well-organized code structure
- ✅ Comprehensive error handling
- ✅ Clear, informative comments
- ✅ Consistent naming conventions
- ✅ Cross-platform compatibility

## Common Tasks

### Adding a New IPC Handler

1. Add handler in main process (`src/main/main.js`)
2. Expose in preload script (`src/preload/preload.js`)
3. Use in renderer (`src/renderer/renderer.js`)

Example in template shows complete pattern with validation and error handling.

### Implementing File Operations

See the file operations section in vanilla template:
- Dialog-based file selection
- Secure file reading/writing
- File watching for real-time updates
- Drag & drop support

### Creating Multi-Window Applications

Use the `createChildWindow` function in the template as a starting point. Supports:
- Parent-child window relationships
- Modal dialogs
- Independent windows

### Cross-Platform Building

Build configuration in `package.json` handles:
- macOS: DMG and ZIP
- Windows: NSIS installer and portable
- Linux: AppImage and DEB package

## Troubleshooting

Common issues and solutions:

**White screen in production:**
- Ensure paths are correct for packaged app
- Set `homepage: "./"` in package.json

**IPC not working:**
- Check contextBridge is exposing APIs correctly
- Verify channel names match between main and preload

**Performance issues:**
- Profile with Chrome DevTools
- Check for memory leaks (event listeners not cleaned up)
- Consider using utility processes for heavy work

**Security warnings:**
- Review security checklist in `references/security-guide.md`
- Ensure all security settings are enabled
- Validate all user inputs

For detailed troubleshooting, consult the reference documentation.

## Next Steps

After creating your Electron app:

1. **Test thoroughly** on all target platforms
2. **Review security checklist** before production
3. **Optimize performance** using profiling tools
4. **Set up auto-updates** with electron-updater
5. **Configure code signing** for distribution
6. **Consider error tracking** for production monitoring

This skill provides the foundation for professional Electron development. All code is production-ready and follows industry best practices.
