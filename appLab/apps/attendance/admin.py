from django.contrib import admin
from .models import Attendances

@admin.register(Attendances)
class AttendancesAdmin(admin.ModelAdmin):
    list_display = ('id', 'student__name', 'date')
