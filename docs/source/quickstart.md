# Quickstart

This tutorial will get you up and running with **bioquik** in just a few minutes.

## Count k-mers from FASTA

Suppose you have a FASTA file called `sequences.fa`:

```shell
bioquik count --input sequences.fa --k 5 --out counts.csv
```

This command counts all 5-mers in the file and writes the results to counts.csv.

## Use from Python

```python
from bioquik.processor import run_count

summary = run_count("sequences.fa", motifs=["ATG", "TATA"])
print(summary)
```

The summary is a pandas.DataFrame with counts for the motifs you requested.