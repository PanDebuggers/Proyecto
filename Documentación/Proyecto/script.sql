-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS MediCareDesk;
USE MediCareDesk;

SET FOREIGN_KEY_CHECKS = 0;

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
  `id_paciente` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `edad` int,
  `genero` ENUM('M', 'F', 'Otro') DEFAULT 'M',
  `contacto_emergencia` varchar(15),
  `observaciones` text,
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP,
  `activo` boolean DEFAULT TRUE
);

CREATE TABLE `Cuidador` (
  `id_cuidador` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `relacion` varchar(50),
  `contacto` varchar(15),
  `email` varchar(100) UNIQUE NOT NULL,
  `password_hash` varchar(255) NOT NULL
);

CREATE TABLE `Paciente_Cuidador` (
  `id_paciente` int NOT NULL,
  `id_cuidador` int NOT NULL,
  `fecha_asignacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_paciente`, `id_cuidador`)
);

CREATE TABLE `Medicamento` (
  `id_medicamento` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL, 
  `principio_activo` varchar(100),
  `indicaciones` text,
  `fecha_caducidad` date,
  `contraindicaciones` text,
  `presentacion` ENUM('Comprimidas', 'Jarabe', 'Crema', 'Solución inyectable', 'otros') NOT NULL,
  `laboratorio` varchar(100),
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Tratamiento` (
  `id_tratamiento` int PRIMARY KEY AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `nombre_tratamiento` varchar(200) NOT NULL,
  `objetivo` text,
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` ENUM('activo', 'suspendido', 'finalizado', 'pendiente') DEFAULT 'pendiente',
  `observaciones` text,
  `responsable` varchar(100),
  `fecha_creacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `Tratamiento_Medicamento` (
  `id_tratamiento_medicamento` int PRIMARY KEY AUTO_INCREMENT,
  `id_tratamiento` int NOT NULL,
  `id_medicamento` int NOT NULL,
  `dosis` varchar(500),
  `frecuencia` ENUM('una_vez_al_dia', 'cada_8_horas', 'cada_12_horas', 'cada_24_horas', 'personalizada') DEFAULT 'una_vez_al_dia',
  `frecuencia_personalizada` varchar(100) NULL,
  `via_administracion` ENUM('oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea', 'inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica') DEFAULT 'oral',
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` ENUM('activo', 'suspendido', 'finalizado', 'pendiente') DEFAULT 'pendiente',
  `hora_preferida` time,
  `fecha_creacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_tratamiento_medicamento` (`id_tratamiento`, `id_medicamento`)
);

CREATE TABLE `Toma` (
  `id_toma` int PRIMARY KEY AUTO_INCREMENT,
  `id_tratamiento_medicamento` int NOT NULL,
  `fecha` date NOT NULL,
  `hora_programada` time NOT NULL,
  `estado` ENUM('programada', 'tomada', 'omitida') DEFAULT 'programada',
  `observaciones` text,
  `registrado_por` varchar(100),
  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP,
  `recordatorio_enviado` boolean DEFAULT FALSE,
  INDEX `idx_toma_fecha_estado` (`fecha`, `estado`)
);

CREATE TABLE `Bitacora_Eventos` (
  `id_evento` int PRIMARY KEY AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `tipo_evento` ENUM('medicamento_tomado', 'medicamento_omitido', 'efecto_adverso', 'interaccion_detectada', 'cambio_tratamiento', 'recordatorio_enviado', 'sistema', 'otro') DEFAULT 'otro',
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

SET FOREIGN_KEY_CHECKS = 1;

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


-- Autenticación de Cuidador
DELIMITER //
CREATE OR REPLACE PROCEDURE `AutenticarCuidadorSimple`(
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    DECLARE v_cuidador_id INT;
    DECLARE v_hash_correcto VARCHAR(255);

    SELECT id_cuidador, password_hash 
    INTO v_cuidador_id, v_hash_correcto
    FROM Cuidador 
    WHERE email = p_email;

    IF v_cuidador_id IS NULL THEN
        SELECT 'USER_NOT_FOUND' AS resultado;
    ELSEIF v_hash_correcto = p_password_hash THEN
        SELECT 'SUCCESS' AS resultado, v_cuidador_id AS id_cuidador;
    ELSE
        SELECT 'INVALID_PASSWORD' AS resultado;
    END IF;
END //
DELIMITER ;

-- Generar tomas para un tratamiento-medicamento
DELIMITER //
DROP PROCEDURE IF EXISTS `GenerarTomasTratamiento`;
CREATE PROCEDURE `GenerarTomasTratamiento`(
    IN p_id_tratamiento_medicamento INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    DECLARE v_frecuencia ENUM('una_vez_al_dia', 'cada_8_horas', 'cada_12_horas', 'cada_24_horas', 'personalizada');
    DECLARE v_hora_preferida TIME;
    DECLARE v_fecha_actual DATE;
    DECLARE v_tomas_por_dia INT;
    DECLARE v_contador INT;
    DECLARE v_hora_toma TIME;

    IF p_fecha_fin < p_fecha_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de fin no puede ser anterior a la fecha de inicio';
    END IF;

    SELECT frecuencia, IFNULL(hora_preferida, '08:00:00')
    INTO v_frecuencia, v_hora_preferida
    FROM Tratamiento_Medicamento
    WHERE id_tratamiento_medicamento = p_id_tratamiento_medicamento;

    IF v_frecuencia IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Frecuencia no encontrada para el tratamiento';
    END IF;

    CASE v_frecuencia
        WHEN 'una_vez_al_dia' THEN SET v_tomas_por_dia = 1;
        WHEN 'cada_8_horas' THEN SET v_tomas_por_dia = 3;
        WHEN 'cada_12_horas' THEN SET v_tomas_por_dia = 2;
        WHEN 'cada_24_horas' THEN SET v_tomas_por_dia = 1;
        WHEN 'personalizada' THEN SET v_tomas_por_dia = 1;
        ELSE SET v_tomas_por_dia = 1;
    END CASE;

    SET v_fecha_actual = p_fecha_inicio;

    WHILE v_fecha_actual <= p_fecha_fin DO
        SET v_contador = 0;
        WHILE v_contador < v_tomas_por_dia DO
            SET v_hora_toma = ADDTIME(v_hora_preferida, SEC_TO_TIME(v_contador * (86400 / v_tomas_por_dia)));
            INSERT INTO Toma (id_tratamiento_medicamento, fecha, hora_programada, estado)
            VALUES (p_id_tratamiento_medicamento, v_fecha_actual, v_hora_toma, 'programada');
            SET v_contador = v_contador + 1;
        END WHILE;
        SET v_fecha_actual = DATE_ADD(v_fecha_actual, INTERVAL 1 DAY);
    END WHILE;
END //
DELIMITER ;

-- Asignar un medicamento a un tratamiento
DELIMITER //
DROP PROCEDURE IF EXISTS `AsignarMedicamentoATratamiento`;
CREATE PROCEDURE `AsignarMedicamentoATratamiento`(
    IN p_id_tratamiento INT,
    IN p_id_medicamento INT,
    IN p_dosis VARCHAR(500),
    IN p_frecuencia ENUM('una_vez_al_dia', 'cada_8_horas', 'cada_12_horas', 'cada_24_horas', 'personalizada'),
    IN p_via_administracion ENUM('oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea', 'inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica'),
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_estado ENUM('activo', 'suspendido', 'finalizado', 'pendiente'),
    IN p_hora_preferida TIME
)
BEGIN
    INSERT INTO Tratamiento_Medicamento (id_tratamiento, id_medicamento, dosis, frecuencia, via_administracion, fecha_inicio, fecha_fin, estado, hora_preferida)
    VALUES (p_id_tratamiento, p_id_medicamento, p_dosis, p_frecuencia, p_via_administracion, p_fecha_inicio, p_fecha_fin, p_estado, p_hora_preferida);
END //
DELIMITER ;

-- Marcar toma como verificada
DELIMITER //
DROP PROCEDURE IF EXISTS `MarcarTomaComoVerificada`;
CREATE PROCEDURE `MarcarTomaComoVerificada`(
    IN p_id_toma INT
)
BEGIN
    UPDATE Toma
    SET estado = 'tomada'
    WHERE id_toma = p_id_toma;
END //
DELIMITER ;

-- Marcar toma como omitida
DELIMITER //
DROP PROCEDURE IF EXISTS `MarcarTomaComoOmitida`;
CREATE PROCEDURE `MarcarTomaComoOmitida`(
    IN p_id_toma INT
)
BEGIN
    UPDATE Toma
    SET estado = 'omitida'
    WHERE id_toma = p_id_toma;
END //
DELIMITER ;

-- Obtener historial de tomas
DELIMITER //
DROP PROCEDURE IF EXISTS `ObtenerHistorialTomas`;
CREATE PROCEDURE `ObtenerHistorialTomas`(
    IN p_id_paciente INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    SELECT * FROM Toma
    WHERE id_tratamiento_medicamento IN (
        SELECT id_tratamiento_medicamento 
        FROM Tratamiento_Medicamento 
        WHERE id_tratamiento IN (
            SELECT id_tratamiento
            FROM Tratamiento
            WHERE id_paciente = p_id_paciente
        )
    )
    AND fecha BETWEEN p_fecha_inicio AND p_fecha_fin;
END //
DELIMITER ;

-- Generar reporte resumen de tomas por paciente
DELIMITER //
DROP PROCEDURE IF EXISTS `GenerarReporteTomasPaciente`;
CREATE PROCEDURE `GenerarReporteTomasPaciente`(
    IN p_id_paciente INT
)
BEGIN
    SELECT p.nombre AS paciente, 
           t.nombre_tratamiento, 
           m.nombre AS medicamento, 
           COUNT(CASE WHEN tom.estado = 'tomada' THEN 1 END) AS tomas_completadas,
           COUNT(CASE WHEN tom.estado = 'omitida' THEN 1 END) AS tomas_omitidas,
           COUNT(CASE WHEN tom.estado = 'pendiente' OR tom.estado = 'programada' THEN 1 END) AS tomas_pendientes
    FROM Paciente p
    JOIN Tratamiento t ON p.id_paciente = t.id_paciente
    JOIN Tratamiento_Medicamento tm ON t.id_tratamiento = tm.id_tratamiento
    JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
    LEFT JOIN Toma tom ON tm.id_tratamiento_medicamento = tom.id_tratamiento_medicamento
    WHERE p.id_paciente = p_id_paciente
    GROUP BY p.id_paciente, t.id_tratamiento, m.id_medicamento;
END //
DELIMITER ;


-- inserccion datos de prueba 

-- 1. Insertar Paciente (Adulto Mayor)
INSERT INTO `Paciente` (`nombre`, `edad`, `genero`, `contacto_emergencia`, `observaciones`) 
VALUES ('Carlos Martínez Fernández', 78, 'M', '+56987654321', 'Paciente con hipertensión y diabetes tipo 2. Requiere asistencia para movilidad. Alergia a la penicilina.');

-- 2. Insertar Cuidador
INSERT INTO `Cuidador` (`nombre`, `relacion`, `contacto`, `email`, `password_hash`) 
VALUES ('María González Pérez', 'Hija', '+56912345678', 'maria.gonzalez@email.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');

-- 3. Insertar Medicamentos
INSERT INTO `Medicamento` (`nombre`, `principio_activo`, `indicaciones`, `fecha_caducidad`, `contraindicaciones`, `presentacion`, `laboratorio`) VALUES 
('Atorvastatina 40mg', 'Atorvastatina', 'Control de colesterol alto', '2025-06-30', 'Enfermedad hepática activa', 'Comprimidas', 'Laboratorio Farmacol'),
('Metformina 850mg', 'Metformina', 'Diabetes mellitus tipo 2', '2024-12-15', 'Insuficiencia renal severa', 'Comprimidas', 'Laboratorio DiabetCare'),
('Donepezilo 10mg', 'Donepezilo', 'Tratamiento de Alzheimer moderado a severo', '2025-09-20', 'Hipersensibilidad al donepezilo', 'Comprimidas', 'Laboratorio NeuroHealth'),
('Omeprazol 20mg', 'Omeprazol', 'Protección gástrica', '2026-03-10', 'Hipersensibilidad al omeprazol', 'Comprimidas', 'Laboratorio GastroSafe');

-- 4. Insertar Tratamiento
INSERT INTO `Tratamiento` (`id_paciente`, `nombre_tratamiento`, `objetivo`, `fecha_inicio`, `fecha_fin`, `estado`, `observaciones`, `responsable`) 
VALUES (1, 'Manejo integral de enfermedades crónicas', 'Control de hipertensión, diabetes y deterioro cognitivo', '2023-11-01', '2024-11-01', 'activo', 'Monitorizar presión arterial diaria y glucosa capilar', 'Dr. Alejandro Soto');

-- 5. Asociar Medicamentos al Tratamiento
INSERT INTO `Tratamiento_Medicamento` (`id_tratamiento`, `id_medicamento`, `dosis`, `frecuencia`, `via_administracion`, `fecha_inicio`, `hora_preferida`) VALUES 
(1, 1, '1 tableta al día', 'una_vez_al_dia', 'oral', '2023-11-01', '20:00:00'),
(1, 2, '1 tableta cada 12 horas', 'cada_12_horas', 'oral', '2023-11-01', '08:00:00'),
(1, 3, '1 tableta al acostarse', 'una_vez_al_dia', 'oral', '2023-11-01', '22:00:00'),
(1, 4, '1 cápsula en ayunas', 'una_vez_al_dia', 'oral', '2023-11-01', '07:30:00');

-- 6. Registrar Tomas de Medicamentos
INSERT INTO `Toma` (`id_tratamiento_medicamento`, `fecha`, `hora_programada`, `estado`, `registrado_por`) VALUES 
(2, '2023-11-15', '08:00:00', 'tomada', 'María González'),
(2, '2023-11-15', '20:00:00', 'omitida', NULL),
(3, '2023-11-15', '22:00:00', 'tomada', 'María González');

-- 7. Registrar Eventos en Bitácora
INSERT INTO `Bitacora_Eventos` (`id_paciente`, `tipo_evento`, `descripcion`) VALUES 
(1, 'medicamento_omitido', 'Paciente olvidó tomar Metformina en la dosis de las 20:00 hrs'),
(1, 'efecto_adverso', 'Paciente reporta mareos leves después de tomar Donepezilo'),
(1, 'recordatorio_enviado', 'Se envió SMS al cuidador sobre dosis omitida de Metformina');
