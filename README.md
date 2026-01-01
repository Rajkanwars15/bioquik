![](./docs/img/logo-readme.png)

# bioquik

**bioquik** is a fast and extensible command-line toolkit for counting CG-anchored DNA motifs in FASTA files. Designed to accelerate bioinformatics pipelines with a simple and parallel interface.

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Docs](https://img.shields.io/badge/docs-latest-grren?logo=readthedocs)](https://bioquik.readthedocs.io/en/latest/)
[![GitHub license](https://img.shields.io/github/license/rajkanwars15/bioquik)](https://github.com/Rajkanwars15/bioquik/blob/main/LICENSE)
[![Build Status](https://github.com/rajkanwars15/bioquik/actions/workflows/test_with_coverage.yml/badge.svg)](https://github.com/rajkanwars15/bioquik/actions/workflows/test_with_coverage.yml)
[![codecov](https://codecov.io/gh/rajkanwars15/bioquik/branch/main/graph/badge.svg)](https://codecov.io/gh/rajkanwars15/bioquik)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

![Publish](https://github.com/Rajkanwars15/bioquik/actions/workflows/publish.yml/badge.svg)
[![PyPI - Version](https://img.shields.io/pypi/v/bioquik?logo=pypi)](https://pypi.org/project/bioquik/)
[![TestPyPI](https://img.shields.io/badge/TestPyPI-bioquik-informational)](https://test.pypi.org/project/bioquik/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20|3.10%20|%203.11|%203.12-blue?logo=python)](https://www.python.org/)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-v0.1.1-royalblue?logo=keepachangelog)](changelog.md)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?logo=contributorcovenant)](code_of_conduct.md)


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

For **users** (latest release from PyPI):

```bash
pip install bioquik
```

For **developers** (editable mode + dev dependencies):

```bash
git clone https://github.com/Rajkanwars15/bioquik
cd bioquik
pip install -e '.[dev,docs]'
````

## Requirements

* Python ≥ 3.9
* Linux/macOS (tested); Windows should work with minor path adjustments

## Documentation

Full docs are hosted on [Read the Docs](https://bioquik.readthedocs.io/en/latest/).

## License

This project is licensed under the terms of the [MIT License](LICENSE).


## Author

[![Static Badge](https://img.shields.io/badge/Rajkanwars15-yellow?logo=GitHub&link=https%3A%2F%2Fgithub.com%2FRajkanwars15)
](https://www.github.com/rajkanwars15)
