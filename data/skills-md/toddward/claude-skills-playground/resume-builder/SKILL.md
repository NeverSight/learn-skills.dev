---
name: resume-builder
description: Generate beautiful, professionally designed resumes as 1-2 page PDFs. Creates clean, sophisticated layouts that balance visual appeal with readability, tailored to specific job opportunities when provided.
license: Complete terms in LICENSE.txt
---

# Resume Builder Skill

This skill creates beautifully designed, professional resumes as PDF documents. The output prioritizes clean typography, thoughtful spacing, and visual hierarchy while maintaining the practical readability employers expect.

## Required Information

Before beginning, gather:

1. **Resume Context** (REQUIRED): The user's professional background, including:
   - Work experience with roles, companies, dates, and accomplishments
   - Education background
   - Skills and competencies
   - Any additional relevant sections (certifications, projects, publications, etc.)

2. **Address Verification** (ALWAYS ASK): 
   - Prompt the user: "What address should appear on your resume? Has this changed from any previous version?"
   - If they have an existing resume, confirm the address is current

3. **Job-Specific Information** (OPTIONAL):
   - If applying for a specific role, request the job description or posting link
   - Ask: "Would you like me to create a cover letter as well?"
   - When tailoring to a job, use web_fetch to analyze the job description and align resume content accordingly

## Design Philosophy

Resumes should be **sophisticated yet accessible** - think of them as the intersection of:
- **Swiss design clarity**: Clean grids, thoughtful hierarchy, generous whitespace
- **Editorial polish**: Typography that's refined but never fussy
- **Scannable structure**: Easy for both human readers and ATS systems

### Visual Principles

**Typography**:
- Use 2-3 fonts maximum from `./assets/fonts` directory
- Recommended combinations:
  - **Professional/Corporate**: Inter (headers & body) - Clean, highly readable, excellent at all sizes
  - **Creative/Modern**: Special Gothic (headers) + Open Sans (body) - Distinctive yet professional
  - **Traditional/Academic**: Open Sans throughout - Reliable, approachable, universally compatible
- Headers: Clean, confident sans-serifs (moderate weight, not ultra-bold)
- Body: Highly readable sans-serif at 10-11pt
- Hierarchy through size, weight, and spacing - not color chaos

**Layout**:
- Generous margins (0.5-0.75 inches minimum)
- Clear section divisions using whitespace, not heavy lines
- Consistent spacing that creates rhythm
- Single column or subtle two-column for optimal readability

**Color** (use sparingly):
- Primarily black text on white
- Optional: One accent color for headers or subtle elements
- Never sacrifice readability for visual flair

**Spacing**:
- Every element has breathing room
- No cramped text or overlapping elements
- Page breaks must fall naturally between sections
- If content exceeds one page, ensure page 2 is substantial (not just a few lines)

## Content Guidelines

### Language & Tone

**CRITICAL**: Maintain authentic, professional language. Do NOT:
- Use buzzwords excessively (synergy, rockstar, ninja, guru)
- Over-inflate accomplishments with hyperbole
- Write in third person or use overly formal Victorian prose
- Create generic, template-sounding bullet points

Instead:
- Use clear, direct language with strong action verbs
- Quantify achievements where possible (numbers, percentages, scale)
- Be specific about technologies, methodologies, and outcomes
- Let accomplishments speak for themselves without excessive adjectives

### Structure

**Standard Sections** (adapt as needed):
1. **Header**: Name (prominent), contact info (email, phone, LinkedIn, location)
2. **Professional Summary** (optional, 2-3 lines maximum if included)
3. **Experience**: Company, Title, Dates, 3-5 bullet points per role
4. **Education**: Degree, Institution, Graduation year, relevant honors
5. **Skills**: Organized logically (by category if extensive)
6. **Additional Sections** as relevant: Certifications, Projects, Publications, Languages, etc.

### Job-Specific Tailoring

When a job description is provided:
1. Analyze key requirements, skills, and keywords from the posting
2. Reorder or emphasize relevant experience
3. Adjust bullet points to highlight applicable accomplishments
4. Mirror language from the job posting (naturally, not robotically)
5. Ensure skills section reflects the role's technical requirements
6. Keep changes authentic - never fabricate or exaggerate

## PDF Creation Process

### Step 1: Information Gathering
```
Collect resume context, verify address, check for job-specific needs
```

### Step 2: Content Organization
```
- Parse experience, education, skills
- Determine optimal structure
- If job posting provided, analyze and tailor content
- Decide on 1 vs 2 pages based on experience level
```

### Step 3: Design Selection
```
Choose a visual approach that balances sophistication with convention:
- Professional services/Corporate: Clean, minimal, traditional
- Creative/Design roles: More personality, thoughtful typography
- Tech/Startup: Modern, crisp, slightly less formal
- Academic/Research: Traditional, content-dense, clear hierarchy
```

### Step 4: PDF Generation

Use Python with reportlab or similar library to create the PDF:

**Page Setup**:
- Letter size (8.5" x 11")
- Margins: 0.5-0.75" on all sides
- If 2 pages needed, ensure clean break between pages

**Typography**:
- Load fonts from `./assets/fonts` directory
- Available fonts: Inter (variable font), Open Sans (variable font), Special Gothic, Montserrat, BBH Sans Bogle
- Register custom fonts with the PDF library using absolute paths
- Use variable fonts (Inter, Open Sans) for flexible weight options
- Set consistent font sizes and line heights

**Layout Implementation**:
- Build content section by section
- Monitor page length to avoid awkward breaks
- If approaching page limit, make strategic decisions:
  - Tighten spacing slightly (without cramping)
  - Move to 2 pages if content warrants it
  - Never cut off content mid-section

**Quality Checks**:
- All text within margins
- No overlapping elements
- Consistent spacing throughout
- Page breaks fall naturally
- Contact information clearly visible
- No orphaned single lines on page 2

### Step 5: Refinement

Before outputting:
- Review hierarchy - can you scan and find key info quickly?
- Check whitespace - does the page breathe?
- Verify no content is cut off or awkwardly broken
- Ensure typography is crisp and professional
- Confirm all user information is accurate

## Cover Letter Generation

If requested alongside resume:

**Structure**:
- Header matching resume (name, contact info)
- Date and employer address
- Professional greeting
- 3-4 paragraphs maximum:
  1. Opening: Position + enthusiasm + brief hook
  2. Why them: Company-specific interest and alignment
  3. Why you: Relevant experience and value proposition
  4. Closing: Call to action and thanks
- Professional sign-off

**Tone**:
- Professional but personable
- Confident without arrogance
- Specific to the company and role
- Avoid generic template language
- Match the company's communication style (formal vs. casual)

**Design**:
- Match resume typography and layout
- Clean, letter-like presentation
- Single page always

## Output

Provide:
1. **resume.pdf** - The completed 1-2 page resume
2. **cover-letter.pdf** (if requested) - Matching cover letter
3. Brief summary noting:
   - Any content decisions made (what was emphasized/de-emphasized)
   - Page count and reasoning
   - Tailoring decisions if job-specific

## Examples of Good Practice

**Information Density**: 
- ✅ "Led team of 8 engineers to deliver customer portal, reducing support tickets by 40%"
- ❌ "Synergistically optimized team dynamics to revolutionize customer experience"

**Page Length**:
- Early career (0-5 years): 1 page
- Mid-career (5-15 years): 1-2 pages
- Senior/Executive (15+ years): 2 pages
- If page 2 would only have 3-4 lines, tighten page 1 instead

**Visual Hierarchy**:
- Name: 18-24pt
- Section headers: 12-14pt
- Job titles: 11-12pt
- Body text: 10-11pt
- Dates/secondary info: 9-10pt

## Critical Reminders

- **Never sacrifice readability for design** - employers need to scan quickly
- **Page breaks are sacred** - content must never be cut off awkwardly
- **Authenticity over inflation** - normal, confident professional language
- **Tailoring is strategic** - emphasize relevant experience, don't fabricate
- **Whitespace is professional** - cramming content looks desperate
- **Test the scan** - can someone find your name, current role, and key skills in 10 seconds?

The goal is a resume that looks like it was designed by someone with impeccable taste who understands that a resume's job is to get interviews, not win design awards.