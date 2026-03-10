---
name: traefik
description: Reverse proxy moderno con autodiscovery nativo en Kubernetes y Let's Encrypt
type: Tool
priority: Recomendada
mode: Self-hosted"
---

# traefik

Traefik es un reverse proxy y load balancer moderno con autodiscovery de servicios en Kubernetes, Docker y otros orquestadores. Alternativa a Nginx con configuración declarativa y certificados automáticos.

## When to use

Usar como alternativa al `api_gateway_agent` basado en Nginx si se prefiere autodiscovery nativo en Kubernetes. Especialmente útil en entornos donde los servicios se escalan dinámicamente.

## Instructions

1. Desplegar en Kubernetes: `helm install traefik traefik/traefik`.
2. Configurar IngressRoute para el orquestador:
   ```yaml
   apiVersion: traefik.io/v1alpha1
   kind: IngressRoute
   spec:
     routes:
       - match: Host(`api.verifid.com`) && PathPrefix(`/v1`)
         services:
           - name: orchestrator
             port: 8000
   ```
3. Habilitar Let's Encrypt: configurar `certificatesResolvers` con ACME.
4. Configurar middleware de rate limiting y circuit breaker.
5. Habilitar dashboard en entorno de desarrollo: `--api.dashboard=true`.
6. Configurar health checks activos hacia los backends.
7. Exponer métricas Prometheus: `--metrics.prometheus=true`.

## Notes

- Traefik tiene mayor overhead que Nginx (~10-15% menos throughput) pero mejor DX.
- El autodiscovery elimina la necesidad de reconfigurar manualmente al escalar servicios.
- En producción de alto tráfico (>10K RPS), Nginx con Lua sigue siendo la opción más eficiente.