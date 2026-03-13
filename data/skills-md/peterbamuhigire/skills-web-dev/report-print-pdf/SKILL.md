---
name: report-print-pdf
description: "Guidance for building report templates that serve both mPDF exports and the browser-based print workflow, including the auto-print standard introduced in the report-printing-style guide."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

**Frontend Design plugin (`webapp-gui-design`):** MUST be active for all visual output from this skill. Use for design system work, component styling, layout decisions, colour selection, typography, responsive design, and visual QA.

# Report Export (PDF + Print)

Build a single, minimal HTML report that renders consistently in **mPDF** and **browser print** (HTML → print dialog). Keep typography compact, tables pagination-friendly, and metadata consistent across outputs.

## Security Baseline (Required)

Always load and apply the **Vibe Security Skill** when reports touch user input, filters, file paths, or authentication. Treat output encoding and access control as mandatory.

**Cross-Platform:** Reports deploy to Windows dev, Ubuntu staging, and Debian production. Use forward-slash paths (`/`) for file references. Use `sys_get_temp_dir()` for temporary PDF files. Ensure font paths work on both OS (use relative paths from project root).

## When to Use

- Generating PDF reports with mPDF in PHP
- Printing HTML reports via browser print dialog
- Needing a shared HTML layout for both PDF and print
- Requiring strict number/date formatting and tight spacing
- Producing multi-page tables with repeating headers

## Core Workflow

1. **Prepare data and metadata**
   - Resolve organization name, address, and logo path
   - Compute report title and optional period label (e.g., `23 Aug, 2025`)
   - Resolve “Printed By” from logged-in user name
   - Format “Printed On” as `d F Y, h:i A` (e.g., `23 September 2025, 05:36 PM`)
   - Never render raw SQL timestamps (e.g., `2026-01-25 00:00:00`). Always format dates as `d M Y` or `d F Y`, and include time only when explicitly required.
   - When building standalone PHP scripts outside of a namespace, never add `use DateTime` (it has no effect) or other global symbol `use` statements; just instantiate the built-in class via `new \DateTime()` so your files stay warning-free.

2. **Build minimal HTML (shared by PDF + Print)**
   - Compact header: logo left, org name/address center/left, report title + period right
   - Tight vertical rhythm: 6–12px gaps, no large vertical spacing
   - DejaVu Sans for clarity at small sizes
   - Table with `thead`/`tbody` and subtle borders

3. **Render with mPDF**
   - Use small margins and a clean footer
   - Keep header inside body HTML (set empty mPDF header)

4. **Render with browser print**
   - API returns full HTML (`text/html`)
   - UI opens new window/tab, writes HTML, calls `window.print()` when ready
   - Print CSS mirrors the PDF layout (compact header, repeating headers, small footer)

## Formatting Helpers

```php
final class ReportFormatting {
    public static function formatDateShort(?string $value): string {
        if (empty($value)) {
            return '-';
        }
        return (new DateTime(substr($value, 0, 10)))->format('d M Y');
    }

    public static function formatDateLong(?string $value): string {
        if (empty($value)) {
            return '-';
        }
        return (new DateTime(substr($value, 0, 10)))->format('d F Y');
    }

    public static function formatPeriod(?string $startDate, ?string $endDate): string {
        if (empty($startDate) && empty($endDate)) {
            return '';
        }
        $start = $startDate ? (new DateTime($startDate))->format('d M, Y') : '';
        $end = $endDate ? (new DateTime($endDate))->format('d M, Y') : '';
        if ($start && $end) {
            return $start === $end ? $start : "$start - $end";
        }
        return $start ?: $end;
    }

    public static function formatPrintedOn(DateTime $date): string {
        return $date->format('d F Y, h:i A');
    }

    public static function formatNumber($value): string {
        if ($value === null || $value === '') {
            return '0';
        }
        $num = (float)$value;
        $isWhole = abs($num - round($num)) < 0.00001;
        return $isWhole
            ? number_format($num, 0, '.', ',')
            : number_format($num, 2, '.', ',');
    }
}
```

## HTML Template (Minimalistic + Clean)

```php
final class ReportHtmlTemplate {
    public static function build(
        array $meta,
        string $tableHtml,
        string $summaryHtml = '',
        bool $includeFooter = false,
        string $printedBy = '',
        string $printedOn = ''
    ): string {
        $orgName = htmlspecialchars($meta['org_name'] ?? '');
        $orgAddress = htmlspecialchars($meta['org_address'] ?? '');
        $reportTitle = htmlspecialchars($meta['title'] ?? '');
        $periodLabel = htmlspecialchars($meta['period'] ?? '');
        $logoPath = htmlspecialchars($meta['logo_path'] ?? '');

        $periodHtml = $periodLabel !== ''
            ? '<div class="period">Period: ' . $periodLabel . '</div>'
            : '';

        $footerHtml = $includeFooter
            ? '<div class="print-footer">'
                . '<div class="print-left">Printed By: ' . htmlspecialchars($printedBy) . '</div>'
                . '<div class="print-right">Printed On ' . htmlspecialchars($printedOn) . '</div>'
            . '</div>'
            : '';

        return <<<HTML
<style>
    body { font-family: dejavu sans; font-size: 10px; color: #111; }
    .report-header { width: 100%; border-bottom: 1px solid #e6e6e6; padding-bottom: 6px; }
    .header-row { display: table; width: 100%; }
    .header-cell { display: table-cell; vertical-align: middle; }
    .logo { width: 54px; height: 54px; }
    .org-name { font-size: 13px; font-weight: bold; margin-bottom: 2px; }
    .org-address { font-size: 9px; color: #555; }
    .report-title { font-size: 12px; font-weight: 600; text-align: right; }
    .period { font-size: 9px; color: #555; text-align: right; margin-top: 2px; }
    .section-gap { margin-top: 8px; }

    table { width: 100%; border-collapse: collapse; margin-top: 6px; }
    thead { display: table-header-group; }
    th { background: #f7f7f7; font-weight: 600; border: 1px solid #e5e5e5; padding: 5px; }
    td { border: 1px solid #e5e5e5; padding: 5px; }
    .text-right { text-align: right; }
    .text-center { text-align: center; }

    .print-footer { width: 100%; font-size: 7px; color: #555; margin-top: 8px; }
    .print-left { float: left; }
    .print-right { float: right; }

    @media print {
        body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .print-footer { position: fixed; bottom: 8px; left: 0; right: 0; }
        .section-gap { margin-top: 6px; }
        tr, td, th { page-break-inside: avoid; }
    }
</style>

<div class="report-header">
    <div class="header-row">
        <div class="header-cell" style="width: 60px;">
            <img class="logo" src="{$logoPath}" alt="Logo" />
        </div>
        <div class="header-cell">
            <div class="org-name">{$orgName}</div>
            <div class="org-address">{$orgAddress}</div>
        </div>
        <div class="header-cell" style="text-align: right;">
            <div class="report-title">{$reportTitle}</div>
            {$periodHtml}
        </div>
    </div>
</div>

<div class="section-gap">{$summaryHtml}</div>
{$tableHtml}
{$footerHtml}
HTML;
    }
}
```

## Table Layout Rules (Multi-Page Friendly)

- Use a proper `thead` + `tbody`
- Set `thead` to `display: table-header-group` for repeating headers
- Keep padding tight (4–6px)
- Use thin borders and subtle header shading
- Avoid breaking rows across pages (`page-break-inside: avoid`)

## mPDF Wrapper Setup

```php
$mpdf = new \Mpdf\Mpdf([
    'format' => 'A4',
    'margin_left' => 10,
    'margin_right' => 10,
    'margin_top' => 38,
    'margin_bottom' => 18,
    'default_font' => 'dejavusans'
]);

$footerHtml = '<div style="width:100%; font-size:7px; color:#555;">'
    . '<div style="float:left;">Printed By: ' . htmlspecialchars($printedBy) . '</div>'
    . '<div style="float:right;">Printed On ' . ReportFormatting::formatPrintedOn(new DateTime()) . '</div>'
    . '</div>';

$mpdf->SetHTMLHeader('');
$mpdf->SetHTMLFooter($footerHtml);
$mpdf->WriteHTML(ReportHtmlTemplate::build($meta, $tableHtml, $summaryHtml));
$mpdf->Output($fileName, 'I');
```

## Print Flow (HTML → Print Dialog)

1. UI calls report API endpoint with filters (date range, status, warehouse, etc.)
2. API renders full HTML report and returns it as `text/html`
3. UI opens a new window/tab, writes HTML, waits for load, then calls `window.print()`
4. Print CSS mirrors the PDF layout (compact header, repeating `thead`, small footer)
5. User prints or saves as PDF from the browser dialog

## Auto-Print Helper

- When building dedicated print views (e.g., `*-print.php`), append this snippet before `</body>` and keep `docs/report-printing-standard.md` in sync:

```html
<script>
  window.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      window.print();
    }, 400);
  });
</script>
```

- The short timeout allows logos, fonts, and computed layout to settle before the native dialog grabs the page.
- Keep `no-print` helpers for reprint actions so the dialog can be reopened without a full refresh.

### Browser Print Example (JS)

```javascript
async function openReportPrint(url, params) {
  const query = new URLSearchParams(params).toString();
  const html = await fetch(`${url}?${query}`, { credentials: "include" }).then(
    (r) => r.text(),
  );

  const printWindow = window.open("", "_blank");
  printWindow.document.open();
  printWindow.document.write(html);
  printWindow.document.close();

  printWindow.onload = () => {
    printWindow.focus();
    printWindow.print();
  };
}
```

### API Endpoint Example (PHP)

```php
header('Content-Type: text/html; charset=utf-8');

$meta = [
    'org_name' => $org->name,
    'org_address' => $org->address,
    'logo_path' => $org->logo_path,
    'title' => $reportTitle,
    'period' => ReportFormatting::formatPeriod($startDate, $endDate)
];

$printedOn = ReportFormatting::formatPrintedOn(new DateTime());
$printedBy = $currentUser->name;

echo ReportHtmlTemplate::build(
    $meta,
    $tableHtml,
    $summaryHtml,
    true,
    $printedBy,
    $printedOn
);
```

## Visual Standards

- **Font**: DejaVu Sans
- **Body text**: 10–11px
- **Table text**: 9–10px
- **Footer text**: 7–8px
- **Spacing**: 6–12px between header and content
- **Color**: White background, subtle gray borders

## Number Formatting Rules

- Whole numbers → commas, no decimals
- Non-whole numbers → commas, 2 decimals

## Summary

Use this skill to produce consistent, clean, minimal **PDF exports and browser-printed reports** with the same HTML: compact header/footer, repeatable table headers, strict number/date formatting, and tight spacing for professional multi-page output.
