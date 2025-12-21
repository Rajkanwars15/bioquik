# Reports

Bioquik writes all outputs to the specified output directory.

---

## Per-file motif counts

For each FASTA file processed, Bioquik generates:

```
<filename>_motif_counts.csv
```

Each CSV contains motif counts for that file.

---

## Combined reports

```python
from bioquik.reports import combine_csv

df = combine_csv(out_dir)
```

This reads all `*_motif_counts.csv` files in `out_dir` and concatenates them.

---

## Writing summaries

```python
from bioquik.reports import write_summary

write_summary(df, out_dir, json_out=True)
```

Outputs:
- `combined_counts.csv` (always)
- `summary.json` (optional)

---

## Plots

If plotting is enabled, Bioquik produces:
- A bar chart of total motif counts
- A heatmap of motif counts by FASTA file