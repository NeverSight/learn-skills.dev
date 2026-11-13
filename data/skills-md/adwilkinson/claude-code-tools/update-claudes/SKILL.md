---
name: update-claudes
author: Andrew Wilkinson (github.com/ADWilkinson)
description: Creates or updates CLAUDE.md files throughout the project to provide comprehensive AI development context. Use this to systematically document your codebase for AI assistants.
allowed-tools: Bash, Glob, Read, Write, Edit, Task
disable-model-invocation: true
---

# /update-claudes

> **Quick Reference**: Analyze project → Score complexity → If complex, launch parallel agents → Create strategic CLAUDE.md files → Validate coverage.

Creates or updates CLAUDE.md files throughout the project to provide comprehensive AI development context.

## Purpose
This command systematically analyzes your project structure and creates/updates CLAUDE.md files at strategic locations to help AI assistants understand your codebase architecture, patterns, and conventions.

## Core Documentation Principle: Document Current State Only

**Always document what "is", never what "was changed" or "improved". Documentation should read as if the current implementation has always existed.**

### Documentation Anti-Patterns to Avoid:
- "Refactored the component to use hooks instead of class components"
- "Improved performance by implementing caching"
- "Previously used X, now uses Y for better results"

### Documentation Best Practices:
- "The component uses React hooks for state management"
- "Implements caching for optimal performance"
- "Uses Y architecture for scalability"

## Step 1: Automatic Project Analysis

First, conduct an automated analysis to understand project structure and complexity:

```bash
# Map existing CLAUDE.md files
find . -name "CLAUDE.md" -type f | sort

# Identify main source directories (Web3/React/TypeScript patterns)
SOURCE_DIRS=$(find . -maxdepth 2 -type d \( -name "src" -o -name "lib" -o -name "app" -o -name "packages" -o -name "components" -o -name "contracts" -o -name "pages" -o -name "hooks" -o -name "contexts" -o -name "utils" -o -name "services" -o -name "types" \) 2>/dev/null | head -8)

# If no standard directories found, use project root
if [ -z "$SOURCE_DIRS" ]; then
    SOURCE_DIRS="."
fi

# Count directories and files across identified source areas
for dir in $SOURCE_DIRS; do
    echo "Analyzing: $dir"
    find "$dir" -type d -mindepth 1 -maxdepth 3 | wc -l  # Directory count
    find "$dir" \( -name "*.tsx" -o -name "*.ts" -o -name "*.js" -o -name "*.jsx" -o -name "*.sol" -o -name "*.vy" -o -name "*.css" -o -name "*.scss" -o -name "*.less" -o -name "*.json" -o -name "*.md" \) | wc -l  # File count
    ls -la "$dir" | head -10  # Structure overview
done

# Check for Web3/React/TypeScript indicators
ls package.json yarn.lock pnpm-lock.yaml tsconfig.json vite.config.* webpack.config.* next.config.* hardhat.config.* foundry.toml truffle-config.js 2>/dev/null || echo "Analyzing project type from files"

# Check for Web3 specific directories and files
find . -maxdepth 2 -type d \( -name "contracts" -o -name "artifacts" -o -name "typechain" -o -name "typechain-types" -o -name "deployments" -o -name "scripts" \) 2>/dev/null
find . -maxdepth 2 -name "*.sol" -o -name "hardhat.config.*" -o -name "foundry.toml" -o -name "remix-*" 2>/dev/null
```

**Automatically assess complexity based on:**
- **Directory count** (>10 directories = complex)
- **File count** (>50 files = complex)
- **Existing CLAUDE.md coverage** (gaps indicate needed documentation)
- **Framework diversity** (multiple languages/frameworks = complex)
- **Feature boundaries** (distinct functional areas)

## Step 2: Automatic Strategy Decision

Based on the analysis results, automatically determine approach:

### Complexity Scoring:
- **Simple Project** (Score 0-2): Direct documentation approach
  - <10 directories, <50 files
  - Single framework/language
  - Few or well-covered CLAUDE.md files

- **Complex Project** (Score 3+): Multi-agent approach
  - 10+ directories, 50+ files
  - Multiple frameworks/languages
  - Significant CLAUDE.md gaps
  - Distinct feature boundaries

### Multi-Agent Strategy (Auto-Deployed for Complex Projects):
If complexity score ≥ 3, automatically spawn these specialized agents in parallel:

- **Project Structure Agent** (general-purpose): Maps overall architecture and identifies documentation gaps
- **Frontend Architecture Agent** (frontend-developer): Analyzes React/UI patterns and component organization
- **Blockchain Integration Agent** (blockchain-specialist): Reviews Web3 patterns, smart contracts, and DeFi integration
- **Backend Integration Agent** (backend-developer): Reviews API patterns, data flow, and service integration
- **Testing Strategy Agent** (testing-specialist): Documents test patterns, coverage, and quality practices

## Step 3: Create CLAUDE.md Files Strategically

### Root Level CLAUDE.md
Always start with or update the main project CLAUDE.md with:
- Project overview and purpose
- Technology stack summary
- Key architectural decisions
- Development setup instructions
- Common development patterns
- Testing approach

### Component-Level CLAUDE.md Files
Create these for major functional areas (adapt paths to your project structure):

**React/TypeScript Frontend:**
- `src/components/CLAUDE.md` - React component patterns, architecture, and reusable UI components
- `src/hooks/CLAUDE.md` - Custom React hooks, state management, and side effect handling
- `src/contexts/CLAUDE.md` - React Context providers, global state, and data sharing patterns
- `src/pages/CLAUDE.md` - Page-level components and routing (Next.js App/Pages Router, React Router)
- `src/services/CLAUDE.md` - API integration, data fetching, and external service communication
- `src/utils/CLAUDE.md` - Shared utilities, helper functions, formatters, and pure functions
- `src/types/CLAUDE.md` - TypeScript type definitions, interfaces, and type utilities

**Web3/Blockchain Integration:**
- `contracts/CLAUDE.md` - Solidity smart contracts and architecture
- `src/web3/CLAUDE.md` or `src/blockchain/CLAUDE.md` - Web3 integration patterns and blockchain interactions
- `src/abis/CLAUDE.md` - Contract ABIs and TypeScript type generation (TypeChain)
- `typechain-types/CLAUDE.md` - Generated TypeScript contract types and usage patterns
- `scripts/CLAUDE.md` - Deployment scripts, contract interactions, and automation
- `src/lib/CLAUDE.md` - Web3 library integrations (viem, ethers, wagmi, privy, etc.)

**Build & Configuration:**
- `src/config/CLAUDE.md` - Application configuration, environment variables, and setup
- `src/constants/CLAUDE.md` - Contract addresses, chain configurations, API endpoints, and constants
- `tests/CLAUDE.md` or `__tests__/CLAUDE.md` - Testing strategies (Jest, Vitest, React Testing Library, Hardhat, Foundry)
- `src/styles/CLAUDE.md` - Styling patterns (CSS Modules, Styled Components, Tailwind CSS, Emotion)

### Feature-Specific CLAUDE.md Files
For complex features with 3+ files and unique patterns, create documentation based on actual feature areas discovered in the project.

## Step 4: CLAUDE.md Content Structure

Use this template for consistency:

```markdown
# [Area Name] - Development Context

## Overview
Brief description of this area's purpose and role in the system.

## Key Files and Structure
```
[discovered-structure]/
├── [main-files]         # Primary files handling [functionality]
├── [type-definitions]   # Type definitions, interfaces, schemas
├── [utilities]          # Helper functions and utilities
└── [tests]              # Test files and test utilities
```

## Architecture Patterns
- Key architectural decisions made in this area
- Design patterns used (e.g., "Uses Repository pattern for data access")
- Integration approaches with other parts of the system
- Framework-specific patterns and conventions

## Development Guidelines
- Coding conventions specific to this area
- Language/framework-specific best practices
- Common patterns to follow when adding new functionality
- Important considerations when modifying existing code

## Testing Strategy
- Testing frameworks and approaches used
- Key test scenarios and edge cases
- Mock strategies and test utilities
- Coverage expectations and quality gates

## Common Tasks
- How to add new [components/modules/handlers/etc.]
- How to modify existing functionality
- How to debug issues in this area
- Development workflow and tooling

## Integration Points
- How this area connects to other parts of the system
- External dependencies and their usage
- Data flow patterns and communication protocols
- API contracts and interfaces
```

## Step 5: Automated Execution

**Execution Logic:**
```
1. Run project analysis commands automatically
2. Calculate complexity score based on metrics
3. If score < 3: Proceed with direct documentation creation
4. If score ≥ 3: Launch multi-agent analysis in parallel
```

**For Simple Projects (Direct Approach):**
Proceed immediately to create CLAUDE.md files using established patterns and templates.

**For Complex Projects (Multi-Agent Approach):**
Automatically launch these agents in parallel using the Task tool:

```
Task 1 (subagent_type: "general-purpose"): "Discover and analyze the actual project structure (not assuming src/ or any specific layout). Identify main source directories, file organization patterns, and existing documentation gaps. Map the real directory structure and return a comprehensive list of CLAUDE.md files needed with priority levels based on the discovered architecture."

Task 2 (subagent_type: "frontend-developer"): "Analyze React/TypeScript frontend architecture including component patterns, custom hooks, Context providers, state management (Redux/Zustand), routing (Next.js/React Router), styling approaches, and build configuration (Vite/Webpack/Next.js). Create CLAUDE.md content for all frontend areas following modern React and TypeScript best practices."

Task 3 (subagent_type: "blockchain-specialist"): "IF Web3/blockchain code is detected (Solidity contracts, Web3 integration, popular libraries like viem/ethers/wagmi/privy/etc.), analyze smart contract architecture, Web3 integration patterns, contract interaction methods, wallet connection strategies, transaction handling, chain configurations, and blockchain-specific utilities. Create CLAUDE.md content for Web3 areas covering contract deployment patterns, ABI usage, TypeChain integration, and dApp architecture with modern Web3 libraries."

Task 4 (subagent_type: "testing-specialist"): "Analyze testing strategies across the entire codebase regardless of language/framework. Identify test directories, testing frameworks used, coverage approaches, and quality practices. Create CLAUDE.md content documenting test patterns, mock strategies, and testing conventions for the actual test setup found."

Task 5 (subagent_type: "general-purpose"): "Analyze configuration files, build systems, deployment setup, CI/CD, documentation, and cross-cutting concerns. Create CLAUDE.md content for infrastructure, tooling, and project management areas based on what actually exists in the project."
```

**Agent Coordination:**
Each agent focuses on their specialty while following the established CLAUDE.md template and quality guidelines. Results are synthesized into a comprehensive documentation update.

## Step 6: Quality Guidelines

**Make Documentation Actionable:**
- Include specific file paths and examples
- Document actual patterns used in the codebase
- Provide guidance for common development tasks
- Focus on what developers (human or AI) need to know

**Keep It Current:**
- Document the present state of the system
- Avoid historical context or change descriptions
- Focus on "how it works" not "how it was built"

**Optimize for AI Consumption:**
- Use clear section headers
- Include file path references
- Structure information hierarchically
- Use consistent formatting

## Step 7: Validation and Completion

After creating CLAUDE.md files:
1. Verify all major functional areas are covered
2. Ensure consistent structure across files
3. Check that integration points are documented
4. Confirm development patterns are captured
5. Test that the documentation helps with common tasks

## When NOT to Create CLAUDE.md Files

Skip documentation for:
- Simple utility functions (1-2 files)
- Standard configurations without customization
- Temporary or experimental code
- Areas that are straightforward applications of documented patterns
- Third-party integrations that are standard implementations

The goal is strategic documentation that genuinely helps AI assistants understand your codebase architecture and development patterns, not comprehensive coverage of every file.
