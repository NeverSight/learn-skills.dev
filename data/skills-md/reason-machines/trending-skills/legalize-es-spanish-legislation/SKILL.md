---
name: legalize-es-spanish-legislation
description: Query, browse, and analyze Spanish legislation stored as Markdown files with full Git history in the legalize-es repository.
triggers:
  - "search Spanish law"
  - "find Spanish legislation"
  - "query BOE law"
  - "look up Spanish legal code"
  - "check Spanish regulation"
  - "find article in Spanish law"
  - "compare versions of Spanish law"
  - "track changes to Spanish legislation"
---

# Legalize ES — Spanish Legislation Git Repository

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What It Is

`legalize-es` is a Git repository containing 8,600+ Spanish laws as Markdown files, with every legislative reform recorded as a Git commit. Each law is a single `.md` file named by its BOE identifier (e.g. `BOE-A-1978-31229.md` for the Spanish Constitution). Reform history goes back to 1960.

**Key capabilities:**
- Full text search across all laws with `grep`
- Exact diff between any two versions of a law using `git diff`
- Timeline of all reforms to a specific law using `git log`
- Historical state of any law at any point in time using `git show`/`git checkout`

---

## Setup

```bash
# Clone the full repo (includes all history)
git clone https://github.com/legalize-dev/legalize-es.git
cd legalize-es

# Shallow clone if you only need current state (much faster)
git clone --depth 1 https://github.com/legalize-dev/legalize-es.git
cd legalize-es
```

All law files live in the `spain/` directory.

---

## File Structure

```
spain/
├── BOE-A-1978-31229.md    # Constitución Española
├── BOE-A-1995-25444.md    # Código Penal
├── BOE-A-2015-11430.md    # Estatuto de los Trabajadores
├── BOE-A-2000-323.md      # Ley de Enjuiciamiento Civil
└── ... (8,600+ laws)
```

### YAML Frontmatter

Every file starts with structured metadata:

```yaml
---
titulo: "Constitución Española"
identificador: "BOE-A-1978-31229"
pais: "es"
rango: "constitucion"
fecha_publicacion: "1978-12-29"
ultima_actualizacion: "2024-02-17"
estado: "vigente"
fuente: "https://www.boe.es/eli/es/c/1978/12/27/(1)"
---
```

**`rango` values:**
- `constitucion`
- `ley-organica`
- `ley`
- `real-decreto-ley`
- `real-decreto-legislativo`

**`estado` values:**
- `vigente` — currently in force
- `derogado` — repealed

---

## Key Commands

### Find a Law by Topic

```bash
# Search law titles in frontmatter
grep -rl "trabajo" spain/ | head -20

# Search for a keyword across all law bodies
grep -rl "huelga" spain/

# Case-insensitive search for a concept
grep -rli "protección de datos" spain/
```

### Read a Specific Article

```bash
# Find Article 18 of the Constitution
grep -A 20 "Artículo 18" spain/BOE-A-1978-31229.md

# Find an article with context (10 lines before, 30 after)
grep -B 10 -A 30 "Artículo 135" spain/BOE-A-1978-31229.md
```

### Find a Law by Its BOE Identifier

```bash
# If you know the BOE ID
cat spain/BOE-A-1995-25444.md

# Search by partial identifier
ls spain/ | grep "BOE-A-1995"
```

### Filter by Law Type

```bash
# List all Organic Laws
grep -rl 'rango: "ley-organica"' spain/

# List all currently active laws
grep -rl 'estado: "vigente"' spain/

# List all repealed laws
grep -rl 'estado: "derogado"' spain/
```

---

## Git History Commands

### See All Reforms to a Law

```bash
# Full reform history of the Spanish Constitution
git log --oneline -- spain/BOE-A-1978-31229.md

# With dates
git log --format="%h %ad %s" --date=short -- spain/BOE-A-1978-31229.md

# With full commit messages (includes reform source URL)
git log -- spain/BOE-A-1978-31229.md
```

### Diff Between Two Versions

```bash
# Diff of a specific reform commit
git show 6660bcf -- spain/BOE-A-1978-31229.md

# Diff between two commits
git diff 6660bcf^..6660bcf -- spain/BOE-A-1978-31229.md

# Diff between two dates
git diff $(git rev-list -1 --before="2011-01-01" HEAD) \
         $(git rev-list -1 --before="2012-01-01" HEAD) \
         -- spain/BOE-A-1978-31229.md
```

### Read Historical Version of a Law

```bash
# State of the Constitution as of 2010-01-01
git show $(git rev-list -1 --before="2010-01-01" HEAD):spain/BOE-A-1978-31229.md

# Check out law at a specific commit (read-only inspection)
git show abc1234:spain/BOE-A-1978-31229.md
```

### Find When a Specific Text Was Added or Removed

```bash
# Find which commit introduced "estabilidad presupuestaria"
git log -S "estabilidad presupuestaria" -- spain/BOE-A-1978-31229.md

# Find which commit changed a specific phrase
git log -G "límite de déficit estructural" --oneline -- spain/BOE-A-1978-31229.md
```

---

## Programmatic Access Patterns

### Shell Script: Extract All Law Titles

```bash
#!/bin/bash
# Extract titles and identifiers from all laws
for file in spain/*.md; do
  id=$(grep 'identificador:' "$file" | head -1 | sed 's/.*: "//;s/".*//')
  title=$(grep 'titulo:' "$file" | head -1 | sed 's/.*: "//;s/".*//')
  echo "$id | $title"
done
```

### Shell Script: Find Laws Updated After a Date

```bash
#!/bin/bash
# Laws updated after 2023-01-01
TARGET_DATE="2023-01-01"
grep -rl "ultima_actualizacion:" spain/ | while read file; do
  date=$(grep 'ultima_actualizacion:' "$file" | head -1 | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
  if [[ "$date" > "$TARGET_DATE" ]]; then
    echo "$date $file"
  fi
done | sort -r
```

### Python: Parse Law Frontmatter

```python
import os
import yaml

def parse_law(filepath):
    """Parse a law Markdown file and return frontmatter + body."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter between --- delimiters
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return metadata, body
    
    return {}, content

# Example: list all active laws
laws_dir = 'spain'
active_laws = []

for filename in os.listdir(laws_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(laws_dir, filename)
        meta, body = parse_law(filepath)
        if meta.get('estado') == 'vigente':
            active_laws.append({
                'id': meta.get('identificador'),
                'titulo': meta.get('titulo'),
                'rango': meta.get('rango'),
                'ultima_actualizacion': meta.get('ultima_actualizacion'),
            })

# Sort by last update
active_laws.sort(key=lambda x: x['ultima_actualizacion'] or '', reverse=True)
for law in active_laws[:10]:
    print(f"{law['ultima_actualizacion']} [{law['rango']}] {law['titulo']}")
```

### Python: Get Reform History via Git

```python
import subprocess
import json

def get_reform_history(boe_id):
    """Get all commits that modified a law file."""
    filepath = f"spain/{boe_id}.md"
    result = subprocess.run(
        ['git', 'log', '--format=%H|%ad|%s', '--date=short', '--', filepath],
        capture_output=True, text=True
    )
    reforms = []
    for line in result.stdout.strip().split('\n'):
        if line:
            hash_, date, subject = line.split('|', 2)
            reforms.append({'hash': hash_, 'date': date, 'subject': subject})
    return reforms

# Example usage
history = get_reform_history('BOE-A-1978-31229')
for reform in history:
    print(f"{reform['date']} {reform['hash'][:7]} {reform['subject']}")
```

### Python: Compare Two Versions of a Law

```python
import subprocess

def diff_law_versions(boe_id, commit_before, commit_after):
    """Get unified diff between two versions of a law."""
    filepath = f"spain/{boe_id}.md"
    result = subprocess.run(
        ['git', 'diff', f'{commit_before}..{commit_after}', '--', filepath],
        capture_output=True, text=True
    )
    return result.stdout

def get_law_at_date(boe_id, date_str):
    """Get the text of a law as it was on a given date (YYYY-MM-DD)."""
    filepath = f"spain/{boe_id}.md"
    # Find the last commit before date
    rev = subprocess.run(
        ['git', 'rev-list', '-1', f'--before={date_str}', 'HEAD'],
        capture_output=True, text=True
    ).stdout.strip()
    
    if not rev:
        return None
    
    content = subprocess.run(
        ['git', 'show', f'{rev}:{filepath}'],
        capture_output=True, text=True
    ).stdout
    return content

# Example: see Constitution before and after 2011 reform
old_text = get_law_at_date('BOE-A-1978-31229', '2011-09-26')
new_text = get_law_at_date('BOE-A-1978-31229', '2011-09-28')
print("Pre-reform length:", len(old_text))
print("Post-reform length:", len(new_text))
```

### Python: Search Across All Laws

```python
import os
import re

def search_laws(query, laws_dir='spain', rango=None, estado='vigente'):
    """Search for a regex pattern across all laws."""
    results = []
    pattern = re.compile(query, re.IGNORECASE)
    
    for filename in os.listdir(laws_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(laws_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Filter by frontmatter fields
        if estado and f'estado: "{estado}"' not in content:
            continue
        if rango and f'rango: "{rango}"' not in content:
            continue
        
        matches = list(pattern.finditer(content))
        if matches:
            titulo_match = re.search(r'titulo: "([^"]+)"', content)
            titulo = titulo_match.group(1) if titulo_match else filename
            results.append({
                'file': filename,
                'titulo': titulo,
                'match_count': len(matches),
                'first_match_context': content[max(0, matches[0].start()-100):matches[0].end()+100]
            })
    
    return sorted(results, key=lambda x: x['match_count'], reverse=True)

# Example: find all active organic laws mentioning "privacidad"
hits = search_laws("privacidad", rango="ley-organica")
for h in hits:
    print(f"[{h['match_count']} matches] {h['titulo']}")
    print(f"  Context: ...{h['first_match_context'].strip()[:150]}...")
    print()
```

---

## Common Workflows

### Workflow 1: Research a Legal Topic

```bash
# 1. Find relevant laws
grep -rl "protección de datos personales" spain/ > relevant_laws.txt

# 2. Get titles of matching files
while read file; do
  grep 'titulo:' "$file" | head -1
done < relevant_laws.txt

# 3. Find the primary law (LOPD/GDPR implementation)
grep -rl 'rango: "ley-organica"' spain/ | xargs grep -l "protección de datos" 
```

### Workflow 2: Track a Specific Reform

```bash
# 1. Find when Article 135 changed (2011 constitutional reform)
git log -S "estabilidad presupuestaria" --oneline -- spain/BOE-A-1978-31229.md

# 2. View the exact changes
git show <commit-hash> -- spain/BOE-A-1978-31229.md

# 3. Read the commit message for official source
git show --format="%B" <commit-hash> | head -10
```

### Workflow 3: Export Laws to JSON

```python
import os, yaml, json

laws = []
for fname in os.listdir('spain'):
    if not fname.endswith('.md'):
        continue
    with open(f'spain/{fname}', 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1])
            meta['filename'] = fname
            laws.append(meta)

with open('laws_index.json', 'w', encoding='utf-8') as f:
    json.dump(laws, f, ensure_ascii=False, indent=2, default=str)

print(f"Exported {len(laws)} laws")
```

---

## Troubleshooting

### Repo is Too Large to Clone

```bash
# Use shallow clone for current state only
git clone --depth 1 https://github.com/legalize-dev/legalize-es.git

# Or clone with limited history
git clone --depth 50 https://github.com/legalize-dev/legalize-es.git
```

### Git Log Shows No History After Shallow Clone

```bash
# Fetch more history
git fetch --deepen=100

# Fetch full history
git fetch --unshallow
```

### Encoding Issues on Windows

```bash
# Force UTF-8 in git
git config core.quotepath false
git config i18n.logoutputencoding utf-8

# In Python, always open files with encoding='utf-8'
```

### Finding a Law Without Its BOE ID

```bash
# Search by partial title (case-insensitive)
grep -ril "enjuiciamiento civil" spain/ | head -5

# Or search in frontmatter only (faster)
grep -rl "Ley de Enjuiciamiento Civil" spain/
```

---

## Data Source & License

- **Legislative content**: Public domain — sourced from [BOE Open Data API](https://www.boe.es/datosabiertos/)
- **Repository structure, metadata, tooling**: MIT License
- **Official source per law**: See `fuente:` field in each file's frontmatter
- **Part of**: [Legalize](https://github.com/legalize-dev/legalize) multi-country project
- **Upcoming**: Programmatic API at [legalize.dev](https://legalize.dev)
