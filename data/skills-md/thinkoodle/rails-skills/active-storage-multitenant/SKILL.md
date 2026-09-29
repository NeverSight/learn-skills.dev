---
name: active-storage-multitenant
description: Expert guidance for Active Storage with activerecord-tenanted. Use when blobs 404 after save, Lexxy/Trix uploads, direct uploads, tenant-signed blob IDs, rails/active_storage redirects, or "Cannot generate a Blob key without a tenant". Requires the activerecord-tenanted skill. Not for single-database Active Storage.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails active_storage:*), Bash(bin/rails db:*), Bash(bin/rails test:*), Bash(bin/rails test)
---

# Active Storage + activerecord-tenanted

Blobs live in the **tenant** database (`tenanted_rails_records = true`). Default Active Storage controllers look in the **global** connection, so uploads succeed and saved images 404. Direct-upload must create the blob inside `with_tenant`, and the `signed_id` must include the tenant key.

Single-database apps: use the `active-storage` skill only. This skill is the Herald overlay.

## Philosophy

1. **Never create a blob without a current tenant.** The storage key is `{tenant_key}/{token}`.
2. **Sign blob id + tenant together.** A tenant-local numeric/UUID id is not globally unique. Serving "the first match" is a cross-tenant leak.
3. **Redirect URLs go through your controllers**, not a public S3 URL, so tenant checks run.
4. **Fail closed on ambiguous legacy IDs.** One match is ok; two matches are 404.

## Config (required)

```ruby
# config/initializers/tenanted.rb
config.active_record_tenanted.tenanted_rails_records = true
config.active_record_tenanted.connection_class = "ApplicationRecord"
```

Without those, blob rows land in global and keys have no prefix.

## Tenant-signed IDs

```ruby
module ActiveStorage::TenantSignedId
  PURPOSE = :tenant_blob_id

  def self.generate(blob, tenant_key: tenant_key_for(blob))
    return blob.signed_id if tenant_key.blank?
    ActiveStorage.verifier.generate({ id: blob.id, tenant: tenant_key }, purpose: PURPOSE)
  end

  def self.verify(signed_id)
    if (payload = ActiveStorage.verifier.verified(signed_id, purpose: PURPOSE))
      payload = payload.with_indifferent_access
      return { id: payload[:id], tenant: payload[:tenant], legacy: false }
    end
    if (legacy_id = ActiveStorage.verifier.verified(signed_id, purpose: :blob_id))
      { id: legacy_id, tenant: nil, legacy: true }
    end
  end

  def self.tenant_key_for(blob)
    tenant_key, blob_token = blob.key.to_s.split("/", 2)
    blob_token.present? ? tenant_key : nil
  end
end
```

`blob_url_template` must pass `tenant:` so Lexxy doesn't generate tenantless URLs:

```erb
<%= f.rich_text_area :body, data: {
  direct_upload_url: project_direct_uploads_path(@project),
  blob_url_template: rails_service_blob_path(":signed_id", ":filename", tenant: @project.tenant_key)
} %>
```

A `?tenant=` query param **must not** upgrade a legacy signed id. If the signed payload has no tenant, ignore the hint and only serve when that blob id is unique across all tenant DBs.

## Direct uploads

Replace `/rails/active_storage/direct_uploads` with a nested route that knows the tenant:

```ruby
class DirectUploadsController < ApplicationController
  include ActiveStorage::SetCurrent

  def create
    blob = ApplicationRecord.with_tenant(Current.account.tenant_key) do
      ActiveStorage::Blob.create_before_direct_upload!(**blob_args)
    end
    render json: {
      signed_id: ActiveStorage::TenantSignedId.generate(blob, tenant_key: Current.account.tenant_key),
      url: rails_service_blob_path(signed_id, blob.filename, tenant: Current.account.tenant_key),
      direct_upload: {
        url: blob.service_url_for_direct_upload,
        headers: blob.service_headers_for_direct_upload
      }
      # plus id, filename, byte_size, checksum, content_type, attachable_sgid
    }
  end
end
```

Return a **Rails redirect URL**, not the S3 URL. `previewable: false` forces Lexxy to use `blob_url_template`.

## Override AS redirect controllers

Rails autoloads `ActiveStorage::Blobs::RedirectController` from `app/controllers/active_storage/...` with the same constant name. No route override.

The concern:

1. `TenantSignedId.verify`
2. If tenant in payload → load blob in that shard only
3. If legacy → scan tenants, 404 if `matches.many?`
4. `ApplicationRecord.current_tenant = @tenant_for_blob` for the rest of the request
5. Redirect to `@blob.url` with `allow_other_host: true`

Same for representations (variants): process **inside** `with_tenant`.

Skip account rows whose tenant DB doesn't exist yet (`TenantDoesNotExistError`) so a new account doesn't abort the scan.

## CSP + storage.yml

Add the bucket host to `connect_src` and `img_src`. Do **not** set `public: true` unless the bucket is actually public — signed headers will break.

## Tests

```ruby
ApplicationRecord.with_tenant(account.tenant_key) do
  blob = ActiveStorage::Blob.create_before_direct_upload!(...)
  assert blob.key.start_with?("#{account.tenant_key}/")
end
```

Also: two tenants with the same numeric blob id must not serve each other's file from a tenantless URL.

## Anti-Patterns

1. **Using stock direct uploads** — blob created untenanted → 404 later, not at upload time.
2. **First-match lookup across tenants** — IDOR.
3. **Putting blobs on GlobalRecord** — `tenanted_rails_records` exists so you don't.
4. **Discovering this only in production S3** — disk service hides redirect/CSP issues. Test with the real service.

## Related

- Shard setup: `activerecord-tenanted`
- Vanilla attachments: `active-storage`
- Lexxy: `action-text`

See [reference.md](reference.md) for the controller file list and lookup algorithm.
