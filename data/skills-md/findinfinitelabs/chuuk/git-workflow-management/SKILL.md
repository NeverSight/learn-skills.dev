---
name: git-workflow-management
description: Automate frequent Git operations including adding changes, committing with meaningful messages, and pushing to remote repositories. Use when you need to save progress, commit code changes, or maintain regular version control workflow with proper commit practices.
---

# Git Workflow Management

## Overview

A comprehensive skill for automating and streamlining Git version control operations, focusing on frequent commits with meaningful messages, proper staging practices, and efficient push workflows. Designed to maintain clean commit history and regular backup of development progress.

## Capabilities

- **Smart Change Detection**: Automatically identify modified, added, and deleted files
- **Intelligent Commit Messaging**: Generate meaningful commit messages based on changes
- **Selective Staging**: Stage specific files or file types based on context
- **Branch Management**: Handle branch creation, switching, and merging workflows
- **Push Automation**: Automated pushing with conflict detection and resolution
- **Commit History Cleanup**: Squashing and organizing commits for clean history

## Core Components

### 1. Automated Change Detection and Staging

```bash
#!/bin/bash
# Smart staging script for different file types

detect_changes() {
    echo "🔍 Detecting changes..."
    
    # Get status of all files
    git status --porcelain | while read -r line; do
        status="${line:0:2}"
        file="${line:3}"
        
        case "$status" in
            "M "|" M") echo "Modified: $file" ;;
            "A "|" A") echo "Added: $file" ;;
            "D "|" D") echo "Deleted: $file" ;;
            "??") echo "Untracked: $file" ;;
            "R ") echo "Renamed: $file" ;;
        esac
    done
}

stage_by_type() {
    local file_pattern="$1"
    local description="$2"
    
    if git diff --name-only --cached | grep -q "$file_pattern"; then
        echo "✅ $description files already staged"
        return 0
    fi
    
    if git diff --name-only | grep -q "$file_pattern"; then
        echo "📁 Staging $description files..."
        git add $(git diff --name-only | grep "$file_pattern")
        return 0
    fi
    
    echo "ℹ️  No $description files to stage"
    return 1
}

smart_staging() {
    echo "🎯 Smart staging workflow..."
    
    # Stage different file types with appropriate grouping
    stage_by_type "\.py$" "Python"
    stage_by_type "\.md$" "Markdown"
    stage_by_type "\.js$\|\.ts$\|\.jsx$\|\.tsx$" "JavaScript/TypeScript"
    stage_by_type "\.css$\|\.scss$\|\.sass$" "Stylesheet"
    stage_by_type "\.html$\|\.htm$" "HTML"
    stage_by_type "\.json$\|\.yml$\|\.yaml$" "Configuration"
    stage_by_type "\.sql$" "Database"
    stage_by_type "requirements\.txt\|package\.json\|Pipfile" "Dependencies"
    
    # Show current staging status
    echo "📋 Currently staged files:"
    git diff --cached --name-only | sed 's/^/  ✓ /'
}
```

### 2. Intelligent Commit Message Generation

```bash
generate_commit_message() {
    local commit_type="$1"
    local scope="$2"
    local description="$3"
    
    # Get staged files for context
    local staged_files=$(git diff --cached --name-only)
    local file_count=$(echo "$staged_files" | wc -l | xargs)
    
    # Analyze changes for automatic message generation
    if [ -z "$description" ]; then
        description=$(analyze_changes_for_message)
    fi
    
    # Generate conventional commit message
    if [ -n "$scope" ]; then
        echo "${commit_type}(${scope}): ${description}"
    else
        echo "${commit_type}: ${description}"
    fi
}

analyze_changes_for_message() {
    local staged_files=$(git diff --cached --name-only)
    local added_files=$(git diff --cached --name-status | grep '^A' | wc -l | xargs)
    local modified_files=$(git diff --cached --name-status | grep '^M' | wc -l | xargs)
    local deleted_files=$(git diff --cached --name-status | grep '^D' | wc -l | xargs)
    
    # Determine primary change type
    if [ "$added_files" -gt 0 ] && [ "$modified_files" -eq 0 ] && [ "$deleted_files" -eq 0 ]; then
        if echo "$staged_files" | grep -q "\.md$"; then
            echo "add documentation and skill definitions"
        elif echo "$staged_files" | grep -q "\.py$"; then
            echo "add new Python modules and functionality"
        else
            echo "add new files and resources"
        fi
    elif [ "$modified_files" -gt 0 ] && [ "$added_files" -eq 0 ] && [ "$deleted_files" -eq 0 ]; then
        if echo "$staged_files" | grep -q "SKILL\.md"; then
            echo "update Claude Skills definitions and capabilities"
        elif echo "$staged_files" | grep -q "\.py$"; then
            echo "improve Python code and functionality"
        elif echo "$staged_files" | grep -q "\.md$"; then
            echo "update documentation and guides"
        else
            echo "update existing functionality"
        fi
    elif [ "$deleted_files" -gt 0 ]; then
        echo "remove obsolete files and cleanup codebase"
    else
        echo "update multiple components and files"
    fi
}

commit_with_message() {
    local message_type="${1:-feat}"
    local scope="$2"
    local custom_message="$3"
    
    # Ensure we have staged changes
    if [ -z "$(git diff --cached --name-only)" ]; then
        echo "❌ No staged changes to commit"
        return 1
    fi
    
    # Generate or use provided commit message
    local commit_message
    if [ -n "$custom_message" ]; then
        commit_message="$custom_message"
    else
        commit_message=$(generate_commit_message "$message_type" "$scope")
    fi
    
    echo "💬 Commit message: $commit_message"
    
    # Show what will be committed
    echo "📝 Files to commit:"
    git diff --cached --name-only | sed 's/^/  • /'
    
    # Create commit
    git commit -m "$commit_message"
    
    if [ $? -eq 0 ]; then
        echo "✅ Commit created successfully"
        return 0
    else
        echo "❌ Commit failed"
        return 1
    fi
}
```

### 3. Comprehensive Git Workflow Functions

```python
import subprocess
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class GitWorkflowManager:
    def __init__(self, repository_path: str = "."):
        """Initialize Git workflow manager."""
        self.repo_path = repository_path
        self.ensure_git_repository()
    
    def ensure_git_repository(self):
        """Ensure we're in a Git repository."""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], 
                         cwd=self.repo_path, 
                         capture_output=True, 
                         check=True)
        except subprocess.CalledProcessError:
            raise RuntimeError(f"Not a Git repository: {self.repo_path}")
    
    def get_status(self) -> Dict[str, List[str]]:
        """Get comprehensive repository status."""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.repo_path, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            status = {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': [],
                'renamed': [],
                'staged': []
            }
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                status_code = line[:2]
                filename = line[3:]
                
                # Check staging area (first character)
                if status_code[0] in ['M', 'A', 'D', 'R', 'C']:
                    status['staged'].append(filename)
                
                # Check working directory (second character)
                if status_code[1] == 'M':
                    status['modified'].append(filename)
                elif status_code[1] == 'D':
                    status['deleted'].append(filename)
                elif status_code == '??':
                    status['untracked'].append(filename)
                elif status_code[0] == 'R':
                    status['renamed'].append(filename)
                elif status_code[0] == 'A':
                    status['added'].append(filename)
            
            return status
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get Git status: {e}")
    
    def stage_files(self, patterns: List[str] = None, all_files: bool = False) -> bool:
        """Stage files based on patterns or all files."""
        try:
            if all_files:
                subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
                print("✅ All files staged")
                return True
            
            if patterns:
                for pattern in patterns:
                    subprocess.run(['git', 'add', pattern], cwd=self.repo_path, check=True)
                print(f"✅ Files matching {patterns} staged")
                return True
            
            # Interactive staging
            return self._interactive_staging()
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to stage files: {e}")
            return False
    
    def _interactive_staging(self) -> bool:
        """Interactive file staging based on file types."""
        status = self.get_status()
        
        if not any(status.values()):
            print("ℹ️  No changes to stage")
            return False
        
        # Group files by type for smart staging
        file_groups = {
            'Python files': [f for f in status['modified'] + status['untracked'] if f.endswith('.py')],
            'Documentation': [f for f in status['modified'] + status['untracked'] if f.endswith(('.md', '.txt', '.rst'))],
            'Configuration': [f for f in status['modified'] + status['untracked'] if f.endswith(('.json', '.yml', '.yaml', '.toml'))],
            'Web files': [f for f in status['modified'] + status['untracked'] if f.endswith(('.html', '.css', '.js', '.ts'))],
            'Data files': [f for f in status['modified'] + status['untracked'] if f.endswith(('.csv', '.tsv', '.sql'))],
            'Other files': []
        }
        
        # Add remaining files to 'Other files'
        all_categorized = set()
        for files in file_groups.values():
            all_categorized.update(files)
        
        all_changes = set(status['modified'] + status['untracked'])
        file_groups['Other files'] = list(all_changes - all_categorized)
        
        # Stage files by groups
        staged_any = False
        for group_name, files in file_groups.items():
            if files:
                print(f"📁 {group_name}: {len(files)} files")
                for file in files:
                    print(f"  • {file}")
                
                try:
                    subprocess.run(['git', 'add'] + files, cwd=self.repo_path, check=True)
                    print(f"✅ Staged {group_name}")
                    staged_any = True
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to stage {group_name}")
        
        return staged_any
    
    def commit_changes(self, message: str = None, commit_type: str = "feat", 
                      scope: str = None, auto_message: bool = True) -> bool:
        """Create a commit with proper message formatting."""
        
        # Check for staged changes
        try:
            result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                                  cwd=self.repo_path, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            if not result.stdout.strip():
                print("❌ No staged changes to commit")
                return False
            
        except subprocess.CalledProcessError:
            print("❌ Failed to check staged changes")
            return False
        
        # Generate commit message if not provided
        if not message and auto_message:
            message = self._generate_auto_commit_message(commit_type, scope)
        elif not message:
            message = f"{commit_type}: update files and functionality"
        
        # Create commit
        try:
            subprocess.run(['git', 'commit', '-m', message], 
                         cwd=self.repo_path, 
                         check=True)
            print(f"✅ Committed: {message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e}")
            return False
    
    def _generate_auto_commit_message(self, commit_type: str, scope: str = None) -> str:
        """Generate automatic commit message based on changes."""
        try:
            # Get staged files
            result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                                  cwd=self.repo_path, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            staged_files = result.stdout.strip().split('\n')
            
            # Analyze file types and changes
            file_analysis = {
                'skills': len([f for f in staged_files if 'skill' in f.lower() or f.endswith('SKILL.md')]),
                'python': len([f for f in staged_files if f.endswith('.py')]),
                'docs': len([f for f in staged_files if f.endswith(('.md', '.txt', '.rst'))]),
                'config': len([f for f in staged_files if f.endswith(('.json', '.yml', '.yaml', '.toml'))]),
                'web': len([f for f in staged_files if f.endswith(('.html', '.css', '.js', '.ts'))]),
                'data': len([f for f in staged_files if f.endswith(('.csv', '.tsv', '.sql'))])
            }
            
            # Generate description based on primary change type
            if file_analysis['skills'] > 0:
                description = "update Claude Skills definitions and capabilities"
            elif file_analysis['python'] > file_analysis['docs']:
                description = "improve Python functionality and code structure"
            elif file_analysis['docs'] > 0:
                description = "update documentation and project guides"
            elif file_analysis['config'] > 0:
                description = "update configuration and settings"
            elif file_analysis['web'] > 0:
                description = "improve web interface and styling"
            elif file_analysis['data'] > 0:
                description = "update data files and database structure"
            else:
                description = "update project files and resources"
            
            # Format commit message
            if scope:
                return f"{commit_type}({scope}): {description}"
            else:
                return f"{commit_type}: {description}"
                
        except subprocess.CalledProcessError:
            return f"{commit_type}: update files and functionality"
    
    def push_changes(self, remote: str = "origin", branch: str = None, 
                    force: bool = False) -> bool:
        """Push changes to remote repository."""
        try:
            # Get current branch if not specified
            if not branch:
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      cwd=self.repo_path, 
                                      capture_output=True, 
                                      text=True, 
                                      check=True)
                branch = result.stdout.strip()
            
            # Check if there are commits to push
            try:
                subprocess.run(['git', 'diff', f'{remote}/{branch}', 'HEAD', '--quiet'], 
                             cwd=self.repo_path, 
                             check=True)
                print("ℹ️  No new commits to push")
                return True
            except subprocess.CalledProcessError:
                pass  # There are differences, proceed with push
            
            # Push changes
            push_command = ['git', 'push', remote, branch]
            if force:
                push_command.append('--force-with-lease')
            
            subprocess.run(push_command, cwd=self.repo_path, check=True)
            print(f"✅ Pushed to {remote}/{branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Push failed: {e}")
            print("💡 Try: git pull --rebase before pushing")
            return False
    
    def quick_commit_and_push(self, message: str = None, commit_type: str = "feat", 
                             scope: str = None, stage_all: bool = True) -> bool:
        """Complete workflow: stage, commit, and push in one operation."""
        print("🚀 Starting quick commit and push workflow...")
        
        # Stage files
        if stage_all:
            if not self.stage_files(all_files=True):
                return False
        else:
            if not self.stage_files():
                return False
        
        # Commit changes
        if not self.commit_changes(message=message, commit_type=commit_type, scope=scope):
            return False
        
        # Push changes
        if not self.push_changes():
            return False
        
        print("🎉 Complete! Changes staged, committed, and pushed successfully.")
        return True
    
    def sync_with_remote(self, remote: str = "origin", branch: str = None) -> bool:
        """Sync local branch with remote (pull with rebase)."""
        try:
            if not branch:
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      cwd=self.repo_path, 
                                      capture_output=True, 
                                      text=True, 
                                      check=True)
                branch = result.stdout.strip()
            
            print(f"🔄 Syncing with {remote}/{branch}...")
            subprocess.run(['git', 'pull', '--rebase', remote, branch], 
                         cwd=self.repo_path, 
                         check=True)
            print("✅ Successfully synced with remote")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Sync failed: {e}")
            return False
```

### 4. Command-Line Interface and Quick Commands

```python
import argparse
import sys

def create_cli():
    """Create command-line interface for Git workflow management."""
    
    parser = argparse.ArgumentParser(description="Git Workflow Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Quick commit command
    quick_parser = subparsers.add_parser('quick', help='Quick stage, commit, and push')
    quick_parser.add_argument('-m', '--message', help='Custom commit message')
    quick_parser.add_argument('-t', '--type', default='feat', 
                            choices=['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'],
                            help='Conventional commit type')
    quick_parser.add_argument('-s', '--scope', help='Commit scope')
    quick_parser.add_argument('--no-stage-all', action='store_true', help='Use interactive staging')
    
    # Stage command
    stage_parser = subparsers.add_parser('stage', help='Stage files')
    stage_parser.add_argument('patterns', nargs='*', help='File patterns to stage')
    stage_parser.add_argument('-a', '--all', action='store_true', help='Stage all files')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', help='Commit message')
    commit_parser.add_argument('-t', '--type', default='feat', help='Commit type')
    commit_parser.add_argument('-s', '--scope', help='Commit scope')
    
    # Push command
    push_parser = subparsers.add_parser('push', help='Push changes to remote')
    push_parser.add_argument('-r', '--remote', default='origin', help='Remote name')
    push_parser.add_argument('-b', '--branch', help='Branch name')
    push_parser.add_argument('-f', '--force', action='store_true', help='Force push with lease')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show repository status')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync with remote repository')
    sync_parser.add_argument('-r', '--remote', default='origin', help='Remote name')
    sync_parser.add_argument('-b', '--branch', help='Branch name')
    
    return parser

def main():
    """Main CLI entry point."""
    parser = create_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize Git workflow manager
    try:
        git_manager = GitWorkflowManager()
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Execute commands
    try:
        if args.command == 'quick':
            success = git_manager.quick_commit_and_push(
                message=args.message,
                commit_type=args.type,
                scope=args.scope,
                stage_all=not args.no_stage_all
            )
        elif args.command == 'stage':
            success = git_manager.stage_files(
                patterns=args.patterns,
                all_files=args.all
            )
        elif args.command == 'commit':
            success = git_manager.commit_changes(
                message=args.message,
                commit_type=args.type,
                scope=args.scope
            )
        elif args.command == 'push':
            success = git_manager.push_changes(
                remote=args.remote,
                branch=args.branch,
                force=args.force
            )
        elif args.command == 'status':
            status = git_manager.get_status()
            print_status(status)
            success = True
        elif args.command == 'sync':
            success = git_manager.sync_with_remote(
                remote=args.remote,
                branch=args.branch
            )
        else:
            parser.print_help()
            success = False
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def print_status(status):
    """Print formatted repository status."""
    print("📊 Repository Status:")
    
    if status['staged']:
        print("✅ Staged files:")
        for file in status['staged']:
            print(f"  • {file}")
    
    if status['modified']:
        print("📝 Modified files:")
        for file in status['modified']:
            print(f"  • {file}")
    
    if status['untracked']:
        print("❓ Untracked files:")
        for file in status['untracked']:
            print(f"  • {file}")
    
    if status['deleted']:
        print("🗑️  Deleted files:")
        for file in status['deleted']:
            print(f"  • {file}")
    
    if not any(status.values()):
        print("✨ Working directory clean")

if __name__ == "__main__":
    main()
```

## Usage Examples

### 1. Quick Workflow (Most Common)

```bash
# Stage all changes, commit with auto-generated message, and push
python git_workflow.py quick

# Quick commit with custom message
python git_workflow.py quick -m "Add new Chuukese language processing features"

# Quick commit with specific type and scope
python git_workflow.py quick -t feat -s chuukese -m "Add accent normalization functionality"
```

### 2. Step-by-Step Workflow

```bash
# Check status
python git_workflow.py status

# Stage specific files
python git_workflow.py stage *.py

# Stage all files
python git_workflow.py stage -a

# Commit with auto-generated message
python git_workflow.py commit -t feat -s skills

# Push to remote
python git_workflow.py push
```

### 3. Sync with Remote

```bash
# Sync with remote repository
python git_workflow.py sync

# Sync specific remote and branch
python git_workflow.py sync -r upstream -b main
```

## Best Practices

### 1. Commit Message Conventions

- **feat**: New features or functionality
- **fix**: Bug fixes
- **docs**: Documentation changes
- **style**: Code style/formatting changes
- **refactor**: Code refactoring without feature changes
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates

### 2. Frequent Commit Guidelines

- Commit after completing logical units of work
- Keep commits focused on single concerns
- Use descriptive commit messages
- Commit before switching contexts or taking breaks
- Push regularly to backup work

### 3. File Organization

- Group related changes in single commits
- Separate feature development from documentation updates
- Commit configuration changes separately from code changes
- Keep dependency updates in dedicated commits

### 4. Workflow Automation

- Use quick commands for routine work
- Set up aliases for common operations
- Automate repetitive staging patterns
- Implement pre-commit hooks for quality checks

## Integration with Development Tools

### 1. VS Code Integration

```json
// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Quick Git Commit",
            "type": "shell",
            "command": "python",
            "args": ["git_workflow.py", "quick"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Git Status",
            "type": "shell",
            "command": "python",
            "args": ["git_workflow.py", "status"],
            "group": "build"
        }
    ]
}
```

### 2. Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gq='python git_workflow.py quick'
alias gs='python git_workflow.py status'
alias gc='python git_workflow.py commit'
alias gp='python git_workflow.py push'
alias gsync='python git_workflow.py sync'
```

## Dependencies

- `subprocess`: Process execution for Git commands
- `argparse`: Command-line interface
- `os`: Operating system interface
- `datetime`: Timestamp management

## Validation Criteria

A successful implementation should:

- ✅ Automatically detect and stage relevant file changes
- ✅ Generate meaningful commit messages based on content
- ✅ Handle Git conflicts and errors gracefully
- ✅ Support both automated and interactive workflows
- ✅ Maintain clean commit history with conventional commits
- ✅ Provide clear status feedback throughout operations
- ✅ Support multiple remotes and branches
- ✅ Include comprehensive error handling and recovery
