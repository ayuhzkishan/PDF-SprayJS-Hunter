@echo off
set "VENV_PYTHON=%~dp0venv\Scripts\python.exe"
"%VENV_PYTHON%" generate_tests.py
if %ERRORLEVEL% EQU 0 (
    echo [OK] Test PDFs generated.
    "%VENV_PYTHON%" main.py --file clean_test.pdf
    "%VENV_PYTHON%" main.py --file malicious_test.pdf
) else (
    echo [ERROR] Failed to generate test PDFs.
)
pause
