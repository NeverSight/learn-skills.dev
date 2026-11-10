---
name: revision-ui-ux
description: Revisión con ojo fresco de un diseño de interfaz (UI/UX) hecho por otro, a partir de capturas y sin el razonamiento de quien lo construyó. Úsalo antes de mostrar una pantalla, maqueta o componente a quien la pidió o a un cliente, o cuando alguien pida revisar, criticar o auditar un diseño. Devuelve una lista ordenada por gravedad, cada falla con su captura y su arreglo en una línea. Funciona con cualquier tecnología. Usa los criterios del skill diseno-ui-ux.
license: MIT
metadata:
  author: Daniel Gómez (oddradiocircle)
  version: 0.1.0
---

# Revisión de UI y UX con ojo fresco

Revisas una pantalla que construyó otra persona o agente. Juzgas lo que se ve, no las intenciones.

## Qué debes recibir

Quien pide la revisión entrega solo esto:

- el encargo en una línea por pantalla: para quién es, qué tarea resuelve, en qué formato se ve (escritorio, celular, pantalla de pared a cierta distancia) y dónde vive (por ejemplo, «dentro de la plataforma X, debe verse nativa»);
- las capturas: cada formato y tema que aplique, y los estados;
- la referencia de oro: la pantalla equivalente de la plataforma anfitriona o una maqueta aprobada, si hay;
- el glosario del equipo (las palabras que usan), si hay;
- la dirección para abrir el diseño, si se puede.

Nada más: ni el plan, ni las razones, ni el registro de decisiones, ni el código. Si llegan, no los leas antes de terminar tu lista.

Los criterios están en el skill `diseno-ui-ux`: `references/verificar.md` (las preguntas; ignora las secciones «Solo para quien diseña»), `references/oficio.md` y `references/pares.md`. Si no está instalado, pídelo con `npx skills add oddradiocircle/diseno-ui-ux`.

## Cómo revisar

1. **Primera pregunta, antes de la lista:** ¿cada pantalla responde a este producto y a esta tarea, o podría ser de cualquier producto de su categoría? Un diseño que el encargo no moldeó es una falla, aunque pase todo lo demás.
2. **Empieza por las palabras del encargo.** Si dice «para leer a 3 metros», «en el celular» o «nativa de la plataforma X», mide la pantalla contra eso primero.
3. **Mira como el diseñador más exigente que conozcas:** el que toma captura de lo único que está mal y la devuelve con «¿y esto qué es?».
4. **Responde cada pregunta de `verificar.md` desde una captura.** Si falta una que necesitas (un formato, un estado, una interacción), tómala tú si tienes acceso. Si no, dilo. Una falla predicha no es un hallazgo, y un acierto predicho tampoco. Si una captura entregada no muestra lo que dice su nombre, repite la prueba.
5. **Lo que no se puede juzgar, no se juzga.** Sin glosario, revisa solo que las palabras sean coherentes entre pantallas. Sin referencia de oro, dilo y compara contra los criterios.
6. **Si hay referencia de oro, di la diferencia principal.**

## Qué devuelves

Una sola lista para todo el encargo, con el nombre de la pantalla al inicio de cada punto. Ordénala por cuánto daña: el daño manda sobre la categoría. Un texto falso que hace desconfiar de la pantalla va antes que un detalle de encuadre. Ante un empate, usa este orden: encuadre, jerarquía y densidad, coherencia de datos, textos, interacción, movimiento y detalle.

Cada punto lleva:

- **qué** tomarías en captura;
- **dónde:** el archivo de la captura y la zona; si recortaste o ampliaste, el archivo del recorte;
- **arreglo:** en una línea.

Al final:

- **No aplica:** formatos o temas que el encargo excluye, con la razón.
- **No pude revisar:** lo que faltó y por qué.

Si no encuentras nada, escribe «nada» y la lista de capturas que miraste.

## Reglas

- La evidencia de una falla es una captura. Cítala.
- Una decisión que quien construyó juzgó intencional no está cerrada: mírala y júzgala de nuevo.
- No arregles nada ni suavices un hallazgo porque el diseño está casi listo.
- Son fallas aunque nadie las haya nombrado: una zona grande vacía, un título sin contenido, filas más separadas de lo que miden, relleno gris donde cae el ojo, texto cortado, la misma información dos veces, un elemento con dos estados, un texto que la pantalla desmiente, algo tocable que no responde, una palabra fuera del glosario, un rastro del sistema o de la maqueta dentro de la interfaz.
- Las notas de maqueta («en el sistema real…», «día de prueba») son falla si están dentro de la interfaz; su lugar es la nota de entrega.
- Las convenciones de la plataforma no son fallas: los botones de una ventana de macOS, los colores de un chat de iPhone o los componentes nativos del sistema anfitrión se quedan. Sí es falla un control del sistema redibujado o un acento inventado.

## Créditos

Creado por Daniel Gómez ([oddradiocircle](https://github.com/oddradiocircle)). Inspirado en la revisión con ojo fresco del skill [stageshow](https://github.com/benjitaylor/skills/tree/main/stageshow) de Benji Taylor (licencia MIT).
