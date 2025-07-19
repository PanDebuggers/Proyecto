# 🛠️ Scripts de mantenimiento — MediCareDesk

Este directorio contiene herramientas para reiniciar o limpiar la base de datos durante el desarrollo.

---

## limpiar_tablas.py
Vacía TODAS las tablas de datos (sin borrar estructura ni archivo .db).

🟢 Úsalo antes de hacer `git push`.

---

## borrar_tabla.py
Vacía UNA tabla específica. Edita la variable `tabla` antes de ejecutarlo.

🔐 Incluye confirmación para evitar errores.

---

## restaurar_base.py
Elimina el archivo `.db` y crea una base nueva desde `MediCareDesk_SQLite.sql`.

⚠️ Destruye todos los datos. Úsalo solo si necesitas empezar completamente desde cero.
