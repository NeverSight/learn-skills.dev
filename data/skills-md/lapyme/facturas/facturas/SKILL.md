---
name: facturas
description: "Emití facturas electrónicas, notas de crédito y notas de débito con ARCA (ex AFIP) desde TypeScript con el paquete facturas. Usala siempre que el usuario quiera facturar en Argentina, obtener un CAE, integrar ARCA o AFIP, WSFE, WSAA o WSMTXCA, emitir como monotributista o responsable inscripto, corregir o anular una factura, reintentar sin duplicar comprobantes o consultar un CUIT en el Padrón, aunque no nombre el paquete. También aplica a pedidos en inglés como Argentina e-invoicing, electronic invoice, AFIP integration o CAE authorization."
license: Apache-2.0
---

# facturas

`facturas` es el SDK de TypeScript para emitir comprobantes electrónicos con
ARCA (ex AFIP). Se conecta directo desde tu servidor, sin SOAP ni XML a la
vista y sin intermediarios. Requiere Node.js 22 o posterior y es solo ESM.

- npm: `facturas`
- Documentación: https://facturas-sdk.dev
- Repositorio: https://github.com/LaPyme/facturas

## No confíes en tu memoria

El paquete está antes de la 1.0 y su API cambia entre versiones menores. Por
ejemplo, el CLI pasó de `--tax-id` a `--cuit` y varios métodos se renombraron
o se quitaron. Lo que recuerdes de versiones anteriores, o de otras librerías
de ARCA, probablemente no aplique.

1. Mirá la versión instalada en `node_modules/facturas/package.json` y la
   última con `npm view facturas version`. Si el proyecto está atrasado,
   avisale al usuario y leé el
   [changelog](https://github.com/LaPyme/facturas/blob/main/packages/arca/CHANGELOG.md).
2. Los tipos en `node_modules/facturas/dist/` son la verdad para la versión
   instalada. Empezá por `index.d.ts`, que reexporta el resto, y buscá ahí cada
   campo antes de usarlo.
3. Cualquier página de la documentación se lee en Markdown agregando `.md` a
   la URL. El índice está en https://facturas-sdk.dev/llms.txt y el texto
   completo en https://facturas-sdk.dev/llms-full.txt.
4. Si no encontrás respaldo en los tipos ni en la documentación, decilo. No
   inventes campos ni códigos de ARCA.

## La primera factura no necesita infraestructura

Sin base de datos, sin tabla y sin servicio externo. El cliente lee cuatro
variables de entorno y guarda el ticket de WSAA en memoria:

| Variable | Valor |
| --- | --- |
| `ARCA_TAX_ID` | CUIT de 11 dígitos |
| `ARCA_CERTIFICATE_PEM` | El certificado PEM completo |
| `ARCA_PRIVATE_KEY_PEM` | La clave privada PEM completa |
| `ARCA_ENVIRONMENT` | `test` (homologación) o `production`. No hay valor por defecto |

```ts
import { createArcaClient } from "facturas";

const arca = createArcaClient();

const factura = await arca.issue({
  issuer: "monotributo",
  salesPoint: 3,
  to: { condition: "consumidor_final" },
  items: [{ amount: 150_000 }], // ARS 1.500,00 en centavos
});
```

El certificado, la autorización del servicio y el punto de venta se habilitan
en ARCA. El SDK no lo hace por el usuario, pero el CLI lo guía:

```sh
npx facturas init --cuit 20123456786 --env test   # clave privada y CSR
npx facturas cert                                  # guarda el certificado de ARCA
npx facturas check                                 # prueba configuración, WSAA, WSFE y puntos de venta
npx facturas issue --sales-point 3 --issuer monotributo   # factura de ARS 1 en homologación
```

Cuando algo falle antes de emitir, sugerí `npx facturas check`: nombra el paso
que falla y dónde corregirlo en ARCA. En ejemplos usá siempre el CUIT de
muestra `20123456786`, nunca uno real.

## El input es de negocio

Pasá datos de la venta y dejá que el SDK derive la clase, el tipo de
comprobante, el IVA de cabecera y el pedido para ARCA. No armes esos valores a
mano.

- `issuer` es la condición fiscal real del emisor: `"monotributo"`,
  `"responsable_inscripto"`, `"exento"` o `"no_alcanzado"`, o su código de
  ARCA (`6`, `1`, `4`, `15`). Es una afirmación legal: preguntala si no la
  sabés, nunca la infieras.
- Un responsable inscripto emite A a receptores RI o monotributistas y B al
  resto. Los demás emisores emiten C.
- Los importes son enteros en centavos. `150_000` es ARS 1.500,00. Nunca uses
  pesos con decimales.
- Clase C: `items: [{ amount }]`. Clase A o B: `items: [{ gross, vat }]` o
  `[{ net, vat }]`, con `vat` en `0`, `2.5`, `5`, `10.5`, `21`, `27`,
  `"exempt"` o `"untaxed"`.
- `to` es el receptor: `{ condition: "consumidor_final" }`, o una condición
  con `cuit`. Desde ARS 10.000.000 el consumidor final también necesita `cuit`
  o `dni`.
- Por defecto la fecha es hoy en Buenos Aires, el concepto es productos y la
  moneda es `ARS`. Para servicios pasá `service: { from, to, dueDate }`.
- ARCA acepta una fecha de hasta 5 días antes o después de hoy para productos,
  sin pasar al mes siguiente, y 10 para servicios. `preview()` e `issue()`
  lanzan `ArcaInputError` con `code: "ARCA_INPUT_DATE_OUTSIDE_WINDOW"` y
  `window: { from, to }` fuera de esa ventana. `voucherDateWindow()` la
  calcula antes, sin I/O.

`arca.preview(input)` es sincrónico y no hace I/O. Devuelve la clase, el tipo,
los importes y el pedido exacto. Compará `preview(input).amounts.sentTotal`
con el total de la venta antes de llamar a `issue()`.

Para campos menos comunes, como moneda extranjera, tributos, FCE o
`optionalFields`, leé [Emitir facturas](https://facturas-sdk.dev/guides/invoices.md).

## Tratá los cuatro resultados

`issue()`, `issueCreditNote()`, `issueDebitNote()` y `recover()` devuelven el
resultado fiscal en vez de lanzarlo. El código tiene que tratar los cuatro:

```ts
switch (factura.kind) {
  case "authorized":
    // Guardá number, cae, caeExpiry, header, amounts y qr.
    await guardar(factura.voucher);
    break;
  case "rejected":
    // ARCA rechazó. El input corregido va con una clave nueva.
    console.error(factura.issues);
    break;
  case "indeterminate":
    // No se sabe si ARCA emitió. Conservá el número y conciliá.
    console.error(factura.attempted, factura.lookup);
    break;
  case "conflict":
    // Otro comprobante ocupa el número. Detené el flujo y avisá a una persona.
    console.error(factura.attempted, factura.found);
    break;
  default:
    factura satisfies never;
}
```

`voucher.qr` es la URL que codifica el QR del comprobante impreso y
`voucher.qrPayload` su JSON. Lo que sí se lanza son los errores de input
(`ArcaInputError`, con un `code` como `ARCA_INPUT_INVALID_AMOUNT`) y de
configuración (`ArcaConfigurationError`), siempre antes de escribir en ARCA. Un
`ArcaInputError` significa que ARCA no emitió nada por esa llamada: corregí el
input y reintentá.

## Reintentos sin duplicados

ARCA no acepta una clave de idempotencia. Si la respuesta se
pierde, reintentar a ciegas puede emitir dos facturas. Para producción, agregá
un `store` persistente y pasá el ID estable de la venta como `idempotencyKey`:

```ts
import { createArcaClient, createPostgresStore } from "facturas";
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const arca = createArcaClient({
  store: createPostgresStore({ query: (text, params) => pool.query(text, params) }),
});

const factura = await arca.issue(input, { idempotencyKey: venta.id });
```

La tabla se crea una vez:

```sql
CREATE TABLE arca_store (
  key text PRIMARY KEY,
  value text NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);
```

También hay `createRedisStore(redis)`, `createFileStore(dir)` para un único
servidor y `createMemoryStore()`, que solo sirve para pruebas porque no
sobrevive a un reinicio. Reglas de la clave:

- Una clave por operación de negocio, de 1 a 255 caracteres, sin CUIT, DNI ni
  datos personales. Nunca un UUID nuevo por intento.
- Una `idempotencyKey` sin `store` lanza antes de cualquier I/O.
- Mismo input con la misma clave. Otro input lanza
  `ARCA_INPUT_IDEMPOTENCY_MISMATCH`.
- Después de `rejected`, el input corregido va con una clave nueva.
- Nunca borres ni hagas vencer los registros del store: guardan el número que
  un reintento tiene que consultar.

Ante `indeterminate`, `recover(clave)` consulta la reserva y nunca emite. Hacé
lo que dice `lookup.kind`:

| `lookup.kind` | Qué hacer |
| --- | --- |
| `not_found` | ARCA confirmó que el número está vacío. Llamá otra vez al método original con la misma clave y el mismo input |
| `failed`, `aborted` | La consulta no terminó. Esperá y volvé a llamar a `recover()` o repetí la llamada original con la misma clave |
| `incomplete` | ARCA tiene un comprobante en el número reservado, pero la consulta no trae los datos para probar que es este. No emitas otro. Probá `recover()` una vez más y, si sigue igual, que lo revise una persona con `reason` y `attempted` |
| `blocked` | Otra reserva frena la secuencia. Conciliá primero la clave `by` con `recover()` y después repetí |
| `superseded` | La secuencia siguió sin esta clave. Emití con una clave nueva |

`recover()` sobre una clave sin reserva lanza
`ARCA_INPUT_RESERVATION_NOT_FOUND`. Detalles en
[Evitar comprobantes duplicados](https://facturas-sdk.dev/guides/avoid-duplicates.md).

## Notas de crédito y débito

ARCA no anula comprobantes. Una corrección es una nota de crédito, que también
es un documento fiscal real. Nombrá la factura original con `for` y elegí el
modo de forma explícita:

```ts
const nota = await arca.issueCreditNote(
  {
    for: { salesPoint: 3, voucherType: 11, number: 41 }, // o factura.voucher
    items: [{ amount: 50_000 }], // devolución parcial, ARS 500,00
  },
  { idempotencyKey: `nc:${devolucion.id}` },
);
```

- `items` acredita líneas y es el caso habitual. `all: true` acredita el
  original completo. Uno de los dos, o un desglose `amounts`, es obligatorio.
- La forma de los ítems sigue la clase del original: `{ amount }` en C,
  `{ gross | net, vat }` en A y B.
- La clase, el receptor, la moneda y el concepto salen del original. La nota
  no lleva `issuer`, `to` ni `currency`.
- `issueDebitNote()` tiene el mismo contrato sin `all: true`.
- `previewCreditNote()` y `previewDebitNote()` son asincrónicas porque
  consultan el original.
- `arca.lookup({ salesPoint, voucherType, number })` consulta un comprobante
  autorizado, en centavos y fechas `YYYY-MM-DD`. Devuelve `null` si ARCA no lo
  tiene.
- `arca.lastAuthorized({ salesPoint, voucherType })` devuelve el último número
  autorizado, o `0`, en WSFE o WSMTXCA.
- `associatedPeriod: { from, to }` en lugar de `for` ajusta un período. Es la
  alternativa cuando no hay un comprobante puntual.

Detalles en [Notas de crédito y débito](https://facturas-sdk.dev/guides/credit-notes.md).

## Producción

- Homologación y producción tienen certificados y puntos de venta propios. El
  par de producción se genera con
  `npx facturas init --cuit 20123456786 --env production`.
- `ARCA_ENVIRONMENT=production` emite documentos reales. Una prueba de ARS 1
  (`items: [{ amount: 100 }]`) también lo es y se corrige con una nota de
  crédito.
- Store persistente compartido por todos los procesos que emiten, e
  `idempotencyKey` en cada emisión.
- `abortSignal: AbortSignal.timeout(20_000)` evita llamadas colgadas. Un corte
  después del envío devuelve `indeterminate` con `lookup.kind === "aborted"`.
- Los logs quedan en `warn`. En `debug` se loguean los pedidos SOAP con datos
  de clientes. Nunca loguees los PEM.

La lista completa está en [Pasar a producción](https://facturas-sdk.dev/guides/production.md).

## Qué evitar

- Armar SOAP o XML a mano, o sumar otra librería de ARCA en paralelo.
- Usar `client.wsfe` para emitir. Es el módulo de transporte. La emisión va por
  `issue()`, `issueCreditNote()` e `issueDebitNote()`.
- Calcular el IVA, la clase o el tipo de comprobante a mano.
- Importes en pesos con decimales en lugar de centavos.
- Reintentar una emisión sin `store` ni `idempotencyKey`.
- Pasar `service: "wsmtxca"` en las opciones sin que el contribuyente o el
  punto de venta lo requiera. WSFE es el valor por defecto.
- Probar en producción antes de homologación.

## Documentación en Markdown

- [Inicio rápido](https://facturas-sdk.dev/getting-started/quickstart.md)
- [Habilitación en ARCA](https://facturas-sdk.dev/getting-started/arca-setup.md)
- [Emitir facturas](https://facturas-sdk.dev/guides/invoices.md)
- [Notas de crédito y débito](https://facturas-sdk.dev/guides/credit-notes.md)
- [Evitar duplicados](https://facturas-sdk.dev/guides/avoid-duplicates.md)
- [Consultar contribuyentes en el Padrón](https://facturas-sdk.dev/guides/taxpayers.md)
- [Pasar a producción](https://facturas-sdk.dev/guides/production.md)
- [Cliente, firmas y resultados](https://facturas-sdk.dev/reference/client.md)
- [Configuración](https://facturas-sdk.dev/reference/configuration.md)
- [Errores](https://facturas-sdk.dev/reference/errors.md)
- [Comandos del CLI](https://facturas-sdk.dev/reference/cli.md)
