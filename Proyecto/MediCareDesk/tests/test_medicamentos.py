import unittest
from unittest.mock import Mock, patch, MagicMock, call
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import sqlite3
import sys


# ========================================================================
# CLASE ORIGINAL PARA TESTING (incluida en el archivo de tests)
# ========================================================================

class MedicamentosManager:
    def __init__(self, frame_dinamico):
        self.frame_dinamico = frame_dinamico
        self.tree = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_FILENAME = os.path.join(self.BASE_DIR, "..", "..", "data", "MediCareDesk.db")
        self.setup_ui()
        
    def setup_ui(self):
        # Limpiar frame dinámico
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

        # Frame principal con scroll
        main_frame = tk.Frame(self.frame_dinamico, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        # CORRECCIÓN PRINCIPAL: Paréntesis correctamente balanceados
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        lbl = tk.Label(
            scrollable_frame,
            text="Gestión de Medicamentos",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
        )
        lbl.pack(pady=(10, 20))

        # Crear tabla Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        columnas = (
            "ID", "Nombre", "Principio Activo", "Presentación",
            "Laboratorio", "Caducidad", "Registro"
        )

        self.tree = ttk.Treeview(
            scrollable_frame, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150, anchor="w")
        self.tree.column("Principio Activo", width=150, anchor="w")
        self.tree.column("Presentación", width=120, anchor="center")
        self.tree.column("Laboratorio", width=120, anchor="w")
        self.tree.column("Caducidad", width=100, anchor="center")
        self.tree.column("Registro", width=120, anchor="center")

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Botones de acción
        btn_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        btn_agregar = ctk.CTkButton(
            btn_frame, text="Agregar Medicamento", command=self.agregar_medicamento)
        btn_agregar.pack(side=tk.LEFT, padx=5)

        btn_editar = ctk.CTkButton(
            btn_frame, text="Editar Medicamento", command=self.editar_medicamento)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = ctk.CTkButton(
            btn_frame,
            text="Eliminar Medicamento",
            command=self.eliminar_medicamento,
            fg_color="#d9534f",
            hover_color="#c9302c",
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_refresh = ctk.CTkButton(btn_frame, text="Refrescar", command=self.cargar_datos)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de medicamentos desde la base de datos"""
        try:
            conn = sqlite3.connect(self.DB_FILENAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicamentos")
            medicamentos = cursor.fetchall()
            
            # Limpiar datos anteriores
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar nuevos datos
            for medicamento in medicamentos:
                self.tree.insert("", "end", values=medicamento)
                
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def agregar_medicamento(self):
        """Método para agregar un nuevo medicamento"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Información", "Función para agregar medicamento")

    def editar_medicamento(self):
        """Método para editar un medicamento existente"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Información", "Función para editar medicamento")

    def eliminar_medicamento(self):
        """Método para eliminar un medicamento"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Información", "Función para eliminar medicamento")


def mostrar_medicamentos(frame_dinamico):
    """Función para mostrar la interfaz de medicamentos"""
    manager = MedicamentosManager(frame_dinamico)
    return manager


# ========================================================================
# TESTS UNITARIOS
# ========================================================================

class TestMedicamentosManager(unittest.TestCase):
    """Tests unitarios para la clase MedicamentosManager"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Mock del frame dinámico
        self.mock_frame = Mock()
        self.mock_frame.winfo_children.return_value = []
        
        # Patches para evitar crear ventanas reales
        self.patches = [
            patch('tkinter.Frame'),
            patch('tkinter.Label'),
            patch('tkinter.Canvas'),
            patch('tkinter.ttk.Scrollbar'),
            patch('tkinter.ttk.Treeview'),
            patch('tkinter.ttk.Style'),
            patch('customtkinter.CTkButton'),
        ]
        
        # Iniciar todos los patches
        self.mocks = [p.start() for p in self.patches]
        
        # Configurar mocks específicos
        self.mock_tk_frame = self.mocks[0]
        self.mock_tk_label = self.mocks[1]
        self.mock_tk_canvas = self.mocks[2]
        self.mock_ttk_scrollbar = self.mocks[3]
        self.mock_ttk_treeview = self.mocks[4]
        self.mock_ttk_style = self.mocks[5]
        self.mock_ctk_button = self.mocks[6]
        
        # Configurar el mock del treeview
        self.mock_tree = Mock()
        self.mock_ttk_treeview.return_value = self.mock_tree
        
        # Configurar el mock del estilo
        self.mock_style = Mock()
        self.mock_ttk_style.return_value = self.mock_style
    
    def tearDown(self):
        """Limpieza después de cada test"""
        # Detener todos los patches
        for p in self.patches:
            p.stop()
    
    def test_init_basic(self):
        """Test de inicialización básica de MedicamentosManager"""
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se asignó el frame dinámico
            self.assertEqual(manager.frame_dinamico, self.mock_frame)
            
            # Verificar que se configuraron las rutas de base de datos
            self.assertIsNotNone(manager.BASE_DIR)
            self.assertIsNotNone(manager.DB_FILENAME)
            self.assertIn("MediCareDesk.db", manager.DB_FILENAME)
    
    def test_setup_ui_clears_frame(self):
        """Test que setup_ui limpia el frame dinámico"""
        mock_widget1 = Mock()
        mock_widget2 = Mock()
        self.mock_frame.winfo_children.return_value = [mock_widget1, mock_widget2]
        
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se llamó destroy en todos los widgets
            mock_widget1.destroy.assert_called_once()
            mock_widget2.destroy.assert_called_once()
    
    def test_setup_ui_creates_main_components(self):
        """Test que setup_ui crea los componentes principales"""
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se crearon los componentes
            self.mock_tk_frame.assert_called()
            self.mock_tk_canvas.assert_called()
            self.mock_ttk_scrollbar.assert_called()
            self.mock_tk_label.assert_called()
            self.mock_ttk_treeview.assert_called()
    
    def test_setup_ui_configures_treeview(self):
        """Test que setup_ui configura correctamente el treeview"""
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se configuraron las columnas del treeview
            expected_columns = (
                "ID", "Nombre", "Principio Activo", "Presentación",
                "Laboratorio", "Caducidad", "Registro"
            )
            
            # Verificar que se creó el treeview con las columnas correctas
            self.mock_ttk_treeview.assert_called_with(
                unittest.mock.ANY, 
                columns=expected_columns, 
                show="headings", 
                selectmode="browse"
            )
            
            # Verificar que se configuraron las columnas
            manager.tree.column.assert_any_call("ID", width=50, anchor="center")
            manager.tree.column.assert_any_call("Nombre", width=150, anchor="w")
            
            # Verificar que se configuraron los headings
            for col in expected_columns:
                manager.tree.heading.assert_any_call(col, text=col)
    
    def test_setup_ui_creates_buttons(self):
        """Test que setup_ui crea todos los botones necesarios"""
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se crearon los botones
            button_calls = self.mock_ctk_button.call_args_list
            
            # Extraer los textos de los botones
            button_texts = []
            for call in button_calls:
                args, kwargs = call
                if 'text' in kwargs:
                    button_texts.append(kwargs['text'])
            
            expected_buttons = [
                "Agregar Medicamento",
                "Editar Medicamento", 
                "Eliminar Medicamento",
                "Refrescar"
            ]
            
            for expected_text in expected_buttons:
                self.assertIn(expected_text, button_texts)
    
    def test_setup_ui_configures_style(self):
        """Test que setup_ui configura el estilo correctamente"""
        with patch.object(MedicamentosManager, 'cargar_datos'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que se configuró el estilo del treeview
            self.mock_style.configure.assert_any_call("Treeview", rowheight=25)
            self.mock_style.configure.assert_any_call("Treeview.Heading", font=("Helvetica", 10, "bold"))
    
    @patch('sqlite3.connect')
    def test_cargar_datos_success(self, mock_connect):
        """Test que cargar_datos funciona correctamente con datos válidos"""
        # Mock de la conexión y cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Datos de prueba
        test_data = [
            (1, "Paracetamol", "Acetaminofén", "500mg", "Pfizer", "2024-12-31", "ABC123"),
            (2, "Ibuprofeno", "Ibuprofeno", "400mg", "Bayer", "2025-06-30", "DEF456")
        ]
        mock_cursor.fetchall.return_value = test_data
        
        # Crear manager sin llamar a cargar_datos en setup_ui
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            manager.tree = Mock()
            manager.tree.get_children.return_value = ["item1", "item2"]
            
            # Ejecutar cargar_datos
            manager.cargar_datos()
            
            # Verificar que se ejecutó la consulta
            mock_cursor.execute.assert_called_with("SELECT * FROM medicamentos")
            
            # Verificar que se limpiaron los datos anteriores
            manager.tree.delete.assert_any_call("item1")
            manager.tree.delete.assert_any_call("item2")
            
            # Verificar que se insertaron los datos
            expected_calls = [
                call("", "end", values=(1, "Paracetamol", "Acetaminofén", "500mg", "Pfizer", "2024-12-31", "ABC123")),
                call("", "end", values=(2, "Ibuprofeno", "Ibuprofeno", "400mg", "Bayer", "2025-06-30", "DEF456"))
            ]
            manager.tree.insert.assert_has_calls(expected_calls)
            
            # Verificar que se cerró la conexión
            mock_conn.close.assert_called_once()
    
    @patch('sqlite3.connect')
    @patch('builtins.print')
    def test_cargar_datos_database_error(self, mock_print, mock_connect):
        """Test que cargar_datos maneja errores de base de datos"""
        # Simular error de base de datos
        mock_connect.side_effect = sqlite3.Error("Database error")
        
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Ejecutar cargar_datos - no debería lanzar excepción
            try:
                manager.cargar_datos()
                # Verificar que se imprimió el error
                mock_print.assert_called_with("Error al cargar datos: Database error")
            except Exception as e:
                self.fail(f"cargar_datos() lanzó una excepción inesperada: {e}")
    
    @patch('tkinter.messagebox.showinfo')
    def test_agregar_medicamento_calls_messagebox(self, mock_showinfo):
        """Test que agregar_medicamento muestra mensaje informativo"""
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Ejecutar agregar_medicamento
            manager.agregar_medicamento()
            
            # Verificar que se mostró el mensaje
            mock_showinfo.assert_called_once_with("Información", "Función para agregar medicamento")
    
    @patch('tkinter.messagebox.showinfo')
    def test_editar_medicamento_calls_messagebox(self, mock_showinfo):
        """Test que editar_medicamento muestra mensaje informativo"""
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Ejecutar editar_medicamento
            manager.editar_medicamento()
            
            # Verificar que se mostró el mensaje
            mock_showinfo.assert_called_once_with("Información", "Función para editar medicamento")
    
    @patch('tkinter.messagebox.showinfo')
    def test_eliminar_medicamento_calls_messagebox(self, mock_showinfo):
        """Test que eliminar_medicamento muestra mensaje informativo"""
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Ejecutar eliminar_medicamento
            manager.eliminar_medicamento()
            
            # Verificar que se mostró el mensaje
            mock_showinfo.assert_called_once_with("Información", "Función para eliminar medicamento")
    
    def test_database_path_construction(self):
        """Test que la ruta de la base de datos se construye correctamente"""
        with patch.object(MedicamentosManager, 'setup_ui'):
            manager = MedicamentosManager(self.mock_frame)
            
            # Verificar que la ruta incluye los componentes esperados
            self.assertIn("data", manager.DB_FILENAME)
            self.assertIn("MediCareDesk.db", manager.DB_FILENAME)
            self.assertTrue(os.path.isabs(manager.DB_FILENAME))


class TestMostrarMedicamentos(unittest.TestCase):
    """Tests para la función mostrar_medicamentos"""
    
    @patch.object(MedicamentosManager, '__init__', return_value=None)
    def test_mostrar_medicamentos_creates_manager(self, mock_init):
        """Test que mostrar_medicamentos crea una instancia de MedicamentosManager"""
        mock_frame = Mock()
        
        # Ejecutar la función
        result = mostrar_medicamentos(mock_frame)
        
        # Verificar que se creó el manager
        mock_init.assert_called_once_with(mock_frame)
        self.assertIsInstance(result, MedicamentosManager)


class TestIntegration(unittest.TestCase):
    """Tests de integración para verificar la interacción entre componentes"""
    
    @patch('sqlite3.connect')
    @patch('tkinter.messagebox.showinfo')
    def test_full_workflow_simulation(self, mock_showinfo, mock_connect):
        """Test que simula un flujo completo de trabajo"""
        # Setup de mocks
        mock_frame = Mock()
        mock_frame.winfo_children.return_value = []
        
        with patch('tkinter.Frame'), \
             patch('tkinter.Label'), \
             patch('tkinter.Canvas'), \
             patch('tkinter.ttk.Scrollbar'), \
             patch('tkinter.ttk.Treeview') as mock_treeview, \
             patch('tkinter.ttk.Style'), \
             patch('customtkinter.CTkButton'):
            
            # Configurar mock de base de datos
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            # Configurar mock del tree
            mock_tree = Mock()
            mock_tree.get_children.return_value = []
            mock_treeview.return_value = mock_tree
            
            # Crear manager
            manager = MedicamentosManager(mock_frame)
            
            # Simular acciones del usuario
            manager.agregar_medicamento()
            manager.editar_medicamento()
            manager.eliminar_medicamento()
            
            # Verificar que todas las operaciones se ejecutaron sin errores
            self.assertEqual(mock_showinfo.call_count, 3)  # 3 llamadas a messagebox
            mock_cursor.execute.assert_called()  # Se ejecutó consulta de cargar datos


if __name__ == '__main__':
    # Configurar el runner de tests
    unittest.main(
        verbosity=2,
        failfast=False,
        buffer=True,
        catchbreak=True
    )