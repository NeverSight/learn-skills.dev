---
name: hccl-test
description: HCCL (Huawei Collective Communication Library) performance testing for Ascend NPU clusters. Use for testing distributed communication bandwidth, verifying HCCL functionality, and benchmarking collective operations like AllReduce, AllGather, AlltoAll. Covers MPI installation, tool compilation, execution parameters, and result analysis.
keywords:
    - hccl
    - 性能测试
    - 集合通信
    - 打流
---

# HCCL Performance Test

HCCL性能测试工具用于测试HCCL（Huawei Collective Communication Library）集合通信的功能正确性以及性能。

## Overview

- **适用场景**：分布式训练场景下的集合通信性能测试
- **源码位置**：`${INSTALL_DIR}/tools/hccl_test`
- **支持版本**：CANN 8.3.RC1, CANN 8.5

### 查看产品型号

```bash
dmidecode -t system | head -20 | grep Product
```

### 支持的产品型号

| 产品系列 | 最大 Rank 数 | 备注 |
|----------|-------------|------|
| Atlas 训练系列产品 | 4096 | - |
| Atlas A2 训练系列产品 | 32K | - |
| Atlas A3 训练系列产品/Atlas A3 推理系列产品 | 32K | AlltoAll/AlltoAllV 最大 8K |
| Atlas 300I Duo 推理卡 | - | - |

### 支持的集合通信算子

HCCL Test 工具支持以下 10 种集合通信算子测试：

| 算子 | 可执行文件 | 通信模式 | 适用场景 |
|------|-----------|---------|---------|
| **AllReduce** | `all_reduce_test` | 多对多 | 梯度聚合、参数同步 |
| **AllGather** | `all_gather_test` | 多对多 | 数据聚合、参数收集 |
| **AllGatherV** | `all_gatherv_test` | 多对多 | 变长数据聚合 |
| **AlltoAll** | `alltoall_test` | 多对多 | 数据重排、负载均衡 |
| **AlltoAllV** | `alltoallv_test` | 多对多 | 变长数据全对全通信 |
| **Broadcast** | `broadcast_test` | 一对多 | 配置分发、初始化 |
| **Reduce** | `reduce_test` | 多对一 | 结果收集到根节点 |
| **ReduceScatter** | `reduce_scatter_test` | 多对多 | 归约后分发 |
| **ReduceScatterV** | `reduce_scatterv_test` | 多对多 | 变长归约后分发 |
| **Scatter** | `scatter_test` | 一对多 | 数据分发 |

> **选择建议**: 分布式训练场景最常用的是 **AllReduce**（梯度聚合）和 **AllGather**（参数同步）。

## Quick Reference

```bash
# 1. 查看产品型号
dmidecode -t system | head -20 | grep Product

# 2. 编译工具
cd ${INSTALL_DIR}/tools/hccl_test
make MPI_HOME=/usr/local/mpich ASCEND_DIR=${INSTALL_DIR}

# 3. 单机测试（替换为本机 IP）
echo "175.99.1.3:8" > hostfile
mpirun -f hostfile -n 8 ./bin/all_reduce_test -p 8 -b 8K -e 256M -f 2 -d fp32 -o sum
```

---

## 1. MPI Installation

HCCL性能测试工具依赖MPI拉起多个进程，默认使用 **MPICH**。

### MPICH Installation (Recommended)

#### Download

下载地址：https://www.mpich.org/static/downloads/

| 产品系列 | 推荐版本 |
|----------|----------|
| Atlas A3 训练系列产品/Atlas A3 推理系列产品 | MPICH 4.1.3 |
| Atlas A2 训练系列产品 | MPICH 3.2.1 |
| Atlas 训练系列产品 | MPICH 3.2.1 |
| Atlas 300I Duo 推理卡 | MPICH 3.2.1 |

#### Installation Steps

```bash
# 1. 解压
tar -zxvf mpich-${version}.tar.gz
cd mpich-${version}

# 2. 配置编译选项
# Atlas A3 产品（必须使用 TCP 协议）
./configure --disable-fortran --prefix=/usr/local/mpich --with-device=ch3:nemesis

# 其他产品
./configure --disable-fortran --prefix=/usr/local/mpich

# 3. 编译安装
make -j 32 && make install
```

**参数说明**：
- `--disable-fortran`：禁用 Fortran 语言支持
- `--prefix`：MPI 安装路径（可自定义）
- `--with-device=ch3:nemesis`：指定使用 TCP 协议（Atlas A3 必须配置）

### Open MPI Installation (Alternative)

适用于需要 IPv6 支持的场景。

下载地址：https://www.open-mpi.org/software/ompi/v4.1/ (Open MPI 4.1.5)

```bash
# 1. 解压
tar -zxvf openmpi-4.1.5.tar.gz
cd openmpi-4.1.5

# 2. 修改支持的最大 Host 数量（大规模集群需要）
# 修改 orte/mca/routed/radix/routed_radix_component.c
# mca_routed_radix_component.radix = 集群中总卡数/单Server中卡数

# 修改 orte/mca/plm/rsh/plm_rsh_component.c
# mca_plm_rsh_component.num_concurrent = 集群中总卡数/单Server中卡数

# 3. 配置
./configure --disable-fortran --enable-ipv6 --prefix=/usr/local/openmpi

# 4. 编译安装
make -j 32 && make install
```

### Network Configuration

配置网络节点信息（在每个参与通信的节点上执行）：

```bash
# 1. 添加主机信息到 /etc/hosts
# 格式：IP地址 主机名
echo "172.16.0.100 $(hostname)" >> /etc/hosts

# EulerOS 需要刷新
nmcli c reload
```

### SSH Trust Configuration

```bash
# 1. 生成密钥（如已存在可跳过）
ssh-keygen -t rsa

# 2. 复制公钥到其他节点
ssh-copy-id -i /root/.ssh/id_rsa.pub ${node_ip}

# 3. 验证 SSH 登录
ssh ${node_ip}
```

---

## 2. Tool Compilation

### Environment Variables

```bash
# MPICH 环境
export INSTALL_DIR=/usr/local/Ascend/ascend-toolkit/latest
export PATH=/usr/local/mpich/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/mpich/lib:${INSTALL_DIR}/lib64:$LD_LIBRARY_PATH
```

```bash
# Open MPI 环境
export INSTALL_DIR=/usr/local/Ascend/ascend-toolkit/latest
export PATH=/usr/local/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/openmpi/lib:${INSTALL_DIR}/lib64:$LD_LIBRARY_PATH
```

> **Note**: `INSTALL_DIR` 是 CANN 软件安装路径。root 用户默认安装路径为 `/usr/local/Ascend/ascend-toolkit/latest`。

### Compile

```bash
cd ${INSTALL_DIR}/tools/hccl_test

# MPICH
make MPI_HOME=/usr/local/mpich ASCEND_DIR=${INSTALL_DIR}

# Open MPI
make MPI_HOME=/usr/local/openmpi ASCEND_DIR=${INSTALL_DIR}
```

编译成功后，在 `${INSTALL_DIR}/tools/hccl_test/bin` 目录下生成可执行文件：

| 可执行文件 | 说明 |
|-----------|------|
| `all_reduce_test` | AllReduce 算子测试 |
| `all_gather_test` | AllGather 算子测试 |
| `all_gatherv_test` | AllGatherV 算子测试 |
| `alltoall_test` | AlltoAll 算子测试 |
| `alltoallv_test` | AlltoAllV 算子测试 |
| `broadcast_test` | Broadcast 算子测试 |
| `reduce_scatter_test` | ReduceScatter 算子测试 |
| `reduce_test` | Reduce 算子测试 |
| `scatter_test` | Scatter 算子测试 |

---

## 3. Tool Execution

### Pre-test Checklist

执行 HCCL Test 前，请确保完成以下检查：

#### 1. 清理残余进程

> **重要**: 如果之前测试异常退出，可能会有残余进程影响本次测试。

```bash
# 检查是否有残余的 hccl_test 进程
ps aux | grep -E "(all_reduce_test|all_gather_test|mpirun)"

# 清理残余进程（MPICH）
mpirun -f hostfile -n 8 pkill -9 -f "all_reduce_test|all_gather_test|mpirun"

# 清理残余进程（Open MPI）
mpirun -hostfile hostfile -n 8 pkill -9 -f "all_reduce_test|all_gather_test|openmpi"
```

**常见问题**: 如果首次运行出现 `Process 0 HcclGetRootInfo failed` 或 `retcode: 7` 错误，通常是因为残余进程干扰，请先执行清理命令。

#### 2. 环境检查清单

| 检查项 | 命令 | 预期结果 |
|-------|------|---------|
| NPU 状态 | `npu-smi info` | 所有 NPU 显示 OK |
| MPI 环境 | `which mpirun` | 显示 mpirun 路径 |
| HCCL Test 工具 | `ls ${INSTALL_DIR}/tools/hccl_test/bin/` | 显示 10 个可执行文件 |
| 防火墙状态 | `systemctl status firewalld` | 建议关闭 |

### Prerequisites

```bash
# 1. 关闭防火墙
systemctl stop firewalld

# 2. 大规模集群调整内核参数（可选）
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
```

### Hostfile Configuration

**MPICH Format** (`节点IP:卡数`)：

```bash
# 单机测试（本机 IP 为 175.99.1.3，8 卡）
175.99.1.3:8

# 双机测试
175.99.1.3:8
175.99.1.4:8
```

**Open MPI Format** (`节点名 slots=卡数`)：

```bash
# 节点名与卡数
node3 slots=8
node4 slots=8
```

> **Important**: Hostfile 中请将属于同一超节点的 AI Server 信息配置在一起，不支持交叉配置。

### Execution Commands

```bash
# MPICH 单机测试
mpirun -n 8 ./bin/all_reduce_test -p 8 -b 8K -e 64M -f 2 -d fp32 -o sum

# MPICH 多机测试
mpirun -f hostfile -n 16 ./bin/all_reduce_test -p 8 -b 8K -e 64M -f 2 -d fp32 -o sum

# Open MPI 单机测试
mpirun --prefix /usr/local/openmpi -n 8 ./bin/all_reduce_test -p 8 -b 8K -e 64M -f 2 -d fp32 -o sum

# Open MPI 多机测试
mpirun --prefix /usr/local/openmpi -hostfile hostfile \
  -x LD_LIBRARY_PATH -x HCCL_SOCKET_FAMILY -x HCCL_SOCKET_IFNAME \
  --allow-run-as-root --mca btl_tcp_if_include eth0 --mca opal_set_max_sys_limits 1 \
  -n 16 ./bin/all_reduce_test -p 8 -b 8K -e 64M -f 2 -d fp32 -o sum
```

### HCCL Environment Variables (Optional)

> **Note**: 以下环境变量默认无需配置。如果测试无法正常运行，再根据实际情况配置。

```bash
# 通信网卡 IP 协议版本
# AF_INET: IPv4 (默认)
# AF_INET6: IPv6
export HCCL_SOCKET_FAMILY=AF_INET

# 通信网卡名配置（4种规格任选1种）
# 精确匹配
export HCCL_SOCKET_IFNAME=eth0,enp0           # 使用指定的 eth0 或 enp0 网卡
export HCCL_SOCKET_IFNAME=^=eth0,enp0         # 不使用 eth0 与 enp0 网卡
# 模糊匹配
export HCCL_SOCKET_IFNAME=eth,enp             # 使用所有以 eth 或 enp 为前缀的网卡
export HCCL_SOCKET_IFNAME=^eth,enp            # 不使用任何以 eth 或 enp 为前缀的网卡

# Socket 建链超时时间（秒）
# 大规模集群建议增加：3K卡建议240s，5K卡建议600s
export HCCL_CONNECT_TIMEOUT=600

# NPU 间共享缓冲区大小（MB）
# 建议设置大于测试数据量以获得最佳性能
export HCCL_BUFFSIZE=2048
```

---

## 4. Parameters

### MPI Parameters

#### MPICH Parameters

| 参数 | 必选 | 说明 |
|------|------|------|
| `-f <hostfile>` | 可选 | Hostfile 节点列表文件（多机必填） |
| `-n <number>` | 必选 | 启动的 NPU 总数（节点数 × 每节点 NPU 数） |

#### Open MPI Parameters

| 参数 | 必选 | 说明 |
|------|------|------|
| `--prefix <path>` | 可选 | Open MPI 安装路径（多机建议配置） |
| `-hostfile <file>` | 可选 | Hostfile 节点列表文件（多机必填） |
| `-n <number>` | 必选 | 启动的 NPU 总数 |
| `-x <env>` | 必选 | 传递给远程节点的环境变量 |
| `--allow-run-as-root` | 可选 | 允许 root 用户执行 |
| `--mca btl_tcp_if_include <nic>` | 可选 | 指定通信网卡 |
| `--mca opal_set_max_sys_limits 1` | 可选 | 大规模集群建议配置 |

### HCCL Test Parameters

| 参数 | 长格式 | 必选 | 默认值 | 说明 |
|------|--------|------|--------|------|
| `-p <npus>` | `--npus` | 可选 | 节点NPU总数 | 单节点参与训练的 NPU 个数 |
| `-b <size>` | `--minbytes` | 可选 | 64M | 测试数据量起始值（单位：K/M/G） |
| `-e <size>` | `--maxbytes` | 可选 | 64M | 测试数据量结束值（单位：K/M/G） |
| `-i <bytes>` | `--stepbytes` | 可选 | 计算 | 增量步长（单位：Bytes） |
| `-f <factor>` | `--stepfactor` | 可选 | - | 乘法因子 |
| `-o <op>` | `--op` | 可选 | sum | 操作类型：sum/prod/max/min |
| `-r <root>` | `--root` | 可选 | 0 | 根节点 Device ID（broadcast/reduce/scatter） |
| `-d <type>` | `--datatype` | 可选 | fp32 | 数据类型 |
| `-n <iters>` | `--iters` | 可选 | 20 | 迭代次数 |
| `-w <warmup>` | `--warmup_iters` | 可选 | 10 | 预热迭代次数 |
| `-c <0/1>` | `--check` | 可选 | 1 | 是否开启结果校验 |
| `-z <0/1>` | `--zero_copy` | 可选 | 0 | 是否开启零拷贝 |

### Data Size Configuration Examples

```bash
# 固定数据量测试
-b 100M -e 100M

# 步长增量测试
-b 100M -e 400M -i 500

# 乘法因子测试
-b 100M -e 400M -f 2  # 测试 100M, 200M, 400M

# 持续测试（使用起始值）
-b 100M -e 400M -i 0  # 只测试 100M
```

### Supported Data Types

| 算子 | 支持的数据类型 |
|------|---------------|
| all_reduce_test, reduce_scatter_test, reduce_test | int8, int16, int32, int64, fp16, fp32, bfp16 |
| broadcast_test, all_gather_test, alltoall_test, scatter_test | int8, uint8, int16, uint16, int32, uint32, int64, uint64, fp16, fp32, fp64, bfp16 |

---

## 5. Constraints

### NPU Count per Node (`-p` parameter)

| 产品系列 | `-p` 范围 | Device ID |
|----------|-----------|-----------|
| Atlas A3 训练系列产品/Atlas A3 推理系列产品 | 1~16 | [0, p-1] |
| Atlas A2 训练系列产品 | 1~8 | [0, p-1] |
| Atlas 训练系列产品 | 1, 2, 4, 8 | [0, p-1] |

### Atlas 300I Duo Specific Constraints

| 测试命令 | 最大 `-p` 值 |
|----------|-------------|
| all_gather_test | 32 |
| all_gatherv_test | 4 |
| all_reduce_test | 32 |
| alltoall_test | 4 |
| alltoallv_test | 4 |
| reduce_scatter_test | 32 |
| reduce_scatterv_test | 4 |

### Zero Copy Constraints

零拷贝功能（`-z 1`）生效条件：
- 仅支持 Atlas A3 训练系列产品/Atlas A3 推理系列产品
- 仅支持 reduce_scatter_test、all_gather_test、all_reduce_test、broadcast_test
- 仅支持通信算法编排展开位置在 AI CPU 的场景

---

## 6. Results

### Output Format

```
data_size      avg_time(us)    alg_bandwidth(GB/s)    check_result
8192           125.3           0.065                  success
16384          132.1           0.124                  success
...
```

| 字段 | 说明 |
|------|------|
| `data_size` | 单个 NPU 上参与集合通信的数据量（Bytes） |
| `avg_time` | 集合通信算子执行耗时（us） |
| `alg_bandwidth` | 算法带宽（GB/s），计算方式：集合通信数据量/耗时 |
| `check_result` | 结果校验标识：success/failed/NULL |

### Result Verification Limits

归约类算子结果校验最大支持卡数：

| 操作类型 | 算子 | INT8 | INT16 | INT32 | INT64 | FP32 | FP16 | BF16 |
|----------|------|------|-------|-------|-------|------|------|------|
| Prod | AllReduce, Reduce, ReduceScatter | 6 | 14 | 30 | 62 | 127 | 15 | 127 |
| Sum | AllReduce, Reduce, ReduceScatter | 63 | 16383 | ~1e9 | ~1e18 | ~1e6 | 511 | 63 |
| Sum | ReduceScatterV | 11 | 181 | 46340 | ~1e9 | 2896 | 31 | 11 |

### Quick Verification Script

使用快速验证脚本一次性测试所有算子：

```bash
# 使用默认配置测试 4 卡
./scripts/quick-verify.sh

# 测试 8 卡
./scripts/quick-verify.sh 8

# 使用 Open MPI 测试 4 卡
./scripts/quick-verify.sh 4 openmpi
```

脚本会自动：
1. 检查环境（MPI、CANN、NPU）
2. 清理残余进程
3. 顺序测试所有 10 个算子
4. 输出测试汇总结果

### Parse Results

使用结果解析脚本生成汇总表格：

```bash
./scripts/parse-hccl-result.py output.log
```

---

## 7. Common Issues

See [references/common-issues.md](references/common-issues.md) for detailed troubleshooting:

- **gethostbyname failed** - 配置 /etc/hosts
- **MPI 库文件链接错误** - 配置 LD_LIBRARY_PATH
- **"bash:orted:未找到命令"** - 清理残余进程
- **"retcode: 7" 错误** - 清理残余进程

### Kill Residual Processes

```bash
# MPICH
mpirun -f hostfile -n 512 pkill -9 -f "all_reduce_test|mpirun"

# Open MPI
mpirun -hostfile hostfile -n 512 pkill -9 -f "all_reduce_test|openmpi"
```

---

## Official References

- **CANN 8.3.RC1**: https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/devaids/hccltool/HCCLpertest_16_0001.html
- **CANN 8.5**: https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/devaids/hccltool/HCCLpertest_16_0001.html
