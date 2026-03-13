---
name: Invoice Generator
slug: invoice-generator
description: Create professional invoices with line items, calculations, payment terms, and branding
category: document-creation
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create invoice"
  - "generate invoice"
  - "make invoice"
  - "invoice for"
  - "bill client"
tags:
  - invoice
  - billing
  - finance
  - payment
  - accounting
---

# Invoice Generator

The Invoice Generator skill automates the creation of professional, branded invoices in multiple formats (PDF, HTML, DOCX). It handles all standard invoice components including line items, tax calculations, discounts, payment terms, and company branding. Perfect for freelancers, agencies, and businesses that need to generate invoices programmatically.

Create invoices from templates, automate recurring billing, generate batch invoices for multiple clients, and maintain consistent branding across all billing documents.

## Core Workflows

### Workflow 1: Generate Standard Invoice (PDF)
**Purpose:** Create a professional PDF invoice with all standard elements

**Steps:**
1. Collect invoice data (client info, line items, amounts)
2. Calculate subtotal, tax, discounts, and total
3. Load invoice template or create layout
4. Add company branding (logo, colors, contact info)
5. Populate invoice details (number, date, due date)
6. Add line items table with descriptions and amounts
7. Display payment terms and methods
8. Generate PDF with proper formatting

**Implementation:**
```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

function generateInvoice(invoiceData, outputPath) {
  const doc = new PDFDocument({ margin: 50 });
  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  // Company header
  doc.fontSize(20)
     .text(invoiceData.company.name, 50, 50)
     .fontSize(10)
     .text(invoiceData.company.address, 50, 80)
     .text(invoiceData.company.email, 50, 95)
     .text(invoiceData.company.phone, 50, 110);

  // Company logo (if exists)
  if (invoiceData.company.logo) {
    doc.image(invoiceData.company.logo, 450, 50, { width: 100 });
  }

  // Invoice title and number
  doc.fontSize(24)
     .text('INVOICE', 400, 150, { align: 'right' })
     .fontSize(12)
     .text(`Invoice #: ${invoiceData.invoiceNumber}`, 400, 180, { align: 'right' })
     .text(`Date: ${invoiceData.date}`, 400, 195, { align: 'right' })
     .text(`Due: ${invoiceData.dueDate}`, 400, 210, { align: 'right' });

  // Bill to section
  doc.fontSize(12)
     .text('BILL TO:', 50, 150)
     .fontSize(10)
     .text(invoiceData.client.name, 50, 170)
     .text(invoiceData.client.address, 50, 185)
     .text(invoiceData.client.email, 50, 200);

  // Line items table
  const tableTop = 250;
  doc.fontSize(10);

  // Table header
  doc.fillColor('#2C3E50')
     .rect(50, tableTop, 500, 25)
     .fill()
     .fillColor('#FFFFFF')
     .text('Description', 60, tableTop + 8)
     .text('Quantity', 320, tableTop + 8)
     .text('Rate', 390, tableTop + 8)
     .text('Amount', 470, tableTop + 8);

  // Table rows
  let currentY = tableTop + 30;
  doc.fillColor('#000000');

  invoiceData.lineItems.forEach((item, index) => {
    const y = currentY + (index * 25);
    const bgColor = index % 2 === 0 ? '#FFFFFF' : '#F8F9FA';

    doc.fillColor(bgColor)
       .rect(50, y, 500, 25)
       .fill()
       .fillColor('#000000')
       .text(item.description, 60, y + 8, { width: 240 })
       .text(item.quantity, 320, y + 8)
       .text(`$${item.rate.toFixed(2)}`, 390, y + 8)
       .text(`$${(item.quantity * item.rate).toFixed(2)}`, 470, y + 8);
  });

  // Totals section
  const totalsY = currentY + (invoiceData.lineItems.length * 25) + 30;

  doc.text('Subtotal:', 380, totalsY)
     .text(`$${invoiceData.subtotal.toFixed(2)}`, 470, totalsY);

  if (invoiceData.tax) {
    doc.text(`Tax (${invoiceData.taxRate}%):`, 380, totalsY + 20)
       .text(`$${invoiceData.tax.toFixed(2)}`, 470, totalsY + 20);
  }

  if (invoiceData.discount) {
    doc.text('Discount:', 380, totalsY + 40)
       .text(`-$${invoiceData.discount.toFixed(2)}`, 470, totalsY + 40);
  }

  // Total
  doc.fontSize(14)
     .fillColor('#2C3E50')
     .rect(380, totalsY + 60, 170, 30)
     .fill()
     .fillColor('#FFFFFF')
     .text('TOTAL:', 390, totalsY + 68)
     .text(`$${invoiceData.total.toFixed(2)}`, 470, totalsY + 68);

  // Payment terms
  doc.fillColor('#000000')
     .fontSize(10)
     .text('Payment Terms:', 50, totalsY + 120)
     .fontSize(9)
     .text(invoiceData.paymentTerms, 50, totalsY + 135, { width: 500 });

  // Footer
  doc.fontSize(8)
     .fillColor('#7F8C8D')
     .text('Thank you for your business!', 50, doc.page.height - 80, {
       align: 'center',
       width: 500
     });

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on('finish', () => resolve(outputPath));
    stream.on('error', reject);
  });
}
```

### Workflow 2: Calculate Invoice Totals
**Purpose:** Automatically calculate subtotals, taxes, discounts, and final total

**Steps:**
1. Sum all line item amounts for subtotal
2. Apply discount (percentage or fixed amount)
3. Calculate tax on discounted subtotal
4. Compute final total
5. Handle rounding to 2 decimal places
6. Validate calculations

**Implementation:**
```javascript
function calculateInvoiceTotals(lineItems, options = {}) {
  // Calculate subtotal
  const subtotal = lineItems.reduce((sum, item) => {
    return sum + (item.quantity * item.rate);
  }, 0);

  // Apply discount
  let discount = 0;
  if (options.discountPercent) {
    discount = subtotal * (options.discountPercent / 100);
  } else if (options.discountAmount) {
    discount = options.discountAmount;
  }

  const afterDiscount = subtotal - discount;

  // Calculate tax
  let tax = 0;
  if (options.taxRate) {
    tax = afterDiscount * (options.taxRate / 100);
  }

  // Calculate total
  const total = afterDiscount + tax;

  return {
    subtotal: parseFloat(subtotal.toFixed(2)),
    discount: parseFloat(discount.toFixed(2)),
    discountedSubtotal: parseFloat(afterDiscount.toFixed(2)),
    tax: parseFloat(tax.toFixed(2)),
    taxRate: options.taxRate || 0,
    total: parseFloat(total.toFixed(2)),
    lineItemCount: lineItems.length
  };
}
```

### Workflow 3: Generate from Template
**Purpose:** Use a branded invoice template for consistency

**Steps:**
1. Load HTML/Word template with placeholders
2. Define data mapping for template variables
3. Replace placeholders with actual data
4. Process line items loop
5. Calculate and insert totals
6. Convert to PDF or save as Word document
7. Apply company branding automatically

**Implementation:**
```javascript
const Handlebars = require('handlebars');
const puppeteer = require('puppeteer');
const fs = require('fs');

async function generateFromTemplate(templatePath, invoiceData, outputPath) {
  // Load template
  const templateHtml = fs.readFileSync(templatePath, 'utf8');
  const template = Handlebars.compile(templateHtml);

  // Register helpers
  Handlebars.registerHelper('currency', function(value) {
    return `$${parseFloat(value).toFixed(2)}`;
  });

  Handlebars.registerHelper('multiply', function(a, b) {
    return (a * b).toFixed(2);
  });

  // Prepare data
  const data = {
    ...invoiceData,
    currentYear: new Date().getFullYear(),
    formattedDate: new Date(invoiceData.date).toLocaleDateString(),
    formattedDueDate: new Date(invoiceData.dueDate).toLocaleDateString()
  };

  // Render template
  const html = template(data);

  // Convert to PDF
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html);
  await page.pdf({
    path: outputPath,
    format: 'A4',
    margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    printBackground: true
  });
  await browser.close();

  return outputPath;
}

// Template example (invoice-template.html):
/*
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .header { background: #2C3E50; color: white; padding: 20px; }
    .line-items { width: 100%; border-collapse: collapse; }
    .line-items th { background: #34495E; color: white; padding: 10px; }
    .line-items td { border-bottom: 1px solid #ddd; padding: 8px; }
    .totals { text-align: right; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{company.name}}</h1>
    <p>{{company.address}}</p>
  </div>
  <h2>Invoice #{{invoiceNumber}}</h2>
  <p>Date: {{formattedDate}} | Due: {{formattedDueDate}}</p>
  <h3>Bill To:</h3>
  <p>{{client.name}}<br>{{client.address}}</p>
  <table class="line-items">
    <thead>
      <tr>
        <th>Description</th>
        <th>Qty</th>
        <th>Rate</th>
        <th>Amount</th>
      </tr>
    </thead>
    <tbody>
      {{#each lineItems}}
      <tr>
        <td>{{description}}</td>
        <td>{{quantity}}</td>
        <td>{{currency rate}}</td>
        <td>{{currency (multiply quantity rate)}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
  <div class="totals">
    <p>Subtotal: {{currency subtotal}}</p>
    {{#if tax}}
    <p>Tax ({{taxRate}}%): {{currency tax}}</p>
    {{/if}}
    <h3>Total: {{currency total}}</h3>
  </div>
  <p>{{paymentTerms}}</p>
</body>
</html>
*/
```

### Workflow 4: Batch Invoice Generation
**Purpose:** Generate multiple invoices for different clients at once

**Steps:**
1. Load client list with invoice details
2. For each client:
   - Prepare invoice data
   - Calculate totals
   - Generate invoice (PDF or other format)
   - Save with unique filename
3. Track generation success/failure
4. Create summary report of all invoices generated
5. Optionally send invoices via email

**Implementation:**
```javascript
async function batchGenerateInvoices(invoices, outputDir) {
  const results = [];

  for (const invoice of invoices) {
    try {
      // Calculate totals
      const totals = calculateInvoiceTotals(invoice.lineItems, {
        taxRate: invoice.taxRate,
        discountPercent: invoice.discountPercent
      });

      const invoiceData = {
        ...invoice,
        ...totals
      };

      // Generate filename
      const filename = `${outputDir}/invoice-${invoice.invoiceNumber}-${invoice.client.name.replace(/\s+/g, '-')}.pdf`;

      // Generate invoice
      await generateInvoice(invoiceData, filename);

      results.push({
        success: true,
        invoiceNumber: invoice.invoiceNumber,
        client: invoice.client.name,
        total: totals.total,
        filename: filename
      });
    } catch (error) {
      results.push({
        success: false,
        invoiceNumber: invoice.invoiceNumber,
        client: invoice.client.name,
        error: error.message
      });
    }
  }

  // Generate summary report
  const summary = {
    totalInvoices: invoices.length,
    successful: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    totalAmount: results
      .filter(r => r.success)
      .reduce((sum, r) => sum + r.total, 0),
    results: results
  };

  fs.writeFileSync(
    `${outputDir}/batch-summary.json`,
    JSON.stringify(summary, null, 2)
  );

  return summary;
}
```

### Workflow 5: Recurring Invoice Generation
**Purpose:** Automate monthly/weekly recurring invoices

**Steps:**
1. Load recurring invoice templates
2. Check due dates for invoice generation
3. For each due invoice:
   - Clone template data
   - Update invoice number (increment)
   - Update dates (invoice date, due date)
   - Generate new invoice
4. Update next billing date
5. Save invoice records
6. Optionally send email notifications

**Implementation:**
```javascript
function generateRecurringInvoices(recurringInvoices) {
  const today = new Date();
  const generated = [];

  recurringInvoices.forEach(template => {
    const nextBillingDate = new Date(template.nextBillingDate);

    if (nextBillingDate <= today) {
      // Generate invoice
      const invoiceData = {
        ...template,
        invoiceNumber: generateNextInvoiceNumber(template.invoiceNumberPrefix),
        date: today.toISOString().split('T')[0],
        dueDate: calculateDueDate(today, template.paymentTermsDays)
      };

      const totals = calculateInvoiceTotals(invoiceData.lineItems, {
        taxRate: template.taxRate
      });

      generateInvoice({ ...invoiceData, ...totals }, `invoices/invoice-${invoiceData.invoiceNumber}.pdf`);

      // Update next billing date
      template.nextBillingDate = calculateNextBillingDate(
        nextBillingDate,
        template.frequency // 'monthly', 'weekly', 'quarterly'
      );

      generated.push(invoiceData);
    }
  });

  return generated;
}

function calculateDueDate(fromDate, days) {
  const dueDate = new Date(fromDate);
  dueDate.setDate(dueDate.getDate() + days);
  return dueDate.toISOString().split('T')[0];
}

function calculateNextBillingDate(currentDate, frequency) {
  const nextDate = new Date(currentDate);
  switch (frequency) {
    case 'weekly':
      nextDate.setDate(nextDate.getDate() + 7);
      break;
    case 'monthly':
      nextDate.setMonth(nextDate.getMonth() + 1);
      break;
    case 'quarterly':
      nextDate.setMonth(nextDate.getMonth() + 3);
      break;
    case 'yearly':
      nextDate.setFullYear(nextDate.getFullYear() + 1);
      break;
  }
  return nextDate.toISOString().split('T')[0];
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Generate invoice | "create invoice for [client]" |
| From template | "use invoice template for [client]" |
| Calculate totals | "calculate invoice totals" |
| Batch generate | "create invoices for [clients]" |
| Recurring invoice | "generate recurring invoices" |
| Add line item | "add item to invoice" |
| Apply discount | "apply [%] discount" |
| Mark as paid | "mark invoice [number] paid" |

## Best Practices

- **Invoice Numbering:** Use sequential numbers with a prefix (e.g., INV-2025-001)
- **Due Dates:** Clearly specify payment terms (Net 30, Net 15, etc.)
- **Itemization:** Provide detailed descriptions for each line item
- **Tax Compliance:** Apply appropriate tax rates based on jurisdiction
- **Payment Methods:** List all accepted payment methods clearly
- **Contact Info:** Include email and phone for billing questions
- **Currency:** Always specify currency (USD, EUR, etc.)
- **Backup:** Store copies of all generated invoices
- **Versioning:** Track invoice revisions if changes are needed
- **Branding:** Maintain consistent company branding across all invoices
- **Legal Info:** Include business registration numbers, tax ID as required
- **Late Fees:** Specify late payment penalties if applicable
- **Accessibility:** Ensure PDFs are readable by screen readers

## Common Patterns

**Freelance Invoice:**
```javascript
const freelanceInvoice = {
  company: {
    name: 'Your Name',
    address: '123 Main St, City, State 12345',
    email: 'you@example.com',
    phone: '(555) 123-4567'
  },
  client: {
    name: 'Client Co.',
    address: '456 Client Ave, City, State 67890',
    email: 'billing@client.com'
  },
  invoiceNumber: 'INV-2025-001',
  date: '2025-01-15',
  dueDate: '2025-02-14', // Net 30
  lineItems: [
    { description: 'Website Design - January 2025', quantity: 1, rate: 3000 },
    { description: 'Consultation (5 hours)', quantity: 5, rate: 150 }
  ],
  taxRate: 0, // No tax for services in some jurisdictions
  paymentTerms: 'Payment due within 30 days. Accepted methods: Bank transfer, PayPal, Check.'
};
```

**Project-Based Invoice:**
```javascript
const projectInvoice = {
  lineItems: [
    { description: 'Phase 1: Discovery & Planning', quantity: 1, rate: 5000 },
    { description: 'Phase 2: Design Mockups', quantity: 1, rate: 7500 },
    { description: 'Phase 3: Development', quantity: 1, rate: 15000 },
    { description: 'Additional Revisions (8 hours)', quantity: 8, rate: 150 }
  ],
  discountPercent: 10, // Early payment discount
  taxRate: 8.5
};
```

## Dependencies

Install required packages:
```bash
npm install pdfkit          # For PDF generation
npm install handlebars      # For templating
npm install puppeteer       # For HTML to PDF conversion
npm install nodemailer      # For email sending (optional)
```

## Error Handling

- **Missing Data:** Validate all required fields before generation
- **Invalid Amounts:** Ensure all monetary values are valid numbers
- **Date Validation:** Verify date formats and logic (due date after invoice date)
- **File Permissions:** Handle write errors when saving invoices
- **Template Errors:** Catch template rendering errors gracefully
- **Currency Precision:** Always round to 2 decimal places for currency

## Performance Tips

- Cache company logo and branding assets
- Reuse PDF/template instances for batch generation
- Pre-validate data before processing
- Use streaming for large batch operations
- Compress PDFs for email transmission

## Advanced Features

**Email Invoice Delivery:**
```javascript
const nodemailer = require('nodemailer');

async function emailInvoice(invoiceData, pdfPath) {
  const transporter = nodemailer.createTransport({ /* config */ });

  await transporter.sendMail({
    from: invoiceData.company.email,
    to: invoiceData.client.email,
    subject: `Invoice ${invoiceData.invoiceNumber} from ${invoiceData.company.name}`,
    html: `
      <p>Dear ${invoiceData.client.name},</p>
      <p>Please find attached invoice ${invoiceData.invoiceNumber} for $${invoiceData.total}.</p>
      <p>Payment is due by ${invoiceData.dueDate}.</p>
      <p>Thank you for your business!</p>
    `,
    attachments: [
      {
        filename: `invoice-${invoiceData.invoiceNumber}.pdf`,
        path: pdfPath
      }
    ]
  });
}
```

**Payment Tracking:**
```javascript
const invoiceStatus = {
  invoiceNumber: 'INV-2025-001',
  status: 'unpaid', // 'unpaid', 'paid', 'overdue', 'cancelled'
  paidDate: null,
  paidAmount: 0,
  paymentMethod: null
};
```