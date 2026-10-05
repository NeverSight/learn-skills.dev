---
name: linux-install-debug
description: >
  安裝一台新 Linux（VM 或實機）或診斷 Linux / macOS 系統問題時的標準化診斷協議。核心紀律是
  讀權威狀態、不靠肉眼猜表象：先定平台座標（發行版 / 架構 / 套件管理器），再依症狀查對應的
  權威來源。涵蓋 SSH 連不上、終端機亂碼、服務 failed 或 restart loop、進程活著但子系統死、
  權限被拒、套件管理器失敗、磁碟滿與檔案系統唯讀、音訊無聲、VT 黑畫面、被 OOM 殺掉，以及把
  失敗變成推播告警。Triggers: 裝 Linux, 新 VM, 首次開機驗證, ssh 連不上, connection refused,
  connection timeout, 終端機亂碼, systemctl status, journalctl, 服務 failed, restart loop,
  進程活著但沒反應, pgrep 騙人, permission denied, EACCES, operation not permitted,
  command not found, unable to locate package, dpkg lock, pacman db lock, partial upgrade,
  unbound variable, shell script 可攜, bash 3.2, timeout 找不到, 容器沒有 sudo,
  keyring 過期, PATH 沒吃到, 磁碟滿, 檔案系統唯讀, OOM, exit 137, dmesg, 黑畫面, getty,
  chvt, 沒聲音, wpctl, DNS 解析不了, 機器沒回應, 服務告警, OnFailure, ntfy, 心跳監控,
  linux install, linux debug, systemd, authoritative state.
license: MIT
metadata:
  version: 1.17.2
  category: ops-diagnostics
---

# Linux Install & Debug

安裝一台新 Linux、或診斷 Linux 系統問題時的標準化診斷協議。核心是一條紀律：**讀權威狀態，不靠肉眼猜表象**。給 AI 快速判斷「出了什麼錯、該做哪些測試」，避免看畫面 / 看症狀就下結論而猜錯。

## 何時啟動

- 安裝新的 Linux 系統（VM 或實機）、需要標準化的安裝 + 首次開機驗證流程
- 遠端（SSH）或本地除錯 Linux：連不上、終端機異常、程式行為不對、服務怪怪的、狀態判不準
- 任何「這現象看起來像 A，但要確認是不是 B」的判斷 — 先讀權威狀態再下結論

## 最高紀律：讀權威狀態，不靠肉眼猜

**表象會騙人。** 畫面上的現象、終端機捲過的輸出、一個視窗長什麼樣，都是表象；能定案的是系統裡記錄這件事的權威來源 — 程式自己的 log、服務註冊表、核心 / systemd 的狀態、資源用量。

實測反例（真實踩過）：一個桌面 shell 的除錯裡，畫面出現密碼框 → 判「鎖了」；接著 `loginctl` 沒 `LockedHint`、`pgrep` 找不到鎖屏程式 → 「更正」成「不是鎖」；兩個判斷都錯。讀那個 shell 自己的 log 才定案：它是走合成器層協議的真鎖，`loginctl`（logind 層）本來就查不到、鎖屏由主程式行程內畫所以沒獨立 process。**肉眼加讀錯層，猜錯兩次；讀對權威來源，一次定案。**

詳見 [讀權威狀態不靠肉眼](references/principles/read-authoritative-state-not-eyeball.md) 與 [讀程式自己的 log](references/principles/read-the-programs-own-log.md)。

## 第零步：先定平台（診斷與修法都是平台相依的）

判讀工具、套件名、修法都因平台 / 發行版 / 架構而異——把 A 平台的經驗直接套到 B 平台，是「工具行為不對」類誤判的常見根因。開始查之前先用三條指令建立座標：

```bash
cat /etc/os-release        # 發行版與版本（Linux）；macOS 用 sw_vers
uname -m                   # CPU 架構：x86_64 / aarch64 — ARM 的套件生態明顯較小
command -v pacman apt-get dnf brew   # 哪個套件管理器在場
```

平台定了之後，這些差異才有判讀基準：

- **套件名與執行檔名分歧**：`fd`（Arch）= `fd-find`（Debian，執行檔 `fdfind`）；`bat` 在 Debian 執行檔叫 `batcat`；`github-cli`（Arch）= `gh`（Debian/Fedora）。「command not found」先確認是沒裝、還是這個發行版叫別的名字。
- **非互動旗標不對稱**：apt 用 `-y`、pacman 用 `--noconfirm`。非 TTY（SSH 一行式、CI、無人值守）下缺對應旗標會卡在 `[Y/n]` 直接失敗。
- **rolling vs stable 的資料庫時序**：Arch 鏡像不保留舊版檔案，stale db 會 404（`failed retrieving file`），修法是先 `pacman -Syu`（只 `-Sy` 不 `-u` 造成 partial upgrade）；Debian stable 無此時序問題、但版本舊，config 語法可能對不上新版文件。
- **工具在不在**：`arp` 常沒裝（用 `ip neigh`）、最小系統連 `sudo` 都沒有；ARM 上 AUR 部分套件不支援、Homebrew on Linux 無 aarch64 bottle。
- **apt 的失敗集中在解析階段**：`Unable to locate package` 有三種可能（這發行版名字不同 / 根本沒打包，退回 GitHub releases / 真打錯）、批次一個爛名字讓整筆交易 abort（症狀是「列十個、一個都沒裝」）、裝 node/python 會拉進整個語言生態的系統套件（實測 `apt install npm` 帶 300+ 個 node-*，語言執行環境該走 version manager）。含 dpkg lock 復原、EOL 的 archive 404，見 [install-and-verify](references/install-and-verify.md) 的 apt/dpkg 段。

## 四步診斷流程（每次都跑）

1. **描述症狀**：現象是什麼，別在這步下結論（「畫面出現密碼框」，不是「鎖了」）。
2. **定位權威來源**：這件事的權威狀態記在哪（用下表對照）。
3. **用對工具讀它**：讀權威來源，不是讀畫面 / 終端機殘影。
4. **權威跟表象矛盾時信權威**：矛盾點通常就是原本會猜錯的地方。

## 權威來源速查表

| 症狀類別                              | 權威來源                        | 工具                                                                                               |
| ------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------- |
| 某程式行為不對                        | 程式自己的 log 檔               | log 路徑、`journalctl -u <unit>`                                                                   |
| 服務由誰提供                          | D-Bus name / socket 註冊        | `busctl`、`ss -lntp`、`lsof`                                                                       |
| 登入 / 鎖定狀態                       | logind                          | `loginctl show-session <id>`                                                                       |
| 服務跑了沒 / failed                   | systemd unit                    | `systemctl status` / `is-active` / `is-failed`、`list-units --failed`、`journalctl -u`             |
| 程式活著沒                            | 行程表（比對正確 comm）         | `pgrep -x`、`pgrep -af`、`ps`                                                                      |
| 進程活著但沒運作（畫得出來卻點不動）  | 程式自己的 log + IPC 回真實狀態 | 專屬 log 指令 `<shell> -l`（非 journalctl）、`<shell> ipc call ...`（回空=子系統死）；別信 `pgrep` |
| 網路通不通                            | 介面 / 路由 / 鄰居表            | `ip -brief a`、`ip neigh`、`ss`（`arp` 常沒裝）                                                    |
| 域名解析                              | resolver 設定                   | `getent hosts <域名>`、`/etc/resolv.conf`、`resolvectl`                                            |
| 磁碟 / 記憶體                         | 檔案系統 / 記憶體用量           | `df -h`、`du -sh`、`free`、`mount \| grep -w ro`                                                   |
| 核心 / 硬體 / 被殺行程(OOM、exit 137) | kernel ring buffer              | `dmesg`、`journalctl -k -b`                                                                        |
| 權限被拒(EACCES)                      | 檔案 mode/owner、路徑逐層、MAC  | `namei -l <path>`、`stat`、`id`、`sudo -l`、`getcap`、`ausearch`(SELinux)                          |
| 程式 log 沉默、不知哪個 syscall 失敗  | syscall 層                      | `strace -f -e trace=file <cmd>`                                                                    |
| VT / 主控台（黑畫面 / 沒登入提示）    | getty 狀態（**chvt 前先查**）   | `systemctl is-active/is-enabled getty@tty<N>` → 再 `chvt`；`cat /sys/class/tty/tty0/active`        |
| 應用無聲（多半不報錯）                | 音訊伺服器 graph                | `wpctl status`：Sinks 空 = 棧缺件（wireplumber 沒裝）；stream `[active]` = 真在播                  |

## 症狀 → 情境路由

- **安裝新系統 / 首次開機驗證** → [install-and-verify](references/install-and-verify.md)（含裝好後主動確認有無服務監控、沒有就建議建立）
- **SSH 連不上（先做 timeout vs refused 分流）、終端機噴亂碼 / 亂碼輸入、要從 SSH 操控圖形桌面** → [remote-access](references/remote-access.md)
- **（從 remote-access 分流後）機器沒回應、域名解析不了、虛擬機開不起來、疑似磁碟滿 / 檔案系統唯讀連鎖** → [machine-unreachable](references/machine-unreachable.md)
- **判程式活著沒 / 服務歸誰 / 服務 failed 或一直重啟(restart loop) / 鎖沒鎖 / session 存活 / 卡住是資源還是相容** → [process-service-state](references/process-service-state.md)
- **進程活著卻不運作（GUI shell / bar 畫得出來但點不動、keybind 叫不出東西、焦點視窗打字正常）** → [process-service-state](references/process-service-state.md) 的「進程活著 ≠ 子系統活著」段（讀 shell 自己的 log + IPC，別信 pgrep）
- **不想肉眼盯服務死活 / 要自動告警 / 怕整台機器當掉沒人知道 / 裝新系統或反覆除服務失敗（主動確認有無監控、無則建議建立）** → [process-service-state](references/process-service-state.md) 的「把失敗變成推播（OnFailure）」段（先確認有無監控 → 沒有優先建議 OnFailure + ntfy 公共站零 daemon → 要更高安全再自架 ntfy + 完整堆疊；含 hung 偵測、canary、topic 安全）
- **權限被拒（Permission denied / EACCES / Operation not permitted / sudo 後冒 root-owned 檔）** → [process-service-state](references/process-service-state.md) 的權限段
- **套件管理器失敗（pacman：db lock / keyring 簽章過期 / partial upgrade / mirror。apt：unable-to-locate / 批次 abort / dpkg lock / EOL archive 404 / node 爆量）** → [install-and-verify](references/install-and-verify.md) 的套件管理器段
- **自己寫的 shell script 壞了（unbound variable 而變數名尾端有怪字元、`timeout` 之類的 GNU 工具在 macOS 找不到、root 容器裡沒有 `sudo`、非互動環境卡在 `[Y/n]`）** → [install-and-verify](references/install-and-verify.md) 的可攜陷阱段。這些歸檔在安裝流程底下，是因為它們都是從寫 bootstrap 腳本時踩出來的，而症狀出現時多半不在裝機情境
- **要讀某程式的 log 定位根因** → [read-logs](references/read-logs.md)
- **要挑 / 推薦工具（同一件事有多個選擇：grep vs ripgrep、哪個檔案管理員、遠端用什麼）** → [tool-options](references/tool-options.md)

## 反模式

- **看畫面就下結論**：畫面有密碼框 ≠ 鎖了；通知沒跳 ≠ 服務沒接管；build 停住 ≠ 不相容。一律回權威來源確認。
- **讀錯層**：Wayland 合成器層的鎖用 logind 的 `LockedHint` 查（查錯層）；用猜的 process 名 `pgrep`（查詢條件錯）。權威來源對、但問錯地方，一樣誤導。
- **急著下昂貴結論**：跳到「不相容 / 要重裝」前，先用最廉價的檢查（`df -h`、資源、資源在不在）排除。
- **一直重試同一個失敗動作**：連不上就一直重連，不去讀網路 / 服務 / 資源的權威狀態。
- **信終端機 scrollback 殘影**：拿捲過的舊輸出當現況。權威狀態是「現在再查一次」的結果，不是畫面上留著的上一次。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
