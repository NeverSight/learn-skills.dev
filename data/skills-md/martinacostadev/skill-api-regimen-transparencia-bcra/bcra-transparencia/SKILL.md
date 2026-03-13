---
name: bcra-transparencia
description: "Consulta la API pública del Régimen de Transparencia del BCRA. Permite buscar y comparar productos financieros de entidades argentinas: cajas de ahorro, plazos fijos, préstamos (personales, hipotecarios, prendarios), tarjetas de crédito y paquetes de productos. Usa cuando el usuario pregunte sobre tasas, comisiones, productos bancarios argentinos, o quiera comparar ofertas entre bancos."
---

# BCRA Transparencia

Skill para consultar la API pública del Régimen de Transparencia del Banco Central de la República Argentina (BCRA).

## Cuándo usar esta skill

Usá esta skill cuando el usuario:

- Pregunte sobre tasas de interés de bancos argentinos
- Quiera comparar productos financieros entre entidades
- Necesite información sobre plazos fijos, préstamos, cajas de ahorro o tarjetas de crédito
- Pregunte por comisiones bancarias en Argentina
- Mencione el BCRA, bancos argentinos, o productos bancarios del sistema financiero argentino

## API

- **Base URL**: `https://api.bcra.gob.ar/transparencia/v1.0/`
- **Autenticación**: Ninguna (API pública)
- **Método**: GET
- **Respuesta**: JSON `{ status, results: [...] }`

### Endpoints disponibles

| Endpoint | Descripción | Uso típico |
|---|---|---|
| `/CajasAhorros` | Cajas de ahorro | Costos de mantenimiento, requisitos |
| `/PaquetesProductos` | Paquetes de productos bancarios | Combos de servicios bancarios |
| `/PlazosFijos` | Plazos fijos | Tasas de interés, montos mínimos |
| `/Prestamos/Prendarios` | Préstamos prendarios | Tasas para compra de vehículos |
| `/Prestamos/Hipotecarios` | Préstamos hipotecarios | Tasas y condiciones de hipotecas |
| `/Prestamos/Personales` | Préstamos personales | Tasas y condiciones de préstamos |
| `/TarjetasCredito` | Tarjetas de crédito | Costos, comisiones, seguros |

Todos aceptan `?codigoEntidad=<int>` como filtro opcional para consultar una entidad específica.

## Cómo consultar

Usá el script `bcra_query.mjs` para hacer consultas:

```bash
# Consultar todos los plazos fijos
node ~/.agents/skills/bcra-transparencia/scripts/bcra_query.mjs PlazosFijos

# Consultar cajas de ahorro del Banco Nación (entidad 11)
node ~/.agents/skills/bcra-transparencia/scripts/bcra_query.mjs CajasAhorros --entidad 11

# Consultar préstamos personales de una entidad
node ~/.agents/skills/bcra-transparencia/scripts/bcra_query.mjs Prestamos/Personales --entidad 44
```

## Códigos de entidad comunes

| Código | Entidad |
|---|---|
| 11 | Banco de la Nación Argentina |
| 14 | Banco de la Provincia de Buenos Aires |
| 17 | Banco de la Ciudad de Buenos Aires |
| 44 | Banco Santander Argentina |
| 7 | Banco de Galicia y Buenos Aires |
| 15 | Banco Macro |
| 34 | Banco Patagonia |
| 72 | Banco HSBC |
| 97 | Banco Provincia de Neuquén |
| 285 | Banco Macro (ex Bisel) |

Si no conocés el código de entidad, consultá sin filtro y buscá la entidad en los resultados.

## Guía de uso

1. **Identificá el endpoint** según lo que pregunte el usuario
2. **Ejecutá el script** con el endpoint y opcionalmente el código de entidad
3. **Analizá los resultados** y presentá la información de forma clara
4. **Compará** si el usuario quiere ver diferencias entre entidades

Para detalles completos de campos y respuestas, consultá `references/api-reference.md`.
