---
name: grpc_server
description: Servidor gRPC de alto rendimiento para comunicación entre microservicios de inferencia ML del pipeline KYC
type: Protocol
priority: Esencial
mode: Self-hosted
---

# grpc_server

Implementa un servidor gRPC para la comunicación de baja latencia entre los microservicios de inferencia del sistema de verificación de identidad. Reemplaza las llamadas REST entre servicios internos (face recognition, liveness detection, OCR, anti-spoofing) con comunicación binaria serializada mediante Protocol Buffers, reduciendo significativamente la latencia y el overhead de red en el pipeline.

## When to use

Usa esta skill cuando necesites implementar o configurar la comunicación gRPC entre microservicios de inferencia dentro del **model_server_agent**. Aplica cuando la latencia de comunicación REST entre servicios internos impacte el objetivo de tiempo de respuesta total de 8 segundos del pipeline de verificación.

## Instructions

1. Definir los servicios y mensajes en archivos `.proto` para cada módulo de inferencia:
   ```protobuf
   syntax = "proto3";
   package kyc.inference;

   service FaceRecognitionService {
       rpc GetEmbedding (FaceRequest) returns (EmbeddingResponse);
       rpc CompareFaces (FaceCompareRequest) returns (MatchResponse);
   }

   message FaceRequest {
       bytes image_data = 1;
       string session_id = 2;
   }

   message EmbeddingResponse {
       repeated float embedding = 1;
       float confidence = 2;
       int64 inference_time_ms = 3;
   }

   message MatchResponse {
       float similarity_score = 1;
       bool is_match = 2;
       float threshold_used = 3;
   }
   ```

2. Generar el código Python a partir de los archivos proto:
   ```bash
   python -m grpc_tools.protoc -I./protos \
     --python_out=./generated \
     --grpc_python_out=./generated \
     protos/face_recognition.proto
   ```

3. Implementar el servidor gRPC con el servicio de inferencia:
   ```python
   import grpc
   from concurrent import futures
   from generated import face_recognition_pb2_grpc as pb2_grpc

   class FaceRecognitionServicer(pb2_grpc.FaceRecognitionServiceServicer):
       def __init__(self, model_runner):
           self.model = model_runner

       def GetEmbedding(self, request, context):
           image = self._deserialize_image(request.image_data)
           embedding = self.model.predict(image)
           return EmbeddingResponse(embedding=embedding.tolist())

   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   pb2_grpc.add_FaceRecognitionServiceServicer_to_server(servicer, server)
   server.add_insecure_port('[::]:50051')
   server.start()
   ```

4. Configurar interceptores para logging, métricas y autenticación entre servicios:
   ```python
   class MetricsInterceptor(grpc.ServerInterceptor):
       def intercept_service(self, continuation, handler_call_details):
           start_time = time.time()
           response = continuation(handler_call_details)
           latency = time.time() - start_time
           metrics.record_grpc_latency(handler_call_details.method, latency)
           return response
   ```

5. Implementar el cliente gRPC para que los servicios consumidores (API gateway, motor de decisión) invoquen la inferencia:
   ```python
   channel = grpc.insecure_channel('model-server:50051')
   stub = pb2_grpc.FaceRecognitionServiceStub(channel)
   response = stub.GetEmbedding(FaceRequest(image_data=image_bytes, session_id=session_id))
   ```

6. Configurar health checking gRPC para integración con Kubernetes readiness/liveness probes:
   ```python
   from grpc_health.v1 import health_pb2_grpc, health
   health_servicer = health.HealthServicer()
   health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
   ```

7. Habilitar compresión gzip para las imágenes transmitidas entre servicios y configurar timeouts apropiados para cada tipo de llamada de inferencia.

## Notes

- Usar comunicación gRPC solo para la capa interna entre microservicios de inferencia; la API pública del sistema KYC debe mantener REST/HTTP para compatibilidad con clientes frontend.
- La serialización binaria de Protocol Buffers reduce significativamente el tamaño de las imágenes transmitidas entre servicios comparado con JSON/base64, lo cual es crítico para el pipeline facial donde se transfieren múltiples imágenes por verificación.
- Configurar deadlines (timeouts) por tipo de llamada: face embedding (~500ms), liveness check (~1s), face comparison (~300ms) para evitar que un servicio lento bloquee el pipeline completo.
