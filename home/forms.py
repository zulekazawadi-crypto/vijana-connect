from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Enrollment


class RegisterForm(UserCreationForm):
    """Sign-up form: username, email and password."""
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ApplicationForm(forms.ModelForm):
    """Details a person fills in to apply for an opportunity."""
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'education', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 4})}


class EnrollmentForm(forms.ModelForm):
    """Details a person fills in to enroll in a training."""
    class Meta:
        model = Enrollment
        fields = ['full_name', 'email', 'phone', 'education']