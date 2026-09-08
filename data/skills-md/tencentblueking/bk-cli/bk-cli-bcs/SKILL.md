---
name: bk-cli-bcs
description: 当需要通过 `bk-cli bcs` 调用 BCS API 时使用；当前主要覆盖 `bk-cli bcs cluster_manager` 下的集群、节点、节点组、节点模板、任务、模板配置和虚拟集群配额操作。
---

# bk-cli bcs

用于让 Agent 通过 `bk-cli bcs` 调用 BCS API。开始前先读取 `../bk-cli-shared/SKILL.md`，共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 等通用调用规则。

当前可用命令层级：

```bash
bk-cli bcs cluster_manager <action>
```

如果用户要操作其他 BCS 模块，先运行 `bk-cli bcs -h` 查看是否已有对应 subsystem。

## Action 清单

`cluster_manager` 当前包含：

- 集群：`create_cluster`、`import_cluster`、`update_cluster`
- 弹性伸缩：`update_auto_scaling_option`、`update_auto_scaling_status`
- 节点：`delete_nodes_from_cluster`、`batch_delete_nodes_from_cluster`、`add_nodes_to_cluster_v2`、`add_subnet_to_cluster`、`update_node_annotations`、`check_node_in_cluster`、`cordon_node`、`drain_node`、`check_drain_node`、`update_node_labels`、`update_node_taints`、`un_cordon_node`
- 节点组：`create_node_group`、`update_node_group`、`disable_node_group_auto_scale`、`enable_node_group_auto_scale`、`update_group_min_max_size`、`update_group_desired_node`、`update_group_desired_size`、`clean_nodes_in_group`、`clean_nodes_in_group_v2`
- 节点模板：`create_node_template`、`update_node_template`、`trans_node_group_to_node_template`
- 任务与配置：`retry_task`、`skip_task`、`create_template_config`、`delete_template_config`、`update_virtual_cluster_quota`

## 调用步骤

1. 找 action：
   ```bash
   bk-cli bcs cluster_manager -h
   ```
2. 看目标 action 的默认帮助。默认 `-h` 会展示 `Usage`、`Examples`、flags，以及是否有 body schema：
   ```bash
   bk-cli bcs cluster_manager create_cluster -h
   ```
3. 如果默认帮助提示可查看 body schema，用 `-h --body-schema` 查看完整 request body schema：
   ```bash
   bk-cli bcs cluster_manager create_cluster -h --body-schema
   ```
4. 按 `Examples` 构造命令。复杂请求体统一通过 `--body '<json>'` 传入，不要猜 body 字段。
5. 首次执行或写操作前先加 `--dry-run`，确认 `request.url`、`request.params`、`request.body`、`request.headers`。

## 输入规则

- 路径参数和 query 参数是普通 flags，例如 `--clusterID`、`--nodeGroupID`、`--nodes`、`--isForce=true`。
- DELETE action 的 query string 也用 flags 传入。
- 有些写操作要求 `--body`；缺失时会返回 `missing_param` 和 `required parameter --body is missing`。
- `-h --body-schema` 只显示 schema，不执行请求。

## 常用示例

更新集群：

```bash
bk-cli bcs cluster_manager update_cluster \
  --clusterID BCS-K8S-12345 \
  --body '{"clusterID":"BCS-K8S-12345"}'
```

下架集群节点：

```bash
bk-cli bcs cluster_manager delete_nodes_from_cluster \
  --clusterID BCS-K8S-12345 \
  --nodes 10.0.0.1,10.0.0.2 \
  --deleteMode terminate \
  --isForce=true \
  --operator admin
```

创建节点组：

```bash
bk-cli bcs cluster_manager create_node_group -h
bk-cli bcs cluster_manager create_node_group -h --body-schema

bk-cli bcs cluster_manager create_node_group \
  --body '{"name":"node-group","clusterID":"BCS-K8S-12345","region":"ap-guangzhou","autoScaling":{"vpcID":"vpc-id","zones":["ap-guangzhou-1"],"maxSize":1},"launchTemplate":{"CPU":1,"GPU":0,"Mem":1},"creator":"admin","nodeOS":"linux"}'
```

回收节点组节点 V2：

```bash
bk-cli bcs cluster_manager clean_nodes_in_group_v2 \
  --nodeGroupID node-group-id \
  --clusterID BCS-K8S-12345 \
  --nodes 10.0.0.1,10.0.0.2 \
  --operator admin
```

## 排障

- `missing_param`：检查是否缺少必填 flag，例如 `--clusterID`、`--nodeGroupID`、`--projectID`、`--body`。
- `required parameter --body is missing`：先运行该 action 的 `-h`，按 `Examples` 补 `--body '<json>'`。
- body JSON 解析失败：把 JSON 压成一行，或用脚本生成合法 JSON 后再传给 `--body`。
- 不确定 body 字段：运行 `bk-cli bcs cluster_manager <action> -h --body-schema`。
- 请求不符合预期：加 `--dry-run` 检查最终请求。
