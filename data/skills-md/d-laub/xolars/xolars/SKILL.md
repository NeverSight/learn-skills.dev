---
name: xolars
description: Use when writing or modifying Python code that imports `xolars` — pairing an xarray Dataset with per-dimension Polars frames, constructing the `Xolars` container, selecting with isel/sel, or doing zarr+parquet round-trips via write/open. Skip for plain xarray or polars work that doesn't touch the `Xolars` class.
---

# xolars public API

`xolars` is one tiny frozen container: an `xarray.Dataset` plus one Polars
frame per dimension, kept aligned to the Dataset's coordinate order through
selection and disk round-trips.

## Public surface

`import xolars` exposes exactly one name:

- `xolars.Xolars` — the container

Use `from xolars import Xolars`. Anything under `xolars._core` is internal.

`Xolars` is `attrs`-frozen and `Generic[F]` where `F = pl.DataFrame | pl.LazyFrame`
— every per-dimension frame is the same kind. It's frozen, so `isel`/`sel`/`collect`
return **new** instances; they never mutate.

## Construction

```python
from xolars import Xolars

xo = Xolars(ds=dataset, df={"sample": sample_frame, "gene": gene_frame})
# positional also works: Xolars(dataset, {"sample": sample_frame})
```

- `ds: xr.Dataset`
- `df: Mapping[Hashable, pl.DataFrame | pl.LazyFrame]` — **a dict keyed by
  dimension name**, one frame per dimension you want metadata for (not every
  dim is required). It is NOT a single frame and NOT a list.

### Invariants enforced at construction (each raises `ValueError`)

For each `dim -> frame`:
1. `dim` must be a real dimension of `ds`.
2. `frame` must have a column **named exactly `dim`** (the join key).
3. That column's values must match `ds[dim]` coordinates as a **set** — same
   length, same membership. Missing or extra IDs raise; partial overlap raises.

Row order does **not** matter: the frame is auto-reordered (via a right-join on
the dim column) to match the Dataset's coordinate order. Don't pre-sort.

## Selection — isel / sel

Same signatures as `xarray.Dataset.isel` / `.sel` (indexers dict or kwargs,
`drop`, `missing_dims`; `sel` also takes `method`/`tolerance`):

```python
xo.isel(sample=slice(0, 10))      # positional
xo.sel(sample=["S1", "S2"])       # label-based
```

Both subset the Dataset **and** filter every per-dimension frame whose dim was
indexed, keeping the frames aligned. A scalar indexer that drops a dimension
also drops that dim's frame. Frames for un-indexed dims pass through untouched.

To filter by metadata (e.g. `age > 50`), filter the frame yourself for the IDs,
then pass them to `sel` — there is no metadata-predicate method on `Xolars`:

```python
frame = xo.df["sample"]                       # may be DataFrame or LazyFrame
ids = frame.filter(pl.col("age") > 50).select("sample")
ids = ids.collect() if isinstance(ids, pl.LazyFrame) else ids
xo2 = xo.sel(sample=ids["sample"].to_list())
```

## Adding data — assign / merge

Both are functional (return a **new** `Xolars`); 1-D data lives in the matching
dimension's Polars frame, N-D data lives in the Dataset.

```python
# assign one or more named variables (xarray.Dataset.assign idiom)
xo2 = xo.assign(gc=("gene_id", gc_array))                 # 1-D -> gene_id frame
xo2 = xo.assign(counts=(("gene_id", "sample_id"), mat))   # 2-D -> Dataset
xo2 = xo.assign(score=some_named_dataarray)               # aligned by label
# passing an xarray.Dataset value is an error -> use merge()

# merge whole objects; 1-D vars in xarray objects move to Polars
xo2 = xo.merge(other_dataset, gene_frame)                 # bare frame: dim inferred
xo2 = xo.merge(frames={"gene_id": [f1, f2]})              # explicit, aligned to gene_id
```

Conflicting names overwrite silently. Polars/xarray inputs are **left-aligned**
to the fixed coordinates (subset → nulls, superset → dropped); existing `ds`
coordinate sets are never grown (though a ≥2-D var may introduce a new dim).

## Disk round-trip — write / open

```python
xo.write(path, mode="w")          # mode is REQUIRED (a zarr write mode)
reopened = Xolars.open(path)      # classmethod -> Xolars[pl.LazyFrame]
```

- `write(path, mode)` creates `path/` containing `dataset.zarr/` plus one
  `{dim}.parquet` per frame. **`mode` has no default** — pass `"w"` (overwrite),
  `"w-"`, `"a"`, etc. (xarray `ZarrWriteModes`).
- `open(path)` reads `dataset.zarr` and `scan_parquet`s every `*.parquet`
  beside it — frames come back **lazy** (`pl.LazyFrame`).
- Both `path` args are typed `pathlib.Path`; pass a `Path`, not a bare string.

## Eager vs lazy — collect

`open` yields LazyFrames. To materialize every frame to `pl.DataFrame`:

```python
eager = reopened.collect()        # -> Xolars[pl.DataFrame]
```

Construction, validation, and selection all work on either kind, so call
`collect()` only when you actually need eager frames.

## Common mistakes

| Mistake | Fix |
|---|---|
| `Xolars(dataset, metadata=df)` | `Xolars(ds=dataset, df={dim: frame})` |
| Passing one bare frame or a list as `df` | `df` is a dict keyed by dimension name |
| Frame lacks a column named after the dim | Add a column named exactly `dim`; it's the join key |
| Frame IDs only partially overlap `ds[dim]` | Must match as a set (same length + membership) or it raises |
| Pre-sorting frame rows to match coords | Unnecessary — auto-reordered on construction |
| `xo.to_zarr(...)` / `Xolars.open_zarr(...)` | `xo.write(path, mode)` / `Xolars.open(path)` |
| `xo.write(path)` | `mode` is required, e.g. `mode="w"` |
| Expecting eager frames after `open` | They're `LazyFrame`; call `.collect()` |
