---
name: kubernetes_liveness_readiness_probes
description: Configuracion de probes de Kubernetes para pods del pipeline KYC con timeouts adaptados a servicios ML
type: Tool
priority: Esencial
mode: Self-hosted
---

# kubernetes_liveness_readiness_probes

Skill para configurar las probes de Kubernetes (liveness, readiness y startup) en los deployments de cada microservicio del pipeline de verificacion de identidad KYC. Los servicios de inferencia ML (face matching, liveness detection, OCR) requieren configuraciones especiales con timeouts mas generosos debido a los tiempos de carga de modelos en GPU y los picos de latencia durante inferencia. Una mala configuracion de probes causa reinicios innecesarios que degradan el servicio.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite configurar, ajustar o depurar las probes de Kubernetes para los pods del pipeline KYC. Es critica durante el despliegue inicial, cuando se observan reinicios inesperados de pods (CrashLoopBackOff), o cuando se actualizan modelos ML que cambian los tiempos de arranque.

## Instructions

1. Configurar la startup probe para servicios ML que necesitan cargar modelos pesados en memoria/GPU (ArcFace, liveness model):
```yaml
# deployment-face-match.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: face-match-service
  namespace: kyc-pipeline
spec:
  template:
    spec:
      containers:
      - name: face-match
        image: kyc/face-match:latest
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
          failureThreshold: 30  # 30 * 10s = 5 min max para cargar modelos
          timeoutSeconds: 5
```

2. Configurar la liveness probe para detectar si el proceso esta colgado (deadlock, OOM parcial):
```yaml
        livenessProbe:
          httpGet:
            path: /live
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 15
          failureThreshold: 3   # 3 fallos consecutivos = reinicio
          timeoutSeconds: 5
          successThreshold: 1
```

3. Configurar la readiness probe para controlar cuando el pod recibe trafico, mas estricta que liveness:
```yaml
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 2   # 2 fallos = dejar de recibir trafico
          timeoutSeconds: 5
          successThreshold: 2   # 2 exitos consecutivos para volver a recibir trafico
```

4. Configurar probes diferenciadas para servicios ligeros (decision engine, API gateway) con timeouts mas cortos:
```yaml
# deployment-decision-engine.yaml
spec:
  template:
    spec:
      containers:
      - name: decision-engine
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 3
          periodSeconds: 5
          failureThreshold: 6   # 30s max startup
          timeoutSeconds: 3
        livenessProbe:
          httpGet:
            path: /live
            port: 8000
          periodSeconds: 10
          failureThreshold: 3
          timeoutSeconds: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          periodSeconds: 5
          failureThreshold: 2
          timeoutSeconds: 3
          successThreshold: 1
```

5. Configurar probes para el servicio de OCR que es CPU-intensivo y puede tener picos de latencia:
```yaml
# deployment-ocr.yaml
spec:
  template:
    spec:
      containers:
      - name: ocr-service
        resources:
          requests:
            cpu: "2"
            memory: "4Gi"
          limits:
            cpu: "4"
            memory: "8Gi"
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 18  # 3 min max para cargar PaddleOCR
          timeoutSeconds: 5
        livenessProbe:
          httpGet:
            path: /live
            port: 8000
          periodSeconds: 15
          failureThreshold: 3
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          periodSeconds: 10
          failureThreshold: 2
          timeoutSeconds: 5
```

6. Agregar configuracion de recursos y QoS class Guaranteed para pods criticos de inferencia:
```yaml
# Pod con GPU para face matching
spec:
  template:
    spec:
      containers:
      - name: face-match
        resources:
          requests:
            cpu: "1"
            memory: "4Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "2"
            memory: "8Gi"
            nvidia.com/gpu: "1"
```

7. Configurar PodDisruptionBudget para asegurar disponibilidad minima durante rolling updates:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: face-match-pdb
  namespace: kyc-pipeline
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: face-match-service
```

8. Implementar un script de validacion que verifique que las probes estan correctamente configuradas en todos los deployments:
```bash
#!/bin/bash
SERVICES=("face-match" "liveness" "ocr" "doc-processing" "antifraud" "decision-engine")
for svc in "${SERVICES[@]}"; do
  echo "Checking probes for $svc..."
  kubectl get deployment "$svc-service" -n kyc-pipeline -o jsonpath='{.spec.template.spec.containers[0].startupProbe}' | jq .
  kubectl get deployment "$svc-service" -n kyc-pipeline -o jsonpath='{.spec.template.spec.containers[0].livenessProbe}' | jq .
  kubectl get deployment "$svc-service" -n kyc-pipeline -o jsonpath='{.spec.template.spec.containers[0].readinessProbe}' | jq .
done
```

## Notes

- Siempre usar startup probe para servicios ML; sin ella, la liveness probe puede reiniciar el pod antes de que el modelo termine de cargarse, causando un CrashLoopBackOff infinito. Un modelo ArcFace puede tardar 60-120 segundos en cargar en GPU.
- La liveness probe debe ser ligera (endpoint /live que solo verifica que el proceso responde); nunca ejecutar inferencia ML en la liveness probe porque bajo carga un timeout en la inferencia causaria reinicios en cascada.
- Monitorizar los eventos de restart de pods (`kubectl get events`) como metrica del health_monitor_agent; un pod que se reinicia mas de 3 veces en una hora indica que los thresholds de las probes necesitan ajuste.
