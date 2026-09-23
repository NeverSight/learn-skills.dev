---
name: building-role-mining-for-rbac-optimization
description: 运用自底向上和自顶向下的角色挖掘技术，从现有用户-权限分配中发现最优 RBAC 角色，减少角色爆炸并强制执行最小权限原则。
domain: cybersecurity
subdomain: identity-access-management
tags: [rbac, role-mining, identity-governance, access-control, least-privilege, clustering]
version: "1.0"
author: mahipal
license: Apache-2.0
---

# 构建 RBAC 优化的角色挖掘

## 概述

角色挖掘（Role Mining）是分析现有用户-权限分配以发现基于角色的访问控制（Role-Based Access Control，RBAC）系统最优角色的过程。组织通过职位变更、项目分配和临时授权随时间积累了过多权限，导致存在大量重叠的细粒度角色，即"角色爆炸"。角色挖掘使用数据分析技术——包括聚类算法、形式概念分析和图方法——将权限整合为最小角色集，准确反映业务职能的同时强制执行最小权限原则。

## 前置条件

- 导出当前用户-权限分配（CSV/数据库格式）
- 身份治理平台或目录服务访问权限
- Python 3.9+（需安装 pandas、scikit-learn、numpy）
- 了解组织结构和职务职能
- 可联系业务利益相关方参与角色验证工作坊

## 核心概念

### 角色挖掘方法

| 方法 | 描述 | 最适用场景 |
|----------|-------------|----------|
| 自底向上 | 分析现有权限以发现常见模式 | 权限有机增长的大型数据集 |
| 自顶向下 | 基于业务需求和职位描述设计角色 | 绿地 RBAC 建设或组织重构 |
| 混合方法 | 将自底向上分析与自顶向下业务验证结合 | 大多数生产环境 |

### 角色挖掘算法

**1. 权限聚类（Permission Clustering）**：使用 k-means 或层次聚类对具有相似权限集的用户进行分组。同一聚类中的用户共享一个公共角色。

**2. 形式概念分析（Formal Concept Analysis，FCA）**：数学框架，从二进制用户-权限矩阵中识别完整的概念集（共享精确权限集的用户组）。

**3. 图方法挖掘（Graph-Based Mining）**：将用户和权限建模为二部图，然后找出代表候选角色的密集子图。

**4. 布尔矩阵分解（Boolean Matrix Decomposition）**：将用户-权限矩阵 U 分解为 U ≈ R × P，其中 R 将用户映射到角色，P 将角色映射到权限。

### 角色挖掘指标

| 指标 | 公式 | 目标 |
|--------|---------|--------|
| 角色数量 | 挖掘后的不同角色总数 | 最小化 |
| 覆盖率 | 被挖掘角色解释的权限 / 总权限 | > 95% |
| 加权结构复杂度（WSC） | 角色-用户 + 角色-权限分配之和 | 最小化 |
| 偏差 | 不被分配角色覆盖的额外权限 | < 5% |

## 实施步骤

### 步骤 1：提取用户-权限数据

从所有身份来源收集当前访问状态：

```python
import pandas as pd
import numpy as np

# 加载用户-权限分配
# 格式：user_id, permission_id（每行一个分配）
assignments = pd.read_csv("user_permissions.csv")

# 创建二进制用户-权限矩阵（UPA 矩阵）
upa_matrix = assignments.pivot_table(
    index="user_id",
    columns="permission_id",
    aggfunc="size",
    fill_value=0
)
upa_matrix = (upa_matrix > 0).astype(int)

print(f"用户数：{upa_matrix.shape[0]}")
print(f"权限数：{upa_matrix.shape[1]}")
print(f"分配数：{assignments.shape[0]}")
print(f"密度：{upa_matrix.values.sum() / upa_matrix.size:.2%}")
```

### 步骤 2：使用聚类进行自底向上角色发现

```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

def find_optimal_clusters(matrix, max_k=50):
    """使用轮廓分析找到最优角色数量。"""
    scores = []
    for k in range(2, min(max_k, matrix.shape[0])):
        clustering = AgglomerativeClustering(
            n_clusters=k, metric="jaccard", linkage="average"
        )
        labels = clustering.fit_predict(matrix)
        score = silhouette_score(matrix, labels, metric="jaccard")
        scores.append((k, score))

    optimal_k = max(scores, key=lambda x: x[1])[0]
    return optimal_k, scores

def mine_roles_clustering(upa_matrix, n_clusters):
    """使用 Jaccard 距离上的层次聚类挖掘角色。"""
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, metric="jaccard", linkage="average"
    )
    user_matrix = upa_matrix.values
    labels = clustering.fit_predict(user_matrix)

    roles = {}
    for cluster_id in range(n_clusters):
        cluster_users = upa_matrix.index[labels == cluster_id]
        cluster_permissions = upa_matrix.loc[cluster_users]

        # 核心角色 = 超过 80% 聚类成员拥有的权限
        permission_frequency = cluster_permissions.mean()
        core_permissions = permission_frequency[permission_frequency >= 0.8].index.tolist()

        roles[f"Role_{cluster_id}"] = {
            "permissions": core_permissions,
            "user_count": len(cluster_users),
            "users": cluster_users.tolist(),
            "coverage": permission_frequency[permission_frequency >= 0.8].mean()
        }

    return roles, labels
```

### 步骤 3：形式概念分析

```python
def mine_roles_fca(upa_matrix, min_support=3):
    """使用形式概念分析（频繁闭合项集）挖掘角色。"""
    from itertools import combinations

    users = upa_matrix.index.tolist()
    permissions = upa_matrix.columns.tolist()

    concepts = []

    # 找出所有至少被 min_support 个用户共享的最大权限集
    for size in range(len(permissions), 0, -1):
        for perm_combo in combinations(permissions, size):
            perm_set = set(perm_combo)
            # 找出拥有该集合中所有权限的用户
            matching_users = []
            for user in users:
                user_perms = set(upa_matrix.columns[upa_matrix.loc[user] == 1])
                if perm_set.issubset(user_perms):
                    matching_users.append(user)

            if len(matching_users) >= min_support:
                # 检查是否为闭合概念（不存在具有相同范围的超集）
                is_closed = True
                for concept in concepts:
                    if set(matching_users) == set(concept["users"]) and \
                       perm_set.issubset(set(concept["permissions"])):
                        is_closed = False
                        break

                if is_closed:
                    concepts.append({
                        "permissions": list(perm_set),
                        "users": matching_users,
                        "support": len(matching_users)
                    })

        if len(concepts) > 100:  # 限制数量以提高性能
            break

    return concepts
```

### 步骤 4：评估和选择角色

```python
def evaluate_role_set(roles, upa_matrix):
    """评估挖掘角色集的质量。"""
    total_assignments = upa_matrix.values.sum()
    covered_assignments = 0
    extra_assignments = 0

    for role_name, role_data in roles.items():
        role_perms = set(role_data["permissions"])
        for user in role_data["users"]:
            user_perms = set(upa_matrix.columns[upa_matrix.loc[user] == 1])
            covered = role_perms.intersection(user_perms)
            extra = role_perms - user_perms
            covered_assignments += len(covered)
            extra_assignments += len(extra)

    metrics = {
        "total_roles": len(roles),
        "total_assignments": total_assignments,
        "covered_assignments": covered_assignments,
        "coverage_rate": covered_assignments / total_assignments if total_assignments else 0,
        "extra_permissions": extra_assignments,
        "deviation_rate": extra_assignments / (covered_assignments + extra_assignments) if (covered_assignments + extra_assignments) else 0,
        "avg_role_size": np.mean([len(r["permissions"]) for r in roles.values()]),
        "avg_users_per_role": np.mean([r["user_count"] for r in roles.values()]),
    }
    return metrics
```

### 步骤 5：业务验证

挖掘候选角色后：

1. 将挖掘出的角色映射到业务职能（部门、职位）
2. 与业务单元负责人举行工作坊，验证角色定义
3. 识别表明配置错误的异常权限
4. 根据反馈完善角色并重新评估指标
5. 记录带有业务理由的角色定义

## 验证清单

- [ ] 已从所有身份来源提取用户-权限矩阵
- [ ] 已比较多种挖掘算法（聚类、FCA）
- [ ] 通过轮廓分析或 WSC 确定最优角色数量
- [ ] 覆盖率超过现有分配的 95%
- [ ] 偏差率低于 5%（额外权限最少）
- [ ] 已与业务利益相关方验证挖掘出的角色
- [ ] 已定义角色层次（父子继承）
- [ ] 已记录例外/异常权限
- [ ] 已创建过渡到新角色模型的迁移计划
- [ ] 已定义持续的角色治理流程

## 参考资料

- [角色挖掘：优化 RBAC - NIST](https://csrc.nist.gov/projects/role-based-access-control)
- [RBAC 标准 - ANSI/INCITS 359-2012](https://www.incits.org/)
- [用于角色工程的形式概念分析](https://link.springer.com/chapter/10.1007/978-3-540-73070-6_7)
- [scikit-learn 聚类文档](https://scikit-learn.org/stable/modules/clustering.html)
