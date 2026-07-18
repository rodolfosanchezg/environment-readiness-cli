# src/readiness_cli/checks.py
from pathlib import Path
from .models import CheckResult

REQUIRED_FILES = ["README.md", "pyproject.toml", ".gitignore"]
REQUIRED_DIRS = ["tests"]

def run_file_checks(base_path: Path) -> list[CheckResult]:
    """
        Verifica existencia de archivos y carpetas requeridas en base_path.
    """