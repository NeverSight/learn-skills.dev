---
name: parasite-case-mcq
description: Create clinical case-based, five-option one-best-answer multiple-choice questions in parasitology that follow medical-education item-writing principles and are classified by physician task (health maintenance, mechanisms of disease, diagnosis, management). Works from a parasite name or from one uploaded research article on the topic. Use when the user requests parasitology questions, examination items, case-based questions, or quizzes, or uploads a parasitology article and asks for items based on it.
license: Apache-2.0 (LICENSE.txt)
metadata:
  version: "1.0.0"
  language: "Korean output with English terms in parentheses"
---

# Parasitology case-based question writing

## Audience and level

- Default to third-year medical students unless the user specifies another audience.
- Prioritize application and judgment over simple recall. Unless the user asks otherwise, write no more than one in four items at the recall (암기형) level.
- Number of items:
  - Mode A (parasite name): write the number the user specifies. If none is stated, write three and say so.
  - Mode B (article): write three items by default, each testing a different physician task chosen from those the article covers best. Write a different number only if the user asks for one.
- Write all output in Korean: item files, notes files, and the response to the user, including headings, labels, and the summary table. Use another language only if the user explicitly asks for it.
- When a technical term appears in Korean text, give the English term in parentheses at its first mention in each item, for example 간흡충(*Clonorchis sinensis*), 프라지콴텔(praziquantel), 호산구증가증(eosinophilia), 충란(egg), 피낭유충(metacercaria). Repeat only the Korean term after the first mention. Do not add English to everyday words.
- Italicize scientific names and spell out the genus at first mention in each item (for example, 간흡충(*Clonorchis sinensis*), then *C. sinensis* or 간흡충).
- In answer options, write the Korean term with the English term in parentheses in every option, so that options stay parallel in form.

## Physician tasks

Every item tests exactly one of the four physician tasks below. The task is decided by what the lead-in asks the examinee to do, not by the topic of the vignette.

| Physician task | Content included | Example item focus |
|---|---|---|
| Health and health maintenance (예방·건강유지) | Epidemiology, sources and routes of infection, risk factors, prevention and control, screening, health education, food safety, vector and reservoir control | "감염을 예방하기 위해 권고할 것은?", "가장 가능성이 높은 감염원은?", "이 지역 주민의 조기 발견을 위한 검사는?" |
| Mechanisms of disease (병태생리·기전) | Life cycle and infective stage, pathogenesis, host immune response, pathological and physiological changes, mechanisms of signs, symptoms, and complications | "이 소견이 나타나는 기전은?", "이 환자에서 감염을 일으킨 기생충의 발육 단계는?", "호산구 증가의 병태생리적 설명은?" |
| Diagnosis (진단) | History and physical examination, test selection and interpretation (stool, blood smear, serology, imaging, molecular tests), differential diagnosis, confirmation, prognosis and expected course | "가장 가능성이 높은 진단은?", "진단을 확인하기 위한 가장 적절한 검사는?", "이 환자에서 예상되는 경과는?" |
| Management (치료·관리) | Drug choice, dose principles, adverse effects and contraindications, nondrug treatment and procedures, acute and chronic management, management of complications, follow-up | "가장 적절한 치료 약물은?", "다음으로 시행할 처치는?", "치료 후 추적 관찰 방법은?" |

Classification rules:

- Epidemiology and route-of-infection questions belong to health and health maintenance. Prognosis and expected-course questions belong to diagnosis. Questions on a drug's mechanism of action, adverse effects, or contraindications belong to management.
- If the lead-in could fit two tasks, rewrite it so that it clearly asks for one.
- Unless the user specifies a distribution, spread an item set across the four tasks: for three items, use three different tasks; for four or more items, include each task at least once.

## Step 1. Choose the source mode

- **Mode A (parasite name):** The user names one or more parasites or a topic and, optionally, the number of items (for example, "Clonorchis sinensis, 4 items"). Base content on standard parasitology textbooks and WHO, CDC, or KDCA resources.
- **Mode B (article):** The user uploads or links one article on the topic (PDF, DOCX, Markdown, DOI, or PMID). Follow the article workflow below.
- If both a parasite name and an article are given, use Mode B and use the name to focus the items.
- If the request gives neither, ask once which mode the user wants before writing.

### Mode B workflow

1. Read the whole article. Take the bibliographic data (authors, title, journal, year, volume, pages, DOI) from the article itself, and verify them through PubMed or the DOI when a lookup tool is available. If they cannot be verified, write "출처 확인 필요(source verification required)."
2. Save a short notes file listing the article's study design, population and setting, and key findings grouped by the four physician tasks.
3. Classify each candidate teaching point:
   - **Established:** consistent with standard textbooks or WHO, CDC, or KDCA guidance.
   - **Article-specific:** a novel, single-study, or local finding (such as a new endemic area, a test-accuracy estimate, or an off-guideline regimen).
4. Key the correct answer to established points. Article-specific findings may shape the vignette (setting, exposure, test used), but if an item's keyed answer depends on them, label it "논문 의존(article-dependent)" and state this in the explanation.
5. Fictionalize every case. If the article is a case report or series, do not reproduce the patient: change age, sex, occupation, timeline, and nonessential details while keeping the clinical logic. Paraphrase in the vignette and options; do not copy sentences or tables into them. Use article figures only as described under "Figures in the stem."
6. By default, write three items on three different physician tasks. Choose the three tasks the article supports best, and state in the response which task was left out and why. If the article supports fewer than three tasks, or fewer distinct, non-overlapping items than requested, say so and write fewer items rather than padding or repeating a task.
7. For each item, record in the answer-and-evidence section the passage of the article from which the correct answer can be inferred (see Step 3, section 4), and cite the article and at least one standard reference that supports the keyed answer.

## Step 2. Plan the item set

Before writing more than one item, list for each item its physician task, learning objective, and item level (암기형, 판단형, or 문제해결형). Check the spread across physician tasks, and make sure no item's vignette or options reveal the answer to another item.

## Step 3. Write each item

Include the following sections in each item, in this order:

1. **Clinical vignette:** Write 3–5 sentences in this order: age and sex, setting, chief complaint and duration, history with epidemiological clues (residence, dietary habits, travel, occupation, animal contact), physical findings, and laboratory, imaging, or microscopy findings. Use a clinical vignette for every physician task; for health and health maintenance items, the vignette may center on a patient, family, or community exposure.
   - Give laboratory values with units, and reference ranges in parentheses when they are not widely known.
   - When the item does not ask for the diagnosis, the diagnosis may be stated or strongly implied. When it does, do not name the parasite or disease in the stem; describe findings instead (for example, "길이 약 30 µm이고 어깨가 있는 유개충란(operculated egg)" rather than "간흡충 충란").
   - The vignette must be needed to answer the question, and it must be realistic and internally consistent (incubation period, timeline, laboratory values).
   - If a figure is available (see "Figures in the stem" below), insert it in the vignette after the sentence that introduces it, and write that sentence so that the examinee must interpret the figure (for example, "대변 검사에서 그림과 같은 충란(egg)이 관찰되었다."). Do not describe in words the findings the figure is meant to show.
2. **Question (lead-in):** Ask one question that tests one physician task.
   - Write a single, positively worded, closed question ending with a question mark.
   - Apply the cover-the-options rule: a competent student should be able to answer from the vignette and lead-in alone, without seeing the options.
   - Use lead-ins like those in the physician-task table, adapted to the vignette.
3. **Answer options:** Provide exactly five options, numbered 1, 2, 3, 4, and 5 (not A–E), with one best answer. Refer to options by these numbers everywhere, including the answer, explanation, and summary.
   - Keep all options homogeneous (for example, all parasites, all drugs, all tests, all preventive measures, all developmental stages, or all mechanisms) and parallel in grammatical form and length.
   - Make every distractor plausible to a student with partial knowledge, drawing on common confusions (for example, *Clonorchis* vs *Metagonimus* vs *Paragonimus*). Each distractor must still be clearly inferior to the keyed answer in a way content experts would agree on.
   - Keep options short and put the clinical information in the stem.
   - Make options mutually exclusive, and list them in a logical order (alphabetical for names, ascending for numbers).
   - Across an item set, vary the position of the correct answer so that options 1–5 are used roughly evenly.
4. **Answer and evidence:** Place this section immediately after the options.
   - **Answer:** State the correct option number.
   - **Explanation:** Explain in 2–3 sentences why it is correct, naming the key discriminating clue in the vignette. Select two principal distractors and explain why each is incorrect in one sentence per distractor.
   - **Evidence:** Give the basis for the keyed answer.
     - Mode B, or whenever the user supplied an article or other material (lecture notes, guideline, textbook excerpt): quote verbatim the passage from which the correct answer can be inferred, in quotation marks, with its location (section, page, table, or paragraph). Quote only text that actually appears in the supplied material; keep it to the shortest passage that supports the answer (usually 1–2 sentences).
     - Mode A without supplied material: cite the textbook or WHO, CDC, or KDCA resource that supports the answer. Do not present remembered wording as a verbatim quotation.
     - Cite only sources that can be verified; do not invent titles, editions, page numbers, or links. If a source cannot be verified, write "출처 확인 필요(source verification required)."
5. **Item classification:** Place this section after the answer and evidence. Record:
   - **Parasite or topic:** the parasite's Korean name with its scientific name in parentheses, or the topic (for example, 간흡충(*Clonorchis sinensis*) or 식품매개 흡충류(foodborne trematodes)).
   - **Item level:** 암기형 (recall: retrieving an isolated fact), 판단형 (interpretation: interpreting findings to reach a judgment such as a diagnosis or mechanism), or 문제해결형 (problem solving: integrating findings to choose an action, such as a test, treatment, or preventive measure).
   - **Learning objective, estimated difficulty** (easy, moderate, or hard), **source mode**, and **article dependence** (established, article-dependent, or not applicable).
6. **Physician task classification:** Place this section after the item classification. Record the one physician task the item tests and a one-line rationale stating what the lead-in asks the examinee to do.

## Figures in the stem

Use figures only in the vignette (stem), never as answer options or in the explanation.

**Figure uploaded by the user (any mode):**

1. Open the image and confirm what it shows (for example, an egg, a blood smear, a CT image, or a skin lesion). If it does not fit the requested topic, say so and ask before using it.
2. Use it in the item whose physician task it best supports; if the user specifies an item, use it there.
3. Save a copy as PNG at `items/images/<topic>_<number>_fig.png`, converting other formats. Keep the original resolution; do not edit the content beyond cropping.

**Figure from the article (Mode B, when the user has not uploaded a figure):**

1. Render the article's pages to images (for example, `pdftoppm -r 200 -png`) and view each figure.
2. Choose the single figure most useful for a clinical vignette: microscopy, histopathology, imaging, gross specimens, or clinical photographs. Do not use phylogenetic trees, gel images, flowcharts, or tables unless the item specifically tests their interpretation.
3. Crop the chosen figure or panel (for example, with Python Pillow) so that it contains only the image. Remove the figure caption, panel labels, arrows, and any text that names the parasite, the disease, or the answer. Keep a scale bar if present.
4. Save the crop as PNG at `items/images/<topic>_<number>_fig.png`, at least 600 pixels on the longer side, and view the saved file to confirm the crop.
5. Use the figure in the one item it fits best, and adapt the vignette so that the figure is consistent with the fictionalized case (age, site, timeline).
6. If the article has no suitable figure, say so in the response and write the items without figures rather than forcing one.

**For every figure:**

- Insert it in the vignette as `![그림 1](images/<topic>_<number>_fig.png)` with a neutral caption (for example, "그림 1. 대변 도말 표본(×400)") that does not reveal the answer.
- Check that it contains nothing that identifies a person (face, name, hospital number, date of birth); crop it out, or do not use the figure.
- Record the figure's source in the evidence section: the article's first author, year, and figure number with its license (for example, "Choi 2026, Fig. 2, CC BY-NC 4.0"), or "작성자 제공 그림" for an uploaded figure. If the article's license does not permit reuse, state that permission is needed before the item is distributed.
- Make sure the figure does not cue the answer to another item in the set.

## Step 4. Check each item before saving

Revise any item that fails a check below, then record the result in the item's quality-check section.

**Testwiseness flaws (cues that let students guess):**

- Grammatical cues: an option does not fit the lead-in grammatically (in Korean, check particles and endings).
- Logical cues: a subset of options is collectively exhaustive, or two options are opposites so that one must be correct.
- Absolute terms such as "always," "never," or "only" in distractors.
- The correct option is the longest, the most detailed, or the only qualified one.
- Clang clues: a word or phrase from the stem appears only in the correct option.
- Convergence: the correct option shares the most elements with the other options.

**Irrelevant-difficulty flaws (difficulty unrelated to the content):**

- Long or complex options, or options containing more than one idea.
- Numeric options that overlap or use inconsistent formats or units.
- Vague frequency terms such as "often," "usually," or "rarely."
- "None of the above," "All of the above," or combination options ("1 and 3").
- Negative or tricky stems, or unnecessary information that only adds reading time.
- Heterogeneous options that mix categories.

**Content checks:**

- The item tests an important, clinically relevant concept rather than trivia (such as an isolated egg measurement or a discoverer's name).
- The item tests exactly one physician task, and its classification matches what the lead-in asks.
- Exactly one option is defensibly best; facts, drugs, and doses match current WHO, CDC, or KDCA guidance. Where recommendations differ by country, follow the cited guidance and say so.
- Demographic details serve an epidemiological purpose only; do not use ethnicity, nationality, or occupation as stereotyped cues.
- No item cues the answer to another item in the set.
- If the item has a figure: the figure is needed to answer, contains no text or marks revealing the answer, identifies no person, matches the vignette, and has its source recorded.

## Prohibited content and formats

- Use fictional cases only; do not use information from real patients, including patients described in uploaded case reports.
- Do not use "All of the above," "None of the above," or combination options.
- Do not use negative question stems such as "Which of the following is NOT correct?"
- Do not use multiple true–false (K-type) formats.

## Output

- Save each item as a separate Markdown file at `items/<topic>_<number>.md` within the user's requested output directory or the current task workspace. Use a descriptive English topic (for example, `clonorchis_01.md`) and a unique sequential number for each filename, so that filenames work on any system.
- In Mode B, also save the article notes at `items/<topic>_article-notes.md`.
- Save figures as PNG in `items/images/`, named after their item (for example, `items/images/clonorchis_01_fig.png`), and reference them by relative path from the item file.
- Use this template for each item file (headings and labels in Korean):

```markdown
# <주제> <번호>

## 증례

<3–5문장; 그림이 있으면 해당 문장 뒤에 삽입>

![그림 1](images/<topic>_<number>_fig.png)

그림 1. <답을 드러내지 않는 중립적 설명>

## 질문

<물음표로 끝나는 문두>

## 답가지

1. ...
2. ...
3. ...
4. ...
5. ...

## 정답과 근거

**정답:** <답가지 번호>

**해설:** <정답을 가르는 증례 단서를 밝힌 2–3문장>

- **<번호>번:** <오답인 이유, 1문장>
- **<번호>번:** <오답인 이유, 1문장>

**근거:**

- 제시 자료: "<정답을 유추할 수 있는 원문 구절>" (<제1저자> <연도>, <절/쪽/표>)
- 참고문헌: <확인 가능한 교과서 또는 WHO, CDC, KDCA 자료, 또는 "출처 확인 필요(source verification required).">
- 그림 출처: <제1저자 연도, Fig. 번호, 이용 허락(license) | 작성자 제공 그림 | 해당 없음>

## 문항분류

- 기생충명 또는 주제: <국문명(학명) 또는 주제>
- 문항 수준: 암기형 | 판단형 | 문제해결형
- 학습목표: <1문장>
- 예상 난이도: 쉬움 | 보통 | 어려움
- 출제 방식: 기생충명 | 논문(<제1저자> <연도>)
- 논문 의존도: 정설(established) | 논문 의존(article-dependent) | 해당 없음

## Physician task 분류

- Physician task: 예방·건강유지(health and health maintenance) | 병태생리·기전(mechanisms of disease) | 진단(diagnosis) | 치료·관리(management)
- 분류 근거: <문두가 수험자에게 무엇을 하게 하는지 1줄>

## 품질 점검

- 답가지를 가리고도 답할 수 있는가(cover-the-options rule): 통과
- 추측 단서(testwiseness flaws): 없음
- 내용과 무관한 난이도(irrelevant-difficulty flaws): 없음
- 내용 점검: 통과
- 그림 점검(답 노출 표지·개인 식별 정보 없음, 출처 기재): 통과 | 해당 없음
```

- End the response with a table, in Korean, summarizing the distribution of generated items by topic and physician task. Use columns for 주제, 예방·건강유지, 병태생리·기전, 진단, 치료·관리, and 계; include a 합계 row. Below the table, give one line each for the answer-key distribution (1–5번) and the item-level distribution (암기형, 판단형, 문제해결형), and list any items flagged "논문 의존(article-dependent)" or "출처 확인 필요(source verification required)."

## Background

The item-writing rules above are adapted from the following guidance. They inform how items are written and are not cited in the items themselves.

- National Board of Medical Examiners (NBME). Constructing written test questions for the basic and clinical sciences (NBME Item-Writing Guide).
- Haladyna TM, Downing SM, Rodriguez MC. A review of multiple-choice item-writing guidelines for classroom assessment. Appl Meas Educ 2002;15:309-333.
- Downing SM. The effects of violating standard item writing principles on tests and students: the consequences of using flawed test items on achievement examinations in medical education. Adv Health Sci Educ Theory Pract 2005;10:133-143.
