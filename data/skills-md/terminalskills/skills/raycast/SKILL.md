---
name: raycast
description: Expert guidance for building Raycast extensions — custom commands, views, and integrations for the Raycast launcher on macOS. Helps developers create productivity extensions using React, TypeScript, and Raycast's API for lists, forms, actions, and preferences.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
  - launcher
  - productivity
  - macos
  - extensions
  - react
---

# Raycast — macOS Launcher Extension Development


## Overview


Building Raycast extensions — custom commands, views, and integrations for the Raycast launcher on macOS. Helps developers create productivity extensions using React, TypeScript, and Raycast's API for lists, forms, actions, and preferences.


## Instructions

### List View Command

Build a searchable list command:

```tsx
// src/search-projects.tsx — Search and open projects from a list
import { List, Action, ActionPanel, Icon, Color, getPreferenceValues } from "@raycast/api";
import { useFetch } from "@raycast/utils";

interface Project {
  id: string;
  name: string;
  url: string;
  language: string;
  stars: number;
  updatedAt: string;
}

export default function SearchProjects() {
  const prefs = getPreferenceValues<{ githubToken: string }>();

  const { data, isLoading } = useFetch<{ items: Project[] }>(
    "https://api.github.com/user/repos?sort=updated&per_page=50",
    {
      headers: { Authorization: `Bearer ${prefs.githubToken}` },
      mapResult: (result: any) => ({
        data: { items: result },
      }),
    }
  );

  return (
    <List isLoading={isLoading} searchBarPlaceholder="Search your repos...">
      {data?.items.map((project) => (
        <List.Item
          key={project.id}
          title={project.name}
          subtitle={project.language}
          accessories={[
            { text: `⭐ ${project.stars}` },
            { date: new Date(project.updatedAt), tooltip: "Last updated" },
          ]}
          icon={{ source: Icon.Code, tintColor: Color.Blue }}
          actions={
            <ActionPanel>
              <Action.OpenInBrowser url={project.url} title="Open on GitHub" />
              <Action.CopyToClipboard
                content={`git clone ${project.url}.git`}
                title="Copy Clone URL"
              />
              <Action.Open
                title="Open in VS Code"
                target={project.url}
                application="Visual Studio Code"
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

### Detail View

Show rich content with markdown:

```tsx
// src/show-readme.tsx — Display a project README with rich formatting
import { Detail, Action, ActionPanel } from "@raycast/api";
import { useFetch } from "@raycast/utils";

export default function ShowReadme({ repoName }: { repoName: string }) {
  const { data, isLoading } = useFetch<string>(
    `https://api.github.com/repos/${repoName}/readme`,
    {
      headers: { Accept: "application/vnd.github.raw" },
      mapResult: (result: any) => ({ data: result }),
    }
  );

  const markdown = data ?? "Loading...";

  return (
    <Detail
      isLoading={isLoading}
      markdown={markdown}
      metadata={
        <Detail.Metadata>
          <Detail.Metadata.Label title="Repository" text={repoName} />
          <Detail.Metadata.Link title="GitHub" target={`https://github.com/${repoName}`} text="Open" />
          <Detail.Metadata.Separator />
          <Detail.Metadata.TagList title="Topics">
            <Detail.Metadata.TagList.Item text="typescript" color={Color.Blue} />
            <Detail.Metadata.TagList.Item text="react" color={Color.Green} />
          </Detail.Metadata.TagList>
        </Detail.Metadata>
      }
      actions={
        <ActionPanel>
          <Action.CopyToClipboard content={markdown} title="Copy README" />
        </ActionPanel>
      }
    />
  );
}
```

### Form Command

Collect user input with forms:

```tsx
// src/create-issue.tsx — Form to create a GitHub issue
import { Form, Action, ActionPanel, showToast, Toast, popToRoot } from "@raycast/api";
import { useState } from "react";

export default function CreateIssue() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(values: {
    repo: string;
    title: string;
    body: string;
    labels: string[];
    priority: string;
  }) {
    setIsSubmitting(true);

    try {
      const response = await fetch(`https://api.github.com/repos/${values.repo}/issues`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getPreferenceValues().githubToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: values.title,
          body: values.body,
          labels: values.labels,
        }),
      });

      if (!response.ok) throw new Error("Failed to create issue");

      const issue = await response.json();
      await showToast({
        style: Toast.Style.Success,
        title: "Issue Created",
        message: `#${issue.number}: ${issue.title}`,
        primaryAction: {
          title: "Open in Browser",
          onAction: () => open(issue.html_url),
        },
      });
      popToRoot();
    } catch (error) {
      await showToast({ style: Toast.Style.Failure, title: "Error", message: String(error) });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Form
      isLoading={isSubmitting}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Create Issue" onSubmit={handleSubmit} />
        </ActionPanel>
      }
    >
      <Form.TextField id="repo" title="Repository" placeholder="owner/repo" />
      <Form.TextField id="title" title="Title" placeholder="Bug: ..." />
      <Form.TextArea id="body" title="Description" placeholder="Describe the issue..." enableMarkdown />
      <Form.TagPicker id="labels" title="Labels">
        <Form.TagPicker.Item value="bug" title="🐛 Bug" />
        <Form.TagPicker.Item value="feature" title="✨ Feature" />
        <Form.TagPicker.Item value="docs" title="📝 Docs" />
      </Form.TagPicker>
      <Form.Dropdown id="priority" title="Priority" defaultValue="medium">
        <Form.Dropdown.Item value="low" title="Low" />
        <Form.Dropdown.Item value="medium" title="Medium" />
        <Form.Dropdown.Item value="high" title="High" />
        <Form.Dropdown.Item value="critical" title="Critical" />
      </Form.Dropdown>
    </Form>
  );
}
```

### Local Storage and Cache

Persist data across command runs:

```typescript
// src/lib/storage.ts — Cache and persist data
import { LocalStorage, Cache } from "@raycast/api";

const cache = new Cache();

// Cache for frequently accessed data (memory + disk, auto-evicts)
async function getCachedRepos(): Promise<Project[]> {
  const cached = cache.get("repos");
  if (cached) return JSON.parse(cached);

  const repos = await fetchRepos();
  cache.set("repos", JSON.stringify(repos), { ttl: 300_000 }); // 5-minute TTL
  return repos;
}

// LocalStorage for persistent user data (survives restarts)
async function addToFavorites(repoId: string) {
  const favorites = JSON.parse((await LocalStorage.getItem<string>("favorites")) ?? "[]");
  if (!favorites.includes(repoId)) {
    favorites.push(repoId);
    await LocalStorage.setItem("favorites", JSON.stringify(favorites));
  }
}

async function getFavorites(): Promise<string[]> {
  return JSON.parse((await LocalStorage.getItem<string>("favorites")) ?? "[]");
}
```

### Menu Bar Command

Create a persistent menu bar item:

```tsx
// src/menu-bar.tsx — Always-visible status in the macOS menu bar
import { MenuBarExtra, Icon, open, getPreferenceValues } from "@raycast/api";
import { useFetch } from "@raycast/utils";

export default function StatusMenuBar() {
  const { data, isLoading } = useFetch<any[]>(
    "https://api.github.com/notifications",
    {
      headers: { Authorization: `Bearer ${getPreferenceValues().githubToken}` },
      keepPreviousData: true,
      initialData: [],
    }
  );

  const unread = data?.length ?? 0;

  return (
    <MenuBarExtra
      icon={Icon.Bell}
      title={unread > 0 ? String(unread) : undefined}
      isLoading={isLoading}
    >
      <MenuBarExtra.Section title="Notifications">
        {data?.slice(0, 10).map((notification) => (
          <MenuBarExtra.Item
            key={notification.id}
            title={notification.subject.title}
            subtitle={notification.repository.name}
            onAction={() => open(notification.subject.url)}
          />
        ))}
      </MenuBarExtra.Section>
      {unread > 10 && (
        <MenuBarExtra.Item
          title={`${unread - 10} more...`}
          onAction={() => open("https://github.com/notifications")}
        />
      )}
    </MenuBarExtra>
  );
}
```

### Extension Manifest

Configure commands and preferences:

```json
// package.json — Extension configuration
{
  "name": "my-github-extension",
  "title": "GitHub Tools",
  "description": "Manage GitHub repos, issues, and notifications",
  "icon": "github-icon.png",
  "author": "your-name",
  "categories": ["Developer Tools"],
  "license": "MIT",
  "commands": [
    {
      "name": "search-projects",
      "title": "Search Projects",
      "description": "Search and open your GitHub repositories",
      "mode": "view"
    },
    {
      "name": "create-issue",
      "title": "Create Issue",
      "description": "Create a new GitHub issue",
      "mode": "view"
    },
    {
      "name": "menu-bar",
      "title": "GitHub Notifications",
      "description": "Show unread notifications in menu bar",
      "mode": "menu-bar",
      "interval": "5m"
    }
  ],
  "preferences": [
    {
      "name": "githubToken",
      "title": "GitHub Token",
      "description": "Personal access token with repo scope",
      "type": "password",
      "required": true
    }
  ]
}
```

## Installation

```bash
# Create a new extension
npx create-raycast-extension my-extension

# Development (opens Raycast with hot reload)
npm run dev

# Build and lint
npm run build
npm run fix-lint

# Publish to Raycast Store
npx ray publish
```


## Examples


### Example 1: Setting up Raycast with a custom configuration

**User request:**

```
I just installed Raycast. Help me configure it for my TypeScript + React workflow with my preferred keybindings.
```

The agent creates the configuration file with TypeScript-aware settings, configures relevant plugins/extensions for React development, sets up keyboard shortcuts matching the user's preferences, and verifies the setup works correctly.

### Example 2: Extending Raycast with custom functionality

**User request:**

```
I want to add a custom detail view to Raycast. How do I build one?
```

The agent scaffolds the extension/plugin project, implements the core functionality following Raycast's API patterns, adds configuration options, and provides testing instructions to verify it works end-to-end.


## Guidelines

1. **Fast time-to-interaction** — Show cached data immediately, then update in background; use `keepPreviousData: true`
2. **Use useFetch from @raycast/utils** — Handles caching, revalidation, and loading states automatically
3. **Meaningful accessories** — Show dates, counts, and status in list item accessories; saves users from opening details
4. **Action panel hierarchy** — Most common action first; Cmd+Enter triggers the primary action
5. **Preferences for secrets** — API keys and tokens go in preferences (type: "password"), not hardcoded
6. **Show toasts for feedback** — Success/failure toasts keep users informed without blocking the UI
7. **Menu bar for monitoring** — Use menu bar commands for status that users check frequently (notifications, CI status)
8. **Cache aggressively** — Raycast commands should feel instant; cache API responses and pre-fetch data
