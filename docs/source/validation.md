# Validation

Bioquik includes validation helpers to ensure inputs are correct before processing.

---

## Directory validation

```python
from pathlib import Path
from bioquik.validate import validate_dir

validate_dir(Path("data/fasta"), name="seq_dir")
```

Ensures the path exists and is a directory.

---

## Pattern validation

```python
from bioquik.validate import validate_patterns

patterns = validate_patterns("ATG,CG*")
```

Ensures:
- At least one pattern is provided
- Patterns are split correctly
- At least one pattern includes `CG`

Returns a list of validated patterns.

---

## Common mistakes

### Passing a FASTA file instead of a directory

```python
run_count(["ATG"], Path("file.fasta"), ...)
```

**Fix:** pass the parent directory containing FASTA files.

### Using unsupported keywords

```python
run_count("file.fasta", motifs=["ATG"])
```

**Fix:** use the documented signature:

```python
run_count(pattern_list, seq_dir, out_dir, workers)
```