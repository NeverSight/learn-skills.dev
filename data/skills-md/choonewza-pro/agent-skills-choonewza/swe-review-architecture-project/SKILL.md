---
name: swe-review-architecture-project
description: >-
  รีวิว Tech Stack, Dependencies, และโครงสร้างโปรเจคอย่างละเอียด พร้อม Version matrix และคำแนะนำด้าน security/compatibility
  ใช้ skill นี้ทันทีเมื่อผู้ใช้พูดถึง: 'ช่วยรีวิวโปรเจคนี้', 'โปรเจคนี้ใช้ tech stack อะไร', 'วิเคราะห์โปรเจค', 'project structure', 
  'ดู dependencies', 'เช็ค package', 'มี library อะไรบ้าง', 'โปรเจคใช้อะไรบ้าง' หรือเมื่อผู้ใช้แชร์ไฟล์ package.json / 
  requirements.txt / pyproject.toml / pom.xml / go.mod / Cargo.toml / composer.json แล้วถามเกี่ยวกับโปรเจค
license: MIT
---

# Review Architecture Project Skill

## Step 1 — อ่านไฟล์โปรเจค

อ่านไฟล์ที่มีอยู่ในโปรเจค โดยเริ่มจาก README.md ก่อน แล้วตามด้วยไฟล์ dependency ตามภาษา/ecosystem ที่ใช้:

- **Node.js**: `package.json`, lockfile (`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`)
- **Python**: `requirements.txt`, `pyproject.toml`, `Pipfile`, `uv.lock`
- **Java/Kotlin**: `pom.xml`, `build.gradle`
- **Go**: `go.mod` | **Rust**: `Cargo.toml` | **PHP**: `composer.json` | **Ruby**: `Gemfile`

อ่านเพิ่มเติมถ้ามี: `Dockerfile`, `docker-compose.yml`, `tsconfig.json`, `.env.example`, config files (vite/next/webpack), CI/CD pipelines

ดูโครงสร้างโฟลเดอร์:

```bash
find . -type f | grep -v node_modules | grep -v .git | grep -v __pycache__ | head -60
```

## Step 2 — Output

**สรุปภาพรวม** — โปรเจคนี้คืออะไร ใช้ stack อะไรหลัก

**Tech Stack & Dependencies** — แสดงเป็นตาราง แยก production vs dev พร้อม version และหน้าที่ของแต่ละ package

**Project Structure** — โครงสร้างโฟลเดอร์หลักพร้อมคำอธิบายสั้นๆ

**ข้อสังเกต** — ระบุเฉพาะที่เจอจริง เช่น outdated packages, security concerns, version conflicts หรือ good practices
