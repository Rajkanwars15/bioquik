# Bioquik Documentation

Welcome to **Bioquik**, a high-performance toolkit for counting DNA sequence motifs across large FASTA datasets.

Bioquik is designed for **batch analysis**. It processes directories of FASTA files in parallel and writes results to disk as CSV, JSON, and optional plots.

---

## Installation

```bash
pip install bioquik           # core
pip install bioquik[viz]      # + matplotlib for plots
```

---

## Quickstart

See the [Quickstart](quickstart.md) guide for command-line and Python API examples.

---

## Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

quickstart
validation
reports
benchmarks
```

```{toctree}
:maxdepth: 2
:caption: Architecture

architecture
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/modules
```
