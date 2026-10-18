@echo off
cd /d "%~dp0"
set "NOLAPATENT_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%NOLAPATENT_PYTHON%" (
  "%NOLAPATENT_PYTHON%" scripts\build.py
) else (
  python scripts\build.py
)
pause
