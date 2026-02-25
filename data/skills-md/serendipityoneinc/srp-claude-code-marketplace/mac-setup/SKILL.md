---
name: mac-setup
description: Mac development environment setup and verification for SRP employees (Mac 开发环境安装配置与验证)
---

# Mac Setup for SRP

为 SRP 员工提供 Mac 开发环境的安装、配置和验证。支持智能检测已安装软件，让用户选择需要安装的组件，并在安装后进行验证检查。

## Quick Start

```
帮我配置 Mac 开发环境
Setup my Mac for SRP development
检查我的 Mac 开发环境
```

## Workflow Overview

执行此 skill 时，按以下 5 个阶段进行：

```
1. 前置检查 → 2. 智能检测 → 3. 用户选择 → 4. 执行安装 → 5. 验证检查
```

## Phase 1: Pre-requisite Check (前置检查)

### 1.1 Check Homebrew

Homebrew 是所有后续安装的前提。

```bash
# 检测 Homebrew 是否已安装
which brew
brew --version
```

**如果未安装 Homebrew：**
提示用户先安装 Homebrew，这是唯一需要手动执行的步骤（因为需要输入密码）：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完成后，配置阿里云镜像加速：
```bash
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc
```

### 1.2 Check Google Cloud Authentication (Optional)

如果用户选择安装 GKE 配置或 Telepresence，需要先完成 gcloud 认证。

```bash
# 检查 gcloud 认证状态
gcloud auth list 2>/dev/null | grep -q "ACTIVE" && echo "authenticated" || echo "not authenticated"
```

**如果未认证且用户选择了需要认证的组件：**
引导用户完成认证（会打开浏览器）：
```bash
gcloud auth login
gcloud auth application-default login
```

## Phase 2: Smart Detection (智能检测)

检测以下所有组件的安装状态。使用此检测逻辑：

### Component Detection Commands

| Component | Category | Detection Command |
|-----------|----------|-------------------|
| Homebrew | Package Manager | `which brew` |
| Claude Code | AI Tools | `which claude` |
| Warp Terminal | Terminal | `ls /Applications/Warp.app 2>/dev/null` |
| Git | Version Control | `which git` |
| GitHub CLI | Version Control | `which gh` |
| Git LFS | Version Control | `which git-lfs` |
| Python 3.13 | Development | `brew list python@3.13 2>/dev/null` |
| Anaconda | Development | `ls /opt/homebrew/anaconda3 2>/dev/null \|\| ls ~/anaconda3 2>/dev/null` |
| Google Cloud SDK | Cloud CLI | `which gcloud` |
| kubectl | Cloud CLI | `which kubectl` |
| Azure CLI | Cloud CLI | `which az` |
| Oracle CLI | Cloud CLI | `which oci` |
| DigitalOcean CLI | Cloud CLI | `which doctl` |
| Terraform | DevOps | `which terraform` |
| Cursor IDE | IDE | `ls /Applications/Cursor.app 2>/dev/null` |
| Orbstack | Containers | `ls /Applications/OrbStack.app 2>/dev/null` |
| Telepresence | VPN | `which telepresence` |

### Configuration Detection

| Configuration | Detection Command |
|---------------|-------------------|
| pip mirror | `grep -q "pypi.tuna.tsinghua.edu.cn" ~/.pip/pip.conf 2>/dev/null` |
| GKE contexts | `kubectl config get-contexts 2>/dev/null \| grep -q "srp-cluster"` |
| KUBECONFIG env | `grep -q "KUBECONFIG=~/.kube/config.srp" ~/.zshrc 2>/dev/null` |
| Cursor extensions | Compare installed vs required extensions |

### Detection Script

执行以下脚本进行完整检测：

```bash
echo "=== Mac Setup Detection Report ==="
echo ""

echo "## Package Manager"
echo -n "Homebrew: "; which brew > /dev/null 2>&1 && echo "✅ Installed ($(brew --version | head -1))" || echo "❌ Not installed"
echo ""

echo "## AI Tools"
echo -n "Claude Code: "; which claude > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## Terminal"
echo -n "Warp Terminal: "; [ -d "/Applications/Warp.app" ] && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## Version Control"
echo -n "Git: "; which git > /dev/null 2>&1 && echo "✅ Installed ($(git --version))" || echo "❌ Not installed"
echo -n "GitHub CLI: "; which gh > /dev/null 2>&1 && echo "✅ Installed ($(gh --version | head -1))" || echo "❌ Not installed"
echo -n "Git LFS: "; which git-lfs > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## Development Environment"
echo -n "Python 3.13: "; brew list python@3.13 > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo -n "Anaconda: "; ([ -d "/opt/homebrew/anaconda3" ] || [ -d "$HOME/anaconda3" ]) && echo "✅ Installed" || echo "❌ Not installed"
echo -n "Orbstack: "; [ -d "/Applications/OrbStack.app" ] && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## IDE"
echo -n "Cursor: "; [ -d "/Applications/Cursor.app" ] && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## Cloud CLI"
echo -n "Google Cloud SDK: "; which gcloud > /dev/null 2>&1 && echo "✅ Installed ($(gcloud --version 2>/dev/null | head -1))" || echo "❌ Not installed"
echo -n "kubectl: "; which kubectl > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo -n "Azure CLI: "; which az > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo -n "Oracle CLI: "; which oci > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo -n "DigitalOcean CLI: "; which doctl > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## DevOps Tools"
echo -n "Terraform: "; which terraform > /dev/null 2>&1 && echo "✅ Installed ($(terraform version | head -1))" || echo "❌ Not installed"
echo -n "Telepresence: "; which telepresence > /dev/null 2>&1 && echo "✅ Installed" || echo "❌ Not installed"
echo ""

echo "## Configurations"
echo -n "pip mirror config: "; grep -q "pypi.tuna.tsinghua.edu.cn" ~/.pip/pip.conf 2>/dev/null && echo "✅ Configured" || echo "❌ Not configured"
echo -n "GKE contexts: "; kubectl config get-contexts 2>/dev/null | grep -q "srp-cluster" && echo "✅ Configured" || echo "❌ Not configured"
echo -n "KUBECONFIG env: "; grep -q "KUBECONFIG" ~/.zshrc 2>/dev/null && echo "✅ Configured" || echo "❌ Not configured"
```

## Phase 3: User Selection (用户选择)

根据检测结果，向用户展示未安装的组件，让用户选择要安装的内容。

**按类别分组展示：**

1. **基础工具 (All Staff)**
   - [ ] Claude Code - AI 编程助手 (公司全员必装)
   - [ ] Warp Terminal - 现代化终端
   - [ ] Git + GitHub CLI + Git LFS - 版本控制

2. **开发环境 (Developers)**
   - [ ] Python 3.13 - 基础 Python
   - [ ] Anaconda - Python 虚拟环境管理
   - [ ] Cursor IDE - AI 增强的代码编辑器
   - [ ] Cursor Extensions - Cursor 扩展插件包
   - [ ] Orbstack - 容器运行环境

3. **云平台 CLI (Developers/DevOps)**
   - [ ] Google Cloud SDK - GCP 访问工具
   - [ ] Azure CLI - Azure 访问工具
   - [ ] Oracle CLI - OCI 访问工具
   - [ ] DigitalOcean CLI - DO 访问工具

4. **DevOps 工具**
   - [ ] Terraform - 基础设施即代码
   - [ ] Miscellaneous - telnet, iftop, mtr, node, maven, ansible, pssh

5. **配置项**
   - [ ] pip 镜像配置 - 使用清华镜像加速
   - [ ] GKE 集群配置 - 配置 K8s 访问上下文
   - [ ] Telepresence VPN - 内网访问工具

使用 AskUserQuestion 工具让用户进行多选。

## Phase 4: Installation (执行安装)

根据用户选择，按依赖顺序执行安装。

### Installation Commands

#### 基础工具

**Claude Code:**
```bash
brew install --cask claude-code
```

**Warp Terminal:**
```bash
brew install --cask warp
```
安装后提示用户加入 SRP Team: https://app.warp.dev/team/9uUrBMqrIoZ7Jj5J6qrnSN

**Git + GitHub CLI + Git LFS:**
```bash
brew install gh git git-lfs
git lfs install
```

#### 开发环境

**Python 3.13:**
```bash
brew install python@3.13
```

**Anaconda:**
```bash
brew install --cask anaconda
```

**Cursor IDE:**
```bash
brew install --cask cursor
```

**Cursor Extensions:**
安装 Cursor 扩展。扩展列表在 skill 目录的 `cursor-extensions.txt` 文件中。

执行时，Claude 应该：
1. 读取 `cursor-extensions.txt` 文件内容
2. 逐行执行 `cursor --install-extension <extension-id>`

```bash
# 示例：安装单个扩展
cursor --install-extension ms-python.python
```

**Orbstack:**
```bash
brew install orbstack
```

#### 云平台 CLI

**Google Cloud SDK:**
```bash
brew install --cask google-cloud-sdk
gcloud components install gke-gcloud-auth-plugin kubectl kustomize bq
brew install gettext
```

**Azure CLI:**
```bash
brew install azure-cli
```

**Oracle CLI:**
```bash
brew install oci-cli
```

**DigitalOcean CLI:**
```bash
brew install doctl
```

#### DevOps 工具

**Terraform:**
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

**Miscellaneous:**
```bash
brew install telnet iftop mtr node maven ansible pssh
```

**Telepresence:**
```bash
sudo curl -fL https://app.getambassador.io/download/tel2oss/releases/download/v2.18.0/telepresence-darwin-arm64 -o /usr/local/bin/telepresence
sudo chmod a+x /usr/local/bin/telepresence
```

#### 配置项

**pip 镜像配置:**
```bash
mkdir -p ~/.pip
tee ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/

[install]
trusted-host=mirrors.aliyun.com
               pypi.ngc.nvidia.com
               pypi.tuna.tsinghua.edu.cn

no-cache-dir = true
EOF
```

**GKE 集群配置:**

前提：需要先完成 gcloud auth login

```bash
# 备份现有配置
[ -f ~/.kube/config.srp ] && mv -f ~/.kube/config.srp ~/.kube/config.srp.bak

# 设置 KUBECONFIG
export KUBECONFIG=~/.kube/config.srp
grep -q "KUBECONFIG" ~/.zshrc || echo 'export KUBECONFIG=~/.kube/config.srp' >> ~/.zshrc

# 获取集群凭证
gcloud container clusters get-credentials srp-cluster-dev-us-east1 --location us-east1 --project srpdev-7b1d3
gcloud container clusters get-credentials srp-cluster-dev-us-west1 --location us-west1 --project srpdev-7b1d3
gcloud container clusters get-credentials srp-cluster-staging-us-east1 --location us-east1 --project srpstaging
gcloud container clusters get-credentials srp-cluster-staging-us-west1 --location us-west1 --project srpstaging
gcloud container clusters get-credentials srp-cluster-production-us-east1 --location us-east1 --project srpproduct-dc37e
gcloud container clusters get-credentials srp-cluster-production-us-west1 --location us-west1 --project srpproduct-dc37e

# 重命名 context 为简短名称
kubectl config rename-context gke_srpdev-7b1d3_us-east1_srp-cluster-dev-us-east1 srp-cluster-dev-us-east1
kubectl config rename-context gke_srpdev-7b1d3_us-west1_srp-cluster-dev-us-west1 srp-cluster-dev-us-west1
kubectl config rename-context gke_srpstaging_us-east1_srp-cluster-staging-us-east1 srp-cluster-staging-us-east1
kubectl config rename-context gke_srpstaging_us-west1_srp-cluster-staging-us-west1 srp-cluster-staging-us-west1
kubectl config rename-context gke_srpproduct-dc37e_us-east1_srp-cluster-production-us-east1 srp-cluster-production-us-east1
kubectl config rename-context gke_srpproduct-dc37e_us-west1_srp-cluster-production-us-west1 srp-cluster-production-us-west1

# 设置默认 context
kubectl config use-context srp-cluster-dev-us-east1
```

## Phase 5: Verification (验证检查)

对已安装的组件进行功能验证，确保安装配置正确。

### Verification Script

```bash
echo "=== Mac Setup Verification Report ==="
echo ""
PASS=0
FAIL=0

verify() {
    local name="$1"
    local cmd="$2"
    echo -n "$name: "
    if eval "$cmd" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASS++))
    else
        echo "❌ FAIL"
        ((FAIL++))
    fi
}

echo "## Software Verification"
verify "Homebrew" "brew --version"
verify "Claude Code" "claude --version"
verify "Warp Terminal" "[ -d '/Applications/Warp.app' ]"
verify "Git" "git --version"
verify "GitHub CLI" "gh --version"
verify "Git LFS" "git lfs version"
verify "Python 3.13" "python3.13 --version"
verify "Anaconda" "conda --version"
verify "Cursor" "[ -d '/Applications/Cursor.app' ]"
verify "Orbstack" "[ -d '/Applications/OrbStack.app' ]"
verify "Google Cloud SDK" "gcloud --version"
verify "kubectl" "kubectl version --client"
verify "Azure CLI" "az --version"
verify "Terraform" "terraform version"
verify "Telepresence" "telepresence version"
echo ""

echo "## Configuration Verification"
verify "pip mirror" "grep -q 'pypi.tuna.tsinghua.edu.cn' ~/.pip/pip.conf"
verify "KUBECONFIG env" "grep -q 'KUBECONFIG' ~/.zshrc"
echo ""

echo "## GKE Connectivity Verification"
verify "GKE contexts configured" "kubectl config get-contexts | grep -q 'srp-cluster'"
verify "GKE dev cluster access" "kubectl --context srp-cluster-dev-us-east1 get namespaces"
echo ""

echo "=== Summary ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"

if [ $FAIL -gt 0 ]; then
    echo ""
    echo "⚠️  Some verifications failed. Please check the items above."
fi
```

### Detailed Verification Checks

| Component | Verification Method | Success Criteria |
|-----------|---------------------|------------------|
| Homebrew | `brew --version` | 返回版本号 |
| Claude Code | `claude --version` | 返回版本号 |
| Warp Terminal | 检查 App 目录 | /Applications/Warp.app 存在 |
| Git | `git --version` | 返回版本号 |
| GitHub CLI | `gh auth status` | 显示认证状态 |
| Git LFS | `git lfs version` | 返回版本号 |
| Python | `python3.13 --version` | 返回 3.13.x |
| Anaconda | `conda --version` | 返回版本号 |
| Cursor | 检查 App 目录 | /Applications/Cursor.app 存在 |
| Orbstack | `orb version` | 返回版本号 |
| gcloud | `gcloud auth list` | 显示 ACTIVE 账号 |
| kubectl | `kubectl cluster-info` | 返回集群信息 |
| GKE access | `kubectl get namespaces` | 返回 namespace 列表 |
| Telepresence | `telepresence version` | 返回版本号 |
| pip config | 检查配置文件 | 包含清华镜像地址 |

### Troubleshooting Guide

**问题：Homebrew 安装失败**
- 检查网络连接
- 尝试使用代理或镜像源

**问题：gcloud auth 失败**
- 确保浏览器可以正常打开
- 检查是否有公司网络限制

**问题：GKE 集群连接失败**
- 确认 gcloud auth 已完成
- 检查是否有 VPN 连接要求
- 确认账号是否有集群访问权限

**问题：Telepresence 连接失败**
- 确保 GKE 配置正确
- 检查是否已运行 `telepresence quit -s`
- 尝试重新连接: `telepresence connect --context srp-cluster-dev-us-east1`

## Reference Documentation

- 飞书文档: [Mac Setup (for SRP)](https://starquest.feishu.cn/wiki/X0dMwOQ6PiJyYbky9VKcgSlLnpc)
- Warp Team 邀请: https://app.warp.dev/team/9uUrBMqrIoZ7Jj5J6qrnSN
- Telepresence 使用指南: 参考飞书文档中的链接

## Related Skills

- `lark-docs`: 访问飞书文档获取最新配置信息
- `lark-messages`: 在飞书群组中寻求帮助
