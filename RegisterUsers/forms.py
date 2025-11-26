from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User



class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre completo",
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre completo",
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "Correo electrónico",
            "class": "form-control"
        })
    )

    password1 = forms.CharField(
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "form-control"
        })
    )

    password2 = forms.CharField(
        required=True,
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repite la contraseña",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise ValidationError("Debe ingresar un nombre de usuario.")

        if username.strip() == "":
            raise ValidationError("El nombre no puede ser solo espacios.")

        if User.objects.filter(username__iexact=username.strip()).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")

        return username.strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre de usuario",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "form-control"
        })
    )