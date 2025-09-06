# bioquik Documentation

Welcome to **bioquik** docs!

---

## 1. Install

```shell
pip install bioquik
```

## 2. Quickstart
### CLI
```shell
bioquik --help
bioquik count --input sequences.fa --k 5 --out counts.csv
```
### Python API
```python
from bioquik.processor import run_count
summary = run_count("data/example.fa", motifs=["ATG"])
```

## 3. Contents
```{toctree}
:maxdepth: 2
:caption: Tutorials

quickstart
validation
reports
```
```{toctree}
:maxdepth: 2
:caption: API Reference

api/modules
```
