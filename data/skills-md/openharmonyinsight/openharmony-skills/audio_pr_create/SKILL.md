---
name: audio_pr_create
description: 使用oh-gc CLI管理GitCode仓库时使用 — 包括认证、issues、PRs、评审人、测试人员、标签、发布和仓库配置。当用户想要提交代码，创建ISSUE，创建PR,更新PR等涉及gitcode网页的操作时使用该技能。
---

# 初始化
- 查看当前是否配置令牌，如果没有配置，用`./assets/config.json`中的'username'和'token'进行git的配置
```
git config --global credential.helper store
```
## 初始化仓库
- 采用```git remote -v```查看当前远端仓库是否存在，远端仓库一般下列形式：
```
upstream	https://gitcode.com/openharmony/multimedia_audio_framework (fetch)
upstream	https://gitcode.com/openharmony/multimedia_audio_framework (push)
```
- 查看fork仓库是否添加，fork仓库格式为: "https://gitcode.com/{username}/{repo}.git"其中，{username}和{repo}为`./assets/config.json`中的'username'和'token'，fork仓库一般命名为origin，
如果没有，使用```git remote add```加上

## 初始化oh-gc CLI
- 参考 `./references/Readme.md`进行oh-gc的初始化，其中登录使用的token采用`./assets/config.json`的token

# 提交注意事项
- 判断当前代码是否有更新
- 查看一下当前用户是否已经git commit过，如果用户已经commit，则push到远端fork仓库，否则，帮助用户进行commit操作，注意！！```git commit```时必须要加上-s，-m的信息中添加"Co-Authored-By: Agent"，提交后进行push到origin的fork仓库
- 查看当前是否已经存在相关PR，如果当前修改只是修改上一笔PR的代码，则直接采用```git commit --amend```后进行push注意添加 -f 不需要重新创建PR，***直接结束当前技能***。否则进行push，并开始下面的PR的创建
- 遵循创建流程，先创建ISSURE然后将ISSUE绑定到PR之中

# 创建流程

## Step1.创建ISSUE
```
// title根据当此任务以及修改确认
// body根据指定的labels选择`assets/ISSUE_TEMPLATE`中的指定模板，必须选择模板，不能自己生成，body中的内容需要进行填充，模板中的版本选择master
// labels需要和模板匹配
// repo为 owner/repo
oh-gc issue:create --repo openharmony/multimedia_audio_framework --title "test cli" --body "test cli" --labels "bug"
```
如果成功创建则获得返回："https://gitcode.com/openharmony/multimedia_audio_framework/issues/11908"
记录其中的"issue_id"为11908

## Step2.创建PR

## 参数配置
1. title需要根据当此任务以及修改确认
2. head为当前提交分支
3. body选择`assets/PR_TEMPLATE/PULL_REQUEST_TEMPLATE.zh-CN.md`并根据内容将模板中的自检结果更新,其中**IssueNo**字段应该填写创建ISSUE中返回的ISSUE url.
**通用规范自检：**字段必须根据本次修改进行填写自检结果，|Y/N/NA|必须选择其中一个进行填写
4. repo为 owner/repo
5. base一般为 master

```
oh-gc pr:create --repo openharmony/multimedia_audio_framework --head feature --base master --title "PR标题" --body body
```

如果创建成功则返回："Created PR #14486: PR标题"
失败，则去查询pr中是否存在已经创建好的，如果存在则返回，如果不存在则直接返回失败原因告知用户，结束流程.

## Step3.开始构建
成功创建PR后，询问用户是否需要开始构建？
用户否认，则退出流程。
用户需要，则等待PR完全初始化后,等30s,帮助用户开始构建
```
oh-gc pr:comment 14486 --body "start build"
```
如果失败，进行重试，重试3次之后如果依旧失败，则告知用户失败原因并退出。