---
name: dashboard-3d
description: Crea un dashboard 3D interactivo de un negocio (una maqueta isométrica en la que haces clic en cada zona y ves sus números) a partir de sus datos (Excel, CSV o datos pegados) o de una entrevista. Se actualiza al guardar el CSV. Úsala cuando alguien pida "un dashboard 3D", "mi negocio en 3D", "un tablero 3D", "un tablero de mi empresa", "un dashboard de mi empresa", "convierte mis datos en un mundo 3D" o quiera adaptar uno de los ejemplos a su negocio.
argument-hint: "[archivo de datos o descripción del negocio]"
---

# Dashboard 3D

Convierte un negocio en una maqueta 3D clicable conectada a un CSV. El dashboard (cámara, tarjetas, paneles, lectura del CSV) ya está hecho en `plantilla/`; tu trabajo es **el mundo**: las zonas, sus números y sus piezas 3D.

`DIR_SKILL` es la carpeta donde está este `SKILL.md`. De ahí salen `scripts/`, `ejemplos/` y `referencias/`.

## 1. Preparar el proyecto

- Si la carpeta actual (o una subcarpeta como `my-dashboard/`) ya tiene `src/mundo.ts`, es un dashboard existente: sigue la sección **Ajustar un dashboard existente** de abajo.
- Si no, créalo sin pedir que clone ni instale nada:
  ```bash
  node "DIR_SKILL/scripts/crear.mjs" my-dashboard --ejemplo tienda
  ```
  Usa otro nombre si `my-dashboard` ya existe. Arranca con un ejemplo que funciona y luego lo reemplazas. `--ejemplo tostadora` encaja mejor con fabricación.

Si falta Node.js 20 o más reciente, dilo y para.

## Ajustar un dashboard existente

No repitas la entrevista. Identifica qué quiere cambiar y toca solo eso:

| Pide | Qué hacer |
| --- | --- |
| Colores, tipografías, logo, "usa mi marca" | `referencias/marca.md` |
| Cuándo una zona pasa a atención o parada | Filas `<zona>_regla` en `datos/planta.csv` (`referencias/csv.md`) |
| Datos nuevos o un archivo actualizado | `referencias/importar.md`; conserva las mismas claves, reglas y umbrales |
| Una zona, una tarjeta o una pieza 3D | Pasos 3 y 4, solo para esa parte |

Antes de sobrescribir `datos/planta.csv`, cópialo a `datos/ejemplos/`. Si el proyecto no tiene `marca.json`, se creó con una versión anterior: cambia los colores en `src/piezas/tema.ts` y dilo. Al terminar haz `npm run validar` y `npm run build`, y mira el resultado en el navegador.

## 2. Entender el negocio

**Si te pasaron datos** (al invocarte o durante la conversación), léelos primero siguiendo `referencias/importar.md` y propón a partir de ellos. No preguntes lo que los datos ya dicen.

**Pregunta solo lo que siga sin saberse**, en un único mensaje corto si son varias cosas, con ejemplos para que respondan fácil:

1. Qué hace el negocio, en dos líneas.
2. Por qué zonas pasa el trabajo, de principio a fin (de 3 a 6 zonas). Ejemplo: recepción → tostado → empaque → almacén.
3. En cada zona, qué te dice que un día va bien o mal.
4. Qué harías al ver cambiar ese número. Si no harías nada, ese número no va.
5. Qué tiene que ver alguien de fuera en 5 segundos (los 3–5 indicadores de arriba).

La 4 no se deduce de los datos: pregúntala siempre. Luego propón como máximo **un número principal por zona** y **cinco indicadores**, cada uno con la decisión que ayuda a tomar. Espera su visto bueno. Criterio completo en `referencias/criterio.md`.

Después pregunta cuándo cada zona pasa a `atención` o `parada`: esos umbrales serán reglas automáticas.

## 3. El archivo

Escribe en `datos/planta.csv` los datos del negocio con el formato de `referencias/csv.md`: columnas `clave,valor,unidad,nota`, claves con el prefijo de su zona (`reparto_pedidos_en_ruta`) y una fila `<zona>_estado` por zona. Cada umbral que te den va como fila `<zona>_regla` (`referencias/csv.md`), para que la zona cambie sola.

No dejes filas que el dashboard no use: `npm run validar` las lista como aviso.

Usa las cifras reales tal como vienen. Si falta alguna, pon un valor plausible y dile exactamente cuáles son inventadas.

## 4. El mundo

1. Crea `src/mundos/<negocio>/` copiando la estructura de un ejemplo de `DIR_SKILL/ejemplos/<ejemplo>/mundo/`: `tienda` (comercio, logística; usa solo piezas del kit), `gimnasio` (servicios con salas y reglas de estado) o `tostadora` (fabricación, con máquinas a medida):
   - `index.tsx` exporta un `MundoTablero` (tipo en `src/mundos/tipos.ts`): título, zonas, indicadores, historial, nombres y `Planta`.
   - Las piezas 3D de cada zona en archivos aparte (como `maquinas.tsx`).
2. Construye cada zona con las piezas de `src/piezas/` (catálogo en `referencias/piezas.md`): formas, bandas, partículas y las comunes (personas, árboles, furgonetas, cajas que circulan). Nada de modelos externos. Que cada zona **haga algo**: una banda que corre, una máquina que gira, un vehículo que llega.
3. Coloca las zonas siguiendo `referencias/mundo.md` (ejes, tamaños, cámara). Para cada zona define su caja de clic (`zona`) y el punto de su tarjeta (`ancla`).
4. Cambia `src/mundo.ts` para que exporte el mundo nuevo y borra el ejemplo con el que arrancó, en `src/mundos/` y en `datos/ejemplos/`.

Reglas que evitan los fallos típicos:
- **Todo se mueve con `useT()`** (segundo del mundo), nunca con estado propio ni con `useFrame` dentro de una pieza. Así funcionan "parada" (congelar) y el arranque.
- **Envuelve cada zona en `<Congela desde={paradaDesde("<zona>")}>`** para que se detenga cuando su estado sea "parada".
- **Todo número en pantalla sale del CSV** (`d.num`, `d.valor`, `d.serie`, `d.filas`). Nada inventado en el código. Escribe la clave literal (`d.num("almacen_stock")`) para que `npm run validar` la compruebe.
- **Colores siempre con `PAL`**, sin códigos sueltos salvo materiales reales (cartón, agua). La marca se cambia en `marca.json`.

## 5. Comprobar

1. `npm run validar` y `npm run build`, los dos sin errores.
2. `npm run dev` y abre la dirección que imprime. Comprueba: se ve la maqueta entera (nada cortado arriba ni tapado por el aviso de controles; si pasa, ajusta `encuadre` y `escala`), cada zona se resalta al pasar el puntero, el clic abre su panel y las tarjetas apuntan a su zona.
3. Abre el panel **Datos**, cambia una cifra y un `<zona>_estado` a `parada`: cambia la cifra al momento, la tarjeta marca PARADA, esa zona se congela y `datos/planta.csv` queda guardado. Si hay reglas, cambia una cifra hasta cruzar su umbral y comprueba que la zona cambia sola. Deshaz los cambios al terminar.

## 6. Entregar

Deja `npm run dev` corriendo y da la dirección. Di qué zonas, números y reglas quedaron (y por qué), en qué carpeta está, qué fila del CSV cambiar para probarlo y qué cifras son inventadas. Ofrece adaptarlo a su marca: colores, tipografías y logo.
