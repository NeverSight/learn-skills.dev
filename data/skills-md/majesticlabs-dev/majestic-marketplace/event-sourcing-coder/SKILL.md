---
name: event-sourcing-coder
description: Record domain events and dispatch to inbox handlers for side effects, audit trails, and activity feeds. Use when building activity logs, syncing external services, or decoupling event creation from processing. Triggers on event recording, audit trails, activity feeds, or inbox patterns.
---

# Event Sourcing for Rails Monoliths

Record significant domain events and dispatch them to specialized handlers - a pragmatic approach to event sourcing without the complexity of full CQRS/ES infrastructure.

## When to Use This Skill

- Building activity feeds or audit trails
- Syncing data to external services (CRMs, analytics, webhooks)
- Automating workflows triggered by domain events
- Decoupling "what happened" from "what to do about it"
- Tracking user actions for analytics or debugging

## When NOT to Use Events

| Scenario | Better Alternative |
|----------|-------------------|
| Simple callbacks on single model | ActiveRecord callbacks |
| Synchronous side effects only | Service objects or ActiveInteraction |
| Need full event replay/rebuilding | Dedicated event sourcing gem (Rails Event Store) |
| Single handler per event | Direct method calls |

## Core Concept

**Decouple recording from processing:**

```
User action → Record Event → Broadcast to Inboxes → Side Effects
                  ↓
              Queryable
              (audit trail)
```

## Setup

### Migration

```ruby
class CreateIssueEvents < ActiveRecord::Migration[8.0]
  def change
    create_table :issue_events do |t|
      t.references :issue, null: false, foreign_key: true
      t.references :actor, null: false, foreign_key: { to_table: :users }
      t.string :action, null: false
      t.jsonb :metadata, default: {}
      t.timestamps
    end

    add_index :issue_events, :action
    add_index :issue_events, :created_at
  end
end
```

### Event Model

```ruby
# app/models/issue/event.rb
module Issue::Event
  extend ActiveSupport::Concern

  ACTIONS = %w[
    created
    assigned
    status_changed
    commented
    closed
    reopened
  ].freeze

  included do
    belongs_to :issue
    belongs_to :actor, class_name: "User"

    validates :action, presence: true, inclusion: { in: ACTIONS }

    after_commit :broadcast_to_inboxes, on: :create
  end

  private

  def broadcast_to_inboxes
    Issue::Event::BroadcastJob.perform_later(self)
  end
end

class Issue::Event < ApplicationRecord
  include Issue::Event
end
```

### Recording Events

```ruby
# app/models/issue.rb
class Issue < ApplicationRecord
  has_many :events, class_name: "Issue::Event", dependent: :destroy

  def record_event!(action:, actor:, metadata: {}, throttle: nil)
    return if throttle && recently_recorded?(action, throttle)

    events.create!(
      action: action,
      actor: actor,
      metadata: metadata
    )
  end

  private

  def recently_recorded?(action, duration)
    events.where(action: action)
          .where("created_at > ?", duration.ago)
          .exists?
  end
end
```

### Usage in Application

```ruby
# In a controller or interaction
issue.record_event!(
  action: "status_changed",
  actor: current_user,
  metadata: { from: "open", to: "in_progress" }
)

# With throttling (prevent duplicate events within timeframe)
issue.record_event!(
  action: "viewed",
  actor: current_user,
  throttle: 5.minutes
)
```

## The Inbox Pattern

Inboxes are specialized handlers that decide whether to process each event type.

### Broadcast Job

```ruby
# app/jobs/issue/event/broadcast_job.rb
class Issue::Event::BroadcastJob < ApplicationJob
  queue_as :events

  INBOXES = [
    Issue::Event::Inboxes::EmailNotifications,
    Issue::Event::Inboxes::SlackNotifications,
    Issue::Event::Inboxes::ExternalSync,
    Issue::Event::Inboxes::AutomationRules
  ].freeze

  def perform(event)
    INBOXES.each do |inbox_class|
      inbox_class.new(event).process
    end
  end
end
```

### Inbox Base Class

```ruby
# app/models/issue/event/inboxes/base.rb
module Issue::Event::Inboxes
  class Base
    attr_reader :event

    delegate :issue, :actor, :action, :metadata, to: :event

    def initialize(event)
      @event = event
    end

    def process
      return unless should_process?

      handle
    end

    private

    def should_process?
      raise NotImplementedError
    end

    def handle
      raise NotImplementedError
    end
  end
end
```

### Example Inbox: Email Notifications

```ruby
# app/models/issue/event/inboxes/email_notifications.rb
module Issue::Event::Inboxes
  class EmailNotifications < Base
    NOTIFY_ACTIONS = %w[assigned commented status_changed].freeze

    private

    def should_process?
      action.in?(NOTIFY_ACTIONS) && recipients.any?
    end

    def handle
      recipients.each do |user|
        IssueMailer.event_notification(
          user: user,
          issue: issue,
          event: event
        ).deliver_later
      end
    end

    def recipients
      @recipients ||= issue.subscribers.where.not(id: actor.id)
    end
  end
end
```

### Example Inbox: External Sync

```ruby
# app/models/issue/event/inboxes/external_sync.rb
module Issue::Event::Inboxes
  class ExternalSync < Base
    SYNC_ACTIONS = %w[created status_changed closed].freeze

    private

    def should_process?
      action.in?(SYNC_ACTIONS) && issue.external_id.present?
    end

    def handle
      ExternalService::SyncIssueJob.perform_later(
        issue_id: issue.id,
        action: action,
        metadata: metadata
      )
    end
  end
end
```

## Activity Feed

Events become queryable for activity feeds:

```ruby
# Recent activity on an issue
issue.events.includes(:actor).order(created_at: :desc).limit(20)

# User's recent activity across all issues
Issue::Event.where(actor: current_user)
            .includes(:issue)
            .order(created_at: :desc)
            .limit(50)

# Activity feed component
class Issue::ActivityFeedComponent < ViewComponent::Base
  def initialize(issue:)
    @events = issue.events.includes(:actor).order(created_at: :desc)
  end
end
```

## Integration with State Machines

Combine with AASM for automatic event recording:

```ruby
class Issue < ApplicationRecord
  include AASM

  aasm column: :status do
    state :open, initial: true
    state :in_progress
    state :resolved
    state :closed

    event :start do
      transitions from: :open, to: :in_progress
      after { record_status_change("open", "in_progress") }
    end

    event :resolve do
      transitions from: :in_progress, to: :resolved
      after { record_status_change("in_progress", "resolved") }
    end
  end

  private

  def record_status_change(from, to)
    record_event!(
      action: "status_changed",
      actor: Current.user,
      metadata: { from: from, to: to }
    )
  end
end
```

## Testing

### Testing Event Recording

```ruby
RSpec.describe Issue do
  describe "#record_event!" do
    let(:issue) { create(:issue) }
    let(:user) { create(:user) }

    it "creates an event" do
      expect {
        issue.record_event!(action: "commented", actor: user)
      }.to change(issue.events, :count).by(1)
    end

    it "stores metadata" do
      issue.record_event!(
        action: "status_changed",
        actor: user,
        metadata: { from: "open", to: "closed" }
      )

      expect(issue.events.last.metadata).to eq(
        "from" => "open",
        "to" => "closed"
      )
    end

    context "with throttling" do
      it "prevents duplicate events within timeframe" do
        issue.record_event!(action: "viewed", actor: user)

        expect {
          issue.record_event!(action: "viewed", actor: user, throttle: 5.minutes)
        }.not_to change(issue.events, :count)
      end
    end
  end
end
```

### Testing Inboxes

```ruby
RSpec.describe Issue::Event::Inboxes::EmailNotifications do
  let(:event) { create(:issue_event, action: "assigned") }
  let(:inbox) { described_class.new(event) }

  describe "#process" do
    context "when issue has subscribers" do
      before { create(:subscription, issue: event.issue) }

      it "sends notification emails" do
        expect { inbox.process }
          .to have_enqueued_mail(IssueMailer, :event_notification)
      end
    end

    context "when action is not notifiable" do
      let(:event) { create(:issue_event, action: "viewed") }

      it "does not send emails" do
        expect { inbox.process }
          .not_to have_enqueued_mail(IssueMailer)
      end
    end
  end
end
```

## Best Practices

### Keep Events Immutable

```ruby
# Good: Events are append-only facts
issue.record_event!(action: "status_changed", ...)

# Avoid: Never update or delete events
event.update!(action: "different")  # Don't do this
```

### Use Meaningful Action Names

```ruby
# Good: Verb in past tense, describes what happened
ACTIONS = %w[created assigned commented resolved closed reopened]

# Avoid: Vague or present-tense actions
ACTIONS = %w[update change action do_thing]
```

### Store Context in Metadata

```ruby
# Good: Capture context at event time
record_event!(
  action: "status_changed",
  actor: current_user,
  metadata: {
    from: previous_status,
    to: new_status,
    reason: params[:reason],
    triggered_by: "manual"  # vs "automation"
  }
)

# Avoid: Relying on current state (it changes)
record_event!(action: "status_changed", actor: current_user)
# Later: "What was the previous status?" - Unknown!
```

### Process Events Asynchronously

```ruby
# Good: Inboxes process in background jobs
after_commit :broadcast_to_inboxes, on: :create

def broadcast_to_inboxes
  BroadcastJob.perform_later(self)
end

# Avoid: Synchronous processing blocks the request
after_create :process_all_inboxes  # Slow!
```

## Detailed References

For advanced patterns:
- `references/event-model.md` - Polymorphic events, custom types, concerns
- `references/inbox-pattern.md` - Inbox composition, error handling, retries
- `references/use-cases.md` - Activity feeds, webhooks, automation rules
