---
name: outgoing-webhooks
description: Expert guidance for delivering signed HTTP webhooks from a Rails app to customer URLs. Use when adding webhooks, HMAC signatures, SSRF protection, webhook deliveries, auto-disable on failure, or posting events to Slack/customer endpoints. Covers Fizzy and Herald delivery. Not inbound Stripe/GitHub webhooks.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails generate*), Bash(bin/rails db:*), Bash(bin/rails test:*), Bash(bin/rails test)
---

# Outgoing Webhooks

Customer-supplied URLs you POST to when something happens. Treat the URL as attacker-controlled. Sign the body. Pin DNS to a public IP. Never let a broken subscriber block the action that triggered the event.

Inbound webhooks (Stripe, GitHub) are the opposite direction — don't use this skill for those.

## Philosophy

1. **SSRF first.** Resolve the host, reject private/loopback/link-local, then `http.ipaddr =` that address so a TTL=0 DNS rebind can't send you to 169.254.169.254.
2. **HMAC the payload.** Show the secret once. Header like `X-Webhook-Signature: sha256=...`.
3. **Delivery is a job with a log row.** The user-facing action commits, then `perform_later`. Failures retry; they don't roll back the event.
4. **Auto-disable after a streak of failures.** Don't hammer a dead endpoint forever.

## Records

```ruby
class Webhook < ApplicationRecord  # tenanted, or board-scoped in Fizzy
  has_secure_token :signing_secret  # or "whsec_#{SecureRandom.urlsafe_base64(32)}"
  has_many :deliveries, dependent: :destroy

  validates :url, presence: true
  validate :url_is_deliverable
end

class WebhookDelivery < ApplicationRecord
  belongs_to :webhook
  # payload, event, attempts, delivering_at, delivered_at, failed_at,
  # response_status, error_message, signature
end
```

In `activerecord-tenanted` apps, Webhook lives in the tenant DB. The job receives a **global** handle (project slug, tenant key) plus `delivery_id`, then `with_tenant`.

## Step 1: SSRF

```ruby
module SsrfProtection
  DISALLOWED = [
    IPAddr.new("0.0.0.0/8"),
    IPAddr.new("10.0.0.0/8"),
    IPAddr.new("100.64.0.0/10"),
    IPAddr.new("127.0.0.0/8"),
    IPAddr.new("169.254.0.0/16"),
    IPAddr.new("172.16.0.0/12"),
    IPAddr.new("192.168.0.0/16"),
    IPAddr.new("198.18.0.0/15"),
    IPAddr.new("::1/128"),
    IPAddr.new("fc00::/7"),
    IPAddr.new("fe80::/10")
  ].freeze

  def self.public_ip(host)
    addrs = Resolv.getaddresses(host.to_s).map { |a| IPAddr.new(a) }
    addrs.find { |ip| DISALLOWED.none? { |net| net.include?(ip.native) } && !ip.loopback? && !ip.private? && !ip.link_local? }
  rescue Resolv::ResolvError, ArgumentError
    nil
  end
end
```

Validate on create **and** at delivery time (DNS can change). Production only for the hard block if you need localhost webhooks in dev — Herald does that. Fizzy always pins.

```ruby
http = Net::HTTP.new(uri.host, uri.port)
http.ipaddr = public_ip.to_s
http.open_timeout = 10
http.read_timeout = 10
http.use_ssl = uri.scheme == "https"
```

Only `http`/`https`. Cap response body (Fizzy: 100 KB) so a subscriber can't fill your disk.

## Step 2: Sign

```ruby
def sign(payload)
  "sha256=#{OpenSSL::HMAC.hexdigest("SHA256", signing_secret, payload)}"
end
```

Sign the **exact bytes** you send (`request.body`). Store the signature on the delivery row so retries don't re-hash a mutated payload. Filter `secret` / `token` from logs.

Show the secret once (same trick as API tokens: short-lived signed id on the show URL). Rotating `regenerate_secret!` is a first-class action.

## Step 3: Fire after commit

```ruby
# after the domain event is committed
delivery = webhook.deliveries.create!(event: "release.published", payload: payload.to_json)
DeliverWebhookJob.perform_later(project.slug, delivery.id)
```

Job:

- `with_tenant` first
- Claim the row (`delivering_at`) so two workers don't double-POST
- Re-check `webhook.enabled?` and plan entitlements
- Retry 5xx and timeouts (`retry_on`, polynomially_longer, ~5 attempts)
- 4xx is terminal
- After N consecutive terminal failures, disable the webhook

A failure in this job must not raise into `PublishReleaseJob`. Herald keeps publish and delivery on separate jobs for that reason.

## Step 4: Headers

```
Content-Type: application/json
User-Agent: App-Webhook/1.0
X-App-Event: release.published
X-App-Delivery: <delivery id>
X-App-Signature: sha256=...
```

Fizzy also sends `X-Webhook-Timestamp`. Receivers should verify HMAC, not trust the event name alone.

## Tests that catch real bugs

- `http://127.0.0.1/` and `http://169.254.169.254/` are rejected in production
- Signature header matches HMAC of the stored payload
- Tenanted job without `with_tenant` cannot find the webhook
- 10 failures auto-disable; a later success (after re-enable) resets the counter
- Publish still succeeds when the endpoint 500s

## Anti-Patterns

1. **`Net::HTTP.post_form(webhook.url)`** — no SSRF pin, no timeout, no signature.
2. **Allowing `localhost` in production** — that's the metadata-service exploit.
3. **Signing a Hash then `to_json` later** — key order will not match.
4. **Delivering inline in the request** — user waits on the subscriber.
5. **One job that publishes and fans out webhooks** — a bad URL retries the publish.
6. **Logging the signing secret or full payload** — `filter_parameters` + truncate response bodies.

## Related

- Tenanted jobs: `activerecord-tenanted`
- Event bus that triggers these (Fizzy): events live in the app; this skill is only delivery

See [reference.md](reference.md) for Fizzy vs Herald and the IP allow/deny list.
