# Validation

**bioquik** includes simple validation helpers to check your input files and motifs.

## Validate a directory of FASTA files

```python
from bioquik.validate import validate_dir

errors = validate_dir("data/")
if errors:
    print("Found problems:", errors)
else:
    print("All FASTA files are valid!")
```

## Validate specific patterns

```python
from bioquik.validate import validate_patterns

patterns = ["ATG", "XYZ"]
valid, invalid = validate_patterns(patterns)
print("Valid:", valid)
print("Invalid:", invalid)
```