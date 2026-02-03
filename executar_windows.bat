@echo off
echo ============================================================
echo    Gerador de Relatorio PRSA - Estatisticas
echo ============================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Verificando dependencias...
echo.

REM Instalar dependencias se necessario
pip install -r requirements.txt

echo.
echo Iniciando aplicacao...
echo.

REM Executar aplicacao
python prsa_report_generator.py

pause
