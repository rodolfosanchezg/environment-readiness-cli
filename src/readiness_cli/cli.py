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

COLOR_BY_STATUS = {
    "PASS": "\033[32m",         # verde
    "WARN": "\033[33m",         # amarillo
    "FAIL": "\033[31m",         # rojo
}

RESET = "\033[0m"

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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Muestra informacion detallada (details) de cada verificacion."
    )
    return parser

def print_colored_report(report, verbose: bool = False) -> None: 
    """
        Imprime el reporte en terminal con color. Vive en cli.py: es
        presentacion pura, no logica de negocio.
    """

    print(f"Estado general: {report.overall_status.value}")
    print()

    for r in report.results:
        color = COLOR_BY_STATUS.get(r.status.value, "")
        print(f"{color}[{r.status.value}]{RESET} {r.name}: {r.message}")
        if verbose and r.details:
            for key, value in r.details.items():
                print(f"    {key}: {value}")

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    base_path = Path(args.path)

    results = run_diagnostics() + run_file_checks(base_path)
    report = build_report(results)
    content = export(report, fmt=args.format, path=args.output)

    if args.output is None and args.format == "text":
        print_colored_report(report, verbose=args.output)
    else:
        if args.output:
            print(f"Reporte guardado en: {args.output}")
        else:
            print(content)

    # Codigo de salida: 0 si PASS o WARN, 1 si hay algun FAIL.
    # Esto permite usar la CLI en pipelines de CI sin detener el resto del reporte.
    return 1 if report.overall_status.value == "FAIL" else 0

if __name__ == "__main__":
    sys.exit(main())