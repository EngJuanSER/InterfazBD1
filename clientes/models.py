from django.db import models

class TipoDocumento(models.Model):
    id_tipo_doc = models.CharField(primary_key=True, max_length=2, db_column='IDTIPODOC')
    desc_tipo_doc = models.CharField(max_length=30, db_column='DESCTIPODOC')

    class Meta:
        managed = False
        db_table = 'TIPODOCUMENTO'

    def __str__(self):
        return self.desc_tipo_doc

class TipoContacto(models.Model):
    id_tipo_conta = models.CharField(primary_key=True, max_length=3, db_column='IDTIPOCONTA')
    desc_tipo_conta = models.CharField(max_length=30, db_column='DESCTIPOCONTA')

    class Meta:
        managed = False
        db_table = 'TIPOCONTACT'

    def __str__(self):
        return self.desc_tipo_conta

class TipoLugar(models.Model):
    id_tipo_lugar = models.IntegerField(primary_key=True, db_column='IDTIPOLUGAR')
    desc_tipo_lugar = models.CharField(max_length=50, db_column='DESCTIPOLUGAR')

    class Meta:
        managed = False
        db_table = 'TIPOLUGAR'

    def __str__(self):
        return self.desc_tipo_lugar

class FormaPago(models.Model):
    id_forma_pago = models.CharField(primary_key=True, max_length=3, db_column='IDFORMAPAGO')
    desc_forma_pago = models.CharField(max_length=40, db_column='DESCFORMAPAGO')

    class Meta:
        managed = False
        db_table = 'FORMAPAGO'

    def __str__(self):
        return self.desc_forma_pago

class Franquicia(models.Model):
    cod_franquicia = models.CharField(primary_key=True, max_length=3, db_column='CODFRANQUICIA')
    nom_franquicia = models.CharField(max_length=40, db_column='NOMFRANQUICIA')

    class Meta:
        managed = False
        db_table = 'FRANQUICIA'

    def __str__(self):
        return self.nom_franquicia

class Especializacion(models.Model):
    cod_especializacion = models.CharField(primary_key=True, max_length=3, db_column='CODESPECIALIZACION')
    nom_especializacion = models.CharField(max_length=30, db_column='NOMESPECIALIZACION')

    class Meta:
        managed = False
        db_table = 'ESPECIALIZACION'

    def __str__(self):
        return self.nom_especializacion

class EtapaProcesal(models.Model):
    cod_etapa = models.CharField(primary_key=True, max_length=3, db_column='CODETAPA')
    nom_etapa = models.CharField(max_length=30, db_column='NOMETAPA')
    orden = models.IntegerField(default=0, db_column='ORDEN')

    class Meta:
        managed = False
        db_table = 'ETAPAPROCESAL'

    def __str__(self):
        return self.nom_etapa

class Impugnacion(models.Model):
    id_impugna = models.CharField(primary_key=True, max_length=2, db_column='IDIMPUGNA')
    nom_impugna = models.CharField(max_length=30, db_column='NOMIMPUGNA')

    class Meta:
        managed = False
        db_table = 'IMPUGNACION'

    def __str__(self):
        return self.nom_impugna

class Instancia(models.Model):
    n_instancia = models.IntegerField(primary_key=True, db_column='NINSTANCIA')

    class Meta:
        managed = False
        db_table = 'INSTANCIA'

    def __str__(self):
        return str(self.n_instancia)

class Lugar(models.Model):
    cod_lugar = models.CharField(primary_key=True, max_length=5, db_column='CODLUGAR')
    id_tipo_lugar = models.ForeignKey(TipoLugar, on_delete=models.PROTECT, db_column='IDTIPOLUGAR')
    lug_cod_lugar = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, db_column='LUG_CODLUGAR')
    nom_lugar = models.CharField(max_length=30, db_column='NOMLUGAR')
    dire_lugar = models.CharField(max_length=40, db_column='DIRELUGAR')
    tel_lugar = models.CharField(max_length=15, db_column='TELLUGAR')
    email_lugar = models.CharField(max_length=50, null=True, blank=True, db_column='EMAILLUGAR')

    class Meta:
        managed = False
        db_table = 'LUGAR'

    def __str__(self):
        return self.nom_lugar

class Cliente(models.Model):
    cod_cliente = models.CharField(primary_key=True, max_length=5, db_column='CODCLIENTE')
    id_tipo_doc = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, db_column='IDTIPODOC')
    nom_cliente = models.CharField(max_length=30, db_column='NOMCLIENTE')
    apell_cliente = models.CharField(max_length=30, db_column='APELLCLIENTE')
    n_documento = models.CharField(max_length=15, db_column='NDOCUMENTO')

    class Meta:
        managed = False
        db_table = 'CLIENTE'

    def __str__(self):
        return f"{self.nom_cliente} {self.apell_cliente}"

class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True, db_column='ID_CONTACTO')
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='CODCLIENTE')
    conse_contacto = models.IntegerField(db_column='CONSECONTACTO')
    id_tipo_conta = models.ForeignKey(TipoContacto, on_delete=models.PROTECT, db_column='IDTIPOCONTA')
    valor_contacto = models.CharField(max_length=50, db_column='VALORCONTACTO')
    notificacion = models.IntegerField(default=0, db_column='NOTIFICACION')

    class Meta:
        managed = False
        db_table = 'CONTACTO'
        unique_together = (('cod_cliente', 'conse_contacto'),)

class Abogado(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10, db_column='CEDULA')
    nombre = models.CharField(max_length=30, db_column='NOMBRE')
    apellido = models.CharField(max_length=30, db_column='APELLIDO')
    n_tarjeta_profesional = models.CharField(max_length=5, db_column='NTARJETAPROFESIONAL')

    class Meta:
        managed = False
        db_table = 'ABOGADO'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class AbogadoEspecial(models.Model):
    id_abogado_esp = models.AutoField(primary_key=True, db_column='ID_ABOGADO_ESP')
    cod_especializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    cedula = models.ForeignKey(Abogado, on_delete=models.CASCADE, db_column='CEDULA')

    class Meta:
        managed = False
        db_table = 'FK_ABOGADO_ESPECIAL'
        unique_together = (('cod_especializacion', 'cedula'),)

class Caso(models.Model):
    no_caso = models.IntegerField(primary_key=True, db_column='NOCASO')
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='CODCLIENTE')
    cod_especializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    fecha_inicio = models.DateField(db_column='FECHAINICIO')
    fecha_fin = models.DateField(null=True, blank=True, db_column='FECHAFIN')
    valor = models.CharField(max_length=10, db_column='VALOR')

    class Meta:
        managed = False
        db_table = 'CASO'

    def __str__(self):
        return f"Caso {self.no_caso} - {self.cod_cliente}"

class Pago(models.Model):
    consec_pago = models.IntegerField(primary_key=True, db_column='CONSECPAGO')
    no_caso = models.ForeignKey(Caso, on_delete=models.CASCADE, db_column='NOCASO')
    cod_franquicia = models.ForeignKey(Franquicia, on_delete=models.PROTECT, null=True, blank=True, db_column='CODFRANQUICIA')
    id_forma_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT, null=True, blank=True, db_column='IDFORMAPAGO')
    fecha_pago = models.DateField(null=True, blank=True, db_column='FECHAPAGO')
    valor_pago = models.IntegerField(db_column='VALORPAGO')
    n_tarjeta = models.IntegerField(null=True, blank=True, db_column='NTARJETA')

    class Meta:
        managed = False
        db_table = 'PAGO'

class EspeciaEtapa(models.Model):
    id_especia_etapa = models.AutoField(primary_key=True, db_column='ID_ESPECIA_ETAPA')
    cod_especializacion = models.ForeignKey(Especializacion, on_delete=models.PROTECT, db_column='CODESPECIALIZACION')
    n_instancia = models.ForeignKey(Instancia, on_delete=models.PROTECT, related_name='etapas_instancia', db_column='NINSTANCIA')
    ins_n_instancia = models.ForeignKey(Instancia, on_delete=models.PROTECT, null=True, blank=True, related_name='etapas_siguiente', db_column='INS_NINSTANCIA')
    cod_etapa = models.ForeignKey(EtapaProcesal, on_delete=models.PROTECT, db_column='CODETAPA')
    id_impugna = models.ForeignKey(Impugnacion, on_delete=models.PROTECT, null=True, blank=True, db_column='IDIMPUGNA')

    class Meta:
        managed = False
        db_table = 'ESPECIA_ETAPA'
        unique_together = (('cod_especializacion', 'n_instancia', 'cod_etapa'),)

class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True, db_column='ID_EXPEDIENTE')
    no_caso = models.ForeignKey(Caso, on_delete=models.CASCADE, db_column='NOCASO')
    cod_especializacion = models.CharField(max_length=3, db_column='CODESPECIALIZACION') # Part of logical FK to EspeciaEtapa
    n_instancia = models.IntegerField(db_column='NINSTANCIA') # Part of logical FK to EspeciaEtapa
    consec_expe = models.IntegerField(db_column='CONSECEXPE')
    cedula = models.ForeignKey(Abogado, on_delete=models.PROTECT, null=True, blank=True, db_column='CEDULA')
    cod_lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT, db_column='CODLUGAR')
    fecha_etapa = models.DateField(db_column='FECHAETAPA')
    paso_etapa = models.IntegerField(null=True, blank=True, db_column='PASOETAPA')

    class Meta:
        managed = False
        db_table = 'EXPEDIENTE'
        unique_together = (('no_caso', 'consec_expe'),)

class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True, db_column='ID_DOCUMENTO')
    id_expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, db_column='ID_EXPEDIENTE')
    con_doc = models.IntegerField(db_column='CONDOC')
    ubica_doc = models.CharField(max_length=50, db_column='UBICADOC')

    class Meta:
        managed = False
        db_table = 'DOCUMENTO'
        unique_together = (('id_expediente', 'con_doc'),)

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True, db_column='ID_RESULTADO')
    id_expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, db_column='ID_EXPEDIENTE')
    con_resul = models.IntegerField(db_column='CONRESUL')
    desc_resul = models.CharField(max_length=200, db_column='DESCRESUL')

    class Meta:
        managed = False
        db_table = 'RESULTADO'
        unique_together = (('id_expediente', 'con_resul'),)

class Suceso(models.Model):
    id_suceso = models.AutoField(primary_key=True, db_column='ID_SUCESO')
    id_expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, db_column='ID_EXPEDIENTE')
    con_suceso = models.IntegerField(db_column='CONSUCESO')
    desc_suceso = models.CharField(max_length=200, db_column='DESCSUCESO')

    class Meta:
        managed = False
        db_table = 'SUCESO'
        unique_together = (('id_expediente', 'con_suceso'),)
