from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_distribution(df: pd.DataFrame, out_dir: Path) -> None:
    """
    Bar chart of total counts per motif.
    """
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
    if df.empty or df["Count"].sum() == 0:
        plt.figure()
        plt.savefig(out_dir / "motif_heatmap.png")
        plt.close()
        return

    pivot = df.pivot_table(
        index="Motif",
        columns=lambda r: Path(r.name).stem,
        values="Count",
        fill_value=0,
    )

    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=90)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Count")
    plt.tight_layout()
    plt.savefig(out_dir / "motif_heatmap.png")
    plt.close()
