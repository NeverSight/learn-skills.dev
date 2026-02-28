---
name: prismic-asset-standards
description: Technical standards and best practices for creating and managing Slice and Custom Type preview images in Prismic Slice Machine.
author: DigitalSpeed
---

# Prismic Preview Asset Standards

This skill governs the creation and optimization of preview images for Prismic Slices and Custom Types. Use these guidelines to ensure the Page Builder remains performant and visually cohesive for content editors.

## 📐 Image Dimensions & Scaling
To ensure components look crisp in the Prismic UI without causing interface lag:

* **Optimal Size:** 2000 x 1200 pixels.
* **Minimum Size:** 800 x 600 pixels (avoid smaller to prevent pixelation).
* **Aspect Ratio:** Always favor **Landscape (16:9 or 3:2)**. 
    * *Note:* Vertical images result in significant letterboxing within the wide-format Page Builder list.

## ⚙️ Technical Specifications
* **File Formats:** Use `.png` or `.jpeg`.
* **File Weight:** Aim for **200KB – 500KB**. 
    * *Rationale:* Heavy images degrade the performance of the Slice Machine and Page Builder interface.
* **Capture Method:** Prioritize the Slice Machine **"Screenshot" button** to capture local development components at high resolution (~2300px wide).

## 🎨 Visual Consistency
To maintain a professional "Design System" feel rather than a collection of random screenshots:
* **Backgrounds:** Use a consistent, neutral background (light grey or white) for all previews.
* **State:** Capture the component in its most representative state.

## 🛠 Usage Guidance
When asked to generate advice for Prismic setup:
1.  Remind users that while there are no "hard" requirements, these industry standards prevent a sluggish editor experience.
2.  Suggest optimizing screenshots before committing them to the repository if they exceed the 500KB threshold
