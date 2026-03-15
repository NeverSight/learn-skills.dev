---
name: ocsf
description: >-
  Answer questions about OCSF (Open Cybersecurity Schema Framework). Use when
  the user asks about OCSF classes, objects, attributes, profiles, extensions,
  or event normalization. Also use when the user wants to classify security
  events, find the right OCSF event class for a log source, or understand OCSF
  attribute naming conventions.
---

# OCSF

Look up OCSF reference documentation and answer from those sources. Only state
facts from files you read. Never invent schema details. If the documentation
does not cover the question, say so.

## Versions

Use the latest stable version unless the user requests a specific one. Stick to
one version per answer.

- [1.0.0](v1.0.0.md)
- [1.1.0](v1.1.0.md)
- [1.2.0](v1.2.0.md)
- [1.3.0](v1.3.0.md)
- [1.4.0](v1.4.0.md)
- [1.5.0](v1.5.0.md)
- [1.6.0](v1.6.0.md)
- **[1.7.0](v1.7.0.md)** ← latest stable
- [1.8.0-dev](v1.8.0-dev.md) ← unreleased development snapshot

Each version page links to its classes, objects, profiles, extensions, and
types.

## File layout

```
introduction.md          # OCSF overview and conceptual sections
introduction/{section}.md
faqs.md                  # Schema design rationale
faqs/{slug}.md
articles.md              # Deep-dive guides on specific topics
articles/{slug}.md
{version}.md             # Version summary (what's new, counts)
{version}/classes.md     # Class index grouped by category
{version}/classes/{name}.md
{version}/objects.md
{version}/objects/{name}.md
{version}/profiles.md
{version}/profiles/{name}.md
{version}/extensions.md
{version}/extensions/{name}/index.md
{version}/extensions/{name}/events/{event}.md
{version}/extensions/{name}/objects/{object}.md
{version}/extensions/{name}/profiles/{profile}.md
{version}/types.md
```

## Question routing

Pick the shortest reading path for the question type.

| Question pattern                              | Start here                                                                                                                       |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Which class fits event X?                     | Category table below → version classes index → candidate class pages                                                             |
| What attributes does class/object Y have?     | Version classes or objects index → the specific page                                                                             |
| How do profiles work? / Which profile for X?  | [Introduction: Profiles](introduction/profiles.md) → version profiles index                                                      |
| How do I extend the schema?                   | [Introduction: Extensions](introduction/extensions.md) or [Patching the Core Schema](articles/patching-core-using-extensions.md) |
| How do I populate observables / model alerts? | [FAQs](faqs.md) and [Articles](articles.md)                                                                                      |
| What changed between versions?                | Compare the two version pages                                                                                                    |
| Conceptual / design question                  | [Introduction](introduction.md) → [FAQs](faqs.md)                                                                                |

When the question asks you to pick a class, read multiple candidates and explain
trade-offs.

## Domain knowledge

### Core concepts

**Attributes** are named fields with a data type. Every OCSF field has a
requirement level: required, recommended, or optional.

**Objects** group related attributes into reusable structures. Objects can nest
other objects.

**Event classes** define schemas for specific security events. Each class belongs
to a category and inherits from Base Event.

**Base Event** provides universal attributes and serves as a catch-all when no
more specific class fits.

**Profiles** are mix-ins that add cross-cutting attributes. A class can apply
multiple profiles.

**Extensions** add vendor-specific attributes without modifying the core schema.

### Event categories

Use the category range to narrow scope before diving into individual class
pages.

| Range | Category             | Focus                                                        |
| ----- | -------------------- | ------------------------------------------------------------ |
| 1xxx  | System Activity      | OS-level: process, file, module, memory, kernel, registry    |
| 2xxx  | Findings             | Detections, vulnerabilities, incidents, compliance           |
| 3xxx  | IAM                  | Authentication, authorization, account and group changes     |
| 4xxx  | Network Activity     | General traffic and protocol-specific activity               |
| 5xxx  | Discovery            | Device, user, service, and resource enumeration              |
| 6xxx  | Application Activity | Web resources, API calls, file hosting, datastore operations |
| 7xxx  | Remediation          | File, process, network, and entity remediation actions       |
| 8xxx  | Unmanned             | Drones, vehicles, and robots                                 |

### Naming conventions

- `snake_case` everywhere: `process_activity`, `network_endpoint`.
- Arrays use plural names: `answers`, `enrichments`, `attacks`.
- When `_id` is `Other` (`99`), the sibling string **must** be populated with
  the source value.

Key suffixes:

| Suffix              | Meaning                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `_id`               | Enum integer identifier with a sibling string (same name minus `_id`). `0` = Unknown, `99` = Other.                     |
| `_uid`              | Schema-unique or external unique identifier (integer for classification attrs, string otherwise). Sibling uses `_name`. |
| `_uuid`             | Globally unique 128-bit identifier (string). No sibling.                                                                |
| `_name`             | Friendly name / caption sibling for `_uid` or `_id` attributes.                                                         |
| `_time`             | Timestamp (`timestamp_t`, milliseconds since epoch).                                                                    |
| `_dt`               | Datetime (`datetime_t`, RFC 3339 string). Added by the Date/Time profile alongside `_time` attributes.                  |
| `_info` / `_detail` | Object carrying supplementary information.                                                                              |
| `_process`          | Reference to a Process object.                                                                                          |
| `_ver`              | Version string.                                                                                                         |
| `_list`             | Array of values.                                                                                                        |

## Answering principles

- Read before answering. Every claim must trace back to a file you read.
- Use the question routing table and category table to narrow scope before
  reading class or object pages.
- Consult [FAQs](faqs.md) for schema design rationale and ambiguous mappings.
- Consult [Articles](articles.md) for deep-dive topics like observables, alerts,
  process parentage, and extensions.
- Read [Introduction](introduction.md) sections for conceptual questions about
  the framework itself.
