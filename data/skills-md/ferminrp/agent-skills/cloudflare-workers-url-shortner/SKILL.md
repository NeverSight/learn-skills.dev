---
name: cloudflare-workers-url-shortner
description: >
  Build and operate a URL shortner on Cloudflare Workers with Upstash Redis and D1.
  Use when the user asks to create shortlinks, redirects, click tracking, analytics,
  request metadata capture (country/city/ip/user-agent), non-blocking tracking,
  or resilient alerting (for example Telegram) on failures.
---

# Cloudflare Workers URL Shortner

Guia practica para disenar un URL shortner rapido, resiliente y observable usando Cloudflare Workers + Upstash Redis + D1.

## Cuando usar esta skill

Usar cuando el usuario pida:

- Crear shortlinks (`/links/:id`, `/r/:slug`, etc.)
- Resolver redirects en Workers con baja latencia
- Contar clicks en Redis
- Guardar eventos de click en D1 con metadata de `request.cf`
- Mantener tracking non-blocking (el redirect nunca debe fallar por analytics)
- Alertar fallas de persistencia (por ejemplo Telegram) con throttle

## Arquitectura recomendada

### Objetivo principal

1. Resolver destination URL rapido.
2. Responder redirect inmediatamente.
3. Ejecutar tracking en background.
4. Si tracking falla, alertar sin romper UX.

### Componentes

- **Cloudflare Worker**:
  - Endpoint publico de redirect (`GET /links/:id`).
  - Lectura de target desde Redis.
  - `waitUntil()` para tracking async.
- **Upstash Redis**:
  - Lookup rapido de target por id/slug.
  - Contador de clicks (`INCR`).
  - Timestamp ultimo click.
  - Locks de throttle para alertas (`SET NX EX`).
- **D1**:
  - Tabla append-only de eventos de click para analitica detallada.
- **Canal de alertas** (ej. Telegram):
  - Notificar errores de persistencia degradada.
  - Throttle para evitar spam.

## Modelo de datos recomendado

### Redis (fast path)

- `shortlink:target:<id>`: URL destino
- `shortlink:clicks:<id>`: contador total
- `shortlink:last-clicked-at:<id>`: ISO timestamp
- `shortlink:alert-lock:d1-persist`: lock para throttle de alertas

### D1 (event log)

Mantener eventos por click (append-only) con:

- Identificadores:
  - `promo_id`/`link_id`
  - `clicked_at`, `clicked_at_unix_ms`
  - `destination_url`, `short_path`, `request_method`
- Red/cliente:
  - `ip_raw`, `ip_hash_sha256`
  - `cf_ray`, `cf_connecting_ipv6`
  - `user_agent`, `referer`, `accept_language`
  - `device_type`, `browser_family`, `os_family`
- Geografia y edge (`request.cf`):
  - `country`, `city`, `region`, `region_code`, `continent`
  - `timezone`, `postal_code`, `latitude`, `longitude`, `metro_code`
  - `colo`, `asn`, `as_organization`, `client_tcp_rtt`
  - `http_protocol`, `tls_version`, `tls_cipher`, `request_priority`
- Snapshots flexibles:
  - `cf_json`
  - `headers_json` (allowlist, no cookies/tokens)

## Metadata de Cloudflare: que capturar

### Desde `request.cf`

- Geografia: `country`, `city`, `region`, `regionCode`, `continent`, `timezone`, `postalCode`, `latitude`, `longitude`, `metroCode`, `isEUCountry`
- Red/edge: `colo`, `asn`, `asOrganization`, `clientTcpRtt`
- Transporte: `httpProtocol`, `tlsVersion`, `tlsCipher`, `requestPriority`
- Bot signals: `botManagement` (si disponible en plan/cuenta)

### Desde headers (allowlist)

- Cloudflare: `cf-connecting-ip`, `cf-connecting-ipv6`, `cf-ipcountry`, `cf-ray`
- Cliente: `user-agent`, `referer`, `accept-language`, `sec-ch-ua`, `sec-ch-ua-mobile`, `sec-ch-ua-platform`, `accept`, `accept-encoding`

### Derivados utiles

- `ip_hash_sha256` (opcionalmente con salt)
- `device_type` (mobile/desktop/tablet)
- `browser_family` (chrome/safari/firefox/edge/opera/other)
- `os_family` (ios/android/windows/macos/linux/other)

## Flujo recomendado del redirect

1. Validar param (`id`/`slug`).
2. Leer target en Redis.
3. Si no existe: `404`.
4. Si existe:
   - Lanzar `waitUntil(registerClickNonFatal(...))`
   - Responder `302`/`307` de inmediato.
5. En `registerClickNonFatal`:
   - `Promise.allSettled` para:
     - Redis metrics (`INCR` + `last-clicked-at`)
     - Insert D1 del evento enriquecido
6. Si falla D1:
   - Intentar lock Redis (`SET key 1 NX EX 900`)
   - Notificar Telegram solo si lock nuevo (`OK`)
7. Si falla Telegram: loggear y nunca throw.

## Buenas practicas clave

### Performance

- No bloquear redirect por tracking.
- Minimizar round-trips a Redis (pipeline cuando corresponda).
- Evitar operaciones costosas sync antes del `redirect`.

### Resiliencia

- Patrón best-effort para analytics.
- Usar `Promise.allSettled` en tareas de background.
- Alertas con throttle para fallas repetitivas.

### Seguridad y privacidad

- Guardar headers solo por allowlist.
- Nunca persistir `authorization`, `cookie` u otros secretos.
- Considerar IP hash + salt configurable.
- Evaluar retencion de eventos y purga periodica si aplica regulacion.

### Observabilidad

- Contextos de error claros (ej. `Shortlink D1 Persist`, `Shortlink Redis Tracking`).
- Incluir `link_id`, path y modo degradado en alertas.
- Crear queries operativas en D1:
  - total clicks por link
  - clicks por pais/ciudad
  - errores recientes de persistencia (si se registran aparte)

### Testing

Cubrir al menos:

- Redirect responde `302` aunque falle D1.
- Redirect responde `302` aunque falle Redis tracking.
- Tracking corre via `waitUntil`.
- D1 guarda metadata esperada (`country`, `city`, `cf_ray`, `ip_hash`).
- Headers sensibles no se persisten.
- Throttle de alertas funciona en ventana configurada.

## Operacion y rollout

1. Crear migracion D1 para tabla de eventos + indices.
2. Deploy del Worker.
3. Smoke test:
   - Redirect valido
   - Incremento Redis
   - Insert de evento en D1
4. Simular fallo D1 y verificar:
   - Redirect intacto
   - alerta Telegram (throttle aplicado)

## Skills complementarias recomendadas

- Wrangler (deploy/migrations/bindings):
  - [cloudflare/skills/wrangler](https://skills.sh/cloudflare/skills/wrangler)
- Cloudflare platform general:
  - `cloudflare`
- Durable Objects (si evoluciona a rate-limiter/stateful logic):
  - `durable-objects`

## Checklist rapido de implementacion

- [ ] Redis keyspace definido para targets/clicks/locks
- [ ] Handler de redirect con `waitUntil`
- [ ] Tracking Redis + D1 en paralelo (non-blocking)
- [ ] Alerta de fallas con throttle
- [ ] Sanitizacion de headers
- [ ] Hash de IP con salt opcional
- [ ] Tests de resiliencia y privacidad
- [ ] Migracion D1 aplicada y validada
