---
name: ros-robotics
description: 适用于 ROS 1 / ROS 2 机器人开发、迁移与联调的 skill。覆盖 catkin/catkin_tools、colcon/ament、package.xml、CMakeLists.txt、launch、URDF/Xacro、RViz、TF、Navigation2、ros2_control、串口/CAN、MCU 与 micro-ROS 等常见工程场景。
---

# ROS Robotics

## 何时使用

当用户请求涉及以下任一主题时使用本 skill：

- `catkin_ws`、`colcon_ws`、`src/CMakeLists.txt`、`package.xml`、`setup.py`
- ROS 1 / ROS 2 package 新建、移植、构建、测试、调试
- `launch` / `launch.py`、参数 YAML、`URDF/Xacro`、RViz、TF
- `topic` / `service` / `action` / `msg` / `srv` / `QoS`
- 底盘、IMU、LiDAR、相机、定位、SLAM、Navigation2、`ros2_control`
- Gazebo / Ignition 仿真、传感器仿真、`ros_gz_bridge`
- Docker 容器化 ROS 开发、`docker-compose` 多节点编排
- Lifecycle 节点、`rclcpp_components` 组件化、进程内通信
- `rosbag2` 录制回放、`mcap`、离线诊断
- SLAM 建图（Cartographer、SLAM Toolbox、ORB-SLAM）
- DDS / QoS 配置、`ROS_DOMAIN_ID`、RMW 选择、多机网络
- 自定义 `msg` / `srv` / `action` 接口定义与生成
- 多机器人系统、命名空间隔离、跨机通信
- MoveIt 2 运动规划、SRDF、运动学插件
- ROS 2 CI/CD（GitHub Actions、colcon test、ament_lint）
- Foxglove Studio / PlotJuggler 数据可视化与离线分析
- MCU / RTOS / UART / CAN / `micro-ROS` 协同开发

## 先做什么

### 1. 先识别工作区

```bash
python scripts/detect_ros_workspace.py <workspace-path>
```

### 2. 再做一致性检查

```bash
python scripts/check_ros_workspace_consistency.py <workspace-path>
```

### 3. 按问题加载最少必要文档

- ROS 1：`references/ros1-catkin.md`
- ROS 2：`references/ros2-colcon.md`
- 混合 / 迁移：`references/interop-and-migration.md`
- 模型 / TF：`references/robot-description-and-tf.md`
- 导航：`references/navigation2.md`
- 控制：`references/ros2-control.md`
- 嵌入式：`references/micro-ros-and-embedded.md`
- 仿真：`references/gazebo-simulation.md`
- Lifecycle / 组件：`references/lifecycle-and-components.md`
- DDS / QoS / 网络：`references/dds-qos-networking.md`
- 录制回放 / 诊断：`references/rosbag-diagnostics.md`
- SLAM / 建图：`references/slam-mapping.md`
- Docker：`references/docker-ros.md`
- 自定义接口：`references/custom-interfaces.md`
- 多机器人：`references/multi-robot.md`
- MoveIt 2：`references/moveit2.md`
- CI/CD：`references/ros2-cicd.md`
- 可视化：`references/foxglove-visualization.md`
- 排障：`references/debug-playbooks.md`
- 审查：`references/review-checklist.md`

## 必须遵守的原则

- 先识别构建系统，再改代码
- 先修 `package.xml` / `CMakeLists.txt` 一致性，再谈重构
- 先看 TF、时间戳、frame、单位，再怪算法
- 先证据链，再修改：构建输出、topic、TF、参数、日志必须可验证
- ROS 1 → ROS 2 先桥接或分层，不要一口气推倒重来
- MCU / `micro-ROS` 先判断是否真的需要进入 ROS 图

## 常见任务处理方式

### 新增或修复 package

- 先判定包类型：`catkin`、`ament_cmake`、`ament_python`
- 先补依赖声明，再补构建逻辑，再补安装规则
- 自定义 `msg` / `srv` / `action` 优先检查生成顺序和依赖闭环（详见 `references/custom-interfaces.md`）

### 构建失败

- 先跑 `rosdep`
- 再核对 `package.xml` 与构建脚本
- 再看环境是否正确 source
- 再看系统依赖、ABI、发行版兼容

### 运行正常但机器人表现不对

- 先看 launch、namespace、remap、参数
- 再看 topic 名称、频率、时间戳、单位、`frame_id`
- 再看 TF 是否单根、静态 / 动态是否分清
- 最后再怀疑算法本身

### Nav2 / `ros2_control`

- Navigation2 优先排 `/cmd_vel` 链路、定位质量、控制频率和底盘单位
- `ros2_control` 优先排硬件接口类型、控制器 YAML、读写周期和 active 状态

### MCU / `micro-ROS`

- 先判断 Linux 侧桥接节点是否足够
- 若 MCU 必须进入 ROS 2 图，再考虑 `micro-ROS`
- 严格检查字节序、校验、超时、重连、时间源和失连保护

## 反模式

- 同一个包混写 `catkin` 与 `ament`
- 只改 `CMakeLists.txt` 不改 `package.xml`
- 忽略 TF、时间戳、单位、坐标轴定义
- 把驱动、协议、滤波、控制、诊断全塞进一个大节点
- 迁移 ROS 1 → ROS 2 时只做 API 替换，不做系统验证

## 输出要求

使用本 skill 处理任务时，优先输出：

1. 当前工作区和包类型判断
2. 关键依据与假设
3. 修改点与原因
4. 最小构建 / 测试 / 运行命令
5. 风险点与回归检查点
