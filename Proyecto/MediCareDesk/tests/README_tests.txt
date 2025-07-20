🧪 Tests del sistema MediCareDesk
Esta carpeta contiene pruebas manuales y unitarias para validar funcionalidades críticas del sistema.

📁 Archivos incluidos
Archivo	Descripción breve
test_auth.py	✅ Pruebas unitarias para validar el login de cuidadores.
test_conexion.py	🔌 Verifica que la base de datos se conecte correctamente y detecta tablas.
test_modelos.py	🧠 Pruebas funcionales de operaciones en modelos.py: inserción y consulta real.
test_tomas.py	🧪 Lugar para pruebas futuras del módulo de tomas de medicamentos.
test_validacion_db.py	📊 Verifica integridad de la estructura de la base de datos SQLite.
test_customtkinter.py	🎨 Verifica visualmente que customtkinter esté instalado y funcione bien.

📝 Notas importantes
test_modelos.py interactúa directamente con la base de datos, así que puede insertar registros reales. Úsalo con una base de pruebas o después de limpiar tablas.

test_customtkinter.py no es una prueba automatizada, solo una verificación visual útil si hay errores con el import.

Algunos tests son manuales y sirven para confirmar conexiones o estructuras.