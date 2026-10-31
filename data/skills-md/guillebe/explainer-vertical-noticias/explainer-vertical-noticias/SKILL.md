---
name: explainer-vertical-noticias
description: "Hacer o mejorar un explainer vertical corto (short, reel o TikTok, 9:16, de 15 a 60 s; 20 s por defecto) a partir de una nota periodística o para explicar un concepto con fuentes, con HyperFrames y una persona que decide en los puntos de control. Cubre guion por tiempos, footage con licencia verificada, storyboard, render, control de nivel medido (ritmo, quietud, tiempo de lectura y sonido audible en celular), crítica adversarial con otro agente y versiones numeradas. Usalo siempre que alguien pida convertir una nota o un tema en un video vertical, «un short de esta noticia», «un explainer de 20 segundos», mejorar o «llevar al nivel» un short existente, sumarle footage o música, o revisarlo antes de publicarlo, aunque no nombre HyperFrames. Also use it for English or Portuguese requests: news explainer, vertical video, short, reel, TikTok from an article, explainer vertical de notícias."
---

# Explainer vertical de noticias

Un explainer vertical corto hecho por un agente, con una persona que dirige en tres puntos de control. Las reglas salen de iterar dos explainers en el taller de Media Party Buenos Aires 2026; los casos concretos, para calibrar, están en `references/ejemplos.md`.

La idea de fondo: el agente hace muchas vueltas de producción y de control; la persona pone el criterio editorial y decide en los puntos de control. Ningún control automático ve errores de contenido, así que siempre hay crítica adversarial sobre el render.

## Antes de empezar

- Cargá el skill `hyperframes` (es la entrada obligatoria para componer y renderizar) y leé `hyperframes-core` antes de escribir HTML. Si no está, se instala con `npx hyperframes skills`.
- Si el proyecto fija una versión de HyperFrames, usá esa.
- Si el proyecto tiene lineamientos propios (estilo, referencias de nivel, marca), leelos antes del guion.
- Acordá con la persona tres parámetros, o usá los valores por defecto:
  - **Duración:** 20 s. Entre 15 y 60 s funciona igual; más largo deja de ser un short.
  - **Formato:** 9:16, compuesto en 720×1280 (`data-width="720" data-height="1280"`): son 2,25 veces menos píxeles por cuadro que 1080×1920, así que renderiza más rápido y pesa menos, y en un celular no se nota. Si la persona pide 1080×1920, multiplicá por 1,5 todas las medidas en píxeles de este skill. Si va a un feed que recorta, 4:5 (720×900) o 1:1 (720×720).
  - **Idioma:** el de la nota o el del pedido. Todo lo que va en pantalla, en ese idioma.
- **Destino:** dónde se publica (redes, sitio propio, presentación). Define la zona segura y si puede llevar link.
- **Llamado a la acción:** qué querés que haga quien terminó de ver (leer la nota completa, seguir la cobertura, seguir la cuenta) y con qué nombre (el medio, la cuenta, la web). Por defecto: **«Leé la nota completa en <medio>»**, con el nombre del medio de la nota (sin nota, «Leé más en <fuente principal>»).

## El flujo

### 0. La nota, o las fuentes (`source.md`)

Armá o actualizá `source.md` en la carpeta del proyecto. Es contra lo que el crítico compara cada cifra, así que tiene que existir antes del guion.

- **Con nota:** el link, la fecha y el autor; las citas textuales de cada dato que va a ir en pantalla (copiadas del HTML de la página, no parafraseadas); los datos oficiales; las diferencias entre fuentes.
- **Sin nota, para explicar un concepto:** juntá dos o tres fuentes confiables con link y fecha, y citá de ellas cada dato. El cierre invita a la mejor de esas fuentes en lugar de a «la nota».

Reglas de los datos:

- **Mirá la fecha.** Si un balance es de hace días, el video tiene que decir de cuándo es («segundo informe, 10/10»). Proyectar un balance viejo sin fecha hace mentir al gancho.
- **Los datos cambian mientras trabajás.** Un balance se actualiza por hora y el informe oficial puede llegar al día siguiente. Rechequeá cada cifra antes de cada render; si cambió, va en una versión nueva y las anteriores quedan con los datos que tenían.
- **Verificá la firma.** El autor está en `<meta name="author">` o en la firma visible; el JSON-LD a veces pone el crédito de la foto como autor.
- **Las estimaciones van atribuidas** («≈ 200 km/h · estimación del ministro»), y si después hay una fuente mejor, se reemplaza.
- **Conceptos distintos no se mezclan** aunque tengan la misma unidad: el tope que fija un reglamento no es la máxima de un tramo.

### A. Guion por tiempos (punto de control A)

Proponé tres ganchos y una tabla `t · qué se ve · texto`, y esperá el ok antes de escribir código. Reglas:

- **Una sola idea.** Fecha, hecho central, lugar y un bloque de consecuencias alcanza. Nueve datos en 20 s no se entienden.
- **Buscá el dato que hace la historia.** A veces es un contraste («la regla pedía 40; iba a unos 200») y dice más que la regla sola.
- **El gancho tiene el dato y la fecha**, entero desde el primer cuadro, y se entiende sin sonido.
- **El gancho no miente:** lo que promete, lo sostiene la fuente.
- **Tiempo de lectura:** cada texto dura al menos 0,5 s + 0,3 s por palabra. En total, unas 2,5 palabras por segundo de video (unas 50 para 20 s) y no más de 6 por placa.
- **Nada de unidades mezcladas en un mismo gráfico**, y no inventes totales que la fuente no da.
- **Seguí el énfasis de la fuente:** si destaca algo, el gráfico no lo puede dejar último.
- **Cierre con una pregunta que la fuente contesta**, y después **una placa de llamado a la acción**:
  - Corta, de 6 palabras o menos, con un verbo y un nombre: «Leé la nota completa en elDiario.es», «Seguí la cobertura en @medio».
  - Dura al menos 1,5 s y entra después de la pregunta, sin taparla. Pregunta y llamado pueden compartir pantalla si los dos se leen enteros.
  - Dónde está el link depende del destino: en el video, si se puede tocar; si no, «link en la descripción» o «en la bio».
  - Que el llamado lleve a lo que promete: si dice «la nota completa», el link es a esa nota.

### Footage y material

Leé `references/footage.md`. En resumen: usá solo planos que muestren lo que la fuente dice, con licencia, fecha, lugar y autor verificados; si un plano no tiene lugar y fecha verificados, no va. Pedí permiso antes de cada descarga, con archivo, fuente y tamaño. El material con derechos se usa solo con el ok de la persona, con crédito, y se registra como de uso restringido.

### B. Storyboard (punto de control B)

Escribí la composición, corré `hyperframes check` (0 errores) y sacá un cuadro por escena con `hyperframes snapshot --at …`. Guardalos con el número de versión (`storyboard/vN-escena-K.png`) y no borres los anteriores. Mostralos, señalá vos mismo lo que ves flojo y esperá las notas. Un formato de nota que funciona: `t=… · dónde · problema → cambio`.

Reglas de composición:

- **Las cifras entran con su valor final** (escala u opacidad). Un contador que cuenta muestra cifras falsas casi todo el tiempo, y una captura puede salir con cualquiera.
- **Un dato general no va sobre la foto de un lugar concreto**: se lee como si fuera de ese lugar.
- **El ritmo está adentro de cada escena** (algo entra, se dibuja o se mueve cada 1 o 2 s), no en sumar cortes y datos.
- **Gráficos que se dibujan al ritmo de la frase**, con un sistema fijo: fondo liso, raya de acento, título con unidad, fuente abajo.
- **Créditos y fuentes legibles** (20 px o más en 720 de ancho).
- **La zona segura depende del destino.** Para redes en 9:16, el texto va entre 175 px desde arriba, 320 px desde abajo y 120 px desde la derecha (en 720×1280). Si no va a redes, fuentes y créditos pueden ir al pie del cuadro.
- **Un plano horizontal en vertical va completo, entre barras diseñadas**, no recortado (se pixela) ni sobre un relleno desenfocado (se ve barato). Recortá las marcas de agua del canal.
- **Lo decorativo no parece documento:** un trazo o un gráfico ilustrativo va sin ejes ni valores, y sin el aspecto de un registro real.
- **Un esquema es esquema o es figurativo, no a mitad de camino.** Rotulá solo lo que dan las fuentes y marcalo («Esquema · posiciones aproximadas»).
- **El movimiento tiene que ser coherente con los datos.** Un vehículo que acelera cuando los registros dicen que frenaba, o que salta de posición entre escenas, contradice la historia.
- **No cortes entre dos fondos iguales.** Si el dato siguiente vive en el mismo esquema, metelo adentro en lugar de pasar a una placa aparte.

### Sonido

Leé `references/sonido.md`. El audio real del hecho va adelante, la música baja debajo, todo normalizado a −14 LUFS. Los graves por debajo de unos 110 Hz no se oyen en un celular: medí la banda audible, no solo la sonoridad.

Si un medio publicó audios del hecho (grabaciones, llamadas), pedí el ok antes de bajarlos, acreditalos y poné la transcripción en pantalla con quién habla. Alargá la escena lo que haga falta para que entre la frase entera, aunque el video pase de la duración acordada.

### C. Render, nivel y crítica (punto de control C)

1. Renderizá a `<proyecto>-vN.mp4` con un número nuevo. El render guarda los cuadros en disco (en 1080×1920, de 1,2 a 1,4 GB para 20 s; en 720×1280, proporcionalmente menos): si falla por espacio, usá `--workers 1`, que codifica mientras captura.
2. Corré el control de nivel:
   ```bash
   python3 scripts/medir_nivel.py <proyecto>-vN.mp4 --html index.html
   ```
   Falla si algo queda quieto más de 2 s, si un texto dura menos que su tiempo de lectura, si la sonoridad está lejos de −14 LUFS o si hay segundos sin señal audible en celular. Informa los cortes pero no los exige: perseguir cortes puede empeorar la legibilidad.
3. Lanzá la crítica adversarial con un agente nuevo que no armó el video. El brief está en `references/critico.md`.
4. Mostrá a la persona el video, las métricas contra la versión anterior y los P0, P1 y P2 del crítico. Los P0 se arreglan; los P1 y P2 los decide la persona.

### Versiones y registro

- Cada cambio es una versión nueva: guardá la composición anterior (por ejemplo, `versiones/index-vN.html`), renderizá a `<proyecto>-vN.mp4` y sumá una línea a «Versiones» en `source.md`. Nunca pises un `-vN` ni dejes un video sin número.
- En `source.md` registrá también el material nuevo con licencia, fecha, lugar y URL; lo que encontró cada crítica; y las lecciones. Es lo que permite que otra persona o agente retome el trabajo sin repetir errores.
- No publiques ni compartas material con derechos sin el ok de la persona.

## Lo que este skill no hace

No reemplaza el criterio editorial: la persona decide qué se cuenta, aprueba el guion y los P1. Tampoco verifica la nota de origen; verifica que el video diga lo mismo que la fuente.
