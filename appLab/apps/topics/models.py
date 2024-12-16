from django.db import models
from apps.students.models import Students, ClassName

class Topics(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'

    def __str__(self):
        return f'{self.name}'
    

class EnabledTopics(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, related_name='student_enabled_topics')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, null=True, related_name='class_name_enabled_topics')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True, related_name='topic_enabled_topics')
    score = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Habilitador'
        verbose_name_plural = 'Habilitadores'

    def __str__(self):
        return f'{self.topic.name} - {self.score}'