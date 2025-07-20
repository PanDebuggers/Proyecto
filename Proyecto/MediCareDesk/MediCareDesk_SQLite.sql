-- Crear tabla Paciente 
CREATE TABLE IF NOT EXISTS Paciente (
  id_paciente INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  edad INTEGER,
  genero TEXT CHECK (genero IN ('M', 'F', 'Otro')) DEFAULT 'M',
  contacto_emergencia TEXT,
  observaciones TEXT,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  activo INTEGER CHECK (activo IN (0,1)) DEFAULT 1,
  id_cuidador INTEGER  -- sin NOT NULL
);

-- Crear tabla Cuidador
CREATE TABLE IF NOT EXISTS Cuidador (
  id_cuidador INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  relacion TEXT,
  contacto TEXT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

-- Crear tabla Medicamento
CREATE TABLE IF NOT EXISTS Medicamento (
  id_medicamento INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  principio_activo TEXT,
  indicaciones TEXT,
  fecha_caducidad DATE,
  contraindicaciones TEXT,
  presentacion TEXT CHECK (presentacion IN ('Comprimidas', 'Jarabe', 'Crema', 'Solución inyectable', 'otros')) NOT NULL,
  laboratorio TEXT,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Tratamiento
CREATE TABLE IF NOT EXISTS Tratamiento (
  id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
  id_paciente INTEGER NOT NULL,
  nombre_tratamiento TEXT NOT NULL,
  descripcion TEXT,
  estado TEXT CHECK (estado IN ('activo', 'suspendido', 'finalizado', 'pendiente')) DEFAULT 'pendiente',
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente)
);

-- Crear tabla Tratamiento_Medicamento
CREATE TABLE IF NOT EXISTS Tratamiento_Medicamento (
  id_tratamiento_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
  id_tratamiento INTEGER NOT NULL,
  id_medicamento INTEGER NOT NULL,
  dosis TEXT,
  frecuencia TEXT CHECK (frecuencia IN ('una_vez_al_dia', 'cada_8_horas', 'cada_12_horas', 'cada_24_horas', 'personalizada')),
  via_administracion TEXT CHECK (via_administracion IN ('oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea', 'inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica')),
  fecha_inicio DATE,
  fecha_fin DATE,
  estado TEXT CHECK (estado IN ('activo', 'suspendido', 'finalizado', 'pendiente')),
  hora_preferida TIME,
  FOREIGN KEY (id_tratamiento) REFERENCES Tratamiento(id_tratamiento),
  FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);

-- Crear tabla Toma
CREATE TABLE IF NOT EXISTS Toma (
  id_toma INTEGER PRIMARY KEY AUTOINCREMENT,
  id_tratamiento_medicamento INTEGER NOT NULL,
  fecha DATE NOT NULL,
  hora_programada TIME NOT NULL,
  estado TEXT CHECK (estado IN ('programada', 'tomada', 'omitida', 'pendiente')) DEFAULT 'programada',
  recordatorio_enviado INTEGER CHECK (recordatorio_enviado IN (0,1)) DEFAULT 0,
  FOREIGN KEY (id_tratamiento_medicamento) REFERENCES Tratamiento_Medicamento(id_tratamiento_medicamento)
);

-- Crear tabla Evento
CREATE TABLE IF NOT EXISTS Evento (
  id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
  id_paciente INTEGER NOT NULL,
  fecha DATE NOT NULL,
  descripcion TEXT NOT NULL,
  FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente)
);

-- Crear tabla Cuidador_Paciente
CREATE TABLE IF NOT EXISTS Cuidador_Paciente (
  id_cuidador INTEGER NOT NULL,
  id_paciente INTEGER NOT NULL,
  PRIMARY KEY (id_cuidador, id_paciente),
  FOREIGN KEY (id_cuidador) REFERENCES Cuidador(id_cuidador),
  FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente)
);


-- Vista Pacientes 
CREATE VIEW IF NOT EXISTS Vista_Pacientes AS
SELECT 
    p.id_paciente,
    p.nombre,
    p.edad,
    p.genero,
    p.contacto_emergencia,
    p.activo,
    cp.id_cuidador,
    COUNT(t.id_tratamiento) AS tratamientos_totales,
    SUM(CASE WHEN t.estado = 'activo' THEN 1 ELSE 0 END) AS tratamientos_activos
FROM 
    Paciente p
JOIN
    Cuidador_Paciente cp ON p.id_paciente = cp.id_paciente
LEFT JOIN 
    Tratamiento t ON p.id_paciente = t.id_paciente
GROUP BY 
    p.id_paciente, cp.id_cuidador;


-- Vista Tratamientos
CREATE VIEW IF NOT EXISTS Vista_Tratamientos AS
SELECT 
    t.id_tratamiento,
    t.nombre_tratamiento,
    t.descripcion,
    t.estado,
    t.fecha_inicio,
    t.fecha_fin,
    p.nombre AS paciente_nombre
FROM
    Tratamiento t
JOIN
    Paciente p ON t.id_paciente = p.id_paciente;
