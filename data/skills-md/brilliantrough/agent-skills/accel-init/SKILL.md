---
name: accel-init
description: 深度学习算力平台初始化主入口：探测（或由用户直说）加速器平台与现状，搭 Python 双栈底座（miniconda+uv+清华源），按平台调研 wheel 矩阵/fork/生态兼容，出方案、执行、走验证阶梯，最后交棒 accel-skill-template 落盘。Use when setting up a fresh compute server for deep learning（CUDA/MUSA/Ascend/ROCm 等驱动、SDK、PyTorch、triton、transformers 生态），when asked 初始化算力环境/装平台栈/新服务器配置深度学习环境，or when a platform stack needs repair and re-validation. 只做 Python 环境不涉平台时直接按常规流程；落盘模板细节看 accel-skill-template。
---

# accel-init：算力平台初始化编排

线性六阶段，每阶段产出明确再进下一阶段；任何一步实况与预期不符，停下对齐而不是硬走。

## 阶段 0：确定平台与现状

先探测，用户已直说平台时也抽查验证：

```bash
# 厂商 smi 工具（命中任一即强信号）
nvidia-smi -L 2>/dev/null; mthreads-gmi 2>/dev/null; npu-smi info 2>/dev/null; rocm-smi --showproductname 2>/dev/null
lspci | grep -iE 'nvidia|display|3d|accelerator|processor.*musa|huawei|amd/ati'   # vendor ID 交叉确认
ls /dev/nvidia* /dev/davinci* /dev/musa* 2>/dev/null
# 驱动/SDK/运行时现状
lsmod | grep -E 'nvidia|mthreads|davinci|amdgpu'; ls /usr/local/ | grep -iE 'cuda|musa|ascend|rocm|CANN'
```

对照 [platforms.md](platforms.md) 的注册表：平台、检测命令、官方入口、已知生态结论。
探测不清或多种加速器并存 → 问用户，不猜。

**环境边界三查**（同样影响后续所有阶段）：

```bash
uname -m                      # aarch64（昇腾等）wheel 生态窄，部分包无预编译只能源编
ls /.dockerenv 2>/dev/null; grep -qE 'docker|kubepods' /proc/1/cgroup 2>/dev/null && echo 容器内
# 容器内 lspci 不可靠，以 /dev 结点 + smi 为准；官方容器路线（nvidia-container/厂商镜像）作为选项提给用户
curl -sm3 -o /dev/null -w '%{http_code}\n' https://pypi.tuna.tsinghua.edu.cn/simple/ https://hf-mirror.com/ 2>/dev/null
```

网络探测不可达（科研服务器常态）→ 源配置全部改走可达路径：访谈时问内网镜像/离线包/代理，不要照抄清华源与 hf-mirror。

**现状分级**（决定后面阶段的范围）：驱动+SDK 全有 / 只有驱动 / 裸机。共享集群通常是第一种。

## 阶段 1：访谈（只问影响行为的）

- root/sudo 有无 → 决定驱动层装不装（无 root 且无驱动 → 停，交回用户找管理员）。
- 装到哪层：最小 torch 栈，还是 +transformers/vllm/分布式。
- 项目对 Python 版本有无要求（决定 wheel 矩阵选哪一列 ABI）。
- 独占还是共享机 → 命名规范、缓存位置、测试卡位（别人占用的卡不测）。
- SDK/版本有无指定（无指定则调研后给推荐行让用户拍板）。
- 外网不可达时：内网镜像地址、离线包在哪、代理怎么用（三选一至少有一样）。

## 阶段 2：Python 双栈底座（与平台无关，先搭）

约定：**miniconda 与 uv 都装好，用户爱用哪个用哪个**；三处默认源配清华：

- miniconda 安装到 `{{用户认可的目录}}`（共享机放大容量盘；安装包走清华镜像 `https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/`）。
- uv：官方安装脚本或 pip 装，任一可用方式（无外网时 `pip install uv` 也可从内网/镜像源拿到）。
- 缓存放大盘：pip/uv/HF 缓存目录指向大容量盘（软链或配置），别塞爆 /home 小盘。
- 源配置三处：pip（`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`）、conda（`~/.condarc` 清华 channels）、uv（`UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple`，写进 `~/.config/uv/uv.toml` 或 shell 配置）。
- apt 源**只提醒不改**：告知清华/中科大镜像地址与手动换法，是否换由用户决定（发行版格式差异大，改错会搞坏 apt）。
- 底座事实全部记入宿主机层（阶段 5 落盘）。

已有 conda/uv/pip 配置的，逐项查实况后只补缺，不覆盖既有配置（尤其已有私密/内网源时保留本机值）。

**数据底座**（算力服务器必做，与平台无关）：按 [model-datasets](../model-datasets/SKILL.md) skill 落地——/data 大盘准备（按现状决策：直接用/软链/初始化 LVM+fstab）、`/data/models|datasets|hub` 目录、uv tool 装 `hf`/`modelscope` CLI、镜像环境变量（HF_ENDPOINT=hf-mirror、HF_HOME、HF_HUB_DISABLE_XET=1）、`dl` 脚本与验证清单（下个 tiny 模型试通后清理）。/data 初始化含分区/格式化，动手前先向用户确认盘是空的。

## 阶段 3：平台调研

**第一入口是厂商官方文档/下载中心，不是公共镜像源。** 平台专用 wheel（torch 后端包、平台版 triton、厂商通信库）在 PyPI/清华源不存在或版本错误——公共源搜不到只证明“不在公共源”，不证明平台不支持；厂商文档怎么写就怎么装。用宿主可用的 web 搜索工具（本项目规范：tavily/firecrawl，不用内置弱搜索）。

检索路径（依次）：
1. 厂商官网 → 文档中心/下载中心 → 安装指南：找 pip index-url、离线 SDK 包、驱动固件下载、版本兼容矩阵。
2. 厂商 GitHub org（如 MooreThreads、Ascend、ROCm）→ torch 后端仓库 README：版本匹配行、生态支持声明（哪些库上游原生、哪些厂商 fork）。
3. 检索式参考：`{{厂商}} {{SDK名}} 安装指南 pip 源`、`{{厂商}} pytorch wheel index-url`、`site:{{官方域}}`。
4. 查到 index-url 后必须实查闭环：`python -m pip index versions torch --index-url <厂商源>`——文档可能落后，以实查为准并记录日期。

逐项查证清单（对照 platforms.md 注册表，含各平台官方入口）：

1. **兼容集**：OS ↔ 驱动 ↔ SDK ↔ 工具链版本约束（官方矩阵）。
2. **wheel 矩阵**：厂商 pip index 上 `torch / torch 后端包 / torchvision / torchaudio / triton(平台版) / tilelang 类` 的可用版本行 × Python ABI；`python -m pip index versions <pkg> --index-url <厂商源>` 实查。
3. **生态兼容**：transformers/accelerate/vllm 等是上游原生支持、厂商 fork（分支+版本）还是不支持——逐库记录证据链接。
4. **防串要点**：公共 CUDA wheel 哪些包会顶掉平台 torch（torch/torchvision/triton/flash-attn/bitsandbytes/nvidia-*）。
5. 现状检查：已装 SDK 的版本、用户态目录、LD_LIBRARY_PATH 约定。

产出：候选方案（通常 1–2 个版本行）+ 步骤清单 + 风险点，给用户拍板。

## 阶段 4：执行与验证阶梯

- 用户态优先；root 操作（驱动、内核模块、系统包）逐条列出并取得明确确认再动。
- **动手前磁盘预检**：`df -h` 目标盘（torch 栈 + SDK + 缓存动辄几十 GB）；不够先清理或换盘，再开装。
- **长下载/长编译后台化**：大 wheel、SDK 离线包、源码编译放 `nohup`/后台 + 轮询日志，不要阻塞在单次命令里。
- 验证阶梯逐级走，每级通过再上一级：
  L1 工具链/版本查询 → L2 ldd 无缺库 → L3 单设备可见+小 matmul+autocast+synchronize → L4 单进程通信库 → L5 双进程 torchrun all-reduce → L6 短真实 workload。
- 任何一级失败：回阶段 3 重查兼容集，不重复硬装。
- 全程记录：确切版本、命令、路径、输出摘要（脱 PID/作业名）——阶段 5 落盘要用。

## 阶段 5：落盘交棒

按 [accel-skill-template](../accel-skill-template/SKILL.md) 固化验证过的知识：
平台三层是**固定通用名**三件套（accel-platform-install / accel-pytorch-python / accel-pytorch-code-porting，已随套装装在本机）——**就地改写正文**为当前平台（每件头部有「如何特化」指引），不新建平台名 skill；宿主机事实进 host 层（本机命名，永不入安装名单）。
改写后的三件套即本机该平台的执行依据；内容对其他机器普适时，跑 `platform-environment-skill-audit` 脱敏后回流仓库更新分发版（旧实例进 git 历史；已装机器不追新版）。

## 边界

- 本 skill 不写代码、不移植项目——那是 `<platform>-pytorch-code-porting` 的事。
- CPU-only 工作站配 Python 底座：阶段 2 单独适用，其余阶段跳过。
- 每台机器的平台栈事实只在宿主机层，平台通用知识只在平台三层，两层不混。
