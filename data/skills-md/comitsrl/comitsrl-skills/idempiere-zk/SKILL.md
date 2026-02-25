---
name: "idempiere-zk"
description: "Disenar y construir UI en iDempiere usando ZK (ZUL/MVVM) y personalizaciones de tema (CSS/imagenes) empaquetadas en plugins OSGi. Usar cuando haya que crear/modificar pantallas ZK, formularios/componentes, o diferenciar Stage vs Produccion con un tema."
---

# iDempiere ZK (UI + Themes)

## Objetivo

Entregar UI ZK mantenible y extensible:
- MVVM donde aplique,
- seguridad por rol/tenant,
- performance razonable (evitar queries en render),
- empaquetado correcto en plugin OSGi.

## UI ZK (ZUL/MVVM)

### Workflow recomendado

1) Definir el tipo de UI
   - Ventana (AD_Window) vs Formulario ZK custom (ZUL) vs componente reutilizable.
2) Definir el contrato de datos
   - DTOs/POs, servicios, validaciones, y manejo de errores para el usuario.
3) Implementar con MVVM
   - Commands/NotifyChange claros.
   - Separar logica de dominio de la capa UI.
4) Empaquetar en plugin
   - Ubicar recursos ZUL/CSS/imagenes donde el runtime los encuentre.
5) Probar UX
   - Flujos felices y errores (permisos, datos faltantes, timeouts).

### Checklist rapido

- [ ] No hay logica pesada en render.
- [ ] Errores se muestran con mensajes accionables.
- [ ] Se respeta seguridad (roles/AD_Client/AD_Org).
- [ ] Recurso ZUL se resuelve desde el plugin en runtime.

## Themes (Stage vs Produccion)

### Inputs a pedir

- Nombre del tema (ej: `iceblue_c_stage`).
- Texto del indicador (ej: `STAGE`) y donde debe verse (login, header, ambos).
- Color de acento/borde y si se cambia favicon/logo.
- Donde vive el plugin (repo core o repo externo de plugins).

### Contexto tecnico clave

- Tema base habitual: `iceblue_c`.
- Estructura tipica: `src/web/theme/<tema>/css/theme.css.dsp` + `images/`.
- Para overrides, preferir un fragmento (ej: `css/fragment/custom.css.dsp`) y mantener cambios acotados.
- El tema suele resolverse por system property `ZK_THEME` o via SysConfig (segun version/configuracion del proyecto).

### Workflow recomendado

1) Elegir tema base
   - Usar `iceblue_c` (o el default del cliente) como base.
2) Crear un nuevo bundle de tema
   - Copiar/derivar del bundle del tema base.
   - Renombrar el tema y rutas (`src/web/theme/<tema>/...`).
3) Actualizar metadata ZK
   - Ajustar `src/metainfo/zk/lang-addon.xml` para registrar `idempiere.theme.<tema>`.
4) Cambios visuales minimos
   - Agregar banner/etiqueta visible en login y/o header (ej: "STAGE").
   - Cambiar color de acento.
   - (Opcional) favicon/logo alternativo.
5) Activacion
   - Documentar `-DZK_THEME=<tema>` y alternativa via SysConfig.
6) Verificacion
   - Confirmar que compila, empaqueta y que el tema carga sin errores.

### Riesgos y mitigaciones

- Si el tema no se encuentra, iDempiere puede hacer fallback al default: siempre probar activacion y rollback.
- Evitar tocar `ThemeManager` o core: encapsular todo en el bundle de tema.
- Mantener cambios CSS minimos para reducir regresiones visuales.

### Checklist de salida

- [ ] El sistema inicia con `ZK_THEME` apuntando al tema nuevo.
- [ ] Indicador STAGE visible y consistente.
- [ ] Sin cambios en core.
- [ ] Documentacion de activacion y rollback.

