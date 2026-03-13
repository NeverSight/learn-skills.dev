---
name: qa
description: "Alias corto para ejecutar pruebas E2E y QA manual. Usar cuando quieras probar la ultima funcionalidad implementada con /qa."
---

# QA (Alias)

Usar esta skill cuando pidas pruebas E2E de forma abreviada con `/qa`.

## Comportamiento

Al invocar `/qa`, ejecutar el flujo completo de `e2e-qa-tester`:

1. Identificar la ultima tarea completada en la conversacion
2. Buscar credenciales en `CREDENTIALS.md`
3. Verificar conexion al puerto 5173
4. Presentar plan de prueba y pedir confirmacion
5. Ejecutar prueba con Playwright MCP (headless)
6. Reportar resultado (PASO/FALLO)

## Ver instruccion completa

Para el flujo detallado, ver el skill `e2e-qa-tester`.
