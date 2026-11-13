---
name: security-authentication
description: >
  Use when configuring Symfony Security — firewalls, authenticators, the User entity,
  password hashing, access control, and voters. Use when the task mentions login,
  authentication, authorization, roles, voter, firewall, or password.
---

# Symfony Security: Authentication & Authorization

## The User entity

```php
#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
#[ORM\UniqueConstraint(name: 'uniq_users_email', fields: ['email'])]
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[ORM\Id, ORM\Column(type: UuidType::NAME, unique: true)]
    private Uuid $id;

    #[ORM\Column(length: 180, unique: true)]
    private string $email;

    /** @var string[] */
    #[ORM\Column]
    private array $roles = [];

    #[ORM\Column]                          // the *hash*, never the plaintext
    private string $password;

    public function __construct(string $email)
    {
        $this->id = Uuid::v7();
        $this->email = $email;
    }

    public function getUserIdentifier(): string { return $this->email; }

    /** @return string[] */
    public function getRoles(): array
    {
        $roles = $this->roles;
        $roles[] = 'ROLE_USER';            // everyone is at least ROLE_USER
        return array_unique($roles);
    }

    public function getPassword(): string { return $this->password; }

    public function setHashedPassword(string $hash): void { $this->password = $hash; }

    public function eraseCredentials(): void { /* no plaintext held */ }
}
```

## Password hashing — never roll your own

Use the hasher service; configure `auto` so Symfony picks the best algorithm (currently bcrypt/argon2) and can rehash on upgrade.

```yaml
# config/packages/security.yaml
security:
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'
```

```php
// Hashing at registration
$user->setHashedPassword($this->passwordHasher->hashPassword($user, $plainPassword));
```

```php
// ❌ NEVER
$user->setPassword(md5($plain));          // broken
$user->setPassword(hash('sha256', $plain)); // unsalted, fast = crackable
```

## Firewalls & access control

```yaml
security:
    providers:
        app_user_provider:
            entity: { class: App\Entity\User, property: email }

    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        api:
            pattern: ^/api
            stateless: true                 # APIs are stateless (token auth)
            provider: app_user_provider
            jwt: ~                          # see jwt-authentication
        main:
            lazy: true
            provider: app_user_provider

    access_control:
        - { path: ^/api/login,  roles: PUBLIC_ACCESS }
        - { path: ^/api/admin,  roles: ROLE_ADMIN }
        - { path: ^/api,        roles: ROLE_USER }
```

`access_control` is coarse-grained (path + role). For per-object decisions, use **voters**.

## Custom authenticator (when the built-ins don't fit)

```php
final class ApiKeyAuthenticator extends AbstractAuthenticator
{
    public function __construct(private readonly UserRepository $users) {}

    public function supports(Request $request): ?bool
    {
        return $request->headers->has('X-API-KEY');
    }

    public function authenticate(Request $request): Passport
    {
        $apiKey = $request->headers->get('X-API-KEY');
        if (!$apiKey) {
            throw new CustomUserMessageAuthenticationException('No API key provided');
        }

        return new SelfValidatingPassport(
            new UserBadge($apiKey, fn (string $key) => $this->users->findByApiKey($key)),
        );
    }

    public function onAuthenticationFailure(Request $request, AuthenticationException $e): Response
    {
        return new JsonResponse(['title' => 'Authentication failed'], Response::HTTP_UNAUTHORIZED);
    }

    public function onAuthenticationSuccess(Request $request, TokenInterface $token, string $firewallName): ?Response
    {
        return null; // continue the request
    }
}
```

## Voters for object-level authorization

Authorization that depends on the *specific object* (owner, tenant, state) belongs in a voter, not in `access_control` or scattered `if` checks.

```php
/** @extends Voter<string, Order> */
final class OrderVoter extends Voter
{
    public const VIEW = 'ORDER_VIEW';
    public const CANCEL = 'ORDER_CANCEL';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::VIEW, self::CANCEL], true) && $subject instanceof Order;
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        if (!$user instanceof User) {
            return false;
        }

        return match ($attribute) {
            self::VIEW   => $subject->getCustomerEmail() === $user->getUserIdentifier(),
            self::CANCEL => $subject->getCustomerEmail() === $user->getUserIdentifier()
                            && $subject->getStatus() === OrderStatus::Pending,
            default      => false,
        };
    }
}
```

```php
// In the controller / handler
$this->denyAccessUnlessGranted(OrderVoter::CANCEL, $order);
```

## Conventions

- `stateless: true` for API firewalls — no session cookie.
- Check authorization as close to the action as possible (`#[IsGranted]` attribute or `denyAccessUnlessGranted`).
- Return **401** for unauthenticated, **403** for authenticated-but-forbidden.
- Never trust `$request` for identity — read the authenticated user from the token / `#[CurrentUser]`.
- Enforce CSRF protection on session-based browser forms; stateless token APIs don't need it.

## Gotchas

- Agent hashes passwords with `md5`/`sha1`/`sha256` — use the `password_hasher` (`auto`).
- Agent stores or logs plaintext passwords — only the hash is persisted; `eraseCredentials()` clears any plaintext.
- Agent puts owner/tenant checks in `access_control` or inline `if` — use a voter for object-level rules.
- Agent makes the API firewall stateful (session) — set `stateless: true`.
- Agent reads the user id from a request param/body — use the authenticated token / `#[CurrentUser]`.
- Agent returns `403` for unauthenticated requests (or `401` for forbidden) — 401 = who are you, 403 = not allowed.
- Agent forgets `ROLE_USER` default in `getRoles()` — every authenticated user should have it.
- Agent writes a custom login form auth from scratch — use `form_login` / the built-in authenticators, or `json_login` for APIs.
