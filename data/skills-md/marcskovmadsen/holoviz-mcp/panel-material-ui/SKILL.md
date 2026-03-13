---
name: panel-material-ui
description: Best practices for developing modern looking tools, dashboards and data apps using HoloViz Panel and Panel Material UI components.
metadata:
  version: "1.0.0"
  author: holoviz
  category: web-development
  difficulty: intermediate
---

# Panel Material UI Development Skills

This guide provides best practices for using Panel Material UI. Optimized for LLMs.

Please develop code, tests and documentation as an **expert Panel analytics app developer** would do when working with a **short time to market**.

**If not already loaded please get the 'panel' skill**.

**This guide focuses on panel-material-ui specific patterns. This guide takes precedence over the panel skills.**

## Installation

```bash
pip install panel-material-ui panel watchfiles hvplot hvsampledata
```

For development in .py files DO always include watchfiles for hotreload.

## Best Practice Hello World App

Let's describe our best practices via a basic Hello World App:

```python
# DO import panel as pn
import panel as pn
# DO import panel_material_ui as pmui
import panel_material_ui as pmui
import param

# DO run pn.extension
# DO remember to add any imports needed by panes, e.g. pn.extension("tabulator", "plotly", ...)
# DON'T add "bokeh" as an extension. It is not needed.
# DON'T add "panel_material_ui" as an extension. It is not needed.
# Do use throttled=True when using slider unless you have a specific reason not to
pn.extension(throttled=True)

# DO organize functions to extract data separately as your app grows
# DO use caching to speed up the app, e.g. for expensive data loading or processing that would return the same result given same input arguments.
# DO add a ttl (time to live argument) for expensive data loading that changes over time
@pn.cache(max_items=3)
def extract(n=5):
    return "Hello World" + "⭐" * n

text = extract()
text_len = len(text)

# DO organize functions to transform data separately as your app grows. Eventually in a separate transform.py file
# DO add caching to speed up expensive data transformations
def transform(data: str, count: int=5)->str:
    """
    Transforms the input data by truncating it to the specified count of characters.
    """
    count = min(count, len(data))
    return data[:count]

# DO organize functions to create plots separately as your app grows. Eventually in a separate plots.py file.
# DO organize custom components and views separately as your app grows. Eventually in separate components.py or views.py file(s).

# DO use param.Parameterized, pn.viewable.Viewer or similar approach to create new components and apps with state and reactivity
class HelloWorld(pn.viewable.Viewer):
    """
    A simple Panel app that displays a "Hello World" message with a slider to control the length of the message.
    """
    # DO define parameters to hold state and drive the reactivity
    characters = param.Integer(default=text_len, bounds=(0, text_len), doc="Number of characters to display")

    def __init__(self, **params):
        super().__init__(**params)

        # DO use sizing_mode="stretch_width" for components unless "fixed" or other sizing_mode is specifically needed
        with pn.config.set(sizing_mode="stretch_width"):
            # DO create widgets using `.from_param` method
            self._characters_input = pmui.IntSlider.from_param(self.param.characters, margin=(10,20))
             # DO Collect input widgets into horizontal, columnar layout unless other layout is specifically needed
            self._inputs = pmui.Column(self._characters_input, max_width=300)
             # DO collect output components into some layout like Column, Row, FlexBox or Grid depending on use case
            self._outputs = pmui.Column(self.model)
            self._panel = pmui.Row(self._inputs, self._outputs)


    # DO use caching to speed up bound methods that are expensive to compute or load data and return the same result for a given state of the class.
    @pn.cache
    # DO prefer .depends over .bind over .rx for reactivity methods on Parameterized classes as it can be typed and documented
    # DON'T use `watch=True` or `.watch` methods to update UI. Only for updating overall app or component state.
    # DO use `watch=True` or `.watch` for triggering side effect like saving file or sending email.
    @param.depends("characters")
    def model(self):
        """
        Returns the "Hello World" message truncated to the specified number of characters.
        """
        return transform(text, self.characters)

    # DO provide a method for displaying the component in a notebook setting, i.e. without using a Template or Page element
    def __panel__(self):
        return self._panel

    # DO provide a method to create a .servable app
    @classmethod
    def create_app(cls, **params):
        """
        Create the Panel app with the interactive model and slider.
        """
        instance = cls(**params)
        # DO use the `Page` to layout the served app unless otherwise specified
        return pmui.Page(
            # DO provide a title for the app
            title="Hello World App",
            # DO provide optional image, optional app description, optional navigation menu, input widgets, optional documentation and optional links in the sidebar
            # DO provide as list of components or a list of single horizontal layout like Column as the sidebar by default is 300 px wide
            sidebar=list(instance._inputs),
            # DO provide a list of layouts and output components in the main area of the app.
            # DO use Grid or FlexBox layouts for complex dashboard layouts instead of combination Rows and Columns.
            main=list(instance._outputs),
        )

# DO provide a method for quick development preview with `python`
if __name__ == "__main__":
    # DO run with `python path_to_this_file.py` for quick development preview
    HelloWorld.create_app().show(port=5007, autoreload=True, open=True)
# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve path_to_this_file.py --port 5007 --dev` add `--show` to open the app in a browser
    HelloWorld.create_app().servable() # DO mark the element(s) to serve with .servable()
```

DO always create test in separate test files and DO run test via pytest:

```python
import ...

# DO put tests into separate test file(s)
# DO test the reactivity of each parameter, function, method, component or app.
# DO run pytest when the code is changed. DON'T create non-pytest scripts or files to test the code.
def test_characters_reactivity():
    """
    Always test that the reactivity works as expected.
    Put tests in a separate test file.
    """
    # Test to be added in separate test file
    hello_world = HelloWorld()
    assert hello_world.model() == text[:hello_world.characters] # DO test the default values of bound methods
    hello_world.characters = 5
    assert hello_world.model() == text[:5] # DO test the reactivity of bound methods when parameters change
    hello_world.characters = 3
    assert hello_world.model() == text[:3]
```

## Panel Material UI Guidelines

### General Instructions

- DO use the new parameter names (e.g. `label`, `color`) instead of legacy aliases (e.g. `name`, `button_type`) for pmui components
- DO use `sizing_mode` parameter over `sx` css styling parameter
- DO use Material UI `sx` parameter for all css styling over `styles` and `stylesheets`
- DO use panel-material-ui components instead of panel components for projects already using panel-material-ui and for new projects
- DON'T configure the `design`, i.e. DO NOT `pn.extension(design='material')`.
- DO prefer professional Material UI icons over emojies

## Component Instructions

### Page

- DO provide the title to the `Page.title` argument. DON'T provide it in the `Page.main` area.
- DO make sure components in the `sidebar` stretch width.
- DO provide an optional image, description, navigation menu to the `Page.sidebar` argument. Normally DON't put them in the `header` or `main` areas.
- DO provide the input widgets as children to the `Page.sidebar` argument
- DO not add advanced or high components to the `Page.header` as it is only 100px high by default. Normally only buttons, indicators, text and navigation links go into the header.
- DON'T include `ThemeToggle` or other widgets to toggle the theme when using the `Page`. A `ThemeToggle` is already built in.
- DO Add a little bit of `margin=10` to the outer layout component(s) in the `main` area. To make them stand out from the `sidebar` components: `Grid(..., container=True, margin=15)`.

DO provide lists of children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=[component1, component2],  # This is correct
    sidebar=[component3, component4],  # This is correct
    main=[a_list_like_layout, a_grid],  # This is correct
)
```

DON'T provide non-lists as children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=component1,  # This is incorrect
    sidebar=list(a_list_like_layout),  # This is incorrect
    main=list(a_grid),  # This is incorrect
)
```

#### Linking Dashboard Theme with Page Theme

DO synchronize component themes with Page theme:

```python
    ...

    dark_theme = param.Boolean(
        doc="""True if the theme is dark""",
        # To enable providing parameters and bound function references
        allow_refs=True
        )

    @classmethod
    def create_app(cls, **params):
        """Create app with synchronized theming."""
        component = cls(**params)

        page = pmui.Page(
            ...,
            dark_theme=component.dark_theme,  # Pass theme to Page
        )

        # Synchronize Page theme to component theme
        component.dark_theme = page.param.dark_theme
        return page
```

### Grid

- DO set `spacing=2` or higher to separate sub components in the grid.
- DO not use `ncols` keyword argument. It is not supported.

### Column/ Row

- DO use `size` parameter instead of `xs`, `sm` or `md` parameters - they do not exist.
- DO use `sx` to set `spacing` instead of setting `spacing` directly. It does not exist.

### List like layouts

For list-like layouts like `Column` and `Row` DO provide children as positional arguments:

```python
pmui.Row(child1, child2, child3) # DO
```

DON'T provide them as separate arguments:

```python
pmui.Row([child1, child2, child3,]) # DON'T
```

### Paper

DO change the default margin to 10px:

```python
pmui.Paper.param.margin.default=10
```

### Switch

- Do add `margin=(10, 20)` when displaying in the sidebar.

### Sliders

- DO add a little bit of margin left and right when displaying in the sidebar.

### Cards

- DO use the `Paper` component over the `Card` unless you need the `Card`s extra features.
- DO set `collapsible=False` unless collapsible is needed.

### Tabulator

- DO use "materialize" `theme` instead of "material". The latter does not exist.

### Non-Existing Components

- Do use `Column` instead of `Box`. The `Box` component does not exist.

## Material UI Examples

### Standalone Icons

DO use `Typography` to make standalone icons without interactivity instead of `IconButton`:

```python
# CORRECT: Typography for standalone decorative icons
pmui.Typography(
    f'<span class="material-icons" style="font-size: 4rem;">lightbulb</span>',
    sizing_mode="fixed", width=60, height=60, sx = {"color": "primary.main"},
)
# INCORRECT: IconButton for decorative icons
pmui.IconButton(icon=icon, disabled=True, ...)
```

### Static Components Pattern (Material UI)

```python
import panel as pn
import panel_material_ui as pmui
import param

pn.extension()

pmui.Paper.param.margin.default=10

class HelloWorld(pn.viewable.Viewer):
    characters = param.Integer(default=10, bounds=(1, 100), doc="Number of characters to display")

    def _get_kpi_card(self):
        # Create a static layout once
        return pmui.Paper(
            pmui.Column(
                pmui.Typography(
                    "📊 Key Performance Metrics",
                    variant="h6",
                    sx={
                        "color": "text.primary",
                        "fontWeight": 700,
                        "mb": 3,
                        "display": "flex",
                        "alignItems": "center",
                        "gap": 1
                    }
                ),
                pmui.Row(
                    # Use a reactive/ bound/ reference value for dynamic content
                    self.kpi_value
                )
            ),
        )

    @param.depends("characters")
    def kpi_value(self):
        return f"The kpi is {self.characters}"

    def __panel__(self):
        return pmui.Paper(
            pmui.Column(
                self.param.characters,
                self._get_kpi_card(),
            ),
            sx={"padding": "20px", "borderRadius": "8px"},
            sizing_mode="stretch_width"
        )

if pn.state.served:
    HelloWorld().servable()
```

**For all other Panel patterns (parameter-driven architecture, reactive updates, serving, etc.), refer tot the 'panel' skill.**
