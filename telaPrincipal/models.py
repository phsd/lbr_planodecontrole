from django.db import models

# Create your models here.
class headerPlanoControle (models.Model):
    mo = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )
    seriei = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    serieii = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    serieiii = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    pdfcriado = models.BooleanField(
        default=False
    )
    datapdfcriado = models.DateTimeField(
        null=True,
        blank=True
    )
    def __str__(self):
        return self.mo

class itemInspecaoPC (models.Model):
    numero = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    cor = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    requisito = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    ilustracao = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    metodoinstrucao = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    unidade = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    operacao = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )

class inspecaoPlanoControle (models.Model):
    id_HPC = models.ForeignKey('headerPlanoControle', on_delete=models.PROTECT)
    id_itemInspecaoPC = models.ForeignKey('itemInspecaoPC', on_delete=models.PROTECT)
    serie = models.IntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    valor = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    username_usuario = models.IntegerField(null=False, blank=False)
    dataRegistro = models.DateTimeField(auto_now_add=True)
