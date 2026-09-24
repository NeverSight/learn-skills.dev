---
name: array-api
description: Conventions that MUST be followed when implementing array API compatible functions and their tests.
---

# Conventions for implementing array API compatible functions and their tests

- **Think (not plan) about the formulation and the way to implement mathematically beautifully a LOT beforehand, ask questions to the user or internet, then finally write code.** Besides being a intelligent assistant, you have to admit that you are **extremely bad at numerical** programming due to the lack of such dataset (clean pure-Python numerical code is very rare). Think about the math formulation, the way to implement it, then at the **very final stage**, write code.

## Function implementation

- This repository is about numerical analysis. You need to make very sure about the math formulation before implementing the code.
- If documentation about the formulation is provided, always read it first, to very make sure the functions are implemented mathematically correctly and beautifully.
- All methods should be array API compatible.
  - **Function: name** Name functions without `compute_`, `calculate_` suffix (e.g. `prime_number(i: int, /)`, not `compute_prime_number`, `p_i`).
  - **Functions / Arguments / Variables: name**: The function / argument / variable names in the code should not the same as the variable name math formulation (e.g. `n`) but very readable (e.g. `n_iterations`).
    For arguments, in the docstring, the corresponding variable name in the math formulation should be mentioned:

    ```text
    n_iterations : Array
                The number of iterations $n$ of shape (...,).
    ```

    Try not to add the word "corresponding to" because it is redundant.

    For variables, in the first definition, comment `# n in docs` etc. (without `$`).

    If you define variable for `f(t)`, where `f` is a function name in code and `t` is a variable name in code, you can name the variable as `f_t` without comment.

  - **Output shape depending on integer output**: If output shape depends on the input argument, it should match the input integer when possible. For example, to compute $0, 1, ...$, set argument name to `n_*_end` (`n_end` if it is obvious) and return `0, 1, ..., n_*_end - 1`, so that the output shape is `(n_*_end,)` and it is intuitive, matches `range(n_end)` convention and `np.arange(n_end)` syntax.
  - **GUFunc compatibility**: If an array is passed to function, the function should be GUFunc-compatible, i.e. the function should only remove / append extra dimensions from the LAST dimensions of the input / output arrays, e.g. `(..., a, b) -> (..., c, d, e)`.
  - **Arguments: arrays** If array is passed to function, use `array_api.latest.Array` as the array type hint, and use `array_api_compat.array_namespace()` to get the array API namespace `xp`. `array_api_compat.array_namespace()` should be ideally called with all input arrays / evaluated function as arguments IF POSSIBLE, e.g. `xp = array_api_compat.array_namespace(x, y, z)` to validate the input arrays are on the same array API and device. The arguments may also contain None, Python scalars, useful when arguments are optional.
  - **Arguments: no arrays -> special kw-only arguments** If NO array is passed to function, add `xp`, `device`, `dtype` as an required keyword-only argument with type hint `array_api.latest.ArrayNamespace`, `Any`, `Any` respectively. Do not add these arguments if an array is passed to function.
  - **Arguments: function -> GUFunc-compatible** If the function needs function arguments, assume that to be also GUFunc-compatible. The argument description should end with `(..., a, b) -> (..., c, d, e)` (No preposition needed for this). Don't add any word in the following sentence: "GUFunc-compatible vectorized function from array to array", just explain the mathematical meaning of the function and its shape convention.
  - **Arguments & Docstring: function shape convention should be reasonable to the function**: Conceptually (mathematically) unrelated axes to function should be placed at the _beginning_ of the shape as `...`.
    - _Example_: When mathetically integrating `n_func` functions using `n_quad` quadrature points, the function shape convention should be written as `(...) -> (..., n_func)` (`(:) -> (:, n_func)` if the user explicitly specifies to implement function not GUFunc-compatible), not `(n_quad) -> (n_quad, n_func)` or `(n_quad) -> (n_func, n_quad)`, because `n_quad` has nothing to do with functions mathematically.
  - `xp.moveaxis()` may be used without worrying about performance, do not worry about internal complexity whcn choosing convention.
  - Do not worry about axis performance when choosing convention.
  - **Docstring: function output-dependent shape**: When the shape is variable (depending on function etc.) one can do `(..., ...(f))` where `f` implies the function but may replaced with something more suitable. `(..., *something)` is also possible but less preferred, yet sometimes it might be more suitable.
  - **Docstring**: docstring should contain doctests. They should be "demostrative", cover the edge cases in terms of math (not errors, wrong types, etc.). When doctests are run, the file in which the function is implemented is imported, therefore do not re-import packages or the function.
  - **Docstring: LaTeX**: Use LaTeX in docstring for mathematical symbols.
    - Do not use sphinx's native math syntax (e.g. `:math:`, `.. math::`).
    - Use `$` for inline math and `$$` for block math. Install `sphinx_math_dollar` to `docs` group (`uv add --group docs sphinx_math_dollar`) and add both `sphinx_math_dollar` and `sphinx.ext.mathjax` to `extensions` in `docs/conf.py` if this is not already done and LaTeX needs to be written in docstring.
    - For LaTeX variables which length longer than 1, use `\mathrm{}` to avoid confusion with multiplication. For variables which length is 1, write as-is.
  - **Docstring: D301**: Be careful to Ruff `D301 escape-sequence-in-docstring: Use r""" if any backslashes in a docstring` when writing LaTeX in docstring. Note that it will be automatically fixed by `prek run -a`.
  - **Docstring**: The docstring should be Numpydoc style.

    ```python
    from array_api.latest import Array, ArrayNamespace

    def func(x: Array, power: Array) -> Array:
        """
        Computes $x^p$.

        Extended description of function.

        Parameters
        ----------
        x : Array
            The base array of shape (...,).
        y : Array
            The power to which $x$ is raised $p$ of shape (...,).

        Returns
        -------
        Array
            $x^p$ of shape (...,).

        Examples
        --------
        >>> func(2, 3)
        8
        >>> import pytest
        >>> with pytest.raises(ValueError):
        >>>     func(0, -1)
        """
    ```

  - **Docstring: shape**: The docstring should mention the shape of the input / output arrays and the argument description should end with `of shape (..., a, b)`.
  - **Comment: shape**: If it is not obvious, simply comment the excepted shape of the variable on top of it, e.g. `# (..., a, b)`. (Not `# shape: (..., a, b)` because it is redundant.)
  - **ExceptionGroup**: If multiple input checks can be done in a row, use `ExceptionGroup` to raise all errors at once, allowing the user to fix all errors at once.
    ```python
    errors = []
    if x <= 0:
        errors.append(ValueError("x must be positive"))
    if y <= 0:
        errors.append(ValueError("y must be positive"))
    if errors:
        raise ExceptionGroup("Invalid input", errors)
    ```
  - **Shape checking**: The function should check the shape at the very beginning of its implementation.
    - Check every shape variable (etc. `N`) is correct
    - Check every variable-length shape variable (etc. `...`, `...(f)`) is both broadcastable and moreover has the same dimensions. (Does not need to have same shape.)
    - These should be done using `array_api_shape_check.check_shapes()` function, which syntax is as follows. The result may be useful for later computation in some cases.

      ```python
      def func(x: Array, y: Array) -> Array:
          """
          Parameters
          ----------
          x : Array
              Array of shape (..., A, B).
          y : Array
              Array of shape (..., ...(C), D, E).
          """
          info = check_shapes("...AB,...*CDE", x, y, names="x,y")
          # use info for later computation if useful
          z = xp.zeros(info.unique["C"].shape_broadcasted, device=x.device, dtype=x.dtype)
      ```

      ```python
      def check_shapes(
          subscripts: str, /, *operands: Array | tuple[int, ...], names: str | None = None
      ) -> SubscriptInfoFromShape:
          """
          Parse variable subscript ndims by solving linear equations.

          Parameters
          ----------
          subscripts : str
              Subscripts separated by "," per operand.

              1. Subscripts must be of length 1
              2. Subscripts must not be "*" or ".".
              3. If start with "*", the subscript is treated as variable.
              4. "..." is replaced with "*.".]
          operands : Array or tuple[int, ...]
              Arrays or shape tuples corresponding to check.
          ndims : Sequence[int]
              The number of dimensions for each operand.
          names : str | None
              The names of operands separated by ",",
              used for error messages. If None, operand indices are used instead.

          Returns
          -------
          SubscriptInfoFromSubcript
              The parsed subscript info.

          Raises
          ------
          ValueError
              If the subscript is invalid.

          Examples
          --------
          >>> info = check_shapes("ij,*k*l,*li", (1, 4), (5, 6, 7), (1, 7, 3))
          >>> info.all
          ((i:1->3, j:4), (*k:(5,), *l:(6, 7)), (*l:(1, 7)->(6, 7), i:3))
          >>> info.unique
          {'i': i:3, 'j': j:4, 'k': *k:(5,), 'l': *l:(6, 7)}

          Internally `check_shapes()` calls `parse_variable_ndim()`,
          which determines the number of dimensions for variable subscripts by least squares.
          If this is successful, checks if each subscript is consistent,
          then finnaly raises error for all inconsistencies at once.

          Diving into the details of the first item:

          >>> item = info.all[0][0]
          >>> item.name  # the name of the subscript
          'i'
          >>> item.is_variable  # whether the subscript is variable (starts with "*")
          False
          >>> item.shape_current  # the current shape of the subscript
          (1,)
          >>> item.shape_broadcasted  # the broadcasted shape of the subscript
          (3,)

          Not enough information to determine variable subscript ndims:

          >>> import pytest
          >>> with pytest.raises(InconsistentNdimErrorMultipleSolutions, match="number of variables"):
          ...     check_shapes("*i*j", (1, 1))
          >>> with pytest.raises(InconsistentNdimErrorMultipleSolutions, match="rank"):
          ...     check_shapes("*i*j,*i*j", (1, 1), (1, 1))

          No solution to determine variable subscript ndims:

          >>> with pytest.raises(InconsistentNdimErrorNoSolutions, match="residuals"):
          ...     check_shapes("*i,*i", (1, 1), (1, 1, 1))
          >>> with pytest.raises(InconsistentNdimErrorNoSolutions, match="negative"):
          ...     check_shapes("*ij", ())

          Does not match:
          >>> with pytest.raises(InconsistentShapeError):
          ...     check_shapes("ij,*k*l,*li", (3, 4), (5, 6), (1, 7, 3))

          """
          ...
      ```

  - **Importing Numpy allowed only for constants**: Never import `numpy` directly, unless for constants like `np.pi` for context when `xp` is not available.
  - **Type promotion**: Understand Type promotion rules, i.e. float64 + complex64 -> complex128. Mixed integer and floating-point type promotion rules are not specified, but we assume that for every floating (including complex) dtype x, x + (int type) -> x.
  - **Type promotion: no wrapping Python scalars**: Avoid wrapping `int` arrays, Python scalars with `xp.asarray()` but use them directly (because it is redundant). The exception is when you need to divide int by int (in this case you only need to wrap one of them).
  - **Type promotion: avoid conversion as much as possible and make it inline**:Avoid creating variables for `int` version, `float` version, `complex` version of the same array as much as possible.
  - **Type promotion**: The type can be converted by `xp.astype(x, dtype, /)`.
  - **Avoid float when possible**: Avoid expressing integer as float. `1` instead of `1.0` whenever possible.
  - **Type promotion: Scipy -> input cpu, output asarray**: As an exception, if Scipy functions are needed (e.g. `scipy.special.yv`), do `xp.asarray(yv(xp.asarray(x, device="cpu")), device=x.device, dtype=x.dtype)`. (Do not specify dtype in the inner `asarray`). Note that every array has property `device` (including NumPy >= 2.0), you don't need `getattr`.
  - **Expand dimensions using []**: When expanding dimensions, prefer something like `x[(...,) + (None,) * n + (slice(None),) * m]` or `x[(slice(None),) * m + (None,) * n + (...,)]`. Never use `xp.reshape()` or `xp.expand_dims()` when the above method is possible. Avoid creating "expanded version` and "non-expanded version" of the same array, unless both of them are frequently used.
  - **Type promotion: no complex -> float (terrible undetectable bug)** Do not `asarray(x, dtype=dtype)` if `x` is complex dtype and `dtype` is float. This sometimes happens when `dtype` is an variable (trying to make function that is any-float compatible e.g. float32 -> float32 / complex64, complex64 -> complex64, float64 -> float64 / complex128, complex128 -> complex128). It will be equivalent to `xp.real(x)` which may cause severe numerical issues. Instead do `xp.asarray(x, dtype=xp.result_type(dtype, 1j))`.

## Tests

- Tests should be also array API compatible.
  - In `tests/conftest.py`, there are fixtures named `xp: ArrayNamespace`, `device: Any`, `dtype: Any`. Any test function must use these fixtures as arguments, and create arrays (i.e. `zeros()`) within the test function.
  - If there is an array passed as fixture / parameter to the test function. wrap it with `xp.asarray(..., device=device, dtype=dtype)` at the beginning of the test function. If it is a scalar, never wrap it but use it directly.
  - Parameterize tests using `pytest.mark.parametrize`.
  - Do not try to read the contents of `tests/conftest.py`.
  - To run python commands, use `uv run python`, `uv run pytest`, etc. Never run `python` directly. You may run `uv run pytest` on your own.
