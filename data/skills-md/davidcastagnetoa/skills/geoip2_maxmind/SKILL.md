---
name: geoip2_maxmind
description: Geolocalización por IP con base de datos descargable MaxMind GeoLite2
type: Library
priority: Recomendada
mode: Self-hosted
---

# geoip2_maxmind

GeoIP2 con la base de datos GeoLite2 de MaxMind permite geolocalizar IPs sin depender de APIs externas. La base de datos se descarga localmente y se actualiza periódicamente.

## When to use

Usar en el `antifraud_agent` para verificar coherencia entre la IP del usuario y la nacionalidad del documento. Una IP de un país diferente al del documento es una señal de riesgo (no bloqueante).

## Instructions

1. Instalar: `pip install geoip2`.
2. Registrarse en MaxMind y obtener license key para GeoLite2.
3. Descargar GeoLite2-Country.mmdb: `geoipupdate` o descarga manual.
4. Cargar base de datos: `reader = geoip2.database.Reader('GeoLite2-Country.mmdb')`.
5. Consultar IP: `response = reader.country(ip_address)`.
6. Comparar: `response.country.iso_code` vs nacionalidad del documento.
7. Si no coinciden, agregar flag `geo_mismatch` con peso moderado en el score de fraude.

## Notes

- GeoLite2 es gratuita pero menos precisa que GeoIP2 comercial (~99.5% vs ~99.8% a nivel país).
- Actualizar la base de datos semanalmente con `geoipupdate` en un cron job.
- No bloquear por geolocalización sola; muchos usuarios legítimos viajan o usan roaming.