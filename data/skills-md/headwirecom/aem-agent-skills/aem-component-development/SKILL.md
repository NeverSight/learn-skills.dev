---
name: aem-component-development
description: >
  Build, extend, and configure AEM components end-to-end. Covers component node structure
  (cq:Component), Touch UI dialogs (cq:dialog with Granite UI), Sling Models, client libraries,
  edit configuration (cq:editConfig), and content templates. Use when creating new AEM
  components, adding or modifying component dialogs, wiring Sling Models, setting up clientlibs,
  extending Core Components, configuring edit behavior, or troubleshooting component rendering.
  Also activate when the user mentions cq:Component, cq:dialog, componentGroup, Granite UI
  widgets, or AEM component architecture.
---

# AEM Component Development

AEM components are the building blocks of page content. Each component is a `cq:Component`
node in the JCR that ties together:

1. **HTL markup** — the rendering template (`.html` file)
2. **Sling Model** — server-side business logic (Java)
3. **Dialog** — author UI for content editing (`cq:dialog`)
4. **Client libraries** — CSS/JS for frontend behavior
5. **Edit config** — authoring toolbar behavior (`cq:editConfig`)

**Prerequisite skill:** This skill assumes HTL knowledge. Load the `htl-scripting` skill for
expression syntax, block statements, XSS contexts, and global objects.

## Component File Structure

Standard Maven archetype layout (Touch UI, modern AEM):

```
ui.apps/src/main/content/jcr_root/apps/<project>/components/<component-name>/
├── .content.xml          ← cq:Component definition (title, group, supertype)
├── <component-name>.html ← HTL rendering script
├── _cq_dialog/
│   └── .content.xml      ← Touch UI dialog (Granite UI)
├── _cq_editConfig/
│   └── .content.xml      ← Edit behavior config
├── _cq_template/
│   └── .content.xml      ← Default content on drag-and-drop
├── _cq_design_dialog/
│   └── .content.xml      ← Policy/design dialog
└── clientlib/             ← Optional co-located clientlib
    ├── .content.xml
    ├── css.txt
    ├── js.txt
    ├── css/
    └── js/

core/src/main/java/<package>/models/
└── <ComponentName>Model.java  ← Sling Model
```

Note: Underscored directories (`_cq_dialog`) are the filesystem representation of JCR nodes
with colons (`cq:dialog`). The FileVault serialization requires this naming.

## Component Definition (`.content.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="My Component"
    jcr:description="A description for authors"
    componentGroup="My Project - Content"
    sling:resourceSuperType="core/wcm/components/text/v2/text"/>
```

### Key Properties

| Property | Purpose |
|---|---|
| `jcr:title` | Display name in component browser |
| `jcr:description` | Tooltip in component browser |
| `componentGroup` | Grouping in component browser. Use `.hidden` to hide |
| `sling:resourceSuperType` | Inherit from another component (rendering, dialog, edit config) |
| `cq:isContainer` | `true` if component can contain child components (like a parsys) |
| `cq:icon` | Coral UI icon name for the component browser |
| `abbreviation` | 2-char abbreviation if no icon |

## Agent Workflow: Creating a New Component

### Step 1: Define the component node

Create `.content.xml` with `jcr:primaryType="cq:Component"`, title, group, and optionally
`sling:resourceSuperType` to extend an existing component.

### Step 2: Create the Sling Model

Write the Java model class in `core/` module. See [references/sling-models.md](references/sling-models.md).

```java
@Model(adaptables = SlingHttpServletRequest.class,
       adapters = MyComponent.class,
       resourceType = "myproject/components/mycomponent",
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
public class MyComponentImpl implements MyComponent {

    @ValueMapValue
    private String title;

    @ValueMapValue
    private String description;

    @Override
    public String getTitle() { return title; }

    @Override
    public String getDescription() { return description; }
}
```

### Step 3: Create the HTL script

```html
<sly data-sly-use.model="com.myproject.core.models.MyComponent"/>
<div class="cmp-mycomponent"
     data-sly-test="${model.title || model.description}">
    <h2 class="cmp-mycomponent__title"
        data-sly-test="${model.title}">${model.title}</h2>
    <div class="cmp-mycomponent__description"
         data-sly-test="${model.description}">
        ${model.description @ context='html'}
    </div>
</div>
<sly data-sly-test="${!model.title && !model.description && (wcmmode.edit || wcmmode.preview)}">
    <div class="cq-placeholder" data-emptytext="My Component"></div>
</sly>
```

### Step 4: Create the dialog

See [references/dialogs.md](references/dialogs.md) for full Granite UI field reference.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
          xmlns:cq="http://www.day.com/jcr/cq/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
          xmlns:nt="http://www.jcp.org/jcr/nt/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="My Component"
    sling:resourceType="cq/gui/components/authoring/dialog">
    <content jcr:primaryType="nt:unstructured"
             sling:resourceType="granite/ui/components/coral/foundation/container">
        <items jcr:primaryType="nt:unstructured">
            <tabs jcr:primaryType="nt:unstructured"
                  sling:resourceType="granite/ui/components/coral/foundation/tabs"
                  maximized="{Boolean}true">
                <items jcr:primaryType="nt:unstructured">
                    <properties jcr:primaryType="nt:unstructured"
                                jcr:title="Properties"
                                sling:resourceType="granite/ui/components/coral/foundation/container"
                                margin="{Boolean}true">
                        <items jcr:primaryType="nt:unstructured">
                            <columns jcr:primaryType="nt:unstructured"
                                     sling:resourceType="granite/ui/components/coral/foundation/fixedcolumns"
                                     margin="{Boolean}true">
                                <items jcr:primaryType="nt:unstructured">
                                    <column jcr:primaryType="nt:unstructured"
                                            sling:resourceType="granite/ui/components/coral/foundation/container">
                                        <items jcr:primaryType="nt:unstructured">
                                            <title jcr:primaryType="nt:unstructured"
                                                   sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
                                                   fieldLabel="Title"
                                                   name="./title"/>
                                            <description jcr:primaryType="nt:unstructured"
                                                         sling:resourceType="granite/ui/components/coral/foundation/form/textarea"
                                                         fieldLabel="Description"
                                                         name="./description"/>
                                        </items>
                                    </column>
                                </items>
                            </columns>
                        </items>
                    </properties>
                </items>
            </tabs>
        </items>
    </content>
</jcr:root>
```

### Step 5: Add client library (if needed)

See [references/clientlibs.md](references/clientlibs.md).

### Step 6: Configure edit behavior (if needed)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:EditConfig"
    cq:actions="[edit,delete,insert,copymove]"
    cq:layout="editbar"
    cq:dialogMode="floating">
    <cq:listeners jcr:primaryType="cq:EditListenersConfig"
                  afteredit="REFRESH_PAGE"
                  afterinsert="REFRESH_PAGE"/>
</jcr:root>
```

## Extending Existing Components

Use `sling:resourceSuperType` to inherit everything from a parent:

```xml
<jcr:root ...
    jcr:primaryType="cq:Component"
    jcr:title="Custom Text"
    sling:resourceSuperType="core/wcm/components/text/v2/text"
    componentGroup="My Project"/>
```

What you inherit automatically:
- HTL rendering scripts (resolved by Sling resource type hierarchy)
- Dialogs (can overlay individual fields via Sling Resource Merger)
- Edit config, descriptions, icons

To **overlay a dialog field**, create only the nodes you need to change under `_cq_dialog/`
and set `sling:resourceSuperType` on the dialog root. The Sling Resource Merger merges your
changes with the parent.

## Core Components

Always prefer extending [AEM Core Components](https://github.com/adobe/aem-core-wcm-components)
over building from scratch. They provide:

- Production-tested, accessible, SEO-friendly markup
- BEM CSS class naming (`cmp-<name>__<element>--<modifier>`)
- Sling Model exporters for JSON/SPA
- Style System support
- Adobe Client Data Layer integration

Common Core Components to extend:
- `core/wcm/components/text/v2/text`
- `core/wcm/components/image/v3/image`
- `core/wcm/components/title/v3/title`
- `core/wcm/components/teaser/v2/teaser`
- `core/wcm/components/list/v4/list`
- `core/wcm/components/container/v1/container`
- `core/wcm/components/page/v3/page`

## Edit Placeholder Pattern

Components MUST render something visible in edit mode even when empty:

```html
<!--/* Reusable Core Components placeholder template */-->
<sly data-sly-use.template="core/wcm/components/commons/v1/templates.html"
     data-sly-call="${template.placeholder @ isEmpty=!model.hasContent}"/>
```

Or manual fallback:
```html
<div class="cq-placeholder" data-emptytext="${component.properties.jcr:title}"
     data-sly-test="${(wcmmode.edit || wcmmode.preview) && isEmpty}"></div>
```

## Content Template (`_cq_template/`)

Pre-populates the component's content node when dragged onto a page:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="nt:unstructured"
    title="Default Title"
    description="Edit this component"/>
```

## Resource Type Resolution

Sling resolves components by `sling:resourceType` on the content node:

1. Content node has `sling:resourceType = "myproject/components/hero"`
2. Sling looks for `/apps/myproject/components/hero/hero.html`
3. If not found, checks `sling:resourceSuperType` chain
4. Falls back to `/libs/` search path

Script resolution order for a resource type `myproject/components/hero`:
1. `hero.html` (matches component name)
2. `html.html` (matches extension)
3. `GET.html` (matches method + extension)
4. Then walks up the `sling:resourceSuperType` chain

## Critical Rules

1. **Always use Touch UI** (`cq:dialog`) — Classic UI dialogs are deprecated.
2. **Prefer Sling Models** over `WCMUsePojo` — Sling Models are testable, cacheable, and
   the standard for AEM as a Cloud Service.
3. **Never modify `/libs`** — always overlay in `/apps`. Use Sling Resource Merger for
   partial overrides.
4. **Always render an edit placeholder** when component has no content.
5. **Use BEM naming** for CSS classes: `cmp-<component>__<element>--<modifier>`.
6. **Set `componentGroup`** or the component won't appear in the authoring UI.
7. **Store dialog field values** with `./` prefix in `name` attribute (e.g., `name="./title"`)
   to write relative to the component's content node.
8. **Extend Core Components** before building from scratch.
9. **Client libraries under `/apps`** need `allowProxy=true` to be served via `/etc.clientlibs/`.

## Reference Files

- [references/dialogs.md](references/dialogs.md) — Touch UI dialog structure, Granite UI field types, tabs, validation
- [references/clientlibs.md](references/clientlibs.md) — Client library folder setup, categories, dependencies, HTL inclusion
- [references/sling-models.md](references/sling-models.md) — Sling Model annotations, injection strategies, adapters, testing
