---
name: feishu-webhook-skill
description: >
  Must Use this skill to send Feishu(飞书/Lark) webhook msgs.
---
以下是向飞书发送Webhook发送消息的专业技能。

## 注意事项

- 本文提供的示例代码中所有的 `receive_id`（消息接收者 ID）、`user_id`（用户的 user_id）、`image_key`（上传图片后获取到的图片标识 key）、`file_key`（上传文件后获取到的文件标识 Key） 等参数值均为示例数据。你在实际开发过程中，需要替换为真实可用的数据。

- 如果需要发送的内容涉及图片，必须阅读 webhook-image.md 文档来了解发送图片的要求。

## 消息内容介绍

在 **发送消息**、**回复消息**、**编辑消息** 接口中，均需要传入消息内容（`content`），不同的消息类型对应的 `content` 也不相同。以文本类型的消息为例，请求体示例如下：

```json
{
    "receive_id": "ou_7d8a6e6df7621556ce0d21922b676706ccs",
    "content": "{\"text\":\" test content\"}",
    "msg_type": "text"
}
```
**注意**：`content` 字段为 string 类型，JSON 结构需要先进行转义再传值。在调用接口时，你可以先构造一个结构体，然后使用 JSON 序列化转换为 string 类型，或者通过第三方的 JSON 转换工具进行转义。

## 各类型的消息内容 JSON 结构

### 富文本 post

在一条富文本消息中，支持添加文字、图片、视频、@、超链接等元素。如下 JSON 格式的内容是一个富文本示例，其中：

- 一个富文本可分多个段落（由多个 `[]` 组成），每个段落可由多个元素组成，每个元素由 tag 和相应的描述组成。
- 图片、视频元素必须是独立的一个段落。
- 实际发送消息时，需要将 JSON 格式的内容压缩为一行、并进行转义。
- 如需参考该 JSON 示例构建富文本消息内容，则需要把其中的 user_id、image_key、file_key 等示例值替换为真实值。

```json 
{
	"zh_cn": {
		"title": "我是一个标题",
		"content": [
			[
				{
					"tag": "text",
					"text": "第一行:",
					"style": ["bold", "underline"]

},
				{
					"tag": "a",
					"href": "http://www.feishu.cn",
					"text": "超链接",
					"style": ["bold", "italic"]
				},
				{
					"tag": "at",
					"user_id": "ou_1avnmsbv3k45jnk34j5",
					"style": ["lineThrough"]
				}
			],
          	[{
				"tag": "img",
				"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
			}],
			[	
				{
					"tag": "text",
					"text": "第二行:",
					"style": ["bold", "underline"]
				},
				{
					"tag": "text",
					"text": "文本测试"
				}
			],
          	[{
				"tag": "img",
				"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
			}],
          	[{
				"tag": "media",
				"file_key": "file_v2_0dcdd7d9-fib0-4432-a519-41d25aca542j",
				"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
			}],
          	[{
				"tag": "emotion",
				"emoji_type": "SMILE"
			}],
			[{
				"tag": "hr"
			}],
			[{
				"tag": "code_block",
				"language": "GO",
				"text": "func main() int64 {\n    return 0\n}"
			}],
			[{
				"tag": "md",
				"text": "**mention user:**<at user_id=\"ou_xxxxxx\">Tom</at>\n**href:**[Open Platform](https://open.feishu.cn)\n**code block:**\n```GO\nfunc main() int64 {\n    return 0\n}\n```\n**text styles:** **bold**, *italic*, ***bold and italic***, ~underline~,~~lineThrough~~\n> quote content\n\n1. item1\n    1. item1.1\n    2. item2.2\n2. item2\n --- \n- item1\n    - item1.1\n    - item2.2\n- item2"
			}]
		]
	},
	"en_us": {
		...
	}
}
``` 

**参数说明**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
zh_cn, en_us | object | 是 | 多语言配置字段。如果不需要配置多语言，则仅配置一种语言即可。<br>- `zh_cn` 为富文本的中文内容<br>- `en_us` 为富文本的英文内容<br>**注意**：该字段无默认值，至少要设置一种语言。<br>**示例值**：zh_cn
∟ title | string | 否 | 富文本消息的标题。<br>**默认值**：空<br>**示例值**：title
∟ content | string | 是 | 富文本消息内容。由多个段落组成（段落由`[]`分隔），每个段落为一个 node 列表，所支持的 node 标签类型以及对应的参数说明，参见下文的 **富文本支持的标签和参数说明** 章节。<br>**注意**：如 **示例值** 所示，各类型通过 tag 参数设置。例如文本（text）设置为 `"tag": "text"`。<br>**示例值**：[[{"tag": "text","text": "text content"}]]

#### **富文本支持的标签和参数说明**

- **text：文本标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
text | string | 是 | 文本内容。<br>**示例值**：test content
un_escape | boolean | 否 | 是否 unescape 解码。默认为 false，无需使用可不传值。<br>**示例值**：false
style | []string | 否 | 文本内容样式，支持的样式有：<br>- bold：加粗<br>- underline：下划线<br>- lineThrough：删除线<br>- italic：斜体<br>**注意**：<br>- 默认值为空，表示无样式。<br>- 传入的值如果不是以上可选值，则被忽略。<br>**示例值**：["bold", "underline"]

-  **a：超链接标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
text | string | 是 | 超链接的文本内容。<br>**示例值**：超链接
href | string | 是 | 超链接地址。<br>**注意**：请确保链接地址的合法性，否则消息会发送失败。<br>**示例值**：https://open.feishu.cn
style | []string | 否 | 超链接文本内容样式，支持的样式有：<br>- bold：加粗<br>- underline：下划线<br>- lineThrough：删除线<br>- italic：斜体<br>**注意**：<br>- 默认值为空，表示无样式。<br>- 传入的值如果不是以上可选值，则被忽略。<br>**示例值**：["bold", "italic"]

- **at：@标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
user_id | string | 是 | 用户 ID，用来指定被 @ 的用户。传入的值可以是用户的 user_id、open_id、union_id。各类 ID 获取方式参见[如何获取 User ID、Open ID 和 Union ID](https://open.feishu.cn/document/home/user-identity-introduction/open-id)。<br>**注意**：<br>- @ 单个用户时，该字段必须传入实际用户的真实 ID。<br>- 如需 @ 所有人，则该参数需要传入 `all`。
style | []string | 否 | at 文本内容样式，支持的样式有：<br>- bold：加粗<br>- underline：下划线<br>- lineThrough：删除线<br>- italic：斜体<br>**注意**：<br>- 默认值为空，表示无样式。<br>- 传入的值如果不是以上可选值，则被忽略。<br>**示例值**：["lineThrough"]

- **img：图片标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
image_key | string | 是 | 图片 Key。通过[上传图片](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)接口可以获取到图片 Key（image_key）。<br>**示例值**：d640eeea-4d2f-4cb3-88d8-c964fab53987

- **media：视频标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
file_key | string | 是 | 视频文件的 Key。通过[上传文件](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)接口上传视频（mp4 格式）后，可以获取到视频文件 Key（file_key）。<br>**示例值**：file_v2_0dcdd7d9-fib0-4432-a519-41d25aca542j
image_key | string | 否 | 视频封面图片的 Key。通过[上传图片](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)接口可以获取到图片 Key（image_key）。<br>**默认值**：空，表示无视频封面。<br>**示例值**：img_7ea74629-9191-4176-998c-2e603c9c5e8g

- **emotion：表情标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
emoji_type | string | 是 | 表情文案类型。可选值参见[表情文案说明](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-reaction/emojis-introduce)。<br>**示例值**：SMILE

- **code_block：代码块标签**

名称 | 类型 | 是否必填 | 描述
---|---|---|---
language | string | 否 | 代码块的语言类型。可选值有 PYTHON、C、CPP、GO、JAVA、KOTLIN、SWIFT、PHP、RUBY、RUST、JAVASCRIPT、TYPESCRIPT、BASH、SHELL、SQL、JSON、XML、YAML、HTML、THRIFT 等。<br>**注意**：<br>- 取值不区分大小写。<br>- 不传值则默认为文本类型。<br>**示例值**：GO
text | string | 是 | 代码块内容。<br>**示例值**：func main() int64 {\n return 0\n}

- **hr：分割线标签**

富文本支持 `tag` 取值为 `hr`，表示一条分割线，该标签内无其他参数。

- **md：Markdown 标签**warning
**注意**：
- `md` 标签会独占一个或多个段落，不能与其他标签在同一行。
- `md` 标签仅支持发送，[获取消息内容](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/get)时将不再包含此标签，会根据 `md` 中的内容转换为其他相匹配的标签。
- 引用、有序、无序列表在获取消息内容时，会简化为文本标签（text）进行输出。

`md` 标签内通过 `text` 参数设置 Markdown 内容。

名称 | 类型 | 是否必填 | 描述
---|---|---|---
text | string | 是 | Markdown 内容。支持的内容参见下表。<br>**示例值**：1. item1\n2. item2

在 `text` 参数内支持的语法如下表所示。

语法 | 示例 | 说明
---|---|---
@ 用户 | `<at user_id="ou_xxxxx">User</at>` | 支持 @ 单个用户或所有人。<br>- @ 单个用户时，需要在 user_id 内传入实际用户的真实 ID。传入的值可以是用户的 user_id、open_id、union_id。各类 ID 获取方式参见[如何获取 User ID、Open ID 和 Union ID](https://open.feishu.cn/document/home/user-identity-introduction/open-id)。<br>- 如需 @ 所有人，需要将 user_id 取值为 `all`。
超链接 | `[Feishu Open Platform](https://open.feishu.cn)` | 在 Markdown 语法内，`[]` 用来设置超链接的文本内容、`()` 用来设置超链接的地址。  <br>**注意**：请确保链接地址的合法性，否则只发送文本内容部分。
有序列表 | `1. item1\n2. item2` | Markdown 配置说明：<br>- 每个编号的 `.` 符与后续内容之间要有一个空格。<br>- 每一列独立一行。如示例所示，可使用 `\n` 换行符换行。<br>- 支持嵌套多层级。<br>- 每个层级缩进 4 个空格，且编号均从 `1.` 开始。<br>- 可以与无序列表混合使用。
无序列表 | `- item1\n- item2` | Markdown 配置说明：<br>- 每列的 `-` 符与后续内容之间要有一个空格。<br>- 每一列独立一行。如示例所示，可使用 `\n` 换行符换行。<br>- 支持嵌套多层级。<br>- 每个层级缩进 4 个空格。<br>- 可以与有序列表混合使用，有序列表以 `1.` 开始编号。
代码块 | \`\`\`GO\nfunc main(){\n return\n}\n\`\`\` | 代码块内容首尾需要使用 \`\`\` 符号包裹，首部 \`\`\` 后紧跟代码语言类型。支持的语言类型有 PYTHON、C、CPP、GO、JAVA、KOTLIN、SWIFT、PHP、RUBY、RUST、JAVASCRIPT、TYPESCRIPT、BASH、SHELL、SQL、JSON、XML、YAML、HTML、THRIFT 等（不区分大小写）。
引用 | `> demo` | 引用内容。`>` 符与后续内容之间要有一个空格。
分割线 | `\n --- \n` | 如示例所示，前后需要各有一个 `\n` 换行符。
加粗 | `**加粗文本**` | 配置说明：<br>- `**` 符与加粗文本之间不能有空格。<br>- 加粗可以与斜体合用。例如 `***加粗+斜体***`。<br>- 加粗的文本不支持再解析其他组件。例如文本为超链接则不会被解析。
斜体 | `*斜体文本*` | 配置说明：<br>- `*` 符与加粗文本之间不能有空格。<br>- 斜体可以与加粗合用。例如 `***加粗+斜体***`。<br>- 斜体的文本不支持再解析其他组件。例如文本为超链接则不会被解析。
下划线 | `~下划线文本~` | 配置说明：<br>- `~` 符与下划线文本之间不能有空格。<br>- 下划线的文本不支持再解析其他组件。例如文本为超链接则不会被解析。<br>- 不支持与加粗、斜体、删除线合用。
删除线 | `~~删除线~~` | 配置说明：<br>- `~~` 符与下划线文本之间不能有空格。<br>- 删除线的文本不支持再解析其他组件。例如文本为超链接则不会被解析。<br>- 不支持与加粗、斜体、下划线合用。

### 卡片 interactive

飞书卡片是一种可以灵活构建图文内容的消息类型：
1. 你应该阅读 webhook-card-common.md来了解卡片结构的详情。
2. 必须阅读 webhook-card-content.md 和webhook-card-container.md 来了解卡片的构造
3. 如果涉及到复杂图表的可视化，则阅读webhook-card-visual.md

