from django.contrib.auth.models import User
from django.db import models

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    horas_realizadas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Asistencia(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    horas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.usuario.username} - {self.asignatura.nombre}"
