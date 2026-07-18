# src/readiness_cli/diagnostics.py
from .models import CheckResult

def run_diagnostics() -> list[CheckResult]:
    """
        Recolecta info del sistema: 
        ** Version Python
        ** SO
        ** Ruta del interprete
        ** venv activo
    """