---
name: playwright-testing
description: Playwright testing. Use this skill to write and run automated tests for web applications using Playwright.
---

# Test authoring guidelines

For more details on Playwright best practices see <https://playwright.dev/docs/best-practices>

## Test user-visible behavior

Automated tests should verify that the application code works for the end users, and avoid relying on implementation details such as things which users will not typically use, see, or even know about such as the name of a function, whether something is an array, or the CSS class of some element. The end user will see or interact with what is rendered on the page, so your test should typically only see/interact with the same rendered output.

## Make tests as isolated as possible

Each test should be completely isolated from another test and should run independently with its own local storage, session storage, data, cookies etc.

## Avoid testing third-party dependencies

Only test what you control. Don't try to test links to external sites or third party servers that you do not control, unless it is specifically for testing purposes.

## Use locators

Locators come with auto waiting and retry-ability. To make tests resilient, we recommend prioritizing user-facing attributes and explicit contracts.

```javascript
// 👍 Use role selectors
page.getByRole("button", { name: "submit" });

// Using filters to locate elements with text
page.getByRole("listitem").filter({ hasText: "Product 2" });

// Use chaining and filtering
page
  .getByRole("listitem")
  .filter({ hasText: "Product 2" })
  .getByRole("button", { name: "Add to cart" });

// 👎 Avoid CSS selectors
page.locator("button.buttonIcon.episode-actions-later");
```

### Locator preference

1. getByRole to locate by explicit and implicit accessibility attributes ⭐⭐⭐⭐⭐
2. getByText to locate by text content
3. getByLabel to locate a form control by associated label's text
4. getByPlaceholder to locate an input by placeholder
5. getByAltText to locate an element, usually image, by its text alternative
6. getByTitle to locate an element by its title attribute
7. getByTestId to locate an element based on its `data-testid`

### Filtering

```javascript
// Filter elements having text
page.getByRole("listitem").filter({ hasText: "Product 2" });

// Filter elements not having text
page.getByRole("listitem").filter({ hasNotText: "Out of stock" });

// Filter elements having another locator inside
page
  .getByRole("listitem")
  .filter({ has: page.getByRole("heading", { name: "Product 2" }) });

// Filter only visible elements
// Note: Hidden elements do not have a role, so this filter is not
//       needed when using getByRole
// 👎 CSS selector is not recommended, use a better locator if possible
page.locator(".something").filter({ visible: true });
```

The filtering locator **must be relative** to the original locator and is queried starting with the original locator match, not the document root. Therefore, the following will not work, because the filtering locator starts matching from the `<ul>` list element that is outside of the `<li>` list item matched by the original locator:

```javascript
// ✖ WRONG
page
  .getByRole('listitem')
  .filter({ has: page.getByRole('list').getByText('Product 2') }))
```

There is `hasNot` which does the opposite of `has`.

### Combining locators

```javascript
// Chaining: Find buttons inside listitems
page.getByRole("listitem").getByRole("button");

// Use `and` for intersection (buttons whose title is Subscribe)
page.getByRole("button").and(page.getByTitle("Subscribe"));

// Use `or` to match multiple locators
page
  .getByRole("button", { name: "New" })
  .or(page.getByText("Confirm security settings"));

// Example: Dismiss a known dialog before clicking New
const newEmail = page.getByRole("button", { name: "New" });
const dialog = page.getByText("Confirm security settings");
await expect(newEmail.or(dialog).first()).toBeVisible();
if (await dialog.isVisible())
  await page.getByRole("button", { name: "Dismiss" }).click();
await newEmail.click();
```

Locators are strict. This means that all operations on locators that imply some target DOM element will throw an exception if more than one element matches. For example, the following call throws if there are several buttons in the DOM:

```javascript
// Throws an error if more than one
await page.getByRole("button").click();

// Click the first button
await page.getByRole("button").first().click();
```

For more info on selectors refer to <https://playwright.dev/docs/locators>

## Use web first assertions

```javascript
// 👎 Don't use manual assertions
expect(await page.getByText("welcome").isVisible()).toBe(true);

// 👍 Use web first assertions
await expect(page.getByText("welcome")).toBeVisible();
```

## When encountering challenges

If you encounter challenges when writing tests, it may be tempting to work around them (e.g. by using timeouts, sleeps, or brittle selectors). DO NOT DO THAT! Instead, try to make the app more testable first. Maybe adding semantic attributes (best), data attributes, or test IDs. For example, if a test script clicks the button too fast (before it is ready to be clicked), consider adjusting the app to initially disable the button until it is really ready to be clicked.

## Locator handlers

When testing a web page, sometimes unexpected overlays like a "Sign up" dialog appear and block actions you want to automate, e.g. clicking a button. These overlays don't always show up in the same way or at the same time, making them tricky to handle in automated tests.

The `addLocatorHandler` lets you set up a special function, called a handler, that activates when it detects that overlay is visible. The handler's job is to remove the overlay, allowing your test to continue as if the overlay wasn't there.

Running the handler will alter your page state mid-test. For example it will change the currently focused element and move the mouse. Make sure that actions that run after the handler are self-contained and do not rely on the focus and mouse state being unchanged.

```javascript
// Setup the handler.
await page.addLocatorHandler(
  page.getByText("Sign up to the newsletter"),
  async () => {
    await page.getByRole("button", { name: "No thanks" }).click();
  },
);

// Write the test as usual.
await page.goto("https://example.com");
await page.getByRole("button", { name: "Start here" }).click();
```

# Page Objects

To set up structure for page objects, extend the base `test` and `expect` functions:

```javascript
// support/index.ts
import { test as base, expect as baseExpect } from "@playwright/test";
import { AppTester } from "./AppTester";

export const test =
  base.extend <
  { app: AppTester } >
  {
    app: async ({ page }, use) => {
      const app = new AppTester(page);
      await use(app);
    },
  };

export const expect = baseExpect;
```

Create a context interface for page objects:

```javascript
// support/PageObjectContext.ts
export interface PageObjectContext {
  page: Page
}
```

Create an AppTester, the root page object:

```javascript
import type { PageObjectContext } from './PageObjectContext'
import { LoginPageTester } from './LoginPageTester'
import { RepoPageTester } from './RepoPageTester'

export class AppTester {
  constructor(public context: PageObjectContext) {}
  get loginPage() {
    return new LoginPageTester(this.context)
  }
  get repoPage() {
    return new RepoPageTester(this.context)
  }
}
```

- Name page objects as well as the root tester class with the `Tester` prefix. It helps us distinguish between production code and test code (when the test lives in the same repository as the production code).
- Use getters to lazily-instantiate page objects, so that we do not create page objects that we do not use. Each page object is simple enough and are stateless, so they do not need to be memoized.

Create a page object for each page in your app. For example, a LoginPageTester:

```javascript
export class LoginPageTester {
  constructor(public context: PageObjectContext) {}
  async goto() {
    const { page } = this.context
    await page.goto('/login')
  }
  async login(username: string, password: string) {
    const { page } = this.context
    await page.getByRole('textbox', { name: 'Username' }).fill(username)
    await page.getByRole('textbox', { name: 'Password' }).fill(password)
    await page.getByRole('button', { name: 'Sign in' }).click()
  }
}
```

A page object:

- Is a class.
- Has a constructor that takes a `PageObjectContext`.
- Exposes methods and properties that represent user actions and elements on the page.

Now it can be used in tests:

```javascript
import { test, expect } from "./support";

test("Create a new issue", async ({ app }) => {
  await app.loginPage.goto();
  await app.loginPage.login("username", "password");
  await app.repoPage.goto("myorg/myrepo");
});
```

Note: Work iteratively and don't create a premature abstraction! Use existing page object if possible. If not, don't create a new page object just yet! Implement it directly inside the test, and get it working first. Once working, analyze your test script to see if the hardcoded behavior should be added to a an existing page object or a new page object should be created.
