---
name: store-model-coder
description: Wrap JSON-backed database columns with ActiveModel-like classes using store_model. Use when creating configuration objects, managing nested JSON attributes, or adding validations to JSON data. Triggers on JSON columns, store_model, typed JSON, configuration objects, or nested attributes.
---

# StoreModel: JSON-Backed ActiveRecord Attributes

Wrap JSON-backed database columns with ActiveModel-like classes for type safety, validations, and clean separation of concerns.

## When to Use This Skill

- Configuration objects with validated fields
- Nested attributes stored in JSON columns
- JSON data requiring type safety and ActiveModel behavior
- Separating JSON logic from parent ActiveRecord model

## When NOT to Use StoreModel

| Scenario | Better Alternative |
|----------|-------------------|
| Simple key-value settings | `ActiveRecord::Store` or `store_accessor` |
| Need database-level queries on JSON | Raw `jsonb` with PostgreSQL operators |
| Data needs relationships/joins | Normalize into separate tables |
| Truly simple JSON without validation | Plain JSON column access |

## Setup

```ruby
# Gemfile
gem "store_model", "~> 3.0"
```

## Basic Usage

### Define a StoreModel Class

```ruby
# app/models/configuration.rb
class Configuration
  include StoreModel::Model

  attribute :model, :string
  attribute :color, :string
  attribute :max_speed, :integer, default: 100

  validates :model, presence: true
  validates :max_speed, numericality: { greater_than: 0 }
end
```

### Register in ActiveRecord

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  attribute :configuration, Configuration.to_type
end
```

### Usage

```ruby
product = Product.new
product.configuration = { model: "rocket", color: "red" }
product.configuration.model  # => "rocket"
product.configuration.color = "blue"
product.save!

# Also accepts StoreModel instances
product.configuration = Configuration.new(model: "shuttle")
```

## Enums

```ruby
class Configuration
  include StoreModel::Model

  attribute :model, :string

  enum :status, %i[draft active archived], default: :draft

  # With custom values
  enum :priority, { low: 0, medium: 1, high: 2 }, default: :medium
end
```

```ruby
config = Configuration.new
config.status        # => "draft"
config.active?       # => false
config.active!       # Sets status to :active
config.status        # => "active"
```

## Validations

```ruby
class Address
  include StoreModel::Model

  attribute :street, :string
  attribute :city, :string
  attribute :zip, :string
  attribute :country, :string, default: "US"

  validates :street, :city, :zip, presence: true
  validates :zip, format: { with: /\A\d{5}(-\d{4})?\z/ }, if: -> { country == "US" }
end
```

### Merging Errors to Parent

```ruby
class User < ApplicationRecord
  attribute :address, Address.to_type

  validates :address, store_model: { merge_errors: true }
end

user = User.new(address: { street: "", city: "" })
user.valid?
user.errors.full_messages
# => ["Address street can't be blank", "Address city can't be blank", "Address zip can't be blank"]
```

## Nested Models

```ruby
class Coordinate
  include StoreModel::Model

  attribute :latitude, :float
  attribute :longitude, :float

  validates :latitude, :longitude, presence: true
end

class Location
  include StoreModel::Model

  attribute :name, :string
  attribute :coordinate, Coordinate.to_type

  validates :name, presence: true
  validates :coordinate, store_model: { merge_errors: true }
end
```

## Array of Models

```ruby
class LineItem
  include StoreModel::Model

  attribute :name, :string
  attribute :quantity, :integer, default: 1
  attribute :price_cents, :integer

  validates :name, :price_cents, presence: true
end

class Order < ApplicationRecord
  attribute :line_items, LineItem.to_array_type

  validates :line_items, store_model: { merge_array_errors: true }
end
```

```ruby
order = Order.new
order.line_items = [
  { name: "Widget", quantity: 2, price_cents: 1000 },
  { name: "Gadget", quantity: 1, price_cents: 2500 }
]
order.line_items.first.name  # => "Widget"
order.line_items.sum(&:price_cents)  # => 3500
```

## Dirty Tracking

StoreModel doesn't automatically detect nested changes. Use one of these approaches:

```ruby
# Option 1: Reassign the entire object
product.configuration = product.configuration.dup.tap { |c| c.color = "green" }

# Option 2: Mark as changed explicitly
product.configuration.color = "green"
product.configuration_will_change!
product.save!

# Option 3: Use attribute assignment
product.configuration = { **product.configuration.attributes, color: "green" }
```

## Controller Pattern

```ruby
class ProductsController < ApplicationController
  def create
    @product = Product.new(product_params)

    if @product.save
      redirect_to @product
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def product_params
    params.require(:product).permit(
      :name,
      configuration: [:model, :color, :max_speed, :status]
    )
  end
end
```

## Testing

```ruby
RSpec.describe Configuration do
  describe "validations" do
    it "requires model" do
      config = described_class.new(model: nil)
      expect(config).not_to be_valid
      expect(config.errors[:model]).to include("can't be blank")
    end
  end

  describe "enums" do
    it "defaults to draft status" do
      config = described_class.new
      expect(config).to be_draft
    end

    it "transitions status" do
      config = described_class.new
      config.active!
      expect(config).to be_active
    end
  end
end

RSpec.describe Product do
  describe "configuration" do
    it "accepts hash" do
      product = described_class.new(configuration: { model: "rocket" })
      expect(product.configuration.model).to eq("rocket")
    end

    it "merges validation errors" do
      product = described_class.new(configuration: { model: nil })
      expect(product).not_to be_valid
      expect(product.errors[:configuration]).to be_present
    end
  end
end
```

## Detailed References

For advanced patterns:
- `references/advanced-patterns.md` - Nested attributes, custom types, one-of types, parent tracking
