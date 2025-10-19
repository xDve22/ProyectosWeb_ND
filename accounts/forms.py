from django import forms
from django.contrib.auth.models import User
from datetime import date

from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["bio", "birth_date", "phone", "address", "city", "country"]

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if not birth_date:
            return birth_date

        today = date.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old.")
        return birth_date
