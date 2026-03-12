---
name: nodejs-express-mongodb-backend-pattern
description: Scaffolds or references a production-ready Node.js REST API with Express 5, TypeScript, Mongoose (MongoDB), Redis, Sentry, JWT auth, bcrypt, rate limiting, and centralized error handling. Use when the user wants to start a new observable and resilient backend, needs a Node.js API boilerplate with security and monitoring, or asks to clone or adapt this template repository.
---

# Node.js Express MongoDB Backend Pattern

## Purpose

This skill helps the agent scaffold, explain, or adapt the **nodejs-express-mongodb-backend-pattern** template — a Node.js REST API boilerplate with observability, security, and resilience built in. The agent should use it when the user wants a backend with Express, MongoDB, Redis, Sentry, JWT authentication, and production-oriented middleware.

## When to use this skill

- The user wants to create a new REST API backend with Node.js and Express.
- The user asks for a production-ready or "observable" Node.js API template.
- The user mentions MongoDB/Mongoose, Redis, Sentry, rate limiting, or JWT auth and wants a starter.
- The user wants to clone, fork, or understand the structure of this repo (nodejs-express-mongodb-backend-pattern).
- The user needs steps to set up env vars, run the app, or add routes/controllers following this template's conventions.

## When NOT to use this skill

- The user wants a frontend or full-stack framework (Next.js, Nuxt, etc.).
- The user explicitly wants a different DB (PostgreSQL, MySQL) without Mongoose.
- The user wants a serverless/lambda architecture instead of a long-running Express server.

## How to use this template

### 1. Clone and install

```bash
git clone https://github.com/laskar-ksatria/building-observable-nodejs-api.git
cd building-observable-nodejs-api
npm install
```

### 2. Environment setup

- Create a `.env` file in the project root.
- Required variables: `PORT`, `MONGODB_URI`, `PRIVATE_KEY`, `TOKEN_EXPIRED`. Optional: `SENTRY_DSN`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`. App exits on startup if required vars are missing. Redis is used for optional caching (e.g. cache GET /api/user for 60s); if Redis is not set, the app runs without cache.
- Generate a JWT secret for `PRIVATE_KEY`:
  - Node: `node -e "console.log(require('crypto').randomBytes(64).toString('base64'))"`
  - OpenSSL: `openssl rand -hex 64`

### 3. Run the app

- Development: `npm run dev`
- Build: `npm run build` then `npm start`

### 4. API surface

- Base path: `/api`
- `POST /api/user/register` — register user (email, full_name, password)
- `POST /api/user/login` — login, returns JWT
- `GET /api/user` — current user (header: `Authorization: Bearer <token>`)
- `GET /` — health check

## Key features

- **Stack:** Express 5, TypeScript, Mongoose, Redis (ioredis), Sentry, Helmet, CORS.
- **Security:** NoSQL injection prevention, rejection of HTML in input, Helmet, CORS.
- **Auth:** JWT + bcrypt; password is hashed on save and never returned in JSON.
- **Resilience:** Per-route rate limiting, overload detection (toobusy), structured HttpError and fallback to Sentry for unexpected errors.
- **Structure:** `src/` with config, controllers, errors, lib, middlewares, models, routes, services, types; entry in `server.ts` with Sentry init.

---

## Conventions (IMPORTANT — follow these when generating code)

### File naming

- Models: `src/models/<entity>.model.ts`
- Controllers: `src/controllers/<entity>.controller.ts`
- Routes: `src/routes/<entity>.route.ts`
- Middlewares: `src/middlewares/<name>.ts`
- Services: `src/services/<name>.ts`
- All file names use **kebab-case**.

### Response format

Every API response follows this shape:

**Success:**

```json
{ "success": true, "data": { ... } }
```

**Error:**

```json
{ "success": false, "error": { "error_id": 0, "message": "...", "errors": [] } }
```

### Middleware order in `app.ts`

Order matters. Follow this exact sequence:

1. `helmet()` — security headers
2. `cors()` — cross-origin config
3. `express.json()` — parse JSON body (with size limit)
4. `express.urlencoded()` — parse URL-encoded body
5. `securityMiddleware` — NoSQL injection + HTML sanitization
6. `toobusy` check — overload detection (HTTP 529)
7. Cache-Control header — `no-store`
8. **Routes** — `app.use("/api", indexRoute)`
9. Health check — `app.get("/")`
10. `ErrorHandling` — **must be last** (global error handler)

### Error handling convention

- **Known/expected errors**: throw `new HttpError(errorStates.someError)`. These return the configured HTTP code and message to the client.
- **Adding a new error state**: add an entry to `errorStates` in `src/errors/index.ts` with a unique `error_id`, `message`, and `http_code`.
- **Sentry reporting**: unexpected errors (anything that is NOT an `HttpError`) are automatically sent to Sentry. For known errors that you still want to report, set `sentry: true` in the error state.
- **Mongoose validation errors**: automatically collected and returned in the `errors` array.

### Adding a new environment variable

1. Add the key to `.env`
2. Add it to `src/env.ts` in the `env` object
3. Use it via `import env from "../env"` then `env.YOUR_VAR`

### Dependencies

```json
{
  "dependencies": {
    "@sentry/node": "^8.x",
    "bcrypt": "^5.x",
    "cors": "^2.x",
    "dotenv": "^17.x",
    "express": "^5.x",
    "express-rate-limit": "^8.x",
    "helmet": "^8.x",
    "ioredis": "^5.x",
    "jsonwebtoken": "^9.x",
    "mongoose": "^9.x",
    "toobusy-js": "^0.5.x"
  },
  "devDependencies": {
    "@types/bcrypt": "^5.x",
    "@types/cors": "^2.x",
    "@types/express": "^4.x",
    "@types/ioredis": "^4.x",
    "@types/jsonwebtoken": "^9.x",
    "@types/toobusy-js": "^0.5.x",
    "nodemon": "^3.x",
    "ts-node": "^10.x",
    "tsx": "^4.x",
    "typescript": "^5.x"
  }
}
```

---

## How to add a new resource (step-by-step)

When the user asks to add a new entity (e.g. "Product"), follow these steps in order:

### Step 1 — Define types in `src/types/index.ts`

```ts
// Product
export interface IProduct {
  name: string;
  price: number;
  description: string;
}

export interface IProductDocument extends IProduct, Document {}
```

### Step 2 — Create model `src/models/product.model.ts`

```ts
import { Schema, model } from "mongoose";
import { IProductDocument } from "../types";

const productSchema = new Schema<IProductDocument>(
  {
    name: { type: String, required: true },
    price: { type: Number, required: true },
    description: { type: String, required: true },
  },
  { versionKey: false, timestamps: true },
);

export const ProductModel = model<IProductDocument>("Product", productSchema);
```

### Step 3 — Create controller `src/controllers/product.controller.ts`

```ts
import { Request, Response, NextFunction } from "express";
import { ProductModel } from "../models/product.model";
import HttpError, { errorStates } from "../errors";

class ProductController {
  static async create(req: Request, res: Response, next: NextFunction) {
    try {
      const product = await ProductModel.create(req.body);
      return res.status(201).json({ success: true, data: { product } });
    } catch (error) {
      next(error);
    }
  }

  static async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const products = await ProductModel.find();
      return res.status(200).json({ success: true, data: { products } });
    } catch (error) {
      next(error);
    }
  }
}

export default ProductController;
```

### Step 4 — Create route `src/routes/product.route.ts`

```ts
import ProductController from "../controllers/product.controller";
import { Router } from "express";
import { RateLimit } from "../services/rate-limit";
import Authentication from "../middlewares/auth";

const router = Router();

router.post("/", RateLimit({ max: 10, ms: 60000 }), Authentication, ProductController.create);
router.get("/", RateLimit({ max: 20, ms: 60000 }), ProductController.getAll);

export default router;
```

### Step 5 — Mount in `src/routes/index.ts`

```ts
import { Router } from "express";
import userRoute from "./user.route";
import productRoute from "./product.route";

const router = Router();
router.use("/user", userRoute);
router.use("/product", productRoute);
export default router;
```

---

## Code examples

The following snippets are the actual code from this template. Use them as the reference pattern when scaffolding a new project.

### Project structure

```
src/
├── config/
│   └── mongodb.ts          # MongoDB connection
├── controllers/
│   └── user.controller.ts  # Request handlers
├── errors/
│   └── index.ts            # HttpError, errorStates
├── lib/
│   └── utils.ts            # bcrypt, emailRegex
├── middlewares/
│   ├── auth.ts             # JWT verification
│   ├── error-handling.ts   # Global error + Sentry
│   └── security.ts         # NoSQL/HTML sanitization
├── models/
│   └── user.model.ts       # Mongoose schema
├── routes/
│   ├── index.ts            # Mounts sub-routes
│   └── user.route.ts       # /api/user routes
├── services/
│   ├── jwt.ts              # GenerateToken, VerifyToken
│   ├── rate-limit.ts       # Per-route rate limiter
│   └── redis.ts            # Optional cache (getCache, setCache, deleteCache)
├── types/
│   └── index.ts            # Shared interfaces
├── app.ts                  # Express app + middleware
├── env.ts                  # Load and export env
└── server.ts               # Entry, Sentry.init, listen
```

### Env config (`src/env.ts`)

```ts
import { config } from "dotenv";
config();

const env = {
  PORT: `${process.env.PORT}`,
  REDIS_HOST: `${process.env.REDIS_HOST}`,
  REDIS_PORT: `${process.env.REDIS_PORT}`,
  SENTRY_DSN: `${process.env.SENTRY_DSN}`,
  TOKEN_EXPIRED: `${process.env.TOKEN_EXPIRED}`,
  PRIVATE_KEY: `${process.env.PRIVATE_KEY}`,
  MONGODB_URI: process.env.MONGODB_URI!,
  REDIS_PASSWORD: `${process.env.REDIS_PASSWORD}`,
};

export default env;
```

### Server entry (`src/server.ts`)

```ts
import * as Sentry from "@sentry/node";
import { server } from "./app";
import toobusy from "toobusy-js";
import env from "./env";
import dbConnect from "./config/mongodb";

if (env.SENTRY_DSN) {
  Sentry.init({ dsn: env.SENTRY_DSN, environment: process.env.NODE_ENV ?? "development" });
}

async function main() {
  await dbConnect();
  server.listen(env.PORT, () => {
    console.log(`Server running on http://localhost:${env.PORT}`);
  });
  process.on("SIGINT", () => { toobusy.shutdown(); process.exit(); });
  process.on("exit", () => toobusy.shutdown());
}

main().catch((err) => { console.error(err); process.exit(1); });
```

### Database config (`src/config/mongodb.ts`)

```ts
import mongoose from "mongoose";
import env from "../env";
import * as Sentry from "@sentry/node";

export default async function dbConnect(): Promise<void> {
  try {
    await mongoose.connect(env.MONGODB_URI);
    mongoose.connection.on("error", (err) => {
      Sentry.captureException(err);
      console.error("MongoDB connection error:", err);
    });
    console.log("Connected to MongoDB");
  } catch (error) {
    console.error("Failed to connect to MongoDB:", error);
    Sentry.captureException(error);
    process.exit(1);
  }
}
```

### Types (`src/types/index.ts`)

```ts
import { Document, Types } from "mongoose";
import { Request } from "express";

export type TGenerateToken = { id: Types.ObjectId };

export interface IAuthRequest extends Request {
  decoded?: TGenerateToken;
}

export interface IErrorMessage {
  message: string;
  error_id: number;
  http_code: number;
  sentry?: boolean;
}

export type CreateLimitType = { max: number; ms: number };

export interface IUser {
  email: string;
  full_name: string;
  password: string;
}

export interface IUserModel extends IUser {
  _id: Types.ObjectId;
}

export interface IUserDocument extends IUser, Document {}
```

### Model (`src/models/user.model.ts`)

```ts
import { emailRegex, hashPassword } from "../lib/utils";
import { Schema, model } from "mongoose";
import { IUserDocument } from "../types";

const userSchema = new Schema<IUserDocument>(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      index: true,
      validate: {
        validator: (value: string) => emailRegex.test(value),
        message: "Invalid email address",
      },
    },
    full_name: { type: String, required: true },
    password: { type: String, required: true },
  },
  { versionKey: false, timestamps: true },
);

userSchema.pre("save", async function () {
  if (!this.isModified("password")) return;
  this.password = await hashPassword(this.password);
});

export const UserModel = model<IUserDocument>("User", userSchema);
```

### Controller (`src/controllers/user.controller.ts`)

```ts
import { Request, Response, NextFunction } from "express";
import { UserModel } from "../models/user.model";
import { comparePassword } from "../lib/utils";
import { IAuthRequest, IUserDocument } from "../types";
import HttpError, { errorStates } from "../errors";
import { GenerateToken } from "../services/jwt";
import { getCache, setCache, CACHE_USER } from "../services/redis";

class UserController {
  static async createUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { email, full_name, password } = req.body;
      const user = (await UserModel.create({ email, full_name, password })) as IUserDocument;
      const access_token = GenerateToken({ id: user._id });
      return res.status(201).json({
        success: true,
        data: {
          access_token,
          user: { _id: user._id, full_name: user.full_name, email: user.email },
        },
      });
    } catch (error) {
      next(error);
    }
  }

  static async loginUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { email, password } = req.body;
      const user = (await UserModel.findOne({ email })) as IUserDocument;
      if (!user) throw new HttpError(errorStates.invalidEmailOrPassword);
      const valid = await comparePassword(password, user.password);
      if (!valid) throw new HttpError(errorStates.invalidEmailOrPassword);
      const access_token = GenerateToken({ id: user._id });
      const { password: _p, ...safeUser } = user.toObject();
      return res.status(200).json({ success: true, data: { user: safeUser, access_token } });
    } catch (error) {
      next(error);
    }
  }

  static async getUser(req: IAuthRequest, res: Response, next: NextFunction) {
    try {
      const userId = req?.decoded?.id;
      if (!userId) throw new HttpError(errorStates.failedAuthentication);

      const idStr = String(userId);
      const cacheKey = CACHE_USER(idStr);
      const cached = await getCache(cacheKey);
      if (cached) {
        const user = JSON.parse(cached);
        return res.status(200).json({ success: true, data: { user } });
      }

      const user = await UserModel.findById(userId);
      if (!user) throw new HttpError(errorStates.failedAuthentication);
      const { password: _p, ...safeUser } = user.toObject();
      await setCache(cacheKey, JSON.stringify(safeUser));

      return res.status(200).json({ success: true, data: { user: safeUser } });
    } catch (error) {
      next(error);
    }
  }
}

export default UserController;
```

### Routes

**Mount (`src/routes/index.ts`):**

```ts
import { Router } from "express";
import userRoute from "./user.route";

const router = Router();
router.use("/user", userRoute);
export default router;
```

**User routes (`src/routes/user.route.ts`):**

```ts
import UserController from "../controllers/user.controller";
import { Router } from "express";
import { RateLimit } from "../services/rate-limit";
import Authentication from "../middlewares/auth";

const router = Router();

router.post("/register", RateLimit({ max: 10, ms: 60000 }), UserController.createUser);
router.post("/login", RateLimit({ max: 10, ms: 60000 }), UserController.loginUser);
router.get("/", RateLimit({ max: 3, ms: 1000 }), Authentication, UserController.getUser);

export default router;
```

### Errors (`src/errors/index.ts`)

```ts
import { IErrorMessage } from "../types";

export const errorStates = {
  internalservererror: { message: "Oops! Something's off-track.", error_id: 0, http_code: 500 },
  highTraffic: { message: "Too many steps at once! Try again soon.", error_id: 1, http_code: 503 },
  rateLimit: { message: "Whoa, slow down! Try again later.", error_id: 2, http_code: 429 },
  failedAuthentication: { message: "Not Authenticated", error_id: 3, http_code: 401 },
  invalidEmailOrPassword: { message: "Invalid email or password", error_id: 4, http_code: 401 },
  tokenExpired: { message: "Session expired—log in again!", error_id: 5, http_code: 401 },
} as const;

class HttpError extends Error {
  statusCode: number;
  error_id: number;
  constructor(args: IErrorMessage) {
    super(args.message);
    this.statusCode = args.http_code;
    this.error_id = args.error_id;
    Object.setPrototypeOf(this, HttpError.prototype);
  }
}

export default HttpError;
```

### Middleware – Security (`src/middlewares/security.ts`)

```ts
import { NextFunction, Request, Response } from "express";

const dangerousKeyPattern = /^\$|\.|\$/;
const htmlTagPattern = /<[^>]*>/;

const sanitizeObject = <T>(value: T): T => {
  const inner = (val: unknown): unknown => {
    if (Array.isArray(val)) return val.map(inner);
    if (val && typeof val === "object") {
      const obj = val as Record<string, unknown>;
      const sanitized: Record<string, unknown> = {};
      Object.keys(obj).forEach((key) => {
        if (dangerousKeyPattern.test(key)) return;
        sanitized[key] = inner(obj[key]);
      });
      return sanitized;
    }
    if (typeof val === "string") {
      if (htmlTagPattern.test(val)) throw new Error("HTML content is not allowed in input.");
      return val;
    }
    return val;
  };
  return inner(value) as T;
};

export const securityMiddleware = (req: Request, res: Response, next: NextFunction): void => {
  try {
    req.body = sanitizeObject(req.body);

    const sanitizedQuery = sanitizeObject(req.query);
    const sanitizedParams = sanitizeObject(req.params);

    Object.keys(req.query).forEach((key) => delete (req.query as any)[key]);
    Object.assign(req.query as any, sanitizedQuery as any);

    Object.keys(req.params).forEach((key) => delete (req.params as any)[key]);
    Object.assign(req.params as any, sanitizedParams as any);

    next();
  } catch (err) {
    res.status(400).json({ message: (err as Error).message || "Invalid input." });
  }
};
```

### Middleware – Error handling (`src/middlewares/error-handling.ts`)

```ts
import { Request, Response, NextFunction } from "express";
import * as Sentry from "@sentry/node";
import HttpError, { errorStates } from "../errors";

export const ErrorHandling = (error: unknown, req: Request, res: Response, next: NextFunction): void => {
  if (error instanceof HttpError) {
    const statusCode = error.statusCode ?? errorStates.internalservererror.http_code;
    if ((error as any).sentry) Sentry.captureException(error);
    res.status(statusCode).json({
      success: false,
      error: { error_id: error.error_id, message: error.message, errors: [] },
    });
    return;
  }

  const validationErrors: Array<Record<string, string>> = [];
  if ((error as any)?.errors) {
    Object.entries((error as any).errors).forEach(([key, value]: [string, any]) => {
      validationErrors.push({ [key]: value.message });
    });
  }

  Sentry.captureException(error);

  const fallback = errorStates.internalservererror;
  res.status(fallback.http_code).json({
    success: false,
    error: { error_id: fallback.error_id, message: fallback.message, errors: validationErrors },
  });
};
```

### Middleware – Auth (`src/middlewares/auth.ts`)

```ts
import HttpError, { errorStates } from "../errors";
import { VerifyToken } from "../services/jwt";
import { Response, NextFunction } from "express";
import { IAuthRequest } from "../types";

export default function Authentication(req: IAuthRequest, res: Response, next: NextFunction) {
  try {
    const token = req?.headers?.authorization;
    if (!token) throw new HttpError(errorStates.failedAuthentication);
    const decoded = VerifyToken(token.split("Bearer ")[1]);
    req.decoded = decoded;
    next();
  } catch (error: unknown) {
    if ((error as { name?: string })?.name === "TokenExpiredError") {
      return next(new HttpError(errorStates.tokenExpired));
    }
    next(error);
  }
}
```

### Services

**Rate limit (`src/services/rate-limit.ts`):**

```ts
import rateLimit from "express-rate-limit";
import { errorStates } from "../errors";
import { CreateLimitType } from "../types";

export const RateLimit = ({ max, ms }: CreateLimitType) =>
  rateLimit({
    windowMs: ms,
    max,
    message: { error_id: errorStates.rateLimit.error_id, message: errorStates.rateLimit.message },
  });
```

**JWT (`src/services/jwt.ts`):**

```ts
import jwt from "jsonwebtoken";
import env from "../env";
import { TGenerateToken } from "../types";

export const GenerateToken = (payload: TGenerateToken): string =>
  jwt.sign(payload, env.PRIVATE_KEY, { expiresIn: env.TOKEN_EXPIRED });

export const VerifyToken = (token: string): TGenerateToken =>
  jwt.verify(token, env.PRIVATE_KEY) as TGenerateToken;
```

**Redis (`src/services/redis.ts`) — optional:**

Redis is used as a cache layer. If `REDIS_HOST` is not set, cache is skipped and the app runs without Redis.

```ts
import Redis from "ioredis";
import env from "../env";

export const CACHE_USER = (id: string) => `user:${id}`;
const USER_CACHE_TTL_SEC = 60;

class RedisClient {
  private static instance: Redis | null = null;

  public static getInstance(): Redis | null {
    if (this.instance !== null) return this.instance;
    if (!env.REDIS_HOST || env.REDIS_HOST === "") return null;
    try {
      this.instance = new Redis({
        host: env.REDIS_HOST,
        port: Number(env.REDIS_PORT) || 6379,
        password: env.REDIS_PASSWORD || undefined,
      });
      this.instance.on("error", (err) => console.error("Redis error:", err));
      return this.instance;
    } catch {
      return null;
    }
  }
}

export const setCache = async (key: string, value: string, expirySeconds = 60): Promise<void> => {
  const redis = RedisClient.getInstance();
  if (!redis) return;
  try {
    await redis.set(key, value, "EX", expirySeconds);
  } catch (err) {
    console.error("Redis setCache error:", err);
  }
};

export const getCache = async (key: string): Promise<string | null> => {
  const redis = RedisClient.getInstance();
  if (!redis) return null;
  try {
    return await redis.get(key);
  } catch (err) {
    console.error("Redis getCache error:", err);
    return null;
  }
};

export const deleteCache = async (key: string): Promise<void> => {
  const redis = RedisClient.getInstance();
  if (!redis) return;
  try {
    await redis.del(key);
  } catch (err) {
    console.error("Redis deleteCache error:", err);
  }
};
```

**Sample: cache-aside in `getUser`**

- Try `getCache(CACHE_USER(userId))`. If hit, return cached JSON.
- Else load user from DB, then `setCache(cacheKey, JSON.stringify(safeUser), 60)` and return.
- When Redis is not configured, `getCache`/`setCache` no-op; the app still works without cache.

### Lib – utils (`src/lib/utils.ts`)

```ts
import bcrypt from "bcrypt";

export const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
const SALT_ROUNDS = 10;

export const hashPassword = async (password: string): Promise<string> =>
  bcrypt.hash(password, SALT_ROUNDS);

export const comparePassword = async (password: string, hashed: string): Promise<boolean> =>
  bcrypt.compare(password, hashed);
```

### App (`src/app.ts`)

```ts
import express, { Express, NextFunction, Request, Response } from "express";
import cors from "cors";
import http from "http";
import toobusy from "toobusy-js";
import helmet from "helmet";
import { securityMiddleware } from "./middlewares/security";
import indexRoute from "./routes";
import { ErrorHandling } from "./middlewares/error-handling";

toobusy.maxLag(120);

const app: Express = express();
const server = http.createServer(app);

app.use(helmet());
app.use(cors({
  origin: ["http://localhost:3005", "http://localhost:3000"],
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
}));
app.use(express.json({ limit: "100kb" }));
app.use(express.urlencoded({ extended: false }));
app.use(securityMiddleware);

app.use((req, res, next) => {
  if (toobusy()) return res.status(529).json({ message: "High Traffic" });
  else next();
});

app.use((req, res, next) => {
  res.setHeader("Cache-Control", "no-store");
  next();
});

app.use("/api", indexRoute);

app.get("/", (req: Request, res: Response, next: NextFunction) => {
  res.send("Our Backend Running Correctly");
});

app.use(ErrorHandling);

export { app, server };
```

---

## Repository and docs

- **GitHub:** [https://github.com/laskar-ksatria/building-observable-nodejs-api](https://github.com/laskar-ksatria/building-observable-nodejs-api)
- Full setup, env table, and API overview: see the repository README.

## Validation / done checklist

When helping the user run or extend this template, confirm:

- `.env` exists with at least `PORT`, `MONGODB_URI`, `PRIVATE_KEY`, `TOKEN_EXPIRED`.
- MongoDB is reachable (and Redis if used).
- `SENTRY_DSN` is set if error monitoring is desired.
- After `npm run dev`, `GET /` returns a success message.
- Auth routes (`/api/user/register`, `/api/user/login`, `GET /api/user`) respond correctly.
- New resources follow the convention: types -> model -> controller -> route -> mount in index.

