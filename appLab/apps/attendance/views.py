from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterUseForm
from .models import Attendances
from apps.students.models import Students

class RegisterUseFormView(FormView):
    template_name = 'attendance/form.html'
    form_class = RegisterUseForm
    success_url = reverse_lazy("attendance_app:attendance")


    def form_valid(self, form):
        user_student = form.cleaned_data["user"]
        email = user_student + '@correo.uss.cl'
        student = Students.objects.filter(email=email).first()   
        
        if student:
            student_id = student.id          
            student = Students.objects.filter(id = student_id).first()

            attendance = Attendances.objects.create(student=student) 
            attendance.save()

            messages.success(
            self.request,
            "Registro de ingreso completado exitosamente"
            )
            return super().form_valid(form)

        else:            
            messages.error(
                self.request,
                "El usuario no coincide con ningún estudiante. Recuerda que tu usuario es la primera parte de tu correo"
            )
        return self.form_invalid(form)
    
class AttendanceListView(ListView):
    model = Attendances
    template_name = 'attendance/attendance.html'  # Ruta del archivo HTML
    context_object_name = 'attendances'  # Nombre del contexto para usar en la plantilla
    paginate_by = 10  # Opcional: Dividir en páginas con 10 elementos por página

    def get_queryset(self):
        # Obtener las asistencias, ordenadas por fecha más reciente
        return Attendances.objects.select_related('student').order_by('-date')