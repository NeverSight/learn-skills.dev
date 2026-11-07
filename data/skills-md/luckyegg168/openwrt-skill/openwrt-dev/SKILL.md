---
name: openwrt-dev
description: >
  OpenWrt 路由器韌體與套件開發的完整指南。涵蓋建構系統、套件開發、
  LuCI 介面、核心模組、網路設定、交叉編譯、除錯與安全。使用此 skill
  當使用者提到 OpenWrt、路由器開發、嵌入式 Linux 網路設備、LuCI、
  UCI、ipk 套件、router firmware、或任何與 OpenWrt 生態系相關的開發任務。
  即使使用者只是問「怎麼在路由器上跑自己的程式」也應觸發。
globs:
  - "**/openwrt/**"
  - "**/luci/**"
  - "**/package/Makefile"
---

# OpenWrt 開發技能包

> 適用版本：OpenWrt 23.05+（核心 5.15+）
> 建構系統：Buildroot / SDK / ImageBuilder
> 網路子系統：UCI + netifd + firewall4 (nftables)

---

## 快速導覽 — 你想做什麼？

| 我想要... | 閱讀 |
|-----------|------|
| 編譯整個 OpenWrt 韌體 | [build-system.md](references/build-system.md) |
| 把自己的程式打包成 `.ipk` | [package-dev.md](references/package-dev.md) |
| 寫一個核心模組 (`.ko`) | [kernel-module.md](references/kernel-module.md) |
| 做一個 LuCI Web 管理頁面 | [luci-app.md](references/luci-app.md) |
| 設定路由器網路 / 防火牆 / Wi-Fi | [networking.md](references/networking.md) |
| 理解交叉編譯工具鏈 | [cross-compilation.md](references/cross-compilation.md) |
| 除錯程式或效能調校 | [debugging.md](references/debugging.md) |
| 安全加固與 CVE 修補 | [security.md](references/security.md) |
| 日常操作指令速查 | [common-recipes.md](references/common-recipes.md) |

---

## OpenWrt 開發環境概述

OpenWrt 是基於 Linux 的嵌入式作業系統，專為網路設備（路由器、AP、閘道器）設計。其建構系統（Buildroot）可交叉編譯整個作業系統及使用者空間套件，產生 sysupgrade 映像或單獨的 `.ipk` 套件。開發流程以 feeds（套件來源倉庫）和 Makefile 為核心，使用 UCI（Unified Configuration Interface）統一管理設定，netifd 管理網路介面，firewall4（nftables 後端）管理防火牆。LuCI 是其 Web 管理介面框架，現代開發使用 JavaScript client-side API。

---

## 決策樹

```
使用者的問題是什麼？
│
├─ 建構/編譯相關
│  ├─ 要編譯完整韌體映像 → build-system.md
│  ├─ 要編譯單一套件 (SDK) → build-system.md § SDK 模式
│  ├─ 只想打包自訂映像 → build-system.md § ImageBuilder
│  └─ 編譯失敗/錯誤 → debugging.md + prompts/debug-build-error.md
│
├─ 套件開發
│  ├─ 建立新套件 → package-dev.md + templates/package-makefile.template
│  ├─ 套件 Makefile 語法 → package-dev.md § 核心變數
│  ├─ 多套件/子套件 → package-dev.md § 多套件分割
│  └─ Go/Python/Rust 套件 → package-dev.md § 語言特定
│
├─ LuCI Web 介面
│  ├─ 建立新 LuCI 應用 → luci-app.md + templates/luci-app-skeleton/
│  ├─ JavaScript API 用法 → luci-app.md § form.Map 完整範例
│  ├─ 選單和權限設定 → luci-app.md § 選單與 ACL
│  └─ 狀態/監控頁面 → luci-app.md § 自訂視圖
│
├─ 核心模組
│  ├─ 寫核心模組 → kernel-module.md + templates/kernel-module-skeleton/
│  ├─ Netfilter hook → kernel-module.md § Netfilter
│  └─ 驅動程式 → kernel-module.md § 裝置驅動
│
├─ 網路設定
│  ├─ WAN/LAN/VLAN → networking.md § 基礎網路
│  ├─ 防火牆(nftables) → networking.md § firewall4
│  ├─ Wi-Fi 設定 → networking.md § 無線網路
│  └─ 互動式設定 → prompts/network-config.md
│
├─ 交叉編譯
│  ├─ 工具鏈結構 → cross-compilation.md
│  ├─ staging_dir 用途 → cross-compilation.md § 目錄結構
│  └─ CMake/autotools 移植 → cross-compilation.md § 建構系統整合
│
├─ 除錯
│  ├─ 線上除錯 → debugging.md § 遠端 GDB
│  ├─ 日誌分析 → debugging.md § logread/procd
│  ├─ 網路封包 → debugging.md § tcpdump
│  └─ 效能分析 → debugging.md § perf
│
└─ 安全
   ├─ 安全加固 → security.md § 編譯時防護
   ├─ CVE 修補 → security.md § CVE 修補流程
   └─ SSH/防火牆硬化 → security.md § 運行時防護
```

---

## 參考文件摘要

| 文件 | 說明 |
|------|------|
| **build-system.md** | Buildroot 全量建構、SDK 套件編譯、ImageBuilder 映像客製、feeds 管理、menuconfig 操作 |
| **package-dev.md** | Makefile 結構與 PKG_* 變數、Build/Configure/Compile/Install 階段、init 腳本與 UCI 設定、多套件分割 |
| **kernel-module.md** | KernelPackage 定義、Kbuild 整合、Netfilter hook、裝置樹 overlay、AutoLoad 設定 |
| **luci-app.md** | JavaScript client-side API（form.Map/Section/Option）、menu.d JSON、ACL 權限、rpcd 後端整合 |
| **networking.md** | UCI 網路設定、netifd 運作原理、firewall4 nftables 規則、DSA VLAN、無線設定、ubus 查詢 |
| **cross-compilation.md** | toolchain 結構、staging_dir 四層目錄、TARGET_* 環境變數、autotools/CMake/Meson 整合、musl 注意事項 |
| **debugging.md** | logread/procd 日誌、遠端 GDB、strace/ltrace、tcpdump 封包分析、perf 效能剖析、kernel oops 解讀 |
| **security.md** | ASLR/PIE/SSP/FORTIFY_SOURCE/RELRO 編譯防護、SECCOMP、SSH 加固、CVE 修補流程、最小權限原則 |
| **common-recipes.md** | 系統管理速查、套件管理 opkg 指令、UCI 操作、Wi-Fi 快速設定、建構指令集、部署腳本範例、ubus 呼叫 |

---

## 模板目錄 (templates/)

| 路徑 | 說明 | 使用方式 |
|------|------|----------|
| `templates/package-makefile.template` | 標準套件 Makefile 模板 | 複製後替換 `{{VARIABLE}}` 變數 |
| `templates/luci-app-skeleton/` | LuCI 應用骨架（JS view + 選單 + ACL + Makefile） | 複製整個目錄，重命名並替換變數 |
| `templates/kernel-module-skeleton/` | 核心模組骨架（Makefile + Kbuild + C 原始碼） | 複製整個目錄，填入模組名稱和邏輯 |

**模板變數慣例：** 使用 `{{VARIABLE_NAME}}` 格式標記需要使用者替換的位置。

### 使用步驟
1. 從 `templates/` 複製對應骨架
2. 全域搜尋 `{{` 找到所有需替換的變數
3. 用實際值替換每個 `{{VARIABLE}}`
4. 根據需求增刪功能
5. 編譯測試：`make package/你的套件/compile V=s`

---

## 提示詞目錄 (prompts/)

| 路徑 | 用途 | 觸發情境 |
|------|------|----------|
| `prompts/generate-package.md` | 產生 OpenWrt 套件 | 「幫我把這個程式打包成 ipk」 |
| `prompts/generate-luci-app.md` | 產生 LuCI Web 介面 | 「幫我做管理頁面 / Web UI」 |
| `prompts/debug-build-error.md` | 診斷編譯錯誤 | 「為什麼 make 失敗了」 |
| `prompts/network-config.md` | 產生網路設定 | 「幫我設定 VLAN / 防火牆 / Wi-Fi」 |

每份提示詞都包含：使用時機、提示詞模板（可直接使用）、期望輸出、範例對話。

---

## 版本相容性說明

| 功能 | 最低版本 | 說明 |
|------|----------|------|
| firewall4 (nftables) | 22.03+ | 取代 firewall3 (iptables) |
| DSA switch driver | 21.02+ | 取代 swconfig |
| LuCI JavaScript API | 21.02+ | 取代 Lua CBI |
| procd init system | 15.05+ | 標準 init 系統 |
| musl libc (預設) | 15.05+ | 取代 uClibc |

> **此技能包所有內容均以 OpenWrt 23.05+ 為準。** 若使用者環境為更舊版本，需注意防火牆（iptables vs nftables）、交換器（swconfig vs DSA）、LuCI（Lua vs JS）的差異。

---

## 常用指令速查

```bash
# 完整建構流程
git clone https://git.openwrt.org/openwrt/openwrt.git
cd openwrt
./scripts/feeds update -a && ./scripts/feeds install -a
make menuconfig    # 選擇 target 和套件
make -j$(nproc)    # 並行編譯

# 單一套件編譯 (SDK)
make package/myapp/compile V=s

# 安裝套件到設備
scp bin/packages/*/base/myapp_1.0-1_*.ipk root@192.168.1.1:/tmp/
ssh root@192.168.1.1 'opkg install /tmp/myapp_1.0-1_*.ipk'

# UCI 操作
uci show network.lan
uci set network.lan.ipaddr='192.168.10.1'
uci commit network && /etc/init.d/network restart
```

---

## 外部資源

- [OpenWrt 官方文件](https://openwrt.org/docs/)
- [OpenWrt Git 倉庫](https://git.openwrt.org/)
- [LuCI JavaScript API 文件](https://openwrt.github.io/luci/jsapi/)
- [OpenWrt packages feed](https://github.com/openwrt/packages)
- [OpenWrt 硬體支援清單](https://openwrt.org/toh/start)
