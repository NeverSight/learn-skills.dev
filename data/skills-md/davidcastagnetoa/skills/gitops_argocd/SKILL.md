---
name: gitops_argocd
description: GitOps — el estado del clúster Kubernetes refleja siempre el estado del repositorio Git
type: Tool
priority: Recomendada
mode: Self-hosted
---

# gitops_argocd

ArgoCD sincroniza automáticamente el estado del clúster Kubernetes con los manifiestos/charts del repositorio Git. Esto garantiza que nadie puede modificar la configuración del cluster manualmente y que el repositorio es la única fuente de verdad.

## When to use

Implementar antes del primer deploy a producción. ArgoCD detecta cualquier drift entre el estado deseado (Git) y el estado real (cluster) y puede corregirlo automáticamente o alertar.

## Instructions

1. Instalar ArgoCD en el cluster:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
2. Crear `Application` de ArgoCD apuntando al chart de Helm:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: kyc-production
   spec:
     source:
       repoURL: https://github.com/company/kyc-system
       targetRevision: main
       path: charts/kyc
       helm:
         valueFiles: [values-prod.yaml]
     destination:
       server: https://kubernetes.default.svc
       namespace: kyc-prod
     syncPolicy:
       automated: { prune: true, selfHeal: true }
   ```
3. `selfHeal: true` — ArgoCD revierte cambios manuales en el cluster automáticamente.
4. `prune: true` — elimina recursos del cluster que se han eliminado del repo.
5. Configurar notificaciones de ArgoCD a Slack para sync success/failure.
6. Image updater: instalar `argocd-image-updater` para que ArgoCD detecte nuevas imágenes en el registry y abra PRs automáticamente.

## Notes

- Con ArgoCD, `kubectl apply` directo en producción está prohibido — todos los cambios van via Git PR.
- El acceso a ArgoCD UI debe estar protegido con SSO (integrar con Keycloak o GitHub OAuth).
- Guardar las credenciales de repositorio de ArgoCD en Vault, no en el cluster directamente.