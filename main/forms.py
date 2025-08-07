from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials.")
            cleaned_data['user'] = user
        return cleaned_data
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
