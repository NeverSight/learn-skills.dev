---
name: go-tdd-baby-steps
description: "v1.0.21 — TDD with baby steps for Go. Use when writing tests, doing TDD, practicing red-green-refactor, or when test cycles feel too large and risky. Also use when the user asks about incremental test development, test-first workflow, or wants help breaking a feature into small testable steps. Covers table-driven tests, testify, t.Run subtests, t.Helper, transformation priority premise, and incremental test progression."
---

# Go TDD Baby Steps

Test-Driven Development using the smallest possible increments, with Go idioms.

## Three Laws of TDD

1. **Don't write production code** until you have a failing test
2. **Don't write more test code** than is sufficient to fail (compilation failures count)
3. **Don't write more production code** than is sufficient to pass the currently failing test

These laws create a tight feedback loop: write a tiny test, watch it fail, write just enough code to pass.

## Red-Green-Refactor

1. **Red** - Write a small test that fails
2. **Green** - Write the minimal code to make it pass
3. **Refactor** - Clean up while keeping tests green

Each cycle should take **~2 minutes**. If longer, the step is too big.

### The Revert Rule

If stuck or code is getting messy:

1. **Revert** to the last green state
2. **Rethink** the approach
3. **Take a smaller step**

Never debug longer than the cycle itself. Revert instead.

## Baby Steps with Go Table-Driven Tests

Build up the test table incrementally — each row adds ONE behavior.

### Step 1: Zero/empty case

```go
func TestParseAmount(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    int
		wantErr bool
	}{
		{name: "empty string", input: "", want: 0, wantErr: true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseAmount(tt.input)
			if tt.wantErr {
				require.Error(t, err)
				return
			}
			require.NoError(t, err)
			assert.Equal(t, tt.want, got)
		})
	}
}
```

Production code (fake it):

```go
func ParseAmount(s string) (int, error) {
	return 0, errors.New("empty")
}
```

### Step 2: Single simple case

Add one row, generalize production code:

```go
{name: "single digit", input: "5", want: 5},
```

```go
func ParseAmount(s string) (int, error) {
	if s == "" {
		return 0, errors.New("empty input")
	}
	return strconv.Atoi(s)
}
```

### Step 3: Edge cases, one at a time

```go
{name: "negative number", input: "-3", want: -3},
{name: "leading zeros", input: "007", want: 7},
{name: "non-numeric", input: "abc", wantErr: true},
```

Each row forces at most one production code change.

## Baby Steps with Subtests and Helpers

Use `t.Run` for progression and `t.Helper` for shared assertions:

```go
func assertStack(t *testing.T, s *Stack, wantLen int, wantEmpty bool) {
	t.Helper()
	assert.Equal(t, wantLen, s.Len())
	assert.Equal(t, wantEmpty, s.IsEmpty())
}

func TestStack(t *testing.T) {
	t.Run("new stack is empty", func(t *testing.T) {
		s := NewStack()
		assertStack(t, s, 0, true)
	})

	t.Run("push one element", func(t *testing.T) {
		s := NewStack()
		s.Push(42)
		assertStack(t, s, 1, false)
	})

	t.Run("pop returns last pushed", func(t *testing.T) {
		s := NewStack()
		s.Push(42)
		got, err := s.Pop()
		require.NoError(t, err)
		assert.Equal(t, 42, got)
		assertStack(t, s, 0, true)
	})

	t.Run("pop empty stack returns error", func(t *testing.T) {
		s := NewStack()
		_, err := s.Pop()
		require.Error(t, err)
	})
}
```

Each `t.Run` block is a baby step — one new behavior per subtest.

## Baby Steps in Production Code

### Fake it till you make it

1. **Return a constant** to pass the first test
2. **Replace constant** with a variable when the second test forces it
3. **Generalize** only when duplication demands it

### Transformation Priority Premise

Prefer simpler transformations:

1. Constant → variable
2. Unconditional → conditional (`if`)
3. Scalar → collection
4. Statement → recursion/iteration
5. Value → mutated value

Choose the transformation that requires the least code change.

## Signals

### Doing it right

- Each cycle is ~2 minutes
- Tests drive design decisions
- Code grows incrementally, never in big leaps
- Refactoring happens in green state only
- You can revert any step and lose at most 2 minutes of work

### Doing it wrong

- Writing multiple tests before making them pass
- Writing production code "you'll need later"
- Skipping the refactor step
- Tests require large production code changes
- Cycles regularly exceed 5 minutes
- Reluctance to revert because "too much work to lose"

## Key Principles

- **Smaller steps are always available.** If stuck, the step is too big.
- **The tests are the design tool.** Let them guide structure.
- **Refactoring is not optional.** Clean code emerges from the refactor step, not the green step.
- **Working software at every step.** After each green, the code works and is shippable.
- **Speed comes from small steps.** Tiny steps are faster than big ones because you spend less time debugging.
