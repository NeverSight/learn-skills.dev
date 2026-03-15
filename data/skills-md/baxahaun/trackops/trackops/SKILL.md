---
name: "trackops"
description: "Skill global de TrackOps para explicar que hace TrackOps, exigir la instalacion explicita del runtime con npm y guiar la activacion local de proyectos y OPERA en cada repositorio."
---

# TrackOps

Si la conversacion y el proyecto deben trabajar en ingles, lee `locales/en/SKILL.md` antes de seguir.

TrackOps sirve para trabajar con agentes sobre proyectos reales sin mezclar la aplicacion y la capa operativa.

Esta skill es la puerta de entrada cuando alguien:

- quiere arrancar un proyecto con agentes IA
- ya tiene un repo y necesita orden operativo
- necesita activar TrackOps y, si hace falta, OPERA
- quiere trabajar en espanol o en ingles con el mismo flujo

## Que hace esta skill

Esta skill:

- explica que es TrackOps y cuando conviene usarlo
- exige una instalacion explicita y visible del runtime
- guia la activacion por repositorio
- ayuda a decidir si OPERA debe seguir por `direct bootstrap` o por `agent handoff`

## Que no hace esta skill

Esta skill no:

- instala paquetes por su cuenta
- ejecuta codigo remoto en silencio
- modifica un repositorio antes de que el runtime exista
- sustituye al runtime `trackops`

## Flujo rapido

Instala la skill del marketplace con:

```bash
npx skills add Baxahaun/trackops
```

Despues, confirma que el runtime `trackops` existe. Si no esta disponible, pide al usuario que lo instale de forma explicita:

```bash
npm install -g trackops
trackops --version
```

Reglas:

- la skill no debe instalar paquetes ni ejecutar codigo remoto por si sola
- el runtime se instala con un paso visible y auditable
- la skill puede verificar `trackops --version`, pero no debe encadenar instalaciones silenciosas
- la skill no debe crear archivos dentro de un repositorio por si sola

## Activacion en un proyecto

Dentro del repositorio:

```bash
trackops init
trackops opera install
```

Reglas base:

- trata la skill global como capa de instrucciones
- trata la instalacion del runtime como explicita y separada
- usa `ops/contract/operating-contract.json` como contrato de maquina cuando exista
- usa `ops/project_control.json` como fuente de verdad operativa
- usa `ops/policy/autonomy.json` antes de acciones sensibles
- usa `/.env` y `/.env.example` como contrato de entorno
- deja la documentacion operativa generada dentro de `ops/`
- usa `trackops locale get|set` y `trackops doctor locale` cuando el idioma importe

## Como entra OPERA

OPERA ya no asume que todo usuario es tecnico.

TrackOps clasifica:

- nivel tecnico del usuario
- estado actual del proyecto
- documentacion disponible

Luego elige una de dos rutas:

- `direct bootstrap`
  para usuarios tecnicos y repos ya definidos
- `agent handoff`
  para ideas tempranas, usuarios no tecnicos o documentacion debil

Si TrackOps deriva al agente:

- lee `ops/bootstrap/agent-handoff.md`
- o imprimelo con `trackops opera handoff --print`
- exige como salida:
  - `ops/bootstrap/intake.json`
  - `ops/bootstrap/spec-dossier.md`
  - `ops/bootstrap/open-questions.md` cuando queden huecos importantes
- reanuda con:

```bash
trackops opera bootstrap --resume
```

## Que debe entender alguien que llega desde skills.sh

- la skill global instala instrucciones en el agente
- el runtime se instala por separado con npm
- `trackops init` activa el proyecto
- `trackops opera install` anade el framework operativo completo solo cuando hace falta
- TrackOps separa producto y operacion para que el repo no se vuelva caotico

## Que referencia leer y cuando

- lee `references/activation.md` solo para instalacion, verificacion del runtime, locale bootstrap y activacion de un repo
- lee `references/workflow.md` solo cuando TrackOps ya esta activo y haga falta operar el dia a dia del repositorio
- lee `references/troubleshooting.md` solo cuando fallen la instalacion explicita, la deteccion de `trackops`, el resume o el contrato de entorno
