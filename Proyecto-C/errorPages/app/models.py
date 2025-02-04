from django.db import models

class ErrorLog(models.Model):
    codigo = models.CharField(max_length=10) #como un varchar
    mensaje = models.TextField() #como un longText
    fecha = models.DateTimeField(auto_now_add=True) #como Date(now())

    def __str__(self):
        return f"{codigo} - {mensaje}"
