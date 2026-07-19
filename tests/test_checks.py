# tests/test_checks.py
"""
    Pruebas unitarias para la verificacion de archivos y carpetas requeridos.
"""

from pathlib import Path

from readiness_cli.checks import (
    check_file_exists,
    check_dir_exists,
    run_file_checks,
)

from readiness_cli.models import Status

def _make_complete_project(base_path: Path) -> None: 
    """
        Crea una estructura de proyecto que cumple todos los requisitos.
    """

    (base_path / "README.md").write_text("# Proyecto de prueba")
    (base_path / "pyproject.toml").write_text("[project]\nname= 'demo'")
    (base_path / ".gitignore").write_text(".venv/")
    (base_path / "tests").mkdir()

# --- Caso Exitoso ---

def test_run_file_checks_all_pass_when_project_is_complete(tmp_path):
    """
        Un proyecto con todos los archivos/carpets requeridos debe dar PASS en todo.
    """

    _make_complete_project(tmp_path)

    results = run_file_checks(tmp_path)

    assert len(results) == 4
    assert all(r.status == Status.PASS for r in results)

# --- Casos de Error ---

def test_checkk_file_exists_fails_when_readme_missing(tmp_path):
    """
        Un archivo requerido ausente debe reportarse como FAIL, no lanzar excepcion.
    """

    result = check_file_exists(tmp_path, "README.md")

    assert result.status == Status.FAIL
    assert "README.md" in result.message

def test_check_dir_exists_fails_when_tests_dir_missing(tmp_path):
    """
        Una carpeta requerida ausente debe reportarse como FAIL, no lanzar excepcion.
    """

    result = check_dir_exists(tmp_path, "tests")

    assert result.status == Status.FAIL
    assert "tests" in result.message

def test_run_file_checks_on_nonexistent_path_does_not_raise(tmp_path):
    """
        Verificar una ruta que no existe en absolut no debe lanzar excepcion,
        sino devolver resultados FAIL para cada elemento esperado.
    """

    fake_path = tmp_path / "esta-carpeta-no-existe"

    results = run_file_checks(fake_path)

    assert len(results) == 4
    assert all(r.status == Status.FAIL for r in results)

def test_run_file_checks_partial_project_mixes_pass_and_fail(tmp_path):
    """
        Un proyecto incompleto (solo README) debe reportar PASS para lo que
        existe y FAIL para lo que falta, sin que un fallo detenga el resto.
    """

    (tmp_path / "README.md").write_text("# Solo README")

    results = run_file_checks(tmp_path)
    by_name = {r.name: r.status for r in results}

    assert by_name["file_README.md"] == Status.PASS
    assert by_name["file_pyproject.toml"] == Status.FAIL
    assert by_name["file_.gitignore"] == Status.FAIL
    assert by_name["dir_tests"] == Status.FAIL