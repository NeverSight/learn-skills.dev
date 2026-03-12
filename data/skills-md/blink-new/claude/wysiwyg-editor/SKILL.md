---
name: wysiwyg-editor
description: Build production-grade WYSIWYG editors using Tiptap v3 with proper markdown-style formatting, instant rendering, and bullet/numbered list support
---

# WYSIWYG Rich Text Editor Skill

Build production-grade WYSIWYG editors using Tiptap v3 with proper markdown-style formatting, instant rendering, and bullet/numbered list support.

## When to Use

Use this skill when:
- Building rich text editors for emails, comments, or content
- Implementing WYSIWYG editing with toolbar controls
- Rendering user-generated HTML content safely
- Need proper bullet and numbered list styling (commonly missed!)

## Quick Start

### 1. Install Dependencies

```bash
bun add @tiptap/react @tiptap/starter-kit @tiptap/extension-link @tiptap/extension-placeholder @tiptap/pm dompurify
bun add -D @types/dompurify
```

### 2. Copy Components

Copy the component files from `assets/components/` to your project:
- `rich-text-editor.tsx` → Full-featured editor with headings, code blocks
- `simple-editor.tsx` → Simplified editor for emails/comments
- `html-content.tsx` → Safe HTML rendering component

### 3. Add Required CSS

Add these styles to your `globals.css` or the editor's class. **This is critical for proper list rendering**:

```css
/* CRITICAL: List styling - often missed, causes bullets/numbers to not appear */
[&_ul]:list-disc [&_ul]:pl-6 
[&_ol]:list-decimal [&_ol]:pl-6

/* Tight spacing for prose content */
prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0
```

## Architecture

### Data Flow

```
User Input → Tiptap Editor → getHTML() → Store as HTML in DB
                                              ↓
Display ← dangerouslySetInnerHTML ← DOMPurify.sanitize() ← HTML from DB
```

### Key Principle: HTML Storage, Not Markdown

- Content is stored and transmitted as **HTML**
- No markdown conversion needed
- HTML is sanitized with DOMPurify before display
- This provides instant rendering without conversion lag

## Implementation Details

### Editor Configuration

```tsx
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";

const editor = useEditor({
  immediatelyRender: false, // Required for SSR/Next.js
  extensions: [
    StarterKit.configure({
      // For simplified editors, disable unused features:
      heading: false,
      codeBlock: false,
      blockquote: false,
      horizontalRule: false,
      // For full editors, configure heading levels:
      // heading: { levels: [1, 2, 3] },
    }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: "text-primary underline underline-offset-2",
      },
    }),
    Placeholder.configure({
      placeholder: "Write your message...",
      emptyEditorClass: "before:content-[attr(data-placeholder)] before:text-muted-foreground before:absolute before:opacity-50 before:pointer-events-none",
    }),
  ],
  content: value,
  editable: true,
  editorProps: {
    attributes: {
      // CRITICAL: These classes enable proper list rendering
      class: cn(
        "prose prose-sm dark:prose-invert max-w-none focus:outline-none min-h-[120px] px-3 py-2",
        "prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0",
        "[&_ul]:list-disc [&_ul]:pl-6 [&_ol]:list-decimal [&_ol]:pl-6"
      ),
    },
  },
  onUpdate: ({ editor }) => {
    const html = editor.getHTML();
    // Handle empty content
    if (html === "<p></p>") {
      onChange("");
    } else {
      onChange(html);
    }
  },
});
```

### Toolbar Commands

```tsx
// Bold
editor.chain().focus().toggleBold().run()
editor.isActive("bold")

// Italic
editor.chain().focus().toggleItalic().run()
editor.isActive("italic")

// Bullet List
editor.chain().focus().toggleBulletList().run()
editor.isActive("bulletList")

// Numbered List
editor.chain().focus().toggleOrderedList().run()
editor.isActive("orderedList")

// Headings
editor.chain().focus().toggleHeading({ level: 1 }).run()
editor.isActive("heading", { level: 1 })

// Links
editor.chain().focus().setLink({ href: url }).run()
editor.chain().focus().unsetLink().run()
editor.isActive("link")

// Undo/Redo
editor.chain().focus().undo().run()
editor.chain().focus().redo().run()
editor.can().undo()
editor.can().redo()
```

### Syncing External Value Changes

```tsx
useEffect(() => {
  if (editor && value !== editor.getHTML()) {
    const currentHtml = editor.getHTML();
    const normalizedValue = value || "<p></p>";
    if (normalizedValue !== currentHtml && value !== "") {
      editor.commands.setContent(value);
    } else if (value === "" && currentHtml !== "<p></p>") {
      editor.commands.setContent("");
    }
  }
}, [editor, value]);
```

## Safe HTML Rendering

### DOMPurify Configuration

```tsx
import DOMPurify from "dompurify";
import { useMemo } from "react";

const sanitizedHtml = useMemo(() => {
  if (!htmlContent) return null;
  return DOMPurify.sanitize(htmlContent, {
    ALLOWED_TAGS: [
      "p", "br", "strong", "b", "em", "i", "u", "s", "a",
      "ul", "ol", "li", "blockquote", "pre", "code", "span", "div",
      "h1", "h2", "h3"
    ],
    ALLOWED_ATTR: ["href", "target", "rel", "class"],
    ADD_ATTR: ["target"],
  });
}, [htmlContent]);
```

### HTML Content Component

```tsx
function HtmlContent({ html, className }: { html: string; className?: string }) {
  const sanitizedHtml = useMemo(() => {
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ["p", "br", "strong", "b", "em", "i", "u", "s", "a", "ul", "ol", "li", "blockquote", "pre", "code", "span", "div"],
      ALLOWED_ATTR: ["href", "target", "rel", "class"],
    });
  }, [html]);

  // Check for actual content
  const hasContent = sanitizedHtml.replace(/<[^>]*>/g, "").trim() !== "";

  if (!hasContent) {
    return <span className="italic opacity-70">No content</span>;
  }

  return (
    <div
      className={cn(
        "prose prose-sm dark:prose-invert max-w-none",
        "prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0",
        "[&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5",
        "prose-a:underline prose-a:underline-offset-2",
        className
      )}
      dangerouslySetInnerHTML={{ __html: sanitizedHtml }}
    />
  );
}
```

## Critical CSS for Lists

**This is the most commonly missed part!** Without these styles, bullet points and numbered lists won't display properly:

```css
/* In the editor's editorProps.attributes.class */
[&_ul]:list-disc [&_ul]:pl-6    /* Bullet points with left padding */
[&_ol]:list-decimal [&_ol]:pl-6  /* Numbers with left padding */

/* For rendered content */
[&_ul]:list-disc [&_ul]:pl-5
[&_ol]:list-decimal [&_ol]:pl-5

/* Tight vertical spacing */
prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0
```

### Why This Matters

Tailwind's `@tailwindcss/typography` (prose classes) provides default styling, but:
1. Lists may not show bullets/numbers without explicit `list-disc`/`list-decimal`
2. Left padding (`pl-5` or `pl-6`) is required for list markers to be visible
3. Without `prose-li:my-0`, list items have excessive vertical spacing

## Complete Component Examples

### Simple Email Editor

See `assets/components/simple-editor.tsx`:
- Bold, Italic
- Bullet and Numbered lists
- Links
- Placeholder text
- Clean minimal toolbar

### Full Rich Text Editor

See `assets/components/rich-text-editor.tsx`:
- All simple editor features
- H1, H2, H3 headings
- Code blocks
- Blockquotes
- Undo/Redo

### HTML Content Display

See `assets/components/html-content.tsx`:
- Safe HTML rendering with DOMPurify
- Proper list styling
- Empty content handling
- Dark mode support

## Usage Example

```tsx
"use client";

import { useState } from "react";
import { SimpleEditor } from "@/components/ui/simple-editor";
import { HtmlContent } from "@/components/ui/html-content";

export function EmailComposer() {
  const [content, setContent] = useState("");

  return (
    <div>
      <SimpleEditor
        value={content}
        onChange={setContent}
        placeholder="Write your email..."
      />
      
      {/* Preview */}
      <div className="mt-4 p-4 border rounded-md">
        <h3 className="text-sm font-medium mb-2">Preview:</h3>
        <HtmlContent html={content} />
      </div>
    </div>
  );
}
```

## Troubleshooting

### Lists Not Showing Bullets/Numbers

Add these classes to the editor content area:
```css
[&_ul]:list-disc [&_ul]:pl-6 [&_ol]:list-decimal [&_ol]:pl-6
```

### Editor Flashing on Initial Render (SSR)

Set `immediatelyRender: false` in `useEditor` options.

### External Value Not Syncing

Implement the `useEffect` sync pattern shown above. Compare with `editor.getHTML()` to avoid infinite loops.

### Empty Paragraph on Clear

Check for `<p></p>` in the `onUpdate` handler and return empty string instead.

## File Structure

```
src/
├── components/
│   └── ui/
│       ├── simple-editor.tsx    # Email-style editor
│       ├── rich-text-editor.tsx # Full-featured editor
│       └── html-content.tsx     # Safe HTML display
└── app/
    └── globals.css              # Ensure prose classes available
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| @tiptap/react | ^3.x | React integration |
| @tiptap/starter-kit | ^3.x | Core extensions bundle |
| @tiptap/extension-link | ^3.x | Hyperlink support |
| @tiptap/extension-placeholder | ^3.x | Placeholder text |
| @tiptap/pm | ^3.x | ProseMirror dependencies |
| dompurify | ^3.x | HTML sanitization |
| @tailwindcss/typography | * | Prose classes (usually bundled with Tailwind v4) |
