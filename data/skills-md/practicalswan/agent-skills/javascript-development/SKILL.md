---
name: javascript-development
description: JavaScript/TypeScript ES2024+, async/await, DOM manipulation, Node.js, and API integration. Use when writing vanilla JS/TS code, working with REST/fetch APIs, implementing frontend logic, or configuring JS build tools.
license: Complete terms in LICENSE.txt
---

# JavaScript Development

Expert guidance for writing modern JavaScript code with ES2024+ features, async programming patterns, DOM manipulation, API integration, and best practices following official JavaScript resources at https://developer.mozilla.org/en-US/docs/Web/JavaScript.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Core JavaScript Development:**
- Writing modern JavaScript with ES2024+ features
- Creating React components and hooks
- Working with DOM manipulation and events
- Implementing forms and user interactions
- Managing state in frontend applications

**Asynchronous Programming:**
- Using Promises and async/await patterns
- Fetching data from APIs
- Handling loading and error states
- Implementing retry mechanisms
- Working with concurrent operations

**Data Handling:**
- Manipulating arrays and objects
- Using modern array methods (map, filter, reduce, find)
- Working with JSON data
- LocalStorage and session management
- Data transformation and formatting

**API Integration:**
- Fetch API for HTTP requests
- Axios for advanced HTTP client features
- RESTful API design and consumption
- Authentication with JWT tokens
- CORS and error handling

---

## Part 1: Modern JavaScript (ES2024+)

### New Features & Syntax

```javascript
// Logical Assignment Operators (ES2021)
const obj = { a: 1 };
obj.a ??= 10;  // Only assign if obj.a is null/undefined
console.log(obj.a); // 1 (no change)

obj.b ??= 20;  // Assign if missing
console.log(obj.b); // 20

// Numeric Separators (ES2021)
const billion = 1_000_000_000;
const bytes = 0xff_13_ff; // Hex

// String methods (ES2022)
const str = "Hello World";
console.log(str.replaceAll('l', 'L')); // "HeLLo WorLd"
console.log(str.at(-1)); // "d" (last character)

// Array methods (ES2023)
const array = [1, 2, 3, 4, 5];
console.log(array.toReversed()); // [5, 4, 3, 2, 1]
console.log(array.toSorted()); // [1, 2, 3, 4, 5]
console.log(array.with(2, 99)); // [1, 2, 99, 4, 5] (non-mutating)

// Hashbang (for scripts)
#!/usr/bin/env node
console.log("Executable script!");

// Object.groupBy (ES2024)
const people = [
    { name: "Alice", age: 25, role: "admin" },
    { name: "Bob", age: 30, role: "user" },
    { name: "Charlie", age: 25, role: "user" },
];

const groupedByAge = Object.groupBy(people, ({ age }) => age);
console.log(groupedByAge);
// { 25: [{name: "Alice", age: 25, role: "admin"}, ...], 30: [...] }

const groupedByRole = Map.groupBy(people, ({ role }) => role);
console.log(groupedByRole);
// Map { "admin" => [...], "user" => [...] }
```

### Template Literals & Tagged Templates

```javascript
// Template literals with expressions
const firstName = "John";
const lastName = "Doe";
const greeting = `Hello, ${firstName} ${lastName}!`;

// Tagged template for custom formatting
function highlight(strings, ...values) {
    return strings.reduce((result, str, i) => {
        return result + str + (values[i] ? `<strong>${values[i]}</strong>` : '');
    }, '');
}

const message = highlight`User ${firstName} is online.`;
// "User <strong>John</strong> is online."
```

### Destructuring & Spread

```javascript
// Object destructuring
const user = { id: 1, name: "Alice", email: "alice@example.com", role: "admin" };
const { name, email, role: userRole } = user;
console.log(name, email, userRole); // "Alice", "alice@example.com", "admin"

// Array destructuring
const numbers = [1, 2, 3, 4, 5];
const [first, second, ...rest] = numbers;
console.log(first, second, rest); // 1, 2, [3, 4, 5]

// Destructuring in function parameters
function processRecipe({ title, difficulty, ingredients = [] }) {
    return `${title} (${difficulty}) - ${ingredients.length} ingredients`;
}

const recipe = { title: "Pasta", difficulty: "Medium", ingredients: ["Pasta", "Sauce"] };
processRecipe(recipe); // "Pasta (Medium) - 2 ingredients"
```

---

## Part 2: Async Programming

### Async/Await Patterns

```javascript
// Basic async/await
async function fetchUser(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const user = await response.json();
        return user;
    } catch (error) {
        console.error("Failed to fetch user:", error);
        throw error;
    }
}

// Parallel async operations with Promise.all
async function fetchRecipeData(recipeId) {
    try {
        const [recipe, reviews, ingredients] = await Promise.all([
            fetch(`/api/recipes/${recipeId}`).then(r => r.json()),
            fetch(`/api/recipes/${recipeId}/reviews`).then(r => r.json()),
            fetch(`/api/recipes/${recipeId}/ingredients`).then(r => r.json()),
        ]);

        return { recipe, reviews, ingredients };
    } catch (error) {
        console.error("Failed to fetch recipe data:", error);
        throw error;
    }
}

// Race with Promise.any (ES2021)
async function fetchFromMultipleEndpoints() {
    const endpoints = [
        '/api/v1/users',
        '/api/v2/users',
        '/api/v3/users',
    ];

    try {
        const response = await Promise.any(
            endpoints.map(url => fetch(url).then(r => r.json()))
        );
        return response;
    } catch (error) {
        // All promises rejected
        console.error("All endpoints failed:", error);
        throw error;
    }
}

// All Settled (ES2020)
async function fetchWithStatus() {
    const requests = [
        fetch('/api/users'),
        fetch('/api/recipes'),
        fetch('/api/stats'),
    ];

    const results = await Promise.allSettled(requests);

    results.forEach((result, index) => {
        if (result.status === 'fulfilled') {
            console.log(`Request ${index} successful`);
        } else {
            console.error(`Request ${index} failed:`, result.reason);
        }
    });
}
```

### Async Iterator (ES2018)

```javascript
// Async generator function
async function* fetchPaginatedUsers(pageSize = 10) {
    let page = 1;
    let hasMore = true;

    while (hasMore) {
        const response = await fetch(`/api/users?page=${page}&limit=${pageSize}`);
        const { users, totalPages } = await response.json();

        yield* users;

        page++;
        hasMore = page <= totalPages;

        // Add delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

// Using async iterator
async function getAllUsers() {
    const userIterator = fetchPaginatedUsers();
    const allUsers = [];

    for await (const user of userIterator) {
        allUsers.push(user);
        console.log(`Fetched: ${user.name}`);
    }

    return allUsers;
}
```

### Top-level Await (ES2022)

```javascript
// In ES modules, you can use await at top level
const config = await fetch('/api/config').then(r => r.json());
console.log('App config loaded:', config);

// This is useful for modules that need to load data before export
export const recipes = await fetch('/api/recipes').then(r => r.json());
export const users = await fetch('/api/users').then(r => r.json());
```

---

## Part 3: API Integration

### Fetch API Patterns

```javascript
// Basic GET request
async function getRecipes(filters = {}) {
    const queryParams = new URLSearchParams(filters);
    const url = `/api/recipes?${queryParams}`;

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }

    return await response.json();
}

// POST request with JSON body
async function createRecipe(recipeData) {
    const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify(recipeData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to create recipe');
    }

    return await response.json();
}

// PUT request with authentication
async function updateRecipe(recipeId, recipeData, token) {
    const response = await fetch(`/api/recipes/${recipeId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(recipeData),
    });

    if (!response.status === 200 && response.status !== 204) {
        throw new Error(`Update failed: ${response.status}`);
    }

    return await response.json();
}

// DELETE request
async function deleteRecipe(recipeId, token) {
    const response = await fetch(`/api/recipes/${recipeId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error(`Delete failed: ${response.status}`);
    }

    return true;
}
```

### Axios Integration

```javascript
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding authentication
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Unauthorized - redirect to login
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// API methods
export const recipesApi = {
    async getAll(filters = {}) {
        const response = await api.get('/recipes', { params: filters });
        return response.data;
    },

    async getById(recipeId) {
        const response = await api.get(`/recipes/${recipeId}`);
        return response.data;
    },

    async create(recipeData) {
        const response = await api.post('/recipes', recipeData);
        return response.data;
    },

    async update(recipeId, recipeData) {
        const response = await api.put(`/recipes/${recipeId}`, recipeData);
        return response.data;
    },

    async delete(recipeId) {
        const response = await api.delete(`/recipes/${recipeId}`);
        return response.data;
    },
};
```

### Error Handling & Retry

```javascript
// Retry utility with exponential backoff
async function fetchWithRetry(url, options = {}, maxRetries = 3) {
    let lastError;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        } catch (error) {
            lastError = error;
            console.log(`Attempt ${attempt + 1} failed, retrying...`);

            // Exponential backoff: 1s, 2s, 4s
            const delay = Math.pow(2, attempt) * 1000;
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    throw new Error(`Failed after ${maxRetries} attempts: ${lastError.message}`);
}

// Usage with error handling
async function getRecipeWithRetry(recipeId) {
    try {
        const recipe = await fetchWithRetry(`/api/recipes/${recipeId}`);
        console.log('Recipe loaded:', recipe);
        return recipe;
    } catch (error) {
        console.error('Failed to load recipe:', error);
        // Show user-friendly error message
        return { error: true, message: 'Failed to load recipe. Please try again.' };
    }
}
```

---

## Part 4: DOM Manipulation & Events

### Element Selection & Manipulation

```javascript
// Modern element selection
const button = document.querySelector('#submit-btn');
const items = document.querySelectorAll('.list-item');
const container = document.getElementById('container');
const firstChild = document.querySelector('.item:first-child');

// Using closest for event delegation
document.addEventListener('click', (event) => {
    const button = event.target.closest('.action-button');
    if (button) {
        console.log('Button clicked:', button.dataset.id);
    }
});

// Element creation and manipulation
function addRecipeToList(recipe) {
    const li = document.createElement('li');
    li.className = 'recipe-item';
    li.dataset.recipeId = recipe.id;

    li.innerHTML = `
        <h3>${recipe.title}</h3>
        <p>${recipe.description}</p>
        <button class="delete-btn">Delete</button>
    `;

    // Add event listener to delete button
    const deleteBtn = li.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', () => deleteRecipe(recipe.id));

    // Append to container
    document.getElementById('recipe-list').appendChild(li);
}

// Element removal
function removeRecipeElement(recipeId) {
    const element = document.querySelector(`[data-recipe-id="${recipeId}"]`);
    if (element) {
        element.remove();
    }
}
```

### Event Handling

```javascript
// Form submission with validation
const form = document.getElementById('recipe-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(form);
    const recipeData = {
        title: formData.get('title'),
        description: formData.get('description'),
        category: formData.get('category'),
        difficulty: formData.get('difficulty'),
    };

    // Validation
    if (!recipeData.title || recipeData.title.length < 3) {
        showError('Title is required and must be at least 3 characters');
        return;
    }

    try {
        // Submit to API
        const response = await fetch('/api/recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(recipeData),
        });

        if (response.ok) {
            showSuccess('Recipe created successfully!');
            form.reset();
        }
    } catch (error) {
        showError('Failed to create recipe: ' + error.message);
    }
});

// Debounce for search input
let searchTimeout;
const searchInput = document.getElementById('search');

searchInput.addEventListener('input', (event) => {
    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
        const query = event.target.value;
        if (query.length >= 2) {
            performSearch(query);
        }
    }, 300); // Wait 300ms after user stops typing
});

// Intersection Observer for infinite scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            loadMoreRecipes();
        }
    });
}, {
    root: null,
    threshold: 0.1,
});

// Observe sentinel element
const sentinel = document.getElementById('load-more-sentinel');
observer.observe(sentinel);
```

---

## Part 5: Data Structures & Algorithms

### Array Methods

```javascript
// map - Transform array
const recipes = [
    { title: 'Pasta', difficulty: 'Medium' },
    { title: 'Salad', difficulty: 'Easy' },
];

const titles = recipes.map(recipe => recipe.title);
// ['Pasta', 'Salad']

// filter - Select elements
const easyRecipes = recipes.filter(recipe => recipe.difficulty === 'Easy');
// [{ title: 'Salad', difficulty: 'Easy' }]

// reduce - Aggregate array
const wordCount = recipes.reduce((count, recipe) => {
    return count + recipe.title.split(' ').length;
}, 0);

// find - Find first matching element
const pasta = recipes.find(recipe => recipe.title.includes('Pasta'));

// some - Check if any matches
const hasMediumDifficulty = recipes.some(recipe => recipe.difficulty === 'Medium'); // true

// every - Check if all match
const allHaveTitles = recipes.every(recipe => recipe.title.length > 0); // true

// sort - Sort array
const sortedRecipes = [...recipes].sort((a, b) =>
    a.title.localeCompare(b.title)
);

// flatMap - Map and flatten
const nested = [[1, 2], [3, 4]];
const flattened = nested.flatMap(arr => arr); // [1, 2, 3, 4]
```

### Object Methods

```javascript
// Object.keys, Object.values, Object.entries
const user = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    role: 'admin',
};

const keys = Object.keys(user); // ['id', 'name', 'email', 'role']
const values = Object.values(user); // [1, 'Alice', 'alice@example.com', 'admin']
const entries = Object.entries(user);
// [['id', 1], ['name', 'Alice'], ['email', 'alice@example.com'], ['role', 'admin']]

// Object.fromEntries - Convert back to object
const filtered = Object.fromEntries(
    Object.entries(user).filter(([key]) => key !== 'role')
);
// { id: 1, name: 'Alice', email: 'alice@example.com' }

// Object.freeze - Make immutable
const config = Object.freeze({ apiUrl: '/api/v1' });
config.apiUrl = '/api/v2'; // Error in strict mode
```

### Set and Map

```javascript
// Set - Unique values
const tags = new Set(['Easy', 'Medium', 'Medium', 'Hard']);
console.log(tags.size); // 3

tags.add('Easy');
 console.log(tags.has('Medium')); // true

tags.delete('Hard');

const uniqueTags = Array.from(tags); // ['Easy', 'Medium']

// Map - Key-value pairs with any type
const userRoles = new Map();
userRoles.set(1, 'admin');
userRoles.set(2, 'user');
userRoles.set('alice', 'editor');

console.log(userRoles.get(1)); // 'admin'
console.log(userRoles.has('alice')); // true

const roles = Array.from(userRoles.entries());
// [[1, 'admin'], [2, 'user'], ['alice', 'editor']]
```

---

## Part 6: Date & Time

### Date Operations

```javascript
// Creating dates
const now = new Date();
const specificDate = new Date('2024-02-01');
const fromTimestamp = new Date(17068896000000);

// Date formatting
function formatDate(date) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    };
    return new Intl.DateTimeFormat('en-US', options).format(date);
}
// "February 1, 2024 at 12:00 PM"

// Relative time (e.g., "2 hours ago")
function getRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) return 'just now';
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    return `${days} day${days > 1 ? 's' : ''} ago`;
}

// Date manipulation
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function isSameDay(date1, date2) {
    return date1.toDateString() === date2.toDateString();
}
```

---

## Part 7: LocalStorage & State Management

### LocalStorage Wrapper

```javascript
class StorageManager {
    static set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Failed to save to localStorage:', error);
        }
    }

    static get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Failed to read from localStorage:', error);
            return defaultValue;
        }
    }

    static remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Failed to remove from localStorage:', error);
        }
    }

    static clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Failed to clear localStorage:', error);
        }
    }

    static has(key) {
        return localStorage.getItem(key) !== null;
    }
}
```

### State Management (Simple)

```javascript
class StateManager {
    constructor(initialState = {}) {
        this.state = initialState;
        this.listeners = [];
    }

    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.notify();
    }

    subscribe(listener) {
        this.listeners.push(listener);
        listener(this.state);
    }

    notify() {
        this.listeners.forEach(listener => listener(this.state));
    }
}

// Usage
const stateManager = new StateManager({
    user: null,
    recipes: [],
    loading: false,
});

stateManager.subscribe((state) => {
    console.log('State updated:', state);
    // Update UI
});

stateManager.setState({ recipes: [...] });
```

---

## Part 8: Utility Functions

### Common Utilities

```javascript
// Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Random ID
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

// Slugify text
function slugify(text) {
    return text
        .toString()
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '');
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Truncate text
function truncate(text, maxLength) {
    return text.length > maxLength
        ? text.substring(0, maxLength - 3) + '...'
        : text;
}
```

---

## JavaScript Development Best Practices

### Code Quality
- [ ] Use `const` and `let` instead of `var`
- [ ] Use strict mode (`'use strict'`)
- [ ] Add JSDoc comments for functions
- [ ] Use modern ES2024+ features
- [ ] Avoid global variables
- [ ] Use meaningful variable and function names

### Asynchronous Code
- [ ] Prefer async/await over .then() chains
- [ ] Handle errors with try-catch
- [ ] Use Promise.all for parallel operations
- [ ] Implement retry logic for network requests
- [ ] Provide loading states for async operations

### DOM & Events
- [ ] Use event delegation for dynamic content
- [ ] Clean up event listeners to prevent memory leaks
- [ ] Use dataset for custom data attributes
- [ ] Validate form input before submission
- [ ] Use debouncing/throttling for rapid events

### Performance
- [ ] Minimize DOM manipulation
- [ ] Use document fragments for bulk inserts
- [ ] Implement lazy loading for images/lists
- [ ] Cache expensive computations
- [ ] Use requestAnimationFrame for animations

### Security
- [ ] Sanitize user input to prevent XSS
- [ ] Use HTTPS for API calls
- [ ] Store tokens securely (HttpOnly cookies)
- [ ] Validate data from localStorage
- [ ] Implement CSRF protection

---

## References & Resources

### Official Documentation
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript) — Complete JavaScript reference
- [ECMAScript 2024 Spec](https://tc39.es/ecma262/) — Latest language specification
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) — HTTP requests with Fetch
- [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Storage) — LocalStorage and SessionStorage

### Libraries & Tools
- [Axios Documentation](https://axios-http.com/) — Popular HTTP client library
- [Vite Documentation](https://vitejs.dev/) — Build tool for modern web apps
- [ESLint](https://eslint.org/) — Code linting for JavaScript
- [Prettier](https://prettier.io/) — Code formatting tool

### Learning Resources
- [JavaScript.info](https://javascript.info/) — Modern JavaScript tutorial
- [JavaScript 30](https://javascript30.com/) — 30-day JavaScript challenge
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS) — Deep dive into JavaScript


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [react-development](../react-development/SKILL.md) | React component and hook patterns |
| [vite-development](../vite-development/SKILL.md) | Build tooling for JS projects |
| [nestjs](../nestjs/SKILL.md) | Server-side JS with NestJS framework |
| [web-testing](../web-testing/SKILL.md) | Test JS apps with Playwright and DevTools |
