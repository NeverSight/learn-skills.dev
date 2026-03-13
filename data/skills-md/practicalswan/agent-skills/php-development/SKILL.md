---
name: php-development
description: PHP 8.0+ development — XAMPP, RESTful APIs, PDO/MySQL/MariaDB, and authentication. Use when building PHP backends, creating API endpoints, configuring XAMPP, or integrating PHP with databases.
license: Complete terms in LICENSE.txt
---

# PHP Development

Expert guidance for building high-quality PHP applications with PHP 8.0+, PDO for secure database access, RESTful API design, and XAMPP environment configuration following official PHP documentation at https://php.net.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Core PHP Development:**
- Building PHP RESTful APIs with proper HTTP methods
- Working with XAMPP (Apache + MySQL + PHP) environment
- Implementing secure database operations with PDO
- Creating authentication and session management systems
- Handling file uploads and form submissions

**Database & Data Layer:**
- Connecting PHP to MySQL/MariaDB with PDO
- Writing prepared statements to prevent SQL injection
- Implementing transaction handling for data integrity
- Creating repository patterns for data access
- Working with MySQLi vs PDO comparisons

**Security & Best Practices:**
- Implementing password hashing (password_hash, password_verify)
- Securing against XSS, CSRF, and SQL injection
- Validating and sanitizing user input
- Managing sessions and authentication tokens
- Configuring CORS headers for API access

**API Development:**
- Designing RESTful endpoints with proper HTTP status codes
- Handling JSON requests and responses
- Implementing middleware for authentication and authorization
- Error handling and logging
- Rate limiting and API versioning

---

## Part 1: PHP 8.0+ Fundamentals

### Modern PHP Features

```php
<?php
// Named arguments (PHP 8.0+)
function createUser(string $name, string $email, bool $isAdmin = false): User {
    return new User($name, $email, $isAdmin);
}

// Call with named arguments
$user = createUser(email: 'user@example.com', name: 'John Doe');

// Union types (PHP 8.0+)
function processValue(string|int|float $value): string {
    return (string)$value;
}

// Nullsafe operator (PHP 8.0+)
$country = $session?->user?->address?->country ?? 'Unknown';

// Constructor property promotion (PHP 8.0+)
class User {
    public function __construct(
        public string $name,
        public string $email,
        private string $passwordHash
    ) {}
}
```

### Type Declarations & Strict Types

```php
<?php
declare(strict_types=1); // Enforce type safety

// Typed properties and return types
class Recipe {
    private int $id;
    private string $title;
    private ?DateTime $createdAt;

    public function __construct(int $id, string $title) {
        $this->id = $id;
        $this->title = $title;
    }

    public function getTitle(): string {
        return $this->title;
    }

    public function setCreatedAt(?DateTime $date): void {
        $this->createdAt = $date;
    }
}

// Union and intersection types
function processData(string|array $data): string|int {
    return is_array($data) ? count($data) : strlen($data);
}
```

---

## Part 2: PDO Database Integration

### Database Connection Class

```php
<?php
class Database {
    private static ?PDO $instance = null;

    public static function getInstance(): PDO {
        if (self::$instance === null) {
            $host = $_ENV['DB_HOST'] ?? 'localhost';
            $dbname = $_ENV['DB_NAME'] ?? 'recipe_sharing_system';
            $username = $_ENV['DB_USER'] ?? 'root';
            $password = $_ENV['DB_PASSWORD'] ?? '';
            $charset = 'utf8mb4';

            $dsn = "mysql:host=$host;dbname=$dbname;charset=$charset";

            try {
                self::$instance = new PDO($dsn, $username, $password, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::ATTR_EMULATE_PREPARES => false,
                ]);
            } catch (PDOException $e) {
                error_log("Database connection failed: " . $e->getMessage());
                throw new RuntimeException("Database connection error");
            }
        }

        return self::$instance;
    }
}
```

### Prepared Statements for Security

```php
<?php
class UserRepository {
    private PDO $db;

    public function __construct(PDO $db) {
        $this->db = $db;
    }

    // Find user by email with prepared statement
    public function findByEmail(string $email): ?array {
        $stmt = $this->db->prepare(
            "SELECT id, email, password_hash, role, status
             FROM user
             WHERE email = :email LIMIT 1"
        );

        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->execute();

        $user = $stmt->fetch();
        return $user ?: null;
    }

    // Create new user with password hashing
    public function create(string $name, string $email, string $password): int {
        $passwordHash = password_hash($password, PASSWORD_DEFAULT);

        $stmt = $this->db->prepare(
            "INSERT INTO user (name, email, password_hash, role, status, created_at, updated_at)
             VALUES (:name, :email, :password_hash, 'user', 'active', NOW(), NOW())"
        );

        $stmt->bindParam(':name', $name, PDO::PARAM_STR);
        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->bindParam(':password_hash', $passwordHash, PDO::PARAM_STR);

        $stmt->execute();

        return (int) $this->db->lastInsertId();
    }

    // Authentication with password verification
    public function authenticate(string $email, string $password): ?array {
        $user = $this->findByEmail($email);

        if ($user === null) {
            return null;
        }

        if (!password_verify($password, $user['password_hash'])) {
            return null;
        }

        // Check if password needs rehash
        if (password_needs_rehash($user['password_hash'], PASSWORD_DEFAULT)) {
            $newHash = password_hash($password, PASSWORD_DEFAULT);
            $this->updatePasswordHash($user['id'], $newHash);
        }

        unset($user['password_hash']); // Remove sensitive data
        return $user;
    }

    private function updatePasswordHash(int $userId, string $hash): void {
        $stmt = $this->db->prepare(
            "UPDATE user SET password_hash = :hash WHERE id = :id"
        );
        $stmt->execute([':hash' => $hash, ':id' => $userId]);
    }
}
```

### Transaction Management

```php
<?php
class RecipeService {
    private PDO $db;

    public function __construct(PDO $db) {
        $this->db = $db;
    }

    // Create recipe with ingredients, instructions, and images in a transaction
    public function createRecipeWithDetails(array $recipeData, array $ingredients, array $instructions): int {
        try {
            $this->db->beginTransaction();

            // Insert recipe
            $stmt = $this->db->prepare(
                "INSERT INTO recipe (title, description, category, difficulty, prep_time, cook_time, servings, author_id, status, created_at, updated_at)
                 VALUES (:title, :description, :category, :difficulty, :prep_time, :cook_time, :servings, :author_id, 'pending', NOW(), NOW())"
            );

            $stmt->execute([
                ':title' => $recipeData['title'],
                ':description' => $recipeData['description'],
                ':category' => $recipeData['category'],
                ':difficulty' => $recipeData['difficulty'],
                ':prep_time' => $recipeData['prepTime'],
                ':cook_time' => $recipeData['cookTime'],
                ':servings' => $recipeData['servings'],
                ':author_id' => $recipeData['authorId'],
            ]);

            $recipeId = (int) $this->db->lastInsertId();

            // Insert ingredients
            $ingredientStmt = $this->db->prepare(
                "INSERT INTO ingredient (recipe_id, name, quantity, unit, sort_order, created_at, updated_at)
                 VALUES (:recipe_id, :name, :quantity, :unit, :sort_order, NOW(), NOW())"
            );

            foreach ($ingredients as $index => $ingredient) {
                $ingredientStmt->execute([
                    ':recipe_id' => $recipeId,
                    ':name' => $ingredient['name'],
                    ':quantity' => $ingredient['quantity'],
                    ':unit' => $ingredient['unit'],
                    ':sort_order' => $index,
                ]);
            }

            // Insert instructions
            $instructionStmt = $this->db->prepare(
                "INSERT INTO instruction (recipe_id, step_number, instruction_text, created_at, updated_at)
                 VALUES (:recipe_id, :step_number, :instruction_text, NOW(), NOW())"
            );

            foreach ($instructions as $index => $instruction) {
                $instructionStmt->execute([
                    ':recipe_id' => $recipeId,
                    ':step_number' => $index + 1,
                    ':instruction_text' => $instruction['text'],
                ]);
            }

            $this->db->commit();

            return $recipeId;

        } catch (Exception $e) {
            $this->db->rollBack();
            error_log("Failed to create recipe: " . $e->getMessage());
            throw $e;
        }
    }
}
```

---

## Part 3: RESTful API Development

### JSON Response Helpers

```php
<?php
class Response {
    public static function json(mixed $data, int $statusCode = 200): never {
        http_response_code($statusCode);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES);
        exit;
    }

    public static function error(string $message, int $statusCode = 400): never {
        self::json([
            'success' => false,
            'error' => $message,
        ], $statusCode);
    }

    public static function success(mixed $data = null, string $message = 'Success'): never {
        self::json([
            'success' => true,
            'message' => $message,
            'data' => $data,
        ]);
    }
}
```

### CORS Middleware

```php
<?php
// Handle CORS headers
$allowedOrigins = [
    'http://localhost:5173', // Vite dev server
    'http://localhost:3000',  // Alternative dev server
];

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';

if (in_array($origin, $allowedOrigins, true)) {
    header("Access-Control-Allow-Origin: $origin");
}

header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Access-Control-Allow-Credentials: true');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}
```

### Authentication Middleware

```php
<?php
function requireAuth(): array {
    $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? '';

    if (!preg_match('/Bearer\s+(.*)$/i', $authHeader, $matches)) {
        Response::error('Unauthorized: Missing or invalid token', 401);
    }

    $token = $matches[1];

    // Validate token (example withJWT)
    try {
        $payload = JWT::decode($token, $_ENV['JWT_SECRET'], ['HS256']);
        return (array) $payload;
    } catch (Exception $e) {
        Response::error('Unauthorized: Invalid token', 401);
    }
}

function requireAdmin(): array {
    $user = requireAuth();

    if ($user['role'] !== 'admin') {
        Response::error('Forbidden: Admin access required', 403);
    }

    return $user;
}
```

### API Controller Example

```php
<?php
require_once '../../config/database.php';
require_once '../../middleware/cors.php';
require_once '../../utils/response.php';

class RecipeController {
    private PDO $db;

    public function __construct() {
        $this->db = Database::getInstance();
    }

    // GET /api/recipes - Get all published recipes
    public function index(): void {
        $category = $_GET['category'] ?? null;
        $difficulty = $_GET['difficulty'] ?? null;
        $search = $_GET['search'] ?? null;
        $limit = (int)($_GET['limit'] ?? 20);
        $offset = (int)($_GET['offset'] ?? 0);

        $query = "SELECT r.*, u.name as author_name,
                         COUNT(DISTINCT rv.id) as view_count,
                         COUNT(DISTINCT lr.id) as like_count,
                         AVG(rev.rating) as average_rating
                  FROM recipe r
                  JOIN user u ON r.author_id = u.id
                  LEFT JOIN recipe_view rv ON r.id = rv.recipe_id
                  LEFT JOIN like_record lr ON r.id = lr.recipe_id
                  LEFT JOIN review rev ON r.id = rev.recipe_id
                  WHERE r.status = 'published'";

        $params = [];

        if ($category !== null) {
            $query .= " AND r.category = :category";
            $params[':category'] = $category;
        }

        if ($difficulty !== null) {
            $query .= " AND r.difficulty = :difficulty";
            $params[':difficulty'] = $difficulty;
        }

        if ($search !== null) {
            $query .= " AND (r.title LIKE :search OR r.description LIKE :search)";
            $searchTerm = "%$search%";
            $params[':search'] = $searchTerm;
            $params[':search2'] = $searchTerm;
        }

        $query .= " GROUP BY r.id ORDER BY r.created_at DESC LIMIT :limit OFFSET :offset";

        $stmt = $this->db->prepare($query);
        $stmt->execute($params);

        $recipes = $stmt->fetchAll();

        Response::success($recipes);
    }

    // GET /api/recipes/:id - Get recipe by ID
    public function show(int $id): void {
        $stmt = $this->db->prepare(
            "SELECT r.*, u.name as author_name, u.email as author_email,
                    GROUP_CONCAT(CONCAT(i.name, ' (', i.quantity, ' ', i.unit, ')') SEPARATOR ', ') as ingredients
             FROM recipe r
             JOIN user u ON r.author_id = u.id
             LEFT JOIN ingredient i ON r.id = i.recipe_id
             WHERE r.id = :id
             GROUP BY r.id"
        );

        $stmt->execute([':id' => $id]);
        $recipe = $stmt->fetch();

        if ($recipe === false) {
            Response::error('Recipe not found', 404);
        }

        // Fetch instructions
        $instStmt = $this->db->prepare(
            "SELECT step_number, instruction_text
             FROM instruction
             WHERE recipe_id = :recipe_id
             ORDER BY step_number"
        );

        $instStmt->execute([':recipe_id' => $id]);
        $recipe['instructions'] = $instStmt->fetchAll();

        Response::success($recipe);
    }

    // POST /api/recipes - Create new recipe
    public function store(): void {
        $user = requireAuth();
        $data = json_decode(file_get_contents('php://input'), true);

        // Validate required fields
        if (empty($data['title']) || empty($data['description'])) {
            Response::error('Title and description are required');
        }

        $recipeData = [
            'title' => $data['title'],
            'description' => $data['description'],
            'category' => $data['category'] ?? 'Uncategorized',
            'difficulty' => $data['difficulty'] ?? 'Medium',
            'prepTime' => (int)($data['prepTime'] ?? 0),
            'cookTime' => (int)($data['cookTime'] ?? 0),
            'servings' => (int)($data['servings'] ?? 1),
            'authorId' => $user['id'],
        ];

        $recipeService = new RecipeService($this->db);

        try {
            $recipeId = $recipeService->createRecipeWithDetails(
                $recipeData,
                $data['ingredients'] ?? [],
                $data['instructions'] ?? []
            );

            Response::success(['id' => $recipeId], 'Recipe created successfully', 201);
        } catch (Exception $e) {
            Response::error('Failed to create recipe: ' . $e->getMessage(), 500);
        }
    }
}
```

---

## Part 4: Input Validation & Sanitization

### Validation Functions

```php
<?php
class Validator {
    public static function email(string $email): bool {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }

    public static function string(string $value, int $min = 1, int $max = 255): bool {
        $length = strlen($value);
        return $length >= $min && $length <= $max;
    }

    public static function integer(int $value, int $min = PHP_INT_MIN, int $max = PHP_INT_MAX): bool {
        return $value >= $min && $value <= $max;
    }

    public static function enum(string $value, array $allowed): bool {
        return in_array($value, $allowed, true);
    }

    public static function required(array $data, array $fields): array {
        $errors = [];
        foreach ($fields as $field) {
            if (empty($data[$field])) {
                $errors[] = "$field is required";
            }
        }
        return $errors;
    }

    public static function sanitize(string $input): string {
        return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
    }
}
```

### Validation Example

```php
<?php
function validateRecipeData(array $data): array {
    $errors = [];

    // Validate title
    if (empty($data['title'])) {
        $errors[] = 'Title is required';
    } elseif (!Validator::string($data['title'], 3, 200)) {
        $errors[] = 'Title must be between 3 and 200 characters';
    }

    // Validate email
    if (!empty($data['email']) && !Validator::email($data['email'])) {
        $errors[] = 'Invalid email address';
    }

    // Validate rating
    if (isset($data['rating']) && !Validator::integer((int)$data['rating'], 1, 5)) {
        $errors[] = 'Rating must be between 1 and 5';
    }

    // Validate difficulty
    if (!empty($data['difficulty']) &&
        !Validator::enum($data['difficulty'], ['Easy', 'Medium', 'Hard'])) {
        $errors[] = 'Difficulty must be Easy, Medium, or Hard';
    }

    // Sanitize all string inputs
    foreach ($data as $key => $value) {
        if (is_string($value)) {
            $data[$key] = Validator::sanitize($value);
        }
    }

    return ['errors' => $errors, 'data' => $data];
}
```

---

## Part 5: Security Best Practices

### Password Management

```php
<?php
class PasswordManager {
    public static function hash(string $password): string {
        // Use algorithm recommended by PHP
        return password_hash($password, PASSWORD_DEFAULT);
    }

    public static function verify(string $password, string $hash): bool {
        return password_verify($password, $hash);
    }

    public static function needsRehash(string $hash): bool {
        return password_needs_rehash($hash, PASSWORD_DEFAULT);
    }

    public static function validateStrength(string $password): array {
        $errors = [];

        if (strlen($password) < 8) {
            $errors[] = 'Password must be at least 8 characters';
        }

        if (!preg_match('/[A-Z]/', $password)) {
            $errors[] = 'Password must contain at least one uppercase letter';
        }

        if (!preg_match('/[a-z]/', $password)) {
            $errors[] = 'Password must contain at least one lowercase letter';
        }

        if (!preg_match('/[0-9]/', $password)) {
            $errors[] = 'Password must contain at least one number';
        }

        if (!preg_match('/[!@#$%^&*(),.?":{}|<>]/', $password)) {
            $errors[] = 'Password must contain at least one special character';
        }

        return $errors;
    }
}
```

### Session Management

```php
<?php
class Session {
    public static function start(): void {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }

    public static function set(string $key, mixed $value): void {
        $_SESSION[$key] = $value;
    }

    public static function get(string $key, mixed $default = null): mixed {
        return $_SESSION[$key] ?? $default;
    }

    public static function remove(string $key): void {
        unset($_SESSION[$key]);
    }

    public static function destroy(): void {
        $_SESSION = [];
        session_destroy();
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $params["path"], $params["domain"],
                $params["secure"], $params["httponly"]
            );
        }
    }

    public static function regenerateId(): void {
        session_regenerate_id(true);
    }
}
```

### CSRF Protection

```php
<?php
class CsrfProtection {
    public static function generateToken(): string {
        if (!isset($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    public static function validateToken(string $token): bool {
        return isset($_SESSION['csrf_token']) &&
               hash_equals($_SESSION['csrf_token'], $token);
    }

    public static function invalidateToken(): void {
        unset($_SESSION['csrf_token']);
    }

    public static function getInputField(): string {
        $token = self::generateToken();
        return "<input type='hidden' name='csrf_token' value='$token'>";
    }
}
```

---

## Part 6: XAMPP Configuration

### `.htaccess` for URL Rewriting

```apache
RewriteEngine On

# Redirect trailing slashes
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} (.+)/$
RewriteRule ^ %1 [L,R=301]

# Handle API routes
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^api/(.*)$ api/index.php [QSA,L]

# Handle frontend routes (SPA)
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.html [QSA,L]
```

### PHP Configuration (php.ini)

```ini
; Enable error reporting for development
error_reporting = E_ALL
display_errors = On
display_startup_errors = On

; Log errors in production
log_errors = On
error_log = "C:/xampp/php/logs/php_error.log"

; Increase upload limits
upload_max_filesize = 10M
post_max_size = 10M

; Enable PDO extensions
extension=pdo_mysql
extension=mysqli

; Enable session handling
session.save_handler = files
session.save_path = "C:/xampp/tmp"
session.use_strict_mode = 1
session.cookie_httponly = 1
session.cookie_secure = 0  ; Set to 1 if HTTPS
session.use_only_cookies = 1

; Set timezone
date.timezone = "Asia/Bangkok"
```

---

## PHP Development Best Practices

### Code Style (PSR-12)
- [ ] Use strict types (`declare(strict_types=1)`)
- [ ] Follow PSR-12 coding standards
- [ ] Use type hints for all functions and methods
- [ ] Use namespaces for autoloading classes
- [ ] Exception handling with try-catch blocks

### Security
- [ ] Always use prepared statements with PDO
- [ ] Hash passwords with `password_hash()`
- [ ] Validate all user input
- [ ] Sanitize output for XSS prevention
- [ ] Use HTTPS in production
- [ ] Implement CSRF protection

### API Design
- [ ] Use proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- [ ] Return JSON responses
- [ ] Handle CORS headers
- [ ] Implement authentication middleware
- [ ] Rate limit endpoints

### Database
- [ ] Use PDO for database connections
- [ ] Implement transactions for multi-step operations
- [ ] Use named parameters in prepared statements
- [ ] Handle connection errors gracefully
- [ ] Close connections properly

---

## References & Resources

### Documentation
- [PHP 8.4+ API Patterns](./references/php-8-4-api-patterns-2026.md) — Modern PHP API development patterns

### Examples
- [PDO Database Patterns](./examples/pdo-database-patterns.php) — PHP PDO database integration examples

### Scripts
- [XAMPP Setup Script](./scripts/xampp-setup.ps1) — PowerShell script to configure XAMPP for PHP development

### Official Documentation
- [PHP Manual](https://www.php.net/manual/en/) — Complete PHP reference
- [ PDO for MySQL](https://www.php.net/manual/en/pdo_mysql.php) — PDO MySQL driver documentation
- [Password Hashing](https://www.php.net/manual/en/book.password.php) — Secure password functions
- [REST API Best Practices](https://restfulapi.net/) — API design principles

### PHP Standards
- [PSR-12: Extended Coding Style](https://www.php-fig.org/psr/psr-12/) — Modern PHP coding style
- [XAMPP Documentation](https://www.apachefriends.org/) — XAMPP setup and configuration

### Security Resources
- [OWASP PHP Security](https://owasp.org/www-community/attacks/xss/) — XSS prevention
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — SQL injection prevention
- [PHP Security Guide](https://www.php.net/manual/en/security.php) — Official PHP security considerations


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [sql-development](../sql-development/SKILL.md) | SQL database integration with PHP/PDO |
| [nestjs](../nestjs/SKILL.md) | Alternative Node.js backend framework |
| [javascript-development](../javascript-development/SKILL.md) | Frontend JS to pair with PHP backend |
