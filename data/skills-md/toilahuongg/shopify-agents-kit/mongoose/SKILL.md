---
name: mongoose
description: Guide for Mongoose ODM (2025-2026 Edition), covering Mongoose 8.x/9.x, TypeScript integration, and performance best practices.
---

# Mongoose Skill (2025-2026 Edition)

This skill provides modern guidelines for using Mongoose with MongoDB, focusing on Mongoose 8.x/9.x, strict TypeScript integration, and performance optimizations relevant to the 2025 ecosystem.

## 🚀 Key Trends & Features (2025/2026)

*   **TypeScript-First:** Mongoose 8+ has superior built-in type inference. `@types/mongoose` is obsolete.
*   **Performance:** Mongoose 9 introduces architectural changes for lower overhead. Native vector search support is now standard for AI features.
*   **Modern JavaScript:** Full support for `async/await` iterators and native Promises.

## 📐 TypeScript Integration (The Strict Way)

Do **NOT** extend `LengthyDocument` or standard `Document`. Use a plain interface and let Mongoose infer the rest.

### 1. Define the Interface (Raw Data)
Define what your data looks like in plain JavaScript objects.

```typescript
import { Types } from 'mongoose';

export interface IUser {
  name: string;
  email: string;
  role: 'admin' | 'user';
  tags: string[];
  organization?: Types.ObjectId; // Use specific type for ObjectIds
  createdAt?: Date;
}
```

### 2. Define the Schema & Model
Create the model with generic typing.

```typescript
import mongoose, { Schema, model } from 'mongoose';
import { IUser } from './interfaces';

const userSchema = new Schema<IUser>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  role: { type: String, enum: ['admin', 'user'], default: 'user' },
  tags: [String],
  organization: { type: Schema.Types.ObjectId, ref: 'Organization' }
}, {
  timestamps: true /* Automatically manages createdAt/updatedAt */
});

// ⚡ 2025 Best Practice: Avoid "extends Document" on the interface.
// Let 'model<IUser>' handle the HydratedDocument type automatically.
export const User = mongoose.models.User || model<IUser>('User', userSchema);
```

### 3. Usage (Type-Safe)

```typescript
// 'user' is typed as HydratedDocument<IUser> automatically
const user = await User.findOne({ email: 'test@example.com' });

if (user) {
  console.log(user.name); // Typed string
  await user.save(); // Typed method
}
```

## ⚡ Performance Optimization

### 1. `.lean()` for Reads
Always use `.lean()` for read-only operations (e.g., GET requests). It skips Mongoose hydration, speeding up queries by 30-50%.

```typescript
// Returns plain JS object (IUser), NOT a Mongoose document
const users = await User.find({ role: 'admin' }).lean(); 
```

### 2. Indexes
Define compound indexes for common query patterns directly in the schema.

```typescript
// Schema definition
userSchema.index({ organization: 1, email: 1 }); // Optimized lookup
```

### 3. Projections
Fetch only what you need. Network I/O is often the bottleneck.

```typescript
const names = await User.find({}, { name: 1 }).lean();
```

## 🛠️ Connection Management (Serverless/Edge Friendly)

For modern serverless/edge environments (like Vercel, Next.js, Remix), use a singleton pattern with caching to prevent connection exhaustion.

```typescript
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI!;

if (!MONGODB_URI) {
  throw new Error('Please define the MONGODB_URI environment variable');
}

/**
 * Global is used here to maintain a cached connection across hot reloads
 * in development. This prevents connections growing exponentially
 * during API Route usage.
 */
let cached = (global as any).mongoose;

if (!cached) {
  cached = (global as any).mongoose = { conn: null, promise: null };
}

async function connectDb() {
  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.promise) {
    const opts = {
      bufferCommands: false,
    };

    cached.promise = mongoose.connect(MONGODB_URI, opts).then((mongoose) => {
      return mongoose;
    });
  }
  
  try {
    cached.conn = await cached.promise;
  } catch (e) {
    cached.promise = null;
    throw e;
  }

  return cached.conn;
}

export default connectDb;
```

## 📚 References

*   [Mongoose Documentation (Latest)](https://mongoosejs.com/docs/)
*   [Mongoose TypeScript Guide](https://mongoosejs.com/docs/typescript.html)
*   [MongoDB Performance Best Practices](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)
