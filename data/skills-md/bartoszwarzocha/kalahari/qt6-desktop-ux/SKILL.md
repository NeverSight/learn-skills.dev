---
name: qt6-desktop-ux
description: Qt6 UI/UX patterns for desktop applications. Use for dialogs, panels, toolbars.
---

# Qt6 Desktop UX Patterns

## 1. QDockWidget (Dockable Panels)

### When to use
- Navigator panel
- Properties panel
- Log panel
- Any side panel

### Pattern
```cpp
QDockWidget* dock = new QDockWidget(tr("Panel Title"), parent);
dock->setObjectName("uniquePanelName");  // for state persistence
dock->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
dock->setFeatures(QDockWidget::DockWidgetMovable |
                  QDockWidget::DockWidgetClosable |
                  QDockWidget::DockWidgetFloatable);

QWidget* content = new QWidget();
// ... setup content layout
dock->setWidget(content);

parent->addDockWidget(Qt::RightDockWidgetArea, dock);
```

## 2. QGroupBox (Visual Grouping)

### When to use
- Group related controls
- Settings sections
- Form sections

### Pattern
```cpp
QGroupBox* group = new QGroupBox(tr("Section Title"));
QVBoxLayout* groupLayout = new QVBoxLayout(group);

// Add controls to groupLayout
groupLayout->addWidget(control1);
groupLayout->addWidget(control2);

// Add group to parent layout
mainLayout->addWidget(group);
```

## 3. Spacing and Margins

### Standard values
- Between controls: 6px
- Group margins: 11px
- Dialog margins: 11px

### Pattern
```cpp
layout->setSpacing(6);
layout->setContentsMargins(11, 11, 11, 11);
```

## 4. QSizePolicy

### Policies
| Policy | Behavior |
|--------|----------|
| Fixed | Exact size, no stretching |
| Preferred | Preferred size, can shrink/grow |
| Expanding | Fills available space |
| Minimum | At least minimum size |
| Maximum | At most maximum size |

### Pattern
```cpp
widget->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
```

## 5. Stretch Factors

### In layouts
```cpp
layout->addWidget(widget1, 0);  // fixed
layout->addWidget(widget2, 1);  // fills remaining space
layout->addStretch(1);          // spacer that expands
```

## 6. QDialog (Modal Windows)

### Pattern
```cpp
class MyDialog : public QDialog {
    Q_OBJECT
public:
    explicit MyDialog(QWidget* parent = nullptr);

private:
    void setupUI();
    void createConnections();

    // Controls as members
    QLineEdit* m_nameEdit;
    QDialogButtonBox* m_buttonBox;
};

MyDialog::MyDialog(QWidget* parent)
    : QDialog(parent)
{
    setWindowTitle(tr("Dialog Title"));
    setupUI();
    createConnections();
}

void MyDialog::setupUI() {
    QVBoxLayout* mainLayout = new QVBoxLayout(this);

    // Content
    m_nameEdit = new QLineEdit();
    mainLayout->addWidget(m_nameEdit);

    // Standard buttons
    m_buttonBox = new QDialogButtonBox(
        QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
    mainLayout->addWidget(m_buttonBox);
}

void MyDialog::createConnections() {
    connect(m_buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
    connect(m_buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
}
```

## 7. Accessibility

### Required for all controls
```cpp
widget->setToolTip(tr("Descriptive tooltip"));
widget->setWhatsThis(tr("Detailed help text"));
widget->setAccessibleName(tr("Name for screen readers"));
```

### Tab order
```cpp
setTabOrder(widget1, widget2);
setTabOrder(widget2, widget3);
```

## 8. Responsive Design

### Minimum sizes
```cpp
widget->setMinimumWidth(200);
widget->setMinimumHeight(100);
```

### Maximum sizes (when needed)
```cpp
widget->setMaximumWidth(400);
```

## 9. QToolBar

### Pattern
```cpp
QToolBar* toolbar = new QToolBar(tr("Main Toolbar"), parent);
toolbar->setObjectName("mainToolbar");
toolbar->setMovable(true);
toolbar->setIconSize(QSize(24, 24));

// Add actions (use ArtProvider!)
QAction* action = core::ArtProvider::getInstance().createAction("file.new", toolbar);
toolbar->addAction(action);
toolbar->addSeparator();
```

## 10. Theme Integration

### Connect to theme changes
```cpp
connect(&core::ThemeManager::getInstance(), &core::ThemeManager::themeChanged,
        this, &MyWidget::onThemeChanged);

void MyWidget::onThemeChanged() {
    // Update colors, refresh UI
    update();
}
```

### Adding new theme colors
When a component needs a new custom color, use the automated script:
```bash
python scripts/add_theme_color.py colorName "#darkHex" "#lightHex" -d "description" -s
```
See `kalahari-coding` skill for full documentation.

## 11. Qt6 Documentation (Context7 MCP)

When unsure about Qt6 API, signals, slots, or properties - **ALWAYS check Context7 first**:

### Step 1: Resolve Qt6 library ID (once per session)
```
mcp__context7__resolve-library-id("Qt6")
```
Returns: `/qt/qtdoc` or similar

### Step 2: Get documentation for specific topic
```
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/qt/qtdoc",
    topic="QDockWidget"
)
```

### Common Qt6 topics to look up:
| Topic | When to use |
|-------|-------------|
| `QDockWidget` | Creating dockable panels |
| `QDialog` | Modal dialogs |
| `QLayout` | Layout management |
| `QSizePolicy` | Widget sizing behavior |
| `signals slots` | Signal/slot connections |
| `QToolBar` | Toolbar creation |
| `QAction` | Action/command patterns |
| `QStyle` | Styling and theming |

### When to use Context7:
- ✅ Unsure about method parameters
- ✅ Need to know available signals/slots
- ✅ Looking for Qt6-specific patterns
- ✅ Checking deprecation status
