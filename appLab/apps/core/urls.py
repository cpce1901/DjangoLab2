from django.urls import path
from .views import PersonalLoginView, UploadStudents, UploadEnabledTopics, ExportStudentsExcelView, StudentCreateView
from django.contrib.auth.views import LogoutView

app_name = 'core_app'

urlpatterns = [
    path('login/', PersonalLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='attendance_app:attendance'),name='logout'),
    path('estudiantes/upload/', UploadStudents.as_view(), name='upload_students'),
    path('estudiantes/add/', StudentCreateView.as_view(), name='student_add'),
    path('estudiantes/export/', ExportStudentsExcelView.as_view(), name='download_students'),
    path('habilitadores/upload/', UploadEnabledTopics.as_view(), name='upload_enabled_topics')
]