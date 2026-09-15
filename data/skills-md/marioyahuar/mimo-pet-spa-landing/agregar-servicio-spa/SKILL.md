---
name: agregar-servicio-spa
description: Usar cuando el usuario pida agregar, crear o registrar un nuevo servicio/tratamiento de spa para mascotas en la landing page de Mimo Pet Spa, para que el servicio aparezca tanto en la sección "Servicios" de la home como en el flujo de reserva de citas.
---

## Objetivo

Incorporar un nuevo servicio de spa para que se visualice en dos lugares:

1. La sección "Servicios" de la home (`src/components/Services.jsx`).
2. El paso "Elige el ritual" del wizard de reserva (`src/components/booking/ReservarCita.jsx`).

## Dónde vive el contenido

Todo el copy de servicios está centralizado en `src/data/content.js`, en **dos arrays distintos** que deben mantenerse sincronizados por el campo `title` (se usa como clave para relacionar el servicio elegido en la reserva con su precio/duración):

- `services.items` → alimenta las tarjetas de la sección "Servicios" (descripción larga + tags).
- `booking.services` → alimenta la lista seleccionable del paso 0 del wizard de reserva (versión resumida).

Ningún componente tiene los servicios hardcodeados; ambos leen de `content.js`, así que basta con editar ese archivo.

## Pasos

1. OBLIGATORIO: Preguntar precio y duración si no se indicó. Reunir del usuario (o inferir razonablemente si no lo especifica): nombre del servicio, precio ("Desde $XX"), duración, breve descripción de marketing, y si debe destacarse como servicio estrella (`featured: true` + `badge: 'Más Solicitado'` o similar).
2. Elegir un icono de Material Symbols acorde (el proyecto usa `material-symbols-outlined` vía el componente `Icon`, ver `src/components/ui/Icon.jsx`). Reutilizar nombres ya usados cuando aplique (`bath`, `bathtub`, `content_cut`, `spa`, `healing`, `air`, `dentistry`, etc.) o cualquier nombre válido de https://fonts.google.com/icons.
3. Agregar un objeto a `services.items` con la forma exacta de los existentes:
   ```js
   {
     icon: 'nombre_icono',
     iconWrap: 'bg-secondary-container/40 text-secondary', // alternar tono secondary/primary como los demás
     title: 'Nombre del servicio',
     description: 'Copy cálido y detallado, tono spa/bienestar sin estrés.',
     tags: [
       { label: 'Desde $XX', className: 'bg-surface-container text-on-surface' },
       { label: 'NN min', className: 'bg-surface-container text-on-surface-variant' },
       { label: 'Tag diferenciador', className: 'bg-secondary-fixed/50 text-secondary' },
     ],
     featured: false,
   }
   ```
4. Agregar el objeto correspondiente a `booking.services`, con el **mismo `title` exacto** (idéntico carácter por carácter) que el usado en `services.items`:
   ```js
   {
     icon: 'nombre_icono',
     title: 'Nombre del servicio', // debe coincidir con services.items
     price: 'Desde $XX',
     duration: 'NN min',
     iconBg: 'bg-secondary-container',
     iconColor: 'text-secondary',
   }
   ```
5. Verificar que el `title` sea idéntico en ambos arrays: `ReservarCita.jsx` hace `booking.services.find((s) => s.title === state.serviceTitle)` para mostrar precio/resumen, y un mismatch rompe ese cruce silenciosamente.
6. Insertar el nuevo servicio **al final** de ambos arrays salvo que el usuario pida un orden específico. `emptyState()` en `ReservarCita.jsx` selecciona por defecto `booking.services[1]`; insertar al final evita cambiar sin querer cuál es el servicio preseleccionado al abrir el formulario.
7. Si el usuario pide cambiar cuál es el servicio destacado/preseleccionado, es una decisión explícita aparte — no reordenar ni tocar `emptyState()` por iniciativa propia.
8. Tras editar, si es posible, levantar `npm run dev` y revisar visualmente que la tarjeta aparece en "Servicios" y la opción aparece en el paso 1 de "Reservar Cita".

## Notas de estilo

- Descripciones en español, tono cálido y premium, coherente con los demás servicios (sensorial, sin estrés, ingredientes orgánicos/naturales).
- Precio con formato `"Desde $XX"`.
- Duración como `"NN min"` o `"NN-NN min"`.
- No tocar `addOns` / `booking.addOns` salvo que el usuario lo pida explícitamente: son tratamientos complementarios (add-ons), no servicios principales, y viven en una sección/paso distinto.
