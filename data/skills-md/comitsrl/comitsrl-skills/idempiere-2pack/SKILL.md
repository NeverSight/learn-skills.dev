---
name: "idempiere-2pack"
description: "Analizar, disenar y operar paquetes 2Pack (Pack Out/Pack In) en iDempiere: tipos de AD_Package_Exp_Detail, handlers OSGi, importacion diferida, activators automaticos (Adempiere/Version2Pack/Incremental), packin desde carpetas, troubleshooting y riesgos de seguridad. Usar cuando el trabajo involucra transporte de diccionario/datos o instalacion automatica via plugin."
---

# iDempiere 2Pack (Pack In/Out)

## Objetivo

Resolver cambios basados en 2Pack de forma repetible y segura:
- exportar (Pack Out) diccionario/datos,
- importar (Pack In) manual o automatico,
- diagnosticar fallas de handlers, SQL, referencias UUID/ID y orden de instalacion,
- reducir riesgos operativos (scripts ejecutables, DDL, locks, reintentos).

## Cuando usar esta skill

- Requerimientos de migracion funcional por 2Pack.
- Plugins que instalan `2Pack.zip` o `2Pack_*.zip` al arrancar.
- Ajustes de `AD_Package_Exp` / `AD_Package_Exp_Detail`.
- Errores en `AD_Package_Imp*`, elementos unresolved/deferred o conflictos de tenant.
- Automatizacion de packin desde carpetas (server startup o proceso).

## Limites y coordinacion

- Si el trabajo es mayormente DDL/diccionario SQL, coordinar con `$idempiere-db`.
- Si el trabajo es bundle OSGi/feature/update-site, coordinar con `$idempiere-plugin-development`.
- Esta skill cubre la capa funcional/runtime de 2Pack (flujo, handlers, activators, operacion).

## Flujo recomendado

1. Clasificar escenario: `manual packin`, `embedded plugin packin`, o `external folder packin`.
2. Definir tipo(s) de detalle (`Data`, `DataSingle`, `SQL`, `SQM`, `SH`, `SCJ`, etc.) y orden.
3. Verificar handler real y prerequisitos (tabla, referencias, tenant, UUID).
4. Ejecutar/importar y validar estado (`Completed successfully`, `Completed - unresolved`, `Import Failed`).
5. Revisar trazas en `AD_Package_Imp_Detail` + notificador y ajustar idempotencia/versionado.
6. Para automaticos: validar naming/version locks/retries y no-reproceso.

## Referencias

- Mapa tecnico completo: `references/core-map.md`.
- Playbook operativo y troubleshooting: `references/operating-playbook.md`.
- Diferencias wiki vs core y caveats: `references/wiki-vs-core.md`.
