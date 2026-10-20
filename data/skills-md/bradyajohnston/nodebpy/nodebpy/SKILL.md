---
name: nodebpy
description: Build, edit and verify Blender node trees (Geometry Nodes, shader materials and worlds, compositor) as Python code with the nodebpy library. Use whenever the task involves writing or changing a Blender node tree, node group or material from Python, porting a hand-made node setup to code, turning an existing .blend node tree into code (to_python), writing reusable node-group classes (CustomGeometryGroup), or running/rebuilding trees in a live Blender session or headless with the bpy module, even if the user just says "geometry nodes", "make a node group", or "a material with nodes" without naming nodebpy.
---

# Writing Blender node trees with nodebpy

nodebpy turns node trees into ordinary Python: every Blender node is a typed class,
instantiating it inside a `with ... tree(...)` block adds it to that tree, `>>` links
nodes, and Python operators build Math / Compare / Boolean nodes. The Python is the
source of truth and the Blender tree its build product.

This file is the loop and the core idioms. Read a reference only when the task needs it:

| Reference | Read it for |
|---|---|
| [references/writing-trees.md](references/writing-trees.md) | node arguments, socket methods, operators, the group interface, rotations, layout |
| [references/zones-and-items.md](references/zones-and-items.md) | repeat / simulation / for-each / closure zones, item nodes, switches |
| [references/shader-compositor.md](references/shader-compositor.md) | materials, shader groups, worlds, compositor groups |
| [references/existing-trees.md](references/existing-trees.md) | editing a user's tree, `to_python`, live re-runs, group classes, asset libraries |
| [references/verifying.md](references/verifying.md) | plotting a tree, checking structure, evaluating geometry and simulations |

## 1. The loop

1. **Write the script to a `.py` file**, so later fixes are small edits.
2. **Run it headless** (or in the user's Blender, section 1.1):

   ```bash
   uv add nodebpy "bpy==5.2.*" matplotlib   # bpy matches the version: 520.x wants 5.2+
   BLENDER_USER_EXTENSIONS=/nonexistent uv run python build_tree.py
   ```

3. **Fix the one error it prints** (section 4), then run again. nodebpy's errors say
   what to change: a mistyped enum lists the closest options, a link to a hidden
   socket names the sockets that exist, a Switch fed mismatched values names each type.
4. **Verify the result before reporting success** ([references/verifying.md](references/verifying.md)).
   A tree that builds is not necessarily the tree you meant: `>>` picks sockets by
   type, and an unlinked input silently uses its default. At minimum, count the nodes
   and links and evaluate the geometry on an object.

### 1.1 Running notes

- `BLENDER_USER_EXTENSIONS=/nonexistent` stops an installed extension (e.g. Molecular
  Nodes) bundling an older nodebpy from shadowing the one in the venv. Also
  `import nodebpy` before `import bpy`.
- A headless session starts from the factory scene (a `Cube` exists) and saves nothing
  unless you call `bpy.ops.wm.save_as_mainfile(filepath=...)`.
- Don't name scripts after stdlib modules (`inspect.py`, `types.py`): `import bpy` then
  crashes with an obscure glog "InitGoogleLogging() twice" error.
- **Inside a running Blender** (text editor, Blender MCP `execute_blender_code`, an
  add-on) the same code works. Rebuild with `clear=True` so modifiers stay attached,
  and re-run scripts with group classes through `nodebpy.live.run_source`
  ([references/existing-trees.md](references/existing-trees.md)).

## 2. Saving context

| Need | Cheap way | Avoid |
|---|---|---|
| Find a node | `nodebpy lookup search "named attribute"` | guessing class names |
| A node's arguments, enum options, variants, outputs | `nodebpy lookup show StoreNamedAttribute` (`--tree shader` / `compositor`) | reading generated source |
| Methods on a socket type | `nodebpy lookup socket Vector` (no argument lists the types) | `dir()` dumps |
| Understand an existing tree | `to_python(bpy.data.node_groups["Name"])` | walking `nodes` / `links` by hand |
| See the wiring | `print(tree.to_mermaid())`; `tree.to_plot("t.png")` when layout matters | screenshots |
| Idiomatic examples | the docs gallery (https://bradyajohnston.github.io/nodebpy/examples/, scripts in `docs/examples/code/`) and the tests (`tests/test_usecases.py`, `test_operators.py`) | |

`nodebpy` is the installed package's console script (`uv run nodebpy ...`, or
`python -m nodebpy ...`), so it describes the version you have. Look up several nodes
at once, and only the ones you are unsure of.

## 3. Core idioms

```python
from nodebpy import geometry as g   # shader as s, compositor as c

with g.tree("Scatter Cubes", clear=True, is_modifier=True) as tree:
    count = tree.inputs.integer("Count", 50, min_value=0)
    scale = tree.inputs.float("Scale", 0.1, min_value=0.0)

    (
        g.Points(count, position=g.RandomValue.vector(min=-1))
        >> g.InstanceOnPoints(instance=g.Cube(), rotation=g.RandomRotation(seed=2), scale=scale)
        >> g.RealizeInstances()
        >> tree.outputs.geometry("Geometry")
    )
```

- **Nodes are classes named after the UI label** ("Random Value" is `g.RandomValue`).
  Variants are class methods, ordered mode > domain > data type > operation:
  `g.Math.sine(x)`, `g.Compare.float.less_than(a, b)`,
  `g.StoreNamedAttribute.point.vector(name="vel", value=v)`.
- **Socket inputs are constructor arguments** (snake_case of the socket name). A value
  can be a node (its best-matching output is linked), a socket, a plain value (the
  default), a list (each item linked into a multi-input such as Join Geometry), `None`
  (left alone) or `...` (filled by the next `>>`). A tuple that mixes values and
  sockets, `g.Cube(size=(1, 1, height))`, becomes a Combine XYZ / Combine Color.
- **Properties are keyword-only UPPER_CASE enums** (`domain="FACE"`); menu *sockets*
  take the item's display name (`g.ResampleCurve(mode="Count")`). New nodes start with
  the values a node added in the editor has.
- **`a >> b` links a's output into b's most compatible input and returns b**, so
  chains read left to right. Target a socket with `a >> b.i.offset`; the interface
  output goes last: `... >> tree.outputs.geometry("Geometry")`.
- **Sockets**: `node.i.<name>` / `node.o.<name>` (snake_case; repeats become
  `value_001`), `node.o["Name"]`, `node.o[0]`. The raw bpy node is `node.node`.
- **Operators build nodes**: `+ - * / ** % //`, `< <= > >= == !=` (Compare), `&`, `|`,
  `^`, `~` (Boolean Math on booleans, Bit Math on integers), `@` (matrices). Integer
  `/` is true division (a float) and `%` is floored modulo, as in Python; use `//` for
  integer division. `==` builds a Compare node, so use `is` to compare node objects.
- **A socket has no Python truth value.** `if socket:`, `and`/`or` and the builtins
  `max()`/`min()` raise `TypeError`: use `a.max(b)`, `a.min(b)`, or a Switch
  (`(x > 0).switch.float(a, b)`), and `is not None` to test a socket exists.
  `round(f)` and `math.floor(f)` return integer sockets.
- **Methods go on the value flowing down the chain**, not on nodes:
  `g.Position().o.position.z`, `pos.transform(world)` (a point: translation applies),
  `normal.transform_direction(world)` (a direction: it doesn't),
  `g.SelfObject().o.self_object.matrix()`, `vec.normalize()`, `f.map_range(0, 1, -1, 1)`.
  `fac.mix.float(a, b)` and `cond.switch.float(a, b)` are the deliberate exceptions:
  they sit on the factor or condition.
- **Per-domain field methods** replace most statistics nodes: on any field,
  `.point` / `.face` / `.edge` / `.corner` / `.spline` / `.instance` / `.layer` give
  `.min(group)`, `.max(group)`, `.mean(group)`, `.total(group)`, `.at(index)`,
  `.evaluate()` and more. `idx == idx.point.min(island)` marks the first vertex of
  each island.
- **Switches take their type from their values**: `g.Switch(cond, g.Cube(), g.Cone())`
  is a Geometry switch. Use a typed variant (`g.Switch.float(...)`) when the values
  don't say.
- **Interface sockets**: `tree.inputs.<type>(name, default, ...)`,
  `tree.outputs.<type>(name)`; keep the returned socket in a variable. Expose the
  values a user would tweak (a count, a seed, a size), not every literal.
- **Fields are evaluated where they are consumed.** A field built from `g.Position()`
  and used after a Set Position sees the moved points; capture values you need from
  the original geometry first (`g.CaptureAttribute`). The same goes for Mesh Island and
  similar context after Mesh to Points, Instance on Points or Realize Instances.
- **Prefer rotation and matrix sockets** to Euler workarounds: `g.RandomRotation()`,
  `pos.rotate(rot)`, `rot.rotate(by)`, matrices with `@`
  ([references/writing-trees.md](references/writing-trees.md)). `g.Cone()` has its
  origin at its base; `g.Cylinder()` and `g.Cube()` are centred.
- **Factor repeated sub-graphs** into plain Python functions that take and return
  sockets; write a `CustomGeometryGroup` when it should be one group node. Frames:
  `with g.Frame("Label"):`. Layout runs when the `with` block exits.

## 4. Errors and what they mean

| Error | Cause and fix |
|---|---|
| `TypeError: Math's operation has no option 'SUBSTRACT'. Did you mean 'SUBTRACT'?` | A mistyped enum or menu value; use a suggested one. |
| `RuntimeError: 'Vector Math' has no 'Vector' output with its current settings {...}; available: ['Value']` | The socket is hidden by the node's mode; use one it lists, or another variant. |
| `RuntimeError: Socket 'A' ... is inactive` | Linking into a socket the current `data_type` greys out; use the variant (`g.Mix.vector(...)`). |
| `SocketError: Can't tell which type of Switch to build: the values are GEOMETRY from ...; VECTOR from ...` | A switch's values disagree; fix the values or use a typed variant. |
| `SocketError: No compatible output socket found ...` / `Cannot link any output ...` | `>>` found no socket pair; name the socket: `a.o.vector >> b.i.offset`. |
| `SocketError: 'Offset' takes 3 components, not 2: (...)` | A tuple of sockets has the wrong length for the input. |
| `TypeError: The truth value of a socket is decided when the tree runs ...` | `if`/`and`/`or`/`max()` on a socket; see section 3. |
| `RuntimeError: ... is ambiguous` | Two sockets share a name; use `.i.value_001`, an index or the identifier. |
| `AttributeError: 'Position' object has no attribute 'x'` | A socket method on a node; go through `.o.<socket>` first. |
| `RuntimeError: Node 'X' must be created within a TreeBuilder context manager` | A node class called outside `with g.tree(...)`. |
| `TypeError: expected a NodeTree type, not TreeBuilder` | Assign `tree.tree`, not `tree`, to `mod.node_group`. |
| `TypeError: ... already exists as GeometryNodeTree ... Use a unique _name` | Two group classes share a `_name` across tree types. |
| `InvalidLinkWarning: Blender can't evaluate 1 link in ...: ... ('Count' takes a single value, not a field)` | A field (Position, Index, a per-element value) reaches an input that takes one value; compute that value without the field, e.g. with an Attribute Statistic or a group input. |
| `DeprecationWarning: Blender deprecates the RotateEuler node` | Use the replacement it names (`g.RotateRotation`). |
| `CodegenError` from `to_python` | A node with no nodebpy class; pass `strict=False` or register an emitter. |

## 5. Checklist before you finish

1. Every node was looked up rather than guessed, and the script runs cleanly.
2. You verified the result (structure, evaluated geometry, or a plot) against the intent.
3. Interface sockets have clear names, defaults and `min_value`/`max_value` where a user
   could enter nonsense.
4. Existing trees were rebuilt with `clear=True` (or `to_python(..., in_place=True)`),
   so no `.001` duplicates are left.
