from django.db import models

# Create your models here.
class Modelo(models.Model):
    modelo_v=models.FileField(null=True, unique=True)
    def __str__(self):
        return self.modelo_v