---
name: vm-code-refactor
description: Intelligent code refactoring based on best practices. Detects code smells, applies design patterns, improves readability, enforces SOLID principles, and optimizes performance. Auto-detects framework and generates comprehensive refactoring plans.
---

# VM Code Refactor Skill

Comprehensive code refactoring with automatic framework detection and best practices enforcement.

## When to Use

- "Refactor this code"
- "Clean up this file"
- "Improve code structure"
- "Apply design patterns"
- "Fix code smells"
- "Reduce technical debt"
- "Make this code more maintainable"

## Workflow

### Step 1: Initial Prompt

**ALWAYS start by asking the user:**

```
question tool parameters:
  questions:
    - question: "Ready to refactor your code?"
      header: "Refactor"
      options:
        - label: "Yes, let's go! (Recommended)"
          description: "Start the refactoring process"
        - label: "No, thanks."
          description: "Exit without changes"
```

**If "No, thanks."** → Stop with:
```
No problem! Run this skill again when you're ready to refactor. 🔧
```

**If "Yes, let's go!"** → Proceed to Step 2

### Step 2: Inspection Decision

**After user confirms "Yes, let's go!", ask:**

```
question tool parameters:
  questions:
    - question: "Would you like me to inspect if refactoring is needed first?"
      header: "Inspect"
      options:
        - label: "Yes, inspect first (Recommended)"
          description: "Analyze codebase for refactoring opportunities before proceeding"
        - label: "Skip inspection"
          description: "Go directly to scope selection if you already know what to refactor"
```

**If "Skip inspection"** → Proceed directly to Step 3 (Scope Selection)

**If "Yes, inspect first"** → Display:

```
Analyzing codebase for refactoring opportunities... 🔍
```

Then prompt for inspection type:

```
question tool parameters:
  questions:
    - question: "What level of inspection would you like?"
      header: "Detail Level"
      options:
        - label: "Quick Scan (Recommended)"
          description: "Count-based summary: total issues by category and priority"
        - label: "Detailed Report"
          description: "Full analysis with file-by-file breakdown of all issues"
```

#### Quick Scan Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFACTORING ANALYSIS - QUICK SCAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework: React 18.2 + TypeScript 5.0
Files Analyzed: 47

Issues Found: 23

By Priority:
  🔴 Critical: 3
  🟡 Major: 8
  🔵 Minor: 12

By Category:
  Code Smells: 15
  SOLID Violations: 5
  Performance Issues: 3

Top 3 Areas Needing Attention:
1. UserManager.ts - God object pattern
2. PaymentService.ts - Tight coupling
3. API routes - N+1 query problems

Recommendation: Refactoring would significantly improve code quality.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceeding to scope selection...
```

#### Detailed Report Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFACTORING ANALYSIS - DETAILED REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework: React 18.2 + TypeScript 5.0
Build Tool: Vite 5.0
Linter: ESLint 8.0
Files Analyzed: 47

## Issues by File:

### src/models/UserManager.ts (Critical)
- God Object: 800+ lines, 15 methods
- Multiple Responsibilities: Auth, Permissions, Notifications, Billing
- Recommendation: Split into 4 separate service classes

### src/services/PaymentService.ts (Critical)
- Tight Coupling: Direct Stripe dependency
- No Dependency Injection
- No Error Handling
- Recommendation: Implement PaymentGateway interface

### src/api/routes/users.ts (Major)
- N+1 Query Problem: 101 queries for 100 users
- Current: 8.2s load time
- Recommendation: Use eager loading (1 query)

### src/components/UserCard.tsx (Major)
- Missing memoization
- Unnecessary re-renders on parent update
- Recommendation: Add React.memo and useCallback

### src/utils/validation.ts (Minor)
- Magic Numbers: Password length 8, email regex
- Recommendation: Extract to constants

[... continue for all files with issues ...]

## Summary:

| Category | Critical | Major | Minor | Total |
|----------|----------|-------|-------|-------|
| Code Smells | 2 | 5 | 8 | 15 |
| SOLID Violations | 1 | 3 | 1 | 5 |
| Performance | 0 | 2 | 1 | 3 |
| **Total** | **3** | **10** | **10** | **23** |

## Recommended Priority Order:
1. Decouple PaymentService (2h) - Critical
2. Break up UserManager (3h) - Critical
3. Fix N+1 queries (1h) - Major
4. Add React memoization (1h) - Major
5. Extract magic numbers (30m) - Minor

Estimated Total Time: 7.5 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceeding to scope selection...
```

**After inspection output, proceed to Step 3 (Scope Selection)**

### Step 3: Scope Selection

**Prompt for refactoring scope:**

```
question tool parameters:
  questions:
    - question: "What would you like to refactor?"
      header: "Scope"
      options:
        - label: "Specific file(s) - I'll provide path(s)"
          description: "Select one or more files to refactor"
        - label: "Entire codebase"
          description: "Analyze and refactor all source files"
        - label: "Cancel"
          description: "Exit without making changes"
```

**Option 1: Specific file(s)**
- Ask user to provide file path(s)
- User can provide multiple paths separated by commas or newlines
- Example: `src/utils/helper.js, src/models/User.js`

**Path Validation:**
After receiving paths, validate each one:

- **All paths invalid**: Display error message and return to scope selection:
  ```
  ❌ The following paths could not be found:
  - src/utils/helper.js
  - src/models/User.js

  Please check the paths and try again.
  ```
  Allow user to retry with corrected paths.

- **Partial paths invalid**: List invalid paths, prompt user to proceed with valid paths only:
  ```
  ⚠️ The following paths could not be found:
  - src/invalid-file.js

  Valid paths found:
  - src/utils/helper.js ✓
  - src/models/User.js ✓

  Would you like to proceed with only the valid paths?
  ```
  User can choose to proceed or return to scope selection to correct paths.

- **All paths valid**: Proceed with analysis immediately.

**Option 2: Entire codebase**
- Scan all source files
- Skip node_modules, dist, build, etc.
- Prioritize by complexity and impact

**Option 3: Cancel**
- Stop with: `Refactoring cancelled. No changes made. 🔧`

### Step 4: Generate Plan

**After Option 1 or 2, display:**
```
Creating Plan... 🔍

Detecting framework and analyzing code...
```

**Framework Detection:**
```
Framework Detected: React 18.2 + TypeScript 5.0 ✓
Build Tool: Vite 5.0
Linter: ESLint 8.0
State Management: Redux Toolkit

Analyzing code patterns and smells...
```

**Generate `REFACTOR_PLANNING.md` in project root**

**After plan creation:**
```
PLAN CREATED! 📋

Location: /project-root/REFACTOR_PLANNING.md

Summary:
- 23 refactoring opportunities found
- Estimated impact: High
- Estimated time: 4-6 hours
```

### Step 5: Implementation Decision

**Prompt for implementation:**

```
question tool parameters:
  questions:
    - question: "Do you want to continue with implementing the plan?"
      header: "Implement"
      options:
        - label: "Yes, implement now (Recommended)"
          description: "Execute the refactoring plan immediately"
        - label: "No, thanks."
          description: "Save the plan for manual implementation later"
```

**Option 1: Yes, implement now (Recommended)**
- Execute refactoring plan
- Create backup of original files
- Apply changes incrementally
- Run tests after each major change
- Display: `ALL DONE! 🎉`

**Option 2: No, thanks.**
- Stop with: `Plan saved. You can implement it manually or run this skill again. 🔧`

## Refactoring Categories

### 1. Code Smells

**Long Method:**
```javascript
// ❌ Too long, does too much
function processOrder(order) {
  // Validate order (20 lines)
  if (!order.id) throw new Error('Invalid order');
  if (!order.items || order.items.length === 0) throw new Error('No items');
  // ... 15 more validation lines
  
  // Calculate total (15 lines)
  let total = 0;
  for (let item of order.items) {
    total += item.price * item.quantity;
    if (item.discount) {
      total -= item.discount;
    }
  }
  
  // Apply tax (10 lines)
  const taxRate = getTaxRate(order.state);
  total = total * (1 + taxRate);
  
  // Process payment (25 lines)
  // ... payment processing logic
  
  // Send confirmation (15 lines)
  // ... email sending logic
  
  return { success: true, total };
}

// ✅ Refactored: Single Responsibility
function processOrder(order) {
  validateOrder(order);
  const subtotal = calculateSubtotal(order.items);
  const total = applyTax(subtotal, order.state);
  const payment = processPayment(order.paymentMethod, total);
  sendConfirmation(order.email, order, payment);
  
  return { success: true, total, paymentId: payment.id };
}

function validateOrder(order) {
  if (!order.id) throw new Error('Invalid order ID');
  if (!order.items?.length) throw new Error('Order has no items');
  if (!order.paymentMethod) throw new Error('No payment method');
}

function calculateSubtotal(items) {
  return items.reduce((sum, item) => {
    const itemTotal = item.price * item.quantity;
    return sum + itemTotal - (item.discount || 0);
  }, 0);
}

function applyTax(amount, state) {
  const taxRate = getTaxRate(state);
  return amount * (1 + taxRate);
}
```

**Duplicate Code:**
```python
# ❌ Repeated logic
class UserService:
    def create_user(self, data):
        if not data.get('email'):
            raise ValueError("Email required")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
            raise ValueError("Invalid email")
        if len(data.get('password', '')) < 8:
            raise ValueError("Password too short")
        # ... create user
    
    def update_user(self, user_id, data):
        if 'email' in data:
            if not data['email']:
                raise ValueError("Email required")
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
                raise ValueError("Invalid email")
        if 'password' in data:
            if len(data['password']) < 8:
                raise ValueError("Password too short")
        # ... update user

# ✅ Refactored: DRY principle
class UserService:
    def create_user(self, data):
        self._validate_user_data(data, require_all=True)
        # ... create user
    
    def update_user(self, user_id, data):
        self._validate_user_data(data, require_all=False)
        # ... update user
    
    def _validate_user_data(self, data, require_all=False):
        if require_all or 'email' in data:
            if not data.get('email'):
                raise ValueError("Email required")
            if not self._is_valid_email(data['email']):
                raise ValueError("Invalid email")
        
        if require_all or 'password' in data:
            if len(data.get('password', '')) < 8:
                raise ValueError("Password must be at least 8 characters")
    
    @staticmethod
    def _is_valid_email(email):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
```

**God Object:**
```javascript
// ❌ Class does everything
class User {
  constructor(data) { this.data = data; }
  
  // User data management
  save() { /* DB logic */ }
  update() { /* DB logic */ }
  delete() { /* DB logic */ }
  
  // Authentication
  login(password) { /* Auth logic */ }
  logout() { /* Auth logic */ }
  resetPassword() { /* Email logic */ }
  
  // Permissions
  hasPermission(resource) { /* Permission logic */ }
  grantPermission(resource) { /* Permission logic */ }
  
  // Notifications
  sendEmail(message) { /* Email logic */ }
  sendSMS(message) { /* SMS logic */ }
  
  // Billing
  chargeCreditCard(amount) { /* Payment logic */ }
  refund(amount) { /* Payment logic */ }
}

// ✅ Refactored: Separation of Concerns
class User {
  constructor(data) {
    this.data = data;
    this.auth = new UserAuth(this);
    this.permissions = new UserPermissions(this);
    this.notifications = new UserNotifications(this);
    this.billing = new UserBilling(this);
  }
  
  save() { return UserRepository.save(this); }
  update(data) { return UserRepository.update(this.id, data); }
  delete() { return UserRepository.delete(this.id); }
}

class UserAuth {
  constructor(user) { this.user = user; }
  login(password) { /* Auth logic */ }
  logout() { /* Auth logic */ }
  resetPassword() { /* Auth logic */ }
}

class UserPermissions {
  constructor(user) { this.user = user; }
  has(resource) { /* Permission logic */ }
  grant(resource) { /* Permission logic */ }
}
```

### 2. SOLID Principles

**Single Responsibility Principle:**
```typescript
// ❌ Multiple responsibilities
class Report {
  data: any[];
  
  constructor(data: any[]) {
    this.data = data;
  }
  
  // Responsibility 1: Data processing
  processData() {
    return this.data.map(item => ({
      ...item,
      total: item.price * item.quantity
    }));
  }
  
  // Responsibility 2: Formatting
  formatAsHTML() {
    const processed = this.processData();
    return `<table>${processed.map(row => 
      `<tr><td>${row.name}</td><td>${row.total}</td></tr>`
    ).join('')}</table>`;
  }
  
  // Responsibility 3: Export
  exportToPDF() {
    const html = this.formatAsHTML();
    // PDF generation logic
  }
  
  // Responsibility 4: Persistence
  saveToDatabase() {
    const processed = this.processData();
    // Database save logic
  }
}

// ✅ Refactored: Single responsibility per class
class ReportData {
  constructor(private data: any[]) {}
  
  process() {
    return this.data.map(item => ({
      ...item,
      total: item.price * item.quantity
    }));
  }
}

class ReportFormatter {
  formatAsHTML(data: any[]) {
    return `<table>${data.map(row => 
      `<tr><td>${row.name}</td><td>${row.total}</td></tr>`
    ).join('')}</table>`;
  }
  
  formatAsJSON(data: any[]) {
    return JSON.stringify(data, null, 2);
  }
}

class ReportExporter {
  exportToPDF(html: string) {
    // PDF generation logic
  }
  
  exportToExcel(data: any[]) {
    // Excel generation logic
  }
}

class ReportRepository {
  save(data: any[]) {
    // Database save logic
  }
}
```

**Open/Closed Principle:**
```python
# ❌ Modifying class to add new behavior
class PaymentProcessor:
    def process(self, payment_method, amount):
        if payment_method == 'credit_card':
            # Credit card logic
            pass
        elif payment_method == 'paypal':
            # PayPal logic
            pass
        elif payment_method == 'bitcoin':  # New payment method requires modification
            # Bitcoin logic
            pass

# ✅ Refactored: Open for extension, closed for modification
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        # Credit card logic
        pass

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        # PayPal logic
        pass

class BitcoinPayment(PaymentMethod):  # New payment method via extension
    def process(self, amount):
        # Bitcoin logic
        pass

class PaymentProcessor:
    def process(self, payment_method: PaymentMethod, amount):
        return payment_method.process(amount)
```

### 3. Design Patterns

**Strategy Pattern:**
```javascript
// ❌ Hard-coded sorting logic
class DataSorter {
  sort(data, type) {
    if (type === 'alphabetical') {
      return data.sort((a, b) => a.name.localeCompare(b.name));
    } else if (type === 'date') {
      return data.sort((a, b) => new Date(a.date) - new Date(b.date));
    } else if (type === 'price') {
      return data.sort((a, b) => a.price - b.price);
    }
  }
}

// ✅ Refactored: Strategy pattern
class SortStrategy {
  sort(data) {
    throw new Error('Must implement sort method');
  }
}

class AlphabeticalSort extends SortStrategy {
  sort(data) {
    return data.sort((a, b) => a.name.localeCompare(b.name));
  }
}

class DateSort extends SortStrategy {
  sort(data) {
    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  }
}

class PriceSort extends SortStrategy {
  sort(data) {
    return data.sort((a, b) => a.price - b.price);
  }
}

class DataSorter {
  constructor(strategy) {
    this.strategy = strategy;
  }
  
  setStrategy(strategy) {
    this.strategy = strategy;
  }
  
  sort(data) {
    return this.strategy.sort(data);
  }
}

// Usage
const sorter = new DataSorter(new AlphabeticalSort());
sorter.sort(data);
sorter.setStrategy(new PriceSort());
sorter.sort(data);
```

**Factory Pattern:**
```typescript
// ❌ Direct instantiation everywhere
const user = new User(data);
const admin = new Admin(data);
const guest = new Guest(data);

// Repeated logic in multiple places
if (data.role === 'admin') {
  return new Admin(data);
} else if (data.role === 'user') {
  return new User(data);
} else {
  return new Guest(data);
}

// ✅ Refactored: Factory pattern
interface User {
  role: string;
  permissions: string[];
  login(): void;
}

class RegularUser implements User {
  role = 'user';
  permissions = ['read'];
  constructor(private data: any) {}
  login() { /* User login logic */ }
}

class Admin implements User {
  role = 'admin';
  permissions = ['read', 'write', 'delete'];
  constructor(private data: any) {}
  login() { /* Admin login logic */ }
}

class Guest implements User {
  role = 'guest';
  permissions = [];
  constructor(private data: any) {}
  login() { /* Guest login logic */ }
}

class UserFactory {
  static create(data: any): User {
    switch (data.role) {
      case 'admin':
        return new Admin(data);
      case 'user':
        return new RegularUser(data);
      default:
        return new Guest(data);
    }
  }
}

// Usage
const user = UserFactory.create(data);
```

### 4. Performance Optimization

**Unnecessary Re-renders (React):**
```jsx
// ❌ Re-renders on every parent update
function UserList({ users, onDelete }) {
  return (
    <div>
      {users.map(user => (
        <UserCard 
          key={user.id} 
          user={user} 
          onDelete={() => onDelete(user.id)}  // New function every render
        />
      ))}
    </div>
  );
}

function UserCard({ user, onDelete }) {
  console.log('UserCard rendered'); // Logs on every parent update
  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={onDelete}>Delete</button>
    </div>
  );
}

// ✅ Refactored: Memoization
import { memo, useCallback } from 'react';

function UserList({ users, onDelete }) {
  const handleDelete = useCallback((userId) => {
    onDelete(userId);
  }, [onDelete]);

  return (
    <div>
      {users.map(user => (
        <UserCard 
          key={user.id} 
          user={user} 
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}

const UserCard = memo(({ user, onDelete }) => {
  console.log('UserCard rendered'); // Only logs when user changes
  
  const handleClick = useCallback(() => {
    onDelete(user.id);
  }, [user.id, onDelete]);
  
  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={handleClick}>Delete</button>
    </div>
  );
});
```

**N+1 Query Problem:**
```python
# ❌ N+1 queries
def get_users_with_posts():
    users = User.objects.all()  # 1 query
    result = []
    for user in users:
        posts = user.posts.all()  # N queries (one per user)
        result.append({
            'user': user,
            'posts': posts
        })
    return result

# ✅ Refactored: Eager loading
def get_users_with_posts():
    users = User.objects.prefetch_related('posts').all()  # 2 queries total
    return [{
        'user': user,
        'posts': user.posts.all()
    } for user in users]
```

**Inefficient Algorithms:**
```javascript
// ❌ O(n²) complexity
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}

// ✅ Refactored: O(n) complexity
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  
  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }
  
  return Array.from(duplicates);
}
```

### 5. Readability Improvements

**Complex Conditionals:**
```python
# ❌ Hard to read nested conditions
def can_access_resource(user, resource):
    if user:
        if user.is_active:
            if user.role == 'admin' or (user.role == 'user' and resource.owner_id == user.id):
                if not resource.is_deleted:
                    if resource.visibility == 'public' or user.id in resource.allowed_users:
                        return True
    return False

# ✅ Refactored: Early returns and extracted conditions
def can_access_resource(user, resource):
    if not user or not user.is_active:
        return False
    
    if resource.is_deleted:
        return False
    
    if user.role == 'admin':
        return True
    
    if resource.owner_id == user.id:
        return True
    
    if resource.visibility == 'public':
        return True
    
    return user.id in resource.allowed_users
```

**Magic Numbers:**
```javascript
// ❌ Magic numbers
function calculateDiscount(total) {
  if (total > 100) {
    return total * 0.1;
  } else if (total > 50) {
    return total * 0.05;
  }
  return 0;
}

setTimeout(() => {
  checkStatus();
}, 86400000);

// ✅ Refactored: Named constants
const DISCOUNT_TIERS = {
  PREMIUM_THRESHOLD: 100,
  PREMIUM_RATE: 0.1,
  STANDARD_THRESHOLD: 50,
  STANDARD_RATE: 0.05
};

const TIME_INTERVALS = {
  ONE_DAY_MS: 24 * 60 * 60 * 1000
};

function calculateDiscount(total) {
  if (total > DISCOUNT_TIERS.PREMIUM_THRESHOLD) {
    return total * DISCOUNT_TIERS.PREMIUM_RATE;
  } else if (total > DISCOUNT_TIERS.STANDARD_THRESHOLD) {
    return total * DISCOUNT_TIERS.STANDARD_RATE;
  }
  return 0;
}

setTimeout(() => {
  checkStatus();
}, TIME_INTERVALS.ONE_DAY_MS);
```

**Poor Naming:**
```typescript
// ❌ Unclear variable names
function calc(a: number, b: number): number {
  const x = a * b;
  const y = x * 0.08;
  const z = x + y;
  return z;
}

// ✅ Refactored: Descriptive names
function calculateOrderTotal(price: number, quantity: number): number {
  const subtotal = price * quantity;
  const tax = subtotal * 0.08;
  const totalWithTax = subtotal + tax;
  return totalWithTax;
}
```

### 6. Error Handling

**Silent Failures:**
```python
# ❌ Errors silently ignored
def fetch_user_data(user_id):
    try:
        response = api.get(f'/users/{user_id}')
        return response.json()
    except:
        return None  # What went wrong?

# ✅ Refactored: Proper error handling
class UserFetchError(Exception):
    pass

def fetch_user_data(user_id):
    try:
        response = api.get(f'/users/{user_id}')
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise UserFetchError(f"User {user_id} not found")
        raise UserFetchError(f"HTTP error: {e.response.status_code}")
    except requests.RequestException as e:
        raise UserFetchError(f"Network error: {str(e)}")
    except ValueError as e:
        raise UserFetchError(f"Invalid JSON response: {str(e)}")
```

**Try-Catch Overuse:**
```javascript
// ❌ Try-catch for control flow
function parseDate(dateString) {
  try {
    return new Date(dateString);
  } catch {
    try {
      return moment(dateString).toDate();
    } catch {
      try {
        return parseCustomFormat(dateString);
      } catch {
        return null;
      }
    }
  }
}

// ✅ Refactored: Validation before parsing
function parseDate(dateString) {
  if (!dateString) return null;
  
  // Try native Date first
  const nativeDate = new Date(dateString);
  if (!isNaN(nativeDate.getTime())) {
    return nativeDate;
  }
  
  // Try moment.js
  if (moment(dateString, moment.ISO_8601, true).isValid()) {
    return moment(dateString).toDate();
  }
  
  // Try custom format
  if (isCustomFormat(dateString)) {
    return parseCustomFormat(dateString);
  }
  
  return null;
}
```

### 7. Architecture Improvements

**Tight Coupling:**
```typescript
// ❌ Tightly coupled
class OrderService {
  processOrder(order: Order) {
    // Direct dependency on specific payment gateway
    const stripe = new StripeGateway(API_KEY);
    const payment = stripe.charge(order.total);
    
    // Direct dependency on specific email service
    const sendgrid = new SendGridClient(API_KEY);
    sendgrid.send({
      to: order.email,
      template: 'order_confirmation'
    });
    
    return { orderId: order.id, paymentId: payment.id };
  }
}

// ✅ Refactored: Dependency injection
interface PaymentGateway {
  charge(amount: number): Promise<Payment>;
}

interface EmailService {
  send(options: EmailOptions): Promise<void>;
}

class OrderService {
  constructor(
    private paymentGateway: PaymentGateway,
    private emailService: EmailService
  ) {}
  
  async processOrder(order: Order) {
    const payment = await this.paymentGateway.charge(order.total);
    
    await this.emailService.send({
      to: order.email,
      template: 'order_confirmation',
      data: { orderId: order.id }
    });
    
    return { orderId: order.id, paymentId: payment.id };
  }
}

// Usage with different implementations
const orderService = new OrderService(
  new StripeGateway(config.stripe),
  new SendGridClient(config.sendgrid)
);

// Easy to swap implementations
const testOrderService = new OrderService(
  new MockPaymentGateway(),
  new MockEmailService()
);
```

### 8. State Management

**Prop Drilling (React):**
```jsx
// ❌ Passing props through multiple levels
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} setUser={setUser} />;
}

function Layout({ user, setUser }) {
  return <Sidebar user={user} setUser={setUser} />;
}

function Sidebar({ user, setUser }) {
  return <UserMenu user={user} setUser={setUser} />;
}

function UserMenu({ user, setUser }) {
  return <div>{user?.name}</div>;
}

// ✅ Refactored: Context API
const UserContext = createContext();

function App() {
  const [user, setUser] = useState(null);
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout />
    </UserContext.Provider>
  );
}

function Layout() {
  return <Sidebar />;
}

function Sidebar() {
  return <UserMenu />;
}

function UserMenu() {
  const { user } = useContext(UserContext);
  return <div>{user?.name}</div>;
}
```

## REFACTOR_PLANNING.md Format

```markdown
# Refactoring Plan

**Generated**: 2026-02-14
**Scope**: Entire Codebase
**Framework**: React 18.2 + TypeScript
**Total Issues**: 23
**Estimated Time**: 4-6 hours

## Executive Summary

Current code health: **68/100** 🟡

**Critical Issues**: 3
**Major Issues**: 8
**Minor Issues**: 12

**Top 3 Priority Areas**:
1. Payment processing module (tight coupling, no error handling)
2. User management (God object pattern)
3. Data fetching layer (N+1 queries, no caching)

## Priority 1: Critical Refactorings (Do First)

### 1. Decouple Payment Processing
**File**: `src/services/PaymentService.ts`  
**Issue**: Tight coupling to Stripe, no abstraction  
**Impact**: Cannot test, cannot swap providers  
**Complexity**: High  
**Time**: 2 hours

**Current Code**:
```typescript
class PaymentService {
  async charge(amount: number) {
    const stripe = new Stripe(process.env.STRIPE_KEY);
    return stripe.charges.create({ amount });
  }
}
```

**Refactored Code**:
```typescript
interface PaymentGateway {
  charge(amount: number): Promise<PaymentResult>;
}

class StripeGateway implements PaymentGateway {
  constructor(private apiKey: string) {}
  
  async charge(amount: number): Promise<PaymentResult> {
    const stripe = new Stripe(this.apiKey);
    const charge = await stripe.charges.create({ amount });
    return { id: charge.id, status: charge.status };
  }
}

class PaymentService {
  constructor(private gateway: PaymentGateway) {}
  
  async charge(amount: number) {
    return this.gateway.charge(amount);
  }
}
```

**Benefits**:
- ✅ Testable (mock gateway)
- ✅ Swappable providers
- ✅ Follows dependency injection
- ✅ Better error handling

---

### 2. Break Up God Object: UserManager
**File**: `src/models/UserManager.ts`  
**Issue**: 800+ lines, handles auth, permissions, notifications, billing  
**Impact**: Hard to maintain, test, understand  
**Complexity**: High  
**Time**: 3 hours

**Refactoring Strategy**:
Split into:
- `User.ts` - Core user model
- `UserAuth.ts` - Authentication
- `UserPermissions.ts` - Authorization
- `UserNotifications.ts` - Email/SMS
- `UserBilling.ts` - Payment operations

**Files to Create**:
```
src/models/
├── User.ts (core data model)
├── UserAuth.ts
├── UserPermissions.ts
├── UserNotifications.ts
└── UserBilling.ts
```

**Migration Steps**:
1. Create new files with extracted code
2. Update User class to compose services
3. Update all imports across codebase
4. Remove old methods from User class
5. Run tests to verify

---

### 3. Fix N+1 Query Problem
**File**: `src/api/routes/users.ts`  
**Issue**: Loading posts in loop, 100+ queries for 100 users  
**Impact**: Page load 8+ seconds, database overload  
**Complexity**: Medium  
**Time**: 1 hour

**Current**:
```typescript
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findByUserId(user.id); // N queries
}
```

**Refactored**:
```typescript
const users = await User.findAll({
  include: [{ model: Post }]  // Single join query
});
```

**Performance Impact**:
- Before: 101 queries, 8.2s load time
- After: 1 query, 0.3s load time
- **27x faster** 🚀

---

## Priority 2: Major Refactorings (Important)

### 4. Extract Magic Numbers to Constants
**Files**: Multiple (15 files)  
**Issue**: Hardcoded values throughout codebase  
**Time**: 1 hour

**Examples to Fix**:
```typescript
// src/utils/validation.ts
if (password.length < 8) { } // ❌

// src/config/constants.ts
export const PASSWORD_MIN_LENGTH = 8;
// src/utils/validation.ts
if (password.length < PASSWORD_MIN_LENGTH) { } // ✅
```

**Files Affected**:
- `src/utils/validation.ts`
- `src/services/DiscountService.ts`
- `src/components/Pagination.tsx`
- ... (12 more)

---

### 5. Apply Strategy Pattern to Sorting
**File**: `src/utils/DataSorter.ts`  
**Issue**: Giant if-else chain for 8 sort types  
**Time**: 45 minutes

[... refactoring details ...]

---

### 6. Memoize React Components
**Files**: `src/components/UserCard.tsx`, `src/components/ProductCard.tsx` (8 components)  
**Issue**: Unnecessary re-renders degrading performance  
**Time**: 1 hour

[... refactoring details ...]

---

## Priority 3: Minor Refactorings (Nice to Have)

### 7. Improve Variable Naming
**Files**: 23 files  
**Issue**: Unclear names (x, data, temp, result)  
**Time**: 2 hours

**Examples**:
```typescript
function calc(a, b) { } // ❌
function calculateOrderTotal(price, quantity) { } // ✅
```

---

### 8. Add JSDoc Comments
**Files**: All service and util files  
**Issue**: No documentation  
**Time**: 2 hours

---

## Code Smell Detection

**Total Code Smells Found**: 47

### By Category:
- Long Methods: 8 instances
- Duplicate Code: 12 instances
- Large Classes: 3 instances
- Long Parameter List: 6 instances
- Feature Envy: 4 instances
- Data Clumps: 5 instances
- Primitive Obsession: 9 instances

### By File:
```
src/services/PaymentService.ts     ⚠️⚠️⚠️ (3 smells)
src/models/UserManager.ts          ⚠️⚠️⚠️⚠️⚠️ (5 smells)
src/utils/DataProcessor.ts         ⚠️⚠️ (2 smells)
```

## Design Pattern Opportunities

**Identified Patterns to Apply**:
1. **Strategy Pattern** - DataSorter, Validators (3 places)
2. **Factory Pattern** - User creation, Response builders (2 places)
3. **Observer Pattern** - Event handling, State updates (4 places)
4. **Decorator Pattern** - API middleware, Logging (2 places)

## Performance Optimizations

**Identified Opportunities**:

| File | Issue | Current | Optimized | Impact |
|------|-------|---------|-----------|--------|
| users.ts | N+1 queries | 8.2s | 0.3s | 🚀 High |
| UserCard.tsx | Re-renders | 45 FPS | 60 FPS | 🔵 Medium |
| DataProcessor.ts | O(n²) algorithm | 2.1s | 0.1s | 🚀 High |
| ProductList.tsx | No virtualization | 15 FPS | 60 FPS | 🚀 High |

## SOLID Principle Violations

**Single Responsibility**: 8 violations
- UserManager.ts
- OrderService.ts
- ReportGenerator.ts

**Open/Closed**: 3 violations
- PaymentProcessor.ts
- NotificationService.ts

**Liskov Substitution**: 0 violations ✅

**Interface Segregation**: 2 violations
- IUserService (too many methods)

**Dependency Inversion**: 5 violations
- Most services (tight coupling)

## Testing Considerations

**Before Refactoring**:
- Create comprehensive tests for affected code
- Ensure 80%+ coverage before changes
- Set up regression test suite

**After Refactoring**:
- All tests must pass
- No reduction in coverage
- Performance tests should show improvement

## Implementation Plan

### Phase 1: Critical (Week 1)
- [ ] Decouple PaymentService (2h)
- [ ] Break up UserManager (3h)
- [ ] Fix N+1 queries (1h)
- [ ] Run full test suite
- **Total**: 6 hours

### Phase 2: Major (Week 2)
- [ ] Extract magic numbers (1h)
- [ ] Apply Strategy pattern (45m)
- [ ] Memoize components (1h)
- [ ] Apply Factory pattern (1h)
- [ ] Run performance benchmarks
- **Total**: 3.75 hours

### Phase 3: Minor (Week 3)
- [ ] Improve naming (2h)
- [ ] Add documentation (2h)
- [ ] Code review and adjustments (1h)
- **Total**: 5 hours

### Phase 4: Validation (Week 3)
- [ ] Final test suite run
- [ ] Performance comparison
- [ ] Code review
- [ ] Deploy to staging
- **Total**: 2 hours

**Grand Total**: 16.75 hours over 3 weeks

## Rollback Plan

If refactoring causes issues:
1. Git revert to pre-refactoring commit
2. Review test failures
3. Apply fixes incrementally
4. Re-run affected tests

**Backup Strategy**:
- Create feature branch: `refactor/payment-service`
- Keep main branch stable
- Merge only after all tests pass

## Success Metrics

**Before Refactoring**:
- Code Health: 68/100
- Test Coverage: 72%
- Performance: 8.2s avg page load
- Cyclomatic Complexity: 18 avg
- Maintainability Index: 62

**After Refactoring** (Target):
- Code Health: 85/100 (+17)
- Test Coverage: 85% (+13%)
- Performance: 0.8s avg page load (-91%)
- Cyclomatic Complexity: 8 avg (-56%)
- Maintainability Index: 82 (+20)

## Tools & Commands

```bash
# Run tests
npm test

# Check coverage
npm test -- --coverage

# Lint code
npm run lint

# Type check
npm run type-check

# Performance test
npm run perf-test

# Build
npm run build
```

## Notes

- All refactorings preserve existing functionality
- No breaking API changes
- Backward compatibility maintained
- Feature flags available for gradual rollout
- Can pause/resume at any phase boundary

## Questions?

Contact the team or create a GitHub issue for clarification on any refactoring.
```

## Detection Rules

**Code Smells Detected:**
- Methods > 50 lines
- Classes > 500 lines
- Functions with > 5 parameters
- Cyclomatic complexity > 10
- Duplicate code blocks > 10 lines
- Nested conditionals > 3 levels

**Anti-Patterns Detected:**
- God objects
- Circular dependencies
- Tight coupling
- Global state
- Magic strings/numbers
- Callback hell

**SOLID Violations:**
- Classes with multiple responsibilities
- Modification needed for extension
- Improper inheritance
- Fat interfaces
- Concrete dependencies

## Framework-Specific Rules

### React
- Unnecessary re-renders
- Missing memoization
- Prop drilling
- Large components (> 300 lines)
- No error boundaries

### Node.js/Express
- Callback hell
- No async/await usage
- Missing error middleware
- No request validation
- Hardcoded configuration

### Python/Django
- Fat models
- Business logic in views
- No service layer
- Raw SQL instead of ORM
- Missing migrations

### Go
- Error shadowing
- Goroutine leaks
- No context usage
- Global variables
- Missing defer for cleanup

## Best Practices Enforced

✅ **DRY** - Don't Repeat Yourself  
✅ **KISS** - Keep It Simple, Stupid  
✅ **YAGNI** - You Aren't Gonna Need It  
✅ **SOLID** - Object-oriented design principles  
✅ **Separation of Concerns**  
✅ **Dependency Injection**  
✅ **Single Responsibility**  
✅ **Composition over Inheritance**  

## Output Messages

**Plan Creation:**
```
✅ Refactoring Plan Generated!

📋 Location: /project-root/REFACTOR_PLANNING.md

Summary:
- 23 refactoring opportunities
- Estimated impact: High
- Estimated time: 16.75 hours
- Code health: 68/100 → 85/100 (+17)

PLAN CREATED! 📋
```

**Implementation:**
```
✅ Refactoring Complete!

📊 Results:
- Files refactored: 28
- Code smells fixed: 47
- Performance improved: 91% faster
- Test coverage: 72% → 85%

Before:
  Code Health: 68/100
  Page Load: 8.2s
  Complexity: 18

After:
  Code Health: 85/100
  Page Load: 0.8s
  Complexity: 8

ALL DONE! 🎉
```

## Safety Guardrails

1. **Never refactor without tests** - If tests don't exist, create them first
2. **One refactoring at a time** - Apply incrementally
3. **Run tests after each change** - Catch regressions immediately
4. **Backup before major changes** - Use git branches
5. **Preserve functionality** - No behavior changes unless specified
6. **Document breaking changes** - If API changes, update docs

## When NOT to Refactor

❌ **Skip refactoring if:**
- Code works and has good tests
- Refactoring adds no value
- Time constraints prevent proper testing
- Team lacks familiarity with pattern
- External dependencies prevent changes
- Risks outweigh benefits

✅ **Refactor when:**
- Adding new features to messy code
- Bug fixes reveal deeper issues
- Performance problems identified
- Team struggles to understand code
- Test coverage is low
- Technical debt is accumulating
