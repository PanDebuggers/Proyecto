@echo off
title Inicialización MediCareDesk - Entorno de Desarrollo
echo -----------------------------------------------
echo Iniciando el entorno de desarrollo de MediCareDesk...
echo -----------------------------------------------

REM 1. Verificar si Python está instalado
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no está instalado. Por favor instálalo desde https://www.python.org/downloads/
    pause
    exit /b
)

REM 2. Crear entorno virtual llamado "env"
echo.
echo [INFO] Creando entorno virtual (env)...
python -m venv env

REM 3. Activar entorno virtual
call env\Scripts\activate.bat

REM 4. Instalar dependencias necesarias del proyecto
echo.
echo [INFO] Instalando dependencias del proyecto...
pip install --upgrade pip
pip install mysql-connector-python schedule reportlab fpdf pylint flake8

REM 5. (OPCIONAL) Inicializar la base de datos
echo.
echo [INFO] Saltando inicialización de base de datos porque aún no existe.
REM python init_db.py

REM 6. Ejecutar la aplicación
echo.
echo [INFO] Ejecutando el sistema MediCareDesk...
python main.py

echo.
echo -----------------------------------------------
echo Proceso de inicialización finalizado.
pause

