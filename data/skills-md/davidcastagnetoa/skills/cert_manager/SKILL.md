---
name: cert_manager
description: Emisión y renovación automática de certificados TLS en Kubernetes usando Let's Encrypt
type: Tool
priority: Esencial
mode: Self-hosted"
---

# cert_manager

cert-manager automatiza el ciclo de vida de los certificados TLS: solicitud, validación, emisión y renovación. Integrado con Let's Encrypt, garantiza que los certificados nunca expiran y elimina el trabajo manual de gestión de TLS.

## When to use

Usar en el cluster Kubernetes de producción para todos los servicios expuestos externamente (Nginx Ingress) e internamente (comunicaciones entre microservicios si no se usa Istio).

## Instructions

1. Instalar cert-manager en Kubernetes:
   ```bash
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
   ```
2. Crear `ClusterIssuer` para Let's Encrypt:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-prod
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: security@company.com
       privateKeySecretRef:
         name: letsencrypt-prod-key
       solvers:
         - http01:
             ingress:
               class: nginx
   ```
3. Añadir anotación en el Ingress de Nginx:
   ```yaml
   annotations:
     cert-manager.io/cluster-issuer: "letsencrypt-prod"
   spec:
     tls:
       - hosts: [api.kyc.company.com]
         secretName: kyc-api-tls
   ```
4. cert-manager renueva automáticamente 30 días antes de expiración.
5. Verificar estado: `kubectl get certificates -A` y `kubectl describe certificate kyc-api-tls`.
6. Para comunicaciones internas mTLS sin Istio, usar `ClusterIssuer` con CA propia (SelfSigned o Vault PKI).

## Notes

- Let's Encrypt tiene rate limits — en staging usar `letsencrypt-staging` para pruebas.
- Para dominios internos (`.svc.cluster.local`), usar una CA interna gestionada por Vault PKI Engine.
- Alertar con Prometheus si algún certificado expira en menos de 14 días (fallo del proceso de renovación).