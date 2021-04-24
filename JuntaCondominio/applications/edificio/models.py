from model_utils.models import TimeStampedModel
from django.db import models

# Create your models here.


class Edificio(TimeStampedModel):

    edificio = models.CharField("Torres", max_length=10) 
    class Meta:
        verbose_name = "Edificio"
        verbose_name_plural = "Edificio"

    def __str__(self):
        return self.edificio


class Propietario(TimeStampedModel):

    nombre = models.CharField("Nombre", max_length=20, blank=True) 
    apellido = models.CharField("Apellido", max_length=20, blank=True) 
    #telefono = models.PhoneNumberField("Telefono")
    email = models.EmailField("Correo Electronico", max_length=254, blank=True,)

    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"

    def __str__(self):
        return self.nombre + " " + self.apellido

    #def get_absolute_url(self):
     #   return reverse("Propietario_detail", kwargs={"pk": self.pk})


class Apartamento(TimeStampedModel):
    TORREA="1"
    TORREB="2"
    ALQUILER = "3"

    TORRE_CHOICES = (
        (TORREA, "Torre A") ,
        (TORREB, "Torre B"),
        (ALQUILER, "Alquiler")
    )

    apartamento = models.CharField("Apartamento", unique= True, max_length=4)
    piso = models.PositiveIntegerField("Piso")
    torre = models.CharField("Torres", choices=TORRE_CHOICES, max_length=1 )
    esquina = models.CharField("Esquina",max_length=10,blank=True)
    alicuota = models.DecimalField("Alicuota", max_digits=5, decimal_places=4)
    propietario =  models.ForeignKey(Propietario, verbose_name="Propietario",related_name="propietario_apart", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"

    def __str__(self):
        return self.apartamento

    # def get_absolute_url(self):
    #     return reverse("Apartamento_detail", kwargs={"pk": self.pk})
