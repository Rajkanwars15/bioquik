# Reports

After running analyses, you can combine and summarize results with **bioquik**.

## Combine multiple CSVs

```python
from bioquik.reports import combine_csv

combined = combine_csv(["counts_1.csv", "counts_2.csv"])
print(combined.head())
```

## Write a summary report

```python
from bioquik.reports import write_summary

write_summary(combined, "summary.csv")
```