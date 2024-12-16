from django.db import models
from apps.students.models import Students

# Create your models here.
class Attendances(models.Model):
    student = models.ForeignKey(Students, verbose_name='Estudiante', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f'{self.student.name} - {self.date}'