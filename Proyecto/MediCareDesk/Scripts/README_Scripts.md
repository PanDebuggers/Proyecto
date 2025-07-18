Esta carpeta cuenta con script importantes para la base de datos, por ejemplo para insertar datos para las pruebas unitarias (como es el caso de insertar_cuidador_test.py), tambien para eliminar datos (eliminar_cuidador_test.py) e incluso tiene uno en caso de querer reiniciar toda la base de datos (reconstruir_base_datos).
**⚠️ Este proceso borra todo.**

Pasos:
1. Asegúrate de tener el archivo `MediCareDesk_SQLite.sql` actualizado.
2. Ejecuta: `python scripts/reconstruir_base_datos.py`
3. Luego vuelve a insertar los datos de prueba necesarios.