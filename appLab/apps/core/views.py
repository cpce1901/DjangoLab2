import pandas as pd
from django.views.generic import FormView, View, ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from .forms import LoginForm, UploadStudentsForm, UploadEnabledTopicsForm, StudentForm
from apps.students.models import Students, ClassName
from apps.topics.models import Topics, EnabledTopics

#OK
class PersonalLoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("attendance_app:attendance")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)
            return super(PersonalLoginView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "La credenciales ingresadas no son validas. Inténtalo de nuevo.",
            )
            return self.form_invalid(form)


# OK
class StudentListCreateView(ListView, FormView):
    model = Students
    template_name = 'core/students/students.html'
    form_class = StudentForm
    success_url = reverse_lazy('core_app:students')  # Redirige a la misma vista después de crear un estudiante

    # Define el queryset explícitamente
    def get_queryset(self):
        return Students.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = self.get_queryset()  # Mostrar todos los estudiantes
        context['form'] = self.get_form()  # Agregar el formulario de creación de estudiante al contexto
        return context

    def form_valid(self, form):
        # Guardar el nuevo estudiante
        form.save()
        messages.success(self.request, "Estudiante creado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Si el formulario no es válido, no hacer nada
        messages.error(self.request, "Hubo un error al crear el estudiante.")
        return super().form_invalid(form)


# OK
class StudentUpdateView(UpdateView):
    model = Students
    form_class = StudentForm
    template_name = 'core/students/update.html'  
    success_url = reverse_lazy('core_app:students')

    def form_valid(self, form):
        messages.success(self.request, "Estudiante actualizado con éxito.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el estudiante.")
        return super().form_invalid(form)


# OK
class StudentDeleteView(View):
    def post(self, request, pk):
        student = get_object_or_404(Students, pk=pk)
        student.delete()
        messages.success(self.request, "Estudiante eliminado con éxito.")
        return redirect('core_app:students')


# OK
class UploadStudents(FormView):
    template_name = 'core/students/upload.html'
    form_class = UploadStudentsForm
    success_url = reverse_lazy("core_app:upload_students")

    def form_valid(self, form):
        class_id = form.cleaned_data["class_id"]
        uploaded_file = self.request.FILES['file']

        # Leer el archivo Excel
        try:
            df = pd.read_excel(uploaded_file, header=1, usecols=['Nombre', 'Apellidos', 'Dirección de correo electrónico'])
        except Exception as e:
            messages.error(self.request, f"Error al leer el archivo: {e}")
            return self.form_invalid(form)
        
        # Obtener la clase seleccionada
        try:
            selected_class = ClassName.objects.get(pk=class_id.id)
        except ClassName.DoesNotExist:
            messages.error(self.request, "La clase seleccionada no existe.")
            return self.form_invalid(form)
        
        # Crear una lista para bulk_create
        students_to_create = []
        existing_emails = set(
            Students.objects.filter(email__in=df['Dirección de correo electrónico']).values_list('email', flat=True)
        )

        # Procesar cada fila del DataFrame
        for _, row in df.iterrows():
            email = row['Dirección de correo electrónico']
            if email not in existing_emails:
                students_to_create.append(
                    Students(
                        name=row['Nombre'],
                        last_name=row['Apellidos'],
                        email=email,
                    )
                )

        # Guardar en la base de datos con una transacción
        with transaction.atomic():
            created_students = Students.objects.bulk_create(students_to_create)

            # Relacionar los estudiantes con la clase
            for student in created_students:
                student.class_name.add(selected_class)

        # Mensajes de éxito
        messages.success(self.request, f"Se han añadido {len(created_students)} estudiantes a la base de datos.")
        return super().form_valid(form)
    
    
# OK
class ExportStudentsExcelView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los estudiantes
            students = Students.objects.all()

            # Crear una lista para almacenar los datos que vamos a exportar
            data = []

            for student in students:
                # Obtener las asignaturas del estudiante
                class_names = student.class_name.all()
                for class_name in class_names:
                    # Obtener las habilitaciones de los estudiantes para la asignatura
                    enabled_topics = EnabledTopics.objects.filter(student=student, class_name=class_name)
                    for enabled_topic in enabled_topics:
                        data.append({
                            'ID': student.id,
                            #'RUT': '',
                            'Estudiante': student.name + " " + student.last_name,
                            'Año': class_name.stage.year,
                            'Semestre': class_name.stage.semester,
                            'Carrera': class_name.principal_class.code,
                            'Sede': 'BES',
                            'Asignatura': class_name.name,
                            'Tecnologia': enabled_topic.topic.name,
                            'Puntaje': enabled_topic.score,
                        })

            # Crear un DataFrame de Pandas con los datos
            df = pd.DataFrame(data)

            # Crear la respuesta HTTP con el archivo Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="estudiantes_habilitadores.xlsx"'

            # Guardar el DataFrame como un archivo Excel en la respuesta
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            # Agregar un mensaje de éxito para que se muestre después de la descarga
            messages.success(request, "Archivo Excel generado exitosamente.")

            # Finalmente, devolver la respuesta del archivo Excel
            return response

        except Exception as e:
            # En caso de error, agregar un mensaje de error
            messages.error(request, f"Hubo un error al generar el archivo: {str(e)}")

            # Redirigir a una página de error, por ejemplo, la lista de estudiantes
            return HttpResponseRedirect(reverse('students_list'))


# OK
class UploadEnabledTopics(FormView):
    template_name = 'core/uploadEnabledTopics.html'
    form_class = UploadEnabledTopicsForm
    success_url = reverse_lazy("core_app:upload_enabled_topics")

    def _topic_reconized(self, topic_name):
        if 'Fabricación 3D' in topic_name:
            return "Fabricación 3D"
        elif 'Representación 3D' in topic_name:
            return "Tecnologías de Inteligencia Artificial para la Representación 3D"
        elif 'Gladius' in topic_name:
            return "Robótica (Gladius Mini S)"
        elif 'JetAuto' in topic_name:
            return "Robótica (UGV  Hiwonder JetAuto)"
        elif 'Dron DJI' in topic_name:
            return "Robotica (Dron DJI Mini 3 Pro)"
        elif 'COBOT' in topic_name:
            return "Robótica (COBOT)"
        elif 'Realidad' in topic_name:
            return "Realidad Virtual y Aumentada"
        elif 'Internet de las cosas' in topic_name:
            return "Internet de las cosas"
        elif 'Machine' in topic_name:
            return "Machine Learning"
        
        return None
        
    def form_valid(self, form):
        class_id = form.cleaned_data["class_id"]
        uploaded_file = self.request.FILES['file']

        # Leer el archivo Excel
        try:
            df = pd.read_excel(uploaded_file, header=1, usecols=['Dirección de correo electrónico', 'Tareas', 'Puntos'])
        except Exception as e:
            messages.error(self.request, f"Error al leer el archivo: {e}")
            return self.form_invalid(form)
    
        # Obtener la clase seleccionada
        try:
            selected_class = ClassName.objects.get(pk=class_id.id)
        except ClassName.DoesNotExist:
            messages.error(self.request, "La clase seleccionada no existe.")
            return self.form_invalid(form)
    
        # Diccionario para almacenar la mejor nota por estudiante y tópico
        best_scores = {}

        # Iterar sobre el DataFrame
        for _, row in df.iterrows():
            email = row['Dirección de correo electrónico']
            topic_name = row['Tareas']
            score = row['Puntos'] if not pd.isna(row['Puntos']) else 0

            # Reconocer el tópico
            topic_key = self._topic_reconized(topic_name)

            if not topic_key:
                # Si el tópico no es reconocido, omitir esta fila
                continue

            # Agrupar por correo y tópico
            if (email, topic_key) not in best_scores:
                best_scores[(email, topic_key)] = score
            else:
                # Mantener solo el puntaje más alto
                best_scores[(email, topic_key)] = max(best_scores[(email, topic_key)], score)

        # Procesar los datos agrupados y actualizar la base de datos
        for (email, topic_key), score in best_scores.items():
            try:
                # Buscar el estudiante por correo
                student = Students.objects.get(email=email)
            except Students.DoesNotExist:
                messages.error(self.request, f"El estudiante con correo {email} no existe.")
                continue

            try:
                # Buscar el tópico
                topic = Topics.objects.get(name=topic_key)
            except Topics.DoesNotExist:
                messages.error(self.request, f"El tópico {topic_key} no existe.")
                continue

            try:
                # Crear o actualizar el habilitador
                enabled_topic, created = EnabledTopics.objects.update_or_create(
                    student=student,
                    class_name=selected_class,
                    topic=topic,
                    defaults={'score': score}
            )
            except Exception as e:
                messages.error(self.request, f"Error al actualizar o crear el habilitador para {email}: {e}")
                continue

        # Mensaje de éxito
        messages.success(self.request, "Archivo procesado correctamente.")
        return super().form_valid(form)
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los habilitadores para mostrar en el template
        context['enabled_topics'] = (
            EnabledTopics.objects
            .select_related('student', 'class_name', 'topic')
            .order_by('student__name', 'class_name__name')
        )
        return context
 
    

        


