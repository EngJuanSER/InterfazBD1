-- ================================================================
-- Database Schema for Sistema de Gestion Legal (Abogados)
-- Adapted from Oracle 12c to Oracle 23c Free
-- PRESERVES ORIGINAL STRUCTURE with Composite Primary Keys 
-- ================================================================

-- Drop existing tables and constraints (cleanup script)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE SUCESO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE RESULTADO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE DOCUMENTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE EXPEDIENTE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ESPECIA_ETAPA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE PAGO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CONTACTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CASO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CLIENTE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FK_ABOGADO_ESPECIAL CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ABOGADO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ETAPAPROCESAL CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE LUGAR CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE INSTANCIA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE IMPUGNACION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ESPECIALIZACION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TIPOLUGAR CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TIPOCONTACT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE TIPODOCUMENTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FORMAPAGO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FRANQUICIA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- ================================================================
-- CATALOG TABLES (Master Data)
-- ================================================================

/*==============================================================*/
/* Table: TIPODOCUMENTO                                         */
/*==============================================================*/
CREATE TABLE TIPODOCUMENTO (
   IDTIPODOC            VARCHAR2(2)           NOT NULL,
   DESCTIPODOC          VARCHAR2(30)          NOT NULL,
   CONSTRAINT PK_TIPODOCUMENTO PRIMARY KEY (IDTIPODOC)
);

/*==============================================================*/
/* Table: TIPOCONTACT                                           */
/*==============================================================*/
CREATE TABLE TIPOCONTACT (
   IDTIPOCONTA          VARCHAR2(3)           NOT NULL,
   DESCTIPOCONTA        VARCHAR2(30)          NOT NULL,
   CONSTRAINT PK_TIPOCONTACT PRIMARY KEY (IDTIPOCONTA)
);

/*==============================================================*/
/* Table: TIPOLUGAR                                             */
/*==============================================================*/
CREATE TABLE TIPOLUGAR (
   IDTIPOLUGAR          NUMBER(4,0)           NOT NULL,
   DESCTIPOLUGAR        VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_TIPOLUGAR PRIMARY KEY (IDTIPOLUGAR)
);

/*==============================================================*/
/* Table: FORMAPAGO                                             */
/*==============================================================*/
CREATE TABLE FORMAPAGO (
   IDFORMAPAGO          VARCHAR2(3)           NOT NULL,
   DESCFORMAPAGO        VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_FORMAPAGO PRIMARY KEY (IDFORMAPAGO)
);

/*==============================================================*/
/* Table: FRANQUICIA                                            */
/*==============================================================*/
CREATE TABLE FRANQUICIA (
   CODFRANQUICIA        VARCHAR2(3)           NOT NULL,
   NOMFRANQUICIA        VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_FRANQUICIA PRIMARY KEY (CODFRANQUICIA)
);

/*==============================================================*/
/* Table: ESPECIALIZACION                                       */
/*==============================================================*/
CREATE TABLE ESPECIALIZACION (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NOMESPECIALIZACION   VARCHAR2(30)          NOT NULL,
   CONSTRAINT PK_ESPECIALIZACION PRIMARY KEY (CODESPECIALIZACION)
);

/*==============================================================*/
/* Table: IMPUGNACION                                           */
/*==============================================================*/
CREATE TABLE IMPUGNACION (
   IDIMPUGNA            VARCHAR2(2)           NOT NULL,
   NOMIMPUGNA           VARCHAR2(30)          NOT NULL,
   CONSTRAINT PK_IMPUGNACION PRIMARY KEY (IDIMPUGNA)
);

/*==============================================================*/
/* Table: INSTANCIA                                             */
/*==============================================================*/
CREATE TABLE INSTANCIA (
   NINSTANCIA         NUMBER(2,0)           NOT NULL,
   DESCINSTANCIA      VARCHAR2(30)          NOT NULL,
   CONSTRAINT PK_INSTANCIA PRIMARY KEY (NINSTANCIA)
);

/*==============================================================*/
/* Table: ETAPAPROCESAL                                         */
/*==============================================================*/
CREATE TABLE ETAPAPROCESAL (
   CODETAPA             VARCHAR2(3)           NOT NULL,
   NOMETAPA             VARCHAR2(30)          NOT NULL,
   ORDEN                NUMBER(2,0)           NOT NULL,
   CONSTRAINT PK_ETAPAPROCESAL PRIMARY KEY (CODETAPA)
);

/*==============================================================*/
/* Table: LUGAR (Hierarchical)                                  */
/*==============================================================*/
CREATE TABLE LUGAR (
   CODLUGAR             VARCHAR2(5)           NOT NULL,
   IDTIPOLUGAR          NUMBER(4,0)           NOT NULL,
   LUG_CODLUGAR         VARCHAR2(5),
   NOMLUGAR             VARCHAR2(30)          NOT NULL,
   DIRELUGAR            VARCHAR2(50),
   TELLUGAR             VARCHAR2(10),
   EMAILLUGAR           VARCHAR2(50),
   CONSTRAINT PK_LUGAR PRIMARY KEY (CODLUGAR),
   CONSTRAINT FK_LUGAR_TIPOLUGAR FOREIGN KEY (IDTIPOLUGAR) REFERENCES TIPOLUGAR (IDTIPOLUGAR),
   CONSTRAINT FK_LUGAR_LUGAR FOREIGN KEY (LUG_CODLUGAR) REFERENCES LUGAR (CODLUGAR)
);

/*==============================================================*/
/* Table: ABOGADO                                               */
/*==============================================================*/
CREATE TABLE ABOGADO (
   CEDULA               VARCHAR2(10)          NOT NULL,
   NOMBRE               VARCHAR2(30)          NOT NULL,
   APELLIDO             VARCHAR2(30)          NOT NULL,
   NTARJETAPROFESIONAL  VARCHAR2(5)           NOT NULL,
   CONSTRAINT PK_ABOGADO PRIMARY KEY (CEDULA)
);

/*==============================================================*/
/* Table: FK_ABOGADO_ESPECIAL (Many-to-Many)                    */
/*==============================================================*/
CREATE TABLE FK_ABOGADO_ESPECIAL (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   CEDULA               VARCHAR2(10)          NOT NULL,
   CONSTRAINT PK_FK_ABOGADO_ESPECIAL PRIMARY KEY (CODESPECIALIZACION, CEDULA),
   CONSTRAINT FK_ABOGADO_ESP_ABOGADO FOREIGN KEY (CEDULA) REFERENCES ABOGADO (CEDULA),
   CONSTRAINT FK_ABOGADO_ESP_ESPECIAL FOREIGN KEY (CODESPECIALIZACION) REFERENCES ESPECIALIZACION (CODESPECIALIZACION)
);

/*==============================================================*/
/* Table: CLIENTE                                               */
/*==============================================================*/
CREATE TABLE CLIENTE (
   CODCLIENTE           VARCHAR2(5)           NOT NULL,
   IDTIPODOC            VARCHAR2(2)           NOT NULL,
   NOMCLIENTE           VARCHAR2(30)          NOT NULL,
   APELLCLIENTE         VARCHAR2(30)          NOT NULL,
   NDOCUMENTO           VARCHAR2(15)          NOT NULL,
   CONSTRAINT PK_CLIENTE PRIMARY KEY (CODCLIENTE),
   CONSTRAINT FK_CLIENTE_TIPODOC FOREIGN KEY (IDTIPODOC) REFERENCES TIPODOCUMENTO (IDTIPODOC)
);

/*==============================================================*/
/* Table: CONTACTO                                              */
/*==============================================================*/
CREATE TABLE CONTACTO (
   CODCLIENTE           VARCHAR2(5)           NOT NULL,
   IDCONTACTO           NUMBER(2,0)           NOT NULL,
   IDTIPOCONTA          VARCHAR2(3)           NOT NULL,
   INFOCONTACTO         VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_CONTACTO PRIMARY KEY (CODCLIENTE, IDCONTACTO),
   CONSTRAINT FK_CONTACTO_CLIENTE FOREIGN KEY (CODCLIENTE) REFERENCES CLIENTE (CODCLIENTE),
   CONSTRAINT FK_CONTACTO_TIPO FOREIGN KEY (IDTIPOCONTA) REFERENCES TIPOCONTACT (IDTIPOCONTA)
);

/*==============================================================*/
/* Table: CASO                                                  */
/*==============================================================*/
CREATE TABLE CASO (
   NOCASO               NUMBER(5,0)           NOT NULL,
   CODCLIENTE           VARCHAR2(5)           NOT NULL,
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   FECHAINICIO          DATE                  NOT NULL,
   FECHAFIN             DATE,
   VALOR                VARCHAR2(10)          NOT NULL,
   CONSTRAINT PK_CASO PRIMARY KEY (NOCASO),
   CONSTRAINT FK_CASO_CLIENTE FOREIGN KEY (CODCLIENTE) REFERENCES CLIENTE (CODCLIENTE),
   CONSTRAINT FK_CASO_ESPECIALIZACION FOREIGN KEY (CODESPECIALIZACION) REFERENCES ESPECIALIZACION (CODESPECIALIZACION)
);

/*==============================================================*/
/* Table: PAGO                                                  */
/*==============================================================*/
CREATE TABLE PAGO (
   CONSECPAGO         NUMBER(3,0)           NOT NULL,
   CODFRANQUICIA      VARCHAR2(3),
   IDFORMAPAGO        VARCHAR2(3),
   FECHAPAGO          DATE,
   VALORPAGO          NUMBER(10,0)          NOT NULL,
   NTARJETA           NUMBER(15,0),
   CONSTRAINT PK_PAGO PRIMARY KEY (CONSECPAGO),
   CONSTRAINT FK_PAGO_FRANQUICIA FOREIGN KEY (CODFRANQUICIA) REFERENCES FRANQUICIA (CODFRANQUICIA),
   CONSTRAINT FK_PAGO_FORMAPAGO FOREIGN KEY (IDFORMAPAGO) REFERENCES FORMAPAGO (IDFORMAPAGO)
);

/*==============================================================*/
/* Table: ESPECIA_ETAPA (Specialization Process Flow)           */
/*==============================================================*/
CREATE TABLE ESPECIA_ETAPA (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NINSTANCIA           NUMBER(2,0)           NOT NULL,
   INS_NINSTANCIA       NUMBER(2,0),
   CODETAPA             VARCHAR2(3)           NOT NULL,
   IDIMPUGNA            VARCHAR2(2),
   CONSTRAINT PK_ESPECIA_ETAPA PRIMARY KEY (CODESPECIALIZACION, NINSTANCIA, CODETAPA),
   CONSTRAINT FK_ESPECIA_ESPECIAL FOREIGN KEY (CODESPECIALIZACION) REFERENCES ESPECIALIZACION (CODESPECIALIZACION),
   CONSTRAINT FK_ESPECIA_ETAPA FOREIGN KEY (CODETAPA) REFERENCES ETAPAPROCESAL (CODETAPA),
   CONSTRAINT FK_ESPECIA_INSTANCIA FOREIGN KEY (INS_NINSTANCIA) REFERENCES INSTANCIA (NINSTANCIA),
   CONSTRAINT FK_ESPECIA_IMPUGNACION FOREIGN KEY (IDIMPUGNA) REFERENCES IMPUGNACION (IDIMPUGNA)
);

-- UNIQUE para permitir FK desde EXPEDIENTE
ALTER TABLE ESPECIA_ETAPA ADD CONSTRAINT UQ_ESPECIA_ETAPA_UNIQUE UNIQUE (CODESPECIALIZACION, NINSTANCIA);

/*==============================================================*/
/* Table: EXPEDIENTE (Composite PK - ORIGINAL STRUCTURE)        */
/*==============================================================*/
CREATE TABLE EXPEDIENTE (
   NOCASO               NUMBER(5,0)           NOT NULL,
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NINSTANCIA           NUMBER(2,0)           NOT NULL,
   CONSECEXPE           NUMBER(4,0)           NOT NULL,
   CEDULA               VARCHAR2(10),
   CODLUGAR             VARCHAR2(5)           NOT NULL,
   FECHAETAPA           DATE                  NOT NULL,
   CONSTRAINT PK_EXPEDIENTE PRIMARY KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE),
   CONSTRAINT FK_EXP_ABOGADO FOREIGN KEY (CEDULA) REFERENCES ABOGADO (CEDULA),
   CONSTRAINT FK_EXP_CASO FOREIGN KEY (NOCASO) REFERENCES CASO (NOCASO),
   CONSTRAINT FK_EXP_ESPECIA_ETAPA FOREIGN KEY (CODESPECIALIZACION, NINSTANCIA) REFERENCES ESPECIA_ETAPA (CODESPECIALIZACION, NINSTANCIA),
   CONSTRAINT FK_EXP_LUGAR FOREIGN KEY (CODLUGAR) REFERENCES LUGAR (CODLUGAR)
);

/*==============================================================*/
/* Table: DOCUMENTO                                             */
/*==============================================================*/
CREATE TABLE DOCUMENTO (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NOCASO               NUMBER(5,0)           NOT NULL,
   NINSTANCIA           NUMBER(2,0)           NOT NULL,
   CONSECEXPE           NUMBER(4,0)           NOT NULL,
   CONDOC               NUMBER(4,0)           NOT NULL,
   NOMDOC               VARCHAR2(50),
   UBICADOC             VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_DOCUMENTO PRIMARY KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONDOC),
   CONSTRAINT FK_DOCUMENTO_EXPEDIENTE FOREIGN KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE) REFERENCES EXPEDIENTE (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE)
);

/*==============================================================*/
/* Table: RESULTADO                                             */
/*==============================================================*/
CREATE TABLE RESULTADO (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NOCASO               NUMBER(5,0)           NOT NULL,
   NINSTANCIA           NUMBER(2,0)           NOT NULL,
   CONSECEXPE           NUMBER(4,0)           NOT NULL,
   CONSECRESUL          NUMBER(4,0)           NOT NULL,
   DESCRESUL            VARCHAR2(200)         NOT NULL,
   CONSTRAINT PK_RESULTADO PRIMARY KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSECRESUL),
   CONSTRAINT FK_RESULTADO_EXPEDIENTE FOREIGN KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE) REFERENCES EXPEDIENTE (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE)
);

/*==============================================================*/
/* Table: SUCESO                                                */
/*==============================================================*/
CREATE TABLE SUCESO (
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NOCASO               NUMBER(5,0)           NOT NULL,
   NINSTANCIA           NUMBER(2,0)           NOT NULL,
   CONSECEXPE           NUMBER(4,0)           NOT NULL,
   CONSUCESO            NUMBER(4,0)           NOT NULL,
   DESCSUCESO           VARCHAR2(200)         NOT NULL,
   CONSTRAINT PK_SUCESO PRIMARY KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSUCESO),
   CONSTRAINT FK_SUCESO_EXPEDIENTE FOREIGN KEY (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE) REFERENCES EXPEDIENTE (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE)
);

COMMIT;

EXIT;
