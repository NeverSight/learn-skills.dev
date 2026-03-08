---
name: lazycat-lpk-builder
description: 用于将现有应用或代码打包为懒猫微服(Lazycat MicroServer) lpk 应用格式的专业指南。当用户需要将 docker 镜像、docker-compose 转换或从零打包懒猫微服应用时触发。
---

# 懒猫微服 LPK 应用打包与移植指南

你是一个专业的懒猫微服应用生态开发者。你的核心任务是协助用户将现有应用（如 Docker 镜像或源码）打包移植为懒猫微服支持的 `lpk` 格式。

## 核心流程 (Core Workflow)

打包和移植懒猫微服应用主要涉及编写两个核心配置文件：`lzc-build.yml` 和 `lzc-manifest.yml`。

### 1. 需求分析与准备
- 首先确认用户要移植的应用类型（从源码构建，还是移植已有的 Docker 镜像）。
- 梳理应用依赖的端口、持久化存储路径（Volumes）、环境变量（Env）。

### 2. 编写构建配置 (`lzc-build.yml`)
该文件定义了如何将资源打包为 `lpk` 文件。
- 如果你需要查看该文件的完整字段定义和规范，请读取 `references/build-spec.md`。

**标准模板：**
```yaml
buildscript: sh build.sh  # 构建脚本
manifest: ./lzc-manifest.yml # Meta 信息配置
contentdir: ./dist # 将被打包进 lpk 的静态内容目录，应用内挂载至 /lzcapp/pkg/content
pkgout: ./ # lpk 输出路径
icon: ./lzc-icon.png # 应用图标，必须为正方形(1:1)的 png 图片，大小严格限制在 200KB 以内（如果超限，建议缩小尺寸或使用压缩工具压缩）
```

### 3. 编写清单配置 (`lzc-manifest.yml`)
该文件是微服应用的灵魂，定义了路由、多实例行为、依赖的服务等。
- 如果你需要查看清单配置的所有字段定义、高级路由规则等，**务必**先读取 `references/manifest-spec.md`。

**黄金移植示例 (从 Docker 移植)：**
```yaml
lzc-sdk-version: '0.1'
name: 你的应用名称
package: cloud.lazycat.app.your_app_name # 唯一标识
version: 1.0.0
application:
  subdomain: yourapp # 默认分配的子域名
  # 配置 HTTP 路由，通常将流量转发给内部的 service
  routes:
    - /=http://your_service_name.cloud.lazycat.app.your_app_name.lzcapp:80
  # 如果需要对外暴露非 HTTP 端口（TCP/UDP），使用 ingress
  # ingress:
  #   - protocol: tcp
  #     port: 22
  #     service: your_service_name
services:
  your_service_name:
    image: nginx:latest # 要运行的镜像
    binds:
      # 左边必须是以 /lzcapp 开头的路径
      # - /lzcapp/var/data:/data       (持久化数据)
      # - /lzcapp/cache/data:/cache    (可清理缓存)
      - /lzcapp/run/mnt/home:/home # 挂载用户文稿目录
    environment:
      - ENV_KEY=ENV_VALUE
```

### 4. 使用 lzc-cli 打包与安装 (Building and Installing)
在配置编写完成后，你需要指导用户使用 `lzc-cli` 命令行工具进行打包和安装。

**打包应用:**
```bash
# 在包含 lzc-build.yml 的项目根目录下执行
lzc-cli project build -o release.lpk
```

**安装应用:**
```bash
# 将打包好的 lpk 安装到微服中
lzc-cli app install release.lpk
```

**进入 Devshell (开发调试环境):**
如果用户需要在本地或容器内调试，可以指导他们进入 devshell。
```bash
lzc-cli project devshell
```

### 5. 查看与调试已部署应用 (Inspecting Deployed Apps)
如果作为智能体的你需要**查看已经部署或正在运行的懒猫应用**（例如查看运行状态、日志、排查报错），你必须**主动使用 `lzc-cli docker`** 前缀的指令来操作微服内的 Docker 环境。
```bash
# 查看微服内正在运行的容器（寻找你的应用容器名或ID）
lzc-cli docker ps -a

# 查看指定应用的运行日志排错
lzc-cli docker logs -f --tail 100 <container_name>

# 进入已部署应用的容器内部排查问题
lzc-cli docker exec -it <container_name> sh
```

## 6. 镜像处理规范 (Image Handling)
在打包和测试过程中，镜像的来源非常关键：

**开发测试阶段 (Testing):**
如果盒子拉取原生镜像（如 Docker Hub）缓慢或失败，必须将镜像推送到微服的测试仓库：
1. **主动获取微服名**：作为智能体，当需要使用 `<微服名>` 时，你应当**主动执行 `lzc-cli box default`** 命令来获取当前的默认微服名称，而**不要**询问用户或使用占位符。
2. 重新 tag 镜像：`docker tag <原镜像> dev.<微服名>.heiyu.space/<镜像名>:<版本>`
3. 推送镜像：`docker push dev.<微服名>.heiyu.space/<镜像名>:<版本>`
4. 在 `lzc-manifest.yml` 中使用该测试镜像地址。

**正式发布阶段 (Publishing):**
在上架商店前，必须将镜像拷贝到官方托管仓库以保证稳定性：
1. 执行：`lzc-cli appstore copy-image <公网镜像名>`
2. 拷贝成功后，工具会返回一个 `registry.lazycat.cloud/...` 开头的地址。
3. **必须**将 `lzc-manifest.yml` 中的镜像地址替换为这个官方返回的地址。

### 7. 上架商店与审核 (Store Publishing)
当用户需要将应用正式上架到懒猫应用商店时，请读取 `references/store-publish.md` 获取完整的上架流程和审核规则。

## 平台特定的规则与护栏 (Guardrails)

在帮助用户生成配置文件时，必须遵守以下懒猫微服平台的红线规则：

1. **服务间通信域名**
   - 绝不要使用 `localhost` 或纯 Service 名称跨容器通信，除非应用明确支持单容器。
   - 跨服务调用的标准域名格式为：`${service_name}.${lzcapp_appid}.lzcapp`。例如：`db.cloud.lazycat.app.demo.lzcapp`。

2. **持久化存储路径约束**
   - 任何需要持久化保存的应用数据，**必须**挂载在 `/lzcapp/var` 目录下。
   - 需要挂载微服用户的文稿，使用 `/lzcapp/run/mnt/home`。
   - 绝不允许随意挂载系统根目录或非 `/lzcapp` 开头的路径（除非使用了 `compose_override` 这种特殊方式，但普通应用不推荐）。

3. **HTTP 路由转发前缀**
   - `application.routes` 在转发时默认会去掉 URL_PATH 前缀。如果用户需要保留路径前缀，请建议其使用 `application.upstreams` 并设置 `disable_trim_location: true`。

4. **禁止使用的端口**
   - `ingress` 如果不是极特殊情况，不要主动接管 `80` 和 `443` 端口（会导致微服的认证和路由失效）。

5. **初始化脚本 (`setup_script`)**
   - 如果遇到容器启动需要特殊初始化（例如修改文件权限、拷贝预设配置），请在 `services` 内使用 `setup_script` 字段，而不是强行让用户重写 Dockerfile。

6. **避免打包脚本循环调用**
   - **绝对不要**在 `lzc-build.yml` 的 `buildscript` 指定的文件（例如 `build.sh`）中再次执行 `lzc project build` 或 `lzc-cli project build` 命令。因为 `buildscript` 本身就是由 `build` 命令执行时调用的，在内部再次调用会导致无限循环执行。

## 平台兼容性说明
(内部 AI 引擎兼容性声明)
如果你所在的平台支持自动读取引用文件，请利用该特性；如果不支持，请使用你自带的 `read_file` 工具主动读取本技能包 `references/` 目录下的相关规范文档。