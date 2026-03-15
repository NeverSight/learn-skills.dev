---
name: resume-a4-generator
description: Generate or update a professional A4 resume based on a premium layout and engineering/architecture-centric vibe.
---

# Resume A4 Generator Skill

This skill allows the AI to generate a professional, A4-sized PDF-printable resume (HTML/CSS) using a structured template. It is designed to highlight engineering excellence, system architecture depth, and product design thinking.

> [!IMPORTANT]
> **Language Selection**: Before generating any content, you **MUST** ask the user whether they prefer the resume in **Chinese** or **English**.

## 📐 Core Structure

### 1. Basic Info (Header)
The header is clean and structured to present high-level information at a glance.
- **Title**: Large bold name (ZH + EN), followed by a high-level role summary.
- **Contact Grid**: A 2-column grid including:
  - Age / Work Experience Years.
  - Phone / Email.
  - Social Profiles (GitHub, Portfolio, Bilibili, etc.).
- **Profile Photo**: 160px x 210px aligned to the right.

### 2. Standard Sections
- **Core Skills (`.skills-grid`)**: Hierarchical list of categories (e.g., AI Coding, Full-stack Architecture, Product Thinking).
- **Education (`.edu-item`)**: Chronological education history with schools and degrees.
- **Work Experience (`.job-item`)**: 
  - Company, Role, and Date range.
  - Content should focus on "Engineering Growth," "Technical Solutions," and "Business Impact."
- **GitHub Activity**: Visual section for showcasing open-source contributions.
- **Honors & Sharing**: Chronological list of awards, talks, and community contributions.

## 🎨 Aesthetics & Vibe (Design System)

- **Typography**: Inter (modern/clean) for English; Noto Sans SC (balanced) for Chinese.
- **Layout**: Fixed A4 `210mm` x `297mm` container with `60mm` horizontal padding.
- **Colors**:
  - Primary: `#333` (Deep Gray/Black)
  - Secondary: `#666` (Medium Gray for descriptions)
  - Background: `#fff` (Page), `#f9f9f9` (Header background)
  - Borders/Lines: `#eee` (Soft separation)
- **Vibe Description**: 
  - "Professional, Engineering-Focused, Structured."
  - Avoid flowery language; use action-oriented verbs (主导, 落地, 演进, 深度, 优化).
  - Emphasize complex technical challenges and their solutions.

## 📝 Usage for Expansion
When adding new content (e.g., a new job or project):
1.  **Style Consistency**: Use `.job-item` for career steps and `.job-point` for details.
2.  **Point Structure**: `[Bold Title] : [Description]`.
3.  **Vibe**: Maintain the "Architectural" tone. Focus on system stability, concurrency, architecture evolution, and engineering efficacy.

## 📂 Resources
- [Main Template](./resources/template.html) (A4 Page Structure)
- [Item Templates](./resources/item-templates.html) (Education, Job, Skill blocks)
- [HR Favorite Resume Format](./resources/hr-favorite-format.png) (Visual Reference)
- [PDF Print Settings](./resources/pdf-print-settings.png) (Export Configuration)
