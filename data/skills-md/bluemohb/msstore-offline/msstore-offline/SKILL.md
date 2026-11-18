---
name: msstore-offline
description: 从微软官方分发接口（FE3 / Windows Update）离线获取并安装 Microsoft Store 应用包（appx / appxbundle / msix），不需要打开 Microsoft Store。适用于商店打不开或报错、winget 安装卡在「启动程序包安装」、以及需要补装 AV1 / HEVC / VP9 等系统媒体扩展的场景。Downloads Microsoft Store packages straight from Microsoft's official delivery API (FE3) and installs them via Add-AppxPackage, bypassing the Store app entirely. Use when the Microsoft Store is broken or unavailable, when winget hangs on install, or when a codec / media extension must be sideloaded.
agent_created: true
---

# Microsoft Store 离线取包与安装

## 用途

在 Microsoft Store 不可用的 Windows 上，直接向微软官方分发服务取回 appx/msix 安装包并本地安装。
取回的包来自 `tlu.dl.delivery.mp.microsoft.com`（微软官方 CDN）、带微软签名，不是第三方重打包。

## 何时使用

- 用户打不开商店，或商店报错（`0x80131500`、`0x80072EFD` 等）
- `winget install` 能查到包但卡在「正在启动程序包安装」
- 需要补装系统媒体扩展：AV1 / HEVC / VP9 / Web 媒体扩展
- 需要把某个商店应用做成离线安装包分发给他人

## 何时不要用

**先确认用户真的需要这个扩展。** 很多播放器自带解码器，装扩展解决不了问题：

- **mpv / VLC / ffmpeg**：自带 dav1d 等软件解码器，AV1/HEVC 是原生支持的，**不需要**任何 Store 扩展。若这些播放器报解码失败，先查版本与 `--hwdec` 参数，不要装扩展。
- 真正会弹「需要 AV1/HEVC 视频扩展」的是 **Media Foundation 系**应用：Windows 媒体播放器、电影和电视、照片、部分浏览器与剪辑软件。

## 不要走的路（都已验证失败）

| 做法 | 结果 |
|---|---|
| `winget install --id <StoreID> --source msstore` | 卡在「启动程序包安装」，因为商店安装管道本身就是坏的 |
| `winget download --source msstore` | 要求 Microsoft Entra ID 登录，普通用户拿不到 |
| `winget install --manifest` | 需管理员先执行 `winget settings --enable LocalManifestFiles` |
| `store.rg-adguard.net` 等镜像 | 国内常被墙（curl error 35 / TLS 握手失败） |
| Microsoft 更新目录（catalog.update.microsoft.com） | 没有这类扩展 |
| 把直链的 `http` 改成 `https` | 该 CDN 用 https 会失败，**必须保持 http** |

## 工作流

### 1. 查询并下载

脚本只依赖 Python 标准库，无需安装任何包：

```bash
python scripts/msstore_fetch.py <ProductID>
python scripts/msstore_fetch.py <ProductID> --download --out ./dl
python scripts/msstore_fetch.py <ProductID> --download --filter x64 --json
```

`ProductID` 是商店链接末尾那段（`apps.microsoft.com/detail/9mvzqvxjbq9v` → `9MVZQVXJBQ9V`），
也接受完整链接。常见 ID 见 `references/known-packages.md`。

先不带 `--download` 跑一次，确认包名、大小、架构符合预期，再决定下不下。

### 2. 必须校验，不要只看「下载成功」

脚本在 `--download` 时会自动比对文件大小和摘要（FE3 的 `Digest` 是 **base64 编码的 SHA-1**，
20 字节；若为 32 字节则是 SHA-256，脚本按长度自适应）。

**不要跳过这一步。** 该 CDN 在重复请求或限流时会返回一个 **150 字节的 `403 Forbidden`
HTML 页**，且 HTTP 状态可能仍是 200、文件名也正常，看起来像下载成功。已实测踩过。

手工核对时：

```bash
ls -l dl/            # 大小应与脚本报告的 Size 完全一致
sha256sum dl/*.appxbundle
```

### 3. 检查包本身

```bash
python -c "import zipfile;z=zipfile.ZipFile('dl/xxx.appxbundle');print(z.namelist());print(z.read('AppxMetadata/AppxBundleManifest.xml').decode('utf-8','replace'))"
```

关注三点：

- 有 `AppxSignature.p7x`、清单里 `Publisher="CN=Microsoft Corporation..."` → 官方签名
- `<PackageDependency>` 是否为空；不为空则要一并下载依赖包（VCLibs 等）并用 `-DependencyPath` 传入
- `<TargetDeviceFamily MinVersion>` 是否高于本机系统版本

### 4. 安装

安装走 `Add-AppxPackage`，不经过商店：

```bat
powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-AppxPackage -Path 'C:\path\to\xxx.appxbundle'"
```

**注意执行环境**：Agent 沙箱里可能禁止从 shell 调用 `powershell.exe`，此时无法代跑安装。
正确做法是生成一个 **GBK 编码**的 `.cmd`（中文注释用 GBK，否则 cmd 里是乱码），内容调用上面的命令，
交给用户双击；或直接让用户双击 `.appxbundle`，由「应用安装程序」接管。

`.cmd` 里要带失败分支，提示用户：右键以管理员身份运行 / 直接双击 appxbundle / 检查系统版本。

### 5. 收尾

提醒用户完全退出并重开播放器或浏览器，必要时重启。装完仍不生效，多半是该应用走自己的解码器，
回到「何时不要用」那一节排查。

## 常见失败

| 现象 | 原因与处理 |
|---|---|
| `未取到 WuCategoryId` | 该产品不是 appx/msix 打包（可能是 Win32 安装器），本技能不适用 |
| `没有匹配的包` | `--filter` 太窄，或该通道没有包；换 `--ring Retail` / `--ring RP` |
| `SOAP 请求失败 HTTP 500` | 缺 `o:Security` 头或 `WindowsUpdateTicketsToken`；检查模板是否被改坏 |
| 500 且报文含 `InvalidSecurity` | 内置匿名设备票据被限流或失效，用 `--device-token` 或环境变量 `MSSTORE_DEVICE_TOKEN` 换一个 |
| 下载得到 150 字节 | CDN 返回 403 错误页，重新取直链再下一次，并确认校验通过 |
| `Add-AppxPackage` 报 `0x80073CF3` | 依赖包缺失或版本冲突，补依赖后重试 |
| 安装报 `0x80073D02` | 目标包正被占用，关掉相关应用再装 |

## 参考

- `references/pitfalls.md` — 协议细节、TLS/代理、校验规则等踩坑记录
- `references/known-packages.md` — 常见扩展的 ProductID 与包名
