---
name: ookami-coding-style-web
description: >
  ookami team web frontend coding style conventions. Use this skill whenever
  writing, modifying, or reviewing JavaScript, JSX, SCSS, React components,
  hooks, selectors, containers, or frontend test files. Also use when the user
  asks about React component structure, Atomic Design conventions, CSS Modules,
  Prettier formatting, Airbnb style guide usage, file naming for .jsx/.js/.scss,
  or how to structure frontend tests with describe/it.
---

# Web Coding Style

Follow these conventions when writing web frontend code.
Full reference: https://github.com/ookamiinc/guides/blob/master/coding_style/web.md

## General

- Use American English.
- Use ES2015+ and JSX. Follow the [Airbnb JavaScript style guide](https://github.com/airbnb/javascript) and [Airbnb React style guide](https://github.com/airbnb/javascript/tree/master/react).
- Use CSS Modules and SCSS. Follow [stylelint-config-standard](https://github.com/stylelint/stylelint-config-standard).

## Check Your Code

Run the linter before submitting:

```
yarn run lint
```

## Code Formatting

Use [Prettier](https://github.com/prettier/prettier) for code formatting.

## File Extensions

- `.js` — standard JavaScript only (no JSX).
- `.jsx` — files containing JSX.
- `.test.js` — unit tests.
- `.test.e2e.js` — end-to-end tests.
- `.worker.js` — web workers.

## Action Types

Define action type constants in SCREAMING_SNAKE_CASE:

```js
const FOO_BAR = 'FOO_BAR';
```

## Directory & Naming Conventions

### `src/components` (Atomic Design)

```
atoms/FooBar/
  |- FooBar.jsx
  |- FooBar.scss
  |- index.js
```

### `src/containers`

- File name: `FooBarContainer.jsx`
- Export name: `FooBarContainer`

### `src/hooks`

- File name: `useFooBar.js`
- Hook name: `useFooBar`

### `src/selectors`

- File name: `fooBar.js`
- Selector name: `fooBarSelector`

## Tests

- Use `describe` to group by function and condition.
- Prefer `it` over `test`.

Example:

```jsx
describe('Button', () => {
  it('renders button', () => {
    const { button } = setup(props);
    expect(button).toBeDefined();
  });

  it('calls onClick function', () => {
    const { button } = setup(props);
    fireEvent.click(button);
    expect(props.onClick).toHaveBeenCalledTimes(1);
  });

  it('matches its snapshot', () => {
    const { asFragment } = setup(props);
    expect(asFragment()).toMatchSnapshot();
  });
});
```
