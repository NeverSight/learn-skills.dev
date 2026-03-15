---
name: tdx-quant-dev
description: 通达信量化平台(TdxQuant)开发辅助技能。当用户提到“通达信”、“TDX”、“TdxQuant”、“量化交易”或询问关于“tqcenter”模块的使用时，使用此技能。它可以帮助搭建环境、调用API、获取行情数据和实现交易策略。
---

# 通达信量化开发技能 (TdxQuant Development Skill)

本技能用于辅助在通达信量化平台 (TdxQuant) 上开发量化交易策略。

## 核心概念

TdxQuant 将 Python 集成到通达信金融终端中。它允许 Python 脚本访问实时和历史行情数据并执行交易策略。
核心模块是 `tqcenter`。

## 环境配置

### 1. Python 路径设置

要使用 `tqcenter` 模块，必须确保 Python 环境能找到该模块。该模块通常位于通达信安装目录下的 `PYPlugins/user` 目录中 (例如 `C:/new_tdx64/PYPlugins/user`)。

通常需要在导入前将此路径添加到 `sys.path`：

```python
import sys
sys.path.append('C:/new_tdx64/PYPlugins/user') 
from tqcenter import tq

if __name__ == '__main__':
    #所有策略连接通达信客户端都必须调用此函数进行初始化
    tq.initialize(__file__)

    #获取平安银行日线前复权收盘数据
    df = tq.get_market_data(
        field_list = ['Close'],
        stock_list = ["000001.SZ"],
        start_time = '20251219',
        end_time = '20251225',
        dividend_type='front',
        period='1d',
    )
    print(df)
```

### 2. 行情数据下载（重要）

**注意：** Python 接口之所以能获取到行情数据，是因为通达信**提前下载好了**行情数据。调用 Python 接口实际上**并没有发生网络请求**，而是直接从本地已经下载好的行情数据文件中读取。如果发现获取到的数据不是最新的，可能是没有下载最新的行情数据导致的。

行情数据包含两项，需要手动下载并覆盖到通达信安装目录（以 `C:/new_tdx64` 为例）：

1.  **日线行情数据**
    -   **下载链接**: `https://data.tdx.com.cn/vipdoc/hsjday.zip`
    -   **更新频率**: 每天盘后约 1 小时后更新。
    -   **操作**: 下载后解压，覆盖到 `C:/new_tdx64/vipdoc` 目录。

2.  **财务数据**
    -   **下载链接**: `https://data.tdx.com.cn/vipdoc/tdxfin.zip`
    -   **更新频率**: 更新频率不高，无需每天下载。
    -   **操作**: 下载后解压，覆盖到 `C:/new_tdx64/vipdoc/cw` 目录。

## API 文档与详细指南

本技能包含了一系列详细的子文档，涵盖了 TdxQuant 开发的各个方面。**请在回答用户具体问题时，优先读取以下相关文档：**

### 基础入门
- [TdxQuant 简介](references/00TdxQuant%20简介.md): 平台介绍、运行环境要求及核心运行逻辑。
- [常见问题](references/11常见问题.md): 常见报错（如 DLL 错误、路径问题）及解决方法。
- [常量枚举](references/08常量枚举.md): 市场类型、复权类型、K线周期等参数的常量定义。

### 核心功能 API
- [通用函数](references/01通用函数.md): 初始化、数据订阅、发送消息/预警、文件下载等。
- [行情类信息](references/02行情类信息.md): 获取实时行情、历史 K 线、分笔数据等。
- [财务类数据](references/03财务类数据.md): 获取财务数据、除权除息信息等。
- [债券和期货数据](references/06债券和期货数据.md): 可转债及期货相关数据获取。

### 板块与选股
- [分类和板块成份股](references/04分类和板块成份股.md): 获取系统分类、行业板块及其成份股。
- [自选股和自定义板块](references/05自选股和自定义板块.md): 管理用户自定义板块及自选股。

### 高级功能
- [调用通达信公式](references/07调用通达信公式.md): 在 Python 中调用通达信指标公式进行计算。
- [回测及模拟交易](references/09回测及模拟交易.md): 策略回测流程及模拟交易说明。

### 示例
- [场景化示例](references/10场景化示例.md): 常见策略场景的代码实现示例。

## 常见问题排查

- **ModuleNotFoundError**: 确保 `PYPlugins/user` 的路径正确并已添加到 `sys.path`。
- **DLL 错误**: 如果看到 `FileNotFoundError: Could not find module ... TPythClient.dll`，请检查父目录 (`../PYPlugins/`) 下是否存在 `tdxrpcx64.dll`，并确保未被杀毒软件拦截。详细排查请参考 [常见问题](references/11常见问题.md)。
- **数据为空**: 确保 `count` 足以进行公式计算 (例如，计算 5 日移动平均线至少需要 5 个数据点)。
- **进程冲突**: 如果外部脚本报告已在运行，请在通达信的 TQ 策略管理器中检查并停止现有的实例。

## 参考资料

- 官方文档: [通达信量化平台帮助文档](https://help.tdx.com.cn/quant/)
- **Tip**: 本技能内置文档更新于 2026年3月1日。由于 TdxQuant 平台可能会持续迭代，如需获取最新的 API 变更和功能说明，请务必访问上述官方文档链接。
