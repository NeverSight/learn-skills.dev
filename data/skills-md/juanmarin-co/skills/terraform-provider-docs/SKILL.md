---
name: terraform-provider-docs
description: Use when configuration or reference documentation for a public Terraform Registry provider is needed.
---

1. Read the provider address from the `source` attribute in `required_providers`.
2. Discover its repository URL from `.data.attributes.source` at:

   ```text
   https://registry.terraform.io/v2/providers/<namespace>/<provider>
   ```

3. Call the Skill tool with `dependency-docs`.
