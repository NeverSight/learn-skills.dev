---
name: floci
description: Emulação local de AWS (e fluxo CI) com Floci — endpoint 4566, SDKs, Docker Compose, S3/SQS/DynamoDB/Lambda e persistência. Use ao configurar Floci, apontar AWS SDK/CLI/Terraform para localhost ou testar integrações cloud sem conta AWS.
---

# Floci

Floci emula serviços AWS na sua máquina (dev/CI) sem conta cloud. Aponte SDK, CLI e IaC para o endpoint — mesmos workflows, credenciais dummy.

> Nome do produto: **Floci** (`floci-io/floci`). Endpoint default: `http://localhost:4566`.

## Stack e escopo

| Peça | Papel |
|------|--------|
| **floci/floci** | Imagem Docker / runtime do emulador |
| **:4566** | Endpoint AWS-compatible único |
| **AWS SDK / CLI / Terraform** | Clientes existentes com `endpoint_url` |
| **Volume `/app/data`** | Persistência local opcional |

Há emuladores irmãos (Azure/GCP/OCI) no ecossistema Floci; esta skill foca no emulador **AWS** (`floci/floci`).

## Subir Floci

```yaml
# docker-compose.yml
services:
  floci:
    image: floci/floci:latest
    ports:
      - "4566:4566"
    volumes:
      - ./data:/app/data
```

```bash
docker compose up -d
```

- `latest` = imagem native (startup rápido). `latest-jvm` se precisar de compatibilidade de plataforma.
- Monte volume se quiser dados entre restarts.

## CLI e env

```bash
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

```bash
aws s3 mb s3://my-bucket
aws sqs create-queue --queue-name orders
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

Com `AWS_ENDPOINT_URL` setado, a CLI recente usa o emulador; senão passe `--endpoint-url`.

## SDKs

**Node (AWS SDK v3)** — S3 costuma exigir path-style:

```ts
import { S3Client } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  endpoint: "http://localhost:4566",
  region: "us-east-1",
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
  forcePathStyle: true,
});
```

**Python (boto3)**:

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)
```

**Go**: configure endpoint no config do AWS SDK v2 (base-endpoint / resolver do projeto) apontando para `http://localhost:4566`, região e credenciais dummy.

- Centralize endpoint via env (`AWS_ENDPOINT_URL` / config do app) — nunca hardcode só em um client.
- Em Docker Compose com app em outro container: use hostname do serviço (`http://floci:4566`) e, se docs do Floci pedirem, `FLOCI_HOSTNAME` para URLs resolvíveis entre containers.

## Serviços comuns em testes

| Serviço | Uso típico em dev/CI |
|---------|----------------------|
| S3 | Upload/download, presign (conforme suporte) |
| SQS / SNS | Filas e pub/sub |
| DynamoDB | Tabelas on-demand |
| Secrets Manager / SSM | Config local |
| Lambda / ECR | Funções e imagens (requer Docker) |
| EventBridge / Step Functions | Orquestração local |

Verifique a superfície por serviço na docs do Floci — nem toda API AWS existe ou é completa.

## CI e práticas

- Suba Floci como serviço do job; smoke test (S3 mb + put) antes da suíte.
- Credenciais `test`/`test`; nunca aponte produção para Floci por engano (guarde endpoint atrás de env `APP_ENV=local|test`).
- Prefira asserts no comportamento do app a depender de detalhes internos do emulador.
- Serviços container-backed (Lambda, RDS, ElastiCache, etc.) precisam de Docker disponível no host/CI.

## Anti-padrões

- Misturar endpoint Floci com credenciais reais de produção
- Assumir 100% de parity com AWS sem checar a operação
- Hardcode `localhost:4566` dentro de libs compartilhadas sem override
- Esquecer `forcePathStyle` no S3 (SDK JS) e culpar o emulador
- Persistir dados sensíveis no volume de Floci sem cuidado

## Critérios de conclusão

- Floci sobe e responde no endpoint configurado
- CLI ou SDK consegue pelo menos um smoke test (S3/SQS/DDB)
- App local/CI aponta endpoint via config/env
- Credenciais dummy isoladas do ambiente prod
- Serviços usados pela feature cobertos pelo emulador (ou mock alternativo documentado)
