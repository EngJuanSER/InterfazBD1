from django.db import models

# Modelo para TipoDocumento
class TipoDocumento(models.Model):
    idTipoDoc = models.CharField(max_length=2, primary_key=True, verbose_name="ID Tipo Documento")
    descTipoDoc = models.CharField(max_length=30, verbose_name="Descripción Tipo Documento")

    class Meta:
        db_table = 'TipoDocumento'
        managed = False  # Django no manejará la creación de esta tabla (ya existe en Oracle)
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

    def __str__(self):
        return f"{self.idTipoDoc} - {self.descTipoDoc}"


# Modelo para Cliente
class Cliente(models.Model):
    codCliente = models.CharField(max_length=5, primary_key=True, verbose_name="Código Cliente")
    nomCliente = models.CharField(max_length=30, verbose_name="Nombre Cliente")
    apellCliente = models.CharField(max_length=30, verbose_name="Apellido Cliente")
    idTipoDoc = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, db_column='idTipoDoc', verbose_name="Tipo Documento")
    nDocumento = models.CharField(max_length=15, verbose_name="Número Documento")

    class Meta:
        db_table = 'Cliente'
        managed = False  # Django no manejará la creación de esta tabla (ya existe en Oracle)
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.codCliente} - {self.nomCliente} {self.apellCliente}"
