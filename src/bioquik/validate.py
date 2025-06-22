from pathlib import Path
from typing import List
import typer
from rich import print

def validate_patterns(patterns: str) -> List[str]:
    """
    Ensure at least one pattern includes 'CG' and split into a list.
    """
    if "CG" not in patterns:
        print("[red]Error: patterns must include 'CG' anchor")
        raise typer.Exit(code=1)
    return [p.strip() for p in patterns.split(",") if p.strip()]

def validate_dir(path: Path, name: str) -> None:
    """
    Ensure that `path` exists and is a directory.
    """
    if not path.is_dir():
        print(f"[red]Error: {name} directory '{path}' not found")
        raise typer.Exit(code=1)
