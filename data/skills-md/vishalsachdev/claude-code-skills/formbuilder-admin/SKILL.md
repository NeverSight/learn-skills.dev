---
name: formbuilder-admin
description: >
  Create, edit, and manage forms in the University of Illinois ATLAS FormBuilder Admin
  application (appserv7.admin.uillinois.edu/FormBuilderAdmin). Use when the user needs to
  work with FormBuilder forms including: creating or editing form questions and sections,
  configuring event session categories and event sessions, setting up payment line items
  and CFOAPAL codes, managing workflow phases and routing triggers with conditional statements,
  configuring authentication and self-registration for local users, editing form periods,
  managing waitlists and registration limits, setting up question triggers for conditional
  visibility, working with text merge fields, handling form responses and reports,
  or troubleshooting form behavior. Keywords: FormBuilder, ATLAS, UIUC, form builder,
  event registration, survey, form questions, payment configuration, workflow, routing
  triggers, phases, event sessions, iPay, CFOAPAL.
compatibility: >
  Requires browser automation with computer use (Claude Desktop, Claude.ai with computer use,
  or similar). The admin interface is a web application at appserv7.admin.uillinois.edu.
---

# FormBuilder Admin

FormBuilder is a University of Illinois web application for creating customizable forms,
surveys, and event registration workflows. The admin interface is at
`appserv7.admin.uillinois.edu/FormBuilderAdmin`.

## Key Concepts

FormBuilder organizes work in a hierarchy: **Unit > Form Group > Form**. Each form has
**periods** (time windows when the form is active), **phases** (workflow steps), **sections**
(content containers), and **questions** (data fields). Phases are connected by **routing
triggers** that move form responses through the workflow when conditions are met.

There are three phase types: **Data Collection** (where users fill out the form),
**Review Approval** (where admins review responses), and **Archive** (final storage).
Only one Data Collection and one Archive phase are allowed per form.

Forms can be **Standard** or **Event Registration** (which adds event sessions, guest
questions, and registration management). Event registration has two modes: **Standard Mode**
(automatic registration on submit) and **Advanced Mode** (registration controlled by routing
triggers). This choice is irreversible.

## Navigation

The admin URL pattern is:
`appserv7.admin.uillinois.edu/FormBuilderAdmin/Unit/{unitId}/FormGroup/{groupId}/Form/{formId}/...`

Key pages append to the Form URL:
- `/Contents` — Form contents editor (questions, sections)
- `/Contents/PaymentInformation` — Payment line items
- `/Lifecycle` — Workflow diagram
- `/Phases` — Phase list and settings
- `/RoutingTriggers` — Routing trigger list
- `/Properties` — Form properties (title, authentication, payment details)
- `/Periods` — Period management
- `/Periods/EventSessions?periodId={id}` — Event sessions for a period
- `/EventSessionCategories` — Event session categories (form-level)

**Important:** Breadcrumb navigation sometimes fails in this application. Prefer direct URL
navigation by constructing the URL from the known base path. Use the sidebar hamburger menu
(☰) for top-level navigation.

## Core Workflows

For detailed procedures on each area, see the reference files:

- **Questions and Sections:** See [references/form-contents.md](references/form-contents.md)
  for adding/editing questions, question types, sections, and question triggers.
- **Event Sessions:** See [references/event-sessions.md](references/event-sessions.md) for
  session categories, creating sessions, and linking sessions to questions and payments.
- **Payments:** See [references/payments.md](references/payments.md) for enabling payments,
  adding payment line items, and CFOAPAL configuration.
- **Workflow and Lifecycle:** See [references/workflow-lifecycle.md](references/workflow-lifecycle.md)
  for phases, routing triggers, conditional statements, and routing actions.
- **Authentication and Access:** See [references/authentication-and-access.md](references/authentication-and-access.md)
  for local user self-registration, security groups, periods, and form access.
- **Troubleshooting:** See [references/gotchas.md](references/gotchas.md) for known pitfalls
  and hard-to-discover fixes.

## Safety Guidelines

- **Always confirm destructive actions** with the user before executing (deleting triggers,
  phases, questions, or responses).
- **Edit triggers before deleting phases.** If a routing trigger references a phase and you
  delete that phase first, the trigger will have a broken reference. Always update or remove
  trigger references to a phase before deleting it.
- **Work step by step.** For multi-step changes (especially workflow modifications), execute
  one step at a time and verify with the user before proceeding.
- **Maintain a change log.** When making multiple changes, keep a running list of what was
  changed so the user can audit and revert if needed.
- **Archive rather than delete questions** when possible. Archiving (setting Is Active to
  unchecked) preserves historical data while hiding the question from the form.
- **Test in Test Email Mode** before going live. When Test Email Mode is on, all emails route
  to the form group's testing email address instead of real recipients.

## UI Interaction Patterns

The admin interface uses a left-panel/right-preview layout on the Form Contents page. Key
patterns:

- **Global Settings panel** (left side): Select the active phase, view payment info, and add
  phases/sections.
- **Form Preview panel** (right side): Shows the form as it appears to users. Click a section
  or question to select it, then use the Form Contents panel to edit/add.
- **Gear icon (⚙):** Used on many list pages (Phases, Routing Triggers, Event Sessions) to
  access Edit/Delete options via dropdown.
- **Blue "EDIT" buttons:** Direct edit access on list items.
- **"+ ADD NEW..." buttons:** Appear in section headers to add new items.
- **Save Changes / Save button:** Always at the bottom of editing panels. Changes are NOT
  auto-saved.
- **Sidebar editing panels:** When editing questions, triggers, or line items, a panel slides
  in from the left or opens inline. Scroll down within this panel to see all fields.