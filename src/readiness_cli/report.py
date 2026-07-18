# src/readiness_cli/report.py
"""
    Construye y presenta el reporte consolidado de diagnostico.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .models import CheckResult, Status

import json
from pathlib import Path


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

def _format_as_text(report: Report) -> str:

    """
        Genera una representacion en texto plano, legible por humanos.
    """

    lines = [
        "=" * 50,
        "REPORTE DE PREPARACION DEL ENTORNO",
        "=" * 50,
        f"Generado: {report.generated_at}",
        f"Estado general: {report.overall_status.value}",
        "",
        "Resumen:",
        f" PASS: {report.summary.get('PASS', 0)}",
        f" WARN: {report.summary.get('WARN', 0)}",
        f" FAIL: {report.summary.get('FAIL', 0)}",
        "",
        "Detalle:",
    ]

    for r in report.results:
        lines.append(f" [{r.status.value}] {r.name}: {r.message}")

    lines.append("=" * 50)
    return "\n".join(lines)

def _format_as_json(report: Report) -> str:
    """
        Genera una representacion en JSON serializable.
    """

    payload = {
        "generated_at": report.generated_at,
        "overall_status": report.overall_status.value,
        "summary": report.summary,
        "results": [
            {
                "name": r.name,
                "status": r.status.value,
                "message": r.message,
                "details": r.details,
            }
            for r in report.results
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def export(report: Report, fmt: str = "text", path: str | None = None) -> str:
    """
        Exporta el reporte como text plano o JSON. 
        Si 'path' es None, retorna el string generado sin escribir a disco.
        Si 'path' se proporciona, escribe el archivo y tambien retorno el string.
        Lanza ValueError si fmt no es 'text' ni 'json' (error de uso, no de datos).
    """

    if fmt not in ("text", "json"):
        raise ValueError(f"Formato no soportado: {fmt!r}. Usa 'text' o 'json'.")
    
    content = _format_as_text(report) if fmt == "text" else _format_as_json(report)

    if path is not None:
        output_path = Path(path)
        output_path.write_text(content, encoding="utf-8")
    
    return content