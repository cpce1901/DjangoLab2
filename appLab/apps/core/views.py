import pandas as pd
from django.views.generic import FormView, View, CreateView
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from .forms import LoginForm, UploadStudentsForm, UploadEnabledTopicsForm, StudentForm
from apps.students.models import Students, ClassName
from apps.topics.models import Topics, EnabledTopics


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


class UploadStudents(FormView):
    template_name = 'core/uploadStudents.html'
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
    
    
    def get_context_data(self, **kwargs):
        context = super(UploadStudents, self).get_context_data(**kwargs)
        students = Students.objects.all()
        context['students'] = students
        return context


class UploadEnabledTopics(FormView):
    template_name = 'core/uploadEnabledTopics.html'
    form_class = UploadEnabledTopicsForm
    success_url = reverse_lazy("core_app:upload_enabled_topics")

    def _topic_reconized(self, topic_name):
        topic_mapping = {
            "Cuestionario - IA (Tecnologías de Inteligencia Artificial para la Representación 3D)": "Tecnologías de Inteligencia Artificial para la Representación 3D",
            "Cuestionario Habilitación - Fabricación 3D (V1)": "Fabricación 3D",
            "Cuestionario Habilitación - Fabricación 3D (V2)": "Fabricación 3D",
            "Cuestionario Habilitación- Robótica (Gladius Mini S)": "Robótica (Gladius Mini S)",
            "Cuestionario Habilitación - Realidad Virtual y Aumentada": "Realidad Virtual y Aumentada",
            "Cuestionario Habilitación - Internet de las cosas": "Internet de las cosas",
            "Cuestionario Habilitacion - Robotica (Dron DJI Mini 3 Pro) V1": "Robotica (Dron DJI Mini 3 Pro)",
            "Cuestionario Habilitacion - Robotica (Dron DJI Mini 3 Pro) V2": "Robotica (Dron DJI Mini 3 Pro)",
            "Cuestionario Habilitación - Robotica (UGV Hiwonder JetAuto) V1": "Robótica (UGV  Hiwonder JetAuto)",
            "Cuestionario Habilitación - Robotica (UGV Hiwonder JetAuto) V2": "Robótica (UGV  Hiwonder JetAuto)",
            "Cuestionario Habilitación - Robótica (COBOT)": "Robótica (COBOT)",
            "Cuestionario Habilitación IA - (Machine Learning)": "Machine Learning"
        }
        return topic_mapping.get(topic_name, None)

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
        
        # Iterar sobre el DataFrame y actualizar los habilitadores
        for _, row in df.iterrows():
            email = row['Dirección de correo electrónico']
            topic_name = row['Tareas']
            score = row['Puntos'] if not pd.isna(row['Puntos']) else 0

            try:
                # Buscar el estudiante por correo
                student = Students.objects.get(email=email)
            except Students.DoesNotExist:
                messages.error(self.request, f"El estudiante con correo {email} no existe.")
                return self.form_invalid(form)

            try:
                # Buscar el tópico
                topic = Topics.objects.get(name=self._topic_reconized(topic_name))
                print(topic)
            except Topics.DoesNotExist:
                continue

            try:
                enabled_topic, created = EnabledTopics.objects.update_or_create(
                    student=student,
                    class_name=selected_class,
                    topic=topic,
                    defaults={'score': score}
                )
            except Exception as e:
                messages.error(self.request, f"Error al actualizar o crear el habilitador: {e}")
                return self.form_invalid(form)

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
        
class StudentCreateView(CreateView):
    model = Students
    form_class = StudentForm
    template_name = 'core/create_student.html'
    success_url = reverse_lazy('core_app:student_list') 