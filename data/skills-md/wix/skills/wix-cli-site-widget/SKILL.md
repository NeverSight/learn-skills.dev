---
name: wix-cli-site-widget
description: Use when building interactive widgets, custom data displays, or configurable site components with settings panels. Triggers include widget, custom element, interactive component, editor component, configurable widget, web component.
compatibility: Requires Wix CLI development environment.
---

# Wix Site Widget Builder

Creates custom element widget extensions for Wix CLI applications. Site widgets are React components converted to web components that appear in the Wix Editor, allowing site owners to add interactive, configurable widgets to their pages with a built-in settings panel.

## Quick Start Checklist

Follow these steps in order when creating a site widget:

1. [ ] Create widget folder: `src/site/widgets/custom-elements/<widget-name>/`
2. [ ] Create `widget.tsx` with React component and `reactToWebComponent` conversion
3. [ ] Create `panel.tsx` with WDS components and `widget.getProp/setProp`
4. [ ] Create `extensions.ts` with `extensions.customElement()` and unique UUID
5. [ ] Update `src/extensions.ts` to import and use the new extension

## Architecture

Site widgets consist of **two required files**:

### 1. Widget Component (`widget.tsx`)

React component converted to a web component using `react-to-webcomponent`:

- Define Props interface with configurable properties (camelCase)
- Create a React functional component that renders the widget UI
- Convert to web component with props mapping
- Use inline styles (no CSS imports)
- Handle Wix Editor environment when using Wix Data API

### 2. Settings Panel (`panel.tsx`)

Settings panel shown in the Wix Editor sidebar:

- Uses Wix Design System components (see [references/SETTINGS_PANEL.md](references/SETTINGS_PANEL.md))
- Manages widget properties via `@wix/editor` widget API
- Loads initial values with `widget.getProp('kebab-case-name')`
- Updates properties with `widget.setProp('kebab-case-name', value)`
- Wrapped in `WixDesignSystemProvider > SidePanel > SidePanel.Content`
- For color pickers, use `inputs.selectColor()` from `@wix/editor` with `FillPreview` — NOT `<Input type="color">`
- For font pickers, use `inputs.selectFont()` from `@wix/editor` with a `Button` — NOT a text Input

## Widget Component Pattern

```typescript
import React, { type FC, useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import reactToWebComponent from 'react-to-webcomponent';

interface WidgetProps {
  title?: string;
  targetDate?: string;
  targetTime?: string;
  bgColor?: string;
  textColor?: string;
  font?: string;
}

const CustomElement: FC<WidgetProps> = ({
  title = 'Countdown',
  targetDate = '',
  targetTime = '00:00',
  bgColor = '#ffffff',
  textColor = '#333333',
  font = "{}",
}) => {
  const { font: textFont, textDecoration } = JSON.parse(font);
  const [time, setTime] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0, isExpired: false });

  useEffect(() => {
    if (!targetDate) return;

    const update = () => {
      const target = new Date(`${targetDate}T${targetTime}`);
      const diff = target.getTime() - Date.now();
      if (diff <= 0) {
        setTime({ days: 0, hours: 0, minutes: 0, seconds: 0, isExpired: true });
        return;
      }
      setTime({
        days: Math.floor(diff / (1000 * 60 * 60 * 24)),
        hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((diff % (1000 * 60)) / 1000),
        isExpired: false,
      });
    };

    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [targetDate, targetTime]);

  const styles = {
    wrapper: {
      backgroundColor: bgColor,
      padding: '24px 32px',
      textAlign: 'center' as const,
      display: 'inline-block',
    },
    title: {
      font: textFont || '600 24px sans-serif',
      color: textColor,
      textDecoration,
      marginBottom: '16px',
    },
  };

  return (
    <div style={styles.wrapper}>
      {title && <div style={styles.title}>{title}</div>}
      {/* Widget content */}
    </div>
  );
};

const customElement = reactToWebComponent(CustomElement, React, ReactDOM, {
  props: {
    title: 'string',
    targetDate: 'string',
    targetTime: 'string',
    bgColor: 'string',
    textColor: 'string',
    font: 'string',
  },
});

export default customElement;
```

**Key Points:**

- Props interface uses **camelCase** (e.g., `targetDate`, `bgColor`)
- `reactToWebComponent` config uses camelCase keys with `'string'` type
- All props are passed as strings from the web component
- Use inline styles, not CSS imports
- Parse complex props (like `font`) from JSON strings: `const { font: textFont, textDecoration } = JSON.parse(font)`
- Apply font via `font` CSS shorthand and `textDecoration` property
- Extract helper components, utility functions, and styles into separate files for clean code organization

## Settings Panel Pattern

```typescript
import React, { type FC, useState, useEffect, useCallback } from "react";
import { widget } from "@wix/editor";
import {
  SidePanel,
  WixDesignSystemProvider,
  Input,
  FormField,
  TimeInput,
  Box,
} from "@wix/design-system";
import "@wix/design-system/styles.global.css";
import { ColorPickerField } from "./components/ColorPickerField";
import { FontPickerField } from "./components/FontPickerField";
import { parseTimeValue } from "./utils";

const DEFAULT_BG_COLOR = "#0a0e27";
const DEFAULT_TEXT_COLOR = "#00ff88";
const DEFAULT_TEXT_FONT = "";
const DEFAULT_TEXT_DECORATION = "";

const Panel: FC = () => {
  const [title, setTitle] = useState<string>("Countdown");
  const [targetDate, setTargetDate] = useState<string>("");
  const [targetTime, setTargetTime] = useState<string>("00:00");
  const [bgColor, setBgColor] = useState<string>(DEFAULT_BG_COLOR);
  const [textColor, setTextColor] = useState<string>(DEFAULT_TEXT_COLOR);
  const [font, setFont] = useState({ font: DEFAULT_TEXT_FONT, textDecoration: DEFAULT_TEXT_DECORATION });

  useEffect(() => {
    Promise.all([
      widget.getProp("title"),
      widget.getProp("target-date"),
      widget.getProp("target-time"),
      widget.getProp("bg-color"),
      widget.getProp("text-color"),
      widget.getProp("font"),
    ])
      .then(([titleVal, dateVal, timeVal, bgColorVal, textColorVal, fontString]) => {
        setTitle(titleVal || "Countdown");
        setTargetDate(dateVal || "");
        setTargetTime(timeVal || "00:00");
        setBgColor(bgColorVal || DEFAULT_BG_COLOR);
        setTextColor(textColorVal || DEFAULT_TEXT_COLOR);
        setFont(JSON.parse(fontString || "{}"));
      })
      .catch((error) => console.error("Failed to fetch widget properties:", error));
  }, []);

  const handleTitleChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = event.target.value;
    setTitle(newTitle);
    widget.setProp("title", newTitle);
  }, []);

  const handleDateChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = event.target.value;
    setTargetDate(newDate);
    widget.setProp("target-date", newDate);
  }, []);

  const handleTimeChange = useCallback(({ date }: { date: Date }) => {
    if (date) {
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const newTime = `${hours}:${minutes}`;
      setTargetTime(newTime);
      widget.setProp("target-time", newTime);
    }
  }, []);

  const handleBgColorChange = (value: string) => {
    setBgColor(value);
    widget.setProp("bg-color", value);
  };

  const handleTextColorChange = (value: string) => {
    setTextColor(value);
    widget.setProp("text-color", value);
  };

  const handleFontChange = (value: { font: string; textDecoration: string }) => {
    setFont(value);
    widget.setProp("font", JSON.stringify(value));
  };

  return (
    <WixDesignSystemProvider>
      <SidePanel width="300" height="100vh">
        <SidePanel.Header title="Countdown Settings" />
        <SidePanel.Content noPadding stretchVertically>
          <Box direction="vertical" gap="24px">
            <SidePanel.Field>
              <FormField label="Title" required>
                <Input
                  type="text"
                  value={title}
                  onChange={handleTitleChange}
                  placeholder="Enter countdown title"
                />
              </FormField>
            </SidePanel.Field>

            <SidePanel.Field>
              <FormField label="Target Date" required>
                <Input
                  type="date"
                  value={targetDate}
                  onChange={handleDateChange}
                />
              </FormField>
            </SidePanel.Field>

            <SidePanel.Field>
              <FormField label="Target Time" required>
                <TimeInput
                  value={parseTimeValue(targetTime)}
                  onChange={handleTimeChange}
                />
              </FormField>
            </SidePanel.Field>

            <ColorPickerField
              label="Background Color"
              value={bgColor}
              onChange={handleBgColorChange}
            />

            <ColorPickerField
              label="Text Color"
              value={textColor}
              onChange={handleTextColorChange}
            />

            <FontPickerField
              label="Text Font"
              value={font}
              onChange={handleFontChange}
            />
          </Box>
        </SidePanel.Content>
      </SidePanel>
    </WixDesignSystemProvider>
  );
};

export default Panel;
```

**Key Points:**

- Prop names in `widget.getProp()` and `widget.setProp()` use **kebab-case** (e.g., `"target-date"`, `"bg-color"`)
- Always update both local state AND widget prop in onChange handlers
- Wrap content in `WixDesignSystemProvider > SidePanel > SidePanel.Content`
- Use WDS components from `@wix/design-system` (see [references/SETTINGS_PANEL.md](references/SETTINGS_PANEL.md))
- Import `@wix/design-system/styles.global.css` for styles
- For colors, use `ColorPickerField` with `inputs.selectColor()` from `@wix/editor` — NOT `<Input type="color">`
- For fonts, use `FontPickerField` with `inputs.selectFont()` from `@wix/editor` — NOT a text Input
- Font values are stored as JSON strings via `JSON.stringify()` / `JSON.parse()`

## Props Naming Convention

**Critical:** Props use different naming conventions in each file:

| File                           | Convention | Example                                       |
| ------------------------------ | ---------- | --------------------------------------------- |
| `widget.tsx` (Props interface) | camelCase  | `targetDate`, `bgColor`, `textColor`          |
| `panel.tsx` (widget API)       | kebab-case | `"target-date"`, `"bg-color"`, `"text-color"` |
| `reactToWebComponent` config   | camelCase  | `targetDate: 'string'`                        |

The web component automatically converts between camelCase (React props) and kebab-case (HTML attributes).

## Wix Data API Integration

When using Wix Data API in widgets, you **must** handle the Wix Editor environment gracefully:

```typescript
import { items } from "@wix/data";
import { window as wixWindow } from "@wix/site-window";

const CustomElement: FC<WidgetProps> = ({ collectionId }) => {
  const [data, setData] = useState(null);
  const [isEditor, setIsEditor] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      const currentViewMode = await wixWindow.viewMode();

      if (currentViewMode === "Editor") {
        // Don't fetch data in editor - show placeholder
        setIsEditor(true);
        return;
      }

      // Fetch real data only on live site
      try {
        const results = await items.query(collectionId).limit(10).find();
        setData(results.items);
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    };

    loadData();
  }, [collectionId]);

  if (isEditor) {
    return (
      <div style={{ padding: "20px", border: "2px dashed #ccc" }}>
        <p>Widget will display data on the live site</p>
        <p>Collection: {collectionId}</p>
      </div>
    );
  }

  // Render widget with real data
  return (
    <div>
      {data?.map((item) => (
        <div key={item._id}>{item.title}</div>
      ))}
    </div>
  );
};
```

**Requirements:**

- Import `{ window as wixWindow }` from `"@wix/site-window"`
- Check `await wixWindow.viewMode()` before fetching data
- If `viewMode === 'Editor'`, show a placeholder UI instead
- Only fetch and render real data when NOT in editor mode

## Color Selection

For color selection in settings panels, use `ColorPickerField` component with `inputs.selectColor()` from `@wix/editor`. Do NOT use `<Input type="color">`.

```typescript
// components/ColorPickerField.tsx
import React, { type FC } from 'react';
import { inputs } from '@wix/editor';
import { FormField, Box, FillPreview, SidePanel } from '@wix/design-system';

interface ColorPickerFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
}

export const ColorPickerField: FC<ColorPickerFieldProps> = ({
  label,
  value,
  onChange,
}) => (
  <SidePanel.Field>
    <FormField label={label}>
      <Box width="30px" height="30px">
        <FillPreview
          fill={value}
          onClick={() => inputs.selectColor(value, { onChange: (val) => { if (val) onChange(val); } })}
        />
      </Box>
    </FormField>
  </SidePanel.Field>
);
```

Usage in panel:

```typescript
const handleBgColorChange = (value: string) => {
  setBgColor(value);
  widget.setProp("bg-color", value);
};

<ColorPickerField label="Background Color" value={bgColor} onChange={handleBgColorChange} />
```

**Important:** Use `inputs.selectColor(value, { onChange })` from `@wix/editor` with `FillPreview` from WDS. This opens the native Wix color picker with theme colors, gradients, and more. Never use `<Input type="color">`.

## Font Selection

For font selection in settings panels, use `FontPickerField` component with `inputs.selectFont()` from `@wix/editor`. Do NOT use a text Input.

```typescript
// components/FontPickerField.tsx
import React, { type FC } from 'react';
import { inputs } from '@wix/editor';
import { FormField, Button, Text, SidePanel } from '@wix/design-system';

interface FontValue {
  font: string;
  textDecoration: string;
}

interface FontPickerFieldProps {
  label: string;
  value: FontValue;
  onChange: (value: FontValue) => void;
}

export const FontPickerField: FC<FontPickerFieldProps> = ({
  label,
  value,
  onChange,
}) => (
  <SidePanel.Field>
    <FormField label={label}>
      <Button
        size="small"
        priority="secondary"
        onClick={() => inputs.selectFont(value, { onChange: (val) => onChange({ font: val.font, textDecoration: val.textDecoration || "" }) })}
        fullWidth
      >
        <Text size="small" ellipsis>Change Font</Text>
      </Button>
    </FormField>
  </SidePanel.Field>
);
```

Usage in panel:

```typescript
const [font, setFont] = useState<FontValue>({ font: "", textDecoration: "" });

const handleFontChange = (value: FontValue) => {
  setFont(value);
  widget.setProp("font", JSON.stringify(value));
};

<FontPickerField label="Text Font" value={font} onChange={handleFontChange} />
```

**Important:** Use `inputs.selectFont(value, { onChange })` from `@wix/editor` with the callback pattern. This provides a rich font picker dialog with bold, italic, size, and typography features. Font values are stored as JSON strings.

## Output Structure

```
src/site/widgets/custom-elements/
└── {widget-name}/
    ├── widget.tsx           # Main widget component
    ├── panel.tsx            # Settings panel component
    ├── extensions.ts         # Extension registration
    ├── components/          # Optional sub-components
    │   ├── ColorPickerField.tsx
    │   └── FontPickerField.tsx
    └── utils/               # Optional helper functions
        └── formatters.ts
```

## Examples

### Countdown Timer Widget

**Request:** "Create a countdown timer widget"

**Output:**

- Widget with configurable title, target date/time, colors, and font
- Settings panel with date picker, time input, color pickers, font picker
- Real-time countdown display with days, hours, minutes, seconds

### Product Showcase Widget

**Request:** "Create a widget that displays products from a collection"

**Output:**

- Widget that queries Wix Data collection
- Editor environment handling (shows placeholder in editor)
- Settings panel for collection selection, display options, styling
- Responsive grid layout with product cards

### Interactive Calculator Widget

**Request:** "Create a calculator widget with customizable colors"

**Output:**

- Functional calculator component
- Settings panel for color customization (background, buttons, text)
- Inline styles for all styling
- No external dependencies

## Frontend Aesthetics

Avoid generic aesthetics. Create distinctive designs with unique fonts (avoid Inter, Roboto, Arial), cohesive color palettes, CSS animations for micro-interactions, and context-specific choices. Don't use clichéd color schemes or predictable layouts.

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Widget-Specific Extension File

Each site widget requires an `extensions.ts` file in its folder:

```typescript
import { extensions } from "@wix/astro/builders";

export const sitewidgetMyWidget = extensions.customElement({
  id: "{{GENERATE_UUID}}",
  name: "My Widget",
  tagName: "my-widget",
  element: "./site/widgets/custom-elements/my-widget/widget.tsx",
  settings: "./site/widgets/custom-elements/my-widget/panel.tsx",
  installation: {
    autoAdd: true,
  },
  width: {
    defaultWidth: 500,
    allowStretch: true,
  },
  height: {
    defaultHeight: 500,
  },
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property       | Type   | Description                            |
| -------------- | ------ | -------------------------------------- |
| `id`           | string | Unique static UUID v4 (generate fresh) |
| `name`         | string | Display name in editor                 |
| `tagName`      | string | HTML custom element tag (kebab-case)   |
| `element`      | string | Path to widget React component         |
| `settings`     | string | Path to settings panel component       |
| `installation` | object | Auto-add behavior                      |
| `width`        | object | Default width and stretch settings     |
| `height`       | object | Default height settings                |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the widget-specific extension file, you MUST read [wix-cli-extension-registration](../wix-cli-extension-registration/SKILL.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the site widget will not be available in the Wix Editor.**

## Code Quality Requirements

- Strict TypeScript (no `any`, explicit return types)
- Functional React components with hooks
- Proper error handling and loading states
- No `@ts-ignore` comments
- Inline styles only (no CSS imports)
- Handle Wix Editor environment when using Wix Data API
- Consistent prop naming (camelCase in widget, kebab-case in panel)

## Verification

After implementation completes, the **wix-cli-orchestrator** will run validation using [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md).
