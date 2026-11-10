---
name: harmony-issue-resolution
description: 处理水杉输入法所有 HarmonyOS issue：从 issue 盘点、ArkTS/NAPI/共享 Rust 定位，到 HAP 构建、签名设备验收和独立 PR；适用于鸿蒙专属问题及明确包含鸿蒙范围的跨平台 issue。
---

# 鸿蒙 issue 处理

这个技能只处理 `platforms/harmony` 原生宿主及明确包含 HarmonyOS 范围的 issue。先读取仓库 `AGENTS.md`、`docs/ARCHITECTURE.md` 和 `.github/CONTRIBUTING.md`；产品本体是 `platforms/harmony`，设置页通过 ArkWeb 加载 `stage-settings.sh` 打包的 rawfile，不能把 Tauri/React 工程当成鸿蒙产品启动或验收。

## 先盘点范围

用 GitHub 当前状态建立清单，不凭标题猜完成度：

```sh
gh issue list --state open --limit 200 --json number,title,labels,url \
  | jq -r '.[] | select((.title + " " + ([.labels[].name]|join(" "))) | test("harmony|鸿蒙|ohos"; "i"))'
```

同时搜索 issue 正文和评论里的 `HarmonyOS`、`鸿蒙`、`platform/harmony`，因为跨平台 issue 可能没有平台标签。读取关联 PR 的状态、验证段和设备证据；合入 develop 不等于鸿蒙 issue 完成。

按 issue 单独建立 `fix/<issue>-harmony-*` 或 `feat/<issue>-harmony-*` 分支和 PR。一个 PR 只处理一个 issue；跨平台需求按平台拆 PR，用 `Refs #N`，最后一个平台完成并有证据后才关闭总 issue。PR 标题、正文、评论和 review 使用中文，Conventional Commits 类型前缀保留英文。

## 路由到正确层

- **键盘、候选、手势、确认键、删除键、预编辑**：先看 `platforms/harmony/entry/src/main/ets/keyboard/` 及其 `input/`、`candidate/`、布局和测试；引擎或策略可复用时下沉到共享 Rust，ArkTS 只做宿主适配。
- **设置页、账户、资源管理、下载状态**：看 `platforms/harmony/entry/src/main/ets/pages/`、`apps/harmony`、`stage-settings.sh` 和 ArkWeb 原生桥；业务规则优先放共享 `client-core`、`client-services` 或 `client-providers`，不要在 React 设置页新增入口。
- **按需资源、HAP 内容、目录和签名**：检查资源清单、打包脚本、哈希校验、安装目录和权限；验证默认 HAP 不携带可按需资源，设置应用与键盘共享同一份已校验资源，不重复复制。
- **发布、AppGallery、公开测试**：读取对应 workflow、版本文件和发布 skill；构建、上传材料、签名可接受、应用市场审核和公开测试提交是不同结果，不能用其中一个代替另一个。
- **CI/测试回归**：行为断言写进 `platforms/harmony/tests/*.test.ts`、设备 smoke 或真实宿主测试，不向 `platforms/harmony/tests/run.sh` 和 `check-host.sh` 继续堆源码 grep。测试输入使用合成值。

## 实现边界

先检索 `.agents/notes/` 中同一设置、键盘行为、资源代次和签名问题的旧笔记；非机械性改动写入 `.agents/notes/implemented/{feature,bug-fix,testing,process}/`，正文用简体中文。不要顺手改变已有默认值；缺字段的兼容读法、默认值或设置契约改变时，必须在 issue/评论中有授权并在 PR 链接它。

界面改动遵守「说明收进标题旁 ?」规则。资源和目录变更必须同时验证 HAP、权限、设备行为和升级/卸载路径。不要把测试签名设备拒绝、模拟器通过或静态包检查写成真机完成。

## 鸿蒙验收

先检查开发机是否有可接受签名和可用设备；没有就保留 PR draft，并把确切阻塞写进验证段。至少运行与改动匹配的本地门禁：

```sh
pnpm run verify-notes
git diff --check
ANDROID_SDK_ROOT=<SDK> bash platforms/harmony/check-host.sh
bash platforms/harmony/tests/run.sh
rbuild bash scripts/verify-local.sh --quick
```

涉及设置 bundle、ArkTS 界面或 HAP 资源时，补跑仓库规定的 Harmony settings bundle/HAP 构建入口；涉及真实输入法行为或资源下载、卸载、切换时，必须在设备接受的签名 HAP 上安装，冷启动设置应用和键盘，记录：安装、首次启用、输入法切换、下载/校验、卸载、再次聚焦后的资源路径与行为。若设备因签名拒绝，记录完整错误码并把设备验收标为未完成。

提交 PR 前确认 `origin/develop` 最近 CI 没有未解释的红灯，跑完 quick 门禁后再推送。PR 必须列出每个 issue 要求对应的命令、设备、版本、结果和未完成项，并附界面改动前后截图；未真实验收的 issue 不关闭。

## 当前开放鸿蒙范围

这份清单用于启动工作，执行前仍需用 GitHub 刷新：详见 [references/open-issues.md](references/open-issues.md)。
