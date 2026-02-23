---
name: backblaze-coder
description: This skill guides Backblaze B2 Cloud Storage integration with OpenTofu/Terraform and B2 CLI. Use when managing B2 buckets, application keys, file uploads, lifecycle rules, or S3-compatible storage.
allowed-tools: Read Write Edit Grep Glob Bash
---

See [references/b2-cli-setup.md](references/b2-cli-setup.md) for B2 CLI installation and authentication.
See [references/b2-key-capabilities.md](references/b2-key-capabilities.md) for application key capabilities and sync flags.

## B2 CLI Operations

### Bucket Management

```bash
b2 bucket list
b2 bucket create my-bucket allPrivate
b2 bucket create my-bucket allPrivate \
  --lifecycle-rules '[{"daysFromHidingToDeleting": 30, "fileNamePrefix": "logs/"}]'
b2 bucket delete my-bucket
```

### File Operations

```bash
b2 ls my-bucket
b2 ls my-bucket path/to/folder/
b2 upload-file my-bucket local-file.txt remote/path/file.txt
b2 upload-file --content-type "application/json" my-bucket data.json data.json
b2 download-file-by-name my-bucket remote/path/file.txt local-file.txt
b2 download-file-by-id <fileId> local-file.txt
b2 rm my-bucket path/to/file.txt
b2 rm --recursive --versions my-bucket path/to/folder/
```

### Sync Operations

```bash
b2 sync /local/path b2://my-bucket/prefix/
b2 sync b2://my-bucket/prefix/ /local/path

b2 sync /local/path b2://my-bucket/ \
  --threads 20 --delete --keep-days 30 --exclude-regex ".*\.tmp$"
```

## Terraform Provider

### Provider Setup

```hcl
terraform {
  required_providers {
    b2 = {
      source  = "Backblaze/b2"
      version = "~> 0.8"
    }
  }
}

provider "b2" {
  # Uses B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY env vars
}
```

### Bucket Resource

```hcl
resource "b2_bucket" "storage" {
  bucket_name = "my-app-storage"
  bucket_type = "allPrivate"

  bucket_info = {
    environment = "production"
    application = "my-app"
  }

  lifecycle_rules {
    file_name_prefix              = "logs/"
    days_from_hiding_to_deleting  = 30
    days_from_uploading_to_hiding = 90
  }

  lifecycle_rules {
    file_name_prefix              = "temp/"
    days_from_hiding_to_deleting  = 1
    days_from_uploading_to_hiding = 7
  }
}

output "bucket_id" {
  value = b2_bucket.storage.bucket_id
}
```

### Bucket with CORS

```hcl
resource "b2_bucket" "web_assets" {
  bucket_name = "my-web-assets"
  bucket_type = "allPublic"

  cors_rules {
    cors_rule_name   = "allowWebApp"
    allowed_origins  = ["https://myapp.com", "https://www.myapp.com"]
    allowed_headers  = ["*"]
    allowed_operations = ["s3_get", "s3_head"]
    expose_headers   = ["x-bz-content-sha1"]
    max_age_seconds  = 3600
  }
}
```

### Bucket with Encryption

```hcl
resource "b2_bucket" "encrypted" {
  bucket_name = "my-encrypted-bucket"
  bucket_type = "allPrivate"

  default_server_side_encryption {
    mode      = "SSE-B2"
    algorithm = "AES256"
  }
}
```

### Bucket with File Lock (Immutable)

```hcl
resource "b2_bucket" "compliance" {
  bucket_name = "compliance-records"
  bucket_type = "allPrivate"

  file_lock_configuration {
    is_file_lock_enabled = true

    default_retention {
      mode = "governance"
      period {
        duration = 365
        unit     = "days"
      }
    }
  }
}
```

### Application Key Resource

```hcl
resource "b2_application_key" "app" {
  key_name     = "my-app-key"
  capabilities = ["listBuckets", "listFiles", "readFiles", "writeFiles"]
  bucket_id    = b2_bucket.storage.bucket_id
  name_prefix  = "uploads/"
}

output "application_key_id" {
  value = b2_application_key.app.application_key_id
}

output "application_key" {
  value     = b2_application_key.app.application_key
  sensitive = true
}
```

### Data Sources

```hcl
data "b2_account_info" "current" {}

output "account_id" {
  value = data.b2_account_info.current.account_id
}

data "b2_bucket" "existing" {
  bucket_name = "my-existing-bucket"
}

output "bucket_id" {
  value = data.b2_bucket.existing.bucket_id
}
```

### Upload File

```hcl
resource "b2_bucket_file" "config" {
  bucket_id    = b2_bucket.storage.bucket_id
  file_name    = "config/settings.json"
  source       = "${path.module}/files/settings.json"
  content_type = "application/json"
}

resource "b2_bucket_file" "data" {
  bucket_id = b2_bucket.storage.bucket_id
  file_name = "data/export.csv"
  source    = "${path.module}/files/export.csv"

  file_info = {
    exported_at = timestamp()
    version     = "1.0"
  }
}
```

## S3-Compatible API

Endpoint format: `s3.<region>.backblazeb2.com` (e.g., `us-west-004`, `eu-central-003`)

### AWS CLI

```ini
# ~/.aws/config
[profile backblaze]
region = us-west-004
output = json

# ~/.aws/credentials - use B2 applicationKeyId / applicationKey
[backblaze]
aws_access_key_id = your-key-id
aws_secret_access_key = your-application-key
```

```bash
aws --profile backblaze --endpoint-url https://s3.us-west-004.backblazeb2.com s3 ls
aws --profile backblaze --endpoint-url https://s3.us-west-004.backblazeb2.com \
  s3 sync /local/path s3://my-bucket/prefix/
```

### Rclone

```ini
# ~/.config/rclone/rclone.conf
[backblaze]
type = b2
account = your-key-id
key = your-application-key
endpoint = s3.us-west-004.backblazeb2.com
```

```bash
rclone sync /local/path backblaze:my-bucket/prefix/
rclone copy -P /local/path backblaze:my-bucket/
```

## Makefile Automation

```makefile
.PHONY: b2-sync-up b2-sync-down b2-backup

B2_BUCKET ?= my-bucket
B2_PREFIX ?= data/
LOCAL_PATH ?= ./data

b2-sync-up:
	b2 sync --threads 20 $(LOCAL_PATH) b2://$(B2_BUCKET)/$(B2_PREFIX)

b2-sync-down:
	b2 sync --threads 20 b2://$(B2_BUCKET)/$(B2_PREFIX) $(LOCAL_PATH)

b2-backup:
	b2 sync --threads 20 --keep-days 30 \
		$(LOCAL_PATH) b2://$(B2_BUCKET)/backups/$(shell date +%Y-%m-%d)/
```

## References

- [references/b2-cli-setup.md](references/b2-cli-setup.md) - CLI installation and authentication
- [references/b2-key-capabilities.md](references/b2-key-capabilities.md) - Application key capabilities and sync flags
- [references/production-setup.md](references/production-setup.md) - Complete production setup
