# src/readiness_cli/report.py
from dataclasses import dataclass
from .models import CheckResult, Status

@dataclass
class Report: 
    results: list[CheckResult]
    summary: dict[Status, int]

def build_report(results: list[CheckResult]) -> Report:
    """
        Agrupa resultados y calcula el resumen PASS/WARN/FAIL.
    """

def export(report: Report, fmt: str, path: str | None = None) -> str:
    """
        Exporta ell reporte coomo text plano o JSON. 
        Si path es None, retorna el string.
    """