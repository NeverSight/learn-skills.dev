---
name: kratos-skills
description: |
  Comprehensive knowledge base for go-kratos microservices framework.

  **Use this skill when:**
  - Building REST/gRPC APIs with kratos (Service → Biz → Data layered architecture)
  - Creating microservices with DDD and Clean Architecture patterns
  - Implementing dependency injection with Wire
  - Configuring service discovery, load balancing, and resilience patterns
  - Troubleshooting kratos issues or understanding framework conventions
  - Generating production-ready microservices code with Protobuf

  **Features:**
  - Complete pattern guides with ✅ correct and ❌ incorrect examples
  - DDD/Clean Architecture enforcement
  - Production best practices
  - Common pitfall solutions
license: MIT
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Kratos Skills for AI Agents

This skill provides comprehensive go-kratos microservices framework knowledge, optimized for AI agents helping developers build production-ready services.

## 🎯 When to Use This Skill

Invoke this skill when working with go-kratos:
- **Creating services**: REST APIs, gRPC services, or microservices architectures
- **Layered architecture**: Implementing Service → Biz → Data layers with DDD
- **Dependency injection**: Using Wire for compile-time DI
- **Production hardening**: Circuit breakers, rate limiting, middleware
- **Debugging**: Understanding errors, fixing configuration, or resolving issues
- **Learning**: Understanding kratos patterns and best practices

## 📚 Knowledge Structure

**Load specific guides as needed** rather than reading everything at once:

### Quick Start
**Link**: [Official Kratos Documentation](https://go-kratos.dev/docs/getting-started/start)
**Contains**: Installation, project creation, basic commands, hello-world examples

### Pattern Guides

#### API & Transport
| File | When to Load |
|------|-------------|
| [references/api-patterns.md](references/api-patterns.md) | Defining Protobuf APIs, generating HTTP/gRPC code |
| [references/transport-patterns.md](references/transport-patterns.md) | HTTP/gRPC server/client configuration |
| [references/encoding-patterns.md](references/encoding-patterns.md) | Custom serialization, content negotiation |
| [references/openapi-guide.md](references/openapi-guide.md) | OpenAPI/Swagger documentation generation |

#### Architecture & Design
| File | When to Load |
|------|-------------|
| [references/architecture-patterns.md](references/architecture-patterns.md) | DDD layers, repository pattern, Wire DI |
| [references/error-patterns.md](references/error-patterns.md) | Error definition, assertions, proto errors |
| [references/middleware-patterns.md](references/middleware-patterns.md) | Custom middleware, request filtering |

#### Infrastructure
| File | When to Load |
|------|-------------|
| [references/config-patterns.md](references/config-patterns.md) | Configuration loading, hot reload, config centers |
| [references/registry-patterns.md](references/registry-patterns.md) | Service discovery (etcd, consul, nacos, k8s) |
| [references/selector-patterns.md](references/selector-patterns.md) | Load balancing (P2C, WRR, random) |

#### Resilience & Reliability
| File | When to Load |
|------|-------------|
| [references/circuit-breaker-patterns.md](references/circuit-breaker-patterns.md) | Fault tolerance, SRE circuit breaker |
| [references/ratelimit-patterns.md](references/ratelimit-patterns.md) | Token bucket, BBR rate limiting |
| [references/recovery-patterns.md](references/recovery-patterns.md) | Panic recovery, stack trace logging |

#### Observability
| File | When to Load |
|------|-------------|
| [references/logging-patterns.md](references/logging-patterns.md) | Structured logging, Zap/Logrus adapters |
| [references/metrics-patterns.md](references/metrics-patterns.md) | Prometheus metrics collection |
| [references/tracing-patterns.md](references/tracing-patterns.md) | OpenTelemetry, Jaeger/Zipkin tracing |
| [references/metadata-patterns.md](references/metadata-patterns.md) | Context propagation, trace IDs |

#### Security & Validation
| File | When to Load |
|------|-------------|
| [references/auth-patterns.md](references/auth-patterns.md) | JWT authentication, claims, token generation |
| [references/validate-patterns.md](references/validate-patterns.md) | Proto field validation, protoc-gen-validate |

#### Data & Tools
| File | When to Load |
|------|-------------|
| [references/ent-patterns.md](references/ent-patterns.md) | Ent ORM integration, schema design |
| [references/cli-guide.md](references/cli-guide.md) | kratos CLI, code generation commands |

### Supporting Resources

| File | When to Load |
|------|-------------|
| [best-practices/overview.md](best-practices/overview.md) | Production deployment, code review checklist |
| [troubleshooting/common-issues.md](troubleshooting/common-issues.md) | Debugging errors, protoc/wire issues |
| [getting-started/claude-code-guide.md](getting-started/claude-code-guide.md) | Claude Code integration, advanced features |

## 🚀 Common Workflows

### Creating a New Service

1. **Create project**: `kratos new <project-name>`
2. **Define API**: Create `.proto` with google.api.http annotations
3. **Generate code**: `kratos proto client api/demo/v1/demo.proto`
4. **Generate service**: `kratos proto server api/demo/v1/demo.proto -t internal/service`
5. **Implement layers**: Biz logic in `internal/biz/`, data access in `internal/data/`
6. **Configure Wire**: Update `cmd/server/wire.go` with provider sets
7. **Run**: `go generate ./... && kratos run`

**Details**: [references/api-patterns.md](references/api-patterns.md)

### Implementing Layered Architecture

1. **Define interfaces** in `internal/biz/` (biz layer)
2. **Implement repositories** in `internal/data/` (data layer)
3. **Write use cases** in `internal/biz/` (biz layer)
4. **Implement handlers** in `internal/service/` (service layer)
5. **Create ProviderSets**: `data.ProviderSet`, `biz.ProviderSet`, `service.ProviderSet`
6. **Wire together** in `cmd/server/wire.go`

**Details**: [references/architecture-patterns.md](references/architecture-patterns.md)

### Adding Middleware

```go
http.Middleware(
    recovery.Recovery(),           // 1. Catch panics first
    validate.Validator(),          // 2. Validate requests
    jwt.Server(keyFunc),           // 3. Authentication
    ratelimit.Server(limiter),     // 4. Rate limiting
    logging.Server(logger),        // 5. Logging
)
```

**Details**: [references/middleware-patterns.md](references/middleware-patterns.md)

### Configuring Service Discovery

```go
// Server-side
reg := etcd.New(client)
app := kratos.New(kratos.Registrar(reg))

// Client-side
dis := etcd.New(client)
conn, _ := grpc.DialInsecure(
    context.Background(),
    grpc.WithEndpoint("discovery:///service-name"),
    grpc.WithDiscovery(dis),
)
```

**Details**: [references/registry-patterns.md](references/registry-patterns.md)

## ⚡ Key Principles

### ✅ Always Follow

- **Layer separation**: Service (API) → Biz (Business) → Data (Persistence)
- **Dependency Inversion**: Interfaces in biz, implementations in data
- **Protobuf-first**: Define APIs and errors in `.proto` files
- **Wire injection**: Compile-time DI, no global state
- **Context propagation**: Pass `ctx context.Context` through all layers
- **Interface-based design**: Program to interfaces, not implementations
- **Error codes**: Structured errors with code, reason, message, metadata

### ❌ Never Do

- Put business logic in service handlers (violates layered architecture)
- Skip interface definition and use concrete types directly
- Use global variables for dependencies
- Define HTTP handlers manually (use generated code from proto)
- Hard-code configuration values
- Skip validation or forget to check `err != nil`
- Modify generated `.pb.go` files

## 📖 Progressive Learning Path

### 🟢 New to kratos?
1. [Official Quick Start](https://go-kratos.dev/docs/getting-started/start) - Install CLI, create first project
2. [references/architecture-patterns.md](references/architecture-patterns.md) - Understand Service → Biz → Data
3. [references/api-patterns.md](references/api-patterns.md) - Learn Protobuf API definition

### 🟡 Building production services?
1. [best-practices/overview.md](best-practices/overview.md) - Production checklist
2. [references/circuit-breaker-patterns.md](references/circuit-breaker-patterns.md) + [references/ratelimit-patterns.md](references/ratelimit-patterns.md) - Add resilience
3. [references/registry-patterns.md](references/registry-patterns.md) - Service discovery
4. [troubleshooting/common-issues.md](troubleshooting/common-issues.md) - Avoid pitfalls

### 🔵 Extending capabilities?
1. [getting-started/claude-code-guide.md](getting-started/claude-code-guide.md) - Advanced Claude Code features
2. [Kratos Examples](https://github.com/go-kratos/examples) - Example projects

## 🔗 Kratos Ecosystem

| Project | Purpose |
|---------|---------|
| [kratos](https://github.com/go-kratos/kratos) | Framework core, CLI tools |
| [kratos-layout](https://github.com/go-kratos/kratos-layout) | Official project template |
| [contrib](https://github.com/go-kratos/kratos/tree/main/contrib) | Plugins for config, registry, log, metrics |
| [aegis](https://github.com/go-kratos/aegis) | Availability algorithms |
| [gateway](https://github.com/go-kratos/gateway) | API Gateway |
| [examples](https://github.com/go-kratos/examples) | Example code |

## 📝 Version Compatibility

- **Target version**: kratos v2.0.0+
- **Go version**: Go 1.19 or later recommended
- **Protoc**: 3.0+

---

**Quick invocation**: Use `/kratos-skills` or ask "How do I [task] with kratos?"
