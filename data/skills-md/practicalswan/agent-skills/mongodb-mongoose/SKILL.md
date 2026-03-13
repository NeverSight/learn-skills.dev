---
name: mongodb-mongoose
description: MongoDB with Mongoose — schemas, models, aggregation pipelines, migrations, and Atlas connections. Use when designing collections, writing queries, or integrating MongoDB into Node.js/Next.js apps.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive guidance for MongoDB database design, Mongoose ODM patterns, and Atlas integration for Node.js/Next.js applications.

## When to Use This Skill

- Designing MongoDB schemas and data models
- Building Mongoose models with validation and middleware
- Implementing the repository pattern for data access
- Writing aggregation pipelines for complex queries
- Managing MongoDB Atlas connections and configuration
- Integrating MongoDB with Next.js API routes
- Database migration strategies


---

## Schema Design

### Data Modeling Principles
- **Embed** when data is accessed together and has a 1:few relationship
- **Reference** when data is accessed independently or has a 1:many/many:many relationship
- Design schemas around query patterns, not normalized relational models
- Use denormalization strategically for read performance

### Mongoose Model Pattern
```javascript
import mongoose from 'mongoose';

const recipeSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true,
    maxlength: [200, 'Title cannot exceed 200 characters'],
    index: true,
  },
  slug: {
    type: String,
    unique: true,
    lowercase: true,
  },
  ingredients: [{
    name: { type: String, required: true },
    amount: { type: Number, required: true },
    unit: { type: String, enum: ['g', 'kg', 'ml', 'l', 'cup', 'tbsp', 'tsp', 'piece'] },
  }],
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true,
  },
  tags: [{ type: String, lowercase: true, trim: true }],
  isPublished: { type: Boolean, default: false },
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true },
});

// Indexes for common queries
recipeSchema.index({ title: 'text', tags: 'text' });
recipeSchema.index({ author: 1, createdAt: -1 });

// Virtual fields
recipeSchema.virtual('ingredientCount').get(function() {
  return this.ingredients.length;
});

// Pre-save middleware
recipeSchema.pre('save', function(next) {
  if (this.isModified('title')) {
    this.slug = this.title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  }
  next();
});

export const Recipe = mongoose.models.Recipe || mongoose.model('Recipe', recipeSchema);
```

### Schema Best Practices
- Always define `required`, `type`, and validation rules
- Use `timestamps: true` for automatic `createdAt`/`updatedAt`
- Add indexes for frequently queried fields
- Use `enum` for fields with fixed values
- Define virtuals for computed properties
- Use middleware (pre/post hooks) for side effects

---

## Repository Pattern

```javascript
class RecipeRepository {
  async findAll(filter = {}, options = {}) {
    const { page = 1, limit = 20, sort = '-createdAt', populate = '' } = options;
    const skip = (page - 1) * limit;

    const [recipes, total] = await Promise.all([
      Recipe.find(filter)
        .sort(sort)
        .skip(skip)
        .limit(limit)
        .populate(populate)
        .lean(),
      Recipe.countDocuments(filter),
    ]);

    return {
      data: recipes,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    };
  }

  async findById(id) {
    return Recipe.findById(id).populate('author', 'name avatar').lean();
  }

  async create(data) {
    const recipe = new Recipe(data);
    return recipe.save();
  }

  async update(id, data) {
    return Recipe.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }

  async delete(id) {
    return Recipe.findByIdAndDelete(id);
  }

  async search(query, options = {}) {
    return this.findAll(
      { $text: { $search: query } },
      { ...options, sort: { score: { $meta: 'textScore' } } }
    );
  }
}

export const recipeRepository = new RecipeRepository();
```

---

## Aggregation Pipelines

### Common Patterns

```javascript
// Group recipes by tag with counts
const tagStats = await Recipe.aggregate([
  { $match: { isPublished: true } },
  { $unwind: '$tags' },
  { $group: { _id: '$tags', count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 20 },
]);

// Author statistics with lookup
const authorStats = await Recipe.aggregate([
  { $group: {
    _id: '$author',
    recipeCount: { $sum: 1 },
    avgRating: { $avg: '$rating' },
  }},
  { $lookup: {
    from: 'users',
    localField: '_id',
    foreignField: '_id',
    as: 'authorInfo',
  }},
  { $unwind: '$authorInfo' },
  { $project: {
    name: '$authorInfo.name',
    recipeCount: 1,
    avgRating: { $round: ['$avgRating', 1] },
  }},
  { $sort: { recipeCount: -1 } },
]);

// Date-based analytics
const monthlyRecipes = await Recipe.aggregate([
  { $match: { createdAt: { $gte: new Date('2024-01-01') } } },
  { $group: {
    _id: { $dateToString: { format: '%Y-%m', date: '$createdAt' } },
    count: { $sum: 1 },
  }},
  { $sort: { _id: 1 } },
]);
```

---

## Atlas Connection

### Connection Setup (Next.js)
```javascript
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
  throw new Error('MONGODB_URI environment variable is not defined');
}

let cached = global.mongoose;
if (!cached) {
  cached = global.mongoose = { conn: null, promise: null };
}

export async function connectDB() {
  if (cached.conn) return cached.conn;

  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI, {
      bufferCommands: false,
    });
  }

  cached.conn = await cached.promise;
  return cached.conn;
}
```

### Connection Best Practices
- Cache connection in development to prevent multiple connections
- Use `bufferCommands: false` for explicit error handling
- Set connection pool size via `maxPoolSize` for production
- Use Atlas connection string with `retryWrites=true&w=majority`

---

## Migration Strategies

### Document Versioning
```javascript
const userSchema = new mongoose.Schema({
  schemaVersion: { type: Number, default: 2 },
  // ... fields
});

userSchema.pre('save', function(next) {
  if (this.schemaVersion < 2) {
    // Migrate old fields to new format
    this.schemaVersion = 2;
  }
  next();
});
```

### Batch Migration Script
```javascript
async function migrateUsers() {
  const batchSize = 100;
  let processed = 0;
  let batch;

  do {
    batch = await User.find({ schemaVersion: { $lt: 2 } }).limit(batchSize);
    for (const user of batch) {
      user.schemaVersion = 2;
      await user.save();
      processed++;
    }
    console.log(`Migrated ${processed} users`);
  } while (batch.length === batchSize);
}
```

---

## Performance Tips

- Use `.lean()` for read-only queries (returns plain objects, 5-10x faster)
- Use `.select()` to return only needed fields
- Create compound indexes matching your query patterns
- Use `$project` early in aggregation to reduce working set
- Avoid `$lookup` in high-frequency queries; denormalize instead
- Use `explain()` to analyze query performance

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow queries | Add indexes, use `.lean()`, check with `explain()` |
| Connection timeouts | Check Atlas network access, increase pool size |
| Validation errors | Review schema constraints, check middleware order |
| Duplicate key errors | Ensure unique indexes, handle with try/catch |
| Memory issues | Use cursors for large datasets, limit batch sizes |

---

## References & Resources

### Documentation
- [Aggregation Reference](./references/aggregation-reference.md) — Pipeline stages, accumulator operators, and common aggregation recipes
- [Indexing Strategies](./references/indexing-strategies.md) — Index types, ESR rule, compound indexes, and performance analysis

### Scripts
- [Seed Database](./scripts/seed-database.js) — Zero-dependency MongoDB seeding script with sample recipe data

### Examples
- [Recipe API Example](./examples/recipe-api-example.md) — Complete Mongoose + Next.js Recipe CRUD API with models, routes, and validation

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [nestjs](../nestjs/SKILL.md) | NestJS backend using Mongoose models |
| [javascript-development](../javascript-development/SKILL.md) | JS patterns for database integration |
| [sql-development](../sql-development/SKILL.md) | Alternative relational database approach |
