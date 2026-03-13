---
name: netlify-forms
description: Guide for using Netlify Forms for HTML form handling. Use when adding contact forms, feedback forms, file upload forms, or any form that should be collected by Netlify. Covers the data-netlify attribute, spam filtering, AJAX submissions, file uploads, notifications, and the submissions API.
---

# Netlify Forms

Netlify Forms collects HTML form submissions without server-side code. Form detection must be enabled in the Netlify UI (Forms section).

## Basic Setup

Add `data-netlify="true"` and a unique `name` to the form:

```html
<form name="contact" method="POST" data-netlify="true">
  <label>Name: <input type="text" name="name" /></label>
  <label>Email: <input type="email" name="email" /></label>
  <label>Message: <textarea name="message"></textarea></label>
  <button type="submit">Send</button>
</form>
```

Netlify's build system detects the form and injects a hidden `form-name` input automatically. For a custom success page, add `action="/thank-you"` to the form tag.

## JavaScript-Rendered Forms (React, Vue, etc.)

For forms rendered by JavaScript frameworks, Netlify's build parser cannot detect the form in static HTML. You must either:

**Option A:** Add a hidden HTML form to your `index.html` (or equivalent static file):

```html
<form name="contact" netlify netlify-honeypot="bot-field" hidden>
  <input type="text" name="name" />
  <input type="email" name="email" />
  <textarea name="message"></textarea>
</form>
```

**Option B:** Include a hidden `form-name` input in your component:

```jsx
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />
  {/* ... fields ... */}
</form>
```

## AJAX Submissions

### Vanilla JavaScript

```javascript
const form = document.querySelector("form");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  await fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(formData).toString(),
  });
});
```

### React Example

```tsx
function ContactForm() {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const response = await fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(formData as any).toString(),
    });
    if (response.ok) {
      // Show success feedback
    }
  };

  return (
    <form name="contact" method="POST" data-netlify="true" onSubmit={handleSubmit}>
      <input type="hidden" name="form-name" value="contact" />
      <input type="text" name="name" placeholder="Name" />
      <input type="email" name="email" placeholder="Email" />
      <textarea name="message" placeholder="Message" />
      <button type="submit">Send</button>
    </form>
  );
}
```

## Spam Filtering

Netlify uses Akismet automatically. Add a honeypot field for extra protection:

```html
<form name="contact" method="POST" netlify-honeypot="bot-field" data-netlify="true">
  <p style="display:none">
    <label>Don't fill this out: <input name="bot-field" /></label>
  </p>
  <!-- visible fields -->
</form>
```

For reCAPTCHA, add `data-netlify-recaptcha="true"` to the form and include `<div data-netlify-recaptcha="true"></div>` where the widget should appear.

## File Uploads

```html
<form name="upload" enctype="multipart/form-data" data-netlify="true">
  <input type="text" name="name" />
  <input type="file" name="attachment" />
  <button type="submit">Upload</button>
</form>
```

For AJAX file uploads, use `FormData` directly — do **not** set `Content-Type` (the browser sets it with the correct boundary):

```javascript
await fetch("/", { method: "POST", body: new FormData(form) });
```

**Limits:** 8 MB max request size, 30-second timeout, one file per input field.

## Notifications

Configure in the Netlify UI under **Project configuration > Notifications**:

- **Email**: Auto-sends on submission. Add `<input type="hidden" name="subject" value="Contact form" />` for custom subject lines.
- **Slack**: Via Netlify App for Slack.
- **Webhooks**: Trigger external services on submission.

## Submissions API

Access submissions programmatically:

```
GET /api/v1/forms/{form_id}/submissions
Authorization: Bearer <PERSONAL_ACCESS_TOKEN>
```

Key endpoints:

| Action | Method | Path |
|---|---|---|
| List forms | GET | `/api/v1/sites/{site_id}/forms` |
| Get submissions | GET | `/api/v1/forms/{form_id}/submissions` |
| Get spam | GET | `/api/v1/forms/{form_id}/submissions?state=spam` |
| Delete submission | DELETE | `/api/v1/submissions/{id}` |
