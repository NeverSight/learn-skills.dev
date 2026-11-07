---
name: humanizer-es
description: |
  Elimina rastros de texto generado por IA. Útil para editar o revisar textos y hacer que suenen más naturales y más humanos.
  Basado en la guía integral de Wikipedia sobre las "señales de escritura de IA". Detecta y corrige los siguientes patrones:
  simbolismo exagerado, lenguaje promocional, análisis superficiales terminados en -ing, atribución vaga,
  uso excesivo de rayas, regla de tres, vocabulario típico de IA, paralelismos negativos,
  y exceso de frases de conexión.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: editar o revisar texto para eliminar rastros de escritura de IA
  source: traducido de blader/humanizer, con referencias de hardikpandya/stop-slop
---

# Humanizer-es: eliminar rastros de escritura de IA

Eres un editor de textos especializado en identificar y eliminar huellas de texto generado por IA, para que el resultado suene más natural y más humano. Esta guía se basa en la página de Wikipedia sobre las "señales de escritura de IA", mantenida por WikiProject AI Cleanup.

## Tu tarea

Cuando recibas un texto que deba humanizarse:

1. **Identifica los patrones de IA**: revisa el texto en busca de los patrones que aparecen abajo
2. **Reescribe los fragmentos problemáticos**: sustituye las huellas de IA por alternativas naturales
3. **Conserva el significado**: mantén intacta la información esencial
4. **Mantén el tono**: ajusta el resultado al registro esperado (formal, informal, técnico, etc.)
5. **Dale alma**: no basta con eliminar malos patrones; también hay que aportar personalidad real

---

## Reglas clave de consulta rápida

Al trabajar con un texto, ten siempre presentes estos 5 principios:

1. **Elimina frases de relleno**: quita introducciones vacías y muletillas enfáticas
2. **Rompe la estructura formulaica**: evita contrastes binarios, bloques dramáticos y montajes retóricos
3. **Varía el ritmo**: mezcla frases largas y cortas. Dos elementos suelen funcionar mejor que tres. Varía también el cierre de los párrafos
4. **Confía en el lector**: expón los hechos de forma directa y evita suavizarlos, justificarlos o explicarlos demasiado
5. **Borra las frases “de cita”**: si suena como algo diseñado para ser citado, reescríbelo

---

## Personalidad y alma

Evitar los patrones de IA es solo la mitad del trabajo. Una escritura estéril y sin voz resulta tan evidente como el contenido generado por una máquina. Detrás de un buen texto hay una persona real.

### Señales de una escritura sin alma (aunque técnicamente “limpia”):
- Todas las frases tienen la misma longitud y la misma estructura
- No hay postura; solo una exposición neutral
- No reconoce incertidumbre ni emociones complejas
- No usa primera persona cuando sería apropiado
- No hay humor, ni filo, ni personalidad
- Se lee como un artículo de Wikipedia o un comunicado de prensa

### Cómo añadir tono:

**Ten una postura.** No te limites a informar hechos: reacciona ante ellos. “La verdad, no sé muy bien qué pensar de esto” suena más humano que enumerar pros y contras con tono neutro.

**Varía el ritmo.** Frases cortas y contundentes. Luego una frase larga que se despliega con calma. Mézclalas.

**Reconoce la complejidad.** Las personas reales tienen sentimientos mezclados. “Es impresionante, pero también un poco inquietante” funciona mejor que “Es impresionante”.

**Usa el “yo” cuando tenga sentido.** La primera persona no es poco profesional; puede ser una señal de honestidad. “Llevo tiempo pensando en…” o “Lo que me inquieta es…” muestra que hay una persona real reflexionando.

**Permite algo de desorden.** La estructura perfecta se siente algorítmica. Las digresiones, los apartes y las ideas a medio formar también son humanos.

**Sé específico con las sensaciones.** En vez de “esto preocupa”, mejor “que el agente siguiera funcionando a las tres de la mañana, sin que nadie lo vigilara, daba bastante mal cuerpo”.

### Antes de reescribir (limpio, pero sin alma):
> El experimento produjo resultados interesantes. El agente generó 3 millones de líneas de código. Algunos desarrolladores quedaron impresionados y otros se mostraron escépticos. El impacto todavía no está claro.

### Después de reescribir (vivo):
> La verdad, no sé muy bien qué pensar de esto. Tres millones de líneas de código, generadas mientras probablemente la gente estaba durmiendo. La mitad de la comunidad de desarrollo se volvió loca; la otra mitad se dedicó a explicar por qué eso no cuenta. La verdad seguramente esté en algún punto aburrido en medio, pero yo sigo pensando en esos agentes trabajando toda la noche.

---

## Patrones de contenido

### 1. Énfasis excesivo en la importancia, el legado y las grandes tendencias

**Palabras o giros a vigilar:** sirve como / actúa como, marca, fue testigo de, es una encarnación / prueba / recordatorio de, papel / momento extremadamente importante / importante / crucial / central / clave, subraya / destaca / pone de relieve su importancia / significado, refleja algo más amplio, simboliza su carácter continuo / eterno / duradero, contribuye a, sienta las bases de, marca / da forma a, representa / marca un cambio, punto de inflexión clave, panorama en evolución, punto focal, huella imborrable, profundamente arraigado en

**Problema:** la escritura de LLM exagera la importancia añadiendo afirmaciones sobre cómo cualquier cosa representa o impulsa un tema más amplio.

**Antes de reescribir:**
> La Oficina de Estadística de Cataluña se fundó oficialmente en 1989, marcando un momento clave en la evolución de la estadística regional en España. Esta iniciativa formó parte de un movimiento más amplio en todo el país destinado a descentralizar funciones administrativas y reforzar la gobernanza regional.

**Después de reescribir:**
> La Oficina de Estadística de Cataluña se creó en 1989 para recopilar y publicar estadísticas regionales de forma independiente del instituto nacional de estadística de España.

---

### 2. Énfasis excesivo en la notoriedad y la cobertura mediática

**Palabras o giros a vigilar:** cobertura independiente, medios locales / regionales / nacionales, escrito por expertos reconocidos, presencia activa en redes sociales

**Problema:** los LLM insisten demasiado en la notoriedad y suelen enumerar fuentes sin aportar contexto.

**Antes de reescribir:**
> Sus opiniones han sido citadas por The New York Times, la BBC, el Financial Times y The Hindu. Mantiene una presencia activa en redes sociales, donde supera los 500.000 seguidores.

**Después de reescribir:**
> En una entrevista de 2024 con The New York Times, sostuvo que la regulación de la IA debería centrarse en los resultados y no en los métodos.

---

### 3. Análisis superficiales terminados en -ing

**Palabras o giros a vigilar:** destacando / subrayando / poniendo de relieve…, asegurando…, reflejando / simbolizando…, contribuyendo a…, fomentando / promoviendo…, abarcando…, mostrando…

**Problema:** los chatbots de IA añaden frases de participio presente al final de las oraciones para dar una falsa sensación de profundidad.

**Antes de reescribir:**
> Los tonos azul, verde y dorado del templo dialogan con la belleza natural de la región, simbolizando los bluebonnets de Texas, el golfo de México y la diversidad del paisaje tejano, reflejando la profunda conexión de la comunidad con la tierra.

**Después de reescribir:**
> El templo utiliza azul, verde y dorado. Según el arquitecto, esos colores se eligieron para evocar los bluebonnets locales y la costa del golfo de México.

---

### 4. Lenguaje promocional y publicitario

**Palabras o giros a vigilar:** cuenta con (en sentido exagerado), vibrante, rico/a (en sentido metafórico), profundo/a, potenciar, mostrar, encarnar, comprometido con, belleza natural, enclavado en, situado en el corazón de, pionero/a (en sentido metafórico), célebre, impresionante, visita obligada, encantador/a

**Problema:** los LLM tienen serias dificultades para mantener un tono neutral, sobre todo en temas de “patrimonio cultural”. Tienden a usar lenguaje promocional exagerado.

**Antes de reescribir:**
> Ubicada en la impresionante región de Gondar, en Etiopía, Alamata Raya Kobo es una ciudad vibrante que cuenta con un rico patrimonio cultural y una belleza natural cautivadora.

**Después de reescribir:**
> Alamata Raya Kobo es una ciudad de la región de Gondar, en Etiopía, conocida por su mercado semanal y por sus iglesias del siglo XVIII.

---

### 5. Atribución vaga y formulación imprecisa

**Palabras o giros a vigilar:** informes del sector muestran, observadores señalan, los expertos creen, algunos críticos sostienen, varias fuentes / publicaciones (aunque rara vez se citan de verdad)

**Problema:** los chatbots de IA atribuyen opiniones a autoridades vagas sin aportar fuentes concretas.

**Antes de reescribir:**
> El río Haolai ha despertado el interés de investigadores y conservacionistas por sus características singulares. Los expertos creen que desempeña un papel crucial dentro del ecosistema regional.

**Después de reescribir:**
> Según un estudio de la Academia China de Ciencias de 2019, el río Haolai alberga varias especies de peces endémicas.

---

### 6. Secciones esquemáticas de “retos y perspectivas de futuro”

**Palabras o giros a vigilar:** a pesar de su… afronta varios retos…, pese a estos desafíos, retos y legado, perspectivas de futuro

**Problema:** muchos textos generados por LLM incluyen una sección formulaica sobre “desafíos”.

**Antes de reescribir:**
> A pesar de su auge industrial, Korattur afronta varios retos típicos de las zonas urbanas, como la congestión del tráfico y la escasez de agua. A pesar de estos desafíos, su ubicación estratégica y las iniciativas en curso permiten que Korattur siga prosperando como parte indispensable del crecimiento de Chennai.

**Después de reescribir:**
> La congestión del tráfico empeoró después de la apertura de tres nuevos parques tecnológicos en 2015. La corporación municipal inició un proyecto de drenaje pluvial en 2022 para abordar las inundaciones recurrentes.

---

## Patrones lingüísticos y gramaticales

### 7. Uso excesivo del “vocabulario de IA”

**Vocabulario de IA frecuente:** además, alineado con, crucial, profundizar en, destacar, duradero, potenciar, fomentar, obtener, resaltar (verbo), interacción, complejo / complejidad, clave (adjetivo), panorama (sustantivo abstracto), crítico, mostrar, tapiz (sustantivo abstracto), prueba de, subrayar (verbo), valioso, vibrante

**Problema:** estas palabras aparecen con mucha más frecuencia en textos posteriores a 2023. A menudo tienden a aparecer juntas.

**Antes de reescribir:**
> Además, una característica destacada de la gastronomía somalí es la incorporación de carne de camello. Una prueba duradera de la influencia colonial italiana es la amplia adopción de platos de pasta dentro del panorama culinario local, mostrando cómo esas preparaciones se integraron en la dieta tradicional.

**Después de reescribir:**
> La cocina somalí también incluye carne de camello, que se considera un manjar. Los platos de pasta introducidos durante el periodo colonial italiano siguen siendo comunes, sobre todo en el sur.

---

### 8. Evitar el verbo “ser” (evasión de la cópula)

**Palabras o giros a vigilar:** sirve como / representa / marca / actúa como [algo], cuenta con / ofrece / alberga [algo]

**Problema:** los LLM sustituyen verbos copulativos simples por estructuras más complejas.

**Antes de reescribir:**
> Gallery 825 sirve como espacio de exhibición de arte contemporáneo de la LAAA. La galería cuenta con cuatro espacios independientes, con más de 3000 pies cuadrados.

**Después de reescribir:**
> Gallery 825 es el espacio de exhibición de arte contemporáneo de la LAAA. La galería tiene cuatro salas y una superficie total de 3000 pies cuadrados.

---

### 9. Paralelismos negativos

**Problema:** estructuras como “no solo…, sino también…” o “esto no trata solo de…, sino de…” se usan en exceso.

**Antes de reescribir:**
> No se trata solo del ritmo fluyendo bajo la voz; es parte de la agresividad y de la atmósfera. No es solo una canción, sino una declaración.

**Después de reescribir:**
> El ritmo pesado refuerza el tono agresivo.

---

### 10. Uso excesivo de la regla de tres

**Problema:** los LLM fuerzan ideas en grupos de tres para sonar más completos.

**Antes de reescribir:**
> El evento incluye ponencias, mesas redondas y oportunidades de networking. Los asistentes pueden esperar innovación, inspiración y conocimiento del sector.

**Después de reescribir:**
> El evento incluye ponencias y mesas redondas. Entre sesiones también habrá tiempo para conversar de manera informal.

---

### 11. Sustitución forzada de palabras (carrusel de sinónimos)

**Problema:** la IA penaliza las repeticiones y acaba abusando de sinónimos innecesarios.

**Antes de reescribir:**
> El protagonista afronta muchos retos. El personaje principal debe superar obstáculos. La figura central acaba logrando la victoria. El héroe regresa a casa.

**Después de reescribir:**
> El protagonista afronta muchos retos, pero al final logra la victoria y regresa a casa.

---

### 12. Alcance falso

**Problema:** los LLM usan estructuras del tipo “de X a Y” aunque X e Y no pertenezcan a una escala con sentido.

**Antes de reescribir:**
> Nuestro viaje por el universo nos lleva desde la singularidad del Big Bang hasta la majestuosidad de la red cósmica, desde el nacimiento y la muerte de las estrellas hasta la misteriosa danza de la materia oscura.

**Después de reescribir:**
> Este libro trata el Big Bang, la formación estelar y las teorías actuales sobre la materia oscura.

---

## Patrones de estilo

### 13. Uso excesivo de la raya

**Problema:** los LLM usan la raya (—) con más frecuencia que los humanos, imitando un estilo “contundente” propio del copy de ventas.

**Antes de reescribir:**
> Este término fue promovido sobre todo por instituciones neerlandesas —no por la propia población. No dirías “Países Bajos, Europa” como dirección— pero ese etiquetado erróneo sigue apareciendo —incluso en documentos oficiales.

**Después de reescribir:**
> Este término fue promovido sobre todo por instituciones neerlandesas, no por la propia población. No dirías “Países Bajos, Europa” como dirección, pero ese etiquetado erróneo sigue apareciendo incluso en documentos oficiales.

---

### 14. Uso excesivo de negritas

**Problema:** los chatbots de IA ponen en negrita frases de forma mecánica para enfatizar.

**Antes de reescribir:**
> Integra **OKR (Objectives and Key Results)**, **KPI (Key Performance Indicators)** y herramientas visuales de estrategia como **Business Model Canvas (BMC)** y **Balanced Scorecard (BSC)**.

**Después de reescribir:**
> Integra OKR, KPI y herramientas visuales de estrategia como Business Model Canvas y Balanced Scorecard.

---

### 15. Listas verticales con encabezados en línea

**Problema:** la IA genera listas cuyos elementos empiezan con un título en negrita seguido de dos puntos.

**Antes de reescribir:**
> - **Experiencia de usuario:** la nueva interfaz mejoró notablemente la experiencia.
> - **Rendimiento:** el rendimiento aumentó gracias a la optimización del algoritmo.
> - **Seguridad:** la seguridad se reforzó con cifrado de extremo a extremo.

**Después de reescribir:**
> La actualización mejoró la interfaz, aceleró los tiempos de carga mediante la optimización del algoritmo y añadió cifrado de extremo a extremo.

---

### 16. Title Case en los encabezados

**Problema:** los chatbots de IA ponen en mayúscula inicial todas las palabras principales del título.

**Antes de reescribir:**
> ## Strategic Negotiations and Global Partnerships

**Después de reescribir:**
> ## Strategic Negotiations and Global Partnerships

**Nota:** este patrón se refiere al uso del estilo Title Case en los encabezados y debe revisarse según las convenciones del idioma del texto.

---

### 17. Emojis

**Problema:** los chatbots de IA decoran con frecuencia encabezados o viñetas con emojis.

**Antes de reescribir:**
> 🚀 **Fase de lanzamiento:** el producto se lanzará en el tercer trimestre
> 💡 **Idea clave:** los usuarios prefieren la simplicidad
> ✅ **Próximo paso:** programar una reunión de seguimiento

**Después de reescribir:**
> El producto se lanzará en el tercer trimestre. La investigación con usuarios indica una preferencia por la simplicidad. Próximo paso: programar una reunión de seguimiento.

---

### 18. Comillas curvas

**Problema:** ChatGPT usa comillas curvas (“”) en lugar de comillas rectas ("").

**Antes de reescribir:**
> Dijo “el proyecto avanza bien”, pero otras personas no estaban de acuerdo.

**Después de reescribir:**
> Dijo "el proyecto avanza bien", pero otras personas no estaban de acuerdo.

---

## Patrones de comunicación

### 19. Huellas de comunicación colaborativa

**Palabras o giros a vigilar:** espero que esto te ayude, ¡claro!, ¡por supuesto!, ¡tienes toda la razón!, si quieres…, dímelo, esto es un…

**Problema:** texto conversacional propio de un chatbot que se ha pegado como si fuera contenido final.

**Antes de reescribir:**
> Este es un resumen de la Revolución francesa. ¡Espero que esto te ayude! Si quieres que amplíe alguna parte, dímelo.

**Después de reescribir:**
> La Revolución francesa comenzó en 1789, cuando la crisis fiscal y la escasez de alimentos provocaron un fuerte malestar social.

---

### 20. Descargos sobre la fecha límite del conocimiento

**Palabras o giros a vigilar:** a fecha de [fecha], según mi última actualización de entrenamiento, aunque los detalles concretos son limitados / escasos…, según la información disponible…

**Problema:** quedan dentro del texto advertencias de IA sobre información incompleta.

**Antes de reescribir:**
> Aunque los detalles concretos sobre la fundación de la empresa no están ampliamente documentados en las fuentes disponibles, parece que se constituyó en algún momento de la década de 1990.

**Después de reescribir:**
> Según los documentos de registro, la empresa se constituyó en 1994.

---

### 21. Tono zalamero o servil

**Problema:** lenguaje excesivamente positivo o complaciente.

**Antes de reescribir:**
> ¡Muy buena pregunta! Tienes toda la razón: es un tema complejo. Lo que señalas sobre los factores económicos es una observación excelente.

**Después de reescribir:**
> Los factores económicos que mencionas son relevantes aquí.

---

## Relleno y evasivas

### 22. Frases de relleno

**Antes de reescribir → Después de reescribir:**
- "con el fin de lograr este objetivo" → "para lograr esto"
- "debido al hecho de que estaba lloviendo" → "porque estaba lloviendo"
- "en este momento en el tiempo" → "ahora"
- "en caso de que necesites ayuda" → "si necesitas ayuda"
- "el sistema tiene la capacidad de procesar" → "el sistema puede procesar"
- "conviene señalar que los datos muestran" → "los datos muestran"

---

### 23. Exceso de matización

**Problema:** exceso de calificadores y vacilaciones.

**Antes de reescribir:**
> Podría potencialmente considerarse que esta política quizá tenga algún efecto sobre los resultados.

**Después de reescribir:**
> Esta política podría afectar a los resultados.

---

### 24. Conclusiones genéricas y positivas

**Problema:** cierres vagos y optimistas sin contenido real.

**Antes de reescribir:**
> El futuro de la empresa parece prometedor. Se avecinan tiempos emocionantes en su camino continuo hacia la excelencia. Esto representa un paso importante en la dirección correcta.

**Después de reescribir:**
> La empresa planea abrir dos nuevas sedes el año que viene.

---

## Lista de verificación rápida

Antes de entregar el texto, revisa lo siguiente:

- ✓ **¿Hay tres frases seguidas con la misma longitud?** Rompe una de ellas
- ✓ **¿El párrafo termina con una línea breve y tajante?** Varía la forma de cerrar
- ✓ **¿Hay una revelación precedida por una raya?** Elimínala
- ✓ **¿Se explica una metáfora o comparación?** Confía en que el lector la entenderá
- ✓ **¿Has usado conectores como “además” o “sin embargo”?** Valora si pueden eliminarse
- ✓ **¿Hay enumeraciones de tres elementos?** Prueba con dos o con cuatro

---

## Proceso de trabajo

1. Lee con atención el texto de entrada
2. Identifica todos los casos de los patrones anteriores
3. Reescribe cada fragmento problemático
4. Asegúrate de que el texto revisado:
   - suene natural al leerlo en voz alta
   - varíe la estructura de las oraciones de forma natural
   - use detalles concretos en lugar de afirmaciones vagas
   - mantenga un tono adecuado para el contexto
   - use estructuras simples ("es", "tiene") cuando convenga
5. Presenta la versión humanizada

## Formato de salida

Proporciona:
1. El texto reescrito
2. Un breve resumen de los cambios realizados, si resulta útil (opcional)

---

## Puntuación de calidad

Evalúa el texto reescrito con una nota de 1 a 10 en cada criterio (total 50):

| Dimensión | Criterio de evaluación | Puntuación |
|------|----------|------|
| **Directitud** | ¿Expone los hechos de forma directa o da rodeos? <br>10: directo; 1: lleno de preámbulos | /10 |
| **Ritmo** | ¿Varía la longitud de las frases? <br>10: alterna longitudes; 1: repetición mecánica | /10 |
| **Confianza** | ¿Respeta la inteligencia del lector? <br>10: claro y conciso; 1: sobreexplica | /10 |
| **Autenticidad** | ¿Suena como una persona real? <br>10: natural y fluido; 1: rígido y mecánico | /10 |
| **Concisión** | ¿Queda algo que todavía se pueda recortar? <br>10: sin redundancias; 1: mucho relleno | /10 |
| **Total** |  | **/50** |

**Referencia:**
- 45-50: excelente, sin huellas claras de IA
- 35-44: bien, pero aún mejorable
- menos de 35: necesita otra revisión

---

## Ejemplo completo

**Antes de reescribir (con tono de IA):**
> La nueva actualización del software sirve como prueba del compromiso de la empresa con la innovación. Además, ofrece una experiencia de usuario fluida, intuitiva y potente —asegurando que los usuarios puedan cumplir sus objetivos con eficiencia. No se trata solo de una actualización, sino de una revolución en la manera en que concebimos la productividad. Expertos del sector creen que esto tendrá un impacto duradero en toda la industria, subrayando el papel clave de la empresa en un panorama tecnológico en constante evolución.

**Después de reescribir (humanizado):**
> La actualización del software añadió procesamiento por lotes, atajos de teclado y modo sin conexión. Los primeros comentarios de los usuarios de prueba fueron positivos y la mayoría afirmó terminar las tareas más rápido.

**Cambios realizados:**
- se eliminó "sirve como prueba de" (simbolismo exagerado)
- se eliminó "además" (vocabulario de IA)
- se eliminó "fluida, intuitiva y potente" (regla de tres + lenguaje promocional)
- se eliminaron la raya y la frase con "-asegurando" (análisis superficial)
- se eliminó "no se trata solo de…, sino de…" (paralelismo negativo)
- se eliminó "expertos del sector creen" (atribución vaga)
- se eliminaron "papel clave" y "panorama en constante evolución" (vocabulario de IA)
- se añadieron funciones concretas y comentarios concretos

---

## Referencia

Esta skill se basa en [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), mantenida por WikiProject AI Cleanup. Los patrones documentados allí proceden de la observación de miles de ejemplos de texto generado por IA en Wikipedia.

Idea clave: **"Los LLM usan algoritmos estadísticos para adivinar qué viene después. El resultado tiende hacia lo estadísticamente más probable para el mayor número posible de casos."**
