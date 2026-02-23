---
name: active-interaction-coder
description: Implement typed business operations with ActiveInteraction. Covers input types, composition, controller patterns, and testing.
---

# ActiveInteraction Coder

Typed business operations as the structured alternative to service objects.

## Why ActiveInteraction Over Service Objects

| Service Objects | ActiveInteraction |
|-----------------|-------------------|
| No standard interface | Consistent `.run` / `.run!` |
| Manual type checking | Built-in type declarations |
| Manual validation | Standard Rails validations |
| Hard to compose | Native composition |
| Verbose boilerplate | Clean, self-documenting |

## Setup

```ruby
# Gemfile
gem "active_interaction", "~> 5.3"
```

## Simple Interaction

```ruby
# app/interactions/users/create.rb
module Users
  class Create < ActiveInteraction::Base
    # Typed inputs
    string :email
    string :name
    string :password, default: nil

    # Validations
    validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
    validates :name, presence: true

    # Main logic
    def execute
      user = User.create!(
        email: email,
        name: name,
        password: password || SecureRandom.alphanumeric(32)
      )

      UserMailer.welcome(user).deliver_later
      user  # Return value becomes outcome.result
    end
  end
end
```

## Running Interactions

```ruby
# In controller
def create
  outcome = Users::Create.run(
    email: params[:email],
    name: params[:name]
  )

  if outcome.valid?
    redirect_to outcome.result, notice: "User created"
  else
    @errors = outcome.errors
    render :new, status: :unprocessable_entity
  end
end

# With bang method (raises on error)
user = Users::Create.run!(email: "user@example.com", name: "John")
```

## Input Types

```ruby
class MyInteraction < ActiveInteraction::Base
  # Primitives
  string :name
  integer :age
  float :price
  boolean :active
  symbol :status

  # Date/Time
  date :birthday
  time :created_at
  date_time :scheduled_at

  # Complex types
  array :tags
  hash :metadata

  # Model instances
  object :user, class: User

  # Typed arrays
  array :emails, default: [] do
    string
  end

  # Optional with default
  string :optional_field, default: nil
  integer :count, default: 0
end
```

## Composing Interactions

```ruby
module Users
  class Register < ActiveInteraction::Base
    string :email, :name, :password

    def execute
      # Compose calls another interaction
      user = compose(Users::Create,
        email: email,
        name: name,
        password: password
      )

      # Errors automatically merged if nested fails
      compose(Users::SendWelcomeEmail, user: user)
      user
    end
  end
end
```

## Controller Pattern

```ruby
class ArticlesController < ApplicationController
  def create
    outcome = Articles::Create.run(
      title: params[:article][:title],
      body: params[:article][:body],
      author: current_user
    )

    if outcome.valid?
      redirect_to article_path(outcome.result), notice: "Article created"
    else
      @article = Article.new(article_params)
      @article.errors.merge!(outcome.errors)
      render :new, status: :unprocessable_entity
    end
  end
end
```

## Testing Interactions

```ruby
RSpec.describe Users::Create do
  let(:valid_params) { { email: "user@example.com", name: "John" } }

  it "creates user with valid inputs" do
    expect { described_class.run(valid_params) }
      .to change(User, :count).by(1)
  end

  it "returns valid outcome" do
    outcome = described_class.run(valid_params)
    expect(outcome).to be_valid
    expect(outcome.result).to be_a(User)
  end

  it "validates email format" do
    outcome = described_class.run(valid_params.merge(email: "invalid"))
    expect(outcome).not_to be_valid
    expect(outcome.errors[:email]).to be_present
  end
end
```

## Advanced Patterns

For composition, error handling, and custom types see:
- `references/active-interaction.md`
