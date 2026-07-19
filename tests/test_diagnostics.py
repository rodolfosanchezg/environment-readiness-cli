# tests/test_diagnostics.py

"""
    Pruebas unitarias para el diagnostico del entorno en ejecucion.
"""

from readiness_cli.diagnostics import (
    check_python_version,
    check_operating_system,
    run_diagnostics,
)

from readiness_cli.models import Status

# --- Caso Exitoso --- 

def test_check_python_version_passes_with_low_minimum():
    """
        Con una version minima trivialmente baja, siempre debe dar PASS.
    """

    result = check_python_version(minimum=(3,0))

    assert result.status == Status.PASS
    assert "version" in result.details

# --- Caso de error / advertencia ---

def test_check_python_version_warns_with_unreaachably_high_minimum():
    """
        Con una version minima imposible de cumplir, debe dar WARN, no fallar.
    """

    result = check_python_version(minimum=(99,0))

    assert result.status == Status.WARN
    assert "99.0" in result.message

def test_check_operating_system_return_pass_and_details():
    result = check_operating_system()

    assert result.status == Status.PASS
    assert "system" in result.details
    assert "machine" in result.details

def test_run_diagnostics_returns_four_results_without_raising():
    """
        run_diagnostics no debe lanzar excepciones y debe cubrir la 4 verificaciones.
    """

    results = run_diagnostics()

    assert len(results) == 4
    names = {r.name for r in results}
    assert names == {
        "python_version",
        "operating_system",
        "interpreter_path",
        "virtualenv_active",
    }