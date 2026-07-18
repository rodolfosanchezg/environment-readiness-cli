# src/readiness_cli/checks.py
"""
    Verifica la existencia de archivos y carpetas requeridos en un proyecto.
"""

from pathlib import Path
from .models import CheckResult, Status

REQUIRED_FILES = ["README.md", "pyproject.toml", ".gitignore"]
REQUIRED_DIRS = ["tests"]

def check_file_exists(base_path: Path, filename: str) -> CheckResult:
    """
        Verifica si un archivo especifico existe dentro de base_path.
    """

    file_path = base_path / filename

    if file_path.is_file():
        return CheckResult(
            name=f"file_{filename}",
            status=Status.PASS,
            message=f"Archivo requerido encontrado: {filename}",
            details={"path": str(file_path)},
        )
    return CheckResult(
        name=f"file_{filename}",
        status=Status.FAIL,
        message=f"Archivo requerido no encontrado: {filename}",
        details={"expected_path": str(file_path)},
    )

def check_dir_exists(base_path: Path, dirname: str) -> CheckResult:
    """
        Verifica si una carpeta especifica existe dentro de base_path.
    """

    dir_path = base_path / dirname

    if dir_path.is_dir():
        return CheckResult(
            name=f"dir_{dirname}",
            status=Status.PASS,
            message=f"Carpeta requerida encontrada: {dirname}/",
            details={"path": str(dir_path)},
        )
    return CheckResult(
        name=f"dir_{dirname}",
        status=Status.FAIL,
        message=f"Carpeta requerida no encontrada: {dirname}/",
        details={"expected_path": str(dir_path)},
    )


def run_file_checks(base_path: Path) -> list[CheckResult]:
    """
        Ejecuta todas las verificaciones de archivos/carpetas requeridos.

        recibe base_path (no asume el directorio actual) para que la funcion sea facilmente
        probable con carpetas temporales en las pruebas unitarias.

        Ningun archivo faltante detiene la verificacion de los demas.
    """
    results: list[CheckResult] = []

    for filename in REQUIRED_FILES:
        results.append(check_file_exists(base_path, filename))

    for dirname in REQUIRED_DIRS:
        results.append(check_dir_exists(base_path, dirname))

    return results