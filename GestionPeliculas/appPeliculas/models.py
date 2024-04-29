from django.db import models

# Create your models here.
class Genero(models.Model):
    getNombre=models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.getNombre
    
class Pelicula(models.Model):
    pelCodigo= models.CharField(max_length=9)
    pelTitulo= models.CharField(max_length=50)
    pelProtagonista = models.CharField(max_length=50)
    pelDuracion = models.IntegerField()
    pelResumen = models.CharField(max_length=2000)
    pelFoto= models.ImageField(upload_to=f"fotos/", null=True, blank=True)
    pelGenero= models.ForeignKey(Genero, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.pelTitulo