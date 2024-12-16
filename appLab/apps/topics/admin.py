from django.contrib import admin
from .models import Topics, EnabledTopics

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    pass


@admin.register(EnabledTopics)
class EnabledTopicsAdmin(admin.ModelAdmin):
    pass