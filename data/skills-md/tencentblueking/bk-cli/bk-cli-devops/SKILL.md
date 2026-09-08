---
name: bk-cli-devops
description: 当需要通过 `bk-cli devops pipeline`、`bk-cli devops codecc`、`bk-cli devops stream` 使用蓝盾 DevOps 子系统命令时使用。适合查询和操作流水线构建、查询制品下载链接、查看 CodeCC 告警明细或统计、查询 Stream 流水线信息、触发 Stream 流水线的场景。只要用户给出 `pipelineId`、`buildId`、`taskId`、`gongfengId`、`gitProjectId`、`yamlPath` 这类 DevOps 标识，或明确提到 蓝盾、CodeCC、Stream、流水线、工蜂项目，就应该优先使用本 skill。
---

# bk-cli devops — 蓝盾 DevOps / CodeCC / Stream 能力使用说明

用于通过 `bk-cli devops` 调用蓝盾 DevOps 平台 API 的系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `devops` 命令自己的分组方式、参数语义和常见用法。

## 先判断命令形态

- `bk-cli devops` 现在只负责分组，本身没有直接 action。
- 必须先判断需求属于哪个 subsystem，再生成 `bk-cli devops <subsystem> <action>`。
- 看到“构建、制品、view、启动/停止构建”优先走 `pipeline`。
- 看到“CodeCC、告警、缺陷、统计、taskId、gongfengId”优先走 `codecc`。
- 看到“Stream、工蜂、YAML 流水线、手动触发、gitProjectId”优先走 `stream`。

## 当前覆盖范围

当前 `devops` system 按三个 subsystem 组织：

- `bk-cli devops pipeline`：`get_build_list`、`get_build_status`、`get_build_start_info`、`get_artifactory_list`、`get_artifactory_user_download_url`、`get_artifactory_third_party_download_url`、`get_view_pipelines`、`start_build`、`stop_build`
- `bk-cli devops codecc`：`get_task_detail`、`get_gf_defect_detail_by_task_id`、`get_defect_detail_by_task_id`、`get_pipeline_defect_detail`、`get_gf_defect_detail`、`get_pipeline_defect_statistic`、`get_gf_defect_statistic`、`get_gf_defect_statistic_by_task_id`、`get_defect_statistic_by_task_id`
- `bk-cli devops stream`：`get_pipelines_list_info`、`get_name2pipeline_info`、`get_pipelines_manual_trigger_info`、`trigger`

## 输入约定和易错点

- CLI flag 名保持上游接口原样，不做本地 snake_case 改写；直接按接口参数名传入，例如 `projectId`、`pipelineId`、`buildNo`、`taskId`、`pageSize`、`yamlPath`。
- `pipeline` 子命令里的 `projectId` 是 蓝盾项目英文名，不是数字 ID。
- `pipelineId` 是流水线 ID，通常为 `p-` 前缀；`buildId` 是构建 ID，通常为 `b-` 前缀。
- `codecc` 相关命令要先分清查询入口：有 `taskId` 就优先按任务查；有 `pipelineId` 就走流水线维度；有 `gongfengId` 就走工蜂开源治理维度。
- `stream get_pipelines_list_info` 使用的是路径参数 `gitProjectId`，值是工蜂项目数字 ID。
- 其余 Stream 接口里的 `projectId` 不是英文名，而是固定格式 `git_${工蜂项目ID}`。
- `start_build` 在未传 `--body` 时会发送空 JSON 对象 `{}`；如果用户已经准备好了启动参数，直接透传 `--body`。
- `stream trigger` 必须显式传入完整 JSON `--body`，不能省略。

## 选择命令的思路

### Pipeline

适用场景：
查询构建历史、看构建状态、获取手动启动参数、查询制品、取下载链接、查看 view 下的流水线、启动或停止构建。

代表命令：

```bash
bk-cli devops pipeline get_build_list --projectId myproject --pipelineId p-xxx
bk-cli devops pipeline get_build_status --projectId myproject --buildId b-xxx
bk-cli devops pipeline get_build_start_info --projectId myproject --pipelineId p-xxx
bk-cli devops pipeline get_artifactory_list --projectId myproject --pipelineId p-xxx --buildId b-xxx --page 1 --pageSize 20
bk-cli devops pipeline get_artifactory_user_download_url --projectId myproject --artifactoryType PIPELINE --path /demo/pkg.tgz
bk-cli devops pipeline get_artifactory_third_party_download_url --projectId myproject --artifactoryType PIPELINE --path /demo/pkg.tgz --ttl 600
bk-cli devops pipeline get_view_pipelines --projectId myproject --viewId allPipeline --page 1 --pageSize 20
bk-cli devops pipeline start_build --projectId myproject --pipelineId p-xxx
bk-cli devops pipeline stop_build --projectId myproject --pipelineId p-xxx --buildId b-xxx
```

补充说明：

- `get_build_list` 常和 `status`、`trigger`、`page`、`pageSize` 一起用。
- `get_view_pipelines` 用于按 view 查询流水线列表；如果用户提到 view、筛选流水线名、按创建人过滤，优先考虑它。
- `start_build` 支持 `--buildNo`，也支持通过 `--body` 传完整启动参数。

### CodeCC

适用场景：
查任务详情、普通任务告警明细、工蜂治理告警明细、按流水线查告警、查各类统计数据。

代表命令：

```bash
bk-cli devops codecc get_task_detail --taskId 123456789
bk-cli devops codecc get_defect_detail_by_task_id --taskId 123456789 --pageNum 1 --pageSize 20
bk-cli devops codecc get_gf_defect_detail_by_task_id --taskId 123456789 --dimension SECURITY
bk-cli devops codecc get_pipeline_defect_detail --pipelineId p-xxx --dimension STANDARD
bk-cli devops codecc get_gf_defect_detail --gongfengId 12345 --toolName COVERITY
bk-cli devops codecc get_pipeline_defect_statistic --pipelineId p-xxx --dimension SECURITY
bk-cli devops codecc get_gf_defect_statistic --gongfengId 12345
bk-cli devops codecc get_gf_defect_statistic_by_task_id --taskId 123456789
bk-cli devops codecc get_defect_statistic_by_task_id --taskId 123456789
```

补充说明：

- `toolName` 和 `dimension` 常一起出现；如果用户明确给了工具名，直接透传。
- 多数明细接口支持 `buildId`，未传时默认按最新构建取数。
- `pageNum` / `pageSize` 是 CodeCC 这组接口常见分页参数，不要误写成 `page`。

### Stream

适用场景：
查工蜂项目下的 Stream 流水线列表、按 YAML 路径查流水线、获取手动触发信息、触发 Stream 流水线。

代表命令：

```bash
bk-cli devops stream get_pipelines_list_info --gitProjectId 12345
bk-cli devops stream get_name2pipeline_info --projectId git_12345 --yamlPath .ci/demo.yml
bk-cli devops stream get_pipelines_manual_trigger_info --projectId git_12345 --pipelineId p-xxx --branchName main
bk-cli devops stream trigger --projectId git_12345 --pipelineId p-xxx --body '{"path":".ci/demo.yml","branch":"main","projectId":"git_12345","customCommitMsg":"manual trigger"}'
```

补充说明：

- `gitProjectId` 和 `projectId=git_<id>` 很容易混淆，先按 action 分清参数名再生成命令。
- `yamlPath` 通常是 `.ci/*.yml` 或 `.ci/*.yaml`。
- `trigger` 的 `--body` 要和上游触发契约一致；如果用户只给了零散字段，不要擅自脑补缺失字段。
