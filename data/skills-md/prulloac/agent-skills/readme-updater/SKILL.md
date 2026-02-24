---
name: readme-updater
description: Use this skill when you need to keep a repository's README.md file updated with project metadata, installation instructions, usage examples, and more. It automates synchronization by analyzing codebase patterns and dependencies.
---

# README Updater

This skill helps maintain a consistent and up-to-date `README.md` file for your repository. It automates the process of extracting information from the project's codebase to ensure documentation is always in sync with implementation.

## Features

1.  **Project Overview Synchronization**: Updates the project description and features list based on the latest implementation.
2.  **Installation & Setup Tracking**: Automatically detects project type (Node.js, Python, Rust, etc.) and updates setup/installation commands.
3.  **Usage Examples Generator**: Scrapes code examples from test suites or `examples/` directory and integrates them into the README.
4.  **Version and Changelog Linking**: Keeps the current version and links to the `CHANGELOG.md` updated.
5.  **Dependency Visualization**: Optionally generates or updates a list of main dependencies or a simple architecture overview.

## Workflow

### Step 1: Analyze the Workspace

Before updating, the agent must gather context about the project's current state.

- **Check root files**: Look for `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `setup.py`, etc.
- **Determine project type**: Identify the primary language and frameworks used
- **Locate entry points**: Find the main script or binary that users will interact with
- **Extract metadata**: Parse version, name, description from configuration files
- **Discover dependencies**: List main dependencies and development dependencies
- **Find examples**: Look for `examples/`, `demo/`, or `test/` directories with usage samples

### Step 2: Identify Update Scope

Determine what needs updating:

- **README exists?** If not, create from standard template
- **Which sections?** Analyze current README and identify stale sections
- **Version changed?** Compare README version with actual version in `package.json`, `Cargo.toml`, etc.
- **Features updated?** Check if new features need to be documented
- **Dependencies changed?** Verify dependency list is current
- **Examples stale?** Check if example code matches current API

### Step 3: Extract Current Information

Build a profile of the project:

1. **Project metadata**: Name, description, version, repository URL
2. **Installation instructions**: Commands needed to set up the project
3. **Usage examples**: Working code examples from tests or examples directory
4. **Configuration**: Environment variables, config files, custom options
5. **Dependencies**: List of critical or main dependencies
6. **Supported platforms**: OS, Node versions, Python versions, etc.

### Step 4: Update README Content

For each section that needs updating:

1. **Project Overview** (Top section):
   - Update project title and description
   - Add/update feature list
   - Add badges (downloads, version, license, build status)

2. **Installation Section**:
   - Update prerequisite list
   - Provide correct install commands for detected project type
   - Include multiple installation methods if applicable

3. **Usage Section**:
   - Add quick start example
   - Update command syntax if changed
   - Include common flags or options

4. **Examples Section**:
   - Extract or update code examples
   - Ensure examples actually work with current version
   - Add multiple usage scenarios

5. **Configuration Section**:
   - Document all environment variables
   - List configuration file locations and formats
   - Provide example configurations

6. **Footer Sections**:
   - Update Contributing link if `CONTRIBUTING.md` exists
   - Keep License reference current
   - Update version and changelog links

### Step 5: Validation & Verification

Always verify the README's correctness after an update:

- ✅ All links are valid and pointing to correct files
- ✅ All commands are correct, tested, and up-to-date
- ✅ Installation steps match actual project requirements
- ✅ Code examples are syntactically correct and runnable
- ✅ Version numbers match across README and `package.json`/manifest files
- ✅ Tone remains consistent with original documentation
- ✅ No broken markdown syntax (proper formatting)
- ✅ Badge URLs and shields are current

### Step 6: Summary & Report

Generate comprehensive update summary showing:

- What sections were modified
- What metadata was discovered and used
- Any detected issues or recommendations
- Before/after comparison of key sections

## Concrete Examples

### Example 1: Node.js Project Update

**Project Type Detected**: Node.js / TypeScript
**Files Scanned**: `package.json` (v2.1.0), `README.md` (old, v1.5.0)

**Before:**
```markdown
# my-awesome-cli

Command-line tool for development tasks.

## Installation

```bash
npm install -g my-awesome-cli
```

## Usage

```bash
my-awesome-cli help
```

## Features

- Task automation
```

**After:**
```markdown
# my-awesome-cli

[![npm version](https://img.shields.io/npm/v/my-awesome-cli.svg)](https://npmjs.org/package/my-awesome-cli)
[![npm downloads](https://img.shields.io/npm/dm/my-awesome-cli.svg)](https://npmjs.org/package/my-awesome-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/user/my-awesome-cli/blob/main/LICENSE)

Advanced command-line tool for automating development workflows with TypeScript support and interactive configuration.

## Features

- **Task Automation**: Easily define and run complex development tasks
- **TypeScript Support**: First-class TypeScript configuration and plugins
- **Interactive Config**: Interactive setup wizard for project configuration
- **Watch Mode**: Automatic task re-run on file changes
- **Plugin System**: Extend functionality with custom plugins

## Installation

### Prerequisites

- Node.js 16.0 or higher
- npm 7.0 or higher (or yarn/pnpm)

### Quick Start

```bash
# Install globally
npm install -g my-awesome-cli

# Or use npx (no installation required)
npx my-awesome-cli --version
```

## Usage

### Basic Commands

```bash
# Show help
my-awesome-cli help

# Initialize project
my-awesome-cli init

# Run a task
my-awesome-cli run build

# Watch mode
my-awesome-cli run build --watch
```

### Examples

**Initialize a new project:**
```bash
my-awesome-cli init
# Follow the interactive prompts to set up your project
```

**Create a custom task:**
```bash
# Edit .myawesomerc.json
{
  "tasks": {
    "build": {
      "commands": ["npm run compile", "npm run bundle"]
    }
  }
}
```

**Run with TypeScript:**
```bash
my-awesome-cli run build --ts
```

## Configuration

### Environment Variables

- `MY_AWESOME_CONFIG`: Path to custom config file (default: `.myawesomerc.json`)
- `MY_AWESOME_LOG_LEVEL`: Logging level (debug, info, warn, error) (default: info)

### Config File Format

Create `.myawesomerc.json` in your project root:

```json
{
  "version": "1.0",
  "tasks": {
    "build": {
      "commands": ["npm run compile"]
    },
    "test": {
      "commands": ["npm test"]
    }
  },
  "plugins": ["@my-awesome-cli/typescript"]
}
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
```

**Update Summary:**
```
═══════════════════════════════════════════════════════════
README UPDATE SUMMARY
═══════════════════════════════════════════════════════════

Project: my-awesome-cli
Type: Node.js / TypeScript
Status: ✅ SUCCESSFULLY UPDATED

───────────────────────────────────────────────────────────
CHANGES MADE
───────────────────────────────────────────────────────────

✅ Version Updated
   Old: v1.5.0 → New: v2.1.0
   Source: package.json

✅ Badges Added
   - npm version badge
   - npm downloads badge  
   - MIT license badge

✅ Features Section Expanded
   Old: 2 features → New: 5 features with descriptions

✅ Installation Section Updated
   - Added prerequisites section
   - Included npx alternative
   - Clearer quick start

✅ Usage Section Enhanced
   - Reorganized commands
   - Added watch mode flag
   - TypeScript examples

✅ Examples Section Created
   - Project initialization example
   - Custom task configuration
   - TypeScript usage example

✅ Configuration Section Added
   - Environment variables documented
   - Config file format with example
   - Plugin system noted

✅ Contributing & License Links Updated
   - Verified files exist
   - Links are current

───────────────────────────────────────────────────────────
METADATA EXTRACTED
───────────────────────────────────────────────────────────

Name: my-awesome-cli
Version: 2.1.0
Description: Advanced command-line tool for automating development workflows...
Main Dependencies: 
  - commander@^11.0.0
  - chalk@^5.0.0
  - ora@^7.0.0

Dev Dependencies: @types/node, typescript, jest

Entry Point: bin/cli.ts

Supported Node Versions: >=16.0.0

═══════════════════════════════════════════════════════════
```

### Example 2: Python Project Update

**Project Type Detected**: Python / PyPI Package
**Files Scanned**: `pyproject.toml` (v0.3.0), `README.md` (v0.2.0)

**Before:**
```markdown
# my-python-lib

Python library for data processing.

## Installation

pip install my-python-lib

## Usage

from my_python_lib import process
result = process(data)
```

**After:**
```markdown
# my-python-lib

[![PyPI version](https://img.shields.io/pypi/v/my-python-lib)](https://pypi.org/project/my-python-lib/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

High-performance data processing library for machine learning and data science workflows.

## Features

- **Fast Processing**: Optimized algorithms for large datasets
- **Type Hints**: Full type annotations for better IDE support
- **Async Support**: Built-in async/await support for concurrent operations
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Pandas Compatible**: Works seamlessly with pandas DataFrames

## Installation

### Requirements

- Python 3.8 or higher
- pip or conda

### From PyPI

```bash
pip install my-python-lib
```

### From Conda

```bash
conda install -c conda-forge my-python-lib
```

### Development Installation

```bash
git clone https://github.com/user/my-python-lib.git
cd my-python-lib
pip install -e ".[dev]"
```

## Quick Start

```python
from my_python_lib import DataProcessor

# Initialize processor
processor = DataProcessor(batch_size=1000)

# Process data
results = processor.transform(data, normalize=True)

# Get statistics
stats = processor.get_stats()
print(f"Processed {stats['count']} items in {stats['time']:.2f}s")
```

## Usage Examples

### Basic Data Processing

```python
import pandas as pd
from my_python_lib import DataProcessor

# Load data
df = pd.read_csv('data.csv')

# Create processor
processor = DataProcessor()

# Process
result = processor.fit_transform(df)
```

### Async Processing

```python
import asyncio
from my_python_lib import AsyncDataProcessor

async def process_large_dataset():
    processor = AsyncDataProcessor(workers=4)
    results = await processor.transform(large_data)
    return results

# Run async processor
asyncio.run(process_large_dataset())
```

### Custom Transformations

```python
from my_python_lib import DataProcessor, transforms

processor = DataProcessor(
    transforms=[
        transforms.Normalize(),
        transforms.Impute(strategy='mean'),
        transforms.FeatureScale()
    ]
)
```

## Configuration

### Environment Variables

- `MY_PYTHON_LIB_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR) (default: INFO)
- `MY_PYTHON_LIB_WORKERS`: Number of worker threads (default: CPU count)
- `MY_PYTHON_LIB_CACHE_DIR`: Directory for caching processed data (default: ~/.cache/my-python-lib)

### Configuration via Code

```python
from my_python_lib import config

config.set_log_level('DEBUG')
config.set_workers(8)
config.enable_caching(cache_dir='/tmp/cache')
```

## API Reference

See [API_REFERENCE.md](docs/API_REFERENCE.md) for complete API documentation.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Licensed under Apache License 2.0 - see [LICENSE](LICENSE) for details.
```

**Update Summary:**
```
═══════════════════════════════════════════════════════════
README UPDATE SUMMARY
═══════════════════════════════════════════════════════════

Project: my-python-lib
Type: Python / PyPI Package
Status: ✅ SUCCESSFULLY UPDATED

───────────────────────────────────────────────────────────
CHANGES MADE
───────────────────────────────────────────────────────────

✅ Version Updated
   Old: v0.2.0 → New: v0.3.0
   Source: pyproject.toml

✅ Badges Added
   - PyPI version badge
   - Python 3.8+ requirement badge
   - Apache 2.0 license badge

✅ Features Section Expanded
   Old: 1 feature → New: 5 features with descriptions

✅ Installation Section Restructured
   - Added requirements section
   - PyPI installation method
   - Conda installation method  
   - Development installation steps

✅ Quick Start Section Added
   - Simple example code
   - Realistic use case

✅ Usage Examples Section Expanded
   - Basic data processing example
   - Async processing example
   - Custom transformations example

✅ Configuration Section Added
   - Environment variables documented
   - Code-based configuration examples

✅ API Reference Link Added
   - Points to docs/API_REFERENCE.md

───────────────────────────────────────────────────────────
METADATA EXTRACTED
───────────────────────────────────────────────────────────

Name: my-python-lib
Version: 0.3.0
Description: High-performance data processing library for machine learning...
Python Version: >=3.8
License: Apache-2.0

Main Dependencies:
  - numpy>=1.20.0
  - pandas>=1.3.0

Dev Dependencies:
  - pytest
  - black
  - mypy
  - sphinx

PyPI URL: https://pypi.org/project/my-python-lib/

═══════════════════════════════════════════════════════════
```

## Output Format Example

When the skill completes an update, it should provide a summary of changes:

### README Update Summary

- ✅ **Installation**: Updated installation section with new Python requirements
- ✅ **Usage**: Added async processing and custom configuration examples
- ✅ **Version**: Updated from v0.2.0 to v0.3.0 to match `pyproject.toml`
- ✅ **Features**: Expanded from 1 to 5 features with detailed descriptions
- ✅ **Badges**: Added PyPI, Python version, and license badges
- ✅ **Configuration**: Added environment variables and code-based setup guide

## References

- [README Template](references/readme_template.md) - Standard layout for project documentation.
- [Project Discovery Patterns](references/discovery_patterns.md) - How to find project info across different languages.
