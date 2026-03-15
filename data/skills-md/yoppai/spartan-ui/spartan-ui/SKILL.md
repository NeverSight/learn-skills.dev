---
name: spartan-ui
description: Guía y herramientas para integrar Spartan UI en proyectos Angular. Úsalo cuando el usuario necesite instalar Spartan UI, configurar temas, usar tipografía o añadir componentes basados en brain y helm. Asegúrate de invocar esta skill siempre que se mencione el desarrollo con Spartan UI en Angular.
---

# Spartan UI Skill

Esta skill proporciona instrucciones precisas y comandos para trabajar con Spartan UI en proyectos Angular.

## Introducción: ¿Cómo funciona?

Spartan UI utiliza una arquitectura de dos capas para ofrecer accesibilidad mantenida y control total sobre el estilo:

- **`spartan/ui/brain`**: Primitivas de UI accesibles y sin estilo instaladas vía npm. Manejan atributos ARIA, navegación por teclado y gestión de foco. Se instalan como dependencias regulares.
- **`spartan/ui/helm`**: Componentes con estilos inspirados en shadcn, construidos con clases de Tailwind CSS. El código se copia directamente a tu proyecto, permitiendo personalización total sin luchar contra una API de temas.

*Opcional*: **`spartan/stack`** proporciona una configuración full-stack con AnalogJs para desarrollo tipo sa-safe (Supabase, Angular, tRPC, Tailwind, AnalogJs, Nx, y Drizzle).

## Instalación y Configuración Inicial

### Requisitos Previos

- **Tailwind CSS**: Instalado y configurado en el proyecto Angular.
- **Versión Recomendada**: Tailwind CSS v4. Algunas funciones pueden no funcionar correctamente en v3.
- **Angular CDK**: Obligatorio para overlays y accesibilidad (`pnpm add @angular/cdk`).

### Inicio Rápido (Recomendado)

```bash
# 1. Instalar la CLI como dependencia de desarrollo
pnpm add -D @spartan-ng/cli
# O: npm i -D @spartan-ng/cli | yarn add -D @spartan-ng/cli | bun add -D @spartan-ng/cli

# 2. Inicializar Spartan CLI
ng g @spartan-ng/cli:init # O npx nx g @spartan-ng/cli:init

# 3. Configurar el tema
ng g @spartan-ng/cli:ui-theme
```

### Configuración Manual

1. **Instalar dependencias**: `pnpm add @spartan-ng/brain @angular/cdk`.
2. **Configurar Capas CSS (Tailwind v4)**: Añade en `styles.css`:

```css
@layer theme, base, components, utilities;
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";
```

1. **Importar Preset**: `@import "@spartan-ng/brain/hlm-tailwind-preset.css";` (incluye `tw-animate-css` y estilos de overlay).
2. **Añadir Variables de Tema**: Usa el generador o copia las variables OKLCH manualmente en `:root` y `.dark`.

## CLI y components.json

### Comandos de la CLI

- `ng g @spartan-ng/cli:init`: Configura el proyecto.
- `ng g @spartan-ng/cli:ui-theme`: Genera la configuración del tema (aplicación, punto de entrada de estilos, tema y radio de borde).
- `ng g @spartan-ng/cli:ui [nombre]`: Añade componentes (instala `brain` y copia `helm`).
- `ng g @spartan-ng/cli:healthcheck`: Detecta y arregla automáticamente APIs obsoletas o conflictos.
- `ng g @spartan-ng/cli:migrate-helm-libraries`: Actualiza todos los componentes Helm locales (¡Cuidado: sobreescribe cambios!).

### Archivo components.json

Se genera al añadir el primer componente. Campos:

- `componentsPath`: Ruta base para generar los componentes.
- `importAlias`: Path de importación (ej. `@spartan-ng/helm`).
- `buildable` (Nx): Si la librería es buildable.
- `generateAs` (Nx): `library` o `entrypoint`.

## Theming y Diseño

### Convención de Colores Semánticos

Spartan una un sistema de pares `background` / `foreground`:

- **Backgrounds**: `bg-primary`, `bg-secondary`, `bg-destructive`, `bg-muted`, `bg-accent`, `bg-popover`, `bg-card`.
- **Foregrounds**: `text-primary-foreground`, etc. (para texto sobre el color de fondo).

### Uso de OKLCH

Las variables se definen usando OKLCH sin la función de espacio de color:

```css
:root {
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
}
```

### Colores Personalizados

Añade variables en `:root` / `.dark` y regístralas en Tailwind:

```css
@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

## Dark Mode

Para una implementación completa se requiere:

- Persistencia con `localStorage`.
- Respeto al esquema del sistema.
- Prevención de "flash" en SSR.
- Uso de Angular Service con Signals.

## Tipografía

Instala las recetas de tipografía con:

```bash
ng g @spartan-ng/cli:ui typography
```

Usa las constantes de `@spartan-ng/helm/typography`: `hlmH1`, `hlmH2`, `hlmH3`, `hlmH4`, `hlmP`, `hlmBlockquote`, `hlmUl`, `hlmCode`, `hlmLead`, `hlmLarge`, `hlmSmall`, `hlmMuted`.

## Mantenimiento y Ciclo de Vida

### Soporte de Versiones

Spartan soporta las **dos últimas versiones mayores de Angular**. Al salir una nueva (v22), se añade soporte para v22 y v21, soltando v20.

### Flujo de Actualización Recomendado

1. Revisar **Changelog**.
2. Actualizar paquetes npm: `pnpm update @spartan-ng/brain @spartan-ng/cli`
   - O: `npm update`, `yarn upgrade` o `bun update` con los mismos paquetes.
3. Ejecutar **Health Check**: `ng g @spartan-ng/cli:healthcheck`.
4. Actualizar **Helm** manualmente (recomendado para conservar personalizaciones) o vía `migrate-helm-libraries`.
5. Verificar con tests E2E.

## Guías de Formularios

Para una integración profunda con la gestión de estados de Angular:

- [Formularios Reactivos](references/forms/reactive-forms.md)

## Referencias de Componentes

Para obtener detalles específicos sobre cómo usar componentes individuales, consulta las siguientes guías detalladas:

- [Accordion](references/components/accordion.md)
- [Alert](references/components/alert.md)
- [Alert Dialog](references/components/alert-dialog.md)
- [Aspect Ratio](references/components/aspect-ratio.md)
- [Autocomplete](references/components/autocomplete.md)
- [Avatar](references/components/avatar.md)
- [Badge](references/components/badge.md)
- [Breadcrumb](references/components/breadcrumb.md)
- [Button](references/components/button.md)
- [Button Group](references/components/button-group.md)
- [Calendar](references/components/calendar.md)
- [Card](references/components/card.md)
- [Carousel](references/components/carousel.md)
- [Checkbox](references/components/checkbox.md)
- [Collapsible](references/components/collapsible.md)
- [Combobox](references/components/combobox.md)
- [Command](references/components/command.md)
- [Context Menu](references/components/context-menu.md)
- [Data Table](references/components/data-table.md)
- [Date Picker](references/components/date-picker.md)
- [Dialog](references/components/dialog.md)
- [Dropdown Menu](references/components/dropdown-menu.md)
- [Empty](references/components/empty.md)
- [Field](references/components/field.md)
- [Form Field](references/components/form-field.md)
- [Hover Card](references/components/hover-card.md)
- [Icon](references/components/icon.md)
- [Input](references/components/input.md)
- [Input Group](references/components/input-group.md)
- [Input OTP](references/components/input-otp.md)
- [Item](references/components/item.md)
- [KBD](references/components/kbd.md)
- [Label](references/components/label.md)
- [Menubar](references/components/menubar.md)
- [Native Select](references/components/native-select.md)
- [Navigation Menu](references/components/navigation-menu.md)
- [Pagination](references/components/pagination.md)
- [Popover](references/components/popover.md)
- [Progress](references/components/progress.md)
- [Radio Group](references/components/radio-group.md)
- [Resizable](references/components/resizable.md)
- [Scroll Area](references/components/scroll-area.md)
- [Select](references/components/select.md)
- [Separator](references/components/separator.md)
- [Sheet](references/components/sheet.md)
- [Sidebar](references/components/sidebar.md)
- [Skeleton](references/components/skeleton.md)
- [Slider](references/components/slider.md)
- [Sonner](references/components/sonner.md)
- [Spinner](references/components/spinner.md)
- [Switch](references/components/switch.md)
- [Table](references/components/table.md)
- [Tabs](references/components/tabs.md)
- [Textarea](references/components/textarea.md)
- [Toggle](references/components/toggle.md)
- [Toggle Group](references/components/toggle-group.md)
- [Tooltip](references/components/tooltip.md)

## FAQ de bolsillo

1. **¿Brain vs Helm?**: Brain es la lógica (npm), Helm es el estilo (código en tu repo). Esta combinación permite mantener la accesibilidad sin sacrificar el control total del estilo.
2. **¿Es obligatorio spartan/stack?**: No. Puedes usar `spartan/ui` de forma independiente en cualquier proyecto Angular con Tailwind CSS.
3. **¿Personalización?**: Edita directamente los archivos en la carpeta Helm generada. Son tuyos desde el momento en que se copian.
4. **¿Tailwind v4?**: Recomendado para mejor soporte de capas y variables CSS modernas (OKLCH).
5. **¿Nx o Angular CLI?**: Spartan CLI es compatible con ambos, ajustando automáticamente la configuración del proyecto.
