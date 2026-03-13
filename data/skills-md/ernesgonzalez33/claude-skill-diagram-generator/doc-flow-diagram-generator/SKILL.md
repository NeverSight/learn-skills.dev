---
name: doc-flow-diagram-generator
description: This skill analyzes documentation websites to automatically generate interactive Mermaid flowcharts showing user workflows and processes. Use this skill when users request flow diagrams, process visualization, or workflow documentation from existing product documentation, API docs, or tutorial sites.
---

# Doc Flow Diagram Generator

## Overview

Generate interactive Mermaid flowcharts from documentation websites by automatically crawling, analyzing content, and identifying user workflows. Create diagrams with clickable links back to source documentation sections.

## Core Capabilities

### 1. Single Page Analysis
Start with analyzing individual documentation pages to identify and visualize basic user workflows.

**When to use:** When users provide a specific documentation URL and want to understand the workflow on that page.

**Examples:**
- "Generate a flow diagram from this getting started guide"
- "Create a workflow chart from this API documentation page"
- "Show me the user journey from this tutorial page"

Use `scripts/single_page_parser.py` to fetch and clean page content, then `scripts/basic_flow_detector.py` to identify sequential steps.

### 2. Enhanced Flow Detection
Analyze complex documentation patterns including conditional flows, alternatives, and decision points.

**When to use:** When basic detection misses important workflow elements or when dealing with sophisticated documentation.

**Examples:**
- "This documentation has conditional steps - can you map out all the possible paths?"
- "Generate flowcharts that show the different options users can choose"

Reference `references/flow_patterns.md` for comprehensive detection strategies, and use `scripts/advanced_flow_detector.py` for improved accuracy.

### 3. Multi-Page Documentation Analysis
Crawl entire documentation sites (3-4 levels deep, same domain) to create comprehensive workflow diagrams.

**When to use:** When users want to understand the complete workflow across an entire product's documentation.

**Examples:**
- "Analyze the entire documentation site and create workflow diagrams"
- "Show me all the user journeys across this product's docs"
- "Generate separate flow diagrams for each major feature in the documentation"

Use `scripts/doc_crawler.py` for site crawling and `scripts/multi_page_analyzer.py` for cross-page flow analysis.

### 4. Interactive Diagram Generation
Create Mermaid flowcharts with clickable nodes that link back to specific documentation sections.

**When to use:** Always - this is the default output format for maximum utility and integration.

**Key features:**
- Clickable nodes with anchor links to source documentation
- Separate diagrams for different workflow categories
- Embeddable in existing documentation platforms

Use `scripts/mermaid_with_links.py` and reference `references/mermaid_templates.md` for consistent output formatting.

## Workflow Decision Tree

**Input Type:**
- Single URL → Use Capability 1 (Single Page Analysis)
- Documentation site root → Use Capability 3 (Multi-Page Analysis)
- Complex conditional flows mentioned → Use Capability 2 (Enhanced Detection)

**Output Requirements:**
- Basic visualization → Generate simple Mermaid flowchart
- Integration with docs → Add clickable links (Capability 4)
- Multiple workflows → Generate separate diagrams per workflow type

**Quality Enhancement:**
- Low detection accuracy → Reference `references/flow_patterns.md` for better patterns
- Need better organization → Use `scripts/flow_categorizer.py` for workflow grouping

## Resources

This skill includes specialized tools and references for documentation analysis and diagram generation:

### scripts/
Python utilities for web scraping, content analysis, and diagram generation:

- `single_page_parser.py` - Fetch and clean content from individual documentation pages
- `basic_flow_detector.py` - Identify sequential workflows using common patterns
- `advanced_flow_detector.py` - Enhanced flow detection with confidence scoring
- `doc_crawler.py` - Multi-page documentation site crawler (respects robots.txt)
- `multi_page_analyzer.py` - Aggregate and categorize flows across multiple pages
- `mermaid_with_links.py` - Generate Mermaid flowcharts with clickable links
- `flow_categorizer.py` - Group and organize related workflows
- `flow_connector.py` - Identify connections between different flows

**Dependencies:** BeautifulSoup4, requests, urllib.robotparser for web scraping and parsing.

### references/
Documentation and patterns for effective flow detection:

- `flow_patterns.md` - Comprehensive patterns for identifying workflows in documentation
- `mermaid_templates.md` - Mermaid syntax templates and best practices
- `link_strategies.md` - Strategies for creating meaningful links back to documentation sections

**Usage:** Load these references when flow detection accuracy needs improvement or when working with complex documentation structures.

### assets/
Templates and examples for consistent diagram output:

- `flow_template.mmd` - Base Mermaid template for consistent styling
- `sample_output.html` - Example of embedded diagrams in documentation
- `integration_examples/` - Templates for common documentation platforms

**Usage:** Copy and customize these templates when generating final diagram outputs for specific platforms.