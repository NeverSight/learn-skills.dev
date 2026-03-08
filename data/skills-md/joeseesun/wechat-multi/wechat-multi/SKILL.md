---
name: wechat-multi
description: macOS 微信多开工具（小绿书）。通过复制 WeChat.app、修改 Bundle ID、重新签名来实现多实例运行。当用户说"打开两个微信"、"微信双开"、"微信多开"、"再开一个微信"、"微信更新后重建"、"修复微信多开"、"关闭所有微信"、"小绿书"等时使用。macOS 专属，脚本位于 scripts/wechat-multi.sh。
---

# WeChat Multi-Instance (小绿书)

## 命令映射

脚本路径：`~/.claude/skills/wechat-multi/scripts/wechat-multi.sh`（以下简称 `SCRIPT`）

## 首次使用

需要 `sudo` 权限。建议配置 sudoers 免密码，否则每次会弹出密码输入：

```bash
echo "$(whoami) ALL=(ALL) NOPASSWD: $(which bash) $(ls ~/.claude/skills/wechat-multi/scripts/wechat-multi.sh)" | sudo tee /etc/sudoers.d/wechat-multi
```

## 命令映射

| 用户说 | 执行命令 |
|--------|----------|
| "打开两个微信" / "微信双开" | `sudo $SCRIPT auto --force` |
| "打开N个微信" / "微信多开N个" | `sudo $SCRIPT multi N --force` |
| "再开一个微信" | `open -n /Applications/小绿书.app` |
| "微信更新后重建" / "修复微信多开" | `sudo $SCRIPT rebuild --force` |
| "关闭所有微信" | `sudo $SCRIPT kill` |

## 注意事项

- 微信更新后副本会失效，运行 `rebuild` 重建
- 副本名为 `小绿书.app`（双开）或 `小绿书1.app`、`小绿书2.app`...（多开）
- 如果提示签名错误，也用 `rebuild` 修复
