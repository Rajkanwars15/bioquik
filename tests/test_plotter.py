import pandas as pd


from bioquik.plotter import plot_distribution


def test_plot_distribution(tmp_path):
    df = pd.DataFrame(
        [
            {"Motif": "AA", "Count": 5},
            {"Motif": "BB", "Count": 2},
        ]
    )
    out = tmp_path / "out"
    out.mkdir()

    # should run without error and create .png
    plot_distribution(df, out)
    assert (out / "motif_distribution.png").exists()


from bioquik.plotter import plot_heatmap

def test_plot_heatmap(tmp_path):
    df = pd.DataFrame(
        {
            "AA": [3, 1],
            "BB": [0, 2],
        },
        index=["file1", "file2"],
    )
    out = tmp_path / "out_heatmap"
    out.mkdir()

    plot_heatmap(df, out)
    assert (out / "motif_heatmap.png").exists()
