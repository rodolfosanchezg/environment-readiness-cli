# src/readiness_cli/models.py
from dataclasses import dataclass, field 
from enum import Enum

class Status(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"

@dataclass
class CheckResult:
    name: str               # ej: "python_version", "readme_exists"
    status: Status
    message: str            # explicacion legible para el usuario
    details: dict = field(default_factory=dict)