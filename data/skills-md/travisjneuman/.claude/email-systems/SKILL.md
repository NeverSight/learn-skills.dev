---
name: email-systems
description: >-
  Transactional email (Resend, SendGrid, SES), templates (React Email, MJML), deliverability (SPF/DKIM/DMARC), and inboxing best practices. Use when building email infrastructure, designing templates, or troubleshooting deliverability.
---

# Email Systems

## Overview

This skill covers building reliable email systems for web applications, including transactional email sending, template design, deliverability optimization, and inbox placement. It addresses integration with email service providers (Resend, AWS SES, SendGrid, Postmark), building responsive HTML email templates with React Email and MJML, configuring DNS records for deliverability (SPF, DKIM, DMARC), managing email types (transactional, notification, marketing), queue management, and bounce/complaint handling.

Use this skill when sending welcome emails, password resets, order confirmations, notification digests, marketing campaigns, or any system-generated email. Also use when debugging deliverability issues or migrating between email providers.

---

## Core Principles

1. **Transactional and marketing are different** - Transactional emails (password reset, receipt) must arrive instantly and reliably. Marketing emails (newsletter, promo) can be batched and should have unsubscribe links. Never mix them on the same sending domain.
2. **HTML email is not web development** - Email clients render HTML from 2004. No flexbox, no grid, no modern CSS. Use tables for layout, inline styles, and test across clients. React Email and MJML abstract this pain.
3. **Deliverability is earned** - SPF, DKIM, and DMARC are table stakes, not guarantees. Maintain low bounce rates (< 2%), low complaint rates (< 0.1%), and warm up new sending domains gradually.
4. **Queue everything** - Never send email synchronously in a request handler. Queue email sends to avoid blocking user requests and to enable retry on failure.
5. **Test before sending** - Use Mailtrap or Ethereal in development, preview in multiple clients (Litmus, Email on Acid), and verify every link works.

---

## Key Patterns

### Pattern 1: React Email Templates with Resend

**When to use:** Building type-safe, component-based email templates with modern DX and reliable delivery.

**Implementation:**

```tsx
// emails/welcome.tsx - React Email template
import {
  Html,
  Head,
  Body,
  Container,
  Section,
  Text,
  Button,
  Img,
  Hr,
  Link,
  Preview,
} from "@react-email/components";

interface WelcomeEmailProps {
  userName: string;
  loginUrl: string;
  guideUrl: string;
}

export function WelcomeEmail({ userName, loginUrl, guideUrl }: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>Welcome to MyApp, {userName}! Here&apos;s how to get started.</Preview>
      <Body style={styles.body}>
        <Container style={styles.container}>
          <Img
            src="https://myapp.com/logo.png"
            width={120}
            height={36}
            alt="MyApp"
          />

          <Section style={styles.section}>
            <Text style={styles.heading}>Welcome, {userName}!</Text>
            <Text style={styles.text}>
              Thanks for signing up. Your account is ready to go.
              Here are three things to get you started:
            </Text>

            <Text style={styles.listItem}>
              <strong>1. Create your first project</strong> - Click "New Project" on your dashboard.
            </Text>
            <Text style={styles.listItem}>
              <strong>2. Invite your team</strong> - Share your workspace with colleagues.
            </Text>
            <Text style={styles.listItem}>
              <strong>3. Explore the guide</strong> - Learn tips and best practices.
            </Text>

            <Section style={styles.buttonContainer}>
              <Button style={styles.button} href={loginUrl}>
                Go to Dashboard
              </Button>
            </Section>
          </Section>

          <Hr style={styles.hr} />

          <Section style={styles.footer}>
            <Text style={styles.footerText}>
              Need help? Reply to this email or visit our{" "}
              <Link href={guideUrl} style={styles.link}>help center</Link>.
            </Text>
            <Text style={styles.footerText}>
              MyApp, Inc. | 123 Street, City, ST 12345
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}

const styles = {
  body: {
    backgroundColor: "#f6f9fc",
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
  },
  container: {
    backgroundColor: "#ffffff",
    margin: "0 auto",
    padding: "20px 0 48px",
    maxWidth: "600px",
    borderRadius: "8px",
  },
  section: { padding: "0 48px" },
  heading: { fontSize: "24px", fontWeight: "bold" as const, marginBottom: "16px" },
  text: { fontSize: "16px", lineHeight: "26px", color: "#404040" },
  listItem: { fontSize: "15px", lineHeight: "24px", color: "#404040", marginBottom: "8px" },
  buttonContainer: { textAlign: "center" as const, marginTop: "24px", marginBottom: "24px" },
  button: {
    backgroundColor: "#0066ff",
    borderRadius: "6px",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: "bold" as const,
    textDecoration: "none",
    textAlign: "center" as const,
    display: "inline-block",
    padding: "12px 24px",
  },
  hr: { borderColor: "#e6ebf1", margin: "32px 0" },
  footer: { padding: "0 48px" },
  footerText: { fontSize: "12px", color: "#8898aa", lineHeight: "20px" },
  link: { color: "#0066ff" },
};

// Default props for preview
WelcomeEmail.PreviewProps = {
  userName: "Jane",
  loginUrl: "https://myapp.com/dashboard",
  guideUrl: "https://myapp.com/guide",
} satisfies WelcomeEmailProps;

export default WelcomeEmail;
```

```typescript
// lib/email.ts - Email sending service
import { Resend } from "resend";
import { WelcomeEmail } from "@/emails/welcome";
import { PasswordResetEmail } from "@/emails/password-reset";

const resend = new Resend(process.env.RESEND_API_KEY);

// Type-safe email sending
type EmailTemplate =
  | { template: "welcome"; props: { userName: string; loginUrl: string; guideUrl: string } }
  | { template: "password-reset"; props: { resetUrl: string; expiresIn: string } }
  | { template: "invoice"; props: { invoiceUrl: string; amount: string; dueDate: string } };

const templates: Record<string, React.FC<Record<string, unknown>>> = {
  welcome: WelcomeEmail,
  "password-reset": PasswordResetEmail,
};

const subjects: Record<string, (props: Record<string, unknown>) => string> = {
  welcome: () => "Welcome to MyApp!",
  "password-reset": () => "Reset your password",
  invoice: (p) => `Invoice for $${p.amount}`,
};

async function sendEmail(
  to: string,
  email: EmailTemplate
): Promise<{ id: string }> {
  const Template = templates[email.template];
  const subject = subjects[email.template](email.props);

  const { data, error } = await resend.emails.send({
    from: "MyApp <hello@myapp.com>",
    to,
    subject,
    react: Template(email.props),
  });

  if (error) {
    throw new EmailSendError(error.message, { to, template: email.template });
  }

  return { id: data!.id };
}

export { sendEmail };
```

**Why:** React Email provides component-based email templates with TypeScript safety, hot reloading during development, and automatic conversion to email-safe HTML. Resend provides high deliverability, simple API, and React Email integration out of the box. Type-safe template definitions prevent sending emails with missing properties.

---

### Pattern 2: Email Queue with Retry Logic

**When to use:** Any production email sending. Never send email synchronously in a request handler.

**Implementation:**

```typescript
// jobs/email.ts - Background email processing
import { Queue, Worker } from "bullmq";
import { Redis } from "ioredis";
import { sendEmail } from "@/lib/email";

const connection = new Redis(process.env.REDIS_URL!, { maxRetriesPerRequest: null });

// Define the email queue
const emailQueue = new Queue("email", {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: "exponential",
      delay: 60_000, // 1 min, then 2 min, then 4 min
    },
    removeOnComplete: { age: 7 * 24 * 60 * 60 }, // Keep completed jobs for 7 days
    removeOnFail: { age: 30 * 24 * 60 * 60 }, // Keep failed jobs for 30 days
  },
});

// Queue an email (call this from your application code)
async function queueEmail(
  to: string,
  template: EmailTemplate,
  options?: { delay?: number; priority?: number }
): Promise<string> {
  const job = await emailQueue.add(
    template.template,
    { to, template },
    {
      delay: options?.delay,
      priority: options?.priority ?? 0,
    }
  );
  return job.id!;
}

// Process emails in the background
const emailWorker = new Worker(
  "email",
  async (job) => {
    const { to, template } = job.data;

    try {
      const result = await sendEmail(to, template);
      return result;
    } catch (error) {
      // Log for monitoring
      console.error(`Email send failed (attempt ${job.attemptsMade + 1}/${job.opts.attempts}):`, {
        to,
        template: template.template,
        error: (error as Error).message,
      });
      throw error; // BullMQ will retry based on backoff config
    }
  },
  {
    connection,
    concurrency: 10, // Process 10 emails concurrently
    limiter: {
      max: 100, // Max 100 emails per minute (respect ESP rate limits)
      duration: 60_000,
    },
  }
);

// Listen for permanent failures
emailWorker.on("failed", (job, error) => {
  if (job && job.attemptsMade >= (job.opts.attempts ?? 3)) {
    // All retries exhausted - alert and log
    alertOps(`Email permanently failed: ${job.data.to} - ${error.message}`);
  }
});

export { queueEmail };
```

```typescript
// Usage in application code
async function handleUserSignup(user: User) {
  // Create user in database (synchronous, in request)
  await db.user.create({ data: user });

  // Queue welcome email (async, background)
  await queueEmail(user.email, {
    template: "welcome",
    props: {
      userName: user.name,
      loginUrl: `${process.env.APP_URL}/dashboard`,
      guideUrl: `${process.env.APP_URL}/guide`,
    },
  });
}
```

**Why:** Queuing emails decouples delivery from user requests. If the email provider is slow or down, user signup still succeeds. Exponential backoff handles transient failures. Rate limiting prevents exceeding ESP quotas. Job retention enables debugging delivery issues.

---

### Pattern 3: DNS Configuration for Deliverability

**When to use:** Setting up a new sending domain or diagnosing deliverability issues.

**Implementation:**

```text
# SPF Record - Authorize sending servers
# Add to DNS as TXT record on your domain
myapp.com.  TXT  "v=spf1 include:_spf.resend.com include:amazonses.com ~all"

# DKIM Record - Cryptographic email signing
# Provider-specific, usually a CNAME record
resend._domainkey.myapp.com.  CNAME  resend._domainkey.example.com.

# DMARC Record - Alignment policy
# Start with p=none (monitor), move to p=quarantine, then p=reject
_dmarc.myapp.com.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@myapp.com; pct=100; adkim=s; aspf=s"

# Return-Path / Bounce domain (custom envelope sender)
bounce.myapp.com.  MX  10  feedback-smtp.us-east-1.amazonses.com.
bounce.myapp.com.  TXT  "v=spf1 include:amazonses.com ~all"
```

```typescript
// Verify DNS configuration programmatically
import { resolveTxt, resolveCname, resolveMx } from "dns/promises";

async function verifyEmailDNS(domain: string): Promise<Record<string, boolean>> {
  const results: Record<string, boolean> = {};

  // Check SPF
  try {
    const txt = await resolveTxt(domain);
    const spf = txt.flat().find((r) => r.startsWith("v=spf1"));
    results.spf = !!spf;
  } catch {
    results.spf = false;
  }

  // Check DMARC
  try {
    const txt = await resolveTxt(`_dmarc.${domain}`);
    const dmarc = txt.flat().find((r) => r.startsWith("v=DMARC1"));
    results.dmarc = !!dmarc;
  } catch {
    results.dmarc = false;
  }

  // Check DKIM (provider-specific selector)
  try {
    const cname = await resolveCname(`resend._domainkey.${domain}`);
    results.dkim = cname.length > 0;
  } catch {
    results.dkim = false;
  }

  return results;
}
```

**Why:** Email authentication (SPF, DKIM, DMARC) proves to receiving mail servers that your emails are legitimate. Without them, emails land in spam. SPF says which servers can send for your domain. DKIM cryptographically signs messages. DMARC tells receivers what to do with unauthenticated email.

---

### Pattern 4: Bounce and Complaint Handling

**When to use:** Maintaining sender reputation and deliverability over time.

**Implementation:**

```typescript
// Webhook handler for bounces and complaints (SES/Resend/SendGrid)
async function handleEmailEvent(event: EmailEvent): Promise<void> {
  switch (event.type) {
    case "bounce": {
      const { email, bounceType } = event;

      if (bounceType === "permanent") {
        // Hard bounce - never send to this address again
        await db.emailSuppression.upsert({
          where: { email },
          create: { email, reason: "hard_bounce", suppressedAt: new Date() },
          update: { reason: "hard_bounce", suppressedAt: new Date() },
        });

        // Update user record
        await db.user.updateMany({
          where: { email },
          data: { emailVerified: false, emailBounced: true },
        });
      } else {
        // Soft bounce - retry later, suppress after 3 soft bounces
        const count = await db.emailEvent.count({
          where: { email, type: "soft_bounce", createdAt: { gte: thirtyDaysAgo() } },
        });

        if (count >= 3) {
          await db.emailSuppression.create({
            data: { email, reason: "repeated_soft_bounce", suppressedAt: new Date() },
          });
        }
      }
      break;
    }

    case "complaint": {
      // Spam complaint - suppress immediately
      await db.emailSuppression.upsert({
        where: { email: event.email },
        create: { email: event.email, reason: "complaint", suppressedAt: new Date() },
        update: { reason: "complaint", suppressedAt: new Date() },
      });

      // Remove from all marketing lists
      await db.marketingSubscription.updateMany({
        where: { email: event.email },
        data: { unsubscribedAt: new Date(), reason: "spam_complaint" },
      });
      break;
    }
  }
}

// Check suppression list before sending
async function canSendTo(email: string): Promise<boolean> {
  const suppressed = await db.emailSuppression.findUnique({
    where: { email },
  });
  return !suppressed;
}
```

**Why:** ESPs monitor bounce and complaint rates. Exceeding thresholds (bounce > 5%, complaints > 0.1%) triggers sending suspensions. A suppression list prevents sending to known-bad addresses, protecting your sender reputation and ensuring legitimate emails reach inboxes.

---

## Email Provider Comparison

| Provider | Best For | Pricing | React Email | Key Feature |
|---|---|---|---|---|
| **Resend** | Developer-friendly transactional | 100/day free, $20/mo for 50k | Native | Best DX, React Email team |
| **AWS SES** | High volume, cost optimization | $0.10 per 1,000 | Via render | Cheapest at scale |
| **SendGrid** | Marketing + transactional | 100/day free | Via render | Marketing automation |
| **Postmark** | Transactional reliability | $15/mo for 10k | Via render | Best transactional deliverability |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Sending email in the request handler | Blocks user response, no retry | Queue with background worker |
| Same domain for transactional + marketing | Marketing reputation affects password resets | Separate subdomains (mail.app.com vs news.app.com) |
| No suppression list | Repeated bounces destroy sender reputation | Maintain and check suppression list before every send |
| Using `<div>` layout in email HTML | Broken rendering in Outlook, Gmail | Use `<table>` layout or React Email/MJML |
| No unsubscribe link in notification emails | CAN-SPAM violation, spam complaints | One-click unsubscribe header + visible link |
| Testing with real email addresses | Spam to real people, complaints | Use Mailtrap, Ethereal, or Resend test mode |
| Sending from a no-reply address | Users can't respond, feels impersonal | Use a monitored reply-to address |

---

## Checklist

- [ ] SPF record configured for sending domain
- [ ] DKIM signing enabled and verified
- [ ] DMARC policy set (start with `p=none`, escalate to `p=quarantine`)
- [ ] Email templates tested in Gmail, Outlook, Apple Mail, Yahoo
- [ ] Emails sent through a queue with retry logic
- [ ] Bounce and complaint webhooks configured
- [ ] Suppression list checked before every send
- [ ] Unsubscribe link present in all notification/marketing emails
- [ ] Separate sending domains for transactional vs marketing
- [ ] Development environment uses test mode (Mailtrap/Ethereal)
- [ ] Rate limiting configured to stay within ESP quotas
- [ ] Return-path / bounce domain configured

---

## Related Resources

- **Skills:** `authentication-patterns` (password reset emails), `payment-integration` (invoice/receipt emails)
- **Skills:** `event-driven-architecture` (email as async event)
- **Rules:** `rules/stacks/react-typescript.md` (React Email component patterns)
