---
name: customer-success
description: >-
  Support workflows, ticketing systems (Zendesk, Intercom), knowledge base design, chatbot design, and metrics (CSAT, NPS). Use when building support infrastructure, designing help centers, or optimizing customer experience.
---

# Customer Success Engineering

## Overview

This skill covers building technical systems that power customer support and success operations. It addresses support ticket system integration (Zendesk, Intercom, Freshdesk), knowledge base architecture, conversational AI chatbot design, customer feedback collection and routing, SLA management and enforcement, escalation workflow automation, self-service portal implementation, and customer health scoring models.

Use this skill when building or integrating support systems, designing chatbot flows, creating self-service documentation portals, implementing SLA tracking, building customer health dashboards, or automating support workflows.

---

## Core Principles

1. **Self-service first** - The best support interaction is the one that never happens. Invest in searchable knowledge bases, in-app help, and contextual guidance before scaling human support.
2. **Automate triage, not resolution** - AI can classify, prioritize, and route tickets effectively. Let humans handle resolution for complex issues. Over-automating resolution creates frustrated customers.
3. **Measure time-to-resolution, not ticket count** - Closing tickets quickly means nothing if the customer's problem isn't solved. Track first-contact resolution rate, customer effort score, and reopen rate.
4. **Context travels with the ticket** - Every handoff (bot to human, L1 to L2) must include full conversation history, user account data, and attempted solutions. Repeating information is the #1 customer complaint.
5. **Feedback is a product signal** - Support tickets are unstructured product feedback. Tag, categorize, and surface trends to product teams. The most common support topic should become the next product improvement.

---

## Key Patterns

### Pattern 1: Knowledge Base Architecture

**When to use:** Building searchable documentation that serves both customers (self-service) and support agents (internal reference).

**Implementation:**

```typescript
// Knowledge base article schema
interface Article {
  id: string;
  slug: string;
  title: string;
  content: string;          // Markdown
  excerpt: string;          // For search results
  category: string;
  subcategory: string;
  tags: string[];
  audience: "customer" | "internal" | "both";
  visibility: "public" | "authenticated" | "internal";
  relatedArticles: string[];
  metadata: {
    createdAt: Date;
    updatedAt: Date;
    author: string;
    reviewedAt: Date | null;
    helpfulVotes: number;
    notHelpfulVotes: number;
    viewCount: number;
  };
}

// Search implementation with vector + full-text hybrid
async function searchKnowledgeBase(
  query: string,
  options?: { category?: string; audience?: string; limit?: number }
): Promise<SearchResult[]> {
  const limit = options?.limit ?? 10;

  // 1. Semantic search (catches paraphrased queries)
  const embedding = await getEmbedding(query);
  const semanticResults = await vectorDb.search({
    vector: embedding,
    filter: {
      audience: options?.audience ?? "customer",
      ...(options?.category && { category: options.category }),
    },
    limit,
  });

  // 2. Full-text search (catches exact terminology)
  const textResults = await db.$queryRaw`
    SELECT id, title, excerpt,
           ts_rank(search_vector, plainto_tsquery('english', ${query})) AS rank
    FROM articles
    WHERE search_vector @@ plainto_tsquery('english', ${query})
      AND audience IN ('customer', 'both')
      ${options?.category ? Prisma.sql`AND category = ${options.category}` : Prisma.empty}
    ORDER BY rank DESC
    LIMIT ${limit}
  `;

  // 3. Merge and deduplicate results
  const merged = mergeSearchResults(semanticResults, textResults);

  // 4. Track search for analytics
  await trackSearch(query, merged.length);

  return merged;
}

// Feedback loop - track article helpfulness
async function rateArticle(
  articleId: string,
  helpful: boolean,
  feedback?: string
): Promise<void> {
  await db.articleFeedback.create({
    data: {
      articleId,
      helpful,
      feedback,
      createdAt: new Date(),
    },
  });

  // Update aggregate counts
  await db.article.update({
    where: { id: articleId },
    data: helpful
      ? { helpfulVotes: { increment: 1 } }
      : { notHelpfulVotes: { increment: 1 } },
  });

  // Flag articles with low helpfulness for review
  const article = await db.article.findUnique({ where: { id: articleId } });
  if (article) {
    const total = article.helpfulVotes + article.notHelpfulVotes;
    const helpfulRate = total > 10 ? article.helpfulVotes / total : 1;

    if (helpfulRate < 0.5 && total > 10) {
      await createReviewTask(articleId, "Low helpfulness score");
    }
  }
}
```

```tsx
// In-app contextual help widget
function HelpWidget({ context }: { context: string }) {
  const [articles, setArticles] = useState<Article[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Fetch relevant articles based on current page/feature context
    if (isOpen) {
      searchKnowledgeBase("", { category: context, limit: 5 })
        .then(setArticles);
    }
  }, [isOpen, context]);

  return (
    <div className="help-widget">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Help"
        aria-expanded={isOpen}
      >
        ?
      </button>
      {isOpen && (
        <div role="dialog" aria-label="Help articles">
          <SearchInput onSearch={(q) => searchKnowledgeBase(q, { category: context }).then(setArticles)} />
          <ArticleList articles={articles} />
          <a href="/support">Contact support</a>
        </div>
      )}
    </div>
  );
}
```

**Why:** Hybrid search (semantic + full-text) covers both conceptual queries ("how do I share my project?") and exact terminology queries ("SSO SAML configuration"). The feedback loop ensures low-quality articles are flagged for improvement. Contextual help surfaces relevant articles without the user needing to search.

---

### Pattern 2: Support Ticket Integration

**When to use:** Connecting your application to a ticketing system for structured support workflows.

**Implementation:**

```typescript
// Unified support ticket interface (abstracts provider)
interface SupportTicket {
  id: string;
  externalId: string;       // Provider's ticket ID
  subject: string;
  description: string;
  status: "open" | "pending" | "in_progress" | "resolved" | "closed";
  priority: "low" | "normal" | "high" | "urgent";
  category: string;
  tags: string[];
  requester: {
    id: string;
    email: string;
    name: string;
  };
  assignee?: {
    id: string;
    name: string;
    group: string;
  };
  metadata: {
    plan: string;
    accountAge: number;
    mrr: number;            // Monthly recurring revenue
    previousTickets: number;
  };
  createdAt: Date;
  updatedAt: Date;
  firstResponseAt?: Date;
  resolvedAt?: Date;
}

// Auto-triage new tickets with AI classification
async function triageTicket(ticket: SupportTicket): Promise<TriageResult> {
  const classification = await classifyTicket(ticket.subject, ticket.description);

  // Priority escalation rules
  let adjustedPriority = classification.priority;

  // Enterprise customers get elevated priority
  if (ticket.metadata.mrr >= 5000) {
    adjustedPriority = elevate(adjustedPriority);
  }

  // Revenue at risk detection
  if (containsCancellationIntent(ticket.description)) {
    adjustedPriority = "urgent";
    classification.tags.push("churn-risk");
  }

  // Route to appropriate team
  const team = determineTeam(classification.category, adjustedPriority);

  return {
    category: classification.category,
    priority: adjustedPriority,
    team,
    tags: classification.tags,
    suggestedArticles: await findRelatedArticles(ticket.subject),
    autoResponse: classification.confidence > 0.9
      ? generateAutoResponse(classification, ticket)
      : null,
  };
}

// SLA enforcement
interface SLAPolicy {
  priority: string;
  firstResponseMinutes: number;
  resolutionMinutes: number;
}

const SLA_POLICIES: SLAPolicy[] = [
  { priority: "urgent", firstResponseMinutes: 30, resolutionMinutes: 240 },
  { priority: "high", firstResponseMinutes: 120, resolutionMinutes: 480 },
  { priority: "normal", firstResponseMinutes: 480, resolutionMinutes: 1440 },
  { priority: "low", firstResponseMinutes: 1440, resolutionMinutes: 4320 },
];

async function checkSLABreaches(): Promise<SLABreach[]> {
  const openTickets = await getOpenTickets();
  const breaches: SLABreach[] = [];

  for (const ticket of openTickets) {
    const policy = SLA_POLICIES.find((p) => p.priority === ticket.priority);
    if (!policy) continue;

    const now = new Date();
    const age = (now.getTime() - ticket.createdAt.getTime()) / 60000;

    // First response SLA
    if (!ticket.firstResponseAt && age > policy.firstResponseMinutes) {
      breaches.push({
        ticketId: ticket.id,
        type: "first_response",
        minutesOverdue: Math.round(age - policy.firstResponseMinutes),
      });
    }

    // Resolution SLA
    if (!ticket.resolvedAt && age > policy.resolutionMinutes) {
      breaches.push({
        ticketId: ticket.id,
        type: "resolution",
        minutesOverdue: Math.round(age - policy.resolutionMinutes),
      });
    }
  }

  return breaches;
}
```

**Why:** AI-powered triage routes tickets to the right team faster, reducing first-response time. Revenue-based priority escalation ensures high-value customers get appropriate attention. SLA monitoring provides accountability and surfaces systemic issues (if a category consistently breaches SLA, it signals a product or documentation gap).

---

### Pattern 3: Customer Health Scoring

**When to use:** Proactively identifying at-risk customers before they churn.

**Implementation:**

```typescript
// Health score calculation
interface HealthSignal {
  name: string;
  weight: number;
  score: (customer: Customer) => number; // 0-100
}

const healthSignals: HealthSignal[] = [
  {
    name: "product_usage",
    weight: 0.3,
    score: (c) => {
      const weeklyActive = c.loginDaysLast30 / 30 * 100;
      return Math.min(100, weeklyActive * 1.5);
    },
  },
  {
    name: "feature_adoption",
    weight: 0.2,
    score: (c) => {
      const total = CORE_FEATURES.length;
      const adopted = c.featuresUsed.filter((f) => CORE_FEATURES.includes(f)).length;
      return (adopted / total) * 100;
    },
  },
  {
    name: "support_sentiment",
    weight: 0.15,
    score: (c) => {
      if (c.ticketsLast90Days === 0) return 70; // Neutral
      const resolved = c.resolvedTicketsLast90Days / c.ticketsLast90Days;
      return resolved * 100;
    },
  },
  {
    name: "expansion_signals",
    weight: 0.15,
    score: (c) => {
      const usageGrowth = c.currentMonthUsage / (c.previousMonthUsage || 1);
      if (usageGrowth > 1.2) return 100;
      if (usageGrowth > 1.0) return 70;
      if (usageGrowth > 0.8) return 40;
      return 10;
    },
  },
  {
    name: "payment_health",
    weight: 0.2,
    score: (c) => {
      if (c.failedPaymentsLast90Days > 2) return 20;
      if (c.failedPaymentsLast90Days > 0) return 60;
      return 100;
    },
  },
];

function calculateHealthScore(customer: Customer): {
  score: number;
  status: "healthy" | "at-risk" | "critical";
  signals: Array<{ name: string; score: number; weight: number }>;
} {
  const signals = healthSignals.map((signal) => ({
    name: signal.name,
    score: signal.score(customer),
    weight: signal.weight,
  }));

  const weightedScore = signals.reduce(
    (total, s) => total + s.score * s.weight,
    0
  );

  return {
    score: Math.round(weightedScore),
    status: weightedScore >= 70 ? "healthy" : weightedScore >= 40 ? "at-risk" : "critical",
    signals,
  };
}

// Scheduled job: calculate health scores and alert CSMs
async function updateHealthScores(): Promise<void> {
  const customers = await db.customer.findMany({
    where: { subscriptionStatus: "active" },
    include: { usage: true, tickets: true, payments: true },
  });

  for (const customer of customers) {
    const health = calculateHealthScore(customer);

    await db.customerHealth.upsert({
      where: { customerId: customer.id },
      create: { customerId: customer.id, ...health },
      update: health,
    });

    // Alert CSM for critical customers
    if (health.status === "critical" && customer.mrr >= 1000) {
      await notifyCSM(customer.csmId, {
        customer: customer.name,
        score: health.score,
        signals: health.signals.filter((s) => s.score < 40),
      });
    }
  }
}
```

**Why:** Health scoring transforms reactive support (wait for churn) into proactive customer success (intervene before churn). Composite scores combining usage, support sentiment, feature adoption, and payment health give a holistic view. Automated alerts for critical accounts ensure high-value customers get timely CSM attention.

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Bot-only support with no human escalation | Frustrated customers, churn | Bot for triage + knowledge, human for resolution |
| No context passed on escalation | Customer repeats everything | Pass full conversation history + account data |
| Measuring success by tickets closed | Incentivizes premature closure | Measure first-contact resolution + customer effort |
| Knowledge base with no feedback loop | Stale, unhelpful articles persist | Track helpfulness votes, flag low performers |
| Same SLA for all customers | Enterprise customers get same priority as free | Tiered SLAs based on plan and revenue |
| Support separate from product feedback | Miss patterns that could prevent tickets | Tag tickets as product feedback, surface trends |

---

## Checklist

- [ ] Knowledge base searchable via hybrid search (semantic + full-text)
- [ ] In-app contextual help widget on key pages
- [ ] Support tickets auto-triaged with AI classification
- [ ] SLA policies defined per priority level
- [ ] SLA breach monitoring with escalation alerts
- [ ] Customer health scores calculated on schedule
- [ ] High-value at-risk customers trigger CSM alerts
- [ ] Full context (conversation + account data) on every escalation
- [ ] Article helpfulness tracked with feedback loop
- [ ] Support trends surfaced to product team monthly

---

## Related Resources

- **Skills:** `llm-app-development` (chatbot RAG), `product-analytics` (support funnel analysis)
- **Skills:** `email-systems` (support notification emails), `accessibility-a11y` (accessible help widgets)
- **Rules:** `rules/stacks/react-typescript.md` (help widget components)
