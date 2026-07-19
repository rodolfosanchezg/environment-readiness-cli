# tests/test_report.py
"""
    Pruebas unitarias para la construccion y exportacion del reporte.
"""

import json

from readiness_cli.models import CheckResult, Status
from readiness_cli.report import build_report, export

def _results_all_pass():
    return [
        CheckResult(name="check_a", status=Status.PASS, message="ok a"),
        CheckResult(name="check_b", status=Status.PASS, message="OK b"),
    ]

def _results_mixed():
    return [
        CheckResult(name="check_a", status=Status.PASS, message="ok a"),
        CheckResult(name="check_b", status=Status.WARN, message="advertencia b"),
        CheckResult(name="check_c", status=Status.FAIL, message="fallo c"),
    ]

# --- Caso Exitoso ---

def test_build_report_overall_status_pass_when_no_fail_or_warn():
    report = build_report(_results_all_pass())

    assert report.overall_status == Status.PASS
    assert report.summary["PASS"] == 2
    assert report.summary["FAIL"] == 0

def test_build_report_overall_status_fail_when_any_fail_present():
    """
        La presencia de un solo FAIL debe marcar el reporte completo como FAIL,
        sin importar que haya otros PASS o WARN.
    """

    report = build_report(_results_mixed())

    assert report.overall_status == Status.FAIL
    assert report.summary["FAIL"] == 1
    assert report.summary["WARN"] == 1

def test_build_report_handles_empty_results_without_raising():
    """
        Una lista vacia de resultados no debe lanzar excepcion.
    """

    report = build_report([])

    assert report.overall_status == Status.PASS
    assert report.summary["PASS"] == 0

def test_export_invalid_format_raises_value_error():
    """
        Un formato no soportado debe fallar de forma explicita y controlada.
    """

    report = build_report(_results_all_pass())

    try:
        export(report, fmt="xml")
        assert False, "Se esperaba ValueError para formato no soportado."
    except ValueError as exc:
        assert "xml" in str(exc)

def test_export_json_produces_valid_parseable_json(tmp_path):
    """
        El export a JSON debe generar un archivo con JSON valiido y consistente
        con losdatos del reporte.
    """

    report = build_report(_results_mixed())
    output_file = tmp_path / "reporte.json"

    export(report, fmt="json", path=str(output_file))

    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["overall_status"] == "FAIL"
    assert len(data["results"]) == 3