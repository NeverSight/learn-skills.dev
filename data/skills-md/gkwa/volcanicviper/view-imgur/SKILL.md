---
name: view-imgur
description: View an imgur image by downloading it with curl and reading the local file. Use whenever an i.imgur.com URL is shared, because WebFetch cannot load imgur URLs directly.
---

## Viewing Imgur Images

WebFetch cannot load imgur URLs — imgur blocks that access path.

To view an imgur image, download it with curl and read the local file:

```
curl -L -o /tmp/image.png "https://i.imgur.com/example.png"
```

Then read `/tmp/image.png` directly using the Read tool.

This applies to all `i.imgur.com` image links.
