---
name: tw-mantine
description: |
  Integrasi Tailwind CSS v4 dengan Mantine v8 untuk Next.js. 
  Gunakan skill ini ketika: 
  (1) Membuat komponen UI yang menggabungkan utility classes Tailwind dengan komponen Mantine,
  (2) Mengkonfigurasi project Next.js dengan Tailwind v4 dan Mantine v8,
  (3) Mengimplementasikan dark mode yang konsisten antara Tailwind dan Mantine,
  (4) Membuat custom theme atau styling untuk komponen Mantine menggunakan Tailwind classes,
  (5) Setup project dengan App Router atau Pages Router.
---

# Tailwind CSS v4 + Mantine v8 Integration

## Overview

Skill ini menyediakan panduan lengkap untuk mengintegrasikan Tailwind CSS v4 dengan Mantine v8 di Next.js. Kombinasi ini memungkinkan:
- **Tailwind**: Utility-first CSS untuk styling cepat dan konsisten
- **Mantine**: Komponen React feature-rich dengan accessibility built-in

## Quick Start

### 1. Install Dependencies

```bash
npm install @mantine/core @mantine/hooks @mantine/form @mantine/modals @mantine/notifications
npm install -D tailwindcss @tailwindcss/postcss
npm install tailwind-merge clsx
```

### 2. Setup PostCSS

Create `postcss.config.mjs`:

```javascript
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

### 3. Setup Global CSS

Untuk detail setup lengkap, lihat:
- **App Router**: [references/app-router-setup.md](references/app-router-setup.md)
- **Pages Router**: [references/pages-router-setup.md](references/pages-router-setup.md)

## Integration Patterns

### Pattern 1: classNames Prop (Recommended)

Gunakan `classNames` prop untuk menerapkan utility classes Tailwind ke bagian spesifik komponen Mantine:

```tsx
import { Button } from '@mantine/core';

function HybridButton() {
  return (
    <Button
      classNames={{
        root: 'hover:scale-105 transition-transform duration-200 shadow-lg',
        label: 'font-semibold tracking-wide',
      }}
    >
      Click Me
    </Button>
  );
}
```

### Pattern 2: style Prop

Gunakan untuk styling inline sederhana:

```tsx
<Button style={{ backgroundColor: 'var(--mantine-color-red-5)' }}>
  Red Button
</Button>
```

### Pattern 3: Global Theme Configuration

Konfigurasi classNames di theme untuk semua instance komponen:

```tsx
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  components: {
    Button: Button.extend({
      classNames: {
        root: 'shadow-md hover:shadow-lg transition-shadow',
      },
    }),
  },
});

function App() {
  return (
    <MantineProvider theme={theme}>
      {/* All buttons will have Tailwind shadows */}
    </MantineProvider>
  );
}
```

## Dark Mode Integration

Tailwind v4 dan Mantine v8 mendukung dark mode secara native. Implementasikan dengan:

### CSS Setup

```css
@import "tailwindcss";

/* Tailwind will automatically detect dark mode from prefers-color-scheme */
```

### Component Usage

```tsx
<div className="bg-white dark:bg-gray-800 rounded-lg p-6">
  <h3 className="text-gray-900 dark:text-white">Title</h3>
  <p className="text-gray-500 dark:text-gray-400">Description</p>
</div>
```

### Mantine Color Scheme

MantineProvider secara otomatis mengikuti sistem color scheme. Tidak perlu konfigurasi tambahan.

## Reusable Hybrid Components

Gunakan komponen template dari `assets/templates/components/`:

- **HybridButton**: Button dengan efek hover dan shadow Tailwind
- **HybridCard**: Card dengan layout flex dan responsive spacing
- **HybridModal**: Modal dengan styling custom menggunakan Tailwind
- **HybridTextInput**: Input dengan styling focus dan error states

## Common Selectors Reference

Setiap komponen Mantine memiliki selectors internal yang dapat di-styling:

| Component | Selectors |
|-----------|-----------|
| Button | `root`, `inner`, `label`, `section` |
| TextInput | `root`, `input`, `label`, `error`, `description` |
| Card | `root`, `section` |
| Modal | `root`, `header`, `body`, `overlay` |
| Select | `root`, `input`, `dropdown`, `options` |

Lihat [references/integration-patterns.md](references/integration-patterns.md) untuk daftar lengkap.

## Best Practices

### Do's
- Gunakan `classNames` untuk styling yang kompleks (hover, focus, transitions)
- Gunakan `style` prop untuk styling inline sederhana
- Definisikan classNames global di theme untuk konsistensi
- Gunakan `tailwind-merge` dan `clsx` untuk menggabungkan classes dinamis

### Don'ts
- Jangan gunakan `sx` prop (deprecated di Mantine 7+)
- Hindari styling yang bertabrakan antara Tailwind dan Mantine defaults
- Jangan override CSS variables Mantine kecuali diperlukan

## Troubleshooting

### Classes tidak diterapkan
- Pastikan Tailwind CSS diimport di global CSS
- Periksa spesifisitas selector CSS
- Gunakan `!important` hanya jika benar-benar diperlukan

### Style conflicts
- Mantine menggunakan CSS variables, prioritaskan utility Tailwind untuk override
- Gunakan `classNames` untuk targeting selector spesifik

## Resources

- [Tailwind v4 Guide](references/tailwind-v4-guide.md)
- [Mantine v8 Guide](references/mantine-v8-guide.md)
- [Integration Patterns](references/integration-patterns.md)
- [App Router Setup](references/app-router-setup.md)
- [Pages Router Setup](references/pages-router-setup.md)
