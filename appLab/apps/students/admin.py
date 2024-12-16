from django.contrib import admin
from django.utils.html import format_html
from .models import Students, ClassName, PrincipalClass, Stages

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('display_full_name', 'display_class_names', 'display_enabled_topics')
    search_fields = ('name', 'last_name', 'email')
    list_filter = ('class_name__principal_class__code', 'class_name__name')
    filter_horizontal = ('class_name', )

    @admin.display(description='Nombre')
    def display_full_name(self, obj):
        return f'{obj.name} {obj.last_name}'
    
    @admin.display(description='Asignaturas')
    def display_class_names(self, obj):
        class_names = obj.class_name.all()
        
        if class_names:
            output = '<ul>'
            for class_name in class_names:
                output += f'<li>{class_name.name}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
        
    @admin.display(description='Habilitadores')
    def display_enabled_topics(self, obj):
        enebaled_topics = obj.student_enabled_topics.all()
        
        if enebaled_topics:
            output = '<ul>'
            for enable_topic in enebaled_topics:
                output += f'<li>{enable_topic.topic} | {enable_topic.score}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''


@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    pass

@admin.register(PrincipalClass)
class PrincipalClassAdmin(admin.ModelAdmin):
    pass

@admin.register(Stages)
class StagesAdmin(admin.ModelAdmin):
    pass
