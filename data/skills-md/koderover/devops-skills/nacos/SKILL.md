---
name: nacos
description: Nacos 配置中心操作。用于：(1) 查询 Nacos 配置 (2) 发布/更新配置 (3) 删除配置 (4) 管理命名空间。环境变量：NACOS_URL, NACOS_USERNAME, NACOS_PASSWORD
---

# Nacos Skill

## 配置

```bash
# ~/.openclaw/workspace/.env
NACOS_URL=http://nacos.example.com
NACOS_USERNAME=nacos
NACOS_PASSWORD=
```

## 访问方式

### 方式 1: Kubernetes Port-Forward

```bash
kubectl port-forward -n nacos svc/nacos-cs 8848:8848 &
# 之后用 localhost:8848 访问
```

### 方式 2: Ingress

```bash
# Nacos 可能有 ingress: nacos.example.com
curl -s "$NACOS_URL/nacos/v1/cs/configs?dataId=xxx"
```

## Nacos 命名空间

| Namespace ID | 名称 | 用途 |
|--------------|------|------|
| (空) | public | 默认 |
| 7a80d936-2a86-4016-a48c-97650baa11d9 | dev | 开发环境 |
| 6f1747c5-be1e-4e0b-9dc7-ccc300147949 | sit | 测试环境 |
| 2262b60c-e7c3-40a9-b0af-2eba5c6ba94f | prod | 生产环境 |

## 操作示例

### 登录获取 Token

```bash
source ~/.openclaw/workspace/.env
TOKEN=$(curl -s -X POST "$NACOS_URL/nacos/v1/auth/users/login" \
  -d "username=$NACOS_USERNAME&password=$NACOS_PASSWORD" | jq -r '.accessToken')
```

### 查询配置

```bash
source ~/.openclaw/workspace/.env

# 获取单个配置
curl -s "$NACOS_URL/nacos/v1/cs/configs?dataId=service1&group=DEFAULT_GROUP&tenant=dev&accessToken=$TOKEN"

# 列出配置（需要分页）
curl -s "$NACOS_URL/nacos/v1/cs/configs?search=accurate&dataId=&group=&tenant=dev&pageNo=1&pageSize=50&accessToken=$TOKEN"
```

### 发布配置

```bash
source ~/.openclaw/workspace/.env

# 发布/更新配置
curl -X POST "$NACOS_URL/nacos/v1/cs/configs" \
  -d "dataId=service1&group=DEFAULT_GROUP&tenant=dev&content=server.port=8080&type=properties&accessToken=$TOKEN"
```

### 删除配置

```bash
source ~/.openclaw/workspace/.env

curl -X DELETE "$NACOS_URL/nacos/v1/cs/configs?dataId=service1&group=DEFAULT_GROUP&tenant=dev&accessToken=$TOKEN"
```

### 命名空间操作

```bash
source ~/.openclaw/workspace/.env

# 获取命名空间列表
curl -s "$NACOS_URL/nacos/v1/console/namespaces?accessToken=$TOKEN"
```

## 使用场景

### 场景 1: 查询服务配置

查询 dev 环境中 service1 的配置：
```bash
source ~/.openclaw/workspace/.env

# 通过 port-forward 访问
kubectl port-forward -n nacos svc/nacos-cs 8848:8848 &
sleep 2
NACOS_URL="http://nacos.example.com:8848"

TOKEN=$(curl -s -X POST "$NACOS_URL/nacos/v1/auth/users/login" \
  -d "username=$NACOS_USERNAME&password=$NACOS_PASSWORD" | jq -r '.accessToken')

curl -s "$NACOS_URL/nacos/v1/cs/configs?dataId=service1&group=DEFAULT_GROUP&tenant=7a80d936-2a86-4016-a48c-97650baa11d9&accessToken=$TOKEN"
```

### 场景 2: 热更新配置

修改配置后即时生效，无需重启服务：
```bash
source ~/.openclaw/workspace/.env

TOKEN=$(curl -s -X POST "$NACOS_URL/nacos/v1/auth/users/login" \
  -d "username=$NACOS_USERNAME&password=$NACOS_PASSWORD" | jq -r '.accessToken')

curl -X POST "$NACOS_URL/nacos/v1/cs/configs" \
  -d "dataId=service1&group=DEFAULT_GROUP&tenant=dev&content=server.port=8080&type=properties&accessToken=$TOKEN"
```

### 场景 3: 批量导出配置

导出某个 namespace 所有配置用于备份：
```bash
source ~/.openclaw/workspace/.env

TOKEN=$(curl -s -X POST "$NACOS_URL/nacos/v1/auth/users/login" \
  -d "username=$NACOS_USERNAME&password=$NACOS_PASSWORD" | jq -r '.accessToken')

# 获取配置列表
curl -s "$NACOS_URL/nacos/v1/cs/configs?search=accurate&dataId=&group=&tenant=dev&pageNo=1&pageSize=100&accessToken=$TOKEN" | jq '.pageItems[] | {dataId, group, content}'
```

## 注意事项

- Nacos 认证信息根据部署情况可能不同
- 配置类型 (type) 常见: properties, json, yaml, xml
- tenant 参数对应 namespace ID，不是名称
