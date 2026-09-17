---
name: spacemit-robot-software-setup
description: SpacemiT Robot SDK 软件安装与源配置基础 skill；用于指导客户安装 ROS2、apt 系统包、SpacemiT 运行包、Python/uv/pip 依赖，以及配置 apt/pip 源。
---

# SpacemiT Robot Software Setup

先按 `spacemit-robot-shared` 确认开发模式、执行机器和 SDK root。本 skill 只处理软件安装、依赖检查和源配置；SDK 首次拉取走 `spacemit-robot-sdk-bootstrap`，日常构建走 `spacemit-robot-build`，远程执行走 `spacemit-robot-remote`。

## 适用范围

使用本 skill 处理：

- 用户询问怎么安装 ROS2、`ros-humble-*` 包、系统 apt 包或 SpacemiT 定制运行包。
- 用户询问怎么配置 Python、pip、uv 源，或 Python 环境依赖安装失败。
- SDK 构建提示缺少 `<system_depend>`、`dpkg` 包、ROS2 包、Python 包。
- 需要解释某个模块的软件依赖来自哪里、应安装到 PC 还是板端。

不使用本 skill 处理：

- SDK 首次 `repo init`、`repo sync` 或目录准备：使用 `spacemit-robot-sdk-bootstrap`。
- `source build/envsetup.sh`、`lunch`、`m`、`mm` 构建决策：使用 `spacemit-robot-build`。
- SSH 连通性、远程命令执行：使用 `spacemit-robot-remote`。
- 组件 API、示例、性能和专项运行：进入对应组件 skill。

## 安全规则

- 执行 `sudo apt update/install/remove`、修改 apt 源、修改全局 pip 配置、安装 uv、下载大文件或删除冲突包前，必须先向用户确认。
- 确认前要说明执行机器、开发模式、要安装或修改的内容、影响范围和回滚方式。
- 只读检查可以直接执行，例如 `dpkg -s`、`apt-cache policy`、`apt-cache show`、`command -v`、`python -m pip config list -v`、`test -f /opt/ros/humble/setup.bash`。
- 不要凭空编造 apt 源地址。SpacemiT apt 包不可见时，先判断板端源是否配置，再让用户参考官方源配置文档或板卡镜像默认源。
- 不要混用上游 `onnxruntime`、上游 `llama.cpp` 与 SpacemiT 加速包。涉及卸载冲突包时必须单独确认。

## 依赖来源优先级

按以下顺序查找依赖，不要先写死安装列表：

1. 当前任务所属模块的 `package.xml`、`pyproject.toml`、`requirements.txt`、`README.md` 或脚本。
2. SDK 公共依赖：`build/package.xml`。
3. ROS2 公共依赖：`build/package_ros2.xml`。
4. SDK 构建逻辑：`build/common.sh`、`build/build.sh`、`build/ros2.sh`、`build/envsetup.sh`、`build/python_env_build.sh`。
5. 已有部署脚本或 Debian metadata，例如 `debian/control`、`postinst`、`scripts/setup*.sh`。

## 执行位置

- `local`：默认认为在板端本机安装目标运行依赖。
- `remote`：在 PC 上通过 `spacemit-robot-remote` 到板端检查和安装目标运行依赖。
- `hybrid`：目标运行依赖、ROS2、板端 apt 包安装在板端；PC 只安装本地编辑、脚本、Python 辅助工具所需依赖。

安装前先明确“这是 PC 工具依赖”还是“这是板端运行依赖”。不能因为用户在 PC 上发起请求，就把目标运行包装到 PC。

## apt 与 package.xml 规则

- `<system_depend>` 的文本通常是 apt 包名。
- `<depend>` 通常是 SDK 包或 ROS 包依赖，不要默认当成 apt 包安装。
- `build/common.sh` 支持 `check`、`arch`、`board`、`realm`、`when`、`check_kind`、`check_arg`、`option_key`、`option_value` 等过滤或检查属性；读取依赖时要尊重这些条件。
- 基础系统依赖来自 `build/package.xml`，当前包括 `build-essential`、`cmake`、`pkg-config`、`wget`、`git`、`jq`、`pybind11-dev`、`python3-build`。
- 需要 ROS2 时再读取 `build/package_ros2.xml`，当前默认 ROS 发行版是 `humble`。
- 优先借助 SDK 构建系统做依赖检查；只有用户明确要手工安装时，才整理 `sudo apt-get install -y <packages>`。
- `AUTO_INSTALL_DEPS=yes` 会让构建系统非交互安装缺失依赖，只能在用户明确同意后使用。
- `sudo apt-get update` 只在 apt 索引陈旧、源刚变更、包不可见且用户同意时执行。

## ROS2 安装规则

- SDK 默认 `ROS_DISTRO=humble`，默认 ROS setup 为 `/opt/ros/${ROS_DISTRO}/setup.bash`。
- 先做只读检查：

```bash
test -f /opt/ros/humble/setup.bash
command -v colcon
dpkg -s ros-humble-ros-base ros-dev-tools
```

- ROS2 公共依赖来自 `build/package_ros2.xml`，当前包括 `ros-humble-ros-base`、`ros-dev-tools`、`ros-humble-robot-localization`、`ros-humble-joint-state-publisher`、`ros-humble-tf-transformations`。
- 模块额外 ROS2 依赖从模块 `package.xml` 的 `<system_depend>` 读取，例如 `ros-humble-slam-toolbox`、`ros-humble-ros2bag`。
- 构建或运行 ROS2 模块时优先使用 SDK 流程：`source build/envsetup.sh` 后执行 `sros2_setup`、`m`、`mm` 或 `build/build.sh package`，不要绕过 SDK 规则直接长期维护一套裸 `colcon build` 流程。

## Python、pip 与 uv 源规则

- 应用目录有 `pyproject.toml` 时，优先使用 SDK 的 Python 环境入口：

```bash
source build/envsetup.sh
m_env_build <app_dir>
```

- `m_env_build` 会在 `output/envs/<project-name>` 创建环境，并把 SDK 内匹配的本地 Python 项目以 editable 方式安装。
- `build/envsetup.sh` 的 `venv <python_version>` 会创建 `${SROBOTIS_ROOT}/.venv`，并设置：

```bash
export UV_INDEX_URL="https://mirrors.aliyun.com/pypi/simple"
export UV_EXTRA_INDEX_URL="https://git.spacemit.com/api/v4/projects/33/packages/pypi/simple"
```

- SpacemiT Python 包源：

```bash
https://git.spacemit.com/api/v4/projects/33/packages/pypi/simple
```

- SDK 当前常用公开镜像：

```bash
https://mirrors.aliyun.com/pypi/simple/
```

- 临时安装包时优先使用命令级参数，避免一上来修改全局配置：

```bash
python -m pip install <package> \
  --prefer-binary \
  --index-url https://git.spacemit.com/api/v4/projects/33/packages/pypi/simple \
  --extra-index-url https://mirrors.aliyun.com/pypi/simple/
```

- 如用户明确要求配置全局 pip 源，先读取当前配置，再确认后执行：

```bash
python -m pip config list -v
python -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
python -m pip config set global.extra-index-url https://git.spacemit.com/api/v4/projects/33/packages/pypi/simple
```

- `scripts/test/run_tests.py` 使用 `SROBOTIS_TEST_PIP_INDEX_URL`、`SROBOTIS_TEST_PIP_EXTRA_INDEX_URLS`、`SROBOTIS_TEST_PIP_EXTRA_INDEX_URL` 控制测试环境 pip 源；这些只用于测试入口，不要当成日常开发的唯一方式。

## SpacemiT 定制运行包

常见 SpacemiT apt 包包括：

- `spacemit-onnxruntime`
- `python3-spacemit-ort`
- `llama.cpp-tools-spacemit`
- `opencv-spacemit`
- `spacemit-ai-gateway`

检查示例：

```bash
apt-cache policy spacemit-onnxruntime python3-spacemit-ort llama.cpp-tools-spacemit opencv-spacemit spacemit-ai-gateway
```

如果 `apt-cache show <package>` 找不到这些包，通常说明 SpacemiT apt 源未配置或当前系统版本不匹配。此时不要改用上游替代包，先确认板卡镜像、系统版本、软件源和 SDK 文档要求。

## 输出要求

回答或执行后说明：

- 当前开发模式和执行机器。
- 已读取的 SDK 依赖来源。
- 要安装或检查的软件包列表。
- 是否涉及 apt 源、pip 源、全局配置或冲突包。
- 已执行的命令和结果。
- 下一步应回到 bootstrap、build、remote、sync 还是组件 skill。
