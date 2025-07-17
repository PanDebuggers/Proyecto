# 🩺 MediCareDesk

**MediCareDesk** es una aplicación de escritorio desarrollada en Python que permite a cuidadores, familiares o personal médico gestionar la administración de medicamentos en adultos mayores. Funciona completamente **sin conexión a internet** y está diseñada para ser fácil de usar, incluso para personas con poca experiencia tecnológica.

---

## 📌 Características principales

- Registro de pacientes, medicamentos y cuidadores
- Programación automática de tomas de medicamentos
- Alertas visuales y sonoras en tiempo real
- Historial detallado de tomas (verificadas u omitidas)
- Control de tratamientos activos, finalizados o suspendidos
- Interfaz gráfica amigable con **Tkinter**
- Base de datos **SQLite local** (no requiere instalación externa)
- Modularidad y patrones de diseño implementados (Observer y Builder)

---

## 🧱 Estructura del repositorio

MediCareDesk/
├── main.py # Punto de entrada de la aplicación
├── requirements.txt # Dependencias necesarias
├── MediCareDesk_SQLite.sql # Script para crear la base de datos
├── data/ # Base de datos SQLite (.db)
├── resources/ # Iconos, sonidos u otros recursos visuales
├── app/
│ ├── db/ # Conexión y operaciones con la base de datos
│ ├── logic/ # Lógica del negocio (autenticación, programación, validaciones)
│ ├── ui/ # Interfaces gráficas (Tkinter)
│ └── utils/ # Funciones auxiliares y patrones de diseño
└── tests/ # Pruebas unitarias


---

## 🛠️ Requisitos

- Python 3.8 o superior
- pip (administrador de paquetes de Python)

---

## 📥 Instalación

1. Clona este repositorio:

```bash
git clone # 🩺 MediCareDesk

**MediCareDesk** es una aplicación de escritorio desarrollada en Python que permite a cuidadores, familiares o personal médico gestionar la administración de medicamentos en adultos mayores. Funciona completamente **sin conexión a internet** y está diseñada para ser fácil de usar, incluso para personas con poca experiencia tecnológica.

---

## 📌 Características principales

- Registro de pacientes, medicamentos y cuidadores
- Programación automática de tomas de medicamentos
- Alertas visuales y sonoras en tiempo real
- Historial detallado de tomas (verificadas u omitidas)
- Control de tratamientos activos, finalizados o suspendidos
- Interfaz gráfica amigable con **Tkinter**
- Base de datos **SQLite local** (no requiere instalación externa)
- Modularidad y patrones de diseño implementados (Observer y Builder)

---

## 🧱 Estructura del repositorio

MediCareDesk/
├── main.py # Punto de entrada de la aplicación
├── requirements.txt # Dependencias necesarias
├── MediCareDesk_SQLite.sql # Script para crear la base de datos
├── data/ # Base de datos SQLite (.db)
├── resources/ # Iconos, sonidos u otros recursos visuales
├── app/
│ ├── db/ # Conexión y operaciones con la base de datos
│ ├── logic/ # Lógica del negocio (autenticación, programación, validaciones)
│ ├── ui/ # Interfaces gráficas (Tkinter)
│ └── utils/ # Funciones auxiliares y patrones de diseño
└── tests/ # Pruebas unitarias

yaml
Copiar
Editar

---

## 🛠️ Requisitos

- Python 3.8 o superior
- pip (administrador de paquetes de Python)

---

## 📥 Instalación

1. Clona este repositorio:

git clone https://github.com/PanDebuggers/Proyecto.git
cd Proyecto/Proyecto/MediCareDesk

Instala las dependencias:

pip install -r requirements.txt
Asegúrate de tener la base de datos. Puedes:

Usar la base preexistente en data/MediCareDesk.db, o

Crear una nueva ejecutando el script:

sqlite3 data/MediCareDesk.db < MediCareDesk_SQLite.sql
cd MediCareDesk


Instala las dependencias:

pip install -r requirements.txt

Asegúrate de tener la base de datos. Puedes:

Usar la base preexistente en data/MediCareDesk.db, o

Crear una nueva ejecutando el script:

sqlite3 data/MediCareDesk.db < MediCareDesk_SQLite.sql

🚀 Ejecución
Simplemente corre el archivo principal:

bash
Copiar
Editar
python main.py
Esto abrirá la interfaz gráfica donde puedes:

Registrar cuidadores

Agregar pacientes y tratamientos

Marcar tomas como completadas u omitidas

Ver historial y alertas

🧪 Pruebas
Puedes ejecutar las pruebas usando pytest o unittest:

pytest tests/

🧠 Patrones de diseño implementados
Observer: permite que las alertas y el historial se actualicen automáticamente cuando ocurre un evento (por ejemplo, marcar una toma).
Builder: facilita la creación de objetos complejos (como pacientes o tratamientos) desde formularios paso a paso.

🔒 Licencia
Este proyecto fue desarrollado con fines académicos por estudiantes de la Universidad Nacional de Colombia, curso de Ingeniería de Software. Está disponible bajo la licencia MIT.

🙌 Autores
Yamid Alfonso Gonzalez Torres
Jenny Catherine Herrera Garzón
Edwin Andrés Marín Vanegas
Diego Steven Pinzón Yossa

Profesor: Oscar Eduardo Álvarez Rodríguez

