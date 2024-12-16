from django.db import models

class Stages(models.Model):
    year = models.SmallIntegerField()
    semester= models.SmallIntegerField()

    class Meta:
        verbose_name = 'Etapa academica'
        verbose_name_plural = 'Etapas academicas'

    def __str__(self):
        return f'{self.year} - {self.semester}'
    

class PrincipalClass(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=8)

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

    def __str__(self):
        return f'{self.name} - {self.code}'


class ClassName(models.Model):
    name = models.CharField(max_length=64)
    code = models.SmallIntegerField()
    principal_class = models.ForeignKey(PrincipalClass, on_delete=models.CASCADE, null=True, blank=True) 
    stage = models.ForeignKey(Stages, on_delete=models.CASCADE, null=True) 

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

    def __str__(self):
        return f'{self.principal_class.code} - {self.name}'



class Students(models.Model):
    name = models.CharField('Nombre', max_length=64)
    last_name = models.CharField('Apellido', max_length=64)
    email = models.CharField('Correo', max_length=128, unique=True)
    class_name = models.ManyToManyField(ClassName, verbose_name='Asignaturas', blank=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def save(self, *args, **kwargs):
        self.email = f"{self.email}{'@correo.uss.cl' if '@correo.uss.cl' not in self.email else ''}"
        super(Students, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.last_name} | {self.email}'
    

