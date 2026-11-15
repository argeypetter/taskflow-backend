from django.db import models

# Create your models here.
class Task(models.Model):
    PRIORIDAD = [('1', 'Alta'),
                 ('2', 'Media'),
                 ('3', 'Baja')]

    ESTADO = [('1', 'Pendiente'),
              ('2', 'Completado')]

    # Django crea automáticamente: id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    prioridad = models.CharField(max_length=5,choices=PRIORIDAD, default='1')
    estado = models.CharField(max_length=5,choices=ESTADO, default='1')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
