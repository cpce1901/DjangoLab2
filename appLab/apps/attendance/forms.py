from django import forms

class RegisterUseForm(forms.Form):
    user = forms.CharField(
        label="USUARIO",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "user",
            "placeholder": "Ingresa tu usuario",
            "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-sm"
        }),
    )