---
name: swe-reports-guide
description: Guidelines and file locations for writing feature and bug fix reports for executives or management. Triggers on requests to write development reports, executive summaries, status updates, feature reports, or bug fix reports.
metadata:
  author: choonewza@gmail.com
  version: "1.0.0"
---

# Dev Reports Guide for Executives

This skill defines the directory structure and writing standards for development and bug fix reports destined for company leadership and executives.

> [!IMPORTANT]
> **MANDATORY PREREQUISITE**: Before writing or modifying ANY development report, status update, or executive summary, you **MUST** read and follow the instructions in the [swe-management-talk](../swe-management-talk/SKILL.md) agent skill. Do not rely on memory — always read the skill file to ensure correct tone, vocabulary, and formatting.

## 1. Directory Structure & File Locations

All reports for executives must be stored in the appropriate subdirectories under `./docs/dev-reports/` as Markdown (`.md`) files:

| Report Type      | Directory Path                 | Example File Path                                              |
| :--------------- | :----------------------------- | :------------------------------------------------------------- |
| **New Features** | `./docs/dev-reports/features/` | `./docs/dev-reports/features/2026-07-06-occasion-mode.md`      |
| **Bug Fixes**    | `./docs/dev-reports/fix-bugs/` | `./docs/dev-reports/fix-bugs/2026-06-26-fix-authentication.md` |

_Note: All filenames must be prefixed with the creation date in `YYYY-MM-DD-` format (e.g., `2026-07-06-redesign-attach-files.md`). If the target directory does not exist, create it. If there is an existing legacy folder named `fix-bug`, align or migrate files to the standard `./docs/dev-reports/fix-bugs/` path as appropriate._

## 2. Writing Standards & Tone

When writing reports for leadership, strictly adhere to the following principles from the `management-talk` skill:

1. **Audience Focus**: Write for engineering-savvy non-engineers (VPs, directors, PMs). They care about _state, customer/business impact, ownership, and next steps_.
2. **Language**: Use professional, polite, and elegant Thai (unless English is explicitly requested) since the project UI is in Thai and the target audience is Thai leadership.
3. **Information Filtering**:
   - **Keep**: Product names, high-level framework names, system-level component names (e.g., Prisma, PostgreSQL, Server Actions, clean architecture layers).
   - **Strip**: Code-level details, function names, raw database column names, file paths, commit SHAs, line numbers, and internal debugging minutiae.
   - **Translate**: Technical mechanisms into plain-English/plain-Thai cause-and-effect (e.g., instead of "caching in local storage to prevent hydrating mismatch", write "saving user preference in browser storage to prevent showing the pop-up repeatedly").

## 3. Required Report Sections

Each executive report should be structured with the following sections:

1. **Header**: Clear title, date, and development status (e.g., Completed, Staging, In Progress).
2. **บทสรุปผู้บริหาร (Executive Summary / TL;DR)**: A bolded summary of what the feature/fix is and its current state.
3. **คุณค่าทางธุรกิจและผลกระทบต่อผู้ใช้งาน (Business Value & UX Impact)**: Bullet points explaining how this improves the brand, solves customer pain points, or increases efficiency.
4. **รายละเอียดความสามารถหลัก (Key Capabilities)**: Plain-language details of what was developed or resolved.
5. **โครงสร้างระบบและความปลอดภัย (Technical Foundation & Security)**: A high-level description of the architecture and security measures.
6. **สถานะปัจจุบันและแผนงานถัดไป (Current Status & Next Steps)**: A checklist of completed tasks and near-term milestones (e.g., Deploy to Staging, QA testing, Admin guidelines, Production release).
