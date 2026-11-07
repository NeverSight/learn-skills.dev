---
name: contextualizar-negocio
description: Contextualiza el negocio de un sistema existente (brownfield) para trabajar AI-first sobre él - arma el mapa de capacidades (qué hace hoy el sistema), saca a la luz las reglas de negocio escondidas en el código y construye el glosario negocio ↔ código junto con el ARCH, todo con evidencia, y se detiene para aprobación humana. Use when the BA role starts on an existing system without a PRD or backlog, or when asked to document what a legacy system does, extract its business rules, or build a domain glossary.
type: skill
tags: [ba, brownfield, capacidades, reglas-de-negocio, glosario]
---

# Contextualizar negocio (brownfield)

## Goal

Responder, en lenguaje de negocio y con evidencia, **qué hace hoy el sistema, bajo qué reglas y
cómo se llama cada cosa**. En un brownfield no hay PRD ni backlog: lo que el sistema hace está en
el código, y muchas de sus reglas no están escritas en ningún otro lado.

Esta skill cubre el **contexto funcional** (capas 3 y 4). El contexto técnico lo produce el ARCH
con `contextualizar-repo`.

**Esta skill no modifica código ni propone funcionalidades nuevas.** Levanta información,
documenta, pregunta y se detiene.

## Principios

1. **Lenguaje de negocio.** Cada capacidad y cada regla se escribe para que la entienda un PO; la
   evidencia técnica va al lado, no en lugar de la explicación.
2. **Nada sin evidencia.** Cada capacidad y cada regla lleva de dónde sale (endpoint, pantalla,
   prueba o `archivo:línea`), o queda `NO VERIFICADO`.
3. **Lo que el código hace no es necesariamente lo que el negocio quiere.** Si una regla parece
   un error o es ambigua, no se corrige ni se interpreta: se convierte en pregunta para el negocio.

## Input

- `docs/contexto/ARQUITECTURA.md` del ARCH (o el aviso `CONTEXTO TÉCNICO LISTO`): dice dónde
  mirar. Si no existe, preguntar si el ARCH va a correr primero; seguir sin él solo si el humano
  lo confirma, y avisar que el levantamiento será más lento y menos preciso.
- Documentación de usuario existente, si la hay.
- Opcional: la aplicación corriendo, para recorrer pantallas.

## Workflow

### 1. Fuentes

Recorrer, en este orden, lo que describe el comportamiento del sistema:

1. **La interfaz pública:** endpoints de la API, pantallas, comandos.
2. **Las pruebas existentes:** describen comportamiento esperado con ejemplos concretos.
3. **La configuración:** opciones y flags que cambian el comportamiento para el usuario.
4. **La documentación de usuario.**
5. **El código**, para confirmar y para encontrar lo que no aparece en las anteriores.

### 2. Mapa de capacidades (capa 3)

Agrupar por **capacidad de negocio**, no por archivo ni por endpoint. Por cada capacidad:

- qué permite hacer, en una frase de negocio;
- quién la usa (actor);
- evidencia (endpoint, pantalla, prueba o `archivo:línea`);
- estado: activa · detrás de una opción de configuración · obsoleta.

Usar `assets/capacidades-template.md`.

### 3. Reglas de negocio escondidas (capa 3)

Buscar en el código **validaciones, límites, transformaciones, permisos y valores por defecto**
que afectan lo que el usuario puede hacer. Por cada regla:

- enunciado en lenguaje de negocio ("un documento no puede nacer con más de 100.000 caracteres");
- evidencia `archivo:línea`;
- si está documentada en algún otro lugar (sí / no);
- si es ambigua o parece un error: **pregunta para el negocio**, sin resolverla.

### 4. Glosario (capa 4)

Construir `docs/contexto/GLOSARIO.md` con `assets/glosario-template.md`:

1. Juntar los términos del dominio que aparecen en la interfaz, la API y el código.
2. Por cada término: definición de negocio, sinónimos y **el nombre que usa el código** si es
   distinto, y el formato de su identificador si tiene uno.
3. La columna **"Dónde vive"** la completa el ARCH: enviarle
   `GLOSARIO: TÉRMINOS NUEVOS: <ruta> — <cantidad de términos>`.
   Si no hay ARCH en la sesión, completarla con evidencia y marcarla `pendiente de revisión técnica`.
4. Si un mismo término significa cosas distintas en lugares distintos, se registra como conflicto,
   no se elige una definición.

### 5. Escribir

| Archivo | Contenido |
|---|---|
| `docs/contexto/CAPACIDADES.md` | Mapa de capacidades + reglas de negocio + preguntas para el negocio |
| `docs/contexto/GLOSARIO.md` | Glosario negocio ↔ código |

Si `AGENTS.md` ya apunta a estos archivos (lo deja el ARCH), no se toca. Si no, se propone
agregar el enlace.

### 6. Autovalidación

- Volver a abrir cada evidencia citada y confirmar que respalda lo que se afirma.
- Confirmar que ninguna capacidad ni regla está escrita como si fuera nueva o propuesta.
- Confirmar que cada término del glosario tiene definición de negocio.

### 7. Gate humano

Presentar el resumen y las **preguntas para el negocio**, idealmente a un PO. **Esperar aprobación
explícita** antes de dar el contexto funcional por cerrado.

## Coordinación con el ARCH

- Esperar `CONTEXTO TÉCNICO LISTO` antes de empezar (salvo que el humano diga lo contrario).
- Enviar `GLOSARIO: TÉRMINOS NUEVOS` cuando haya términos sin ubicación en el código.
- Al recibir `GLOSARIO COMPLETO`, revisar que cada ubicación corresponda a la definición de
  negocio; si no, devolver la diferencia concreta.
- Máximo dos vueltas por el mismo desacuerdo; después decide el humano.

## Constraints

- No modifica código ni documentación técnica del ARCH.
- No propone funcionalidades nuevas: documenta las existentes.
- No resuelve reglas ambiguas: las pregunta.
- No da el contexto funcional por cerrado sin aprobación humana.
