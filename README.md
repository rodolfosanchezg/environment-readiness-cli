# Environment Readiness CLI

Herramienta de línea de comandos que evalúa si un equipo está preparado para
ejecutar un proyecto Python, y genera un reporte legible en texto o JSON.

## Problema

Antes de empezar a trabajar en un proyecto Python, es fácil pasar por alto
detalles del entorno (versión de Python, archivos de configuración faltantes,
entorno virtual no activado) que causan errores confusos más adelante. Esta
herramienta automatiza ese diagnóstico inicial.

## Instalación

Requiere Python 3.9 o superior.

```bash
git clone https://github.com/rodolfosanchezg/environment-readiness-cli.git
cd environment-readiness-cli
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

> **Nota (Windows/PowerShell):** si al activar el entorno virtual aparece un error
> relacionado con la política de ejecución de scripts (`... cannot be loaded because
> running scripts is disabled on this system`), ejecuta el siguiente comando en la
> misma sesión de PowerShell y vuelve a intentar la activación:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```
>
> Este cambio aplica solo a la sesión actual de PowerShell (no es permanente ni
> afecta al resto del sistema).

## Uso

Evaluar el directorio actual e imprimir el reporte en pantalla:

```bash
readiness-cli
```

Elegir formato de salida:

```bash
readiness-cli --format json
```

Evaluar otra ruta y guardar el resultado en un archivo:

```bash
readiness-cli --path C:/otro-proyecto --format json --output reporte.json
```

Ver todas las opciones disponibles:

```bash
readiness-cli --help
```

## Arquitectura

cli.py (argparse)
│
├──> diagnostics.run_diagnostics()   → versión Python, SO, ruta intérprete, venv activo
├──> checks.run_file_checks()        → README, pyproject.toml, .gitignore, tests/
├──> report.build_report()           → consolida resultados en PASS/WARN/FAIL
└──> report.export()                 → texto plano o JSON, a pantalla o archivo

- `diagnostics.py`: recolecta información del sistema.
- `checks.py`: verifica archivos/carpetas requeridos, recibe `base_path` como parámetro (facilita pruebas con carpetas temporales).
- `report.py`: agrupa resultados individuales, calcula el estado general y exporta.
- `cli.py`: único punto de entrada; no contiene lógica de negocio.

### Decisiones técnicas

- **Ningún chequeo lanza excepciones hacia arriba.** Cada verificación devuelve un `CheckResult` con estado PASS/WARN/FAIL, incluso ante archivos faltantes o rutas inexistentes. Esto permite que un fallo aislado no detenga el resto del diagnóstico.
- **`base_path` como parámetro explícito** en `checks.py`, en lugar de usar `Path.cwd()` internamente, para que la lógica sea testeable con carpetas temporales sin tocar el sistema de archivos real.
- **Separación estricta entre recolección de datos y presentación**: `diagnostics.py` y `checks.py` no saben nada de texto/JSON; `report.py` no sabe cómo se obtuvieron los datos.

## Pruebas

```bash
pytest -v
```

14 pruebas unitarias cubren:
- Casos exitosos (proyecto completo, versión de Python válida, reporte sin errores).
- Casos de error (archivos/carpetas faltantes, rutas inexistentes, formato de exportación inválido, versión mínima de Python no alcanzada).

## Limitaciones conocidas

- No valida el *contenido* de los archivos requeridos, solo su existencia.
- No verifica dependencias instaladas ni su compatibilidad de versiones.
- La detección de entorno virtual no distingue entre `venv`, `virtualenv` o `conda`.

## Pendientes / roadmap

- [ ] Salida coloreada en terminal y bandera `--verbose` (reto opcional de la semana).
- [ ] Verificación de dependencias declaradas en `pyproject.toml`.
- [ ] Soporte para archivo de configuración personalizado (qué archivos/carpetas son requeridos).

## Licencia

Uso educativo — Programa de 24 Semanas Python Developer.