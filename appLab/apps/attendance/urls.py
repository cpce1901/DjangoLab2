from django.urls import path
from .views import RegisterUseFormView, AttendanceListView

app_name = 'attendance_app'

urlpatterns = [
    path('', RegisterUseFormView.as_view(), name='attendance'),
    path('asistencia/', AttendanceListView.as_view(), name='attendance_all'),
]