---
name: ontology-semantic-modeler
description: >
  Generates Snowflake Cortex Analyst semantic models from OWL ontology files mapped to existing tables.
  Parses OWL classes and relationships, creates metadata tables, abstract views, and semantic model YAML
  with verified queries for hierarchy traversal. Includes ontology visualization.
  Use when: building ontology semantic model, OWL to semantic model, map ontology to tables,
  generate ontology views, ontology semantic view, bridge ontology with data tables.
allowed-tools: "Read Write Edit Bash(python*) Bash(uv*) Bash(pip*) Bash(mkdir*) Bash(ls*) snowflake_sql_execute notebook_actions"
metadata:
  author: tjia
  version: 1.0.0
  category: workflow-automation
  tags: [ontology, semantic-model, owl, cortex-analyst, knowledge-graph]
---

# Ontology Semantic Modeler

Generate Cortex Analyst semantic models that bridge OWL ontologies with Snowflake data tables.

## When to Use

- You have an OWL/RDF ontology file defining a domain (classes, subClassOf, properties)
- You have Snowflake tables containing domain data (or an existing semantic model YAML describing them)
- You want Cortex Analyst to understand ontological relationships (hierarchy traversal, cohort expansion, entity unification)

## Workflow Overview

This skill follows a 6-step sequential workflow. Confirm each step's output before proceeding.

### Step 1: Gather Inputs

Collect from the user:

1. **OWL file path** - Local `.owl`, `.rdf`, or `.ttl` file
2. **Target Snowflake location** - `DATABASE.SCHEMA` where objects will be created
3. **Data source** - One or both of:
   - Snowflake table names (will introspect columns via `DESCRIBE TABLE`)
   - Existing semantic model YAML file path
4. **Ontology name** - Short identifier (e.g., `BIOMED`, `GENE`, `PHARMA`)

Store these in variables for later steps. If the user provides only some inputs, ask for the rest.

### Step 2: Parse OWL Ontology

Run the OWL parser script to extract ontology structure:

```bash
uv run --script scripts/parse_owl.py \
  --owl-file "<owl_path>" \
  --output-dir "/tmp/ontology_parsed"
```

This produces JSON files in `/tmp/ontology_parsed/`:
- `classes.json` - All OWL classes with hierarchy (class name, parent, description, is_abstract)
- `relations.json` - Object properties with domain/range, transitivity, inverse
- `individuals.json` - Named individuals if present

**Review the output with the user.** Show class count, relationship types, hierarchy depth. Ask if any classes should be excluded or if mappings need adjustment.

### Step 3: Map Ontology to Physical Tables

For each OWL class, determine which Snowflake table contains its instances:

1. If tables were provided, run `DESCRIBE TABLE` on each to get column metadata
2. If a semantic model YAML was provided, read it to extract table/column info
3. Use the mapping logic:
   - Match OWL class names to table names (fuzzy match on name similarity)
   - For each matched class, identify: ID column, name column, description column
   - For unmatched abstract classes, mark as `IS_ABSTRACT = TRUE` (no physical table)

Present the proposed mapping table to the user:

| OWL Class | Physical Table | ID Column | Name Column | Filter |
|-----------|---------------|-----------|-------------|--------|

Ask the user to confirm or adjust mappings.

For relationships, map OWL object properties to edge sources:
- `subClassOf` typically maps to a knowledge graph edge table
- Domain-specific relations map to join tables or foreign keys

### Step 4: Generate SQL Artifacts

Save the confirmed mappings to a JSON file (use `assets/mappings_template.json` as the starting structure), then run the generator:

```bash
uv run --script scripts/generate_artifacts.py \
  --classes-json "/tmp/ontology_parsed/classes.json" \
  --relations-json "/tmp/ontology_parsed/relations.json" \
  --mappings-json "<mappings_json_path>" \
  --database "<DATABASE>" \
  --schema "<SCHEMA>" \
  --ontology-name "<ONTOLOGY_NAME>" \
  --output-dir "/tmp/generated"
```

This produces three files. Alternatively, generate them manually using the confirmed mappings:

**4a. Metadata Tables SQL** (`01_metadata_tables.sql`)

Generate `CREATE TABLE` + `INSERT` statements for:
- `ONT_CLASS` - Class hierarchy from OWL
- `ONT_RELATION_DEF` - Relationship definitions from OWL properties
- `ONT_CLASS_MAPPING` - Class-to-table mappings from Step 3
- `ONT_RELATION_MAPPING` - Relationship-to-table mappings from Step 3

Use the template at `references/metadata_tables_template.sql` as the pattern.

**4b. Abstract Views SQL** (`02_abstract_views.sql`)

For each hierarchical relationship (IS_HIERARCHICAL=TRUE), generate:
- A resolved relationship view (e.g., `VW_ONT_SUBCLASS_OF`)
- Descendant/ancestor helper views

For each abstract class with concrete subclasses, generate:
- A `UNION ALL` view unifying all concrete instances (e.g., `VW_ONT_{CLASS_NAME}`)

For statistical summaries:
- Hierarchy stats view (direct children/parent counts)
- Coverage views (which data entities have ontology mappings)

Use the template at `references/abstract_views_template.sql` as the pattern.

**4c. Semantic Model YAML** (`03_ontology_semantic_model.yaml`)

Generate a Cortex Analyst semantic model YAML containing:
- One table entry per abstract view created in 4b
- Dimensions for all columns in each view
- Verified queries for common ontology patterns:
  - "What are the direct children of X?" (direct subclass lookup)
  - "What are all descendants of X?" (recursive CTE)
  - "What types of X exist?" (entity type listing)
  - "How many entities of each type?" (hierarchy stats)

Use the template at `references/semantic_model_template.yaml` as the pattern.

**Present all generated SQL and YAML to the user for review before execution.**

### Step 5: Deploy to Snowflake

After user approval, execute the SQL in order:

```python
# 1. Create metadata tables
snowflake_sql_execute(sql=metadata_sql)

# 2. Create abstract views
snowflake_sql_execute(sql=views_sql)

# 3. Create semantic view
create_semantic_view_sql = f"""
CREATE OR REPLACE SEMANTIC VIEW {database}.{schema}.{ontology_name}_ONTOLOGY_SEMANTIC_VIEW
  AS SEMANTIC MODEL '{yaml_content}'
"""
snowflake_sql_execute(sql=create_semantic_view_sql)
```

Run verification queries to confirm row counts and data integrity.

### Step 6: Visualize (Optional)

If the user wants visualization, launch the Streamlit app:

```bash
uv run --script scripts/visualize_ontology.py -- \
  --classes-json "/tmp/ontology_parsed/classes.json" \
  --relations-json "/tmp/ontology_parsed/relations.json" \
  --semantic-model "<path_to_generated_yaml>" \
  --port 8501
```

This shows:
- Interactive ontology class hierarchy (tree view)
- Relationship graph (nodes = classes, edges = properties)
- Generated semantic model summary (tables, dimensions, verified queries)
- Coverage matrix (which OWL classes mapped to which tables)

## Degrees of Freedom

The user can customize:
- **Which OWL classes to include** - Filter by namespace, depth, or explicit list
- **Table mapping strategy** - Auto-detect vs. manual specification
- **View naming convention** - Default `VW_ONT_` prefix, customizable
- **Verified query patterns** - Add domain-specific query templates
- **Hierarchy depth limit** - Default 10 levels for recursive CTEs
- **Semantic model name** - Default `{ONTOLOGY_NAME}_ONTOLOGY_SEMANTIC_VIEW`

## Error Handling

- **OWL parse failure**: Check file format (OWL/XML, Turtle, RDF/XML). The parser supports all three.
- **No table matches**: Ask user to provide explicit mappings. Not all OWL classes need physical tables.
- **SQL execution errors**: Check permissions (`CREATE TABLE`, `CREATE VIEW` on target schema). Show exact error and suggest grants.
- **Empty views**: Verify filter conditions in ONT_CLASS_MAPPING match actual data values.

## Reference Files

- `references/metadata_tables_template.sql` - Template for ONT_CLASS, ONT_RELATION_DEF, ONT_CLASS_MAPPING, ONT_RELATION_MAPPING
- `references/abstract_views_template.sql` - Template for hierarchy views, entity union views, stats views
- `references/semantic_model_template.yaml` - Template for Cortex Analyst semantic model YAML
- `references/example_biomed_output/` - Complete example from the BIOMED approach 2 solution
