---
name: Letter Writer
slug: letter-writer
description: Generate formal and informal letters including business correspondence, cover letters, and personal communications
category: document-creation
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "write letter"
  - "create cover letter"
  - "draft business letter"
  - "compose correspondence"
  - "generate letter"
tags:
  - letters
  - correspondence
  - cover-letter
  - business-writing
  - communication
---

# Letter Writer

The Letter Writer skill automates the creation of professional and personal letters with proper formatting, tone, and structure. It handles various letter types including business correspondence, cover letters, recommendation letters, thank you notes, and formal communications. The skill ensures appropriate formatting, professional language, and customization for different audiences and purposes.

Generate letters in multiple formats (PDF, DOCX, HTML) with customizable templates for different occasions and communication needs.

## Core Workflows

### Workflow 1: Generate Cover Letter
**Purpose:** Create a compelling cover letter tailored to a specific job application

**Steps:**
1. Collect job details (position, company, requirements)
2. Extract candidate's relevant qualifications
3. Structure letter with proper business format
4. Write engaging opening paragraph
5. Detail relevant experience and achievements
6. Connect skills to job requirements
7. Craft strong closing with call to action
8. Format with proper spacing and margins
9. Export to PDF and DOCX

**Implementation:**
```javascript
const { Document, Packer, Paragraph, AlignmentType, TextRun } = require('docx');
const fs = require('fs');

async function generateCoverLetter(letterData, outputPath) {
  const doc = new Document({
    sections: [{
      properties: {
        page: {
          margin: {
            top: 1440,    // 1 inch
            right: 1440,
            bottom: 1440,
            left: 1440
          }
        }
      },
      children: [
        // Your contact information
        new Paragraph({
          text: letterData.sender.name,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.sender.address,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: `${letterData.sender.city}, ${letterData.sender.state} ${letterData.sender.zip}`,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.sender.email,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.sender.phone,
          spacing: { after: 200 }
        }),

        // Date
        new Paragraph({
          text: new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          }),
          spacing: { after: 200 }
        }),

        // Recipient information
        new Paragraph({
          text: letterData.recipient.name || 'Hiring Manager',
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.recipient.company,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.recipient.address,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: `${letterData.recipient.city}, ${letterData.recipient.state} ${letterData.recipient.zip}`,
          spacing: { after: 200 }
        }),

        // Salutation
        new Paragraph({
          text: `Dear ${letterData.recipient.name || 'Hiring Manager'}:`,
          spacing: { after: 200 }
        }),

        // Opening paragraph
        new Paragraph({
          text: `I am writing to express my strong interest in the ${letterData.position} position at ${letterData.recipient.company}. ${letterData.opening}`,
          alignment: AlignmentType.JUSTIFIED,
          spacing: { after: 200 }
        }),

        // Body paragraphs
        ...letterData.bodyParagraphs.map(para =>
          new Paragraph({
            text: para,
            alignment: AlignmentType.JUSTIFIED,
            spacing: { after: 200 }
          })
        ),

        // Closing paragraph
        new Paragraph({
          text: letterData.closing || `Thank you for considering my application. I am excited about the opportunity to contribute to ${letterData.recipient.company} and would welcome the chance to discuss how my skills and experience align with your needs. I look forward to hearing from you.`,
          alignment: AlignmentType.JUSTIFIED,
          spacing: { after: 200 }
        }),

        // Signature
        new Paragraph({
          text: 'Sincerely,',
          spacing: { after: 400 }
        }),
        new Paragraph({
          text: letterData.sender.name
        })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  return outputPath;
}

// Helper function to generate body paragraphs based on job requirements
function generateCoverLetterBody(candidateData, jobData) {
  const paragraphs = [];

  // Experience paragraph
  const relevantExperience = candidateData.experience
    .filter(exp => exp.relevanceScore > 0.7)
    .slice(0, 2);

  if (relevantExperience.length > 0) {
    const expText = `With ${calculateYearsExperience(candidateData.experience)} years of experience in ${jobData.industry}, I have developed strong expertise in ${jobData.keySkills.slice(0, 3).join(', ')}. In my current role at ${relevantExperience[0].company}, ${relevantExperience[0].achievements[0].toLowerCase()}`;
    paragraphs.push(expText);
  }

  // Skills and qualifications paragraph
  const matchingSkills = candidateData.skills
    .filter(skill => jobData.requiredSkills.includes(skill.name))
    .slice(0, 4);

  if (matchingSkills.length > 0) {
    const skillsText = `I am particularly well-suited for this role given my proficiency in ${matchingSkills.map(s => s.name).join(', ')}. ${candidateData.achievements.find(a => a.includes(matchingSkills[0].name)) || 'I have successfully applied these skills to deliver measurable results.'}`;
    paragraphs.push(skillsText);
  }

  // Company-specific paragraph
  if (jobData.companyInfo) {
    const companyText = `I am particularly drawn to ${jobData.company} because of ${jobData.companyInfo.appeal || 'your reputation for innovation and excellence'}. I believe my background in ${jobData.relevantBackground} would enable me to make immediate contributions to your team.`;
    paragraphs.push(companyText);
  }

  return paragraphs;
}
```

### Workflow 2: Business Letter Generator
**Purpose:** Create formal business correspondence with proper formatting

**Steps:**
1. Select letter type (inquiry, complaint, proposal, etc.)
2. Format with business letter structure
3. Use professional tone and language
4. Include subject line if needed
5. Write clear, concise content
6. Add proper closing and signature block
7. Format for letterhead if available

**Implementation:**
```javascript
async function generateBusinessLetter(letterData, outputPath) {
  const letterTypes = {
    inquiry: {
      subject: 'Inquiry Regarding',
      opening: 'I am writing to inquire about',
      tone: 'polite and professional'
    },
    complaint: {
      subject: 'Concern Regarding',
      opening: 'I am writing to bring to your attention',
      tone: 'firm but professional'
    },
    proposal: {
      subject: 'Proposal for',
      opening: 'I am pleased to present',
      tone: 'professional and enthusiastic'
    },
    thankyou: {
      subject: 'Thank You',
      opening: 'I wanted to express my sincere gratitude for',
      tone: 'warm and appreciative'
    }
  };

  const template = letterTypes[letterData.type] || letterTypes.inquiry;

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        // Company letterhead (if provided)
        ...(letterData.letterhead ? [
          new Paragraph({
            text: letterData.letterhead.companyName,
            alignment: AlignmentType.CENTER,
            spacing: { after: 0 }
          }),
          new Paragraph({
            text: letterData.letterhead.address,
            alignment: AlignmentType.CENTER,
            spacing: { after: 0 }
          }),
          new Paragraph({
            text: `${letterData.letterhead.phone} | ${letterData.letterhead.email}`,
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 }
          })
        ] : []),

        // Date
        new Paragraph({
          text: new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          }),
          spacing: { after: 200 }
        }),

        // Recipient
        new Paragraph({
          text: letterData.recipient.name,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.recipient.title,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.recipient.company,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.recipient.address,
          spacing: { after: 200 }
        }),

        // Subject line
        ...(letterData.subject ? [
          new Paragraph({
            children: [
              new TextRun({ text: 'RE: ', bold: true }),
              new TextRun(letterData.subject)
            ],
            spacing: { after: 200 }
          })
        ] : []),

        // Salutation
        new Paragraph({
          text: `Dear ${letterData.recipient.name}:`,
          spacing: { after: 200 }
        }),

        // Body
        ...letterData.paragraphs.map(para =>
          new Paragraph({
            text: para,
            alignment: AlignmentType.JUSTIFIED,
            spacing: { after: 200 }
          })
        ),

        // Closing
        new Paragraph({
          text: letterData.closing || 'Sincerely,',
          spacing: { after: 400 }
        }),

        // Signature
        new Paragraph({
          text: letterData.sender.name,
          spacing: { after: 0 }
        }),
        new Paragraph({
          text: letterData.sender.title
        })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  return outputPath;
}
```

### Workflow 3: Recommendation Letter Generator
**Purpose:** Create letters of recommendation for employees, students, or colleagues

**Steps:**
1. Collect information about the person being recommended
2. Understand the purpose and recipient of the letter
3. Establish credibility and relationship
4. Detail specific qualifications and achievements
5. Provide concrete examples
6. Compare to peers if appropriate
7. Give enthusiastic endorsement
8. Offer to provide additional information

**Implementation:**
```javascript
function generateRecommendationLetter(recommendationData) {
  const letterData = {
    sender: recommendationData.recommender,
    recipient: recommendationData.recipient || {
      name: 'To Whom It May Concern'
    },
    type: 'recommendation',

    paragraphs: [
      // Opening - establish relationship
      `I am writing to enthusiastically recommend ${recommendationData.candidate.name} for ${recommendationData.purpose}. I have had the pleasure of working with ${recommendationData.candidate.firstName} for ${recommendationData.duration} in my capacity as ${recommendationData.recommender.title} at ${recommendationData.recommender.company}.`,

      // Qualifications and strengths
      `During our time working together, ${recommendationData.candidate.firstName} has consistently demonstrated exceptional ${recommendationData.strengths.join(', ')}. ${recommendationData.standoutQualities}`,

      // Specific examples
      ...recommendationData.examples.map(example =>
        `For instance, ${example.description} This ${example.impact}`
      ),

      // Comparison to peers (if applicable)
      ...(recommendationData.comparison ? [
        `${recommendationData.candidate.firstName} stands out among ${recommendationData.comparison.peerGroup} for ${recommendationData.comparison.distinguishingFactors}.`
      ] : []),

      // Strong endorsement
      `I am confident that ${recommendationData.candidate.firstName} will be an outstanding ${recommendationData.targetRole} and will bring the same level of dedication, skill, and enthusiasm that I have witnessed firsthand. ${recommendationData.candidate.pronoun} has my highest recommendation without reservation.`,

      // Offer additional information
      `Please feel free to contact me at ${recommendationData.recommender.phone} or ${recommendationData.recommender.email} if you would like to discuss ${recommendationData.candidate.firstName}'s qualifications further.`
    ]
  };

  return generateBusinessLetter(letterData, recommendationData.outputPath);
}
```

### Workflow 4: Thank You Note Generator
**Purpose:** Create professional thank you letters for various occasions

**Steps:**
1. Identify occasion (interview, gift, meeting, etc.)
2. Express gratitude specifically
3. Mention key details from the interaction
4. Reinforce interest or relationship
5. Keep concise but sincere
6. Use warm but professional tone
7. Format appropriately for medium

**Implementation:**
```javascript
function generateThankYouLetter(thankYouData) {
  const templates = {
    interview: {
      opening: `Thank you for taking the time to meet with me ${thankYouData.when} to discuss the ${thankYouData.position} position at ${thankYouData.company}.`,
      body: `I enjoyed learning more about ${thankYouData.discussionTopics} and was particularly excited to hear about ${thankYouData.highlight}. Our conversation reinforced my strong interest in joining your team and contributing to ${thankYouData.contribution}.`,
      closing: `I am very enthusiastic about this opportunity and believe my ${thankYouData.relevantSkills} would be a strong fit for your needs. Thank you again for your time and consideration. I look forward to hearing from you.`
    },

    meeting: {
      opening: `Thank you for meeting with me on ${thankYouData.date} to discuss ${thankYouData.topic}.`,
      body: `I found our conversation about ${thankYouData.keyPoints} very valuable. Your insights regarding ${thankYouData.insight} gave me a new perspective on ${thankYouData.subject}.`,
      closing: `I appreciate your time and expertise. I look forward to our continued collaboration.`
    },

    gift: {
      opening: `Thank you so much for the thoughtful ${thankYouData.gift}.`,
      body: `Your generosity and thoughtfulness are greatly appreciated. ${thankYouData.personalNote}`,
      closing: `Thank you again for thinking of me. Your kindness means a lot.`
    },

    networking: {
      opening: `It was a pleasure meeting you at ${thankYouData.event} on ${thankYouData.date}.`,
      body: `I enjoyed our conversation about ${thankYouData.topic} and found your perspective on ${thankYouData.insight} particularly interesting. I would love to stay connected and explore opportunities for ${thankYouData.futureCollaboration}.`,
      closing: `Thank you for taking the time to speak with me. I've connected with you on LinkedIn and look forward to staying in touch.`
    }
  };

  const template = templates[thankYouData.type] || templates.meeting;

  return {
    sender: thankYouData.sender,
    recipient: thankYouData.recipient,
    subject: `Thank you - ${thankYouData.regarding}`,
    paragraphs: [
      template.opening,
      template.body,
      template.closing
    ],
    closing: 'Best regards,'
  };
}
```

### Workflow 5: Batch Letter Generation
**Purpose:** Create multiple personalized letters from a template and data source

**Steps:**
1. Load letter template with placeholders
2. Load recipient data (CSV, JSON, database)
3. For each recipient:
   - Merge data with template
   - Personalize content
   - Generate letter
   - Save with unique filename
4. Track generation progress
5. Create summary report

**Implementation:**
```javascript
const Handlebars = require('handlebars');

async function batchGenerateLetters(templatePath, recipientsData, outputDir) {
  const template = fs.readFileSync(templatePath, 'utf8');
  const compiledTemplate = Handlebars.compile(template);

  const results = [];

  for (const recipient of recipientsData) {
    try {
      // Merge recipient data with template
      const letterContent = compiledTemplate(recipient);

      // Generate filename
      const filename = `${outputDir}/letter-${recipient.id}-${recipient.name.replace(/\s+/g, '-')}.docx`;

      // Create letter data
      const letterData = {
        sender: recipient.sender || recipientsData.defaultSender,
        recipient: {
          name: recipient.name,
          title: recipient.title,
          company: recipient.company,
          address: recipient.address
        },
        paragraphs: letterContent.split('\n\n').filter(p => p.trim()),
        subject: recipient.subject
      };

      // Generate letter
      await generateBusinessLetter(letterData, filename);

      results.push({
        success: true,
        recipientId: recipient.id,
        name: recipient.name,
        filename: filename
      });

    } catch (error) {
      results.push({
        success: false,
        recipientId: recipient.id,
        name: recipient.name,
        error: error.message
      });
    }
  }

  // Generate summary report
  const summary = {
    total: recipientsData.length,
    successful: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results: results
  };

  fs.writeFileSync(
    `${outputDir}/batch-summary.json`,
    JSON.stringify(summary, null, 2)
  );

  return summary;
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Cover letter | "write cover letter for [position]" |
| Business letter | "create business letter to [recipient]" |
| Recommendation | "generate recommendation letter" |
| Thank you note | "write thank you letter" |
| Formal letter | "draft formal correspondence" |
| Batch letters | "create letters for [recipients]" |

## Best Practices

- **Proper Format:** Use standard business letter format with correct spacing
- **Professional Tone:** Match tone to purpose and audience
- **Concise Writing:** Be clear and direct; avoid unnecessary words
- **Proofreading:** Zero typos or grammatical errors
- **Personalization:** Customize each letter; avoid generic content
- **Specific Details:** Include concrete examples and specific information
- **Active Voice:** Use active voice for stronger, clearer writing
- **Appropriate Length:** Cover letters: 3-4 paragraphs; business letters: as needed but concise
- **Call to Action:** End with clear next steps or desired outcome
- **Signature:** Include proper signature block with contact information
- **Formatting:** Consistent fonts, margins, and spacing
- **Timeliness:** Send thank you notes within 24-48 hours

## Common Patterns

**Job Application Package:**
```javascript
{
  coverLetter: generateCoverLetter(candidateData, jobData),
  resume: generateResume(candidateData),
  references: generateReferencesList(candidateData.references)
}
```

**Customer Service Response:**
```javascript
{
  type: 'response',
  tone: 'apologetic and solution-oriented',
  structure: ['acknowledge issue', 'explain what happened', 'describe resolution', 'offer compensation', 'prevent future']
}
```

## Dependencies

Install required packages:
```bash
npm install docx
npm install handlebars     # For templating
npm install pdf-lib        # For PDF generation
npm install nodemailer     # For email sending (optional)
```

## Error Handling

- **Missing Data:** Provide default values for optional fields
- **Invalid Addresses:** Validate address formatting
- **Template Errors:** Catch rendering errors gracefully
- **File Permissions:** Handle write errors

## Advanced Features

**Email Integration:**
```javascript
async function sendLetter(letterPath, recipientEmail, subject) {
  const transporter = nodemailer.createTransporter(config);

  await transporter.sendMail({
    from: senderEmail,
    to: recipientEmail,
    subject: subject,
    html: '<p>Please find attached letter.</p>',
    attachments: [{ path: letterPath }]
  });
}
```

**Signature Integration:**
```javascript
async function addDigitalSignature(letterPath, signatureImagePath) {
  // Add scanned signature image to letter
  // Position at signature block
}
```

**Template Library:**
```javascript
const letterTemplates = {
  coverLetter: './templates/cover-letter.hbs',
  businessInquiry: './templates/business-inquiry.hbs',
  recommendation: './templates/recommendation.hbs',
  thankYou: './templates/thank-you.hbs'
};
```