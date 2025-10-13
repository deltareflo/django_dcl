from enum import unique
from django.db import models
import uuid
# Create your models here.
#from django.contrib.auth.models import User

class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True


class DatosPersonales(ClaseModelo):
    SOL='Soltero'
    CAS='Casado'
    VIU = 'Viudo'
    SEP = 'Separado'
    DIV = 'Divorciado'
    CON = 'Concubinado'
    TIPO_ESTADO = [
        (SOL,'Soltero'),
        (CAS,'Casado'),
        (VIU,'Viudo'),
        (SEP,'Separado'),
        (DIV,'Divorciado'),
        (CON,'Concubinado'),
    ]
    cedula = models.IntegerField(unique=True)

    nombre = models.CharField(
        max_length=120
    )
    apellido = models.CharField(
        max_length=120
    )

    fechaNacimiento = models.DateField()
    edad = models.IntegerField()
    nacionalidad = models.CharField(
        max_length=50
    )
    estadoCivil = models.CharField(
        max_length=20
    )
    email = models.EmailField(
        max_length=150
    )
    celular = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )


class Disc(ClaseModelo):
    ITEM_A = [
        ('cauteloso/a', 'cauteloso/a'),
        ('decidido/a', 'decidido/a'),
        ('receptivo/a', 'receptivo/a'),
        ('bondadoso/a', 'bondadoso/a')
    ]
    aplicante = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    campo_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    item_1 = models.CharField(max_length=50)
    item_2 = models.CharField(max_length=50)
    item_3 = models.CharField(max_length=50)
    item_4 = models.CharField(max_length=50)
    item_5 = models.CharField(max_length=50)
    item_6 = models.CharField(max_length=50)
    item_7 = models.CharField(max_length=50)
    item_8 = models.CharField(max_length=50)
    item_9 = models.CharField(max_length=50)
    item_10 = models.CharField(max_length=50)
    item_11 = models.CharField(max_length=50)
    item_12 = models.CharField(max_length=50)
    item_13 = models.CharField(max_length=50)
    item_14 = models.CharField(max_length=50)
    item_15 = models.CharField(max_length=50)
    item_16 = models.CharField(max_length=50)
    item_17 = models.CharField(max_length=50)
    item_18 = models.CharField(max_length=50)
    item_19 = models.CharField(max_length=50)
    item_20 = models.CharField(max_length=50)
    item_21 = models.CharField(max_length=50)
    item_22 = models.CharField(max_length=50)
    item_23 = models.CharField(max_length=50)
    item_24 = models.CharField(max_length=50)
    item_25 = models.CharField(max_length=50)
    item_26 = models.CharField(max_length=50)
    item_27 = models.CharField(max_length=50)
    item_28 = models.CharField(max_length=50)
    item_29 = models.CharField(max_length=50)
    item_30 = models.CharField(max_length=50)
    item_31 = models.CharField(max_length=50)
    item_32 = models.CharField(max_length=50)
    item_33 = models.CharField(max_length=50)
    item_34 = models.CharField(max_length=50)
    item_35 = models.CharField(max_length=50)
    item_36 = models.CharField(max_length=50)
    item_37 = models.CharField(max_length=50)
    item_38 = models.CharField(max_length=50)
    item_39 = models.CharField(max_length=50)
    item_40 = models.CharField(max_length=50)
    item_41 = models.CharField(max_length=50)
    item_42 = models.CharField(max_length=50)
    item_43 = models.CharField(max_length=50)
    item_44 = models.CharField(max_length=50)
    item_45 = models.CharField(max_length=50)
    item_46 = models.CharField(max_length=50)
    item_47 = models.CharField(max_length=50)
    item_48 = models.CharField(max_length=50)
    item_49 = models.CharField(max_length=50)
    item_50 = models.CharField(max_length=50)
    item_51 = models.CharField(max_length=50)
    item_52 = models.CharField(max_length=50)
    item_53 = models.CharField(max_length=50)
    item_54 = models.CharField(max_length=50)
    item_55 = models.CharField(max_length=50)
    item_56 = models.CharField(max_length=50)


class TrabajoEquipo(ClaseModelo):
    aplicante = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    campo_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    item1a = models.IntegerField()
    item1b = models.IntegerField()
    item1c = models.IntegerField()
    item1d = models.IntegerField()
    item2a = models.IntegerField()
    item2b = models.IntegerField()
    item2c = models.IntegerField()
    item2d = models.IntegerField()
    item3a = models.IntegerField()
    item3b = models.IntegerField()
    item3c = models.IntegerField()
    item3d = models.IntegerField()
    item4a = models.IntegerField()
    item4b = models.IntegerField()
    item4c = models.IntegerField()
    item4d = models.IntegerField()
    item5a = models.IntegerField()
    item5b = models.IntegerField()
    item5c = models.IntegerField()
    item5d = models.IntegerField()
    item6a = models.IntegerField()
    item6b = models.IntegerField()
    item6c = models.IntegerField()
    item6d = models.IntegerField()
    item7a = models.IntegerField()
    item7b = models.IntegerField()
    item7c = models.IntegerField()
    item7d = models.IntegerField()
    item8a = models.IntegerField()
    item8b = models.IntegerField()
    item8c = models.IntegerField()
    item8d = models.IntegerField()
    item9a = models.IntegerField()
    item9b = models.IntegerField()
    item9c = models.IntegerField()
    item9d = models.IntegerField()
    item10a = models.IntegerField()
    item10b = models.IntegerField()
    item10c = models.IntegerField()
    item10d = models.IntegerField()
    item11a = models.IntegerField()
    item11b = models.IntegerField()
    item11c = models.IntegerField()
    item11d = models.IntegerField()
    item12a = models.IntegerField()
    item12b = models.IntegerField()
    item12c = models.IntegerField()
    item12d = models.IntegerField()

class Liderazgo(ClaseModelo):
    aplicante = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    campo_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    item1a = models.IntegerField()
    item1b = models.IntegerField()
    item1c = models.IntegerField()
    item1d = models.IntegerField()
    item1e = models.IntegerField()
    item2a = models.IntegerField()
    item2b = models.IntegerField()
    item2c = models.IntegerField()
    item2d = models.IntegerField()
    item2e = models.IntegerField()
    item3a = models.IntegerField()
    item3b = models.IntegerField()
    item3c = models.IntegerField()
    item3d = models.IntegerField()
    item3e = models.IntegerField()
    item4a = models.IntegerField()
    item4b = models.IntegerField()
    item4c = models.IntegerField()
    item4d = models.IntegerField()
    item4e = models.IntegerField()
    item5a = models.IntegerField()
    item5b = models.IntegerField()
    item5c = models.IntegerField()
    item5d = models.IntegerField()
    item5e = models.IntegerField()
    item6a = models.IntegerField()
    item6b = models.IntegerField()
    item6c = models.IntegerField()
    item6d = models.IntegerField()
    item6e = models.IntegerField()
    item7a = models.IntegerField()
    item7b = models.IntegerField()
    item7c = models.IntegerField()
    item7d = models.IntegerField()
    item7e = models.IntegerField()
    item8a = models.IntegerField()
    item8b = models.IntegerField()
    item8c = models.IntegerField()
    item8d = models.IntegerField()
    item8e = models.IntegerField()
    item9a = models.IntegerField()
    item9b = models.IntegerField()
    item9c = models.IntegerField()
    item9d = models.IntegerField()
    item9e = models.IntegerField()
    item10a = models.IntegerField()
    item10b = models.IntegerField()
    item10c = models.IntegerField()
    item10d = models.IntegerField()
    item10e = models.IntegerField()
    item11a = models.IntegerField()
    item11b = models.IntegerField()
    item11c = models.IntegerField()
    item11d = models.IntegerField()
    item11e = models.IntegerField()
    item12a = models.IntegerField()
    item12b = models.IntegerField()
    item12c = models.IntegerField()
    item12d = models.IntegerField()
    item12e = models.IntegerField()
