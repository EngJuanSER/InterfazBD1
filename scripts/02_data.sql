/*==============================================================*/
/* Script para insertar datos de prueba - REQUERIMIENTO         */
/* 5 registros en TipoDocumento y 5 registros en Cliente        */
/*==============================================================*/


-- Insertar datos básicos en TIPODOCUMENTO
INSERT INTO TIPODOCUMENTO (ID_TIPO_DOC, DESC_TIPO_DOC) VALUES ('CC', 'Cédula de Ciudadanía');
INSERT INTO TIPODOCUMENTO (ID_TIPO_DOC, DESC_TIPO_DOC) VALUES ('CE', 'Cédula de Extranjería');
INSERT INTO TIPODOCUMENTO (ID_TIPO_DOC, DESC_TIPO_DOC) VALUES ('TI', 'Tarjeta de Identidad');
INSERT INTO TIPODOCUMENTO (ID_TIPO_DOC, DESC_TIPO_DOC) VALUES ('PA', 'Pasaporte');
INSERT INTO TIPODOCUMENTO (ID_TIPO_DOC, DESC_TIPO_DOC) VALUES ('NI', 'NIT');


-- Insertar 5 Clientes de prueba 
INSERT INTO CLIENTE (CLIENTE_ID, ID_TIPO_DOC, NOMBRE_CLIENTE, APELLIDO_CLIENTE, N_DOCUMENTO_CLIENTE,
                     DIRECCION_NOTIFICACION, FECHA_NACIMIENTO, OBSERVACIONES)
VALUES (1, 'CC', 'Pedro', 'López', '1111222233', 
        'Calle 100 #15-20, Bogotá', TO_DATE('1980-05-15', 'YYYY-MM-DD'), 
        'Cliente preferencial');

INSERT INTO CLIENTE (CLIENTE_ID, ID_TIPO_DOC, NOMBRE_CLIENTE, APELLIDO_CLIENTE, N_DOCUMENTO_CLIENTE,
                     DIRECCION_NOTIFICACION, FECHA_NACIMIENTO, OBSERVACIONES)
VALUES (2, 'CC', 'Ana', 'Ramírez', '4444555566', 
        'Carrera 7 #45-30, Medellín', TO_DATE('1975-08-22', 'YYYY-MM-DD'), 
        'Contactar por email');

INSERT INTO CLIENTE (CLIENTE_ID, ID_TIPO_DOC, NOMBRE_CLIENTE, APELLIDO_CLIENTE, N_DOCUMENTO_CLIENTE,
                     DIRECCION_NOTIFICACION, FECHA_NACIMIENTO, OBSERVACIONES)
VALUES (3, 'CE', 'Luis', 'Fernández', '7777888899', 
        'Avenida 6 #10-50, Cali', TO_DATE('1990-12-10', 'YYYY-MM-DD'), 
        'Extranjero residente');

INSERT INTO CLIENTE (CLIENTE_ID, ID_TIPO_DOC, NOMBRE_CLIENTE, APELLIDO_CLIENTE, N_DOCUMENTO_CLIENTE,
                     DIRECCION_NOTIFICACION, FECHA_NACIMIENTO, OBSERVACIONES)
VALUES (4, 'TI', 'María', 'Torres', '9999888877', 
        'Calle 50 #20-15, Barranquilla', TO_DATE('2005-03-25', 'YYYY-MM-DD'), 
        'Cliente menor de edad');

INSERT INTO CLIENTE (CLIENTE_ID, ID_TIPO_DOC, NOMBRE_CLIENTE, APELLIDO_CLIENTE, N_DOCUMENTO_CLIENTE,
                     DIRECCION_NOTIFICACION, FECHA_NACIMIENTO, OBSERVACIONES)
VALUES (5, 'PA', 'John', 'Smith', 'AB123456', 
        'Carrera 15 #80-40, Bogotá', TO_DATE('1985-07-18', 'YYYY-MM-DD'), 
        'Cliente extranjero');

COMMIT;
