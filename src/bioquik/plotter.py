from pathlib import Path
import pandas as pd


def plot_distribution(df: pd.DataFrame, out_dir: Path) -> None:
    """
    Bar chart of total counts per motif.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Install with `pip install bioquik[viz]` to enable visualization.")
    # Nothing to plot?  Save an empty figure so downstream scripts/tests succeed.
    if df.empty or df["Count"].sum() == 0:
        plt.figure()
        plt.savefig(out_dir / "motif_distribution.png")
        plt.close()
        return

    totals = df.groupby("Motif")["Count"].sum().sort_values(ascending=False)

    plt.figure()
    totals.plot(kind="bar")
    plt.xlabel("Motif")
    plt.ylabel("Total Count")
    plt.tight_layout()
    plt.savefig(out_dir / "motif_distribution.png")
    plt.close()


def plot_heatmap(df: pd.DataFrame, out_dir: Path) -> None:
    """
    Heatmap of motif counts by file.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Install with `pip install bioquik[viz]` to enable visualization.")
    if df.empty or df.to_numpy().sum() == 0:
        plt.figure()
        plt.savefig(out_dir / "motif_heatmap.png")
        plt.close()
        return

    # Support both long-form (Motif/Count) and wide-form dataframes
    if "Motif" in df.columns and "Count" in df.columns:
        pivot = df.pivot_table(
            index="Motif",
            columns=lambda r: Path(r).stem if isinstance(r, str) else r,
            values="Count",
            fill_value=0,
        )
    else:
        # Treat dataframe as wide-form: rows = files, cols = motifs
        pivot = df.copy()
        pivot.index = [Path(str(i)).stem for i in pivot.index]

    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=90)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Count")
    plt.tight_layout()
    plt.savefig(out_dir / "motif_heatmap.png")
    plt.close()
