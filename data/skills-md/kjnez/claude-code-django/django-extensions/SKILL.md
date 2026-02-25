---
name: django-extensions
description: Django-extensions management commands for project introspection, debugging, and development. Use when exploring URLs, models, settings, database schema, running scripts, or profiling performance. Triggers on questions about Django project structure, model fields, URL routes, or requests to run development servers.
---

# Django Extensions

This project has django-extensions installed. Use these commands to understand and interact with the Django project.

## Introspection

### Show URL Routes
```bash
python manage.py show_urls
```

### List Model Information
```bash
# All models
python manage.py list_model_info

# Specific model with signatures and field classes
python manage.py list_model_info --model <app.Model> --signature --field-class

# All methods including private
python manage.py list_model_info --model <app.Model> --all-methods --signature
```

### Print Settings
```bash
# All settings
python manage.py print_settings --format=pprint

# Wildcards supported
python manage.py print_settings AUTH*
python manage.py print_settings DATABASE*
python manage.py print_settings *_DIRS
```

### Show Permissions
```bash
python manage.py show_permissions
python manage.py show_permissions <app_label>
```

### Show Template Tags
```bash
python manage.py show_template_tags
```

## Development

### Enhanced Shell (shell_plus)
```bash
python manage.py shell_plus
python manage.py shell_plus --print-sql
```
Auto-imports all models. Use `--dont-load app1` to skip apps.

### Enhanced Dev Server (runserver_plus)
```bash
python manage.py runserver_plus
python manage.py runserver_plus --print-sql
```
Includes Werkzeug debugger for interactive debugging.

## Database

### SQL Diff (Compare Models to Schema)
```bash
python manage.py sqldiff -a        # SQL differences
python manage.py sqldiff -a -t     # Text differences (readable)
```

## Script Execution

### Run Scripts with Django Context
```bash
python manage.py runscript <script_name>
python manage.py runscript <script_name> --script-args arg1 arg2
python manage.py runscript <script_name> --traceback
```
Scripts in `scripts/` directory must define a `run()` function.

## Profiling

### Profile Server Requests
```bash
python manage.py runprofileserver --prof-path=/tmp/profiles
python manage.py runprofileserver --use-cprofile --prof-path=/tmp/profiles
python manage.py runprofileserver --kcachegrind --prof-path=/tmp/profiles
```

## Notes

- Model notation: `app.ModelName` (e.g., `core.EmailAccount`, `metabox.Thread`)
- Settings wildcards: `AUTH*`, `*_DIRS`, `DATABASE*`
- Commands run from project root
