---
name: docker-compose-orchestration
description: Container orchestration with Docker Compose for multi-container applications, networking, volumes, and production deployment
---

# Docker Compose Orchestration

A comprehensive skill for orchestrating multi-container applications using Docker Compose. This skill enables rapid development, deployment, and management of containerized applications with service definitions, networking strategies, volume management, health checks, and production-ready configurations.

## When to Use This Skill

Use this skill when:

- Building multi-container applications (microservices, full-stack apps)
- Setting up development environments with databases, caching, and services
- Orchestrating frontend, backend, and database services together
- Managing service dependencies and startup order
- Configuring networks and inter-service communication
- Implementing persistent storage with volumes
- Deploying applications to development, staging, or production
- Creating reproducible development environments
- Managing application lifecycle (start, stop, rebuild, scale)
- Monitoring application health and implementing health checks
- Migrating from single containers to multi-service architectures
- Testing distributed systems locally

## Core Concepts

### Docker Compose Philosophy

Docker Compose simplifies multi-container application management through:

- **Declarative Configuration**: Define entire application stacks in YAML
- **Service Abstraction**: Each component is a service with its own configuration
- **Automatic Networking**: Services can communicate by name automatically
- **Volume Management**: Persistent data and shared storage across containers
- **Environment Isolation**: Each project gets its own network namespace
- **Reproducibility**: Same configuration works across all environments

### Key Docker Compose Entities

1. **Services**: Individual containers and their configurations
2. **Networks**: Communication channels between services
3. **Volumes**: Persistent storage and data sharing
4. **Configs**: Non-sensitive configuration files
5. **Secrets**: Sensitive data (passwords, API keys)
6. **Projects**: Collection of services under a single namespace

### Compose File Structure

```yaml
version: "3.8"  # Compose file format version

services:       # Define containers
  service-name:
    # Service configuration

networks:       # Define custom networks
  network-name:
    # Network configuration

volumes:        # Define named volumes
  volume-name:
    # Volume configuration

configs:        # Application configs (optional)
  config-name:
    # Config source

secrets:        # Sensitive data (optional)
  secret-name:
    # Secret source
```

## Service Definition Patterns

### Basic Service Definition

```yaml
services:
  web:
    image: nginx:alpine           # Use existing image
    container_name: my-web        # Custom container name
    restart: unless-stopped       # Restart policy
    ports:
      - "80:80"                   # Host:Container port mapping
    environment:
      - ENV_VAR=value             # Environment variables
    volumes:
      - ./html:/usr/share/nginx/html  # Volume mount
    networks:
      - frontend                  # Connect to network
```

### Build-Based Service

```yaml
services:
  app:
    build:
      context: ./app              # Build context directory
      dockerfile: Dockerfile      # Custom Dockerfile
      args:                       # Build arguments
        NODE_ENV: development
      target: development         # Multi-stage build target
    image: myapp:latest           # Tag resulting image
    ports:
      - "3000:3000"
```

### Service with Dependencies

```yaml
services:
  web:
    image: nginx
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
      redis:
        condition: service_started  # Wait for start only

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    image: redis:alpine
```

### Service with Advanced Configuration

```yaml
services:
  backend:
    build: ./backend
    command: npm run dev          # Override default command
    working_dir: /app             # Set working directory
    user: "1000:1000"             # Run as specific user
    hostname: api-server          # Custom hostname
    domainname: example.com       # Domain name
    env_file:
      - .env                      # Load env from file
      - .env.local
    environment:
      DATABASE_URL: "postgresql://db:5432/myapp"
      REDIS_URL: "redis://cache:6379"
    volumes:
      - ./backend:/app            # Source code mount
      - /app/node_modules         # Preserve node_modules
      - app-data:/data            # Named volume
    ports:
      - "3000:3000"               # Application port
      - "9229:9229"               # Debug port
    expose:
      - "8080"                    # Expose to other services only
    networks:
      - backend
      - frontend
    labels:
      - "com.example.description=Backend API"
      - "com.example.version=1.0"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Multi-Container Application Patterns

### Pattern 1: Full-Stack Web Application

**Scenario:** React frontend + Node.js backend + PostgreSQL database

```yaml
version: "3.8"

services:
  # Frontend React Application
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:4000/api
      - CHOKIDAR_USEPOLLING=true  # For hot reload
    networks:
      - frontend
    depends_on:
      - backend

  # Backend Node.js API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
      - "9229:9229"  # Debugger
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://cache:6379
      - JWT_SECRET=dev-secret
    env_file:
      - ./backend/.env.local
    networks:
      - frontend
      - backend
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    command: npm run dev

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  cache:
    image: redis:7-alpine
    container_name: redis-cache
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - backend
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
```

### Pattern 2: Microservices Architecture

**Scenario:** Multiple services with reverse proxy and service discovery

```yaml
version: "3.8"

services:
  # NGINX Reverse Proxy
  proxy:
    image: nginx:alpine
    container_name: reverse-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - public
    depends_on:
      - auth-service
      - user-service
      - order-service
    restart: unless-stopped

  # Authentication Service
  auth-service:
    build: ./services/auth
    container_name: auth-service
    expose:
      - "8001"
    environment:
      - SERVICE_NAME=auth
      - DATABASE_URL=postgresql://db:5432/auth_db
      - JWT_SECRET=${JWT_SECRET}
    networks:
      - public
      - internal
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # User Service
  user-service:
    build: ./services/user
    container_name: user-service
    expose:
      - "8002"
    environment:
      - SERVICE_NAME=user
      - DATABASE_URL=postgresql://db:5432/user_db
      - AUTH_SERVICE_URL=http://auth-service:8001
    networks:
      - public
      - internal
    depends_on:
      - auth-service
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Order Service
  order-service:
    build: ./services/order
    container_name: order-service
    expose:
      - "8003"
    environment:
      - SERVICE_NAME=order
      - DATABASE_URL=postgresql://db:5432/order_db
      - USER_SERVICE_URL=http://user-service:8002
      - RABBITMQ_URL=amqp://rabbitmq:5672
    networks:
      - public
      - internal
    depends_on:
      - user-service
      - db
      - rabbitmq
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Shared PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init-multi-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    networks:
      - internal
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

networks:
  public:
    driver: bridge
  internal:
    driver: bridge
    internal: true  # No external access

volumes:
  postgres-data:
  rabbitmq-data:
```

### Pattern 3: Development Environment with Hot Reload

**Scenario:** Development setup with live code reloading and debugging

```yaml
version: "3.8"

services:
  # Development Frontend
  frontend-dev:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
      - "9222:9222"  # Chrome DevTools
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next  # Next.js build cache
    environment:
      - NODE_ENV=development
      - WATCHPACK_POLLING=true
      - NEXT_PUBLIC_API_URL=http://localhost:4000
    networks:
      - dev-network
    stdin_open: true
    tty: true
    command: npm run dev

  # Development Backend
  backend-dev:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "4000:4000"
      - "9229:9229"  # Node.js debugger
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
      - DATABASE_URL=postgresql://postgres:dev@db:5432/dev_db
    networks:
      - dev-network
    depends_on:
      - db
      - mailhog
    command: npm run dev:debug

  # PostgreSQL with pgAdmin
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=dev
      - POSTGRES_DB=dev_db
    ports:
      - "5432:5432"
    volumes:
      - dev-db-data:/var/lib/postgresql/data
    networks:
      - dev-network

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@dev.local
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    networks:
      - dev-network
    depends_on:
      - db

  # MailHog for Email Testing
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI
    networks:
      - dev-network

networks:
  dev-network:
    driver: bridge

volumes:
  dev-db-data:
```

## Networking Strategies

### Default Bridge Network

```yaml
services:
  web:
    image: nginx
    # Automatically connected to default network

  app:
    image: myapp
    # Can communicate with 'web' via service name
```

### Custom Bridge Networks

```yaml
version: "3.8"

services:
  frontend:
    image: react-app
    networks:
      - public

  backend:
    image: api-server
    networks:
      - public    # Accessible from frontend
      - private   # Accessible from database

  database:
    image: postgres
    networks:
      - private   # Isolated from frontend

networks:
  public:
    driver: bridge
  private:
    driver: bridge
    internal: true  # No internet access
```

### Network Aliases

```yaml
services:
  api:
    image: api-server
    networks:
      backend:
        aliases:
          - api-server
          - api.internal
          - api-v1.internal

networks:
  backend:
    driver: bridge
```

### Host Network Mode

```yaml
services:
  app:
    image: myapp
    network_mode: "host"  # Use host network stack
    # No port mapping needed, uses host ports directly
```

### Custom Network Configuration

```yaml
networks:
  custom-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-custom
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
    labels:
      - "com.example.description=Custom network"
```

## Volume Management

### Named Volumes

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data  # Named volume

  backup:
    image: postgres:15
    volumes:
      - postgres-data:/backup:ro  # Read-only mount
    command: pg_dump -U postgres > /backup/dump.sql

volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/on/host
```

### Bind Mounts

```yaml
services:
  web:
    image: nginx
    volumes:
      # Relative path bind mount
      - ./html:/usr/share/nginx/html

      # Absolute path bind mount
      - /var/log/nginx:/var/log/nginx

      # Read-only bind mount
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
```

### tmpfs Mounts (In-Memory)

```yaml
services:
  app:
    image: myapp
    tmpfs:
      - /tmp
      - /run
    # Or with options:
    volumes:
      - type: tmpfs
        target: /app/cache
        tmpfs:
          size: 1000000000  # 1GB
```

### Volume Sharing Between Services

```yaml
services:
  app:
    image: myapp
    volumes:
      - shared-data:/data

  worker:
    image: worker
    volumes:
      - shared-data:/data

  backup:
    image: backup-tool
    volumes:
      - shared-data:/backup:ro

volumes:
  shared-data:
```

### Advanced Volume Configuration

```yaml
volumes:
  data:
    driver: local
    driver_opts:
      type: "nfs"
      o: "addr=10.40.0.199,nolock,soft,rw"
      device: ":/docker/example"

  cache:
    driver: local
    driver_opts:
      type: tmpfs
      device: tmpfs
      o: "size=100m,uid=1000"

  external-volume:
    external: true  # Volume created outside Compose
    name: my-existing-volume
```

## Health Checks

### HTTP Health Check

```yaml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Database Health Check

```yaml
services:
  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  mysql:
    image: mysql:8
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 3

  mongodb:
    image: mongo:6
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Application Health Check

```yaml
services:
  app:
    build: ./app
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  api:
    build: ./api
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Complex Health Checks

```yaml
services:
  redis:
    image: redis:alpine
    healthcheck:
      test: |
        sh -c '
        redis-cli ping | grep PONG &&
        redis-cli --raw incr ping | grep 1
        '
      interval: 10s
      timeout: 3s
      retries: 5
```

## Development vs Production Configurations

### Base Configuration (compose.yaml)

```yaml
version: "3.8"

services:
  web:
    image: myapp:latest
    environment:
      - NODE_ENV=production
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Development Override (compose.override.yaml)

```yaml
# Automatically merged with compose.yaml in development
version: "3.8"

services:
  web:
    build:
      context: .
      target: development
    volumes:
      - ./src:/app/src  # Live code reload
      - /app/node_modules
    ports:
      - "3000:3000"     # Expose for local access
      - "9229:9229"     # Debugger port
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev

  db:
    ports:
      - "5432:5432"     # Expose for local tools
    environment:
      - POSTGRES_PASSWORD=dev
    volumes:
      - ./init-dev.sql:/docker-entrypoint-initdb.d/init.sql
```

### Production Configuration (compose.prod.yaml)

```yaml
version: "3.8"

services:
  web:
    image: myapp:${VERSION:-latest}
    restart: always
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 5s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  # Production additions
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/prod.conf:/etc/nginx/nginx.conf:ro
      - ssl-certs:/etc/nginx/ssl:ro
    restart: always
    depends_on:
      - web

secrets:
  db_password:
    external: true

volumes:
  postgres-data:
    driver: local
  ssl-certs:
    external: true
```

### Staging Configuration (compose.staging.yaml)

```yaml
version: "3.8"

services:
  web:
    image: myapp:staging-${VERSION:-latest}
    restart: unless-stopped
    environment:
      - NODE_ENV=staging
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G

  db:
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - staging-db-data:/var/lib/postgresql/data

volumes:
  staging-db-data:
```

## Essential Docker Compose Commands

### Project Management

```bash
# Start services
docker compose up                    # Foreground
docker compose up -d                 # Detached (background)
docker compose up --build            # Rebuild images
docker compose up --force-recreate   # Recreate containers
docker compose up --scale web=3      # Scale service to 3 instances

# Stop services
docker compose stop                  # Stop containers
docker compose down                  # Stop and remove containers/networks
docker compose down -v               # Also remove volumes
docker compose down --rmi all        # Also remove images

# Restart services
docker compose restart               # Restart all services
docker compose restart web           # Restart specific service
```

### Service Management

```bash
# Build services
docker compose build                 # Build all services
docker compose build web             # Build specific service
docker compose build --no-cache      # Build without cache
docker compose build --pull          # Pull latest base images

# View services
docker compose ps                    # List containers
docker compose ps -a                 # Include stopped containers
docker compose top                   # Display running processes
docker compose images                # List images

# Logs
docker compose logs                  # View all logs
docker compose logs -f               # Follow logs
docker compose logs web              # Service-specific logs
docker compose logs --tail=100 web   # Last 100 lines
```

### Execution and Debugging

```bash
# Execute commands
docker compose exec web sh           # Interactive shell
docker compose exec web npm test     # Run command
docker compose exec -u root web sh   # Run as root

# Run one-off commands
docker compose run web npm install   # Run command in new container
docker compose run --rm web test     # Remove container after
docker compose run --no-deps web sh  # Don't start dependencies
```

### Configuration Management

```bash
# Multiple compose files
docker compose -f compose.yaml -f compose.prod.yaml up

# Environment-specific deployment
docker compose --env-file .env.prod up
docker compose -p myproject up       # Custom project name

# Configuration validation
docker compose config                # Validate and view config
docker compose config --quiet        # Only validation
docker compose config --services     # List services
docker compose config --volumes      # List volumes
```

## 15+ Compose Examples

### Example 1: NGINX + PHP + MySQL (LAMP Stack)

```yaml
version: "3.8"

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./public:/var/www/html
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - lamp
    depends_on:
      - php

  php:
    build:
      context: ./php
      dockerfile: Dockerfile
    volumes:
      - ./public:/var/www/html
    networks:
      - lamp
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: myapp
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - lamp

networks:
  lamp:

volumes:
  mysql-data:
```

### Example 2: Django + PostgreSQL + Redis + Celery

```yaml
version: "3.8"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/django_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data

  celery:
    build: .
    command: celery -A myproject worker -l info
    volumes:
      - .:/code
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/django_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A myproject beat -l info
    volumes:
      - .:/code
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/django_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres-data:
  redis-data:
```

### Example 3: React + Node.js + MongoDB + NGINX

```yaml
version: "3.8"

services:
  frontend:
    build:
      context: ./frontend
      args:
        REACT_APP_API_URL: http://localhost/api
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
    networks:
      - app-network

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - MONGODB_URI=mongodb://mongo:27017/myapp
      - JWT_SECRET=dev-secret
    depends_on:
      - mongo
    networks:
      - app-network

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
      - mongo-config:/data/configdb
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secret
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mongo-data:
  mongo-config:
```

### Example 4: Spring Boot + MySQL + Adminer

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/springdb?useSSL=false
      - SPRING_DATASOURCE_USERNAME=root
      - SPRING_DATASOURCE_PASSWORD=secret
      - SPRING_JPA_HIBERNATE_DDL_AUTO=update
    depends_on:
      db:
        condition: service_healthy
    networks:
      - spring-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: springdb
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - spring-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  adminer:
    image: adminer:latest
    ports:
      - "8081:8080"
    environment:
      ADMINER_DEFAULT_SERVER: db
    networks:
      - spring-network

networks:
  spring-network:

volumes:
  mysql-data:
```

### Example 5: WordPress + MySQL + phpMyAdmin

```yaml
version: "3.8"

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress-data:/var/www/html
    depends_on:
      - db
    networks:
      - wordpress-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - wordpress-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    depends_on:
      - db
    networks:
      - wordpress-network

networks:
  wordpress-network:

volumes:
  wordpress-data:
  db-data:
```

### Example 6: Elasticsearch + Kibana + Logstash (ELK Stack)

```yaml
version: "3.8"

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro
    ports:
      - "5000:5000"
      - "9600:9600"
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    networks:
      - elk
    depends_on:
      - elasticsearch

networks:
  elk:
    driver: bridge

volumes:
  elasticsearch-data:
```

### Example 7: GitLab + GitLab Runner

```yaml
version: "3.8"

services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab
    restart: unless-stopped
    hostname: gitlab.local
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab.local'
        gitlab_rails['gitlab_shell_ssh_port'] = 2222
    ports:
      - "80:80"
      - "443:443"
      - "2222:22"
    volumes:
      - gitlab-config:/etc/gitlab
      - gitlab-logs:/var/log/gitlab
      - gitlab-data:/var/opt/gitlab
    networks:
      - gitlab-network

  gitlab-runner:
    image: gitlab/gitlab-runner:latest
    container_name: gitlab-runner
    restart: unless-stopped
    volumes:
      - gitlab-runner-config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - gitlab-network
    depends_on:
      - gitlab

networks:
  gitlab-network:

volumes:
  gitlab-config:
  gitlab-logs:
  gitlab-data:
  gitlab-runner-config:
```

### Example 8: Jenkins + Docker-in-Docker

```yaml
version: "3.8"

services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    user: root
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins-data:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
      - /usr/bin/docker:/usr/bin/docker
    environment:
      - JAVA_OPTS=-Djenkins.install.runSetupWizard=false
    networks:
      - jenkins-network

  jenkins-agent:
    image: jenkins/inbound-agent:latest
    container_name: jenkins-agent
    environment:
      - JENKINS_URL=http://jenkins:8080
      - JENKINS_AGENT_NAME=agent1
      - JENKINS_SECRET=${AGENT_SECRET}
      - JENKINS_AGENT_WORKDIR=/home/jenkins/agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - jenkins-network
    depends_on:
      - jenkins

networks:
  jenkins-network:

volumes:
  jenkins-data:
```

### Example 9: Prometheus + Grafana + Node Exporter

```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    networks:
      - monitoring
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring

networks:
  monitoring:

volumes:
  prometheus-data:
  grafana-data:
```

### Example 10: RabbitMQ + Multiple Consumers

```yaml
version: "3.8"

services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: secret
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
      - ./rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf:ro
    networks:
      - messaging
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  producer:
    build: ./services/producer
    environment:
      RABBITMQ_URL: amqp://admin:secret@rabbitmq:5672
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - messaging

  consumer-1:
    build: ./services/consumer
    environment:
      RABBITMQ_URL: amqp://admin:secret@rabbitmq:5672
      WORKER_ID: 1
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - messaging
    deploy:
      replicas: 3

  consumer-2:
    build: ./services/consumer
    environment:
      RABBITMQ_URL: amqp://admin:secret@rabbitmq:5672
      WORKER_ID: 2
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - messaging

networks:
  messaging:

volumes:
  rabbitmq-data:
```

### Example 11: Traefik Reverse Proxy

```yaml
version: "3.8"

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/dynamic:/etc/traefik/dynamic:ro
    networks:
      - traefik-network

  whoami:
    image: traefik/whoami
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.whoami.rule=Host(`whoami.local`)"
      - "traefik.http.routers.whoami.entrypoints=web"
    networks:
      - traefik-network

  app:
    image: nginx:alpine
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.local`)"
      - "traefik.http.routers.app.entrypoints=web"
      - "traefik.http.services.app.loadbalancer.server.port=80"
    networks:
      - traefik-network

networks:
  traefik-network:
    driver: bridge
```

### Example 12: MinIO + PostgreSQL Backup

```yaml
version: "3.8"

services:
  minio:
    image: minio/minio:latest
    container_name: minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio-data:/data
    networks:
      - storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - storage

  backup:
    image: postgres:15-alpine
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ./scripts/backup.sh:/backup.sh:ro
    entrypoint: ["/bin/sh", "/backup.sh"]
    depends_on:
      - postgres
      - minio
    networks:
      - storage

networks:
  storage:

volumes:
  minio-data:
  postgres-data:
```

### Example 13: Apache Kafka + Zookeeper

```yaml
version: "3.8"

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    volumes:
      - zookeeper-data:/var/lib/zookeeper/data
      - zookeeper-logs:/var/lib/zookeeper/log
    networks:
      - kafka-network

  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - kafka-data:/var/lib/kafka/data
    networks:
      - kafka-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
    networks:
      - kafka-network

networks:
  kafka-network:

volumes:
  zookeeper-data:
  zookeeper-logs:
  kafka-data:
```

### Example 14: Keycloak + PostgreSQL (Identity & Access Management)

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15-alpine
    container_name: keycloak-db
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - keycloak-network

  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: keycloak
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: password
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    command: start-dev
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    networks:
      - keycloak-network

networks:
  keycloak-network:

volumes:
  postgres-data:
```

### Example 15: Portainer (Docker Management UI)

```yaml
version: "3.8"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "8000:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer-data:/data
    networks:
      - portainer-network

networks:
  portainer-network:

volumes:
  portainer-data:
```

### Example 16: SonarQube + PostgreSQL (Code Quality)

```yaml
version: "3.8"

services:
  sonarqube:
    image: sonarqube:community
    container_name: sonarqube
    depends_on:
      - db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonarqube-conf:/opt/sonarqube/conf
      - sonarqube-data:/opt/sonarqube/data
      - sonarqube-logs:/opt/sonarqube/logs
      - sonarqube-extensions:/opt/sonarqube/extensions
    ports:
      - "9000:9000"
    networks:
      - sonarqube-network

  db:
    image: postgres:15-alpine
    container_name: sonarqube-db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - postgresql-data:/var/lib/postgresql/data
    networks:
      - sonarqube-network

networks:
  sonarqube-network:

volumes:
  sonarqube-conf:
  sonarqube-data:
  sonarqube-logs:
  sonarqube-extensions:
  postgresql-data:
```

## Best Practices

### Service Configuration

1. **Use Specific Image Tags**: Avoid `latest` in production
2. **Health Checks**: Always define health checks for critical services
3. **Resource Limits**: Set CPU and memory limits in production
4. **Restart Policies**: Use appropriate restart policies
5. **Environment Variables**: Use `.env` files for sensitive data
6. **Named Volumes**: Use named volumes for data persistence
7. **Network Isolation**: Separate frontend/backend networks
8. **Logging Configuration**: Set up proper log rotation

### Development Workflow

1. **Hot Reload**: Mount source code as volumes for live updates
2. **Debug Ports**: Expose debugger ports in development
3. **Override Files**: Use `compose.override.yaml` for local config
4. **Build Caching**: Structure Dockerfiles for efficient caching
5. **Separate Concerns**: One process per container
6. **Service Naming**: Use descriptive, consistent service names

### Security

1. **Secrets Management**: Use Docker secrets or external secret managers
2. **Non-Root Users**: Run containers as non-root users
3. **Read-Only Filesystems**: Mount volumes as read-only when possible
4. **Network Segmentation**: Use multiple networks for isolation
5. **Environment Isolation**: Never commit sensitive `.env` files
6. **Image Scanning**: Scan images for vulnerabilities
7. **Minimal Base Images**: Use Alpine or distroless images

### Production Deployment

1. **Image Versioning**: Tag images with semantic versions
2. **Rolling Updates**: Configure gradual rollout strategies
3. **Monitoring**: Integrate with monitoring solutions
4. **Backup Strategy**: Implement automated backups
5. **High Availability**: Deploy replicas of critical services
6. **Load Balancing**: Use reverse proxies for load distribution
7. **Configuration Management**: Externalize configuration
8. **Disaster Recovery**: Test backup and restore procedures

## Troubleshooting

### Common Issues

**Services can't communicate**
- Check network configuration
- Verify service names are correct
- Ensure services are on same network
- Check firewall rules

**Volumes not persisting**
- Verify named volumes are defined
- Check volume mount paths
- Ensure proper permissions
- Review Docker volume driver

**Services failing health checks**
- Increase start_period
- Verify health check command
- Check service logs
- Ensure dependencies are ready

**Port conflicts**
- Check for existing services on ports
- Use different host ports
- Review port mapping syntax

**Build failures**
- Clear build cache: `docker compose build --no-cache`
- Check Dockerfile syntax
- Verify build context
- Review build arguments

### Debugging Commands

```bash
# View detailed container information
docker compose ps -a
docker compose logs -f service-name
docker inspect container-name

# Execute commands in running containers
docker compose exec service-name sh
docker compose exec service-name env

# Check network connectivity
docker compose exec service-name ping other-service
docker compose exec service-name netstat -tulpn

# Review configuration
docker compose config
docker compose config --services
docker compose config --volumes

# Clean up resources
docker compose down -v
docker system prune -a --volumes
```

## Advanced Usage

### Multi-Stage Builds for Optimization

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    # Dockerfile uses multi-stage builds
```

```dockerfile
# Development stage
FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Environment-Specific Deployments

```bash
# Development
docker compose up

# Staging
docker compose -f compose.yaml -f compose.staging.yaml up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d

# With environment file
docker compose --env-file .env.prod -f compose.yaml -f compose.prod.yaml up -d
```

### Scaling Services

```bash
# Scale specific service
docker compose up -d --scale worker=5

# Scale multiple services
docker compose up -d --scale worker=5 --scale consumer=3
```

### Conditional Service Activation with Profiles

```yaml
services:
  web:
    image: nginx
    # Always starts

  debug:
    image: debug-tools
    profiles:
      - debug  # Only starts with --profile debug

  test:
    build: .
    profiles:
      - test   # Only starts with --profile test
```

```bash
# Start with debug profile
docker compose --profile debug up

# Start with multiple profiles
docker compose --profile debug --profile test up
```

## Quick Reference

### Essential Commands

```bash
# Start and manage
docker compose up -d                    # Start detached
docker compose down                     # Stop and remove
docker compose restart                  # Restart all
docker compose stop                     # Stop without removing

# Build and pull
docker compose build                    # Build all images
docker compose pull                     # Pull all images
docker compose build --no-cache        # Clean build

# View and monitor
docker compose ps                       # List containers
docker compose logs -f                  # Follow logs
docker compose top                      # Running processes
docker compose events                   # Real-time events

# Execute and debug
docker compose exec service sh          # Interactive shell
docker compose run --rm service cmd     # One-off command
```

### File Structure

```
project/
├── compose.yaml              # Base configuration
├── compose.override.yaml     # Local overrides (auto-loaded)
├── compose.prod.yaml         # Production config
├── compose.staging.yaml      # Staging config
├── .env                      # Default environment
├── .env.prod                 # Production environment
├── services/
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── src/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── src/
│   └── worker/
│       ├── Dockerfile
│       └── src/
└── docker/
    ├── nginx/
    │   └── nginx.conf
    └── scripts/
        └── init.sql
```

## Resources

- Docker Compose Documentation: https://docs.docker.com/compose/
- Compose File Specification: https://docs.docker.com/compose/compose-file/
- Docker Hub: https://hub.docker.com/
- Awesome Compose Examples: https://github.com/docker/awesome-compose
- Docker Compose GitHub: https://github.com/docker/compose
- Best Practices Guide: https://docs.docker.com/develop/dev-best-practices/

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: DevOps, Container Orchestration, Application Deployment
**Compatible With**: Docker Compose v3.8+, Docker Engine 20.10+
