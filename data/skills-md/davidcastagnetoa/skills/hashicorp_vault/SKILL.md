---
name: hashicorp_vault
description: Gestor centralizado de secretos con auditoría, rotación automática y lease management
type: Tool
priority: Esencial
mode: Self-hosted
---

# hashicorp_vault

HashiCorp Vault es el almacén central de todos los secretos del sistema: credenciales de BBDD, claves de cifrado, API keys. Ningún secreto debe estar en código o variables de entorno en texto plano.

## When to use

Usar para gestionar todos los secretos del sistema. Los servicios deben obtener secretos de Vault en tiempo de ejecución.

## Instructions

1. Instalar y lanzar Vault en Kubernetes: usar el Helm chart oficial: `helm install vault hashicorp/vault`.
2. Inicializar y unseal: `vault operator init -key-shares=5 -key-threshold=3`.
3. Habilitar el secrets engine KV v2: `vault secrets enable -path=kyc kv-v2`.
4. Almacenar secretos: `vault kv put kyc/database password="secret"`.
5. Configurar autenticación Kubernetes: `vault auth enable kubernetes`.
6. En el código Python: usar `hvac` para obtener secretos: `pip install hvac`. `client = hvac.Client(url='http://vault:8200', token=os.getenv('VAULT_TOKEN'))`. `secret = client.secrets.kv.v2.read_secret_version(path='database')`.
7. Activar auditing: `vault audit enable file file_path=/vault/logs/audit.log`.

## Notes

- Documentación: https://developer.hashicorp.com/vault
- Dynamic secrets para BBDD: Vault genera credenciales PostgreSQL con TTL corto para cada servicio.
- Usar Vault Agent Injector en Kubernetes para inyección automática de secretos en pods.