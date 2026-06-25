# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic 
Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.0] - 2026-06-25

### Added
- `run_count` exported from the top-level `bioquik` package (`from bioquik import run_count`)
- `__all__` defined in all public modules (`motifs`, `plotter`, `processor`, `reports`, `validate`, `wavelettree`)
- `__version__` now read from installed package metadata via `importlib.metadata` instead of a hard-coded string
- Python 3.13 classifier and experimental CI matrix entry; `tox.ini` for local multi-version testing
- Multi-version CI matrix (Python 3.9, 3.10, 3.11, 3.12, 3.13) with `fail-fast: false`
- Benchmark suite (`benchmarks/`) comparing FM-index vs naive `str.count()` baseline
- Fixture generator (`benchmarks/generate_fixtures.py`) for reproducible synthetic FASTA files
- Cross-validation test suite (`tests/test_correctness.py`) asserting FM-index counts match naive counts
- New tests for `WaveletTree.rank`, `FMIndex.locate`, `motifs.build_pattern_to_motifs`, and CLI edge cases
- GitHub issue and PR templates (`.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`)
- Pre-commit config (`.pre-commit-config.yaml`) with `ruff` and `ruff-format` hooks
- `benchmarks.md` documentation page; `index.md` toctree updated

### Changed
- `validate_patterns` and `validate_dir` now raise `ValueError` instead of calling `typer.Exit`; the CLI layer catches `ValueError` and exits with code 1 — library callers should catch `ValueError` directly
- `matplotlib` version pin relaxed from `>=3.10.3` to `>=3.8` to restore Python 3.9 compatibility
- `[tool.pytest.ini_options]` added to `pyproject.toml` with `pythonpath = ["."]` so the `benchmarks` package is importable in CI without extra installation steps
- `ruff` lint and coverage configuration consolidated into `pyproject.toml`
- Type annotations modernized from `typing.List`/`typing.Dict` to built-in `list`/`dict` throughout
- Documentation URL updated from GitHub README to `https://bioquik.readthedocs.io/`

### Fixed
- **`motifs.py`** — `build_pattern_to_motifs` was silently undercounting motifs for patterns with wildcards on both sides (e.g. `**CG**`). `pre_vars`/`post_vars` were generators that exhausted after the first outer iteration, producing only `4^pre_cg` motifs instead of the correct `4^(pre_cg + post_cg)`. Fixed by materialising both as lists before the nested loop.
- **`wavelettree.py`** — `WaveletTree._rank1` returned stale rank counts for any position beyond `sample_rate` characters into the sequence. An off-by-one `[0]` initialiser in `prefix_ranks` shifted all sample indices by one. Fixed by starting `prefix_ranks` as an empty list.
- **`plotter.py`** — `plot_heatmap` raised `TypeError` when called with a mixed string/int DataFrame (as produced by `combine_csv`). `df.to_numpy().sum()` was replaced with a column-aware check: `df["Count"].sum()` for long-form or `df.select_dtypes("number").values.sum()` for wide-form.

## [0.1.1] - 2025-12-??  <!-- replace ?? with appropriate day once known -->

### Added
- Optional `viz` extra dependency for visualization support
- Test coverage for heatmap plotting

### Changed
- Lazy import of matplotlib to prevent forced kernel restart

### Fixed
- Heatmap plotting now supports both long-form and wide-form inputs without errors

## [0.1.0] - 2025-09-07

First public repo