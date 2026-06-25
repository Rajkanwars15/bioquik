# Validation

Bioquik validates inputs before processing to give clear errors early.

---

## Pattern validation

```python
from bioquik.validate import validate_patterns

patterns = validate_patterns("*CG*,**CG**")
# returns ["*CG*", "**CG**"]
```

Rules enforced:
- The input string must contain at least one `CG` anchor
- Patterns are comma-separated and stripped of whitespace
- Empty tokens are ignored

Raises `ValueError` with a descriptive message on failure — this means it is safe to call from library code as well as the CLI:

```python
try:
    patterns = validate_patterns("AAAA")
except ValueError as e:
    print(e)  # "patterns must include 'CG' anchor"
```

---

## Directory validation

```python
from pathlib import Path
from bioquik.validate import validate_dir

validate_dir(Path("data/fasta"), name="seq_dir")
```

Ensures the path exists and is a directory. Raises `ValueError` if not:

```python
try:
    validate_dir(Path("does_not_exist"), "seq_dir")
except ValueError as e:
    print(e)  # "seq_dir directory 'does_not_exist' not found"
```

---

## CLI behaviour

When called through the CLI, validation errors print a red message and exit with code 1. Library callers should catch `ValueError` directly.

---

## Common mistakes

### Patterns without a CG anchor

```python
validate_patterns("ATG,TAC")  # ValueError: patterns must include 'CG' anchor
```

Bioquik is designed for CG-anchored motif analysis. Every call must include at least one pattern containing the literal `CG`.

### Passing a FASTA file instead of a directory

```python
from bioquik import run_count
run_count(["*CG*"], Path("file.fasta"), out_dir, workers=4)
# ValueError: sequence directory 'file.fasta' not found
```

Pass the **directory** containing FASTA files, not a single file path.
