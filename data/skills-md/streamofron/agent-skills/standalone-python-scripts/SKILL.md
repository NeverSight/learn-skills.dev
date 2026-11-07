---
name: standalone-python-scripts
description: Use when creating standalone Python scripts with uv; the script is a single file for standalone execution rather than a larger project with pyproject.toml
---

# Standalone Python Scripts

Guidelines for writing single-file Python scripts that use PEP 723 inline metadata and uv for dependency management.

## When to Use

- Creating a standalone Python script (single file, no pyproject.toml)
- Writing a CLI tool or utility script
- Building a quick automation or one-off script with external dependencies

**NOT for:** larger Python projects with multiple modules, packages, or a pyproject.toml/setup.py structure.

## Procedure

1. **Check Python version support** — before setting `requires-python`, verify the target version is not end-of-life and has at least one year until EOL. Check https://devguide.python.org/versions/ for current status. Only target older versions if explicitly requested by the user.

2. **Minimize dependencies** — only add external packages that clearly save time or provide essential functionality. Prefer standard library when reasonable.

3. **Add PEP 723 inline metadata** — declare dependencies at the top of the script using the `# /// script` block format:
   ```python
   # /// script
   # requires-python = ">=3.12"
   # dependencies = [
   #     "click>=8.1",
   #     "arrow>=1.3",
   # ]
   # ///
   ```

4. **Use the uv shebang** — when the script has non-stdlib dependencies, use:
   ```python
   #!/usr/bin/env -S uv run --script
   ```
   This allows direct execution: `./script.py`

5. **Prefer Click for argument parsing** — when the script needs CLI arguments, use Click over argparse or other libraries.

6. **Prefer Arrow for date/time** — when the script handles dates or times, use Arrow over datetime or other libraries.

7. **Make executable** — after creating the script, run `chmod +x script.py` to make it directly executable.

## Example

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.1",
#     "arrow>=1.3",
# ]
# ///

import click
import arrow

@click.command()
@click.option("--name", default="World", help="Name to greet")
@click.option("--date", is_flag=True, help="Show today's date")
def main(name, date):
    """Greet someone and optionally show the date."""
    click.echo(f"Hello, {name}!")
    if date:
        click.echo(f"Today is {arrow.now().format('YYYY-MM-DD')}")

if __name__ == "__main__":
    main()
```

## Pitfalls

- **Over-engineering:** Don't add dependencies for trivial tasks. If `datetime` works, don't add Arrow. If `argparse` suffices, don't add Click.
- **Missing shebang:** Without `#!/usr/bin/env -S uv run --script`, the script won't run directly with `./script.py`.
- **Invalid metadata block:** The `# /// script` block must be at the top and follow PEP 723 format exactly.
- **Forgetting to chmod:** The script needs execute permissions (`chmod +x`) to run directly.
- **Version drift:** Pin minimum versions in dependencies to avoid surprises when uv resolves packages.

## Verification

After creating the script:
1. Check the metadata block is valid: `uv run --script script.py --help`
2. Run the script directly: `./script.py`
3. Verify dependencies are installed and the script works as expected

Quick checklist:
```
Is the Python version still supported (not EOL, >1 year to EOL)?
Does the script have a shebang line?
Is the PEP 723 metadata block present and valid?
Are dependencies minimal and justified?
Is the script executable (chmod +x)?
```
