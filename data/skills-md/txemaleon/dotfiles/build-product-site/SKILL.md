---
name: build-product-site
description: "Coordina la creación o mejora de la home y las páginas de posicionamiento de un proyecto web: contexto y preguntas, arquitectura, copy, diseño y SEO/GEO mediante skills especialistas. Usar para una carta de presentación, web de producto, home con casos de uso, integraciones, comparativas o guías. No para cambios visuales aislados, desarrollo de funcionalidades del producto ni auditorías SEO generales."
license: "Adaptación del proceso de Page Foundry (MIT); ver LICENSE y references/sources.md."
metadata:
  version: 1.0.0
---

# Construir una web de producto

Dirige el trabajo desde lo que el visitante necesita entender hasta una página
comprobada. La home presenta el proyecto y orienta; cada página que la acompaña
resuelve una intención propia. Cada fase consume las decisiones y evidencias
de la anterior. Ejecuta las skills especialistas: enumerarlas no hace su trabajo.

## 1. Fijar el encargo y reutilizar lo que existe

- Identifica proyecto, repositorio, dominio, páginas/idiomas y resultado pedido:
  mapa/brief, copy, implementación o revisión. Respeta lo ya autorizado; si pidió
  construir, continúa hasta la implementación y su verificación local. Si pidió
  plan o textos, ese es el resultado y no habilita código o publicación.
- Lee instrucciones del proyecto, contexto de producto, decisiones de marca,
  rutas/contenidos existentes y evidencia del alcance. Usa fuentes canónicas,
  no toda la documentación por rutina. Comprueba versiones si el repo y la web
  publicada difieren; un candidato local no demuestra disponibilidad pública.
- Separa hechos verificados, información del propietario, hipótesis y huecos.
  Por claim material conserva fuente/fecha y estado: disponible, condicionado,
  roadmap o desconocido. El copy público refleja capacidades disponibles para
  el destinatario. No deduzcas clientes, resultados, precios o garantías.
- Mantén un único brief vivo: propósito, público/intención, propuesta, pruebas,
  límites, voz/marca, páginas incluidas y decisiones pendientes. Reutiliza su
  ubicación canónica, incluida `.agents/product-marketing.md` si ya existe.
  No clones el contexto en otro archivo porque una skill prefiera otro nombre.
  En trabajos breves basta el brief en conversación; persiste solo lo necesario
  para continuidad o lo requerido por el repositorio. No crees un informe aparte.

## 2. Preguntar solo lo que cambia el resultado

Antes de preguntar, marca cada dimensión como resuelta, inferible o pendiente:

| Dimensión | Decisión que debe permitir |
| --- | --- |
| Qué es y para quién | Categoría comprensible, público principal y situación de uso |
| Qué aporta | Resultado concreto, alternativa actual y diferencia demostrable |
| Qué debe creer el visitante | Objeciones y evidencia real que las responde |
| Qué puede hacer después | Acción principal y caminos para quien aún investiga |
| Qué define al proyecto | Voz, identidad, referencias y elementos a conservar |
| Qué páginas tienen sentido | Intenciones, idiomas, contenido existente y alcance |

Pregunta por los pendientes materiales en lotes cortos, normalmente 1–3.
Usa el mecanismo de preguntas del entorno y continúa con trabajo independiente.
No reabras respuestas recibidas ni pidas valores CSS. Si el encargo y contexto
resuelven estas decisiones, procede sin una entrevista o aprobación ritual.
Una preferencia inferible puede declararse y ajustarse; una capacidad, precio,
prueba o permiso no se inventa. Si un hueco cambia el posicionamiento o impide
una afirmación, espera la respuesta para esa parte o retira la afirmación.

## 3. Ejecutar especialistas con el mismo contrato

Resuelve nombres en el catálogo activo (acepta namespaces) y abre su `SKILL.md`.
Si no está enumerada, busca únicamente en las carpetas de skills del proyecto y
del usuario. No dependas de rutas de una máquina concreta ni releas el mismo
archivo en la sesión. Carga sus referencias solo cuando la tarea las necesite.

Entrega a cada especialista: encargo/idioma, brief vigente, fuentes, URLs y
archivos permitidos, decisiones de fases previas y resultado esperado. Aplica
su método a ese alcance. Las sugerencias de otras skills no amplían el trabajo
ni crean nuevos requisitos de autorización: prevalecen usuario/repositorio y
el contrato de esta ejecución. No impongas sus templates, cifras de ejemplo,
auditorías completas o creación de archivos cuando no correspondan.

| Momento | Skill | Resultado consumido después |
| --- | --- | --- |
| Resolver posicionamiento o una home nueva | `product-marketing` | Brief comprobado, público, diferencias, objeciones y pruebas |
| Definir varias páginas, navegación o la función de una nueva ruta | `site-architecture` | Mapa de páginas/intenciones y enlaces con el sitio existente |
| Planear descubrimiento y respuestas para buscadores | `seo-geo` | Consultas/preguntas, intención y requisitos SEO/GEO con fuentes actuales |
| Escribir cada página incluida | `copywriting` | Estructura argumentada, titulares, cuerpo, pruebas, CTA y metadatos |
| Revisar claridad y recorrido | `cro` | Correcciones concretas de argumento, jerarquía, objeciones y acción |
| Corregir copy genérico o artificial | `de-smell` | Texto específico que conserva hechos, voz y sentido |
| Implementar una página o dirección visual nueva | `frontend-design` | Composición y código fieles al brief, copy y sistema existente |
| Pulir detalles de la UI modificada | `make-interfaces-feel-better` | Ajustes focales de legibilidad, estados y composición |
| Comprobar páginas construidas | `agent-browser` y `seo-audit` | Evidencia visual/funcional y SEO acotada a las rutas afectadas |
| Solo si se ha pedido una familia de páginas a escala | `programmatic-seo` | Fuente de datos y valor único comprobable por página |

No cargues toda la tabla en cada petición. Una revisión de copy no requiere
diseño; una página hermana no obliga a rehacer la home. Usa `cro` sobre el
argumento antes de construir; revísalo de nuevo únicamente si el render cambia
su sentido, recorrido o prueba. Al usar `seo-geo`/`seo-audit`, aplica las
distinciones de [search-quality.md](references/search-quality.md).

La ejecución normal cabe en un agente. Los subagentes son opcionales, sujetos
a las instrucciones del entorno, no un requisito de calidad. Mantén una línea
por especialista realmente usado: **skill → decisión/resultado → dónde se
aplicó**. Un archivo leído o una lista de nombres no es un resultado ejecutado.
Si falta una dependencia necesaria, usa un equivalente disponible solo si
cubre su función y declara el cambio; si no, informa el hueco y continúa con
lo independiente. No simules su ejecución ni instales paquetes silenciosamente.

## 4. Hacer que las páginas formen un sitio

Lee [page-contracts.md](references/page-contracts.md) al crear el mapa o decidir
la estructura. Para cada página candidata define:

**URL existente/propuesta · intención y público · papel respecto a la home ·
promesa y evidencia · argumento/secciones · siguiente acción · enlaces ·
idioma/indexación/canonical propuestos · estado y razón de inclusión.**

Compara primero con el inventario: conservar, mejorar, integrar en una ruta
existente, crear o aplazar. Una keyword por sí sola no justifica otra página.
Mantén diferencias claras entre home, campaña, caso de uso, integración,
comparativa y guía. No metas todo en la navegación principal ni canonicalices
páginas distintas a la home para evitar que compitan. Cambios de rutas,
redirecciones, políticas de indexación o tracking requieren su alcance explícito.

Presenta el mapa y el argumento como propuesta concreta dentro del trabajo.
Continúa si el encargo ya autoriza ejecutarlos; pregunta cuando haya una decisión
material sin resolver. No construyas páginas adicionales sugeridas por el mapa
si el usuario solo pidió una. Conserva las otras como candidatas explicadas.

## 5. De estructura a copy y diseño

- Cada sección tiene un mensaje, un trabajo para el visitante y una prueba
  cuando afirma algo. Decide su orden por la intención y la dificultad de
  entender el producto, no por una secuencia fija hero/features/testimonios/FAQ.
- Da prioridad a mostrar la utilidad: contenido real o componentes reales del
  producto con un fixture seguro. Una ilustración puede explicar una idea, pero
  una maqueta de marketing no se presenta como captura del producto funcionando.
  Distingue datos ilustrativos de clientes, métricas o resultados reales.
- Estabiliza el argumento y el copy antes de desarrollar el diseño completo.
  Diseño y copy pueden ajustar longitud/énfasis entre sí; conserva claims,
  alcance y acciones. No cambies toda la marca para una página nueva ni pierdas
  identidad buscando evitar un cliché. No hay framework, estética o animación
  obligatorios: trabaja en el sistema real del repositorio.
- Reutiliza contexto y decisiones compartidas entre páginas. Mantén específico
  el contenido central de cada una; no repitas la home con un título distinto.

## 6. Comprobar y entregar el resultado pedido

En mapa/copy: contrasta cada claim con su fuente, comprueba que títulos y
secciones se entienden sin explicación del autor, que no hay intenciones
duplicadas y que los enlaces/acciones propuestos tienen destino y estado claro.

En implementación: ejecuta los checks proporcionados del repositorio y prueba
los comportamientos modificados. Inspecciona en navegador escritorio y móvil:
contenido real, legibilidad, desbordamientos, teclado, enlaces/CTA y estados
interactivos afectados. Comprueba metadata/canonical y contenido textual/JSON-LD
de las rutas modificadas en fuente o DOM, sin inferir ausencias de un extractor.
Agrupa la revisión y las correcciones; no repitas suites o pulido sin una razón.

Si no puede ejecutarse el navegador o falta acceso a una fuente, identifica lo
no comprobado. No sustituye la verificación renderizada un build correcto; un
score del agente tampoco acredita usabilidad, indexación, citas o conversión.
Entrega lo construido o el copy/mapa solicitado, skills efectivamente usadas,
checks y límites. Separa validación local de observación publicada.

Publicar, desplegar, modificar buscadores, contratar servicios o contactar a
terceros son acciones separadas sujetas a su autorización. No son requisitos
para entregar una preparación o implementación local. En Project Manager,
coordina y conserva el brief; la ejecución de producto pertenece a su repo/hilo.

Procedencia y dependencias: [sources.md](references/sources.md).
