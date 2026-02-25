---
name: find-my-skills
description: Use this skill when users need to find the most suitable tools from **locally installed skills**. Suitable for "recommend skills for stage Y", "choose skills based on my project", "are there local skills that can do X". This skill fully considers conversation context, project background and progress, and provides accurate recommendations through multi-dimensional classification (workflow stages, domains, file types, etc.). For searching and installing new external skills, please use find-skills.
---

# Find My Skills - Local Skills Intelligent Recommendation System

An intelligent local skills recommendation system that helps you quickly find the most suitable tools from your installed skills.

## ✨ Core Features

1. **Local-First Search**: Focus on your installed skills, avoid duplicate installations
2. **Context-Aware**: Precise recommendations based on conversation history and project progress
3. **Multi-Dimensional Classification**: Workflow stages, professional domains, function types, and more
4. **Flexible Classification Strategies**: 5 preset strategies plus custom strategies
5. **Automatic Index Generation**: One-click scan of local skills and index creation

## 🚀 Quick Start

### First-Time Use

If you're using find-my-skills for the first time, you need to initialize:

```
/find-my-skills:init
```

The initialization process will:
1. Scan your local `~/.claude/skills/` and `~/.agents/skills/` directories
2. Extract metadata (name, description) from each skill
3. Let you choose a classification strategy (workflow-oriented, domain-oriented, functional-oriented, etc.)
4. Generate a personalized `skills-catalog.md` directory document
5. Create index data for quick recommendations

**Estimated Time**: 2-3 minutes (depending on the number of installed skills)

### Choose Classification Strategy

During initialization, 5 classification strategies are provided:

| Strategy | Description | Suitable For |
|----------|-------------|--------------|
| **Workflow-Oriented** | Organized by project development process (Planning→Implementation→Review→Documentation→Deployment) | Software developers, project managers |
| **Domain-Oriented** | Organized by professional domain (Bioinformatics, ML, Academic Research, etc.) | Researchers, data scientists |
| **Functional-Oriented** | Organized by function type (Create, Analyze, Transform, Query, etc.) | General users, cross-domain workers |
| **Mixed** | Two-dimensional classification: Workflow × Domain | Advanced users |
| **Custom** | User-defined classification dimensions and keywords | Users with specific needs |

💡 **Recommendation**: If unsure, choose "Domain-Oriented" or "Workflow-Oriented"

---

## 📌 When to Use find-my-skills vs find-skills

### Use `/find-my-skills` (this skill) when:
- ✅ Need to recommend the most suitable tools from **locally installed skills**
- ✅ Want recommendations that **consider project context and current progress**
- ✅ Need skills for specific workflow stages (planning, implementation, review, etc.)
- ✅ Need skills for specific professional domains (bioinformatics, ML, etc.)
- ✅ Need **skill combination suggestions** and **follow-up recommendations**

### Use `/find-skills` (external search) when:
- 🔍 Need to **search online registry** for new skills
- 📦 Need to **install skills not yet installed**
- 🆕 Want to explore **latest community contributions**
- 🌐 Unsure if a certain capability exists locally

**Quick Judgment**: If it contains words like "online", "search", "install", "new", use external find-skills; otherwise use this skill.

---

## 🎯 Usage Methods

### Method 1: Direct Need Description (Recommended)

The most natural way, directly tell AI your needs:

```
"I need to analyze single-cell sequencing data"
"How to plan a new project"
"Is there a tool to generate PDF reports"
```

AI will:
- Analyze your conversation history and project context
- Understand your current work stage
- Recommend the most suitable skill combinations
- Explain recommendation reasons
- Provide usage examples

### Method 2: Use Subskill Skills (Quick Navigation)

If you clearly know the type of need, you can directly use the corresponding subskill:

#### By Workflow Stage

| Subskill Command | Description | Use Cases |
|-----------------|-------------|-----------|
| `/find-my-skills:planning` | Planning & design stage tools | Requirements analysis, scope definition, architecture design |
| `/find-my-skills:implementing` | Implementation stage tools | Coding, testing, debugging |
| `/find-my-skills:reviewing` | Review & validation stage tools | Code review, test validation, quality check |
| `/find-my-skills:documenting` | Documentation stage tools | Documentation writing, report generation, knowledge recording |

#### By Professional Domain

| Subskill Command | Description | Use Cases |
|-----------------|-------------|-----------|
| `/find-my-skills:bioinformatics` | Bioinformatics tools | Biological data analysis, genomics, molecular biology |
| `/find-my-skills:ml` | Machine learning & data science tools | Data processing, model training, AI development |
| `/find-my-skills:academic` | Academic research & paper tools | Literature review, paper writing, academic publishing |

#### By Function Type

| Subskill Command | Description | Use Cases |
|-----------------|-------------|-----------|
| `/find-my-skills:write` | Writing & creation tools | Documentation, reports, content creation |
| `/find-my-skills:visualize` | Visualization & chart tools | Data visualization, chart creation, graphic design |

---

## 🧠 Recommendation Logic

### Context-First Principle ⚠️

Recommended skills must match the current project state and progress, not answer questions in isolation.

AI will:
1. **Review conversation history**: Understand current project background, goals, and principles
2. **Assess project progress**: Identify the stage the user is currently at
3. **Analyze project characteristics**: Understand tech stack, domain characteristics, scale and complexity
4. **Consider completed work**: Identify completed work and problems to solve
5. **Understand user intent**: Infer real needs from context

### Multi-Dimensional Matching

The recommendation algorithm considers 4 dimensions (sorted by weight):

1. **Workflow Stage** (40%): Planning, implementation, review, documentation, deployment
2. **Professional Domain** (30%): Bioinformatics, machine learning, software engineering, etc.
3. **File Type** (20%): .docx, .py, .md, biological data formats, etc.
4. **Function Type** (10%): Create, analyze, transform, query, etc.

### Recommendation Output Format

```
📋 Context Understanding:
[Brief explanation of understanding of current project state]

Main Recommendation:
- `/namespace:skill-name` - Recommendation reason
  Usage example: ...

Alternative Options:
- `/namespace:alternative1` - Description
- `/namespace:alternative2` - Description

Supporting Recommendations:
- `/namespace:complementary` - Can be used together to...

📌 Next Step Suggestions:
[Follow-up suggestions based on project progress]
```

---

## 🔄 Maintenance and Updates

### Refresh Index

When you install new skills or want to change classification strategy:

```
/find-my-skills:init --refresh
```

### View Generated Catalog

After initialization, `skills-catalog.md` will be generated in the current directory, where you can:
- View all installed skills
- Browse by category
- Quickly find specific functions

### Custom Classification

If preset strategies don't meet your needs, you can:
1. Copy `templates/custom-strategy-template.yaml`
2. Modify classification dimensions and keywords
3. Re-run initialization and select your custom strategy

---

## 📚 Usage Examples

### Example 1: Project Planning Stage

```
User: "I'm starting a bioinformatics project, what should I do first?"

AI Analysis:
- Workflow Stage: Planning & design
- Professional Domain: Bioinformatics
- Context: Project initiation

Recommendations:
Main: /boundary-lock (Define project scope)
Supporting: /scientific-skills:literature-review (Literature research)
Next Step: After planning, use /find-my-skills:implementing to find implementation tools
```

### Example 2: Data Analysis Stage

```
User: "I have single-cell RNA-seq data to analyze"

AI Analysis:
- Workflow Stage: Implementation
- Professional Domain: Bioinformatics (transcriptomics)
- File Type: Biological data format
- Context: Data analysis task

Recommendations:
Main: /scientific-skills:scanpy (Standard single-cell analysis tool)
Alternative: /scientific-skills:scvi-tools (Deep learning approach)
Supporting: /scientific-skills:anndata (Data structure management)
Next Step: After analysis, use /find-my-skills:visualize for result visualization
```

### Example 3: Paper Writing Stage

```
User: "Need to write a machine learning paper"

AI Analysis:
- Workflow Stage: Documentation
- Professional Domain: Machine learning + Academic research
- File Type: Academic documents
- Context: Academic writing task

Recommendations:
Main: /ml-paper-writing:20-ml-paper-writing (ML paper specialized)
Supporting:
- /scientific-skills:citation-management (Citation management)
- /scientific-skills:venue-templates (Conference templates)
- /scientific-skills:scientific-visualization (Result charts)
```

---

## 🛠️ Technical Details

### Index Data Storage

- **Location**: `~/.claude/skills/find-my-skills/user-index.json`
- **Format**: JSON
- **Content**: Skills metadata, classification info, strategy configuration

### Catalog Document Generation

- **Location**: `./skills-catalog.md` (current directory)
- **Format**: Markdown
- **Content**: Structured skills catalog, organized by selected strategy

### Compatibility

- ✅ macOS
- ✅ Linux
- ✅ Windows (WSL)
- ✅ Cross-user environment

---

## 🆘 Troubleshooting

### Issue 1: Initialization Fails

**Symptoms**: Error when running `/find-my-skills:init`

**Possible Causes**:
- Permission issues
- SKILL.md format errors
- Directory doesn't exist

**Solutions**:
```bash
# Check directory permissions
chmod +x ~/.claude/skills
chmod +x ~/.agents/skills

# Force re-initialization
/find-my-skills:init --force
```

### Issue 2: Inaccurate Recommendations

**Symptoms**: Recommended skills don't match needs

**Possible Causes**:
- Index is outdated
- Inappropriate classification strategy
- Context understanding deviation

**Solutions**:
1. Refresh index: `/find-my-skills:init --refresh`
2. Change classification strategy
3. Provide more detailed need description

### Issue 3: Cannot Find a Skill

**Symptoms**: You know a skill is installed, but it doesn't appear in recommendations

**Possible Causes**:
- Index not updated
- Keywords don't match
- Skill is in non-standard directory

**Solutions**:
1. Refresh index
2. Check `skills-catalog.md` to confirm if indexed
3. Use custom classification strategy to add relevant keywords

---

## 📖 Related Resources

- **Initialization Guide**: `/find-my-skills:init` for detailed initialization process
- **Classification Strategy Templates**: YAML files in `templates/` directory
- **Skills Catalog**: Generated `skills-catalog.md`
- **Project Plan**: `/Users/stephen/.claude/plans/memoized-herding-lake.md`

---

## 🤝 Relationship with Other Skills

- **find-skills** (external): Complementary relationship, local index vs online search
- **Subskill skills**: Inheritance relationship, providing scenario-specific optimization
- **Other skills**: Recommended objects, quickly located through this skill

---

## 💡 Best Practices

1. **Must initialize on first use**: Ensure index data exists
2. **Regularly refresh index**: Update promptly after installing new skills
3. **Provide sufficient context**: Let AI understand your project background
4. **Use subskills for quick navigation**: Use subskills directly when need type is clear
5. **View generated catalog**: `skills-catalog.md` can be referenced offline
6. **Custom strategies**: Create your own classification when presets don't meet needs

---

**Get Started**: `/find-my-skills:init` 🚀
