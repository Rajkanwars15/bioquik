# Quickstart

This guide gets you up and running with **Bioquik**.

---

## Command-line usage

Bioquik operates on a directory of FASTA files.

```shell
bioquik count \
  --patterns ATG,CG* \
  --seq-dir data/fasta \
  --out-dir results \
  --workers 4 \
  --plot
```

### Parameters

- `--patterns`: Comma-separated motif patterns (wildcards supported)
- `--seq-dir`: Directory containing `.fasta` files
- `--out-dir`: Output directory for reports
- `--workers`: Number of parallel worker processes
- `--plot`: Generate plots

---

## Python usage

```python
from pathlib import Path
from bioquik.processor import run_count

run_count(
    pattern_list=["ATG", "CG*"],
    seq_dir=Path("data/fasta"),
    out_dir=Path("results"),
    workers=4,
)
```

### Notes

- `run_count` processes **all FASTA files** in `seq_dir`
- Results are written to `out_dir`
- The function returns `None`

---

## Single-file processing (advanced)

```python
from bioquik.fasta_worker import process_fasta_file
from bioquik.motifs import build_pattern_to_motifs

mapping = build_pattern_to_motifs(["ATG"])

csv_path = process_fasta_file(
    "example.fasta",
    mapping,
    out_dir="results"
)
```