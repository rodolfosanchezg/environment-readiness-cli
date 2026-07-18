# src/readiness_cli/report.py
"""
    Construye y presenta el reporte consolidado de diagnostico.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .models import CheckResult, Status

@dataclass
class Report: 
    results: list[CheckResult]
    summary: dict[str, int] = field(default_factory=dict)
    generated_at: str = ""

    @property
    def overall_status(self) -> Status:
        """
            El estado general del reporte: 
            FAIL si hay algun fallo.
            WARN si hay alguna advertencia sin fallo.
            PASS si todo es correcto.
        """

        if self.summary.get(Status.FAIL.value, 0) > 0:
            return Status.FAIL
        if self.summary.get(Status.WARN.value, 0) > 0:
            return Status.WARN
        return Status.PASS

def build_report(results: list[CheckResult]) -> Report:
    """
        Agrupa resultados individuales y calcula el resumen PASS/WARN/FAIL.
        
        No falla si la lista de resultados esta vacia o si contiene errores parciales.

        Cada CheckResult ya llega resuelto desde diagnostics/checks.
    """
    summary = {status.value: 0 for status in Status}

    for result in results:
        summary[result.status.value] += 1

    return Report(
        results=results,
        summary=summary,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

"""
def export(report: Report, fmt: str, path: str | None = None) -> str:
    
        Exporta ell reporte coomo text plano o JSON. 
        Si path es None, retorna el string.
    
"""