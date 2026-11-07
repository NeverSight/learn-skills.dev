---
name: linkedin-company-page
description: Draft, publish, and verify a post on a LinkedIn company Page administered by the connected member. Use for an organization's LinkedIn feed, not a personal profile.
when_to_use: |
  Use when the user explicitly targets a LinkedIn company Page. The member
  must administer the Page and the OAuth app must have Community Management
  API access with w_organization_social and r_organization_social.
connections: [linkedin/company-page]
allowed_tools: [Bash, publish_artifact]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# LinkedIn company Page

The OAuth token is injected as `$LINKEDIN_COMPANY_PAGE_TOKEN`. This is a
separate connection from the personal LinkedIn connector. The user must supply
the numeric organization ID of a Page they administer. The API rejects Pages
outside their authorized roles.

The script uses the official versioned Posts API. It defaults to a **dry run**;
`--confirm` performs the public write. Do not use a cookie or browser fallback.

```bash
SCRIPT="$SKILL_DIR/scripts/linkedin_company_page.py"
python3 "$SCRIPT" publish --organization-id 123456 --text-file post.txt
# Show the exact text and target Page to the user before this call:
python3 "$SCRIPT" publish --organization-id 123456 --text-file post.txt --confirm
```

The confirmed call returns the LinkedIn post URN from `x-restli-id`, then reads
the post back through `GET /rest/posts/{urn}`. Treat `201` alone as a submitted
post, not verified delivery. If the readback fails, report the URN as pending;
never retry the write until the existing post's status is established.

`LINKEDIN_API_VERSION` can override the default monthly API version if LinkedIn
retires it. The token and request headers must never be printed.

After a verified public URL is returned, record it once with
`publish_artifact(kind="article", channel="linkedin-company-page", title="<title>", url="<real URL>", status="delivered")`.

Official references: [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api), [Organization Access Control](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-access-control).
