---
name: kubernetes_helm
description: Orquestación de contenedores en producción con Helm para gestionar releases versionadas
type: Tool
priority: Esencial
mode: Self-hosted
---

# kubernetes_helm

Kubernetes gestiona el ciclo de vida de todos los microservicios KYC en producción: scheduling, scaling, health checks y rolling deployments. Helm empaqueta los manifiestos como charts versionados y reproducibles.

## When to use

Usar para el despliegue en staging y producción. Docker Compose es solo para desarrollo local. El chart de Helm debe poder deployar el sistema completo con `helm install kyc ./charts/kyc`.

## Instructions

1. Estructura del chart en `charts/kyc/`:
   ```
   charts/kyc/
   ├── Chart.yaml
   ├── values.yaml
   ├── values-prod.yaml
   └── templates/
       ├── deployment-api.yaml
       ├── deployment-worker.yaml
       ├── service.yaml
       ├── ingress.yaml
       ├── hpa.yaml
       └── configmap.yaml
   ```
2. Definir recursos en `values.yaml`:
   ```yaml
   api:
     replicaCount: 3
     image: { repository: registry.company.com/kyc-api, tag: latest }
     resources:
       requests: { cpu: "500m", memory: "512Mi" }
       limits: { cpu: "2000m", memory: "2Gi" }
   worker_gpu:
     replicaCount: 2
     resources:
       limits: { nvidia.com/gpu: 1 }
   ```
3. Configurar HPA para workers CPU: `minReplicas: 2, maxReplicas: 10, targetCPUUtilizationPercentage: 70`.
4. Rolling update strategy: `maxSurge: 1, maxUnavailable: 0` — siempre hay instancias disponibles durante el deploy.
5. Usar `helm upgrade --install kyc ./charts/kyc -f values-prod.yaml` para deploys idempotentes.
6. Guardar el state de Helm en el cluster — `helm history kyc` muestra todos los releases y permite rollback.

## Notes

- Nunca modificar los manifiestos directamente en el cluster — siempre via `helm upgrade`. GitOps (ArgoCD) garantiza esto.
- Los GPU workers deben tener `nodeSelector: { gpu: "true" }` y tolerations para los taints de nodos GPU.
- Usar Helmfile si hay múltiples charts interdependientes (postgres, redis, kyc-api) para gestionarlos juntos.