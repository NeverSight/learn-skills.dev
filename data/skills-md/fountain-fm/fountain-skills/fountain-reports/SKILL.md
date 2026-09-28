---
name: fountain-reports
description: Build the reports the user reads - compose components into a preset, then email or print it.
---

## Overview

This skill owns how a report looks, so no caller invents its own format.
A report is a preset, which is an ordered list of components.
Each component is a markdown template that the data fills.
The caller names the preset and gives the data.
This skill composes the report.
It delivers the report the way the Reporting section asks: email, printed, combined with a later report,
or not at all.
The user customizes a preset once, in the preferences, and every later report follows that customization.

## Input

- The preset name.
- The data that the preset's components need, from the caller.
- Optional: the surface, when the user is present and asks to read the report here.
- Report customizations from the Reporting section of the preferences, when the show has any.

## Output

- The report, delivered as the Reporting section asks.
  Email is the default.

## Housekeeping

You MUST read HOUSEKEEPING.md if you haven't already.

## Requirements

- Fountain API.
- Skill **fountain-onboarding**.

## Process

1. Read the report customizations from the Reporting section of the preferences.
   A customization can drop a component, reorder them, change a subject line, or change the delivery.
2. Read the preset from `assets/presets`, and apply the customization.
3. Fill each component template from `assets/components` with the caller's data.
   Drop a component whose data the caller did not give, and say so after the send.
   This rule never drops a component that needs no data, because that component is never missing data.
   Only a customization can drop it.
4. Deliver the report as the Reporting section asks: email via the Project API, printed in the chat,
   combined into a report sent later in the same run, or not at all.
   Email is the default, and goes to the addresses under Reporting.
   Run skill **fountain-onboarding** when the section holds no addresses.
   When the caller asks for both, send the report and also print it in the chat.
   When the user asked only to read it here, print it instead of sending it.
   A printed report has the same words as the sent report.
   So the reader never has to open the mail to learn what the chat left out.
   Say plainly when a report was composed but not sent.
   A send that returns success is not proof of delivery, so say which of the two you saw.

## Additional notes

The presets:

- `performance` - the numbers for a window: headline, channels overview, yesterday's clips, learnings,
  warnings.
- `review-posts-simple` - the posts that wait for a decision, and nothing else.
  The reader reads the words in the dashboard, where the reader approves or deletes.
  So the mail says which posts exist, and sends the reader to the dashboard.
  The approve note says whether approving renders a clip or sends it.
  A second preset does not do this job.
- `review-posts` - the whole day in one mail: the posts that wait for a decision, then the numbers.
  The user asks for it in place of the two presets above.
  The Reporting section records which of these forms the show wants.
- `settings` - the current settings, each with its origin, and the tour of the headings.
  Sent when the user asks what their settings are.

A preset is named for the state that it reports.
It is never named for the occasion, or for the skill that sends it.
So any skill that starts a chain can reuse it unchanged.

The printed surface is for the review in the chat.
There the user reads the same report that the email holds, so the two never disagree.
A caller that prints and sends gives the reader one report in two places, and never two reports.

Combining joins reports, and not machines.
A report can wait only for a report that is sent later in the same run.
This is because nothing holds a pending report between machines.

A component is small and single-purpose.
A new kind of email is a new preset made from the same components.
A missing block is a new component, and never markdown that a caller writes by hand.
This is because two callers that write the same block by hand soon write it in two different ways.

Numbers come from the caller and go into the template unchanged.
This skill formats the numbers.
It MUST NOT recompute, round away, or soften what the caller measured.

Send markdown, and never HTML.
The Project API renders the markdown itself.
It strips every attribute from the result, so styling that this skill sets does not reach the reader.
The Project API styles the tables, and keeps the column alignment that the markdown sets.
So markdown holds everything that a report needs.
