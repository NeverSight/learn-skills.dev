---
name: ip_blacklist_whitelist
description: Bloqueo de IPs maliciosas y rangos no permitidos antes de que lleguen a los servicios
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# ip_blacklist_whitelist

El bloqueo de IPs en Nginx/Redis es la defensa más eficiente contra atacantes conocidos: IPs baneadas por rate limiting, rangos de datacenter asociados a fraud farms, y IPs en listas negras de abuso.

## When to use

Usar como primera capa de filtrado en Nginx, antes del JWT validation y del rate limiter. Las IPs bloqueadas reciben un 403 inmediato sin consumir recursos de los agentes KYC.

## Instructions

1. Usar módulo GeoIP2 de Nginx: `ngx_http_geoip2_module` para bloquear por país si aplica.
2. Blacklist estática en `/etc/nginx/conf.d/blacklist.conf`:
   ```nginx
   geo $blocked_ip {
       default 0;
       10.0.0.1 1;
       192.168.1.0/24 1;
   }
   ```
3. Integrar con Redis para blacklist dinámica via lua-resty-redis:
   ```lua
   local redis = require "resty.redis"
   local red = redis:new()
   red:connect("redis", 6379)
   local blocked = red:get("ip:blocked:" .. ngx.var.remote_addr)
   if blocked == "1" then ngx.exit(403) end
   ```
4. Cuando `rate_limiter` detecta abuso, escribir en Redis `ip:blocked:{ip}` con TTL de 24h.
5. Mantener lista de rangos de Tor exit nodes actualizada (descargar de `check.torproject.org/exit-addresses`).
6. Para whitelisting de IPs de partners internos, usar variable de entorno `TRUSTED_IPS`.

## Notes

- Las IPs de Tor y proxies conocidos deben tratarse con nivel de riesgo elevado, no necesariamente bloqueadas — depende de la política del negocio.
- Sincronizar la blacklist entre múltiples instancias de Nginx via Redis compartido.
- Auditar la blacklist semanalmente — las IPs cambian de dueño.