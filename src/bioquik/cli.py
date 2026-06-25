from __future__ import annotations

import os
import shutil
from pathlib import Path

import typer
from rich import print

from .plotter import plot_distribution, plot_heatmap
from .processor import run_count
from .reports import combine_csv, write_summary
from .validate import validate_dir, validate_patterns

app = typer.Typer(
    help="bioquik — an attempt to make biotech faster and easier ;) ",
    add_help_option=True,
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def _root(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        raise typer.Exit()


@app.command(help="Count CG-anchored motifs in FASTA files and generate reports.")
def count(
    patterns: str = typer.Option(
        ..., help="Comma-separated wildcard patterns (must include 'CG')"
    ),
    seq_dir: Path = typer.Option(Path("seq"), help="Directory containing .fasta files"),
    workers: int = typer.Option(os.cpu_count(), help="Number of worker processes"),
    out_dir: Path = typer.Option(Path("bioquik_results"), help="Directory for results"),
    json_out: bool = typer.Option(False, help="Also write combined JSON summary"),
    plot: bool = typer.Option(False, help="Generate distribution & heatmap plots"),
) -> None:
    # 1) Validate inputs
    try:
        pattern_list: list[str] = validate_patterns(patterns)
        validate_dir(seq_dir, "sequence")
    except ValueError as e:
        print(f"[red]Error: {e}")
        raise typer.Exit(code=1) from None
    # clear any previous results to avoid mixing old CSVs
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 2) Process FASTAs in parallel
    run_count(pattern_list, seq_dir, out_dir, workers)

    # 3) Combine & write reports
    df_all = combine_csv(out_dir)
    write_summary(df_all, out_dir, json_out=json_out)

    # 4) Optionally plot
    if plot:
        plot_distribution(df_all, out_dir)
        plot_heatmap(df_all, out_dir)

    print(f"[green]Finished. Results in {out_dir}")


if __name__ == "__main__":
    app()
