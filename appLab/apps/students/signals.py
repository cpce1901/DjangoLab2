from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.topics.models import Topics, EnabledTopics
from .models import Students, ClassName

@receiver(m2m_changed, sender=Students.class_name.through)
def create_enabled_topics_for_student(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":  # Solo se ejecuta después de agregar clases
        topics = Topics.objects.all()
        classes = instance.class_name.all()  # Obtiene las clases del estudiante
        for class_obj in classes:  # Por cada clase del estudiante
            for topic in topics:  # Por cada tópico existente
                # Crea un EnabledTopic por cada combinación de clase y tópico
                EnabledTopics.objects.get_or_create(
                    student=instance,
                    class_name=class_obj,
                    topic=topic,
                    defaults={"score": 0},
                )
    # Cuando se eliminan clases
    elif action == "pre_remove":
        # pk_set contiene las claves primarias de las clases que se están eliminando
        for class_id in pk_set:
            class_obj = ClassName.objects.get(id=class_id)  # Obtén la clase usando su id
            topics = Topics.objects.all()
            for topic in topics:  # Por cada tópico existente
                # Elimina el EnabledTopic para esta clase y estudiante
                EnabledTopics.objects.filter(
                    student=instance,
                    class_name=class_obj,
                    topic=topic
                ).delete()