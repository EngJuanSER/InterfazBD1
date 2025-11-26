"""
Modelos Django para el Sistema de Gestion Legal
Estos modelos mapean las tablas de Oracle definidas en 01_modelo.sql
NOTA: managed = False porque las tablas ya existen en Oracle

IMPORTANTE: Estos modelos NO SE UTILIZAN para consultas ni manipulacion de datos en la aplicacion.
Toda la interaccion con la base de datos se realiza mediante SQL RAW (cursor.execute)
en las vistas (views.py) para cumplir con el requerimiento de no usar ORM.
Estos modelos existen solo como referencia de la estructura o para herramientas de introspeccion.
"""
from django.db import models


# =============================================================================
# TABLAS MAESTRAS (Catalogos)
# =============================================================================

class TipoDocumento(models.Model):
    """Catalogo de tipos de documento de identidad"""
    idtipodoc = models.CharField(primary_key=True, max_length=2, db_column='IDTIPODOC')
    desctipodoc = models.CharField(max_length=30, db_column='DESCTIPODOC')

    class Meta:
        managed = False
        db_table = 'TIPODOCUMENTO'

    def __str__(self):
        return f"{self.idtipodoc} - {self.desctipodoc}"


class TipoContacto(models.Model):
    """Catalogo de tipos de contacto"""
    idtipoconta = models.CharField(primary_key=True, max_length=3, db_column='IDTIPOCONTA')
    desctipoconta = models.CharField(max_length=30, db_column='DESCTIPOCONTA')

    class Meta:
        managed = False
        db_table = 'TIPOCONTACT'

    def __str__(self):
        return f"{self.idtipoconta} - {self.desctipoconta}"


class TipoLugar(models.Model):
    """Catalogo de tipos de lugar (Juzgado, Tribunal, Corte, etc.)"""
    idtipolugar = models.IntegerField(primary_key=True, db_column='IDTIPOLUGAR')
    desctipolugar = models.CharField(max_length=50, db_column='DESCTIPOLUGAR')

    class Meta:
        managed = False
        db_table = 'TIPOLUGAR'

    def __str__(self):
        return self.desctipolugar


class FormaPago(models.Model):
    """Catalogo de formas de pago"""
    idformapago = models.CharField(primary_key=True, max_length=3, db_column='IDFORMAPAGO')
    descformapago = models.CharField(max_length=40, db_column='DESCFORMAPAGO')

    class Meta:
        managed = False
        db_table = 'FORMAPAGO'

    def __str__(self):
        return self.descformapago


class Franquicia(models.Model):
    """Catalogo de franquicias de tarjetas"""
    codfranquicia = models.CharField(primary_key=True, max_length=3, db_column='CODFRANQUICIA')
    nomfranquicia = models.CharField(max_length=40, db_column='NOMFRANQUICIA')

    class Meta:
        managed = False
        db_table = 'FRANQUICIA'

    def __str__(self):
        return self.nomfranquicia


class Especializacion(models.Model):
    """Catalogo de especializaciones legales"""
    codespecializacion = models.CharField(primary_key=True, max_length=3, db_column='CODESPECIALIZACION')
    nomespecializacion = models.CharField(max_length=30, db_column='NOMESPECIALIZACION')

    class Meta:
        managed = False
        db_table = 'ESPECIALIZACION'

    def __str__(self):
        return self.nomespecializacion


class EtapaProcesal(models.Model):
    """Catalogo de etapas procesales"""
    codetapa = models.CharField(primary_key=True, max_length=3, db_column='CODETAPA')
    nometapa = models.CharField(max_length=30, db_column='NOMETAPA')
    orden = models.IntegerField(default=0, db_column='ORDEN')

    class Meta:
        managed = False
        db_table = 'ETAPAPROCESAL'

    def __str__(self):
        return self.nometapa


class Impugnacion(models.Model):
    """Catalogo de tipos de impugnacion"""
    idimpugna = models.CharField(primary_key=True, max_length=2, db_column='IDIMPUGNA')
    nomimpugna = models.CharField(max_length=30, db_column='NOMIMPUGNA')

    class Meta:
        managed = False
        db_table = 'IMPUGNACION'

    def __str__(self):
        return self.nomimpugna


class Instancia(models.Model):
    """Catalogo de instancias judiciales"""
    ninstancia = models.IntegerField(primary_key=True, db_column='NINSTANCIA')

    class Meta:
        managed = False
        db_table = 'INSTANCIA'

    def __str__(self):
        return f"Instancia {self.ninstancia}"


# =============================================================================
# TABLAS DE CONFIGURACION
# =============================================================================

class Lugar(models.Model):
    """Lugares judiciales con jerarquia"""
    codlugar = models.CharField(primary_key=True, max_length=5, db_column='CODLUGAR')
    idtipolugar = models.ForeignKey(TipoLugar, on_delete=models.PROTECT, db_column='IDTIPOLUGAR')
    lug_codlugar = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, db_column='LUG_CODLUGAR')
    nomlugar = models.CharField(max_length=30, db_column='NOMLUGAR')
    direlugar = models.CharField(max_length=40, db_column='DIRELUGAR')
    tellugar = models.CharField(max_length=15, db_column='TELLUGAR')
    emaillugar = models.CharField(max_length=50, null=True, blank=True, db_column='EMAILLUGAR')

    class Meta:
        managed = False
        db_table = 'LUGAR'

    def __str__(self):
        return self.nomlugar


class EspeciaEtapa(models.Model):
    """Configuracion de etapas por especializacion"""
    id_especia_etapa = models.AutoField(primary_key=True, db_column='ID_ESPECIA_ETAPA')
    codespecializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    ninstancia = models.ForeignKey(Instancia, on_delete=models.PROTECT, db_column='NINSTANCIA', related_name='especia_etapa_instancia')
    ins_ninstancia = models.ForeignKey(Instancia, on_delete=models.PROTECT, null=True, blank=True, db_column='INS_NINSTANCIA', related_name='especia_etapa_siguiente')
    codetapa = models.ForeignKey(EtapaProcesal, on_delete=models.PROTECT, db_column='CODETAPA')
    idimpugna = models.ForeignKey(Impugnacion, on_delete=models.PROTECT, null=True, blank=True, db_column='IDIMPUGNA')

    class Meta:
        managed = False
        db_table = 'ESPECIA_ETAPA'

    def __str__(self):
        return f"{self.codespecializacion} - {self.codetapa}"


# =============================================================================
# TABLAS PRINCIPALES
# =============================================================================

class Cliente(models.Model):
    """Informacion de clientes"""
    codcliente = models.CharField(primary_key=True, max_length=5, db_column='CODCLIENTE')
    idtipodoc = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, db_column='IDTIPODOC')
    nomcliente = models.CharField(max_length=30, db_column='NOMCLIENTE')
    apellcliente = models.CharField(max_length=30, db_column='APELLCLIENTE')
    ndocumento = models.CharField(max_length=15, db_column='NDOCUMENTO')

    class Meta:
        managed = False
        db_table = 'CLIENTE'

    def __str__(self):
        return f"{self.nomcliente} {self.apellcliente}"


class Contacto(models.Model):
    """Contactos de clientes"""
    id_contacto = models.AutoField(primary_key=True, db_column='ID_CONTACTO')
    codcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='CODCLIENTE')
    consecontacto = models.IntegerField(db_column='CONSECONTACTO')
    idtipoconta = models.ForeignKey(TipoContacto, on_delete=models.PROTECT, db_column='IDTIPOCONTA')
    valorcontacto = models.CharField(max_length=50, db_column='VALORCONTACTO')
    notificacion = models.IntegerField(default=0, db_column='NOTIFICACION')

    class Meta:
        managed = False
        db_table = 'CONTACTO'

    def __str__(self):
        return f"{self.codcliente} - {self.valorcontacto}"


class Abogado(models.Model):
    """Informacion de abogados"""
    cedula = models.CharField(primary_key=True, max_length=10, db_column='CEDULA')
    nombre = models.CharField(max_length=30, db_column='NOMBRE')
    apellido = models.CharField(max_length=30, db_column='APELLIDO')
    ntarjetaprofesional = models.CharField(max_length=5, db_column='NTARJETAPROFESIONAL')

    class Meta:
        managed = False
        db_table = 'ABOGADO'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class AbogadoEspecializacion(models.Model):
    """Especializaciones de abogados"""
    id_abogado_esp = models.AutoField(primary_key=True, db_column='ID_ABOGADO_ESP')
    codespecializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    cedula = models.ForeignKey(Abogado, on_delete=models.CASCADE, db_column='CEDULA')

    class Meta:
        managed = False
        db_table = 'FK_ABOGADO_ESPECIAL'

    def __str__(self):
        return f"{self.cedula} - {self.codespecializacion}"


class Caso(models.Model):
    """Casos legales"""
    nocaso = models.IntegerField(primary_key=True, db_column='NOCASO')
    codcliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='CODCLIENTE')
    codespecializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    fechainicio = models.DateField(db_column='FECHAINICIO')
    fechafin = models.DateField(null=True, blank=True, db_column='FECHAFIN')
    valor = models.CharField(max_length=10, db_column='VALOR')

    class Meta:
        managed = False
        db_table = 'CASO'

    def __str__(self):
        return f"Caso {self.nocaso} - {self.codcliente}"


class Pago(models.Model):
    """Pagos de casos"""
    consecpago = models.IntegerField(primary_key=True, db_column='CONSECPAGO')
    nocaso = models.ForeignKey(Caso, on_delete=models.CASCADE, db_column='NOCASO')
    codfranquicia = models.ForeignKey(Franquicia, on_delete=models.PROTECT, null=True, blank=True, db_column='CODFRANQUICIA')
    idformapago = models.ForeignKey(FormaPago, on_delete=models.PROTECT, null=True, blank=True, db_column='IDFORMAPAGO')
    fechapago = models.DateField(null=True, blank=True, db_column='FECHAPAGO')
    valorpago = models.IntegerField(db_column='VALORPAGO')
    ntarjeta = models.BigIntegerField(null=True, blank=True, db_column='NTARJETA')

    class Meta:
        managed = False
        db_table = 'PAGO'

    def __str__(self):
        return f"Pago {self.consecpago} - Caso {self.nocaso}"


class Expediente(models.Model):
    """Expedientes de casos"""
    # Composite primary key fields (no auto PK)
    nocaso = models.IntegerField(db_column='NOCASO')
    codespecializacion = models.CharField(max_length=3, db_column='CODESPECIALIZACION')
    ninstancia = models.IntegerField(db_column='NINSTANCIA')
    consecexpe = models.IntegerField(db_column='CONSECEXPE')
    cedula = models.CharField(max_length=10, null=True, blank=True, db_column='CEDULA')
    codlugar = models.CharField(max_length=5, db_column='CODLUGAR')
    fechaetapa = models.DateField(db_column='FECHAETAPA')
    # pasoetapa removed from schema

    class Meta:
        managed = False
        db_table = 'EXPEDIENTE'
        unique_together = (('codespecializacion', 'nocaso', 'ninstancia', 'consecexpe'),)

    def __str__(self):
        return f"Expediente {self.consecexpe} - Caso {self.nocaso}"


class Documento(models.Model):
    """Documentos de expedientes"""
    # Composite PK fields
    codespecializacion = models.CharField(max_length=3, db_column='CODESPECIALIZACION')
    nocaso = models.IntegerField(db_column='NOCASO')
    ninstancia = models.IntegerField(db_column='NINSTANCIA')
    consecexpe = models.IntegerField(db_column='CONSECEXPE')
    condoc = models.IntegerField(db_column='CONDOC')
    ubicadoc = models.CharField(max_length=50, db_column='UBICADOC')

    class Meta:
        managed = False
        db_table = 'DOCUMENTO'
        unique_together = (('codespecializacion', 'nocaso', 'ninstancia', 'consecexpe', 'condoc'),)

    def __str__(self):
        return f"Doc {self.condoc} - Exp {self.id_expediente}"


class Resultado(models.Model):
    """Resultados de expedientes"""
    # Composite PK fields
    codespecializacion = models.CharField(max_length=3, db_column='CODESPECIALIZACION')
    nocaso = models.IntegerField(db_column='NOCASO')
    ninstancia = models.IntegerField(db_column='NINSTANCIA')
    consecexpe = models.IntegerField(db_column='CONSECEXPE')
    conresul = models.IntegerField(db_column='CONRESUL')
    descresul = models.CharField(max_length=200, db_column='DESCRESUL')

    class Meta:
        managed = False
        db_table = 'RESULTADO'
        unique_together = (('codespecializacion', 'nocaso', 'ninstancia', 'consecexpe', 'conresul'),)

    def __str__(self):
        return f"Resultado {self.conresul} - Exp {self.id_expediente}"


class Suceso(models.Model):
    """Sucesos de expedientes"""
    # Composite PK fields
    codespecializacion = models.CharField(max_length=3, db_column='CODESPECIALIZACION')
    nocaso = models.IntegerField(db_column='NOCASO')
    ninstancia = models.IntegerField(db_column='NINSTANCIA')
    consecexpe = models.IntegerField(db_column='CONSECEXPE')
    consuceso = models.IntegerField(db_column='CONSUCESO')
    descsuceso = models.CharField(max_length=200, db_column='DESCSUCESO')

    class Meta:
        managed = False
        db_table = 'SUCESO'
        unique_together = (('codespecializacion', 'nocaso', 'ninstancia', 'consecexpe', 'consuceso'),)

    def __str__(self):
        return f"Suceso {self.consuceso} - Exp {self.id_expediente}"
