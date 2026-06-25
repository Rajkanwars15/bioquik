# Reports

Bioquik writes all outputs to the specified output directory.

---

## Per-file motif counts

For each FASTA file processed, Bioquik generates:

```
<filename>_motif_counts.csv
```

Columns: `Pattern`, `Motif`, `Count`. Only motifs with non-zero counts are written.

---

## Combined reports

```python
from bioquik.reports import combine_csv

df = combine_csv(out_dir)
```

Reads all `*_motif_counts.csv` files in `out_dir` and concatenates them into a single DataFrame.

---

## Writing summaries

```python
from bioquik.reports import write_summary

write_summary(df, out_dir, json_out=False)
```

Always writes:
- `combined_counts.csv` — full per-motif table

With `json_out=True`, also writes:
- `combined_counts.json` — motif → total count across all files

```python
write_summary(df, out_dir, json_out=True)
# creates out_dir/combined_counts.csv
# creates out_dir/combined_counts.json
```

---

## Plots

Optional visualisations require the `viz` extra:

```bash
pip install bioquik[viz]
```

### CLI

```bash
bioquik count --patterns "*CG*" --seq-dir data/ --plot
```

Generates:
- `motif_distribution.png` — bar chart of total counts per motif
- `motif_heatmap.png` — heatmap of counts by file

### Python

```python
from bioquik.plotter import plot_distribution, plot_heatmap
from bioquik.reports import combine_csv

df = combine_csv(out_dir)
plot_distribution(df, out_dir)
plot_heatmap(df, out_dir)
```

`plot_heatmap` accepts both long-form DataFrames (with `Motif`/`Count` columns, as produced by `combine_csv`) and wide-form DataFrames (rows = files, columns = motifs).
