---
name: landing-page-mastery
description: >
  Sistema experto para crear y optimizar landing pages de alta conversión para productos digitales.
  Úsala para crear páginas desde cero (SaaS, cursos, ebooks, newsletters, Micro-SaaS),
  auditar páginas existentes para mejorar conversión, o generar copy persuasivo (PAS, AIDA).
  Incluye estructuras, copy, diseño, CTAs, prueba social y optimización técnica.
---

# Landing Page Mastery

Sistema experto para la creación y optimización de landing pages de alta conversión.

> **IMPORTANTE**: Todo el output generado por esta skill debe ser estrictamente en **ESPAÑOL**, independientemente del idioma de los archivos de referencia.

## Selección de Flujo de Trabajo

- **¿Crear desde cero?** → Sigue el "Flujo de Creación"
- **¿Auditar página existente?** → Sigue el "Flujo de Auditoría"

---

## Flujo de Creación

### Paso 1: Descubrimiento (Requerido)

Antes de escribir código o copy, recopila esta información del usuario:

```
CONTEXTO DEL PRODUCTO:
- Tipo de producto: [SaaS/Curso/Ebook/Newsletter/Coaching/Herramienta]
- Precio: [Gratis/Bajo/Medio/Alto/Enterprise]
- Público objetivo: [¿Quién exactamente?]
- Problema principal: [Una frase]
- Diferenciador clave: [¿Por qué tú vs alternativas?]

CONTEXTO DE MARCA:
- Tono: [Profesional/Casual/Divertido/Autoritario]
- Estilo: [Moderno-pulido/Humano-auténtico/Híbrido]
- Colores de marca: [Si existen]
```

### Paso 2: Selección de Estructura

Basado en el tipo de producto, selecciona la estructura adecuada de `references/structures.md`:

| Tipo de Producto | Estructura Recomendada |
|------------------|------------------------|
| SaaS/Herramienta | Longitud completa (12-14 secciones) |
| Curso/Coaching | Basada en historia (10-12 secciones) |
| Ebook/Lead Magnet| Formato corto (6-8 secciones) |
| Newsletter | Ultra-corta (4-5 secciones) |

### Paso 3: Redacción del Copy (Primero)

Utiliza los frameworks de copy de `references/copywriting.md`:

1.  **Titular Hero** → Usa la Fórmula de Resultado Específico
2.  **Sección de Problema** → Usa PAS (Problema-Agitación-Solución)
3.  **Características** → Mapeo Beneficio > Característica
4.  **Testimonios** → Usa el formato STAR
5.  **Texto de CTA** → Usa verbos de acción personalizados

### Paso 4: Diseño y Construcción

Sigue las guías de diseño de `references/design.md`:

1.  Selecciona paleta de colores basada en psicología del producto
2.  Elige tipografía (evita fuentes genéricas)
3.  Implementa diseño responsive mobile-first
4.  Añade micro-interacciones para engagement
5.  Optimiza para tiempo de carga < 2 segundos

### Paso 5: Optimización de Conversión

Aplica elementos de conversión de `references/conversion-elements.md`:

-   Sticky CTA (móvil: barra inferior fija)
-   Indicadores de confianza cerca de los CTAs
-   Manejo de objeciones bajo los botones
-   Reducción de campos en formularios (de 11 a 4 → +120% conversión)

---

## Flujo de Auditoría

### Paso 1: Recopilar Datos

Solicita al usuario:
-   URL o captura de pantalla de la página actual
-   Tasa de conversión actual (si se conoce)
-   Fuente de tráfico (ads/orgánico/social)
-   Objetivo principal de conversión

### Paso 2: Ejecutar Auditoría Sistemática

Usa el checklist de `references/audit-checklist.md`. Puntúa cada categoría:

| Categoría | Puntos Max |
|-----------|------------|
| Sección Hero | 20 |
| Propuesta de Valor | 15 |
| Prueba Social | 15 |
| Optimización CTA | 15 |
| Calidad del Copy | 15 |
| Diseño y UX | 10 |
| Rendimiento Técnico | 10 |

### Paso 3: Priorizar Mejoras

Categoriza los problemas por impacto:

-   🔴 **Crítico**: Problemas que causan >10% caída de conversión
-   🟡 **Alto**: Problemas que causan 5-10% caída de conversión
-   🟢 **Medio**: Problemas que causan <5% caída de conversión

### Paso 4: Entregar Recomendaciones

```markdown
## Puntuación de Auditoría: [X]/100

### Problemas Críticos
1. [Problema] → [Solución] → [Impacto Estimado]

### Prioridad Alta
1. [Problema] → [Solución] → [Impacto Estimado]

### Victorias Rápidas (Quick Wins)
1. [Problema] → [Solución] → [Impacto Estimado]
```

---

## Benchmarks Clave (2026)

| Métrica | Promedio | Bueno | Excelente |
|---------|----------|-------|-----------|
| CVR General | 6.6% | 10% | 15%+ |
| CVR SaaS | 3.8% | 7% | 10%+ |
| CVR Eventos | 12.3% | 18% | 25%+ |
| Tiempo de Carga | 3s | 2s | <1s |
| Tasa de Rebote | 50% | 35% | <25% |

---

## Anti-Patrones (Nunca Hacer)

1.  ❌ Titulares genéricos ("Bienvenido al Futuro")
2.  ❌ Múltiples enlaces de navegación (mata 15% de conversiones)
3.  ❌ Fotos de stock de gente genérica
4.  ❌ "Enviar" como texto de CTA
5.  ❌ Formularios con >4 campos inicialmente
6.  ❌ Sin prueba social "above the fold" (parte visible sin scroll)
7.  ❌ Propuestas de valor vagas ("Hacemos las cosas mejor")
8.  ❌ Testimonios anónimos ("¡Genial! - J.")
9.  ❌ Degradados púrpuras sobre blanco (estilo "AI-slop" genérico)
10. ❌ Falta de Sticky CTA en móvil

---

## Archivos de Referencia

-   `references/structures.md` - Estructuras de página por tipo de producto
-   `references/copywriting.md` - Frameworks y fórmulas de copy
-   `references/design.md` - Guías de diseño visual
-   `references/audit-checklist.md` - Checklist de auditoría de 100 puntos
-   `references/conversion-elements.md` - CTAs, formularios, pricing
-   `references/sections-catalog.md` - Catálogo de todas las secciones
