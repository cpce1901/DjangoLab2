from django import forms
from apps.students.models import Students, ClassName

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "id": "floatingInput",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm",
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "id": "floatingPassword",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm",
            }
        ),
    )


class UploadStudentsForm(forms.Form):
    class_id = forms.ModelChoiceField(
        queryset=ClassName.objects.all(),
        label="Asignatura",
        help_text="Selecciona la clase a la que deseas asignar estudiantes.",
        widget=forms.Select(
            attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-2 py-2 my-2 focus:ring-2 focus:ring-blue-400 focus:outline-none',
            }
        ),
    )
        
    file = forms.FileField(
        label="Archivo Excel",
        help_text="Sube un archivo Excel que contenga los datos de los estudiantes.",
        widget=forms.FileInput(
            attrs={
                'accept': '.xls,.xlsx',
                'class': 'w-full border border-gray-300 rounded-lg px-2 py-2 my-2 focus:ring-2 focus:ring-blue-400 focus:outline-none',
            }
        ),
    )


class UploadEnabledTopicsForm(forms.Form):
    class_id = forms.ModelChoiceField(
        queryset=ClassName.objects.all(),
        label="Clase",
        help_text="Selecciona la clase a la que deseas asignar estudiantes.",
    )
        
    file = forms.FileField(
        label="Archivo Excel",
        help_text="Sube un archivo Excel que contenga los datos de los estudiantes.",
        widget=forms.FileInput(
            attrs={
                'accept': '.xls,.xlsx',
                'class': 'border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
            }
        ),
    )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'last_name', 'email', 'class_name']
        widgets = {
            'class_name': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'border border-gray-300 rounded-lg px-2 py-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'w-8/12 border border-gray-300 rounded-lg px-2 py-2 my-2 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'w-8/12 border border-gray-300 rounded-lg px-2 py-2 my-2 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'w-8/12 border border-gray-300 rounded-lg px-2 py-2 my-2 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            )
        }

    # Aseguramos que 'class_name' no sea obligatorio
    class_name = forms.ModelMultipleChoiceField(
        queryset=ClassName.objects.all(),  # Aquí se puede poner el queryset si es necesario
        required=False,  # Hacer que 'class_name' no sea obligatorio
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'px-2 py-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
        })
    )
