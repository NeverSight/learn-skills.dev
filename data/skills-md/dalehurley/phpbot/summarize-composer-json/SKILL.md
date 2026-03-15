---
name: summarize-composer-json
description: "Analyze and summarize PHP Composer configuration files (composer.json). Use this skill when the user asks to summarize, review, analyze, or understand a composer.json file. Extracts and explains project metadata, dependencies, requirements, scripts, and configuration settings in a clear, structured format."
tags: [php, composer, dependency-management, file-analysis, documentation, auto-generated]
version: 0.1.0
---

# Skill: summarize-composer-json

## When to Use
Use this skill when the user asks to:
- Summarize a composer.json file
- Analyze PHP project dependencies
- Review composer configuration
- Understand project requirements
- Extract metadata from composer.json
- Explain what packages a PHP project uses

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `composer_json_content` | Yes | The full content of the composer.json file to analyze | {"name": "vendor/project", "require": {"php": "^8.2"}} |

## Procedure
1. Receive the composer.json file content from the user (via file attachment or paste)
2. Parse the JSON structure to extract key sections: name, description, require, scripts, autoload, config, authors, license
3. Organize findings into logical categories: project metadata, PHP/extension requirements, dependencies with versions, executable binaries, available scripts, namespace configuration
4. Format output with clear headers, bullet points, and explanations of what each dependency does
5. Highlight critical information such as minimum PHP version, key packages, and available commands
6. Present summary in a readable format that explains both what the project is and how it's structured

## Example

Example requests that trigger this skill:

```
## Attached File Context The following files have been provided by the user as context: ### File: composer.json (38 lines, 891 bytes) ```json { "name": "dalehurley/phpbot", "description": "PHP Bot for automating your life - An evolving AI assistant powered by Claude", "type": "project", "require": { "php": "^8.2", "ext-readline": "*", "cboden/ratchet": "^0.4.4", "claude-php/agent": "^1.4.6", "claude-php/claude-php-sdk": "^0.5.3", "phpoffice/phpword": "^1.0", "react/datagram": "^1.2" }, "license": "MIT", "autoload": { "psr-4": { "Dalehurley\\Phpbot\\": "src/" } }, "bin": [ "bin/phpbot" ], "authors": [ { "name": "Dale Hurley", "email": "dale.hurley@createmy.com.au" } ], "scripts": { "phpbot": "php bin/phpbot", "web": "bin/run-web.sh" }, "config": { "sort-packages": true, "process-timeout": 0 } } ``` ## User Request summarise
```
