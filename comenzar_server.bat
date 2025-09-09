@echo off
title Gestor de Dossiers - Global News
color 0A

echo.
echo ===============================================
echo    GESTOR DE DOSSIERS - GLOBAL NEWS
echo    Desarrollado por Kevin Gomez
echo ===============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si los archivos necesarios existen
if not exist "app.py" (
    echo ERROR: No se encontró app.py
    pause
    exit /b 1
)

if not exist "templates\" (
    echo ERROR: No se encontró la carpeta templates
    pause
    exit /b 1
)

if not exist "static\" (
    echo ERROR: No se encontró la carpeta static
    pause
    exit /b 1
)

REM Crear directorio de logs si no existe
if not exist "logs\" mkdir logs

echo Iniciando servidor...
echo.

REM Ejecutar el servidor
python run_server.py

echo.
echo Servidor detenido.
pause