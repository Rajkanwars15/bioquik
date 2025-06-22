# bioquik

**bioquik** is a fast and extensible command-line toolkit for counting CG-anchored DNA motifs in FASTA files. Designed to accelerate bioinformatics pipelines with a simple and parallel interface.

## Features

- Expand wildcard patterns (e.g. `**CG**`) into exact motifs
- Count motifs using a memory-efficient FM-index
- Parallel processing of multiple FASTA files
- Generates:
  - Per-file CSVs
  - Combined summary CSV
  - Optional JSON summary
  - Optional plots (motif distribution, frequency heatmap)
- Rich progress indicators
- Fully tested with Pytest

## Installation

To install the latest version in editable mode with development dependencies:

```bash
pip install -e '.[dev]'
````

## CLI Usage

Run the command-line interface:

```bash
bioquik --help
```

Example:

```bash
bioquik count \
  --patterns '**CG**' \
  --seq-dir path/to/fasta/files \
  --out-dir results/ \
  --json-out \
  --plot
```

## Testing

Run tests with:

```bash
pytest
```

## Requirements

* Python ≥ 3.9
* Linux/macOS (tested); Windows should work with minor path adjustments

## License

This project is licensed under the terms of the [MIT License](LICENSE).


## Author

[![Static Badge](https://img.shields.io/badge/Rajkanwars15-yellow?logo=GitHub&link=https%3A%2F%2Fgithub.com%2FRajkanwars15)
](https://www.github.com/rajkanwars15)
