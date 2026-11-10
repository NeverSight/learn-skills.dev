---
name: diseno-ui-ux
description: Proceso y criterio para diseñar interfaces y experiencias de usuario (UI/UX) que se vean y se usen como un producto real, con cualquier tecnología (HTML, frameworks web, apps móviles, extensiones de una plataforma, maquetas). Úsalo al diseñar, rediseñar o pulir una pantalla, maqueta, componente, flujo, tablero, formulario o texto de interfaz, y al decidir cómo se ve o se comporta algo. Deja registradas las decisiones de diseño con su porqué. Para revisar un diseño ya hecho con ojo fresco, usa revision-ui-ux.
license: MIT
metadata:
  author: Daniel Gómez (oddradiocircle)
  version: 0.1.0
---

# Diseño de UI y UX

Una pantalla buena se reconoce, se entiende a la primera y deja hacer la tarea sin pensar en el sistema que hay detrás. Este skill es el proceso para llegar ahí y el criterio para decidir en cada paso. No depende de ninguna tecnología: sirve igual para una maqueta en HTML, una app web o móvil, o un componente dentro de otra plataforma.

## La idea central

**Se ve como un producto real, simplificado a lo que la persona necesita, con un solo lugar donde mirar, y todo lo que se mueve tiene una causa.**

Cinco maneras de fallar:

- **Demasiado.** Datos, números y etiquetas en todas partes. Entre más detalle, más parece generado.
- **Boceto.** Dos cajas grises y un botón. Quitó justo lo que hacía reconocible la pantalla.
- **Plano.** Todo pesa lo mismo, en la misma tarjeta con borde. El ojo no sabe dónde caer.
- **Genérico.** Una pantalla gris que podría ser de cualquier producto. La marca y el carácter del cliente son parte del encargo.
- **Del sistema.** La pantalla habla como el código: nombres de proveedores, colas, códigos, horas UTC, errores crudos.

El remedio: una pantalla completa y ordenada, palabras reales en lo que importa, aire para respirar y el peso visual sobre el resultado.

## Qué tan exigente ser

Diseña como alguien a quien van a juzgar por esa pantalla. Luego mírala como lo haría el diseñador más exigente que conozcas: el que toma captura de lo único que está mal y la devuelve con «¿y esto qué es?». Un punto fuera de su avatar, una unidad sola en una línea, un botón pegado al campo. Si puedes imaginar esa captura, ya encontraste lo siguiente que hay que arreglar.

Cuando piden «mejor diseño», piden **más fino**, no **más cosas**: el mismo contenido con más oficio (tipografía, color, jerarquía, detalle). Refinar no es agregar secciones.

## Proceso

La mayor parte de la calidad se decide antes del código. Escribe el plan primero.

1. **Entender la tarea.** ¿Quién usa la pantalla, en qué momento de su trabajo, en qué dispositivo y a qué distancia? ¿Qué decisión o acción tiene que salir de ahí? Si la regla central admite dos lecturas, muéstrala con un ejemplo de datos reales y confírmala antes de construir. Ver `references/decisiones.md`.
2. **Las palabras del usuario.** Cuenta en sus mensajes, correos o documentos cómo nombran las cosas y arma un glosario con las más frecuentes. Ese glosario vale para todas las pantallas del producto. Ver `references/textos.md`.
3. **La referencia de oro.** Escoge la pantalla más parecida que ya funcione y esté aprobada: la pantalla equivalente de la plataforma donde vivirá la tuya, una maqueta aprobada o un producto real que resuelva lo mismo. Haz una captura y tenla al lado todo el tiempo. Si la tuya es la más vacía, plana o pequeña de las dos, eso es lo primero que hay que arreglar. De la referencia se toma la interacción y el oficio, nunca la identidad de otra marca.
4. **El plan en cinco líneas.** El objeto principal, la acción, el resultado, qué se deja por fuera y en qué formatos se verá (escritorio, celular, pantalla de pared). El celular es un segundo diseño, no la misma pantalla apretada. Si un formato no aplica, escríbelo con la razón.
5. **El aspecto.** Si hay un sistema de diseño anfitrión (la librería de componentes del producto, la plataforma donde se integra o la marca), úsalo. Nunca imites a mano un botón, un campo o una etiqueta que el sistema ya tiene. Y lo nativo no basta: mide la pantalla equivalente del anfitrión y copia su espaciado, radios, tipografía e íconos. Sin sistema anfitrión, parte de la marca del cliente y define tokens (colores, tipos, espacios) antes de componer. Ver `references/oficio.md`.
6. **La pantalla quieta.** Construye con las reglas de `references/oficio.md`: palabras reales solo donde cae el ojo, una sola cifra grande, un solo estado por elemento, nada repetido, datos que no se contradicen.
7. **El movimiento.** Solo si ayuda a entender qué pasó. Ver `references/movimiento.md`.
8. **Verificar con capturas.** Toma capturas reales en cada formato y tema que aplique, y con los estados: vacío, cargando, con error, lleno y con el texto más largo. Prueba cada interacción con un clic o toque real. Cada respuesta sale de una captura, no del código. Ver `references/verificar.md`.
9. **Revisión con ojo fresco.** Antes de mostrar algo importante, pide una revisión con el skill `revision-ui-ux` a otra persona o a otro agente que solo reciba las capturas, la referencia, el glosario y el encargo en una línea, sin tus razones.
10. **Registrar las decisiones.** Cada decisión de diseño que no sea obvia queda escrita con su porqué, las alternativas y quién la aprobó. Ver `references/decisiones.md`.

## Fallas que vuelven en cada ronda

Revísalas antes de entregar:

- **Información repetida** en el mismo contexto: un aviso arriba y abajo, una etiqueta que repite lo que ya dice la pantalla.
- **Dos estados a la vez** en un elemento, o el mismo estado con dos nombres en el producto.
- **Números e íconos juntos** en el mismo elemento. Se escoge uno.
- **Datos que se contradicen:** un texto que dice algo que la pantalla de al lado desmiente.
- **Rastros del sistema** en la pantalla: proveedores, identificadores, colas, UTC, errores técnicos.
- **Palabras que el equipo no usa.** La especificación puede tener sus términos técnicos; la pantalla, no.
- **Imitaciones a mano** de componentes que el sistema anfitrión ya tiene.
- **Relleno donde cae el ojo** o una zona grande vacía sin razón.
- **Íconos inventados,** mezclados de varias familias, o destellos y morado para decir «IA».
- **Algo que aparece o desaparece de golpe,** o algo que parece tocable y no responde.
- **Solo se probó en un formato.**

## Referencias

- `references/oficio.md`: la pantalla quieta (contención, jerarquía, tipografía, espaciado, íconos, color, estados, coherencia, formatos, componentes).
- `references/textos.md`: palabras de la interfaz (glosario del usuario, lenguaje claro, errores, sin rastros del sistema).
- `references/movimiento.md`: lo que se mueve y por qué.
- `references/decisiones.md`: cuándo preguntar y cómo dejar escrita cada decisión.
- `references/verificar.md`: la revisión final, la tabla «ves / haces» y la entrega.
- `references/pares.md`: pares «así no / así sí» aprendidos de correcciones reales. Cuando alguien corrija un diseño con un criterio que sirve para otras pantallas, agrega el par.

## Créditos

Creado por Daniel Gómez ([oddradiocircle](https://github.com/oddradiocircle)). El proceso y parte del criterio de oficio se inspiran en el skill [stageshow](https://github.com/benjitaylor/skills/tree/main/stageshow) de Benji Taylor (licencia MIT), adaptado a interfaces reales y sin tecnología fija.
