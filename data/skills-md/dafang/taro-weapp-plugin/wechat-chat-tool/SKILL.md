---
name: wechat-chat-tool
description: 微信小程序聊天工具开发指南。当开发聊天工具分包、配置 chatTools、发送消息到群聊、动态消息、获取群成员信息、wx.openChatTool、wx.getChatToolInfo 时使用。
---

# 微信小程序聊天工具开发指南

基础库 3.7.8+ 支持，Android/iOS 微信 8.0.56+

## 快速配置

### app.json 配置示例

```json
{
  "subPackages": [
    {
      "root": "packageChatTool",
      "pages": ["pages/entry/index"],
      "entry": "entry.js", // 独立分包入口文件（必须）
      "independent": true,
      "componentFramework": "glass-easel",
      "renderer": "skyline"
    }
  ],
  "chatTools": [{
    "root": "packageChatTool",
    "entryPagePath": "pages/entry/index",
    "desc": "功能描述",
    "scopes": []
  }],
  "rendererOptions": {
    "skyline": {
      "disableABTest": true,
      "defaultDisplayBlock": true,
      "defaultContentBox": true
    }
  }
}
```

其中 `entry.js` 的代码通常：

```
// 独立分包入口文件
// 用于聊天工具模式的初始化

const enterOptions = wx.getEnterOptionsSync()
console.log('[ChatTool Entry] Enter options:', enterOptions)
```

**注意事项**:

- 分包体积不超过 500KB
- 必须使用 skyline 渲染
- 每个小程序目前仅支持配置一个聊天工具

## 核心 API

### 进入/退出聊天模式

| API                 | 用途                                                     |
| ------------------- | -------------------------------------------------------- |
| `wx.openChatTool`   | 打开聊天工具模式（可传入 opengid 或 open_single_roomid） |
| `wx.getApiCategory` | 判断是否在聊天工具模式（apiCategory === 'chatTool'）     |
| `wx.navigateBack`   | 退出聊天工具模式                                         |

### 获取聊天信息

| API                     | 用途                              |
| ----------------------- | --------------------------------- |
| `wx.getChatToolInfo`    | 在聊天工具分包内获取绑定群聊信息  |
| `wx.getGroupEnterInfo`  | 进入前获取群聊 id 信息            |
| `wx.selectGroupMembers` | 选择聊天室成员，返回 group_openid |

### ID 类型

- `opengid`: 群聊唯一标识
- `open_single_roomid`: 单聊唯一标识
- `group_openid`: 用户在此聊天室下的唯一标识

### 发送到聊天

| API                         | 用途                         |
| --------------------------- | ---------------------------- |
| `wx.shareAppMessageToGroup` | 发送小程序卡片               |
| `wx.notifyGroupMembers`     | 发送提醒消息（@成员 + 任务） |
| `wx.shareImageToGroup`      | 发送图片                     |
| `wx.shareVideoToGroup`      | 发送视频                     |
| `wx.shareFileToGroup`       | 发送文件                     |
| `wx.shareEmojiToGroup`      | 发送表情                     |

### 动态消息

1. 服务端创建 `activity_id`
2. 前端 `wx.updateShareMenu` 声明动态消息
3. 服务端 `setChatToolMsg` 更新状态

```javascript
wx.updateShareMenu({
  withShareTicket: true,
  isUpdatableMessage: true,
  activityId: "xxx",
  useForChatTool: true,
  chooseType: 1, // 1=指定成员, 2=全部成员
  participant: members,
  templateInfo: {
    templateId: "4A68CBB88A92B0A9311848DBA1E94A199B166463", // 完成类
    // 或 '2A84254B945674A2F88CE4970782C402795EB607' 参与类
  },
});
```

## 禁用能力

聊天工具模式下不支持：

- 普通转发（button open-type=share）
- 外跳接口（navigateToMiniProgram 等）
- 广告组件（ad、ad-custom）

## 7. 聊天工具核心API详解

### wx.openChatTool

打开聊天工具。

#### 参数

##### Object object

| 属性     | 类型     | 默认值 | 必填 | 说明                                                                                          |
| -------- | -------- | ------ | ---- | --------------------------------------------------------------------------------------------- |
| url      | string   |        | 是   | 聊天工具分包内的页面路径                                                                      |
| roomid   | string   |        | 否   | 聊天室id，不传则拉起群选择框，可以传入多聊群的 opengid 值，或者单聊群的 open_single_roomid 值 |
| chatType | number   |        | 否   | 群聊类型                                                                                      |
| success  | function |        | 否   | 接口调用成功的回调函数                                                                        |
| fail     | function |        | 否   | 接口调用失败的回调函数                                                                        |
| complete | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）                                              |

##### object.chatType 合法值

| 值 | 说明               |
| -- | ------------------ |
| 1  | 微信联系人单聊     |
| 2  | 企业微信联系人单聊 |
| 3  | 普通微信群聊       |
| 4  | 企业微信互通群聊   |

#### 示例代码

```javascript
wx.openChatTool({
  url: "pages/chat/index", // 示例路径
  chatType: 1, // 微信联系人单聊
  success(res) {
    console.log("打开聊天工具成功", res);
  },
  fail(err) {
    console.error("打开聊天工具失败", err);
  },
});
```

### wx.getApiCategory

#### wx.getApiCategory()

> 基础库 2.22.1 开始支持，低版本需做
> [兼容处理](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html)。

获取当前小程序的 API 类别。

##### 返回值

###### string

当前 API 类别。

**合法值**

| 值                   | 说明                                                   |
| -------------------- | ------------------------------------------------------ |
| default              | 默认类别                                               |
| nativeFunctionalized | 原生功能化，视频号直播商品、商品橱窗等场景打开的小程序 |
| browseOnly           | 仅浏览，朋友圈快照页等场景打开的小程序                 |
| embedded             | 内嵌，通过打开半屏小程序能力打开的小程序               |
| chatTool             | 聊天工具打开小程序                                     |

##### 示例代码

```javascript
const apiCategory = wx.getApiCategory();
console.log(apiCategory);
```

### wx.shareAppMessageToGroup

#### wx.shareAppMessageToGroup(Object object)

> 基础库 3.7.12 开始支持，低版本需做
> [兼容处理](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html)。

转发小程序卡片到聊天。

##### 参数

###### Object object

| 属性     | 类型     | 默认值   | 必填 | 说明                                                                |
| -------- | -------- | -------- | ---- | ------------------------------------------------------------------- |
| title    | string   |          | 是   | 转发标题                                                            |
| path     | string   | 当前页面 | 否   | 转发路径，必须是以 / 开头的完整路径，默认为当前页面                 |
| imageUrl | string   | 截图     | 否   | 自定义图片路径，支持 PNG 及 JPG，显示图片长宽比是 5:4，默认使用截图 |
| success  | function |          | 否   | 接口调用成功的回调函数                                              |
| fail     | function |          | 否   | 接口调用失败的回调函数                                              |
| complete | function |          | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）                    |

##### 示例代码

```javascript
wx.shareAppMessageToGroup({
  title: "分享标题",
  path: "/path/to/page",
  imageUrl: "",
});
```

### wx.shareVideoToGroup

#### wx.shareVideoToGroup(Object object)

分享视频到聊天。

##### 参数

###### Object object

| 属性             | 类型     | 默认值 | 必填 | 说明                                                     |
| ---------------- | -------- | ------ | ---- | -------------------------------------------------------- |
| videoPath        | string   |        | 是   | 要分享的视频地址，必须为本地路径或临时路径               |
| thumbPath        | string   |        | 否   | 缩略图路径，若留空则使用视频首帧                         |
| needShowEntrance | boolean  | true   | 否   | 分享的图片消息是否要带小程序入口                         |
| entrancePath     | string   | ''     | 否   | 从消息小程序入口打开小程序的路径，默认为聊天工具启动路径 |
| success          | function |        | 否   | 接口调用成功的回调函数                                   |
| fail             | function |        | 否   | 接口调用失败的回调函数                                   |
| complete         | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）         |

##### 示例代码

```javascript
wx.shareVideoToGroup({
  videoPath: "path/to/video.mp4",
  thumbPath: "path/to/thumb.png",
  needShowEntrance: true,
  success(res) {
    console.log("分享视频成功", res);
  },
  fail(err) {
    console.error("分享视频失败", err);
  },
});
```

### wx.shareImageToGroup

#### wx.shareImageToGroup(Object object)

分享图片到聊天。

##### 参数

###### Object object

| 属性             | 类型     | 默认值 | 必填 | 说明                                                     |
| ---------------- | -------- | ------ | ---- | -------------------------------------------------------- |
| imagePath        | string   |        | 是   | 要分享的图片地址，必须为本地路径或临时路径               |
| needShowEntrance | boolean  | true   | 否   | 分享的图片消息是否要带小程序入口                         |
| entrancePath     | string   | ''     | 否   | 从消息小程序入口打开小程序的路径，默认为聊天工具启动路径 |
| success          | function |        | 否   | 接口调用成功的回调函数                                   |
| fail             | function |        | 否   | 接口调用失败的回调函数                                   |
| complete         | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）         |

##### 示例代码

```javascript
wx.shareImageToGroup({
  imagePath: "path/to/image.png",
  needShowEntrance: true,
  success(res) {
    console.log("分享图片成功", res);
  },
  fail(err) {
    console.error("分享图片失败", err);
  },
});
```

### wx.shareEmojiToGroup

#### wx.shareEmojiToGroup(Object object)

分享表情到聊天。

##### 参数

###### Object object

| 属性             | 类型     | 默认值 | 必填 | 说明                                                     |
| ---------------- | -------- | ------ | ---- | -------------------------------------------------------- |
| imagePath        | string   |        | 是   | 要分享的表情地址，必须为本地路径或临时路径               |
| needShowEntrance | boolean  | true   | 否   | 分享的表情消息是否要带小程序入口                         |
| entrancePath     | string   | ''     | 否   | 从消息小程序入口打开小程序的路径，默认为聊天工具启动路径 |
| success          | function |        | 否   | 接口调用成功的回调函数                                   |
| fail             | function |        | 否   | 接口调用失败的回调函数                                   |
| complete         | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）         |

##### 示例代码

```javascript
wx.shareEmojiToGroup({
  imagePath: "path/to/image.png",
  needShowEntrance: true,
  success(res) {
    console.log("分享表情成功", res);
  },
  fail(err) {
    console.error("分享表情失败", err);
  },
});
```

### wx.selectGroupMembers

#### wx.selectGroupMembers(Object object)

从群组中选择成员。

##### 参数

###### Object object

| 属性           | 类型     | 默认值 | 必填 | 说明                                             |
| -------------- | -------- | ------ | ---- | ------------------------------------------------ |
| maxSelectCount | number   |        | 否   | 最多可选人数                                     |
| success        | function |        | 否   | 接口调用成功的回调函数                           |
| fail           | function |        | 否   | 接口调用失败的回调函数                           |
| complete       | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行） |

###### object.success 回调函数

####### 参数

######## Object res

| 属性    | 类型           | 说明                                                             |
| ------- | -------------- | ---------------------------------------------------------------- |
| members | Array.<string> | 所选用户在此聊天室下的唯一标识，同一个用户在不同的聊天室下id不同 |

##### 示例代码

```javascript
wx.selectGroupMembers({
  maxSelectCount: 10,
  success(res) {
    console.log("选择成员成功", res.members);
  },
  fail(err) {
    console.error("选择成员失败", err);
  },
});
```

### wx.notifyGroupMembers

#### wx.notifyGroupMembers(Object object)

发送消息提醒群成员。

##### 参数

###### Object object

| 属性         | 类型           | 默认值   | 必填 | 说明                                                                                                                                  |
| ------------ | -------------- | -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------- |
| title        | string         |          | 是   | 文字链标题，发送的内容将由微信拼接为：@的成员列表+“请完成：”/"请参与："+打开小程序的文字链，如「@alex @cindy 请完成：团建报名统计」。 |
| members      | Array.<string> |          | 是   | 需要提醒的用户 group_openid 列表                                                                                                      |
| entrancePath | string         |          | 是   | 文字链跳转路径                                                                                                                        |
| type         | string         | complete | 否   | 展示的动词                                                                                                                            |
| success      | function       |          | 否   | 接口调用成功的回调函数                                                                                                                |
| fail         | function       |          | 否   | 接口调用失败的回调函数                                                                                                                |
| complete     | function       |          | 否   | 接口调用结束的回调函数（调用成功、失败都会执行）                                                                                      |

###### object.type 合法值

| 值          | 说明   |
| ----------- | ------ |
| participate | 请参与 |
| complete    | 请完成 |

##### 示例代码

```javascript
wx.notifyGroupMembers({
  title: "团建报名统计",
  members: ["openid1", "openid2"],
  entrancePath: "/pages/index/index",
  type: "complete",
  success(res) {
    console.log("提醒成功", res);
  },
  fail(err) {
    console.error("提醒失败", err);
  },
});
```

## 完整文档

详见 [reference.md](reference.md)
