# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Path setup --------------------------------------------------------------
# Add src directory so autodoc can import bioquik
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
project = "bioquik"
copyright = "2025, Rajkanwar Singh"
author = "Rajkanwar Singh"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",          # Markdown support
    "sphinx.ext.autodoc",   # API docs from docstrings
    "sphinx.ext.napoleon",  # Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "linkify",
]

master_doc = "index"