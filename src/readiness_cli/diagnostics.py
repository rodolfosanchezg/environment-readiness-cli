# src/readiness_cli/diagnostics.py
"""
    Recolecta informacion del entorno de ejecucion
    ** Interprete
    ** SO
    ** venv
"""

import platform
import sys
import os

from .models import CheckResult, Status

def check_python_version(minimum: tuple[int, int] = (3, 9)) -> CheckResult:
    """
        Reporta la version de Python activa y valida conta una version minima.
    """
    current = sys.version_info[:2]
    version_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    if current >= minimum:
        return CheckResult(
            name="python_version",
            status=Status.PASS,
            message=f"Version de Python detectada: {version_str}",
            details={"version": version_str, "minimum_required": f"{minimum[0]}.{minimum[1]}"},
        )
    return CheckResult(
        name="python_version",
        status=Status.WARN,
        message=(
            f"Version de Python {version_str} es menor a la minima recomendada "
            f"({minimum[0]}.{minimum[1]})"
        ),
        details={"version": version_str, "minimum_required": f"{minimum[0]}.{minimum[1]}"},
    )

def check_operating_system() -> CheckResult:
    """
        Reporta el sistema operativo y la arquicture detectados.
    """
    system = platform.system()
    release = platform.release()
    machine = platform.machine()

    return CheckResult(
        name="operating_system",
        status=Status.PASS,
        message=f"Sistema operativo detectado: {system} {release} ({machine})",
        details={"system": system, "release": release, "machine": machine},
    )

def check_interpreter_path() -> CheckResult:
    """
        Reporta la ruta absoluta del interprete de Python en ejecucion.
    """
    interpreter_path = sys.executable

    if interpreter_path and os.path.exists(interpreter_path):
        return CheckResult(
            name="interpreter_path",
            status=Status.PASS,
            message=f"Ruta del interprete: {interpreter_path}",
            details={"path": interpreter_path},
        )
    return CheckResult(
        name="interpreter_path",
        status=Status.WARN,
        message="No fue posible determinar una ruta valida del interprete activo.",
        details={"path": interpreter_path or "desconocida"},
    )

def check_virtualenv_active() -> CheckResult:
    """
        Detecta si el programa se esta ejecutando dentro de un entorno virtual.
    """

    in_venv = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        or bool(os.environ.get("VIRTUAL_ENV"))
    )

    if in_venv:
        return CheckResult(
            name="virtualenv_active",
            status=Status.PASS,
            message="El programa se esta ejecutando dentro de un entorno virtual.",
            details={"venv_path": os.environ.get("VIRTUAL_ENV", sys.prefix)},
        )
    return CheckResult(
        name="virtualenv_active",
        status=Status.WARN,
        message="No se detecto un entorno virtual activo. Se recomienda usar uno.",
        details={},
    )

def run_diagnostics() -> list[CheckResult]:
    """
        Ejecuta todos los diagnosticos de sistema y retorna la lista de resultados. 
        Ningun chequeo individual detiene la ejecucion de los demas.
        Cada funcion captura su propio caso de exito o advertencia y returna un CheckResult.
    """
    return [
        check_python_version(),
        check_operating_system(),
        check_interpreter_path(),
        check_virtualenv_active(),
    ]