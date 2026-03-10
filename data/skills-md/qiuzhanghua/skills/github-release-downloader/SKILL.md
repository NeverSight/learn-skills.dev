---
name: github-release-downloader
description: Skill for downloading GitHub Release assets / 从GitHub仓库下载最新Release资产的Claude Skill
metadata:
  author: 邱张华(qiuzhanghua@msn.com)
license: MIT
---

# GitHub Release Downloader / GitHub Release 下载器

## Overview / 概述

This is a Claude Skill for downloading the latest Release assets from GitHub repositories. Using the PyGithub library, this skill can fetch the latest release version of a repository, list all available asset files, and download specified assets to a local directory based on user needs.

这是一个用于从GitHub仓库下载最新Release资产的Claude Skill。通过使用PyGithub库，该技能可以获取仓库的最新发布版本，列出所有可用的资产文件，并根据用户需求下载指定的资源到本地目录。

## Features / 功能特点

- Automatically fetch the latest Release info from GitHub repositories / 自动获取GitHub仓库的最新Release信息
- Support downloading historical releases by specifying Release tags / 支持指定Release标签（Tag）下载历史版本
- Automatically filter and only download executables and archives (.exe, .zip, .tar.gz, .tar.zst, .dmg, .tar.bz2, .tar.xz) / 自动过滤只下载可执行文件和压缩包
- List all Release assets with name, size, and download URL / 列出所有Release资产的名称、大小和下载URL
- Support filtering and downloading specific assets by name / 支持按名称筛选并下载特定资产
- Support downloading all assets to a specified directory / 支持下载所有资产到指定目录
- Provide detailed download progress and status information / 提供详细的下载进度和状态信息
- Support custom download paths / 支持自定义下载路径

## Usage / 使用方法

### Basic Syntax / 基本语法

```
Please help me download Release from [owner]/[repo]

Examples:
Please help me download Release from octocat/Hello-World
Please help me download the latest Release from microsoft/vscode to ./origin/vscode
Please help me download "react.zip" from facebook/react
```

```
请帮我从 [owner]/[repo] 下载Release资源

例如：
请帮我从 octocat/Hello-World 下载Release
请帮我从 microsoft/vscode 下载最新的Release到 ./origin/vscode 目录
请帮我从 facebook/react 下载名为 "react.zip" 的资源
```

### Parameter Description / 参数说明

- **owner**: GitHub repository owner username or organization name / GitHub仓库所有者用户名或组织名称
- **repo**: GitHub repository name / GitHub仓库名称
- **download_path** (optional): Download save directory path, defaults to "origin/{repo}" folder under current directory / 下载保存的目录路径，默认为当前目录下的"origin/{repo}"文件夹
- **asset_name** (optional): Specific asset name to download, downloads all assets if not specified / 要下载的特定资产名称，如果不指定则下载所有资产
- **tag** (optional): Specify Release tag (e.g., v1.0.0), downloads latest Release if not specified / 指定Release标签（如 v1.0.0），如果不指定则下载最新Release

### Download All Assets / 下载所有资源

When not specifying a specific asset name, all asset files of that Release will be downloaded:

当不指定具体资产名称时，将下载该Release的所有资产文件：

```
Please help me download all Release assets from owner/repo
请帮我从 owner/repo 下载所有Release资源
```

### Download Specific Assets / 下载指定资源

You can filter and download specific asset files by name:

可以通过名称筛选下载特定的资源文件：

```
Please help me download "example-linux-x64.tar.gz" from owner/repo
请帮我从 owner/repo 下载名为 "example-linux-x64.tar.gz" 的资源
```

### Download Specific Tag Release / 下载指定Tag的Release

You can download a specific version's Release assets by specifying a Tag:

可以通过指定Tag来下载特定版本的Release资源：

```
Please help me download Release v1.0.0 from owner/repo
Please help me download Release v1.0.0 from owner/repo to ./history directory

请帮我从 owner/repo 下载 v1.0.0 版本的Release
请帮我从 owner/repo 下载 v1.0.0 版本到 ./history 目录
```

## Technical Implementation / 技术实现

This Skill uses PyGithub library to interact with GitHub API, main features include:

该Skill使用PyGithub库与GitHub API进行交互，主要功能包括：

1. **Get Latest Release**: Use `repo.get_latest_release()` to get the latest release / 获取最新Release：使用`repo.get_latest_release()`获取最新发布版本
2. **Get Release by Tag**: Use `repo.get_release(tag)` to get the release for a specified tag / 获取指定Tag的Release：使用`repo.get_release(tag)`获取指定标签的Release
3. **Get Asset List**: Use `release.get_assets()` to get all downloadable assets / 获取资产列表：使用`release.get_assets()`获取所有可下载的资产
4. **Download Assets**: Directly download asset files through `browser_download_url` / 下载资产：通过`browser_download_url`直接下载资产文件

### Dependencies / 依赖要求

- Python 3.12+ / Python 3.12+
- PyGithub library / PyGithub库
- requests library (for file downloads) / requests库（用于文件下载）
- click library (CLI) / click库（命令行界面）

### Direct Run (Recommended) / 直接运行（推荐）

This script supports uv auto-installing dependencies, just run directly:

该脚本支持uv自动安装依赖，直接运行即可：

```bash
# Direct run, uv will auto-install dependencies
uv run scripts/download_release.py owner repo

# With parameters
uv run scripts/download_release.py owner repo --tag v1.0.0
uv run scripts/download_release.py owner repo --asset-name "linux" --save-dir ./origin/repo
```

```bash
# 直接运行，uv会自动安装依赖
uv run scripts/download_release.py owner repo

# 指定参数
uv run scripts/download_release.py owner repo --tag v1.0.0
uv run scripts/download_release.py owner repo --asset-name "linux" --save-dir ./origin/repo
```

The script header already contains dependency declarations, uv will automatically resolve and install:

脚本头部已包含依赖声明，uv会自动解析并安装：

- pygithub
- requests
- click

## Notes / 注意事项

1. Valid GitHub API access is required, authentication tokens may be needed in some cases / 需要有效的GitHub API访问，部分情况下可能需要配置认证令牌
2. Large asset files may require longer download times / 大型资产文件可能需要较长的下载时间
3. Please ensure sufficient disk space for saving downloaded files / 请确保有足够的磁盘空间用于保存下载的文件
4. Some private repositories may require appropriate access permissions / 部分私有仓库可能需要适当的访问权限
5. **Authentication Token**: If not specified via `--token` parameter, will automatically read from environment variable `GITHUB_TOKEN` / 认证令牌：如果未通过 `--token` 参数指定，将自动从环境变量 `GITHUB_TOKEN` 读取

## Example Output / 示例输出

Example output when download is successful:

成功下载时的输出示例：

```
Fetching latest Release info from owner/repo...
Release version: v1.0.0
Release title: Initial Release
Number of assets: 3

Available assets:
1. example-linux-x64.tar.gz (size: 45.2 MB)
2. example-macos-x64.tar.gz (size: 48.1 MB)
3. example-windows-x64.zip (size: 50.3 MB)

Downloading: example-linux-x64.tar.gz
Download complete: ./origin/repo/example-linux-x64.tar.gz
```

```
正在获取 owner/repo 的最新Release信息...
Release版本: v1.0.0
发布标题: Initial Release
资产数量: 3

可用资产：
1. example-linux-x64.tar.gz (大小: 45.2 MB)
2. example-macos-x64.tar.gz (大小: 48.1 MB)
3. example-windows-x64.zip (大小: 50.3 MB)

正在下载: example-linux-x64.tar.gz
下载完成: ./origin/repo/example-linux-x64.tar.gz
```

## Error Handling / 错误处理

Common error situations and handling:

常见的错误情况及处理方式：

- **Repository not found**: Check if owner and repo names are correct / 仓库不存在：检查owner和repo名称是否正确
- **No Release**: The repository may not have published any Release yet / 无Release：该仓库可能尚未发布任何Release
- **Network error**: Check network connection or try using a proxy / 网络错误：检查网络连接或尝试使用代理
- **Insufficient permissions**: For private repositories, provide a valid access token / 权限不足：对于私有仓库，需要提供有效的访问令牌
