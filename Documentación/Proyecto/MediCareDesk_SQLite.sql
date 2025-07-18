-- Crear base de datos si no existe
-- OMITIDO PARA SQLite
-- OMITIDO PARA SQLite

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS `Toma`;
DROP TABLE IF EXISTS `Bitacora_Eventos`;
DROP TABLE IF EXISTS `Tratamiento_Medicamento`;
DROP TABLE IF EXISTS `Tratamiento`;
DROP TABLE IF EXISTS `Paciente_Cuidador`;
DROP TABLE IF EXISTS `Medicamento`;
DROP TABLE IF EXISTS `Cuidador`;
DROP TABLE IF EXISTS `Paciente`;

-- Crear tablas
CREATE TABLE `Paciente` (
  `id_paciente` int PRIMARY KEY ,
  `nombre` varchar(100) NOT NULL,
  `edad` int,
  `genero` TEXT CHECK (genero IN ('M', 'F', 'Otro')) DEFAULT 'M',
  `contacto_emergencia` varchar(15),
  `observaciones` text,
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP,
  `activo` INTEGER CHECK (%s IN (0,1)) DEFAULT TRUE
);

-- Datos de prueba: Pacientes
INSERT INTO Paciente (id_paciente, nombre, edad, genero, contacto_emergencia, observaciones, activo)
VALUES 
  (1, 'Juan Pérez', 67, 'M', '3001234567', 'Paciente con hipertensión', 1),
  (2, 'María Gómez', 74, 'F', '3109876543', 'Diabética, requiere control diario', 1),
  (3, 'Alex Rojas', 59, 'Otro', '3012345678', 'Alérgico a penicilina', 1);

CREATE TABLE `Cuidador` (
  `id_cuidador` int PRIMARY KEY AUTOINCREMENT,
  `nombre` varchar(100) NOT NULL,
  `relacion` varchar(50),
  `contacto` varchar(15),
  `email` varchar(100) UNIQUE NOT NULL,
  `password_hash` varchar(255) NOT NULL
);

-- Datos de prueba: Cuidadores
INSERT INTO Cuidador (id_cuidador, nombre, relacion, contacto, email, password_hash)
VALUES 
  (1, 'Catherine Herrera', 'Hija', '3214567890', 'cathy@example.com', '1234'),
  (2, 'Luis Torres', 'Enfermero', '3156789012', 'luis.torres@cuidados.com', 'luispass'),
  (3, 'Sandra López', 'Hermana', '3123456789', 'sandra.lopez@cuida.org', 'clave123');

CREATE TABLE `Paciente_Cuidador` (
  `id_paciente` int NOT NULL,
  `id_cuidador` int NOT NULL,
  `fecha_asignacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_paciente`, `id_cuidador`)
);

CREATE TABLE `Medicamento` (
  `id_medicamento` int PRIMARY KEY AUTOINCREMENT ,
  `nombre` varchar(100) NOT NULL, 
  `principio_activo` varchar(100),
  `indicaciones` text,
  `fecha_caducidad` date,
  `contraindicaciones` text,
  `presentacion` TEXT CHECK (presentacion IN ('Comprimidas', 'Jarabe', 'Crema', 'Solución inyectable', 'otros')) NOT NULL,
  `laboratorio` varchar(100),
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Datos de prueba: Medicamentos
INSERT INTO Medicamento (id_medicamento, nombre, principio_activo, indicaciones, fecha_caducidad, contraindicaciones, presentacion, laboratorio)
VALUES 
  (1, 'Paracetamol', 'Acetaminofén', 'Fiebre y dolor', '2026-01-01', 'No exceder dosis en insuficiencia hepática', 'Comprimidas', 'Genfar'),
  (2, 'Ibuprofeno', 'Ibuprofeno', 'Dolor muscular', '2025-11-15', 'Evitar en pacientes con úlcera gástrica', 'Comprimidas', 'Bayer'),
  (3, 'Salbutamol', 'Salbutamol', 'Crisis asmáticas', '2024-12-31', 'Evitar uso excesivo sin control médico', 'Solución inyectable', 'GlaxoSmithKline');

CREATE TABLE `Tratamiento` (
  `id_tratamiento` int PRIMARY KEY AUTOINCREMENT,
  `id_paciente` int NOT NULL,
  `nombre_tratamiento` varchar(200) NOT NULL,
  `objetivo` text,
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` TEXT CHECK (estado IN ('activo', 'suspendido', 'finalizado', 'pendiente')) DEFAULT 'pendiente',
  `observaciones` text,
  `responsable` varchar(100),
  `fecha_creacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE `Tratamiento_Medicamento` (
  `id_tratamiento_medicamento` int PRIMARY KEY AUTOINCREMENT,
  `id_tratamiento` int NOT NULL,
  `id_medicamento` int NOT NULL,
  `dosis` varchar(500),
  `frecuencia` TEXT CHECK (frecuencia IN ('una_vez_al_dia', 'cada_8_horas', 'cada_12_horas', 'cada_24_horas', 'personalizada')) DEFAULT 'una_vez_al_dia',
  `frecuencia_personalizada` varchar(100) NULL,
  `via_administracion` TEXT CHECK (via_administracion IN ('oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea', 'inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica')) DEFAULT 'oral',
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` TEXT CHECK (estado IN ('activo', 'suspendido', 'finalizado', 'pendiente')) DEFAULT 'pendiente',
  `hora_preferida` time,
  `fecha_creacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_tratamiento_medicamento` (`id_tratamiento`, `id_medicamento`)
);

CREATE TABLE `Toma` (
  `id_toma` int PRIMARY KEY AUTOINCREMENT,
  `id_tratamiento_medicamento` int NOT NULL,
  `fecha` date NOT NULL,
  `hora_programada` time NOT NULL,
  `estado` TEXT CHECK (estado IN ('programada', 'tomada', 'omitida')) DEFAULT 'programada',
  `observaciones` text,
  `registrado_por` varchar(100),
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP,
  `recordatorio_enviado` INTEGER CHECK (%s IN (0,1)) DEFAULT FALSE,
  INDEX `idx_toma_fecha_estado` (`fecha`, `estado`)
);

CREATE TABLE `Bitacora_Eventos` (
  `id_evento` int PRIMARY KEY AUTOINCREMENT,
  `id_paciente` int NOT NULL,
  `tipo_evento` TEXT CHECK (tipo_evento IN ('medicamento_tomado', 'medicamento_omitido', 'efecto_adverso', 'interaccion_detectada', 'cambio_tratamiento', 'recordatorio_enviado', 'sistema', 'otro')) DEFAULT 'otro',
  `descripcion` text,
  `fecha` timestamp DEFAULT CURRENT_TIMESTAMP
);


-- Crear claves foráneas
ALTER TABLE `Paciente_Cuidador` 
ADD CONSTRAINT `fk_paciente_cuidador_paciente` 
FOREIGN KEY (`id_paciente`) REFERENCES `Paciente` (`id_paciente`) ON DELETE CASCADE;

ALTER TABLE `Paciente_Cuidador` 
ADD CONSTRAINT `fk_paciente_cuidador_cuidador` 
FOREIGN KEY (`id_cuidador`) REFERENCES `Cuidador` (`id_cuidador`) ON DELETE CASCADE;

ALTER TABLE `Tratamiento` 
ADD CONSTRAINT `fk_tratamiento_paciente` 
FOREIGN KEY (`id_paciente`) REFERENCES `Paciente` (`id_paciente`) ON DELETE CASCADE;

ALTER TABLE `Tratamiento_Medicamento` 
ADD CONSTRAINT `fk_tratamiento_medicamento_tratamiento` 
FOREIGN KEY (`id_tratamiento`) REFERENCES `Tratamiento` (`id_tratamiento`) ON DELETE CASCADE;

ALTER TABLE `Tratamiento_Medicamento` 
ADD CONSTRAINT `fk_tratamiento_medicamento_medicamento` 
FOREIGN KEY (`id_medicamento`) REFERENCES `Medicamento` (`id_medicamento`) ON DELETE RESTRICT;

ALTER TABLE `Toma` 
ADD CONSTRAINT `fk_toma_tratamiento_medicamento` 
FOREIGN KEY (`id_tratamiento_medicamento`) REFERENCES `Tratamiento_Medicamento` (`id_tratamiento_medicamento`) ON DELETE CASCADE;

ALTER TABLE `Bitacora_Eventos` 
ADD CONSTRAINT `fk_bitacora_paciente` 
FOREIGN KEY (`id_paciente`) REFERENCES `Paciente` (`id_paciente`) ON DELETE CASCADE;

PRAGMA foreign_keys = ON;

-- Índices para mejorar performance
CREATE INDEX `idx_tratamiento_paciente` ON `Tratamiento` (`id_paciente`);
CREATE INDEX `idx_tratamiento_medicamento_tratamiento` ON `Tratamiento_Medicamento` (`id_tratamiento`);
CREATE INDEX `idx_tratamiento_medicamento_medicamento` ON `Tratamiento_Medicamento` (`id_medicamento`);
CREATE INDEX `idx_toma_fecha` ON `Toma` (`fecha`);
CREATE INDEX `idx_toma_tratamiento_medicamento` ON `Toma` (`id_tratamiento_medicamento`);
CREATE INDEX `idx_bitacora_fecha` ON `Bitacora_Eventos` (`fecha`);
CREATE INDEX `idx_bitacora_paciente` ON `Bitacora_Eventos` (`id_paciente`);
CREATE INDEX `idx_cuidador_email` ON `Cuidador` (`email`);


-- Vista de Pacientes con sus Datos Personales
CREATE OR REPLACE VIEW `Vista_Pacientes` AS
SELECT 
    p.id_paciente,
    p.nombre AS paciente,
    p.edad,
    p.genero,
    p.contacto_emergencia,
    p.observaciones,
    p.fecha_registro,
    p.activo
FROM Paciente p;

-- Vista de Medicamentos con sus Detalles
CREATE OR REPLACE VIEW `Vista_Medicamentos` AS
SELECT 
    m.id_medicamento,
    m.nombre AS medicamento,
    m.principio_activo,
    m.indicaciones,
    m.fecha_caducidad,
    m.presentacion,
    m.laboratorio
FROM Medicamento m;

-- Vista de Alerta de Toma de Medicamento
CREATE OR REPLACE VIEW `Vista_Alertas_Tomas` AS
SELECT 
    p.nombre AS paciente,
    m.nombre AS medicamento,
    t.hora_programada,
    DATEDIFF(t.hora_programada, CURTIME()) AS tiempo_restante
FROM Toma t
JOIN Tratamiento_Medicamento tm ON t.id_tratamiento_medicamento = tm.id_tratamiento_medicamento
JOIN Tratamiento tr ON tm.id_tratamiento = tr.id_tratamiento
JOIN Paciente p ON tr.id_paciente = p.id_paciente
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
WHERE t.fecha = CURDATE() AND t.estado = 'programada';

-- Vista de Historial de Tomas de Paciente
CREATE OR REPLACE VIEW `Vista_Historial_Tomas_Paciente` AS
SELECT
    p.nombre AS paciente,
    t.nombre_tratamiento,
    m.nombre AS medicamento,
    tom.fecha,
    tom.hora_programada,
    tom.estado AS estado_toma,
    tom.observaciones
FROM Toma tom
JOIN Tratamiento_Medicamento tm ON tom.id_tratamiento_medicamento = tm.id_tratamiento_medicamento
JOIN Tratamiento t ON tm.id_tratamiento = t.id_tratamiento
JOIN Paciente p ON t.id_paciente = p.id_paciente
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
ORDER BY tom.fecha DESC, tom.hora_programada DESC;

-- Vista Tomas Hoy
CREATE OR REPLACE VIEW `Vista_Tomas_Hoy` AS
SELECT 
    t.id_toma,
    p.nombre AS paciente,
    tr.nombre_tratamiento,
    m.nombre AS medicamento,
    tm.dosis,
    t.hora_programada,
    t.estado,
    t.observaciones,
    t.registrado_por,
    t.fecha_registro
FROM Toma t
JOIN Tratamiento_Medicamento tm ON t.id_tratamiento_medicamento = tm.id_tratamiento_medicamento
JOIN Tratamiento tr ON tm.id_tratamiento = tr.id_tratamiento
JOIN Paciente p ON tr.id_paciente = p.id_paciente
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
WHERE t.fecha = CURDATE()
ORDER BY t.hora_programada;

-- Vista General de Tratamientos
CREATE OR REPLACE VIEW `Vista_General_Tratamientos` AS 
SELECT 
    t.id_tratamiento, 
    t.nombre_tratamiento, 
    t.objetivo, 
    t.fecha_inicio, 
    t.fecha_fin, 
    t.estado, 
    t.observaciones, 
    p.nombre AS paciente, 
    p.edad, 
    p.genero, 
    p.contacto_emergencia, 
    p.observaciones AS paciente_observaciones
FROM Tratamiento t
JOIN Paciente p ON t.id_paciente = p.id_paciente;

