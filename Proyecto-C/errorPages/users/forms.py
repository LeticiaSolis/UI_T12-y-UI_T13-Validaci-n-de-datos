from multiprocessing import AuthenticationError
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel', 'password1', 'password2']
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            pattern = r'^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$'
            if not re.match(pattern, email):
                raise forms.ValidationError("El correo debe seguir el formato con dominio @utez.edu.mx")
            return email

        def clean_control_number(self):
            control_number = self.cleaned_data.get('control_number')
            if not re.fullmatch(r'^[a-zA-Z0-9]{10}$', control_number):
                raise forms.ValidationError("La matricula debe tener exactamente 10 caracteres, permitiendo solo letras y números")
            return control_number

        def clean_age(self):
            age = self.cleaned_data.get('age')
            if age < 10 or age > 99:
                raise forms.ValidationError("La edad debe estar entre 10 y 99 años.")
            return age

        def clean_tel(self):
            tel = self.cleaned_data.get('tel')
            if len(str(tel)) != 10:
                raise forms.ValidationError("El número de teléfono debe tener 10 dígitos.")
            return tel

        def clean_password1(self):
            password = self.cleaned_data.get('password1')
            pattern = r'^(?=.*[A-Za-z])(?=.*[\!\#\$\%\&\?])(?=.*\d)[A-Za-z\d\!\#\$\%\&\?]{8,}$'
            if not re.match(pattern, password):
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, incluir letras, números y un carácter especial (!,#,$,%,&,?)")
            return password
        
        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            return password2


class CustomUserLoginForm(AuthenticationForm):
    email = forms.CharField(label="Correo electrónico", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
                                
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = AuthenticationError(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data
    
   