---
name: action-mailer-coder
description: Use when creating or refactoring Action Mailer emails. Applies Rails 7.1+ conventions, parameterized mailers, preview workflows, background delivery, and email design best practices.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Action Mailer Coder

## Mailer Design Principles

### Group Related Emails

```ruby
class NotificationMailer < ApplicationMailer
  def comment_reply(user, comment)
    @user = user
    @comment = comment
    mail(to: @user.email, subject: "New reply to your comment")
  end

  def mentioned(user, mention)
    @user = user
    @mention = mention
    mail(to: @user.email, subject: "You were mentioned")
  end
end
```

### Parameterized Mailers

```ruby
class NotificationMailer < ApplicationMailer
  before_action { @user = params.fetch(:user) }
  before_action { @account = params.fetch(:account) }

  def comment_reply
    @comment = params.fetch(:comment)
    mail(to: @user.email, subject: "New reply on #{@account.name}")
  end
end

# Calling the mailer
NotificationMailer.with(user: user, account: account, comment: comment).comment_reply.deliver_later
```

### Dynamic Defaults with Inheritance

```ruby
class AccountMailer < ApplicationMailer
  default from: -> { build_from_address }
  before_action { @account = params.fetch(:account) }

  private

  def build_from_address
    @account.custom_email_sender? ?
      email_address_with_name(@account.custom_email_address, @account.custom_email_name) :
      email_address_with_name("hello@example.com", @account.name)
  end
end
```

## Background Delivery

```ruby
UserMailer.with(user: user).welcome.deliver_later                    # Immediate queue
UserMailer.with(user: user).welcome.deliver_later(wait: 1.hour)      # Delayed
UserMailer.with(user: user).digest.deliver_later(wait_until: Date.tomorrow.morning)  # Scheduled
```

## Email Previews

```ruby
# test/mailers/previews/notification_mailer_preview.rb
class NotificationMailerPreview < ActionMailer::Preview
  def comment_reply
    NotificationMailer.with(
      user: User.first,
      account: Account.first,
      comment: Comment.first
    ).comment_reply
  end
end
```

Access at: `http://localhost:3000/rails/mailers`

## Internationalization

```ruby
def welcome
  @user = params.fetch(:user)
  I18n.with_locale(@user.locale) do
    mail(to: @user.email, subject: t(".subject", name: @user.name))
  end
end
```

## Attachments

```ruby
def invoice(order)
  attachments.inline["logo.png"] = File.read("app/assets/images/logo.png")
  attachments["invoice.pdf"] = generate_pdf(order)
  mail(to: order.email, subject: "Your Invoice ##{order.number}")
end
```

## Testing (RSpec)

```ruby
RSpec.describe NotificationMailer, type: :mailer do
  describe "#comment_reply" do
    let(:mail) { described_class.with(user: user, comment: comment).comment_reply }

    it "renders the headers" do
      expect(mail.subject).to match(/New reply/)
      expect(mail.to).to eq([user.email])
    end

    it "delivers later" do
      expect { mail.deliver_later }.to have_enqueued_job(ActionMailer::MailDeliveryJob)
    end
  end
end
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| One mailer per email | Hard to navigate | Group related emails |
| Skipping `.with()` | Implicit dependencies | Use parameterized mailers |
| `deliver_now` | Blocks request | Use `deliver_later` |
| Missing previews | Can't visually test | Create preview classes |

## Output Format

When creating mailers, provide:

1. **Mailer Class** - The complete implementation
2. **Views** - HTML and text templates
3. **Preview** - Preview class for visual testing
4. **Tests** - Example test cases
