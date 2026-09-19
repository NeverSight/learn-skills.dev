---
name: stelow-product-ads
description: Advertising strategies for online placement based on the Transtheoretical Model of Change. Covers the 5 stages of audience awareness and ad categories for each stage.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Communication: Ads for Online Placement

The solution's audience can be in 5 stages according to the **Transtheoretical Model of Change**:

## 5 Stages

**1. Pre-contemplation (Ignorance)**: people who are not yet aware of the problem or that their life can be better.
- *Focus*: raise awareness about the problem and its impacts, showing how life can be better if the problem is solved
- *Communication*: highlight the benefits of a life without the problem, without directly mentioning the solution. Use stories, examples, and testimonials to generate identification and awaken interest.
- *Calls to action*: engage with your brand (like, comment, download free material, follow on social media, subscribe to receive news) to nurture the relationship and increase awareness about the problem

**2. Contemplation (Awareness)**: people who are aware of the problem and its urgencies, but haven't yet decided to seek a solution or don't know that one is available.
- *Focus*: present your solution as an answer to the audience's urgencies, showing how it can solve the problem and improve people's lives
- *Communication*: explain the benefits of your solution clearly and concisely, using testimonials, case studies, and demonstrations to prove its effectiveness
- *Calls to action*: invite the audience to learn more about the solution, offering access to informative content, webinars, free demonstrations, or initial consultations

**3. Preparation**: people who have already decided to seek a solution and are preparing to act.
- *Focus*: help the audience prepare for change, providing detailed information, clarifying doubts, and assisting in planning next steps
- *Communication*: offer educational content, step-by-step guides, planning tools, benefit calculators, and testimonials from customers who have successfully gone through the preparation phase
- *Calls to action*: encourage the next step — schedule a consultation, request a quote, or enroll in a coaching program

**4. Action**: people who are implementing the change and using your solution.
- *Focus*: offer support and encouragement so the audience stays motivated and overcomes change challenges
- *Communication*: maintain regular contact with customers, offering tips, reminders, additional resources, and personalized follow-up. Create an environment of support and celebration of achievements.
- *Calls to action*: encourage continuing to use the solution, share progress, and provide feedback on the experience

**5. Maintenance**: people who have already adopted the solution and seek to maintain results and continue evolving.
- *Focus*: retain customers, offering continuous support, relevant content, and improvement opportunities
- *Communication*: maintain regular contact through email marketing, newsletters, social media, and exclusive events. Offer loyalty programs, solution updates, and educational content to keep them engaged.
- *Calls to action*: encourage sharing experiences, providing feedback, participating in online communities, and referring your solution to other people

---

## Ad Categories by Stage

### Pre-Contemplation Phase
- **Curiosity and Intrigue**: awaken curiosity with instigating questions, impactful phrases, and surprising information
- **Impactful Images**: visually striking images that represent the problem or the negative impact
- **Myths and Truths**: debunk mistaken beliefs about the problem
- **Provocations and Questions**: challenge the audience with questions that lead them to reflect on their behaviors
- **Future Scenarios**: present a positive future scenario vs. negative (if it persists)
- **Comic Exaggeration**: use humor and exaggeration to make the problem lighter and more memorable

### Contemplation Phase
- **Comparison and Solution**: show how your solution stands out from alternatives
- **Detailed Explanations**: provide clear information about the problem and how your solution solves it
- **Practical Demonstrations**: show the solution in action through videos, tutorials, success cases
- **Creative Analogies**: use unexpected analogies and metaphors to explain the problem and solution
- **Unexpected Benefits**: highlight the surprising and unexpected benefits your solution offers
- **Dilemmas**: present common dilemmas the audience faces, showing that you understand their difficulties

### Preparation Phase
- **Guides and Tutorials (How-To)**: offer practical content with step-by-step instructions
- **Expert Interviews**: present interviews with experts who address the problem, the solution, and the benefits
- **Tools and Resources**: offer free tools, resources, and materials (spreadsheets, checklists, templates, ebooks)
- **Interactive Quizzes and Tests**: create quizzes that help the audience evaluate their situation

### Action Phase
- **Irresistible Offers**: create special offers with mental triggers of urgency and scarcity
- **Stories and Testimonials**: show success stories of people who used the solution
- **Mental Triggers**: reciprocity, social proof, authority, scarcity, urgency, and novelty
- **Clear and Objective Calls to Action**: use clear, objective, and persuasive CTAs

### Maintenance Phase
- **Exclusive Content**: offer exclusive content for customers (webinars, ebooks, VIP groups, online courses)
- **Support and Community**: create efficient communication channels and encourage interaction
- **Loyalty Programs**: implement programs with exclusive benefits for recurring customers
- **Challenges and Contests**: promote challenges that motivate customers to continue using the solution
- **Inspiring Customer Stories**: share stories of customers who overcame challenges and achieved significant results
- **User-Generated Content**: encourage customers to create and share content related to the solution

## Completeness contract

The host validates these minima — never submit fewer:

- Channel plan covering all 5 awareness stages (Pre-Contemplation, Contemplation, Preparation, Action, Maintenance).
- Kill criteria per channel.
- At least 500 words and 5 headings.

## Examples

### Example: launch ads for a new B2B scheduling tool

**Input:** "We launch next month. Where should we advertise?"

**Steps:**
1. Classify audience awareness (likely stage 1-2: unaware of the problem).
2. Pick stage-matched categories (problem-agitation + category-creation, not feature-comparison).
3. Propose 2-3 channels per category with a test budget split.

**Output:** Channel plan mapped to awareness stages, with kill criteria per channel.

## Edge Cases

### Audience spans multiple stages
- Segment creative by stage; never run stage-1 and stage-4 copy in the same ad set.
### No budget for testing
- Say so explicitly; recommend one organic channel instead of thin-paid spread.
### Regulated domain (finance, health)
- Flag claim restrictions before proposing any copy.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : promotions  (no transitions defined in stages.yaml)
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : <next stage from stages.yaml>
gate           : <none|approval-required>
rework-on      : <previous stage if rework path>
```

Workflow mode: emit the above Hand-off block verbatim, then stop.

### Workflow slice

Standalone (non-workflow) steps are not part of the workflow slice. In
workflow mode this skill emits the Hand-off block and exits.

