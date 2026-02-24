---
name: unlayer-integration
description: Integrates the Unlayer editor into web applications — React, Vue, Angular, or plain JavaScript setup, component props, editor access patterns, multiple instances.
---

# Integrate Unlayer Editor

## Overview

Unlayer provides official wrappers for React, Vue, and Angular, plus a plain JavaScript embed. All wrappers share the same underlying API — only the editor access pattern differs.

## Which Framework?

| Framework | Package | Install | Editor Access |
|-----------|---------|---------|---------------|
| React | `react-email-editor` | `npm i react-email-editor` | `useRef<EditorRef>` → `ref.current?.editor` |
| Vue | `vue-email-editor` | `npm i vue-email-editor` | `this.$refs.emailEditor.editor` |
| Angular | `angular-email-editor` | `npm i angular-email-editor` | `@ViewChild` → `this.emailEditor.editor` |
| Plain JS | CDN script tag | `<script>` embed | Global `unlayer` object |

> ⚠️ **Before installing any Unlayer package**, verify the version exists on npm:
> ```bash
> npm view react-email-editor version   # check latest published version
> ```
> Never pin a version number you haven't verified. Use `npm install <package> --save` without a version to get the latest, or run `npm view <package> versions --json` to see all available versions.

---

## React (Complete Working Example)

```bash
npm install react-email-editor --save
```

```tsx
import React, { useRef, useState } from 'react';
import EmailEditor, { EditorRef, EmailEditorProps } from 'react-email-editor';

const EmailBuilder = () => {
  const emailEditorRef = useRef<EditorRef>(null);
  const [saving, setSaving] = useState(false);

  // Save design JSON + export HTML to your backend
  const handleSave = () => {
    const unlayer = emailEditorRef.current?.editor;
    if (!unlayer) return;

    setSaving(true);
    unlayer.exportHtml(async (data) => {
      try {
        const response = await fetch('/api/templates', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            design: data.design,  // Save this — needed to edit later
            html: data.html,      // The rendered HTML output
          }),
        });
        if (!response.ok) throw new Error('Save failed');
        console.log('Saved successfully');
      } catch (err) {
        console.error('Save error:', err);
      } finally {
        setSaving(false);
      }
    });
  };

  // Load a saved design when editor is ready
  const onReady: EmailEditorProps['onReady'] = async (unlayer) => {
    try {
      const response = await fetch('/api/templates/123');
      if (response.ok) {
        const saved = await response.json();
        unlayer.loadDesign(saved.design); // Pass the saved design JSON
      }
    } catch (err) {
      console.log('No saved design, starting blank');
    }
  };

  return (
    <div>
      <button onClick={handleSave} disabled={saving}>
        {saving ? 'Saving...' : 'Save'}
      </button>
      <EmailEditor
        ref={emailEditorRef}
        onReady={onReady}
        options={{
          projectId: 123456, // Dashboard > Project > Settings
          displayMode: 'email',
        }}
      />
    </div>
  );
};

export default EmailBuilder;
```

**Your backend should accept and return:**

```typescript
// POST /api/templates — save
{ design: object, html: string }

// GET /api/templates/:id — load
{ design: object, html: string, updatedAt: string }
```

**React Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `Object` | `{}` | All `unlayer.init()` options (projectId, displayMode, etc.) |
| `tools` | `Object` | `{}` | Per-tool configuration |
| `appearance` | `Object` | `{}` | Theme and panel settings |
| `onReady` | `Function` | — | Called when editor is ready (receives `unlayer` instance) |
| `onLoad` | `Function` | — | Called when iframe loads (before ready) |
| `style` | `Object` | `{}` | Container inline styles |
| `minHeight` | `String` | `'500px'` | Minimum editor height |

> Docs: https://docs.unlayer.com/builder/react-component
> GitHub: https://github.com/unlayer/react-email-editor

---

## Vue (Complete Working Example)

```bash
npm install vue-email-editor --save
```

```vue
<template>
  <div id="app">
    <button v-on:click="handleSave" :disabled="saving">
      {{ saving ? 'Saving...' : 'Save' }}
    </button>
    <EmailEditor ref="emailEditor" v-on:load="editorLoaded" />
  </div>
</template>

<script>
import { EmailEditor } from 'vue-email-editor';

export default {
  components: { EmailEditor },
  data() {
    return { saving: false };
  },
  methods: {
    async editorLoaded() {
      try {
        const response = await fetch('/api/templates/123');
        if (response.ok) {
          const saved = await response.json();
          this.$refs.emailEditor.editor.loadDesign(saved.design);
        }
      } catch (err) {
        console.log('No saved design, starting blank');
      }
    },
    handleSave() {
      this.saving = true;
      this.$refs.emailEditor.editor.exportHtml(async (data) => {
        try {
          await fetch('/api/templates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ design: data.design, html: data.html }),
          });
        } catch (err) {
          console.error('Save error:', err);
        } finally {
          this.saving = false;
        }
      });
    },
  },
};
</script>
```

**Props:** `minHeight`, `options`, `tools`, `appearance`, `locale`, `projectId`.

> Docs: https://docs.unlayer.com/builder/vue-component
> GitHub: https://github.com/unlayer/vue-email-editor

---

## Angular (Complete Working Example)

```bash
npm install angular-email-editor --save
```

**Module (app.module.ts):**

```typescript
import { EmailEditorModule } from 'angular-email-editor';

@NgModule({ imports: [EmailEditorModule] })
export class AppModule {}
```

**Component (app.component.ts):**

```typescript
import { Component, ViewChild } from '@angular/core';
import { EmailEditorComponent } from 'angular-email-editor';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})
export class AppComponent {
  @ViewChild(EmailEditorComponent)
  private emailEditor: EmailEditorComponent;
  saving = false;

  async editorLoaded() {
    try {
      const response = await fetch('/api/templates/123');
      if (response.ok) {
        const saved = await response.json();
        this.emailEditor.editor.loadDesign(saved.design);
      }
    } catch (err) {
      console.log('No saved design');
    }
  }

  handleSave() {
    this.saving = true;
    this.emailEditor.editor.exportHtml(async (data) => {
      try {
        await fetch('/api/templates', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ design: data.design, html: data.html }),
        });
      } catch (err) {
        console.error('Save error:', err);
      } finally {
        this.saving = false;
      }
    });
  }
}
```

**Template (app.component.html):**

```html
<div>
  <button (click)="handleSave()" [disabled]="saving">
    {{ saving ? 'Saving...' : 'Save' }}
  </button>
  <email-editor (loaded)="editorLoaded($event)"></email-editor>
</div>
```

> Docs: https://docs.unlayer.com/builder/angular-component

---

## Plain JavaScript

```html
<script src="https://editor.unlayer.com/embed.js"></script>
<div id="editor-container" style="height: 700px;"></div>

<script>
  unlayer.init({
    id: 'editor-container',
    projectId: 1234,
    displayMode: 'email',
  });

  unlayer.addEventListener('editor:ready', async function () {
    try {
      const response = await fetch('/api/templates/123');
      if (response.ok) {
        const saved = await response.json();
        unlayer.loadDesign(saved.design);
      }
    } catch (err) {
      console.log('Starting blank');
    }
  });

  function handleSave() {
    unlayer.exportHtml(async function (data) {
      await fetch('/api/templates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ design: data.design, html: data.html }),
      });
    });
  }
</script>
```

> Docs: https://docs.unlayer.com/builder/installation

---

## Multiple Editor Instances

Use `createEditor()` instead of `init()`:

```javascript
const editor1 = unlayer.createEditor({ id: 'email-editor', displayMode: 'email' });
const editor2 = unlayer.createEditor({ id: 'web-editor', displayMode: 'web' });

editor1.loadDesign(emailDesign);
editor2.loadDesign(webDesign);
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Container too small | Minimum **1024px wide x 700px tall**. Editor fills its container. |
| Calling methods before ready | Always wait for `editor:ready` event or `onReady` callback |
| Using `init()` for multiple editors | Use `unlayer.createEditor()` instead |
| Missing `projectId` | Get it from Dashboard > Project > Settings |
| Only saving HTML, not design JSON | Always save **both** — design JSON lets users edit later |
| No loading state while saving | Disable the save button to prevent double saves |
| Pinning a non-existent package version | Run `npm view <package> version` to verify before pinning. Use `npm install <package> --save` without a version to get the latest. |

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| Editor shows blank white space | Container div has 0 height | Set explicit height: `min-height: 700px` |
| `editor:ready` never fires | Script not loaded or wrong `id` | Check `id` matches an existing div, check network tab for embed.js |
| `ref.current?.editor` is undefined | Accessed before mount | Only use inside `onReady` callback |
| Design doesn't load | Malformed JSON | Validate JSON, check `schemaVersion` field |

## Resources

- [Installation Guide](https://docs.unlayer.com/builder/installation)
- [React Component](https://docs.unlayer.com/builder/react-component)
- [Vue Component](https://docs.unlayer.com/builder/vue-component)
- [Angular Component](https://docs.unlayer.com/builder/angular-component)
