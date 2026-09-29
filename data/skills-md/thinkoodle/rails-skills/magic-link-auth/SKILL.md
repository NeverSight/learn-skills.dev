---
name: magic-link-auth
description: Expert guidance for passwordless email-code authentication in Rails — the 37signals token/code pattern used by Basecamp, Fizzy, and apps like Herald. Use when adding sign-in, sign-up, magic links, one-time codes, OTP, verification codes, session tokens, pending authentication tokens, personal access tokens, Bearer API auth, passwordless login, or replacing Devise/has_secure_password. Do not use the Rails 8 password generator for this flow.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails generate*), Bash(bin/rails db:*), Bash(bin/rails test:*), Bash(bin/rails test)
---

# Magic Link / Token-Code Auth

Passwordless Rails auth: the human types a short **code** from email; the browser/API holds **tokens**. This is the Basecamp/Fizzy pattern (also used in Herald). It is not `bin/rails generate authentication` and not Devise.

## Philosophy

1. **Codes are for humans, tokens are for machines.** Mixing them is the #1 implementation bug.
2. **Same response whether the email exists or not.** Enumeration via "no account found" is a hole.
3. **Bind the code step to the email that requested it.** A code for alice@ must not sign in bob@ just because the attacker typed it.
4. **Consume codes. Destroy sessions.** Reuse is a bug; logout must actually log out.
5. **Identity authenticates. User belongs to a tenant.** Don't hang sessions on the tenant membership record.

## The Four Secrets

| Name | Who holds it | Lifetime | Shape |
|------|----------------|----------|--------|
| **Code** | Human, via email | ~15 minutes, one-time | 6 Crockford base32 chars |
| **Pending authentication token** | Cookie (and JSON body for native apps) | Same as the code | Message verifier of the email |
| **Session token** | Signed cookie | Until the Session row is destroyed | `session.signed_id` |
| **Access token** (optional) | `Authorization: Bearer` | Until revoked | `has_secure_token` |

Do not invent a fifth. Do not store the session token as a custom random column unless you already did — Fizzy uses Active Record `signed_id` and no `sessions.token` column.

## Flow

```
POST /session          email
  → find identity (or fake it)
  → create MagicLink, email the code
  → set pending_authentication_token cookie
  → redirect to code form

POST /session/magic_link   code
  → MagicLink.consume(code)
  → secure_compare pending email vs identity email
  → Session.create! + session_token cookie
  → clear pending token

Later requests
  → Session.find_signed(cookies.signed[:session_token])
  → or Bearer access token
```

Native apps do the same two POSTs as JSON and send the pending token back as a cookie. See [reference.md](reference.md) for the API contract.

## Step 1: Check What Exists

```bash
ls app/models/identity.rb app/models/magic_link.rb app/models/session.rb
ls app/controllers/concerns/authentication.rb
rg "has_secure_password|devise|generate authentication" app/ config/
```

If the app already has this pattern, extend it — don't bolt on Devise or the Rails 8 password generator.

## Step 2: Models

**Identity** is the person. Email is unique, normalized, and the only login identifier.

```ruby
class Identity < ApplicationRecord
  has_many :magic_links, dependent: :destroy
  has_many :sessions, dependent: :destroy
  has_many :access_tokens, dependent: :destroy

  validates :email_address, format: { with: URI::MailTo::EMAIL_REGEXP }
  normalizes :email_address, with: ->(value) { value.strip.downcase.presence }

  def send_magic_link(**attributes)
    attributes[:purpose] = attributes.delete(:for) if attributes.key?(:for)

    magic_links.create!(attributes).tap do |magic_link|
      MagicLinkMailer.sign_in_instructions(magic_link).deliver_later
    end
  end
end
```

**MagicLink** is the code. Unique, expiring, consumed by destroy.

```ruby
class MagicLink < ApplicationRecord
  CODE_LENGTH = 6
  EXPIRATION_TIME = 15.minutes

  belongs_to :identity
  enum :purpose, %w[ sign_in sign_up ], prefix: :for, default: :sign_in

  scope :active, -> { where(expires_at: Time.current...) }
  scope :stale,  -> { where(expires_at: ..Time.current) }

  before_validation :generate_code, on: :create
  before_validation :set_expiration, on: :create
  validates :code, uniqueness: true, presence: true

  def self.consume(code)
    active.find_by(code: Code.sanitize(code))&.consume
  end

  def self.cleanup
    stale.delete_all
  end

  def consume
    destroy
    self
  end

  private
    def generate_code
      self.code ||= loop do
        candidate = MagicLink::Code.generate(CODE_LENGTH)
        break candidate unless self.class.exists?(code: candidate)
      end
    end

    def set_expiration
      self.expires_at ||= EXPIRATION_TIME.from_now
    end
end
```

**Code sanitization** — people type O/0 and I/L/1 interchangeably. Sanitize on consume, not on generate.

```ruby
module MagicLink::Code
  CODE_SUBSTITUTIONS = { "O" => "0", "I" => "1", "L" => "1" }.freeze

  def self.generate(length)
    SecureRandom.base32(length)
  end

  def self.sanitize(code)
    return if code.blank?

    code.to_s.upcase
      .then { |c| CODE_SUBSTITUTIONS.reduce(c) { |result, (from, to)| result.gsub(from, to) } }
      .gsub(/[^#{SecureRandom::BASE32_ALPHABET.join}]/, "")
  end
end
```

**Session** is the logged-in browser/app. No token column.

```ruby
class Session < ApplicationRecord
  belongs_to :identity
end
```

Cookie value is `session.signed_id`. Lookup is `Session.find_signed(cookies.signed[:session_token])`. Destroy the row to log that device out.

## Step 3: Migrations

```ruby
create_table :identities, id: :uuid do |t|
  t.string :email_address, null: false
  t.timestamps
end
add_index :identities, :email_address, unique: true

create_table :magic_links, id: :uuid do |t|
  t.references :identity, type: :uuid, null: false, foreign_key: true
  t.string :code, null: false
  t.integer :purpose, null: false, default: 0
  t.datetime :expires_at, null: false
  t.timestamps
end
add_index :magic_links, :code, unique: true
add_index :magic_links, :expires_at

create_table :sessions, id: :uuid do |t|
  t.references :identity, type: :uuid, null: false, foreign_key: true
  t.string :user_agent
  t.string :ip_address
  t.timestamps
end
```

Use `expires_at` (indexed, cleanable). Do not derive expiry only from `created_at`. Do not keep consumed codes around with `consumed_at` unless you need an audit trail — Fizzy destroys them.

## Step 4: Authentication Concern

Resume the session on every request. Require it by default. The sign-in controllers opt out.

```ruby
module Authentication
  extend ActiveSupport::Concern

  included do
    before_action :require_authentication
    helper_method :authenticated?, :email_address_pending_authentication
    include Authentication::ViaMagicLink
  end

  class_methods do
    def require_unauthenticated_access(**options)
      skip_before_action :require_authentication, **options
      before_action :resume_session, **options
      before_action :redirect_authenticated_user, **options
    end
  end

  private
    def authenticated?
      Current.identity.present?
    end

    def require_authentication
      resume_session || authenticate_by_bearer_token || request_authentication
    end

    def resume_session
      if session = find_session_by_cookie
        set_current_session session
      end
    end

    def find_session_by_cookie
      Session.find_signed(cookies.signed[:session_token])
    end

    def authenticate_by_bearer_token
      return unless request.authorization.to_s.include?("Bearer")

      authenticate_or_request_with_http_token do |token|
        if identity = Identity.find_by_permissible_access_token(token, method: request.method)
          Current.identity = identity
        end
      end
    end

    def request_authentication
      session[:return_to_after_authenticating] = request.url
      redirect_to new_session_path
    end

    def start_new_session_for(identity)
      identity.sessions.create!(user_agent: request.user_agent, ip_address: request.remote_ip).tap do |session|
        set_current_session session
      end
    end

    def set_current_session(session)
      Current.session = session
      cookies.signed.permanent[:session_token] = {
        value: session.signed_id, httponly: true, same_site: :lax
      }
    end

    def terminate_session
      Current.session.destroy
      cookies.delete(:session_token)
    end

    def redirect_authenticated_user
      redirect_to root_path if authenticated?
    end
end
```

`Current.session=` should also set `Current.identity`. See [reference.md](reference.md) for Current, Bearer lookup, and access-token show-once.

## Step 5: Pending Token + Enumeration Cover

The pending token is a **message verifier**, not a database row. It stores the email and expires with the code. The code form never takes an email param.

```ruby
module Authentication::ViaMagicLink
  extend ActiveSupport::Concern

  included do
    after_action :ensure_development_magic_link_not_leaked
  end

  private
    def redirect_to_fake_session_magic_link(email_address)
      fake = MagicLink.new(
        identity: Identity.new(email_address: email_address),
        code: SecureRandom.base32(6),
        expires_at: MagicLink::EXPIRATION_TIME.from_now
      )
      redirect_to_session_magic_link fake
    end

    def redirect_to_session_magic_link(magic_link)
      serve_development_magic_link(magic_link)
      set_pending_authentication_token(magic_link)

      respond_to do |format|
        format.html { redirect_to session_magic_link_path }
        format.json { render json: { pending_authentication_token: pending_authentication_token }, status: :created }
      end
    end

    def set_pending_authentication_token(magic_link)
      cookies[:pending_authentication_token] = {
        value: pending_authentication_token_verifier.generate(
          magic_link.identity.email_address, expires_at: magic_link.expires_at
        ),
        httponly: true, same_site: :lax, expires: magic_link.expires_at
      }
    end

    def email_address_pending_authentication
      pending_authentication_token_verifier.verified(pending_authentication_token)
    end

    def pending_authentication_token_verifier
      Rails.application.message_verifier(:pending_authentication)
    end

    def pending_authentication_token
      cookies[:pending_authentication_token]
    end

    def clear_pending_authentication_token
      cookies.delete(:pending_authentication_token)
    end

    def serve_development_magic_link(magic_link)
      if Rails.env.development? && magic_link.present?
        flash[:magic_link_code] = magic_link.code
        response.set_header("X-Magic-Link-Code", magic_link.code)
      end
    end

    def ensure_development_magic_link_not_leaked
      unless Rails.env.development?
        raise "Leaking magic link via flash in #{Rails.env}?" if flash[:magic_link_code].present?
      end
    end
end
```

Unknown emails go through `redirect_to_fake_session_magic_link`. Same redirect, same pending cookie, no email sent, no Identity created.

## Step 6: Controllers

Rate-limit **both** steps. Code brute force is the real attack.

```ruby
class SessionsController < ApplicationController
  require_unauthenticated_access except: :destroy
  rate_limit to: 10, within: 3.minutes, only: :create, with: :rate_limit_exceeded

  def create
    if identity = Identity.find_by(email_address: email_address)
      redirect_to_session_magic_link identity.send_magic_link
    else
      redirect_to_fake_session_magic_link email_address
    end
  end

  def destroy
    terminate_session
    redirect_to new_session_path
  end

  private
    def email_address
      params.expect(:email_address)
    end
end
```

```ruby
class Sessions::MagicLinksController < ApplicationController
  require_unauthenticated_access
  rate_limit to: 10, within: 15.minutes, only: :create, with: :rate_limit_exceeded
  before_action :ensure_pending_email

  def create
    if magic_link = MagicLink.consume(code)
      authenticate(magic_link)
    else
      redirect_to session_magic_link_path, flash: { shake: true }
    end
  end

  private
    def authenticate(magic_link)
      if ActiveSupport::SecurityUtils.secure_compare(
        email_address_pending_authentication || "", magic_link.identity.email_address
      )
        clear_pending_authentication_token
        start_new_session_for magic_link.identity
        redirect_to after_authentication_url
      else
        clear_pending_authentication_token
        redirect_to new_session_path, alert: "Something went wrong. Please try again."
      end
    end

    def code
      params.expect(:code)
    end
end
```

Wrong code: stay on the form, don't say why. Cross-user code: kill the pending token and start over. Never create a session for a code that doesn't match the pending email.

Open signup: `find_or_create_by!` then `send_magic_link(for: :sign_up)`, and send the new user to a completion step (name, account) **after** the code — not before. Closed signup: fake path, no identity.

## Step 7: Routes, Mailer, View, Logging

```ruby
resource :session do
  scope module: :sessions do
    resource :magic_link, only: %i[show create]
  end
end
```

Put the code in the **subject** so it is readable from a notification: `"Your App code is #{magic_link.code}"`. Body repeats it large. Mention the 15-minute window.

Code field: `autocomplete: "one-time-code"`, `maxlength: 6`, submit on Enter and paste. Show the pending email on the page so the user knows where it went. In development only, flash the code.

```ruby
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += %i[ passw secret token _key crypt salt otp code ]
```

Schedule `MagicLink.cleanup` (Solid Queue recurring, or a rake task). Stale rows are expired codes that were never used.

## Tests That Must Exist

Sign in by posting the real flow, not by stuffing `Current`:

```ruby
def sign_in_as(identity)
  identity.send_magic_link
  post session_path, params: { email_address: identity.email_address }
  post session_magic_link_path, params: { code: identity.magic_links.last.code }
end
```

Cover: valid code sets `session_token` and destroys the MagicLink; invalid/expired code does not; code for a different email does not; unknown email still renders the code form; missing pending token redirects to sign-in; rate limit; development flash is absent in test/production.

## Anti-Patterns

1. **Email as a query param on the verify form** — skip the pending token and anyone with a code can attach any email. Fizzy binds via the verifier cookie.
2. **`find_or_create_by` on every sign-in** — creates identities for attackers' throwaway emails. Only create on an explicit sign-up path.
3. **Telling the user the email doesn't exist** — use the fake magic-link redirect.
4. **Numeric 6-digit codes without extra controls** — 1e6 space, brute-forceable without tight rate limits. Prefer base32 (32^6) plus rate limits.
5. **`has_secure_password` + this flow** — two auth systems. Pick one.
6. **Storing the session token in the Rails session cookie store** — the Session row is the source of truth so you can revoke a device.
7. **Showing an access token more than once** — generate, display via a short-lived signed id, never again.
8. **Skipping `secure_compare` on the pending email** — use `ActiveSupport::SecurityUtils.secure_compare`.
9. **Leaving codes in the DB after use** — consume by `destroy` (or `consumed_at` if you must audit).
10. **Flashing the code outside development** — the after_action raise exists because this will happen.

## Reference

See [reference.md](reference.md) for Identity vs User (also the `identity-membership` skill), Herald/Mosaic variants, JSON/native-app contract, personal access tokens, Current attributes, and test helpers.
