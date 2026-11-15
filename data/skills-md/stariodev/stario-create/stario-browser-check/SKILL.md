---
name: stario-browser-check
description: Load before you open a browser, take a screenshot, run Playwright, or use computer use on a Stario app. It names the test that answers each question about a page without a browser, the order to find a bug, and the two cases where a browser is right - client JavaScript that holds state, and a bug that the HTML does not show.
---

# A browser is the last check

The server writes all the HTML. Datastar morphs it into the page. Thus a question about a page is a question about the server answer, and `TestClient` reads that answer in milliseconds. When a test shows the right HTML in the right event, the browser shows it.

## The test for each question

| The question | The proof |
| --- | --- |
| Does the other tab update? | Two streams, one command, the change in the next event of both (skill `stario-feature`). |
| Does the button post to a real route? Does each `$signal` exist? Does a dialog stay open? Does the stream keep its element? | `tests/test_pages.py`. It runs in `just check` on every page that a link reaches. |
| Does it still hold with rows on the page? | The page test adds rows, then `assert not await check(client, url)` (from `tests.test_pages`). |
| Does the command answer? | `client.post(...)`: 204, a `datastar-patch-signals` event, or `window.location`. |
| Does a repaint lose what I typed? | `if_missing=True` on the stream element, and the inputs are not patched again. |
| Does the sort survive a reload? | `GET` with the query returns the sorted HTML. |
| Does login protect the page? | Signed out: 303, or `window.location` for a Datastar request (skill `stario-auth`). |
| Does a class apply? | Its literal is in a `.py` file under `app/`, then `just css`. |
| Does a JavaScript call exist? | `tests/test_js.py`. |
| Does it look right? | Ask the user. When the user watches the app, the user is the browser. |

An app from before stario-create 5.7 adds the page check with `uvx stario-create@latest add pages`. It finds each page from the links and from the `GET` routes in each `urls.py`.

## When the user says that it does not work

1. `curl -s localhost:8000/todos` and `curl -sN localhost:8000/todos/live`, on the server of the user. Read the HTML.
2. Write a test that fails the way the user describes. Fix the code until it passes.
3. Only when 1 and 2 show the right HTML and the page is still wrong, use the browser check.

## The browser check

A browser is right in two cases only:

- Client JavaScript in `static/js/` that holds state: a drag, a ruler, viewport handling, a gesture.
- A bug that steps 1 and 2 cannot show: a console error, a browser difference.

Never for a page load, a form, a live update, a login, a redirect, a style, or a screenshot to "see it". Never use computer use on a Stario app: the user looks.

```bash
uvx stario-create@latest add browser
uv run --with playwright playwright install chromium
uv run --with playwright python scripts/browser.py /todos
```

`scripts/browser.py` starts the app on a free port with the settings in `.env`, opens the page in two tabs, runs `steps`, prints each console error, saves a screenshot, and stops the app. It never touches a server it did not start. Edit `steps` for the one interaction you check. Wait with `expect`, not with a sleep. Keep `playwright` out of the dependencies, so `just check` stays fast.
