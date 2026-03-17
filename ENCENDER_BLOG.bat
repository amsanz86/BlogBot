@echo off
title Auto Viral Blog Engine - Lanzador
color 0b

echo ======================================================
echo          AUTO VIRAL BLOG ENGINE - STARTUP
echo ======================================================
echo.
echo [1/3] Verificando dependencias...
pip install -r requirements.txt > nul 2>&1

echo [2/3] Iniciando Programador (main.py) en segundo plano...
:: Lanzamos el motor en una ventana minimizada para que no moleste
start "Blog Engine - Scheduler" /min python main.py

echo [3/3] Iniciando Servidor de Vista Previa (preview.py)...
:: Lanzamos la vista previa y abrimos el navegador
start "Blog Engine - Web Server" python preview.py

echo.
echo ======================================================
echo   ¡TODO LISTO Y FUNCIONANDO!
echo ======================================================
echo.
echo  - El MOTOR esta corriendo minimizado en tu barra de tareas.
echo  - El BLOG esta disponible en tu navegador.
echo  - No cierres las ventanas negras si quieres que siga publicando.
echo.
echo Presiona cualquier tecla para salir de este lanzador...
pause > nul
