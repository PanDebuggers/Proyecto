-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS MediCareDesk;
USE MediCareDesk;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `Vista_Tratamiento_Completo`;
DROP TABLE IF EXISTS `Vista_Resumen_Tomas`;
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
  -- Campos para login
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
  `frecuencia_personalizada` varchar(100) NULL, -- Para casos especiales
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
  `estado` ENUM('programada', 'tomada', 'omitida', 'vencida') DEFAULT 'programada',
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

-- Vistas
CREATE OR REPLACE VIEW `Vista_Tratamiento_Completo` AS
SELECT 
    t.id_tratamiento,
    t.nombre_tratamiento,
    t.objetivo,
    t.fecha_inicio as fecha_inicio_tratamiento,
    t.fecha_fin as fecha_fin_tratamiento,
    t.estado as estado_tratamiento,
    p.nombre as paciente,
    p.edad as edad_paciente,
    m.nombre as medicamento,
    m.principio_activo,
    tm.dosis,
    tm.frecuencia,
    tm.via_administracion,
    tm.fecha_inicio as fecha_inicio_medicamento,
    tm.fecha_fin as fecha_fin_medicamento,
    tm.estado as estado_medicamento,
    tm.hora_preferida
FROM Tratamiento t
JOIN Paciente p ON t.id_paciente = p.id_paciente
JOIN Tratamiento_Medicamento tm ON t.id_tratamiento = tm.id_tratamiento
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento;

CREATE OR REPLACE VIEW `Vista_Resumen_Tomas` AS
SELECT 
    p.nombre as paciente,
    t.nombre_tratamiento,
    m.nombre as medicamento,
    COUNT(CASE WHEN tom.estado = 'tomada' THEN 1 END) as tomas_completadas,
    COUNT(CASE WHEN tom.estado = 'omitida' THEN 1 END) as tomas_omitidas,
    COUNT(CASE WHEN tom.estado = 'pendiente' OR tom.estado = 'programada' THEN 1 END) as tomas_pendientes,
    COUNT(CASE WHEN tom.estado = 'vencida' THEN 1 END) as tomas_vencidas,
    COUNT(*) as total_tomas,
    ROUND((COUNT(CASE WHEN tom.estado = 'tomada' THEN 1 END) / COUNT(*)) * 100, 2) as porcentaje_adherencia
FROM Paciente p
JOIN Tratamiento t ON p.id_paciente = t.id_paciente
JOIN Tratamiento_Medicamento tm ON t.id_tratamiento = tm.id_tratamiento
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
LEFT JOIN Toma tom ON tm.id_tratamiento_medicamento = tom.id_tratamiento_medicamento
GROUP BY p.id_paciente, t.id_tratamiento, m.id_medicamento;

CREATE OR REPLACE VIEW `Vista_Tomas_Hoy` AS
SELECT 
    t.id_toma,
    p.nombre as paciente,
    tr.nombre_tratamiento,
    m.nombre as medicamento,
    tm.dosis,
    t.hora_programada,
    t.hora_real,
    t.estado,
    t.observaciones,
    tm.instrucciones_especiales
FROM Toma t
JOIN Tratamiento_Medicamento tm ON t.id_tratamiento_medicamento = tm.id_tratamiento_medicamento
JOIN Tratamiento tr ON tm.id_tratamiento = tr.id_tratamiento
JOIN Paciente p ON tr.id_paciente = p.id_paciente
JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
WHERE t.fecha = CURDATE()
ORDER BY t.hora_programada;

-- Procedimientos almacenados
DELIMITER //

CREATE PROCEDURE `AutenticarCuidador`(
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255)
)
BEGIN
    DECLARE v_cuidador_id INT;
    DECLARE v_bloqueado BOOLEAN DEFAULT FALSE;

    -- Verificar si el cuidador existe y está activo
    SELECT id_cuidador INTO v_cuidador_id
    FROM Cuidador 
    WHERE email = p_email 
    AND activo = TRUE 
    AND (bloqueado_hasta IS NULL OR bloqueado_hasta < NOW());
    
    IF v_cuidador_id IS NOT NULL THEN
        -- Verificar contraseña
        IF EXISTS (
            SELECT 1 FROM Cuidador 
            WHERE id_cuidador = v_cuidador_id 
            AND password_hash = p_password_hash
        ) THEN
            -- Login exitoso
            UPDATE Cuidador 
            SET ultimo_acceso = NOW(), 
                intentos_fallidos = 0,
                bloqueado_hasta = NULL
            WHERE id_cuidador = v_cuidador_id;
            
            SELECT 'SUCCESS' as resultado, v_cuidador_id as id_cuidador;
        ELSE
            -- Contraseña incorrecta
            UPDATE Cuidador 
            SET intentos_fallidos = intentos_fallidos + 1,
                bloqueado_hasta = CASE 
                    WHEN intentos_fallidos >= 4 THEN DATE_ADD(NOW(), INTERVAL 30 MINUTE)
                    ELSE bloqueado_hasta
                END
            WHERE id_cuidador = v_cuidador_id;
            
            SELECT 'INVALID_PASSWORD' as resultado;
        END IF;
    ELSE
        SELECT 'USER_NOT_FOUND' as resultado;
    END IF;
END //

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

    -- Obtener frecuencia y hora preferida
    SELECT frecuencia, IFNULL(hora_preferida, '08:00:00')
    INTO v_frecuencia, v_hora_preferida
    FROM Tratamiento_Medicamento
    WHERE id_tratamiento_medicamento = p_id_tratamiento_medicamento;
    
    -- Configurar intervalos según frecuencia
    CASE v_frecuencia
        WHEN 'una_vez_al_dia' THEN SET v_tomas_por_dia = 1;
        WHEN 'cada_8_horas' THEN SET v_tomas_por_dia = 3;
        WHEN 'cada_12_horas' THEN SET v_tomas_por_dia = 2;
        WHEN 'cada_24_horas' THEN SET v_tomas_por_dia = 1;
        ELSE SET v_tomas_por_dia = 1;
    END CASE;
    
    -- Generar tomas para cada día
    SET v_fecha_actual = p_fecha_inicio;
    
    WHILE v_fecha_actual <= p_fecha_fin DO
        SET v_contador = 0;
        
        WHILE v_contador < v_tomas_por_dia DO
            -- Calcular hora de la toma
            SET v_hora_toma = ADDTIME(v_hora_preferida, SEC_TO_TIME(v_contador * (86400 / v_tomas_por_dia)));
            
            -- Insertar toma
            INSERT INTO Toma (id_tratamiento_medicamento, fecha, hora_programada, estado)
            VALUES (p_id_tratamiento_medicamento, v_fecha_actual, v_hora_toma, 'programada');
            
            SET v_contador = v_contador + 1;
        END WHILE;
        
        SET v_fecha_actual = DATE_ADD(v_fecha_actual, INTERVAL 1 DAY);
    END WHILE;
    
END //

DELIMITER ;


--ejemplos

INSERT INTO `Medicamento` (`nombre`, `principio_activo`, `indicaciones`, `fecha_caducidad`, `contraindicaciones`, `presentacion`, `laboratorio`) VALUES
('Losartán 50mg', 'Losartán', 'Hipertensión arterial', '2025-12-31', 'Embarazo, hiperpotasemia', 'Comprimidas', 'Laboratorio ABC'),
('Metformina 500mg', 'Metformina', 'Diabetes tipo 2', '2025-10-15', 'Insuficiencia renal', 'Comprimidas', 'Laboratorio XYZ'),
('Aspirina 100mg', 'Ácido acetilsalicílico', 'Prevención cardiovascular', '2026-03-20', 'Úlcera péptica activa', 'Comprimidas', 'Laboratorio DEF'),
('Omeprazol 20mg', 'Omeprazol', 'Protector gástrico', '2025-08-15', 'Hipersensibilidad', 'Cápsulas', 'Laboratorio GHI');

INSERT INTO `Tratamiento` (`id_paciente`, `nombre_tratamiento`, `objetivo`, `fecha_inicio`, `fecha_fin`, `estado`, `responsable`) VALUES
(1, 'Control de Hipertensión', 'Mantener presión arterial < 140/90', '2024-01-15', '2024-12-31', 'activo', 'Dr. González'),
(2, 'Control de Diabetes', 'Mantener HbA1c < 7%', '2024-02-01', '2024-12-31', 'activo', 'Dr. Martínez'),
(3, 'Tratamiento Integral', 'Control de múltiples condiciones', '2024-03-01', '2024-12-31', 'activo', 'Dr. López');

INSERT INTO `Tratamiento_Medicamento` (`id_tratamiento`, `id_medicamento`, `dosis`, `frecuencia`, `via_administracion`, `fecha_inicio`, `estado`, `hora_preferida`) VALUES
(1, 1, '50mg', 'una_vez_al_dia', 'oral', '2024-01-15', 'activo', '08:00:00'),
(2, 2, '500mg', 'dos_veces_al_dia', 'oral', '2024-02-01', 'activo', '08:00:00'),
(3, 3, '100mg', 'una_vez_al_dia', 'oral', '2024-03-01', 'activo', '20:00:00'),
(3, 4, '20mg', 'una_vez_al_dia', 'oral', '2024-03-01', 'activo', '08:00:00');

INSERT INTO `Toma` (`id_tratamiento_medicamento`, `fecha`, `hora_programada`, `estado`, `recordatorio_enviado`) VALUES
(1, '2024-01-15', '08:00:00', 'programada', FALSE),
(2, '2024-02-01', '08:00:00', 'tomada', TRUE),
(2, '2024-02-01', '20:00:00', 'programada', FALSE),
(3, '2024-03-01', '20:00:00', 'programada', FALSE),
(4, '2024-03-01', '08:00:00', 'tomada', TRUE);
