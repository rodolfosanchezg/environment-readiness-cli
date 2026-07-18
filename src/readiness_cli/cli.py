# src/readiness_cli/cli.py
import argparse

def build_parser() -> argparse.ArgumentParser:
    """
        Define argumentos: 
        --format {text,json}
        --output <path>
        --verbose
    """

def main() -> int:
    """
        Orquesta diagnostics + checks + report.
        Retorna coodigo de salida (0 o 1)
    """