---
name: anthropic-cybersecurity-skills
description: Use 754 structured cybersecurity skills mapped to MITRE ATT&CK, NIST CSF, ATLAS, D3FEND, and NIST AI RMF for AI-driven security operations
triggers:
  - "help me investigate this security incident"
  - "analyze this malware sample"
  - "perform memory forensics on this dump"
  - "hunt for threats in our environment"
  - "check cloud security posture"
  - "map this attack to MITRE ATT&CK"
  - "what security skills are available"
  - "guide me through incident response"
---

# anthropic-cybersecurity-skills

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## Overview

The Anthropic Cybersecurity Skills library provides 754 production-grade cybersecurity skills spanning 26 security domains. Each skill is structured following the agentskills.io standard and mapped to five industry frameworks: MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, MITRE D3FEND, and NIST AI RMF. This enables AI agents to perform security operations with expert-level guidance.

## Installation

```bash
# Option 1: Using npx (recommended)
npx skills add mukul975/Anthropic-Cybersecurity-Skills

# Option 2: Git clone
git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git
cd Anthropic-Cybersecurity-Skills

# Option 3: Add as submodule
git submodule add https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git skills/cybersecurity
```

## Directory Structure

```
skills/
├── {skill-name}/
│   ├── SKILL.md              # Skill definition with YAML frontmatter
│   ├── references/
│   │   ├── standards.md      # Framework mappings
│   │   └── workflows.md      # Technical procedures
│   ├── scripts/
│   │   └── *.py              # Helper scripts
│   └── assets/
│       └── *.md              # Templates and checklists
```

## Discovering Skills

### By Domain

Skills are organized into 26 domains. List all domains:

```python
import os
import yaml

def list_domains():
    domains = {}
    for skill_dir in os.listdir('skills'):
        skill_path = f'skills/{skill_dir}/SKILL.md'
        if os.path.exists(skill_path):
            with open(skill_path, 'r') as f:
                content = f.read()
                # Extract YAML frontmatter
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    frontmatter = yaml.safe_load(content[3:yaml_end])
                    domain = frontmatter.get('domain', 'unknown')
                    subdomain = frontmatter.get('subdomain', 'general')
                    
                    if domain not in domains:
                        domains[domain] = {}
                    if subdomain not in domains[domain]:
                        domains[domain][subdomain] = []
                    domains[domain][subdomain].append(frontmatter['name'])
    
    return domains

# Usage
domains = list_domains()
for domain, subdomains in domains.items():
    print(f"\n{domain.upper()}")
    for subdomain, skills in subdomains.items():
        print(f"  {subdomain}: {len(skills)} skills")
```

### By Framework Mapping

Find skills mapped to specific ATT&CK techniques:

```python
def find_by_attack_technique(technique_id):
    """Find skills mapped to a specific ATT&CK technique"""
    matching_skills = []
    
    for skill_dir in os.listdir('skills'):
        skill_path = f'skills/{skill_dir}/SKILL.md'
        if os.path.exists(skill_path):
            with open(skill_path, 'r') as f:
                content = f.read()
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    frontmatter = yaml.safe_load(content[3:yaml_end])
                    
                    # Check ATT&CK mappings in references
                    refs_path = f'skills/{skill_dir}/references/standards.md'
                    if os.path.exists(refs_path):
                        with open(refs_path, 'r') as ref_file:
                            if technique_id in ref_file.read():
                                matching_skills.append({
                                    'name': frontmatter['name'],
                                    'description': frontmatter['description'],
                                    'path': skill_path
                                })
    
    return matching_skills

# Usage
skills = find_by_attack_technique('T1003')  # Credential Dumping
for skill in skills:
    print(f"{skill['name']}: {skill['description']}")
```

### By Tags

Search skills by tags:

```python
def search_by_tags(search_tags):
    """Find skills matching any of the provided tags"""
    results = []
    
    for skill_dir in os.listdir('skills'):
        skill_path = f'skills/{skill_dir}/SKILL.md'
        if os.path.exists(skill_path):
            with open(skill_path, 'r') as f:
                content = f.read()
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    frontmatter = yaml.safe_load(content[3:yaml_end])
                    
                    skill_tags = frontmatter.get('tags', [])
                    if any(tag in skill_tags for tag in search_tags):
                        results.append(frontmatter)
    
    return results

# Usage
malware_skills = search_by_tags(['malware-analysis', 'reverse-engineering'])
for skill in malware_skills:
    print(f"{skill['name']}: {', '.join(skill['tags'])}")
```

## Loading and Executing Skills

### Progressive Loading Pattern

Load only frontmatter first (low token cost), then full content when needed:

```python
class SkillLoader:
    def __init__(self, skills_dir='skills'):
        self.skills_dir = skills_dir
    
    def scan_all_frontmatter(self):
        """Scan all skill frontmatter (~30 tokens each)"""
        skills_index = []
        
        for skill_dir in os.listdir(self.skills_dir):
            skill_path = f'{self.skills_dir}/{skill_dir}/SKILL.md'
            if os.path.exists(skill_path):
                with open(skill_path, 'r') as f:
                    content = f.read()
                    if content.startswith('---'):
                        yaml_end = content.find('---', 3)
                        frontmatter = yaml.safe_load(content[3:yaml_end])
                        frontmatter['path'] = skill_path
                        skills_index.append(frontmatter)
        
        return skills_index
    
    def load_full_skill(self, skill_name):
        """Load complete skill content (~500-2000 tokens)"""
        skill_path = f'{self.skills_dir}/{skill_name}/SKILL.md'
        
        with open(skill_path, 'r') as f:
            content = f.read()
        
        # Parse frontmatter and body
        if content.startswith('---'):
            yaml_end = content.find('---', 3)
            frontmatter = yaml.safe_load(content[3:yaml_end])
            body = content[yaml_end + 3:].strip()
            
            return {
                'metadata': frontmatter,
                'content': body,
                'references': self._load_references(skill_name),
                'scripts': self._load_scripts(skill_name)
            }
    
    def _load_references(self, skill_name):
        """Load framework mappings and workflows"""
        refs = {}
        refs_dir = f'{self.skills_dir}/{skill_name}/references'
        
        if os.path.exists(refs_dir):
            for ref_file in os.listdir(refs_dir):
                with open(f'{refs_dir}/{ref_file}', 'r') as f:
                    refs[ref_file.replace('.md', '')] = f.read()
        
        return refs
    
    def _load_scripts(self, skill_name):
        """Load helper scripts"""
        scripts = {}
        scripts_dir = f'{self.skills_dir}/{skill_name}/scripts'
        
        if os.path.exists(scripts_dir):
            for script_file in os.listdir(scripts_dir):
                with open(f'{scripts_dir}/{script_file}', 'r') as f:
                    scripts[script_file] = f.read()
        
        return scripts

# Usage
loader = SkillLoader()

# Step 1: Scan all skills (lightweight)
all_skills = loader.scan_all_frontmatter()
print(f"Found {len(all_skills)} skills")

# Step 2: Find relevant skills
memory_forensics = [s for s in all_skills if 'memory-analysis' in s.get('tags', [])]

# Step 3: Load top matches fully
for skill in memory_forensics[:3]:
    full_skill = loader.load_full_skill(skill['name'])
    print(f"\n{skill['name']}")
    print(f"Content length: {len(full_skill['content'])} chars")
```

## Common Usage Patterns

### Incident Response Workflow

```python
def incident_response_guide(incident_type):
    """Get relevant IR skills for incident type"""
    loader = SkillLoader()
    all_skills = loader.scan_all_frontmatter()
    
    # Map incident types to skill domains
    incident_mappings = {
        'ransomware': ['malware-analysis', 'incident-response', 'forensics'],
        'data_breach': ['threat-hunting', 'forensics', 'cloud-security'],
        'phishing': ['email-security', 'threat-intelligence', 'endpoint-security'],
        'insider_threat': ['behavior-analytics', 'iam', 'forensics']
    }
    
    relevant_tags = incident_mappings.get(incident_type, [])
    relevant_skills = [
        s for s in all_skills 
        if any(tag in s.get('tags', []) for tag in relevant_tags)
    ]
    
    # Prioritize by subdomain
    prioritized = sorted(
        relevant_skills,
        key=lambda s: (
            s.get('subdomain') == 'incident-response',
            len(set(s.get('tags', [])) & set(relevant_tags))
        ),
        reverse=True
    )
    
    return prioritized[:5]

# Usage
ransomware_skills = incident_response_guide('ransomware')
for skill in ransomware_skills:
    print(f"- {skill['name']}: {skill['description']}")
```

### ATT&CK Technique Coverage

```python
def check_attack_coverage(technique_id):
    """Check which skills cover a specific ATT&CK technique"""
    loader = SkillLoader()
    
    coverage = []
    for skill_dir in os.listdir('skills'):
        refs_path = f'skills/{skill_dir}/references/standards.md'
        if os.path.exists(refs_path):
            with open(refs_path, 'r') as f:
                content = f.read()
                if technique_id in content:
                    skill = loader.load_full_skill(skill_dir)
                    coverage.append({
                        'name': skill['metadata']['name'],
                        'description': skill['metadata']['description'],
                        'domain': skill['metadata']['subdomain']
                    })
    
    return coverage

# Usage
t1003_coverage = check_attack_coverage('T1003')  # Credential Dumping
print(f"Skills covering T1003: {len(t1003_coverage)}")
for skill in t1003_coverage:
    print(f"  {skill['domain']}: {skill['name']}")
```

### Multi-Framework Compliance Check

```python
def compliance_mapper(skill_name):
    """Show all framework mappings for a skill"""
    loader = SkillLoader()
    skill = loader.load_full_skill(skill_name)
    
    frameworks = {
        'MITRE ATT&CK': skill['metadata'].get('attack_techniques', []),
        'NIST CSF 2.0': skill['metadata'].get('nist_csf', []),
        'MITRE ATLAS': skill['metadata'].get('atlas_techniques', []),
        'MITRE D3FEND': skill['metadata'].get('d3fend_techniques', []),
        'NIST AI RMF': skill['metadata'].get('nist_ai_rmf', [])
    }
    
    print(f"\nFramework mappings for: {skill_name}\n")
    for framework, mappings in frameworks.items():
        if mappings:
            print(f"{framework}:")
            for mapping in mappings:
                print(f"  - {mapping}")

# Usage
compliance_mapper('performing-memory-forensics-with-volatility3')
```

## Working with Skill Scripts

Many skills include helper scripts in `scripts/` directories:

```python
import subprocess
import json

def execute_skill_script(skill_name, script_name, **kwargs):
    """Execute a skill's helper script with arguments"""
    script_path = f'skills/{skill_name}/scripts/{script_name}'
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found: {script_path}")
    
    # Build command with arguments
    cmd = ['python', script_path]
    for key, value in kwargs.items():
        cmd.extend([f'--{key}', str(value)])
    
    # Execute
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return {
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode
    }

# Usage example with memory forensics skill
result = execute_skill_script(
    'performing-memory-forensics-with-volatility3',
    'process.py',
    dump_file='/path/to/memory.dmp',
    plugin='windows.pslist'
)

if result['returncode'] == 0:
    print(result['stdout'])
else:
    print(f"Error: {result['stderr']}")
```

## Environment Configuration

Skills that require API keys or credentials reference environment variables:

```bash
# .env file for skills requiring external services
export VIRUSTOTAL_API_KEY=your_vt_key_here
export SHODAN_API_KEY=your_shodan_key_here
export MISP_URL=https://your-misp-instance.com
export MISP_API_KEY=your_misp_key_here
export SPLUNK_HOST=your-splunk-host
export SPLUNK_TOKEN=your_splunk_token
```

Load in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Skills will reference these
vt_key = os.getenv('VIRUSTOTAL_API_KEY')
misp_url = os.getenv('MISP_URL')
```

## Integration Examples

### With Claude Code / Cursor

Place in your project's `.claud/` or `.cursorrules`:

```markdown
# Cybersecurity Skills Context

This project has access to 754 cybersecurity skills in the `skills/` directory.

When I ask security questions:
1. Scan skill frontmatter in skills/*/SKILL.md
2. Match by domain, subdomain, or tags
3. Load top 3 relevant skills fully
4. Follow the Workflow sections step-by-step
5. Verify results using Verification sections

Example: "analyze this memory dump" 
→ load performing-memory-forensics-with-volatility3/SKILL.md
→ execute Volatility3 commands from Workflow
→ validate findings using Verification checklist
```

### With Custom AI Agent (Python)

```python
class CybersecurityAgent:
    def __init__(self, skills_dir='skills'):
        self.loader = SkillLoader(skills_dir)
        self.skill_index = self.loader.scan_all_frontmatter()
    
    def handle_query(self, user_query):
        """Process security query using relevant skills"""
        # Step 1: Find relevant skills
        relevant = self._match_skills(user_query)
        
        # Step 2: Load top matches
        top_skills = [
            self.loader.load_full_skill(s['name']) 
            for s in relevant[:3]
        ]
        
        # Step 3: Extract workflow steps
        workflows = []
        for skill in top_skills:
            content = skill['content']
            # Extract Workflow section
            if '## Workflow' in content:
                start = content.index('## Workflow')
                end = content.index('##', start + 1) if '##' in content[start + 1:] else len(content)
                workflows.append(content[start:end])
        
        return {
            'matched_skills': [s['metadata']['name'] for s in top_skills],
            'workflows': workflows,
            'framework_mappings': self._get_mappings(top_skills)
        }
    
    def _match_skills(self, query):
        """Simple keyword matching (replace with semantic search)"""
        query_lower = query.lower()
        scores = []
        
        for skill in self.skill_index:
            score = 0
            desc = skill['description'].lower()
            tags = ' '.join(skill.get('tags', [])).lower()
            
            # Score by keyword matches
            for word in query_lower.split():
                if word in desc:
                    score += 2
                if word in tags:
                    score += 1
            
            if score > 0:
                scores.append((score, skill))
        
        return [s for _, s in sorted(scores, reverse=True)]
    
    def _get_mappings(self, skills):
        """Extract framework mappings from loaded skills"""
        mappings = {
            'attack': set(),
            'nist_csf': set(),
            'atlas': set()
        }
        
        for skill in skills:
            meta = skill['metadata']
            mappings['attack'].update(meta.get('attack_techniques', []))
            mappings['nist_csf'].update(meta.get('nist_csf', []))
            mappings['atlas'].update(meta.get('atlas_techniques', []))
        
        return {k: list(v) for k, v in mappings.items()}

# Usage
agent = CybersecurityAgent()
response = agent.handle_query("investigate credential dumping attack")

print("Matched skills:", response['matched_skills'])
print("\nATT&CK Techniques:", response['framework_mappings']['attack'])
print("\nFirst workflow:")
print(response['workflows'][0][:500])
```

## Troubleshooting

### Skill Not Found

```python
def verify_skill_exists(skill_name):
    """Check if skill exists and is properly formatted"""
    skill_path = f'skills/{skill_name}/SKILL.md'
    
    if not os.path.exists(skill_path):
        print(f"❌ Skill not found: {skill_path}")
        return False
    
    with open(skill_path, 'r') as f:
        content = f.read()
    
    if not content.startswith('---'):
        print(f"❌ Invalid format: missing YAML frontmatter")
        return False
    
    try:
        yaml_end = content.find('---', 3)
        frontmatter = yaml.safe_load(content[3:yaml_end])
        required_fields = ['name', 'description', 'domain', 'subdomain']
        
        for field in required_fields:
            if field not in frontmatter:
                print(f"❌ Missing required field: {field}")
                return False
        
        print(f"✅ Skill valid: {skill_name}")
        return True
        
    except Exception as e:
        print(f"❌ YAML parse error: {e}")
        return False
```

### Framework Mapping Missing

If a skill doesn't show framework mappings, check `references/standards.md`:

```python
def audit_framework_mappings(skill_name):
    """Check which framework mappings exist for a skill"""
    refs_path = f'skills/{skill_name}/references/standards.md'
    
    if not os.path.exists(refs_path):
        print(f"⚠️  No references/standards.md found")
        return
    
    with open(refs_path, 'r') as f:
        content = f.read()
    
    frameworks = {
        'ATT&CK': r'T\d{4}',
        'NIST CSF': r'[A-Z]{2}\.[A-Z]{2}',
        'ATLAS': r'AML\.T\d{4}',
        'D3FEND': r'D3-[A-Z]+',
        'AI RMF': r'[A-Z]+-\d+\.\d+'
    }
    
    import re
    for name, pattern in frameworks.items():
        matches = re.findall(pattern, content)
        if matches:
            print(f"✅ {name}: {', '.join(set(matches))}")
        else:
            print(f"⚠️  {name}: No mappings found")
```

## Key Features Summary

- **754 skills** across 26 security domains
- **5 framework mappings**: ATT&CK, NIST CSF, ATLAS, D3FEND, AI RMF
- **Progressive loading**: scan frontmatter (~30 tokens), load full content only when needed
- **Structured workflows**: step-by-step procedures in every skill
- **Helper scripts**: working Python scripts in `scripts/` directories
- **Framework standards**: complete mappings in `references/standards.md`
- **agentskills.io compliant**: works with 26+ AI coding platforms

## License

Apache 2.0 — see repository for full license text.

## Contributing

Contributions welcome following the project's CONTRIBUTING.md guidelines. All skills must include YAML frontmatter, structured Markdown sections, and framework mappings.
