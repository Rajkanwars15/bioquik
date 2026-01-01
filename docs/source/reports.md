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

Bioquik includes optional visualization utilities for summarizing motif distributions.

### Enabling Visualization

Plotting functionality is not included in the minimal installation. To enable visual outputs, install Bioquik with the visualization extra:

```
pip install bioquik[viz]
```

This installs Matplotlib, which is required for rendering figures.

### What Bioquik Generates

When plotting is enabled, the following images are created in the output directory:

- `motif_distribution.png`: Bar chart of total motif counts aggregated across input FASTA files.
- `motif_heatmap.png`: Heatmap showing how motif counts vary by file.

These are created automatically by the CLI when analysis completes.

### Using Plotting Functions Programmatically

If you're working interactively in Python, you can directly generate the same plots:

```python
from bioquik.plotter import plot_distribution, plot_heatmap
from bioquik.reports import combine_csv

# Combine outputs from prior motif scans
df = combine_csv(out_dir)

# Generate the plots
plot_distribution(df, out_dir)
plot_heatmap(df, out_dir)
```

Both functions will save images directly to `out_dir`, allowing integration into custom pipelines.

Visualization is entirely optional and does not affect core counting or summary reporting functionality.