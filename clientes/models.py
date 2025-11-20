from django.db import models


class TipoDocumento(models.Model):
    """Catálogo de tipos de documento de identidad"""
    id_tipo_doc = models.CharField(primary_key=True, max_length=2, db_column='ID_TIPO_DOC')
    desc_tipo_doc = models.CharField(max_length=30, db_column='DESC_TIPO_DOC')

    class Meta:
        managed = False
        db_table = 'TIPODOCUMENTO'
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

    def __str__(self):
        return f"{self.id_tipo_doc} - {self.desc_tipo_doc}"


class TipoProceso(models.Model):
    """Catálogo de tipos de procesos legales"""
    tipo_id = models.IntegerField(primary_key=True, db_column='TIPO_ID')
    nombre_tipo_proceso = models.CharField(max_length=50, db_column='NOMBRE_TIPO_PROCESO')

    class Meta:
        managed = False
        db_table = 'TIPOPROCESO'
        verbose_name = "Tipo de Proceso"
        verbose_name_plural = "Tipos de Proceso"

    def __str__(self):
        return self.nombre_tipo_proceso


class JudicialEntidad(models.Model):
    """Entidades judiciales (juzgados, tribunales, etc.)"""
    entidad_id = models.IntegerField(primary_key=True, db_column='ENTIDAD_ID')
    nombre = models.CharField(max_length=200, db_column='NOMBRE')
    tipo_entidad = models.CharField(max_length=80, blank=True, null=True, db_column='TIPO_ENTIDAD')
    direccion = models.TextField(blank=True, null=True, db_column='DIRECCION')
    ciudad = models.CharField(max_length=100, blank=True, null=True, db_column='CIUDAD')
    departamento = models.CharField(max_length=100, blank=True, null=True, db_column='DEPARTAMENTO')
    telefono = models.CharField(max_length=50, blank=True, null=True, db_column='TELEFONO')
    email = models.CharField(max_length=100, blank=True, null=True, db_column='EMAIL')

    class Meta:
        managed = False
        db_table = 'JUDICIALENTIDAD'
        verbose_name = "Entidad Judicial"
        verbose_name_plural = "Entidades Judiciales"

    def __str__(self):
        return self.nombre


class Abogado(models.Model):
    """Información de abogados"""
    abogado_id = models.IntegerField(primary_key=True, db_column='ABOGADO_ID')
    id_tipo_doc = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        db_column='ID_TIPO_DOC'
    )
    n_documento_abogado = models.CharField(max_length=15, unique=True, db_column='N_DOCUMENTO_ABOGADO')
    nombre_abogado = models.CharField(max_length=100, db_column='NOMBRE_ABOGADO')
    apellido_abogado = models.CharField(max_length=100, db_column='APELLIDO_ABOGADO')
    tarjeta_profesional = models.CharField(max_length=50, unique=True, db_column='TARJETA_PROFESIONAL')
    especializacion = models.CharField(max_length=100, blank=True, null=True, db_column='ESPECIALIZACION')
    email_abogado = models.CharField(max_length=100, blank=True, null=True, db_column='EMAIL_ABOGADO')
    telefono_abogado = models.CharField(max_length=50, blank=True, null=True, db_column='TELEFONO_ABOGADO')

    class Meta:
        managed = False
        db_table = 'ABOGADO'
        verbose_name = "Abogado"
        verbose_name_plural = "Abogados"

    def __str__(self):
        return f"{self.nombre_abogado} {self.apellido_abogado} - {self.tarjeta_profesional}"


class Cliente(models.Model):
    """Información de clientes"""
    cliente_id = models.IntegerField(primary_key=True, db_column='CLIENTE_ID')
    id_tipo_doc = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        db_column='ID_TIPO_DOC'
    )
    nombre_cliente = models.CharField(max_length=100, db_column='NOMBRE_CLIENTE')
    apellido_cliente = models.CharField(max_length=100, db_column='APELLIDO_CLIENTE')
    n_documento_cliente = models.CharField(max_length=15, unique=True, db_column='N_DOCUMENTO_CLIENTE')
    direccion_notificacion = models.TextField(blank=True, null=True, db_column='DIRECCION_NOTIFICACION')
    fecha_nacimiento = models.DateField(blank=True, null=True, db_column='FECHA_NACIMIENTO')
    observaciones = models.TextField(blank=True, null=True, db_column='OBSERVACIONES')

    class Meta:
        managed = False
        db_table = 'CLIENTE'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido_cliente}"


class Caso(models.Model):
    """Casos legales"""
    caso_id = models.IntegerField(primary_key=True, db_column='CASO_ID')
    cliente_id = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column='CLIENTE_ID'
    )
    tipo_id = models.ForeignKey(
        TipoProceso,
        on_delete=models.PROTECT,
        db_column='TIPO_ID'
    )
    expediente = models.CharField(max_length=60, unique=True, db_column='EXPEDIENTE')
    fecha_inicio = models.DateField(blank=True, null=True, db_column='FECHA_INICIO')
    fecha_fin = models.DateField(blank=True, null=True, db_column='FECHA_FIN')
    valor = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True, db_column='VALOR')
    estado = models.CharField(max_length=50, blank=True, null=True, db_column='ESTADO')

    class Meta:
        managed = False
        db_table = 'CASO'
        verbose_name = "Caso"
        verbose_name_plural = "Casos"

    def __str__(self):
        return f"{self.expediente} - {self.estado}"


class CasoAbogado(models.Model):
    """Relación entre casos y abogados asignados"""
    caso_abogado_id = models.IntegerField(primary_key=True, db_column='CASO_ABOGADO_ID')
    caso_id = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE,
        db_column='CASO_ID'
    )
    abogado_id = models.ForeignKey(
        Abogado,
        on_delete=models.PROTECT,
        db_column='ABOGADO_ID'
    )
    rol = models.CharField(max_length=50, blank=True, null=True, db_column='ROL')
    fecha_asignacion = models.DateField(blank=True, null=True, db_column='FECHA_ASIGNACION')
    fecha_remocion = models.DateField(blank=True, null=True, db_column='FECHA_REMOCION')

    class Meta:
        managed = False
        db_table = 'CASOABOGADO'
        verbose_name = "Caso-Abogado"
        verbose_name_plural = "Casos-Abogados"

    def __str__(self):
        return f"Caso {self.caso_id} - Abogado {self.abogado_id} ({self.rol})"


class CasoEtapa(models.Model):
    """Etapas o eventos de un caso"""
    caso_etapa_id = models.IntegerField(primary_key=True, db_column='CASO_ETAPA_ID')
    caso_id = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE,
        db_column='CASO_ID'
    )
    entidad_id = models.ForeignKey(
        JudicialEntidad,
        on_delete=models.PROTECT,
        db_column='ENTIDAD_ID'
    )
    fecha_evento = models.DateField(blank=True, null=True, db_column='FECHA_EVENTO')
    estado_evento = models.CharField(max_length=50, blank=True, null=True, db_column='ESTADO_EVENTO')
    descripcion = models.TextField(blank=True, null=True, db_column='DESCRIPCION')
    resultado = models.TextField(blank=True, null=True, db_column='RESULTADO')
    instancia = models.SmallIntegerField(blank=True, null=True, db_column='INSTANCIA')

    class Meta:
        managed = False
        db_table = 'CASOETAPA'
        verbose_name = "Etapa de Caso"
        verbose_name_plural = "Etapas de Casos"

    def __str__(self):
        return f"Etapa {self.caso_etapa_id} - Caso {self.caso_id}"


class CasoEtapaAbogado(models.Model):
    """Abogados que intervienen en cada etapa del caso"""
    id = models.IntegerField(primary_key=True, db_column='ID')
    abogado_id = models.ForeignKey(
        Abogado,
        on_delete=models.PROTECT,
        db_column='ABOGADO_ID'
    )
    caso_etapa_id = models.ForeignKey(
        CasoEtapa,
        on_delete=models.CASCADE,
        db_column='CASO_ETAPA_ID'
    )
    rol = models.CharField(max_length=50, blank=True, null=True, db_column='ROL')

    class Meta:
        managed = False
        db_table = 'CASOETAPAABOGADO'
        verbose_name = "Abogado en Etapa"
        verbose_name_plural = "Abogados en Etapas"

    def __str__(self):
        return f"Etapa {self.caso_etapa_id} - Abogado {self.abogado_id}"


class ClienteContacto(models.Model):
    """Información de contacto del cliente"""
    contacto_id = models.IntegerField(primary_key=True, db_column='CONTACTO_ID')
    cliente_id = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='CLIENTE_ID'
    )
    tipo_contacto = models.CharField(max_length=30, blank=True, null=True, db_column='TIPO_CONTACTO')
    desc_contacto = models.CharField(max_length=200, blank=True, null=True, db_column='DESC_CONTACTO')
    observacion = models.CharField(max_length=200, blank=True, null=True, db_column='OBSERVACION')

    class Meta:
        managed = False
        db_table = 'CLIENTECONTACTO'
        verbose_name = "Contacto de Cliente"
        verbose_name_plural = "Contactos de Clientes"

    def __str__(self):
        return f"{self.tipo_contacto}: {self.desc_contacto}"


class Documento(models.Model):
    """Documentos adjuntos a las etapas del caso"""
    documento_id = models.IntegerField(primary_key=True, db_column='DOCUMENTO_ID')
    caso_etapa_id = models.ForeignKey(
        CasoEtapa,
        on_delete=models.CASCADE,
        db_column='CASO_ETAPA_ID'
    )
    nombre_original = models.CharField(max_length=250, blank=True, null=True, db_column='NOMBRE_ORIGINAL')
    tipo_mime = models.CharField(max_length=100, blank=True, null=True, db_column='TIPO_MIME')
    ruta_archivo = models.CharField(max_length=500, blank=True, null=True, db_column='RUTA_ARCHIVO')
    usuario_subida = models.CharField(max_length=100, blank=True, null=True, db_column='USUARIO_SUBIDA')
    descripcion = models.TextField(blank=True, null=True, db_column='DESCRIPCION')

    class Meta:
        managed = False
        db_table = 'DOCUMENTO'
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.nombre_original or f"Documento {self.documento_id}"


class EtapaProcesal(models.Model):
    """Definición de etapas procesales por tipo de proceso"""
    etapa_id = models.IntegerField(primary_key=True, db_column='ETAPA_ID')
    tipo_id = models.ForeignKey(
        TipoProceso,
        on_delete=models.PROTECT,
        db_column='TIPO_ID'
    )
    nombre_etapa_procesal = models.CharField(max_length=80, db_column='NOMBRE_ETAPA_PROCESAL')
    orden = models.SmallIntegerField(blank=True, null=True, db_column='ORDEN')

    class Meta:
        managed = False
        db_table = 'ETAPAPROCESAL'
        verbose_name = "Etapa Procesal"
        verbose_name_plural = "Etapas Procesales"

    def __str__(self):
        return self.nombre_etapa_procesal


class Impugnacion(models.Model):
    """Recursos o impugnaciones presentadas en las etapas"""
    impugnacion_id = models.IntegerField(primary_key=True, db_column='IMPUGNACION_ID')
    caso_etapa_id = models.ForeignKey(
        CasoEtapa,
        on_delete=models.CASCADE,
        db_column='CASO_ETAPA_ID'
    )
    tipo_recurso = models.CharField(max_length=100, blank=True, null=True, db_column='TIPO_RECURSO')
    fecha_presentacion = models.DateField(blank=True, null=True, db_column='FECHA_PRESENTACION')
    instancia_destino = models.SmallIntegerField(blank=True, null=True, db_column='INSTANCIA_DESTINO')
    estado = models.CharField(max_length=50, blank=True, null=True, db_column='ESTADO')
    observaciones = models.TextField(blank=True, null=True, db_column='OBSERVACIONES')

    class Meta:
        managed = False
        db_table = 'IMPUGNACION'
        verbose_name = "Impugnación"
        verbose_name_plural = "Impugnaciones"

    def __str__(self):
        return f"{self.tipo_recurso} - {self.estado}"


class Pago(models.Model):
    """Pagos relacionados con los casos"""
    pago_id = models.IntegerField(primary_key=True, db_column='PAGO_ID')
    caso_id = models.ForeignKey(
        Caso,
        on_delete=models.CASCADE,
        db_column='CASO_ID'
    )
    fecha_pago = models.DateField(blank=True, null=True, db_column='FECHA_PAGO')
    monto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True, db_column='MONTO')
    forma_pago = models.CharField(max_length=50, blank=True, null=True, db_column='FORMA_PAGO')
    nota = models.TextField(blank=True, null=True, db_column='NOTA')

    class Meta:
        managed = False
        db_table = 'PAGO'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.pago_id} - ${self.monto}"
