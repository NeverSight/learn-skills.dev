---
name: alloy-howtos
description: "Titanium Alloy CLI and configuration guide. Use when creating, reviewing, analyzing, or examining Alloy projects, running alloy commands (new, generate, compile), configuring alloy.jmk or config.json, debugging compilation errors, creating conditional views, using Backbone.Events for communication, or writing custom XML tags."
argument-hint: "[task]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(alloy *), Bash(node *)
---

# Titanium Alloy How-tos

Practical guide for Alloy MVC projects in the Titanium SDK.

## Project detection

:::info Auto-detects Alloy projects
This skill checks for Alloy projects when invoked and provides CLI and configuration guidance.

Detection is automatic. No manual command is needed.

Alloy project indicators:
- `app/` folder with Alloy structure
- `alloy.jmk` or `config.json` files

Behavior based on detection:
- Alloy detected -> Provide Alloy CLI command guidance, configuration file help, Alloy-specific troubleshooting
- Not detected -> Explain this skill is for Alloy projects only and suggest Alloy guides if the user wants to migrate
:::

## Quick reference

| Topic                                        | Reference                                                               |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| Best Practices & Naming Conventions          | [best_practices.md](references/best_practices.md)                       |
| CLI Commands (new, generate, compile)        | [cli_reference.md](references/cli_reference.md)                         |
| Configuration Files (alloy.jmk, config.json) | [config_files.md](references/config_files.md)                           |
| Custom XML Tags & Reusable Components        | [custom_tags.md](references/custom_tags.md)                             |
| Debugging & Common Errors                    | [debugging_troubleshooting.md](references/debugging_troubleshooting.md) |
| Code Samples & Conditionals                  | [samples.md](references/samples.md)                                     |

## Key practices

### Naming conventions
- **Never use double underscore prefixes** (`__foo`) - reserved for Alloy
- **Never use JavaScript reserved words as IDs**

### Global events - use Backbone.Events
Avoid `Ti.App.fireEvent` / `Ti.App.addEventListener`. It can cause memory leaks and poor performance.

Use the Backbone.Events pattern:
```javascript
// In alloy.js
Alloy.Events = _.clone(Backbone.Events);

// Listener
Alloy.Events.on('updateMainUI', refreshData);
// Clean up on close
$.controller.addEventListener('close', () => {
    Alloy.Events.off('updateMainUI');
});

// Trigger
Alloy.Events.trigger('updateMainUI');
```

### Global variables in non-controller files
Always require Alloy modules:
```javascript
const Alloy = require('alloy');
const Backbone = require('alloy/backbone');
const _ = require('alloy/underscore')._;
```

## Conditional views

Use `if` attributes in XML for conditional rendering (evaluated before render):

```xml
<Alloy>
    <Window>
        <View if="Alloy.Globals.isLoggedIn()" id="notLoggedIn">
             <Label text="Not logged in" />
        </View>
        <View if="!Alloy.Globals.isLoggedIn()" id="loggedIn">
            <Label text="Logged in" />
        </View>
    </Window>
</Alloy>
```

Conditional TSS styles:
```tss
"#info[if=Alloy.Globals.isIos7Plus]": {
    font: { textStyle: Ti.UI.TEXT_STYLE_FOOTNOTE }
}
```

Data-binding conditionals:
```xml
<TableViewRow if="$model.shouldShowCommentRow()">
```

## Common error solutions

| Error                                   | Solution                                                |
| --------------------------------------- | ------------------------------------------------------- |
| `No app.js found`                       | Run `alloy compile --config platform=<platform>`        |
| Android assets not showing              | Use absolute paths (prepend `/`)                        |
| `Alloy is not defined` (non-controller) | Add `const Alloy = require('alloy');`                   |
| iOS `invalid method passed to UIModule` | Creating Android-only object - use `platform` attribute |

## CLI quick reference

```bash
# New project
alloy new [path] [template]

# Generate components
alloy generate controller <name>
alloy generate model <name> <adapter> <schema>
alloy generate style --all

# Compile
alloy compile [--config platform=android,deploytype=test]

# Extract i18n strings
alloy extract-i18n en --apply

# Copy/move/remove controllers
alloy copy <old> <new>
alloy move <old> <new>
alloy remove <name>
```

## Configuration files priority

**config.json precedence:** `os:ios` > `env:production` > `global`

Access at runtime: `Alloy.CFG.yourKey`

## Custom XML tags

Create reusable components without widgets. Drop a file in `app/lib/`:

**app/lib/checkbox.js**
```javascript
exports.createCheckBox = args => {
    const wrapper = Ti.UI.createView({ layout: "horizontal", checked: false });
    const box = Ti.UI.createView({ width: 15, height: 15, borderWidth: 1 });
    // ... build component, return Ti.UI.* object
    return wrapper;
};
```

**view.xml**
```xml
<CheckBox module="checkbox" id="terms" caption="I agree" onChange="onCheck" />
```

Key: the `module` attribute points to the file in `app/lib/` (without `.js`). The function must be `create<TagName>`.

See [custom_tags.md](references/custom_tags.md) for complete examples.

## Resources

### references/

Reference docs by topic:
- **best_practices.md** - Coding standards, naming conventions, global events patterns
- **cli_reference.md** - All CLI commands with options and model schema format
- **config_files.md** - alloy.jmk tasks, config.json structure, widget.json format
- **custom_tags.md** - Creating reusable custom XML tags without widgets
- **debugging_troubleshooting.md** - Common errors with solutions
- **samples.md** - Controller examples, conditional views, data-binding patterns

## Related skills

For tasks beyond Alloy CLI and configuration, use these related skills:

| Task                                     | Use This Skill |
| ---------------------------------------- | -------------- |
| Modern architecture, services, patterns  | `ti-expert`    |
| Alloy MVC concepts, models, data binding | `alloy-guides` |
| SDK config, Hyperloop, app distribution  | `ti-guides`    |
