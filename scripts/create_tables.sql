-- =====================================================
-- Script para crear tablas en Oracle Database
-- Base de Datos: Gestión de Clientes
-- Autor: Sistema de Registro de Clientes
-- Fecha: 2025
-- =====================================================

-- Eliminar tablas si existen (opcional, para pruebas)
-- DROP TABLE Cliente CASCADE CONSTRAINTS;
-- DROP TABLE TipoDocumento CASCADE CONSTRAINTS;

-- =====================================================
-- CREACIÓN DE TABLAS
-- =====================================================

-- Tabla: TipoDocumento
-- Descripción: Almacena los tipos de documento disponibles
CREATE TABLE TipoDocumento (
    idTipoDoc VARCHAR2(2) NOT NULL,
    descTipoDoc VARCHAR2(30) NOT NULL,
    CONSTRAINT pk_tipodocumento PRIMARY KEY (idTipoDoc)
);

-- Tabla: Cliente
-- Descripción: Almacena la información de los clientes
CREATE TABLE Cliente (
    codCliente VARCHAR2(5) NOT NULL,
    nomCliente VARCHAR2(30) NOT NULL,
    apellCliente VARCHAR2(30) NOT NULL,
    idTipoDoc VARCHAR2(2) NOT NULL,
    nDocumento VARCHAR2(15) NOT NULL,
    CONSTRAINT pk_cliente PRIMARY KEY (codCliente),
    CONSTRAINT fk_cliente_tipodoc FOREIGN KEY (idTipoDoc) 
        REFERENCES TipoDocumento(idTipoDoc)
);

-- =====================================================
-- INSERCIÓN DE DATOS
-- =====================================================

-- Insertar 5 registros en TipoDocumento
INSERT INTO TipoDocumento (idTipoDoc, descTipoDoc) 
VALUES ('CC', 'Cédula de Ciudadanía');

INSERT INTO TipoDocumento (idTipoDoc, descTipoDoc) 
VALUES ('CE', 'Cédula de Extranjería');

INSERT INTO TipoDocumento (idTipoDoc, descTipoDoc) 
VALUES ('TI', 'Tarjeta de Identidad');

INSERT INTO TipoDocumento (idTipoDoc, descTipoDoc) 
VALUES ('PA', 'Pasaporte');

INSERT INTO TipoDocumento (idTipoDoc, descTipoDoc) 
VALUES ('RC', 'Registro Civil');

-- Insertar 5 registros en Cliente
INSERT INTO Cliente (codCliente, nomCliente, apellCliente, idTipoDoc, nDocumento) 
VALUES ('00001', 'Juan', 'Pérez García', 'CC', '1234567890');

INSERT INTO Cliente (codCliente, nomCliente, apellCliente, idTipoDoc, nDocumento) 
VALUES ('00002', 'María', 'González López', 'CC', '9876543210');

INSERT INTO Cliente (codCliente, nomCliente, apellCliente, idTipoDoc, nDocumento) 
VALUES ('00003', 'Carlos', 'Rodríguez Martínez', 'CE', '123456789');

INSERT INTO Cliente (codCliente, nomCliente, apellCliente, idTipoDoc, nDocumento) 
VALUES ('00004', 'Ana', 'Sánchez Torres', 'PA', 'AB1234567');

INSERT INTO Cliente (codCliente, nomCliente, apellCliente, idTipoDoc, nDocumento) 
VALUES ('00005', 'Luis', 'Ramírez Díaz', 'TI', '1098765432');

-- Confirmar transacción
COMMIT;

-- =====================================================
-- CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Verificar datos insertados en TipoDocumento
SELECT * FROM TipoDocumento ORDER BY idTipoDoc;

-- Verificar datos insertados en Cliente
SELECT * FROM Cliente ORDER BY codCliente;

-- Consulta con JOIN para ver clientes con tipo de documento
SELECT 
    c.codCliente,
    c.nomCliente,
    c.apellCliente,
    t.descTipoDoc,
    c.nDocumento
FROM 
    Cliente c
INNER JOIN 
    TipoDocumento t ON c.idTipoDoc = t.idTipoDoc
ORDER BY 
    c.codCliente;

-- =====================================================
-- INFORMACIÓN ADICIONAL
-- =====================================================

-- Para ejecutar este script en Oracle:
-- 1. Conectarse a Oracle SQL Developer o SQL*Plus
-- 2. sqlplus usuario/contraseña@host:puerto/servicio
-- 3. @ruta/al/archivo/create_tables.sql

-- Ejemplo:
-- sqlplus system/oracle@localhost:1521/XEPDB1
-- @/home/usuario/InterfazBD1/scripts/create_tables.sql
