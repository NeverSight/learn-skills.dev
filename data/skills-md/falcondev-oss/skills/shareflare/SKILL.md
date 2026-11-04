---
name: shareflare
description: Share any local file through a public URL. Use whenever you need to share a file, including attaching artifacts to GitHub issues or pull requests, showing a file to the user, or fulfilling a request for a shareable URL.
---

# Share files

For every requested file:

1. Require non-empty `SHAREFLARE_URL` and `SHAREFLARE_TOKEN`. If either is unset, stop and name the missing variable.
2. Set `file` to the path and confirm it is a readable regular file.
3. Upload it and capture the response:

```sh
curl --fail-with-body --silent --show-error \
  --data-binary "@$file" \
  -H "Authorization: Bearer $SHAREFLARE_TOKEN" \
  -H "Content-Type: $(file --brief --mime-type -- "$file")" \
  "${SHAREFLARE_URL%/}/"
```

4. Return the URL printed by the service. Completion means every requested file has one returned URL.

Keep `SHAREFLARE_TOKEN` out of output and files.
