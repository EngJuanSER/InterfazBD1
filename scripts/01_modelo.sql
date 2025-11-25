/*==============================================================*/
/* DBMS name:      ORACLE Version 12c/19c/21c                   */
/* Created on:     2025-11-25                                   */
/* Description:    Adapted for Django (Surrogate Keys)          */
/*==============================================================*/

-- Cleanup
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ABOGADO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CASO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CLIENTE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE CONTACTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE DOCUMENTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ESPECIALIZACION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ESPECIA_ETAPA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE ETAPAPROCESAL CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE EXPEDIENTE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FK_ABOGADO_ESPECIAL CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FORMAPAGO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE FRANQUICIA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE IMPUGNACION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE INSTANCIA CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE LUGAR CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE PAGO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE RESULTADO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE SUCESO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TIPOCONTACT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TIPODOCUMENTO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TIPOLUGAR CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

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
   DESCFORMAPAGO        VARCHAR2(40)          NOT NULL,
   CONSTRAINT PK_FORMAPAGO PRIMARY KEY (IDFORMAPAGO)
);

/*==============================================================*/
/* Table: FRANQUICIA                                            */
/*==============================================================*/
CREATE TABLE FRANQUICIA (
   CODFRANQUICIA        VARCHAR2(3)           NOT NULL,
   NOMFRANQUICIA        VARCHAR2(40)          NOT NULL,
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
/* Table: ETAPAPROCESAL                                         */
/*==============================================================*/
CREATE TABLE ETAPAPROCESAL (
   CODETAPA             VARCHAR2(3)           NOT NULL,
   NOMETAPA             VARCHAR2(30)          NOT NULL,
   ORDEN                NUMBER(2,0)           DEFAULT 0,
   CONSTRAINT PK_ETAPAPROCESAL PRIMARY KEY (CODETAPA)
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
   NINSTANCIA           NUMBER(1,0)           NOT NULL,
   CONSTRAINT PK_INSTANCIA PRIMARY KEY (NINSTANCIA)
);

/*==============================================================*/
/* Table: LUGAR                                                 */
/*==============================================================*/
CREATE TABLE LUGAR (
   CODLUGAR             VARCHAR2(5)           NOT NULL,
   IDTIPOLUGAR          NUMBER(4,0)           NOT NULL,
   LUG_CODLUGAR         VARCHAR2(5),
   NOMLUGAR             VARCHAR2(30)          NOT NULL,
   DIRELUGAR            VARCHAR2(40)          NOT NULL,
   TELLUGAR             VARCHAR2(15)          NOT NULL,
   EMAILLUGAR           VARCHAR2(50),
   CONSTRAINT PK_LUGAR PRIMARY KEY (CODLUGAR),
   CONSTRAINT FK_LUGAR_TIPOLUGAR FOREIGN KEY (IDTIPOLUGAR) REFERENCES TIPOLUGAR (IDTIPOLUGAR),
   CONSTRAINT FK_LUGAR_PADRE FOREIGN KEY (LUG_CODLUGAR) REFERENCES LUGAR (CODLUGAR)
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
/* Table: CONTACTO (Has Composite PK -> Surrogate Added)        */
/*==============================================================*/
CREATE TABLE CONTACTO (
   ID_CONTACTO          NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   CODCLIENTE           VARCHAR2(5)           NOT NULL,
   CONSECONTACTO        NUMBER(4,0)           NOT NULL,
   IDTIPOCONTA          VARCHAR2(3)           NOT NULL,
   VALORCONTACTO        VARCHAR2(50)          NOT NULL,
   NOTIFICACION         NUMBER(1,0)           DEFAULT 0 NOT NULL,
   CONSTRAINT PK_CONTACTO_SURROGATE PRIMARY KEY (ID_CONTACTO),
   CONSTRAINT UK_CONTACTO_ORIGINAL UNIQUE (CODCLIENTE, CONSECONTACTO),
   CONSTRAINT FK_CONTACTO_CLIENTE FOREIGN KEY (CODCLIENTE) REFERENCES CLIENTE (CODCLIENTE),
   CONSTRAINT FK_CONTACTO_TIPO FOREIGN KEY (IDTIPOCONTA) REFERENCES TIPOCONTACT (IDTIPOCONTA)
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
/* Table: FK_ABOGADO_ESPECIAL (Composite PK -> Surrogate)       */
/*==============================================================*/
CREATE TABLE FK_ABOGADO_ESPECIAL (
   ID_ABOGADO_ESP       NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   CEDULA               VARCHAR2(10)          NOT NULL,
   CONSTRAINT PK_ABOGADO_ESP_SURROGATE PRIMARY KEY (ID_ABOGADO_ESP),
   CONSTRAINT UK_ABOGADO_ESP_ORIGINAL UNIQUE (CODESPECIALIZACION, CEDULA),
   CONSTRAINT FK_AE_ESPECIALIZACION FOREIGN KEY (CODESPECIALIZACION) REFERENCES ESPECIALIZACION (CODESPECIALIZACION),
   CONSTRAINT FK_AE_ABOGADO FOREIGN KEY (CEDULA) REFERENCES ABOGADO (CEDULA)
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
   CONSECPAGO           NUMBER(3,0)           NOT NULL,
   NOCASO               NUMBER(5,0)           NOT NULL,
   CODFRANQUICIA        VARCHAR2(3),
   IDFORMAPAGO          VARCHAR2(3),
   FECHAPAGO            DATE,
   VALORPAGO            NUMBER(10,0)          NOT NULL,
   NTARJETA             NUMBER(15,0),
   CONSTRAINT PK_PAGO PRIMARY KEY (CONSECPAGO),
   CONSTRAINT FK_PAGO_CASO FOREIGN KEY (NOCASO) REFERENCES CASO (NOCASO),
   CONSTRAINT FK_PAGO_FRANQUICIA FOREIGN KEY (CODFRANQUICIA) REFERENCES FRANQUICIA (CODFRANQUICIA),
   CONSTRAINT FK_PAGO_FORMAPAGO FOREIGN KEY (IDFORMAPAGO) REFERENCES FORMAPAGO (IDFORMAPAGO)
);

/*==============================================================*/
/* Table: ESPECIA_ETAPA (Composite PK -> Surrogate)             */
/*==============================================================*/
CREATE TABLE ESPECIA_ETAPA (
   ID_ESPECIA_ETAPA     NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NINSTANCIA           NUMBER(1,0)           NOT NULL,
   INS_NINSTANCIA       NUMBER(1,0),
   CODETAPA             VARCHAR2(3)           NOT NULL,
   IDIMPUGNA            VARCHAR2(2),
   CONSTRAINT PK_ESPECIA_ETAPA_SURROGATE PRIMARY KEY (ID_ESPECIA_ETAPA),
   CONSTRAINT UK_ESPECIA_ETAPA_ORIGINAL UNIQUE (CODESPECIALIZACION, NINSTANCIA, CODETAPA),
   CONSTRAINT FK_EE_ESPECIALIZACION FOREIGN KEY (CODESPECIALIZACION) REFERENCES ESPECIALIZACION (CODESPECIALIZACION),
   CONSTRAINT FK_EE_INSTANCIA FOREIGN KEY (NINSTANCIA) REFERENCES INSTANCIA (NINSTANCIA),
   CONSTRAINT FK_EE_INSTANCIA_SIG FOREIGN KEY (INS_NINSTANCIA) REFERENCES INSTANCIA (NINSTANCIA),
   CONSTRAINT FK_EE_ETAPA FOREIGN KEY (CODETAPA) REFERENCES ETAPAPROCESAL (CODETAPA),
   CONSTRAINT FK_EE_IMPUGNACION FOREIGN KEY (IDIMPUGNA) REFERENCES IMPUGNACION (IDIMPUGNA)
);

/*==============================================================*/
/* Table: EXPEDIENTE (Composite PK -> Surrogate)                */
/*==============================================================*/
CREATE TABLE EXPEDIENTE (
   ID_EXPEDIENTE        NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   NOCASO               NUMBER(5,0)           NOT NULL,
   CODESPECIALIZACION   VARCHAR2(3)           NOT NULL,
   NINSTANCIA           NUMBER(1,0)           NOT NULL,
   CONSECEXPE           NUMBER(4,0)           NOT NULL,
   CEDULA               VARCHAR2(10),
   CODLUGAR             VARCHAR2(5)           NOT NULL,
   FECHAETAPA           DATE                  NOT NULL,
   PASOETAPA            NUMBER(2,0),
   CONSTRAINT PK_EXPEDIENTE_SURROGATE PRIMARY KEY (ID_EXPEDIENTE),
   CONSTRAINT UK_EXPEDIENTE_ORIGINAL UNIQUE (NOCASO, CONSECEXPE),
   CONSTRAINT FK_EXP_CASO FOREIGN KEY (NOCASO) REFERENCES CASO (NOCASO),
   CONSTRAINT FK_EXP_ABOGADO FOREIGN KEY (CEDULA) REFERENCES ABOGADO (CEDULA),
   CONSTRAINT FK_EXP_LUGAR FOREIGN KEY (CODLUGAR) REFERENCES LUGAR (CODLUGAR)
);

/*==============================================================*/
/* Table: DOCUMENTO (Composite PK -> Surrogate)                 */
/*==============================================================*/
CREATE TABLE DOCUMENTO (
   ID_DOCUMENTO         NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   ID_EXPEDIENTE        NUMBER(10)            NOT NULL,
   CONDOC               NUMBER(4,0)           NOT NULL,
   UBICADOC             VARCHAR2(50)          NOT NULL,
   CONSTRAINT PK_DOCUMENTO_SURROGATE PRIMARY KEY (ID_DOCUMENTO),
   CONSTRAINT UK_DOCUMENTO_ORIGINAL UNIQUE (ID_EXPEDIENTE, CONDOC),
   CONSTRAINT FK_DOC_EXPEDIENTE FOREIGN KEY (ID_EXPEDIENTE) REFERENCES EXPEDIENTE (ID_EXPEDIENTE)
);

/*==============================================================*/
/* Table: RESULTADO (Composite PK -> Surrogate)                 */
/*==============================================================*/
CREATE TABLE RESULTADO (
   ID_RESULTADO         NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   ID_EXPEDIENTE        NUMBER(10)            NOT NULL,
   CONRESUL             NUMBER(4,0)           NOT NULL,
   DESCRESUL            VARCHAR2(200)         NOT NULL,
   CONSTRAINT PK_RESULTADO_SURROGATE PRIMARY KEY (ID_RESULTADO),
   CONSTRAINT UK_RESULTADO_ORIGINAL UNIQUE (ID_EXPEDIENTE, CONRESUL),
   CONSTRAINT FK_RES_EXPEDIENTE FOREIGN KEY (ID_EXPEDIENTE) REFERENCES EXPEDIENTE (ID_EXPEDIENTE)
);

/*==============================================================*/
/* Table: SUCESO (Composite PK -> Surrogate)                    */
/*==============================================================*/
CREATE TABLE SUCESO (
   ID_SUCESO            NUMBER(10)            GENERATED BY DEFAULT AS IDENTITY,
   ID_EXPEDIENTE        NUMBER(10)            NOT NULL,
   CONSUCESO            NUMBER(4,0)           NOT NULL,
   DESCSUCESO           VARCHAR2(200)         NOT NULL,
   CONSTRAINT PK_SUCESO_SURROGATE PRIMARY KEY (ID_SUCESO),
   CONSTRAINT UK_SUCESO_ORIGINAL UNIQUE (ID_EXPEDIENTE, CONSUCESO),
   CONSTRAINT FK_SUC_EXPEDIENTE FOREIGN KEY (ID_EXPEDIENTE) REFERENCES EXPEDIENTE (ID_EXPEDIENTE)
);

COMMIT;
