# src/readiness_cli/cli.py

"""
    Punto de entrada en linea de comandos para Environment Readiness CLI.
"""

import argparse
import sys
from pathlib import Path

from .diagnostics import run_diagnostics
from .checks import run_file_checks
from .report import build_report, export

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="readiness-cli",
        description="Evalua si el entorno actual esta listo para ejecutar un proyecto Python."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Ruta del proyecto a evaluar (por defecto: directorio actual).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Formato de salida del reporte (por defecto: text).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Ruta de archivo donde guardar el report. Si se omite, se imprime en pantalla."
    )
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    base_path = Path(args.path)

    results = run_diagnostics() + run_file_checks(base_path)
    report = build_report(results)
    content = export(report, fmt=args.format, path=args.output)

    if args.output:
        print(f"Reporte guardado en: {args.output}")
    else:
        print(content)

    # Codigo de salida: 0 si PASS o WARN, 1 si hay algun FAIL.
    # Esto permite usar la CLI en pipelines de CI sin detener el resto del reporte.
    return 1 if report.overall_status.value == "FAIL" else 0

if __name__ == "__main__":
    sys.exit(main())