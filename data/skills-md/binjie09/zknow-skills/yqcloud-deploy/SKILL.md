---
name: yqcloud-deploy
description: 燕千云部署管理工具。用于查询 ChartMuseum 中的 Helm Chart 版本、管理 GitOps 仓库部署配置、修改环境变量和 chartVersion。当用户需要：(1) 查询某个服务的可用 chart 版本，(2) 部署或更新服务到不同环境（test/preprod/stag），(3) 修改部署配置或环境变量，(4) 查看当前部署状态时使用此技能。
---

# 燕千云部署管理

## 环境信息

燕千云使用 GitOps 方式管理部署，有三个环境和多个仓库：

- **test 环境**: git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/yq-test.git
- **preprod 环境（三个都是，且部署不一样的服务）**: git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/yq-preprod.git  git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/yq-preprod.git  git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/preprod-fronts.git
- **stag 环境**（实施环境）: 后端 git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/yqc-stag.git 前端：git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/stag-front.git

## 工作流程

### 1. 查询可用的 Chart 版本

使用 ChartMuseum API 获取某个服务的所有可用版本：

```bash
# 从 GitOps 仓库的 release-xxx.yaml 中找到 repoUrl
# repoUrl 就是 base_url

# 查询指定服务的所有版本
curl -s "{base_url}/api/charts/{chart_name}" | tee ~/tmp/{chart_name}_versions.json

# 示例
curl -s "https://chart.choerodon.com.cn/hand-yanqianyun/zknow-platform/api/charts/zknow-workflow" | tee ~/tmp/zknow-workflow_versions.json
```

API 返回所有版本，无分页。结果保存到 `~/tmp/` 方便查看和搜索。

### 2. 克隆 GitOps 仓库

首次使用时，将目标环境的 GitOps 仓库克隆到本地：

```bash
# 克隆到统一目录
mkdir -p ~/yq-gitops

# 根据环境选择对应仓库
cd ~/yq-gitops

# test 环境
git clone https://code.choerodon.com.cn/hand-yanqianyun-yqcloud-gitops/yq-test.git

# preprod 环境
git clone git@code.choerodon.com.cn:hand-yanqianyun-yqcloud-gitops/yq-preprod.git

# stag 环境
git clone https://code.choerodon.com.cn/hand-yanqianyun-yqcloud-gitops/yqc-stag.git
```

### 3. 修改部署配置

部署配置文件格式为 `release-{service_name}.yaml`。

#### 更新 Chart 版本

修改 `chartVersion` 字段：

```bash
cd ~/yq-gitops/{environment}

# 编辑对应的 release 文件
# 找到 chartVersion 字段并修改为目标版本
```

#### 修改环境变量

在 `release-{service_name}.yaml` 中找到 `values` 或 `env` 部分进行修改。

### 4. 提交并推送

修改完成后提交并推送，触发自动部署：

```bash
git add .
git commit -m "Update {service_name} to version {version}"
git push
```

推送后，GitOps 系统会自动检测变更并执行部署。

## 常见操作

### 查看当前部署版本

```bash
cd ~/yq-gitops/{environment}
grep -A 5 "chartVersion" release-{service_name}.yaml
```

### 查看环境变量配置

```bash
cd ~/yq-gitops/{environment}
cat release-{service_name}.yaml
```

### 搜索特定版本

```bash
# 在保存的版本列表中搜索
cat ~/tmp/{chart_name}_versions.json | grep "{version_pattern}"
```

## 注意事项

- ChartMuseum API 无需认证（如果需要认证，添加 `-u username:password`）
- 修改前先 `git pull` 确保本地是最新状态
- 提交信息应清晰说明修改内容
- 推送后可通过 GitOps 平台查看部署状态
