cho -----------------------------------------------

REM Verificar si Python está instalado
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no está instalado. Por favor instálalo desde https://www.python.org/downloads/
    pause
    exit /b
)

REM Crear entorno virtual llamado "env"
echo.
echo [INFO] Creando entorno virtual (env)
python -m venv env

REM Activar entorno virtual
call env\Scripts\activate.bat

REM Instalar dependencias necesarias del proyecto
echo.
echo [INFO] Instalando dependencias del proyecto
pip install --upgrade pip
pip install mysql-connector-python schedule reportlab fpdf pylint flake8

REM Inicializar la base de datos con un script de Python
echo.
echo [INFO] Inicializando la base de datos
python init_db.py

REM Ejecutar el sistema principal (cuando esté listo)
echo.
echo [INFO] Ejecutando el sistema MediCareDesk...
python main.py

echo.
echo -----------------------------------------------
echo Proceso de inicialización finalizado.
pause

