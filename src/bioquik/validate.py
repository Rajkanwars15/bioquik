from pathlib import Path

__all__ = ["validate_patterns", "validate_dir"]


def validate_patterns(patterns: str) -> list[str]:
    """Ensure at least one pattern includes 'CG' and split into a list."""
    if "CG" not in patterns:
        raise ValueError("patterns must include 'CG' anchor")
    return [p.strip() for p in patterns.split(",") if p.strip()]


def validate_dir(path: Path, name: str) -> None:
    """Ensure that *path* exists and is a directory."""
    if not path.is_dir():
        raise ValueError(f"{name} directory '{path}' not found")
