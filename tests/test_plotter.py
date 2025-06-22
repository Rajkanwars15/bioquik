import pandas as pd
from pathlib import Path

import pytest

from bioquik.plotter import plot_distribution

def test_plot_distribution(tmp_path):
    df = pd.DataFrame([
        {"Motif": "AA", "Count": 5},
        {"Motif": "BB", "Count": 2},
    ])
    out = tmp_path / "out"
    out.mkdir()

    # should run without error and create .png
    plot_distribution(df, out)
    assert (out / "motif_distribution.png").exists()
