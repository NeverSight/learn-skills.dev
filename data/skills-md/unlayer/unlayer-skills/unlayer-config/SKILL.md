---
name: unlayer-config
description: Configures the Unlayer editor — feature flags, appearance, theming, merge tags, design tags, display conditions, special links, HMAC security, file storage, image uploads, localization, custom fonts, validation.
---

# Configure the Editor

## Overview

Unlayer's behavior is controlled through `unlayer.init()` options and runtime methods. This skill covers features, appearance, dynamic content, security, and file storage.

**Where to find keys:**
- **Project ID** — Dashboard > Project > Settings
- **Project Secret** (for HMAC) — Dashboard > Project > Settings > API Keys
- **Cloud API Key** (for image/PDF export) — Dashboard > Project > Settings > API Keys

Dashboard: [console.unlayer.com](https://console.unlayer.com)

---

## Feature Flags

Control what's available in the editor:

```javascript
unlayer.init({
  features: {
    audit: true,             // Content validation
    preview: true,           // Preview button
    undoRedo: true,          // Undo/redo
    stockImages: true,       // Stock photo library
    userUploads: true,       // User upload tab
    preheaderText: true,     // Email preheader field
    textEditor: {
      spellChecker: true,
      tables: false,         // Tables inside text blocks
      cleanPaste: 'confirm', // true | false | 'basic' | 'confirm'
      emojis: true,
    },

    // Paid features:
    ai: true,                // AI text generation
    collaboration: false,    // Real-time collaboration
    sendTestEmail: false,    // Test email button
  },
});
```

See [references/feature-flags.md](references/feature-flags.md) for all flags (AI sub-options, image editor, color picker, etc.).

---

## Appearance & Theming

```javascript
unlayer.init({
  appearance: {
    theme: 'modern_dark',    // 'modern_light' | 'modern_dark' | 'classic_light' | 'classic_dark'
    panels: {
      tools: {
        dock: 'right',       // 'left' | 'right' (default: 'right')
        collapsible: true,
      },
    },
    actionBar: {
      placement: 'top',     // 'top' | 'bottom' | 'top_left' | 'top_right' | 'bottom_left' | 'bottom_right'
    },
  },
});

// Change at runtime:
unlayer.setAppearance({ theme: 'modern_dark' });
// Or just the theme:
unlayer.setTheme('modern_dark');
```

### Custom Fonts

```javascript
unlayer.init({
  fonts: {
    showDefaultFonts: true,
    customFonts: [{
      label: 'Poppins',
      value: "'Poppins', sans-serif",
      url: 'https://fonts.googleapis.com/css?family=Poppins:400,700',
      weights: [400, 700],  // or [{ label: 'Regular', value: 400 }, { label: 'Bold', value: 700 }]
    }],
  },
});
```

### Tab Configuration

```javascript
unlayer.init({
  tabs: {
    content: { enabled: true, position: 1 },
    blocks: { enabled: true, position: 2 },
    body: { enabled: true, position: 3 },
    images: { enabled: true, position: 4 },
    uploads: { enabled: true, position: 5 },
  },
});
```

---

## Merge Tags

Merge tags are placeholders replaced at send time (e.g., `{{first_name}}`). They use your template engine's syntax (Handlebars, Liquid, Jinja, etc.):

```javascript
unlayer.setMergeTags({
  first_name: {
    name: 'First Name',
    value: '{{first_name}}',        // Your template syntax
    sample: 'John',                  // Shown in editor preview
  },
  last_name: {
    name: 'Last Name',
    value: '{{last_name}}',
    sample: 'Doe',
  },
  company: {
    name: 'Company',                 // Nested group
    mergeTags: {
      name: { name: 'Company Name', value: '{{company.name}}', sample: 'Acme Inc' },
      logo: { name: 'Logo URL', value: '{{company.logo}}' },
    },
  },
  products: {
    name: 'Products',
    rules: {
      repeat: {
        name: 'Repeat for Each Product',
        before: '{{#each products}}', // Loop start — syntax depends on your template engine
        after: '{{/each}}',           // Loop end
        sample: true,                  // Show sample data in editor
      },
    },
    mergeTags: {
      name: { name: 'Product Name', value: '{{this.name}}' },
      price: { name: 'Price', value: '{{this.price}}' },
      image: { name: 'Image URL', value: '{{this.image}}' },
    },
  },
});

// Autocomplete trigger (optional)
unlayer.setMergeTagsConfig({ autocompleteTriggerChar: '{{', sort: true });
```

### Design Tags (Editor-Only Placeholders)

Design tags are replaced in the editor UI but NOT in exports — useful for showing personalized content to the template author:

```javascript
unlayer.setDesignTags({
  business_name: 'Acme Corp',
  current_user_name: 'Jane Smith',
});
unlayer.setDesignTagsConfig({ delimiter: ['{{', '}}'] });
```

### Display Conditions (Paid)

Wrap content in conditional blocks for your template engine:

```javascript
unlayer.setDisplayConditions([
  {
    type: 'segment',
    label: 'VIP Customers',
    description: 'Only shown to VIP segment',
    before: '{% if customer.vip %}',   // Your template engine syntax
    after: '{% endif %}',
  },
  {
    type: 'segment',
    label: 'New Subscribers',
    description: 'First 30 days only',
    before: '{% if subscriber.age_days < 30 %}',
    after: '{% endif %}',
  },
]);
```

### Special Links

Pre-defined links users can insert (unsubscribe, preferences, etc.):

```javascript
unlayer.setSpecialLinks({
  unsubscribe: {
    name: 'Unsubscribe',
    href: '{{unsubscribe_url}}',
    target: '_blank',
  },
  preferences: {
    name: 'Preferences',
    specialLinks: {
      email_prefs: { name: 'Email Preferences', href: '{{preferences_url}}' },
      profile: { name: 'Profile Settings', href: '{{profile_url}}' },
    },
  },
});
```

---

## HMAC Security

Prevents users from impersonating each other. Generate the HMAC signature **server-side** using your Project Secret (Dashboard > Project > Settings > API Keys):

**Node.js:**

```javascript
const crypto = require('crypto');
const signature = crypto
  .createHmac('sha256', 'YOUR_PROJECT_SECRET')  // From Dashboard
  .update(String(userId))
  .digest('hex');
```

**Python/Django:**

```python
import hmac, hashlib

signature = hmac.new(
    b'YOUR_PROJECT_SECRET',
    bytes(str(request.user.id), encoding='utf-8'),
    digestmod=hashlib.sha256
).hexdigest()
```

**Client-side** — pass the server-generated signature:

```javascript
unlayer.init({
  user: {
    id: userId,                       // Must match what you signed
    signature: signatureFromServer,    // HMAC from your backend
    name: 'John Doe',                 // Optional
    email: 'john@acme.com',          // Optional
  },
});
```

See [references/security.md](references/security.md) for Ruby and PHP examples.

---

## File Storage & Image Upload

### Custom Upload (Your Server)

```javascript
unlayer.registerCallback('image', (file, done) => {
  const data = new FormData();
  data.append('file', file.attachments[0]);

  fetch('/api/uploads', { method: 'POST', body: data })
    .then((r) => {
      if (!r.ok) throw new Error('Upload failed');
      return r.json();
    })
    .then((result) => done({ progress: 100, url: result.url }))
    .catch((err) => console.error('Upload error:', err));
});
```

**Your backend should return:**

```json
{ "url": "https://your-cdn.com/images/uploaded-file.png" }
```

### File Manager (Browse Uploaded Images)

Requires `user.id` in init — images are scoped per user:

```javascript
unlayer.init({
  user: { id: 123 },                  // Required for file manager
  features: { userUploads: { enabled: true, search: true } },
});

unlayer.registerProvider('userUploads', (params, done) => {
  // params: { page, perPage, searchText }
  fetch(`/api/images?userId=123&page=${params.page}&perPage=${params.perPage}`)
    .then((r) => r.json())
    .then((data) => {
      done(
        data.items.map((img) => ({
          id: img.id,                  // Required
          location: img.url,           // Required — the image URL
          width: img.width,            // Optional but recommended
          height: img.height,          // Optional but recommended
          contentType: img.contentType, // Optional: 'image/png'
          source: 'user',              // Required: must be 'user'
        })),
        { hasMore: data.hasMore, page: params.page, total: data.total }
      );
    });
});
```

**Your backend should return:**

```json
{
  "items": [
    { "id": "img_1", "url": "https://...", "width": 800, "height": 600, "contentType": "image/png" }
  ],
  "hasMore": true,
  "total": 42
}
```

See [references/file-storage.md](references/file-storage.md) for upload progress with XHR, image deletion, and Amazon S3 setup.

---

## Localization

```javascript
unlayer.init({
  locale: 'es-ES',
  textDirection: 'rtl',        // 'ltr' | 'rtl' | null
  translations: {
    es: { Save: 'Guardar', Cancel: 'Cancelar' },
  },
});
```

---

## Validation

```javascript
// Global validator — runs on all content
unlayer.setValidator(async ({ html, design, defaultErrors }) => {
  return [...defaultErrors]; // Return modified error list
});

// Per-tool validator
unlayer.setToolValidator('text', async ({ html, defaultErrors }) => {
  return defaultErrors;
});

// Run audit on demand
unlayer.audit((result) => {
  // result: { status: 'FAIL' | 'PASS', errors: [{ id, icon, severity, title, description }] }
  if (result.status === 'FAIL') {
    console.log('Issues found:', result.errors);
  }
});
```

---

## safeHtml (XSS Protection)

```javascript
unlayer.init({
  safeHtml: true,   // Sanitize HTML via DOMPurify

  // Or with custom options:
  safeHtml: {
    domPurifyOptions: {
      FORCE_BODY: true,
    },
  },

  // WRONG: safeHTML (capital HTML) is DEPRECATED — use safeHtml
});
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `safeHTML` (uppercase) | Use `safeHtml` (camelCase) — old casing deprecated |
| `features.blocks = false` hides tab | It disables blocks but NOT the tab — use `tabs` config |
| Deprecated `colorPicker.presets` | Use `colorPicker.colors` instead (string[] or ColorGroup[]) |
| Missing `user.id` for file manager | File Manager requires `user.id` in init |
| Project Secret exposed in frontend | **Never** put the secret in client code — generate HMAC server-side |
| Merge tag syntax mismatch | Match your template engine: `{{var}}` (Handlebars), `${var}` (JS), `{% %}` (Jinja) |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Merge tags don't appear | Check `setMergeTags()` is called after `editor:ready` or passed in `init()` |
| HMAC signature rejected | Ensure `user.id` matches exactly what you signed, and secret is correct |
| File manager shows empty | Check `user.id` is set, `userUploads.enabled = true`, provider returns correct format |
| Theme doesn't apply | Use `unlayer.setAppearance({ theme: 'modern_dark' })` or `unlayer.setTheme('modern_dark')` after init |

## Paid Features

| Feature | How to Enable |
|---------|---------------|
| Custom CSS/JS | `customCSS`, `customJS` in init |
| Display conditions | `setDisplayConditions()` |
| Style guide | `setStyleGuide()` |
| Export Image/PDF/ZIP | Cloud API key required |
| AI features | `features.ai` |
| Collaboration | `features.collaboration` |

## Resources

- [Appearance](https://docs.unlayer.com/builder/appearance)
- [Merge Tags](https://docs.unlayer.com/builder/dynamic-content/merge-tags)
- [Design Tags](https://docs.unlayer.com/builder/dynamic-content/design-tags)
- [Display Conditions](https://docs.unlayer.com/builder/dynamic-content/display-conditions)
- [Special Links](https://docs.unlayer.com/builder/special-links)
- [Security (HMAC)](https://docs.unlayer.com/builder/security)
- [File Storage](https://docs.unlayer.com/builder/file-storage)
- [File Manager](https://docs.unlayer.com/builder/file-manager)
- [Localization](https://docs.unlayer.com/builder/localization)
- [Color Management](https://docs.unlayer.com/builder/color-management)
