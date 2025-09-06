# Contributing to bioquik

Thanks for your interest in contributing!  
This document explains how to set up a development environment, run tests, and build the docs.

---

## 1. Setup

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/Rajkanwars15/bioquik.git
cd bioquik
python -m venv venv
```

Activate the `venv` 
1. on macOS/Linux
```shell
source venv/bin/activate
```
2. on Windows
```shell
venv\Scripts\activate
```

Install dependencies (including dev and docs):
```shell
pip install -e ".[dev,docs]"
```

## 2. Running Tests
We use pytest with coverage reporting:
```shell
pytest -q --cov=bioquik
```

## 3. Code Style
We use [ruff](https://docs.astral.sh/ruff/) and pre-commit hooks:
```shell
ruff check .
pre-commit install   # install git hooks
```

Run formatters before committing:
```shell
ruff check . --fix
```

## 4. Building Documentation

We use [Sphinx](https://www.sphinx-doc.org/en/master/) with MyST markdown:

Generate API docs
```shell
sphinx-apidoc -o docs/source/api src/bioquik
```

Build HTML docs
```shell
sphinx-build -b html docs/source docs/build
```

Open the docs:
```shell
open docs/build/index.html   # macOS
```

## 5. Submitting Changes
1.	Fork the repo and create a feature branch. 
2. Add tests for any new functionality. 
3. pytest and ensure all tests pass. 
4. mit a pull request with a clear description.
