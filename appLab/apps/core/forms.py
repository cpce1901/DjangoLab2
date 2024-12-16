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
                "class": "input-field bg-gray-700 text-gray-300 focus:ring-blue-500 focus:border-blue-500",
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
                "class": "input-field bg-gray-700 text-gray-300 focus:ring-blue-500 focus:border-blue-500",
            }
        ),
    )


class UploadStudentsForm(forms.Form):
    class_id = forms.ModelChoiceField(
        queryset=ClassName.objects.all(),
        label="Clase",
        help_text="Selecciona la clase a la que deseas asignar estudiantes.",
        widget=forms.Select(
            attrs={
                'class': 'w-full bg-gray-100 border-gray-200 text-gray-800 rounded-md shadow-sm focus:ring-blue-300 focus:border-blue-300',
            }
        ),
    )
        
    file = forms.FileField(
        label="Archivo Excel",
        help_text="Sube un archivo Excel que contenga los datos de los estudiantes.",
        widget=forms.FileInput(
            attrs={
                'accept': '.xls,.xlsx',
                'class': 'w-full bg-gray-100 border-gray-200 text-gray-800 rounded-md shadow-sm focus:ring-blue-300 focus:border-blue-300',
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
                    'class': 'border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'border border-gray-300 rounded-lg p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none'
                }
            )      
        }

