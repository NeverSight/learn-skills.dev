---
name: polkadot-products-devnet
description: Guía para crear, conectar y publicar Polkadot Products en Products Devnet (Paseo Asset Hub 1000, chainId 420420417) con versiones probadas. Usar cuando el usuario pregunte por Polkadot, Polkadot Products, Products Devnet, Product SDK (@parity/product-sdk), Polkadot Desktop o la Polkadot App como Host, contratos en Solidity on Polkadot sobre REVM, desplegar con Remix y MetaMask, ABI, OpenZeppelin, PGAS, faucet de Paseo, Bulletin, nombres .dot con dotns, o publicar con pad (polkadot-app-deploy). Responde primero con sus referencias y su registro curado de fuentes, cita la fuente y marca "no verificado" lo que no esté ahí.
metadata:
  autor: BrandonFilth
  evento: Polkadot México – Bootcamp + Hackathon UANL, 29–31 oct 2026
  probada: "2026-10-15"
---

# Polkadot Products en Products Devnet

Skill para construir una app (Polkadot Product) que corre dentro de un Host (Polkadot Desktop o la
Polkadot App), usa un contrato Solidity en Asset Hub y se publica en Bulletin con un nombre `.dot`.
Todo está ajustado a **Products Devnet** y a las versiones de `references/versiones.md`.

## Cuándo usarla

- Crear o modificar una app con `@parity/product-sdk`.
- Escribir, compilar, desplegar o llamar un contrato Solidity en Polkadot (REVM).
- Configurar MetaMask, el faucet, Remix o Blockscout para el devnet.
- Publicar la app (`pad`, `dotns`, Bulletin, manifest, icono).
- Diagnosticar un error del entorno, del SDK, de firmas o de publicación.
- Revisar si el entorno del usuario tiene lo necesario.

## Cómo responder

1. Buscar primero en `references/` (índice abajo), leyendo solo el archivo que haga falta.
2. Si no está, consultar las URLs de `references/fuentes.md` con la herramienta web del agente. Las
   skills de Parity se leen por sus enlaces `raw` fijados, no instaladas.
3. Si hace falta otra página de la documentación, buscarla en `https://docs.polkadot.com/llms.txt` y
   citarla como "fuera del registro curado".
4. Si el agente no puede leer páginas web, decirlo y responder solo con `references/`.
5. Citar siempre el archivo o la URL de donde sale el dato.
6. Si no aparece en ninguna fuente: decir **"no verificado"**, explicar qué habría que probar y no
   inventar APIs, direcciones, versiones ni comandos.
7. Lo marcado **POR VERIFICAR** en las referencias se presenta como tal, no como hecho.

## Reglas obligatorias

- **Red:** Products Devnet. Asset Hub 1000, chainId `420420417`, descriptor `devnet_asset_hub`
  (`@parity/product-sdk-descriptors/devnet-asset-hub`). Nunca `paseo`, `paseo_asset_hub`, Paseo Next
  v2 ni la red "Paseo PassetHub (420420422)".
- **Versiones exactas** de `references/versiones.md`, sin `^` ni `~`: `@parity/product-sdk` 0.27.0,
  `@parity/product-sdk-descriptors` 0.11.0, override `@parity/truapi` 0.13.1, pnpm 12.6.0. No
  actualizar ninguna sin que el usuario lo pida y lo pruebe en el Host.
- **Solo pnpm.** `pnpm install`, `pnpm add <pkg>@<versión> --save-exact`,
  `pnpm dlx --ignore-scripts <cli>@<versión>`. Nunca npm ni yarn para instalar en el proyecto.
- **Contratos:** Solidity `pragma solidity 0.8.28;`, sin optimizador, desplegados con Remix +
  MetaMask (REVM). Límite de 24,576 bytes. OpenZeppelin 5.6.1 para tokens y permisos.
- **SDK:** conectar con `createChainClient({ chains: { assetHub: devnet_asset_hub } })`; no usar
  `getChainAPI()` con Desktop 0.1.3.
- **Simular antes de firmar:** `.query()` antes de cada `.tx()`. Una firma a la vez.
- **Gas de la app:** PGAS vía `SmartContractAllowance`; el usuario final no necesita PAS.
- **Vite:** `base: './'` y el plugin que deja solo el descriptor del devnet
  (`references/app-sdk.md`, *Vite*).
- **Probar:** ningún Host se conecta a `localhost`. Conexión, firmas y PGAS solo con la app
  publicada en su `.dot` y abierta desde el Host; `pnpm dev` solo en un navegador normal.
- **Publicar:** el mismo flujo con dos usos. Parte común: `pad` 0.16.7 sin sesión, desde la
  carpeta del proyecto, con `--env devnet --js-merkle`, a un nombre temporal sin dígitos (`tmp` +
  fecha en letras), nunca el nombre propio, sin mnemónico ni keystore.
  1. **Pruebas rápidas** con `--no-manifest`: copiar el CID y pegarlo con Resolve en `dotns.dot`
     desde el Host (`contenthash` del nombre propio).
  2. **Publicación final** con icono, nombre y descripción: `polkadot-app-deploy.config.mjs` en el
     commit con `domain: process.env.APP_DOT`, sin `--no-manifest`, el nombre temporal en
     `APP_DOT`; luego el CID con Resolve y el JSON de `Verified text[manifest]:` como Custom Record
     `manifest` del dominio principal (sin `app.`).

  Volver a publicar solo para renovar el almacenamiento (antes de ~14 días) o para una versión
  nueva (`references/publicar.md`, secciones 2 y 4).
- **Secretos:** nunca pedir, leer, escribir ni mostrar mnemónicos, llaves privadas o `.env` con
  secretos. Solo cuentas de testnet.

## Qué ignorar de las skills de Parity

Las skills oficiales (`paritytech/product-sdk`, carpeta `product-sdk/skills`, Apache-2.0) son buena
referencia de la API, pero para este devnet **se ignora**:

1. **Sus ejemplos de red:** usan `getChainAPI("paseo")` y `paseo_asset_hub`, que apuntan a Paseo Next
   v2. Aquí se usa `devnet_asset_hub`.
2. **"Los contratos compilan a PolkaVM; no uses tooling de Ethereum"** (también en el *setup prompt*
   oficial). Aquí los contratos son Solidity en REVM con Remix + MetaMask. No usar `resolc`, `cdm`,
   `cdm.json` ni `ContractManager`; se usa `createContract(runtime, dirección, abi)`.
3. **Cualquier preset o entorno que no sea devnet:** `paseo`, `polkadot`, `kusama`, `previewnet`.
4. **APIs del SDK nuevo:** la rama `main` documenta el SDK ≥ 0.36 sobre `polkadot-api` 3. Consultar la
   versión fijada al tag `@parity/product-sdk@0.27.0` (commit `07fed91`, enlace en
   `references/fuentes.md`). Si una firma de función difiere, gana `references/app-sdk.md`.
5. **`npm init` / `npm install`** de `product-sdk-app-builder`: usar pnpm.

## Índice de referencias

| Archivo | Contenido |
|---|---|
| `references/red-devnet.md` | RPCs, chainId, génesis, Blockscout, Bulletin, faucet, MetaMask, PGAS, descriptor del SDK |
| `references/versiones.md` | Versiones fijas, resultado de la prueba del 2026-10-15, versiones más recientes no probadas |
| `references/contratos.md` | Solidity/REVM, Remix + MetaMask, ABI, tamaño, OpenZeppelin 5.6.1, cuentas y mapeo de direcciones |
| `references/app-sdk.md` | Sandbox, Vite, `createContract`, `.query()` → `.tx()`, cuenta del Product, PGAS, lecturas por ETH-RPC, plugin de Vite sin metadatos de otras cadenas |
| `references/publicar.md` | Dos usos del mismo flujo con `pad`: pruebas con `--no-manifest` y publicación final con config + `APP_DOT` (Resolve + Custom Record `manifest`), nombres `.dot`, `dotns`, icono blake2b, marcadores en Android |
| `references/errores-comunes.md` | Síntoma → causa → solución |
| `references/fuentes.md` | Registro curado de fuentes (URL + fijación + qué cubre) |

## Revisar el entorno

```sh
node <carpeta-de-la-skill>/scripts/verificar-entorno.mjs [ruta/del/proyecto]
```

Solo lee: no instala, no escribe y no usa la red. Revisa Node ≥ 22.19, pnpm, Git, Polkadot Desktop
y, si hay `package.json`, las versiones exactas, el override de truapi, `devEngines`, lockfiles de
otros gestores, lo instalado en `node_modules` y `base: './'` de Vite. Sale con código 1 si hay
algún ✘. Correrlo antes de diagnosticar un problema de instalación.

## Flujo típico de una app

1. Contrato en Remix → dirección + ABI (`references/contratos.md`).
2. Proyecto Vite + TS con las versiones fijas (`references/versiones.md`), verificado con el script.
3. Conexión, lecturas y escrituras con el SDK (`references/app-sdk.md`).
4. Parte visual y lecturas con `pnpm dev` en un navegador normal. Conexión, firmas y PGAS solo con
   la app publicada en su `.dot` y abierta desde el Host: ni Desktop ni la Polkadot App se conectan
   a `localhost` (`references/app-sdk.md`, *Dónde probar*).
5. `pnpm build` → publicar (`references/publicar.md`, sección 2) → pegar el CID en el
   `contenthash` → abrir el `.dot` en el Host. Dos usos: pruebas con `--no-manifest`; versión
   final con config + `APP_DOT`, Resolve y Custom Record `manifest`.
